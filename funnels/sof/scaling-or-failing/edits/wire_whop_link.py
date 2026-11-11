#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Point the test page's two buy buttons straight at the real Whop checkout
link -- a plain href, nothing else.

JOSHUA, 2026-11-04: "okay we would just be using whop" ->
"https://whop.com/checkout/plan_9fd3QJCm3n9sM here is the link".

Checked before wiring anything: the link itself, in a real browser. It is
a complete, working, already-branded ("Scaling or Failing" name and logo,
pulled from Whop's own account settings, not anything this repo set up)
checkout for "SoF Full Access Pass", $2,997, one-time payment, with
Google Pay / Apple Pay / card. No quantity control anywhere on it --
confirmed by searching the rendered page's own text for the word, not
assumed from the screenshot alone.

That one fact is what simplifies everything. Every button this session
has built up to now (the cart-cookie write, the n8n fetch-and-redirect)
existed to get a shopper to a working payment page while working AROUND
Lightfunnels' own checkout. A plan with a single fixed price needs none of
that -- it is exactly the external-link pattern the real page's ticket
button already used for the Stripe link (`EB_HREF`) before any of this
session's work started. This script returns it to that pattern, just
pointed at Whop instead of the dead Stripe link.

Scoped to the sof-v3 TEST step only, same as every other change this
session made to it. The live page's buttons are untouched.

    py funnels/sof/scaling-or-failing/edits/wire_whop_link.py
    py funnels/sof/scaling-or-failing/edits/wire_whop_link.py --apply
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
STEP_SLUG = "sof-v3"
WHOP_URL = "https://whop.com/checkout/plan_9fd3QJCm3n9sM"
APPLY = "--apply" in sys.argv

OLD_PROMO = ('<a class="sof-promo" href="https://www.scalingorfailing.com/'
             'sof-checkout/checkout" onclick="document.cookie=\'lf_609354_'
             'cart=\'+encodeURIComponent(JSON.stringify({body:[{price_'
             'bundle:null,variants:[{quantity:1,id:4301675370,payment_'
             'settings:{type:null,cycle:null}}]}]}))+\';path=/\'">')
NEW_PROMO = '<a class="sof-promo" href="%s">' % WHOP_URL

OLD_TBTN = ('<a class="sof-tbtn" href="https://www.scalingorfailing.com/'
            'sof-checkout/checkout" onclick="document.cookie=\'lf_609354_'
            'cart=\'+encodeURIComponent(JSON.stringify({body:[{price_'
            'bundle:null,variants:[{quantity:1,id:4301675370,payment_'
            'settings:{type:null,cycle:null}}]}]}))+\';path=/\'">')
NEW_TBTN = '<a class="sof-tbtn" href="%s">' % WHOP_URL


def main():
    ACCT = open(".lf_account").read().strip()
    HH = lf_api.session_headers(ACCT)
    steps = lf_api.get_funnel_steps(None, FUNNEL, extra_headers=HH)["steps"]
    step = next(s for s in steps if s["slug"] == STEP_SLUG)

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

    corpus = real_text_corpus(step["body"])
    for label, old in (("promo", OLD_PROMO), ("ticket", OLD_TBTN)):
        n = corpus.count(old)
        print("%-8s found %d time(s)" % (label, n))
        assert n == 1, "%s: expected exactly 1, found %d" % (label, n)

    if not APPLY:
        print("\ndry run. pass --apply to write.")
        return

    r = lf_api.edit_step_bodies(
        None, FUNNEL, [(OLD_PROMO, NEW_PROMO), (OLD_TBTN, NEW_TBTN)],
        extra_headers=HH, step_uids=[step["uid"]], force=True)
    print(json.dumps(r, indent=1))


main()
