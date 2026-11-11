#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""A quantity stepper ON the checkout page itself, not just the buy page.

JOSHUA, 2026-11-03: "oh cant it be on the checkout itself?" -- after the
buy-page version (add_quantity_adjuster.py) was built and confirmed
working, he asked for it on the page the shopper actually lands on.

WHY THIS IS POSSIBLE: `CheckoutSummary` reads whatever is in the cart
cookie AT PAGE LOAD -- that is the entire mechanism the earlier quantity
test relied on (hand-editing the cookie to quantity:2 or 3 and reloading
the SAME checkout page recomputed the subtotal correctly every time, no
return trip to the buy page needed). So a stepper that edits the cookie
and reloads works exactly where the shopper already is.

WHERE IT LIVES: inserted as a new FIRST child of `Col 5e1fbbf3`, directly
above `CheckoutSummary` (confirmed before writing: that Col's only child
was CheckoutSummary itself, so this cannot be stepping on anything the
managed component owns). One more `HtmlElement`, same reasoning as the
buy-page version: raw HTML so `getElementById` has something real to find,
not an LF block whose own id never reaches the rendered DOM.

⚠️ NOT WIRED INTO `CheckoutSummary`'s OWN "1" BADGE. That badge is the
managed component's own display and is left alone; this is a second,
separate control above it. Both show the same number (confirmed by
testing), just via two different code paths -- a little redundant, not
broken. Worth deciding later whether to hide the managed badge instead.

    py funnels/sof/scaling-or-failing/edits/add_checkout_quantity.py
    py funnels/sof/scaling-or-failing/edits/add_checkout_quantity.py --apply
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
STEP = "step_eFWf92EsCWvQNx5OzREcH"   # checkout
SUMMARY_COL_ID = "5e1fbbf3-7286-46ee-a4b5-6b8965369bb7"
FUNNEL_NUM_ID = 609354
VARIANT_ID = 4301675370
APPLY = "--apply" in sys.argv

COOKIE_RE = r"lf_%d_cart=([^;]+)" % FUNNEL_NUM_ID

# ⚠️ THE FALLBACK CART MUST BE A BARE JS OBJECT LITERAL, NEVER A
# JSON-STRING-PLUS-JSON.parse. A JSON string needs its keys double-quoted
# ("body", "price_bundle", ...), and this whole script sits inside an
# `onclick="..."` HTML attribute ALSO delimited by double quotes -- the
# first literal `"` inside the fallback closes the attribute early, and
# the rest of the handler leaks onto the page as visible text (exactly
# what happened the first time this shipped: the onclick body rendered as
# a wall of text next to the Quantity label). A plain object literal has
# no quotes to collide with (bare keys, null, numbers), which is also how
# the buy-page version (add_quantity_adjuster.py) was already written
# correctly from the start.
# ⚠️ WHY THE BUTTON SAVES FIELDS ITSELF, NOT JUST THE AUTOSAVE SCRIPT'S OWN
# BLUR LISTENERS. Confirmed directly, not guessed: the quantity click was
# captured with `location.reload` stubbed out first, so its own logic ran
# but the actual navigation didn't -- and `localStorage` already held
# `"shipping.email":""` at that exact point, before any reload, before any
# delay. Extending the restore script's retry window from 6s to 45s made
# no difference either, which rules out "the right value exists somewhere
# and just needs more time to win a race" -- the value saveField's blur
# handler captured for THIS one field was already empty by the moment of
# the click. Whatever clears it does so as (or before) the click fires,
# not afterward, so no amount of delayed restore recovers a value that was
# never correctly saved in the first place. The fix is to stop depending
# on that blur handler for this moment: snapshot every named field
# straight into the SAME `lf_checkout_data` key the autosave script reads,
# synchronously, in the same tick as the click, before anything else runs.
SNAPSHOT_JS = (
    "try{"
    "var K='lf_checkout_data';"
    "var d=JSON.parse(localStorage.getItem(K))||{};"
    "var fs=document.querySelectorAll('input[name],select[name],textarea[name]');"
    "fs.forEach(function(el){"
    "if(!el.name)return;"
    "var k=(el.classList.contains('billing')?'billing.':'shipping.')+el.name;"
    "d[k]=el.value;"
    "});"
    "localStorage.setItem(K,JSON.stringify(d));"
    "}catch(e){}"
)

