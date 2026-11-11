#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Flip the page off Early Bird pricing the moment the countdown hits zero.

JOSHUA, 2026-10-30: "lets make it so after the timer the price visible would
be the compare." Eline the same morning: the price changes later today, she
will check it after all hands, and asked whether there is a non-live site to
test on. There is not, and this is built so there does not need to be -- see
THE PREVIEW SWITCH below.

THE DEADLINE IS THE COUNTDOWN'S OWN. 2026-10-31T06:59:59Z, which is 23:59:59
on 30 October in US Pacific -- moved there from Bangkok midnight on
2026-10-30, see move_countdown_to_us.py. It is the same instant the gold countdown bar counts
to and the same fact the "ENDS OCT 30" pill states, so all three move together
or the page contradicts itself. If that date moves, it moves in THREE places:
this file, COUNTDOWN_ENDS in pagescore/build_sof_event.py, and the pill's copy
in COPY_EDITS["949:1473"].

EARLY BIRD IS WRITTEN IN SEVEN PLACES, NOT ONE. Changing only the number would
leave a card charging full price while promising a $1,000 saving:

    .sof-promo span   sticky top bar, BOTH pages   GET EARLY BIRD TICKET & SAVE $1000
    .sof-cta span     hero button (x2)             GET EARLY BIRD TICKET
    .sof-tbanner b    gold strip on the card       LOWEST PRICE IT WILL EVER BE
    .sof-badges       the two pills                SAVE $1,000 / ENDS OCT 30
    .sof-tname        ticket name                  EARLY BIRD
    .sof-tprice       the price                    $1997
    .sof-tcompare     the struck-through price     $2997
    .sof-tbtn span    the card's button            GET EARLY BIRD TICKET

The countdown bar is an eighth, and it needs nothing: the page's own timer
script already removes it at zero.

NO FLASH. The script runs in <head>, so it cannot touch the body yet. It sets
a class on <html> immediately and the CSS holds the four bits of copy at
visibility:hidden -- hidden, not removed, so nothing moves -- until the swap
has run. Without that the old $1997 paints for a frame and then jumps.

THE PREVIEW SWITCH, which is the answer to "do we have a test site":

    ?eb=ended   forces the after state, whatever the clock says
    ?eb=live    forces the before state, for checking after the deadline

So Eline opens ...?eb=ended on the real page and sees exactly what visitors
will see tonight. Nobody else sees it and nothing is published early. It is
NOT remembered between pages on purpose -- a sticky preview is how a test
state leaks into a normal visit, which already caught us once on ?ref=.

TWO THINGS THIS DELIBERATELY DOES NOT DO:

1. IT DOES NOT TOUCH THE STRIPE LINK. Undecided as of this writing. If the
   price is bumped on the existing payment link in Stripe there is nothing to
   do. If a NEW link is made for $2997, its URL has to be added here or the
   page will say $2997 and the checkout will charge $1997.

2. IT DOES NOT CORRECT THE META PIXEL VALUE. AddToCart and InitiateCheckout
   carry value:1997 hardcoded in the page's own footer script, inside a
   closure this cannot reach. After the flip those two events under-report by
   $1000. Fixing it means a page redeploy, not a header write.

    py funnels/sof/scaling-or-failing/edits/wire_price_flip.py            dry run
    py funnels/sof/scaling-or-failing/edits/wire_price_flip.py --apply
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
MARK = "sof-price-flip"
APPLY = "--apply" in sys.argv
# --reinstall replaces a block already installed, for iterating on the copy or
# the layout. It cuts from the marker comment to the end of header_scripts,
# which is safe only because this block is appended LAST; the asserts below
# prove nothing else lives in what it is about to cut.
REINSTALL = "--reinstall" in sys.argv
PAGES = [
    "https://www.scalingorfailing.com/event/scaling-failing",
    "https://www.scalingorfailing.com/event/contact",
]

# Same instant as COUNTDOWN_ENDS in pagescore/build_sof_event.py.
ENDS = "2026-10-31T06:59:59Z"

# AGREED IN THE TEAM CHAT, 2026-10-30: 'so early bird --> "full access pass"',
# 'Button --> SECURE YOUR SEAT', and for "lowest price it will ever be",
# 'just say Limited seats'. The sticky top bar was not mentioned and follows
# the buttons.
#
# THE PILLS: ONE STAYS, AND IT HAS TO. Hiding both was the first attempt and
# Joshua's verdict was "feels empty" -- correct, and measurably so. The card's
# top is a three-row grid (pills / name / price) with the Scalizard spanning
# all three, and the sticker is TALLER than the name and price together. Hide
# the pills and the row does not collapse: the leftover height pools in it,
# leaving 90px of dead space above the title. Keeping one pill fills the row
# the design drew, and needs no CSS override at all -- measured 90px of gap
# down to 0. "SAVE $1,000" cannot stay, because it is false at full price, so
# the pill is rewritten instead and its "ENDS OCT 30" sibling is hidden.
AFTER_PRICE = "$2997"
AFTER_NAME = "FULL ACCESS PASS"
AFTER_BAR = "SECURE YOUR SEAT"           # sticky top bar, both pages
AFTER_BTN = "SECURE YOUR SEAT  →"   # hero button and the card's button
AFTER_BANNER = "LIMITED SEATS"           # the gold strip, keeps its tick
AFTER_PILL = "FINAL PRICE"               # the surviving pill. See above.

