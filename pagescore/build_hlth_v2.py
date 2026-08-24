#!/usr/bin/env python3
"""Oura Ring 4 vs HLTH Band advertorial, V2 (Figma node 36:2, "Oura vs HLTH V2 ·
TechUnboxed · 1441"). This is the V2 redesign of build_oura_hlth.py (Figma node
12:3, V1). Structure was verified section-by-section against V1 with figwright
get_design_context; ~95% of the design is IDENTICAL to V1 (same copy, colors,
tables, ranking card, citation card, FAQs, endmatter, footer legal). This file
copies V1's helpers and unchanged sections verbatim and only rewrites the parts
that genuinely differ in V2. See the diff summary below.

REAL DIFFERENCES V1 -> V2 (measured, not guessed):
1. New H1 ("Don't Buy A Smart Ring Until You've Read This" vs V1's "Oura Ring 4
   vs HLTH Band: ...") and new Standfirst.
2. New Hookline, and the old single "Then the HLTH Band went viral..." paragraph
   (with colored spans) is replaced by TWO plain paragraphs ("sticker price" /
   "two years") with different copy and no inline color spans.
3. The breadcrumb is no longer the first item inside the article flow. V2 pulls
   it into its own "Header · site" band (white bg, 1px bottom border #E4E6E2,
   14px top/bottom padding) that sits between the dark logo bar and the article
   -- and its copy changed to "Home > Wearables > Smart Ring Buying Guide" (red
   final crumb) to match the new angle.
4. The "Background" frame (36:5) is NOT a full-page decorative SVG behind
   everything, despite its name -- it measures 1440x70 at y=36, i.e. it is
   V1's dark (#1C1C1E) logo_bar strip, just re-authored with the TechUnboxed
   wordmark drawn as vector paths instead of a raster fill. Functionally
   identical to V1's logo_bar; reuses the same hosted logo asset (see the
   manifest note -- no new LF upload is in scope for this read-only task).
5. Byline strip border is genuinely DASHED (Figma dashPattern:[1.5,3]), not
   solid as V1 mistakenly built it. Corrected here.
6. The Price section's chart is a completely different chart TYPE: V1 used
   horizontal progress-bar rows; V2 uses a line/area chart (two diverging
   lines + a shaded "£481 gap" area + gridlines + end labels). Rebuilt as an
   inline SVG (see cost_chart_v2()) since it can't be reproduced with the bar
   helpers.
7. Vertical rhythm: V2's article column uses a flat 16px auto-layout gap PLUS
   explicit "spacer N" frames between most sections (rather than V1's flat
   20px gap + occasional Title margin-top). Reproduced here with an explicit
   sp(px) spacer element inserted wherever Figma has a named spacer frame, on
   a 16px base gap -- matches the measured rhythm exactly instead of
   approximating.
8. Endmatter now has a 2px solid black top rule before "Sources" (V1 had none).
9. Two small "external link" glyph icons appear in V2 (ranking Trustpilot row,
   citation header) that V1 lacks. NOT reproduced: get_design_context's "full"
   detail returns vector bounding boxes but not path "d" data, so an exact
   recreation isn't measurable without a follow-up get_node call on those
   specific ids -- rather than guess at a generic icon, this was left out.
   Everything else (tag row, shop grid, "at a glance" table + values, editor's
   pick ranking card, battery bar chart + values, 3-year cost table + values,
   citation card, video placeholder, all FAQ copy, sources/disclaimer/author
   box, footer legal) is copied VERBATIM from V1 -- confirmed identical by
   diffing every TEXT node's `characters` field against V1's literal strings.

Typography / SSR gotchas: identical to V1 (see build_oura_hlth.py). Serif copy
= "Georgia, Gelasio, serif" (unquoted); UI chrome = "Inter, InterFallback,
sans-serif" (unquoted). No `overflow`, `boxShadow`, `maxWidth:"none"`, or
`alignItems:"baseline"` anywhere (503s the LF SSR renderer).

This script only ASSEMBLES the `kids` list / step body -- per task scope, it
does NOT call createStep/updateFunnel or any other LF write API. Wire that in
the same way build_oura_hlth.py does (bottom of that file) when ready to
publish.
"""
import sys, os, json, uuid
sys.path.insert(0, '.')
import lf_api

tok = open('.session_token').read().strip() if os.path.exists('.session_token') else ''
ACCT = open('.lf_account').read().strip() if os.path.exists('.lf_account') else ''
HH = {"account-id": ACCT, "version": "1",
      "Origin": "https://app.lightfunnels.com", "Referer": "https://app.lightfunnels.com/"}
def sgql(q, v=None): return lf_api.gql(tok, q, v, extra_headers=HH)
def nid(): return str(uuid.uuid4())

FUNNEL = "fun_hLmlmrbjeoGf3UZZvBEHY"
IMG = json.load(open("pagescore/.cache/hlth_v2_img_map.json"))

PDP = "https://hlthtrack.co.uk/products/wearable-hlth-band"  # QA: one canonical storefront domain
TP  = "https://www.trustpilot.com/review/hlthtrack.com"
# QA 21 Aug: Oura restructured their URLs -- /en-us/product/... now redirects to
# /en-us/store/... which 404s. /store/rings/oura-ring-4 is live (200) and is the
# same URL this page already cites for the published specifications.
OURA_URL = "https://ouraring.com/store/rings/oura-ring-4"

# ---- fonts (identical to V1) ----
SERIF = "GelasioText, Georgia, serif"
SANS  = "Inter, InterFallback, sans-serif"

# ---- perf: real Gelasio webfont (not just the Georgia fallback) -- Gelasio is
#      Google's metric-compatible Georgia substitute (verified empirically: <0.1%
#      text-width delta vs Georgia at both 400 and 700 over realistic heading-length
#      copy), so putting it first in SERIF causes no reflow even if it swaps in late
#      -- no ascent/descent-override gymnastics needed like the Inter/InterFallback
#      fix below. Google's CSS API currently serves the identical static file for the
#      400 and 700 latin-normal requests (a verified live quirk), but Chromium still
#      renders font-weight:700 as genuinely bold via the file's variable-font axis
#      (measured ~5% lower ink density than 400, matching Figma's lighter Gelasio Bold
#      vs. the old heavier Georgia Bold).
# Platform bug fix: Lightfunnels auto-detects any "Gelasio" font-family used
# in the page's styles and self-hosts it via its OWN CDN proxy
# (/cf-fonts/v/gelasio/5.2.8/<script>/wght/normal.woff2) -- but that proxy
# has a bug specific to variable fonts: it serves the LITERAL SAME file for
# weight:400 and weight:700 (verified live via curl on the served HTML),
# silently overriding whatever correct multi-weight setup we inject
# ourselves, since LF's own generated @font-face for the literal family
# "Gelasio" wins the cascade. Separately, even Google's OWN combined-query
# CSS (family=Gelasio:ital,wght@0,400;0,700;1,400) turned out to serve
# byte-identical variable-font files for 400 vs 700 too (verified via
# curl+diff) -- correct bold rendering there depends on the browser's
# variable-font instancing kicking in, which is not guaranteed across
# engines. Fix: rename the family to "GelasioText" (a name LF's proxy won't
# recognize/collide with) and hand-write @font-face rules pointing at
# ISOLATED single-weight-only Google Fonts queries (family=Gelasio:wght@400
# and :wght@700 requested with NO other weight in the same query) --
# verified via curl+md5 to return genuinely different static files
# (19,612 vs 19,852 bytes, different hashes), so bold is real regardless of
# variable-font support.
GELASIO_HEAD = (
    '<link rel="preload" as="font" type="font/woff2" crossorigin '
    'href="https://fonts.gstatic.com/s/gelasio/v14/cIfiMaFfvUQxTTqS3iKJkLGbI41wQL8Ilxcr8zHs9RbblYs.woff2">\n'
    '<link rel="preload" as="font" type="font/woff2" crossorigin '
    'href="https://fonts.gstatic.com/s/gelasio/v14/cIfiMaFfvUQxTTqS3iKJkLGbI41wQL_WkBcr8zHs9RbblYs.woff2">\n'
    '<style>'
    "@font-face{font-family:GelasioText;font-style:normal;font-weight:400;font-display:swap;"
    "src:url(https://fonts.gstatic.com/s/gelasio/v14/cIfiMaFfvUQxTTqS3iKJkLGbI41wQL8Ilxcr8zHs9RbblYs.woff2) format('woff2')}"
    "@font-face{font-family:GelasioText;font-style:normal;font-weight:700;font-display:swap;"
    "src:url(https://fonts.gstatic.com/s/gelasio/v14/cIfiMaFfvUQxTTqS3iKJkLGbI41wQL_WkBcr8zHs9RbblYs.woff2) format('woff2')}"
    "@font-face{font-family:GelasioText;font-style:italic;font-weight:400;font-display:swap;"
    "src:url(https://fonts.gstatic.com/s/gelasio/v14/cIfsMaFfvUQxTTqS9Cu7b2nySBfeR6rA1M9vwzPm9DTfjYoqWA.woff2) format('woff2')}"
    '</style>\n')

# ---- perf: Inter preload + real @font-face + metric-matched fallback (verified zero-CLS
#      recipe, identical to V1 / build_test3.py / references/performance.md) ----
_HERO = IMG["hero"]["src"]
_CDN  = "https://assets.lightfunnels.com/cdn-cgi/image/width=%d,quality=80,format=auto/"
_SRCSET = ", ".join("%s%s %dw" % (_CDN % w, _HERO, w) for w in (384, 750, 1080, 1920, 3840))
_FONT_PRELOAD = "".join(
    '<link rel="preload" as="font" type="font/woff2" crossorigin '
    'href="/cf-fonts/s/inter/5.2.8/latin/%d/normal.woff2">\n' % w for w in (400, 600, 700, 800))
_INTER_WEIGHTS = (400, 500, 600, 700, 800, 900)
_INTER_FACE = "<style>" + "".join(
    "@font-face{font-family:Inter;font-style:normal;font-weight:%d;font-display:swap;"
    "src:url(/cf-fonts/s/inter/5.2.8/latin/%d/normal.woff2) format('woff2')}" % (w, w)
    for w in _INTER_WEIGHTS) + "</style>\n"
_FALLBACK_FACE = (
    "<style>@font-face{font-family:InterFallback;src:local('Arial'),local('Liberation Sans'),local('Helvetica Neue');"
    "ascent-override:90.44%;descent-override:22.52%;line-gap-override:0%;size-adjust:107.12%}</style>\n")
PERF = (
    GELASIO_HEAD +
    '<link rel="preload" as="image" fetchpriority="high" '
    'imagesrcset="%s" imagesizes="(min-width: 1280px) 50vw, 100vw">\n'
    '<style>img[title="hero"]{height:403px!important;width:100%%!important;object-fit:cover;aspect-ratio:auto}'
    '@media (max-width:767px){img[title="hero"]{height:196px!important}}</style>\n' % _SRCSET
    + _INTER_FACE + _FALLBACK_FACE + _FONT_PRELOAD)
# QA: the LF storefront theme emits maximum-scale=1, which blocks pinch-zoom.
# There is no per-step viewport knob, so rewrite the tag at runtime.
# QA: Terms / Privacy / Editorial standards / Affiliate policy used to be dead
# href="#" links on every page. This is the same modal system already live on
# /smartwatch-review/0sAhHP7ki -- four overlays with the real legal copy, plus
# its CSS and click handler. Footer links carry the ids the handler listens for.
LEGAL_MODALS = open("pagescore/tu_legal_modals.html", encoding="utf-8").read()
PERF_FOOTER = (
    '<script>(function(){var v=document.querySelector("meta[name=viewport]");if(v&&/maximum-scale/.test(v.content))v.setAttribute("content","width=device-width, initial-scale=1");})();</script>\n'
    '<script>(function(){function f(){var h=document.querySelector(\'img[title="hero"]\');'
    'if(h){h.setAttribute("fetchpriority","high");h.setAttribute("loading","eager");}'
    'var lg=document.querySelector(\'img[title="logo"]\');if(lg)lg.removeAttribute("fetchpriority");}'
    'if(document.readyState!=="loading")f();else document.addEventListener("DOMContentLoaded",f);})();</script>\n') + LEGAL_MODALS

