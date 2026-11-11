#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Rebuild two sections from the new Figma frame: the marquee and the partners.

JOSHUA, 2026-10-31: a new frame "Scaling Or Failing V2" (1027:282), with two
sections changed -- "the marquee below the hero" and "the our partners powered
by below the ticket section" -- plus "the ticket design on the figma is stale
so dont pay any mind to it" and "the old marquee is now also gone".

This PATCHES pagescore/build_sof_event.py. It does not touch the live page. The
page is then built to a SEPARATE STEP, QA'd there, and only promoted once it is
proven -- Joshua's call: "make a separate step then build from there one
everything is working replace the live with the tested version".

    SOF_SLUG=sof-v3 py pagescore/build_sof_event.py        -> /event/sof-v3

⚠️ THE NEW FRAME IS 1440 WIDE. THE OLD ONE WAS 1920.
Every other section here was drawn at 1920 and renders inside the .sof-scale
zoom that maps 1920 onto 1400. A value read off the new frame is therefore 3/4
of what this build's desktop CSS expects, so EVERY desktop number below is the
measured value x 4/3. Skip that and these two sections render at three quarters
the size of the eight around them, with every string and every hex still
correct -- which is precisely the failure no copy or colour check can see.
Mobile is 390 in both frames, so mobile values are used exactly as measured.

⚠️ THE BAND CREAM IS #F7ECCE, AND THE FRAME ONLY SAYS SO SIDEWAYS. The marquee
frame's own fill is a parchment IMAGE, which this build renders flat like every
other cream band. The actual value came from the edge-fade gradient, whose
opaque stop is the colour it fades FROM: rgb(0.9686, 0.9255, 0.8078). The fades
must match the band exactly or they read as two grey smears.

WHAT CHANGED, ALL MEASURED

  marquee   was: a gold band, six phrases looping left (the "ticker")
            now: a cream band, "SPONSORED BY" over a red rule, the three
                 sponsor logos looping left behind 56/267px edge fades
  partners  was: MAIN PARTNER / POWERED BY 48 / one 368x105 plate
            now: OUR PARTNERS / POWERED BY 70 / one 760x200 plate, and a new
                 row of two 280x96 plates, Suits Finance and Outcraft

⚠️ THE SAME LOGO SHIPS IN TWO COLOURS. BestFulfill is navy #041C32 in the
marquee and red #C01400 on its plate; Suits and Outcraft are navy in both. Each
logo is therefore defined ONCE as an SVG <symbol> whose paths are
`currentColor`, and the colour is set in CSS where it is used. Verified before
converting: every fill="white" in the exports is a <clipPath> rect, never
artwork, so recolouring the paths cannot blank one out.