# THE BUTTONS KEEP THE EXISTING LINK. Joshua, 2026-10-31: "change of plans we
# would use the old link and eline would just change the product".
#
#     buy.stripe.com/3cIfZh0RM201aiyg01dby04     stays, on every button
#
# So the page is a pure copy change and Stripe is handled entirely by Eline on
# that one link. Nothing here has to stay in step with it.
#
# ⚠️ THIS IS NOW A HUMAN STEP ON A CLOCK, not an automatic one. The page
# switches to $2997 by itself at the deadline; the link does not. Until Eline
# has changed the product, the page asks $2997 and the checkout takes $1997.
#
# A General Admission link WAS supplied and wired for about ten minutes before
# the plan changed: buy.stripe.com/aFa4gz1VQ4893Ua157dby08, "SoF General
# Admission", $2,997.00. It is live and correct, and the affiliate codes work
# on it (JEM gave $2,547.45, the same 15%). If the plan changes back, the swap
# is in this file's git history and it swapped the URL PATH only, so an
# affiliate's ?prefilled_promo_code= survived it.

# The selectors whose TEXT changes, and what it becomes. Everything else is
# hidden by CSS, which needs no JavaScript and cannot flash.
# .sof-tbanner b, not .sof-tbanner: the strip keeps its tick icon.
# The pill is scoped through .sof-badges so it can never reach a .sof-badge
# somewhere else on the page.
SWAPS = [
    (".sof-badges .sof-badge:not(.sof-badge--urgent)", AFTER_PILL),
    (".sof-tbanner b", AFTER_BANNER),
    (".sof-promo span", AFTER_BAR),
    (".sof-cta span", AFTER_BTN),
    (".sof-tbtn span", AFTER_BTN),
    (".sof-tname", AFTER_NAME),
    (".sof-tprice", AFTER_PRICE),
]

SWAP_JS = ",".join("['%s','%s']" % (sel, txt) for sel, txt in SWAPS)

SCRIPT = """<!-- %s -->
<style>
/* %s: everything that only makes sense while Early Bird is running.
   display:none rather than a text swap, so these need no JavaScript at all
   and cannot flash. .sof-cd is belt and braces -- the page's own countdown
   script removes it at zero, this covers the frame before that runs.

   ONE PILL SURVIVES: .sof-badge--urgent ("ENDS OCT 30") goes, its sibling is
   rewritten. Hiding the whole .sof-badges row left 90px of dead space above
   the title, because the Scalizard spans all three grid rows and is taller
   than the name and price together, so the slack pools in the empty row. */
html.sof-eb-over .sof-cd,
html.sof-eb-over .sof-badge--urgent,
html.sof-eb-over .sof-tcompare{display:none!important}
/* The strings that CHANGE rather than disappear. Held invisible until
   the swap has run, or the old price paints for a frame and then jumps.
   visibility, not display: the box keeps its space, so nothing moves. */
html.sof-eb-over .sof-badges .sof-badge:not(.sof-badge--urgent),
html.sof-eb-over .sof-tbanner b,
html.sof-eb-over .sof-promo span,
html.sof-eb-over .sof-cta span,
html.sof-eb-over .sof-tbtn span,
html.sof-eb-over .sof-tname,
html.sof-eb-over .sof-tprice{visibility:hidden}
html.sof-eb-done .sof-badges .sof-badge:not(.sof-badge--urgent),
html.sof-eb-done .sof-tbanner b,
html.sof-eb-done .sof-promo span,
html.sof-eb-done .sof-cta span,
html.sof-eb-done .sof-tbtn span,
html.sof-eb-done .sof-tname,
html.sof-eb-done .sof-tprice{visibility:visible}
</style>
<script>
/* Early Bird ends -> the page shows the full price. Same instant the gold
   countdown bar counts to. ?eb=ended previews the after state on the live
   page; ?eb=live shows the before state once the deadline has passed. */
(function () {
  var END = Date.parse('%s');
  var root = document.documentElement;

  var over;
  try {
    var q = new URLSearchParams(window.location.search).get('eb');
    over = q === 'ended' ? true : (q === 'live' ? false : Date.now() >= END);
  } catch (e) { over = Date.now() >= END; }
  if (!over) return;

  /* Set BEFORE the body exists, so the CSS above is already holding the old
     copy invisible by the time any of it would paint. */
  root.className += ' sof-eb-over';

  var SWAPS = [%s];

  function apply() {
    for (var i = 0; i < SWAPS.length; i++) {
      var els = document.querySelectorAll(SWAPS[i][0]);
      for (var j = 0; j < els.length; j++) {
        /* Already right: skip, so this pass writes nothing to the DOM and
           cannot re-trigger the observer below. */
        if (els[j].textContent !== SWAPS[i][1]) els[j].textContent = SWAPS[i][1];
      }
    }
    /* The Stripe link is deliberately NOT touched. See the module note. */
    if (root.className.indexOf('sof-eb-done') < 0) root.className += ' sof-eb-done';
  }

  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', apply);
  else apply();

  /* LF hydrates its blocks from JSON after load and can replace these nodes,
     which would put $1997 back. Debounced to one run per frame, because an
     unthrottled document-wide observer running querySelectorAll is its own
     scroll-jank source on a page that is also running Lenis. */
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
</script>""" % (MARK, MARK, ENDS, SWAP_JS)