# ---- colors (measured, identical set to V1 + a couple of new chart-only tones) ----
DARK   = {"r":22,"g":24,"b":28,"a":1}    # #16181C main text
BODY   = {"r":74,"g":79,"b":87,"a":1}    # #4A4F57 secondary text
MUTED  = {"r":154,"g":160,"b":168,"a":1} # #9AA0A8 dateline
BORDER = {"r":228,"g":230,"b":226,"a":1} # #E4E6E2
HARD_SHADOW = {"r":201,"g":204,"b":210,"a":1} # #C9CCD2 flat offset "shadow" (boxShadow 503s the SSR, see gotcha)
SOFT_SHADOW = {"r":242,"g":242,"b":242,"a":1} # ~5% black over white -- approximates the Figma effect_139lzk7
                                                # DROP_SHADOW (#0000000D, 0/1 offset, 4px blur) on white cards
                                                # (ranking card, citation card, cost-chart card). Real boxShadow/
                                                # filter is untested and risky on this renderer, so this fakes the
                                                # blur falloff as a thin lighter-gray sliver peeking out below.
TABLEBG= {"r":247,"g":248,"b":246,"a":1} # #F7F8F6
PINK   = {"r":251,"g":238,"b":236,"a":1} # #FBEEEC
RED    = {"r":230,"g":57,"b":70,"a":1}   # #E63946
BLUE   = {"r":26,"g":95,"b":208,"a":1}   # #1A5FD0
YELLOW_TAG = {"r":228,"g":236,"b":74,"a":1} # #E4EC4A
WHITE  = {"r":255,"g":255,"b":255,"a":1}
GOLD   = {"r":245,"g":179,"b":1,"a":1}   # #F5B301
TP_GREEN = {"r":0,"g":182,"b":122,"a":1} # #00B67A
TP_EMPTY = {"r":220,"g":220,"b":230,"a":1} # #DCDCE6
CHART_TRACK = {"r":236,"g":238,"b":241,"a":1} # #ECEEF1
CHART_GRAY  = {"r":195,"g":199,"b":205,"a":1} # #C3C7CD
HILITE_YEL  = {"r":255,"g":233,"b":92,"a":1}  # #FFE95C
DASH_BORDER = {"r":185,"g":189,"b":196,"a":1} # #B9BDC4
SUPPORT_BG  = {"r":244,"g":244,"b":242,"a":1} # #F4F4F2
SUPPORT_TXT = {"r":107,"g":111,"b":118,"a":1} # #6B6F76
HEADER_BG   = {"r":28,"g":28,"b":30,"a":1}    # #1C1C1E

# ---- helpers (verbatim from V1) ----
def _media(st, m):
    if m:
        for k, v in m.items(): st.append({"prop": k, "value": v, "media": 767})

def title(content, fs, lh, weight="700", mt=0, color=DARK, align="left", ls=None, m=None, font=SERIF, level="2"):
    st=[{"prop":"fontFamily","value":font},{"prop":"color","value":color},
        {"prop":"fontSize","value":fs},{"prop":"lineHeight","value":lh},
        {"prop":"fontWeight","value":weight},{"prop":"textAlign","value":align},
        {"prop":"width","value":"100%"},{"prop":"maxWidth","value":"100%"}]
    if ls: st.append({"prop":"letterSpacing","value":ls})
    if mt: st.append({"prop":"margin","value":{"top":"%spx"%mt}})
    _media(st, m)
    return {"t":"Title","id":nid(),"p":{"size":level,"content":content,"widthOption":"fill"},"styles":st}

def text(content, size="18px", lh="30px", color=DARK, weight="400", align="left", italic=False,
         mw="100%", m=None, font=SERIF):
    st=[{"prop":"fontFamily","value":font},{"prop":"color","value":color},
        {"prop":"fontSize","value":size},{"prop":"lineHeight","value":lh},
        {"prop":"fontWeight","value":weight},{"prop":"textAlign","value":align},
        {"prop":"maxWidth","value":mw},{"prop":"width","value":"100%"}]
    if italic: st.append({"prop":"fontStyle","value":"italic"})
    _media(st, m)
    return {"t":"Text","id":nid(),"p":{"content":content},"styles":st}

def inline_text(*a, **kw):
    # text() hardcodes width:100%, which forces short inline fragments inside a flex
    # row (e.g. "£349" + "+ £5.99/month membership") to each claim the full row width
    # and wrap onto their own line. This variant shrinks to its own content instead,
    # matching Figma's HUG sizing for these price-row fragments.
    node = text(*a, **kw)
    node["styles"].append({"prop":"width","value":"auto"})
    return node

def container(children, styles):
    return {"t":"Container","id":nid(),"styles":styles,"p":{"children":children}}

def soft_card(card, radius="14px", sliver="3px"):
    # Wrap an already-styled white card in a same-radius, very-light-gray
    # outer container with a couple px of bottom padding -- the sliver of
    # SOFT_SHADOW peeking out below fakes the card's subtle blurred drop-shadow.
    return container([card], [{"prop":"borderRadius","value":radius},
        {"prop":"backgroundColor","value":SOFT_SHADOW},
        {"prop":"padding","value":{"bottom":sliver}}])

def rowf(children, styles=None, gap="16px", align="stretch", justify=None, wrap=False):
    s=[{"prop":"lfDisplay","value":"flex"},{"prop":"flexDirection","value":"row"},
       {"prop":"gap","value":gap},{"prop":"alignItems","value":align},{"prop":"width","value":"100%"}]
    if justify: s.append({"prop":"justifyContent","value":justify})
    if wrap: s.append({"prop":"flexWrap","value":"wrap"})
    if styles: s.extend(styles)
    return container(children, s)

def col(children, styles=None, gap="8px"):
    s=[{"prop":"lfDisplay","value":"flex"},{"prop":"flexDirection","value":"column"},
       {"prop":"gap","value":gap},{"prop":"width","value":"100%"}]
    if styles: s.extend(styles)
    return container(children, s)

def sp(px):
    """Explicit spacer block matching a Figma 'spacer N' frame (V2's vertical
    rhythm is: 16px base column gap, PLUS one of these wherever the design has
    a named spacer sibling). Never guess a flat gap where Figma shows a real
    spacer node -- insert the exact measured height."""
    return container([], [{"prop":"width","value":"100%"},{"prop":"height","value":"%dpx"%px},
        {"prop":"lfDisplay","value":"block"}])

# These two are the only images the perf/JS hooks target (img[title="hero"],
# img[title="logo"]) -- title renders as a literal HTML title="" attribute, which
# shows as a native hover tooltip, so every other image must NOT get one (was
# leaking internal manifest keys like "hlth_product" as visible tooltips).
_TITLE_NEEDED = {"hero", "logo"}

# QA: LF emits an alt attribute but never populates it (the logo proves it:
# title="logo", alt=""). Confirmed live that the Image block honours p["alt"].
# Decorative images keep alt="" so screen readers skip them.
ALT = {
    "logo": "",            # decorative: the wordmark repeats in header and footer
    "avatar": "", "avatar_byline": "", "avatar_author": "",  # byline names the author adjacent
    "hero": "An Oura Ring held in one hand beside the HLTH Band worn on a wrist",
    "oura_product": "The Oura Ring 4 in gold, shown against a plain background",
    "hlth_product": "The HLTH Band, a screenless tracker with a woven fabric strap",
    "hlth_product_rank": "The HLTH Band photographed against a black background",
    "heart_bp": "The HLTH app showing blood pressure readings plotted across a day",
    "sleep_screens": "HLTH app screens breaking one night into deep, REM and light sleep",
    "training": "The HLTH Band worn on the wrist during a workout",
    "lifestyle": "The HLTH Band worn on a wrist at rest",
}

def img_block(key, height=None, radius="10px", full=True, fit="cover", mh=None, border=False, alt=None):
    m=IMG[key]
    st=[{"prop":"maxWidth","value":"100%"},{"prop":"borderRadius","value":radius},
        {"prop":"objectFit","value":fit},{"prop":"lfDisplay","value":"block"}]
    if border:
        st.append({"prop":"borderStyle","value":"solid"})
        st.append({"prop":"borderColor","value":BORDER})
        st.append({"prop":"borderWidth","value":"1px"})
    if full: st.append({"prop":"width","value":"100%"})
    if height: st.append({"prop":"height","value":height})
    if mh: st.append({"prop":"height","value":mh,"media":767})
    p = {"src_id":m["src_id"],"src_uid":m["src_uid"],"src":m["src"]}
    if key in _TITLE_NEEDED: p["title"] = key
    p["alt"] = ALT.get(key, "") if alt is None else alt
    return {"t":"Image","id":nid(),"p":p,"styles":st}

def inline_img(key, w, h, radius="0px", fit="contain"):
    m=IMG[key]
    return {"t":"Image","id":nid(),"p":{"src_id":m["src_id"],"src_uid":m["src_uid"],"src":m["src"]},
        "styles":[{"prop":"width","value":w},{"prop":"height","value":h},{"prop":"objectFit","value":fit},
                  {"prop":"borderRadius","value":radius},{"prop":"lfDisplay","value":"block"},{"prop":"flexShrink","value":"0"}]}

def logo_img(w="140px", h="35px"):
    m=IMG["logo"]
    return {"t":"Image","id":nid(),"p":{"title":"logo","src":m["src"]},
        "styles":[{"prop":"width","value":w},{"prop":"height","value":h},{"prop":"maxWidth","value":"100%"},
                  {"prop":"objectFit","value":"contain"},{"prop":"lfDisplay","value":"block"}]}

def button(label, href=PDP, bg=RED, fg=WHITE, full=False, size="15px", weight="700", radius="10px", ls=None,
           pad_v="13px", pad_h="10px"):
    lab_st=[{"prop":"fontFamily","value":SANS},{"prop":"color","value":fg},
            {"prop":"fontSize","value":size},{"prop":"fontWeight","value":weight},
            {"prop":"lineHeight","value":"20px"},{"prop":"textAlign","value":"center"},
            {"prop":"whiteSpace","value":"nowrap"},{"prop":"maxWidth","value":"100%"}]
    if ls: lab_st.append({"prop":"letterSpacing","value":ls})
    lab={"t":"Text","id":nid(),"p":{"content":label},"styles":lab_st}
    lw=container([lab],[{"prop":"lfDisplay","value":"flex"},{"prop":"alignItems","value":"center"},
        {"prop":"justifyContent","value":"center"},{"prop":"maxWidth","value":"100%"}])
    st=[{"prop":"backgroundColor","value":bg},{"prop":"borderRadius","value":radius},
        {"prop":"padding","value":{"top":pad_v,"bottom":pad_v,"left":pad_h,"right":pad_h}},
        {"prop":"lfDisplay","value":"flex"},{"prop":"alignItems","value":"center"},
        {"prop":"justifyContent","value":"center"}]
    if full: st.append({"prop":"width","value":"100%"})
    return {"t":"BlockLink","id":nid(),"p":{"destination":{"type":"static","value":href},
        "target":"_blank","widthOption":"auto","children":[lw]},"styles":st}

STAR = "★"
def tp_stars(rating, color, box=19):
    fs = 12
    half=round(rating*2)/2; full=int(half); hh=(half-full)==0.5
    out='<span style="display:inline-flex;gap:2.2px;vertical-align:middle">'
    tpl=('<span style="display:inline-flex;align-items:center;justify-content:center;width:%dpx;height:%dpx;'
         'border-radius:3px;color:#fff;font-size:%dpx;background:%s">' + STAR + '</span>')
    for i in range(5):
        if i<full: bg=color
        elif i==full and hh: bg="linear-gradient(90deg,%s 50%%,#dcdce6 50%%)"%color
        else: bg="#dcdce6"
        out+=tpl%(box,box,fs,bg)
    return out+'</span>'

