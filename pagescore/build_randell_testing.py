#!/usr/bin/env python3
"""Brand-new "randell testing" funnel (slug randell-testing), step
bh-advertorial-v1: "The Screenless Health Tracker That's Outselling
Smartwatches in the UK" -- built from Figma file "HLTH" (Page 2) node
235:958 ("Branded Hype Advertorial V1", desktop 1440x5499) + its mobile
companion 235:1098 ("Branded Hype Advertorial V1 -- Mobile", 390x6336).
Run id randell-testing-20260824; frame dumps saved to
pagescore/runs/randell-testing-20260824/design.json (+ design_mobile.json).

235:958 was diffed node-by-node against what build_bh_advertorial_v1.py
(source: the older node 217:395) ships. Copy, structure, images, and the
measured per-paragraph color asymmetry are IDENTICAL except for:

  1. Section-5 paragraph: the red PDP link reads "HLTH Band's" with a
     STRAIGHT apostrophe (U+0027) in 235:1034, where the old builder ships
     a curly U+2019. Reproduced straight, as 235:958 says.
  2. Byline "In Partnership With HLTH" (235:999): both styled ranges are
     #191E2A -- there is no #000000 span on "HLTH" like the old builder
     ships. Rendered uniform #191E2A.
  3. Footer "DISCLAIMER" label (235:1072): JetBrains Mono Bold 10.5px in
     this frame (old builder shipped Inter). Reproduced as
     fontFamily "JetBrains Mono, monospace" (unquoted -- quoted font names
     crash the LF editor canvas); if LF doesn't serve JetBrains Mono the
     monospace fallback still reads closer to the design than Inter.

Verified identical to the old builder's values (not assumed): H1 40/52 ->
28/36 @767, H2 30/39 -> 22/30 @767 with a 32px own padding-top on top of
the column's 18px gap, avatar 95 -> 64px, body paragraphs 18/31 with base
color #4C4C4C on intro/s2/s3 vs #191E2A on s1/s4/s5/closing (the real
asymmetry in the file, confirmed per-range via scan_text_nodes), blockquote
17/31 italic (#191E2A bold lead-in, #7C7C7C medium body) with a 3px #E63946
left border, CTA pill #E63946 r10 2px #F6F6F6 border 350x67 (mobile frame
shows the same 345px-overflowing-326-column artifact as 217:536 --
reproduced as width:100% max-width:350px centered), images 517/517/467px
desktop -> 240/240/250px @767, section-5 image the only linked figure
("Figure -> Link"), footer legal links #BCD9E4, footer divider
rgba(255,255,255,.14), OverlayBlur disclaimer panel has no fill (plain
centered text), header/footer "SVG" frames have no fills (render nothing --
omitted). "SPONSORED ARTICLE" is SF Pro in the frame; SF Pro is not a
webfont, kept as Inter (same decision as the old builder).

All 8 raster assets (byline avatar, s1 phone / s3 wrist / s5 teardown
photos, 4 social icons) were exported from 235:958 and compared against
pagescore/.cache/bh_advertorial_img_map.json -- pixel-identical (dHash 0
on exact-size pairs, visually confirmed on the photos), so the already-
hosted LF library images are REUSED, no re-upload. The vector TECH UNBOXED
wordmark is the same hosted logo PNG. Figma carries NO hyperlinks anywhere
in this frame (all "Link -" frames are untitled); PDP/Trustpilot targets
and the legal-modal wiring follow the established sibling-funnel
convention, same as the old builder.

Creates the funnel if the slug doesn't exist yet (createFunnel ->
createStep -> updateFunnel attach + starting_step_id), publishes it
(explicitly authorized for this run so QA can reach the page), and is safe
to re-run: an existing bh-advertorial-v1 step in this funnel is redeployed
in place, siblings untouched, deploy_guard consulted before every write.
"""
import sys, os, json, uuid
sys.path.insert(0, '.')
sys.path.insert(0, 'pagescore')
import lf_api
from deploy_guard import guard

tok = open('.session_token').read().strip() if os.path.exists('.session_token') else ''
ACCT = open('.lf_account').read().strip() if os.path.exists('.lf_account') else ''
HH = {"account-id": ACCT, "version": "1",
      "Origin": "https://app.lightfunnels.com", "Referer": "https://app.lightfunnels.com/"}
def sgql(q, v=None): return lf_api.gql(tok, q, v, extra_headers=HH)
def nid(): return str(uuid.uuid4())

FUNNEL_NAME = "randell testing"
FUNNEL_SLUG = "randell-testing"
STEP_SLUG = "bh-advertorial-v1"
VISUAL = {"x": 100, "y": 100}
IMG = json.load(open("pagescore/.cache/bh_advertorial_img_map.json"))

