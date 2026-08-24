#!/usr/bin/env python3
"""HLTH Band "Top 5 Fitness-Tracker, im Test" listicle advertorial -- GERMAN
localization, added as a NEW step in the SAME live funnel fun_hLmlmrbjeoGf3UZZvBEHY
("TUB - All smart ring - Meta"), alongside the English top-5-fitness-trackers-
ranked-2026 step and the existing oura-vs-hlth-band-* steps.

Source: Figma file "HLTH", frame 145:15 "Ranked Comparison * desktop 1441"
(desktop, ~16,330px tall) and frame 145:1031 "Ranked Comparison * mobile 391"
(mobile, ~22,540px tall) -- the SAME node tree/component structure as the
English frame 60:1153/60:2087, just with German copy and German-market (EUR)
pricing. Every string below was read verbatim from Figma text-node
"characters" fields (via figwright get_node/get_design_context) -- none of it
is a machine translation of the English copy. Confirmed structural facts,
not assumed:
  - All hyperlinks (HLTH PDP, Amazon affiliate links w/ same tag, Trustpilot
    review URLs, blog.techunboxed.co further-reading URLs) are IDENTICAL to
    the English version -- the German design does not use localized domains.
  - Desktop big-list rows carry NO Trustpilot hyperlink/icon (same as
    English); mobile big-list rows DO (same as English) -- reconfirmed
    directly on this frame, not inherited by assumption.
  - FAQ is question-only, no answers anywhere in the subtree (same as
    English) -- reconfirmed directly on 145:872/145:1906.
  - Pricing is genuinely localized German-market pricing (not a straight
    GBP->EUR unit conversion) -- e.g. Whoop 269 EUR/yr, Apple Watch 257 EUR,
    Garmin 315 EUR, Fitbit 93.99/163.99 EUR, all read directly off the
    product rows and cross-checked against the cost-comparison table.

JUDGMENT CALL (flagged, not silently applied): the footer legal block
(medical disclaimer / advertorial disclosure / copyright) does not exist as
a node under either German frame, exactly like the English frame. Rather
than fabricate a German legal/medical translation (a real compliance risk if
done wrong), this file reuses the EXACT SAME ENGLISH legal text verbatim,
matching the English step's own precedent of reusing v3's footer for
site-wide compliance consistency. This should be reviewed/translated by a
native-speaker/legal pass before this page is publicly promoted to a German
audience -- flagged explicitly here and in the completion report.
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
STEP_SLUG = "top-5-fitness-tracker-2026-de"
IMG = json.load(open("pagescore/.cache/rc_img_map.json"))

# Confirmed identical to the English step's hyperlinks -- the German Figma
# frame's own button/text hyperlink fields point at these SAME URLs, not
# localized .de domains.
PDP = "https://hlthtrack.co.uk/products/wearable-hlth-band"
# Same uploaded product video as the English step (real footage, same asset,
# uploaded via getSignedUrls+importImage under images_library -- products_files
# uploads aren't publicly reachable on the assets CDN, verified via a 403).
COST_VIDEO_URL = "https://assets.lightfunnels.com/account-90380/images_library/0cd469e1-9d83-4b0b-b330-80edab2d9c52.mp4"
TP  = "https://www.trustpilot.com/review/hlthtrack.com"

# ---- fonts ----
SERIF = "GelasioText, Georgia, serif"
SANS  = "Inter, InterFallback, sans-serif"

GELASIO_HEAD = (
    '<link rel="preload" as="font" type="font/woff2" crossorigin '
    'href="https://fonts.gstatic.com/s/gelasio/v14/cIfiMaFfvUQxTTqS3iKJkLGbI41wQL8Ilxcr8zHs9RbblYs.woff2">\n'
    '<link rel="preload" as="font" type="font/woff2" crossorigin '
    'href="https://fonts.gstatic.com/s/gelasio/v14/cIfiMaFfvUQxTTqS3iKJkLGbI41wQL_vkBcr8zHs9RbblYs.woff2">\n'
    '<style>'
    "@font-face{font-family:GelasioText;font-style:normal;font-weight:400;font-display:swap;"
    "src:url(https://fonts.gstatic.com/s/gelasio/v14/cIfiMaFfvUQxTTqS3iKJkLGbI41wQL8Ilxcr8zHs9RbblYs.woff2) format('woff2')}"
    "@font-face{font-family:GelasioText;font-style:normal;font-weight:700;font-display:swap;"
    "src:url(https://fonts.gstatic.com/s/gelasio/v14/cIfiMaFfvUQxTTqS3iKJkLGbI41wQL_vkBcr8zHs9RbblYs.woff2) format('woff2')}"
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
    '<style>img[title="hero"]{height:402px!important;width:100%%!important;object-fit:cover;aspect-ratio:auto}'
    '@media (max-width:767px){img[title="hero"]{height:196px!important}}'
    # QA: the unbroken DOI URL in Quellen citation 2 set a 293px intrinsic width
    # inside a 280px column, panning the whole page 19px sideways at 320. This is the
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
    # QA: this page is entirely German but the LF storefront theme emits
    # <html lang="en"> and exposes no per-step locale knob. This shim corrects it for
    # screen readers and in-browser translation; it does NOT change the SSR HTML that
    # crawlers read -- a real fix needs platform support (see plan, question 17).
    '<script>document.documentElement.lang="de";</script>\n'
    '<script>(function(){function f(){var h=document.querySelector(\'img[title="hero"]\');'
    'if(h){h.setAttribute("fetchpriority","high");h.setAttribute("loading","eager");}'
    'var lg=document.querySelector(\'img[title="logo"]\');if(lg)lg.removeAttribute("fetchpriority");}'
    'if(document.readyState!=="loading")f();else document.addEventListener("DOMContentLoaded",f);})();</script>\n') + LEGAL_MODALS

# ---- colors (measured, identical to English step) ----
DARK   = {"r":22,"g":24,"b":28,"a":1}
BODY   = {"r":74,"g":79,"b":87,"a":1}
MUTED  = {"r":154,"g":160,"b":168,"a":1}
BORDER = {"r":228,"g":230,"b":226,"a":1}
TABLEBG= {"r":247,"g":248,"b":246,"a":1}
PINK   = {"r":251,"g":238,"b":236,"a":1}
RED    = {"r":230,"g":57,"b":70,"a":1}
BLUE   = {"r":26,"g":95,"b":208,"a":1}
YELLOW_TAG = {"r":228,"g":236,"b":74,"a":1}
WHITE  = {"r":255,"g":255,"b":255,"a":1}
GOLD   = {"r":245,"g":179,"b":1,"a":1}
TP_GREEN = {"r":0,"g":182,"b":122,"a":1}
CHECK_GREEN = {"r":30,"g":158,"b":74,"a":1}
DASH_BORDER = {"r":185,"g":189,"b":196,"a":1}
SUPPORT_BG  = {"r":244,"g":244,"b":242,"a":1}
SUPPORT_TXT = {"r":107,"g":111,"b":118,"a":1}
HEADER_BG   = {"r":40,"g":40,"b":43,"a":1}

# ---- helpers (identical to English step) ----
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
    # QA: German compounds overflow at 320 ("DIE MIT SMARTWATCH-FUNKTIONEN" is
    # 258px in a 238px box). Keep nowrap on desktop, let it wrap on mobile.
    node["styles"].append({"prop":"whiteSpace","value":"normal","media":767})
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
            {"prop":"whiteSpace","value":"nowrap"},{"prop":"maxWidth","value":"100%"},
            # QA: "Verfügbarkeit des HLTH Band prüfen →" is 299px inside a 240px
            # button at 320 -- the German label is far longer than the EN original.
            {"prop":"whiteSpace","value":"normal","media":767}]
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
    # Same continuous-percentage green-fill logic verified for the English
    # step (universal Trustpilot green #00B67A, no rating-based color band).
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
    # Same presence rule verified on THIS German frame directly: desktop
    # teaser (145:1099... well 145:1099 is desktop teaser's icon under
    # 145:74/145:99), mobile teaser (145:1121) and all 5 mobile big-list rows
    # have it; all 5 desktop big-list rows do not.
    return '<span style="display:inline-block;margin-left:%gpx">%s</span>' % (gap, ext_link_icon(size, color))

def caption(t="(Bildnachweis: Marcus Pendleton / TechUnboxed)"):
    return text(t, size="13px", lh="19px", color=BODY, italic=True, font=SERIF)

def para(t, color=DARK):
    return text(t, size="18px", lh="29.7px", color=color, font=SERIF)

def video_block(src, poster=None, height="402px", mh="230px", radius="10px", border=True):
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
    inner = container([text(html, size="22px", lh="30.8px", weight="700", italic=True, font=SERIF,
        ls="-0.22px")],
        [{"prop":"borderStyle","value":"solid"},{"prop":"borderColor","value":RED},
         {"prop":"borderWidth","value":"0px 0px 0px 4px"},
         {"prop":"padding","value":{"top":"6px","bottom":"6px","left":"22px","right":"0px"}}])
    return col([inner], gap="0px", styles=[{"prop":"padding","value":{"top":"12px","bottom":"12px"}}])

def h2(content):
    return title(content, "28px", "35px", weight="700", color=DARK, ls="-0.28px", font=SERIF,
                 m={"fontSize":"22px","lineHeight":"27.5px","letterSpacing":"-0.22px"})

# ============================== HEADER (site chrome) ========================
support_bar = {"t":"Section","id":nid(),
    "styles":[{"prop":"backgroundColor","value":SUPPORT_BG},
              {"prop":"borderStyle","value":"solid"},{"prop":"borderColor","value":BORDER},
              {"prop":"borderWidth","value":"1px 0px 1px 0px"},
              {"prop":"padding","value":{"top":"9px","bottom":"9px","left":"12px","right":"12px"}}],
    "p":{"layout":"","dividerPosition":["top"],"horizontalFlip":False,
         "embedded_video":{"src":"","video_size":"stretch","video_position":"center"},
         # Verbatim from Figma node 145:17.
         "children":[text("Diese Seite finanziert sich über ihre Leser; über Links können wir Provisionen erhalten.",
             size="13px", lh="18px", color=SUPPORT_TXT, align="center", font=SANS)]}}

logo_bar = {"t":"Section","id":nid(),
    "styles":[{"prop":"backgroundColor","value":HEADER_BG},
              {"prop":"padding","value":{"top":"14px","bottom":"14px","left":"28px","right":"28px"}}],
    "p":{"layout":"","dividerPosition":["top"],"horizontalFlip":False,
         "embedded_video":{"src":"","video_size":"stretch","video_position":"center"},
         "children":[container([logo_img()],[{"prop":"lfDisplay","value":"flex"},
             {"prop":"justifyContent","value":"center"},{"prop":"width","value":"100%"}])]}}

# Verbatim from Figma nodes 145:34 (desktop) and 145:1053 (mobile) -- BOTH
# confirmed identical: one uniform gray (#4A4F57, Regular) run for
# "Start > Wearables > " (no separate lighter chevron color, unlike a first
# guess), then "Beste Fitness-Tracker 2026" in red (#E63946) Semibold. No
# embedded hyperlinks on the text itself -- the functional Home/Wearables
# links below are reused site-nav infrastructure, same as the English step's
# BREADCRUMB_RC, not fabricated editorial content.
BREADCRUMB_RC_DE = ('<a href="https://blog.techunboxed.co/" style="color:#4A4F57;text-decoration:none">Start</a>'
    ' <span style="color:#4A4F57">&gt;</span> '
    '<a href="https://blog.techunboxed.co/category/wearables" style="color:#4A4F57;text-decoration:none">Wearables</a>'
    ' <span style="color:#4A4F57">&gt;</span> '
    '<span style="color:#E63946;font-weight:600">Beste Fitness-Tracker 2026</span>')

header_site_bar = {"t":"Section","id":nid(),
    "styles":[{"prop":"borderStyle","value":"solid"},{"prop":"borderColor","value":BORDER},
              {"prop":"borderWidth","value":"0px 0px 1px 0px"},
              {"prop":"padding","value":{"top":"14px","bottom":"14px"}},
              # Desktop relies on the "boxed" layout's own auto-centering margins.
              # Mobile has no such margin, and Figma's own "header · site" frame
              # (node 145:1051) bakes in paddingLeft/Right:20 directly -- without
              # it the breadcrumb sat flush against the viewport edge.
              {"prop":"padding","value":{"left":"20px","right":"20px"},"media":767}],
    "p":{"layout":"boxed","dividerPosition":["top"],"horizontalFlip":False,
         "embedded_video":{"src":"","video_size":"stretch","video_position":"center"},
         "children":[text(BREADCRUMB_RC_DE, size="13px", lh="17px", font=SANS)]}}

# ============================== ARTICLE HEAD ================================
kids=[]
kids.append(title("Wir haben 1.850 € ausgegeben, um die 5 besten Fitness-Tracker 2026 zu testen. "
    "Der Außenseiter für 92 € hat gewonnen.",
    "40px","46px", weight="700", ls="-0.4px", font=SERIF, level="1",
    m={"fontSize":"28px","lineHeight":"32px","letterSpacing":"-0.28px"}))
kids.append(text("Der Newcomer misst, was eine 465-€-Uhr nicht kann, kostet im Angebot nur 92 € und hält "
    "fast einen Monat mit einer Akkuladung durch. Wir zeigen dir genau, was er kann und ob er zu dir passt.",
    size="20px", lh="30px", color=BODY, font=SERIF))

# tag row -- verbatim German labels (145:40 "Kaufberatung", 145:45 "Im Trend")
tag_guides = container([text("Kaufberatung", size="15px", lh="15px", color=WHITE, weight="700", font=SANS)],
    [{"prop":"backgroundColor","value":RED},{"prop":"borderRadius","value":"8px"},
     {"prop":"padding","value":{"top":"7px","bottom":"7px","left":"15px","right":"15px"}}])
trending_svg = ('<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="#16181C" stroke-width="2.5" '
    'stroke-linecap="round" stroke-linejoin="round"><polyline points="22 7 13.5 15.5 8.5 10.5 2 17"/>'
    '<polyline points="16 7 22 7 22 13"/></svg>')
tag_trending = container([rowf([
        {"t":"HtmlElement","id":nid(),"p":{"content":trending_svg},"styles":[{"prop":"flexShrink","value":"0"}]},
        text("Im Trend", size="15px", lh="15px", color=DARK, weight="700", font=SANS)],
    gap="6px", align="center")],
    [{"prop":"backgroundColor","value":YELLOW_TAG},{"prop":"borderRadius","value":"8px"},
     {"prop":"padding","value":{"top":"7px","bottom":"7px","left":"15px","right":"15px"}}])
kids.append(rowf([tag_guides, tag_trending], gap="10px", align="center", justify="flex-start",
    styles=[{"prop":"width","value":"fit-content"}]))
kids.append(sp(2))

# byline -- verbatim German (145:50 name, 145:51 role, 145:53 bio, 145:54 date)
byline_who = col([
    text('<span style="text-decoration:underline">Marcus Pendleton</span>',
         size="15.5px", lh="20px", color=DARK, weight="800", font=SANS),
    text("Leitender Autor", size="13.5px", lh="18px", color=BODY, font=SANS),
], gap="2px", styles=[{"prop":"width","value":"150px"},{"prop":"flexShrink","value":"0"}])
byline_bio = col([
    text('<span style="color:#4A4F57">Marcus ist leitender Autor bei TechUnboxed und testet die neuesten '
         'Smartwatches und Fitness-Tracker. </span><b style="color:#16181C;text-decoration:underline">Vollständige '
         'Bio lesen</b>',
         size="14.5px", lh="22px", font=SANS),
    text("Zuletzt aktualisiert am 18. Juli 2026", size="12.5px", lh="16px", color=MUTED, font=SANS),
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
kids.extend(figure(img_block("hero", height="402px", mh="196px", border=True)))
kids.append(sp(10))

# ---- qualifying questions (verbatim, 145:58-61) ----
kids.append(text("Möchtest du deine Gesundheit genau erfassen und verbessern?", size="18px", lh="29.7px",
    weight="700", font=SERIF))
kids.append(text("Suchst du einen Tracker, der deine Blutdrucktrends, deine Herzfrequenz und deinen Schlaf "
    "ohne monatliches Abo verfolgt?", size="18px", lh="29.7px", weight="700", font=SERIF))
kids.append(text("Suchst du etwas Einfaches und Bequemes, das für ganz normale Menschen gemacht ist?",
    size="18px", lh="29.7px", weight="700", font=SERIF))
kids.append(para("Wenn du bei einer dieser Fragen genickt hast, bist du hier richtig. Wir haben 1.850 € "
    "ausgegeben, um die beliebtesten Tracker zu kaufen und gegen das neue Band zu testen, das in Deutschland "
    "gerade viral geht."))
kids.append(sp(6))

# ============================== TEASER: Editor's Pick card ===================
def accordion_block(pros, cons):
    def row(mark, color, txt):
        return ('<div style="display:flex;gap:0;padding:2px 0">'
            '<span style="flex-shrink:0;width:20px;font-weight:700;color:%s">%s</span>'
            '<span style="color:#16181C">%s</span></div>') % (color, mark, txt)
    pros_html = "".join(row("&#10003;", "#1E9E4A", p) for p in pros)
    cons_html = "".join(row("&#10007;", "#E63946", c) for c in cons)
    body = ('<div style="display:none;padding-top:8px" class="rc-acc-body">'
        '<div style="display:flex;flex-direction:column;font-family:%s;font-size:13px;line-height:19px">'
        '<b style="color:#16181C;margin-bottom:2px">Vorteile</b>%s'
        '<div style="height:7px"></div>'
        '<b style="color:#16181C;margin-bottom:2px">Nachteile</b>%s'
        '</div></div>') % (SANS, pros_html, cons_html)
    summary = ('<div onclick="var b=this.nextElementSibling;b.style.display=b.style.display===\'none\'?\'block\':\'none\';'
        'var c=this.querySelector(\'.rc-chev\');c.style.transform=b.style.display===\'none\'?\'rotate(0deg)\':\'rotate(180deg)\';" '
        'style="display:flex;align-items:center;gap:8px;cursor:pointer;padding:2px 0;font-family:%s;font-size:13px;font-weight:600;color:#4A4F57">'
        'Vor- &amp; Nachteile <svg class="rc-chev" width="10" height="10" viewBox="0 0 10 10" fill="none" '
        'stroke="#E63946" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" '
        'style="transition:transform .2s"><polyline points="1 3 5 7 9 3"/></svg></div>') % SANS
    return {"t":"HtmlElement","id":nid(),"p":{"content":summary+body},"styles":[{"prop":"width","value":"100%"}]}

# Verbatim from Figma node 145:62 (desktop teaser accordion) -- a 6-pro/2-con
# subset of the full 8-pro/2-con big-list-row set, same subsetting pattern as
# the English teaser.
TEASER_PROS = ["Kein Abo, keine gesperrten Funktionen", "Bestätigte Akkulaufzeit von 30 Tagen",
    "Misst Blutdrucktrends, Ruhepuls, HRV &amp; SpO2", "Vollständige Schlafphasen (Tiefschlaf, REM, Leichtschlaf)",
    "Leichtes 18-g-Design ohne Display", "Kein Größen-Set – es ist ein Armband, es passt"]
TEASER_CONS = ["Neues Unternehmen – häufig ausverkauft", "Kein integriertes GPS (nutzt dein Smartphone)"]

def rank_card_desktop():
    thumb = container([img_block("hlth_thumb", height="120px", radius="8px", fit="cover")],
        [{"prop":"width","value":"120px"},{"prop":"flexShrink","value":"0"}])
    badge = rowf([
        inline_text(STAR, size="15px", lh="15px", color=GOLD, weight="700", font=SANS),
        _nowrap(inline_text("REDAKTIONSTIPP · TESTSIEGER", size="12px", lh="15px", color=DARK, weight="800", font=SANS,
             ls="1.2px")),
    ], gap="6px", align="center", styles=[{"prop":"width","value":"fit-content"}])
    tprow = rowf([
        text(tp_stars(4.6, 19) +
             '&nbsp;&nbsp;<a href="%s" target="_blank" style="color:#16181C;font-weight:800;font-size:15px;'
             'text-decoration:none">4,6</a>' % TP + tp_ext(13, 8),
             size="15px", lh="19px", font=SANS),
    ], gap="8px", align="center", styles=[{"prop":"width","value":"fit-content"}])
    main = col([
        badge, sp(4),
        text("HLTH Band 1.0", size="21px", lh="27px", color=DARK, weight="700", font=SERIF), sp(6),
        tprow, sp(8),
        accordion_block(TEASER_PROS, TEASER_CONS),
    ], gap="0px", styles=[{"prop":"flex","value":"1"},{"prop":"minWidth","value":"0"}])
    price_row = text('<span style="font-weight:800;font-size:20px;color:#16181C">92 €</span>&nbsp;'
                      '<span style="text-decoration:line-through;color:#4A4F57;font-size:14px">185 €</span>',
                 size="20px", lh="26px", align="center", font=SANS)
    buy = col([
        button("Bei HLTH ansehen", href=PDP, full=True), sp(10),
        price_row, sp(3),
        text("Kostenloser Versand", size="12.5px", lh="17px", color=BODY, align="center", font=SANS),
    ], gap="0px", styles=[{"prop":"width","value":"200px"},{"prop":"flexShrink","value":"0"},{"prop":"alignItems","value":"center"}])
    row = rowf([thumb, main, buy], gap="20px", align="flex-start",
        styles=[{"prop":"padding","value":{"top":"22px","bottom":"22px","left":"20px","right":"20px"}}])
    return container([row], [{"prop":"width","value":"100%"},{"prop":"backgroundColor","value":WHITE},
        {"prop":"borderRadius","value":"14px"},{"prop":"borderStyle","value":"solid"},
        {"prop":"borderColor","value":BORDER},{"prop":"borderWidth","value":"1px"},
        {"prop":"lfDisplay","value":"none","media":767}])

def tp_wordmark(size=15, gap="7px"):
    return rowf([
        inline_text(STAR, size="%dpx"%size, lh="%dpx"%size, color=TP_GREEN, weight="700", font=SANS),
        _nowrap(inline_text("Trustpilot", size="%dpx"%round(size*0.8), lh="%dpx"%round(size*1.0), color=DARK, weight="700", font=SANS)),
    ], gap=gap, align="center", styles=[{"prop":"width","value":"fit-content"}])

def rank_card_mobile():
    # Verbatim from Figma node 145:1082 (mobile teaser): dark header bar with
    # red "REDAKTIONSTIPP" pill (left) and "⭐ Testsieger" text (right,
    # separate node -- not the combined "REDAKTIONSTIPP · TESTSIEGER" string
    # used on desktop).
    header_bar = rowf([
        container([_nowrap(text("REDAKTIONSTIPP", size="10.5px", lh="13px", color=WHITE, weight="800", font=SANS, ls="0.7px"))],
            [{"prop":"backgroundColor","value":RED},{"prop":"borderRadius","value":"5px"},
             {"prop":"padding","value":{"top":"5px","bottom":"5px","left":"9px","right":"9px"}},
             {"prop":"width","value":"fit-content"},{"prop":"flexShrink","value":"0"}]),
        _nowrap(inline_text('<span style="color:#4A4F57">⭐</span> <span style="color:#FFFFFF">Testsieger</span>',
             size="12.5px", lh="16px", weight="700", font=SANS)),
    ], gap="0px", justify="space-between", align="center",
        styles=[{"prop":"width","value":"100%"},{"prop":"backgroundColor","value":DARK},
                {"prop":"borderRadius","value":"14px 14px 0px 0px"},
                {"prop":"padding","value":{"top":"14px","bottom":"14px","left":"20px","right":"20px"}}])

    tp_row_mini = rowf([
        text(tp_stars(4.6, 14) +
             '&nbsp;<a href="%s" target="_blank" style="color:#16181C;font-weight:800;font-size:12px;'
             'text-decoration:none">4,6</a>' % TP + tp_ext(7.46, 4.6),
             size="12px", lh="15px", font=SANS),
    ], gap="8px", align="center", styles=[{"prop":"width","value":"fit-content"}])
    name = text("HLTH Band 1.0", size="21px", lh="27px", color=DARK, weight="700", font=SERIF)
    text_col = col([tp_wordmark(13), sp(6), tp_row_mini, sp(7), name, sp(14),
        accordion_block(TEASER_PROS, TEASER_CONS)], gap="0px",
        styles=[{"prop":"flex","value":"1"},{"prop":"minWidth","value":"0"}])
    thumb = container([img_block("hlth_thumb", height="96px", radius="8px", fit="contain")],
        [{"prop":"width","value":"96px"},{"prop":"flexShrink","value":"0"}])
    top_row = rowf([text_col, thumb], gap="14px", align="flex-start")
    price_row = rowf([
        inline_text('<span style="font-weight:800;font-size:20px;color:#16181C">92 €</span>&nbsp;&nbsp;'
             '<span style="text-decoration:line-through;color:#4A4F57;font-size:14px">185 €</span>',
             size="20px", lh="26px", font=SANS),
        inline_text("Kostenloser Versand", size="12.5px", lh="17px", color=BODY, font=SANS),
    ], gap="0px", justify="space-between", align="center")
    buy_block = col([
        button("Bei HLTH ansehen", href=PDP, full=True), sp(4),
        price_row,
    ], gap="0px")
    body_ = col([top_row, sp(10), buy_block],
        gap="0px", styles=[{"prop":"padding","value":{"top":"20px","bottom":"20px","left":"20px","right":"20px"}}])
    st=[{"prop":"lfDisplay","value":"none"},{"prop":"lfDisplay","value":"flex","media":767},
        {"prop":"flexDirection","value":"column"},{"prop":"gap","value":"0px"},
        {"prop":"width","value":"100%"},
        {"prop":"backgroundColor","value":WHITE},{"prop":"borderRadius","value":"14px"},
        {"prop":"borderStyle","value":"solid"},{"prop":"borderColor","value":BORDER},
        {"prop":"borderWidth","value":"1px"}]
    return {"t":"Container","id":nid(),"styles":st,"p":{"children":[header_bar, body_]}}

kids.append(rank_card_desktop())
kids.append(rank_card_mobile())
kids.append(sp(28))

kids.append(text("Unser Favorit nach 30 Tagen im Test. Der vollständige Vergleich aller fünf Geräte steht "
    "weiter unten.", size="14px", lh="22px", color=BODY, align="center", font=SERIF))
kids.append(text('<span style="font-weight:700">Seit das </span>'
    '<a href="%s" target="_blank" style="font-weight:700;color:#1A5FD0;text-decoration:underline">HLTH Band</a>'
    '<span style="font-weight:700"> im April auf den Markt kam,</span> ist es der Tracker, nach dem uns Leser '
    "immer wieder schreiben. Elf E-Mails in einer einzigen Woche waren es zeitweise. Und nach sechs Jahren "
    "Wearable-Tests habe ich gelernt, allem zu misstrauen, was so schnell gehypt wird." % PDP,
    size="18px", lh="29.7px", font=SERIF))
kids.append(para('Unser Test hat bestätigt, was viele schon ahnen. <span style="font-weight:700">Am teuersten '
    'heißt nicht automatisch am besten.</span> Der Newcomer hat sich bei den Dingen durchgesetzt, die hier '
    "wirklich zählen: konstante Daten, eine Akkulaufzeit, über die du nicht mehr nachdenkst, und die "
    "Gesamtkosten über zwei Jahre. Und er hat keine einzige Funktion hinter monatlichen Gebühren versteckt."))
kids.append(text('<span style="font-weight:700">Der Sieger: das </span>'
    '<a href="%s" target="_blank" style="font-weight:700;color:#1A5FD0;text-decoration:underline">HLTH Band</a>'
    '<span style="font-weight:700">.</span> Der Newcomer für 92 € hat jeden großen Namen in diesem Test '
    "geschlagen. Hier siehst du, wie alle fünf abschneiden, warum der Außenseiter gewonnen hat und wer "
    "ehrlicherweise besser etwas anderes kaufen sollte." % PDP,
    size="18px", lh="29.7px", font=SERIF))
kids.append(sp(28))

# ============================== HOW WE TESTED ================================
kids.append(h2("So haben wir getestet"))
kids.append(para("Wir haben jedes Band einen ganzen Monat lang Tag und Nacht getragen. Gleiche Handgelenke, "
    "gleiche Wochen, gleicher Alltag. Das haben wir gemessen:"))
kids.append(sp(4))

METHOD_ITEMS = [
    ("Konstanz der Messwerte", "Wir haben Herzfrequenz, HRV und Blutdrucktrends an denselben Tagen direkt "
     "verglichen und die Ruheblutdruckwerte unter gleichen Bedingungen mit einer medizinischen "
     "Blutdruckmanschette abgeglichen."),
    ("Schlafmessung", "Wir haben die Schlafphasen jedes Geräts 30 Morgen in Folge mit unserem tatsächlichen "
     "Befinden am Morgen abgeglichen."),
    ("Akku, ganz real", "Wir haben jeden Akku mit allen Sensoren komplett leerlaufen lassen, inklusive SpO2 "
     "die ganze Nacht. Keine Laborbedingungen. Echte Wochen, echte Workouts, echte Reisen."),
    ("Echte Kosten über 2 Jahre", "Wir haben zusammengerechnet, was jedes Gerät über zwei Jahre wirklich "
     "kostet, inklusive jedem Abo und jeder gesperrten Funktion."),
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
kids.append(h2("Die besten Modelle, getestet von TechUnboxed"))
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

def rank_row(name, badge_label, has_star, tp_rating, tp_rating_text, pros_cons, score, btn_label, btn_href,
             price_html, sub_text, thumb_key, tp_url, thumb_h="120px", is_last=False):
    badge_children = []
    if has_star:
        badge_children.append(inline_text(STAR, size="15px", lh="15px", color=GOLD, weight="700", font=SANS))
    badge_children.append(_nowrap(inline_text(badge_label, size="12px", lh="15px",
        color=(DARK if has_star else BODY), weight="800", font=SANS, ls="1.2px")))
    badge = rowf(badge_children, gap="6px", align="center", styles=[{"prop":"width","value":"fit-content"}])

    # Desktop big-list rows carry no Trustpilot hyperlink/icon in this German
    # frame either (confirmed directly, e.g. node 145:171/145:249) -- plain text.
    tprow = text(tp_stars(tp_rating, 19) +
        '&nbsp;&nbsp;<span style="color:#16181C;font-weight:800;font-size:15px">%s</span>' % tp_rating_text,
        size="15px", lh="19px", font=SANS)

    main = col([
        badge, sp(4),
        text(name, size="21px", lh="27px", color=DARK, weight="700", font=SERIF), sp(6),
        tprow, sp(9),
        rank_li(pros_cons),
    ], gap="0px", styles=[{"prop":"flex","value":"1"},{"prop":"minWidth","value":"0"}])

    buy = col([
        text("UNSERE WERTUNG", size="11px", lh="15px", color=BODY, weight="800", font=SANS, ls="1.43px", align="center"),
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

def rank_row_mobile(name, badge_label, has_star, tp_rating, tp_rating_text, pros_cons, score, btn_label, btn_href,
             price_html, sub_text, thumb_key, tp_url, thumb_h="120px", is_last=False):
    badge_children = []
    if has_star:
        badge_children.append(inline_text(STAR, size="15px", lh="15px", color=GOLD, weight="700", font=SANS))
    badge_children.append(_nowrap(inline_text(badge_label, size="12px", lh="15px",
        color=(DARK if has_star else BODY), weight="800", font=SANS, ls="1.2px")))
    badge = rowf(badge_children, gap="6px", align="center", justify="center",
        styles=[{"prop":"width","value":"100%"}])

    score_row = rowf([
        inline_text("UNSERE WERTUNG", size="11px", lh="15px", color=BODY, weight="800", font=SANS, ls="1.43px"),
        inline_text(score_block(score)["p"]["content"], size="34px", lh="34px"),
    ], gap="10px", align="baseline", justify="center", styles=[{"prop":"width","value":"100%"}])

    mobile_thumb_h = round(240 * int(thumb_h.rstrip("px")) / 120)
    thumb = container([img_block(thumb_key, height="%dpx"%mobile_thumb_h, radius="8px", fit="cover")],
        [{"prop":"width","value":"240px"},{"prop":"margin","value":{"left":"auto","right":"auto"}}])

    # Mobile big-list rows DO carry the hyperlink + external-link icon
    # (confirmed directly on this German frame, e.g. node 145:1195/145:1275).
    tprow = text(tp_stars(tp_rating, 19) +
            '&nbsp;&nbsp;<a href="%s" target="_blank" style="color:#16181C;font-weight:800;font-size:15px;'
            'text-decoration:none">%s</a>' % (tp_url, tp_rating_text) + tp_ext(13, 8),
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

# All fields below read verbatim from Figma nodes 145:171/249/320/391/468
# (desktop) and 145:1195/1275/1348/1421/1500 (mobile) -- genuinely localized
# German-market EUR pricing, not a straight GBP->EUR unit swap.
# ---- Amazon DE (QA) ----------------------------------------------------------
# This page prices in EUR, so its Amazon links now go to amazon.de. Every ASIN below
# was fetched from amazon.de and confirmed to be a live product page; the US Apple
# ASIN (B0DGHQ2QH6) 404s on .de and is remapped to the German SE 3 GPS 40mm listing.
#
# !! AMZ_TAG is still the US associate tag. A "-20" tag does not track on amazon.de,
# !! so these clicks currently earn nothing. Replace with the DE tag (usually "-21").
AMZ_TAG = "techunboxed04-20"
AMZ = {
    "whoop":  "https://www.amazon.de/dp/B0DY2SWV16",
    "apple":  "https://www.amazon.de/dp/B0FQFL725M",
    "garmin": "https://www.amazon.de/dp/B0F38FCHD2",
    "fitbit": "https://www.amazon.de/dp/B0CC62ZG1M",
}
def amz(key): return "%s?tag=%s" % (AMZ[key], AMZ_TAG)

RANK_ROWS = [


    dict(name="1. HLTH Band 1.0", badge_label="BESTE GESAMTWERTUNG", has_star=True, tp_rating=4.6, tp_rating_text="4,6",
        pros_cons=[(True,"Kein Abo, keine gesperrten Funktionen"),(True,"Bestätigte Akkulaufzeit von 30 Tagen"),
            (True,"Misst Blutdruck, Ruhepuls, HRV &amp; SpO2"),(True,"Vollständige Schlafphasen (Tiefschlaf, REM, Leichtschlaf)"),
            (True,"Multi-Wellenlängen-PPG"),(True,"Adaptives Energiemanagement"),
            (True,"Leichtes 18-g-Design ohne Display"),(True,"Wasserdicht (1 ATM)"),
            (False,"Neues Unternehmen – häufig ausverkauft"),(False,"Kein integriertes GPS (nutzt dein Smartphone)")],
        score="9.9/10", btn_label="Bei HLTH ansehen", btn_href=PDP,
        price_html='<span style="font-weight:800;font-size:20px;color:#16181C">92 €</span>&nbsp;'
            '<span style="text-decoration:line-through;color:#4A4F57;font-size:14px">185 €</span>',
        sub_text="Kostenloser Versand", thumb_key="hlth_thumb", thumb_h="120px",
        tp_url="https://www.trustpilot.com/review/hlthtrack.com"),
    dict(name="2. Whoop 5.0 Peak", badge_label="DER MIT ABO", has_star=False, tp_rating=3.2, tp_rating_text="3,2",
        pros_cons=[(True,"Ausgezeichnete Recovery- &amp; Belastungsanalyse"),(True,"Bequemes Armband ohne Display"),
            (True,"Misst HRV, Schlaf &amp; SpO2"),(True,"Multi-Wellenlängen-PPG"),
            (False,"269 € pro Jahr, Jahr für Jahr"),(False,"Gerät funktioniert nicht mehr bei Kündigung"),
            (False,"Blutdruckmessung erst ab 420-€-Tarif"),(False,"Häufige Beschwerden über die Herzfrequenzmessung bei 5.0")],
        score="9.0/10", btn_label="Zu Amazon",
        btn_href=amz("whoop"),
        price_html='<span style="font-weight:800;font-size:20px;color:#16181C">269 €/Jahr</span>',
        sub_text="2–3 Tage Lieferzeit mit Prime", thumb_key="whoop_thumb", thumb_h="120px",
        tp_url="https://www.trustpilot.com/review/whoop.com"),
    dict(name="3. Apple Watch SE 3", badge_label="DIE MIT SMARTWATCH-FUNKTIONEN", has_star=False, tp_rating=1.8, tp_rating_text="1,8",
        pros_cons=[(True,"Erstklassige App &amp; smarte Funktionen"),(True,"Gute Kommunikationsmöglichkeiten"),
            (True,"Präzise Herzfrequenzmessung &amp; integriertes GPS"),(True,"Schlafapnoe-Warnungen &amp; Handgelenktemperatur"),
            (False,"Kein EKG, keine Sauerstoffmessung, kein Blutdruck"),(False,"Funktioniert nur mit iPhone"),
            (False,"Nächtliches Laden unterbricht die Schlafmessung"),(False,"Wir haben ständig draufgeschaut")],
        score="7.9/10", btn_label="Zu Amazon",
        btn_href=amz("apple"),
        price_html='<span style="font-weight:800;font-size:20px;color:#16181C">257 €</span>',
        sub_text="7–12 Tage Lieferzeit", thumb_key="apple_thumb", thumb_h="120px",
        tp_url="https://au.trustpilot.com/review/applewatch.com"),
    dict(name="4. Garmin Vivoactive 6", badge_label="DIE FÜR SPORTLER", has_star=False, tp_rating=1.5, tp_rating_text="1,5",
        pros_cons=[(True,"Zuverlässiges GPS &amp; Sportmodi"),(True,"Präzise Fitnessmessung"),
            (True,"7 Tage Akkulaufzeit"),(True,"Kostenlose Garmin-Connect-App"),
            (False,"Einmalige Investition von 293 €"),(False,"Umständliche App-Bedienung"),
            (False,"Keine Blutdruckmessung"),(False,"Kein EKG, kein Höhenmesser"),
            (False,"Kein Lautsprecher/Mikrofon für Anrufe"),(False,"Klobig und unbequem beim Schlafen")],
        score="7.5/10", btn_label="Zu Amazon",
        btn_href=amz("garmin"),
        price_html='<span style="font-weight:800;font-size:20px;color:#16181C">315 €</span>',
        sub_text="2–3 Tage Lieferzeit mit Prime", thumb_key="garmin_thumb", thumb_h="120px",
        tp_url="https://www.trustpilot.com/review/www.garmin.com"),
    dict(name="5. Fitbit Charge 6", badge_label="DIE FÜR DEN MAINSTREAM", has_star=False, tp_rating=1.6, tp_rating_text="1,6",
        pros_cons=[(True,"Integriertes EKG &amp; SpO2"),(True,"Kompaktes, leichtes Armband"),
            (True,"Integriertes GPS + schwimmfest"),
            (False,"Datenschutzbedenken nach der Google-Übernahme"),
            (False,"Schlafwert &amp; Readiness nur mit Premium für 11,99 €/Monat"),
            (False,"Reale Akkulaufzeit nur 2–5 Tage"),(False,"Keine Blutdruckmessung"),
            (False,"GPS unzuverlässig"),(False,"Datenverlust bei der Google-Migration")],
        score="5.9/10", btn_label="Zu Amazon",
        btn_href=amz("fitbit"),
        price_html='<span style="font-weight:800;font-size:20px;color:#16181C">93,99 €</span>&nbsp;'
            '<span style="text-decoration:line-through;color:#4A4F57;font-size:14px">163,99 €</span>',
        sub_text="2–3 Tage Lieferzeit mit Prime", thumb_key="fitbit_thumb", thumb_h="147px",
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
kids.append(h2("Warum das HLTH Band unser Sieger ist"))
kids.append(sp(10))
kids.extend(figure(img_block("why_hlth_won", height="402px", mh="230px", border=True)))
kids.append(sp(10))
kids.append(para('Das HLTH Band überzeugt durch sein simples Design und seine ernstzunehmenden '
    'Gesundheitsfunktionen. Es hielt konstant mit Geräten mit, die <span style="font-weight:700">drei- bis '
    'fünfmal so teuer</span> sind. Sein Multi-Wellenlängen-PPG-Sensor geht dabei einen Schritt weiter als die '
    'Einzelwellenlängen-Sensoren der meisten Budget-Bänder und liefert rund um die Uhr fortlaufende Messwerte '
    'zu Blutdrucktrends, Herzfrequenz, HRV und Ruhepuls.'))
kids.append(para('Es ist eines der wenigen Bänder auf dem Markt, das <span style="font-weight:700">Blutdrucktrends '
    'ohne Abo erfasst</span>. Also genau die Art von Langzeitbild, das du zu deinem nächsten Arztbesuch '
    'mitnehmen kannst, kostenlos, jeden einzelnen Tag. Und es zeichnet vollständige Schlafphasen auf, über '
    'einen Akku, der in unserem Test <span style="font-weight:700">27 Tage durchgehalten hat</span>. Das sind '
    '27 Nächte lückenloser Schlafdaten, mit denen Apple Watch und Fitbit durch ihr nächtliches Laden schlicht '
    'nicht mithalten können.'))
kids.append(para('Normalerweise ist dieses Maß an Überwachung nur mit einer Mitgliedschaft für 269 € pro Jahr '
    'zu haben oder steckt in einer Smartwatch, die jede Nacht leer ist. Das HLTH Band ist die Ausnahme. Für '
    '<span style="font-weight:700">92 €</span> ist es der leistungsfähigste bildschirmlose Gesundheitstracker, '
    'den wir dieses Jahr getestet haben.'))
kids.append(callout("Es ist eines der wenigen Bänder, zu welchem Preis auch immer, das Blutdrucktrends ohne "
    "Abo erfasst."))
kids.append(sp(16))

# ============================== CUFF / BLOOD PRESSURE TEST ====================
kids.append(h2("Wir haben erwartet, dass es im Test versagt. Hat es nicht."))
kids.append(sp(10))
kids.extend(figure(img_block("cuff_test", height="402px", mh="230px", border=True)))
kids.append(sp(10))
kids.append(para('Als wir das HLTH Band ausgepackt haben, ist uns als Erstes das Gewicht aufgefallen. Mit '
    '<span style="font-weight:700">18 Gramm</span> sitzt es am Handgelenk wie ein Gummiarmband. Das Armband '
    'hatte in den ersten ein, zwei Tagen einen leichten Gummigeruch, der wieder verschwunden ist. Nach einer '
    'Woche im Wechsel zwischen Apple Watch und Garmin fühlte es sich an, als würde man eine Last ablegen, als '
    'wir es wieder angelegt haben. Ich habe es den ganzen Monat am linken Handgelenk getragen, beim Training am '
    'Bizeps-Band.'))
kids.append(para('Doch Tragekomfort bringt nichts ohne Konstanz, also haben wir die Behauptung getestet, die am '
    'meisten zählt: den Blutdruck. Jeder Kardiologe, den wir befragt haben, war sich einig, dass eine einzelne '
    'Momentmessung fast nichts aussagt, weil sich der Blutdruck ständig verändert, durch Stress, Bewegung, '
    'Essen und Schlaf. <span style="font-weight:700">Nur ein längerfristiger Trend zeigt ein echtes '
    'Muster.</span> Also haben wir das Band unter Ruhebedingungen mit einer medizinischen Blutdruckmanschette '
    'verglichen, und das HLTH Band lag über mehrere Sitzungen hinweg konstant innerhalb der empfohlenen '
    '±10 mmHg.'))
kids.append(para("Das ist wichtig, weil eine Manschette nur einen einzigen Moment erfasst. Das HLTH Band "
    "misst den ganzen Tag über, während du arbeitest, schläfst und dich erholst. Dieses fortlaufende Bild "
    "zeigt dir Muster, die eine einzelne Messung niemals zeigen kann. Kein anderes Gerät in unserem Test bot "
    "durchgehende Blutdrucktrends zu irgendeinem Preis, mit Ausnahme von Whoop, dort aber nur im Tarif für "
    "420 € pro Jahr."))
kids.append(callout("Fast einen Monat mit einer einzigen Ladung. Selbst mit allen Sensoren, die die ganze "
    "Nacht laufen, hat unseres 27 Tage durchgehalten, dann steckst du es kurz an und vergisst es wieder. Eine "
    "Smartwatch dagegen ist jede einzelne Nacht leer."))
kids.append(sp(16))

# ============================== THE APP ======================================
kids.append(h2("Die App hat mich wirklich überzeugt"))
kids.append(sp(10))
kids.append(para("HLTH ist hier einen anderen Weg gegangen als die großen Marken. Statt die App so kompliziert "
    "wie möglich aussehen zu lassen, ist sie darauf ausgelegt, extrem übersichtlich zu sein. Das Band misst "
    "Herzfrequenz, HRV, Blutdruck, Blutsauerstoff, Schlafphasen, Stress und Workouts. Den ganzen Tag, die "
    "ganze Nacht. Aber Messen ist nur die halbe Arbeit. Die Daten müssen einfach zu lesen sein, und genau hier "
    "gewinnt das Band ganz still und leise."))
kids.extend(figure(img_block("app_home", radius="10px", border=True, fit="contain")))
kids.append(sp(10))
kids.append(para("Du öffnest die App und der Startbildschirm zeigt dir alles auf einen Blick. Oben die "
    "Schritte. Darunter Herzfrequenz, Schlaf, Blutdruck und Blutsauerstoff, jeweils in einer eigenen Karte mit "
    "dem aktuellsten Wert ganz vorne. Kein Durchwühlen von Menüs. Der Blick darauf wurde für mich zum "
    "Morgenritual, während der Wasserkocher lief."))
kids.append(callout("Weil es nie über Nacht geladen werden muss, ist es in jeder einzelnen Nacht am "
    "Handgelenk, Daten, die eine Apple Watch am Ladekabel schlicht nicht erfassen kann."))
kids.extend(figure(img_block("app_bp", radius="10px", border=True, fit="contain")))
kids.append(sp(10))
kids.append(text('Tippe auf eine Karte und sie öffnet sich. Hier die Blutdruckansicht. Oben ein großer Wert, '
    'darunter ein vollständiges Diagramm, wie er sich über den Tag bewegt hat. Orange Linie für systolisch, '
    'lila für diastolisch. Jeder Anstieg und jedes Absinken, Stunde für Stunde, mit einem Normalbereich '
    'darunter, damit du weißt, wie gut aussieht, ohne es googeln zu müssen. Und jeder Bildschirm folgt '
    'demselben Aufbau. Einmal verstanden, verstehst du die ganze App.',
    size="18px", lh="29.7px", font=SERIF))
kids.extend(figure(img_block("app_sleep", radius="10px", border=True, fit="contain")))
kids.append(sp(10))
kids.append(text('Den Schlaf haben wir am häufigsten geprüft. Er teilt deine Nacht in Leicht-, Tief- und '
    'REM-Schlaf auf, mit den Gesamtstunden ganz oben. Ein Blick genügt, um zu wissen, ob du dich erholt hast '
    'oder nur dagelegen bist. Auch die Herzdaten gehen tiefer als eine einzelne Zahl. Ruhe- und '
    'Live-Herzfrequenz in einem Ganztagesdiagramm. Workouts in fünf Zonen aufgeteilt, wobei die Liste der '
    'Sportarten kürzer ist als bei Garmin, gut zu wissen, wenn du etwas Ausgefallenes machst. HRV über Nacht, '
    'das Erholungssignal, das die meisten Tracker auslassen. Blutsauerstoff als einfacher Prozentwert. Alles '
    'läuft im Hintergrund, ganz ohne Brustgurt.', size="18px", lh="29.7px", font=SERIF))
kids.append(sp(16))

# ============================== BICEP STRAP ==================================
kids.append(h2("Das Bizeps Band ist ein tolles Extra"))
kids.append(sp(10))
kids.extend(figure(img_block("bicep_strap", height="402px", mh="230px", border=True)))
kids.append(sp(10))
kids.append(para('Hier ist eine einfache Regel zu Wearables am Handgelenk, über die die großen Marken kaum '
    'sprechen: <span style="font-weight:700">Je weniger sich der Sensor bewegt, desto genauer sind deine '
    'Messwerte.</span> Dein Handgelenk ist das aktivste Gelenk, das du hast. Es dreht, beugt und schwingt bei '
    'jedem Schritt, und all diese Bewegung ist Störrauschen, gegen das sich der Sensor durchsetzen muss.'))
kids.append(para('Dein Bizeps bewegt sich im Vergleich dazu kaum. Genau das macht das mitgelieferte Bizeps-Band '
    'zu einer so cleveren Ergänzung. Befestigst du dasselbe Band beim Laufen oder Training am Oberarm, sitzt es '
    'ruhig am Muskel, was <span style="font-weight:700">gleichmäßigere Messwerte bedeutet, genau dann, wenn '
    'dein Körper am stärksten gefordert ist</span>. Wir haben es im Alltag am Handgelenk getragen und beim '
    'Training auf den Bizeps gewechselt. Der Wechsel dauert etwa zehn Sekunden.'))
kids.append(sp(16))

# ============================== COST COMPARISON ==============================
kids.append(h2("Was wird dich das wirklich kosten?"))
kids.append(sp(10))
kids.extend(figure(video_block(COST_VIDEO_URL, poster=IMG["cost_video_still"]["src"],
    height="402px", mh="230px", border=True),
    cap_text="(Videonachweis: Marcus Pendleton / TechUnboxed)"))
kids.append(sp(10))
kids.append(para("Das hängt ganz davon ab, für welches Gerät du dich entscheidest. Es lohnt sich, das "
    "durchzurechnen, denn der Preis auf dem Etikett ist nur die halbe Wahrheit."))
kids.append(sp(10))

# Verbatim from Figma node 145:595 (all values in EUR, genuinely localized
# German-market pricing).
COST_COLUMNS = ["WHOOP 5.0 PEAK", "APPLE WATCH SE 3", "FITBIT CHARGE 6", "GARMIN VIVOACTIVE 6", "HLTH BAND"]
COST_ROWS = [
    ("Jahr 1", ["269 €", "257 €", "234 €", "315 €", "92 €"]),
    ("Jahr 2", ["269 €", "0 €", "141 €", "0 €", "0 €"]),
    ("Gesamt über 2 Jahre", ["538 €", "257 €", "375 €", "315 €", "92 €"]),
    ("Abo", ["Pflicht", "Nein", "Optional", "Nein", "Nein"]),
]
def _cost_table_html():
    pct_label, pct_col = 19.4, 16.12
    m_pct_label, m_pct_col = 25.71, 14.858
    cols_html = ('<col class="rc-ct-c0">') + \
        ("".join('<col class="rc-ct-c">' for _ in COST_COLUMNS))
    th = '<th class="rc-ct-th">GERÄT</th>'
    th += "".join('<th class="rc-ct-th">%s</th>' % c for c in COST_COLUMNS)
    body_rows = ""
    for label, vals in COST_ROWS:
        is_sub_row = (label == "Abo")
        row_cls = " rc-ct-sub" if is_sub_row else ""
        tds = '<td class="rc-ct-label%s">%s</td>' % (row_cls, label)
        for i, v in enumerate(vals):
            is_hlth = (i == len(vals) - 1)
            cls = "rc-ct-val" + (" rc-ct-hlth" if is_hlth else "") + row_cls
            tds += '<td class="%s">%s</td>' % (cls, v)
        body_rows += "<tr>%s</tr>" % tds
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
kids.append(callout("92 €, einmalig. Über zwei Jahre kostet das Whoop 538 €, und es hört genau an dem Tag auf "
    "zu funktionieren, an dem du kündigst."))
kids.append(sp(10))

kids.append(para('<span style="font-weight:700">Worauf verzichtest du also für 92 €?</span> Ehrlich gesagt auf '
    'drei Dinge. Es gibt <span style="font-weight:700">kein Display</span>, du prüfst alles in der App, was für '
    'uns eher ein Vorteil als ein Nachteil war. Es gibt <span style="font-weight:700">kein integriertes GPS</span>, '
    'das Band nutzt für Routen dein Smartphone, wer also ohne Handy läuft, wird es vermissen. Und kaum jemand '
    'wird das Logo erkennen, denn <span style="font-weight:700">HLTH ist ein junges Unternehmen</span>. Wenn das '
    'für dich in Ordnung ist, ist das HLTH Band vielleicht genau die richtige Wahl.'))
kids.append(para('<span style="font-weight:700">Preis-Check:</span> Der Preis von 92 € ist ein '
    'Einführungsangebot, reduziert von 185 €. Wir haben ihn am 1. Juli und erneut am 18. Juli 2026 geprüft, und '
    'der Rabatt war beide Male aktiv. HLTH stellt das Band in kleinen Chargen her, und frühere Chargen waren '
    'bereits ausverkauft. Prüfe daher die aktuelle Verfügbarkeit, bevor auch diese Charge vergriffen ist.'))
kids.append(para('Obwohl es das günstigste Gerät ist, das wir getestet haben, fühlte sich an seiner Leistung '
    'nichts billig an. Die Daten, die es über 30 Tage geliefert hat, ließen die meisten teureren Geräte darüber '
    'wie überkomplizierte Antworten auf eine einfache Frage wirken. Und jedes HLTH Band kommt mit einer '
    '<span style="font-weight:700">30-tägigen Geld-zurück-Garantie</span>, es ist also kein echtes Risiko, es '
    'selbst auszuprobieren.'))
kids.append(container([button("Verfügbarkeit des HLTH Band prüfen →", href=PDP, full=True,
    pad={"top":"13px","bottom":"13px","left":"20px","right":"20px"})], [{"prop":"width","value":"100%"}]))
kids.append(text('<a href="%s" target="_blank" style="color:#1A5FD0;text-decoration:underline">Das HLTH '
    'Band auf der offiziellen Website ansehen →</a>' % PDP, size="18px", lh="29.7px", align="center", font=SERIF))
kids.append(sp(16))

# ============================== COMMUNITY PROOF ==============================
kids.append(h2("Was die Health-Tracking-Community über das HLTH Band sagt"))
kids.append(sp(10))
kids.append(para("Unsere Einschätzung kennst du jetzt. So sieht es von außen aus. Zuerst das Band im Video, "
    "Tag und Nacht getragen statt im Studio gefilmt:"))
kids.append(sp(6))

def video_embed_rc(youtube_embed_url, title="HLTH Band Video-Review"):
    return {"t":"HtmlElement","id":nid(),"p":{"content":(
        '<div style="position:relative;width:100%%;padding-top:56.25%%;border-radius:12px;'
        'overflow:hidden;background:#000">'
        '<iframe src="%s" title="%s" loading="lazy" '
        'style="position:absolute;top:0;left:0;width:100%%;height:100%%;border:0" '
        'allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" '
        'allowfullscreen></iframe></div>'
    ) % (youtube_embed_url, title)}, "styles":[{"prop":"width","value":"100%"}]}

# Same product review video as the English step -- there is no separate
# German-dubbed edit provided; this is the same physical unboxing/test video.
kids.append(video_embed_rc("https://www.youtube.com/embed/lMZoKLSmd6M"))
kids.append(sp(10))
kids.append(para("Dann ist da Trustpilot. Für eine Marke ist es einer der schwierigeren Orte, den eigenen Ruf "
    "zu formen, denn Trustpilot betreibt Betrugserkennung, verifiziert Bewerter und bestraft Firmen, die beim "
    "Frisieren ihrer Bewertungen erwischt werden. So schneiden die Bewertungen des HLTH Band ab:"))
kids.extend(figure(img_block("trustpilot_shot", height="252px", mh="180px", radius="8px", fit="contain"),
    cap_text="Screenshot der Trustpilot-Seite des HLTH Band (trustpilot.com/review/hlthtrack.com), aufgenommen "
             "am 8. August 2026."))
kids.append(sp(10))

# Verbatim from Figma node 145:684 -- all 6 reviews show 5/5 stars.
REVIEWS = [
    ("Funktioniert so gut wie mein teures Band", "Schlaf- und HRV-Daten sind gleich wie bei meinem alten Band, "
        "das 3 mal so viel gekostet hat. Die Batterie hält auch wochenlang.", "Verifizierter Käufer"),
    ("Keine monatlichen Kosten", "Macht das gleiche wie die großen Firmen, ohne das große Preisschild oder die "
        "monatlichen Kosten.", "Verifizierter Käufer"),
    ("Ich vergesse, dass ich es trage", "Es ist so leicht, ich vergesse wirklich, dass ich es trage. Endlich "
        "ein Tracker, den ich die ganze Zeit benutze.", "Verifizierter Käufer"),
    ("Sehr hilfreiches Team", "Hatte eine Frage und der Support hat mir innerhalb einer Stunde geantwortet. "
        "Super Service.", "J. Porras, vor 5 Tagen"),
    ("Ich hab es jeden Tag an", "Misst Puls, Schlaf, Stress, HRV und Blutsauerstoff. Kann ich nur empfehlen!",
        "Joanna"),
    ("Ist am nächsten Tag angekommen", "Ich habe es am Abend bestellt und es war am nächsten Tag schon da. Die "
        "Verpackung war auch sehr schön.", "Verifizierter Käufer"),
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
kids.append(para("Wenn man genug davon liest, tauchen immer wieder dieselben Punkte auf. Nutzer schwärmen "
    "davon, wie leicht das Band ist, dass der Akku wirklich Wochen statt Tage hält und dass alles in einer "
    "einzigen, übersichtlichen App zusammenläuft. Das andere wiederkehrende Thema ist Geld: kein Abo, keine "
    "gesperrten Funktionen, nach den 92 € fällt nichts weiter an."))
kids.append(text('<a href="%s" target="_blank" style="color:#1A5FD0;text-decoration:underline">Mehr '
    'Bewertungen auf Trustpilot ansehen →</a>' % TP, size="18px", lh="29.7px", font=SERIF))
kids.append(sp(16))

# ============================== FAQ ==========================================
kids.append(h2("Deine Fragen, beantwortet"))
kids.append(sp(10))

# Figma nodes 145:872 (desktop) and 145:1906 (mobile) both confirmed via a raw
# get_node read: each row is ONLY a bold question + a red "+" glyph. No answer
# text exists anywhere in the file, on either frame -- same as the English
# step. Reproduced verbatim as static question rows.
FAQ_ITEMS = [
    ("Funktioniert das HLTH Band mit iPhone und Android?", [
        "Beides. Du brauchst ein iPhone 8 oder neuer, oder ein Android-Gerät mit Version 8.0 oder neuer. Die "
        "Verbindung läuft über Bluetooth.",
        "Die App ist in beiden Stores kostenlos. Die Einrichtung hat bei uns etwa drei Minuten gedauert.",
        "Das Band selbst hat kein Display, dein Handy zeigt dir alles an. Öffne die App, wenn du deine Werte "
        "sehen willst. Den Rest der Zeit macht das Band einfach still seine Arbeit.",
    ]),
    ("Gibt es wirklich kein Abo? Wo ist der Haken?", [
        "Kein Abo. Du zahlst einmalig 92 €, und alles ist freigeschaltet. Blutdrucktrends, HRV, Schlafphasen, "
        "Blutsauerstoff. Alles dabei.",
        "Der Haken ist nicht das Geld. Es geht darum, was das Band nicht kann.",
        "Es hat kein Display, du schaust also in die App. Es hat kein eingebautes GPS, Laufstrecken laufen also "
        "über dein Handy. Und es ist eine neue Marke, das Logo kennt also noch niemand.",
        "Zum Vergleich: Bei Whoop hört die Hardware auf zu funktionieren, sobald du nicht mehr zahlst. "
        "Blutdruckmessung gibt's dort erst in der 359-€-pro-Jahr-Stufe.",
    ]),
    ("Wie genau ist die Blutdruckmessung?", [
        "Seien wir ehrlich, hier liegen viele Leute falsch.",
        "Das HLTH Band ist ein Wellness-Gerät, kein Medizinprodukt. Es zeigt dir Trends über den Tag. Es ersetzt "
        "nicht die Manschette beim Arzt.",
        "Wir haben es in Ruhe mit einer medizinischen Manschette verglichen. Es lag jedes Mal innerhalb von "
        "±10 mmHg.",
        "Manche Nutzer:innen bemerken, dass ihre Werte etwas höher oder niedriger liegen als bei der Manschette. "
        "Das ist normal für diese Art von Sensor. Der Trend stimmt trotzdem, und der Trend ist das Nützliche "
        "daran.",
        "Für gleichmäßigere Werte: eng anlegen und immer am selben Handgelenk tragen. Die nicht-dominante Hand "
        "funktioniert am besten.",
        "Willst du eine exakte Zahl? Nimm eine Manschette. Willst du sehen, was dein Blutdruck über den Tag "
        "macht? Das hier ist der günstige Weg, es herauszufinden.",
    ]),
    ("Kann ich damit duschen oder schwimmen?", [
        "Ja. Es ist mit 1ATM zertifiziert. Duschen, Schwitzen, Abwasch, Bahnen im Pool. Alles kein Problem.",
        "Wir haben es einen Monat lang jeden Tag mit in die Dusche genommen. Keine Probleme.",
        "Nur Tauchen und Hochdruckreiniger solltest du vermeiden. Nach dem Schwimmen kurz abspülen und das "
        "Armband trocknen. Wie bei jedem Band, das du dauerhaft trägst.",
    ]),
    ("Wie lade ich es und wie lange dauert das?", [
        "Ladegerät aufstecken und etwa 90 Minuten liegen lassen. Zehn Minuten reichen für drei Tage, wenn's "
        "schnell gehen muss.",
        "Danach vergisst du es einen Monat lang.",
        "Genau das hat uns überzeugt. Unseres hielt 27 Tage durch, mit allen Sensoren aktiv, inklusive "
        "Blutsauerstoffmessung über Nacht. Geladen wurde also, während der Wasserkocher lief, nicht jeden Abend "
        "vorm Schlafengehen.",
        "Das bedeutet auch: Es ist in jeder einzigen Nacht am Handgelenk. Nicht am Ladekabel, während es deinen "
        "Schlaf verpasst.",
    ]),
    ("Was, wenn es für mich nicht passt?", [
        "Du hast 30 Tage Zeit. Schick es zurück für eine volle Rückerstattung, geöffnet oder nicht, ohne "
        "Nachfragen. Rücksendungen sind kostenlos.",
        "Zusätzlich gibt's ein Jahr Garantie, und es ist CE-zertifiziert.",
        "Im schlimmsten Fall trägst du es einen Monat und merkst, es ist nichts für dich. Den Support erreichst "
        "du unter info@hlthtrack.com, werktags von 8 bis 17 Uhr (UK-Zeit). Leser:innen berichten, dass sie "
        "meist noch am selben Tag eine Antwort bekommen.",
    ]),
    ("Was ist im Lieferumfang enthalten?", [
        "Der Sensor, zwei Armbänder und ein Ladekabel.",
        "Ein Armband ist aus weichem Stoff für tagsüber und zum Schlafen. Das andere ist aus Silikon für "
        "Workouts und Wasser. Es passt für Handgelenke bis etwa 24 cm, es gibt also kein Größen-Set und keine "
        "zweiwöchige Wartezeit zum Start.",
        "Das Wechseln der Armbänder dauert nur Sekunden.",
        "Das Bizeps-Band, mit dem wir trainiert haben, gibt es separat für 14,95 €. Lohnt sich, wenn du läufst "
        "oder trainierst. Kannst du auch einfach weglassen, wenn nicht.",
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
kids.append(h2("Unser Fazit"))
kids.append(sp(10))
kids.extend(figure(img_block("closing_lifestyle", height="402px", mh="230px", border=True)))
kids.append(sp(10))
kids.append(para("Wenn du neugierig auf deinen Blutdruck und deinen Schlaf bist und Tracker satt hast, die "
    "jede Nacht ans Ladekabel müssen oder jedes Jahr ein Abo kosten, ist das HLTH Band eine einfache "
    "Empfehlung. Es macht das Gesundheitstracking, auf das es wirklich ankommt, ohne Display, ohne "
    "nächtlichen Ladevorgang und ohne monatliche Gebühr."))
kids.append(text("So sehe ich das: In einem Jahr hast du entweder zwölf Monate deiner eigenen Herz-, "
    "Schlaf- und Blutdrucktrends, auf die du zurückblicken kannst, oder du rätst immer noch. Für einmalig "
    "92 € ist das keine schwere Entscheidung.", size="18px", lh="29.7px", font=SERIF))
kids.append(container([button("Verfügbarkeit des HLTH Band prüfen →", href=PDP, full=True,
    pad={"top":"13px","bottom":"13px","left":"20px","right":"20px"})], [{"prop":"width","value":"100%"}]))
kids.append(sp(28))

# ============================== ENDMATTER ====================================
def em_h2(t_):
    return container([title(t_, "22px", "28px", weight="700", ls="-0.22px", font=SERIF)],
        [{"prop":"padding","value":{"top":"24px","bottom":"12px"}}])

endmatter_kids = [sp(24), em_h2("Quellen")]
# Same English-language academic sources/URLs as the international version --
# not localized, since academic citations aren't translated (verbatim from
# Figma nodes 145:910/145:913, identical text to English's REFS).
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

endmatter_kids.append(em_h2("Weiterlesen"))
# Same hrefs as the English step's Further Reading -- not localized/region-
# specific in Figma (verbatim from nodes 145:919-935).
# QA: see the English step -- the first two cards named articles the blog does not
# publish. Labels now match the article each card actually opens; card 2 repointed.
FURTHER = [
    ("KAUFBERATUNG", "Kaufberatung für dein erstes Wearable",
        "https://blog.techunboxed.co/article/complete-wearable-buying-guide"),
    ("VERGLEICH", "Smart Rings vs. Smartwatches: Was misst den Schlaf besser?",
        "https://blog.techunboxed.co/article/smart-rings-vs-smartwatches-sleep-tracking"),
    ("ERKLÄRT", "Wie genau sind Blutdruckmessungen am Handgelenk?",
        "https://blog.techunboxed.co/article/blood-pressure-monitors-at-home-vs-wearable"),
    ("ERKLÄRT", "Verbessern Fitness-Tracker wirklich deine Gesundheit? Was die Forschung sagt",
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

endmatter_kids.append(em_h2("Über den Autor"))
author_avatar = container([{"t":"Image","id":nid(),"p":{"src_id":IMG["avatar_author"]["src_id"],
    "src_uid":IMG["avatar_author"]["src_uid"],"src":IMG["avatar_author"]["src"]},
    "styles":[{"prop":"width","value":"78px"},{"prop":"height","value":"78px"},
              {"prop":"borderRadius","value":"50%"},{"prop":"objectFit","value":"cover"}]}],
    [{"prop":"width","value":"78px"},{"prop":"flexShrink","value":"0"}])
author_box = rowf([author_avatar, col([
    text("Marcus Pendleton", size="18px", lh="24px", color=DARK, weight="700", font=SERIF), sp(2),
    text("Leitender Autor, Wearables · TechUnboxed", size="13.5px", lh="18px", color=BODY, font=SANS), sp(10),
    text("Marcus testet seit sechs Jahren Wearables für TechUnboxed, mehr als 40 Geräte quer durch "
         "Smartwatches, Ringe und bildschirmlose Bänder. Er trägt täglich einen Oura Ring und wechselt "
         "Testgeräte am anderen Handgelenk durch. Nach einer familiären Vorgeschichte mit Bluthochdruck "
         "achtet er besonders darauf, wie Alltagstracker mit Herz- und Kreislaufdaten umgehen.",
         size="14.5px", lh="22.5px", color=DARK, font=SANS), sp(8),
    text("Vor TechUnboxed war er zehn Jahre im Handel für Unterhaltungselektronik tätig. Er testet jedes "
         "Gerät selbst, Tag und Nacht, mindestens 30 Tage lang, bevor er darüber schreibt.",
         size="13px", lh="20px", color=BODY, font=SANS),
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
# JUDGMENT CALL (see module docstring): kept in English, same as the English
# step's own reuse of v3's footer -- this Figma frame has no footer-legal
# node in EITHER language, so this is shared compliance infrastructure, not
# page content. A German legal/medical translation should get a dedicated
# native-speaker/legal review before this page goes live for a DE audience.
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
TITLE = "Wir haben 1.850 € ausgegeben, um die 5 besten Fitness-Tracker 2026 zu testen. Der Außenseiter für 92 € hat gewonnen."
OG = json.load(open("pagescore/.cache/og_img_map.json"))  # QA: purpose-cut 1200x630 share images
SEO = {
    "title": "Top 5 Fitness-Tracker 2026 im Test & Ranking",
    "description": "Wir haben 1.850 € für 5 Fitness-Tracker ausgegeben -- Whoop, Apple, Garmin, Fitbit und HLTH. "
        "Der 92-€-Tracker ohne Bildschirm hat gewonnen.",
    "keywords": "Fitness-Tracker, bester Fitness-Tracker 2026, Fitness-Tracker Test, HLTH Band, "
        "Whoop vs Apple Watch, Fitness-Tracker ohne Bildschirm, Blutdruck-Tracker, Wearable Vergleich",
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
    other_steps = [{"id": s["id"], "slug": s["slug"], "title": s["title"], "type": s["type"],
                    "settings": s["settings"], "visual": s["visual"]}
                   for s in existing_steps if s["slug"] != STEP_SLUG]
    new_steps_list = other_steps + [{"id": collide["id"], "slug": STEP_SLUG, "title": TITLE, "type": "article_page",
        "settings": {"custom_html": CUSTOM_HTML, "seo": SEO}, "visual": collide["visual"], "body": body}]
    print("redeploying existing step ->", collide["id"])
else:
    create_r = sgql('''mutation($fid: ID!, $node: InputStep!){ createStep(funnel_id:$fid, node:$node){ step { id uid } } }''',
        {"fid": FUNNEL, "node": {"slug": STEP_SLUG, "title": TITLE, "type": "article_page",
            "settings": {"custom_html": CUSTOM_HTML, "seo": SEO}, "visual": {"x": 1090, "y": 220}, "body": body}})
    NEW_STEP_ID = create_r["createStep"]["step"]["id"]
    print("created detached step ->", create_r["createStep"]["step"])
    new_steps_list = [{"id": s["id"], "slug": s["slug"], "title": s["title"], "type": s["type"],
                        "settings": s["settings"], "visual": s["visual"]} for s in existing_steps]
    new_steps_list.append({"id": NEW_STEP_ID, "slug": STEP_SLUG, "title": TITLE, "type": "article_page",
        "settings": {"custom_html": CUSTOM_HTML, "seo": SEO}, "visual": {"x": 1090, "y": 220}, "body": body})

r2 = sgql('''mutation($id: ID!, $node: InputFunnel!){ updateFunnel(id:$id,node:$node){ id starting_step_id published steps { uid slug title } } }''',
    {"id": FUNNEL, "node": {"published": True, "steps": new_steps_list}})
print("WROTE", json.dumps(r2["updateFunnel"], indent=2))
