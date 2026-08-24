#!/usr/bin/env python3
"""Oura Ring 4 vs HLTH Band advertorial (Figma node 12:3, "Oura vs HLTH ·
TechUnboxed V1 · 1440") as native LF blocks. Content + styles measured
verbatim from figwright. Writes the FIRST step into the empty, unpublished
funnel fun_hLmlmrbjeoGf3UZZvBEHY via the from-scratch recipe (createStep then
updateFunnel with starting_step_id).

Typography note: the Figma design sets editorial copy in "Gelasio" (serif)
and UI chrome (tags/byline/tables/buttons/cards) in "SF Pro". Neither is safe
to web-font-load without repeating the whole CLS investigation in
references/performance.md (no pre-computed metric-override values exist for
Gelasio, and SF Pro isn't legally embeddable). Decision: serif copy uses the
system stack "Georgia, 'Gelasio', 'Times New Roman', serif" (Gelasio was
commissioned by Google specifically as a metric-compatible Georgia
substitute, so this is a close, ZERO-download, zero-CLS match); UI chrome
reuses the already-proven Inter/InterFallback CLS-safe stack from
build_test3.py. No new font-loading risk introduced.

SSR/editor gotchas (verified live on this exact funnel per the
lf-editor-ssr-gotchas memory note): quoted font-family names crash the LF
EDITOR canvas (storefront is fine, but the editor 500s) -> font stacks below
are UNQUOTED. And `overflow`, `boxShadow`, `maxWidth:"none"`,
`alignItems:"baseline"` are accepted by the API but 503 the SSR renderer ->
none of those props/values are used anywhere in this file.
"""
import sys, os, json, uuid
sys.path.insert(0, '.')
import lf_api

tok = open('.session_token').read().strip()
ACCT = open('.lf_account').read().strip()
HH = {"account-id": ACCT, "version": "1",
      "Origin": "https://app.lightfunnels.com", "Referer": "https://app.lightfunnels.com/"}
def sgql(q, v=None): return lf_api.gql(tok, q, v, extra_headers=HH)
def nid(): return str(uuid.uuid4())

FUNNEL = "fun_hLmlmrbjeoGf3UZZvBEHY"
IMG = json.load(open("/private/tmp/claude-501/-Users-randellbenedictcalilung-lf-agent-bridge/87bcedeb-b3fc-4741-a18e-df0d9a042abe/scratchpad/oura_hlth_img_map.json"))

PDP = "https://hlthtrack.com/products/wearable-hlth-band"
TP  = "https://www.trustpilot.com/review/hlthtrack.com"
OURA_URL = "https://ouraring.com/en-us/product/rings/oura-ring-4"

# ---- fonts ----
# NOTE (font-swap follow-up, see below): flipped to real-Gelasio-first. The claim in
# the paragraph above ("SERIF uses local Georgia/Times, no download, so it cannot
# shift on swap") was the pre-fix rationale for NOT loading Gelasio; superseded once
# the user explicitly asked to load the real webfont despite the CLS-risk tradeoff.
# Verified empirically (see GELASIO_HEAD comment) that Gelasio is close enough to
# Georgia metrically that this still doesn't introduce reflow.
SERIF = "Gelasio, Georgia, serif"   # editorial copy (Gelasio in Figma) — UNQUOTED, see gotcha above
SANS  = "Inter, InterFallback, sans-serif"                # UI chrome (SF Pro in Figma)

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
GELASIO_HEAD = (
    '<link rel="preconnect" href="https://fonts.googleapis.com">\n'
    '<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>\n'
    '<link rel="preload" as="font" type="font/woff2" crossorigin '
    'href="https://fonts.gstatic.com/s/gelasio/v14/cIf9MaFfvUQxTTqS9C6hYQ.woff2">\n'
    '<link href="https://fonts.googleapis.com/css2?family=Gelasio:ital,wght@0,400;0,700;1,400&display=swap" '
    'rel="stylesheet">\n')
# IMPORTANT -- DO NOT re-run this script's write section below as-is: the LIVE step
# (slug "oura-vs-hlth-band-v1", id step_ez7sidd3Dknpc-Z-4vhg0) already has this exact
# Gelasio fix applied (verified live 2026-08-19: header already carries GELASIO_HEAD's
# stylesheet link, body already has SERIF="Gelasio, Georgia, serif" baked in), AND its
# live body content has otherwise diverged significantly from what this checked-in
# script currently generates (different Pros/Cons copy, a real embedded YouTube video,
# working PDP <a> links vs this script's plain spans) -- some other session/edit path
# updated the live page without updating this file. Re-running this script's
# create/update flow below would REVERT that live content. SLUG below was also stale
# ("oura-vs-hlth-band" vs the live "oura-vs-hlth-band-v1"), which combined with the
# hardcoded published:False / starting_step_id below would have unpublished the
# WHOLE LIVE FUNNEL (fixed defensively below, but still: do not run this write path
# without re-diffing body content against live first).
#
# ---- perf: Inter preload + real @font-face + metric-matched fallback (verified zero-CLS
#      recipe from build_test3.py / references/performance.md). Only needed for SANS text;
#      SERIF uses local Georgia/Times, no download, so it cannot shift on swap.
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
PERF_FOOTER = (
    '<script>(function(){function f(){var h=document.querySelector(\'img[title="hero"]\');'
    'if(h){h.setAttribute("fetchpriority","high");h.setAttribute("loading","eager");}'
    'var lg=document.querySelector(\'img[title="logo"]\');if(lg)lg.removeAttribute("fetchpriority");}'
    'if(document.readyState!=="loading")f();else document.addEventListener("DOMContentLoaded",f);})();</script>\n')
# ONE shared delegated click-listener for every "Pros & Cons" accordion (used twice in the
# article -> 2 desktop + 2 mobile card instances). Native Container/Text blocks carry no
# onclick prop, so the toggle lives here instead of 4 duplicated inline handlers.
ACCORDION_JS = (
    '<script>document.addEventListener("click",function(e){'
    'var t=e.target.closest(".hlth-acc-toggle");if(!t)return;'
    'var b=t.nextElementSibling;if(!b)return;'
    # use COMPUTED style, not b.style.display: the initial "none" comes from an LF-authored
    # CSS rule (lfDisplay), not an inline style, so b.style.display is "" on first click and
    # a naive `b.style.display!=="none"` check is wrong until the 2nd click (verified live).
    'var open=getComputedStyle(b).display!=="none";'
    'b.style.display=open?"none":"flex";'
    'var c=t.querySelector(".hlth-chev");'
    'if(c)c.style.transform=open?"rotate(0deg)":"rotate(180deg)";'
    '});</script>\n')

# ---- colors (measured) ----
DARK   = {"r":22,"g":24,"b":28,"a":1}    # #16181C main text
BODY   = {"r":74,"g":79,"b":87,"a":1}    # #4A4F57 secondary text
MUTED  = {"r":154,"g":160,"b":168,"a":1} # #9AA0A8 dateline
BORDER = {"r":228,"g":230,"b":226,"a":1} # #E4E6E2
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

