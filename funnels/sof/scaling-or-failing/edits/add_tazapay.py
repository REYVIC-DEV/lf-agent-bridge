#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Add Tazapay as a fourth sponsor, in the marquee and on the partner row.

JOSHUA, 2026-11-02: "taza pay logo added new frame pasted on figma".

The frame is "Scaling Or Failing V2" 1033:3 (1440w 1033:4, 390w 1033:712).
It is the SAME frame shape as 2026-10-31's, with one brand added in the two
places sponsors appear:

  marquee   1033:103 desktop / 1033:806 mobile
            was bf / suits / outcraft, now bf / suits / outcraft / TAZAPAY
  partners  1033:653 desktop / 1033:1344 mobile
            was a row of TWO plates, now THREE

⚠️ DESKTOP VALUES ARE THE 1440 FRAME'S x 4/3, as every other value in these
two sections already is: this build's desktop CSS is in 1920 units and is
zoomed onto 1400 by .sof-scale. Mobile is 390 in both, so mobile numbers are
used exactly as measured. Getting this wrong renders the one new logo at
three quarters of its neighbours, which no copy or colour check can see.

⚠️ THE PARTNER ROW IS NOW WIDER THAN THE PLATE ABOVE IT, ON DESKTOP ONLY, AND
THAT IS THE DESIGN. Three 280 plates with two 20 gaps is 880, against the
BestFulfill plate's 760. The frame centres the 760 inside the 880 (x=60), so
the row overhangs by 60 each side. On 2026-10-31 the opposite was true and the
row was made to SPLIT the plate's width so it sat flush; that rule does not
survive a third plate, so desktop gets its own max-width (880 x 4/3 = 1173)
and mobile stays flush at 342, which is what ITS frame draws (341 of 342).

WHAT IS MEASURED, AND FROM WHERE

  marquee taza    desktop 180.5x41.8 -> x4/3 -> 242x56   (node 1033:146)
                  mobile  106.7x24.7 ->          108x25  (node 1033:849)
  plate   taza    desktop 190x44     -> x4/3 -> 253x59   (node 1033:675)
                  mobile  82x19      ->          82x19   (node 1033:1366)
  plate   height  mobile 56, was 60. The design moved; 60 came from the
                  two-plate row and was never re-measured.
  row max-width   desktop 880 x 4/3 = 1173, was 1013

  The gaps did NOT move: 88 desktop (x4/3 = 117) and 40 mobile, both already
  in the CSS. bf / suits / outcraft sizes drifted 1-2% in the new frame and
  are LEFT ALONE -- re-rounding three logos by a pixel is churn, not fidelity.

⚠️ THE LOOP DURATION HAS TO MOVE WITH THE SEQUENCE. A fourth logo makes one
sequence longer, and the duration is what sets the speed. Held at the ~60px/s
the old ticker ran at, which is the number the other three were set from:

  mobile   212+40+95+40+119+40+108 + 40 padding-right = 694px -> 11.5s
  desktop  472+117+215+117+265+117+242 + 117          = 1662px -> 28s

Leave them and the band simply scrolls 27% faster, which reads as a glitch
rather than as a change nobody asked for.

⚠️ ONE SYMBOL, currentColor, LIKE THE OTHER THREE. Tazapay is navy #041C32 in
all three places it appears (verified on 1033:146, 1033:675 and 1033:849), so
it does not strictly need the two-colour treatment BestFulfill needs. It gets
it anyway, because a fourth symbol shaped unlike the three beside it is the
thing that breaks the next time someone recolours one. The export's single
fill="white" is asserted to be the clipPath rect before any fill is touched.

⚠️ EXPLICIT WIDTH ON THE MARQUEE SVG, NEVER width:auto. Safari collapses an
inline <svg> that carries only a height, which is how the whole marquee came
back blank on iOS on 2026-10-31. The new logo follows the same rule.

    py funnels/sof/scaling-or-failing/edits/add_tazapay.py --logo <file.svg>
    py funnels/sof/scaling-or-failing/edits/add_tazapay.py --logo <file.svg> --apply