PDP = "https://hlthtrack.co.uk/products/wearable-hlth-band"
TP  = "https://www.trustpilot.com/review/hlthtrack.com"

# ---- fonts: Inter end-to-end (headings AND body), measured on 235:958 ----
SANS = "Inter, InterFallback, sans-serif"
# 235:1072 is JetBrains Mono Bold in the frame (diff #3 in the docstring).
MONO = "JetBrains Mono, monospace"

# ---- perf: Inter preload + real @font-face + metric-matched InterFallback
#      (verified zero-CLS recipe, references/performance.md). No hero
#      preload: the first heavy image sits below the fold on both frames.
_FONT_PRELOAD = "".join(
    '<link rel="preload" as="font" type="font/woff2" crossorigin '
    'href="/cf-fonts/s/inter/5.2.8/latin/%d/normal.woff2">\n' % w for w in (400, 600, 700, 800))
_INTER_WEIGHTS = (300, 400, 500, 600, 700, 800)
_INTER_FACE = "<style>" + "".join(
    "@font-face{font-family:Inter;font-style:normal;font-weight:%d;font-display:swap;"
    "src:url(/cf-fonts/s/inter/5.2.8/latin/%d/normal.woff2) format('woff2')}" % (w, w)
    for w in _INTER_WEIGHTS) + "</style>\n"
_FALLBACK_FACE = (
    "<style>@font-face{font-family:InterFallback;src:local('Arial'),local('Liberation Sans'),local('Helvetica Neue');"
    "ascent-override:90.44%;descent-override:22.52%;line-gap-override:0%;size-adjust:107.12%}</style>\n")
PERF = _INTER_FACE + _FALLBACK_FACE + _FONT_PRELOAD
# LF's storefront theme emits maximum-scale=1 (blocks pinch-zoom); no
# per-step viewport knob, so rewrite the tag at runtime. Legal links open
# the same modal system live on the sibling pages (real copy, CSS, handler).
LEGAL_MODALS = open("pagescore/tu_legal_modals.html", encoding="utf-8").read()
PERF_FOOTER = (
    '<script>(function(){var v=document.querySelector("meta[name=viewport]");if(v&&/maximum-scale/.test(v.content))v.setAttribute("content","width=device-width, initial-scale=1");'
    # Fix 1 (run randell-testing-20260824): give the section-5 teardown image
    # link a real accessible name -- the renderer hardcodes "Untitled link".
    'document.querySelectorAll("a.s5-offer-link").forEach(function(a){a.setAttribute("aria-label","See the HLTH Band offer")});'
    '})();</script>\n') + LEGAL_MODALS

# ---- colors (measured per-node on 235:958; base color is NOT uniform
#      across paragraphs -- see docstring) ----
DARK       = {"r":25,"g":30,"b":42,"a":1}    # #191E2A
GREY_BODY  = {"r":76,"g":76,"b":76,"a":1}    # #4C4C4C
GREY_QUOTE = {"r":124,"g":124,"b":124,"a":1} # #7C7C7C
RED        = {"r":230,"g":57,"b":70,"a":1}   # #E63946
TAG_GREY   = {"r":189,"g":189,"b":189,"a":1} # #BDBDBD
AZURE_LINK = {"r":188,"g":217,"b":228,"a":1} # #BCD9E4
WHITE      = {"r":255,"g":255,"b":255,"a":1}
BTN_BORDER = {"r":246,"g":246,"b":246,"a":1} # #F6F6F6

# ---- helpers (same shape as the sibling builders) ----
def _media(st, m):
    if m:
        for k, v in m.items(): st.append({"prop": k, "value": v, "media": 767})

def title(content, fs, lh, weight="700", color=DARK, align="left", ls=None, m=None, font=SANS, level="2"):
    st=[{"prop":"fontFamily","value":font},{"prop":"color","value":color},
        {"prop":"fontSize","value":fs},{"prop":"lineHeight","value":lh},
        {"prop":"fontWeight","value":weight},{"prop":"textAlign","value":align},
        {"prop":"width","value":"100%"},{"prop":"maxWidth","value":"100%"}]
    if ls: st.append({"prop":"letterSpacing","value":ls})
    _media(st, m)
    return {"t":"Title","id":nid(),"p":{"size":level,"content":content,"widthOption":"fill"},"styles":st}

def text(content, size="18px", lh="30px", color=DARK, weight="400", align="left", italic=False,
         mw="100%", m=None, font=SANS, ls=None):
    st=[{"prop":"fontFamily","value":font},{"prop":"color","value":color},
        {"prop":"fontSize","value":size},{"prop":"lineHeight","value":lh},
        {"prop":"fontWeight","value":weight},{"prop":"textAlign","value":align},
        {"prop":"maxWidth","value":mw},{"prop":"width","value":"100%"}]
    if italic: st.append({"prop":"fontStyle","value":"italic"})
    if ls: st.append({"prop":"letterSpacing","value":ls})
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