# ---- helpers ----
def _media(st, m):
    if m:
        for k, v in m.items(): st.append({"prop": k, "value": v, "media": 767})

def title(content, fs, lh, weight="700", mt=0, color=DARK, align="left", ls=None, m=None, font=SERIF):
    st=[{"prop":"fontFamily","value":font},{"prop":"color","value":color},
        {"prop":"fontSize","value":fs},{"prop":"lineHeight","value":lh},
        {"prop":"fontWeight","value":weight},{"prop":"textAlign","value":align},
        {"prop":"width","value":"100%"},{"prop":"maxWidth","value":"100%"}]
    if ls: st.append({"prop":"letterSpacing","value":ls})
    if mt: st.append({"prop":"margin","value":{"top":"%spx"%mt}})
    _media(st, m)
    return {"t":"Title","id":nid(),"p":{"size":"2","content":content,"widthOption":"fill"},"styles":st}

def text(content, size="18px", lh="30px", color=DARK, weight="400", align="left", italic=False,
         mw="100%", m=None, font=SERIF):
    st=[{"prop":"fontFamily","value":font},{"prop":"color","value":color},
        {"prop":"fontSize","value":size},{"prop":"lineHeight","value":lh},
        {"prop":"fontWeight","value":weight},{"prop":"textAlign","value":align},
        {"prop":"maxWidth","value":mw},{"prop":"width","value":"100%"}]
    if italic: st.append({"prop":"fontStyle","value":"italic"})
    _media(st, m)
    return {"t":"Text","id":nid(),"p":{"content":content},"styles":st}

def zws():
    """Zero-footprint filler child. A Container with NO children shows a persistent
    "+Add Element" ghost overlay in the LF editor (pure editor chrome, but clutters the
    canvas badly on decorative divs like bar-chart fills/swatches/dividers that are never
    meant to hold real content) -- give every such Container this instead of []."""
    return {"t":"Text","id":nid(),"p":{"content":"&#8203;"},
        "styles":[{"prop":"fontSize","value":"1px"},{"prop":"lineHeight","value":"1px"},
                  {"prop":"width","value":"0px"},{"prop":"height","value":"0px"},
                  {"prop":"maxWidth","value":"0px"},
                  {"prop":"margin","value":{"top":"0px","bottom":"0px","left":"0px","right":"0px"}},
                  {"prop":"padding","value":{"top":"0px","bottom":"0px","left":"0px","right":"0px"}}]}

def container(children, styles, cls=None):
    p = {"children":children}
    if cls: p["className"] = cls
    return {"t":"Container","id":nid(),"styles":styles,"p":p}

def rowf(children, styles=None, gap="16px", align="stretch", justify=None, wrap=False, cls=None):
    s=[{"prop":"lfDisplay","value":"flex"},{"prop":"flexDirection","value":"row"},
       {"prop":"gap","value":gap},{"prop":"alignItems","value":align},{"prop":"width","value":"100%"}]
    if justify: s.append({"prop":"justifyContent","value":justify})
    if wrap: s.append({"prop":"flexWrap","value":"wrap"})
    if styles: s.extend(styles)
    return container(children, s, cls=cls)

def col(children, styles=None, gap="8px", cls=None):
    s=[{"prop":"lfDisplay","value":"flex"},{"prop":"flexDirection","value":"column"},
       {"prop":"gap","value":gap},{"prop":"width","value":"100%"}]
    if styles: s.extend(styles)
    return container(children, s, cls=cls)

def img_block(key, height=None, radius="10px", full=True, fit="cover", mh=None):
    m=IMG[key]
    st=[{"prop":"maxWidth","value":"100%"},{"prop":"borderRadius","value":radius},
        {"prop":"objectFit","value":fit},{"prop":"lfDisplay","value":"block"}]
    if full: st.append({"prop":"width","value":"100%"})
    if height: st.append({"prop":"height","value":height})
    if mh: st.append({"prop":"height","value":mh,"media":767})
    return {"t":"Image","id":nid(),"p":{"title":key,"src_id":m["src_id"],"src_uid":m["src_uid"],"src":m["src"]},"styles":st}

def inline_img(key, w, h, radius="0px", fit="contain"):
    m=IMG[key]
    return {"t":"Image","id":nid(),"p":{"title":key,"src_id":m["src_id"],"src_uid":m["src_uid"],"src":m["src"]},
        "styles":[{"prop":"width","value":w},{"prop":"height","value":h},{"prop":"objectFit","value":fit},
                  {"prop":"borderRadius","value":radius},{"prop":"lfDisplay","value":"block"},{"prop":"flexShrink","value":"0"}]}

def logo_img(w="140px", h="35px"):
    m=IMG["logo"]
    return {"t":"Image","id":nid(),"p":{"title":"logo","src":m["src"]},
        "styles":[{"prop":"width","value":w},{"prop":"height","value":h},{"prop":"maxWidth","value":"100%"},
                  {"prop":"objectFit","value":"contain"},{"prop":"lfDisplay","value":"block"}]}

