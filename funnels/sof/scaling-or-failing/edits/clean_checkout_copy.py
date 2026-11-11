#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Strip the Garlic/Vitruevian-specific leftovers out of the cloned checkout
body: an order bump for their own alarm-clock product, a $10.09 physical
-shipping section, a fake "00:00" urgency timer, and two copies of their
supplement trust badges ("3rd-Party Lab Tested Softgels", "150,000 Reviews").

JOSHUA, 2026-11-03: continuing "make a simple checkout for me asap".

build_simple_checkout.py already de-branded the one thing a plain substring
search could find (a logo image + its link). These five are structural, not
textual -- no amount of string replacement finds an order bump for a product
we don't sell, so each was located by walking the tree for its exact block
type (`OrderBump`, `ShippingRatesForm`) or exact copy string, then verified
by printing its full subtree before deciding it was safe to cut: every one
below is Container/Image/Text/Stars only, nothing from CheckoutSummary's own
managed children (`Repeater`, the Subtotal/Discount/Total block) and nothing
from the live Payment/Button chain, which sit as PLAIN SIBLINGS to three of
these five inside the same two parents (`CheckoutSummary` and the form
column `Container 38fe3748`) and must not be touched.

NOT removed, on purpose: three "Lorem Ipsum" placeholder blocks inside the
mobile order-summary accordion. They were never filled in on the Garlic page
either -- a pre-existing gap in a page that already takes real payments, not
something this script introduced. Low visibility (collapsed by default),
flagged here rather than guessed at under time pressure.

Run against the CHECKOUT FUNNEL's checkout step (fun_MaCLh5DOqyw_f1Viin3Z_,
step_eFWf92EsCWvQNx5OzREcH), not the Garlic funnel -- this edits OUR clone.

    py funnels/sof/scaling-or-failing/edits/clean_checkout_copy.py
    py funnels/sof/scaling-or-failing/edits/clean_checkout_copy.py --apply
