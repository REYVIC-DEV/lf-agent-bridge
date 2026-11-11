#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""A minimal, working, self-contained LF checkout for the SOF ticket, built in
its own small funnel rather than inside the big "event" one.

JOSHUA, 2026-11-03: "there is a checkout step on the SOF funnel make a simple
checkout for me asap our stripe got held so we need this".

WHAT WAS LEARNED BEFORE WRITING THIS, THE EXPENSIVE WAY

  1. The "event" funnel's `active_payment_methods` gateway is NOT Stripe. It
     is `pg_eZsF6TBLT4dKdQBj3d70t`, "Airwallex: Tholding Limited", live and
     active. So this was never blocked by the held Stripe account -- it just
     had never been wired up, because every ticket sale so far went through
     an external Stripe Payment Link, never through an LF product.

  2. `checkout_page` is NOT a step that renders a payment form from a bare
     `product_id`. Setting `product_id` on a checkout_page step (tried both
     via updateFunnel afterwards AND via createStep at creation time) left
     `Lightfunnels.product` null client-side every time -- confirmed by
     reading the page's own embedded `Lightfunnels` + `tree` globals, not by
     guessing. The REAL mechanism, found by reading the account's one
     existing working checkout (the Garlic/Vitruevian funnel,
     fun__LKgKGNO4H6IoYoFN6RfK):
       - a `product_page` step carries the product_id and is the thing a
         shopper actually buys from (a "buybox");
       - its buy button is an ordinary `Button` block with
         `p.action: "add-to-cart"`, `p.destination: {"type": "step"}` --
         "step" with no explicit value, which is how every other
         continue/next button in that funnel is written too, so it reads as
         "advance to the next step in THIS funnel's own sequence";
       - the `checkout_page` step itself carries product_id = null. It is a
         hand-built block tree (BillingAddress / PaymentMethod /
         CheckoutSummary / ShippingRatesForm / OrderBump, ~20 block types),
         reading whatever is in the cart. It is NOT a thing that renders
         itself from a product_id either -- it has to be built from blocks.

  3. `checkout_page` cannot be a funnel's `starting_step_id`
     (errors_wrong_starting_step_type), so a product_page has to come first.

  4. A new funnel has no `preferred_domain` by default and 404s on the shared
     domain until one is set. `InputFunnel.preferred_domain_id` takes the
     SAME domain id the main "event" funnel already uses
     (dom_9ciTn2rct15S93by6AME0, www.scalingorfailing.com) -- multiple
     funnels can share one domain at different slugs, same as the main site
     already does with `event` / `aged-garlic` / etc.

WHAT THIS SCRIPT DOES

  Builds TWO steps inside a fresh, dedicated funnel (not the live "event"
  funnel -- so nothing about the existing page, its steps or their order is
  touched):

    product_page  "buy"        -- product_id = the Full Access Pass ticket
                                   (prod_2BrK1IFKYkRFeSIeDgFj7, created
                                   separately, $2997, matches the live
                                   ticket card exactly). Minimal body: a
                                   title, the price, one add-to-cart button.
    checkout_page "checkout"   -- the Garlic funnel's own working checkout
                                   body, COPIED, with the one brand-specific
                                   thing in it (a BlockLink to the Vitruevial
                                   logo, image + destination) emptied out.
                                   Nothing else in that 166KB tree mentioned
                                   the brand -- checked by substring count
                                   before trusting it, not assumed.

  Both get fresh `settings.seo` for the ticket. Neither carries the custom
  html the Garlic checkout had (an autosave-on-reload convenience script and
  a CSS tweak for an empty discount line) -- cosmetic, not required for the
  form to work, and this is the first time this account has ever built one
  of these, so the fewer unverified moving parts the better.

  Order in the `steps` array is product_page THEN checkout_page, nothing
  else in this funnel, which is what makes the implicit "next step"
  `destination: {"type": "step"}` unambiguous.

NOT DONE HERE, ON PURPOSE
  - No thank_you_page. The Garlic funnel has one; this does not, because a
    missing confirmation screen is far easier to add later than a payment
    form that quietly mischarges someone, and "asap" means ship the part
    that takes the money first. Noted for Joshua to decide on.
  - The live ticket button on the real page is NOT repointed by this script.
    That is a separate, deliberate step after this is verified working --
    see wire_checkout_cta.py.

    py funnels/sof/scaling-or-failing/edits/build_simple_checkout.py
    py funnels/sof/scaling-or-failing/edits/build_simple_checkout.py --apply