_TRANSPARENT_PX = "data:image/gif;base64,R0lGODlhAQABAIAAAAAAAP///yH5BAEAAAAALAAAAAABAAEAAAIBTAA7"
def sp(px):
    # An empty Container spacer is silently stripped from this template's SSR
    # HTML (verified on the sibling page via curl); an Image block survives,
    # so the spacer is a 1x1 transparent gif stretched to the target height.
    return {"t":"Image","id":nid(),"p":{"src":_TRANSPARENT_PX},
        "styles":[{"prop":"width","value":"100%"},{"prop":"height","value":"%dpx"%px},
                  {"prop":"lfDisplay","value":"block"}]}

# LF emits alt but does not populate it from p.title -- set p.alt explicitly.
# Decorative images (spacers, social icons, byline avatar) intentionally keep
# alt="" so screen readers skip them. The logo is the site's identity, not
# decoration -- QA run randell-testing-20260824 fix 2.
ALT = {
    "logo": "TechUnboxed",
    "byline_avatar": "",
    "step1_phone": "The HLTH companion app showing a day of blood pressure readings, "
                   "with the band worn on the wrist",
    "step3_wrist": "The HLTH Band worn on a wrist, showing its screenless fabric strap",
    "step5_teardown": "An exploded view of the HLTH Band showing its sensor board and battery",
    "icon_instagram": "", "icon_youtube": "", "icon_rss": "", "icon_x": "",
}

def img_block(key, height=None, mh=None, radius="0px", fit="cover", alt=None):
    m = IMG[key]
    st=[{"prop":"maxWidth","value":"100%"},{"prop":"width","value":"100%"},
        {"prop":"borderRadius","value":radius},{"prop":"objectFit","value":fit},
        {"prop":"lfDisplay","value":"block"}]
    if height: st.append({"prop":"height","value":height})
    if mh: st.append({"prop":"height","value":mh,"media":767})
    p = {"src_id":m["src_id"],"src_uid":m["src_uid"],"src":m["src"]} if m.get("src_id") else {"src":m["src"]}
    p["alt"] = ALT.get(key, "") if alt is None else alt
    return {"t":"Image","id":nid(),"p":p,"styles":st}

def img_link(key, href, height=None, mh=None, radius="0px", fit="cover"):
    # QA run randell-testing-20260824 fix 1: LF's storefront renderer HARDCODES
    # aria-label="Untitled link" on every BlockLink <a> (verified in the
    # production bundle -- the literal appears in both <a>-rendering components,
    # with no name/label prop feeding it), so no body prop can set the
    # accessible name. The link is tagged with the documented p.className and
    # the footer script (PERF_FOOTER) sets a real aria-label at parse time; a
    # manual setAttribute survives hydration (React prod ignores attribute
    # mismatches) and re-renders (vdom-to-vdom diff never re-writes it).
    return {"t":"BlockLink","id":nid(),"p":{"destination":{"type":"static","value":href},
        "target":"_blank","widthOption":"fill","className":"s5-offer-link",
        "children":[img_block(key, height, mh, radius, fit)]},
        "styles":[{"prop":"width","value":"100%"}]}

def button(label, href=PDP, mb="10px"):
    lab = {"t":"Text","id":nid(),"p":{"content":label},"styles":[
        {"prop":"fontFamily","value":SANS},{"prop":"color","value":WHITE},
        {"prop":"fontSize","value":"17px"},{"prop":"fontWeight","value":"700"},
        {"prop":"lineHeight","value":"31px"},{"prop":"textAlign","value":"center"},
        {"prop":"textTransform","value":"uppercase"},{"prop":"whiteSpace","value":"nowrap"},
        # At 320px the 265px label overflows the pill; let it wrap below 767.
        {"prop":"whiteSpace","value":"normal","media":767}]}
    lw = container([lab], [{"prop":"lfDisplay","value":"flex"},{"prop":"alignItems","value":"center"},
        {"prop":"justifyContent","value":"center"}])
    return {"t":"BlockLink","id":nid(),"p":{"destination":{"type":"static","value":href},
        "target":"_blank","widthOption":"fill","children":[lw]},
        "styles":[{"prop":"backgroundColor","value":RED},{"prop":"borderRadius","value":"10px"},
            {"prop":"borderStyle","value":"solid"},{"prop":"borderColor","value":BTN_BORDER},
            {"prop":"borderWidth","value":"2px"},
            {"prop":"padding","value":{"top":"16px","bottom":"16px","left":"37px","right":"37px"}},
            {"prop":"padding","value":{"top":"16px","bottom":"16px","left":"12px","right":"12px"},"media":767},
            {"prop":"width","value":"100%"},{"prop":"maxWidth","value":"350px"},
            {"prop":"margin","value":{"left":"auto","right":"auto","top":"30px","bottom":mb}},
            {"prop":"lfDisplay","value":"flex"},{"prop":"alignItems","value":"center"},
            {"prop":"justifyContent","value":"center"}]}

