#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""V-B "Health gadgets for over-60s" -- the B5 arm, "The one question".

  live   https://www.techunboxed.co/over-60s-health/best-health-gadgets-over-60-v2
  funnel fun_Z6I8-bN5nVJ_SwGgR9WWK  (published; the CONTROL keeps starting_step_id)
  run    vb-b5-2026-09-29
  design Figma card 850:1943 (760 x 1109) + 850:1957 (390 x 1280), via figwright

A LEAD SWAP AND NOTHING ELSE. Everything from the "We tested:" list down is built by
pagescore/vb_gadgets_shared.py, the same call the control makes, and
`verify_shared_identical()` fails the build if the two arms ever diverge outside the
lead. That is the only way an A/B test stays a one-variable experiment.

THE LEAD, as measured off the card (desktop / 390):
  850:1947 / 1961  h1     Gelasio Bold  40/46  ->  28/32     #1a1a1a
  850:1948 / 1962  deck   Gelasio REGULAR 20/30 -> 17/26     #6b7078   <- NEW vs control
  850:1528         byline Inter Regular 14/20                #6b7078   <- see DECISION 1
  850:1949 / 1963  hero   720x336 at BOTH widths (the 390 card's inner rect carries
                          targetAspectRatio 720:336 too), radius 6, scaleMode FILL
  850:1952 / 1966  para   Inter BOLD    18/31                #1a1a1a
  850:1953 / 1967  para   Inter BOLD    18/31                #1a1a1a
  850:1954 / 1968  para   Inter Regular 18/31                #2b2e33
  850:1955 / 1969  para   Inter Regular 18/31                #2b2e33
  850:1956 / 1970  para   Inter Regular 18/31                #2b2e33

NOT BUILT -- Figma annotations, not page content:
  850:1944/1958  the `angle` chip ("B5 · THE ONE QUESTION", 12px Inter Bold, 6%
                 letter-spacing, red #e2483d on #f5f6f7, radius 4)
  850:1946/1960  the 1px rule directly under it
  850:1950/1964  the grey "FEATURED IMAGE" placeholder label, which the real image
                 rectangle covers anyway
  Shipping the chip would put a "FROM TEST" badge on a live advertorial.

-------------------------------------------------------------------------------------
DECISIONS -- what the B5 card left open
-------------------------------------------------------------------------------------
1. THE BYLINE IS KEPT, and sits between the deck and the hero.

   The B5 card has no byline. But it is a LEAD CARD, not a page: it is the only other
   frame in the section besides the full control page, so there is no sibling card to
   read a convention from, and the card also omits every other piece of page chrome
   (support bar, logo, nav, promo bar, breadcrumb, footer) which obviously still ships.

   Three things decide it:
     * The brief for this test names exactly three changes -- headline, subhead, first
       five paragraphs. Dropping the author attribution is a fourth.
     * Removing the byline from ONE arm would make the test measure lead angle AND
       author credibility at once, which is precisely what an A/B test must not do.
     * V-A's designed 390 PAGE (850:1029), the same template, has h1 -> deck -> byline
       -> hero in that order (850:1059 wrapper, then byline 850:1062). That is a
       measured precedent for where a deck and a byline coexist, so the order here is
       read off a real page rather than invented.

   Flagged in the report as the one genuinely ambiguous call on this card.

2. THE DECK IS GELASIO **REGULAR**, not Inter and not Bold. V-A's mobile deck is Inter
   Bold 24/28; B5's is Gelasio Regular 20/30 desktop, 17/26 at 390, in #6b7078. Node
   names carry no "set family to ..." instruction, so the applied font is the intended
   one -- built as measured, not as the sibling variant does it.

3. ONE HERO ASSET, NO ART DIRECTION. The control needs two files because its hero is
   1.94:1 on desktop and 16:9 at 390. B5's is 720:336 at BOTH breakpoints (the 390
   card's rectangle 850:1965 keeps targetAspectRatio 720:336), so one file is correct
   and a second would be waste. The image itself is a DIFFERENT photograph from the
   control's -- confirmed by pixel diff (mean 48.9/255), not by trusting the filename.

4. NOT THE ENTRY PAGE. `deploy(..., make_starting=False)` and the shared writer asserts
   afterwards that `starting_step_id` still points at the control.
"""
import sys, os
sys.path.insert(0, '.')
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from vb_gadgets_shared import (
    C, h, text, title, hero_picture, assemble, verify, verify_shared_identical,
    build_head, deploy, IMG, SERIF, INK, BODY, META, PAGE_BASE,
)

STEP_SLUG = "best-health-gadgets-over-60-v2"
PAGE_URL = PAGE_BASE + STEP_SLUG
CONTROL_URL = PAGE_BASE + "best-health-gadgets-over-60"

# ------------------------------------------------------------------ the lead
LEAD = [
    # the page's ONLY h1
    title(h(C["850:1947"]), "40px", "46px", level="1", font=SERIF, color=INK,
          m={"fontSize": "28px", "lineHeight": "32px"}),
    # deck -- Gelasio Regular, grey; see DECISION 2
    text(h(C["850:1948"]), size="20px", lh="30px", color=META, font=SERIF,
         m={"fontSize": "17px", "lineHeight": "26px"}),
    # byline -- carried over from the control unchanged; see DECISION 1
    text(h(C["850:1528"]), size="14px", lh="20px", color=META),
    hero_picture("featured_b5", (720, 336)),
    text(h(C["850:1952"]), weight="700", color=INK),
    text(h(C["850:1953"]), weight="700", color=INK),
    text(h(C["850:1954"]), color=BODY),
    text(h(C["850:1955"]), color=BODY),
    text(h(C["850:1956"]), color=BODY),
]

# ------------------------------------------------------------------ assemble
body = assemble(LEAD, PAGE_URL)

# Identical inventory to the control: the B5 lead contains no money figure at all
# (checked against the card -- no £ in any of 850:1947..1956), so all 28 tagged
# figures come from the shared half.
verify(body, (8, 4, 16))
verify_shared_identical(CONTROL_URL, PAGE_URL)

TITLE = "Before You Buy A Health Gadget For Someone Over 60"
OG = IMG["og_b5"]        # 1200x630, cut from B5's own hero
SEO = {
    "title": TITLE,
    "description": ("One question sorts every health gadget for an older parent, and it "
                    "is not accuracy. We gave five to testers aged 60 to 82 for a month "
                    "and scored only that."),
    "keywords": ("health gadgets for over 60s, best health gadget for elderly parents, "
                 "HLTH Band, Withings Sleep Analyzer, Oura Ring 4, fall alarm, "
                 "pulse oximeter, no subscription health tracker, easy to use health tracker"),
    "social_image_uid": OG["src_uid"],
}
CUSTOM_HTML = build_head(SEO, OG, "featured_b5")

if "--dry" in sys.argv:
    print("DRY RUN -- body built and checked, nothing written.")
    sys.exit(0)

# make_starting stays False: the control is the funnel's entry page (DECISION 4).
deploy(STEP_SLUG, TITLE, SEO, body, CUSTOM_HTML, {"x": 90, "y": 320}, make_starting=False)
print("LIVE  ", PAGE_URL)
