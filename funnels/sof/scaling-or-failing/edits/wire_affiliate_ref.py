#!/usr/bin/env python3
"""Put an affiliate's promo code on the Stripe buttons, from a ?ref= in the URL.

Seven affiliates each have their own Stripe payment link, identical except for
the promo code on the end:

    https://buy.stripe.com/3cIfZh0RM201aiyg01dby04?prefilled_promo_code=JEM

Rather than build seven copies of the site, the site reads the code off its own
URL and rewrites the buttons:

    scalingorfailing.com/event/?ref=JEM
      -> both Stripe buttons become ...?prefilled_promo_code=JEM

JOSHUA'S TWO CALLS, 2026-10-30:
  - the parameter is `ref`, and only `ref`
  - ANY code is accepted, not a fixed list of the seven. A new affiliate works
    the moment the code exists in Stripe, with no edit to this site. An unknown
    code simply means Stripe applies no discount, which is the same outcome as a
    typo in a hand-made link.

WHAT IT TOUCHES. Exactly the anchors whose href starts with the Stripe payment
host, which on 2026-10-30 is three links across the two pages:

    /event/scaling-failing   a.sof-promo   sticky early-bird bar
                             a.sof-tbtn    the ticket card button
    /event/contact           a.sof-promo   sticky early-bird bar

Nothing else on either page is read or written. Matching on the href rather than
on a class means a fourth Stripe button added later is picked up for free.

THREE THINGS WORTH KNOWING ABOUT THE SCRIPT:

1. THE CODE IS CLEANED, NOT TRUSTED. Uppercased and accepted only if it is 1-40
   characters of A-Z, 0-9, dash or underscore. Anything else is dropped and the
   button stays the plain link. So a junk or hostile `?ref=` cannot reshape the
   Stripe URL - it never reaches it.

2. IT IS REMEMBERED FOR THE VISIT, in sessionStorage. The nav sends people to
   /event/contact, and without this the code would be gone when they came back
   and the affiliate would lose the sale. Session scope, so it dies with the tab
   rather than following someone around for weeks.

3. IT RE-APPLIES ON DOM CHANGES. Lightfunnels hydrates its blocks from JSON
   after load, which can replace the anchors that were rewritten. A
   MutationObserver puts the code back. Two guards keep that from spinning:
   a link already carrying the right code is skipped, so the pass writes nothing
   and triggers no further mutation, and the callback is debounced to one run per
   animation frame, because an unthrottled whole-document observer doing a
   querySelectorAll is its own source of scroll jank on a page running Lenis.

Appended to the funnel `header_scripts`, after the Lenis block and the contact
form handler, because that is the only script slot this account exposes.
Idempotent: it stops if the marker is already there.

    py funnels/sof/scaling-or-failing/edits/wire_affiliate_ref.py            dry run
    py funnels/sof/scaling-or-failing/edits/wire_affiliate_ref.py --apply
"""
import io
import os
import sys
import time
import urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", "..", "..", ".."))
sys.path.insert(0, ROOT)
os.chdir(ROOT)
import lf_api  # noqa: E402

FUNNEL = "fun_RoOL_WXDCAxK4hEk0v5xX"
MARK = "sof-affiliate-ref"
PAGES = [
    "https://www.scalingorfailing.com/event/scaling-failing",
    "https://www.scalingorfailing.com/event/contact",
]
STRIPE = "https://buy.stripe.com/"
APPLY = "--apply" in sys.argv

