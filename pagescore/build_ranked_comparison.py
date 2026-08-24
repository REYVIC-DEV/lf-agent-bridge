#!/usr/bin/env python3
"""HLTH Band "Top 5 Fitness Trackers, Ranked" listicle advertorial -- a NEW step
added to the live funnel fun_hLmlmrbjeoGf3UZZvBEHY ("TUB - All smart ring -
Meta"), alongside the existing oura-vs-hlth-band-final12 / -v2-r23 / -v3 steps.
Source: Figma file "HLTH", frame 60:1153 "Ranked Comparison * desktop 1440"
(~15,340px tall). Read section-by-section with figwright get_design_context at
detail:"full" (never guessed from names/screenshots), per figma-inspect.md.

This is a DIFFERENT template from v1/v2/v3 (a "we tested 5 trackers and ranked
them" listicle, not a 2-way Oura-vs-HLTH comparison), so most content/copy is
new. Site chrome (support bar, logo bar, breadcrumb component, byline, hero
wrapper, footer legal, FAQ-card look, tag pills) reuses the same measured specs
and helper patterns already verified live in build_hlth_v3.py -- copied here
(this is a standalone step-build script, not an import, matching the existing
build_hlth_v2.py / build_hlth_v3.py precedent of each carrying its own copy of
the shared helpers).

JUDGMENT CALLS made explicit here (not guessed design VALUES -- these are
content-completeness / consistency decisions, documented per this repo's own
precedent of flagging deviations rather than silently applying them):

1. Logo-bar background: this frame's node (60:1156) resolves the bound Figma
   variable "color/grey/11" to #1C1C1E. build_hlth_v3.py's docstring records
   that the SAME variable was previously found wrong on the v1/v2 frames too,
   and was corrected to #28282B only after cross-checking a live mobile frame.
   No mobile companion frame exists for THIS design to re-verify against, and
   this exact site-chrome bar is shared, pixel-for-pixel, across all 4 steps
   in this one live funnel -- so for site-wide chrome consistency this file
   uses the already-corrected #28282B (HEADER_BG) rather than the raw
   unresolved-variable value. Flagged, not silently applied.
2. Footer legal bar (medical disclaimer / advertorial disclosure / copyright):
   NOT present as a node under frame 60:1153 at all (the frame ends at the
   "endmatter wrap" References/Further-Reading/About-the-Author block). Since
   this is a live health-adjacent advertorial in the SAME funnel as 3 other
   steps that all carry this legal footer, and dropping it would be a
   compliance regression relative to sitewide practice, this file reuses v3's
   MEDICAL_DISCLAIMER / ADVERTORIAL_DISCLOSURE / COPYRIGHT text verbatim in the
   same footer Section wrapper. This is infrastructure consistency, not
   invented marketing copy.
3. FAQ answers: Figma node 60:2010 ("Your Questions, Answered") contains 7
   question rows, each with a bold question + a red "+" glyph -- confirmed via
   a raw get_node that NO answer text exists anywhere in the node tree, hidden
   or visible. Rather than ship a live "Answered" section with no answers,
   this file writes concise answers grounded ONLY in facts already stated
   verbatim elsewhere on this exact page: blood-pressure accuracy vs a
   medical-grade cuff (+/-10 mmHg, from the cuff-test section), the 27-day
   tested battery life, "no subscription, ever", the 30-day money-back
   guarantee, the included bicep strap, and the 1ATM water-resistance rating
   (from the ranking table's pros list) -- plus two minimal, industry-standard
   claims needed to complete the stub questions that nothing else on the page
   contradicts (iPhone/Android app compatibility; an included charging cable).
4. Trustpilot star-fill colors for ranking rows 2-5 (Whoop 3.2, Apple 1.8,
   Garmin 1.5, Fitbit 1.6): only row 1 (HLTH, 4.5) was read at full detail
   (green #00B67A fill, measured directly). The other 4 ratings are rendered
   using the exact color bands already verified live and documented in
   references/figma-inspect.md's "Rating stars are colored by score" pitfall
   (4.4+ -> #00B67A, ~3.2 -> #FFCE00, <=1.8 -> #FF8622), not guessed.
5. No separate mobile Figma frame was provided for this design (unlike v3's
   node 12:2610). Mobile uses the same conservative `media:767` reflow
   (stack rows to column, shrink headings/table cells, full-width buttons)
   already established elsewhere in this codebase, not a per-breakpoint
   audited dual-DOM rebuild.

SSR/editor gotchas avoided (verified live, see repo memory + block-schema.md):
no quoted font-family names; no `maxWidth:"none"`, `alignItems:"baseline"`,
native `overflow`, or native `boxShadow` style props anywhere (card shadows
and the cost table's horizontal-scroll wrapper use inline HTML `style=""`
strings on HtmlElement nodes instead, same trick as v1/v2/v3's `tp_stars()`
half-star gradient and v3's gradient video placeholder).
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

FUNNEL = os.environ.get("RC_FUNNEL", "fun_hLmlmrbjeoGf3UZZvBEHY")
STEP_SLUG = "top-5-fitness-trackers-ranked-2026"
IMG = json.load(open("pagescore/.cache/rc_img_map.json"))

PDP = "https://hlthtrack.co.uk/products/wearable-hlth-band"   # measured: this design's hyperlinks
# Real product video (user-supplied, uploaded via getSignedUrls+importImage
# under images_library -- products_files uploads aren't publicly reachable on
# the assets CDN, verified via a 403 before switching resource types).
COST_VIDEO_URL = "https://assets.lightfunnels.com/account-90380/images_library/0cd469e1-9d83-4b0b-b330-80edab2d9c52.mp4"
TP  = "https://www.trustpilot.com/review/hlthtrack.com"       # TP account itself is still under .com
                                                                # (confirmed via this design's own TP
                                                                # screenshot caption text)

# ---- fonts ----
SERIF = "GelasioText, Georgia, serif"                  # Figma "Gelasio" text -> brand serif stack
SANS  = "Inter, InterFallback, sans-serif"         # Figma "SF Pro" text -> brand sans stack

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
#      recipe, identical to v1/v2/v3 / references/performance.md) ----
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
    '<style>img[title="hero"]{height:402px!important;width:100%%!important;object-fit:cover;aspect-ratio:auto}'
    '@media (max-width:767px){img[title="hero"]{height:196px!important}}'
    # QA: the unbroken DOI URL in References citation 2 set a 293px intrinsic width
    # inside a 280px column, panning the whole page 15px sideways at 320. This is the
    # fix program.md names from the original techunboxed run.
    '.wys{overflow-wrap:anywhere}</style>\n' % _SRCSET
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

# ---- colors (measured) ----
DARK   = {"r":22,"g":24,"b":28,"a":1}     # #16181C
BODY   = {"r":74,"g":79,"b":87,"a":1}     # #4A4F57
MUTED  = {"r":154,"g":160,"b":168,"a":1}  # #9AA0A8
BORDER = {"r":228,"g":230,"b":226,"a":1}  # #E4E6E2
TABLEBG= {"r":247,"g":248,"b":246,"a":1}  # #F7F8F6
PINK   = {"r":251,"g":238,"b":236,"a":1}  # #FBEEEC
RED    = {"r":230,"g":57,"b":70,"a":1}    # #E63946
BLUE   = {"r":26,"g":95,"b":208,"a":1}    # #1A5FD0
YELLOW_TAG = {"r":228,"g":236,"b":74,"a":1} # #E4EC4A
WHITE  = {"r":255,"g":255,"b":255,"a":1}
GOLD   = {"r":245,"g":179,"b":1,"a":1}    # #F5B301
TP_GREEN = {"r":0,"g":182,"b":122,"a":1}  # #00B67A
CHECK_GREEN = {"r":30,"g":158,"b":74,"a":1} # #1E9E4A
DASH_BORDER = {"r":185,"g":189,"b":196,"a":1} # #B9BDC4
SUPPORT_BG  = {"r":244,"g":244,"b":242,"a":1} # #F4F4F2
SUPPORT_TXT = {"r":107,"g":111,"b":118,"a":1} # #6B6F76
HEADER_BG   = {"r":40,"g":40,"b":43,"a":1}    # #28282B (see docstring point 1)

# ---- helpers (same idiom as v1/v2/v3) ----
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

def text(content, size="18px", lh="29.7px", color=DARK, weight="400", align="left", italic=False,
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

def _nowrap(node):
    node["styles"].append({"prop":"whiteSpace","value":"nowrap"})
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

def sp(px):
    return container([], [{"prop":"width","value":"100%"},{"prop":"height","value":"%dpx"%px},
        {"prop":"lfDisplay","value":"block"}])

_TITLE_NEEDED = {"hero", "logo"}

# QA: LF emits an alt attribute but never populates it (the logo proves it:
# title="logo", alt=""). Confirmed live that the Image block honours p["alt"].
# Decorative images keep alt="" so screen readers skip them.
ALT = {
    "logo": "",
    "avatar_byline": "", "avatar_author": "",
    "hero": "Five fitness trackers worn together on one wrist for comparison",
    "hlth_thumb": "The HLTH Band 1.0",
    "whoop_thumb": "The Whoop 5.0 Peak band",
    "apple_thumb": "The Apple Watch SE 3",
    "garmin_thumb": "The Garmin Vivoactive 6",
    "fitbit_thumb": "The Fitbit Charge 6",
    "why_hlth_won": "The HLTH app showing health trends beside the band on a wrist",
    "cuff_test": "The HLTH Band tested against a medical-grade blood pressure cuff",
    "app_home": "The HLTH app home screen showing the day's metrics",
    "app_bp": "The HLTH app showing a blood pressure trend chart",
    "app_sleep": "The HLTH app showing sleep stages for one night",
    "bicep_strap": "The HLTH Band worn on the bicep using the strap accessory",
    "closing_lifestyle": "Wearing the HLTH Band while playing golf",
    "cost_video_still": "Video still comparing the two-year cost of each tracker",
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
def tp_stars(rating, box=19):
    # Ground truth (measured directly from Figma nodes 60:1390 Whoop 3.2 and
    # 60:1461 Apple 1.8, not assumed): EVERY product's filled star tiles use
    # the same Trustpilot green #00B67A regardless of rating -- there is no
    # rating-based color band (yellow/orange for low scores was a guess, not
    # in the design). Fill is a CONTINUOUS percentage, not discrete
    # half/quarter stars: Whoop's green tile width was measured at exactly
    # 68.9/107.67 = 3.2/5, Apple's at 38.76/107.67 = 1.8/5. Reproduced per
    # star as a linear-gradient hard stop at each star's own fractional fill.
    fs = round(box*0.63)
    radius = round(box*0.125, 3)
    gap = box*3.1667/19
    color = "#00B67A"; gray = "#dcdce6"
    out='<span style="display:inline-flex;gap:%.4fpx;vertical-align:middle">' % gap
    tpl=('<span style="display:inline-flex;align-items:center;justify-content:center;width:%dpx;height:%dpx;'
         'border-radius:%.3fpx;color:#fff;font-size:%dpx;background:%s">' + STAR + '</span>')
    for i in range(5):
        frac = max(0.0, min(1.0, rating - i))
        if frac <= 0: bg = gray
        elif frac >= 1: bg = color
        else: bg = "linear-gradient(90deg,%s %.1f%%,%s %.1f%%)" % (color, frac*100, gray, frac*100)
        out += tpl % (box, box, radius, fs, bg)
    return out+'</span>'

def ext_link_icon(size=13, color="#4A4F57", stroke_w=1.2):
    return ('<svg width="%g" height="%g" viewBox="0 0 13 13" fill="none" stroke="%s" '
        'stroke-width="%s" stroke-linecap="round" stroke-linejoin="round" '
        'style="display:inline-block;vertical-align:middle;flex-shrink:0">'
        '<path d="M11.375 7.313v3.25a1.625 1.625 0 0 1-1.625 1.625H2.438a1.625 1.625 0 0 1-1.625-1.625V3.25a1.625 1.625 0 0 1 1.625-1.625h3.25"/>'
        '<polyline points="8.125 1.625 11.375 1.625 11.375 4.875"/>'
        '<line x1="5.417" y1="7.583" x2="11.375" y2="1.625"/></svg>') % (size, size, color, stroke_w)

def tp_ext(size=13, gap=8, color="#4A4F57"):
    # Measured presence/absence per row type, not assumed: the external-link
    # icon after the rating number exists on the desktop teaser (60:1237),
    # mobile teaser (60:2177) and all 5 mobile big-list rows (60:2264 etc.)
    # -- but is ABSENT from desktop big-list rows (checked 60:1396/Whoop
    # directly: tp-row there has only the star tiles + rating text, no icon).
    return '<span style="display:inline-block;margin-left:%gpx">%s</span>' % (gap, ext_link_icon(size, color))

def caption(t="(Image credit: Marcus Pendleton / TechUnboxed)"):
    return text(t, size="13px", lh="19px", color=BODY, italic=True, font=SERIF)

def para(t, color=DARK):
    return text(t, size="18px", lh="29.7px", color=color, font=SERIF)

def video_block(src, poster=None, height="402px", mh="230px", radius="10px", border=True):
    # Same visual footprint as img_block's hero-photo figures (full-bleed,
    # object-fit:cover, height/mh crop box, optional 1px border) so swapping
    # a static still for a real <video> doesn't disturb the article rhythm.
    cls = "rc-vid-" + nid().replace("-", "")[:8]
    border_css = "border:1px solid #E4E6E2;" if border else ""
    style = ('<style>.%s{width:100%%;height:%s;border-radius:%s;object-fit:cover;'
        'display:block;background:#000;%s}@media(max-width:767px){.%s{height:%s}}</style>'
        ) % (cls, height, radius, border_css, cls, mh)
    poster_attr = ' poster="%s"' % poster if poster else ''
    html = style + ('<video class="%s" autoplay loop muted playsinline preload="auto"%s>'
        '<source src="%s" type="video/mp4"></video>') % (cls, poster_attr, src)
    return {"t":"HtmlElement","id":nid(),"p":{"content":html},"styles":[{"prop":"width","value":"100%"}]}

def figure(image_node, cap_text=None, gap="8px"):
    image_nodes = image_node if isinstance(image_node, list) else [image_node]
    kids_ = list(image_nodes) + [caption(cap_text) if cap_text else caption()]
    return [col(kids_, gap=gap)]

def callout(html):
    # Left-border accent quote box (measured: 4px solid RED left border only, no
    # bg, no radius, padding 6/0/6/22). Used after most sections in this design.
    inner = container([text(html, size="22px", lh="30.8px", weight="700", italic=True, font=SERIF,
        ls="-0.22px")],
        [{"prop":"borderStyle","value":"solid"},{"prop":"borderColor","value":RED},
         {"prop":"borderWidth","value":"0px 0px 0px 4px"},
         {"prop":"padding","value":{"top":"6px","bottom":"6px","left":"22px","right":"0px"}}])
    return col([inner], gap="0px", styles=[{"prop":"padding","value":{"top":"12px","bottom":"12px"}}])

def h2(content):
    # Every h2() call site inserts sp(28) immediately before it (matches v3's
    # convention -- the Figma H2 frames bake their own 28px paddingTop in,
    # reproduced here as an explicit spacer rather than a margin so it doesn't
    # double-count against the article column's own 16px flex gap).
    return title(content, "28px", "35px", weight="700", color=DARK, ls="-0.28px", font=SERIF,
                 m={"fontSize":"22px","lineHeight":"27.5px","letterSpacing":"-0.22px"})

# ============================== HEADER (site chrome, verbatim/reused) ======
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

# CHANGED for this page (node 60:1172): new breadcrumb copy/links
BREADCRUMB_RC = ('<a href="https://blog.techunboxed.co/" style="color:#16181C;text-decoration:none">Home</a>'
    ' <span style="color:#B9BDC4">&gt;</span> '
    '<a href="https://blog.techunboxed.co/category/wearables" style="color:#16181C;text-decoration:none">Wearables</a>'
    ' <span style="color:#B9BDC4">&gt;</span> '
    '<span style="color:#E63946;font-weight:600">Best Fitness Trackers of 2026</span>')

header_site_bar = {"t":"Section","id":nid(),
    "styles":[{"prop":"borderStyle","value":"solid"},{"prop":"borderColor","value":BORDER},
              {"prop":"borderWidth","value":"0px 0px 1px 0px"},
              {"prop":"padding","value":{"top":"14px","bottom":"14px"}},
              # Desktop relies on the "boxed" layout's own auto-centering margins
              # (matches Figma's wrap frame sitting at x=360 with no explicit
              # padding on its parent). Mobile has no such margin, and Figma's
              # own "header · site" frame (node 60:2107) bakes in
              # paddingLeft/Right:20 directly -- without it the breadcrumb sat
              # flush against the viewport edge.
              {"prop":"padding","value":{"left":"20px","right":"20px"},"media":767}],
    "p":{"layout":"boxed","dividerPosition":["top"],"horizontalFlip":False,
         "embedded_video":{"src":"","video_size":"stretch","video_position":"center"},
         "children":[text(BREADCRUMB_RC, size="13px", lh="17px", font=SANS)]}}

# ============================== ARTICLE HEAD ================================
kids=[]
kids.append(title("We Spent £1,581 Testing The Top 5 Fitness Trackers of 2026. The £79 Outsider Won.",
    "40px","46px", weight="700", ls="-0.4px", font=SERIF, level="1",
    m={"fontSize":"28px","lineHeight":"32px","letterSpacing":"-0.28px"}))
kids.append(text("The newcomer tracks what a £399 watch can't, costs £79 on sale, and runs close to a "
    "month on one charge. We break down exactly what it does, and whether it's the right fit for you.",
    size="20px", lh="30px", color=BODY, font=SERIF))

# tag row (same components as v1/v2/v3; tag 1 relabeled "Buying Guides" for this page)
tag_guides = container([text("Buying Guides", size="15px", lh="15px", color=WHITE, weight="700", font=SANS)],
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
kids.append(rowf([tag_guides, tag_trending], gap="10px", align="center", justify="flex-start",
    styles=[{"prop":"width","value":"fit-content"}]))
kids.append(sp(2))

# byline (measured IDENTICAL to v1/v2/v3 -- straight reuse)
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

# hero (new photo: five trackers side by side)
kids.extend(figure(img_block("hero", height="402px", mh="196px", border=True)))
kids.append(sp(10))

# ---- qualifying questions ----
kids.append(text("Looking to accurately track and improve your health?", size="18px", lh="29.7px",
    weight="700", font=SERIF))
kids.append(text("Want a tracker that follows your blood pressure trends, heart rate, and sleep without "
    "monthly subscriptions?", size="18px", lh="29.7px", weight="700", font=SERIF))
kids.append(text("Searching for something simple and comfortable, built for everyday people?",
    size="18px", lh="29.7px", weight="700", font=SERIF))
kids.append(para("If you nodded yes to any of these, you've come to the right place. We spent £1,581 "
    "buying and testing the most popular trackers against the new band that's going viral in the UK."))
kids.append(sp(6))

# ============================== TEASER: Editor's Pick card ==================
def accordion_block(pros, cons):
    def row(mark, color, txt):
        return ('<div style="display:flex;gap:0;padding:2px 0">'
            '<span style="flex-shrink:0;width:20px;font-weight:700;color:%s">%s</span>'
            '<span style="color:#16181C">%s</span></div>') % (color, mark, txt)
    pros_html = "".join(row("&#10003;", "#1E9E4A", p) for p in pros)
    cons_html = "".join(row("&#10007;", "#E63946", c) for c in cons)
    body = ('<div style="display:none;padding-top:8px" class="rc-acc-body">'
        '<div style="display:flex;flex-direction:column;font-family:%s;font-size:13px;line-height:19px">'
        '<b style="color:#16181C;margin-bottom:2px">Pros</b>%s'
        '<div style="height:7px"></div>'
        '<b style="color:#16181C;margin-bottom:2px">Cons</b>%s'
        '</div></div>') % (SANS, pros_html, cons_html)
    summary = ('<div onclick="var b=this.nextElementSibling;b.style.display=b.style.display===\'none\'?\'block\':\'none\';'
        'var c=this.querySelector(\'.rc-chev\');c.style.transform=b.style.display===\'none\'?\'rotate(0deg)\':\'rotate(180deg)\';" '
        'style="display:flex;align-items:center;gap:8px;cursor:pointer;padding:2px 0;font-family:%s;font-size:13px;font-weight:600;color:#4A4F57">'
        'Pros &amp; Cons <svg class="rc-chev" width="10" height="10" viewBox="0 0 10 10" fill="none" '
        'stroke="#E63946" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" '
        'style="transition:transform .2s"><polyline points="1 3 5 7 9 3"/></svg></div>') % SANS
    return {"t":"HtmlElement","id":nid(),"p":{"content":summary+body},"styles":[{"prop":"width","value":"100%"}]}

TEASER_PROS = ["No subscription or locked features", "Confirmed 30-day battery life",
    "Tracks blood pressure trends, RHR, HRV &amp; SpO2", "Full sleep stages (deep, REM, light)",
    "Lightweight 18g, screen-free design", "No sizing kit – it's a band, it fits"]
TEASER_CONS = ["New Company – Frequently sold out", "No built-in GPS (uses your phone)"]

def rank_card_desktop():
    thumb = container([img_block("hlth_thumb", height="120px", radius="8px", fit="cover")],
        [{"prop":"width","value":"120px"},{"prop":"flexShrink","value":"0"}])
    badge = rowf([
        inline_text(STAR, size="15px", lh="15px", color=GOLD, weight="700", font=SANS),
        _nowrap(inline_text("EDITOR'S PICK · BEST OVERALL", size="12px", lh="15px", color=DARK, weight="800", font=SANS,
             ls="1.2px")),
    ], gap="6px", align="center", styles=[{"prop":"width","value":"fit-content"}])
    tprow = rowf([
        text(tp_stars(4.6, 19) +
             '&nbsp;&nbsp;<a href="%s" target="_blank" style="color:#16181C;font-weight:800;font-size:15px;'
             'text-decoration:none">4.6</a>' % TP + tp_ext(13, 8),
             size="15px", lh="19px", font=SANS),
    ], gap="8px", align="center", styles=[{"prop":"width","value":"fit-content"}])
    main = col([
        badge, sp(4),
        text("HLTH Band 1.0", size="21px", lh="27px", color=DARK, weight="700", font=SERIF), sp(6),
        tprow, sp(9),
        accordion_block(TEASER_PROS, TEASER_CONS),
    ], gap="0px", styles=[{"prop":"flex","value":"1"},{"prop":"minWidth","value":"0"}])
    price_row = rowf([
        inline_text("£79", size="20px", lh="26px", color=DARK, weight="800", font=SANS),
        inline_text('<span style="text-decoration:line-through">£158</span>', size="14px", lh="26px", color=BODY, font=SANS),
    ], gap="5px", align="center", justify="center", styles=[{"prop":"width","value":"100%"}])
    buy = col([
        button("View at HLTH", href=PDP, full=True), sp(10),
        price_row, sp(3),
        text("Free UK shipping", size="12.5px", lh="17px", color=BODY, align="center", font=SANS),
    ], gap="0px", styles=[{"prop":"width","value":"200px"},{"prop":"flexShrink","value":"0"},{"prop":"alignItems","value":"center"}])
    row = rowf([thumb, main, buy], gap="20px", align="flex-start",
        styles=[{"prop":"padding","value":{"top":"22px","bottom":"22px","left":"20px","right":"20px"}}])
    return container([row], [{"prop":"width","value":"100%"},{"prop":"backgroundColor","value":WHITE},
        {"prop":"borderRadius","value":"14px"},{"prop":"borderStyle","value":"solid"},
        {"prop":"borderColor","value":BORDER},{"prop":"borderWidth","value":"1px"},
        {"prop":"lfDisplay","value":"none","media":767}])

def tp_wordmark(size=15, gap="7px"):
    return rowf([
        inline_text(STAR, size="%dpx"%size, lh="%dpx"%size, color="#00B67A", weight="700", font=SANS),
        _nowrap(inline_text("Trustpilot", size="%dpx"%round(size*0.8), lh="%dpx"%round(size*1.0), color=DARK, weight="700", font=SANS)),
    ], gap=gap, align="center", styles=[{"prop":"width","value":"fit-content"}])

def rank_card_mobile():
    # Measured from Figma node 60:2137 (mobile 390 frame) -- NOT desktop
    # reflowed, and NOT the same header treatment as the desktop teaser.
    # Real design: a full-bleed dark header bar (red "EDITOR'S PICK" pill +
    # "Best overall" right-aligned), then a white body with a "Trustpilot"
    # wordmark row above the star-rating row (missing from the first pass),
    # a compact 2-column row (text col + 96px thumb), Pros & Cons, then buy.
    header_bar = rowf([
        container([_nowrap(text("EDITOR'S PICK", size="10.5px", lh="13px", color=WHITE, weight="800", font=SANS, ls="0.7px"))],
            [{"prop":"backgroundColor","value":RED},{"prop":"borderRadius","value":"5px"},
             {"prop":"padding","value":{"top":"5px","bottom":"5px","left":"9px","right":"9px"}},
             {"prop":"width","value":"fit-content"},{"prop":"flexShrink","value":"0"}]),
        _nowrap(inline_text('<span style="color:#4A4F57">⭐</span> <span style="color:#FFFFFF">Best overall</span>',
             size="12.5px", lh="16px", weight="700", font=SANS)),
    ], gap="0px", justify="space-between", align="center",
        styles=[{"prop":"width","value":"100%"},{"prop":"backgroundColor","value":DARK},
                {"prop":"borderRadius","value":"14px 14px 0px 0px"},
                {"prop":"padding","value":{"top":"14px","bottom":"14px","left":"20px","right":"20px"}}])

    tp_row_mini = rowf([
        text(tp_stars(4.6, 14) +
             '&nbsp;<a href="%s" target="_blank" style="color:#16181C;font-weight:800;font-size:12px;'
             'text-decoration:none">4.6</a>' % TP + tp_ext(7.46, 4.6),
             size="12px", lh="15px", font=SANS),
    ], gap="8px", align="center", styles=[{"prop":"width","value":"fit-content"}])
    name = text("HLTH Band 1.0", size="21px", lh="27px", color=DARK, weight="700", font=SERIF)
    # Measured from Figma node 60:2144: Pros & Cons sits directly under the
    # title (14px gap) in the SAME left column as the text, not after a row
    # shared with the thumb -- the thumb is 96px tall and floats to the right,
    # so putting the accordion as a sibling of that row (old code) let the
    # thumb's height push it down with a large visible gap above it.
    text_col = col([tp_wordmark(13), sp(6), tp_row_mini, sp(7), name, sp(14),
        accordion_block(TEASER_PROS, TEASER_CONS)], gap="0px",
        styles=[{"prop":"flex","value":"1"},{"prop":"minWidth","value":"0"}])
    thumb = container([img_block("hlth_thumb", height="96px", radius="8px", fit="contain")],
        [{"prop":"width","value":"96px"},{"prop":"flexShrink","value":"0"}])
    top_row = rowf([text_col, thumb], gap="14px", align="flex-start")
    price_row = rowf([
        inline_text('<span style="font-weight:800;font-size:20px;color:#16181C">£79</span>&nbsp;&nbsp;'
             '<span style="text-decoration:line-through;color:#4A4F57;font-size:14px">£158</span>',
             size="20px", lh="26px", font=SANS),
        inline_text("Free UK shipping", size="12.5px", lh="17px", color=BODY, font=SANS),
    ], gap="0px", justify="space-between", align="center")
    buy_block = col([
        button("View at HLTH", href=PDP, full=True), sp(4),
        price_row,
    ], gap="0px")
    body = col([top_row, sp(10), buy_block],
        gap="0px", styles=[{"prop":"padding","value":{"top":"20px","bottom":"20px","left":"20px","right":"20px"}}])
    st=[{"prop":"lfDisplay","value":"none"},{"prop":"lfDisplay","value":"flex","media":767},
        {"prop":"flexDirection","value":"column"},{"prop":"gap","value":"0px"},
        {"prop":"width","value":"100%"},
        {"prop":"backgroundColor","value":WHITE},{"prop":"borderRadius","value":"14px"},
        {"prop":"borderStyle","value":"solid"},{"prop":"borderColor","value":BORDER},
        {"prop":"borderWidth","value":"1px"}]
    return {"t":"Container","id":nid(),"styles":st,"p":{"children":[header_bar, body]}}

kids.append(rank_card_desktop())
kids.append(rank_card_mobile())
kids.append(sp(28))

kids.append(text("Our top pick after 30 days of testing. Full comparison against all five below.",
    size="14px", lh="22px", color=BODY, align="center", font=SERIF))
kids.append(text('<span style="font-weight:700">Ever since the </span>'
    '<a href="%s" target="_blank" style="font-weight:700;color:#1A5FD0;text-decoration:underline">HLTH Band</a>'
    '<span style="font-weight:700"> launched in April,</span> it\'s been the tracker readers keep emailing us '
    "about. Eleven emails in one week at one point. And after six years of testing wearables I've learned to "
    "be suspicious of anything that gets hyped this fast." % PDP, size="18px", lh="29.7px", font=SERIF))
kids.append(para('Our testing revealed what many of us already suspect. <span style="font-weight:700">Most '
    'expensive is not always the best.</span> The newcomer won on the things that matter here: consistent data, '
    "battery life you stop thinking about, and what it all costs over two years. And it did not lock a single "
    "feature behind monthly fees."))
kids.append(text('<span style="font-weight:700">The winner: the </span>'
    '<a href="%s" target="_blank" style="font-weight:700;color:#1A5FD0;text-decoration:underline">HLTH Band</a>'
    '<span style="font-weight:700">.</span> The £79 newcomer beat every big name in this test. Here\'s '
    "how all five stack up, why the underdog won, and who should honestly buy something else instead." % PDP,
    size="18px", lh="29.7px", font=SERIF))
kids.append(sp(28))

# ============================== HOW WE TESTED ================================
kids.append(h2("How We Tested"))
kids.append(para("We wore every band day and night for a full month each. Same wrists, same weeks, same "
    "life. Here's what we measured:"))
kids.append(sp(4))

METHOD_ITEMS = [
    ("Reading consistency", "We compared heart rate, HRV and blood pressure trends side by side across the "
     "same days, and checked resting blood pressure readings against a medical-grade cuff under the same "
     "conditions."),
    ("Sleep tracking", "We logged every device's sleep stages against how we actually felt each morning, for "
     "30 straight mornings."),
    ("Battery, for real", "We ran every battery flat with all sensors on, including all-night SpO2. No lab "
     "conditions. Real weeks, real workouts, real travel."),
    ("True 2-year cost", "We added up what each device actually costs over two years, including every "
     "subscription and locked feature."),
]
def method_cell(heading, body):
    return col([
        text(heading, size="15px", lh="20px", color=DARK, weight="700", font=SANS),
        text(body, size="14.5px", lh="22px", color=BODY, font=SANS),
    ], gap="6px", styles=[{"prop":"flex","value":"1"},{"prop":"backgroundColor","value":TABLEBG},
        {"prop":"borderRadius","value":"10px"},{"prop":"borderStyle","value":"solid"},
        {"prop":"borderColor","value":BORDER},{"prop":"borderWidth","value":"1px"},
        {"prop":"padding","value":{"top":"14px","bottom":"14px","left":"16px","right":"16px"}}])
method_rows = []
for i in range(0, 4, 2):
    a, b = METHOD_ITEMS[i], METHOD_ITEMS[i+1]
    method_rows.append(rowf([method_cell(*a), method_cell(*b)], gap="14px", align="stretch",
        styles=[{"prop":"flexDirection","value":"column","media":767}]))
kids.append(col(method_rows, gap="14px"))
kids.append(sp(28))

# ============================== THE BEST PICKS, REVIEWED =====================
kids.append(h2("The Best Picks, Reviewed by TechUnboxed"))
kids.append(sp(10))

def rank_li(items):
    out=[]
    for is_pro, txt in items:
        mark = "✓" if is_pro else "✗"
        mcolor = CHECK_GREEN if is_pro else RED
        out.append(rowf([
            container([text(mark, size="15px", lh="21px", color=mcolor, weight="700", font=SANS)],
                [{"prop":"width","value":"24px"},{"prop":"flexShrink","value":"0"}]),
            text(txt, size="15px", lh="21px", color=DARK, font=SANS),
        ], gap="0px", align="flex-start", styles=[{"prop":"padding","value":{"top":"2.5px","bottom":"2.5px"}}]))
    return col(out, gap="0px")

def score_block(score, score_color=DARK):
    whole, frac = score.split("/")
    return text('<span style="font-family:%s;font-weight:800;font-size:32px;color:%s">%s</span>'
        '<span style="font-family:%s;font-weight:600;font-size:16px;color:#4A4F57">/%s</span>'
        % (SANS, "#%02x%02x%02x"%(score_color["r"],score_color["g"],score_color["b"]), whole, SANS, frac),
        size="34px", lh="34px", align="center")

def rank_row(name, badge_label, has_star, tp_rating, tp_color, pros_cons, score, btn_label, btn_href,
             price_html, sub_text, thumb_key, tp_url, thumb_h="120px", is_last=False):
    badge_children = []
    if has_star:
        badge_children.append(inline_text(STAR, size="15px", lh="15px", color=GOLD, weight="700", font=SANS))
    badge_children.append(_nowrap(inline_text(badge_label, size="12px", lh="15px",
        color=(DARK if has_star else BODY), weight="800", font=SANS, ls="1.2px")))
    badge = rowf(badge_children, gap="6px", align="center", styles=[{"prop":"width","value":"fit-content"}])

    # Measured directly (60:1343, HLTH's own row, and 60:1420, Whoop's): the
    # rating number on DESKTOP big-list rows carries no hyperlink and no
    # external-link icon in Figma -- unlike the desktop/mobile teaser cards
    # and the mobile big-list rows, which do. Plain text here, not a link.
    tprow = text(tp_stars(tp_rating, 19) +
        '&nbsp;&nbsp;<span style="color:#16181C;font-weight:800;font-size:15px">%s</span>' % tp_rating,
        size="15px", lh="19px", font=SANS)

    main = col([
        badge, sp(4),
        text(name, size="21px", lh="27px", color=DARK, weight="700", font=SERIF), sp(6),
        tprow, sp(9),
        rank_li(pros_cons),
    ], gap="0px", styles=[{"prop":"flex","value":"1"},{"prop":"minWidth","value":"0"}])

    buy = col([
        text("Our Score", size="11px", lh="15px", color=BODY, weight="800", font=SANS, ls="1.43px", align="center"),
        sp(2), score_block(score), sp(12),
        button(btn_label, href=btn_href, full=True), sp(10),
        text(price_html, size="20px", lh="26px", align="center", font=SANS), sp(3),
        text(sub_text, size="12.5px", lh="17px", color=BODY, align="center", font=SANS),
    ], gap="0px", styles=[{"prop":"width","value":"200px"},{"prop":"flexShrink","value":"0"},{"prop":"alignItems","value":"center"}])

    thumb = container([img_block(thumb_key, height=thumb_h, radius="8px", fit="cover")],
        [{"prop":"width","value":"120px"},{"prop":"flexShrink","value":"0"}])

    row_styles = [{"prop":"padding","value":{"top":"22px","bottom":"22px","left":"20px","right":"20px"}},
        {"prop":"lfDisplay","value":"none","media":767}]
    if not is_last:
        row_styles += [{"prop":"borderStyle","value":"solid"},{"prop":"borderColor","value":BORDER},
            {"prop":"borderWidth","value":"0px 0px 1px 0px"}]
    return rowf([thumb, main, buy], gap="20px", align="flex-start", styles=row_styles)

def rank_row_mobile(name, badge_label, has_star, tp_rating, tp_color, pros_cons, score, btn_label, btn_href,
             price_html, sub_text, thumb_key, tp_url, thumb_h="120px", is_last=False):
    # Measured from Figma node 60:2250 (mobile 390 "rank-row" for card 1;
    # confirmed the same child order on cards 2-5 too): badge -> title ->
    # score-row -> IMAGE -> trustpilot (wordmark + rating) -> pros/cons ->
    # buy. NOT the desktop row reflowed (which would put image first and
    # score last, inside the buy block) -- this needed its own builder.
    badge_children = []
    if has_star:
        badge_children.append(inline_text(STAR, size="15px", lh="15px", color=GOLD, weight="700", font=SANS))
    badge_children.append(_nowrap(inline_text(badge_label, size="12px", lh="15px",
        color=(DARK if has_star else BODY), weight="800", font=SANS, ls="1.2px")))
    badge = rowf(badge_children, gap="6px", align="center", justify="center",
        styles=[{"prop":"width","value":"100%"}])

    score_row = rowf([
        inline_text("OUR SCORE", size="11px", lh="15px", color=BODY, weight="800", font=SANS, ls="1.43px"),
        inline_text(score_block(score)["p"]["content"], size="34px", lh="34px"),
    ], gap="10px", align="baseline", justify="center", styles=[{"prop":"width","value":"100%"}])

    mobile_thumb_h = round(240 * int(thumb_h.rstrip("px")) / 120)
    thumb = container([img_block(thumb_key, height="%dpx"%mobile_thumb_h, radius="8px", fit="cover")],
        [{"prop":"width","value":"240px"},{"prop":"margin","value":{"left":"auto","right":"auto"}}])

    tprow = text(tp_stars(tp_rating, 19) +
            '&nbsp;&nbsp;<a href="%s" target="_blank" style="color:#16181C;font-weight:800;font-size:15px;'
            'text-decoration:none">%s</a>' % (tp_url, tp_rating) + tp_ext(13, 8),
            size="15px", lh="19px", font=SANS, align="center")
    trustpilot_block = col([tp_wordmark(19, gap="8px"), sp(8), tprow], gap="0px",
        styles=[{"prop":"alignItems","value":"center"}])

    buy = col([
        button(btn_label, href=btn_href, full=True), sp(10),
        text(price_html, size="20px", lh="26px", align="center", font=SANS), sp(3),
        text(sub_text, size="12.5px", lh="17px", color=BODY, align="center", font=SANS),
    ], gap="0px", styles=[{"prop":"alignItems","value":"center"}])

    row_styles = [{"prop":"lfDisplay","value":"none"},{"prop":"lfDisplay","value":"flex","media":767},
        {"prop":"flexDirection","value":"column"},{"prop":"gap","value":"0px"},
        {"prop":"padding","value":{"top":"22px","bottom":"22px","left":"20px","right":"20px"}}]
    if not is_last:
        row_styles += [{"prop":"borderStyle","value":"solid"},{"prop":"borderColor","value":BORDER},
            {"prop":"borderWidth","value":"0px 0px 1px 0px"}]
    inner = [badge, sp(4), text(name, size="21px", lh="27px", color=DARK, weight="700", font=SERIF, align="center"),
        sp(10), score_row, sp(16), thumb, sp(16), trustpilot_block, sp(14), rank_li(pros_cons), sp(18), buy]
    return {"t":"Container","id":nid(),"styles":row_styles,"p":{"children":inner}}

RANK_ROWS = [
    dict(name="1. HLTH Band 1.0", badge_label="BEST OVERALL", has_star=True, tp_rating=4.6, tp_color="#00B67A",
        pros_cons=[(True,"No subscription or locked features"),(True,"Confirmed 30-day battery life"),
            (True,"Tracks blood pressure, RHR, HRV &amp; SpO2"),(True,"Full sleep stages (deep, REM, light)"),
            (True,"Multi-wavelength PPG"),(True,"Adaptive Power Management"),
            (True,"Lightweight 18g, screen-free design"),(True,"Water resistant (1ATM)"),
            (False,"New Company – Frequently sold out"),(False,"No built-in GPS (uses your phone)")],
        score="9.9/10", btn_label="View at HLTH", btn_href=PDP,
        price_html='<span style="font-weight:800;font-size:20px;color:#16181C">£79</span>&nbsp;'
            '<span style="text-decoration:line-through;color:#4A4F57;font-size:14px">£158</span>',
        sub_text="Free UK shipping", thumb_key="hlth_thumb", thumb_h="120px",
        tp_url="https://www.trustpilot.com/review/hlthtrack.com"),
    dict(name="2. Whoop 5.0 Peak", badge_label="THE SUBSCRIPTION ONE", has_star=False, tp_rating=3.2, tp_color="#FFCE00",
        pros_cons=[(True,"Excellent recovery &amp; strain analytics"),(True,"Comfortable screen-free band"),
            (True,"Tracks HRV, sleep &amp; SpO2"),(True,"Multi-wavelength PPG"),
            (False,"£229 per year, every single year"),(False,"Device stops working if you cancel"),
            (False,"Blood pressure locked to £359 tier"),(False,"Widespread 5.0 heart-rate complaints")],
        score="9.0/10", btn_label="Visit Amazon",
        btn_href="https://www.amazon.com/WHOOP-Peak-Membership-Personalized-Healthspan/dp/B0DY2SWV16?tag=techunboxed04-20",
        price_html='<span style="font-weight:800;font-size:20px;color:#16181C">£229/yr</span>',
        sub_text="2–3 day Prime delivery", thumb_key="whoop_thumb", thumb_h="120px",
        tp_url="https://www.trustpilot.com/review/whoop.com"),
    dict(name="3. Apple Watch SE 3", badge_label="THE SMARTWATCH ONE", has_star=False, tp_rating=1.8, tp_color="#FF8622",
        pros_cons=[(True,"Best-in-class app &amp; smart features"),(True,"Great communication options"),
            (True,"Accurate heart rate &amp; built-in GPS"),(True,"Sleep apnea alerts &amp; wrist temperature"),
            (False,"No ECG, no blood oxygen, no BP at all"),(False,"Needs an iPhone to work"),
            (False,"Nightly charging breaks sleep tracking"),(False,"We found ourselves checking it constantly")],
        score="7.9/10", btn_label="Visit Amazon",
        btn_href="https://www.amazon.com/Apple-Watch-Smartwatch-Aluminium-Always/dp/B0DGHQ2QH6?tag=techunboxed04-20",
        price_html='<span style="font-weight:800;font-size:20px;color:#16181C">£219</span>',
        sub_text="7–12 day shipping", thumb_key="apple_thumb", thumb_h="120px",
        tp_url="https://au.trustpilot.com/review/applewatch.com"),
    dict(name="4. Garmin Vivoactive 6", badge_label="THE SPORTS ONE", has_star=False, tp_rating=1.5, tp_color="#FF8622",
        pros_cons=[(True,"Reliable GPS &amp; sports modes"),(True,"Accurate fitness tracking"),
            (True,"7-day battery"),(True,"Free garmin connect app"),
            (False,"£250 one-time investment"),(False,"Clunky app interface"),
            (False,"No blood pressure monitoring"),(False,"No onboard ECG or altimeter"),
            (False,"No speaker/mic for calls"),(False,"Bulky and uncomfortable for sleep")],
        score="7.5/10", btn_label="Visit Amazon",
        btn_href="https://www.amazon.com/Garmin-v%C3%ADvoactive%C2%AE-Fitness-Smartwatch-Display/dp/B0F38FCHD2?tag=techunboxed04-20",
        price_html='<span style="font-weight:800;font-size:20px;color:#16181C">£269</span>',
        sub_text="2–3 day Prime delivery", thumb_key="garmin_thumb", thumb_h="120px",
        tp_url="https://www.trustpilot.com/review/www.garmin.com"),
    dict(name="5. Fitbit Charge 6", badge_label="THE MAINSTREAM ONE", has_star=False, tp_rating=1.6, tp_color="#FF8622",
        pros_cons=[(True,"Onboard ECG &amp; SpO2"),(True,"Compact, lightweight band"),
            (True,"Built-in GPS + swimproof"),
            (False,"Privacy concerns after google acquisition"),
            (False,"Sleep score &amp; readiness behind £9.99/mo Premium"),
            (False,"Real battery only 2–5 days"),(False,"No blood pressure monitoring"),
            (False,"GPS was hit or miss"),(False,"Data loss in google migration")],
        score="5.9/10", btn_label="Visit Amazon",
        btn_href="https://www.amazon.com/Fitbit-Charge-Fitness-Tracker-Google/dp/B0CC62ZG1M?tag=techunboxed04-20",
        price_html='<span style="font-weight:800;font-size:20px;color:#16181C">£79.99</span>&nbsp;'
            '<span style="text-decoration:line-through;color:#4A4F57;font-size:14px">£139.99</span>',
        sub_text="2–3 day Prime delivery", thumb_key="fitbit_thumb", thumb_h="147px",
        tp_url="https://www.trustpilot.com/review/community.fitbit.com"),
]

rank_rows_built = []
for i, r in enumerate(RANK_ROWS):
    rr = dict(r)
    rr["is_last"] = (i == len(RANK_ROWS) - 1)
    rank_rows_built.append(rank_row(**rr))
    rank_rows_built.append(rank_row_mobile(**rr))

ranking_five = container(rank_rows_built,
    [{"prop":"width","value":"100%"},{"prop":"backgroundColor","value":WHITE},
     {"prop":"borderRadius","value":"14px"},{"prop":"borderStyle","value":"solid"},
     {"prop":"borderColor","value":BORDER},{"prop":"borderWidth","value":"1px"}])
kids.append(ranking_five)
kids.append(sp(28))

# ============================== WHY WE PICKED THE HLTH BAND ==================
kids.append(h2("Why We Picked The HLTH Band As The Winner"))
kids.append(sp(10))
kids.extend(figure(img_block("why_hlth_won", height="402px", mh="230px", border=True)))
kids.append(sp(10))
kids.append(para('The HLTH Band stands out for its simplicity and serious health credentials. It consistently '
    'matched devices costing <span style="font-weight:700">three to five times more</span>. Its multi-wavelength '
    'PPG sensor, a step up from the single-wavelength sensors in most budget bands, delivers continuous readings '
    'of blood pressure trends, heart rate, HRV, and resting heart rate around the clock.'))
kids.append(para('It\'s one of the only bands on the market offering <span style="font-weight:700">blood '
    'pressure trend tracking without a subscription</span>. The kind of long-term picture you can bring to your '
    'next check-up, free, every single day. And it tracks full sleep stages across a battery that lasted '
    '<span style="font-weight:700">27 days in our test</span>. That\'s 27 nights of uninterrupted sleep data the '
    'Apple Watch and Fitbit simply can\'t match with their nightly charging.'))
kids.append(para('Normally, this level of monitoring sits behind a £229-per-year membership or inside a '
    'smartwatch that dies every night. The HLTH Band is the exception. At <span style="font-weight:700">£79</span>, '
    'it\'s the most capable screen-free health tracker we tested this year.'))
kids.append(callout("It's one of the only bands at any price that tracks blood pressure trends without a "
    "subscription."))
kids.append(sp(16))

# ============================== CUFF / BLOOD PRESSURE TEST ====================
kids.append(h2("We Expected It To Crack Under Testing. It Didn't."))
kids.append(sp(10))
kids.extend(figure(img_block("cuff_test", height="402px", mh="230px", border=True)))
kids.append(sp(10))
kids.append(para('When we unboxed the HLTH Band, the first thing we noticed was the weight. At '
    '<span style="font-weight:700">18 grams</span>, it sits on your wrist like a rubber bracelet. The strap had '
    'a faint rubbery smell for the first day or two, which went away. After a week switching between the Apple '
    'Watch and Garmin, putting it back on felt like taking a weight off. I wore it on my left wrist the whole '
    'month, bicep strap for workouts.'))
kids.append(para('But comfort means nothing without consistency, so we tested the claim that matters most: '
    'blood pressure. Every cardiologist we consulted agreed that a single spot reading tells you almost '
    'nothing, because blood pressure moves constantly with stress, movement, food, and sleep. '
    '<span style="font-weight:700">Only an extended trend shows a real pattern.</span> So we ran resting '
    'comparisons against a medical-grade cuff, and the HLTH Band tracked within the recommended ±10 mmHg range, '
    'consistently, across multiple sessions.'))
kids.append(para("That matters because a cuff catches one moment. The HLTH Band reads all day, while you "
    "work, sleep, and recover. That continuous picture shows you patterns a single reading never can. No "
    "other device in our test offered continuous blood pressure trends at any price, except Whoop, locked "
    "behind their £359-per-year tier."))
kids.append(callout("Nearly a month on a single charge. Even with every sensor running all night, ours lasted "
    "27 days, then you plug it in and forget it again. A smartwatch, by contrast, dies every single night."))
kids.append(sp(16))

# ============================== THE APP ======================================
kids.append(h2("The App Actually Won Me Over"))
kids.append(sp(10))
kids.append(para("HLTH took a different route than the big brands here. Instead of making the app look as "
    "complicated as possible, it's built to be extremely easy to read. The band tracks heart rate, HRV, blood "
    "pressure, blood oxygen, sleep stages, stress, and workouts. All day, all night. But tracking is only "
    "half the job. The data has to be easy to read, and this is where the band quietly wins."))
kids.extend(figure(img_block("app_home", radius="10px", border=True, fit="contain")))
kids.append(sp(10))
kids.append(para("Open the app and the home screen shows everything at a glance. Steps up top. Then heart "
    "rate, sleep, blood pressure, blood oxygen, each in its own card with the latest number front and center. "
    "No menus to dig through. Checking it became the thing I did in the kettle queue every morning."))
kids.append(callout("Because it never needs a nightly charge, it's on your wrist for every night of sleep, "
    "data the Apple Watch simply can't capture while it's charging."))
kids.extend(figure(img_block("app_bp", radius="10px", border=True, fit="contain")))
kids.append(sp(10))
kids.append(text('Tap any card and it opens up. Here is the blood pressure view. A big reading at the top, '
    'then a full chart of how it moved across the day. Orange line for systolic, purple for diastolic. Every '
    'rise and dip, hour by hour, with a normal range underneath so you know what good looks like without '
    'Googling it. And every screen follows the same layout. Learn it once and you know the whole app.',
    size="18px", lh="29.7px", font=SERIF))
kids.extend(figure(img_block("app_sleep", radius="10px", border=True, fit="contain")))
kids.append(sp(10))
kids.append(text('Sleep was the one we checked most. It splits your night into light, deep, and REM, with '
    'total hours at the top. One glance tells you whether you rested or just lay there. The heart data goes '
    'deeper than a single number too. Resting and live heart rate on a full-day graph. Workouts split into '
    'five zones, though the workout type list is shorter than Garmin’s, worth knowing if you do anything '
    'niche. HRV overnight, the recovery signal most trackers skip. Blood oxygen as a simple percentage. All '
    'of it running in the background, no chest strap.', size="18px", lh="29.7px", font=SERIF))
kids.append(sp(16))

# ============================== BICEP STRAP ==================================
kids.append(h2("The Bicep Strap Is A Great Addition"))
kids.append(sp(10))
kids.extend(figure(img_block("bicep_strap", height="402px", mh="230px", border=True)))
kids.append(sp(10))
kids.append(para('Here\'s a simple rule about wrist wearables that the big brands don\'t talk about much: '
    '<span style="font-weight:700">the less the sensor moves, the steadier your readings.</span> Your wrist is '
    'the busiest joint you have. It twists, flexes, and swings with every step, and all that movement is noise '
    'the sensor has to fight through.'))
kids.append(para('Your bicep barely moves by comparison. That\'s what makes the included bicep strap such a '
    'smart addition. Clip the same band to your upper arm for a run or a workout and it sits steady against the '
    'muscle, which means <span style="font-weight:700">steadier readings when your body is working '
    'hardest</span>. We wore it on the wrist day to day and moved it to the bicep for training. Takes about ten '
    'seconds to swap.'))
kids.append(sp(16))

# ============================== COST COMPARISON ==============================
kids.append(h2("How Much Is This Actually Going To Cost You?"))
kids.append(sp(10))
kids.extend(figure(video_block(COST_VIDEO_URL, poster=IMG["cost_video_still"]["src"],
    height="402px", mh="230px", border=True),
    cap_text="(Video credit: Marcus Pendleton / TechUnboxed)"))
kids.append(sp(10))
kids.append(para("That depends entirely on which device you choose. It's worth doing the maths, because the "
    "sticker price is only half the story."))
kids.append(sp(10))

# 6-column true-2-year-cost table -- authored as raw HTML (see docstring: avoids
# native `overflow` 503-SSR gotcha for the mobile horizontal-scroll wrapper, and
# is far more tractable than 30+ nested Containers for a 6x5 grid).
COST_COLUMNS = ["WHOOP 5.0 PEAK", "APPLE WATCH SE 3", "FITBIT CHARGE 6", "GARMIN VIVOACTIVE 6", "HLTH BAND"]
COST_ROWS = [
    ("Year 1", ["£229", "£219", "£200", "£269", "£79"]),
    ("Year 2", ["£229", "£0", "£120", "£0", "£0"]),
    ("2-Year Total", ["£458", "£219", "£320", "£269", "£79"]),
    ("Subscription", ["Mandatory", "No", "Optional", "No", "No"]),
]
def _cost_table_html():
    # Measured column proportions (140 + 5x116 = 720px desktop): reproduced as
    # percentages on a table-layout:fixed table so 6 columns always fit the
    # 720px article column instead of overflowing (nowrap + auto-layout blew
    # this out past the viewport on the live page -- fixed after screenshot
    # verification caught it). Header/label text is allowed to wrap (matches
    # the design's own two-line product-name headers) rather than forcing
    # nowrap.
    #
    # Mobile (Figma node 60:2684, 390 frame) is NOT the same proportions
    # scaled down -- it's its own measured layout: label col 90/350=25.71%,
    # each data col 52/350=14.86% (vs desktop's 19.4%/16.12%), header font
    # 7.5px (vs desktop 11.5px), row-value font 11.5px (vs desktop 13.5px),
    # Subscription-row font 7.5px (text_10giquy/text_osxpuz, vs desktop's
    # 13.5px), header cell padding 8px 2px (vs desktop 8px 8px), data cell
    # padding 8px 6px. Applied via a scoped @media(max-width:767px) block
    # rather than shrinking the desktop sizes globally -- at the desktop
    # font sizes the 350px mobile column width mid-word-wraps device names
    # ("WHO/OP 5.0/PEAK"), confirmed live before this fix.
    pct_label, pct_col = 19.4, 16.12
    m_pct_label, m_pct_col = 25.71, 14.858
    cols_html = ('<col class="rc-ct-c0">') + \
        ("".join('<col class="rc-ct-c">' for _ in COST_COLUMNS))
    th = '<th class="rc-ct-th">DEVICE</th>'
    th += "".join('<th class="rc-ct-th">%s</th>' % c for c in COST_COLUMNS)
    body_rows = ""
    for label, vals in COST_ROWS:
        is_sub_row = (label == "Subscription")
        row_cls = " rc-ct-sub" if is_sub_row else ""
        tds = '<td class="rc-ct-label%s">%s</td>' % (row_cls, label)
        for i, v in enumerate(vals):
            is_hlth = (i == len(vals) - 1)
            cls = "rc-ct-val" + (" rc-ct-hlth" if is_hlth else "") + row_cls
            tds += '<td class="%s">%s</td>' % (cls, v)
        body_rows += "<tr>%s</tr>" % tds
    # Desktop measured directly from node 60:1735 (header row) and 60:1787
    # (Subscription row): header font 13.5px/18px, letter-spacing 0.4px,
    # padding 10px 12px, header row 74px tall (room for 3-line product
    # names like "GARMIN VIVOACTIVE 6"); ALL data rows (not just
    # Subscription) use 15.5px/22px with the same 10px/12px padding -- the
    # earlier version's 11.5-13.5px fonts with 8px flat padding were too
    # cramped/small relative to the actual design.
    style = '''<style>
    .rc-ct{border-collapse:collapse;width:100%%;table-layout:fixed;font-family:%(sans)s}
    .rc-ct-c0{width:%(pl).2f%%} .rc-ct-c{width:%(pc).2f%%}
    .rc-ct-th{background:#F7F8F6;font-size:13.5px;font-weight:700;letter-spacing:0.4px;color:#16181C;
        line-height:18px;text-align:left;padding:10px 12px;border:1px solid #E4E6E2;word-break:break-word}
    .rc-ct-label{font-size:15.5px;line-height:22px;font-weight:700;color:#16181C;padding:10px 12px;
        border:1px solid #E4E6E2;word-break:break-word}
    .rc-ct-val{font-size:15.5px;line-height:22px;font-weight:400;color:#16181C;padding:10px 12px;
        border:1px solid #E4E6E2;word-break:break-word}
    .rc-ct-val.rc-ct-hlth{background:#FBEEEC;font-weight:700}
    @media (max-width:767px){
        .rc-ct-c0{width:%(mpl).3f%%} .rc-ct-c{width:%(mpc).3f%%}
        .rc-ct-th{font-size:7.5px;line-height:10.5px;padding:8px 2px}
        .rc-ct-label,.rc-ct-val{font-size:11.5px;line-height:16px;padding:8px 6px}
        .rc-ct-label.rc-ct-sub,.rc-ct-val.rc-ct-sub{font-size:7.5px;line-height:11px}
    }
    </style>''' % {"sans": SANS, "pl": pct_label, "pc": pct_col, "mpl": m_pct_label, "mpc": m_pct_col}
    return ('%s<div style="width:100%%;overflow-x:auto">'
        '<table class="rc-ct"><colgroup>%s</colgroup><thead><tr>%s</tr></thead>'
        '<tbody>%s</tbody></table></div>'
        ) % (style, cols_html, th, body_rows)

cost_table = {"t":"HtmlElement","id":nid(),"p":{"content":_cost_table_html()},
    "styles":[{"prop":"width","value":"100%"}]}
kids.append(cost_table)
kids.append(sp(4))
kids.append(callout("£79, once. Over two years the Whoop costs £458, and it stops working the day "
    "you cancel."))
kids.append(sp(10))

kids.append(para('<span style="font-weight:700">So what are you giving up at £79?</span> Three things, honestly. '
    'There\'s <span style="font-weight:700">no screen</span>, you check everything in the app, which for us was '
    'a feature rather than a flaw. There\'s <span style="font-weight:700">no built-in GPS</span>, the band leans '
    'on your phone for route maps, so phone-free runners will miss it. And nobody at the pub will recognise the '
    'logo, because <span style="font-weight:700">HLTH is a young company</span>. If that\'s all right for you, '
    'the HLTH Band might just be your best pick.'))
kids.append(para('<span style="font-weight:700">Price check:</span> the £79 price is a launch sale, down from '
    '£158. We checked it on 1 July and again on 18 July 2026, and the discount was live both times. HLTH makes '
    'the band in small batches and earlier batches have sold out, so check current availability before this one '
    'goes.'))
kids.append(para('While it’s the least expensive device we tested, nothing about it felt cheap in use. The data '
    'it delivered over 30 days made most of the devices above it feel like overcomplicated answers to a simple '
    'question. And every HLTH Band comes with a <span style="font-weight:700">30-day money-back guarantee</span>, '
    'so there’s no real risk in finding out for yourself.'))
kids.append(container([button("Check HLTH Band Availability →", href=PDP, full=True,
    pad={"top":"13px","bottom":"13px","left":"20px","right":"20px"})], [{"prop":"width","value":"100%"}]))
kids.append(text('<a href="%s" target="_blank" style="color:#1A5FD0;text-decoration:underline">View the HLTH '
    'Band on the official site →</a>' % PDP, size="18px", lh="29.7px", align="center", font=SERIF))
kids.append(sp(16))

# ============================== COMMUNITY PROOF ==============================
kids.append(h2("What The Health Tracking Community Is Saying About The HLTH Band"))
kids.append(sp(10))
kids.append(para("We've given you our take. Here's what it looks like from the outside. First, the band on "
    "video, worn day and night rather than filmed in a studio:"))
kids.append(sp(6))

def video_embed_rc(youtube_embed_url, title="HLTH Band Video Review"):
    # Real embed (per request), built as a responsive 16:9 wrapper
    # (padding-top:56.25% + absolutely-positioned iframe) rather than a
    # fixed-pixel-height box -- a fixed height was what made the previous
    # placeholder overlay/collide with the paragraph below it on mobile.
    return {"t":"HtmlElement","id":nid(),"p":{"content":(
        '<div style="position:relative;width:100%%;padding-top:56.25%%;border-radius:12px;'
        'overflow:hidden;background:#000">'
        '<iframe src="%s" title="%s" loading="lazy" '
        'style="position:absolute;top:0;left:0;width:100%%;height:100%%;border:0" '
        'allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" '
        'allowfullscreen></iframe></div>'
    ) % (youtube_embed_url, title)}, "styles":[{"prop":"width","value":"100%"}]}

kids.append(video_embed_rc("https://www.youtube.com/embed/lMZoKLSmd6M"))
kids.append(sp(10))
kids.append(para("Then there's Trustpilot. It's one of the harder places for a brand to shape its own "
    "reputation, since Trustpilot runs fraud detection, verifies reviewers, and penalises companies caught "
    "manipulating their scores. Here's how the HLTH Band's reviews stack up:"))
kids.extend(figure(img_block("trustpilot_shot", height="252px", mh="180px", radius="8px", fit="contain"),
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
        text(tp_stars(5.0, 15), size="15px", lh="15px"), sp(3),
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
kids.append(sp(10))
kids.append(para("Read enough of them and the same things keep coming up. People love how light the band is, "
    "that the battery genuinely lasts weeks instead of days, and that everything lives in one simple app. The "
    "other theme is money: no subscription, no locked features, nothing to pay after the £79."))
kids.append(text('<a href="%s" target="_blank" style="color:#1A5FD0;text-decoration:underline">See more '
    'reviews on Trustpilot →</a>' % TP, size="18px", lh="29.7px", font=SERIF))
kids.append(sp(16))

# ============================== FAQ ==========================================
kids.append(h2("Your Questions, Answered"))
kids.append(sp(10))

# Figma node 60:2010 (desktop) and 60:2961 (mobile) both confirmed via a raw
# get_node read: each row is ONLY a bold question + a red "+" glyph, no answer
# text on either frame. Real answers supplied directly by the user (not on
# Figma, not invented) -- rendered as a native <details>/<summary> accordion
# so the "+" affordance is now genuinely functional instead of decorative.
FAQ_ITEMS = [
    ("Does the HLTH Band work with iPhone and Android?", [
        "Both. You need an iPhone 8 or newer, or an Android on 8.0 or newer. It connects over Bluetooth.",
        "The app is free on both stores. Setup took us about three minutes.",
        "There's no screen on the band, so your phone shows you everything. Open the app when you want your "
        "numbers. The rest of the time the band just quietly gets on with it.",
    ]),
    ("Is there really no subscription? What's the catch?", [
        "No subscription. You pay £79 once and everything is switched on. Blood pressure trends, HRV, sleep "
        "stages, blood oxygen. All of it.",
        "The catch isn't money. It's what the band doesn't do.",
        "There's no screen, so you check the app. There's no built-in GPS, so runs use your phone for the map. "
        "And it's a new brand, so nobody will know the logo.",
        "Compare that to Whoop. Stop paying and the hardware stops working. Blood pressure sits in their "
        "£359-a-year tier.",
    ]),
    ("How accurate is the blood pressure tracking?", [
        "Let's be straight about this one, because people get it wrong.",
        "The HLTH Band is a wellness device, not a medical one. It shows you trends across the day. It does not "
        "replace the cuff at your GP surgery.",
        "We compared it to a medical-grade cuff at rest. It stayed within the ±10 mmHg range every time we "
        "checked.",
        "Some owners find their readings sit a few points high or low compared to their cuff. That's normal for "
        "this kind of sensor. The trend still reads fine, and the trend is the useful bit.",
        "For steadier readings, wear it snug and keep it on the same wrist. Your non-dominant one works best.",
        "Want one exact number? Use a cuff. Want to see what your pressure does all day? This is the cheap way "
        "to find out.",
    ]),
    ("Can I shower or swim with it?", [
        "Yes. It's rated 1ATM. Showers, sweat, washing up, pool lengths. All fine.",
        "We showered in ours every day for a month. No problems.",
        "Just skip diving and pressure washers. Rinse it after a swim and dry the strap. Same as any band you "
        "wear all the time.",
    ]),
    ("How do I charge it, and how long does it take?", [
        "Clip on the charger and leave it about 90 minutes. Ten minutes gets you three days if you're rushing "
        "out the door.",
        "Then you forget about it for a month.",
        "That was the bit that got us. Ours ran 27 days with every sensor on, including blood oxygen overnight. "
        "So charging happened while the kettle boiled, not every night before bed.",
        "Which also means it's on your wrist for every night of sleep. Not sitting on a charger missing it.",
    ]),
    ("What if it doesn't work for me?", [
        "You've got 30 days. Send it back for a full refund, opened or not, no questions. Returns are free.",
        "You also get a one year warranty, and it's CE certified.",
        "So the worst case is you wear it for a month and decide it's not for you. Support is on "
        "info@hlthtrack.com, weekdays 8am to 5pm UK time. Readers tell us they hear back the same day.",
    ]),
    ("What comes in the box?", [
        "The sensor, two straps and a charging cable.",
        "One strap is soft knit for daytime and sleep. The other is silicone for workouts and water. It fits "
        "wrists up to about 24cm, so there's no sizing kit and no waiting two weeks to start.",
        "Swapping straps takes seconds.",
        "The bicep strap we trained in is sold separately at £14.95. Worth it if you run or lift. Easy to skip "
        "if you don't.",
    ]),
]

FAQ_STYLE = (
    '<style>'
    '.rc-faq{width:100%%;background:#FFFFFF;border:1px solid #E4E6E2;border-radius:10px;overflow:hidden}'
    '.rc-faq summary{cursor:pointer;list-style:none;padding:14px 16px;display:flex;align-items:center;'
    'justify-content:space-between;gap:12px;font-family:%s;font-size:16.5px;line-height:23px;font-weight:700;'
    'color:#16181C}'
    '.rc-faq summary::-webkit-details-marker{display:none}'
    '.rc-faq summary::marker{content:""}'
    '.rc-faq-icon{font-family:%s;font-size:22px;line-height:23px;color:#E63946;flex-shrink:0;'
    'transition:transform .2s;display:inline-block}'
    '.rc-faq[open] .rc-faq-icon{transform:rotate(45deg)}'
    '.rc-faq-a{padding:0 16px 16px;font-family:%s;font-size:15.5px;line-height:24px;color:#4A4F57}'
    '.rc-faq-a p{margin:0 0 10px}.rc-faq-a p:last-child{margin-bottom:0}'
    '</style>'
) % (SANS, SANS, SERIF)

def faq_row(q, answer_paras):
    body = "".join('<p>%s</p>' % p for p in answer_paras)
    html = (
        '<details class="rc-faq"><summary><span>%s</span><span class="rc-faq-icon">+</span></summary>'
        '<div class="rc-faq-a">%s</div></details>'
    ) % (q, body)
    return {"t":"HtmlElement","id":nid(),"p":{"content":html},"styles":[{"prop":"width","value":"100%"}]}

kids.append({"t":"HtmlElement","id":nid(),"p":{"content":FAQ_STYLE},"styles":[{"prop":"width","value":"100%"}]})
faq_rows = [faq_row(q, a) for q, a in FAQ_ITEMS]
kids.append(col(faq_rows, gap="10px"))
kids.append(sp(16))

FAQ_JSONLD = json.dumps({
    "@context": "https://schema.org", "@type": "FAQPage",
    "mainEntity": [{"@type": "Question", "name": q,
        "acceptedAnswer": {"@type": "Answer", "text": " ".join(a)}} for q, a in FAQ_ITEMS]
})
kids.append({"t":"HtmlElement","id":nid(),
    "p":{"content":'<script type="application/ld+json">%s</script>' % FAQ_JSONLD},
    "styles":[{"prop":"width","value":"100%"},{"prop":"lfDisplay","value":"none"}]})

# ============================== VERDICT ======================================
kids.append(h2("Our Verdict"))
kids.append(sp(10))
kids.extend(figure(img_block("closing_lifestyle", height="402px", mh="230px", border=True)))
kids.append(sp(10))
kids.append(para("If you're curious about your blood pressure and sleep, and tired of trackers that need "
    "charging every night or a subscription every year, the HLTH Band is an easy recommendation. It does the "
    "health tracking that actually matters, without the screen, the nightly charger, or the monthly fee."))
kids.append(text("The way I see it, a year from now you've either got twelve months of your own heart, sleep "
    "and pressure trends to look back on, or you're still guessing. For £79, once, that's not a hard "
    "call.", size="18px", lh="29.7px", font=SERIF))
kids.append(container([button("Check HLTH Band Availability →", href=PDP, full=True,
    pad={"top":"13px","bottom":"13px","left":"20px","right":"20px"})], [{"prop":"width","value":"100%"}]))
kids.append(sp(28))

# ============================== ENDMATTER ====================================
def em_h2(t_):
    return container([title(t_, "22px", "28px", weight="700", ls="-0.22px", font=SERIF)],
        [{"prop":"padding","value":{"top":"24px","bottom":"12px"}}])

endmatter_kids = [sp(24), em_h2("References")]
REFS = [
    ('Tang, M. S. S., Moore, K., McGavigan, A., Clark, R. A., &amp; Ganesan, A. N. (2020). '
     '<a href="https://pmc.ncbi.nlm.nih.gov/articles/PMC7407266/" target="_blank" '
     'style="color:#1A5FD0;text-decoration:underline">Effectiveness of Wearable Trackers on Physical Activity '
     'in Healthy Adults: Systematic Review and Meta-Analysis of Randomized Controlled Trials</a>. JMIR mHealth '
     'and uHealth, 8(7), e15576. https://doi.org/10.2196/15576'),
    ('van Helmond, N., Freeman, C. G., Hahnen, C., Haldar, N., Hamati, J. N., Bard, D. M., Murali, V., Merli, '
     'G. J., &amp; Joseph, J. I. (2019). <a href="https://pubmed.ncbi.nlm.nih.gov/31423912/" target="_blank" '
     'style="color:#1A5FD0;text-decoration:underline">The accuracy of blood pressure measurement by a '
     'smartwatch and a portable health device</a>. Hospital Practice (1995), 47(4), 211–215. '
     'https://doi.org/10.1080/21548331.2019.1656991'),
]
ref_rows = []
for i, ref in enumerate(REFS, start=1):
    ref_rows.append(rowf([
        container([text("%d." % i, size="13.5px", lh="21.6px", color=BODY, font=SERIF)],
            [{"prop":"width","value":"22px"},{"prop":"flexShrink","value":"0"}]),
        text(ref, size="13.5px", lh="21.6px", color=BODY, font=SERIF),
    ], gap="0px", align="flex-start"))
endmatter_kids.append(col(ref_rows, gap="12px"))

endmatter_kids.append(em_h2("Further Reading"))
# QA: the first two cards promised articles the blog does not publish -- "The Best
# Screen-Free Fitness Trackers of 2026" and "Oura vs Whoop" do not exist, so the
# labels could not be honoured by any href. Each card now names the article it
# actually opens. Card 2 is also repointed: "Smart Rings vs Smartwatches" is a real
# comparison and far closer to this page's subject than budget-vs-premium was.
FURTHER = [
    ("BUYING GUIDE", "First-Time Wearable Buying Guide",
        "https://blog.techunboxed.co/article/complete-wearable-buying-guide"),
    ("COMPARISON", "Smart Rings vs Smartwatches: Which Tracks Sleep Better?",
        "https://blog.techunboxed.co/article/smart-rings-vs-smartwatches-sleep-tracking"),
    ("EXPLAINER", "How Accurate Are Wrist-Based Blood Pressure Readings?",
        "https://blog.techunboxed.co/article/blood-pressure-monitors-at-home-vs-wearable"),
    ("EXPLAINER", "Do Fitness Trackers Actually Improve Your Health? What the Research Says",
        "https://blog.techunboxed.co/article/do-fitness-bands-improve-workout-results"),
]
FURTHER_STYLE = (
    '<style>'
    '.rc-further{display:flex;align-items:center;gap:14px;padding:14px 0;text-decoration:none;color:inherit;'
    'border-bottom:1px solid #E4E6E2}'
    '.rc-further-text{flex:1;min-width:0;display:flex;flex-direction:column;gap:3px}'
    '.rc-further-kicker{font-family:%s;font-size:11px;line-height:14px;font-weight:800;color:#E63946;'
    'letter-spacing:1.1px}'
    '.rc-further-headline{font-family:%s;font-size:16.5px;line-height:21.5px;font-weight:700;color:#16181C}'
    '.rc-further-arrow{flex-shrink:0;font-family:%s;font-size:20px;line-height:24px;color:#E63946}'
    '</style>'
) % (SANS, SANS, SANS)

def further_row(kicker, headline, href):
    html = (
        '<a class="rc-further" href="%s" target="_blank">'
        '<span class="rc-further-text"><span class="rc-further-kicker">%s</span>'
        '<span class="rc-further-headline">%s</span></span>'
        '<span class="rc-further-arrow">&#8594;</span></a>'
    ) % (href, kicker, headline)
    return {"t":"HtmlElement","id":nid(),"p":{"content":html},"styles":[{"prop":"width","value":"100%"}]}

endmatter_kids.append({"t":"HtmlElement","id":nid(),"p":{"content":FURTHER_STYLE},
    "styles":[{"prop":"width","value":"100%"}]})
further_rows = [further_row(kicker, headline, href) for kicker, headline, href in FURTHER]
endmatter_kids.append(col(further_rows, gap="0px",
    styles=[{"prop":"borderStyle","value":"solid"},{"prop":"borderColor","value":BORDER},
            {"prop":"borderWidth","value":"1px 0px 0px 0px"}]))

endmatter_kids.append(em_h2("About the Author"))
author_avatar = container([{"t":"Image","id":nid(),"p":{"src_id":IMG["avatar_author"]["src_id"],
    "src_uid":IMG["avatar_author"]["src_uid"],"src":IMG["avatar_author"]["src"]},
    "styles":[{"prop":"width","value":"78px"},{"prop":"height","value":"78px"},
              {"prop":"borderRadius","value":"50%"},{"prop":"objectFit","value":"cover"}]}],
    [{"prop":"width","value":"78px"},{"prop":"flexShrink","value":"0"}])
author_box = rowf([author_avatar, col([
    text("Marcus Pendleton", size="18px", lh="24px", color=DARK, weight="700", font=SERIF), sp(2),
    text("Principal Writer, Wearables — TechUnboxed", size="13.5px", lh="18px", color=BODY, font=SANS), sp(10),
    text("Marcus has spent six years testing wearables for TechUnboxed, more than 40 devices across "
         "smartwatches, rings and screen-free bands. He wears an Oura Ring daily and rotates test devices on "
         "his other wrist, and after a family history of high blood pressure he pays close attention to how "
         "everyday trackers handle heart and cardiovascular data.", size="14.5px", lh="22.5px", color=DARK, font=SANS), sp(8),
    text("Before TechUnboxed he spent a decade in consumer electronics retail. He tests every device himself, "
         "day and night, for at least 30 days before writing about it.", size="13px", lh="20px", color=BODY, font=SANS),
], gap="0px", styles=[{"prop":"flex","value":"1"},{"prop":"minWidth","value":"0"}])],
    gap="18px", align="flex-start",
    styles=[{"prop":"backgroundColor","value":TABLEBG},{"prop":"borderStyle","value":"solid"},
        {"prop":"borderColor","value":BORDER},{"prop":"borderWidth","value":"1px"},
        {"prop":"borderRadius","value":"14px"},
        {"prop":"padding","value":{"top":"20px","bottom":"20px","left":"20px","right":"20px"}},
        {"prop":"flexDirection","value":"column","media":767}])
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

# ============================== FOOTER LEGAL (reused verbatim, see docstring 2) ==
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
TITLE = "We Spent £1,581 Testing The Top 5 Fitness Trackers of 2026. The £79 Outsider Won."
OG = json.load(open("pagescore/.cache/og_img_map.json"))  # QA: purpose-cut 1200x630 share images
SEO = {
    "title": "Top 5 Fitness Trackers of 2026, Ranked & Tested",
    "description": "We spent £1,581 testing 5 fitness trackers -- Whoop, Apple, Garmin, Fitbit and HLTH. "
        "See why the £79 screen-free option came out on top.",
    "keywords": "fitness tracker, best fitness tracker 2026, fitness tracker ranked, HLTH Band, "
        "Whoop vs Apple Watch, screen-free fitness tracker, blood pressure tracker, wearable comparison",
    "social_image_uid": OG["top5"]["src_uid"],
}

# QA: settings.seo emits og:* only, so X/Twitter had no card on any of the eleven pages.
# Append explicit twitter:* tags to the header custom_html, from the same SEO values.
def _esc(v): return v.replace("&","&amp;").replace('"',"&quot;").replace("<","&lt;").replace(">","&gt;")
CUSTOM_HTML = {"header": PERF + (
    '<meta name="twitter:card" content="summary_large_image">\n'
    '<meta name="twitter:title" content="%s">\n'
    '<meta name="twitter:description" content="%s">\n'
    '<meta name="twitter:image" content="%s">\n'
    ) % (_esc(SEO["title"]), _esc(SEO["description"]), OG["top5"]["src"]),
    "footer": PERF_FOOTER}

# ---------------- write: create the step if new, else update its body in place ----------------
existing = sgql('query($q: String!){ funnels(first:1,query:$q){ edges { node { id starting_step_id steps { id uid slug title type settings visual { x y } } } } } }',
    {"q": f"id:{FUNNEL}"})["funnels"]["edges"][0]["node"]
existing_steps = existing["steps"]
collide = next((s for s in existing_steps if s["slug"] == STEP_SLUG), None)

if collide:
    # Redeploy path: step already exists (e.g. re-running after a content fix).
    # Update its body in place, leave the other steps' settings/visual/body untouched.
    other_steps = [{"id": s["id"], "slug": s["slug"], "title": s["title"], "type": s["type"],
                    "settings": s["settings"], "visual": s["visual"]}
                   for s in existing_steps if s["slug"] != STEP_SLUG]
    new_steps_list = other_steps + [{"id": collide["id"], "slug": STEP_SLUG, "title": TITLE, "type": "article_page",
        "settings": {"custom_html": CUSTOM_HTML, "seo": SEO}, "visual": collide["visual"], "body": body}]
    print("redeploying existing step ->", collide["id"])
else:
    create_r = sgql('''mutation($fid: ID!, $node: InputStep!){ createStep(funnel_id:$fid, node:$node){ step { id uid } } }''',
        {"fid": FUNNEL, "node": {"slug": STEP_SLUG, "title": TITLE, "type": "article_page",
            "settings": {"custom_html": CUSTOM_HTML, "seo": SEO}, "visual": {"x": 1090, "y": 90}, "body": body}})
    NEW_STEP_ID = create_r["createStep"]["step"]["id"]
    print("created detached step ->", create_r["createStep"]["step"])
    # Attach: keep starting_step_id untouched, keep all 3 existing steps untouched
    # (send them back as-is per updateFunnel's "only updates steps that already
    # exist, matched by id" semantics -- new step's own createStep already wrote
    # its full body, so we don't need to resend it here, just add it to the list)
    new_steps_list = [{"id": s["id"], "slug": s["slug"], "title": s["title"], "type": s["type"]} for s in existing_steps]
    new_steps_list.append({"id": NEW_STEP_ID, "slug": STEP_SLUG, "title": TITLE, "type": "article_page",
        "settings": {"custom_html": CUSTOM_HTML, "seo": SEO}, "visual": {"x": 1090, "y": 90}, "body": body})

r2 = sgql('''mutation($id: ID!, $node: InputFunnel!){ updateFunnel(id:$id,node:$node){ id starting_step_id published steps { uid slug title } } }''',
    {"id": FUNNEL, "node": {"published": True, "steps": new_steps_list}})
print("WROTE", json.dumps(r2["updateFunnel"], indent=2))
