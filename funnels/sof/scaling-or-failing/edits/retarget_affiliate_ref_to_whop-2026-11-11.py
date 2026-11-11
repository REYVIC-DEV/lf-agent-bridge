#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Retarget the `?ref=` affiliate-code script from Stripe to Whop.

JOSHUA, 2026-11-11: found by testing directly in the browser that Whop's
hosted checkout DOES read a query parameter and auto-apply it -- just not
any of the names we guessed (`promo`, `code`, `coupon`, `d`,
`prefilled_promo_code`). The real one is `promoCode` (exact case), confirmed
live: `whop.com/checkout/plan_9fd3QJCm3n9sM/?promoCode=JEM` showed
$2,547.45, 15% off, with no embed and no modal -- a plain redirect link.

`wire_affiliate_ref.py` (2026-10-30) already does exactly the mechanism we
want: read `?ref=` off our own URL, clean it, and rewrite every button whose
href starts with the payment host, adding the field Whop/Stripe reads. It
was built for Stripe and never updated when checkout moved to Whop on
2026-11-04 -- confirmed still live and still matching `buy.stripe.com`,
which no button on the page has pointed at since that migration, so it has
been a dead no-op for a week.

This script is a 2-line retarget of that same installed script, not a
rewrite: `PREFIX` -> `https://whop.com/checkout/` (covers both the full-price
button/promo-bar link at plan_9fd3QJCm3n9sM and the split-pay link at
plan_fkxLUG1tlaOdO -- matched by href prefix, same as the original comment
promised: "a fourth button added later is picked up for free"), `FIELD` ->
`promoCode`. Everything else -- the `ref`-only param, the A-Z0-9_- cleaning,
sessionStorage persistence across the nav's /contact link, the
MutationObserver re-apply -- is untouched.

    py funnels/sof/scaling-or-failing/edits/retarget_affiliate_ref_to_whop-2026-11-11.py
    py funnels/sof/scaling-or-failing/edits/retarget_affiliate_ref_to_whop-2026-11-11.py --apply
"""
import io
import os
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", "..", "..", ".."))
sys.path.insert(0, ROOT)
os.chdir(ROOT)
import lf_api

FUNNEL = "fun_RoOL_WXDCAxK4hEk0v5xX"
MARK = "sof-affiliate-ref"

OLD_PREFIX = "var PREFIX = 'https://buy.stripe.com/';"
NEW_PREFIX = "var PREFIX = 'https://whop.com/checkout/';"
OLD_FIELD = "prefilled_promo_code"
NEW_FIELD = "promoCode"

Q = """
query HS($q: String!) {
  funnels(first: 1, query: $q) { edges { node { id header_scripts } } }
}
"""
MUT = """
mutation SetHS($id: ID!, $node: InputFunnel!) {
  updateFunnel(id: $id, node: $node) { id }
}
"""

APPLY = "--apply" in sys.argv


def main():
    ACCT = open(".lf_account").read().strip()
    HH = lf_api.session_headers(ACCT)
    edges = lf_api.gql(None, Q, {"q": "id:%s" % FUNNEL}, extra_headers=HH)["funnels"]["edges"]
    assert edges, "funnel not found"
    cur = edges[0]["node"].get("header_scripts") or ""

    assert MARK in cur, "marker %r not found -- wire_affiliate_ref.py script is not installed" % MARK
    prefix_hits = cur.count(OLD_PREFIX)
    field_hits = cur.count(OLD_FIELD)
    assert prefix_hits == 1, "expected 1 occurrence of the Stripe PREFIX line, found %d" % prefix_hits
    assert field_hits == 2, "expected 2 occurrences of %r (declaration + comment), found %d" % (OLD_FIELD, field_hits)
    assert "whop.com" not in cur, "header_scripts already mentions whop.com -- check before overwriting"

    print("affiliate-ref script found, Stripe PREFIX found once, %r found twice" % OLD_FIELD)

    if not APPLY:
        print("\ndry run. pass --apply to write.")
        return

    bak = os.path.join(HERE, "..", "header_scripts.pre-whop-retarget-2026-11-11.html")
    bak = os.path.abspath(bak)
    with io.open(bak, "w", encoding="utf-8", newline="") as fh:
        fh.write(cur)
    print("backup -> %s" % os.path.relpath(bak, ROOT))

    new = cur.replace(OLD_PREFIX, NEW_PREFIX).replace(OLD_FIELD, NEW_FIELD)
    assert new.count(MARK) == 1
    assert new.count("whop.com/checkout/") == 1
    assert new.count(NEW_FIELD) == 2
    assert OLD_PREFIX not in new and OLD_FIELD not in new

    lf_api.gql(None, MUT, {"id": FUNNEL, "node": {"header_scripts": new}}, extra_headers=HH)
    back = lf_api.gql(None, Q, {"q": "id:%s" % FUNNEL}, extra_headers=HH)["funnels"]["edges"][0]["node"].get("header_scripts") or ""
    assert back == new, "read-back differs from what was sent"
    print("header_scripts written and read back identical: %d -> %d chars" % (len(cur), len(new)))


main()