⚠️ ONE SYMBOL PER BRAND, FROM THE PLATE EXPORT. Marquee and plate are the same
artwork at different sizes, except Figma exported the marquee Outcraft CLIPPED
(182x38 against its node's own 204x37). The plate exports are unclipped and
their aspect ratios match the marquee nodes to within 1.7%, so they are the
honest source for both. Each is drawn at the design's HEIGHT with width:auto,
so its own viewBox keeps the proportion.

⚠️ THE SEAM. The track holds TWO identical sequences and animates to -50%, with
the inter-sequence gap living INSIDE the sequence as padding-right. That is the
mechanism the old ticker already used and documented at length: with a
track-level gap G the track is 2S+G and -50% lands half a gap short, which
shows as a visible jump every single cycle. Reused, not reinvented.

TWO VALUES THE FRAME DOES NOT STATE, AND WHERE THEY CAME FROM
  * the loop DURATION. Set so both breakpoints scroll at ~60px/s, the speed the
    old ticker ran at (2552px per 40s). One sequence is 1319px desktop and
    548px mobile, hence 22s and 9s.
  * the desktop eyebrow stays 26px. The frame says 19, and 19 x 4/3 = 25.33,
    which after the 0.729 zoom differs from the existing 26 by a quarter of a
    pixel. Changing it would be churn, not fidelity.

    py funnels/.../patch_marquee_and_partners.py --logos <dir>            check
    py funnels/.../patch_marquee_and_partners.py --logos <dir> --apply
"""
import io
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", "..", "..", ".."))
BUILDER = os.path.join(ROOT, "pagescore", "build_sof_event.py")
LOGO_DIR = sys.argv[sys.argv.index("--logos") + 1] if "--logos" in sys.argv else None
APPLY = "--apply" in sys.argv

LOGO_SRC = {"bf": "1027-878.svg", "suits": "1027-904.svg", "oc": "1027-913.svg"}
CREAM = "#F7ECCE"


def symbol(key, path):
    """One <symbol> per brand, artwork recoloured to currentColor.

    Only the artwork hexes are swapped. Every fill="white" here is a <clipPath>
    rect; recolouring one would be invisible in the file and catastrophic on
    the page, so the swap is anchored on the two hexes the artwork uses and the
    white count is asserted unchanged.
    """
    s = io.open(path, encoding="utf-8").read()
    view = re.search(r'viewBox="([^"]+)"', s).group(1)
    body = s[s.index(">", s.index("<svg")) + 1:s.rindex("</svg>")]

    white = body.count('fill="white"')
    for hexv in ("#041C32", "#C01400"):
        body = body.replace('fill="%s"' % hexv, 'fill="currentColor"')
    assert body.count('fill="white"') == white, "a clip rect was recoloured"
    assert "#041C32" not in body and "#C01400" not in body, "a fill was missed"

    # Ids are local to each exported file, so three symbols on one page would
    # otherwise share clipPath ids and clip each other.
    for ident in re.findall(r'id="([^"]+)"', body):
        body = body.replace('"%s"' % ident, '"sof-%s-%s"' % (key, ident))
        body = body.replace("url(#%s)" % ident, "url(#sof-%s-%s)" % (key, ident))
    return '<symbol id="sof-logo-%s" viewBox="%s">%s</symbol>' % (key, view, body)


# ----------------------------------------------------------------- the CSS
MARQ_CSS = """
/* ========= 2b · SPONSOR LOGO MARQUEE (1027:382 / 1027:1043) =============
   Replaces the six-phrase gold ticker, which the new frame deletes outright.

   Desktop numbers are the 1440 frame's x 4/3, because this build's desktop CSS
   is in 1920 units and is zoomed onto 1400 by .sof-scale. See the patch script
   for why that conversion is the whole ballgame.

   The seam is solved exactly as the ticker solved it: two identical sequences,
   animate to -50%, and the inter-sequence gap lives INSIDE the sequence as
   padding-right. A track-level gap makes the track 2S+G, and -50% then lands
   half a gap short on every cycle. */
.sof-marqbar{display:flex;flex-direction:column;align-items:center;
  gap:14px;padding:22px 0;border-bottom:2px solid #041C32;overflow:hidden}
.sof-marq-head{display:flex;flex-direction:column;align-items:center;gap:8px}
.sof-marq-lab{font-family:__COND__;font-weight:700;font-size:14px;
  letter-spacing:.28em;color:#a3051b;line-height:1.2}
.sof-marq-rule{width:48px;height:3px;
  background:linear-gradient(90deg,#A3051B 0%,#D14A14 100%)}
.sof-marq-win{position:relative;width:100%;overflow:hidden}
.sof-marq-track{display:flex;align-items:center;width:max-content;
  animation:sof-marq 9s linear infinite;will-change:transform}
.sof-marq-seq{display:flex;align-items:center;flex:0 0 auto;
  gap:40px;padding-right:40px}
/* Height only: each symbol's own viewBox keeps its proportion, which is what
   lets one symbol serve both the marquee and the plate. */
.sof-marq-logo{display:block;flex:0 0 auto;width:auto;color:#041C32}
.sof-marq-logo--bf{height:33px}
.sof-marq-logo--suits{height:26px}
.sof-marq-logo--oc{height:22px}
@keyframes sof-marq{from{transform:translateX(0)}
                    to{transform:translateX(-50%)}}
/* The fade must be the band's own cream or it reads as a grey smear. The
   value is the opaque stop of the frame's own gradient. */
.sof-marq-fade{position:absolute;top:0;bottom:0;width:56px;pointer-events:none}
.sof-marq-fade--l{left:0;background:linear-gradient(90deg,__CREAM__ 0%,
  __CREAM__D9 25%,__CREAM__00 100%)}
.sof-marq-fade--r{right:0;background:linear-gradient(270deg,__CREAM__ 0%,
  __CREAM__D9 25%,__CREAM__00 100%)}
/* A band sliding forever is exactly what this setting is for. */
@media (prefers-reduced-motion:reduce){
  .sof-marq-track{animation:none}
}
""".replace("__CREAM__", CREAM)

MARQ_CSS_D = """
  /* 2b · sponsor logo marquee — the 1440 frame's values x 4/3 */
  .sof-marqbar{gap:29px;padding:53px 0;border-bottom-width:4px}
  .sof-marq-head{gap:16px}
  .sof-marq-lab{font-size:32px}
  .sof-marq-rule{width:128px;height:4px}
  .sof-marq-seq{gap:117px;padding-right:117px}
  .sof-marq-logo--bf{height:73px}
  .sof-marq-logo--suits{height:59px}
  .sof-marq-logo--oc{height:49px}
  .sof-marq-track{animation-duration:22s}
  .sof-marq-fade{width:267px}
"""

PART_CSS = """.sof-sponsor{padding-top:64px;padding-bottom:64px;text-align:center}
.sof-partner{font-family:__COND__;font-weight:700;font-size:13px;letter-spacing:.28em;
  color:#a3051b;line-height:1.2}
.sof-sponsor-rule{width:48px;height:3px;margin:8px auto 0;
  background:linear-gradient(90deg,#A3051B 0%,#D14A14 100%)}
.sof-powered{font-family:__DISPLAY__;font-weight:900;font-size:48px;line-height:92%;
  letter-spacing:-0.01em;color:#041C32;margin-top:13px}
/* Navy at 6% fill and 18% stroke, per 918:584 -- the plate reads as a tint
   of the cream it sits on, which is why it had to flip with the band. */
.sof-plate{width:100%;max-width:342px;height:124px;margin:40px auto 0;
  border-radius:16px;background:#041C320F;border:1px solid #041C322E;
  display:flex;align-items:center;justify-content:center}
.sof-plate .sof-plate-logo{width:280px;height:43px;color:#C01400}
/* NEW 2026-10-31 (1027:902 / 1027:1551): the two smaller partners, which the
   previous frame did not have at all. */
.sof-sponsors{display:flex;align-items:center;justify-content:center;
  gap:10px;margin-top:32px}
.sof-splate{width:136px;height:60px;border-radius:16px;
  background:#041C320F;border:1px solid #041C322E;
  display:flex;align-items:center;justify-content:center}
.sof-splate svg{display:block;color:#041C32}
.sof-splate--suits svg{width:84px;height:23px}
.sof-splate--oc svg{width:90px;height:16px}
"""

PART_CSS_D = """  /* 9 · sponsor — the 1440 frame's values x 4/3. The eyebrow stays 26:
     19 x 4/3 is 25.33, which after the zoom differs by a quarter pixel. */
  .sof-sponsor{padding-top:120px;padding-bottom:120px}
  .sof-partner{font-size:26px}
  .sof-sponsor-rule{width:93px;margin-top:16px}
  .sof-powered{font-size:93px;margin-top:29px}
  .sof-plate{max-width:1013px;height:267px;border-radius:32px;border-width:2px;
    margin-top:107px}
  .sof-plate .sof-plate-logo{width:747px;height:115px}
  .sof-sponsors{gap:27px;margin-top:96px}
  .sof-splate{width:373px;height:128px;border-radius:32px;border-width:2px}
  .sof-splate--suits svg{width:233px;height:64px}
  .sof-splate--oc svg{width:252px;height:46px}
"""


def main():
    if not LOGO_DIR:
        sys.exit("Pass --logos <dir> holding %s" % ", ".join(LOGO_SRC.values()))
    syms = {k: symbol(k, os.path.join(LOGO_DIR, f)) for k, f in LOGO_SRC.items()}
    defs = ('<svg width="0" height="0" aria-hidden="true" focusable="false"'
            ' style="position:absolute">%s</svg>'
            % "".join(syms[k] for k in ("bf", "suits", "oc")))

    src = io.open(BUILDER, encoding="utf-8").read()
    orig = src

    # ---- 1. the symbol sheet and the two builders -----------------------
    new_funcs = '''LOGO_DEFS = %r


def marquee_html():
    """Two identical sequences. The second is aria-hidden: it exists only so
    the loop has something to scroll into, and a screen reader meeting each
    sponsor twice would be reading a rendering trick aloud."""
    seq = "".join(
        '<svg class="sof-marq-logo sof-marq-logo--%%s" role="img"'
        ' aria-label="%%s"><use href="#sof-logo-%%s"/></svg>' %% (k, label, k)
        for k, label in (("bf", "BestFulfill"), ("suits", "Suits Finance"),
                         ("oc", "Outcraft")))
    hidden = seq.replace(' role="img"', ' aria-hidden="true"')
    for label in ("BestFulfill", "Suits Finance", "Outcraft"):
        hidden = hidden.replace(' aria-label="%%s"' %% label, "")
    return (
        '%%s'
        '<div class="sof-marq-head"><p class="sof-marq-lab">%%s</p>'
        '<div class="sof-marq-rule" aria-hidden="true"></div></div>'
        '<div class="sof-marq-win">'
        '<div class="sof-marq-track">'
        '<div class="sof-marq-seq">%%s</div>'
        '<div class="sof-marq-seq" aria-hidden="true">%%s</div>'
        '</div>'
        '<div class="sof-marq-fade sof-marq-fade--l" aria-hidden="true"></div>'
        '<div class="sof-marq-fade sof-marq-fade--r" aria-hidden="true"></div>'
        '</div>'
    ) %% (LOGO_DEFS, T("1027:384"), seq, hidden)
''' % defs

    assert "def ticker_html" in src
    i = src.index("# ------------------------------------------------------- 2b | ticker marquee")
    j = src.index("# ------------------------------------------- 9c | who it's for, and the FAQ")
    src = src[:i] + ("# --------------------------------------- 2b | sponsor logo marquee\n"
                     "# 1027:382 desktop / 1027:1043 mobile, new on 2026-10-31. The six-phrase\n"
                     "# ticker it replaces is gone from the frame entirely.\n"
                     + new_funcs + "\n\n") + src[j:]

    new_sponsor = '''def sponsor_html():
    """OUR PARTNERS, POWERED BY, the BestFulfill plate, and -- new on
    2026-10-31 -- a row of two smaller plates for the other two partners.

    The BestFulfill mark is the SAME symbol the marquee uses; only its colour
    differs, red here and navy there, which is why the symbol carries
    currentColor rather than a baked fill."""
    small = "".join(
        '<div class="sof-splate sof-splate--%s">'
        '<svg role="img" aria-label="%s"><use href="#sof-logo-%s"/></svg></div>'
        % (k, label, k)
        for k, label in (("suits", "Suits Finance"), ("oc", "Outcraft")))
    return (
        '<p class="sof-partner">%s</p>'
        '<div class="sof-sponsor-rule" aria-hidden="true"></div>'
        '<h2 class="sof-powered">%s</h2>'
        '<div class="sof-plate">'
        '<svg class="sof-plate-logo" role="img" aria-label="BestFulfill">'
        '<use href="#sof-logo-bf"/></svg></div>'
        '<div class="sof-sponsors">%s</div>'
    ) % (T("949:1513"), T("949:1515"), small)
'''
    a = src.index("def sponsor_html():")
    b = src.index("# ---------------------------------------", a)
    src = src[:a] + new_sponsor + "\n\n" + src[b:]

    # ---- 2. CSS ---------------------------------------------------------
    k = src.index("/* ============== 2b · TICKER MARQUEE")
    k2 = src.index("/* ========== 6b · MISSION MAP")
    src = src[:k] + MARQ_CSS.strip() + "\n\n" + src[k2:]

    old_d = src[src.index("  .sof-tick-track{animation-duration:40s}"):]
    old_d = old_d[:old_d.index("\n\n")]
    src = src.replace(old_d, MARQ_CSS_D.strip("\n"), 1)
    src = src.replace(".sof-ticker > .sof-cap{overflow:hidden}",
                      ".sof-marqbar > .sof-cap{overflow:hidden}", 1)
    src = src.replace("""  .sof-ticker{height:104px;border-top-width:6px;border-bottom-width:6px}\n""", "")

    p = src.index(".sof-sponsor{padding-top:64px")
    p2 = src.index("/* ===================== 10 · FOOTER")
    src = src[:p] + PART_CSS + "\n" + src[p2:]

    q = src.index("  /* 9 · sponsor */")
    q2 = src.index("  /* 10 · footer", q)
    src = src[:q] + PART_CSS_D + "\n" + src[q2:]

    # ---- 3. mounts and copy --------------------------------------------
    src = src.replace(
        'section(ticker_html(), extra_class="sof-ticker", bleed=True, wrap=False),',
        'section(marquee_html(), extra_class="sof-marqbar", bleed=True, wrap=False),', 1)
    # Eline's "drop the +1 from the marquee" override, 2026-10-21. It retuned a
    # phrase in the SIX-PHRASE TICKER, which the new frame deletes, so the node
    # it targets no longer renders anywhere. Left in place it would be a dead
    # entry whose comment points at a function that no longer exists.
    dead = ('    # Eline, 2026-10-21: drop the +1 from the marquee. It counted the VIP\n'
            '    # third day, which is now invite only and not for sale. One entry covers\n'
            '    # both frames and both rendered copies -- ticker_html duplicates the\n'
            '    # sequence from this single node.\n'
            '    "949:1137": "2 DAYS",\n')
    assert src.count(dead) == 1, "the stale ticker copy override moved"
    src = src.replace(dead, "", 1)

    src = src.replace('"949:1457": "FINAL PRICE",',
                      '# The eyebrow is "OUR PARTNERS" in the new frame (1027:871).\n'
                      '    "949:1513": "OUR PARTNERS",\n'
                      '    "949:1457": "FINAL PRICE",', 1)

    # ---- 4. prove it ----------------------------------------------------
    # ⚠️ NOT "sof-tick": it is a substring of "sof-tickets", which is the TICKET
    # section and must survive untouched. Asserting on the bare stem reported
    # the ticker as still present when it was long gone, and a careless fix
    # would have been to delete the ticket section's rules instead.
    for gone in ("sof-tick-", "sof-ticker", "ticker_html", "TICKER_NODES",
                 "TICK_STAR"):
        assert gone not in src, "left behind: %s" % gone
    for keep in (".sof-tickets", "tickets_html"):
        assert keep in src, "the ticket section was damaged: %s" % keep
    for want in ("def marquee_html", "sof-marqbar", "sof-logo-bf", "sof-splate",
                 "currentColor", '"949:1513": "OUR PARTNERS"', CREAM):
        assert want in src, "missing: %s" % want
    assert src.count("sof-logo-bf") >= 2, "the symbol is not used in both places"
    import ast
    ast.parse(src)

    print("symbols : %s" % ", ".join("%s=%dch" % (k, len(v)) for k, v in syms.items()))
    print("builder : %d -> %d chars (%+d)" % (len(orig), len(src), len(src) - len(orig)))
    print("ticker  : fully removed, marquee mounted in its place")
    print("parses clean.")
    if not APPLY:
        print("\nCHECK ONLY. Re-run with --apply to write the builder.")
        return
    io.open(BUILDER, "w", encoding="utf-8", newline="").write(src)
    print("\nWRITTEN. Now build to a SEPARATE step and QA it there:")
    print("  SOF_SLUG=sof-v3 py pagescore/build_sof_event.py")


main()
