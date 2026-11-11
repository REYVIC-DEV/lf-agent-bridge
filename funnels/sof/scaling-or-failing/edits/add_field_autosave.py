#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Keep Contact/Delivery/Billing fields across the checkout-page reload the
quantity stepper now does.

JOSHUA, 2026-11-03: "okay but if it refresh make sure what is typed on the
fields are not lost on refresh" -- said right after the quantity stepper
on the checkout page was built to work by editing the cart cookie and
calling `location.reload()`.

SOURCE: Garlic's own checkout (fun__LKgKGNO4H6IoYoFN6RfK, step `checkouts`)
already carries exactly this -- a `settings.custom_html.footer` script that
watches every named input/select/textarea, saves each one to localStorage
keyed by name (billing.* vs shipping.*, by css class), and restores it
on load via a MutationObserver (fields get re-created as React re-renders,
so a one-time DOMContentLoaded scan would miss anything added later). It
was deliberately left OUT of the earlier de-branding pass as a pure
convenience this build didn't need yet -- it is needed now.

⚠️ ONE LINE REMOVED FROM THE ORIGINAL: `localStorage.removeItem(STORAGE_KEY)`
at the top, which fires on every load INCLUDING the reload this is being
added to support. Keeping it would wipe the saved values before they can
ever be restored -- the exact bug Joshua is asking to avoid, caused by the
very mechanism meant to prevent it. Whatever that line was for on Garlic's
own checkout (most likely: starting clean on a brand new visit vs. a
mid-session reload, a distinction this script has no way to make), it
cannot survive unmodified here.

Writes to settings.custom_html.footer, scoped to the one checkout step via
step_uids -- same place, same mechanism as every other per-step script in
this project, not the shared article-page builder.

    py funnels/sof/scaling-or-failing/edits/add_field_autosave.py
    py funnels/sof/scaling-or-failing/edits/add_field_autosave.py --apply
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
APPLY = "--apply" in sys.argv

# Garlic's own script, verbatim, MINUS the `localStorage.removeItem` line
# that fires on every load (see docstring).
AUTOSAVE_SCRIPT = """<script>
(function(){

const STORAGE_KEY = "lf_checkout_data";

function getStored(){
  try{
    return JSON.parse(localStorage.getItem(STORAGE_KEY)) || {};
  }catch{
    return {};
  }
}

function setStored(data){
  localStorage.setItem(STORAGE_KEY,JSON.stringify(data));
}

function getKey(el){

  if(!el.name) return null;

  if(el.classList.contains("billing")){
    return "billing." + el.name;
  }

  return "shipping." + el.name;
}

function saveField(el){

  const key = getKey(el);
  if(!key) return;

  const data = getStored();

  data[key] = el.value;

  setStored(data);

}

function nativeValueSetter(el){

  /* ⚠️ `el.value = x` alone does not survive a later React re-render.
     React wraps HTMLInputElement.prototype's own `value` setter to track
     whether a change came from the user or from outside code; writing the
     plain property bypasses that tracker, so the field LOOKS restored
     right up until the app next re-renders for any unrelated reason (an
     async cart/session fetch, the payment iframe's own postMessage,
     anything), at which point React puts its own -- still empty --
     internal value back. Confirmed directly: the plain assignment held
     for 4+ seconds with nothing else touching the field, then was gone
     once the page did something else. Going through the native prototype
     setter is the standard workaround -- it is what lets React's own
     tracker see the write as real. */

  const proto = el.tagName === "TEXTAREA"
    ? window.HTMLTextAreaElement.prototype
    : window.HTMLInputElement.prototype;

  return Object.getOwnPropertyDescriptor(proto, "value").set;

}

function restoreField(el){

  const key = getKey(el);
  if(!key) return;

  const data = getStored();

  if(!(key in data)) return;

  if(!el.value){
    nativeValueSetter(el).call(el, data[key]);
  }

  el.dispatchEvent(new Event("input",{bubbles:true}));
  el.dispatchEvent(new Event("change",{bubbles:true}));

}

function watchLine1(el){

  if(el.dataset.lfLine1Watch) return;
  el.dataset.lfLine1Watch = "1";

  let last = el.value;

  setInterval(function(){

    if(el.value !== last){
      last = el.value;
      saveField(el);
    }

  },300);

}

function attachField(el){

  if(!el) return;

  /* ⚠️ RESTORE ON EVERY SCAN, NOT ONLY ON FIRST ATTACH. `getKey(el)` needs
     `el.name`, and the MutationObserver can see this input before React
     has finished setting that attribute -- so the one-shot restore this
     used to be would silently no-op (no key yet) and never run again,
     because it was gated behind the SAME flag used to stop the listeners
     below from being bound twice. Confirmed directly: typed values saved
     to localStorage correctly (proving the listeners DID bind and DID
     eventually see a real name), but never came back after a reload
     (proving the one restore attempt ran before the name existed).
     restoreField() is cheap and already a no-op once the field holds a
     real value or there is nothing stored for it, so calling it again on
     every scan costs nothing once it has already succeeded. */
  restoreField(el);

  /* ⚠️ A FEW DELAYED RETRIES, SEPARATE FROM THE SCAN-DRIVEN ONE ABOVE.
     Every ordinary field was fixed by going through the native value
     setter -- but Email specifically kept resetting to empty even when
     set that exact way, immediately, not after some later unrelated
     render. That means whatever resets it is not "a stale React render
     happened" (the bug the native setter fixes), it is something that
     runs AGAIN shortly after mount and wins the race regardless of how
     carefully the value is set once. Retrying a few times over the next
     few seconds is a direct, cheap way to eventually land a restore AFTER
     that reset has already fired, rather than only ever racing it.
     Scheduled once per element (own flag, independent of `lfSaved`,
     which only gates the LISTENER binding below) so a field already
     holding a real value is not touched again -- restoreField's own
     `if(!el.value)` guard makes every one of these a no-op the moment
     the restore has actually taken. */
  if(!el.dataset.lfRetryScheduled){
    el.dataset.lfRetryScheduled = "1";
    [400, 1000, 2000, 3500, 6000].forEach(function(ms){
      setTimeout(function(){ restoreField(el); }, ms);
    });
  }

  if(el.dataset.lfSaved) return;

  el.dataset.lfSaved = "1";

  const handler = ()=>saveField(el);

  el.addEventListener("input",handler);
  el.addEventListener("change",handler);
  el.addEventListener("blur",handler);
  el.addEventListener("keyup",handler);
  el.addEventListener("paste",handler);

  if(el.name === "line1"){
    watchLine1(el);
  }

}

function captureShippingMethod(){

  const active = document.querySelector("._266 .zsy6s.active");
  if(!active) return;

  const row = active.closest(".Cq73x");
  if(!row) return;

  const label = row.querySelector("._271");
  if(!label) return;

  const data = getStored();

  data.shipping_method = label.textContent.trim();

  setStored(data);

}

function capturePaymentMethod(){

  const active = document.querySelector("#payment-picker .zsy6s.active");
  if(!active) return;

  const wrapper = active.closest(".SK2Ly");
  if(!wrapper) return;

  const title = wrapper.querySelector(".b56om");
  if(!title) return;

  const data = getStored();

  data.payment_method = title.textContent.trim();

  setStored(data);

}

function captureBillingSame(){

  const checkbox = document.querySelector("._209 input[type='checkbox']");
  if(!checkbox) return;

  const data = getStored();

  data.billing_same = checkbox.checked;

  setStored(data);

}

function attachBillingSame(){

  const checkbox = document.querySelector("._209 input[type='checkbox']");
  if(!checkbox || checkbox.dataset.lfBound) return;

  checkbox.dataset.lfBound = "1";

  checkbox.addEventListener("change",captureBillingSame);

}

function attachPaymentListener(){

  const root = document.querySelector("#payment-picker");
  if(!root || root.dataset.lfPayBound) return;

  root.dataset.lfPayBound = "1";

  root.addEventListener("click",()=>{
    setTimeout(capturePaymentMethod,120);
  });

}

function scan(){

  const fields = document.querySelectorAll("input[name], select[name], textarea[name]");

  fields.forEach(attachField);

  captureShippingMethod();
  capturePaymentMethod();
  captureBillingSame();

  attachBillingSame();
  attachPaymentListener();

}

const observer = new MutationObserver(scan);

/* ⚠️ `attributes:true` matters here, not just childList. If a field's
   `name` only gets set after the input already exists (a ref effect
   registering it, rather than it being present on first paint), that is
   an ATTRIBUTE mutation on a node already in the tree -- a childList-only
   observer never sees it, so scan() would never run again for that node
   and the early, name-less restore attempt would stand as the only one. */
observer.observe(document.documentElement,{
  childList:true,
  subtree:true,
  attributes:true,
  attributeFilter:["name","value"]
});

if(document.readyState === "loading"){
  document.addEventListener("DOMContentLoaded",scan);
}else{
  scan();
}

})();
</script>"""