def cta_row(href=PDP, mb="10px"):
    return button("GET UP TO £79 OFF HLTH BAND", href, mb=mb)

def h2(content):
    # Measured (235:1003 etc., identical on 235:1098): each H2 frame carries
    # a 32px paddingTop in ADDITION to the column's 18px gap. Title blocks
    # drop margin/padding in this renderer, so the extra space is a real
    # sp() sibling; h2() returns [spacer, title] -- callers kids.extend(...).
    node = title(content, "30px", "39px", weight="700", color=DARK,
                 m={"fontSize":"22px","lineHeight":"30px"})
    return [sp(18), node]

def hlth_link(label="HLTH Band"):
    return '<a href="%s" style="color:#E63946;font-weight:700;text-decoration:underline">%s</a>' % (PDP, label)

def tp_link(label="Trustpilot"):
    return '<a href="%s" style="color:#E63946;font-weight:700;text-decoration:underline">%s</a>' % (TP, label)

def sb(t, color=None):
    st = "font-weight:600" + (";color:%s" % color if color else "")
    return '<span style="%s">%s</span>' % (st, t)

# ============================== HEADER (dark chrome, 235:959) ==============
sponsored_bar = {"t":"Section","id":nid(),
    "styles":[{"prop":"backgroundColor","value":DARK},
              {"prop":"padding","value":{"top":"7px","bottom":"7px"}}],
    "p":{"layout":"","dividerPosition":["top"],"horizontalFlip":False,
         "embedded_video":{"src":"","video_size":"stretch","video_position":"center"},
         "children":[text("SPONSORED ARTICLE", size="11px", lh="17.6px", color=TAG_GREY,
             align="center", font=SANS, ls="1px")]}}

header_logo_bar = {"t":"Section","id":nid(),
    "styles":[{"prop":"backgroundColor","value":DARK},
              {"prop":"padding","value":{"top":"14px","bottom":"14px","left":"24px","right":"24px"}}],
    "p":{"layout":"","dividerPosition":["top"],"horizontalFlip":False,
         "embedded_video":{"src":"","video_size":"stretch","video_position":"center"},
         "children":[container([img_block("logo", height="50px", radius="0px", fit="contain")],
             [{"prop":"width","value":"200px"},{"prop":"lfDisplay","value":"flex"},
              {"prop":"justifyContent","value":"center"},{"prop":"margin","value":{"left":"auto","right":"auto"}}])]}}

# ============================== ARTICLE HEAD (235:985/235:1125) =============
kids=[]
kids.append(title("The Screenless Health Tracker That's Outselling Smartwatches in the UK",
    "40px", "52px", weight="700", color=DARK, font=SANS, level="1",
    m={"fontSize":"28px","lineHeight":"36px"}))

byline_avatar = container([img_block("byline_avatar", height="95px", mh="64px", radius="50%", fit="cover")],
    [{"prop":"width","value":"95px"},{"prop":"height","value":"95px"},{"prop":"flexShrink","value":"0"},
     {"prop":"width","value":"64px","media":767},{"prop":"height","value":"64px","media":767}])
byline = rowf([
    byline_avatar,
    col([
        text("By", size="14px", lh="20px", color=DARK, weight="300", font=SANS, ls="1px"),
        text("CHRIS KOWALSKI", size="13.8px", lh="20px", color=DARK, weight="700", font=SANS, ls="3.3px"),
        text("June 28, 2026", size="13.5px", lh="20px", color=DARK, weight="400", font=SANS, ls="1px"),
        # 235:999: both ranges are #191E2A -- no #000000 span (diff #2).
        text("In Partnership With HLTH", size="13.2px", lh="20px",
             color=DARK, weight="300", font=SANS, ls="1px"),
    ], gap="0px", styles=[{"prop":"flex","value":"1"},{"prop":"minWidth","value":"0"}]),
], gap="10px", align="flex-start", styles=[{"prop":"margin","value":{"top":"6px"}}])
kids.append(byline)

kids.append(text(
    "As a longevity optimiser who’s always on the hunt for smarter, more " +
    sb("affordable ways to take care of my body", color="#191E2A") +
    ", the search for a trusted tracker almost never stops. I've been wearing a smartwatch every day "
    "for the last four years and was never able to fully trust the data. But the " + hlth_link("HLTH band") +
    " – a " + sb("screenless wearable") + " that only tracks health, is the first one to change that. "
    "It's rated 4.6 on " + tp_link("Trustpilot") + " and has sold out three times since its release in the UK this April.",
    size="18px", lh="31px", color=GREY_BODY, font=SANS))