def ext_link_icon(size=13, color="#4A4F57", stroke_w=1.2):
    # Figma node 36:187 "Icon · external link" -- box + arrow-out glyph, measured
    # geometry (13x13, stroke #4A4F57 ~1.19px, round caps/joins) but no exact bezier
    # path data is exposed by the design-context tool, so this is the standard
    # external-link glyph (box missing its top-right corner + an arrow through the
    # gap) redrawn to match that box size/stroke/color exactly.
    return ('<svg width="%d" height="%d" viewBox="0 0 13 13" fill="none" stroke="%s" '
        'stroke-width="%s" stroke-linecap="round" stroke-linejoin="round" '
        'style="display:inline-block;vertical-align:middle;flex-shrink:0">'
        '<path d="M11.375 7.313v3.25a1.625 1.625 0 0 1-1.625 1.625H2.438a1.625 1.625 0 0 1-1.625-1.625V3.25a1.625 1.625 0 0 1 1.625-1.625h3.25"/>'
        '<polyline points="8.125 1.625 11.375 1.625 11.375 4.875"/>'
        '<line x1="5.417" y1="7.583" x2="11.375" y2="1.625"/></svg>') % (size, size, color, stroke_w)

def caption(t="(Image credit: Marcus Pendleton / TechUnboxed)"):
    return text(t, size="13px", lh="18px", color=BODY, italic=True, font=SERIF)

def para(t): return text(t, size="18px", lh="30px", color=DARK, font=SERIF)

def winline_hlth(mt=0):
    return text('<span style="color:#E63946">Winner: </span>'
                 '<a href="%s" target="_blank" style="color:#1A5FD0;text-decoration:underline">HLTH Band</a>' % PDP,
                 size="18px", lh="30px", weight="700", font=SERIF,
                 m=({"margin":{"top":"%spx"%mt}} if mt else None))

def winline_oura():
    return text('<span style="color:#E63946">Winner: </span>'
                 '<a href="%s" target="_blank" style="color:#1A5FD0;text-decoration:underline">Oura Ring 4</a>' % OURA_URL,
                 size="18px", lh="30px", weight="700", font=SERIF)

def winline_hlth_plain():
    # Heart Tracking's winline (12:1868) is measured as plain solid red in
    # Figma, but every winline now links through to the winning product's own
    # PDP, matching every other HLTH-wins instance on the page.
    return text('<span style="color:#E63946">Winner: </span>'
                 '<a href="%s" target="_blank" style="color:#1A5FD0;text-decoration:underline">HLTH Band</a>' % PDP,
                 size="18px", lh="30px", weight="700", font=SERIF)

def h2(content, mt=24):
    return title(content, "28px", "35px", weight="700", color=DARK, ls="-0.28px", mt=mt, font=SERIF,
                 m={"fontSize":"22px","lineHeight":"28px","letterSpacing":"-0.22px"})

def figure(image_node, cap=True):
    """Group an image with its caption -- V2's Figma sometimes splits the raw
    image and its Figcaption across sibling frames (an authoring artifact, not
    a real design difference; both still render as one figure visually)."""
    kids_ = [image_node]
    if cap: kids_.append(caption())
    return kids_

# ============================== HEADER ===================================
support_bar = {"t":"Section","id":nid(),
    "styles":[{"prop":"backgroundColor","value":SUPPORT_BG},
              {"prop":"borderStyle","value":"solid"},{"prop":"borderColor","value":BORDER},
              {"prop":"borderWidth","value":"0px 0px 1px 0px"},
              {"prop":"padding","value":{"top":"9px","bottom":"9px"}}],
    "p":{"layout":"","dividerPosition":["top"],"horizontalFlip":False,
         "embedded_video":{"src":"","video_size":"stretch","video_position":"center"},
         "children":[text("This site is reader-supported; links may earn us commissions.",
             size="13px", lh="18px", color=SUPPORT_TXT, align="center", font=SANS)]}}

# "Background" (Figma 36:5) is really V1's dark logo_bar strip, just re-drawn
# with the wordmark as vector paths instead of a raster fill. Same asset reused.
logo_bar = {"t":"Section","id":nid(),
    "styles":[{"prop":"backgroundColor","value":HEADER_BG},
              # desktop token is Figma "color/grey/11" (#1C1C1E); the mobile frame
              # binds this same strip to a different token, "color/grey/16" (#28282B)
              {"prop":"backgroundColor","value":{"r":40,"g":40,"b":43,"a":1},"media":767},
              {"prop":"padding","value":{"top":"14px","bottom":"14px"}}],
    "p":{"layout":"","dividerPosition":["top"],"horizontalFlip":False,
         "embedded_video":{"src":"","video_size":"stretch","video_position":"center"},
         "children":[container([logo_img()],[{"prop":"lfDisplay","value":"flex"},
             {"prop":"justifyContent","value":"center"},{"prop":"width","value":"100%"}])]}}

# NEW in V2: a standalone breadcrumb band (Figma "Header · site" 36:19), white bg,
# 1px bottom border, sitting BETWEEN the logo bar and the article. V1 had the
# breadcrumb as the first line inside the article flow instead.
BREADCRUMB_V2 = ('<span style="color:#16181C">Home</span> <span style="color:#B9BDC4">&gt;</span> '
    '<span style="color:#16181C">Wearables</span> <span style="color:#B9BDC4">&gt;</span> '
    '<span style="color:#E63946;font-weight:600">Smart Ring Buying Guide</span>')

header_site_bar = {"t":"Section","id":nid(),
    "styles":[{"prop":"backgroundColor","value":WHITE},
              {"prop":"borderStyle","value":"solid"},{"prop":"borderColor","value":BORDER},
              {"prop":"borderWidth","value":"0px 0px 1px 0px"},
              {"prop":"padding","value":{"top":"14px","bottom":"14px"}},
              {"prop":"padding","value":{"top":"14px","bottom":"14px","left":"20px","right":"20px"},"media":767}],
    "p":{"layout":"boxed","dividerPosition":["top"],"horizontalFlip":False,
         "embedded_video":{"src":"","video_size":"stretch","video_position":"center"},
         "children":[text(BREADCRUMB_V2, size="13px", lh="18px", font=SANS)]}}

# ============================== ARTICLE HEAD ==============================
kids=[]
kids.append(title("Don't Buy A Smart Ring Until You've Read This",
    "40px","46px", weight="700", ls="-0.4px", font=SERIF, level="1",
    m={"fontSize":"28px","lineHeight":"32px","letterSpacing":"-0.28px"}))
kids.append(text("Before you spend £349 on a ring, there's a number the box won't tell you. We break down "
    "exactly what you're paying for, and what you're not getting.",
    size="20px", lh="30px", color=BODY, font=SERIF))

# tag row (identical to V1)
tag_comparison = container([text("Comparison", size="15px", lh="15px", color=WHITE, weight="700", font=SANS)],
    [{"prop":"backgroundColor","value":RED},{"prop":"borderRadius","value":"8px"},
     {"prop":"padding","value":{"top":"7px","bottom":"7px","left":"15px","right":"15px"}}])
trending_svg = ('<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="#16181C" stroke-width="2.5" '
    'stroke-linecap="round" stroke-linejoin="round"><polyline points="22 7 13.5 15.5 8.5 10.5 2 17"/>'
    '<polyline points="16 7 22 7 22 13"/></svg>')
tag_trending = container([rowf([
        {"t":"HtmlElement","id":nid(),"p":{"content":trending_svg},"styles":[{"prop":"flexShrink","value":"0"}]},
        text("Trending", size="15px", lh="15px", color=DARK, weight="700", font=SANS)],
    gap="6px", align="center")],
    [{"prop":"backgroundColor","value":YELLOW_TAG},{"prop":"borderRadius","value":"8px"},
     {"prop":"padding","value":{"top":"7px","bottom":"7px","left":"15px","right":"15px"}}])
kids.append(rowf([tag_comparison, tag_trending], gap="10px", align="center", justify="flex-start",
    styles=[{"prop":"width","value":"fit-content"}]))
kids.append(sp(2))

# byline strip -- same content as V1, but border is genuinely DASHED (Figma
# dashPattern:[1.5,3]; V1 built it solid) + measured 2px left/right padding.
byline_who = col([
    text("Marcus Pendleton", size="15.5px", lh="20px", color=DARK, weight="800", font=SANS),
    text("Principal Writer", size="13.5px", lh="18px", color=BODY, font=SANS),
], gap="2px", styles=[{"prop":"width","value":"150px"},{"prop":"flexShrink","value":"0"}])
# Read full bio / Hide bio toggle -- per Figma reference node 205:14
# ("REFERENCE - byline expanded state"): the bio ships collapsed ending in
# a bold-underlined "Read full bio"; tapping it swaps to the expanded copy
# (verbatim from node 205:24) ending in "Hide bio", which swaps back.
# Two inline spans, one hidden at a time, toggled by the bold link itself --
# same onclick-swap mechanic as the accordion() blocks elsewhere on this page.
_bio_collapsed_html = (
    '<span style="color:#4A4F57">Marcus is a lead writer at TechUnboxed, reviewing and testing the latest '
    'smartwatches and fitness trackers. </span>'
    '<b style="color:#16181C;text-decoration:underline;cursor:pointer" '
    'onclick="this.parentElement.style.display=\'none\';'
    'this.parentElement.nextElementSibling.style.display=\'inline\'">Read full bio</b>')
_bio_expanded_html = (
    '<span style="color:#4A4F57">Marcus is a lead writer at TechUnboxed, reviewing and testing the latest '
    "smartwatches and fitness trackers. Over six years he's tested more than 40 devices. He wears an Oura Ring on "
    "his right hand and rotates test bands on his left, he's 47 with a family history of high blood pressure, and "
    'he checks his numbers the way other people check the football scores. </span>'
    '<b style="color:#16181C;text-decoration:underline;cursor:pointer" '
    'onclick="this.parentElement.style.display=\'none\';'
    'this.parentElement.previousElementSibling.style.display=\'inline\'">Hide bio</b>')
byline_bio_toggle = {"t":"HtmlElement","id":nid(),"p":{"content":(
    '<span style="font-family:%s;font-size:14.5px;line-height:22px;display:inline">%s</span>'
    '<span style="font-family:%s;font-size:14.5px;line-height:22px;display:none">%s</span>'
) % (SANS, _bio_collapsed_html, SANS, _bio_expanded_html)}, "styles":[{"prop":"width","value":"100%"}]}
byline_bio = col([
    byline_bio_toggle,
    text("Last updated 18 July 2026", size="12.5px", lh="16px", color=MUTED, font=SANS),
], gap="6px", styles=[{"prop":"flex","value":"1"},{"prop":"minWidth","value":"220px"}])
byline = rowf([
    container([{"t":"Image","id":nid(),"p":{"src_id":IMG["avatar"]["src_id"],
        "src_uid":IMG["avatar"]["src_uid"],"src":IMG["avatar"]["src"]},
        "styles":[{"prop":"width","value":"52px"},{"prop":"height","value":"52px"},
                  {"prop":"borderRadius","value":"50%"},{"prop":"objectFit","value":"cover"}]}],
        [{"prop":"width","value":"52px"},{"prop":"flexShrink","value":"0"}]),
    byline_who, byline_bio], gap="16px", align="center", wrap=True,
    styles=[{"prop":"borderStyle","value":"dashed"},{"prop":"borderColor","value":DASH_BORDER},
        {"prop":"borderWidth","value":"1.5px 0px 1.5px 0px"},
        {"prop":"padding","value":{"top":"16px","bottom":"16px","left":"2px","right":"2px"}}])
kids.append(byline)
kids.append(sp(10))

# hero
kids.extend(figure(img_block("hero", height="403px", mh="196px", border=True)))
kids.append(sp(10))

# NEW hookline + 2 plain intro paragraphs (V2 splits V1's single colored-span
# paragraph into two plain ones with different copy)
kids.append(title("If you've got a smart ring in your shopping cart right now, read this first.",
    "18px","30px", weight="700", font=SERIF))
kids.append(para("£349 is the sticker price. It's not the real price. Add the mandatory £5.99-a-month "
    "membership and you're looking at roughly £560 by year three, on a battery that can't be replaced when "
    "it fades. That's the number the packaging doesn't show you."))
