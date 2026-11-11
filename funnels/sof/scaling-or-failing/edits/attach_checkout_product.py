#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Attach the Full Access Pass product to the existing (empty) checkout step,
and give it a real slug.

JOSHUA, 2026-11-03: "there is a checkout step on the SOF funnel make a simple
checkout for me asap our stripe got held so we need this".

WHAT WAS FOUND BEFORE WRITING ANYTHING

  - The funnel already carries a `checkout_page` step (uid
    step_IYG7F03bG5X3nHZKbetnP), created at some earlier point, empty body,
    auto-generated slug `_f7tcJ5FS`, NO product attached.
  - The funnel's active payment gateway is NOT Stripe. It is
    `pg_eZsF6TBLT4dKdQBj3d70t`, identifier "Airwallex: Tholding Limited",
    active + platform_active, live (not test). So this checkout does not
    depend on the held Stripe account at all -- it is a separate rail that
    was already wired in, just never used.
  - The account's product catalog (queried via `products`) has nothing for
    SOF: every ticket sale so far went through an external Stripe Payment
    Link (EB_HREF), never through an LF product. So there is no ticket
    product to reuse; one has to be created.
  - `checkout_page`'s body is NOT hand-authored HTML like the article pages
    this repo usually builds. It is a fixed LF template: the schema exposes
    `Checkout`/`OrderSummary` query types for it, not a block/component tree,
    and empty `body.p.children: []` is what a normal, working checkout_page
    step actually looks like before a product is attached. Setting
    `product_id` is what turns it on.

THE PRODUCT, created separately via createProduct (prod_2BrK1IFKYkRFeSIeDgFj7):
  title   "Scaling or Failing 2026 -- Full Access Pass"
  price   $2997 digital_product, one variant, no shipping
  -- matches the live ticket card exactly (949:1458 / 949:1459), so no new
  pricing decision was made here.

THIS SCRIPT only touches the checkout step: sets its product_id, gives it the
slug `checkout` instead of the auto-generated id, and a title that will not
read as a CMS placeholder if it ever appears in a tab or a receipt. Every
sibling step is echoed back with ITS OWN stored fields untouched, same
pattern as every other SOF edit script -- updateFunnel validates every step
in the list, so a sibling missing `settings` fails the whole write.

    py funnels/sof/scaling-or-failing/edits/attach_checkout_product.py
    py funnels/sof/scaling-or-failing/edits/attach_checkout_product.py --apply
"""
import io
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.abspath(os.path.join(HERE, "..", "..", "..", "..")))
os.chdir(os.path.abspath(os.path.join(HERE, "..", "..", "..", "..")))
import lf_api

FUNNEL = "fun_RoOL_WXDCAxK4hEk0v5xX"
CHECKOUT_STEP = "step_IYG7F03bG5X3nHZKbetnP"
PRODUCT = "prod_2BrK1IFKYkRFeSIeDgFj7"
NEW_SLUG = "checkout"
NEW_TITLE = "Secure Your Seat — Scaling or Failing"
APPLY = "--apply" in sys.argv

ACCT = open(".lf_account").read().strip()
HH = lf_api.session_headers(ACCT)

n = lf_api.gql(
    None,
    """query($id:ID!){node(id:$id){... on Funnel{
         id published starting_step_id
         steps{uid slug title type product_id settings
               visual{x y}}}}}""",
    {"id": FUNNEL}, extra_headers=HH)["node"]

mine = next(s for s in n["steps"] if s["uid"] == CHECKOUT_STEP)
assert mine["type"] == "checkout_page"
assert not mine.get("product_id"), (
    "checkout step already has product_id=%r -- this script is for the "
    "FIRST attach only; re-running it would silently replace a product "
    "that already went live" % mine.get("product_id"))

others = [{"id": s["uid"], "slug": s["slug"], "title": s["title"],
           "type": s["type"], "settings": s["settings"], "visual": s["visual"]}
          for s in n["steps"] if s["uid"] != CHECKOUT_STEP]
mine_out = {"id": CHECKOUT_STEP, "slug": NEW_SLUG, "title": NEW_TITLE,
            "type": "checkout_page", "settings": mine["settings"],
            "visual": mine["visual"], "product_id": PRODUCT}

print("BEFORE: slug=%r title=%r product_id=%r" % (
    mine["slug"], mine["title"], mine.get("product_id")))
print("AFTER:  slug=%r title=%r product_id=%r" % (
    mine_out["slug"], mine_out["title"], mine_out["product_id"]))
print("siblings echoed untouched: %s" % [o["slug"] for o in others])

if not APPLY:
    print("\ndry run. pass --apply to write.")
    sys.exit(0)

r = lf_api.gql(
    None,
    "mutation($id:ID!,$node:InputFunnel!){updateFunnel(id:$id,node:$node){"
    "id steps{uid slug title type product_id}}}",
    {"id": FUNNEL, "node": {"steps": others + [mine_out]}},
    extra_headers=HH)
print("\nWROTE", json.dumps(r["updateFunnel"], indent=1))