def button(label, href=PDP, bg=RED, fg=WHITE, full=False, size="15px", weight="700", radius="10px", ls=None):
    lab_st=[{"prop":"fontFamily","value":SANS},{"prop":"color","value":fg},
            {"prop":"fontSize","value":size},{"prop":"fontWeight","value":weight},
            {"prop":"lineHeight","value":"20px"},{"prop":"textAlign","value":"center"},
            {"prop":"whiteSpace","value":"nowrap"},{"prop":"maxWidth","value":"100%"}]
    if ls: lab_st.append({"prop":"letterSpacing","value":ls})
    lab={"t":"Text","id":nid(),"p":{"content":label},"styles":lab_st}
    lw=container([lab],[{"prop":"lfDisplay","value":"flex"},{"prop":"alignItems","value":"center"},
        {"prop":"justifyContent","value":"center"},{"prop":"maxWidth","value":"100%"}])
    st=[{"prop":"backgroundColor","value":bg},{"prop":"borderRadius","value":radius},
        {"prop":"padding","value":{"top":"13px","bottom":"13px","left":"10px","right":"10px"}},
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

def caption(t="(Image credit: Marcus Pendleton / TechUnboxed)"):
    return text(t, size="13px", lh="18px", color=BODY, italic=True, font=SERIF)

def para(t): return text(t, size="18px", lh="30px", color=DARK, font=SERIF)

def winline_hlth(mt=0):
    return text('<span style="color:#E63946">Winner: </span>'
                 '<span style="color:#1A5FD0;text-decoration:underline">HLTH Band</span>',
                 size="18px", lh="30px", weight="700", font=SERIF,
                 m=({"margin":{"top":"%spx"%mt}} if mt else None))

def winline_oura():
    return text('Winner: Oura Ring 4', size="18px", lh="30px", weight="700", color=RED, font=SERIF)

def h2(content, mt=24):
    return title(content, "28px", "35px", weight="700", color=DARK, ls="-0.28px", mt=mt, font=SERIF,
                 m={"fontSize":"22px","lineHeight":"28px"})

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

logo_bar = {"t":"Section","id":nid(),
    "styles":[{"prop":"backgroundColor","value":HEADER_BG},
              {"prop":"padding","value":{"top":"14px","bottom":"14px"}}],
    "p":{"layout":"","dividerPosition":["top"],"horizontalFlip":False,
         "embedded_video":{"src":"","video_size":"stretch","video_position":"center"},
         "children":[container([logo_img()],[{"prop":"lfDisplay","value":"flex"},
             {"prop":"justifyContent","value":"center"},{"prop":"width","value":"100%"}])]}}

BREADCRUMB = ('<span style="color:#16181C">Home</span> <span style="color:#B9BDC4">&gt;</span> '
    '<span style="color:#16181C">Wearables</span> <span style="color:#B9BDC4">&gt;</span> '
    '<span style="color:#E63946;font-weight:600">Oura Ring 4 vs HLTH Band</span>')

# ============================== ARTICLE HEAD ==============================
kids=[]
kids.append(text(BREADCRUMB, size="13px", lh="18px", font=SANS, m={"fontSize":"14px"}))
kids.append(title("Oura Ring 4 vs HLTH Band: Which Is Better For Health Tracking?",
    "40px","46px", weight="700", ls="-0.4px", font=SERIF,
    m={"fontSize":"26px","lineHeight":"31px"}))
kids.append(text("One costs £349 plus £5.99 a month. The other costs £79 once. We wore both for a "
    "month, nine rounds, and the famous ring wins exactly one of them.",
    size="20px", lh="30px", color=BODY, font=SERIF, m={"fontSize":"17px","lineHeight":"25px"}))

# tag row
tag_comparison = container([text("Comparison", size="15px", lh="15px", color=WHITE, weight="700", font=SANS)],
    [{"prop":"backgroundColor","value":RED},{"prop":"borderRadius","value":"8px"},
     {"prop":"padding","value":{"top":"7px","bottom":"7px","left":"15px","right":"15px"}}])
TRENDING_SVG = ('<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="#16181C" stroke-width="2.5" '
    'stroke-linecap="round" stroke-linejoin="round" style="vertical-align:-2px;margin-right:6px">'
    '<polyline points="22 7 13.5 15.5 8.5 10.5 2 17"/><polyline points="16 7 22 7 22 13"/></svg>')
tag_trending = container([text(TRENDING_SVG + "Trending", size="15px", lh="15px", color=DARK, weight="700", font=SANS)],
    [{"prop":"backgroundColor","value":YELLOW_TAG},{"prop":"borderRadius","value":"8px"},
     {"prop":"padding","value":{"top":"7px","bottom":"7px","left":"15px","right":"15px"}}])
kids.append(rowf([tag_comparison, tag_trending], gap="10px", align="center", justify="flex-start",
    styles=[{"prop":"width","value":"fit-content"}]))

# byline strip
byline_who = col([
    text("Marcus Pendleton", size="15.5px", lh="20px", color=DARK, weight="800", font=SANS),
    text("Principal Writer", size="13.5px", lh="18px", color=BODY, font=SANS),
], gap="2px", styles=[{"prop":"width","value":"150px"},{"prop":"flexShrink","value":"0"}])
byline_bio = col([
    text('<span style="color:#4A4F57">Marcus is a lead writer at TechUnboxed, reviewing and testing the latest '
         'smartwatches and fitness trackers. </span><b style="color:#16181C;text-decoration:underline">Read full bio</b>',
         size="14.5px", lh="22px", font=SANS),
    text("Last updated 18 July 2026", size="12.5px", lh="16px", color=MUTED, font=SANS),
], gap="6px", styles=[{"prop":"flex","value":"1"},{"prop":"minWidth","value":"220px"}])
byline = rowf([
    container([{"t":"Image","id":nid(),"p":{"title":"avatar","src_id":IMG["avatar"]["src_id"],
        "src_uid":IMG["avatar"]["src_uid"],"src":IMG["avatar"]["src"]},
        "styles":[{"prop":"width","value":"52px"},{"prop":"height","value":"52px"},
                  {"prop":"borderRadius","value":"50%"},{"prop":"objectFit","value":"cover"}]}],
        [{"prop":"width","value":"52px"},{"prop":"flexShrink","value":"0"}]),
    byline_who, byline_bio], gap="16px", align="center", wrap=True,
    styles=[{"prop":"borderStyle","value":"solid"},{"prop":"borderColor","value":DASH_BORDER},
        {"prop":"borderWidth","value":"1.5px 0px 1.5px 0px"},
        {"prop":"padding","value":{"top":"16px","bottom":"16px"}}])
kids.append(byline)

# hero
kids.append(img_block("hero", height="403px", mh="196px"))
kids.append(caption())

# hookline + intro
kids.append(title("I'll say this upfront: I've worn an Oura Ring every day for two years, and I love the thing.",
    "18px","30px", weight="700", font=SERIF, m={"fontSize":"17px","lineHeight":"26px"}))
kids.append(text('<span style="color:#16181C">Then the </span>'
    '<span style="color:#1A5FD0;text-decoration:underline">HLTH Band</span>'
    '<span style="color:#16181C"> went absolutely viral this summer and flooded my inbox with one question: '
    'do I really need the £349 ring, or does the £79 band do the job? I wanted to wave it off. But the maths '
    'stopped me. By year three, the ring costs about £560. The band costs £79, once. Seven times the price. '
    "I'd been recommending it without ever checking.</span>", font=SERIF))
kids.append(para("One way to find out. A month with both, ring on my right hand, band on my left wrist. Same "
    "days, same workouts, same nights. Some rounds weren't close. One went the way you'd never guess from the "
    "prices. Here's the whole month, round by round."))

# ============================== SHOP GRID (2 cards) ========================
def shop_button(label, href):
    lab={"t":"Text","id":nid(),"p":{"content":label},
        "styles":[{"prop":"fontFamily","value":SANS},{"prop":"color","value":WHITE},
            {"prop":"fontSize","value":"15px"},{"prop":"fontWeight","value":"600"},
            {"prop":"lineHeight","value":"20px"},{"prop":"textAlign","value":"center"}]}
    return {"t":"BlockLink","id":nid(),"p":{"destination":{"type":"static","value":href},"target":"_blank",
        "widthOption":"auto","children":[container([lab],[{"prop":"lfDisplay","value":"flex"},
            {"prop":"alignItems","value":"center"},{"prop":"justifyContent","value":"center"}])]},
        "styles":[{"prop":"backgroundColor","value":DARK},{"prop":"padding","value":{"top":"12px","bottom":"12px"}},
            {"prop":"lfDisplay","value":"flex"},{"prop":"alignItems","value":"center"},
            {"prop":"justifyContent","value":"center"},{"prop":"width","value":"100%"}]}

oura_card = col([
    img_block("oura_product", height="351px", radius="6px", fit="cover"),
    col([
        text("Oura", size="13.5px", lh="18px", color=BODY, font=SANS),
        text("Oura Ring 4", size="18px", lh="23px", color=DARK, weight="700", font=SANS),
    ], gap="6px"),
    rowf([text("£349", size="15.5px", lh="21px", color=DARK, font=SANS),
          text("+ £5.99/month membership", size="13px", lh="21px", color=BODY, font=SANS)],
        gap="6px", align="center", styles=[{"prop":"width","value":"fit-content"}]),
    shop_button("Shop Now", OURA_URL),
], gap="12px", styles=[{"prop":"width","value":"100%"}])

hlth_card = col([
    img_block("hlth_product", height="351px", radius="6px", fit="cover"),
    col([
        text("HLTH", size="13.5px", lh="18px", color=BODY, font=SANS),
        text("HLTH Band 1.0", size="18px", lh="23px", color=DARK, weight="700", font=SANS),
    ], gap="6px"),
    rowf([text('<span style="text-decoration:line-through">£158</span>', size="15.5px", lh="21px", color=BODY, font=SANS),
          text("£79", size="15.5px", lh="21px", color=RED, weight="700", font=SANS),
          text("one time, no subscription", size="13px", lh="21px", color=BODY, font=SANS)],
        gap="6px", align="center", wrap=True, styles=[{"prop":"width","value":"fit-content"}]),
    shop_button("Shop Now", PDP),
], gap="12px", styles=[{"prop":"width","value":"100%"}])

kids.append(rowf([oura_card, hlth_card], gap="18px", align="flex-start",
    styles=[{"prop":"flexDirection","value":"column","media":767},{"prop":"gap","value":"32px","media":767}]))

kids.append(container([zws()],[{"prop":"width","value":"100%"},{"prop":"height","value":"1px"},
    {"prop":"backgroundColor","value":BORDER},{"prop":"margin","value":{"top":"10px","bottom":"10px"}}]))
kids.append(para("If a wrist band versus a finger ring sounds like apples and oranges, it isn't. Both do the "
    "same job: track your heart, sleep and recovery in the background, no screen, and show you the trends. "
    "The difference is what each body part lets the hardware do. That difference decides almost every round below."))

# ============================== TABLE: AT A GLANCE =========================
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
               align=align, font=SANS, m={"fontSize":"12.5px" if header else "13.5px"})
    if header:
        txt["styles"].append({"prop":"letterSpacing","value":"0.4px"})
    return container([txt], st)