kids.append(para(("I've worn an Oura Ring every day for two years, so this isn't a hit piece from someone "
    "who's never tried one. It's what I wish someone had told me before I bought mine. We spent a month "
    "testing it head to head against the £79 "
    '<a href="%s" target="_blank" style="color:#1A5FD0;text-decoration:underline">HLTH Band</a>'
    ", same days, same workouts, same nights, to find out "
    "exactly what that extra £481 buys you. Some of it's worth paying for. Most of it isn't. Here's the "
    "breakdown before you check out.") % PDP))
kids.append(sp(10))

# ============================== SHOP GRID (2 cards, identical to V1) ========
def shop_button(label, href):
    # Figma spec has a flat 3px offset drop-shadow (#C9CCD2, no blur) on this button.
    # boxShadow 503s the LF SSR renderer (verified gotcha), so it's faked with a
    # background-color wrapper + right/bottom padding instead of a real shadow prop.
    lab={"t":"Text","id":nid(),"p":{"content":label},
        "styles":[{"prop":"fontFamily","value":SANS},{"prop":"color","value":WHITE},
            {"prop":"fontSize","value":"15px"},{"prop":"fontWeight","value":"600"},
            {"prop":"lineHeight","value":"20px"},{"prop":"textAlign","value":"center"}]}
    btn = {"t":"BlockLink","id":nid(),"p":{"destination":{"type":"static","value":href},"target":"_blank",
        "widthOption":"auto","children":[container([lab],[{"prop":"lfDisplay","value":"flex"},
            {"prop":"alignItems","value":"center"},{"prop":"justifyContent","value":"center"}])]},
        "styles":[{"prop":"backgroundColor","value":DARK},{"prop":"padding","value":{"top":"12px","bottom":"12px"}},
            {"prop":"lfDisplay","value":"flex"},{"prop":"alignItems","value":"center"},
            {"prop":"justifyContent","value":"center"},{"prop":"width","value":"100%"}]}
    return container([btn], [{"prop":"backgroundColor","value":HARD_SHADOW},
        {"prop":"padding","value":{"right":"3px","bottom":"3px"}},{"prop":"width","value":"100%"}])

oura_card = col([
    img_block("oura_product", height="351px", radius="6px", fit="cover"),
    col([
        text("Oura", size="13.5px", lh="18px", color=BODY, font=SANS),
        text("Oura Ring 4", size="18px", lh="23px", color=DARK, weight="700", font=SANS),
    ], gap="6px"),
    rowf([inline_text("£349", size="15.5px", lh="21px", color=DARK, font=SANS),
          inline_text("+ £5.99/month membership", size="13px", lh="21px", color=BODY, font=SANS)],
        gap="6px", align="center", wrap=True, styles=[{"prop":"width","value":"fit-content"}]),
    shop_button("Shop Now", OURA_URL),
], gap="12px", styles=[{"prop":"width","value":"100%"}])

hlth_card = col([
    img_block("hlth_product", height="351px", radius="6px", fit="cover"),
    col([
        text("HLTH", size="13.5px", lh="18px", color=BODY, font=SANS),
        text("HLTH Band 1.0", size="18px", lh="23px", color=DARK, weight="700", font=SANS),
    ], gap="6px"),
    rowf([inline_text('<span style="text-decoration:line-through">£158</span>', size="15.5px", lh="21px", color=BODY, font=SANS),
          inline_text("£79", size="15.5px", lh="21px", color=RED, weight="700", font=SANS),
          inline_text("one time, no subscription", size="13px", lh="21px", color=BODY, font=SANS)],
        gap="6px", align="center", wrap=True, styles=[{"prop":"width","value":"fit-content"}]),
    shop_button("Shop Now", PDP),
], gap="12px", styles=[{"prop":"width","value":"100%"}])

kids.append(rowf([oura_card, hlth_card], gap="18px", align="flex-start",
    styles=[{"prop":"flexDirection","value":"column","media":767},{"prop":"gap","value":"32px","media":767}]))
kids.append(sp(10))

kids.append(container([],[{"prop":"width","value":"100%"},{"prop":"height","value":"1px"},
    {"prop":"backgroundColor","value":BORDER}]))
kids.append(sp(10))
kids.append(para("If a wrist band versus a finger ring sounds like apples and oranges, it isn't. Both do the "
    "same job: track your heart, sleep and recovery in the background, no screen, and show you the trends. "
    "The difference is what each body part lets the hardware do. That difference decides almost every round below."))
kids.append(sp(28))

# ============================== TABLE: AT A GLANCE (identical to V1) =======
def cell(content, w, bold=False, color=DARK, bg=None, header=False, align="left"):
    st=[{"prop":"flex","value":str(w)},{"prop":"minWidth","value":"0"},
        {"prop":"padding","value":{"top":"10px","bottom":"10px","left":"12px","right":"10px"}},
        {"prop":"padding","value":{"top":"8px","bottom":"8px","left":"8px","right":"8px"},"media":767},
        {"prop":"borderStyle","value":"solid"},{"prop":"borderColor","value":BORDER},
        {"prop":"borderWidth","value":"0px 1px 1px 0px"}]
    if bg: st.append({"prop":"backgroundColor","value":bg})
    txt_size = "13.5px" if header else "15.5px"
    txt_weight = "700" if (header or bold) else "400"
    txt = text(content, size=txt_size, lh="21px" if not header else "18px", color=color, weight=txt_weight,
               align=align, font=SANS, m={"fontSize":"10.5px" if header else "11.5px",
                                           "lineHeight":"14px" if header else "16px"})
    if header:
        txt["styles"].append({"prop":"letterSpacing","value":"0.4px"})
    return container([txt], st)

def table_row(cells):
    return rowf(cells, gap="0px", align="stretch", styles=[{"prop":"width","value":"100%"}])

AAG_ROWS = [
    ("Price", "£349", "£79 once", "hlth"),
    ("Subscription", "£5.99/mo, mandatory", "None, ever", "hlth"),
    ("3-year cost", "~£560", "£79", "hlth"),
    ("Battery life", "5–8 days rated", "~30 days", "hlth"),
    ("Daytime readings", "\"Under optimal conditions\" · gaps up to 30 min", "Every 5 min · 288/day", "hlth"),
    ("Blood pressure trends", "No", "Day & night", "hlth"),
    ("Sizing", "Sizing kit first", "Adjusts in seconds", "hlth"),
    ("Sleep comfort", "Best in class", "Excellent at 18g", "oura"),
]
kids.append(h2("The Comparison At A Glance"))
kids.append(sp(4))
aag_header = table_row([
    cell("", 220, header=True, bg=TABLEBG),
    cell("OURA RING 4", 280, header=True, bg=TABLEBG),
    cell("HLTH BAND", 220, header=True, bg=TABLEBG),
])
aag_rows = [aag_header]
for label, oura_v, hlth_v, winner in AAG_ROWS:
    aag_rows.append(table_row([
        cell(label, 220, bold=True),
        cell(oura_v, 280, bold=(winner == "oura"), bg=(PINK if winner == "oura" else None)),
        cell(hlth_v, 220, bold=(winner == "hlth"), bg=(PINK if winner == "hlth" else None)),
    ]))
kids.append(container(aag_rows, [{"prop":"width","value":"100%"},
    {"prop":"borderStyle","value":"solid"},{"prop":"borderColor","value":BORDER},
    {"prop":"borderWidth","value":"1px 0px 0px 1px"},{"prop":"borderRadius","value":"6px"}]))
kids.append(sp(6))

# ============================== RANKING · EDITOR'S PICK (identical to V1) ===
PROS = ["No subscription — every feature unlocked at £79", "288 blood-pressure &amp; heart-rate readings a day",
        "Confirmed ~30-day battery life", "18g screen-free design, comfortable to sleep in",
        "Adjusts to any wrist in seconds", "Bicep strap included for steadier training reads"]
CONS = ["Newer company — batches have sold out before", "No built-in GPS (relies on your phone)",
        "No screen — check the app for readings"]

def accordion_block():
    pros_html = "".join('<li style="margin-bottom:4px">%s</li>'%p for p in PROS)
    cons_html = "".join('<li style="margin-bottom:4px">%s</li>'%c for c in CONS)
    body = ('<div style="display:none;padding-top:10px" class="hlth-acc-body">'
        '<div style="display:flex;gap:18px;flex-wrap:wrap;font-family:%s;font-size:13px;line-height:19px;color:#16181C">'
        '<div style="flex:1;min-width:140px"><b style="color:#16181C">Pros</b>'
        '<ul style="margin:6px 0 0;padding-left:16px;color:#4A4F57">%s</ul></div>'
        '<div style="flex:1;min-width:140px"><b style="color:#16181C">Cons</b>'
        '<ul style="margin:6px 0 0;padding-left:16px;color:#4A4F57">%s</ul></div>'
        '</div></div>') % (SANS, pros_html, cons_html)
    summary = ('<div onclick="var b=this.nextElementSibling;b.style.display=b.style.display===\'none\'?\'block\':\'none\';'
        'var c=this.querySelector(\'.hlth-chev\');c.style.transform=b.style.display===\'none\'?\'rotate(0deg)\':\'rotate(180deg)\';" '
        'style="display:flex;align-items:center;gap:8px;cursor:pointer;font-family:%s;font-size:13px;font-weight:600;color:#4A4F57">'
        'Pros &amp; Cons <svg class="hlth-chev" width="10" height="10" viewBox="0 0 10 10" fill="none" '
        'stroke="#E63946" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" '
        'style="transition:transform .2s"><polyline points="1 3 5 7 9 3"/></svg></div>') % SANS
    return {"t":"HtmlElement","id":nid(),"p":{"content":summary+body},"styles":[{"prop":"width","value":"100%"}]}

def rank_card_desktop(img_key="hlth_product_rank"):
    thumb = container([img_block(img_key, height="120px", radius="8px", fit="contain")],
        [{"prop":"width","value":"120px"},{"prop":"flexShrink","value":"0"}])
    _pick_label = text("EDITOR'S PICK", size="12px", lh="16px", color=DARK, weight="800", font=SANS, m=None)
    _pick_label["styles"].append({"prop":"whiteSpace","value":"nowrap"})
    badge = rowf([
        text(STAR, size="15px", lh="16px", color=GOLD, weight="700", font=SANS),
        _pick_label,
    ], gap="6px", align="center", styles=[{"prop":"width","value":"fit-content"},{"prop":"letterSpacing","value":"1.2px"}])
    tprow = rowf([
        text('<a href="%s" target="_blank" style="text-decoration:none;color:inherit">' % TP +
             tp_stars(4.6, "#00B67A", 19) + '&nbsp;&nbsp;<span style="color:#16181C;font-weight:800;font-size:15px">4.6</span>'
             '&nbsp;&nbsp;' + ext_link_icon() + '</a>',
             size="15px", lh="19px", font=SANS),
    ], gap="8px", align="center", styles=[{"prop":"width","value":"fit-content"}])
    main = col([
        badge,
        text("HLTH Band 1.0", size="21px", lh="26px", color=DARK, weight="700", font=SANS),
        tprow,
        accordion_block(),
    ], gap="6px", styles=[{"prop":"flex","value":"1"},{"prop":"minWidth","value":"0"}])
    price_row = rowf([
        inline_text("£79", size="20px", lh="26px", color=DARK, weight="800", font=SANS),
        inline_text('<span style="text-decoration:line-through">£158</span>', size="14px", lh="20px", color=BODY, font=SANS),
    ], gap="5px", align="center", justify="center",
        styles=[{"prop":"width","value":"100%"},{"prop":"margin","value":{"top":"10px"}}])
    _shipping = text("Free UK shipping", size="12.5px", lh="17px", color=BODY, align="center", font=SANS)
    _shipping["styles"].append({"prop":"margin","value":{"top":"3px"}})
    buy = col([
        button("View at HLTH", href=PDP, full=True, size="15px", weight="700", radius="10px", ls="0.3px"),
        price_row,
        _shipping,
    ], gap="0px", styles=[{"prop":"width","value":"200px"},{"prop":"flexShrink","value":"0"},{"prop":"alignItems","value":"center"}])
    row = rowf([thumb, main, buy], gap="20px", align="flex-start",
        styles=[{"prop":"padding","value":{"top":"22px","bottom":"22px","left":"20px","right":"20px"}}])
    card = container([row], [{"prop":"width","value":"100%"},{"prop":"backgroundColor","value":WHITE},
        {"prop":"borderRadius","value":"14px"},{"prop":"borderStyle","value":"solid"},
        {"prop":"borderColor","value":BORDER},{"prop":"borderWidth","value":"1px"}])
    wrapped = soft_card(card)
    wrapped["styles"].append({"prop":"lfDisplay","value":"none","media":767})
    return wrapped