kids.append(text(
    "Here's why I'm putting my " + sb("smartwatch in the drawer") +
    " — and why you might want to do the same.",
    size="18px", lh="31px", color=GREY_BODY, font=SANS))

# ============================== 5 NUMBERED SECTIONS =========================
kids.extend(h2("1. It takes 288 readings a day"))
kids.append(img_block("step1_phone", height="517px", mh="240px", radius="0px"))
kids.append(text(
    "Most wearables take a few readings an hour, then fill the gaps with estimates. " + hlth_link("HLTH Band") +
    " takes " + sb("288 readings ") + "a day across " + sb("blood pressure, heart rate, HRV, sleep and more.") +
    " Plus its algorithm filters out noise automatically, so only clean data reaches your trends.<br><br>" +
    sb("More readings means more accuracy. And more accuracy means you're seeing what's actually happening "
       "in your body."),
    size="18px", lh="31px", color=DARK, font=SANS))

kids.extend(h2("2. No slimy subscriptions or hidden fees"))
kids.append(text(
    "This is the one that made me " + sb("double-take.") +
    " While most trackers charge you to rent your own health data and bury it in fine print, " +
    hlth_link("HLTH band") + " is a one-time purchase. The app is " + sb("completely free") +
    ", and all your data – blood pressure trends, heart rate, HRV, sleep stages – is accessible "
    "from day one.<br><br>When you see the quality of the device and the data, the price genuinely feels "
    "like they've made a mistake.",
    size="18px", lh="31px", color=GREY_BODY, font=SANS))
kids.append(cta_row())

kids.extend(h2("3. Comfortable design you actually sleep in"))
kids.append(img_block("step3_wrist", height="517px", mh="240px", radius="0px"))
kids.append(text(
    hlth_link("HLTH Band") + " weighs under " + sb("18 grams (less than 30 pence!)") +
    ", and uses non-itchy flexible material for the band that feels like nothing. That makes it easy to " +
    sb("sleep with or wear for any occasion") + " without looking like you’re sick or even wearing a "
    "health tracker. This isn’t just a cool design choice; it’s " + sb("scientifically proven") +
    " that most heart events and health issues happen at night. So nightly tracking is even more important "
    "than day time tracking.",
    size="18px", lh="31px", color=GREY_BODY, font=SANS))

kids.extend(h2("4. Proven 30 day battery life"))
kids.append(text(
    "We all know that daily wear is key to finding our real baseline and avoiding health issues, but keeping "
    "trackers on is tricky when the battery dies daily. Enter " + hlth_link("HLTH Band’s") + " " +
    sb("Flow Sense Intelligent routing feature.") + " Their advanced sensor watches your vitals and provides "
    "real-time adjustment to battery power, to prevent it from draining too fast.",
    size="18px", lh="31px", color=DARK, font=SANS))
blockquote = container([
    text('<span style="font-style:italic;font-weight:700;color:#191E2A">The result?</span> '
         '<span style="font-style:italic;font-weight:500;color:#7C7C7C">Battery life that lasts up to 30 days '
         'on a single charge. Whether you’re a busy professional, new parent, or retiree, I think we can '
         'all appreciate this feature.</span>', size="17px", lh="31px", font=SANS)
], [{"prop":"borderStyle","value":"solid"},{"prop":"borderColor","value":RED},
    {"prop":"borderWidth","value":"0px 0px 0px 3px"},
    {"prop":"padding","value":{"top":"0px","bottom":"20px","left":"19px","right":"16px"}}])
kids.append(blockquote)
kids.append(cta_row())

kids.extend(h2("5. Trend readings every 5 minutes"))
kids.append(img_link("step5_teardown", PDP, height="467px", mh="250px", radius="0px"))
kids.append(text(
    # 235:1034 uses a STRAIGHT apostrophe in "HLTH Band's" (diff #1).
    "Many devices on the market only take some readings at night or space them hours apart to save battery "
    "for screens. " + hlth_link("HLTH Band's") + " continuous " +
    sb("tracking spaces out readings as low as every 5 minutes,") +
    " making it easier than ever to see how your " + sb("food, sleep, workouts, and lifestyle habits") +
    " impact your health. So any changes you make can be seen quickly in your numbers.",
    size="18px", lh="31px", color=DARK, font=SANS))
kids.append(cta_row())