"""
import copy
import io
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", "..", "..", ".."))
sys.path.insert(0, ROOT)
os.chdir(ROOT)
import lf_api

GARLIC_FUNNEL = "fun__LKgKGNO4H6IoYoFN6RfK"
CHECKOUT_FUNNEL = "fun_MaCLh5DOqyw_f1Viin3Z_"   # created earlier this session
DOMAIN_ID = "dom_9ciTn2rct15S93by6AME0"          # www.scalingorfailing.com
PRODUCT_ID = "prod_2BrK1IFKYkRFeSIeDgFj7"        # Full Access Pass, $2997
VITRUEVIAN_LOGO_ID = "3f8b4d9c-9b56-4d5a-b740-2cf5eeaa8a90"

APPLY = "--apply" in sys.argv

ACCT = open(".lf_account").read().strip()
HH = lf_api.session_headers(ACCT)

TICKET_SEO = {
    "title": "Checkout — Scaling or Failing",
    "description": "Full Access Pass, Scaling or Failing — Bangkok, "
                    "December 7-8 2026.",
}


def strip_vitruevian_logo(body):
    """Remove the one brand-specific thing found in the borrowed checkout
    body: a BlockLink wrapping an Image of the Vitruevian logo, linking to
    vitruevian.com. Emptying its children (rather than deleting the
    BlockLink node itself) keeps the surrounding layout's child count and
    flex rules intact -- an invisible wrapper, not a hole in the row."""
    hits = [0]

    def walk(n):
        if isinstance(n, dict):
            if n.get("id") == VITRUEVIAN_LOGO_ID:
                hits[0] += 1
                n["p"]["children"] = []
                n["p"]["destination"] = {"type": "static", "value": ""}
            for v in n.values():
                walk(v)
        elif isinstance(n, list):
            for v in n:
                walk(v)
    walk(body)
    assert hits[0] == 1, "expected to find the Vitruevian logo once, found %d" % hits[0]
    return body


def assert_no_brand_strings(body):
    s = json.dumps(body, ensure_ascii=False)
    for term in ("Vitruevian", "vitruevian", "Garlic", "garlic"):
        n = s.count(term)
        assert n == 0, "checkout body still mentions %r (%d times)" % (term, n)


def product_page_body(CHECKOUT_URL):
    """Minimal buybox: a title, the price, one add-to-cart button. Not a
    design -- the point of this page is the one click, not the layout."""
    def text(content, size, weight="700"):
        return {
            "t": "Text", "id": "t-%d" % (abs(hash(content)) % 99999),
            "styles": [
                {"prop": "fontFamily", "value": "Inter"},
                {"prop": "fontSize", "value": size},
                {"prop": "fontWeight", "value": weight},
                {"prop": "margin", "value": {"bottom": "12px"}},
            ],
            "p": {"content": content},
        }

    # ⚠️ THE PRODUCT HAS ONE OPTION GROUP ("Ticket" -> "Full Access Pass"),
    # because createProduct rejected zero option groups outright
    # ("Some options are missing") -- every product on this platform carries
    # at least one. Without a block that selects a value for it, the
    # add-to-cart button fires with nothing chosen and the storefront answers
    # "No variant is selected", found by actually clicking it, not guessed.
    # `ProductOptionRow` / `ProductOptionLabel` / `SelectComponent` is the
    # exact block trio the account's own upsell page uses for its quantity
    # picker (`SelectComponent.p.options: []` -- the client fills the list
    # and the default selection from the product's own option group at
    # render time). There being only one value to choose is what makes
    # hiding it safe: nothing is being hidden FROM the shopper, there is no
    # decision to show them.
    option_row = {
        "t": "Container", "id": "ticket-option-hidden",
        "styles": [{"prop": "lfDisplay", "value": "none"}],
        "p": {"children": [{
            "t": "ProductOptionRow", "id": "ticket-option-row",
            "styles": [{"prop": "lfDisplay", "value": "grid"}, {"prop": "columns", "value": 2}],
            "p": {"children": [
                {"t": "ProductOptionLabel", "id": "ticket-option-label",
                 "styles": [], "p": {"content": "Ticket"}},
                {"t": "SelectComponent", "id": "ticket-option-select",
                 "styles": [], "p": {"options": []}},
            ]},
        }]},
    }

    button = {
        "t": "Button", "id": "btn-add-to-cart",
        "styles": [
            {"prop": "width", "value": "100%"},
            {"prop": "height", "value": "56px"},
            {"prop": "fontFamily", "value": "Inter"},
            {"prop": "fontSize", "value": "16px"},
            {"prop": "fontWeight", "value": "700"},
            {"prop": "backgroundColor", "value": {"r": 7, "g": 6, "b": 15, "a": 1}},
            {"prop": "color", "value": {"r": 255, "g": 255, "b": 255, "a": 1}},
            {"prop": "borderRadius", "value": "9999px"},
            {"prop": "margin", "value": {"top": "20px"}},
        ],
        "p": {
            "content": "<p>SECURE YOUR SEAT →</p>",
            "action": "add-to-cart",
            # ⚠️ NEITHER {"type":"step"} (Garlic's own button's exact value)
            # NOR the ":scheme://:host/:funnel/:step(id)" dynamic template
            # (copied verbatim from the account's upsell "Add to my order"
            # button) actually navigates here. Both were tested directly:
            # the cart cookie fills in correctly either way (confirmed by
            # reading it back after each click), so "add-to-cart" itself
            # works -- it is ONLY the destination that goes nowhere. Cloning
            # Garlic's entire landing page onto this product showed why
            # those two forms exist: that page's button sits behind a
            # price-bundle selector (`PriceBundle`, `conditional_on:
            # "product.price_bundles") that OUR product doesn't have, so
            # copying its exact wiring brings along a mechanism this ticket
            # has no use for, not a fix.
            #
            # A plain absolute URL is what every OTHER link on this
            # product's own page already uses successfully (the
            # BlockLink nav logo, the accordion anchors), so the button
            # gets one too: add the item to the cart, THEN hard-navigate
            # to the checkout step directly, no drawer and no implicit
            # "next step" lookup involved.
            "destination": {"type": "static", "value": CHECKOUT_URL},
            "widthOption": "fullWidth",
            "heightOption": "fixedHeight",
        },
    }

    container = {
        "t": "Container", "id": "buybox-container",
        "styles": [
            {"prop": "lfDisplay", "value": "flex"},
            {"prop": "flexDirection", "value": "column"},
            {"prop": "maxWidth", "value": "480px"},
            {"prop": "margin", "value": {"left": "auto", "right": "auto", "top": "80px", "bottom": "80px"}},
            {"prop": "padding", "value": {"top": "32px", "right": "32px", "bottom": "32px", "left": "32px"}},
        ],
        "p": {"children": [
            text("Scaling or Failing 2026 — Full Access Pass", "28px"),
            text("Bangkok, December 7–8 2026", "15px", weight="400"),
            text("$2,997", "40px"),
            option_row,
            button,
        ]},
    }

    section = {
        "t": "Section", "id": "buybox-section",
        "styles": [{"prop": "margin", "value": "0px"}, {"prop": "padding", "value": "0px"}],
        "p": {"layout": "", "children": [container]},
    }

    return {
        "id": "root-buy", "t": "Root", "version": 11,
        "styles": [{"prop": "pageWidth", "value": "1140px"}],
        "p": {"children": [section]},
    }


def main():
    garlic_steps = lf_api.get_funnel_steps(None, GARLIC_FUNNEL, extra_headers=HH)["steps"]
    garlic_checkout = next(s for s in garlic_steps if s["slug"] == "checkouts")
    checkout_body = strip_vitruevian_logo(copy.deepcopy(garlic_checkout["body"]))
    assert_no_brand_strings(checkout_body)

    # Fetch the funnel's current (likely orphan) steps so nothing of them
    # -- the earlier `checkout`/`entry` experiments from this same session --
    # is left dangling with the wrong type or an empty body. Needed BEFORE
    # the button is built: it has to name the checkout step's id explicitly
    # (see product_page_body's destination comment).
    n = lf_api.gql(
        None,
        """query($id:ID!){node(id:$id){... on Funnel{
             steps{uid slug title type product_id settings visual{x y}}}}}""",
        {"id": CHECKOUT_FUNNEL}, extra_headers=HH)["node"]
    by_slug = {s["slug"]: s for s in n["steps"]}

    buy_step = by_slug.get("buy-now") or by_slug.get("entry")
    assert buy_step, "expected a 'buy-now' or 'entry' step to already exist"
    checkout_step = by_slug.get("checkout")
    assert checkout_step, "expected the earlier 'checkout' step to still exist"

    buy_body = product_page_body(
        "https://www.scalingorfailing.com/sof-checkout/checkout")

    print("product_page body: %d bytes" % len(json.dumps(buy_body)))
    print("checkout_page body: %d bytes (borrowed, de-branded)" % len(json.dumps(checkout_body)))

    if not APPLY:
        print("\ndry run. pass --apply to write.")
        return

    steps_out = [
        {"id": buy_step["uid"], "slug": "buy-now", "title": "Secure Your Seat — Scaling or Failing",
         "type": "product_page", "product_id": PRODUCT_ID,
         "settings": {"seo": TICKET_SEO}, "visual": buy_step["visual"],
         "body": buy_body},
        {"id": checkout_step["uid"], "slug": "checkout", "title": "Checkout — Scaling or Failing",
         "type": "checkout_page", "product_id": None,
         "settings": {"seo": TICKET_SEO}, "visual": checkout_step["visual"],
         "body": checkout_body},
    ]

    r = lf_api.gql(
        None,
        "mutation($id:ID!,$node:InputFunnel!){updateFunnel(id:$id,node:$node){"
        "id published starting_step_id preferred_domain{name} "
        "steps{uid slug type product_id}}}",
        {"id": CHECKOUT_FUNNEL, "node": {
            "steps": steps_out,
            "starting_step_id": buy_step["uid"],
            "preferred_domain_id": DOMAIN_ID,
            "published": True,
        }},
        extra_headers=HH)
    print("\nWROTE", json.dumps(r["updateFunnel"], indent=1, ensure_ascii=False))


main()