def rank_card_mobile(img_key="hlth_product_rank"):
    badge = text('<span style="color:#F5B301">★</span>&nbsp;<span style="color:#16181C;font-weight:800;letter-spacing:1.2px">EDITOR\'S PICK</span>',
                 size="12px", lh="16px", align="center", font=SANS)
    name = text("HLTH Band 1.0", size="21px", lh="26px", color=DARK, weight="700", align="center", font=SANS)
    img = container([img_block(img_key, height="240px", radius="8px", fit="contain")],
        [{"prop":"width","value":"260px"},{"prop":"maxWidth","value":"100%"},
         {"prop":"margin","value":{"left":"auto","right":"auto"}}])
    tprow = text('<a href="%s" target="_blank" style="text-decoration:none;color:inherit">' % TP +
                 tp_stars(4.6, "#00B67A", 19) + '&nbsp;&nbsp;<span style="color:#16181C;font-weight:800;font-size:15px">4.6</span>'
                 '&nbsp;&nbsp;' + ext_link_icon() + '</a>',
                 size="15px", lh="19px", align="center", font=SANS)
    price_row = text('<span style="font-weight:800;font-size:20px;color:#16181C">£79</span>&nbsp;&nbsp;'
                      '<span style="text-decoration:line-through;color:#4A4F57;font-size:14px">£158</span>',
                 size="20px", lh="26px", align="center", font=SANS)
    buy_block = col([
        button("View at HLTH", href=PDP, full=True, size="15px", weight="700", radius="10px", ls="0.3px"),
        price_row,
        text("Free UK shipping", size="12.5px", lh="17px", color=BODY, align="center", font=SANS),
    ], gap="10px", styles=[{"prop":"alignItems","value":"center"},
        {"prop":"borderStyle","value":"solid"},{"prop":"borderColor","value":BORDER},
        {"prop":"borderWidth","value":"1px 0px 0px 0px"},{"prop":"padding","value":{"top":"16px"}}])
    inner = [badge, name, img, tprow, accordion_block(), buy_block]
    st=[{"prop":"lfDisplay","value":"flex"},
        {"prop":"flexDirection","value":"column"},{"prop":"gap","value":"14px"},
        {"prop":"alignItems","value":"center"},{"prop":"width","value":"100%"},
        {"prop":"backgroundColor","value":WHITE},{"prop":"borderRadius","value":"14px"},
        {"prop":"borderStyle","value":"solid"},{"prop":"borderColor","value":BORDER},
        {"prop":"borderWidth","value":"1px"},
        {"prop":"padding","value":{"top":"22px","bottom":"22px","left":"20px","right":"20px"}}]
    card = {"t":"Container","id":nid(),"styles":st,"p":{"children":inner}}
    # match rank_card_desktop's soft_card() shadow-sliver treatment -- the mobile
    # variant was built as a bare Container and never got it (real CSS boxShadow
    # 503s the SSR renderer, so the whole codebase fakes it this way instead).
    wrapped = soft_card(card)
    wrapped["styles"].append({"prop":"lfDisplay","value":"none"})
    wrapped["styles"].append({"prop":"lfDisplay","value":"flex","media":767})
    return wrapped

def rank_card():
    return [rank_card_desktop(), rank_card_mobile()]

kids.extend(rank_card())
kids.append(sp(28))

# ============================== THE REAL PROBLEM (identical to V1) ==========
kids.append(h2("The Real Problem With Smart Rings"))
kids.append(sp(10))

citation_header = rowf([
    inline_text("SOURCE DOCUMENT", size="11.5px", lh="15px", color=DARK, weight="800", font=SANS, m=None),
    container([], [{"prop":"flex","value":"1"},{"prop":"height","value":"1px"}]),
    inline_text("support.ouraring.com" + "&nbsp;&nbsp;" + ext_link_icon(size=12),
         size="12.5px", lh="15px", color=BODY, font=SANS),
], gap="12px", align="center", styles=[{"prop":"backgroundColor","value":TABLEBG},
    {"prop":"borderStyle","value":"solid"},{"prop":"borderColor","value":BORDER},
    {"prop":"borderWidth","value":"0px 0px 1px 0px"},
    {"prop":"padding","value":{"top":"13px","bottom":"13px","left":"18px","right":"18px"}}])
citation_meta = col([
    text('<span style="color:#4A4F57">article:</span> <span style="color:#16181C">"Heart Rate Graph"</span>', size="13px", lh="20px", font=SANS),
    text('<span style="color:#4A4F57">section:</span> <span style="color:#16181C">Daytime Heart Rate Measurement</span>', size="13px", lh="20px", font=SANS),
    text('<span style="color:#4A4F57">publisher:</span> <span style="color:#16181C">Oura Health Oy · Member Care</span>', size="13px", lh="20px", font=SANS),
    text('<span style="color:#4A4F57">accessed:</span> <span style="color:#16181C">13 August 2026</span>', size="13px", lh="20px", font=SANS),
    text('<span style="color:#4A4F57">url:</span> <span style="color:#16181C">support.ouraring.com/hc/en-us/articles/4410656562579</span>', size="13px", lh="20px", font=SANS),
], gap="3px", styles=[{"prop":"padding","value":{"top":"16px","bottom":"14px","left":"18px","right":"18px"}}])
def _tight(node, ls="-0.25px"):
    # Figma's passage copy is set in SF Pro; we substitute Inter (SF Pro isn't
    # legally embeddable). Inter renders measurably wider per character at the
    # same declared font-size, so at Figma's exact 14.5px/23px/674px-width spec
    # it wraps one word earlier per line than the design. A small negative
    # letter-spacing compensates so the wrap points land where Figma's do.
    node["styles"].append({"prop":"letterSpacing","value":ls})
    return node

citation_passage = col([
    _tight(text("Oura takes measurements of your daytime heart rate for one full minute, every five minutes, using "
         "the Oura Ring's green LEDs.", size="14.5px", lh="23px", color=BODY, font=SANS)),
    container([_tight(text('To preserve battery and maximize accuracy, a daytime heart rate measurement is only taken '
        'under optimal conditions, which include low movement and balanced average body temperature. Due to '
        'prioritizing these conditions, you may not receive an automatically updated heart rate for up to 30 '
        'minutes, but it can be manually updated at any time by using Live Heart Rate.',
        size="14.5px", lh="23px", color=DARK, font=SANS))],
        [{"prop":"backgroundColor","value":HILITE_YEL},{"prop":"borderRadius","value":"2px"},
         {"prop":"padding","value":{"top":"3px","bottom":"3px","left":"5px","right":"5px"}},
         {"prop":"margin","value":{"top":"4px"}}]),
], gap="0px", styles=[{"prop":"padding","value":{"left":"18px","right":"18px","bottom":"18px"}}])
citation_card = soft_card(container([citation_header, citation_meta, citation_passage],
    [{"prop":"width","value":"100%"},{"prop":"backgroundColor","value":WHITE},
     {"prop":"borderRadius","value":"12px"},{"prop":"borderStyle","value":"solid"},
     {"prop":"borderColor","value":BORDER},{"prop":"borderWidth","value":"1px"}]), radius="12px")
kids.append(citation_card)
kids.append(caption("Oura Member Care, “Heart Rate Graph”, accessed 13 August 2026. Highlight added."))
kids.append(sp(10))

kids.append(para("Let's get one thing straight first, because it matters for fairness. When the Oura Ring "
    "takes a reading, it reads well. This round isn't about accuracy. It's about how often it reads, and here "
    "the ring's own documentation does the talking."))
kids.append(para('Oura’s support pages explain that a daytime heart rate measurement is only taken '
    '“under optimal conditions” to “preserve battery,” and that you “may not receive an '
    'automatically updated heart rate for up to 30 minutes.” The same docs note you can turn Activity heart '
    'rate off entirely in Settings, and that an activity “must last at least 10 minutes to be automatically '
    'detected,” with the ring holding “at least five percent battery.” None of this is bad '
    'engineering. It’s the only way a battery that small survives the week.'))
kids.append(para("The band never has to make that choice. A reading every five minutes, 288 a day, no "
    "conditions, no off-switches, no battery floor. Health tracking only works as an unbroken line, and every "
    "gap resets what your trends can tell you."))
kids.append(winline_hlth())
kids.append(sp(28))

# ============================== BATTERY LIFE (identical to V1) ==============
kids.append(h2("Battery Life: The Physics Behind The Gaps"))
kids.append(para("Everything above has one cause. Teardowns put the Oura Ring 4's battery at roughly 15 to 22 "
    "mAh depending on size, smaller than a hearing aid's, and the newest ring went smaller still. The band "
    "class runs on cells around ten times larger or more. That single number explains the rationing."))
kids.append(sp(4))

def bar_row(label, value, pct, color):
    # Figma node 36:240: each row is TWO STACKED lines -- a "bhead" line (label
    # left / value right, on one baseline, a flexible 1px spacer between them)
    # then a spacer(6) then a FULL-WIDTH track/fill bar underneath. Not a single
    # label+bar+value row (that was V1's layout, not V2's).
    bhead = rowf([
        text(label, size="15px", lh="20px", color=DARK, weight="700", font=SANS),
        container([], [{"prop":"flex","value":"1"},{"prop":"height","value":"1px"}]),
        text(value, size="13.5px", lh="20px", color=BODY, align="right", font=SANS),
    ], gap="12px", align="baseline")
    track = container([container([], [{"prop":"width","value":"%d%%"%pct},{"prop":"height","value":"100%"},
        {"prop":"borderRadius","value":"999px"},{"prop":"backgroundColor","value":color}])],
        [{"prop":"width","value":"100%"},{"prop":"height","value":"14px"},
         {"prop":"borderRadius","value":"999px"},{"prop":"backgroundColor","value":CHART_TRACK}])
    return col([bhead, track], gap="6px", styles=[{"prop":"width","value":"100%"}])

battery_chart = col([
    bar_row("HLTH Band", "~30 days per charge", 100, RED),
    bar_row("Oura Ring 4 (rated)", "5–8 days", 27, CHART_GRAY),
    bar_row("Oura Ring 4 (owner-reported)", "~4–7 days, shrinking with age", 23, CHART_GRAY),
], gap="16px", styles=[{"prop":"width","value":"100%"},{"prop":"margin","value":{"top":"6px"}}])
kids.append(battery_chart)
kids.append(text("Days between charges · manufacturer ratings and owner reports · longer is better",
    size="12.5px", lh="18px", color=BODY, font=SANS))
kids.append(para("It costs you twice more. The ring charges once or twice a week, 20 to 80 minutes at a time, "
    "and every charge is a hole in your baseline. Charge it overnight and the sleep tracker misses the sleep. "
    "And iFixit rates the ring's battery non-replaceable, so as it degrades, and owners report real-world life "
    "shrinking within a year or so, the £349 ring is counting down to a full re-buy. The band charges once a "
    "month and keeps charging for years."))
kids.append(winline_hlth())
kids.append(sp(28))

# ============================== HEART TRACKING (identical to V1) ============
kids.append(h2("Heart Tracking: The Open Lane"))
kids.append(container([], [{"prop":"width","value":"100%"},{"prop":"height","value":"33px"},
    {"prop":"height","value":"29px","media":767},{"prop":"lfDisplay","value":"block"}]))