# ============================== CLOSING =====================================
kids.extend(h2("Ready to keep better watch of your health with HLTH Band?"))
kids.append(text(
    "From the continuous tracking and tight intervals to 30 day battery and comfortable design, " +
    hlth_link("HLTH Band") + " is packed with features that make health tracking smarter, more accurate, "
    "and more affordable.",
    size="18px", lh="31px", color=DARK, font=SANS))
kids.append(text(
    "If you’re ready to keep a better eye on your health, protect your heart, and save money doing it. " +
    hlth_link("HLTH Band") + " is the partner you’ve been waiting for. Now, THIS is one launch worth "
    "getting excited about.",
    size="18px", lh="31px", color=DARK, font=SANS))
# Measured (235:1044 "Frame 513835"): final CTA + fine print in their own
# frame with itemSpacing:8 on top of the button's 10px bottom margin. The
# fine print is a FIXED 542px box centered in the 700px column.
_fine_print = text(
    '<span style="font-style:italic;text-decoration:underline">Special </span>'
    '<span style="font-style:italic;font-weight:700;text-decoration:underline">50% off coupon</span>'
    '<span style="font-style:italic;text-decoration:underline"> valid for UK customers only while supplies '
    'last</span>', size="18px", lh="28px", color=DARK, align="center", font=SANS, mw="542px")
_fine_print["styles"].append({"prop":"margin","value":{"left":"auto","right":"auto"}})
kids.append(col([
    cta_row(mb="10px"),
    _fine_print,
], gap="8px"))

article_col = container(kids,
    [{"prop":"maxWidth","value":"700px"},{"prop":"width","value":"100%"},
     {"prop":"margin","value":{"left":"auto","right":"auto"}},
     {"prop":"padding","value":{"left":"32px","right":"32px"},"media":767},
     {"prop":"lfDisplay","value":"flex"},{"prop":"flexDirection","value":"column"},{"prop":"gap","value":"18px"}])

article = {"t":"Section","id":nid(),
    # Measured (235:958 root itemSpacing:56 + "Main" 235:983's 20px vertical
    # padding) -- 76px between the header chrome and the H1, and between the
    # fine print and the footer chrome, both breakpoints.
    "styles":[{"prop":"backgroundColor","value":WHITE},{"prop":"padding","value":{"top":"76px","bottom":"76px"}}],
    "p":{"layout":"boxed","dividerPosition":["top"],"horizontalFlip":False,
         "embedded_video":{"src":"","video_size":"stretch","video_position":"center"},"children":[article_col]}}

# ============================== FOOTER (dark chrome, 235:1049) ==============
DISCLAIMER_TXT = (
    "This product is a general wellness and fitness device. It is not a medical device and is not intended "
    "to diagnose, treat, cure, or prevent any disease or health condition, including any heart condition. "
    "Its readings (including heart rate, heart rate variability, blood pressure, and blood oxygen) are "
    "estimates for general wellness purposes only, are not clinically validated, and should not be relied "
    "upon for any medical decision. Do not use this device to detect, monitor, or manage any medical "
    "condition. It is not a substitute for professional medical advice, examination, diagnosis, or "
    "treatment, or for medical-grade monitoring equipment. Always consult a qualified physician or "
    "healthcare provider with any questions about your health, before making health decisions, and if you "
    "experience symptoms such as chest pain, shortness of breath, or dizziness — seek emergency care "
    "immediately. Individual results may vary.")

# 235:1070 "OverlayBlur" has NO fill (just a backdrop blur over the flat dark
# footer) -- visually a no-op, reproduced as plain centered/padded text.
footer_disclaimer_panel = col([
    # 235:1072: JetBrains Mono Bold 10.5, textCase UPPER (diff #3).
    text("DISCLAIMER", size="10.5px", lh="10.5px", color=WHITE, weight="700", align="center", font=MONO,
         ls="2.31px"),
    text(DISCLAIMER_TXT, size="13px", lh="20.15px", color=WHITE, align="center", font=SANS),
], gap="6px", styles=[
    {"prop":"maxWidth","value":"852px"},{"prop":"margin","value":{"left":"auto","right":"auto"}},
    {"prop":"padding","value":{"top":"16px","bottom":"16px","left":"18px","right":"18px"}}])

# Figma's legal links are untitled (no URLs); they open the same legal
# modals as the sibling pages -- markup/CSS/handler injected via PERF_FOOTER.
FOOTER_LINK = '<a href="#{0}" id="{1}" style="color:#BCD9E4;text-decoration:none">{2}</a>'
footer_links = rowf([
    inline_text(FOOTER_LINK.format("tu-terms", "terms", "Terms"), size="12px", lh="12px", color=AZURE_LINK, font=SANS),
    inline_text(FOOTER_LINK.format("tu-priv", "priv", "Privacy"), size="12px", lh="12px", color=AZURE_LINK, font=SANS),
    inline_text(FOOTER_LINK.format("tu-edit", "edit", "Editorial standards"), size="12px", lh="12px", color=AZURE_LINK, font=SANS),
    inline_text(FOOTER_LINK.format("tu-aff", "aff", "Affiliate policy"), size="12px", lh="12px", color=AZURE_LINK, font=SANS),
], gap="18px", align="center", justify="flex-start",
    styles=[{"prop":"width","value":"fit-content"},{"prop":"justifyContent","value":"center","media":767}])