Q = 'query($id:ID!){node(id:$id){... on Funnel{name header_scripts}}}'
MUT = 'mutation($id:ID!,$node:InputFunnel!){updateFunnel(id:$id,node:$node){id}}'

tok = open(".session_token").read().strip()
h = lf_api.session_headers(open(".lf_account").read().strip())

node = lf_api.gql(tok, Q, {"id": FUNNEL}, extra_headers=h)["node"]
cur = node.get("header_scripts") or ""
print("funnel: %s" % node.get("name"))
print("header_scripts: %d chars" % len(cur))

original = cur
if MARK in cur:
    if not REINSTALL:
        sys.exit("Already installed (marker %r present). Pass --reinstall to "
                 "replace it." % MARK)
    i = cur.index("<!-- %s -->" % MARK)
    cut = cur[i:]
    # Everything else in this header must be BEFORE the cut, or this would
    # silently delete the Lenis block, the contact handler or the affiliate
    # rewrite along with it.
    # NOT "prefilled_promo_code": a previously installed price-flip block can
    # name it in its own comments, and then this guard fires on our own text.
    # "sof-affiliate-ref" is the affiliate block's unique marker and proves
    # the same thing without the false positive.
    for probe in ("lenis", "sof-contact-form -> n8n", "sof-affiliate-ref"):
        if probe in cut:
            sys.exit("ABORT: %r is inside the block this would cut. The "
                     "price-flip block is no longer last in header_scripts, "
                     "so --reinstall is not safe here." % probe)
    cur = cur[:i].rstrip()
    print("reinstall: removing the previous block (%d chars)" % len(cut))

# Every element this is about must actually be on the page, or the script is
# wiring nothing and would fail silently at midnight. Counted off the served
# HTML, which carries each block twice (rendered DOM + LF's JSON config), so
# the test is "present", not an exact count.
WANT = ['class="sof-promo"', 'class="sof-cta"', 'class="sof-tbanner"',
        'class="sof-badges"', 'class="sof-tname"', 'class="sof-tprice"',
        'class="sof-tcompare"', 'class="sof-tbtn"', 'data-cd-ends="%s"' % ENDS]
seen = set()
for url in PAGES:
    req = urllib.request.Request(url + "?cb=%d" % time.time(),
                                 headers={"User-Agent": "Mozilla/5.0",
                                          "Cache-Control": "no-cache"})
    html = urllib.request.urlopen(req, timeout=90).read().decode("utf-8", "replace")
    found = [w for w in WANT if w in html]
    seen.update(found)
    print("  %-62s %d/%d markers" % (url.split("//")[1], len(found), len(WANT)))
missing = [w for w in WANT if w not in seen]
assert not missing, "not on either page: %s" % ", ".join(missing)
print("  all %d markers present across the two pages" % len(WANT))

new = cur.rstrip() + "\n\n" + SCRIPT + "\n"
print("header_scripts: %d -> %d chars (+%d)" % (len(cur), len(new), len(new) - len(cur)))

# Nothing that is already there may move. The append is the only change.
assert new.startswith(cur.rstrip()), "the existing header was disturbed"
# NOT "prefilled_promo_code": this block's own comments name it now, so
# counting it compares two different things. "sof-affiliate-ref" is the
# affiliate block's unique marker and proves the same thing.
for probe in ("lenis", "sof-contact-form -> n8n", "sof-affiliate-ref",
              "sof-form"):
    assert new.count(probe) == cur.count(probe), "%s count changed" % probe
assert new.count(MARK) == 2  # the comment and the CSS note
assert new.count(ENDS) == 1

bak = os.path.abspath(os.path.join(HERE, "..", "header_scripts.pre-price-flip-%s.html"
                                   % time.strftime("%Y-%m-%d")))

if not APPLY:
    print("\nDRY RUN. Re-run with --apply to write.")
    print("After applying, check it WITHOUT waiting for midnight:")
    for url in PAGES:
        print("  %s?eb=ended" % url)
    sys.exit(0)

# `original`, not `cur`: on a --reinstall `cur` has already had the old block
# cut off it. And never overwrite -- the first backup is the only one that is
# genuinely pre-flip, and a same-day reinstall would replace it with a header
# that already carries the flip.
if os.path.exists(bak):
    print("backup kept (already exists) -> %s" % os.path.relpath(bak, ROOT))
else:
    with io.open(bak, "w", encoding="utf-8", newline="") as fh:
        fh.write(original)
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

print("\nThe flip is client side, so it does NOT show in this HTML.")
print("Check it in a browser:")
for url in PAGES:
    print("  %s?eb=ended" % url)
