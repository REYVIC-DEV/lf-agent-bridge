#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""V-A "health trackers for seniors" -- the A1 arm, "Warning + hidden cost".

  live   https://www.techunboxed.co/over-60s-health/best-health-tracker-over-60-v2
  funnel fun_Z6I8-bN5nVJ_SwGgR9WWK   (published; the V-B control keeps starting_step_id)
  run    va-a1-2026-09-29
  design cards 850:1015 (760 x 1125) and 850:1472 (390 x 1279)

A LEAD SWAP AND NOTHING ELSE. Everything from the "We tested:" list down is built by
pagescore/va_gadgets_shared.py -- the same call the control makes -- and
`verify_shared_identical()` fails the build if the two arms diverge outside the lead.

THE LEAD, as measured (desktop / 390):
  850:1019 / 1476  h1     Gelasio Bold  40/46  ->  28/32   #1a1a1a
  850:1020 / 1477  deck   Gelasio REGULAR 20/30 -> 17/26   #6b7078   <- carries £219
  850:605          byline Inter Regular 14/20              #6b7078   <- see DECISION 1
  hero                    the CONTROL's 720x405 image      <- see DECISION 2
  850:1024 / 1481  para   Inter BOLD    18/31              #1a1a1a
  850:1025 / 1482  para   Inter Regular 18/31              #2b2e33   <- £219 £79.99 £9.99 £440
  850:1026 / 1483  para   Inter Regular 18/31              #2b2e33
  850:1027 / 1484  para   Inter Regular 18/31              #2b2e33
  850:1028 / 1485  para   Inter Regular 18/31              #2b2e33   <- £79 (our product)

NOT BUILT -- Figma annotations, not page content:
  850:1016/1473  the `angle` chip ("A1 · WARNING + HIDDEN COST (FROM TEST)", 12px Inter
                 Bold, 6% letter-spacing, red #e2483d on #f5f6f7, radius 4)
  850:1018/1475  the 1px rule directly under it
  850:1022/1479  the grey "FEATURED IMAGE" placeholder label
  Shipping the chip would put a FROM-TEST badge on a live advertorial.

-------------------------------------------------------------------------------------
DECISIONS
-------------------------------------------------------------------------------------
1. THE BYLINE IS KEPT, between the deck and the hero. The A1 card has none, but it is
   a LEAD CARD, not a page -- it also omits the support bar, logo, nav, promo bar,
   breadcrumb and footer, all of which obviously still ship. The brief for this test
   names three changes (headline, subhead, first five paragraphs); dropping the author
   attribution would be a fourth, and removing it from ONE arm would make the test
   measure lead angle and author credibility at once. The order h1 -> deck -> byline is
   read off V-A's own designed 390 page (850:1059 wrapper, then byline 850:1062), not
   invented. Same call as the V-B/B5 pair, for the same reasons.

2. THE HERO IS THE CONTROL'S, ON THE COORDINATOR'S EXPLICIT INSTRUCTION -- and that
   instruction's premise does not hold, so here is the evidence rather than a silent
   choice. The A1 card has its OWN hero (850:1023, "ChatGPT Image Sep 25, 2026,
   01_17_40 AM 1") at 720x336, and it is a genuinely different photograph from the
   control's 850:606 ("...Sep 24, 2026, 11_31_17 PM 1", 720x405): mean per-channel
   difference 47.2/255, the same magnitude as the B5-vs-control pair that was
   definitively a different shot. Same subject and arrangement (four trackers on two
   older wrists), different setting -- the control's is indoors on a wooden table, A1's
   is outdoors against foliage and paving.
   Built as instructed, with the control's asset AND the control's 720x405 ratio, since
   cropping the control image to 336 would match neither design. Switching to A1's own
   hero is a one-line change; flagged in the report.

3. NOT THE ENTRY PAGE. `make_starting=False`, and the shared writer asserts afterwards
   that `starting_step_id` still points at the V-B control.
"""
import sys, os
sys.path.insert(0, '.')
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from va_gadgets_shared import (
    C, h, text, title, hero_picture, assemble, verify, verify_shared_identical,
    build_head, deploy, copy_html, IMG, SERIF, INK, BODY, META, PAGE_BASE,
)

STEP_SLUG = "best-health-tracker-over-60-v2"
PAGE_URL = PAGE_BASE + STEP_SLUG
CONTROL_URL = PAGE_BASE + "best-health-tracker-over-60"

# ------------------------------------------------------------------ the lead
LEAD = [
    title(h(C["850:1019"]), "40px", "46px", level="1", font=SERIF, color=INK,
          m={"fontSize": "28px", "lineHeight": "32px"}),
    # deck -- Gelasio REGULAR, grey, and it carries a money figure
    text(copy_html("850:1020"), size="20px", lh="30px", color=META, font=SERIF,
         m={"fontSize": "17px", "lineHeight": "26px"}),
    # byline -- carried over from the control unchanged; see DECISION 1
    text(h(C["850:605"]), size="14px", lh="20px", color=META),
    # the control's hero, at the control's ratio and radius 0; see DECISION 2
    hero_picture("va_hero", (720, 405), radius="0px"),
    text(h(C["850:1024"]), weight="700", color=INK),
    text(copy_html("850:1025"), color=BODY),
    text(h(C["850:1026"]), color=BODY),
    text(h(C["850:1027"]), color=BODY),
    text(copy_html("850:1028"), color=BODY),
]

# ------------------------------------------------------------------ assemble
body = assemble(LEAD, PAGE_URL)

# The A1 lead adds money the control lead does not have, so the inventory differs from
# the control's by exactly those figures:
#   price   9 = the control's 8, plus £79 in 850:1028
#   compare 4 = unchanged (all in the shared half)
#   fx     22 = the control's 17, plus £219 in the deck (1020) and
#               £219/£79.99/£9.99/£440 in 850:1025
verify(body, (9, 4, 22))
verify_shared_identical(CONTROL_URL, PAGE_URL)

TITLE = "Over 55? Read This Before You Buy A Smartwatch"
OG = IMG["og_va"]        # the control's hero, per DECISION 2
SEO = {
    "title": TITLE,
    "description": ("The sticker price is not the real price. We wore five health "
                    "trackers for a month each and worked out what you actually pay, "
                    "and what you actually keep using."),
    "keywords": ("best health tracker for seniors, smartwatch hidden cost, health "
                 "tracker over 60, HLTH Band, Fitbit Premium cost, Oura membership, "
                 "no subscription fitness tracker, easy to use health tracker"),
    "social_image_uid": OG["src_uid"],
}
# lenis=True: desktop-only smooth scroll, in this STEP's own footer custom_html.
CUSTOM_HTML = build_head(SEO, OG, "va_hero")

if "--dry" in sys.argv:
    print("DRY RUN -- body built and checked, nothing written.")
    sys.exit(0)

deploy(STEP_SLUG, TITLE, SEO, body, CUSTOM_HTML, {"x": 480, "y": 320}, make_starting=False)
print("LIVE  ", PAGE_URL)