def social_icon(key, href=None):
    # Figma's icon links are untitled (no handles exist) -- decorative only,
    # plain images, nothing clickable. Same decision as the sibling pages.
    return {"t":"Container","id":nid(),
        "p":{"children":[img_block(key, height="26px", radius="0px", fit="contain")]},
        "styles":[{"prop":"width","value":"26px"},{"prop":"height","value":"26px"},{"prop":"flexShrink","value":"0"}]}

social_row = rowf([
    social_icon("icon_instagram"),
    social_icon("icon_youtube"),
    social_icon("icon_rss"),
    social_icon("icon_x"),
], gap="13px", align="center", justify="flex-start", styles=[{"prop":"width","value":"fit-content"}])

footer_bottom_left = col([
    text("© 2026 TechUnboxed.", size="12px", lh="12px", color=WHITE, font=SANS),
    footer_links,
], gap="18px", styles=[{"prop":"width","value":"fit-content"},
    {"prop":"alignItems","value":"center","media":767},
    {"prop":"gap","value":"14px","media":767}])

footer_bottom = rowf([footer_bottom_left, social_row], gap="18px", align="center", justify="space-between",
    styles=[{"prop":"flexDirection","value":"column","media":767},{"prop":"gap","value":"14px","media":767}])

# Mobile (235:1098 footer): the divider bar spans the full viewport with its
# own 16px/20px inset -- media-scoped negative margin cancels footer_inner's
# mobile 36px padding so it lands flush with the viewport edge.
footer_bottom_wrap = container([footer_bottom], [
    {"prop":"width","value":"100%"},{"prop":"borderStyle","value":"solid"},
    {"prop":"borderColor","value":{"r":255,"g":255,"b":255,"a":0.14}},
    {"prop":"borderWidth","value":"1px 0px 1px 0px"},
    {"prop":"padding","value":{"top":"27px","bottom":"27px","left":"27px","right":"27px"}},
    {"prop":"padding","value":{"top":"20px","bottom":"20px","left":"16px","right":"16px"},"media":767},
    {"prop":"margin","value":{"left":"-36px","right":"-36px"},"media":767},
    {"prop":"width","value":"calc(100% + 72px)","media":767}])

# Measured (235:1053): logo-to-disclaimer gap 31px (15 Margin pad-top + 16
# OverlayBlur pad-top); disclaimer-to-divider gap 35px (pad-bottom).
footer_inner = col([footer_disclaimer_panel, footer_bottom_wrap], gap="35px",
    styles=[{"prop":"maxWidth","value":"1320px"},{"prop":"margin","value":{"left":"auto","right":"auto"}},
        {"prop":"padding","value":{"left":"20px","right":"20px"}},
        {"prop":"padding","value":{"left":"36px","right":"36px"},"media":767}])

footer_logo_img = img_block("logo", height="50px", radius="0px", fit="contain")
footer_logo_img["styles"].append({"prop":"width","value":"200px"})
footer_logo_img["styles"].append({"prop":"margin","value":{"top":"0px","right":"auto","bottom":"0px","left":"auto"}})
footer_logo = container([footer_logo_img],
    [{"prop":"width","value":"100%"},{"prop":"borderStyle","value":"solid"},
     {"prop":"borderColor","value":DARK},{"prop":"borderWidth","value":"1px 0px 0px 0px"},
     {"prop":"padding","value":{"top":"72px","bottom":"31px","left":"0px","right":"0px"}}])

footer = {"t":"Section","id":nid(),
    "styles":[{"prop":"backgroundColor","value":DARK}],
    "p":{"layout":"","dividerPosition":["top"],"horizontalFlip":False,
         "embedded_video":{"src":"","video_size":"stretch","video_position":"center"},
         "children":[container([footer_logo, footer_inner], [{"prop":"width","value":"100%"}])]}}

body = {"id":nid(),"t":"Root","version":11,
    "styles":[{"prop":"pageWidth","value":"700px"},{"prop":"backgroundColor","value":WHITE}],
    "p":{"children":[sponsored_bar, header_logo_bar, article, footer]}}

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
if iss: raise SystemExit("body failed sanity check")