"""
import io
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", "..", "..", ".."))
sys.path.insert(0, ROOT)
os.chdir(ROOT)
import lf_api

FUNNEL = "fun_MaCLh5DOqyw_f1Viin3Z_"
CHECKOUT_STEP = "step_eFWf92EsCWvQNx5OzREcH"
APPLY = "--apply" in sys.argv

# ⚠️ THE FOOTER LINKS WERE BROKEN, NOT JUST MISLABELLED -- found by actually
# reading every link's href, which is what caught it: four of the five
# ("Refund policy", "Shipping", "Privacy policy", "Terms of service") are a
# `destination: {"type":"dynamic", "value":":scheme://:host/:funnel/:step(id)"}`
# naming step ids that exist in GARLIC's funnel, not this one, so every one
# resolved to ".../sof-checkout/undefined" -- a dead link, not a wrong-brand
# one. "Contact" was worse: a STATIC link straight to
# "https://99brands1.myshopify.com/pages/contact", an entirely different,
# unrelated Shopify store. This ticket funnel has no refund/shipping/terms/
# privacy pages of its own, so the four dead ones are REMOVED rather than
# repointed at content that does not exist; Contact is repointed at the
# real, already-live SOF contact page.
FOOTER_LINK_PARENT = "f825e151-6115-43cc-bb46-4e87ffacb737"
FOOTER_LINKS_TO_DROP = [
    "d1144292-2b36-45c9-b48b-5d7507ef41af",   # Refund policy -> undefined
    "6a2e5133-9640-48a0-8391-43571a23d2c6",   # Shipping -> undefined
    "4a9a45b7-70a6-45f1-9879-82b610cdfe64",   # Privacy policy -> undefined
    "56147b93-8bdf-4030-92bf-03360b4ba79e",   # Terms of service -> undefined
]
FOOTER_CONTACT_LINK = "d08302e0-a532-4ce3-ab04-3884295342a0"
FOOTER_CONTACT_URL = "https://www.scalingorfailing.com/event/contact"

# (parent container id, [child ids to remove from it], human label)
REMOVALS = [
    ("38fe3748-48dc-43cd-aae7-3575ae47c8c0",
     ["91afa79a-1ebd-41e2-8c1b-585b06ad768f",   # "Shipping method" heading
      "bde971a3-5609-44d4-9ed8-574e50d2790a",   # the $10.09 shipping-rate form
      "1c1575d8-b822-4cb3-ba06-659a9ecb48f7"],  # trust badges, copy #1
     "form column"),
    ("27898034-4c65-4b0a-9575-0dcb8db3316a",
     ["96248dbd-209f-4503-9d28-ac509a8a19d0",   # order bump (alarm clock)
      "bcbd15bf-029d-407b-b9f9-0edefdecdab1"],  # trust badges, copy #2
     "CheckoutSummary"),
    ("4c6a4c60-d8f5-4aff-b1a9-844f11472ba5",
     ["e7110ed2-7b7e-4859-8e83-824d6180301b"],  # "reserved for: 00:00" banner
     "urgency banner wrapper"),
    ("d7803a4c-a6a2-4e91-9c6c-bcd2beef5704",
     ["0d6ff8b1-c1c5-4fda-86fb-958b126d0ac6"],  # top "+150,000 Customers" /
     # 30-Day Guarantee / Fast Shipping / Secure Checkout banner -- the THIRD
     # and last copy of these trust badges, sitting directly under the
     # page's top-level Col rather than inside either of the two containers
     # the first two copies were found in.
     "page-top trust banner"),
]


def find(n, nid):
    if isinstance(n, dict):
        if n.get("id") == nid:
            return n
        for v in n.values():
            r = find(v, nid)
            if r is not None:
                return r
    elif isinstance(n, list):
        for v in n:
            r = find(v, nid)
            if r is not None:
                return r
    return None


def main():
    ACCT = open(".lf_account").read().strip()
    HH = lf_api.session_headers(ACCT)

    n = lf_api.gql(
        None,
        """query($id:ID!){node(id:$id){... on Funnel{
             steps{uid slug title type product_id settings visual{x y} body}}}}""",
        {"id": FUNNEL}, extra_headers=HH)["node"]
    step = next(s for s in n["steps"] if s["uid"] == CHECKOUT_STEP)
    body = step["body"]
    before_size = len(json.dumps(body))

    # ⚠️ IDEMPOTENT ON PURPOSE. This script grew a fourth removal after the
    # first three were already applied once; re-running against a fresh
    # fetch means those three are already gone. A group is only an error if
    # SOME but not all of its ids are missing (a partial, inconsistent cut);
    # all-present or all-absent are both fine.
    total_removed = 0
    for parent_id, child_ids, label in REMOVALS:
        parent = find(body, parent_id)
        assert parent is not None, "parent %s (%s) not found" % (parent_id, label)
        before = len(parent["p"]["children"])
        before_ids = {c["id"] for c in parent["p"]["children"]}
        present = [c for c in child_ids if c in before_ids]
        if not present:
            print("%-22s already removed, skipping" % label)
            continue
        assert len(present) == len(child_ids), (
            "%s: partial match, only %s of %s present" % (label, present, child_ids))
        parent["p"]["children"] = [c for c in parent["p"]["children"]
                                    if c["id"] not in child_ids]
        removed = before - len(parent["p"]["children"])
        assert removed == len(child_ids), (
            "%s: removed %d, expected %d" % (label, removed, len(child_ids)))
        total_removed += removed
        print("%-22s removed %d of %d children" % (label, removed, before))

    # Footer links: drop the four that resolve to ".../undefined", repoint
    # Contact at the real SOF contact page instead of the unrelated store.
    footer = find(body, FOOTER_LINK_PARENT)
    assert footer is not None, "footer link container not found"
    before_ids = {c["id"] for c in footer["p"]["children"]}
    present = [c for c in FOOTER_LINKS_TO_DROP if c in before_ids]
    if present:
        assert len(present) == len(FOOTER_LINKS_TO_DROP), (
            "footer links: partial match, only %s present" % present)
        before = len(footer["p"]["children"])
        footer["p"]["children"] = [c for c in footer["p"]["children"]
                                    if c["id"] not in FOOTER_LINKS_TO_DROP]
        print("footer dead links    removed %d of %d children"
              % (before - len(footer["p"]["children"]), before))
        total_removed += len(FOOTER_LINKS_TO_DROP)
    else:
        print("footer dead links    already removed, skipping")

    contact = find(body, FOOTER_CONTACT_LINK)
    assert contact is not None, "footer Contact link not found"
    old_dest = contact["p"].get("destination")
    if old_dest != {"type": "static", "value": FOOTER_CONTACT_URL}:
        assert old_dest == {"type": "static", "value": "https://99brands1.myshopify.com/pages/contact"}, (
            "Contact link destination changed unexpectedly: %r" % old_dest)
        contact["p"]["destination"] = {"type": "static", "value": FOOTER_CONTACT_URL}
        print("footer Contact link  repointed to %s" % FOOTER_CONTACT_URL)
    else:
        print("footer Contact link  already repointed, skipping")

    # Post-condition: none of the five brand-specific strings, and none of
    # the broken/wrong-brand footer links, survive.
    s = json.dumps(body, ensure_ascii=False)
    for bad in ("3rd-Party Lab Tested Softgels", "150,000 Reviews",
                "reserved for: 00:00", "Bluetooth Alarm Clock",
                "Shipping Label", "99brands1.myshopify.com",
                ":step(step_QYXvCCUSxFDvjfdrcicjJ)",
                ":step(step_BibKODou_1TP5Vtp0SZnw)",
                ":step(step_l4Vj1pq-pwTonfLhquy6O)",
                ":step(step_CTSpsnYRrE3e1cph8bnce)"):
        assert bad not in s, "still present after removal: %r" % bad

    print("\n%d blocks removed, body %d -> %d bytes" % (total_removed, before_size, len(s)))

    if not APPLY:
        print("dry run. pass --apply to write.")
        return

    others = [{"id": st["uid"], "slug": st["slug"], "title": st["title"],
               "type": st["type"], "settings": st["settings"],
               "visual": st["visual"], "product_id": st.get("product_id")}
              for st in n["steps"] if st["uid"] != CHECKOUT_STEP]
    mine = {"id": CHECKOUT_STEP, "slug": step["slug"], "title": step["title"],
            "type": step["type"], "settings": step["settings"],
            "visual": step["visual"], "product_id": step.get("product_id"),
            "body": body}

    r = lf_api.gql(
        None,
        "mutation($id:ID!,$node:InputFunnel!){updateFunnel(id:$id,node:$node){"
        "id steps{uid slug}}}",
        {"id": FUNNEL, "node": {"steps": others + [mine]}}, extra_headers=HH)
    print("WROTE", json.dumps(r["updateFunnel"], indent=1))


main()
