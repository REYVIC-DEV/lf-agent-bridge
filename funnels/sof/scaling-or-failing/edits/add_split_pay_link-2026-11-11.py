#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Add the Whop split-pay link to the LIVE ticket card on scaling-failing.

JOSHUA, 2026-11-11: picked layout Option A (plain text link under the main
button) from the mockup, confirmed the split-pay checkout is
plan_fkxLUG1tlaOdO (2 payments of $1,498.50), and said to make it live.

The button markup (`class="sof-tbtn"`) lives in the step's `body` JSON, same
place wire_whop_link_live.py edited. The CSS for the whole page, including
every `.sof-tbtn` rule, is NOT in `body` at all -- it lives in
`settings.custom_html.header` (confirmed by reading the live step: `body`
has no `<style>` text anywhere, `settings.custom_html.header` is 127KB and
does). So this script has to patch two different fields of the same step in
one mutation: `body` for the new <p> link, `header` for its CSS.

Scoped to `scaling-failing` only -- `contact` has no ticket card, just the
promo-bar link that wire_whop_link_live.py already repointed.

    py funnels/sof/scaling-or-failing/edits/add_split_pay_link-2026-11-11.py
    py funnels/sof/scaling-or-failing/edits/add_split_pay_link-2026-11-11.py --apply
"""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", "..", "..", ".."))
sys.path.insert(0, ROOT)
os.chdir(ROOT)
import lf_api

FUNNEL = "fun_RoOL_WXDCAxK4hEk0v5xX"
STEP_SLUG = "scaling-failing"

# ---- body (markup) -------------------------------------------------------
OLD_BTN = (
    '<a class="sof-tbtn" href="https://whop.com/checkout/plan_9fd3QJCm3n9sM">'
    '<i aria-hidden="true"></i><span>SECURE YOUR SEAT  →</span></a>'
)
NEW_BTN = OLD_BTN + (
    '<p class="sof-tsplit">or <a href="https://whop.com/checkout/plan_fkxLUG1tlaOdO/">'
    'split into 2 payments of $1,498.50</a></p>'
)

# ---- header (CSS) ---------------------------------------------------------
OLD_CSS_MOBILE = (
    '.sof-tbtn span{position:absolute;left:0;right:0;top:0;height:60px;border-radius:30px;\n'
    '  background:#FCCF44;border:3px solid #041C32;display:flex;align-items:center;\n'
    '  justify-content:center;font-family:Fira Sans Condensed, Arial Narrow, sans-serif;'
    'font-weight:700;font-size:22.65px;\n'
    '  color:#041C32;line-height:1;white-space:pre}'
)
NEW_CSS_MOBILE = OLD_CSS_MOBILE + (
    '\n.sof-tsplit{text-align:center;margin:14px 0 0;'
    'font-family:Poppins, ui-sans-serif, system-ui, sans-serif;'
    'font-weight:500;font-size:14px;color:#041C32}'
    '\n.sof-tsplit a{color:#041C32;font-weight:700;text-decoration:underline}'
)

OLD_CSS_DESKTOP = (
    '.sof-tbtn span{height:104px;border-radius:52px;border-width:6px;font-size:54px;\n'
    '    letter-spacing:.01em}'
)
NEW_CSS_DESKTOP = OLD_CSS_DESKTOP + '\n  .sof-tsplit{font-size:20px;margin-top:20px}'

APPLY = "--apply" in sys.argv


def main():
    ACCT = open(".lf_account").read().strip()
    HH = lf_api.session_headers(ACCT)
    steps = lf_api.get_funnel_steps(None, FUNNEL, extra_headers=HH)["steps"]
    mine = next((s for s in steps if s["slug"] == STEP_SLUG), None)
    assert mine is not None, "step %r not found in funnel %r" % (STEP_SLUG, FUNNEL)

    def count_in_body(node, target):
        n = 0
        if isinstance(node, dict):
            for v in node.values():
                n += count_in_body(v, target)
        elif isinstance(node, list):
            for v in node:
                n += count_in_body(v, target)
        elif isinstance(node, str):
            n += node.count(target)
        return n

    btn_hits = count_in_body(mine["body"], OLD_BTN)
    assert btn_hits == 1, \
        "expected exactly 1 occurrence of the ticket button in body, found %d" % btn_hits

    header = mine["settings"]["custom_html"]["header"]
    assert header.count(OLD_CSS_MOBILE) == 1, \
        "expected exactly 1 occurrence of the mobile .sof-tbtn span rule, found %d" % \
        header.count(OLD_CSS_MOBILE)
    assert header.count(OLD_CSS_DESKTOP) == 1, \
        "expected exactly 1 occurrence of the desktop .sof-tbtn span rule, found %d" % \
        header.count(OLD_CSS_DESKTOP)

    print("scaling-failing: button match ok, mobile CSS match ok, desktop CSS match ok")

    if not APPLY:
        print("\ndry run. pass --apply to write.")
        return

    def replace_in_body(node):
        if isinstance(node, dict):
            return {k: replace_in_body(v) for k, v in node.items()}
        if isinstance(node, list):
            return [replace_in_body(v) for v in node]
        if isinstance(node, str) and OLD_BTN in node:
            return node.replace(OLD_BTN, NEW_BTN)
        return node

    new_body = replace_in_body(mine["body"])
    new_header = header.replace(OLD_CSS_MOBILE, NEW_CSS_MOBILE) \
                        .replace(OLD_CSS_DESKTOP, NEW_CSS_DESKTOP)
    new_settings = dict(mine["settings"])
    new_settings["custom_html"] = dict(mine["settings"]["custom_html"])
    new_settings["custom_html"]["header"] = new_header

    step = {
        "id": mine["id"],
        "slug": mine["slug"],
        "title": mine["title"],
        "type": mine["type"],
        "settings": new_settings,
        "visual": {"x": mine["visual"]["x"], "y": mine["visual"]["y"]},
        "body": new_body,
    }
    mutation = """
    mutation AddSplitPay($id: ID!, $node: InputFunnel!) {
      updateFunnel(id: $id, node: $node) { id steps { uid } }
    }
    """
    r = lf_api.gql(None, mutation, {"id": FUNNEL, "node": {"steps": [step]}},
                   extra_headers=HH)
    print(json.dumps(r, indent=1))


main()
