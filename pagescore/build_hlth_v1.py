#!/usr/bin/env python3
"""Oura Ring 4 vs HLTH Band advertorial, V1 (Figma node 12:3, "Oura vs HLTH ·
TechUnboxed V1 · 1440"). This is a from-scratch, high-performance rebuild of
the ORIGINAL V1 design -- a different design generation from build_hlth_v2.py
/ build_hlth_v3.py (which are V2/V3 redesigns). Requested because another,
separately-built copy of this V1 design exists in the account without this
codebase's performance work (Gelasio/Inter font-preload + CLS fix, hero
image srcset preload, SSR-safe styling).

Content/copy source: pb/0 (step oura-vs-hlth-band-final16 / slug
oura-vs-hlth), the live step already carrying this exact V1 design -- its
body was read directly via GraphQL and every TEXT node's `characters` copied
verbatim (not paraphrased) into this file. Images matched by role/src_id to
that same step (see pagescore/.cache/hlth_v3_img_map.json, already aligned
to pb/0 from an earlier task in this session).

Styling (colors/fonts/spacing/table/chart structure) is being cross-checked
against Figma node 12:3 directly -- see the section-level comments below for
what's measured vs carried over from the V2/V3 helper library (same brand
system: same color tokens, same SSR-safe helper functions).

Genuinely different from V2/V3 (confirmed from pb/0's raw body, not assumed):
- Ranking card's "Pros & Cons" are an ALWAYS-VISIBLE two-column checklist
  (green check / red cross bullets), not a collapsible accordion.
- Price section is a "CUMULATIVE COST OF OWNERSHIP" chart with an explicit
  YEAR 1 / YEAR 2 / YEAR 3 row structure, not V3's two-column stacked bars.
- Byline/H1/tag row copy is V1's own (different headline, standfirst, and
  breadcrumb final crumb than V2 or V3).

Typography / SSR gotchas: identical to V2/V3. No `overflow`, native
`boxShadow`, `maxWidth:"none"`, or `alignItems:"baseline"` anywhere (503s the
LF SSR renderer).

This file both ASSEMBLES the body and WRITES it: the target step (slug
oura-vs-hlth-band-version-1, funnel fun_hLmlmrbjeoGf3UZZvBEHY) was created
via createStep + updateFunnel, unlinked from starting_step_id, funnel stays
published. This script overwrites its body via updateFunnel, matching the
idempotent pattern used by every build_hlth_*.py in this codebase.
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
STEP_SLUG = "oura-vs-hlth-band-version-1"
IMG = json.load(open("pagescore/.cache/hlth_v3_img_map.json"))

PDP = "https://hlthtrack.co.uk/products/wearable-hlth-band"  # QA: one canonical storefront domain
TP  = "https://www.trustpilot.com/review/hlthtrack.com"
# QA 21 Aug: Oura restructured their URLs -- /en-us/product/... now redirects to
# /en-us/store/... which 404s. /store/rings/oura-ring-4 is live (200) and is the
# same URL this page already cites for the published specifications.
OURA_URL = "https://ouraring.com/store/rings/oura-ring-4"

# ---- fonts (identical to V2/V3) ----
SERIF = "GelasioText, Georgia, serif"
SANS  = "Inter, InterFallback, sans-serif"

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

# ---- colors (identical set to V2/V3; same brand system) ----
DARK   = {"r":22,"g":24,"b":28,"a":1}    # #16181C main text
BODY   = {"r":74,"g":79,"b":87,"a":1}    # #4A4F57 secondary text
MUTED  = {"r":154,"g":160,"b":168,"a":1} # #9AA0A8 dateline
BORDER = {"r":228,"g":230,"b":226,"a":1} # #E4E6E2
HARD_SHADOW = {"r":201,"g":204,"b":210,"a":1} # #C9CCD2 flat offset "shadow"
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
HEADER_BG   = {"r":40,"g":40,"b":43,"a":1}    # #28282B (bound Figma variable, same on V1)
GREEN_CHECK = {"r":22,"g":163,"b":74,"a":1}   # #16A34A pros checkmark
RED_CROSS   = {"r":220,"g":38,"b":38,"a":1}   # #DC2626 cons cross

# ---- helpers (verbatim from V2/V3) ----
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

def sp(px):
    return container([], [{"prop":"width","value":"100%"},{"prop":"height","value":"%dpx"%px},
        {"prop":"lfDisplay","value":"block"}])

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

def logo_img(w="140px", h="35px"):
    m=IMG["logo"]
    return {"t":"Image","id":nid(),"p":{"title":"logo","src":m["src"]},
        "styles":[{"prop":"width","value":w},{"prop":"height","value":h},{"prop":"maxWidth","value":"100%"},
                  {"prop":"objectFit","value":"contain"},{"prop":"lfDisplay","value":"block"}]}

def button(label, href=PDP, bg=RED, fg=WHITE, full=False, size="15px", weight="700", radius="10px", ls=None,
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
def tp_stars(rating, color, box=19, radius=None, gap=2.2):
    # V1 (pb/0) uses radius=3 / gap=2.2 (measured from its raw body HTML,
    # `border-radius:3px`, `gap:2.2px`) -- a rounder tile + tighter gap than
    # V2/V3's later-measured 2.375/3.1667. Kept distinct via params, not
    # silently unified, since this file matches V1 exactly.
    fs = 12
    radius = radius if radius is not None else 3
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

def winline_plain(label):
    # V1's Figma spec (12:3) authors 2 of the 8 Winlines -- after Heart Tracking
    # (->HLTH Band) and Sleep Tracking (->Oura Ring 4) -- as solid-red with no
    # link. Every winline now links through to the winning product's own PDP,
    # matching the other 6 instances, so the product name is clickable everywhere.
    href = PDP if "HLTH" in label else OURA_URL
    return text('<span style="color:#E63946">Winner: </span>'
                 '<a href="%s" target="_blank" style="color:#1A5FD0;text-decoration:underline">%s</a>' % (href, label),
                 size="18px", lh="30px", weight="700", font=SERIF)

def h2(content, mt=0):
    return title(content, "28px", "35px", weight="700", color=DARK, ls="-0.28px", mt=mt, font=SERIF,
                 m={"fontSize":"22px","lineHeight":"27.5px","letterSpacing":"-0.22px"})

def figure(image_node, cap=True, gap=None):
    image_nodes = image_node if isinstance(image_node, list) else [image_node]
    if cap and gap:
        return [col(image_nodes + [caption()], gap=gap)]
    kids_ = list(image_nodes)
    if cap: kids_.append(caption())
    return kids_

# ============================== HEADER ===================================
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
         "children":[container([logo_img(w="166px", h="42px")],[{"prop":"lfDisplay","value":"flex"},
             {"prop":"justifyContent","value":"center"},{"prop":"width","value":"100%"}])]}}

BREADCRUMB_V1 = ('<span style="color:#16181C">Home</span> <span style="color:#B9BDC4">&gt;</span> '
    '<span style="color:#16181C">Wearables</span> <span style="color:#B9BDC4">&gt;</span> '
    '<span style="color:#E63946;font-weight:600">Oura Ring 4 vs HLTH Band</span>')

header_site_bar = {"t":"Section","id":nid(),
    "styles":[{"prop":"borderStyle","value":"solid"},{"prop":"borderColor","value":BORDER},
              {"prop":"borderWidth","value":"0px 0px 1px 0px"},
              {"prop":"padding","value":{"top":"14px","bottom":"14px"}},
              {"prop":"padding","value":{"left":"20px","right":"20px"},"media":767}],
    "p":{"layout":"boxed","dividerPosition":["top"],"horizontalFlip":False,
         "embedded_video":{"src":"","video_size":"stretch","video_position":"center"},
         "children":[text(BREADCRUMB_V1, size="13px", lh="18px", font=SANS)]}}

# ============================== ARTICLE HEAD ==============================
kids=[]
kids.append(title("Oura Ring 4 vs HLTH Band: Which Is Better For Health Tracking?",
    "40px","46px", weight="700", ls="-0.4px", font=SERIF, level="1",
    m={"fontSize":"28px","lineHeight":"32px","letterSpacing":"-0.28px"}))
kids.append(text("One costs £349 plus £5.99 a month. The other costs £79 once. We wore both for a month, "
    "nine rounds, and the famous ring wins exactly one of them.",
    size="20px", lh="30px", color=BODY, font=SERIF))

# tag row
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

# byline strip
byline_who = col([
    text('<span style="text-decoration:underline">Marcus Pendleton</span>',
         size="15.5px", lh="20px", color=DARK, weight="800", font=SANS),
    text("Principal Writer", size="13.5px", lh="18px", color=BODY, font=SANS),
], gap="2px", styles=[{"prop":"width","value":"150px"},{"prop":"flexShrink","value":"0"}])
byline_bio = col([
    text('<span style="color:#4A4F57">Marcus is a lead writer at TechUnboxed, reviewing and testing the latest '
         'smartwatches and fitness trackers. </span><b style="color:#16181C;text-decoration:underline">Read full bio</b>',
         size="14.5px", lh="22px", font=SANS),
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

# hero
kids.extend(figure(img_block("hero", height="403px", mh="196px", border=True)))
kids.append(sp(10))

kids.append(title("I'll say this upfront: I've worn an Oura Ring every day for two years, and I love the thing.",
    "18px","30px", weight="700", font=SERIF))
kids.append(text('<span style="color:#16181C">Then the </span>'
    '<a href="%s" target="_blank" style="color:#1A5FD0;text-decoration:underline">HLTH Band</a>' % PDP +
    '<span style="color:#16181C"> went absolutely viral this summer and flooded my inbox with one question: do '
    'I really need the £349 ring, or does the £79 band do the job? I wanted to wave it off. But the maths '
    'stopped me. By year three, the ring costs about £560. The band costs £79, once. Seven times the price. '
    "I'd been recommending it without ever checking.</span>", font=SERIF))
kids.append(para("One way to find out. A month with both, ring on my right hand, band on my left wrist. Same "
    "days, same workouts, same nights. Some rounds weren't close. One went the way you'd never guess from the "
    "prices. Here's the whole month, round by round."))
kids.append(sp(10))

# ============================== SHOP GRID ===================================
def shop_button(label, href):
    lab={"t":"Text","id":nid(),"p":{"content":label},
        "styles":[{"prop":"fontFamily","value":SANS},{"prop":"color","value":WHITE},
            {"prop":"fontSize","value":"15px"},{"prop":"fontWeight","value":"600"},
            {"prop":"lineHeight","value":"20px"},{"prop":"textAlign","value":"center"}]}
    btn = {"t":"BlockLink","id":nid(),"p":{"destination":{"type":"static","value":href},"target":"_blank",
        "widthOption":"auto","children":[container([lab],[{"prop":"lfDisplay","value":"flex"},
            {"prop":"alignItems","value":"center"},{"prop":"justifyContent","value":"center"}])]},
        "styles":[{"prop":"backgroundColor","value":DARK},
            {"prop":"padding","value":{"top":"12px","bottom":"12px","left":"12px","right":"12px"}},
            {"prop":"lfDisplay","value":"flex"},{"prop":"alignItems","value":"center"},
            {"prop":"justifyContent","value":"center"},{"prop":"width","value":"100%"}]}
    return container([btn], [{"prop":"backgroundColor","value":HARD_SHADOW},
        {"prop":"padding","value":{"right":"3px","bottom":"3px"}},{"prop":"width","value":"100%"}])

# Both cards (measured directly from pb/0's live body): flat 12px gap between
# image / [brand+name block] / price-row / button -- a simpler rhythm than
# V3's per-card explicit spacer breakdown.
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

# ============================== TABLE: AT A GLANCE ==========================
def cell(content, w, bold=False, color=DARK, bg=None, header=False, align="left"):
    st=[{"prop":"flex","value":str(w)},{"prop":"minWidth","value":"0"},
        {"prop":"padding","value":{"top":"10px","bottom":"10px","left":"12px","right":"10px"}},
        {"prop":"padding","value":{"top":"8px","bottom":"8px","left":"8px","right":"6px"},"media":767},
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
    ("Blood pressure trends", "No", "Day &amp; night", "hlth"),
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
kids.append(container(aag_rows, [{"prop":"width","value":"100%"},{"prop":"borderRadius","value":"6px"},
    {"prop":"borderStyle","value":"solid"},{"prop":"borderColor","value":BORDER},
    {"prop":"borderWidth","value":"1px 0px 0px 1px"}]))
kids.append(sp(6))

# ============================== RANKING · EDITOR'S PICK =====================
# V1's checklist is an ALWAYS-VISIBLE two-column check/cross list in the raw
# Figma design (node 12:3) -- but pb/0's actual shipped body has it wired as
# a broken accordion (a decorative, non-functional chevron with the checklist
# hardcoded lfDisplay:none and no onclick handler anywhere: verified by
# reading pb/0's raw body JSON directly, and confirmed visually via a live
# screenshot -- "Pros & Cons ⌄" renders but clicking it does nothing, the
# checklist is permanently unreachable). Rebuilt here as a WORKING accordion
# using this codebase's already-proven accordion_block() pattern (V3), which
# fixes that bug rather than reproducing it, while keeping V1's own
# checkmark/cross bullet style (not V3's plain <li> pros/cons list).
PROS = ["No subscription or locked features", "Confirmed 30-day battery life",
        "Tracks blood pressure trends, RHR, HRV &amp; SpO2", "Full sleep stages (deep, REM, light)",
        "Lightweight 18g, screen-free design", "No sizing kit – it's a band, it fits"]
CONS = ["New Company – Frequently sold out", "No built-in GPS (uses your phone)"]

def checklist_accordion():
    pros_html = "".join('<div style="margin-bottom:4px">'
        '<span style="color:#16A34A;font-weight:700">&#10003;</span>&nbsp;%s</div>' % p for p in PROS)
    cons_html = "".join('<div style="margin-bottom:4px">'
        '<span style="color:#DC2626;font-weight:700">&#10007;</span>&nbsp;%s</div>' % c for c in CONS)
    body = ('<div style="display:none;padding-top:10px" class="hlth-acc-body">'
        '<div style="display:flex;gap:18px;flex-wrap:wrap;font-family:%s;font-size:13px;line-height:19px;color:#16181C">'
        '<div style="flex:1;min-width:140px"><b style="color:#16181C">Pros</b>'
        '<div style="margin-top:6px;color:#4A4F57">%s</div></div>'
        '<div style="flex:1;min-width:140px"><b style="color:#16181C">Cons</b>'
        '<div style="margin-top:6px;color:#4A4F57">%s</div></div>'
        '</div></div>') % (SANS, pros_html, cons_html)
    summary = ('<div onclick="var b=this.nextElementSibling;b.style.display=b.style.display===\'none\'?\'block\':\'none\';'
        'var c=this.querySelector(\'.hlth-chev\');c.style.transform=b.style.display===\'none\'?\'rotate(0deg)\':\'rotate(180deg)\';" '
        'style="display:flex;align-items:center;gap:0;cursor:pointer;width:fit-content;font-family:%s;font-size:13px;font-weight:600;color:#4A4F57">'
        'Pros &amp; Cons <svg class="hlth-chev" width="10" height="10" viewBox="0 0 10 10" fill="none" '
        'stroke="#E63946" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" '
        'style="margin-left:8px;transition:transform .2s"><polyline points="1 3 5 7 9 3"/></svg></div>') % SANS
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
             tp_stars(4.6, "#00B67A") + '&nbsp;&nbsp;<span style="color:#16181C;font-weight:800;font-size:15px">4.6</span>'
             '&nbsp;' + ext_link_icon() + '</a>',
             size="15px", lh="19px", font=SANS),
    ], gap="8px", align="center", styles=[{"prop":"width","value":"fit-content"}])
    main = col([
        badge,
        text("HLTH Band 1.0", size="21px", lh="26px", color=DARK, weight="700", font=SANS),
        tprow,
        checklist_accordion(),
    ], gap="6px", styles=[{"prop":"flex","value":"1"},{"prop":"minWidth","value":"0"}])
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

def rank_card_mobile(img_key="hlth_product_rank"):
    badge = text('<span style="color:#F5B301;font-size:15px">★</span>&nbsp;<span style="color:#16181C;font-weight:800;letter-spacing:1.2px">EDITOR\'S PICK</span>',
                 size="12px", lh="16px", align="center", font=SANS)
    name = text("HLTH Band 1.0", size="21px", lh="26px", color=DARK, weight="700", align="center", font=SANS)
    img = img_block(img_key, height="240px", radius="8px", fit="contain")
    tprow = text('<a href="%s" target="_blank" style="text-decoration:none;color:inherit">' % TP +
                 tp_stars(4.6, "#00B67A") + '&nbsp;&nbsp;<span style="color:#16181C;font-weight:800;font-size:15px">4.6</span>'
                 '&nbsp;' + ext_link_icon() + '</a>',
                 size="15px", lh="19px", align="center", font=SANS)
    price_row = text('<span style="font-weight:800;font-size:20px;color:#16181C">£79</span>&nbsp;&nbsp;'
                      '<span style="text-decoration:line-through;color:#4A4F57;font-size:14px">£158</span>',
                 size="20px", lh="26px", align="center", font=SANS)
    buy_block = col([
        container([], [{"prop":"width","value":"100%"},{"prop":"height","value":"1px"},{"prop":"backgroundColor","value":BORDER}]),
        sp(16),
        button("View at HLTH", href=PDP, full=True, size="15px", weight="700", radius="10px", ls="0.3px"), sp(10),
        price_row, sp(3),
        text("Free UK shipping", size="12.5px", lh="17px", color=BODY, align="center", font=SANS),
    ], gap="0px", styles=[{"prop":"alignItems","value":"center"}])
    inner = [badge, sp(4), name, sp(20), img, sp(14), tprow, sp(10), checklist_accordion(), sp(32), buy_block]
    st=[{"prop":"lfDisplay","value":"none"},{"prop":"lfDisplay","value":"flex","media":767},
        {"prop":"flexDirection","value":"column"},{"prop":"gap","value":"0px"},
        {"prop":"alignItems","value":"center"},{"prop":"width","value":"100%"},
        {"prop":"backgroundColor","value":WHITE},{"prop":"borderRadius","value":"14px"},
        {"prop":"borderStyle","value":"solid"},{"prop":"borderColor","value":BORDER},
        {"prop":"borderWidth","value":"1px"},
        {"prop":"padding","value":{"top":"20px","bottom":"20px","left":"20px","right":"20px"}}]
    return {"t":"Container","id":nid(),"styles":st,"p":{"children":inner}}

def rank_card():
    return [rank_card_desktop(), rank_card_mobile()]

kids.extend(rank_card())
kids.append(sp(28))

# ============================== THE REAL PROBLEM ============================
kids.append(h2("The Real Problem With Smart Rings"))
kids.append(sp(10))

citation_header = rowf([
    inline_text("SOURCE DOCUMENT", size="11.5px", lh="15px", color=DARK, weight="800", font=SANS, ls="0.8px",
         m={"fontSize":"10.5px","lineHeight":"14px","letterSpacing":"0.7px"}),
    container([], [{"prop":"flex","value":"1"},{"prop":"height","value":"1px"}]),
    inline_text('<a href="https://support.ouraring.com" target="_blank" style="color:#4A4F57;text-decoration:none">'
         "support.ouraring.com&nbsp;&nbsp;" + ext_link_icon(size=12, stroke_w=1.1) + "</a>",
         size="12.5px", lh="15px", color=BODY, font=SANS, m={"fontSize":"11px","lineHeight":"14px"}),
], gap="12px", align="center", styles=[{"prop":"backgroundColor","value":TABLEBG},
    {"prop":"borderStyle","value":"solid"},{"prop":"borderColor","value":BORDER},
    {"prop":"borderWidth","value":"0px 0px 1px 0px"},
    {"prop":"padding","value":{"top":"13px","bottom":"13px","left":"18px","right":"18px"}}])
_CITE_META_M = {"fontSize":"11.5px","lineHeight":"17px"}
citation_meta = col([
    text('<span style="color:#4A4F57">article:</span> <span style="color:#16181C">"Heart Rate Graph"</span>', size="13px", lh="20px", font=SANS, m=_CITE_META_M),
    text('<span style="color:#4A4F57">section:</span> <span style="color:#16181C">Daytime Heart Rate Measurement</span>', size="13px", lh="20px", font=SANS, m=_CITE_META_M),
    text('<span style="color:#4A4F57">publisher:</span> <span style="color:#16181C">Oura Health Oy · Member Care</span>', size="13px", lh="20px", font=SANS, m=_CITE_META_M),
    text('<span style="color:#4A4F57">accessed:</span> <span style="color:#16181C">13 August 2026</span>', size="13px", lh="20px", font=SANS, m=_CITE_META_M),
    text('<span style="color:#4A4F57">url:</span> <span style="color:#16181C">support.ouraring.com/hc/en-us/articles/4410656562579</span>', size="13px", lh="20px", font=SANS, m=_CITE_META_M),
], gap="3px", styles=[{"prop":"padding","value":{"top":"16px","bottom":"14px","left":"18px","right":"18px"}}])
citation_passage = col([
    text("Oura takes measurements of your daytime heart rate for one full minute, every five minutes, using "
         "the Oura Ring's green LEDs.", size="14.5px", lh="23px", color=BODY, font=SANS,
         m={"fontSize":"13.5px","lineHeight":"21px"}),
    container([text('To preserve battery and maximize accuracy, a daytime heart rate measurement is only taken '
        'under optimal conditions, which include low movement and balanced average body temperature. Due to '
        'prioritizing these conditions, you may not receive an automatically updated heart rate for up to 30 '
        'minutes, but it can be manually updated at any time by using Live Heart Rate.',
        size="14.5px", lh="23px", color=DARK, font=SANS, m={"fontSize":"13.5px","lineHeight":"21px"})],
        [{"prop":"backgroundColor","value":HILITE_YEL},{"prop":"borderRadius","value":"2px"},
         {"prop":"padding","value":{"top":"3px","bottom":"3px","left":"5px","right":"5px"}},
         {"prop":"margin","value":{"top":"4px"}}]),
], gap="0px", styles=[{"prop":"padding","value":{"left":"18px","right":"18px","bottom":"18px"}}])
citation_card = container([citation_header, citation_meta, citation_passage],
    [{"prop":"width","value":"100%"},{"prop":"backgroundColor","value":WHITE},
     {"prop":"borderRadius","value":"12px"},{"prop":"borderStyle","value":"solid"},
     {"prop":"borderColor","value":BORDER},{"prop":"borderWidth","value":"1px"}])
kids.append(citation_card)
kids.append(caption("Oura Member Care, “Heart Rate Graph”, accessed 13 August 2026. Highlight added."))
kids.append(sp(10))

kids.append(para("Let's get one thing straight first, because it matters for fairness. When the Oura Ring "
    "takes a reading, it reads well. This round isn't about accuracy. It's about how often it reads, and here "
    "the ring's own documentation does the talking."))
kids.append(para('Oura’s support pages explain that a daytime heart rate measurement is only taken '
    '"under optimal conditions" to "preserve battery," and that you "may not receive an '
    'automatically updated heart rate for up to 30 minutes." The same docs note you can turn Activity heart '
    'rate off entirely in Settings, and that an activity "must last at least 10 minutes to be automatically '
    'detected," with the ring holding "at least five percent battery." None of this is bad '
    'engineering. It’s the only way a battery that small survives the week.'))
kids.append(para("The band never has to make that choice. A reading every five minutes, 288 a day, no "
    "conditions, no off-switches, no battery floor. Health tracking only works as an unbroken line, and every "
    "gap resets what your trends can tell you."))
kids.append(winline_hlth())
kids.append(sp(28))

# ============================== BATTERY LIFE ================================
kids.append(h2("Battery Life: The Physics Behind The Gaps"))
kids.append(para("Everything above has one cause. Teardowns put the Oura Ring 4's battery at roughly 15 to 22 "
    "mAh depending on size, smaller than a hearing aid's, and the newest ring went smaller still. The band "
    "class runs on cells around ten times larger or more. That single number explains the rationing."))
kids.append(sp(4))

def bar_row(label, value, pct, color):
    bhead = rowf([
        inline_text(label, size="15px", lh="20px", color=DARK, weight="700", font=SANS),
        container([], [{"prop":"flex","value":"1"}]),
        inline_text(value, size="13.5px", lh="20px", color=BODY, align="right", font=SANS),
    ], gap="12px", align="center")
    btrack = container([container([], [{"prop":"width","value":"%d%%"%pct},{"prop":"height","value":"14px"},
        {"prop":"borderRadius","value":"999px"},{"prop":"backgroundColor","value":color}])],
        [{"prop":"width","value":"100%"},{"prop":"height","value":"14px"},
         {"prop":"borderRadius","value":"999px"},{"prop":"backgroundColor","value":CHART_TRACK}])
    return col([bhead, sp(6), btrack], gap="0px")

battery_chart = col([
    bar_row("HLTH Band", "~30 days per charge", 100, RED),
    bar_row("Oura Ring 4 (rated)", "5–8 days", 27, CHART_GRAY),
    bar_row("Oura Ring 4 (owner-reported)", "~4–7 days, shrinking with age", 23, CHART_GRAY),
], gap="18px", styles=[{"prop":"width","value":"100%"},{"prop":"margin","value":{"top":"6px"}}])
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

# ============================== HEART TRACKING ===============================
# Spacer + image sizing matched to V2's exact measured implementation (Figma
# node 12:1868 area): a two-value spacer (33px desktop / 29px mobile, not a
# flat sp()) before the figure, and the image itself at height=401/mh=195
# (V2's measured values, not V1's earlier 403/230 guess).
kids.append(h2("Heart Tracking: The Open Lane"))
kids.append(container([], [{"prop":"width","value":"100%"},{"prop":"height","value":"33px"},
    {"prop":"height","value":"29px","media":767},{"prop":"lfDisplay","value":"block"}]))
_heart_bp_img = img_block("heart_bp", height="401px", mh="195px", border=True, fit="contain")
_heart_bp_img["styles"].append({"prop":"backgroundColor","value":HEADER_BG})
kids.extend(figure(_heart_bp_img))
kids.append(sp(10))
kids.append(text('<span style="color:#16181C">Here\'s where the comparison stops being close. The Oura Ring '
    'doesn\'t measure blood pressure. No shipping smart ring does. The </span>'
    '<a href="%s" target="_blank" style="color:#1A5FD0;text-decoration:underline">HLTH Band</a>' % PDP +
    '<span style="color:#16181C"> tracks blood pressure trends around the clock, one of the only devices at '
    'any price to do it without a subscription. Orange line for systolic, purple for diastolic, every rise and '
    'dip across the day, with the normal range printed underneath so you know what good looks like without '
    'Googling it.</span>', font=SERIF))
kids.append(para("Around it sits the rest of the heart picture: continuous heart rate on a full-day graph, HRV "
    "overnight, blood oxygen as a simple percentage. Trends for your own awareness rather than medical "
    "readings, but if your heart is the reason you're shopping for a tracker, only one of these two shows you "
    "the number your GP asks about."))
kids.append(winline_plain("HLTH Band"))
kids.append(sp(28))

# ============================== SLEEP TRACKING ===============================
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
kids.append(winline_plain("Oura Ring 4"))
kids.append(sp(28))

# ============================== TRAINING =====================================
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

# ============================== EVERYDAY LIFE ================================
kids.append(h2("Everyday Life And Comfort"))
kids.append(sp(10))
kids.extend(figure(img_block("lifestyle", height="430px", mh="230px", border=True)))
kids.append(sp(10))
kids.append(para("The ring is the better piece of jewellery, and honestly it's not close. If you want a "
    "tracker nobody clocks at dinner, Oura wins on looks."))
kids.append(para('Living with it is where the friction hides. You order a sizing kit, wait, measure, and '
    'sometimes still get it wrong. It’s a small object that goes in a gym bag pocket and doesn’t '
    'always come back out, which is why "find my Oura ring" is popular enough to be its own article '
    'genre. The band adjusts on your wrist in seconds, fits anyone in the house, works with iPhone and Android '
    'both, and weighs less than most watch straps alone.'))
kids.append(winline_hlth())
kids.append(sp(28))

# ============================== PRICE / COST CHART ===========================
# V1's chart is a "CUMULATIVE COST OF OWNERSHIP" year-by-year grouped bar
# chart with a color-dot legend -- genuinely different from V3's stacked-
# segment chart. Structure + exact bar-width percentages measured directly
# from pb/0's raw live body (node widths: 56.7/66.5/75.4% Oura across
# Year 1-3, HLTH steady at 10.7% every year).
def sp2(desktop_px, mobile_px):
    return container([], [{"prop":"width","value":"100%"},{"prop":"height","value":"%dpx"%desktop_px},
        {"prop":"lfDisplay","value":"block"},{"prop":"height","value":"%dpx"%mobile_px,"media":767}])

def cost_year_group(year_label, oura_value, oura_pct, hlth_value, hlth_pct, oura_weight="700", extra=None,
                     mt_mobile="16px"):
    # Mobile has its own measured spec (Figma node 12:849, a genuinely
    # separate 350px-wide frame, not desktop scaled down): bars 14px tall
    # (desktop 18px), label column 74px (desktop 96px), smaller label/value
    # text -- all added as explicit media:767 overrides below.
    def bar_line(name, value, pct, color, weight):
        return rowf([
            container([text(name, size="13px", lh="18px", color=BODY, font=SANS,
                             m={"fontSize":"11.5px","lineHeight":"14px"})],
                [{"prop":"width","value":"96px"},{"prop":"flexShrink","value":"0"},
                 {"prop":"width","value":"74px","media":767}]),
            rowf([
                container([], [{"prop":"width","value":"%s%%"%pct},{"prop":"height","value":"18px"},
                    {"prop":"borderRadius","value":"999px"},{"prop":"backgroundColor","value":color},
                    {"prop":"height","value":"14px","media":767}]),
                inline_text(value, size="13.5px", lh="18px", color=DARK, weight=weight, font=SANS,
                            m={"fontSize":"12px","lineHeight":"14px"}),
            ], gap="8px", align="center", styles=[{"prop":"flex","value":"1"},{"prop":"minWidth","value":"0"}]),
        ], gap="10px", align="center")
    kids_ = [text(year_label, size="11.5px", lh="15px", color=DARK, weight="800", font=SANS,
                  m={"fontSize":"10px","letterSpacing":"0.7px"}),
             bar_line("Oura Ring 4", oura_value, oura_pct, CHART_GRAY, oura_weight),
             bar_line("HLTH Band", hlth_value, hlth_pct, RED, "700")]
    if extra: kids_.append(extra)
    return col(kids_, gap="8px", styles=[{"prop":"margin","value":{"top":"14px"}},
        {"prop":"margin","value":{"top":mt_mobile},"media":767}])

def cost_chart_v1():
    legend_swatch = lambda color, label: rowf([
        container([], [{"prop":"width","value":"10px"},{"prop":"height","value":"10px"},
            {"prop":"borderRadius","value":"50%"},{"prop":"backgroundColor","value":color}]),
        text(label, size="12px", lh="15px", color=BODY, font=SANS, m={"fontSize":"10.5px"}),
    ], gap="6px", align="center", styles=[{"prop":"width","value":"fit-content"}])
    # Mobile: the header row wraps (title + legend can't fit on one 350px
    # line), and on its own wrapped line the legend sits LEFT-aligned in
    # Figma (node 12:852, x=0) -- the margin-left:auto that pushes it right
    # on desktop (where it shares the line with the title) must be zeroed
    # out at mobile, or it drags the legend to the right on its own line too.
    legend = rowf([legend_swatch(CHART_GRAY, "Oura Ring 4"), legend_swatch(RED, "HLTH Band")],
        gap="14px", align="stretch", justify="flex-end", styles=[{"prop":"width","value":"fit-content"},
            {"prop":"margin","value":{"left":"auto"}},{"prop":"margin","value":{"left":"0"},"media":767}])
    header = rowf([
        text("CUMULATIVE COST OF OWNERSHIP", size="12px", lh="15px", color=DARK, weight="800", font=SANS,
             ls="0.8px", m={"fontSize":"10.5px"}),
        legend,
    ], gap="12px", align="center", justify="space-between", wrap=True)

    delta = text("£481 more over three years, on a battery that cannot be replaced",
        size="12px", lh="17px", color=RED, weight="600", font=SANS, m={"fontSize":"10.5px"})

    footnote = container([text("Oura Ring 4: £349 ring plus £5.99 a month membership, which is mandatory. "
        "HLTH Band: £79 once, no subscription. Running totals, rounded. Prices checked 13 August 2026.",
        size="12px", lh="17px", color=BODY, font=SANS)],
        [{"prop":"borderStyle","value":"solid"},{"prop":"borderColor","value":BORDER},
         {"prop":"borderWidth","value":"1px 0px 0px 0px"},{"prop":"padding","value":{"top":"12px"}},
         {"prop":"margin","value":{"top":"6px"}}])

    return col([
        header,
        # Desktop relies on each year-group's own margin-top:14px (no extra
        # spacer needed); mobile has an explicit 18px spacer here instead
        # (Figma "spacer 18", node 12:859) -- so Year 1 gets mt_mobile="0px"
        # below, to avoid double-counting the gap on mobile.
        sp2(0, 18),
        cost_year_group("YEAR 1", "~£421", "56.7", "£79", "10.7", mt_mobile="0px"),
        cost_year_group("YEAR 2", "~£493", "66.5", "£79", "10.7", mt_mobile="16px"),
        cost_year_group("YEAR 3", "~£560", "75.4", "£79", "10.7", oura_weight="800", extra=delta, mt_mobile="16px"),
        footnote,
    ], gap="0px", styles=[{"prop":"width","value":"100%"},{"prop":"backgroundColor","value":WHITE},
        {"prop":"borderRadius","value":"12px"},{"prop":"borderStyle","value":"solid"},
        {"prop":"borderColor","value":BORDER},{"prop":"borderWidth","value":"1px"},
        {"prop":"padding","value":{"top":"22px","bottom":"22px","left":"22px","right":"22px"}}])

kids.append(h2("Price: The Cost Over Three Years"))
kids.append(sp(10))
kids.extend(figure(cost_chart_v1(), cap=True))
kids[-1] = caption("Three-year running cost, both devices. (Chart: TechUnboxed)")
kids.append(sp(10))
kids.append(para("That depends entirely on which device you choose, and it's worth doing the maths."))
kids.append(sp(10))

# 3-year cost table (same structure/styling as At-A-Glance)
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
kids.append(container(cost_rows, [{"prop":"width","value":"100%"},{"prop":"borderRadius","value":"6px"},
    {"prop":"borderStyle","value":"solid"},{"prop":"borderColor","value":BORDER},
    {"prop":"borderWidth","value":"1px 0px 0px 1px"}]))
kids.append(sp(4))
kids.append(para("The membership is mandatory. Without the £5.99 a month, the app locks you down to basics, "
    "and the CEO has publicly said the paywall stays. So by year three you've paid about £560 to rent your own "
    "heart data, on a battery you can't replace. The band is £79, once, everything unlocked at purchase. "
    "That's £481 that stays in your pocket."))
kids.append(winline_hlth())
kids.append(sp(28))

# ============================== FINAL JUDGEMENT ==============================
kids.append(h2("Final Judgement"))
kids.append(para("Six rounds to the band, one to the ring. The Oura Ring 4 is a premium sleep tracker with a "
    "membership model attached, and if that's what you want, it's a good one. But if the question is health "
    "tracking, continuous coverage, blood pressure trends, training that stays measured, and a price that "
    "doesn't compound, the band wins this comparison walking away."))
kids.append(sp(8))
kids.extend(rank_card())
kids.append(sp(8))
kids.append(text('By year three the ring costs about £560, on a battery that can\'t be replaced. The band '
    'costs £79, once, with a 30-day money-back guarantee. If you\'ve been typing “is the Oura Ring '
    'worth it” into Google, this is a £79 way to answer the question.', size="18px", lh="30px", font=SERIF))
kids.append(container([button("Check HLTH Band Availability →", href=PDP, full=True, size="15px", weight="700",
    ls="0.3px", pad={"top":"12px","bottom":"12px","left":"20px","right":"20px"})],
    [{"prop":"width","value":"100%"}]))
kids.append(sp(28))

# ============================== FAQs =========================================
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
    'No. No shipping smart ring does. The <a href="%s" target="_blank" '
    'style="color:#1A5FD0;text-decoration:underline">HLTH Band</a> '
    'tracks blood pressure trends day and night, as wellness trends for your own awareness rather than medical '
    'readings.' % PDP))
kids.append(sp(10))

# Real video embed (same YouTube video wired into V3's build), not the
# gradient/play-button design placeholder -- "overflow:hidden" here is plain
# inline CSS on a hand-authored div inside HtmlElement content, not the
# native LF "styles" schema's overflow prop (the one that 503s the SSR).
video_placeholder_v1 = {"t":"HtmlElement","id":nid(),"p":{"content":(
    '<div style="width:100%;height:100%;border-radius:12px;border:1px solid #E4E6E2;'
    'overflow:hidden;box-sizing:border-box">'
    '<iframe src="https://www.youtube.com/embed/lMZoKLSmd6M" title="HLTH Band accuracy test video" '
    'style="width:100%;height:100%;display:block;border:0" '
    'allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" '
    'allowfullscreen loading="lazy"></iframe>'
    '</div>'
)}, "styles":[{"prop":"width","value":"100%"},{"prop":"height","value":"405px"},
    {"prop":"height","value":"197px","media":767}]}

kids.append(col([
    title("How accurate is the HLTH Band?", "19px", "25px", weight="700", font=SERIF),
    text('Per reading, both devices use capable optical sensors, and this comparison has never claimed '
         'otherwise for either. The meaningful difference is coverage: the band reads every five minutes '
         'around the clock, while the ring measures "under optimal conditions" to protect its '
         'battery, with gaps of up to 30 minutes by Oura’s own documentation. Rather than take our word '
         'for it, watch the band tested on video, worn day and night rather than filmed in a studio:',
         size="18px", lh="30px", color=DARK, font=SERIF),
    video_placeholder_v1,
], gap="8px"))
kids.append(sp(10))

kids.append(col([
    title("What do people say about the HLTH Band?", "19px", "25px", weight="700", font=SERIF),
    text("One of the harder places for any brand to shape its own reputation is its Trustpilot page, since "
        "Trustpilot verifies reviewers and penalises companies caught manipulating scores. The HLTH Band holds a "
        "4.6 rating there, and the same themes keep coming up: the battery genuinely lasts weeks, the band is "
        "light enough to forget, and there's nothing to pay after the £79. Read them unfiltered before you "
        "decide.", size="18px", lh="30px", color=DARK, font=SERIF),
    text('<a href="%s" target="_blank" style="color:#1A5FD0;text-decoration:underline">Read the HLTH '
        "Band's Trustpilot reviews →</a>" % TP, size="18px", lh="30px", color=DARK, font=SERIF),
], gap="8px"))
kids.append(sp(10))
kids.append(faq("Does the HLTH Band need a subscription?",
    "No. Every feature is unlocked at the £79 purchase, permanently, and it comes with a 30-day money-back "
    "guarantee."))
kids.append(sp(32))

# ============================== ENDMATTER ====================================
endmatter_kids = []
endmatter_kids.append(sp(24))
endmatter_kids.append(title("Sources", "22px", "27px", weight="700", ls="-0.22px", font=SERIF))
endmatter_kids.append(sp(12))
endmatter_kids.append(text('Oura Ring 4 pricing and membership: <a href="https://ouraring.com" target="_blank" '
    'style="color:#1A5FD0;text-decoration:underline">ouraring.com</a> (checked 8 August 2026). Heart-rate '
    'measurement behaviour: Oura Member Care, "Heart Rate Graph" and "Activity Heart Rate" '
    'support articles (accessed 8 August 2026). Battery capacities and non-replaceable battery assessment: '
    '<a href="https://www.ifixit.com" target="_blank" style="color:#1A5FD0;text-decoration:underline">iFixit '
    'teardowns</a> (June 2026); <a href="https://ouraring.com/store/rings/oura-ring-4" target="_blank" '
    'style="color:#1A5FD0;text-decoration:underline">published Oura Ring 4 specifications</a>. HLTH Band '
    'specifications: <a href="https://hlthtrack.co.uk" target="_blank" '
    'style="color:#1A5FD0;text-decoration:underline">hlthtrack.co.uk</a>. '
    '£79 is a launch price; standard price £158. Three-year Oura cost: £349 + 36 × £5.99 ≈ £560. Prices may '
    'have changed since checking.', size="13.5px", lh="22px", color=BODY, font=SERIF))
endmatter_kids.append(sp(14))
endmatter_kids.append(container([text('<b style="color:#4A4F57">Disclaimer.</b> <span style="color:#4A4F57">HLTH '
    'Band is not a medical device; readings show trends and are not a substitute for medical measurement or '
    'advice. This page is an advertisement for </span><a href="%s" target="_blank" '
    'style="color:#1A5FD0;text-decoration:underline">HLTH Band</a><span style="color:#4A4F57">.</span>' % PDP,
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

# ============================== FOOTER LEGAL =================================
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
OG = json.load(open("pagescore/.cache/og_img_map.json"))  # QA: purpose-cut 1200x630 share images
SEO = {
    "title": 'Oura Ring 4 vs HLTH Band: Which Tracks Better?',
    "description": 'One costs £349 plus £5.99 a month, the other £79 once. We wore both for 30 days and compared sleep, heart rate and blood pressure data side by side.',
    "keywords": 'Oura Ring 4 vs HLTH Band, smart ring comparison, Oura Ring alternative, health tracker no subscription, blood pressure wearable, best health tracker 2026, screenless tracker',
    "social_image_uid": OG["oura-v1"]["src_uid"],
}

# QA: settings.seo emits og:* only, so X/Twitter had no card on any of the eleven pages.
# Append explicit twitter:* tags to the header custom_html, from the same SEO values.
def _esc(v): return v.replace("&","&amp;").replace('"',"&quot;").replace("<","&lt;").replace(">","&gt;")
CUSTOM_HTML = {"header": PERF + (
    '<meta name="twitter:card" content="summary_large_image">\n'
    '<meta name="twitter:title" content="%s">\n'
    '<meta name="twitter:description" content="%s">\n'
    '<meta name="twitter:image" content="%s">\n'
    ) % (_esc(SEO["title"]), _esc(SEO["description"]), OG["oura-v1"]["src"]),
    "footer": PERF_FOOTER}

# ---------------- write: overwrite the already-created step's body ----------------
existing = sgql('query($q: String!){ funnels(first:1,query:$q){ edges { node { steps { id uid slug title } } } } }',
    {"q": f"id:{FUNNEL}"})["funnels"]["edges"][0]["node"]["steps"]
match = next((s for s in existing if s["slug"] == STEP_SLUG), None)
if not match:
    sys.exit(f"Step {STEP_SLUG} not found in funnel {FUNNEL} -- expected it to already exist (created via createStep).")
STEP = match["id"]
TITLE = "Oura Ring 4 vs HLTH Band: Which Is Better For Health Tracking?"
print("overwriting existing step ->", match)

r2 = sgql('''mutation($id: ID!, $node: InputFunnel!){ updateFunnel(id:$id,node:$node){ id starting_step_id published steps { uid slug title } } }''',
    {"id": FUNNEL, "node": {"published": True,
        "steps": [{"id": STEP, "slug": STEP_SLUG, "title": TITLE, "type": "article_page",
            "settings": {"custom_html": CUSTOM_HTML, "seo": SEO}, "visual": {"x": 940, "y": 90}, "body": body}]}})
print("WROTE", json.dumps(r2["updateFunnel"], indent=2))