def table_row(cells, highlight_last=True, last_row=False):
    st=[{"prop":"width","value":"100%"}]
    return rowf(cells, gap="0px", align="stretch", styles=st)

AAG_ROWS = [
    ("Price", "£349", "£79 once"),
    ("Subscription", "£5.99/mo, mandatory", "None, ever"),
    ("3-year cost", "~£560", "£79"),
    ("Battery life", "5–8 days rated", "~30 days"),
    ("Daytime readings", "\"Under optimal conditions\" · gaps up to 30 min", "Every 5 min · 288/day"),
    ("Blood pressure trends", "No", "Day & night"),
    ("Sizing", "Sizing kit first", "Adjusts in seconds"),
    ("Sleep comfort", "Best in class", "Excellent at 18g"),
]
aag_header = table_row([
    cell("", 220, header=True, bg=TABLEBG),
    cell("OURA RING 4", 280, header=True, bg=TABLEBG),
    cell("HLTH BAND", 220, header=True, bg=TABLEBG),
])
aag_rows = [aag_header]
for label, oura_v, hlth_v in AAG_ROWS:
    aag_rows.append(table_row([
        cell(label, 220, bold=True),
        cell(oura_v, 280),
        cell(hlth_v, 220, bold=True, bg=PINK),
    ]))
kids.append(h2("The Comparison At A Glance"))
kids.append(container(aag_rows, [{"prop":"width","value":"100%"},
    {"prop":"borderStyle","value":"solid"},{"prop":"borderColor","value":BORDER},
    {"prop":"borderWidth","value":"1px 0px 0px 1px"},{"prop":"borderRadius","value":"6px"}]))

# ============================== RANKING · EDITOR'S PICK ====================
PROS = ["No subscription — every feature unlocked at £79", "288 blood-pressure &amp; heart-rate readings a day",
        "Confirmed ~30-day battery life", "18g screen-free design, comfortable to sleep in",
        "Adjusts to any wrist in seconds", "Bicep strap included for steadier training reads"]
CONS = ["Newer company — batches have sold out before", "No built-in GPS (relies on your phone)",
        "No screen — check the app for readings"]

CHEV_SVG = ('<svg class="hlth-chev" width="10" height="10" viewBox="0 0 10 10" fill="none" '
    'stroke="#E63946" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" '
    'style="vertical-align:1px;margin-left:8px;transition:transform .2s">'
    '<polyline points="1 3 5 7 9 3"/></svg>')

def acc_line(t, sign=True):
    ic = ('<span style="color:#16a34a;font-weight:700">✓</span>' if sign
          else '<span style="color:#dc2626;font-weight:700">✗</span>')
    return text('%s&nbsp;<span style="color:#4A4F57">%s</span>' % (ic, t), size="13px", lh="19px", font=SANS)

def accordion_block():
    # native Container/Text blocks — clickable summary toggled by ONE delegated
    # click-listener in the page's header custom_html (see ACCORDION_JS below),
    # not a per-instance inline onclick (LF blocks don't support onclick anyway).
    summary = container([text('Pros &amp; Cons' + CHEV_SVG, size="13px", lh="18px", color=BODY, weight="600", font=SANS)],
        [{"prop":"lfDisplay","value":"flex"},{"prop":"alignItems","value":"center"},
         {"prop":"width","value":"fit-content"}], cls="hlth-acc-toggle")
    pros_col = col([text("Pros", size="13px", lh="18px", color=DARK, weight="700", font=SANS)]
        + [acc_line(p, True) for p in PROS], gap="4px", styles=[{"prop":"flex","value":"1"},{"prop":"minWidth","value":"140px"}])
    cons_col = col([text("Cons", size="13px", lh="18px", color=DARK, weight="700", font=SANS)]
        + [acc_line(c, False) for c in CONS], gap="4px", styles=[{"prop":"flex","value":"1"},{"prop":"minWidth","value":"140px"}])
    body = rowf([pros_col, cons_col], gap="18px", align="flex-start", wrap=True,
        styles=[{"prop":"lfDisplay","value":"none"},{"prop":"margin","value":{"top":"10px"}}],
        cls="hlth-acc-body")
    return col([summary, body], gap="0px")