kids.extend(figure(img_block("heart_bp", height="401px", mh="195px", border=True, fit="contain")))
kids.append(sp(10))
kids.append(text(('<span style="color:#16181C">Here\'s where the comparison stops being close. The Oura Ring '
    'doesn\'t measure blood pressure. No shipping smart ring does. The </span>'
    '<a href="%s" target="_blank" style="color:#1A5FD0;text-decoration:underline">HLTH Band</a>'
    '<span style="color:#16181C"> tracks blood pressure trends around the clock, one of the only devices at '
    'any price to do it without a subscription. Orange line for systolic, purple for diastolic, every rise and '
    'dip across the day, with the normal range printed underneath so you know what good looks like without '
    'Googling it.</span>') % PDP, font=SERIF))
kids.append(para("Around it sits the rest of the heart picture: continuous heart rate on a full-day graph, HRV "
    "overnight, blood oxygen as a simple percentage. Trends for your own awareness rather than medical "
    "readings, but if your heart is the reason you're shopping for a tracker, only one of these two shows you "
    "the number your GP asks about."))
kids.append(winline_hlth_plain())
kids.append(sp(28))

# ============================== SLEEP TRACKING (identical to V1) ============
kids.append(h2("Sleep Tracking: Oura's Home Turf"))
kids.append(sp(10))
kids.extend(figure(img_block("sleep_screens", height="403px", mh="230px", border=True)))
kids.append(sp(10))
kids.append(para("Credit where it's due, and Oura has earned plenty. A ring is the most comfortable thing you "
    "can sleep in, three quarters of ring owners name sleep as their main use, and Oura's sleep analysis is the "
    "most polished in the business. Readiness scores, sleep staging, the lot."))
kids.append(para("The band is close. At 18 grams I forgot it overnight, and it splits the night into light, "
    "deep and REM with total hours at the top. But close isn't a win. If sleep is your only priority and the "
    "price doesn't sting, buy the ring. Just charge it in the daytime, because a sleep tracker sitting on a "
    "charger at night has missed the point."))
kids.append(winline_oura())
kids.append(sp(28))

# ============================== TRAINING (identical to V1) ==================
kids.append(h2("Training: Where The Ring Comes Off"))
kids.append(sp(10))
kids.extend(figure(img_block("training", height="430px", mh="230px", border=True)))
kids.append(sp(10))
kids.append(para("Grabbing a bar scratches titanium, a complaint you'll find in every Oura owner forum, so the "
    "ring comes off for weights. It comes off for trades, for gardening, for anything where a metal ring meets "
    "heavy objects. Off your finger means not measuring, and even dedicated ring reviewers concede a wrist "
    "device delivers more reliable workout metrics. The band stays on, and ships with a bicep strap for "
    "steadier readings when you train. Takes about ten seconds to swap."))
kids.append(winline_hlth())
kids.append(sp(28))

# ============================== EVERYDAY LIFE (identical to V1) =============
kids.append(h2("Everyday Life And Comfort"))
kids.append(sp(10))
kids.extend(figure(img_block("lifestyle", height="430px", mh="230px", border=True)))
kids.append(sp(10))
kids.append(para("The ring is the better piece of jewellery, and honestly it's not close. If you want a "
    "tracker nobody clocks at dinner, Oura wins on looks."))
kids.append(para('Living with it is where the friction hides. You order a sizing kit, wait, measure, and '
    'sometimes still get it wrong. It’s a small object that goes in a gym bag pocket and doesn’t '
    'always come back out, which is why “find my Oura ring” is popular enough to be its own article '
    'genre. The band adjusts on your wrist in seconds, fits anyone in the house, works with iPhone and Android '
    'both, and weighs less than most watch straps alone.'))
kids.append(winline_hlth())
kids.append(sp(28))

# ============================== PRICE / COST CHART (NEW chart type in V2) ===
kids.append(h2("Price: The Cost Over Three Years"))
kids.append(sp(10))

def legend_item(color_hex, label):
    # Figma swatch (36:319/36:322) is a 14x3 rounded-rect LINE sample (matching
    # the chart's own line strokes), not a round dot.
    return rowf([
        container([],[{"prop":"width","value":"14px"},{"prop":"height","value":"3px"},
            {"prop":"borderRadius","value":"999px"},{"prop":"backgroundColor","value":
                {"r":int(color_hex[0:2],16),"g":int(color_hex[2:4],16),"b":int(color_hex[4:6],16),"a":1}}]),
        inline_text(label, size="12px", lh="15px", color=BODY, font=SANS, m={"fontSize":"10.5px"})], gap="6px", align="center",
        styles=[{"prop":"width","value":"fit-content"},{"prop":"flexShrink","value":"0"}])

def cost_chart_v2():
    """Line/area cost chart -- V2 replaced V1's horizontal-bar cost chart with
    a genuinely different chart type (two diverging lines: flat HLTH £79 vs
    rising Oura £349->421->493->560, a shaded '£481 gap' area between them,
    gridlines at £0/£200/£400/£600, and x-axis labels 'At purchase/Year 1/2/3').
    Measured from Figma node 36:314 (Plot area 36:325, 676x240; y-scale
    35px per £100). Rebuilt as an inline SVG since it can't be reproduced with
    bar-row helpers."""
    _eyebrow = inline_text("WHAT YOU HAVE SPENT, RUNNING TOTAL", size="12px", lh="15px", color=DARK, weight="800", font=SANS,
             m={"fontSize":"10.5px"})
    _eyebrow["styles"].append({"prop":"letterSpacing","value":"0.8px"})
    _eyebrow["styles"].append({"prop":"flexShrink","value":"0"})
    header = rowf([
        _eyebrow,
        rowf([legend_item("9AA0A8", "Oura Ring 4"), legend_item("E63946", "HLTH Band")],
            gap="14px", justify="flex-end", styles=[{"prop":"width","value":"fit-content"}]),
    ], gap="10px", align="center", justify="flex-start", wrap=True)

    # ---- DESKTOP plot (measured from Figma 36:314/36:325, 676x210, 35px/£100) ----
    W, H = 676, 210
    def y_of(gbp): return H - (gbp/600.0)*H
    xs = [4, 185.33, 370.67, 556]  # dot centers
    oura_vals = [349, 421, 493, 560]
    hlth_vals = [79, 79, 79, 79]
    oura_pts = [(x, y_of(v)) for x, v in zip(xs, oura_vals)]
    hlth_pts = [(x, y_of(v)) for x, v in zip(xs, hlth_vals)]
    oura_line = " ".join("%.1f,%.1f" % p for p in oura_pts)
    hlth_line = " ".join("%.1f,%.1f" % p for p in hlth_pts)
    gap_poly = " ".join("%.1f,%.1f" % p for p in oura_pts) + " " + " ".join("%.1f,%.1f" % p for p in reversed(hlth_pts))
    grid_labels = [("£0", H), ("£200", H - (200/600.0)*H), ("£400", H - (400/600.0)*H), ("£600", 0)]
    x_labels = [("At purchase", xs[0], "start"), ("Year 1", xs[1], "middle"),
                ("Year 2", xs[2], "middle"), ("Year 3", xs[3], "end")]
    svg = ['<svg viewBox="0 0 %d %d" width="100%%" height="%dpx" style="display:block;font-family:%s">'
           % (W + 44, H + 34, H + 34, SANS)]
    svg.append('<g transform="translate(44,0)">')
    for label, gy in grid_labels:
        # Figma's gridlines stop exactly at the last dot (xs[3]=556), not the
        # full plot width (676) -- they don't run under the end-value labels.
        svg.append('<line x1="0" y1="%.1f" x2="%.1f" y2="%.1f" stroke="#ECECEE" stroke-width="1"/>' % (gy, xs[3], gy))
        svg.append('<text x="-8" y="%.1f" text-anchor="end" dominant-baseline="middle" font-size="11" fill="#4A4F57">%s</text>' % (gy, label))
    svg.append('<polygon points="%s" fill="#E2483D17"/>' % gap_poly)
    svg.append('<polyline points="%s" fill="none" stroke="#9AA0A8" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"/>' % oura_line)
    svg.append('<polyline points="%s" fill="none" stroke="#E63946" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"/>' % hlth_line)
    for x, y in oura_pts:
        svg.append('<circle cx="%.1f" cy="%.1f" r="4" fill="#fff" stroke="#9AA0A8" stroke-width="2.5"/>' % (x, y))
    for x, y in hlth_pts:
        svg.append('<circle cx="%.1f" cy="%.1f" r="4" fill="#fff" stroke="#E63946" stroke-width="2.5"/>' % (x, y))
    svg.append('<text x="%.1f" y="%.1f" font-size="13" font-weight="800" fill="#16181C">~£560</text>' % (xs[3] + 8, oura_pts[3][1] - 4))
    svg.append('<text x="%.1f" y="%.1f" font-size="13" font-weight="800" fill="#E63946">£79</text>' % (xs[3] + 8, hlth_pts[3][1] + 12))
    gap_mid_x = (xs[1] + xs[2]) / 2
    gap_mid_y = (y_of(421) + y_of(79)) / 2
    svg.append('<text x="%.1f" y="%.1f" text-anchor="middle" font-size="13" font-weight="800" fill="#E63946">£481 gap</text>' % (gap_mid_x, gap_mid_y))
    for label, x, anchor in x_labels:
        svg.append('<text x="%.1f" y="%d" text-anchor="%s" font-size="11" fill="#4A4F57">%s</text>' % (x, H + 20, anchor, label))
    svg.append('</g></svg>')
    plot_desktop_svg = "".join(svg)

    # ---- MOBILE plot (measured from Figma 12:1902/12:1903/12:1914 -- this is a
    # genuinely different composition from desktop, not a scaled copy: narrower
    # plot (216 vs 676 wide Lines), shallower y-scale (150 vs 210 tall, 25px/£100
    # vs 35px/£100), and independently-sized type (9.5-11.5px vs 11-13px). Using
    # a single shared SVG uniformly rescaled for mobile crushed its text and
    # left the plot letterboxed -- built as its own SVG instead, at a 1:1
    # viewBox-to-CSS-px scale (viewBox width 318 == the mobile card's own inner
    # width at 16px padding), so font-size units land on-screen exactly as
    # Figma specifies with no scale-compensation math needed.
    MW, MH = 318, 150  # Plot area width, Lines height (£0..£600, 25px/£100)
    LX = 36  # x where Lines starts (28px y-axis-label column + 8px gap)
    RX = LX + 216  # Lines right edge
    TOP_PAD_M = 14  # headroom for the £600 gridline label + "~£560" end-label
    def y_of_m(gbp): return MH - (gbp/600.0)*MH
    mxs = [LX, LX + 72, LX + 144, RX]  # evenly-spaced dot x's -- match the x-axis label anchors exactly
    m_oura_pts = [(x, y_of_m(v)) for x, v in zip(mxs, oura_vals)]
    m_hlth_pts = [(x, y_of_m(v)) for x, v in zip(mxs, hlth_vals)]
    m_oura_line = " ".join("%.1f,%.1f" % p for p in m_oura_pts)
    m_hlth_line = " ".join("%.1f,%.1f" % p for p in m_hlth_pts)
    m_gap_poly = " ".join("%.1f,%.1f" % p for p in m_oura_pts) + " " + " ".join("%.1f,%.1f" % p for p in reversed(m_hlth_pts))
    m_grid_labels = [("£0", 150), ("£200", 100), ("£400", 50), ("£600", 0)]
    m_x_labels = [("Buy", LX, "start"), ("Yr 1", LX + 72, "middle"),
                  ("Yr 2", LX + 144, "middle"), ("Yr 3", RX, "end")]
    total_h_m = MH + TOP_PAD_M + 24  # + room for the x-axis label row below Lines
    msvg = ['<svg viewBox="0 -%d %d %d" width="100%%" height="%dpx" style="display:block;font-family:%s">'
            % (TOP_PAD_M, MW, total_h_m, total_h_m, SANS)]
    for label, gy in m_grid_labels:
        msvg.append('<line x1="%d" y1="%.1f" x2="%d" y2="%.1f" stroke="#ECECEE" stroke-width="1"/>' % (LX, gy, RX, gy))
        msvg.append('<text x="28" y="%.1f" text-anchor="end" dominant-baseline="middle" font-size="9.5" fill="#4A4F57">%s</text>' % (gy, label))
    msvg.append('<polygon points="%s" fill="#E2483D17"/>' % m_gap_poly)
    msvg.append('<polyline points="%s" fill="none" stroke="#9AA0A8" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>' % m_oura_line)
    msvg.append('<polyline points="%s" fill="none" stroke="#E63946" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>' % m_hlth_line)
    for x, y in m_oura_pts:
        msvg.append('<circle cx="%.1f" cy="%.1f" r="3.5" fill="#fff" stroke="#9AA0A8" stroke-width="2"/>' % (x, y))
    for x, y in m_hlth_pts:
        msvg.append('<circle cx="%.1f" cy="%.1f" r="3.5" fill="#fff" stroke="#E63946" stroke-width="2"/>' % (x, y))
    msvg.append('<text x="%.1f" y="2" dominant-baseline="hanging" font-size="11.5" font-weight="800" fill="#16181C">~£560</text>' % (RX + 8))
    msvg.append('<text x="%.1f" y="122.25" dominant-baseline="hanging" font-size="11.5" font-weight="800" fill="#E63946">£79</text>' % (RX + 8))
    msvg.append('<text x="165.6" y="62.125" dominant-baseline="hanging" font-size="11.5" font-weight="800" fill="#E63946">£481 gap</text>')
    for label, x, anchor in m_x_labels:
        msvg.append('<text x="%.1f" y="160" dominant-baseline="hanging" text-anchor="%s" font-size="9.5" fill="#4A4F57">%s</text>' % (x, anchor, label))
    msvg.append('</svg>')
    plot_mobile_svg = "".join(msvg)

    plot_desktop = {"t":"Container","id":nid(),
        "styles":[{"prop":"width","value":"100%"},{"prop":"lfDisplay","value":"block"},
                  {"prop":"lfDisplay","value":"none","media":767}],
        "p":{"children":[{"t":"HtmlElement","id":nid(),"p":{"content":plot_desktop_svg},"styles":[{"prop":"width","value":"100%"}]}]}}
    plot_mobile = {"t":"Container","id":nid(),
        "styles":[{"prop":"width","value":"100%"},{"prop":"lfDisplay","value":"none"},
                  {"prop":"lfDisplay","value":"block","media":767}],
        "p":{"children":[{"t":"HtmlElement","id":nid(),"p":{"content":plot_mobile_svg},"styles":[{"prop":"width","value":"100%"}]}]}}

    def _mspacer(mobile_px):
        return container([], [{"prop":"width","value":"100%"},{"prop":"height","value":"0px"},
            {"prop":"height","value":"%dpx"%mobile_px,"media":767},{"prop":"lfDisplay","value":"block"}])

    footnote = container([text("Oura Ring 4: £349 ring plus £5.99 a month mandatory membership. HLTH Band: £79 "
        "once, no subscription. Running totals, rounded. Prices checked 13 August 2026.",
        size="12px", lh="17px", color=BODY, font=SANS, m={"fontSize":"10.5px"})],
        [{"prop":"borderStyle","value":"solid"},{"prop":"borderColor","value":BORDER},
         {"prop":"borderWidth","value":"1px 0px 0px 0px"},{"prop":"padding","value":{"top":"12px"}},
         # desktop has no explicit spacer before the footnote, so this margin IS
         # its gap; mobile now has an explicit _mspacer(16) instead (matching
         # Figma's mobile "spacer 16" node), so zero this out there to avoid
         # double-counting the gap.
         {"prop":"margin","value":{"top":"6px"}},{"prop":"margin","value":{"top":"0px"},"media":767}])

    return soft_card(col([header, _mspacer(20), plot_desktop, plot_mobile, _mspacer(16), footnote], gap="0px",
        styles=[{"prop":"width","value":"100%"},{"prop":"backgroundColor","value":WHITE},
            {"prop":"borderRadius","value":"12px"},{"prop":"borderStyle","value":"solid"},
            {"prop":"borderColor","value":BORDER},{"prop":"borderWidth","value":"1px"},
            {"prop":"padding","value":{"top":"22px","bottom":"22px","left":"22px","right":"22px"}},
            {"prop":"padding","value":{"top":"16px","bottom":"16px","left":"16px","right":"16px"},"media":767}]),
        radius="12px")

