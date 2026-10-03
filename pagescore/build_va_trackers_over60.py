#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""V-A "health trackers for seniors" -- the CONTROL arm.

  live   https://www.techunboxed.co/over-60s-health/best-health-tracker-over-60
  funnel fun_Z6I8-bN5nVJ_SwGgR9WWK   (published; the V-B control keeps starting_step_id)
  run    va-control-2026-09-29
  design frame 850:562 (1440 x 12623) + its OWN 390 frame 850:1029 (390 x 13679)

Only the LEAD lives here; everything from the "We tested:" list down is built by
pagescore/va_gadgets_shared.py, the same call the A1 arm makes.

THE LEAD (what A1 swaps out), desktop / 390:
  850:602          wrapper   VERTICAL gap 8
   |- 850:603/1060 h1        Gelasio Bold 40/46 -> 28/32     #1a1a1a
   |- 850:604/1061 sub-deck  Inter   Bold 32/46 -> 24/28     #1a1a1a   (Inter, not Gelasio)
  850:605          byline    Inter Regular 14/20             #6b7078
                             -- seven multi-space runs (3,3,2,2,2,2,3); h() keeps them
  850:606          hero      a BARE RECTANGLE, 720x405 (16:9) at radius **0**, FILL.
                             Every product image is 16:9 too and sits at radius 6; the
                             hero does not. Reproduced as measured.
  850:607          para      Inter BOLD    18/31             #1a1a1a
  850:608          para      Inter Regular 18/31             #2b2e33
  850:609          para      Inter BOLD    18/31             #1a1a1a -- carries the only
                             CURLY quotes on the page, U+201C/U+201D, with a STRAIGHT
                             apostrophe inside. Copy comes from va_copy.py, so exact.
  850:610, 850:611 para      Inter Regular 18/31             #2b2e33

RUNNING IT
  python3 pagescore/build_va_trackers_over60.py --dry     build + check, write nothing
  python3 pagescore/build_va_trackers_over60.py           deploy

This page is NOT the funnel's entry page -- the V-B control keeps that, and the shared
writer asserts it after every mutation.
"""
import sys, os
sys.path.insert(0, '.')
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from va_gadgets_shared import (
    C, h, text, title, hero_picture, assemble, verify, verify_shared_identical,
    build_head, deploy, col, IMG, SERIF, SANS, INK, BODY, META, PAGE_BASE,
)

STEP_SLUG = "best-health-tracker-over-60"
PAGE_URL = PAGE_BASE + STEP_SLUG
A1_URL = PAGE_BASE + "best-health-tracker-over-60-v2"   # for the shared-body proof

# ------------------------------------------------------------------ the lead
LEAD = [
    # the h1 wrapper: its own 8px gap, tighter than the column's 20
    col([
        title(h(C["850:603"]), "40px", "46px", level="1", font=SERIF, color=INK,
              m={"fontSize": "28px", "lineHeight": "32px"}),
        title(h(C["850:604"]), "32px", "46px", level="2", font=SANS, color=INK,
              m={"fontSize": "24px", "lineHeight": "28px"}),
    ], gap="8px"),
    text(h(C["850:605"]), size="14px", lh="20px", color=META),
    hero_picture("va_hero", (720, 405), radius="0px"),
    text(h(C["850:607"]), weight="700", color=INK),
    text(h(C["850:608"]), color=BODY),
    text(h(C["850:609"]), weight="700", color=INK),
    text(h(C["850:610"]), color=BODY),
    text(h(C["850:611"]), color=BODY),
]

# ------------------------------------------------------------------ assemble
body = assemble(LEAD, PAGE_URL)

# The control's LEAD carries no money at all, so every tagged figure below comes from
# the shared half. Inventoried off the nodes, then asserted -- finding an untagged
# figure after launch is the failure mode this counts against.
#   price   8 = promo bar, 640, 802, 812, 821 (offer CTA), 822, 948, 1011
#   compare 4 = promo bar, 640, 812, 1011
#   fx     17 = 675(2) 681(1) 691(3) 709(1) 743(1) 744(3) 750(1) 760(1)
#               776(1) 777(1) 794(1) 924(1)
verify(body, (8, 4, 17))
verify_shared_identical(PAGE_URL, A1_URL)

TITLE = "We Tested The 5 Top-Rated Health Trackers For Seniors"
OG = IMG["og_va"]        # 1200x630, cut from this page's own hero
SEO = {
    "title": TITLE,
    "description": ("Five top-rated health trackers, a month each, worn day and night by "
                    "people over 60. See which one they kept wearing, and what each one "
                    "really costs."),
    "keywords": ("best health tracker for seniors, health tracker over 60, HLTH Band, "
                 "Oura Ring 4, Apple Watch SE 3, Fitbit Charge 6, Garmin Vivoactive 6, "
                 "no subscription fitness tracker, easy to use health tracker"),
    "social_image_uid": OG["src_uid"],
}
# lenis=True: desktop-only smooth scroll, in this STEP's own footer custom_html.
CUSTOM_HTML = build_head(SEO, OG, "va_hero")

if "--dry" in sys.argv:
    print("DRY RUN -- body built and checked, nothing written.")
    sys.exit(0)

deploy(STEP_SLUG, TITLE, SEO, body, CUSTOM_HTML, {"x": 480, "y": 90}, make_starting=False)
print("LIVE  ", PAGE_URL)