STEP_JS = (
    "(function(){"
    + SNAPSHOT_JS +
    "var m=document.cookie.match(/" + COOKIE_RE + "/);"
    "var c=m?JSON.parse(decodeURIComponent(m[1])):"
    "{body:[{price_bundle:null,variants:[{quantity:1,id:%d,"
    "payment_settings:{type:null,cycle:null}}]}]};"
    "var v=c.body[0].variants[0];"
) % VARIANT_ID

MINUS_ONCLICK = STEP_JS + (
    "if(v.quantity>1){v.quantity-=1;}"
    "document.cookie='lf_%d_cart='+encodeURIComponent(JSON.stringify(c))+';path=/';"
    "location.reload();})()"
) % FUNNEL_NUM_ID

PLUS_ONCLICK = STEP_JS + (
    "v.quantity+=1;"
    "document.cookie='lf_%d_cart='+encodeURIComponent(JSON.stringify(c))+';path=/';"
    "location.reload();})()"
) % FUNNEL_NUM_ID

INIT_SCRIPT = (
    "(function(){"
    "var m=document.cookie.match(/" + COOKIE_RE + "/);"
    "if(!m)return;"
    "try{"
    "var c=JSON.parse(decodeURIComponent(m[1]));"
    "var q=c.body[0].variants[0].quantity;"
    "var el=document.getElementById('sof-checkout-qty');"
    "if(el&&q)el.textContent=String(q);"
    "}catch(e){}"
    "})();"
)

HTML = (
    '<div style="display:flex;align-items:center;justify-content:space-between;'
    'padding:16px 0;border-bottom:1px solid #D6DCE9;font-family:Inter,sans-serif">'
    '<span style="font-size:14px;color:#57637A;font-weight:500">Quantity</span>'
    '<div style="display:flex;align-items:center;gap:14px">'
    '<button type="button" onclick="' + MINUS_ONCLICK + '" '
    'style="width:32px;height:32px;border-radius:9999px;border:2px solid #041C32;'
    'background:#fff;color:#041C32;font-size:16px;font-weight:700;cursor:pointer;'
    'line-height:1">−</button>'
    '<span id="sof-checkout-qty" style="font-size:16px;font-weight:700;'
    'min-width:18px;display:inline-block;text-align:center;color:#041C32">1</span>'
    '<button type="button" onclick="' + PLUS_ONCLICK + '" '
    'style="width:32px;height:32px;border-radius:9999px;border:2px solid #041C32;'
    'background:#fff;color:#041C32;font-size:16px;font-weight:700;cursor:pointer;'
    'line-height:1">+</button>'
    '</div></div><script>' + INIT_SCRIPT + '</script>'
)


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

    def find(nd, tid):
        if isinstance(nd, dict):
            if nd.get("id") == tid:
                return nd
            for v in nd.values():
                r = find(v, tid)
                if r is not None:
                    return r
        elif isinstance(nd, list):
            for v in nd:
                r = find(v, tid)
                if r is not None:
                    return r

    col = find(body, SUMMARY_COL_ID)
    assert col is not None, "summary column not found"

    stepper = {
        "t": "HtmlElement", "id": "checkout-qty-stepper",
        "styles": [{"prop": "width", "value": "100%"},
                   {"prop": "padding", "value": {"left": "20px", "right": "20px"}}],
        "p": {"content": HTML},
    }
    existing_idx = next((i for i, c in enumerate(col["p"]["children"])
                          if c.get("id") == "checkout-qty-stepper"), None)
    if existing_idx is not None:
        # ⚠️ REPLACE, not skip: the first version of this shipped with a
        # real bug (see STEP_JS's comment) and left broken content live on
        # the desktop checkout. Re-running this script is how that gets
        # corrected, so matching the id must overwrite, not no-op.
        col["p"]["children"][existing_idx] = stepper
        print("replaced existing stepper (was broken), HTML: %d bytes" % len(HTML))
    else:
        col["p"]["children"].insert(0, stepper)
        print("inserted, HTML: %d bytes" % len(HTML))

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
