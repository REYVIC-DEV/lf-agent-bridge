#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""A SECOND buybox step, pointed at Joshua's own product, for testing
alongside the one already verified working -- not a replacement of it.

JOSHUA, 2026-11-03: "change product to the one i created", then "make the
dummy step so we can test first".

His product: `prod_p4MkRss_YruVzCqlVb5z8`, "SoF General Admission", $2,997,
digital_product, one real uploaded image, but -- checked before writing
anything -- **zero option groups and zero variants**:

    options: []
    variants: []

That is the opposite of `prod_2BrK1IFKYkRFeSIeDgFj7` (the one built earlier
this session), which NEEDED one option group because `createProduct`
rejected a bare `options: []` outright ("Some options are missing"). Created
through the dashboard UI rather than the API, this one apparently doesn't
hit that rule, or the UI fills in something the API call didn't. Whether
the storefront still needs an explicit variant-selector block to avoid the
earlier "No variant is selected" error, for a product that has no variants
at all, is exactly what this test step is for -- built WITHOUT that hidden
selector first, since there is nothing here for it to select between.

Lives in the SAME test funnel as the verified one (fun_MaCLh5DOqyw_f1Viin3Z_,
sof-checkout), as a new step, slug `buy-test`:

    https://www.scalingorfailing.com/sof-checkout/buy-test

Reuses the ALREADY-VERIFIED checkout step as its destination -- checkout
reads whatever is in the cart, it was never specific to one product, so
there is no reason to duplicate it for this test.

    py funnels/sof/scaling-or-failing/edits/add_test_buy_step.py
    py funnels/sof/scaling-or-failing/edits/add_test_buy_step.py --apply
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

CHECKOUT_FUNNEL = "fun_MaCLh5DOqyw_f1Viin3Z_"
PRODUCT_ID = "prod_p4MkRss_YruVzCqlVb5z8"      # SoF General Admission, $2,997
CHECKOUT_URL = "https://www.scalingorfailing.com/sof-checkout/checkout"
IMAGE_PATH = ("https://assets.lightfunnels.com/account-90380/images_library/"
              "52e02c2e-5a33-48e2-af68-7f7010d89b00._5dGZ_Nl-HGsVJlNnoUXb.webp")
APPLY = "--apply" in sys.argv


def product_page_body():
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

    image = {
        "t": "Image", "id": "buy-test-image",
        "styles": [
            {"prop": "width", "value": "100%"},
            {"prop": "maxWidth", "value": "320px"},
            {"prop": "borderRadius", "value": "12px"},
            {"prop": "margin", "value": {"bottom": "20px"}},
        ],
        "p": {"src": IMAGE_PATH, "alt": "SoF General Admission"},
    }

    button = {
        "t": "Button", "id": "btn-add-to-cart-test",
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
            "content": "<p>SECURE YOUR SEAT (TEST) →</p>",
            "action": "add-to-cart",
            # Verified working pattern from the other buy page: plain static
            # link, no destination-swallowing by the add-to-cart handler.
            "destination": {"type": "static", "value": CHECKOUT_URL},
            "widthOption": "fullWidth",
            "heightOption": "fixedHeight",
        },
    }

    container = {
        "t": "Container", "id": "buybox-container-test",
        "styles": [
            {"prop": "lfDisplay", "value": "flex"},
            {"prop": "flexDirection", "value": "column"},
            {"prop": "alignItems", "value": "center"},
            {"prop": "maxWidth", "value": "480px"},
            {"prop": "margin", "value": {"left": "auto", "right": "auto", "top": "80px", "bottom": "80px"}},
            {"prop": "padding", "value": {"top": "32px", "right": "32px", "bottom": "32px", "left": "32px"}},
        ],
        "p": {"children": [
            image,
            text("SoF General Admission (TEST PRODUCT)", "28px"),
            text("Bangkok, December 7–8 2026", "15px", weight="400"),
            text("$2,997", "40px"),
            button,
        ]},
    }

    section = {
        "t": "Section", "id": "buybox-section-test",
        "styles": [{"prop": "margin", "value": "0px"}, {"prop": "padding", "value": "0px"}],
        "p": {"layout": "", "children": [container]},
    }

    return {
        "id": "root-buy-test", "t": "Root", "version": 11,
        "styles": [{"prop": "pageWidth", "value": "1140px"}],
        "p": {"children": [section]},
    }


def main():
    ACCT = open(".lf_account").read().strip()
    HH = lf_api.session_headers(ACCT)

    n = lf_api.gql(
        None,
        """query($id:ID!){node(id:$id){... on Funnel{
             steps{uid slug title type product_id settings visual{x y}}}}}""",
        {"id": CHECKOUT_FUNNEL}, extra_headers=HH)["node"]
    existing_slugs = {s["slug"] for s in n["steps"]}
    assert "buy-test" not in existing_slugs, (
        "a 'buy-test' step already exists -- this script is for the first "
        "creation only, re-running would make a second one")

    body = product_page_body()
    print("test buybox body: %d bytes" % len(json.dumps(body)))
    print("product: %s" % PRODUCT_ID)
    print("destination: %s" % CHECKOUT_URL)

    if not APPLY:
        print("\ndry run. pass --apply to write.")
        return

    created = lf_api.gql(
        None,
        'mutation($fid:ID!,$node:InputStep!){createStep(funnel_id:$fid,'
        'node:$node){step{id uid slug type product_id}}}',
        {"fid": CHECKOUT_FUNNEL,
         "node": {"slug": "buy-test",
                  "title": "TEST — Secure Your Seat (SoF General Admission)",
                  "type": "product_page", "product_id": PRODUCT_ID,
                  "settings": {}, "visual": {"x": 1200, "y": 420},
                  "body": body}},
        extra_headers=HH)
    sid = created["createStep"]["step"]["id"]
    print("created detached step ->", created["createStep"]["step"])

    others = [{"id": s["uid"], "slug": s["slug"], "title": s["title"],
               "type": s["type"], "settings": s["settings"],
               "visual": s["visual"], "product_id": s.get("product_id")}
              for s in n["steps"]]
    new_step = {"id": sid, "slug": "buy-test",
                "title": "TEST — Secure Your Seat (SoF General Admission)",
                "type": "product_page", "product_id": PRODUCT_ID,
                "settings": {}, "visual": {"x": 1200, "y": 420}}
    r = lf_api.gql(
        None,
        "mutation($id:ID!,$node:InputFunnel!){updateFunnel(id:$id,node:$node){"
        "id steps{uid slug type product_id}}}",
        {"id": CHECKOUT_FUNNEL, "node": {"steps": others + [new_step]}},
        extra_headers=HH)
    print("\nWROTE", json.dumps(r["updateFunnel"], indent=1))
    print("\ntest at: https://www.scalingorfailing.com/sof-checkout/buy-test")


main()
