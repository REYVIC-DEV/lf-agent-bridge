#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Push the Whop checkout link to the LIVE site -- scaling-failing and
contact, the two real steps, not the sof-v3 test clone.

JOSHUA, 2026-11-04: "please push to real site", after confirming the Whop
link works end to end on the test clone (wire_whop_link.py).

Checked before writing anything: BOTH live steps still carry the dead
Stripe link (`EB_HREF`), as a plain href with no onclick -- the
cart-cookie JS from the abandoned LF-checkout plan was only ever applied
to the sof-v3 test step, never to these two. So this is a pure href swap,
simpler than the test-page version needed (nothing to strip out).

    scaling-failing  2 occurrences -- the promo bar AND the ticket button
    contact          1 occurrence -- the promo bar only (no ticket card
                     on the contact page)

    py funnels/sof/scaling-or-failing/edits/wire_whop_link_live.py
    py funnels/sof/scaling-or-failing/edits/wire_whop_link_live.py --apply
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
STEP_SLUGS = ["scaling-failing", "contact"]
OLD_HREF = "https://buy.stripe.com/3cIfZh0RM201aiyg01dby04"
WHOP_URL = "https://whop.com/checkout/plan_9fd3QJCm3n9sM"
APPLY = "--apply" in sys.argv


def real_text_corpus(body):
    chunks = []

    def walk(n):
        if isinstance(n, dict):
            c = n.get("content")
            if isinstance(c, str):
                chunks.append(c)
            for v in n.values():
                walk(v)
        elif isinstance(n, list):
            for v in n:
                walk(v)
    walk(body)
    return "\n".join(chunks)


def main():
    ACCT = open(".lf_account").read().strip()
    HH = lf_api.session_headers(ACCT)
    steps = lf_api.get_funnel_steps(None, FUNNEL, extra_headers=HH)["steps"]
    targets = [s for s in steps if s["slug"] in STEP_SLUGS]
    assert len(targets) == len(STEP_SLUGS), \
        "expected steps %s, found %s" % (STEP_SLUGS, [s["slug"] for s in targets])

    total = 0
    for s in targets:
        n = real_text_corpus(s["body"]).count(OLD_HREF)
        print("%-18s occurrences: %d" % (s["slug"], n))
        total += n
    assert total == 3, "expected 3 total (2 + 1), found %d" % total

    if not APPLY:
        print("\ndry run. pass --apply to write.")
        return

    r = lf_api.edit_step_bodies(
        None, FUNNEL, [(OLD_HREF, WHOP_URL)],
        extra_headers=HH, step_uids=[s["uid"] for s in targets], force=True)
    print(json.dumps(r, indent=1))


main()
