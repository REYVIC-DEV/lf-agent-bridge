#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Mirror the live Stripe discount codes onto the Lightfunnels checkout.

JOSHUA, 2026-11-03: pasted
`N8N/documentation/stripe-discount-codes-2026-11-03.md` then "setup the
discount codes on LF".

WHAT THIS MIRRORS, FROM THAT SNAPSHOT

  39 codes behind "Speaker 15% discount" (e2BVLWG0): 15% off, one-time
  duration, no redemption cap, no product restriction in Stripe. One of
  the 39, TOPIHEINONEN, is already deactivated and unused there -- created
  here too, but `active=False`, to keep the mirror honest rather than
  silently dropping a row.

  TOPI1000 (NICP6tS8): $1,000 off, no cap, no expiry. Flagged in the
  source doc as a real risk (unlimited $1,000 off a $2,997 ticket,
  forever) -- Joshua's call, asked directly: replicate as-is, no cap added.

  OCTBKK50 (FqqzKA41): $50 off, max redemptions 2, unused, possibly
  orphaned (named for a BKK private-event product already removed from
  this account). Asked directly: create it anyway.

  NOT mirrored: the 6 codes behind "Free - Test" (0i0kNite, 100% off).
  Every one is already deactivated in Stripe; there is no live code there
  to mirror, only a history of test/comp orders.

⚠️ EVERY CODE HERE IS SCOPED TO THIS ONE PRODUCT
(`products_ids: ["prod_p4MkRss_YruVzCqlVb5z8"]`, SoF General Admission),
which the source doc flags as a GAP in the Stripe setup: none of the 5
Stripe coupons has a product restriction, so a code meant for the SoF
ticket also works on the $15,000 consulting calls, the $10,000 mentorship
packages, anything else on that Stripe account. Lightfunnels supports the
restriction Stripe doesn't have here, and this checkout sells exactly one
product, so there is no reason not to use it.

⚠️ `one_time_usage_per_customer` is FALSE for every code below, on purpose.
Stripe shows no per-customer restriction on any of these 5 coupons, so
adding one here would be inventing a restriction the source never had --
not a faithful mirror. If a per-customer cap is wanted later, that is a
deliberate change to make, not something to default into silently.

    py funnels/sof/scaling-or-failing/edits/setup_discounts.py
    py funnels/sof/scaling-or-failing/edits/setup_discounts.py --apply
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

PRODUCT_ID = "prod_p4MkRss_YruVzCqlVb5z8"   # SoF General Admission
APPLY = "--apply" in sys.argv

# ---- 15% speaker codes (coupon e2BVLWG0), active unless noted -------------
SPEAKER_CODES = [
    "VICTOR15", "SOPHIA15", "SHAWNHE15", "AIRA15", "STEVEE15", "MERT15",
    "KEVIN15", "LUCAS15", "SF15", "STEVE15", "TOPIHEINONEN7WOW", "JEROEN15",
    "BOBBY15", "DARA15", "ALEX15", "OUTCRAFT15", "ELINE15", "NICO15",
    "BESTFULFILL15", "BANGKOKM15", "SANTERI15", "SEB15", "JOOHAN15",
    "DAVID15", "PARSA15", "KNJ15", "UGIS15", "MATTEO15", "MARLON15",
    "BESTFULFILL", "BARRY", "DEE", "RONAK", "JOSHUA", "AMPIFIRE", "JEM",
    "PHIL", "GONZALO", "ELINEAQUINO", "TOPI",
]
INACTIVE_SPEAKER_CODES = {"TOPIHEINONEN"}   # deactivated, unused, in Stripe too

ALL_CODES = []
for code in SPEAKER_CODES:
    ALL_CODES.append({
        "code": code, "type": "percentage", "value": 15,
        "active": True, "limited_usage": False, "usage_limit": 0,
        "one_time_usage_per_customer": False, "products_ids": [PRODUCT_ID],
    })
for code in INACTIVE_SPEAKER_CODES:
    ALL_CODES.append({
        "code": code, "type": "percentage", "value": 15,
        "active": False, "limited_usage": False, "usage_limit": 0,
        "one_time_usage_per_customer": False, "products_ids": [PRODUCT_ID],
    })

ALL_CODES.append({
    "code": "TOPI1000", "type": "fixed", "value": 1000,
    "active": True, "limited_usage": False, "usage_limit": 0,
    "one_time_usage_per_customer": False, "products_ids": [PRODUCT_ID],
})
ALL_CODES.append({
    "code": "OCTBKK50", "type": "fixed", "value": 50,
    "active": True, "limited_usage": True, "usage_limit": 2,
    "one_time_usage_per_customer": False, "products_ids": [PRODUCT_ID],
})

# ⚠️ The source doc's own prose says "39 rows"; its ACTUAL table has 41
# (counted directly from the markdown, not by eye -- see the dry run this
# produced before the assertion was corrected to match). Trusting the real
# table over the doc's own stale parenthetical.
assert len(ALL_CODES) == 41 + 2, "expected 43 codes (41 speaker-table rows + TOPI1000 + OCTBKK50), got %d" % len(ALL_CODES)
assert len(set(c["code"] for c in ALL_CODES)) == len(ALL_CODES), "duplicate code in the list"


def main():
    ACCT = open(".lf_account").read().strip()
    HH = lf_api.session_headers(ACCT)

    existing = lf_api.gql(
        None, 'query{ discounts(first:200, query:""){ edges { node { code } } } }',
        extra_headers=HH)["discounts"]["edges"]
    existing_codes = {e["node"]["code"] for e in existing}

    todo = [c for c in ALL_CODES if c["code"] not in existing_codes]
    skip = [c["code"] for c in ALL_CODES if c["code"] in existing_codes]
    if skip:
        print("already exist, skipping: %s" % ", ".join(skip))
    print("to create: %d" % len(todo))
    for c in todo:
        print("  %-18s %-10s %5s%s  active=%-5s cap=%s"
              % (c["code"], c["type"], c["value"],
                 "%" if c["type"] == "percentage" else "",
                 c["active"], c["usage_limit"] if c["limited_usage"] else "none"))

    if not APPLY:
        print("\ndry run. pass --apply to write.")
        return

    mutation = """mutation($node: InputDiscount!) {
        createDiscount(input: {node: $node}) { node { id code } }
    }"""
    created = []
    for c in todo:
        r = lf_api.gql(None, mutation, {"node": c}, extra_headers=HH)
        created.append(r["createDiscount"]["node"])
    print("\ncreated %d:" % len(created))
    for n in created:
        print("  ", n)


main()
