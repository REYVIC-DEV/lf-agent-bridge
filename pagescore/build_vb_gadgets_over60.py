#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""V-B "Health gadgets for over-60s" -- the CONTROL arm.

  live   https://www.techunboxed.co/over-60s-health/best-health-gadgets-over-60
  funnel fun_Z6I8-bN5nVJ_SwGgR9WWK  (published; this step is its starting_step_id)
  run    vb-control-2026-09-29
  design Figma frame 850:1487, 1440 x 13029, read through figwright

This file is now only the LEAD. Everything from the "We tested:" list down lives in
pagescore/vb_gadgets_shared.py and is built identically for the B5 arm -- see that
module's docstring for why, and `verify_shared_identical()` for the proof that runs on
every build.

THE LEAD (what the B5 arm swaps out):
  850:1527  h1        Gelasio Bold 40/46 -> 28/32 at 390 (V-A 850:1060)
  850:1528  byline    Inter Regular 14/20 #6b7078; its multi-space runs are visual, so
                      h() converts them to &nbsp; rather than letting HTML collapse them
  850:1529  hero      720x371 (1.94:1) desktop, 16:9 at 390 -> two assets, art-directed
  850:1532  intro     Inter BOLD 18/31 #1a1a1a
  850:1533-1537       Inter Regular 18/31 #2b2e33, five paragraphs

RUNNING IT
  python3 pagescore/build_vb_gadgets_over60.py --dry     build + check, write nothing
  python3 pagescore/build_vb_gadgets_over60.py           deploy

This page is LIVE, so the guard refuses a rebuild unless a human authorises this one
slug: LF_ALLOW_REDEPLOY=best-health-gadgets-over-60. Never set that from an agent.

KNOWN, MEASURED, NOT WORTH ANOTHER CYCLE (carried in the session note):
  * The comment text column is 662px live where the design says 640. `maxWidth` IS set
    in comment_row(); Lightfunnels does not apply that style prop on this container.
    One comment wraps to 1 line where the design wraps to 2 -- the single remaining
    design_diff RESTYLED.
  * The img[title=""] CLS reservation never reaches document.styleSheets. It does not
    matter: real CLS measured with a PerformanceObserver across a full-page scroll is
    0, with zero layout shifts and all seven photos loading. LF's own classes already
    reserve the box. Left in place, inert; do not chase it.
"""
import sys, os
sys.path.insert(0, '.')
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from vb_gadgets_shared import (
    C, h, text, title, hero_picture, assemble, verify, verify_shared_identical,
    build_head, deploy, IMG, SERIF, INK, META, PAGE_BASE,
)

STEP_SLUG = "best-health-gadgets-over-60"
PAGE_URL = PAGE_BASE + STEP_SLUG
B5_URL = PAGE_BASE + "best-health-gadgets-over-60-v2"   # for the shared-body proof

# ------------------------------------------------------------------ the lead
LEAD = [
    # the page's ONLY h1
    title(h(C["850:1527"]), "40px", "46px", level="1", font=SERIF, color=INK,
          m={"fontSize": "28px", "lineHeight": "32px"}),
    text(h(C["850:1528"]), size="14px", lh="20px", color=META),
    hero_picture("featured", (720, 371), "featured_mobile", (16, 9)),
    text(h(C["850:1532"]), weight="700", color=INK),
] + [text(h(C[i])) for i in ("850:1533", "850:1534", "850:1535", "850:1536", "850:1537")]

# ------------------------------------------------------------------ assemble
body = assemble(LEAD, PAGE_URL)

# price 8 = promo bar, 1566, 1730, 1740, 1749 (offer CTA), 1750, 1876, 1939
# compare 4 = promo bar, 1566, 1740, 1939
# fx 16 = 1601,1620 (1 ea) 1636 (2) 1652 (3) 1670,1687 (2 ea) 1705,1716 (1 ea) 1939 (3)
# The control's LEAD carries no money figures, so these are all from the shared half.
verify(body, (8, 4, 16))
verify_shared_identical(PAGE_URL, B5_URL)

TITLE = "Best Health Gadgets for Over-60s: 5 Tested for a Month"
OG = IMG["og_vb"]        # 1200x630, cut from this page's own featured image
SEO = {
    "title": TITLE,
    "description": ("We gave five top-rated health gadgets to testers aged 60 to 82 for a "
                    "month, with no manuals and no help. See which one they were all "
                    "still using at the end."),
    "keywords": ("health gadgets for over 60s, best health gadget for elderly parents, "
                 "HLTH Band, Withings Sleep Analyzer, Oura Ring 4, fall alarm, "
                 "pulse oximeter, no subscription health tracker, easy to use health tracker"),
    "social_image_uid": OG["src_uid"],
}
CUSTOM_HTML = build_head(SEO, OG, "featured", "featured_mobile")

if "--dry" in sys.argv:
    print("DRY RUN -- body built and checked, nothing written.")
    sys.exit(0)

# This page IS the funnel's entry page, so it keeps starting_step_id.
deploy(STEP_SLUG, TITLE, SEO, body, CUSTOM_HTML, {"x": 90, "y": 90}, make_starting=True)
print("LIVE  ", PAGE_URL)
