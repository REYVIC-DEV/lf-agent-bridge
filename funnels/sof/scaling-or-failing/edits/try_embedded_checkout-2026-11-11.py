#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Try Whop's embedded checkout (Elements) behind our OWN button, on the
sof-v3 TEST step only.

JOSHUA, 2026-11-11: asked whether our styled button could fire the embed's
JS instead of linking out, so the promo code -- read from our own URL's
`?ref=`, same param the old Stripe-era `wire_affiliate_ref.py` used -- can
be passed into Whop's `promoCode` create() option, auto-applying it before
the buyer sees the price. Confirmed from docs.whop.com (not login-gated):
no API key needed on the page, create()/mount() aren't documented as
load-time-only, and destroy() is the documented way to reset before
mounting again.

What this changes, test step only:
  - The one ticket button (`.sof-tbtn`) becomes a <button>, not a link, with
    a `data-sof-checkout="<plan id>"` attribute instead of an href. Every
    `.sof-tbtn` CSS rule targets the class, not the tag, so the swap does
    not touch how it looks.
  - A hidden modal (`#sof-checkout-overlay`) and the Whop Elements script
    are appended to the step's `custom_html.footer`. Closed by default;
    opens only on click.
  - Clicking the button reads `?ref=` from the page's own URL, creates the
    Whop checkout with that as `promoCode`, and mounts it into the modal.
    No `?ref=` means no promoCode argument at all -- not an empty string.

NOT touched: the live `scaling-failing` / `contact` steps, the promo-bar
link, or anything in build_sof_event.py. This is a sof-v3-only experiment
to prove the pattern before it goes anywhere near the live page.

    py funnels/sof/scaling-or-failing/edits/try_embedded_checkout-2026-11-11.py
    py funnels/sof/scaling-or-failing/edits/try_embedded_checkout-2026-11-11.py --apply
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
PLAN_ID = "plan_9fd3QJCm3n9sM"

OLD_BTN = (
    '<a class="sof-tbtn" href="https://whop.com/checkout/plan_9fd3QJCm3n9sM">'
    '<i aria-hidden="true"></i><span>SECURE YOUR SEAT  →</span></a>'
)
NEW_BTN = (
    '<button type="button" class="sof-tbtn" data-sof-checkout="%s">'
    '<i aria-hidden="true"></i><span>SECURE YOUR SEAT  →</span></button>'
) % PLAN_ID

EMBED_BLOCK = """
<style>
#sof-checkout-overlay{display:none;position:fixed;inset:0;z-index:9999;
  background:rgba(7,6,15,.6);align-items:center;justify-content:center;padding:20px}
#sof-checkout-overlay.sof-open{display:flex}
#sof-checkout-box{position:relative;background:#fff;border-radius:16px;
  width:100%;max-width:480px;max-height:90vh;overflow:auto;padding:24px}
#sof-checkout-close{position:absolute;top:8px;right:12px;width:32px;height:32px;
  border:none;background:none;font-size:24px;line-height:1;cursor:pointer;color:#041C32}
</style>
<div id="sof-checkout-overlay">
  <div id="sof-checkout-box">
    <button type="button" id="sof-checkout-close" aria-label="Close">&times;</button>
    <div id="checkout"></div>
  </div>
</div>
<script src="https://cdn.whop.com/elements/amber/elements.js" data-whop-elements></script>
<script>
(function(){
  var REF = new URLSearchParams(location.search).get('ref');
  var handle = null;
  function openCheckout(planId){
    document.getElementById('sof-checkout-overlay').classList.add('sof-open');
    if (handle) { handle.destroy(); handle = null; }
    var opts = {plan: planId, returnUrl: location.origin + '/thank-you'};
    if (REF) { opts.promoCode = REF; }
    // Two create() calls, not one: the first makes the checkout GROUP (where
    // plan/promoCode/returnUrl live), the second makes the actual mountable
    // "checkout" element from that group. Confirmed the hard way on sof-v3:
    // calling .mount() on the group's return value throws
    // "handle.mount is not a function".
    var group = window.WhopElements().checkout.create(opts);
    handle = group.create('checkout');
    handle.mount('#checkout');
  }
  function closeCheckout(){
    document.getElementById('sof-checkout-overlay').classList.remove('sof-open');
    if (handle) { handle.destroy(); handle = null; }
    document.getElementById('checkout').innerHTML = '';
  }
  document.addEventListener('click', function(e){
    var btn = e.target.closest('[data-sof-checkout]');
    if (btn) { e.preventDefault(); openCheckout(btn.getAttribute('data-sof-checkout')); return; }
    if (e.target.id === 'sof-checkout-close' || e.target.id === 'sof-checkout-overlay') {
      closeCheckout();
    }
  });
})();
</script>
"""

APPLY = "--apply" in sys.argv


def main():
    ACCT = open(".lf_account").read().strip()
    HH = lf_api.session_headers(ACCT)
    steps = lf_api.get_funnel_steps(None, FUNNEL, extra_headers=HH)["steps"]
    mine = next((s for s in steps if s["slug"] == STEP_SLUG), None)
    assert mine is not None, "step %r not found in funnel %r" % (STEP_SLUG, FUNNEL)

    def count_in_body(node, target):
        n = 0
        if isinstance(node, dict):
            for v in node.values():
                n += count_in_body(v, target)
        elif isinstance(node, list):
            for v in node:
                n += count_in_body(v, target)
        elif isinstance(node, str):
            n += node.count(target)
        return n

    btn_hits = count_in_body(mine["body"], OLD_BTN)
    assert btn_hits == 1, \
        "expected exactly 1 occurrence of the ticket button in body, found %d" % btn_hits

    footer = mine["settings"]["custom_html"]["footer"]
    assert "cdn.whop.com" not in footer, \
        "footer already has a Whop embed script -- this script would double it up"

    print("sof-v3: button match ok, footer has no existing embed script")

    if not APPLY:
        print("\ndry run. pass --apply to write.")
        return

    def replace_in_body(node):
        if isinstance(node, dict):
            return {k: replace_in_body(v) for k, v in node.items()}
        if isinstance(node, list):
            return [replace_in_body(v) for v in node]
        if isinstance(node, str) and OLD_BTN in node:
            return node.replace(OLD_BTN, NEW_BTN)
        return node

    new_body = replace_in_body(mine["body"])
    new_settings = dict(mine["settings"])
    new_settings["custom_html"] = dict(mine["settings"]["custom_html"])
    new_settings["custom_html"]["footer"] = footer + EMBED_BLOCK

    step = {
        "id": mine["id"],
        "slug": mine["slug"],
        "title": mine["title"],
        "type": mine["type"],
        "settings": new_settings,
        "visual": {"x": mine["visual"]["x"], "y": mine["visual"]["y"]},
        "body": new_body,
    }
    mutation = """
    mutation TryEmbed($id: ID!, $node: InputFunnel!) {
      updateFunnel(id: $id, node: $node) { id steps { uid } }
    }
    """
    r = lf_api.gql(None, mutation, {"id": FUNNEL, "node": {"steps": [step]}},
                   extra_headers=HH)
    print(json.dumps(r, indent=1))


main()
