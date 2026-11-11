#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Revert the two LIVE buttons from Whop back to the Stripe link.

JOSHUA, 2026-11-04: "make sure we are able to switch back to stripe when
needed" -- said right after the Whop link went live on scaling-failing and
contact.

This is the exact mirror of `wire_whop_link_live.py`, reversed: it does
nothing unless and until someone runs it with `--apply`. Kept as a ready,
tested-by-dry-run script rather than a note in a doc, because "switch back
when needed" means FAST, not "go re-derive the old URL from NOTES.md under
pressure". The old Stripe link is still live on Stripe's own side (only
where the BUTTON points was ever changed, never anything on Stripe) --
confirmed in the original push's own report, so pointing back at it is a
real, working revert, not a dead end.

    py funnels/sof/scaling-or-failing/edits/revert_to_stripe_live.py
    py funnels/sof/scaling-or-failing/edits/revert_to_stripe_live.py --apply
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
WHOP_URL = "https://whop.com/checkout/plan_9fd3QJCm3n9sM"
STRIPE_URL = "https://buy.stripe.com/3cIfZh0RM201aiyg01dby04"
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
        n = real_text_corpus(s["body"]).count(WHOP_URL)
        print("%-18s Whop occurrences: %d" % (s["slug"], n))
        total += n
    assert total == 3, (
        "expected 3 total (2 on scaling-failing + 1 on contact) -- got %d. "
        "If this is 0, Whop may have already been reverted; nothing to do."
        % total)

    if not APPLY:
        print("\ndry run. pass --apply to revert live to Stripe.")
        return

    r = lf_api.edit_step_bodies(
        None, FUNNEL, [(WHOP_URL, STRIPE_URL)],
        extra_headers=HH, step_uids=[s["uid"] for s in targets], force=True)
    print(json.dumps(r, indent=1))
    print("\n⚠️ reverted live -- run pagescore/verify_pages.py sof --save "
          "afterward so the baseline matches again.")


main()
