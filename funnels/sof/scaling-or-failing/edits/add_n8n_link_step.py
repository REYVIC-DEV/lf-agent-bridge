#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""A new, separate step for the n8n-generated-payment-link scenario.

JOSHUA, 2026-11-03/04: "I plan to make a n8n endpoint we can call that will
generate the links itself so no api key is on LF, lets try to make new
steps for this specific scenario" -- said right after asking "wait what if
i have api access on airwallex?".

WHY A NEW STEP, NOT A CHANGE TO THE EXISTING ONE: the whole point is a
different architecture, not a patch. Everything built so far this session
(buy-now/buy-test's cart cookie, the checkout page cloned from Garlic, the
quantity stepper, the field-autosave script) exists because Lightfunnels'
OWN checkout has to collect contact/billing/card details itself. If
Airwallex's hosted payment page collects all of that instead, none of
that machinery is needed for THIS flow: no cart, no checkout_page, no
field restore. One page, one button, one outbound call. Kept entirely
separate so the already-working cart-based flow is untouched and still
there to fall back on or compare against.

    https://www.scalingorfailing.com/sof-checkout/buy-link

THE CONTRACT THIS PAGE NEEDS FROM N8N -- not yet live, this is what the
button calls once it exists:

    POST https://primary-production-f5243.up.railway.app/webhook/sof-payment-link
    Content-Type: application/x-www-form-urlencoded   (a CORS "simple
      request" -- no preflight OPTIONS, same reasoning as sof-contact-form;
      see N8N/documentation/sof-contact-form.md)

    body:  product=sof-general-admission&quantity=<1-99>

    response (JSON, 200): {"ok": true, "url": "<Airwallex hosted payment
      page URL for exactly that quantity>"}
    response (JSON, 200): {"ok": false, "error": "<message>"}  on any
      rejection (bad quantity, Airwallex API error, etc.) -- still HTTP
      200, same `responseMode: lastNode` pattern as the contact form, so
      the page can always read a real JSON body rather than a CORS-
      opaque error.

⚠️ THE PRICE IS NOT TRUSTED FROM THE CLIENT, ON PURPOSE. The request sends
`quantity` and a `product` key, never an amount -- n8n is expected to look
up the SoF General Admission price itself (or hold it as a Config node
constant, same pattern as `send_to` in the contact-form workflow) and
compute total = price * quantity server-side. A button that could tell
Airwallex what to charge would be the single easiest fraud vector this
page could have; nothing here hands it that power.

⚠️ THE WEBHOOK PATH ABOVE IS A GUESS, MATCHED TO THE CONTACT-FORM
CONVENTION (`/webhook/sof-<thing>`), NOT YET CONFIRMED. `N8N_WEBHOOK_URL`
below is the ONE constant to change once Joshua builds the real workflow
and knows its actual path.

    py funnels/sof/scaling-or-failing/edits/add_n8n_link_step.py
    py funnels/sof/scaling-or-failing/edits/add_n8n_link_step.py --apply
"""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", "..", "..", ".."))
sys.path.insert(0, ROOT)
os.chdir(ROOT)
import lf_api

FUNNEL = "fun_MaCLh5DOqyw_f1Viin3Z_"   # the sof-checkout test funnel
SLUG = "buy-link"
N8N_WEBHOOK_URL = "https://primary-production-f5243.up.railway.app/webhook/sof-payment-link"
IMAGE_PATH = ("https://assets.lightfunnels.com/account-90380/images_library/"
              "52e02c2e-5a33-48e2-af68-7f7010d89b00._5dGZ_Nl-HGsVJlNnoUXb.webp")
LOGO_PATH = IMAGE_PATH   # same "Scaling or Failing" wordmark used elsewhere
APPLY = "--apply" in sys.argv

HTML = """
<div style="background:#0B1A32;padding:24px;text-align:center">
  <img src="%(logo)s" alt="Scaling or Failing"
       style="height:44px;width:auto;max-width:220px;object-fit:contain">
</div>
<div style="max-width:480px;margin:80px auto;padding:32px;text-align:center;
            font-family:Inter,sans-serif">
  <h2 style="font-size:28px;font-weight:700;margin:0 0 8px;color:#041C32">
    SoF General Admission</h2>
  <p style="font-size:15px;margin:0 0 8px;color:#57637A">
    Bangkok, December 7&ndash;8 2026</p>
  <p style="font-size:40px;font-weight:700;margin:0 0 20px;color:#041C32">
    $2,997</p>
  <div style="display:flex;align-items:center;justify-content:center;
              gap:18px;margin:0 0 20px">
    <button type="button" id="sof-link-qty-minus"
      style="width:40px;height:40px;border-radius:9999px;border:2px solid #041C32;
             background:#fff;color:#041C32;font-size:20px;font-weight:700;
             cursor:pointer;line-height:1">&minus;</button>
    <span id="sof-link-qty" style="font-size:20px;font-weight:700;min-width:24px;
          display:inline-block;color:#041C32">1</span>
    <button type="button" id="sof-link-qty-plus"
      style="width:40px;height:40px;border-radius:9999px;border:2px solid #041C32;
             background:#fff;color:#041C32;font-size:20px;font-weight:700;
             cursor:pointer;line-height:1">+</button>
  </div>
  <button type="button" id="sof-link-buy"
    style="display:block;width:100%%;height:56px;line-height:56px;padding:0;
           background:#041C32;color:#fff;border:none;border-radius:9999px;
           font-weight:700;font-size:16px;cursor:pointer;font-family:inherit">
    SECURE YOUR SEAT &rarr;
  </button>
  <p id="sof-link-error" style="display:none;color:#A3051B;font-size:14px;
     margin-top:14px"></p>
</div>
<script>
(function(){
  var qtyEl = document.getElementById('sof-link-qty');
  var errEl = document.getElementById('sof-link-error');
  var buyBtn = document.getElementById('sof-link-buy');

  document.getElementById('sof-link-qty-minus').addEventListener('click', function(){
    var n = parseInt(qtyEl.textContent, 10);
    if (n > 1) qtyEl.textContent = String(n - 1);
  });
  document.getElementById('sof-link-qty-plus').addEventListener('click', function(){
    var n = parseInt(qtyEl.textContent, 10);
    qtyEl.textContent = String(n + 1);
  });

  buyBtn.addEventListener('click', function(){
    errEl.style.display = 'none';
    buyBtn.disabled = true;
    var original = buyBtn.textContent;
    buyBtn.textContent = 'One moment\\u2026';

    var qty = parseInt(qtyEl.textContent, 10) || 1;
    var body = 'product=sof-general-admission&quantity=' + encodeURIComponent(qty);

    fetch('%(webhook)s', {
      method: 'POST',
      headers: {'Content-Type': 'application/x-www-form-urlencoded'},
      body: body
    })
      .then(function(r){ return r.json(); })
      .then(function(data){
        if (data && data.ok && data.url) {
          window.location.href = data.url;
          return;
        }
        throw new Error((data && data.error) || 'Could not start checkout.');
      })
      .catch(function(e){
        errEl.textContent = (e && e.message) ||
          'Something went wrong. Please try again or contact us.';
        errEl.style.display = 'block';
        buyBtn.disabled = false;
        buyBtn.textContent = original;
      });
  });
})();
</script>
""" % {"logo": LOGO_PATH, "webhook": N8N_WEBHOOK_URL}


def main():
    ACCT = open(".lf_account").read().strip()
    HH = lf_api.session_headers(ACCT)
    n = lf_api.gql(
        None,
        """query($id:ID!){node(id:$id){... on Funnel{
             steps{uid slug title type product_id settings visual{x y}}}}}""",
        {"id": FUNNEL}, extra_headers=HH)["node"]
    existing = next((s for s in n["steps"] if s["slug"] == SLUG), None)

    body = {
        "id": "root-buy-link", "t": "Root", "version": 11,
        "styles": [{"prop": "pageWidth", "value": "1140px"}],
        "p": {"children": [{
            "t": "Section", "id": "buy-link-section",
            "styles": [{"prop": "margin", "value": "0px"}, {"prop": "padding", "value": "0px"}],
            "p": {"layout": "", "children": [{
                "t": "HtmlElement", "id": "buy-link-html",
                "styles": [{"prop": "width", "value": "100%"}],
                "p": {"content": HTML},
            }]},
        }]},
    }

    print("page body: %d bytes" % len(json.dumps(body)))
    print("calls: %s" % N8N_WEBHOOK_URL)

    if not APPLY:
        print("dry run. pass --apply to write.")
        return

    others = [{"id": s["uid"], "slug": s["slug"], "title": s["title"], "type": s["type"],
               "settings": s["settings"], "visual": s["visual"], "product_id": s.get("product_id")}
              for s in n["steps"] if s["slug"] != SLUG]

    if existing:
        mine = {"id": existing["uid"], "slug": SLUG, "title": "Secure Your Seat (n8n link)",
                "type": "article_page", "settings": existing["settings"],
                "visual": existing["visual"], "body": body}
        print("replacing existing buy-link step")
    else:
        created = lf_api.gql(
            None,
            'mutation($fid:ID!,$node:InputStep!){createStep(funnel_id:$fid,'
            'node:$node){step{id uid slug}}}',
            {"fid": FUNNEL, "node": {
                "slug": SLUG, "title": "Secure Your Seat (n8n link)",
                "type": "article_page", "settings": {}, "visual": {"x": 1600, "y": 420},
                "body": body}},
            extra_headers=HH)
        sid = created["createStep"]["step"]["id"]
        print("created detached step ->", created["createStep"]["step"])
        mine = {"id": sid, "slug": SLUG, "title": "Secure Your Seat (n8n link)",
                "type": "article_page", "settings": {}, "visual": {"x": 1600, "y": 420}}

    r = lf_api.gql(
        None,
        "mutation($id:ID!,$node:InputFunnel!){updateFunnel(id:$id,node:$node){"
        "id steps{uid slug type}}}",
        {"id": FUNNEL, "node": {"steps": others + [mine]}}, extra_headers=HH)
    print(json.dumps(r, indent=1))
    print("\nlive at: https://www.scalingorfailing.com/sof-checkout/%s" % SLUG)


main()