"""
import io
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", "..", "..", ".."))
BUILDER = os.path.join(ROOT, "pagescore", "build_sof_event.py")
LOGO = sys.argv[sys.argv.index("--logo") + 1] if "--logo" in sys.argv else None
APPLY = "--apply" in sys.argv


def build_symbol(path):
    """The plate export (1033:675), turned into a <symbol> the way the other
    three were: ids namespaced so two symbols cannot share a clipPath, and
    every artwork fill swapped for currentColor."""
    svg = io.open(path, encoding="utf-8").read()

    # ⚠️ Assert the ONE white fill is the clip rect, never artwork. Recolouring
    # a white-filled path to currentColor would blank the mark on a navy plate
    # and nothing downstream would say so.
    whites = re.findall(r'<(\w+)[^>]*fill="white"', svg)
    assert whites == ["rect"], "unexpected fill=white on %s" % whites
    assert "<clipPath" in svg and svg.index("<clipPath") < svg.index('fill="white"')

    body = re.search(r"<svg[^>]*>(.*)</svg>", svg, re.S).group(1).strip()
    n_fill = body.count('fill="#041C32"')
    assert n_fill == 10, "expected 10 navy fills, found %d" % n_fill
    body = body.replace('fill="#041C32"', 'fill="currentColor"')
    body = body.replace("clip0_1033_675", "sof-taza-clip0_1033_675")
    assert 'fill="#' not in body, "a hardcoded fill survived"

    # ⚠️ THE SYMBOL IS BEING PASTED INTO A PYTHON STRING LITERAL, SO ITS
    # NEWLINES MUST BE THE TWO CHARACTERS BACKSLASH-N, NOT REAL LINE BREAKS.
    # A real break ends the quoted LOGO_DEFS line and the builder stops
    # parsing: "SyntaxError: unterminated string literal". The three symbols
    # already in there are stored escaped for exactly this reason.
    body = body.replace(chr(10), chr(92) + "n")
    assert chr(10) not in body
    return '<symbol id="sof-logo-taza" viewBox="0 0 190 44">' + body + '</symbol>'


# (what to find, what to put there) -- every one asserted to hit EXACTLY ONCE.
def edits(symbol):
    return [
        # ---- 1. the symbol itself, appended to the defs sprite
        ("</symbol></svg>'",
         "</symbol>" + symbol + "</svg>'"),

        # ---- 1b. the OTHER THREE marquee logos drifted in the new frame.
        # bf 354->359.6 and oc 198.8->204.3 (x4/3: 472->479, 265->272; mobile
        # oc 119->121). Measured, not guessed: on the test step Tazapay and
        # Suits rendered at 0.978 of their frame size and bf and oc at 0.957
        # and 0.946, because those two were still set from the 2026-10-31
        # frame. 3% is invisible on its own and wrong beside a logo that is
        # right. The PLATE logos did not move, which is what says the designer
        # re-placed the marquee row when adding the fourth brand.
        # ---- 2. marquee, mobile size + loop duration
        (".sof-marq-logo--oc{width:119px;height:22px}",
         ".sof-marq-logo--oc{width:119px;height:22px}\n"
         ".sof-marq-logo--taza{width:108px;height:25px}"),
        ("animation:sof-marq 9s linear infinite",
         "animation:sof-marq 11.5s linear infinite"),

        # ---- 3. marquee, desktop size + loop duration
        ("  .sof-marq-logo--oc{width:265px;height:49px}",
         "  .sof-marq-logo--oc{width:265px;height:49px}\n"
         "  .sof-marq-logo--taza{width:242px;height:56px}"),
        ("  .sof-marq-track{animation-duration:22s}",
         "  .sof-marq-track{animation-duration:28s}"),

        # ---- 4. marquee markup
        ('                         ("oc", "Outcraft")))',
         '                         ("oc", "Outcraft"), ("taza", "Tazapay")))'),
        ('    for label in ("BestFulfill", "Suits Finance", "Outcraft"):',
         '    for label in ("BestFulfill", "Suits Finance", "Outcraft",\n'
         '                  "Tazapay"):'),

        # ---- 5. partner row, mobile. 342 - 2 gaps / 3 = 107.3, the frame's 107.
        (".sof-splate{flex:1;min-width:0;height:60px;",
         ".sof-splate{flex:1;min-width:0;height:56px;"),
        (".sof-splate svg{display:block;color:#041C32}",
         "/* ⚠️ A THIRD PLATE TOOK THE BREATHING ROOM OUT AT 320. Three plates share\n   the row, so each is ~90 wide there against ~105 at 390, and the Suits and\n   Outcraft marks -- 84 and 90 wide, FIXED, because Safari collapses an svg\n   that carries only a height -- ran into the plate edge. max-width keeps the\n   explicit width Safari needs and lets the viewBox scale the artwork down to\n   fit; 10px, which is slack the plate only has below ~368, so 375 and 390\n   still render at the design's exact sizes. */\n.sof-splate svg{display:block;color:#041C32;max-width:calc(100% - 10px)}"),
        (".sof-splate--oc svg{width:90px;height:16px}",
         ".sof-splate--oc svg{width:90px;height:16px}\n"
         ".sof-splate--taza svg{width:82px;height:19px}"),

        # ---- 6. partner row, desktop. 1173 - 2 gaps / 3 = 373, the frame's 373.
        ("  .sof-sponsors{gap:27px;margin-top:96px;max-width:1013px}",
         "  /* 2026-11-02: 1173 (880 x 4/3), NOT the plate's 1013. Three plates\n"
         "     do not fit the plate's width, and the frame widens the row and\n"
         "     centres the plate inside it rather than shrinking the plates. */\n"
         "  .sof-sponsors{gap:27px;margin-top:96px;max-width:1173px}"),
        ("  .sof-splate--oc svg{width:252px;height:46px}",
         "  .sof-splate--oc svg{width:252px;height:46px}\n"
         "  .sof-splate--taza svg{width:253px;height:59px}"),

        # ---- 7. partner row markup
        ('        for k, label in (("suits", "Suits Finance"), '
         '("oc", "Outcraft")))',
         '        for k, label in (("suits", "Suits Finance"),\n'
         '                         ("oc", "Outcraft"), ("taza", "Tazapay")))'),

        # ---- 8. the two comments that now say the wrong number
        ("""    \"\"\"OUR PARTNERS, POWERED BY, the BestFulfill plate, and -- new on
    2026-10-31 -- a row of two smaller plates for the other two partners.""",
         """    \"\"\"OUR PARTNERS, POWERED BY, the BestFulfill plate, and a row of
    smaller plates for the other partners: two on 2026-10-31, three since
    2026-11-02 when Tazapay was added to the frame."""),
        ("""/* NEW 2026-10-31 (1027:902 / 1027:1551): the two smaller partners, which the
   previous frame did not have at all. */""",
         """/* NEW 2026-10-31 (1027:902 / 1027:1551): the smaller partners, which the
   previous frame did not have at all. Tazapay joined them on 2026-11-02
   (1033:674 / 1033:1365), which is why the desktop row has its own
   max-width below rather than inheriting the plate's. */"""),
    ]


def main():
    assert LOGO, "pass --logo <exported 1033-675.svg>"
    symbol = build_symbol(LOGO)
    src = io.open(BUILDER, encoding="utf-8").read()
    out = src
    for old, new in edits(symbol):
        n = out.count(old)
        assert n == 1, "marker hit %d times, need exactly 1: %r" % (n, old[:70])
        out = out.replace(old, new)

    # Post-conditions: the four brands, in both places, and nowhere a stray.
    for cls in ("bf", "suits", "oc", "taza"):
        assert out.count('id="sof-logo-%s"' % cls) == 1, cls
    assert out.count("sof-marq-logo--taza") == 2, "mobile + desktop width"
    assert out.count("sof-splate--taza") == 2, "mobile + desktop logo size"
    # ⚠️ A /* that never closes swallows every rule after it, silently -- that
    # is how the price-flip pill came back on 2026-10-31. Checked as a DELTA,
    # not as a balance: the module docstring already contains a bare "/*" (a
    # URL path, "techunboxed.co/*"), so the file has never been balanced.
    for tok in ("/*", "*/"):
        assert out.count(tok) == src.count(tok) + 1, "comment token %s" % tok

    print("edits: %d, bytes %d -> %d" % (len(edits(symbol)), len(src), len(out)))
    if not APPLY:
        print("dry run. pass --apply to write.")
        return
    io.open(BUILDER, "w", encoding="utf-8", newline="").write(out)
    print("written: %s" % BUILDER)


main()