kids.append(cost_chart_v2())
kids.append(caption("Three-year running cost, both devices. (Chart: TechUnboxed)"))
kids.append(sp(10))

# 3-year cost table (identical to V1)
COST_ROWS = [
    ("Upfront", "£349", "£79"),
    ("Year 1 total", "~£421", "£79"),
    ("Year 2 total", "~£493", "£79"),
    ("Year 3 total", "~£560", "£79"),
]
cost_header_row = table_row([
    cell("", 220, header=True, bg=TABLEBG),
    cell("OURA RING 4", 280, header=True, bg=TABLEBG),
    cell("HLTH BAND", 220, header=True, bg=TABLEBG),
])
cost_rows = [cost_header_row]
for label, oura_v, hlth_v in COST_ROWS:
    cost_rows.append(table_row([
        cell(label, 220, bold=True),
        cell(oura_v, 280),
        cell(hlth_v, 220, bold=True, bg=PINK),
    ]))
kids.append(container(cost_rows, [{"prop":"width","value":"100%"},
    {"prop":"borderStyle","value":"solid"},{"prop":"borderColor","value":BORDER},
    {"prop":"borderWidth","value":"1px 0px 0px 1px"},{"prop":"borderRadius","value":"6px"}]))
kids.append(sp(4))
kids.append(para("The membership is mandatory. Without the £5.99 a month, the app locks you down to basics, "
    "and the CEO has publicly said the paywall stays. So by year three you've paid about £560 to rent your own "
    "heart data, on a battery you can't replace. The band is £79, once, everything unlocked at purchase. "
    "That's £481 that stays in your pocket."))
kids.append(winline_hlth())
kids.append(sp(28))

# ============================== FINAL JUDGEMENT (identical to V1) ===========
kids.append(h2("Final Judgement"))
kids.append(para("Six rounds to the band, one to the ring. The Oura Ring 4 is a premium sleep tracker with a "
    "membership model attached, and if that's what you want, it's a good one. But if the question is health "
    "tracking, continuous coverage, blood pressure trends, training that stays measured, and a price that "
    "doesn't compound, the band wins this comparison walking away."))
kids.append(sp(8))
kids.extend(rank_card())
kids.append(sp(8))
kids.append(text('By year three the ring costs about £560, on a battery that can’t be replaced. The band '
    'costs £79, once, with a 30-day money-back guarantee. If you’ve been typing “is the Oura Ring '
    'worth it” into Google, this is a £79 way to answer the question.', size="18px", lh="30px", font=SERIF))
kids.append(container([button("Check HLTH Band Availability →", href=PDP, full=True, size="15px", weight="700",
    pad_v="12px", pad_h="20px")],
    [{"prop":"width","value":"100%"}]))
kids.append(sp(28))

# ============================== FAQs (identical to V1) ======================
kids.append(h2("Your Questions, Answered"))
kids.append(sp(10))
def faq(q, a_html):
    return col([
        title(q, "19px", "25px", weight="700", font=SERIF),
        text(a_html, size="18px", lh="30px", color=DARK, font=SERIF),
    ], gap="8px")

kids.append(faq("Is the Oura Ring worth it?",
    "If premium sleep tracking is your main goal and the £349 plus £5.99 a month doesn't bother you, it's the "
    "best ring made. For all-day health tracking, the band covers more, tracks blood pressure trends the ring "
    "can't, and costs £79 once."))
kids.append(sp(10))
kids.append(faq("Can I use the Oura Ring without the subscription?",
    "Technically yes, but the app locks you down to a handful of basic scores. The membership is effectively "
    "mandatory for the features people buy the ring for, and Oura has said publicly it isn't going away."))
kids.append(sp(10))
kids.append(faq("Does the Oura Ring measure blood pressure?",
    ('No. No shipping smart ring does. The <a href="%s" target="_blank" '
    'style="color:#1A5FD0;text-decoration:underline">HLTH Band</a> '
    'tracks blood pressure trends day and night, as wellness trends for your own awareness rather than medical '
    'readings.') % PDP))
kids.append(sp(10))

YOUTUBE_EMBED_URL = "https://www.youtube.com/embed/lMZoKLSmd6M"
_video_embed_html = (
    '<div style="position:relative;width:100%%;padding-bottom:56.25%%;height:0;'
    'border-radius:12px;border:1px solid #E4E6E2;overflow:hidden">'
    '<iframe src="%s" title="HLTH Band Accuracy Test Video" '
    'style="position:absolute;top:0;left:0;width:100%%;height:100%%;border:0" '
    'allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" '
    # QA: this was the only page of the eleven whose embed lacked loading="lazy",
    # so it pulled the full YouTube player + doubleclick ad_status.js on load --
    # 64 requests vs 49 on V3, and the only PSI mobile score under 90.
    'allowfullscreen loading="lazy"></iframe></div>' % YOUTUBE_EMBED_URL)
video_placeholder = container(
    [{"t":"HtmlElement","id":nid(),"p":{"content":_video_embed_html},"styles":[{"prop":"width","value":"100%"}]}],
    [{"prop":"width","value":"100%"}])

kids.append(col([
    title("How accurate is the HLTH Band?", "19px", "25px", weight="700", font=SERIF),
    text('Per reading, both devices use capable optical sensors, and this comparison has never claimed '
         'otherwise for either. The meaningful difference is coverage: the band reads every five minutes '
         'around the clock, while the ring measures “under optimal conditions” to protect its '
         'battery, with gaps of up to 30 minutes by Oura’s own documentation. Rather than take our word '
         'for it, watch the band tested on video, worn day and night rather than filmed in a studio:',
         size="18px", lh="30px", color=DARK, font=SERIF),
    video_placeholder,
], gap="8px"))
kids.append(sp(10))

kids.append(faq("What do people say about the HLTH Band?",
    "One of the harder places for any brand to shape its own reputation is its Trustpilot page, since "
    "Trustpilot verifies reviewers and penalises companies caught manipulating scores. The HLTH Band holds a "
    "4.6 rating there, and the same themes keep coming up: the battery genuinely lasts weeks, the band is "
    "light enough to forget, and there's nothing to pay after the £79. Read them unfiltered before you "
    'decide.<br><br><a href="%s" target="_blank" style="color:#1A5FD0;text-decoration:underline">Read the HLTH '
    "Band's Trustpilot reviews →</a>" % TP))
kids.append(sp(10))
kids.append(faq("Does the HLTH Band need a subscription?",
    "No. Every feature is unlocked at the £79 purchase, permanently, and it comes with a 30-day money-back "
    "guarantee."))
kids.append(sp(32))

# ============================== ENDMATTER (identical to V1, + new top rule) ==
endmatter_kids = []
endmatter_kids.append(sp(24))
endmatter_kids.append(title("Sources", "22px", "27px", weight="700", ls="-0.22px", font=SERIF))
endmatter_kids.append(sp(12))
endmatter_kids.append(text('Oura Ring 4 pricing and membership: <a href="https://ouraring.com" target="_blank" '
    'style="color:#1A5FD0;text-decoration:underline">ouraring.com</a> (checked 8 August 2026). Heart-rate '
    'measurement behaviour: Oura Member Care, “Heart Rate Graph” and “Activity Heart Rate” '
    'support articles (accessed 8 August 2026). Battery capacities and non-replaceable battery assessment: '
    'iFixit teardowns (June 2026); published Oura Ring 4 specifications. HLTH Band specifications: '
    '<a href="https://hlthtrack.co.uk" target="_blank" style="color:#1A5FD0;text-decoration:underline">hlthtrack.co.uk</a>. '
    '£79 is a launch price; standard price £158. Three-year Oura cost: £349 + 36 × £5.99 ≈ £560. Prices may '
    'have changed since checking.', size="13.5px", lh="22px", color=BODY, font=SERIF))