SCRIPT = """<!-- %s -->
<script>
/* Affiliate promo codes on the Stripe buttons, taken from ?ref= on our own URL.
   scalingorfailing.com/event/?ref=JEM  ->  buttons carry prefilled_promo_code=JEM
   Any code is accepted so a new affiliate needs no site change; it is cleaned
   first, so a junk or hostile value can never reshape the Stripe URL. */
(function () {
  var PARAM  = 'ref';
  var STORE  = 'sof_ref';
  var PREFIX = '%s';
  var FIELD  = 'prefilled_promo_code';

  /* Uppercase, and only A-Z 0-9 _ - up to 40 chars. Anything else becomes ''
     and the buttons are left exactly as they shipped. */
  function clean(v) {
    if (!v) return '';
    v = String(v).trim().toUpperCase();
    return /^[A-Z0-9_-]{1,40}$/.test(v) ? v : '';
  }

  var code = '';
  try { code = clean(new URLSearchParams(window.location.search).get(PARAM)); } catch (e) {}

  /* Remember it for the rest of the visit. The nav links out to /event/contact,
     and without this the code is lost on the way back and the affiliate loses
     the sale. sessionStorage, so it ends with the tab. */
  try {
    if (code) window.sessionStorage.setItem(STORE, code);
    else code = clean(window.sessionStorage.getItem(STORE));
  } catch (e) {}

  if (!code) return;

  function apply() {
    var links = document.querySelectorAll('a[href^="' + PREFIX + '"]');
    for (var i = 0; i < links.length; i++) {
      var a = links[i], u;
      try { u = new URL(a.href); } catch (e) { continue; }
      /* Already right: skip, so this pass writes nothing to the DOM and cannot
         re-trigger the observer below. */
      if (u.searchParams.get(FIELD) === code) continue;
      u.searchParams.set(FIELD, code);
      a.href = u.toString();
    }
  }

  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', apply);
  else apply();

  /* LF hydrates its blocks from JSON after load and can replace these anchors,
     which would silently drop the code. Debounced to one run per frame: an
     unthrottled document-wide observer running querySelectorAll is a scroll-jank
     source on a page that is also running Lenis. */
  var queued = false;
  function schedule() {
    if (queued) return;
    queued = true;
    requestAnimationFrame(function () { queued = false; apply(); });
  }
  try {
    new MutationObserver(schedule).observe(document.documentElement,
                                           { childList: true, subtree: true });
  } catch (e) {}
})();
</script>""" % (MARK, STRIPE)

Q = 'query($id:ID!){node(id:$id){... on Funnel{name header_scripts}}}'
MUT = 'mutation($id:ID!,$node:InputFunnel!){updateFunnel(id:$id,node:$node){id}}'

tok = open(".session_token").read().strip()
h = lf_api.session_headers(open(".lf_account").read().strip())

node = lf_api.gql(tok, Q, {"id": FUNNEL}, extra_headers=h)["node"]
cur = node.get("header_scripts") or ""
print("funnel: %s" % node.get("name"))
print("header_scripts: %d chars" % len(cur))

if MARK in cur:
    sys.exit("Already installed (marker %r present). Nothing to do." % MARK)

# The buttons this is for must actually exist, or the script is wiring nothing.
total = 0
for url in PAGES:
    req = urllib.request.Request(url + "?cb=%d" % time.time(),
                                 headers={"User-Agent": "Mozilla/5.0",
                                          "Cache-Control": "no-cache"})
    html = urllib.request.urlopen(req, timeout=90).read().decode("utf-8", "replace")
    n = html.count('href="' + STRIPE)
    print("  %-62s %d Stripe button(s)" % (url.split("//")[1], n))
    total += n
assert total >= 3, "expected at least 3 Stripe buttons across the two pages, found %d" % total

new = cur.rstrip() + "\n\n" + SCRIPT + "\n"
print("header_scripts: %d -> %d chars (+%d)" % (len(cur), len(new), len(new) - len(cur)))

# Nothing that is already there may move. The append is the only change.
assert new.startswith(cur.rstrip()), "the existing header was disturbed"
for probe in ("lenis", "sof-contact-form -> n8n", "sof-form"):
    assert new.count(probe) == cur.count(probe), "%s count changed" % probe
assert new.count(MARK) == 1

bak = os.path.join(HERE, "..", "header_scripts.pre-affiliate-%s.html"
                   % time.strftime("%Y-%m-%d"))
bak = os.path.abspath(bak)

if not APPLY:
    print("\nDRY RUN. Re-run with --apply to write.")
    sys.exit(0)

with io.open(bak, "w", encoding="utf-8", newline="") as fh:
    fh.write(cur)
print("backup -> %s" % os.path.relpath(bak, ROOT))

lf_api.gql(tok, MUT, {"id": FUNNEL, "node": {"header_scripts": new}}, extra_headers=h)
back = lf_api.gql(tok, Q, {"id": FUNNEL}, extra_headers=h)["node"]["header_scripts"] or ""
assert back == new, "read-back differs from what was sent"
print("header_scripts written and read back identical.")

time.sleep(8)
for url in PAGES:
    req = urllib.request.Request(url + "?cb=%d" % time.time(),
                                 headers={"User-Agent": "Mozilla/5.0",
                                          "Cache-Control": "no-cache"})
    html = urllib.request.urlopen(req, timeout=90).read().decode("utf-8", "replace")
    print("  %-62s marker served: %s" % (url.split("//")[1], MARK in html))

print("\nThe rewrite itself is client side, so it does NOT show in this HTML.")
print("Check it in a browser: open a page with ?ref=JEM and read the button's href.")
