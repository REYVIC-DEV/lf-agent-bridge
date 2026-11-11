#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Write the post-Early-Bird page into the page itself, and retire the script.

JOSHUA, 2026-10-31, once the deadline had passed and the flip was live:
"now that it is live we can change it so it does not apply with script but a
permanent change", and "countdown is done we can make it permanent now".

Up to now the General Admission page was produced at runtime: the page shipped
Early Bird markup and a header script rewrote six strings on every load. That
was the right shape while the change was in the FUTURE and had to happen by
itself at an exact instant. It is the wrong shape now that the instant has
passed -- the real copy is the copy, and a visitor should not need JavaScript
to be told the right price.

WHAT THIS WRITES INTO BOTH STEP BODIES

    LOWEST PRICE IT WILL EVER BE   ->  LIMITED SEATS
    SAVE $1,000                    ->  FINAL PRICE
    ENDS OCT 30                    ->  removed, the pill element and all
    EARLY BIRD (ticket name)       ->  FULL ACCESS PASS
    $1997                          ->  $2997
    $2997 struck through           ->  removed, the element and all
    GET EARLY BIRD TICKET          ->  SECURE YOUR SEAT   (3 buttons)
    GET EARLY BIRD TICKET & SAVE $1000 -> SECURE YOUR SEAT (sticky bar, both pages)
    the gold countdown bar         ->  removed, both pages

THE STRIPE LINK IS NOT TOUCHED. Joshua's call on 2026-10-31: the buttons keep
`buy.stripe.com/3cIfZh0RM201aiyg01dby04` and Eline reprices that one link in
Stripe. Nothing here depends on when she does it.

THE COUNTDOWN IS CUT PER STEP, NOT BY A SHARED CONSTANT. The two pages carry
DIFFERENT countdown markup: the digits are rendered at build time, so the
landing page says 36 MIN 09 SEC and contact says 35 MIN 29 SEC. A single
hardcoded `old` string would have silently matched one page and missed the
other, which is exactly how the deadline move went wrong on 2026-10-30. So the
string is extracted from each body and removed from that body.

Only the `.sof-cd` div goes, not its section, which is what the runtime script
has been doing all along and is already proven to leave no visible band: the
gold is painted on `.sof-cd` itself and the section's padding is zero.

ORDER MATTERS, AND IT IS SAFE IN THIS ORDER ONLY. Bodies first, then the
served HTML is checked, and the header script is removed ONLY if that check
passed. The other way round there would be a window where the body still said
Early Bird and nothing was left to correct it. While both are in place they
agree, so there is no visible moment of change.

⚠️ `?eb=ended` AND `?eb=live` DIE WITH THE SCRIPT. They were there to preview
an unreleased state. There is no unreleased state now.

⚠️ ALSO NEEDS DOING, NOT BY THIS SCRIPT: pagescore/build_sof_event.py still
generates the Early Bird copy, so a rebuild would undo all of this. Its
countdown already self-disables past the deadline; the copy does not.

    py funnels/sof/scaling-or-failing/edits/bake_general_admission.py            dry run
    py funnels/sof/scaling-or-failing/edits/bake_general_admission.py --apply