def rank_card_desktop(img_key="hlth_product_rank"):
    thumb = container([img_block(img_key, height="120px", radius="8px", fit="contain")],
        [{"prop":"width","value":"120px"},{"prop":"flexShrink","value":"0"}])
    badge = rowf([
        text(STAR, size="15px", lh="16px", color=GOLD, weight="700", font=SANS),
        text("EDITOR'S PICK", size="12px", lh="16px", color=DARK, weight="800", font=SANS, m=None),
    ], gap="6px", align="center", styles=[{"prop":"width","value":"fit-content"},{"prop":"letterSpacing","value":"1.2px"}])
    tprow = rowf([
        text(tp_stars(4.5, "#00B67A", 19) + '&nbsp;&nbsp;<span style="color:#16181C;font-weight:800;font-size:15px">4.5</span>',
             size="15px", lh="19px", font=SANS),
    ], gap="8px", align="center", styles=[{"prop":"width","value":"fit-content"}])
    main = col([
        badge,
        text("HLTH Band 1.0", size="21px", lh="26px", color=DARK, weight="700", font=SANS),
        tprow,
        accordion_block(),
    ], gap="6px", styles=[{"prop":"flex","value":"1"},{"prop":"minWidth","value":"0"}])
    price_row = rowf([
        text("£79", size="20px", lh="26px", color=DARK, weight="800", font=SANS),
        text('<span style="text-decoration:line-through">£158</span>', size="14px", lh="20px", color=BODY, font=SANS),
    ], gap="5px", align="center", justify="center", styles=[{"prop":"width","value":"100%"}])
    buy = col([
        button("View at HLTH", href=PDP, full=True, size="15px", weight="700", radius="10px", ls="0.3px"),
        price_row,
        text("Free UK shipping", size="12.5px", lh="17px", color=BODY, align="center", font=SANS),
    ], gap="10px", styles=[{"prop":"width","value":"200px"},{"prop":"flexShrink","value":"0"},{"prop":"alignItems","value":"center"}])
    row = rowf([thumb, main, buy], gap="20px", align="flex-start",
        styles=[{"prop":"padding","value":{"top":"22px","bottom":"22px","left":"20px","right":"20px"}}])
    return container([row], [{"prop":"width","value":"100%"},{"prop":"backgroundColor","value":WHITE},
        {"prop":"borderRadius","value":"14px"},{"prop":"borderStyle","value":"solid"},
        {"prop":"borderColor","value":BORDER},{"prop":"borderWidth","value":"1px"},
        {"prop":"lfDisplay","value":"none","media":767}])

def rank_card_mobile(img_key="hlth_product_rank"):
    badge = text('<span style="color:#F5B301">★</span>&nbsp;<span style="color:#16181C;font-weight:800;letter-spacing:1.2px">EDITOR\'S PICK</span>',
                 size="12px", lh="16px", align="center", font=SANS)
    name = text("HLTH Band 1.0", size="21px", lh="26px", color=DARK, weight="700", align="center", font=SANS)
    img = container([img_block(img_key, height="240px", radius="8px", fit="contain")],
        [{"prop":"width","value":"260px"},{"prop":"maxWidth","value":"100%"},
         {"prop":"margin","value":{"left":"auto","right":"auto"}}])
    tprow = text(tp_stars(4.5, "#00B67A", 19) + '&nbsp;&nbsp;<span style="color:#16181C;font-weight:800;font-size:15px">4.5</span>',
                 size="15px", lh="19px", align="center", font=SANS)
    price_row = text('<span style="font-weight:800;font-size:20px;color:#16181C">£79</span>&nbsp;&nbsp;'
                      '<span style="text-decoration:line-through;color:#4A4F57;font-size:14px">£158</span>',
                 size="20px", lh="26px", align="center", font=SANS)
    inner = [badge, name, img, tprow, accordion_block(),
        button("View at HLTH", href=PDP, full=True, size="15px", weight="700", radius="10px", ls="0.3px"),
        price_row,
        text("Free UK shipping", size="12.5px", lh="17px", color=BODY, align="center", font=SANS)]
    st=[{"prop":"lfDisplay","value":"none"},{"prop":"lfDisplay","value":"flex","media":767},
        {"prop":"flexDirection","value":"column"},{"prop":"gap","value":"14px"},
        {"prop":"alignItems","value":"center"},{"prop":"width","value":"100%"},
        {"prop":"backgroundColor","value":WHITE},{"prop":"borderRadius","value":"14px"},
        {"prop":"borderStyle","value":"solid"},{"prop":"borderColor","value":BORDER},
        {"prop":"borderWidth","value":"1px"},
        {"prop":"padding","value":{"top":"22px","bottom":"22px","left":"20px","right":"20px"}}]
    return {"t":"Container","id":nid(),"styles":st,"p":{"children":inner}}

def rank_card():
    return [rank_card_desktop(), rank_card_mobile()]

kids.extend(rank_card())

# ============================== THE REAL PROBLEM ============================
kids.append(h2("The Real Problem With Smart Rings"))