def main():
    ACCT = open(".lf_account").read().strip()
    HH = lf_api.session_headers(ACCT)
    n = lf_api.gql(
        None,
        """query($id:ID!){node(id:$id){... on Funnel{
             steps{uid slug title type product_id settings visual{x y} body}}}}""",
        {"id": FUNNEL}, extra_headers=HH)["node"]
    step = next(s for s in n["steps"] if s["uid"] == STEP)
    settings = step["settings"]
    custom_html = dict(settings.get("custom_html") or {})

    # ⚠️ REPLACE, not skip-if-present. The first version of this script had
    # a real bug (see nativeValueSetter's comment: restored values did not
    # survive a React re-render) and is still live on the checkout step.
    # Cut everything from our own marker onward -- nothing else has ever
    # been appended after it on this step -- then put the fixed version
    # back.
    marker = 'const STORAGE_KEY = "lf_checkout_data"'
    footer = custom_html.get("footer") or ""
    idx = footer.find(marker)
    if idx != -1:
        # back up to the start of that <script> tag, not just the marker
        tag_start = footer.rfind("<script>", 0, idx)
        before = footer[:tag_start] if tag_start != -1 else footer[:idx]
        print("replacing existing autosave script (was missing the native setter fix)")
    else:
        before = footer

    custom_html["footer"] = before + "\n" + AUTOSAVE_SCRIPT
    settings = dict(settings)
    settings["custom_html"] = custom_html

    print("footer script: %d bytes" % len(custom_html["footer"]))
    if not APPLY:
        print("dry run. pass --apply to write.")
        return

    others = [{"id": s["uid"], "slug": s["slug"], "title": s["title"], "type": s["type"],
               "settings": s["settings"], "visual": s["visual"], "product_id": s.get("product_id")}
              for s in n["steps"] if s["uid"] != STEP]
    mine = {"id": STEP, "slug": step["slug"], "title": step["title"], "type": step["type"],
            "settings": settings, "visual": step["visual"],
            "product_id": step.get("product_id"), "body": step["body"]}
    r = lf_api.gql(
        None,
        "mutation($id:ID!,$node:InputFunnel!){updateFunnel(id:$id,node:$node){"
        "id steps{uid slug}}}",
        {"id": FUNNEL, "node": {"steps": others + [mine]}}, extra_headers=HH)
    print(json.dumps(r, indent=1))


main()
