#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Add a quantity stepper to the buy-test page, so a shopper can choose more
than one ticket before reaching checkout.

JOSHUA, 2026-11-03: "is it possible quantity adjuster on the checkout".

CHECKED BEFORE BUILDING ANYTHING: the checkout page's own order summary
(the `Repeater` under `CheckoutSummary`) is Container/Image/Text only --
read-only, no +/- control of its own, confirmed by walking its full
subtree. But the quantity IN THE CART COOKIE genuinely drives the price,
not just the little "1" badge: writing `quantity:2` by hand and reloading
checkout showed the subtotal exactly double (379,845.82 vs 189,922.91 PHP,
a clean 2.0x). So a quantity control has to live on the BUY page, before
the cart is written -- and it can, since quantity is read live at click
time, not baked in anywhere upstream.

⚠️ REBUILT AS ONE RAW HtmlElement, NOT LF Button/Container/Text blocks.
The LF block tree has no STABLE id in its rendered DOM -- its own ids get
hashed into generated classNames (confirmed by inspecting a live page's
compiled output), so `document.getElementById(...)` would have nothing
reliable to find. The real article pages (build_sof_event.py) never hit
this problem because every interactive element there is hand-authored raw
HTML inside an `HtmlElement` block, which renders EXACTLY as written --
same mechanism the real page's own "SECURE YOUR SEAT" button already uses
successfully (wire_one_click.py). Reused here rather than fighting the
block system for something it was never built to expose.

    py funnels/sof/scaling-or-failing/edits/add_quantity_adjuster.py
    py funnels/sof/scaling-or-failing/edits/add_quantity_adjuster.py --apply
"""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", "..", "..", ".."))
sys.path.insert(0, ROOT)
os.chdir(ROOT)
import lf_api

FUNNEL = "fun_MaCLh5DOqyw_f1Viin3Z_"
STEP = "step_J8VAHRmKUNoU4eHLNepf2"   # buy-test
CHECKOUT_URL = "https://www.scalingorfailing.com/sof-checkout/checkout"
IMAGE_PATH = ("https://assets.lightfunnels.com/account-90380/images_library/"
              "52e02c2e-5a33-48e2-af68-7f7010d89b00._5dGZ_Nl-HGsVJlNnoUXb.webp")
FUNNEL_NUM_ID = 609354
VARIANT_ID = 4301675370   # "SoF General Admission", observed and confirmed twice
APPLY = "--apply" in sys.argv

CART_JS_TEMPLATE = (
    "document.cookie='lf_%d_cart='+encodeURIComponent(JSON.stringify("
    "{body:[{price_bundle:null,variants:[{quantity:q,id:%d,"
    "payment_settings:{type:null,cycle:null}}]}]}))+';path=/'"
) % (FUNNEL_NUM_ID, VARIANT_ID)

HTML = (
    '<div style="max-width:480px;margin:80px auto;padding:32px;'
    'text-align:center;font-family:Inter,sans-serif">'
    '<img src="%s" alt="SoF General Admission" '
    'style="max-width:260px;margin:0 auto 20px;display:block">'
    '<h2 style="font-size:28px;font-weight:700;margin:0 0 8px;color:#041C32">'
    'SoF General Admission (TEST PRODUCT)</h2>'
    '<p style="font-size:15px;margin:0 0 8px;color:#57637A">'
    'Bangkok, December 7–8 2026</p>'
    '<p style="font-size:40px;font-weight:700;margin:0 0 20px;color:#041C32">'
    '$2,997</p>'
    '<div style="display:flex;align-items:center;justify-content:center;'
    'gap:18px;margin:0 0 20px">'
    '<button type="button" '
    'onclick="var e=document.getElementById(\'sof-qty\');'
    'var n=parseInt(e.textContent,10);if(n>1){e.textContent=String(n-1);}" '
    'style="width:40px;height:40px;border-radius:9999px;border:2px solid #041C32;'
    'background:#fff;color:#041C32;font-size:20px;font-weight:700;cursor:pointer;'
    'line-height:1">−</button>'
    '<span id="sof-qty" style="font-size:20px;font-weight:700;min-width:24px;'
    'display:inline-block;color:#041C32">1</span>'
    '<button type="button" '
    'onclick="var e=document.getElementById(\'sof-qty\');'
    'var n=parseInt(e.textContent,10);e.textContent=String(n+1);" '
    'style="width:40px;height:40px;border-radius:9999px;border:2px solid #041C32;'
    'background:#fff;color:#041C32;font-size:20px;font-weight:700;cursor:pointer;'
    'line-height:1">+</button>'
    '</div>'
    '<a href="%s" onclick="'
    'var q=parseInt(document.getElementById(\'sof-qty\').textContent,10)||1;'
    '%s" '
    'style="display:block;width:100%%;height:56px;line-height:56px;'
    'background:#041C32;color:#fff;border-radius:9999px;font-weight:700;'
    'text-decoration:none;font-size:16px">SECURE YOUR SEAT (TEST) →</a>'
    '</div>'
) % (IMAGE_PATH, CHECKOUT_URL, CART_JS_TEMPLATE)


def main():
    ACCT = open(".lf_account").read().strip()
    HH = lf_api.session_headers(ACCT)
    n = lf_api.gql(
        None,
        """query($id:ID!){node(id:$id){... on Funnel{
             steps{uid slug title type product_id settings visual{x y} body}}}}""",
        {"id": FUNNEL}, extra_headers=HH)["node"]
    step = next(s for s in n["steps"] if s["uid"] == STEP)
    body = step["body"]

    # body.p.children[0] is the navy header Section (keep); [1] is the
    # Section holding the old Button/Container/Text buybox (replace).
    assert body["p"]["children"][0]["id"].startswith("sof-header"), \
        "expected the header section first -- tree shape changed"
    old_section = body["p"]["children"][1]
    assert old_section["t"] == "Section", "expected the buybox Section second"

    new_section = {
        "t": "Section", "id": "buybox-section-test-html",
        "styles": [{"prop": "margin", "value": "0px"}, {"prop": "padding", "value": "0px"}],
        "p": {"layout": "", "children": [{
            "t": "HtmlElement", "id": "buybox-html-test",
            "styles": [{"prop": "width", "value": "100%"}],
            "p": {"content": HTML},
        }]},
    }
    body["p"]["children"][1] = new_section

    print("new HtmlElement content: %d bytes" % len(HTML))
    if not APPLY:
        print("dry run. pass --apply to write.")
        return

    others = [{"id": s["uid"], "slug": s["slug"], "title": s["title"], "type": s["type"],
               "settings": s["settings"], "visual": s["visual"], "product_id": s.get("product_id")}
              for s in n["steps"] if s["uid"] != STEP]
    mine = {"id": STEP, "slug": step["slug"], "title": step["title"], "type": step["type"],
            "settings": step["settings"], "visual": step["visual"],
            "product_id": step.get("product_id"), "body": body}
    r = lf_api.gql(
        None,
        "mutation($id:ID!,$node:InputFunnel!){updateFunnel(id:$id,node:$node){"
        "id steps{uid slug}}}",
        {"id": FUNNEL, "node": {"steps": others + [mine]}}, extra_headers=HH)
    print(json.dumps(r, indent=1))


main()