# citation card (recreated in HTML/blocks — solid fills, not an image, per figma fill types)
citation_header = rowf([
    text("SOURCE DOCUMENT", size="11.5px", lh="15px", color=DARK, weight="800", font=SANS, m=None),
    container([zws()], [{"prop":"flex","value":"1"},{"prop":"height","value":"1px"}]),
    text("support.ouraring.com", size="12.5px", lh="15px", color=BODY, font=SANS),
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
citation_passage = col([
    text("Oura takes measurements of your daytime heart rate for one full minute, every five minutes, using "
         "the Oura Ring's green LEDs.", size="14.5px", lh="23px", color=BODY, font=SANS),
    container([text('To preserve battery and maximize accuracy, a daytime heart rate measurement is only taken '
        'under optimal conditions, which include low movement and balanced average body temperature. Due to '
        'prioritizing these conditions, you may not receive an automatically updated heart rate for up to 30 '
        'minutes, but it can be manually updated at any time by using Live Heart Rate.',
        size="14.5px", lh="23px", color=DARK, font=SANS)],
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

# ============================== BATTERY LIFE =================================
kids.append(h2("Battery Life: The Physics Behind The Gaps"))
kids.append(para("Everything above has one cause. Teardowns put the Oura Ring 4's battery at roughly 15 to 22 "
    "mAh depending on size, smaller than a hearing aid's, and the newest ring went smaller still. The band "
    "class runs on cells around ten times larger or more. That single number explains the rationing."))

def bar_row(label, value, pct, color, w_label="180px"):
    track = container([container([zws()], [{"prop":"width","value":"%d%%"%pct},{"prop":"height","value":"14px"},
        {"prop":"borderRadius","value":"999px"},{"prop":"backgroundColor","value":color}])],
        [{"prop":"flex","value":"1"},{"prop":"minWidth","value":"0"},{"prop":"height","value":"14px"},
         {"prop":"borderRadius","value":"999px"},{"prop":"backgroundColor","value":CHART_TRACK}])
    return rowf([
        container([text(label, size="15px", lh="20px", color=DARK, weight="700", font=SANS)],
            [{"prop":"width","value":w_label},{"prop":"flexShrink","value":"0"}]),
        track,
        container([text(value, size="13.5px", lh="20px", color=BODY, align="right", font=SANS)],
            [{"prop":"width","value":"170px"},{"prop":"flexShrink","value":"0"},
             {"prop":"width","value":"110px","media":767}]),
    ], gap="12px", align="center",
        styles=[{"prop":"flexDirection","value":"column","media":767},
                {"prop":"alignItems","value":"flex-start","media":767},{"prop":"gap","value":"6px","media":767}])

battery_chart = col([
    bar_row("HLTH Band", "~30 days per charge", 100, RED),
    bar_row("Oura Ring 4 (rated)", "5–8 days", 27, CHART_GRAY),
    bar_row("Oura Ring 4 (owner-reported)", "~4–7 days, shrinking with age", 23, CHART_GRAY, w_label="260px"),
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

# ============================== HEART TRACKING ================================
kids.append(h2("Heart Tracking: The Open Lane"))
kids.append(img_block("heart_bp", height="403px", mh="230px"))
kids.append(caption())
kids.append(text('<span style="color:#16181C">Here\'s where the comparison stops being close. The Oura Ring '
    'doesn\'t measure blood pressure. No shipping smart ring does. The </span>'
    '<span style="color:#1A5FD0;text-decoration:underline">HLTH Band</span>'
    '<span style="color:#16181C"> tracks blood pressure trends around the clock, one of the only devices at '
    'any price to do it without a subscription. Orange line for systolic, purple for diastolic, every rise and '
    'dip across the day, with the normal range printed underneath so you know what good looks like without '
    'Googling it.</span>', font=SERIF))
kids.append(para("Around it sits the rest of the heart picture: continuous heart rate on a full-day graph, HRV "
    "overnight, blood oxygen as a simple percentage. Trends for your own awareness rather than medical "
    "readings, but if your heart is the reason you're shopping for a tracker, only one of these two shows you "
    "the number your GP asks about."))
kids.append(winline_hlth())

# ============================== SLEEP TRACKING ================================
kids.append(h2("Sleep Tracking: Oura's Home Turf"))
kids.append(img_block("sleep_screens", height="403px", mh="230px"))
kids.append(caption())
kids.append(para("Credit where it's due, and Oura has earned plenty. A ring is the most comfortable thing you "
    "can sleep in, three quarters of ring owners name sleep as their main use, and Oura's sleep analysis is the "
    "most polished in the business. Readiness scores, sleep staging, the lot."))
kids.append(para("The band is close. At 18 grams I forgot it overnight, and it splits the night into light, "
    "deep and REM with total hours at the top. But close isn't a win. If sleep is your only priority and the "
    "price doesn't sting, buy the ring. Just charge it in the daytime, because a sleep tracker sitting on a "
    "charger at night has missed the point."))
kids.append(winline_oura())

# ============================== TRAINING ================================
kids.append(h2("Training: Where The Ring Comes Off"))
kids.append(img_block("training", height="430px", mh="230px"))
kids.append(caption())
kids.append(para("Grabbing a bar scratches titanium, a complaint you'll find in every Oura owner forum, so the "
    "ring comes off for weights. It comes off for trades, for gardening, for anything where a metal ring meets "
    "heavy objects. Off your finger means not measuring, and even dedicated ring reviewers concede a wrist "
    "device delivers more reliable workout metrics. The band stays on, and ships with a bicep strap for "
    "steadier readings when you train. Takes about ten seconds to swap."))
kids.append(winline_hlth())

# ============================== EVERYDAY LIFE ================================
kids.append(h2("Everyday Life And Comfort"))
kids.append(img_block("lifestyle", height="430px", mh="230px"))
kids.append(caption())
kids.append(para("The ring is the better piece of jewellery, and honestly it's not close. If you want a "
    "tracker nobody clocks at dinner, Oura wins on looks."))
kids.append(para('Living with it is where the friction hides. You order a sizing kit, wait, measure, and '
    'sometimes still get it wrong. It’s a small object that goes in a gym bag pocket and doesn’t '
    'always come back out, which is why “find my Oura ring” is popular enough to be its own article '
    'genre. The band adjusts on your wrist in seconds, fits anyone in the house, works with iPhone and Android '
    'both, and weighs less than most watch straps alone.'))
kids.append(winline_hlth())

# ============================== PRICE / COST CHART ================================
kids.append(h2("Price: The Cost Over Three Years"))

def cost_bar_row(label, value, pct, color, bold_value=False):
    track = container([container([zws()], [{"prop":"width","value":"%.1f%%"%pct},{"prop":"height","value":"12px"},
        {"prop":"borderRadius","value":"999px"},{"prop":"backgroundColor","value":color}])],
        [{"prop":"flex","value":"1"},{"prop":"minWidth","value":"0"},{"prop":"height","value":"12px"},
         {"prop":"borderRadius","value":"999px"},{"prop":"backgroundColor","value":CHART_TRACK}])
    return rowf([
        container([text(label, size="13px", lh="18px", color=BODY, font=SANS)],
            [{"prop":"width","value":"96px"},{"prop":"flexShrink","value":"0"}]),
        track,
        container([text(value, size="13.5px", lh="18px", color=DARK, weight="800" if bold_value else "700",
                        align="right", font=SANS)],
            [{"prop":"width","value":"64px"},{"prop":"flexShrink","value":"0"}]),
    ], gap="10px", align="center")

def cost_year(label, oura_val, oura_pct, hlth_val, hlth_pct, extra=None):
    rows=[text(label, size="11.5px", lh="15px", color=DARK, weight="800", font=SANS,
               m={"fontSize":"11px"}),]
    body=[cost_bar_row("Oura Ring 4", oura_val, oura_pct, CHART_GRAY),
          cost_bar_row("HLTH Band", hlth_val, hlth_pct, RED)]
    if extra: body.append(extra)
    return col(rows+body, gap="8px", styles=[{"prop":"margin","value":{"top":"14px"}}])

legend = rowf([
    rowf([container([zws()],[{"prop":"width","value":"10px"},{"prop":"height","value":"10px"},
        {"prop":"borderRadius","value":"50%"},{"prop":"backgroundColor","value":CHART_GRAY}]),
        text("Oura Ring 4", size="12px", lh="15px", color=BODY, font=SANS)], gap="6px", align="center",
        styles=[{"prop":"width","value":"fit-content"}]),
    rowf([container([zws()],[{"prop":"width","value":"10px"},{"prop":"height","value":"10px"},
        {"prop":"borderRadius","value":"50%"},{"prop":"backgroundColor","value":RED}]),
        text("HLTH Band", size="12px", lh="15px", color=BODY, font=SANS)], gap="6px", align="center",
        styles=[{"prop":"width","value":"fit-content"}]),
], gap="14px", justify="flex-end", styles=[{"prop":"width","value":"fit-content"},{"prop":"margin","value":{"left":"auto"}}])

cost_header = rowf([
    text("CUMULATIVE COST OF OWNERSHIP", size="12px", lh="15px", color=DARK, weight="800", font=SANS,
         m={"fontSize":"11px"}),
    legend,
], gap="12px", align="center", justify="space-between", wrap=True)

delta_callout = text("£481 more over three years, on a battery that cannot be replaced",
    size="12px", lh="17px", color=RED, weight="600", font=SANS, m={"fontSize":"11.5px"})

cost_chart = col([
    cost_header,
    cost_year("YEAR 1", "~£421", 56.7, "£79", 10.7),
    cost_year("YEAR 2", "~£493", 66.5, "£79", 10.7),
    cost_year("YEAR 3", "~£560", 75.4, "£79", 10.7, extra=delta_callout),
    container([text("Oura Ring 4: £349 ring plus £5.99 a month membership, which is mandatory. HLTH Band: £79 "
        "once, no subscription. Running totals, rounded. Prices checked 13 August 2026.",
        size="12px", lh="17px", color=BODY, font=SANS)],
        [{"prop":"borderStyle","value":"solid"},{"prop":"borderColor","value":BORDER},
         {"prop":"borderWidth","value":"1px 0px 0px 0px"},{"prop":"padding","value":{"top":"12px"}},
         {"prop":"margin","value":{"top":"6px"}}]),
], gap="0px", styles=[{"prop":"width","value":"100%"},{"prop":"backgroundColor","value":WHITE},
    {"prop":"borderRadius","value":"12px"},{"prop":"borderStyle","value":"solid"},
    {"prop":"borderColor","value":BORDER},{"prop":"borderWidth","value":"1px"},
    {"prop":"padding","value":{"top":"22px","bottom":"22px","left":"22px","right":"22px"}}])
kids.append(cost_chart)
kids.append(caption("Three-year running cost, both devices. (Chart: TechUnboxed)"))
kids.append(para("That depends entirely on which device you choose, and it's worth doing the maths."))

# 3-year cost table
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
kids.append(para("The membership is mandatory. Without the £5.99 a month, the app locks you down to basics, "
    "and the CEO has publicly said the paywall stays. So by year three you've paid about £560 to rent your own "
    "heart data, on a battery you can't replace. The band is £79, once, everything unlocked at purchase. "
    "That's £481 that stays in your pocket."))
kids.append(winline_hlth())

# ============================== FINAL JUDGEMENT ================================
kids.append(h2("Final Judgement"))
kids.append(para("Six rounds to the band, one to the ring. The Oura Ring 4 is a premium sleep tracker with a "
    "membership model attached, and if that's what you want, it's a good one. But if the question is health "
    "tracking, continuous coverage, blood pressure trends, training that stays measured, and a price that "
    "doesn't compound, the band wins this comparison walking away."))
kids.extend(rank_card())
kids.append(text('By year three the ring costs about £560, on a battery that can’t be replaced. The band '
    'costs £79, once, with a 30-day money-back guarantee. If you’ve been typing “is the Oura Ring '
    'worth it” into Google, this is a £79 way to answer the question.', size="18px", lh="30px", font=SERIF))
kids.append(container([button("Check HLTH Band Availability →", href=PDP, full=True, size="15px", weight="700")],
    [{"prop":"width","value":"100%"}]))

# ============================== FAQs ================================
kids.append(h2("Your Questions, Answered"))
def faq(q, a_html):
    return col([
        title(q, "19px", "25px", weight="700", font=SERIF, m={"fontSize":"18px","lineHeight":"24px"}),
        text(a_html, size="18px", lh="30px", color=DARK, font=SERIF),
    ], gap="8px", styles=[{"prop":"margin","value":{"top":"18px"}}])

kids.append(faq("Is the Oura Ring worth it?",
    "If premium sleep tracking is your main goal and the £349 plus £5.99 a month doesn't bother you, it's the "
    "best ring made. For all-day health tracking, the band covers more, tracks blood pressure trends the ring "
    "can't, and costs £79 once."))
kids.append(faq("Can I use the Oura Ring without the subscription?",
    "Technically yes, but the app locks you down to a handful of basic scores. The membership is effectively "
    "mandatory for the features people buy the ring for, and Oura has said publicly it isn't going away."))
kids.append(faq("Does the Oura Ring measure blood pressure?",
    'No. No shipping smart ring does. The <span style="color:#1A5FD0;text-decoration:underline">HLTH Band</span> '
    'tracks blood pressure trends day and night, as wellness trends for your own awareness rather than medical '
    'readings.'))

GREY_VIDEO_LABEL = {"r":207,"g":211,"b":217,"a":1}  # #CFD3D9
PLAY_TRIANGLE = '<span style="display:inline-block">▶</span>'  # inline glyph, matches feat()/tp_stars() icon pattern
video_placeholder = container([
    container([text(PLAY_TRIANGLE, size="20px", lh="20px", color=WHITE, align="center", font=SANS,
                     m=None)],
        [{"prop":"width","value":"70px"},{"prop":"height","value":"49px"},{"prop":"borderRadius","value":"13px"},
         {"prop":"backgroundColor","value":RED},{"prop":"lfDisplay","value":"flex"},
         {"prop":"alignItems","value":"center"},{"prop":"justifyContent","value":"center"}]),
    text("HLTH BAND ACCURACY TEST VIDEO", size="12.5px", lh="16px", color=GREY_VIDEO_LABEL, weight="600",
         align="center", font=SANS, m={"fontSize":"11px"}),
], [{"prop":"width","value":"100%"},{"prop":"height","value":"405px"},{"prop":"height","value":"220px","media":767},
    {"prop":"borderRadius","value":"12px"},{"prop":"borderStyle","value":"solid"},{"prop":"borderColor","value":BORDER},
    {"prop":"backgroundColor","value":{"r":26,"g":28,"b":32,"a":1}},
    {"prop":"lfDisplay","value":"flex"},{"prop":"flexDirection","value":"column"},
    {"prop":"alignItems","value":"center"},{"prop":"justifyContent","value":"center"},{"prop":"gap","value":"16px"}])

kids.append(col([
    title("How accurate is the HLTH Band?", "19px", "25px", weight="700", font=SERIF, m={"fontSize":"18px","lineHeight":"24px"}),
    text('Per reading, both devices use capable optical sensors, and this comparison has never claimed '
         'otherwise for either. The meaningful difference is coverage: the band reads every five minutes '
         'around the clock, while the ring measures “under optimal conditions” to protect its '
         'battery, with gaps of up to 30 minutes by Oura’s own documentation. Rather than take our word '
         'for it, watch the band tested on video, worn day and night rather than filmed in a studio:',
         size="18px", lh="30px", color=DARK, font=SERIF),
    video_placeholder,
], gap="8px", styles=[{"prop":"margin","value":{"top":"18px"}}]))

kids.append(faq("What do people say about the HLTH Band?",
    "One of the harder places for any brand to shape its own reputation is its Trustpilot page, since "
    "Trustpilot verifies reviewers and penalises companies caught manipulating scores. The HLTH Band holds a "
    "4.5 rating there, and the same themes keep coming up: the battery genuinely lasts weeks, the band is "
    "light enough to forget, and there's nothing to pay after the £79. Read them unfiltered before you "
    'decide.<br><br><a href="%s" target="_blank" style="color:#1A5FD0;text-decoration:underline">Read the HLTH '
    "Band's Trustpilot reviews →</a>" % TP))
kids.append(faq("Does the HLTH Band need a subscription?",
    "No. Every feature is unlocked at the £79 purchase, permanently, and it comes with a 30-day money-back "
    "guarantee."))

# ============================== ENDMATTER ================================
kids.append(title("Sources", "22px", "27px", weight="700", ls="-0.22px", font=SERIF, mt=32))
kids.append(text('Oura Ring 4 pricing and membership: <a href="https://ouraring.com" target="_blank" '
    'style="color:#1A5FD0;text-decoration:underline">ouraring.com</a> (checked 8 August 2026). Heart-rate '
    'measurement behaviour: Oura Member Care, “Heart Rate Graph” and “Activity Heart Rate” '
    'support articles (accessed 8 August 2026). Battery capacities and non-replaceable battery assessment: '
    'iFixit teardowns (June 2026); published Oura Ring 4 specifications. HLTH Band specifications: '
    '<a href="https://hlthtrack.com" target="_blank" style="color:#1A5FD0;text-decoration:underline">hlthtrack.co.uk</a>. '
    '£79 is a launch price; standard price £158. Three-year Oura cost: £349 + 36 × £5.99 ≈ £560. Prices may '
    'have changed since checking.', size="13.5px", lh="22px", color=BODY, font=SERIF))
kids.append(container([text('<b style="color:#4A4F57">Disclaimer.</b> <span style="color:#4A4F57">HLTH Band '
    'is not a medical device; readings show trends and are not a substitute for medical measurement or '
    'advice. This page is an advertisement for </span><a href="%s" target="_blank" '
    'style="color:#1A5FD0;text-decoration:underline">HLTH Band</a>.' % PDP,
    size="13.5px", lh="22px", font=SERIF)],
    [{"prop":"borderStyle","value":"solid"},{"prop":"borderColor","value":BORDER},
     {"prop":"borderWidth","value":"1px 0px 0px 0px"},{"prop":"padding","value":{"top":"14px"}},
     {"prop":"margin","value":{"top":"14px"}}]))

kids.append(title("About the Author", "22px", "27px", weight="700", ls="-0.22px", font=SERIF, mt=30))
author_avatar = container([{"t":"Image","id":nid(),"p":{"title":"avatar","src_id":IMG["avatar"]["src_id"],
    "src_uid":IMG["avatar"]["src_uid"],"src":IMG["avatar"]["src"]},
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
        {"prop":"flexDirection","value":"column","media":767},{"prop":"alignItems","value":"center","media":767},
        {"prop":"textAlign","value":"center","media":767}])
kids.append(author_box)

article_col = container(kids,
    [{"prop":"maxWidth","value":"720px"},{"prop":"width","value":"100%"},
     {"prop":"margin","value":{"left":"auto","right":"auto"}},
     {"prop":"padding","value":{"left":"20px","right":"20px"},"media":767},
     {"prop":"lfDisplay","value":"flex"},{"prop":"flexDirection","value":"column"},{"prop":"gap","value":"20px"}])

# ============================== FOOTER LEGAL ================================
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
COPYRIGHT = ('© 2026 TechUnboxed · <a href="#" style="color:#4A4F57;text-decoration:underline">Terms</a> · '
    '<a href="#" style="color:#4A4F57;text-decoration:underline">Privacy</a> · '
    '<a href="#" style="color:#4A4F57;text-decoration:underline">Editorial standards</a> · '
    '<a href="#" style="color:#4A4F57;text-decoration:underline">Affiliate policy</a>')

footer_col = col([
    text(MEDICAL_DISCLAIMER, size="12.5px", lh="20px", color=BODY, align="center", font=SANS, mw="900px"),
    text(ADVERTORIAL_DISCLOSURE, size="12.5px", lh="20px", color=BODY, align="center", font=SANS, mw="900px"),
    text(COPYRIGHT, size="12.5px", lh="20px", color=BODY, align="center", font=SANS),
], gap="16px", styles=[{"prop":"maxWidth","value":"720px"},{"prop":"margin","value":{"left":"auto","right":"auto"}},
    {"prop":"alignItems","value":"center"}])

footer = {"t":"Section","id":nid(),
    "styles":[{"prop":"backgroundColor","value":TABLEBG},
              {"prop":"borderStyle","value":"solid"},{"prop":"borderColor","value":BORDER},
              {"prop":"borderWidth","value":"1px 0px 0px 0px"},
              {"prop":"padding","value":{"top":"36px","bottom":"36px","left":"40px","right":"40px"}},
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
    "p":{"children":[support_bar, logo_bar, article, footer]}}

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

CUSTOM_HTML = {"header": PERF, "footer": PERF_FOOTER + ACCORDION_JS}

# ---------------- write: createStep then updateFunnel (from-scratch recipe) ----------------
# Idempotent: if a step with this slug already exists in the funnel (re-running this script
# to iterate), reuse its id and just overwrite the body via updateFunnel instead of
# createStep (which rejects a duplicate slug). NOTE: explicitly pass published:False on every
# updateFunnel call below -- setting starting_step_id on a funnel for the FIRST time was
# observed to silently auto-publish it (verified live on this exact funnel); we do not rely
# on server defaults for this field again.
# FIXED (font-swap follow-up): SLUG was stale ("oura-vs-hlth-band" -- a pre-launch
# working slug) vs the ACTUAL live slug "oura-vs-hlth-band-v1" the step carries today
# (confirmed live 2026-08-19). Matching by the stale slug would silently miss the
# real step, createStep a brand-new ORPHAN duplicate, and then the code below would
# have pointed starting_step_id at that orphan AND hardcoded published:False --
# unpublishing the entire live multi-step funnel. Matching the live slug instead.
SLUG = "oura-vs-hlth-band-v1"
TITLE = "Oura Ring 4 vs HLTH Band"

existing = sgql('query($q: String!){ funnels(first:1,query:$q){ edges { node { starting_step_id published steps { id uid slug } } } } }',
    {"q": f"id:{FUNNEL}"})["funnels"]["edges"][0]["node"]
match = next((s for s in existing["steps"] if s["slug"] == SLUG), None)

if match:
    STEP = match["id"]
    print("reusing existing step ->", match)
else:
    r = sgql('''mutation($fid: ID!, $node: InputStep!){ createStep(funnel_id:$fid, node:$node){ step { id uid slug } } }''',
        {"fid": FUNNEL, "node": {"slug": SLUG, "title": TITLE, "type": "article_page",
            "settings": {"custom_html": CUSTOM_HTML}, "visual": {"x":100,"y":100}, "body": body}})
    STEP = r["createStep"]["step"]["id"]
    print("createStep ->", r["createStep"]["step"])

# FIXED: never hardcode starting_step_id/published here -- this funnel is LIVE with
# starting_step_id already pointed at this exact step and published=True. Echo back
# the funnel's OWN current values (matches the safe pattern used in build_hlth_v2.py)
# instead of clobbering them.
r2 = sgql('''mutation($id: ID!, $node: InputFunnel!){ updateFunnel(id:$id,node:$node){ id starting_step_id published steps { uid slug title } } }''',
    {"id": FUNNEL, "node": {"starting_step_id": existing["starting_step_id"], "published": existing["published"],
        "steps": [{"id": STEP, "slug": SLUG, "title": TITLE, "type": "article_page",
            "settings": {"custom_html": CUSTOM_HTML}, "visual": {"x":100,"y":100}, "body": body}]}})
print("WROTE", json.dumps(r2["updateFunnel"], indent=2))
print("article blocks:", len(kids))