"""
import json
import os
import re
import sys
import time
import urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", "..", "..", ".."))
sys.path.insert(0, ROOT)
os.chdir(ROOT)
import lf_api  # noqa: E402

FUNNEL = "fun_RoOL_WXDCAxK4hEk0v5xX"
FLIP_MARK = "sof-price-flip"
APPLY = "--apply" in sys.argv

RARR = u"→"
PAGES = {
    "scaling-failing": "https://www.scalingorfailing.com/event/scaling-failing",
    "contact": "https://www.scalingorfailing.com/event/contact",
}

# (old, new, how many times it must appear in THAT step's body)
PAIRS = {
    "scaling-failing": [
        ("<b>LOWEST PRICE IT WILL EVER BE</b>", "<b>LIMITED SEATS</b>", 1),

        # The whole pill row, because one pill LEAVES and the other is
        # rewritten. "SAVE $1,000" cannot simply be reworded in place without
        # also dropping its --urgent sibling, and doing both in one exact
        # string is what makes the result provable.
        ('<div class="sof-badges"><span class="sof-badge">SAVE $1,000</span>'
         '<span class="sof-badge sof-badge--urgent">ENDS OCT 30</span></div>',
         '<div class="sof-badges"><span class="sof-badge">FINAL PRICE</span></div>', 1),

        ('<p class="sof-tname">EARLY BIRD</p>',
         '<p class="sof-tname">FULL ACCESS PASS</p>', 1),

        # The whole price row: $1997 becomes $2997 AND the struck-through
        # compare price leaves. Same reasoning as the pills.
        ('<div class="sof-tpricerow"><p class="sof-tprice">$1997</p>'
         '<p class="sof-tcompare"><span class="sof-vh">Was </span>$2997</p></div>',
         '<div class="sof-tpricerow"><p class="sof-tprice">$2997</p></div>', 1),

        # THREE buttons share this exact label: the ticket card's and the two
        # hero CTAs (one per breakpoint). All three are meant to change.
        ("<span>GET EARLY BIRD TICKET  %s</span>" % RARR,
         "<span>SECURE YOUR SEAT  %s</span>" % RARR, 3),

        ("<span>GET EARLY BIRD TICKET &amp; SAVE $1000</span>",
         "<span>SECURE YOUR SEAT</span>", 1),
    ],
    "contact": [
        ("<span>GET EARLY BIRD TICKET &amp; SAVE $1000</span>",
         "<span>SECURE YOUR SEAT</span>", 1),
    ],
}

# Non-greedy, and the first </span></span></div> closes sof-cd-u, then
# sof-cd-units, then sof-cd itself. The section around it stays.
CD = re.compile(r'<div class="sof-cd" data-cd-ends="[^"]*">.*?</span></span></div>',
                re.S)

Q = 'query($id:ID!){node(id:$id){... on Funnel{name header_scripts}}}'
MUT = 'mutation($id:ID!,$node:InputFunnel!){updateFunnel(id:$id,node:$node){id}}'

tok = open(".session_token").read().strip()
h = lf_api.session_headers(open(".lf_account").read().strip())

funnel = lf_api.get_funnel_steps(tok, FUNNEL, extra_headers=h)
print("funnel %s" % funnel.get("name"))

plan = []
for slug, pairs in PAIRS.items():
    step = next(s for s in funnel["steps"] if s.get("slug") == slug)
    blob = json.dumps(step["body"])
    raw = blob.encode().decode("unicode_escape")
    print("\n--- %s (%s)" % (slug, step["uid"]))

    todo = []
    for old, new, want in pairs:
        n = raw.count(old)
        if n == 0 and raw.count(new):
            print("  already done : %s" % old[:58])
            continue
        if n != want:
            sys.exit("ABORT: %r appears %d times in %s, expected %d"
                     % (old[:58], n, slug, want))
        print("  %d x %s" % (n, old[:58]))
        todo.append((old, new))

    cds = CD.findall(raw)
    if cds:
        if len(cds) != 1:
            sys.exit("ABORT: %d countdown bars in %s, expected 1" % (len(cds), slug))
        print("  1 x countdown bar (%d chars) -> removed" % len(cds[0]))
        todo.append((cds[0], ""))
    else:
        print("  countdown bar: already gone")

    if todo:
        plan.append((slug, step, todo))

cur = lf_api.gql(tok, Q, {"id": FUNNEL}, extra_headers=h)["node"]["header_scripts"] or ""
drop_script = FLIP_MARK in cur
if drop_script:
    i = cur.index("<!-- %s -->" % FLIP_MARK)
    cut = cur[i:]
    for probe in ("lenis", "sof-contact-form -> n8n", "sof-affiliate-ref"):
        if probe in cut:
            sys.exit("ABORT: %r is inside the block this would cut." % probe)
    new_scripts = cur[:i].rstrip() + "\n"
    print("\nheader_scripts: %d -> %d chars (the %s block goes)"
          % (len(cur), len(new_scripts), FLIP_MARK))
else:
    print("\nheader_scripts: no %s block, nothing to remove" % FLIP_MARK)

if not plan and not drop_script:
    sys.exit("Nothing to do.")
if not APPLY:
    sys.exit("\nDRY RUN. Re-run with --apply to write.")

# ---- 1. bodies ----------------------------------------------------------
for slug, step, todo in plan:
    bak = os.path.abspath(os.path.join(
        HERE, "..", "steps", "%s.pre-bake-ga-%s.json" % (slug, time.strftime("%Y-%m-%d"))))
    if not os.path.exists(bak):
        open(bak, "w", encoding="utf-8").write(json.dumps(step["body"], indent=2))
        print("backup -> %s" % os.path.relpath(bak, ROOT))
    r = lf_api.edit_step_bodies(tok, FUNNEL, todo, extra_headers=h,
                                force=True, step_uids=[step["uid"]])
    print("%s written: %d step(s)" % (slug, r.get("steps_changed")))
    if r.get("steps_changed") != 1:
        sys.exit("ABORT: expected 1 step changed for %s, got %r" % (slug, r.get("steps_changed")))

# ---- 2. prove it on the real pages BEFORE retiring the script -----------
time.sleep(10)
# ⚠️ ELEMENT-PRECISE, NOT PLAIN TEXT. The first run of this checked for bare
# "$1997", "SAVE $1,000", "ENDS OCT 30" and "sof-cd-units" and reported all
# four still present on BOTH pages -- including "$1997" on contact, which has
# no ticket card at all. Every one was a COMMENT: two in the flip script's own
# explanation of what it replaces, one in the page's CSS note deriving 1997 +
# 1000 = 2997, and the countdown's CSS rules, which are harmless once no
# element uses them. The body edits had in fact landed perfectly. A served
# page carries its own stylesheet and scripts, so grepping it for a bare
# string tests the commentary as much as the content.
GONE = ["LOWEST PRICE IT WILL EVER BE", ">SAVE $1,000<", ">ENDS OCT 30<",
        ">EARLY BIRD<", ">$1997<", "GET EARLY BIRD TICKET  ",
        # Not "data-cd-ends": the page's own footer script READS that
        # attribute by name and keeps doing so harmlessly once no element
        # carries it. Same trap as the four above. This matches the element.
        'class="sof-cd"']
HERE_NOW = {"scaling-failing": ["LIMITED SEATS", "FINAL PRICE", "FULL ACCESS PASS",
                                "$2997", "SECURE YOUR SEAT"],
            "contact": ["SECURE YOUR SEAT"]}
ok = True
for slug, url in PAGES.items():
    page = urllib.request.urlopen(urllib.request.Request(
        url + "?cb=%d" % time.time(),
        headers={"User-Agent": "Mozilla/5.0", "Cache-Control": "no-cache"}),
        timeout=90).read().decode("utf-8", "replace")
    print("\n%s" % url)
    for s in HERE_NOW[slug]:
        good = s in page
        ok &= good
        print("  present %-24s %s" % (s, good))
    for s in GONE:
        good = s not in page
        ok &= good
        print("  gone    %-24s %s" % (s, good))

if not ok:
    sys.exit("\nABORT: the pages do not read right yet, so the script STAYS. "
             "Nothing was removed. Fix the body, re-run.")

# ---- 3. only now, retire the script -------------------------------------
if drop_script:
    bak = os.path.abspath(os.path.join(
        HERE, "..", "header_scripts.pre-bake-ga-%s.html" % time.strftime("%Y-%m-%d")))
    if not os.path.exists(bak):
        open(bak, "w", encoding="utf-8").write(cur)
        print("\nbackup -> %s" % os.path.relpath(bak, ROOT))
    lf_api.gql(tok, MUT, {"id": FUNNEL, "node": {"header_scripts": new_scripts}},
               extra_headers=h)
    back = lf_api.gql(tok, Q, {"id": FUNNEL}, extra_headers=h)["node"]["header_scripts"] or ""
    assert back == new_scripts, "read-back differs from what was sent"
    print("header_scripts written and read back identical.")

    time.sleep(8)
    for slug, url in PAGES.items():
        page = urllib.request.urlopen(urllib.request.Request(
            url + "?cb=%d" % time.time(),
            headers={"User-Agent": "Mozilla/5.0", "Cache-Control": "no-cache"}),
            timeout=90).read().decode("utf-8", "replace")
        print("  %-62s flip script gone: %s"
              % (url.split("//")[1], FLIP_MARK not in page))

print("\nThe page now says it outright. No JavaScript involved.")