TITLE = "The Screenless Health Tracker That's Outselling Smartwatches in the UK"
OG = json.load(open("pagescore/.cache/og_img_map.json"))  # purpose-cut 1200x630 share image
SEO = {
    "title": "The Screenless Tracker Outselling Smartwatches in the UK",
    "description": "It takes 288 readings a day, has no subscription, and lasts 30 days on a charge. Here's why the HLTH Band is outselling smartwatches in the UK.",
    "keywords": "HLTH Band, screenless health tracker, smart ring alternative, health tracker no subscription, continuous blood pressure tracker, best health tracker UK 2026, wearable without screen",
    "social_image_uid": OG["bh-v1"]["src_uid"],
}

# settings.seo emits og:* only -- append explicit twitter:* tags for X cards.
def _esc(v): return v.replace("&","&amp;").replace('"',"&quot;").replace("<","&lt;").replace(">","&gt;")
CUSTOM_HTML = {"header": PERF + (
    '<meta name="twitter:card" content="summary_large_image">\n'
    '<meta name="twitter:title" content="%s">\n'
    '<meta name="twitter:description" content="%s">\n'
    '<meta name="twitter:image" content="%s">\n'
    ) % (_esc(SEO["title"]), _esc(SEO["description"]), OG["bh-v1"]["src"]),
    "footer": PERF_FOOTER}

# ---------------- resolve or create the funnel ----------------
def _find_funnel():
    r = sgql('query($q: String!){ funnels(first:250, query:$q){ count '
             'edges { node { id name slug published starting_step_id '
             'steps { id uid slug title type settings visual { x y } } } } } }',
             {"q": "order_by:id order_dir:desc"})["funnels"]
    if r["count"] > len(r["edges"]):
        raise SystemExit("account has %d funnels, fetched %d -- raise the page size" % (r["count"], len(r["edges"])))
    return next((e["node"] for e in r["edges"] if e["node"]["slug"] == FUNNEL_SLUG), None)

funnel = _find_funnel()
if funnel is None:
    created = sgql('mutation($node: InputCreateFunnel!){ createFunnel(node:$node){ id name slug published starting_step_id } }',
        {"node": {"name": FUNNEL_NAME, "slug": FUNNEL_SLUG,
                  "funnel_steps": ["article_page"], "currency": "USD", "lang": "en"}})["createFunnel"]
    print("created funnel ->", created["id"], created["slug"])
    funnel = dict(created, steps=[])
FUNNEL = funnel["id"]
print("funnel:", FUNNEL, funnel["slug"], "published:", funnel.get("published"))

# ---------------- deploy guard (refuses to silently rewrite a live page) ----
guard(FUNNEL, STEP_SLUG)

# ---------------- write: create the step if new, else update in place ------
existing_steps = funnel.get("steps") or []
collide = next((s for s in existing_steps if s["slug"] == STEP_SLUG), None)

if collide:
    new_steps_list = [{"id": collide["id"], "slug": STEP_SLUG, "title": TITLE, "type": "article_page",
        "settings": {"custom_html": CUSTOM_HTML, "seo": SEO}, "visual": collide["visual"], "body": body}]
    print("redeploying existing step ->", collide["id"])
    funnel_patch = {"published": True, "steps": new_steps_list}
else:
    create_r = sgql('''mutation($fid: ID!, $node: InputStep!){ createStep(funnel_id:$fid, node:$node){ step { id uid slug } } }''',
        {"fid": FUNNEL, "node": {"slug": STEP_SLUG, "title": TITLE, "type": "article_page",
            "settings": {"custom_html": CUSTOM_HTML, "seo": SEO}, "visual": VISUAL, "body": body}})
    NEW_STEP_ID = create_r["createStep"]["step"]["id"]
    print("created detached step ->", create_r["createStep"]["step"])
    new_steps_list = [{"id": NEW_STEP_ID, "slug": STEP_SLUG, "title": TITLE, "type": "article_page",
        "settings": {"custom_html": CUSTOM_HTML, "seo": SEO}, "visual": VISUAL, "body": body}]
    # Publishing this brand-new funnel is explicitly authorized for run
    # randell-testing-20260824 ("publish it so QA can reach it").
    funnel_patch = {"published": True, "steps": new_steps_list}
    if not funnel.get("starting_step_id"):
        funnel_patch["starting_step_id"] = NEW_STEP_ID

r2 = sgql('''mutation($id: ID!, $node: InputFunnel!){ updateFunnel(id:$id,node:$node){ id starting_step_id published steps { uid slug title visual { x y } } } }''',
    {"id": FUNNEL, "node": funnel_patch})
print("WROTE", json.dumps(r2["updateFunnel"], indent=2))
print("LIVE URL: https://www.techunboxed.co/%s/%s" % (FUNNEL_SLUG, STEP_SLUG))
