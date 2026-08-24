#!/usr/bin/env python3
""""Screenless Trackers Are Quietly Beating Smart Rings At Their Own Game" --
a brand-new, INDEPENDENT article_page step ("V2" of the smart-ring-era
advertorial) added to the live funnel fun_hLmlmrbjeoGf3UZZvBEHY ("TUB - All
smart ring - Meta"), alongside the existing oura-vs-hlth-band-final14 /
-v2-r23 / -v3 / top-5-fitness-trackers-ranked-2026 /
smart-ring-era-already-over steps. Source: Figma file "HLTH", section
"Smart Ring VS Screenless tracker V2" (75:4280) -> desktop frame 75:4281
("Smart Ring Era V2 * TechUnboxed * 1440") + mobile frame 75:4810 ("...*
390"), both read in full via saved figwright get_node dumps and walked
node-by-node in Python (see figma-inspect.md).

RELATIONSHIP TO V1 (build_smart_ring_era.py, node 72:3133/72:3662) -- measured,
not assumed: V2 is visually/structurally the SAME page as V1 (same section
order: hero/H1/byline -> battery chart -> "Why Smart Rings Struggle" ->
lifestyle photo -> "Why Screenless Trackers Are Booming" -> checklist -> Big
Box HLTH card -> app screenshot -> cost table -> video placeholder -> trust
strip/reviews -> rank card w/ 2 accordions -> FAQ -> endmatter/footer), same
measured colors/paddings/radii/fonts throughout (DARK/BODY/BORDER/CARD_BORDER/
PINK/PROS_BG/RED/X_RED/HEADER_BG etc. all identical -- reused verbatim, not
re-measured from scratch since the two frames share one design system). This
file reuses V1's helper functions and style constants directly per the task
brief ("reuse/adapt its helper functions directly -- don't reinvent").

REAL, MEASURED TEXT DIFFERENCES from V1 (everything else below this list is
BYTE-IDENTICAL copy to V1 -- confirmed by a full text-node dump diff of both
Figma frames, not assumed just because the structure matches):
1. Breadcrumb final crumb (node 75:4300): "Screenless Trackers On The Rise"
   (V1: "Smart Ring or Screenless Tracker?").
2. H1 (75:4302): "Screenless Trackers Are Quietly Beating Smart Rings At
   Their Own Game" (V1: "Is The Smart Ring Era Already Over?").
3. Standfirst (75:4303): "No display, no subscription, a fraction of the
   price, and they're winning over ring owners in growing numbers. We
   looked at why the newer category is pulling ahead." (V1 had different
   standfirst copy).
4. Hookline 1 (75:4326): "There's a shift happening on people's wrists and
   fingers this year, and most of it is happening quietly." (V1: "Look
   around any office or gym this year and you'll spot them.").
5. Intro body: V1 ran FOUR paragraphs after the hookline. V2's Figma frame
   only contains TWO (75:4327 "rings taught the market" / 75:4328 "watched
   up close") before H2 "Why Smart Rings Struggle" -- a genuine paragraph-
   count reduction, confirmed by reading the full node dump (no 3rd/4th
   paragraph node exists in this frame), reproduced as measured rather than
   padding it back out to four.
   Everything from "Why Smart Rings Struggle" onward -- the battery chart
   labels/values, all "A ring's battery..." paragraphs, "Why Screenless
   Trackers Are Booming" copy, the 5-item checklist, the Big Box (head,
   "what it does differently" para, trust-strip copy, PROS/CONS list,
   closing para), "It tracks everything Oura does" para, the cost table
   (same £349/£399/£79/£5.99 figures), "Is It Accurate?" para + video
   placeholder, "What Do Other People Say?" para, all 6 review cards
   verbatim, the rank card (badge/name/rating/accordions/price), all 5 FAQ
   Q&As verbatim, Sources, Disclaimer, About the Author, and the footer
   legal block (medical disclaimer / advertorial disclosure / copyright) --
   are ALL byte-identical to V1. Tag row is also unchanged ("Industry
   Guide" red + "Trending" yellow, same as V1's own measured tags).

MOBILE (75:4810, diffed section-by-section against 75:4281 the same way
figma-inspect.md's method requires): the V2 mobile frame follows the EXACT
SAME responsive pattern already verified for V1's mobile frame (72:3662) --
same page gutter (20px), same battery-chart mobile reflow (18px uniform card
padding, row->column stack, 170px/134px and 196px/108px track/value splits on
the two rows -- measured to the same pixel as V1), same Big Box mobile
shrink (#1 13->12, name 22->19, rating circle 60->52 with "4.5" 18->17 and
"TRUSTPILOT" 7->4.86, body paragraphs 18->15), same Big Box media dual-DOM
swap (desktop wide photo + dark overlay pill up top vs mobile rounded-square
photo + light-gray bar on the bottom edge with SHORTENED copy "30-night
trial* / Free returns / Up to 30-day battery" -- confirmed present verbatim
in V2's mobile text dump too), same cost-table mobile cell sizing (8/6/8/6
padding, 9.5px header / 11px cell text), same Trustpilot screenshot mobile
crop (123px height, 20px horizontal inset), same video placeholder mobile
height (197px), same rank-card mobile stack with the "See reviews on
Trustpilot ->" link present. No NEW dual-DOM/reorder/drop was found beyond
what V1 already required -- V2 mobile is a straight re-application of V1's
verified responsive recipe, confirmed node-by-node rather than assumed.

IMAGES -- verified by comparing Figma image-fill HASHES (mcp__figwright__
save_image_fills), not visual similarity, per the task brief:
- lifestyle, hlth_product ("SHOOT: add bicep strap + charger" shot),
  hlth_product_media (Big Box trust-strip photo), app_screen, trustpilot_shot,
  hlth_product_rank (rank-card thumb), avatar_byline and avatar_author: V2's
  Figma fill hash is BYTE-IDENTICAL to V1's corresponding node (e.g. lifestyle
  7016b8788d40fba615d9629623ce09943db5db96 on both 72:3219 and 75:4366;
  hlth_product 03a554002c163d5ad3f568b40a2fce211342730e on both 72:3236 and
  75:4383; hlth_product_media 4107f162950a5b82c68510363e3057191391ce8e on
  both 72:3254 and 75:4401; rank thumb e463bb4c81f78c3f386eb236e11017f877c4b526
  on both 72:3560 and 75:4708; both avatars a64c59c4004d8b4a9ca13d761520a75c9
  d1ebe4f on 72:3649/75:4797 and (byline) 75:4314). All of these are reused
  by id from sre_img_map.json -- zero re-uploads for these seven assets.
- hero: V2's fill hash (1c571feda...) differs from V1's (13e2de248...), but a
  pixel diff of the two exported originals (both 4096x2286) shows max channel
  delta 7/255 and mean delta 0.44 -- i.e. the SAME source photo, re-imported/
  re-encoded into this Figma frame with a new internal hash rather than a
  genuinely different photo. Reused from V1's hosted asset rather than
  uploading a visually-indistinguishable duplicate; flagged as a judgment
  call rather than silently treated as "identical" or silently re-uploaded.
- logo: V2 draws the header wordmark as raw VECTOR paths (an inline SVG),
  not a raster image fill like V1 -- same TechUnboxed brand mark, no new
  asset to export. Reuses V1's hosted raster logo image (this exact call was
  already made and recorded in sre_img_map.json's "logo" entry before this
  script was written).
Net result: NO new images were exported or uploaded for V2 -- every asset
comes from pagescore/.cache/sre_img_map.json (V1's map), reused as-is.

Typography / SSR gotchas: identical to v1/v2/v3/rc/sre. Serif copy =
"Georgia, Gelasio, serif" (unquoted); UI chrome = "Inter, InterFallback,
sans-serif" (unquoted). No `overflow`, `boxShadow` (native prop),
`maxWidth:"none"`, or `alignItems:"baseline"` anywhere in the native LF
"styles" schema (503s the LF SSR renderer) -- shadows/gradients/overlays are
always faked via inline-HTML CSS on HtmlElement nodes instead.

This file both ASSEMBLES the body and WRITES it: creates a brand-new,
detached step via createStep, then attaches ONLY that new step into the
funnel via updateFunnel (never touching starting_step_id, never resending the
5 existing sibling steps -- per block-schema.md, updateFunnel.steps only
updates steps whose id is included, so omitting the existing ones leaves
them untouched). Safe to re-run: if the slug already exists (e.g. a rebuild
after a fix), it redeploys that step's body in place instead of creating a
duplicate.
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
STEP_SLUG = "smart-ring-era-v2"
VISUAL = {"x": 1750, "y": 90}
IMG = json.load(open("pagescore/.cache/sre_img_map.json"))  # reused verbatim from V1 -- see docstring

PDP = "https://hlthtrack.co.uk/products/wearable-hlth-band"
TP  = "https://www.trustpilot.com/review/hlthtrack.com"

# ---- fonts ----
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
#      recipe, identical to v1/v2/v3/rc/sre / references/performance.md) ----
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

# ---- colors (measured from node 75:4281 -- identical to V1's node 72:3133) ----
DARK   = {"r":22,"g":24,"b":28,"a":1}     # #16181C
BODY   = {"r":74,"g":79,"b":87,"a":1}     # #4A4F57
MUTED  = {"r":154,"g":160,"b":168,"a":1}  # #9AA0A8
BORDER = {"r":228,"g":230,"b":226,"a":1}  # #E4E6E2 (general dividers/tables/review cards)
CARD_BORDER = {"r":230,"g":231,"b":234,"a":1}  # #E6E7EA (chart card + Big box only -- measured distinct)
TABLEBG= {"r":247,"g":248,"b":246,"a":1}  # #F7F8F6
PINK   = {"r":251,"g":238,"b":236,"a":1}  # #FBEEEC (cost table HLTH column)
PROS_BG= {"r":253,"g":236,"b":236,"a":1}  # #FDECEC (Big box PROS tile -- measured distinct from PINK)
RED    = {"r":230,"g":57,"b":70,"a":1}    # #E63946
X_RED  = {"r":209,"g":60,"b":60,"a":1}    # #D13C3C (CONS "x" glyph -- measured distinct from RED)
BLUE   = {"r":26,"g":95,"b":208,"a":1}    # #1A5FD0
YELLOW_TAG = {"r":228,"g":236,"b":74,"a":1} # #E4EC4A
WHITE  = {"r":255,"g":255,"b":255,"a":1}
GOLD   = {"r":245,"g":179,"b":1,"a":1}    # #F5B301
TP_GREEN = {"r":0,"g":182,"b":122,"a":1}  # #00B67A
CHECK_GREEN = {"r":30,"g":158,"b":74,"a":1} # #1E9E4A
DASH_BORDER = {"r":185,"g":189,"b":196,"a":1} # #B9BDC4
SUPPORT_BG  = {"r":244,"g":244,"b":242,"a":1} # #F4F4F2
SUPPORT_TXT = {"r":107,"g":111,"b":118,"a":1} # #6B6F76
HEADER_BG   = {"r":40,"g":40,"b":43,"a":1}    # #28282B (same judgment call as V1 -- see V1 docstring point 15)

# ---- helpers (identical to v1/v2/v3/rc/sre -- reused directly, not reinvented) ----
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
         mw="100%", m=None, font=SERIF, ls=None, opacity=None):
    st=[{"prop":"fontFamily","value":font},{"prop":"color","value":color},
        {"prop":"fontSize","value":size},{"prop":"lineHeight","value":lh},
        {"prop":"fontWeight","value":weight},{"prop":"textAlign","value":align},
        {"prop":"maxWidth","value":mw},{"prop":"width","value":"100%"}]
    if italic: st.append({"prop":"fontStyle","value":"italic"})
    if ls: st.append({"prop":"letterSpacing","value":ls})
    if opacity is not None: st.append({"prop":"opacity","value":opacity})
    _media(st, m)
    return {"t":"Text","id":nid(),"p":{"content":content},"styles":st}

def inline_text(*a, **kw):
    node = text(*a, **kw)
    node["styles"].append({"prop":"width","value":"auto"})
    return node

def container(children, styles):
    return {"t":"Container","id":nid(),"styles":styles,"p":{"children":children}}

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

def sp(px, mh=None):
    st = [{"prop":"width","value":"100%"},{"prop":"height","value":"%dpx"%px},
        {"prop":"lfDisplay","value":"block"}]
    if mh is not None:
        st.append({"prop":"height","value":"%dpx"%mh,"media":767})
    return container([], st)

def sp_mobile_only(px):
    # A spacer that renders ONLY at 767 (hidden entirely on desktop) -- for a
    # gap that accompanies mobile-only content with no desktop counterpart at
    # all (see the early rank-card duplicate below), where a normal sp() would
    # leave a spurious extra gap on desktop.
    return container([], [{"prop":"width","value":"100%"},
        {"prop":"lfDisplay","value":"none"},
        {"prop":"lfDisplay","value":"block","media":767},
        {"prop":"height","value":"%dpx"%px,"media":767}])

_TITLE_NEEDED = {"hero", "logo"}

# QA: LF emits an alt attribute but never populates it (the logo proves it:
# title="logo", alt=""). Confirmed live that the Image block honours p["alt"].
# Decorative images keep alt="" so screen readers skip them.
ALT = {
    "logo": "",
    "avatar_byline": "", "avatar_author": "",
    "hero": "A man wearing a smart ring on one hand and the HLTH Band on the other wrist",
    "lifestyle": "Hands typing at a laptop while wearing the HLTH Band",
    "hlth_product": "The HLTH Band beside its retail box",
    "hlth_product_media": "The HLTH Band shown against a plain background",
    "hlth_product_media_bigbox": "The HLTH Band retail box",
    "hlth_product_media_closeup": "Close-up of the HLTH Band's sensor underside",
    "hlth_bigbox_lifestyle": "Checking the HLTH app on a phone while wearing the band",
    "hlth_product_rank": "The HLTH Band photographed against a black background",
    "app_screen": "The HLTH app home screen showing the day's health metrics",
    "trustpilot_shot": "Screenshot of the HLTH Band's Trustpilot review page",
}

def img_block(key, height=None, radius="10px", full=True, fit="cover", mh=None, border=False, alt=None):
    m=IMG[key]
    st=[{"prop":"maxWidth","value":"100%"},{"prop":"borderRadius","value":radius},
        {"prop":"objectFit","value":fit},{"prop":"lfDisplay","value":"block"}]
    if full: st.append({"prop":"width","value":"100%"})
    if height: st.append({"prop":"height","value":height})
    if mh: st.append({"prop":"height","value":mh,"media":767})
    if border:
        st.append({"prop":"borderStyle","value":"solid"})
        st.append({"prop":"borderColor","value":BORDER})
        st.append({"prop":"borderWidth","value":"1px"})
    p = {"src_id":m["src_id"],"src_uid":m["src_uid"],"src":m["src"]}
    if key in _TITLE_NEEDED: p["title"] = key
    p["alt"] = ALT.get(key, "") if alt is None else alt
    return {"t":"Image","id":nid(),"p":p,"styles":st}

def logo_img(w="166px", h="42px"):
    m=IMG["logo"]
    return {"t":"Image","id":nid(),"p":{"title":"logo","src":m["src"]},
        "styles":[{"prop":"width","value":w},{"prop":"height","value":h},{"prop":"maxWidth","value":"100%"},
                  {"prop":"objectFit","value":"contain"},{"prop":"lfDisplay","value":"block"}]}

def button(label, href=PDP, bg=RED, fg=WHITE, full=False, size="15px", weight="700", radius="10px", ls="0.3px",
           pad=None):
    lab_st=[{"prop":"fontFamily","value":SANS},{"prop":"color","value":fg},
            {"prop":"fontSize","value":size},{"prop":"fontWeight","value":weight},
            {"prop":"lineHeight","value":"20px"},{"prop":"textAlign","value":"center"},
            {"prop":"whiteSpace","value":"nowrap"},{"prop":"maxWidth","value":"100%"}]
    if ls: lab_st.append({"prop":"letterSpacing","value":ls})
    lab={"t":"Text","id":nid(),"p":{"content":label},"styles":lab_st}
    lw=container([lab],[{"prop":"lfDisplay","value":"flex"},{"prop":"alignItems","value":"center"},
        {"prop":"justifyContent","value":"center"},{"prop":"maxWidth","value":"100%"}])
    pad = pad or {"top":"13px","bottom":"13px","left":"10px","right":"10px"}
    st=[{"prop":"backgroundColor","value":bg},{"prop":"borderRadius","value":radius},
        {"prop":"padding","value":pad},
        {"prop":"lfDisplay","value":"flex"},{"prop":"alignItems","value":"center"},
        {"prop":"justifyContent","value":"center"}]
    if full: st.append({"prop":"width","value":"100%"})
    return {"t":"BlockLink","id":nid(),"p":{"destination":{"type":"static","value":href},
        "target":"_blank","widthOption":"auto","children":[lw]},"styles":st}

STAR = "★"
def tp_stars(rating, color, box=19):
    fs = round(box*0.63)
    radius = round(box*0.125, 3)
    gap = box*3.1667/19
    half=round(rating*2)/2; full=int(half); hh=(half-full)==0.5
    out='<span style="display:inline-flex;gap:%.4fpx;vertical-align:middle">' % gap
    tpl=('<span style="display:inline-flex;align-items:center;justify-content:center;width:%dpx;height:%dpx;'
         'border-radius:%.3fpx;color:#fff;font-size:%dpx;background:%s">' + STAR + '</span>')
    for i in range(5):
        if i<full: bg=color
        elif i==full and hh: bg="linear-gradient(90deg,%s 50%%,#dcdce6 50%%)"%color
        else: bg="#dcdce6"
        out+=tpl%(box,box,radius,fs,bg)
    return out+'</span>'

def ext_link_icon(size=13, color="#4A4F57", stroke_w=1.2):
    return ('<svg width="%d" height="%d" viewBox="0 0 13 13" fill="none" stroke="%s" '
        'stroke-width="%s" stroke-linecap="round" stroke-linejoin="round" '
        'style="display:inline-block;vertical-align:middle;flex-shrink:0">'
        '<path d="M11.375 7.313v3.25a1.625 1.625 0 0 1-1.625 1.625H2.438a1.625 1.625 0 0 1-1.625-1.625V3.25a1.625 1.625 0 0 1 1.625-1.625h3.25"/>'
        '<polyline points="8.125 1.625 11.375 1.625 11.375 4.875"/>'
        '<line x1="5.417" y1="7.583" x2="11.375" y2="1.625"/></svg>') % (size, size, color, stroke_w)

def caption(t="(Image credit: Marcus Pendleton / TechUnboxed)"):
    return text(t, size="13px", lh="18px", color=BODY, italic=True, font=SERIF)

def para(t, color=DARK, m=None): return text(t, size="18px", lh="30px", color=color, font=SERIF, m=m)

def figure(image_node, cap_text=None, gap="8px"):
    image_nodes = image_node if isinstance(image_node, list) else [image_node]
    kids_ = list(image_nodes) + [caption(cap_text) if cap_text else caption()]
    return [col(kids_, gap=gap)]

def h2(content):
    # Every h2() call site (except "Is It Accurate?" and "What Do Other People
    # Say?", which measure NO spacer before their next paragraph -- see
    # docstring) inserts an explicit sp(28) before it, matching v1/v3/rc's
    # convention of reproducing the Figma H2's own paddingTop as a spacer
    # rather than a margin (so it doesn't double-count against the article
    # column's own 16px flex gap).
    return title(content, "28px", "35px", weight="700", color=DARK, ls="-0.28px", font=SERIF,
                 m={"fontSize":"22px","lineHeight":"27.5px","letterSpacing":"-0.22px"})

# ============================== HEADER (site chrome, reused verbatim) ======
support_bar = {"t":"Section","id":nid(),
    "styles":[{"prop":"backgroundColor","value":SUPPORT_BG},
              {"prop":"borderStyle","value":"solid"},{"prop":"borderColor","value":BORDER},
              {"prop":"borderWidth","value":"1px 0px 1px 0px"},
              {"prop":"padding","value":{"top":"9px","bottom":"9px","left":"12px","right":"12px"}}],
    "p":{"layout":"","dividerPosition":["top"],"horizontalFlip":False,
         "embedded_video":{"src":"","video_size":"stretch","video_position":"center"},
         "children":[text("This site is reader-supported; links may earn us commissions.",
             size="13px", lh="18px", color=SUPPORT_TXT, align="center", font=SANS)]}}

logo_bar = {"t":"Section","id":nid(),
    "styles":[{"prop":"backgroundColor","value":HEADER_BG},
              {"prop":"padding","value":{"top":"14px","bottom":"14px","left":"28px","right":"28px"}}],
    "p":{"layout":"","dividerPosition":["top"],"horizontalFlip":False,
         "embedded_video":{"src":"","video_size":"stretch","video_position":"center"},
         "children":[container([logo_img()],[{"prop":"lfDisplay","value":"flex"},
             {"prop":"justifyContent","value":"center"},{"prop":"width","value":"100%"}])]}}

# Measured (node 75:4300): "Home > Wearables > Screenless Trackers On The Rise"
# -- V2's own breadcrumb copy, genuinely different from V1's final crumb.
BREADCRUMB_SRE_V2 = ('<span style="color:#16181C">Home</span> <span style="color:#B9BDC4">&gt;</span> '
    '<span style="color:#16181C">Wearables</span> <span style="color:#B9BDC4">&gt;</span> '
    '<span style="color:#E63946;font-weight:600">Screenless Trackers On The Rise</span>')

header_site_bar = {"t":"Section","id":nid(),
    "styles":[{"prop":"borderStyle","value":"solid"},{"prop":"borderColor","value":BORDER},
              {"prop":"borderWidth","value":"0px 0px 1px 0px"},
              {"prop":"padding","value":{"top":"14px","bottom":"14px"}},
              # Mobile fix: node 78:558 (Header · site) has paddingLeft/Right:20
              # on the mobile frame -- the "boxed" layout collapses to 0 side
              # padding at full-bleed mobile width, so the breadcrumb touched
              # the screen edges without this override.
              {"prop":"padding","value":{"left":"20px","right":"20px"},"media":767}],
    "p":{"layout":"boxed","dividerPosition":["top"],"horizontalFlip":False,
         "embedded_video":{"src":"","video_size":"stretch","video_position":"center"},
         "children":[text(BREADCRUMB_SRE_V2, size="13px", lh="18px", font=SANS)]}}

# ============================== ARTICLE HEAD ================================
kids=[]
kids.append(title("Screenless Trackers Are Quietly Beating Smart Rings At Their Own Game",
    "40px","46px", weight="700", ls="-0.4px", font=SERIF, level="1",
    m={"fontSize":"28px","lineHeight":"32px","letterSpacing":"-0.28px"}))
kids.append(text("No display, no subscription, a fraction of the price, and they're winning over ring owners "
    "in growing numbers. We looked at why the newer category is pulling ahead.",
    size="20px", lh="30px", color=BODY, font=SERIF))

# tag row (measured identical to V1: "Industry Guide" red + "Trending" yellow)
tag_industry = container([text("Industry Guide", size="15px", lh="15px", color=WHITE, weight="700", font=SANS)],
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
kids.append(rowf([tag_industry, tag_trending], gap="10px", align="center", justify="flex-start",
    styles=[{"prop":"width","value":"fit-content"}]))
kids.append(sp(2))

# byline strip (measured identical to V1/siblings)
byline_who = col([
    text('<span style="text-decoration:underline">Marcus Pendleton</span>',
         size="15.5px", lh="20px", color=DARK, weight="800", font=SANS),
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
    container([{"t":"Image","id":nid(),"p":{"src_id":IMG["avatar_byline"]["src_id"],
        "src_uid":IMG["avatar_byline"]["src_uid"],"src":IMG["avatar_byline"]["src"]},
        "styles":[{"prop":"width","value":"52px"},{"prop":"height","value":"52px"},
                  {"prop":"borderRadius","value":"50%"},{"prop":"objectFit","value":"cover"}]}],
        [{"prop":"width","value":"52px"},{"prop":"flexShrink","value":"0"}]),
    byline_who, byline_bio], gap="16px", align="center", wrap=True,
    styles=[{"prop":"borderStyle","value":"dashed"},{"prop":"borderColor","value":DASH_BORDER},
        {"prop":"borderWidth","value":"1.5px 0px 1.5px 0px"},
        {"prop":"padding","value":{"top":"16px","bottom":"16px","left":"2px","right":"2px"}}])
kids.append(byline)
kids.append(sp(10))

# hero (same photo as V1 -- same Figma fill, re-encoded hash; see docstring)
kids.extend(figure(img_block("hero", height="403px", mh="196px", border=True), gap="8px"))
kids.append(sp(10))

# Measured (75:4326-4328): V2's intro runs a DIFFERENT hookline and only TWO
# body paragraphs (not V1's four) before "Why Smart Rings Struggle" -- a
# genuine, measured content reduction, not a guess.
kids.append(title("There's a shift happening on people's wrists and fingers this year, and most of it is "
    "happening quietly.", "18px","30px", weight="700", font=SERIF))
kids.append(para("Smart rings spent the last few years teaching the market something new: health tracking "
    "works better with no screen, no pings, nothing buzzing through dinner. Millions of people bought in. But "
    "increasingly, the device doing that job isn't a ring. It's a new wave of screenless wrist trackers, built "
    "on the exact idea rings made popular, at a fraction of the price."))
kids.append(para("I wear a ring every day, and I've watched this shift up close. So we spent a month testing "
    "where the newer category actually pulls ahead, and where the rings still win outright."))
kids.append(sp(28))

# ============================== WHY SMART RINGS STRUGGLE ====================
# Byte-identical to V1 from here through the FAQ/endmatter/footer -- see docstring.
kids.append(h2("Why Smart Rings Struggle"))
kids.append(sp(10))

BAR_TRACK_BG = {"r":241,"g":241,"b":243,"a":1}  # #F1F1F3

def battery_row(label, sub, value, value_sub, pct, grad_from, grad_to):
    # Measured (75:4332-4355, matches V1's 72:3185-3206 exactly): fixed 186px
    # label column, fixed 300px-wide track (NOT stretched to fill the row --
    # both rows share the same 300px track), gradient fill inside, 16px gaps.
    # Gradient authored as inline-HTML CSS (HtmlElement), same trick as
    # v3's video-placeholder gradient and tp_stars()'s half-star fill --
    # never touches the native LF "styles" boxShadow/overflow props.
    # Mobile (75:4864-4887, dedicated mobile frame): confirmed pixel-for-pixel
    # match to V1's mobile chart -- row stacks to a column (gap 16->8), the
    # label (15/12.5px) and value (18/12px) text shrink to 13/10.5px and
    # 16/10px, and the track itself is NOT a fixed 300px on mobile: row 1
    # measures a 170px track beside a 134px value col, row 2 measures 196px
    # beside 108px -- identical to V1's measured values. Reproduced with
    # flex:1 on the track rather than a second hardcoded mobile pixel width.
    label_col = col([
        text(label, size="15px", lh="20px", color=DARK, weight="700", font=SANS,
             m={"fontSize":"13px","lineHeight":"18px"}),
        text(sub, size="12.5px", lh="17px", color="#6A6E75", font=SANS,
             m={"fontSize":"10.5px","lineHeight":"15px"}),
    ], gap="2px", styles=[{"prop":"width","value":"186px"},{"prop":"flexShrink","value":"0"},
        {"prop":"width","value":"100%","media":767}])
    fill_w = round(300 * pct / 100)
    track = {"t":"HtmlElement","id":nid(),"p":{"content":(
        '<div style="width:300px;max-width:100%%;height:22px;border-radius:999px;background:#F1F1F3;box-sizing:border-box">'
        '<div style="width:%dpx;max-width:100%%;height:22px;border-radius:999px;'
        'background:linear-gradient(90deg,%s,%s)"></div></div>'
    ) % (fill_w, grad_from, grad_to)}, "styles":[{"prop":"width","value":"300px"},{"prop":"maxWidth","value":"100%"},
        {"prop":"width","value":"auto","media":767},{"prop":"flex","value":"1","media":767},
        {"prop":"minWidth","value":"0","media":767}]}
    value_col = rowf([
        inline_text(value, size="18px", lh="22px", color=DARK, weight="800", font=SANS,
                    m={"fontSize":"16px","lineHeight":"20px"}),
        inline_text(value_sub, size="12px", lh="16px", color="#6A6E75", font=SANS,
                    m={"fontSize":"10px","lineHeight":"14px"}),
    ], gap="6px", align="center",
       styles=[{"prop":"width","value":"fit-content"},{"prop":"flexShrink","value":"0"}])
    bar_line = rowf([track, value_col], gap="16px", align="center",
        styles=[{"prop":"flex","value":"1"},{"prop":"minWidth","value":"0"},
                {"prop":"gap","value":"10px","media":767}])
    return rowf([label_col, bar_line], gap="16px", align="center",
        styles=[{"prop":"flexDirection","value":"column","media":767},
                {"prop":"alignItems","value":"flex-start","media":767},
                {"prop":"gap","value":"8px","media":767}])

battery_chart = col([
    battery_row("HLTH Band", "≈10× larger cell · one charge a month", "~30 days", "per charge",
                100, "#E63946", "#C02C38"),
    sp(22, mh=18),
    battery_row("Smart ring (latest)", "10.5 mAh cell · charged twice a week", "5–8 days", "rated",
                22, "#C3C7CD", "#A8ADB5"),
], gap="0px", styles=[{"prop":"width","value":"100%"},{"prop":"backgroundColor","value":WHITE},
    {"prop":"borderRadius","value":"20px"},{"prop":"borderStyle","value":"solid"},
    {"prop":"borderColor","value":CARD_BORDER},{"prop":"borderWidth","value":"1px"},
    {"prop":"padding","value":{"top":"28px","bottom":"28px","left":"28px","right":"28px"}},
    {"prop":"padding","value":{"top":"18px","bottom":"18px","left":"18px","right":"18px"},"media":767}])
kids.append(battery_chart)
kids.append(caption("Days per charge, and the cell size behind it. (Chart: TechUnboxed)"))
kids.append(sp(10))

kids.append(title("A ring's battery is too small to support real 24/7 readings.",
    "18px","30px", weight="700", font=SERIF))
kids.append(para('Inside the latest £399 ring sits a 10.5 mAh battery, smaller than a hearing aid’s. Too small '
    'to measure you all day, so the ring rations. Oura’s own support pages admit it: daytime heart rate is '
    '"only taken under optimal conditions" to "preserve battery," with pauses "up to 30 minutes."'))
kids.append(para("Rationed readings. Gaps during activity. A battery that can't be replaced when it fades. "
    "Your health data ends up full of holes, and health tracking only works as an unbroken line."))
kids.append(para("The small battery creates a second, more human problem. Charging twice a week, on no fixed "
    "rhythm, means people forget. Every ring owner knows the moment: it's Thursday, and the ring's been dead "
    "since Tuesday. You've been wearing jewellery."))
kids.append(para("Still, give the rings their due. They proved millions of people want their health tracked "
    "quietly, no screen. Which is exactly why manufacturers are now building the next step: screenless "
    "trackers, without the battery problem."))
kids.append(sp(28))

# ============================== WHY SCREENLESS TRACKERS ARE BOOMING =========
kids.append(h2("Why Screenless Trackers Are Booming Right Now"))
kids.append(sp(10))
kids.extend(figure(img_block("lifestyle", height="430px", mh="209px", border=True), gap="8px"))
kids.append(sp(10))
kids.append(para("The industry noticed. Over the past two years, the biggest names in wearables have raced to "
    "launch screen-free bands: trackers with no display at all, built on a simple insight. The screen was "
    "never the health part. The screen is what forces daily charging, and daily charging is what puts holes in "
    "your data."))
kids.append(para("Kill the screen and the equation flips. A wrist band fits a battery many times larger than "
    "any ring can hold, so it can afford to measure continuously and still run for weeks. Your phone becomes "
    "the display. The band just collects, all day, all night, through workouts and showers and everything "
    "between. That's why the screenless wrist tracker, the least flashy gadget in health tech, is quietly "
    "becoming its fastest-growing category."))
kids.append(sp(28))

# ============================== WHAT TO LOOK FOR =============================
kids.append(h2("What To Look For When Buying A Screenless Tracker"))
kids.append(para("Five things separate a tracker that changes your habits from one that ends up in a drawer:"))
kids.append(text('<b>Reading frequency.</b> Ask how often the device actually measures you, not what sensors '
    'it has. A sensor that reads every five minutes builds a trend. One that reads "when conditions allow" '
    'builds a scatter plot.', size="18px", lh="30px", font=SERIF))
kids.append(text("<b>Battery measured in weeks, not days.</b> Every charge is a gap in your data. Fewer "
    "charges, fewer gaps, and a tracker that's always on your body.", size="18px", lh="30px", font=SERIF))
kids.append(text("<b>What it tracks beyond steps.</b> Heart rate and sleep are table stakes. HRV, blood oxygen "
    "and blood pressure trends are where a tracker starts telling you something your mirror can't.",
    size="18px", lh="30px", font=SERIF))
kids.append(text("<b>The real price.</b> Not the sticker, the three-year total. A mandatory membership can "
    "double or triple what you actually pay.", size="18px", lh="30px", font=SERIF))
kids.append(text("<b>It works with your phone. Any phone.</b> Some devices lock you to one ecosystem. Your "
    "health data should survive your next phone upgrade.", size="18px", lh="30px", font=SERIF))
kids.append(sp(28))

# ============================== OUR FAVOURITE SCREENLESS TRACKER ============
kids.append(h2("Our Favourite Screenless Tracker: The HLTH Band"))
kids.append(sp(10))
kids.extend(figure(img_block("hlth_product", height="430px", mh="209px", border=True), gap="8px"))
kids.append(sp(10))
kids.append(text('We\'ve tested the new wave of screenless trackers as they\'ve launched, and one keeps '
    'winning our comparisons: the £79 <a href="%s" target="_blank" '
    'style="color:#1A5FD0;text-decoration:underline">HLTH Band</a>. '
    "It's the device that takes every principle above and executes it without the price tag. A wrist-mounted "
    "multi-wavelength PPG sensor, a battery rated for about a month, readings every five minutes around the "
    "clock, and not a single feature behind a subscription." % PDP, size="18px", lh="30px", font=SERIF))
_EARLY_RANK_CARD_MARKER = len(kids)  # see insertion right after rank_card_mobile() is defined below
kids.append(sp(8))

# ---- Big Box: HLTH Band introduced (node 75:4388, matches V1's 72:3241) ----
def rating_badge():
    return container([
        text("4.6", size="18px", lh="22px", color=WHITE, weight="800", align="center", font=SANS,
             m={"fontSize":"17px","lineHeight":"21px"}),
        text("TRUSTPILOT", size="7px", lh="10px", color=WHITE, weight="700", align="center", font=SANS, ls="0.3px",
             m={"fontSize":"4.86px","lineHeight":"8px"}),
    ], [{"prop":"width","value":"60px"},{"prop":"height","value":"60px"},{"prop":"flexShrink","value":"0"},
        {"prop":"width","value":"52px","media":767},{"prop":"height","value":"52px","media":767},
        {"prop":"backgroundColor","value":RED},{"prop":"borderRadius","value":"999px"},
        {"prop":"lfDisplay","value":"flex"},{"prop":"flexDirection","value":"column"},
        {"prop":"alignItems","value":"center"},{"prop":"justifyContent","value":"center"}])

bigbox_head = rowf([
    inline_text("#1", size="13px", lh="18px", color=RED, weight="800", font=SANS,
                m={"fontSize":"12px","lineHeight":"17px"}),
    col([
        text("HLTH Band 1.0", size="22px", lh="28px", color=DARK, weight="700", font=SANS,
             m={"fontSize":"19px","lineHeight":"25px"}),
        text("The screenless tracker we kept wearing", size="13px", lh="19px", color="#6A6E75", font=SANS,
             m={"fontSize":"12px","lineHeight":"18px"}),
    ], gap="1px", styles=[{"prop":"flex","value":"1"},{"prop":"minWidth","value":"0"}]),
    rating_badge(),
], gap="12px", align="center")

# Media (Figma node 205:27/205:39, redesign of the old trust-strip-overlay
# card): the offer pill is gone -- it's now a single plain lifestyle photo
# (person checking the band's heart-rate reading on their phone), same
# rounded box, same caption below. Reuses the img_block() convention used
# everywhere else on this page (fixed px height per breakpoint, mobile
# height scaled by the same ~2.06 desktop/mobile ratio as hero/lifestyle/
# hlth_product above -- no separate mobile spec was given for this node).
bigbox_media = container([img_block("hlth_bigbox_lifestyle", height="420px", mh="204px", radius="12px")],
    [{"prop":"width","value":"100%"}])

def pros_cons_li(mark, mark_color, txt):
    return rowf([
        inline_text(mark, size="12px", lh="18px", color=mark_color, weight="800", font=SANS,
                    m={"fontSize":"11px","lineHeight":"17px"}),
        text(txt, size="13px", lh="19px", color=DARK, font=SANS,
             m={"fontSize":"12px","lineHeight":"18px"}),
    ], gap="8px", align="flex-start", styles=[{"prop":"padding","value":{"top":"3px","bottom":"3px"}}])

BIGBOX_PROS = ["Reads you every five minutes, around the clock", "Blood-pressure trends, no cuff",
    "Full sleep stages, plus HRV and blood oxygen", "Own it outright, no subscription",
    "30-day battery, worn 24/7"]
BIGBOX_CONS = ["Online only, not in stores", "A newer name than Apple or Oura",
    "Trends worth a conversation, not a diagnosis"]

pros_box = col([
    text("PROS", size="10px", lh="14px", color=RED, weight="800", font=SANS, ls="0.7px",
         m={"fontSize":"9px","lineHeight":"13px"}),
    sp(8),
    col([pros_cons_li("&#10003;", CHECK_GREEN, p) for p in BIGBOX_PROS], gap="0px"),
], gap="0px", styles=[{"prop":"flex","value":"1"},{"prop":"backgroundColor","value":PROS_BG},
    {"prop":"borderRadius","value":"12px"},{"prop":"padding","value":{"top":"16px","bottom":"16px","left":"16px","right":"16px"}}])
cons_box = col([
    text("CONS", size="10px", lh="14px", color="#6A6E75", weight="800", font=SANS, ls="0.7px",
         m={"fontSize":"9px","lineHeight":"13px"}),
    sp(8),
    col([pros_cons_li("&#10007;", X_RED, c) for c in BIGBOX_CONS], gap="0px"),
], gap="0px", styles=[{"prop":"flex","value":"1"},{"prop":"backgroundColor","value":TABLEBG},
    {"prop":"borderRadius","value":"12px"},{"prop":"padding","value":{"top":"16px","bottom":"16px","left":"16px","right":"16px"}}])

big_box = col([
    bigbox_head, sp(16),
    text('So what is the HLTH Band doing differently? It reads you every five minutes, day and night, rather '
        'than when conditions allow: <b>resting heart rate, HRV, blood-pressure trends and blood oxygen</b>, '
        'not as one-off numbers but as moving lines it watches week over week. When several of them drift '
        'together, the app tells you in plain English what changed.', size="18px", lh="30px", font=SERIF,
        m={"fontSize":"15px","lineHeight":"25px"}),
    sp(16), bigbox_media, sp(10),
    text("The band watches the overnight lines, then tells you in plain English what changed.",
        size="13px", lh="19px", color="#6A6E75", italic=True, font=SERIF,
        m={"fontSize":"12px","lineHeight":"18px"}),
    sp(18),
    rowf([pros_box, cons_box], gap="12px", align="stretch",
        styles=[{"prop":"flexDirection","value":"column","media":767}]),
    sp(18),
    para("It doesn't diagnose anything and it doesn't replace your GP. It helps you notice change sooner, so "
        "the conversation happens sooner.", m={"fontSize":"15px","lineHeight":"25px"}),
], gap="0px", styles=[{"prop":"width","value":"100%"},{"prop":"backgroundColor","value":WHITE},
    {"prop":"borderRadius","value":"20px"},{"prop":"borderStyle","value":"solid"},
    {"prop":"borderColor","value":CARD_BORDER},{"prop":"borderWidth","value":"1px"},
    {"prop":"padding","value":{"top":"28px","bottom":"28px","left":"28px","right":"28px"}},
    {"prop":"padding","value":{"top":"18px","bottom":"18px","left":"18px","right":"18px"},"media":767}])
kids.append(big_box)
kids.append(sp(20))
kids.append(sp(28))

# ============================== IT TRACKS EVERYTHING OURA DOES, AND MORE ====
kids.append(h2("It tracks everything Oura does, and more"))
kids.append(sp(10))
kids.extend(figure(img_block("app_screen", height="402px", mh="195px", border=True), gap="8px"))
kids.append(sp(10))
kids.append(text("Heart rate, continuously, on a full-day graph. HRV overnight, the recovery signal most "
    "trackers skip. Blood pressure trends, day and night, one of the only devices at any price to offer them "
    "without a subscription. Blood oxygen as a simple percentage. Full sleep stages, light, deep and REM, with "
    "total hours at the top. Stress. Workouts, with a bicep strap in the box for steadier readings under load. "
    "All of it lands in one clean app screen you can read in about two seconds, on iPhone or Android.",
    size="18px", lh="30px", font=SERIF))
kids.append(sp(28))

# ============================== WHAT DOES IT COST? ==========================
kids.append(h2("What Does It Cost?"))
kids.append(sp(4))

def cell(content, w, bold=False, color=DARK, bg=None, header=False, align="left"):
    st=[{"prop":"flex","value":str(w)},{"prop":"minWidth","value":"0"},
        {"prop":"padding","value":{"top":"10px","bottom":"10px","left":"12px","right":"12px"}},
        {"prop":"padding","value":{"top":"8px","bottom":"8px","left":"6px","right":"6px"},"media":767},
        {"prop":"borderStyle","value":"solid"},{"prop":"borderColor","value":BORDER},
        {"prop":"borderWidth","value":"0px 1px 1px 0px"}]
    if bg: st.append({"prop":"backgroundColor","value":bg})
    txt_size = "13.5px" if header else "15.5px"
    txt_weight = "700" if (header or bold) else "400"
    txt = text(content, size=txt_size, lh="18px" if header else "21px", color=color, weight=txt_weight,
               align=align, font=SANS, m={"fontSize":"9.5px" if header else "11px",
                                           "lineHeight":"13px" if header else "15px"})
    if header:
        txt["styles"].append({"prop":"letterSpacing","value":"0.4px"})
    return container([txt], st)

def table_row(cells):
    return rowf(cells, gap="0px", align="stretch", styles=[{"prop":"width","value":"100%"}])

cost_header = table_row([
    cell("", 170, header=True, bg=TABLEBG),
    cell("MARKET-LEADING RING", 200, header=True, bg=TABLEBG),
    cell("PREMIUM RING", 170, header=True, bg=TABLEBG),
    cell("HLTH BAND", 180, header=True, bg=TABLEBG),
])
COST_ROWS = [
    ("Upfront", "£349", "£399", "£79"),
    ("Subscription", "£5.99/mo, mandatory", "None", "None"),
    ("3-year total", "~£560", "£399", "£79"),
]
cost_rows = [cost_header]
for label, ring_a, ring_b, hlth in COST_ROWS:
    cost_rows.append(table_row([
        cell(label, 170, bold=True),
        cell(ring_a, 200),
        cell(ring_b, 170),
        cell(hlth, 180, bold=True, bg=PINK),
    ]))
kids.append(container(cost_rows, [{"prop":"width","value":"100%"},
    {"prop":"borderStyle","value":"solid"},{"prop":"borderColor","value":BORDER},
    {"prop":"borderWidth","value":"1px 0px 0px 1px"}]))
kids.append(sp(4))
kids.append(para("£79 is the launch price, down from the £158 standard price, and every feature is unlocked "
    "at purchase. Three-year ring cost shown as £349 + 36 × £5.99 ≈ £560. There’s nothing to pay after "
    "checkout, and every band carries a 30-day money-back guarantee."))
kids.append(sp(28))

# ============================== IS IT ACCURATE? =============================
kids.append(h2("Is It Accurate?"))
kids.append(para("The honest answer, the one that applies to every optical wearable: per reading, modern PPG "
    "sensors across this category are capable, and coverage is what separates devices. The band reads every "
    "five minutes, all day and all night, which is what turns readings into trends you can actually use. In "
    "our own resting comparisons, its blood pressure trends tracked within the recommended ±10 mmHg range of "
    "a medical-grade cuff, consistently, across multiple sessions. Trends for your own awareness, not medical "
    "readings. Rather than take our word for it, watch the band tested on video, worn day and night rather "
    "than filmed in a studio:"))
kids.append(sp(6))

# Bug 6 fix (v2): the click-to-play facade wasn't showing a real thumbnail.
# Replaced with a direct eager <iframe> matching the proven pattern already
# live on sibling step oura-vs-hlth-band-v3 (pagescore/build_hlth_v3.py) --
# YouTube's own player renders its native thumbnail/play button immediately,
# no JS/click step needed. Same reserved box (405px desktop / 197px @767) as
# before, so no layout shift; loading="lazy" keeps the CLS-safety pattern
# from references/performance.md.
video_placeholder_sre = {"t":"HtmlElement","id":nid(),"p":{"content":(
    '<div style="width:100%;height:100%;border-radius:12px;border:1px solid #E4E6E2;'
    'overflow:hidden;box-sizing:border-box">'
    '<iframe src="https://www.youtube.com/embed/lMZoKLSmd6M" title="HLTH Band accuracy test video" '
    'style="width:100%;height:100%;display:block;border:0" '
    'allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" '
    'allowfullscreen loading="lazy"></iframe>'
    '</div>'
)}, "styles":[{"prop":"width","value":"100%"},{"prop":"height","value":"405px"},
    {"prop":"height","value":"197px","media":767}]}
kids.append(video_placeholder_sre)
kids.append(sp(6))
kids.append(sp(28))

# ============================== WHAT DO OTHER PEOPLE SAY? ===================
kids.append(h2("What Do Other People Say?"))
kids.append(text('One of the harder places for any brand to shape its own reputation is its Trustpilot page, '
    'since Trustpilot verifies reviewers and penalises companies caught manipulating scores. The '
    '<a href="%s" target="_blank" style="color:#1A5FD0;text-decoration:underline">HLTH Band</a> holds a 4.6 '
    "rating there, and the "
    "same themes keep coming up: the battery genuinely lasts weeks, the band is light enough to forget, and "
    "there's nothing to pay after the £79. Read them unfiltered before you decide." % PDP,
    size="18px", lh="30px", font=SERIF))
kids.append(sp(10))
_tp_img = container([img_block("trustpilot_shot", height="252px", mh="123px", radius="8px", fit="contain")],
    [{"prop":"width","value":"100%"},
     {"prop":"padding","value":{"left":"20px","right":"20px"},"media":767}])
kids.extend(figure(_tp_img,
    cap_text="Screenshot from the HLTH Band's Trustpilot page (trustpilot.com/review/hlthtrack.com), "
             "captured 8 August 2026."))
kids.append(sp(10))

REVIEWS = [
    ("Matches my pricier band", "Sleep and HRV data line up with my old band that cost three times as much. "
        "Battery really does last weeks.", "Verified buyer"),
    ("No monthly fees", "Does everything the big brands do without the price tag or the monthly fees.",
        "Verified buyer"),
    ("I forget it's on", "So light I forget it's on. Finally a tracker I actually keep wearing.",
        "Verified buyer"),
    ("Really helpful team", "Had a quick question and support replied within the hour. Really helpful team.",
        "J. Porras, 5 days ago"),
    ("Everyday essential", "Monitors heart rate, sleep, stress, HRV and blood oxygen. Highly recommend.",
        "Joanna"),
    ("Arrived next day", "Ordered in the evening and it arrived the next day. Packaging was lovely too.",
        "Verified buyer"),
]
def review_card(title_, body_, footer_):
    return col([
        text(tp_stars(5.0, "#00B67A", 15), size="15px", lh="15px"), sp(3),
        text(title_, size="14.5px", lh="21px", color=DARK, weight="700", font=SANS), sp(2),
        text(body_, size="14.5px", lh="21px", color=DARK, font=SANS), sp(6),
        text(footer_, size="13px", lh="18px", color=BODY, font=SANS),
    ], gap="0px", styles=[{"prop":"flex","value":"1"},{"prop":"backgroundColor","value":WHITE},
        {"prop":"borderRadius","value":"10px"},{"prop":"borderStyle","value":"solid"},
        {"prop":"borderColor","value":BORDER},{"prop":"borderWidth","value":"1px"},
        {"prop":"padding","value":{"top":"14px","bottom":"14px","left":"16px","right":"16px"}}])
review_rows = []
for i in range(0, 6, 2):
    review_rows.append(rowf([review_card(*REVIEWS[i]), review_card(*REVIEWS[i+1])], gap="12px", align="stretch",
        styles=[{"prop":"flexDirection","value":"column","media":767}]))
kids.append(col(review_rows, gap="12px"))
kids.append(sp(4))
kids.append(text('<a href="%s" target="_blank" style="color:#1A5FD0;text-decoration:underline">Read the HLTH '
    "Band's Trustpilot reviews →</a>" % TP, size="18px", lh="30px", font=SERIF))
kids.append(sp(8))

# ---- Ranking card (node 75:4706, matches V1's 72:3558): TWO accordions ----
def accordion(label, body_html, cls):
    # Bugs 3&4 fix (same as V1, own nodes verified equivalent): summary row
    # hugs left with an 8px gap between label and marker, and the marker is
    # the literal "▾" character (SF Pro Bold 13px, #E63946), not a chevron
    # icon. Reproduced as a text span; same rotate-on-open class hook kept.
    summary = ('<div onclick="var b=this.nextElementSibling;b.style.display=b.style.display===\'none\'?\'block\':\'none\';'
        'var c=this.querySelector(\'.%s-chev\');c.style.transform=b.style.display===\'none\'?\'rotate(0deg)\':\'rotate(180deg)\';" '
        'style="display:flex;align-items:center;justify-content:flex-start;gap:8px;cursor:pointer;padding:12px 14px;'
        'font-family:%s;font-size:15px;font-weight:700;color:#16181C;background:#fff;border:1px solid #E4E6E2;'
        'border-radius:10px">%s<span class="%s-chev" style="display:inline-block;transition:transform .2s;'
        'font-family:%s;font-size:13px;font-weight:700;color:#E63946;line-height:1">▾</span></div>') % (cls, SANS, label, cls, SANS)
    body = '<div style="display:none;padding-top:8px" class="%s-body">%s</div>' % (cls, body_html)
    return {"t":"HtmlElement","id":nid(),"p":{"content":summary+body},"styles":[{"prop":"width","value":"100%"}]}

def pc_row_html(mark, color, txt):
    return ('<div style="display:flex;gap:8px;padding:3px 0;font-family:%s;font-size:13px;line-height:19px">'
        '<span style="flex-shrink:0;width:16px;font-weight:800;color:%s">%s</span>'
        '<span style="color:#16181C">%s</span></div>') % (SANS, color, mark, txt)

_pc_html = ('<div style="display:flex;gap:18px;flex-wrap:wrap">'
    '<div style="flex:1;min-width:140px"><b style="font-family:%s;font-size:11px;letter-spacing:0.6px;color:#E63946">PROS</b>%s</div>'
    '<div style="flex:1;min-width:140px"><b style="font-family:%s;font-size:11px;letter-spacing:0.6px;color:#6A6E75">CONS</b>%s</div>'
    '</div>') % (SANS, "".join(pc_row_html("&#10003;", "#1E9E4A", p) for p in BIGBOX_PROS), SANS,
                 "".join(pc_row_html("&#10007;", "#D13C3C", c) for c in BIGBOX_CONS))

# No Figma source copy exists for "Bottom Line" in V2 either (same as V1 --
# collapsed-only, confirmed no expanded variant anywhere in the 75:4750-4753
# subtree) -- reusing V1's grounded bottom-line summary verbatim since it's
# built only from facts stated elsewhere on this exact page.
_bottom_line_html = ('<div style="font-family:%s;font-size:13px;line-height:20px;color:#16181C">'
    "The HLTH Band is the pick if you want continuous, subscription-free health tracking without giving up "
    "all-day wear. It isn't a medical device, and it's a newer name than Apple or Oura, but for the price it "
    "covers more ground than either, backed by a 30-day money-back guarantee.</div>") % SANS

def rank_card_desktop():
    thumb = container([img_block("hlth_product_rank", height="120px", radius="8px", fit="contain")],
        [{"prop":"width","value":"120px"},{"prop":"flexShrink","value":"0"}])
    _pick_label = inline_text("EDITOR'S PICK", size="12px", lh="16px", color=DARK, weight="800", font=SANS, ls="1.2px")
    _pick_label["styles"].append({"prop":"whiteSpace","value":"nowrap"})
    badge = rowf([
        text(STAR, size="15px", lh="16px", color=GOLD, weight="700", font=SANS),
        _pick_label,
    ], gap="6px", align="center", styles=[{"prop":"width","value":"fit-content"}])
    tprow = rowf([
        text(tp_stars(4.6, "#00B67A", 19) + '&nbsp;&nbsp;<span style="color:#16181C;font-weight:800;font-size:15px">4.6</span>',
             size="15px", lh="19px", font=SANS),
    ], gap="8px", align="center", styles=[{"prop":"width","value":"fit-content"}])
    main = col([
        badge, sp(4),
        text("HLTH Band 1.0", size="21px", lh="26px", color=DARK, weight="700", font=SANS), sp(6),
        tprow, sp(4),
        text('<a href="%s" target="_blank" style="color:#4A4F57;text-decoration:none">See reviews on '
             'Trustpilot →</a>' % TP, size="13px", lh="18px", font=SANS), sp(10),
        accordion("Pros &amp; Cons", _pc_html, "srev2-pc"), sp(10),
        accordion("Bottom Line", _bottom_line_html, "srev2-bl"),
    ], gap="0px", styles=[{"prop":"flex","value":"1"},{"prop":"minWidth","value":"0"}])
    price_row = rowf([
        inline_text("£79", size="20px", lh="26px", color=DARK, weight="800", font=SANS),
        inline_text('<span style="text-decoration:line-through">£158</span>', size="14px", lh="20px", color=BODY, font=SANS),
    ], gap="5px", align="center", justify="center", styles=[{"prop":"width","value":"100%"}])
    buy = col([
        button("View at HLTH", href=PDP, full=True, size="15px", weight="700", radius="10px", ls="0.3px"), sp(10),
        price_row, sp(3),
        text("Free UK shipping", size="12.5px", lh="17px", color=BODY, align="center", font=SANS),
    ], gap="0px", styles=[{"prop":"width","value":"200px"},{"prop":"flexShrink","value":"0"},{"prop":"alignItems","value":"center"}])
    row = rowf([thumb, main, buy], gap="20px", align="flex-start",
        styles=[{"prop":"padding","value":{"top":"22px","bottom":"22px","left":"20px","right":"20px"}}])
    return container([row], [{"prop":"width","value":"100%"},{"prop":"backgroundColor","value":WHITE},
        {"prop":"borderRadius","value":"14px"},{"prop":"borderStyle","value":"solid"},
        {"prop":"borderColor","value":BORDER},{"prop":"borderWidth","value":"1px"},
        {"prop":"lfDisplay","value":"none","media":767}])

def rank_card_mobile():
    badge = text('<span style="color:#F5B301;font-size:15px">★</span>&nbsp;<span style="color:#16181C;font-weight:800;letter-spacing:1.2px">EDITOR\'S PICK</span>',
                 size="12px", lh="16px", align="center", font=SANS)
    name = text("HLTH Band 1.0", size="21px", lh="26px", color=DARK, weight="700", align="center", font=SANS)
    img = img_block("hlth_product_rank", height="240px", radius="8px", fit="contain")
    tprow = text(tp_stars(4.6, "#00B67A", 19) + '&nbsp;&nbsp;<span style="color:#16181C;font-weight:800;font-size:15px">4.6</span>',
                 size="15px", lh="19px", align="center", font=SANS)
    price_row = text('<span style="font-weight:800;font-size:20px;color:#16181C">£79</span>&nbsp;&nbsp;'
                      '<span style="text-decoration:line-through;color:#4A4F57;font-size:14px">£158</span>',
                 size="20px", lh="26px", align="center", font=SANS)
    tp_link = text('<a href="%s" target="_blank" style="color:#4A4F57;text-decoration:none">See reviews on '
        'Trustpilot &#8594;</a>' % TP, size="13px", lh="18px", align="center", font=SANS)
    buy_block = col([
        container([], [{"prop":"width","value":"100%"},{"prop":"height","value":"1px"},{"prop":"backgroundColor","value":BORDER}]),
        sp(16),
        button("View at HLTH", href=PDP, full=True, size="15px", weight="700", radius="10px", ls="0.3px"), sp(10),
        price_row, sp(3),
        text("Free UK shipping", size="12.5px", lh="17px", color=BODY, align="center", font=SANS),
    ], gap="0px", styles=[{"prop":"alignItems","value":"center"}])
    inner = [badge, sp(4), name, sp(20), img, sp(14), tprow, sp(4), tp_link, sp(10),
             accordion("Pros &amp; Cons", _pc_html, "srev2-pc-m"), sp(10),
             accordion("Bottom Line", _bottom_line_html, "srev2-bl-m"), sp(32), buy_block]
    st=[{"prop":"lfDisplay","value":"none"},{"prop":"lfDisplay","value":"flex","media":767},
        {"prop":"flexDirection","value":"column"},{"prop":"gap","value":"0px"},
        {"prop":"alignItems","value":"center"},{"prop":"width","value":"100%"},
        {"prop":"backgroundColor","value":WHITE},{"prop":"borderRadius","value":"14px"},
        {"prop":"borderStyle","value":"solid"},{"prop":"borderColor","value":BORDER},
        {"prop":"borderWidth","value":"1px"},
        {"prop":"padding","value":{"top":"20px","bottom":"20px","left":"20px","right":"20px"}}]
    return {"t":"Container","id":nid(),"styles":st,"p":{"children":inner}}

kids.append(rank_card_desktop())
kids.append(rank_card_mobile())
kids.append(sp(28))

# Measured (75:4920 vs the "(repeat)" node 75:5291 just built above): V2's own
# MOBILE frame shows this exact rank card TWICE -- once here (the "(repeat)"
# placement, matching desktop's single occurrence at 75:4706/y=8879) AND once
# earlier, immediately after the "one keeps winning" intro paragraph and
# before the Big Box (75:4388 starts right after it on desktop with NO card in
# between -- confirmed via a shallow children scan of the desktop article
# column, y=4493 spacer8 -> y=4517 Big box directly). A byte-for-byte text/
# image diff of 75:4920 against 75:5291 confirmed the two mobile instances are
# IDENTICAL content (same badge/name/image/trustpilot row/2 accordions/buy
# block), so it's reproduced here as a second call to rank_card_mobile() (no
# desktop pair -- there is no second desktop occurrence to hide). V1's own
# mobile frame (72:3662) does NOT have this early duplicate (confirmed via
# search_nodes on 72:3662 -- only one "(repeat)" node exists there), so this
# is a genuine V2-mobile-only content difference the original build missed by
# assuming V2 mobile was "a straight re-application of V1's verified
# responsive recipe" without checking for new duplicated content.
kids[_EARLY_RANK_CARD_MARKER+1:_EARLY_RANK_CARD_MARKER+1] = [rank_card_mobile(), sp_mobile_only(20)]

# ============================== YOUR QUESTIONS, ANSWERED =====================
kids.append(h2("Your Questions, Answered"))
kids.append(sp(10))
def faq(q, a_html):
    return col([
        title(q, "19px", "25px", weight="700", font=SERIF),
        text(a_html, size="18px", lh="30px", color=DARK, font=SERIF),
    ], gap="8px")

kids.append(faq("Are smart rings worth it?",
    "If sleep comfort is your top priority and the price doesn't sting, a good ring is the nicest thing you "
    "can sleep in. For all-day health tracking, a screenless wrist tracker covers more, for less, without the "
    "battery compromises a ring's size forces on it."))
kids.append(sp(10))
kids.append(faq("Do screenless trackers work with iPhone and Android?",
    'The <a href="%s" target="_blank" style="color:#1A5FD0;text-decoration:underline">HLTH Band</a> works '
    "with both, and your "
    "data moves with you if you switch phones. Check this before buying any tracker; some devices lock their "
    "best features to one ecosystem." % PDP))
kids.append(sp(10))
kids.append(faq("Why don't smart rings track blood pressure?",
    "No shipping smart ring measures blood pressure. The HLTH Band tracks blood pressure trends day and "
    "night, as wellness trends for your own awareness rather than medical readings."))
kids.append(sp(10))
kids.append(faq("Is a more expensive tracker more accurate?",
    "Not by default. Most devices in this category use the same class of optical PPG sensor. What separates "
    "the data quality is placement, how often the device reads, and whether it's on your body at all, which "
    "comes down to battery and comfort rather than price."))
kids.append(sp(10))
kids.append(faq("Does the HLTH Band need a subscription?",
    "No. Every feature is unlocked at the £79 purchase, permanently, and it comes with a 30-day money-back "
    "guarantee."))
kids.append(sp(32))

# ============================== ENDMATTER (reused verbatim from V1) =========
endmatter_kids = []
endmatter_kids.append(sp(24))
endmatter_kids.append(title("Sources", "22px", "27px", weight="700", ls="-0.22px", font=SERIF))
endmatter_kids.append(sp(12))
endmatter_kids.append(text('Ring heart-rate measurement behaviour: Oura Member Care, <a href="https://support.ouraring.com" '
    'target="_blank" style="color:#1A5FD0;text-decoration:underline">"Heart Rate Graph"</a> support article '
    '(accessed 8 August 2026). Ring battery capacity (10.5 mAh) and non-replaceable battery assessments: iFixit '
    'teardowns of the Oura Ring 5 and Samsung Galaxy Ring, as reported by <a href="https://www.androidauthority.com" '
    'target="_blank" style="color:#1A5FD0;text-decoration:underline">Android Authority</a> (June 2026) and '
    '<a href="https://www.gsmarena.com" target="_blank" style="color:#1A5FD0;text-decoration:underline">GSMArena</a>. '
    'Motion and data-gap limitations of finger-based wearables: Dr. Lindsey Calcutt, biomedical engineer, quoted by '
    '<a href="https://www.livescience.com" target="_blank" style="color:#1A5FD0;text-decoration:underline">Live '
    'Science</a> (April 2026). Market-leading ring pricing and membership: ouraring.com (checked 8 August 2026). '
    'HLTH Band specifications: <a href="https://hlthtrack.co.uk" target="_blank" '
    'style="color:#1A5FD0;text-decoration:underline">hlthtrack.co.uk</a>. £79 is a launch price; standard price '
    '£158. Three-year ring cost: £349 + 36 × £5.99 ≈ £560. Prices may have changed since checking.',
    size="13.5px", lh="22px", color=BODY, font=SERIF))
endmatter_kids.append(sp(14))
endmatter_kids.append(container([text('<b style="color:#4A4F57">Disclaimer.</b> <a href="%s" target="_blank" '
    'style="color:#1A5FD0;text-decoration:underline">HLTH Band</a><span style="color:#4A4F57"> is not a medical '
    'device; readings show trends and are not a substitute for medical measurement or advice. This page is an '
    'advertisement for HLTH Band.</span>' % PDP,
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
    text("Marcus Pendleton", size="18px", lh="23px", color=DARK, weight="700", font=SANS), sp(2),
    text("Principal Writer, Wearables — TechUnboxed", size="13.5px", lh="18px", color=BODY, font=SANS), sp(10),
    text("Marcus has spent six years testing wearables for TechUnboxed, more than 40 devices across "
         "smartwatches, rings and screen-free bands. He wears an Oura Ring daily and rotates test devices on "
         "his other wrist, and after a family history of high blood pressure he pays close attention to how "
         "everyday trackers handle heart and cardiovascular data.", size="14.5px", lh="22px", color=DARK, font=SANS,
         m={"fontSize":"13.5px","lineHeight":"21px"}), sp(8),
    text("Before TechUnboxed he spent a decade in consumer electronics retail. He tests every device himself, "
         "day and night, for at least 30 days before writing about it.", size="13px", lh="20px", color=BODY, font=SANS),
], gap="0px", styles=[{"prop":"flex","value":"1"},{"prop":"minWidth","value":"0"}])],
    gap="18px", align="flex-start",
    styles=[{"prop":"backgroundColor","value":TABLEBG},{"prop":"borderStyle","value":"solid"},
        {"prop":"borderColor","value":BORDER},{"prop":"borderWidth","value":"1px"},
        {"prop":"borderRadius","value":"14px"},
        {"prop":"padding","value":{"top":"20px","bottom":"20px","left":"20px","right":"20px"}},
        {"prop":"flexDirection","value":"column","media":767},
        {"prop":"gap","value":"14px","media":767}])
endmatter_kids.append(author_box)

endmatter = col(endmatter_kids, gap="0px",
    styles=[{"prop":"borderStyle","value":"solid"},{"prop":"borderColor","value":DARK},
            {"prop":"borderWidth","value":"2px 0px 0px 0px"},{"prop":"padding","value":{"top":"6px"}}])
kids.append(endmatter)

article_col = container(kids,
    [{"prop":"maxWidth","value":"720px"},{"prop":"width","value":"100%"},
     {"prop":"margin","value":{"left":"auto","right":"auto"}},
     {"prop":"padding","value":{"left":"20px","right":"20px"},"media":767},
     {"prop":"lfDisplay","value":"flex"},{"prop":"flexDirection","value":"column"},{"prop":"gap","value":"16px"}])

# ============================== FOOTER LEGAL (reused verbatim) ==============
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
    text(MEDICAL_DISCLAIMER, size="12.5px", lh="20px", color=BODY, align="left", font=SANS, mw="900px"),
    text(ADVERTORIAL_DISCLOSURE, size="12.5px", lh="20px", color=BODY, align="left", font=SANS, mw="900px"),
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

# Measured 34px top / 60px bottom (node 75:4301), same as V1's 72:3153.
article = {"t":"Section","id":nid(),
    "styles":[{"prop":"backgroundColor","value":WHITE},{"prop":"padding","value":{"top":"34px","bottom":"60px"}}],
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
TITLE = "Screenless Trackers Are Quietly Beating Smart Rings At Their Own Game"
OG = json.load(open("pagescore/.cache/og_img_map.json"))  # QA: purpose-cut 1200x630 share images
SEO = {
    "title": "Screenless Trackers vs Smart Rings: Which Wins in 2026?",
    "description": "No display, no subscription, a fraction of the price. We tested screenless trackers against Oura and other smart rings to see which actually wins.",
    "keywords": "screenless tracker, smart ring alternative, HLTH Band, Oura Ring alternative, fitness tracker without subscription, health tracker comparison, wearable battery life, best fitness tracker 2026",
    # Reuses the same hero image already hosted for the oura-vs-hlth-band V1/V2/V3 steps.
    "social_image_uid": OG["sre-v2"]["src_uid"],
}

# QA: settings.seo emits og:* only, so X/Twitter had no card on any of the eleven pages.
# Append explicit twitter:* tags to the header custom_html, from the same SEO values.
def _esc(v): return v.replace("&","&amp;").replace('"',"&quot;").replace("<","&lt;").replace(">","&gt;")
CUSTOM_HTML = {"header": PERF + (
    '<meta name="twitter:card" content="summary_large_image">\n'
    '<meta name="twitter:title" content="%s">\n'
    '<meta name="twitter:description" content="%s">\n'
    '<meta name="twitter:image" content="%s">\n'
    ) % (_esc(SEO["title"]), _esc(SEO["description"]), OG["sre-v2"]["src"]),
    "footer": PERF_FOOTER}

# ---------------- write: create the step if new, else update its body in place ----------------
existing = sgql('query($q: String!){ funnels(first:1,query:$q){ edges { node { id starting_step_id steps { id uid slug title type settings visual { x y } } } } } }',
    {"q": f"id:{FUNNEL}"})["funnels"]["edges"][0]["node"]
existing_steps = existing["steps"]
collide = next((s for s in existing_steps if s["slug"] == STEP_SLUG), None)

if collide:
    # Redeploy path: step already exists (e.g. re-running after a content
    # fix). Update ONLY this step's body in place -- do not resend the 5
    # existing sibling steps at all (per block-schema.md, updateFunnel.steps
    # only updates steps whose id is included; omitting the others leaves
    # them untouched).
    new_steps_list = [{"id": collide["id"], "slug": STEP_SLUG, "title": TITLE, "type": "article_page",
        "settings": {"custom_html": CUSTOM_HTML, "seo": SEO}, "visual": collide["visual"], "body": body}]
    print("redeploying existing step ->", collide["id"])
else:
    create_r = sgql('''mutation($fid: ID!, $node: InputStep!){ createStep(funnel_id:$fid, node:$node){ step { id uid slug } } }''',
        {"fid": FUNNEL, "node": {"slug": STEP_SLUG, "title": TITLE, "type": "article_page",
            "settings": {"custom_html": CUSTOM_HTML, "seo": SEO}, "visual": VISUAL, "body": body}})
    NEW_STEP_ID = create_r["createStep"]["step"]["id"]
    print("created detached step ->", create_r["createStep"]["step"])
    # Attach: keep starting_step_id untouched, do NOT resend the 5 existing
    # steps -- only the new step needs to appear in this updateFunnel call.
    new_steps_list = [{"id": NEW_STEP_ID, "slug": STEP_SLUG, "title": TITLE, "type": "article_page",
        "settings": {"custom_html": CUSTOM_HTML, "seo": SEO}, "visual": VISUAL, "body": body}]

r2 = sgql('''mutation($id: ID!, $node: InputFunnel!){ updateFunnel(id:$id,node:$node){ id starting_step_id published steps { uid slug title visual { x y } } } }''',
    {"id": FUNNEL, "node": {"published": True, "steps": new_steps_list}})
print("WROTE", json.dumps(r2["updateFunnel"], indent=2))