endmatter_kids.append(sp(14))
endmatter_kids.append(container([text('<b style="color:#4A4F57">Disclaimer.</b> <span style="color:#4A4F57">HLTH Band '
    'is not a medical device; readings show trends and are not a substitute for medical measurement or '
    'advice. This page is an advertisement for </span><a href="%s" target="_blank" '
    'style="color:#1A5FD0;text-decoration:underline">HLTH Band</a>.' % PDP,
    size="13.5px", lh="22px", font=SERIF)],
    [{"prop":"borderStyle","value":"solid"},{"prop":"borderColor","value":BORDER},
     {"prop":"borderWidth","value":"1px 0px 0px 0px"},{"prop":"padding","value":{"top":"14px"}}]))
endmatter_kids.append(sp(30))
endmatter_kids.append(title("About the Author", "22px", "27px", weight="700", ls="-0.22px", font=SERIF))
endmatter_kids.append(sp(12))
author_avatar = container([{"t":"Image","id":nid(),"p":{"src_id":IMG["avatar_author"]["src_id"],
    "src_uid":IMG["avatar_author"]["src_uid"],"src":IMG["avatar_author"]["src"]},
    "styles":[{"prop":"width","value":"78px"},{"prop":"height","value":"78px"},
              {"prop":"borderRadius","value":"50%"},{"prop":"objectFit","value":"cover"}]}],
    [{"prop":"width","value":"78px"},{"prop":"flexShrink","value":"0"}])
author_box = rowf([author_avatar, col([
    text("Marcus Pendleton", size="18px", lh="23px", color=DARK, weight="700", font=SANS),
    text("Principal Writer, Wearables — TechUnboxed", size="13.5px", lh="18px", color=BODY, font=SANS),
    text("Marcus has spent six years testing wearables for TechUnboxed, more than 40 devices across "
         "smartwatches, rings and screen-free bands. He wears an Oura Ring daily and rotates test devices on "
         "his other wrist, and after a family history of high blood pressure he pays close attention to how "
         "everyday trackers handle heart and cardiovascular data.", size="14.5px", lh="22px", color=DARK, font=SANS,
         m={"fontSize":"13.5px","lineHeight":"21px"}),
    text("Before TechUnboxed he spent a decade in consumer electronics retail. He tests every device himself, "
         "day and night, for at least 30 days before writing about it.", size="13px", lh="20px", color=BODY, font=SANS),
], gap="8px", styles=[{"prop":"flex","value":"1"},{"prop":"minWidth","value":"0"}])],
    gap="18px", align="flex-start",
    styles=[{"prop":"backgroundColor","value":TABLEBG},{"prop":"borderStyle","value":"solid"},
        {"prop":"borderColor","value":BORDER},{"prop":"borderWidth","value":"1px"},
        {"prop":"borderRadius","value":"14px"},
        {"prop":"padding","value":{"top":"20px","bottom":"20px","left":"20px","right":"20px"}},
        {"prop":"flexDirection","value":"column","media":767},{"prop":"alignItems","value":"flex-start","media":767}])
endmatter_kids.append(author_box)

# NEW in V2: 2px solid black top rule before the whole endmatter block (V1 had none)
endmatter = col(endmatter_kids, gap="0px",
    styles=[{"prop":"borderStyle","value":"solid"},{"prop":"borderColor","value":DARK},
            {"prop":"borderWidth","value":"2px 0px 0px 0px"},{"prop":"padding","value":{"top":"6px"}}])
kids.append(endmatter)

article_col = container(kids,
    [{"prop":"maxWidth","value":"720px"},{"prop":"width","value":"100%"},
     {"prop":"margin","value":{"left":"auto","right":"auto"}},
     {"prop":"padding","value":{"left":"20px","right":"20px"},"media":767},
     {"prop":"lfDisplay","value":"flex"},{"prop":"flexDirection","value":"column"},{"prop":"gap","value":"16px"}])

# ============================== FOOTER LEGAL (identical to V1) =============
MEDICAL_DISCLAIMER = ('<b style="color:#4A4F57">Disclaimer.</b> This product is a general wellness and fitness '
    'device. It is not a medical device and is not intended to diagnose, treat, cure, or prevent any disease or '
    'health condition, including any heart condition. Its readings (including heart rate, heart rate '
    'variability, blood pressure, and blood oxygen) are estimates for general wellness purposes only, are not '
    'clinically validated, and should not be relied upon for any medical decision. Do not use this device to '
    'detect, monitor, or manage any medical condition. It is not a substitute for professional medical advice, '
    'examination, diagnosis, or treatment, or for medical-grade monitoring equipment. Always consult a '
    'qualified physician or healthcare provider with any questions about your health, and if you experience '
    'symptoms such as chest pain, shortness of breath, or dizziness, seek emergency care immediately. '
    'Individual results may vary.')
ADVERTORIAL_DISCLOSURE = ('<b style="color:#4A4F57">Advertorial disclosure.</b> This article is promotional '
    'content published as part of a paid advertising campaign. Some links are affiliate or advertising links '
    'and we may earn a commission at no extra cost to you. Prices, discounts and stock messaging are set by '
    "the retailer and confirmed only at checkout on the retailer's website.")
COPYRIGHT = ('© 2026 TechUnboxed · <a href="#tu-terms" id="terms" style="color:#4A4F57;text-decoration:underline">Terms</a> · '
    '<a href="#tu-priv" id="priv" style="color:#4A4F57;text-decoration:underline">Privacy</a> · '
    '<a href="#tu-edit" id="edit" style="color:#4A4F57;text-decoration:underline">Editorial standards</a> · '
    '<a href="#tu-aff" id="aff" style="color:#4A4F57;text-decoration:underline">Affiliate policy</a>')

footer_col = col([
    text(MEDICAL_DISCLAIMER, size="12.5px", lh="20px", color=BODY, align="left", font=SANS),
    text(ADVERTORIAL_DISCLOSURE, size="12.5px", lh="20px", color=BODY, align="left", font=SANS),
    text(COPYRIGHT, size="12.5px", lh="20px", color=BODY, align="left", font=SANS),
], gap="12px", styles=[{"prop":"maxWidth","value":"720px"},{"prop":"margin","value":{"left":"auto","right":"auto"}},
    {"prop":"alignItems","value":"flex-start"}])

footer = {"t":"Section","id":nid(),
    "styles":[{"prop":"backgroundColor","value":TABLEBG},
              {"prop":"borderStyle","value":"solid"},{"prop":"borderColor","value":BORDER},
              {"prop":"borderWidth","value":"1px 0px 0px 0px"},
              {"prop":"padding","value":{"top":"28px","bottom":"28px","left":"40px","right":"40px"}},
              {"prop":"padding","value":{"left":"20px","right":"20px"},"media":767}],
    "p":{"layout":"boxed","dividerPosition":["top"],"horizontalFlip":False,
         "embedded_video":{"src":"","video_size":"stretch","video_position":"center"},
         "children":[footer_col]}}

article = {"t":"Section","id":nid(),
    "styles":[{"prop":"backgroundColor","value":WHITE},{"prop":"padding","value":{"top":"22px","bottom":"48px"}}],
    "p":{"layout":"boxed","dividerPosition":["top"],"horizontalFlip":False,
         "embedded_video":{"src":"","video_size":"stretch","video_position":"center"},"children":[article_col]}}

body = {"id":nid(),"t":"Root","version":11,
    "styles":[{"prop":"pageWidth","value":"720px"},{"prop":"backgroundColor","value":WHITE}],
    "p":{"children":[support_bar, logo_bar, header_site_bar, article, footer]}}

# ---------------- sanity check ----------------
def _scan(nd, path="root"):
    bad=[]
    if isinstance(nd, dict):
        if "t" in nd and "id" not in nd: bad.append(path+" missing id")
        for k, v in nd.items():
            if v is None: bad.append(path+"."+k+" None")
            bad += _scan(v, path+"."+str(k))
    elif isinstance(nd, list):
        for i, x in enumerate(nd): bad += _scan(x, path+f"[{i}]")
    return bad
iss = _scan(body)
print("sanity issues:", len(iss)); [print("  !", x) for x in iss[:10]]

CUSTOM_HTML = {"header": PERF, "footer": PERF_FOOTER}
OG = json.load(open("pagescore/.cache/og_img_map.json"))  # QA: purpose-cut 1200x630 share images
SEO = {
    "title": "Don't Buy A Smart Ring Until You've Read This",
    "description": "Before you spend £349 on a smart ring, there's a number the box won't tell you. Here's what 30 days wearing a ring and a £79 band actually revealed.",
    "keywords": 'smart ring, Oura Ring 4, should I buy a smart ring, smart ring subscription cost, HLTH Band, smart ring alternative, health tracker without subscription',
    "social_image_uid": OG["oura-v2"]["src_uid"],
}

# QA: settings.seo emits og:* only, so X/Twitter had no card on any of the eleven pages.
# Append explicit twitter:* tags to the header custom_html, from the same SEO values.
def _esc(v): return v.replace("&","&amp;").replace('"',"&quot;").replace("<","&lt;").replace(">","&gt;")
CUSTOM_HTML = {"header": PERF + (
    '<meta name="twitter:card" content="summary_large_image">\n'
    '<meta name="twitter:title" content="%s">\n'
    '<meta name="twitter:description" content="%s">\n'
    '<meta name="twitter:image" content="%s">\n'
    ) % (_esc(SEO["title"]), _esc(SEO["description"]), OG["oura-v2"]["src"]),
    "footer": PERF_FOOTER}

# ---------------- write: update the EXISTING V2 step body only ----------------
# STEP is hardcoded to the known V2 step id -- never looked up by slug (the slug was
# renamed live to oura-vs-hlth-band-v2-r1 to bust a storefront cache, so matching by
# the original slug would miss it and wrongly createStep a duplicate).
# Fetches the step's OWN current slug/title/visual/settings and the funnel's OWN
# current starting_step_id/published state and resends them byte-for-byte unchanged
# -- this call only ever changes `body`. The `steps` array below references ONLY
# this one step id; V1 (step_ez7sidd3Dknpc-Z-4vhg0, live-edited in another session)
# is never included in the payload.
STEP = "step_1G8JSgYhh7AMR0LJgl5tV"
# NOTE (font-swap change): slug-bumping was only ever needed to bust the storefront
# cache for BODY/copy edits. rename_v2_slug.py already reset the live slug to the
# clean "oura-vs-hlth-band-v2" (no suffix). This is a header/footer custom_html +
# font-family-order change only -- per references/performance.md ("Keep the
# URL/slug stable once shared with teammates -- these fixes never require a slug
# change") and the storefront-cache note (production URL updates fast on a session
# write), we redeploy the SAME live slug instead of bumping it again.
NEXT_SLUG_SUFFIX = ""  # intentionally not bumped for this change -- see note above

cur = sgql('''query($q: String!){ funnels(first:1, query:$q){ edges { node {
    starting_step_id published
    steps { id uid slug title type settings visual { x y } } } } } }''',
    {"q": f"id:{FUNNEL}"})["funnels"]["edges"][0]["node"]
v2 = next(s for s in cur["steps"] if s["id"] == STEP)
print("current V2 step:", v2["slug"], v2["title"])
print("current funnel starting_step_id:", cur["starting_step_id"], "published:", cur["published"])

new_slug = v2["slug"] + NEXT_SLUG_SUFFIX
# FIXED (font-swap change): this used to resend v2["settings"] (the OLD live
# settings) unchanged, silently discarding the freshly-built CUSTOM_HTML -- a
# pre-existing bug from when this script only ever touched `body`. Merge
# CUSTOM_HTML into the fetched settings (preserving any other keys, e.g. `seo`)
# instead of overwriting settings wholesale or leaving it stale.
new_settings = dict(v2["settings"])
new_settings["custom_html"] = CUSTOM_HTML
new_settings["seo"] = SEO
r2 = sgql('''mutation($id: ID!, $node: InputFunnel!){ updateFunnel(id:$id,node:$node){ id starting_step_id published steps { uid slug title } } }''',
    {"id": FUNNEL, "node": {"starting_step_id": cur["starting_step_id"], "published": cur["published"],
        "steps": [{"id": v2["id"], "slug": new_slug, "title": v2["title"], "type": v2["type"],
            "settings": new_settings, "visual": v2["visual"], "body": body}]}})
print("WROTE", json.dumps(r2["updateFunnel"], indent=2))
print("new live URL slug:", new_slug)
print("article blocks:", len(kids))
