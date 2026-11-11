#!/usr/bin/env python3
"""TechUnboxed "best sleep masks for side sleepers" advertorial -- BOTH A/B test
variants, built from one script into the live funnel fun_lqsXwH8BnCdqs44RJzEEf
("TUB - Sleep mask comparison - Meta", slug `sleep-masks`, already published).

    py pagescore/build_sleep_masks.py              # variant A (the entry page)
    SM_VARIANT=b py pagescore/build_sleep_masks.py # variant B

Source: Figma file "99 Commerce", page "Build 1".
  A  section 983:2575 -- desktop 983:2576 (1440x9759), mobile 983:2887 (390x9672)
  B  section 983:3199 -- desktop 983:3200 (1440x9223), mobile 983:3506 (390x9188)

Every value here was read off the node with figwright `get_nodes_info` (geometry,
fills, type) and `get_design_context detail:"full"` (styled text runs), never off a
screenshot. The four frame dumps are committed at
pagescore/runs/sleep-mask-2026-10-26/{a,b}_{desktop,mobile}.json and combined into
design.json for design_diff.py.

WHAT ACTUALLY DIFFERS BETWEEN A AND B (measured by diffing the two desktop dumps
node-for-node -- these four nodes and nothing else):
  1. H1          983:2600 vs 983:3224
  2. Subhead     983:2601 vs 983:3225
  3. Qualifier questions frame -- visible:false in A (983:2626), visible with three
     different questions in B (983:3250)
  4. Intro copy  983:2630 (4 paras + 2 inline headings) vs 983:3254 (4 paras, two of
     which carry the unfilled [NUMBER] / [TO CONFIRM] placeholders)
Everything from "How the 5 masks ranked" down is byte-identical, so it is built once
from shared data and used by both variants.

MOBILE (390) is a `media:767` restyle of the same DOM, not a separate build -- the
two mobile frames carry identical copy to their desktop frames. The only structural
differences, all measured:
  - article gutter          padding 0 -> 16px left/right  (390 - 32 = 358 column)
  - "Section 2" item gap    56 -> 40 ;  review card gap 18 -> 14
  - bullet row indent       paddingLeft 20 -> 8
  - "The Real Talk"         paddingTop 40 -> 28, gap 18 -> 14
  - buybox                  row/gap24/pad24 -> column/gap16/pad16, photo 250x304 fixed
                            -> full width x 300
  - footer                  padding 360 -> 16, link row HUG -> FILL (wraps)
  - type scale              per-node, see the m={...} overrides at each call site
  - ONE extra element: a mobile-only "THE RESULTS" kicker above the ranking H2
    (983:2952 / 983:3566), absent from both desktop frames -- so it is built with
    lfDisplay:none at base and flex @767 rather than hidden the other way round.

DECISIONS -- things the design did not settle, resolved here and flagged:

 1. THE FIVE PLACEHOLDERS ARE RENDERED, INCLUDING THE TWO FIGMA HIDES. The brief
    requires all five unfilled placeholders to appear on the live page so the client
    can be shown exactly what is still missing. Two of them are `visible:false` in
    BOTH Figma frames -- `★★★★★ [RATING] · [REVIEW COUNT] reviews` (983:2837 /
    3149 / 3456 / 3763) and `[RRP]` (983:2840 / 3152 / 3459 / 3766). They are built
    VISIBLE here, in their Figma document order (rating line between the product name
    and the price; [RRP] beside the price, carrying the node's STRIKETHROUGH). That is a
    deliberate override of the frame's visibility, not a misread. The other three --
    `Excellent [RATING] | [REVIEW COUNT] reviews on Trustpilot`, and B's `How we
    tested: ... [NUMBER] days ...` and `The winner: ... [TO CONFIRM: ...]` -- are
    visible in Figma and are reproduced as-is. No rating, price, review count or
    test result has been invented anywhere.

 2. "Qualifier questions" is hidden in A and shown in B, exactly as the frames say.
    A's three questions are therefore NOT on variant A at all.

 3. CTA DESTINATION IS UNKNOWN, so the CTA is not a link. The Figma node
    `button · CHECK AVAILABILITY` (983:2861) is a plain frame with no hyperlink, and
    no sleep-mask product URL exists anywhere in this repo. Rather than invent a
    destination or ship `href="#"` (banned), the button is built as a styled
    Container that matches the design pixel-for-pixel but navigates nowhere. This
    needs a human answer before the page takes traffic.

 4. BREADCRUMB ITEMS ARE NOT LINKS. "Home" and "Sleep" are plain TEXT nodes with no
    hyperlink in either frame, and no destinations are given. Reproduced as text.

 5. PRODUCT NAMES IN THE REVIEW HEADINGS ARE NOT LINKS EITHER. They are red
    (#B3001B) and underlined, which reads like a link, but the Figma segments carry
    no `hyperlink` field. Reproduced as styled text, so there is no dead link.

 6. FOOTER LEGAL LINKS go to the existing modal system (pagescore/tu_legal_modals.html),
    the same four overlays already live on the other TechUnboxed pages. The design
    shows "Terms / Privacy / Editorial standards / Affiliate policy" as plain text
    with no destinations; a real modal beats both a dead link and inert text.

 7. THE HERO IS ONE HtmlElement, not two Image blocks. Figma node 983:2611 is a
    rounded 10px box holding two absolutely-positioned image fills -- 396x371 and
    264x371 with a 4px gutter (mobile 212x220 / 142x220, same 4px). Matching it with
    native blocks needs per-corner radii (`10px 0 0 10px`), which is an unproven LF
    style prop and those have 503'd the SSR before. One HtmlElement with a class
    defined in the step header reproduces it exactly and risks nothing.

 8. LOGO: the Figma logo node (983:2579) was exported and uploaded rather than
    reusing the TechUnboxed logo already in the LF library, because the hosted copy
    could not be fetched to verify it matches this frame. It is 5 KB.

 9. SOCIAL IMAGE: a 1200x630 centre crop of the hero photograph (the tester asleep on
    their side in the mask), which is what the article is about. The design carries
    no share image.

10. FONT PROXY WORKAROUND (same platform bug build_ranked_comparison.py documents for
    Gelasio): Lightfunnels self-hosts any Google family it finds in a block's
    `fontFamily` through its own CDN proxy, and that proxy serves ONE file for every
    weight of a variable family -- which would flatten Jost SemiBold 600 and Jost
    Bold 700 into the same face. So JOST is renamed `JostText`, a name the proxy will
    not claim, and both weights are declared by hand against isolated single-weight
    Google Fonts URLs verified to return different files. Libre Baskerville keeps its
    real name because only its 400 is used, so there is nothing for the proxy to
    collapse. All three families (Inter too) are declared in the step header, because
    LF reads the whole stack string as one family name and asks Google for that --
    a request that fails, harmlessly, and leaves our own faces as the only ones.

11. INVISIBLE COLOUR SPLITS ARE REPRODUCED ANYWAY. Several paragraphs are broken into
    runs that differ only between #2B2F36 and #000000, and one single-space run in the
    card-#1 bullets is #1F2328 where cards #2-#5 use #2B2F36. These are editing
    artefacts in the source file and are invisible on screen, but reproducing them is
    free and keeps the page honest to the node.

SSR/editor gotchas avoided (verified live, see references/performance.md): no quoted
font-family names; no `maxWidth:"none"`, `alignItems:"baseline"`, native `overflow`,
native `boxShadow` or `zIndex` anywhere; no `<style>` tag inside a block (all CSS is
in settings.custom_html.header, which renders in <head>).
"""
import sys, os, json, re, uuid
sys.path.insert(0, '.')
import lf_api
from deploy_guard import guard

tok = open('.session_token').read().strip()
ACCT = open('.lf_account').read().strip()
HH = {"account-id": ACCT, "version": "1",
      "Origin": "https://app.lightfunnels.com", "Referer": "https://app.lightfunnels.com/"}
def sgql(q, v=None): return lf_api.gql(tok, q, v, extra_headers=HH)
def nid(): return str(uuid.uuid4())

FUNNEL = os.environ.get("SM_FUNNEL", "fun_lqsXwH8BnCdqs44RJzEEf")
VARIANT = os.environ.get("SM_VARIANT", "a").strip().lower()
if VARIANT not in ("a", "b"):
    raise SystemExit("SM_VARIANT must be 'a' or 'b' (got %r)" % VARIANT)
IS_A = VARIANT == "a"
STEP_SLUG = "best-sleep-masks-side-sleepers" + ("" if IS_A else "-v2")
VISUAL = {"x": 90, "y": 90} if IS_A else {"x": 460, "y": 90}

IMG = json.load(open("pagescore/.cache/sleep_img_map.json"))

# ---------------------------------------------------------------- colours
# every one read off a node fill; the hex comment is the Figma value
INK      = {"r":17, "g":24, "b":39,  "a":1}   # #111827  headline / breadcrumb ink
BODY     = {"r":55, "g":65, "b":81,  "a":1}   # #374151  intro + buybox feature copy
MUTED    = {"r":107,"g":114,"b":128, "a":1}   # #6B7280  image credit, RRP, guarantee
GREY_CRUMB={"r":156,"g":163,"b":175, "a":1}   # #9CA3AF  breadcrumb separators
GREY_UPD = {"r":120,"g":120,"b":120, "a":1}   # #787878  "Last updated"
RED      = {"r":230,"g":58, "b":69,  "a":1}   # #E63A45  accent / badge / CTA
BLUE_TAG = {"r":29, "g":111,"b":224, "a":1}   # #1D6FE0  "Buying Guides" pill
LIME_TAG = {"r":232,"g":244,"b":98,  "a":1}   # #E8F462  "↗ Trending" pill
INK_TAG  = {"r":0,  "g":0,  "b":0,   "a":1}   # #000000
BYLINE_LBL={"r":30, "g":30, "b":30,  "a":1}   # #1E1E1E  "By"
BYLINE_NM={"r":0,  "g":133,"b":255, "a":1}    # #0085FF  "James Whitfield"
HEAD_BG  = {"r":28, "g":28, "b":30,  "a":1}   # #1C1C1E  sponsored header bar
FOOT_BG  = {"r":35, "g":35, "b":38,  "a":1}   # #232326  footer
FOOT_TXT = {"r":155,"g":155,"b":159, "a":1}   # #9B9B9F  footer disclaimer body
GREY_BD  = {"r":189,"g":189,"b":189, "a":1}   # #BDBDBD  sponsored label + footer links
WHITE    = {"r":255,"g":255,"b":255, "a":1}
JINK     = {"r":31, "g":35, "b":40,  "a":1}   # #1F2328  Jost ink
LBINK    = {"r":43, "g":47, "b":54,  "a":1}   # #2B2F36  Libre Baskerville ink
PHOTO_BG = {"r":217,"g":217,"b":222, "a":1}   # #D9D9DE  product-photo plate
BUY_BG   = {"r":246,"g":246,"b":247, "a":1}   # #F6F6F7  buybox plate
TP_GREEN = {"r":0,  "g":182,"b":122, "a":1}   # #00B67A  Trustpilot star tile

# ---------------------------------------------------------------- fonts
# The Inter stack is the verified zero-CLS recipe from references/performance.md:
# real Inter faces + a metric-matched InterFallback so the swap reflows nothing.
SANS = "Inter, InterFallback, sans-serif"
JOST = "JostText, Inter, InterFallback, sans-serif"
BASK = "Libre Baskerville, Georgia, serif"

_INTER_W = (400, 600, 700, 800, 900)
_FONT_PRELOAD = "".join(
    '<link rel="preload" as="font" type="font/woff2" crossorigin '
    'href="/cf-fonts/s/inter/5.2.8/latin/%d/normal.woff2">\n' % w for w in _INTER_W)
_INTER_FACE = "<style>" + "".join(
    "@font-face{font-family:Inter;font-style:normal;font-weight:%d;font-display:swap;"
    "src:url(/cf-fonts/s/inter/5.2.8/latin/%d/normal.woff2) format('woff2')}" % (w, w)
    for w in _INTER_W) + "</style>\n"
_FALLBACK_FACE = (
    "<style>@font-face{font-family:InterFallback;"
    "src:local('Arial'),local('Liberation Sans'),local('Helvetica Neue');"
    "ascent-override:90.44%;descent-override:22.52%;line-gap-override:0%;"
    "size-adjust:107.12%}</style>\n")

# Jost 600/700 and Libre Baskerville 400, latin subset, each requested with NO other
# weight in the query so Google returns genuinely different static files (the same
# check build_ranked_comparison.py documents for Gelasio).
_JOST600 = "https://fonts.gstatic.com/s/jost/v20/92zPtBhPNqw79Ij1E865zBUv7mx9IjVBNIg.woff2"
_JOST700 = "https://fonts.gstatic.com/s/jost/v20/92zPtBhPNqw79Ij1E865zBUv7mxEIjVBNIg.woff2"
_BASK400 = ("https://fonts.gstatic.com/s/librebaskerville/v24/"
            "kmKUZrc3Hgbbcjq75U4uslyuy4kn0olVQ-LglH6T17uj8Q4iDgNP.woff2")
_ARTICLE_FACES = "".join(
    '<link rel="preload" as="font" type="font/woff2" crossorigin href="%s">\n' % u
    for u in (_JOST600, _JOST700, _BASK400)) + (
    "<style>"
    "@font-face{font-family:JostText;font-style:normal;font-weight:600;font-display:swap;"
    "src:url(%s) format('woff2')}"
    "@font-face{font-family:JostText;font-style:normal;font-weight:700;font-display:swap;"
    "src:url(%s) format('woff2')}"
    "@font-face{font-family:'Libre Baskerville';font-style:normal;font-weight:400;"
    "font-display:swap;"
    "src:url(%s) format('woff2')}"
    "</style>\n") % (_JOST600, _JOST700, _BASK400)

# Inline run styles. Every mixed-typography paragraph in the design is a sequence of
# these; the class carries family/weight/size/colour and the media query carries the
# mobile size, because a `media` override cannot reach inside a Text block's HTML.
_RUN_CSS = (
    "<style>"
    ".sm-j{font-family:%(J)s;font-weight:600;font-size:15px;color:#1F2328}"
    ".sm-jh{font-family:%(J)s;font-weight:600;font-size:16px;color:#1F2328}"
    ".sm-nm{font-family:%(B)s;font-weight:400;font-size:16px;color:#B3001B;"
    "text-decoration:underline}"
    ".sm-li{font-family:%(B)s;font-weight:400;font-size:15px;color:#1F2328}"
    ".sm-lg{font-family:%(B)s;font-weight:400;font-size:15px;color:#2B2F36}"
    ".sm-lk{font-family:%(B)s;font-weight:400;font-size:15px;color:#000000}"
    ".sm-bg{font-family:%(B)s;font-weight:400;font-size:16px;color:#2B2F36}"
    ".sm-bk{font-family:%(B)s;font-weight:400;font-size:16px;color:#000000}"
    ".sm-tb{font-family:%(S)s;font-weight:700;font-size:13px;color:#111827}"
    ".sm-tr{font-family:%(S)s;font-weight:400;font-size:13px;color:#111827}"
    ".sm-ts{font-family:%(S)s;font-weight:600;font-size:13px;color:#000000}"
    ".sm-ib{font-family:%(S)s;font-weight:700;font-size:17px;color:#374151}"
    ".sm-ir{font-family:%(S)s;font-weight:400;font-size:17px;color:#374151}"
    "@media(max-width:767px){"
    ".sm-j{font-size:14px}.sm-jh{font-size:15px}.sm-nm{font-size:15px}"
    ".sm-li,.sm-lg,.sm-lk{font-size:14px}.sm-bg,.sm-bk{font-size:15px}}"
    # QA: long unbroken strings pan the page sideways at 320px. LF puts class="wys"
    # on its own rich-text blocks, so this needs no className of ours (setting one
    # on a <p> is a documented way to break this renderer).
    ".wys{overflow-wrap:anywhere}"
    # Hero: Figma 983:2611 -- a 10px rounded box with two image fills side by side,
    # 396 : 264 with a 4px gutter (mobile 212 : 142, same gutter), both full height.
    ".sm-hero{display:flex;gap:4px;width:100%%;height:371px}"
    ".sm-hero>div{min-width:0}"
    ".sm-hero .a{flex:396 1 0}"
    ".sm-hero .b{flex:264 1 0;background:#DAD9DF}"
    ".sm-hero img{display:block;width:100%%;height:371px;object-fit:cover}"
    ".sm-hero .a img{border-radius:10px 0 0 10px}"
    ".sm-hero .b img{border-radius:0 10px 10px 0}"
    "@media(max-width:767px){.sm-hero{height:220px}.sm-hero img{height:220px}}"
    "</style>\n") % {"J": JOST, "B": BASK, "S": SANS}

_HERO = IMG["hero_left"]["src"]
_HERO_PRELOAD = ('<link rel="preload" as="image" fetchpriority="high" href="%s">\n'
                 % _HERO)

PERF = (_FONT_PRELOAD + _INTER_FACE + _FALLBACK_FACE + _ARTICLE_FACES
        + _HERO_PRELOAD + _RUN_CSS)

LEGAL_MODALS = open("pagescore/tu_legal_modals.html", encoding="utf-8").read()
PERF_FOOTER = (
    # QA: the LF storefront theme emits maximum-scale=1, which blocks pinch-zoom.
    # There is no per-step viewport knob, so rewrite the tag at runtime.
    '<script>(function(){var v=document.querySelector("meta[name=viewport]");'
    'if(v&&/maximum-scale/.test(v.content))'
    'v.setAttribute("content","width=device-width, initial-scale=1");})();</script>\n'
    '<script>(function(){function f(){'
    'var h=document.querySelector(\'img[title="hero"]\');'
    'if(h){h.setAttribute("fetchpriority","high");h.setAttribute("loading","eager");}'
    'var lg=document.querySelector(\'img[title="logo"]\');'
    'if(lg)lg.removeAttribute("fetchpriority");}'
    'if(document.readyState!=="loading")f();'
    'else document.addEventListener("DOMContentLoaded",f);})();</script>\n') + LEGAL_MODALS

# ---------------------------------------------------------------- helpers
def esc(s):
    return (s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
             .replace('"', "&quot;").replace("\n", "<br>"))

def _media(st, m):
    if m:
        for k, v in m.items():
            st.append({"prop": k, "value": v, "media": 767})

def _type(font, color, fs, lh, weight, align, ls):
    st = [{"prop": "fontFamily", "value": font},
          {"prop": "fontSize", "value": fs},
          {"prop": "lineHeight", "value": lh},
          {"prop": "fontWeight", "value": weight},
          {"prop": "textAlign", "value": align},
          {"prop": "width", "value": "100%"},
          {"prop": "maxWidth", "value": "100%"}]
    if color is not None:
        st.insert(1, {"prop": "color", "value": color})
    if ls:
        st.append({"prop": "letterSpacing", "value": ls})
    return st

def title(content, fs, lh, weight="700", color=INK, align="left", ls=None, m=None,
          font=SANS, level="2"):
    st = _type(font, color, fs, lh, weight, align, ls)
    _media(st, m)
    return {"t": "Title", "id": nid(),
            "p": {"size": level, "content": content, "widthOption": "fill"},
            "styles": st}

def text(content, fs="17px", lh="29px", weight="400", color=BODY, align="left",
         ls=None, m=None, font=SANS, extra=None, auto=False):
    st = _type(font, color, fs, lh, weight, align, ls)
    if auto:                       # HUG in Figma -- shrink-wrap instead of filling
        st = [s for s in st if s["prop"] != "width"]
        st.append({"prop": "width", "value": "auto"})
    if extra:
        st.extend(extra)
    _media(st, m)
    return {"t": "Text", "id": nid(), "p": {"content": content}, "styles": st}

def rich(runs, **kw):
    """A paragraph built from measured styled runs (class per run, see _RUN_CSS)."""
    return text("".join('<span class="sm-%s">%s</span>' % (c, esc(t)) for c, t in runs), **kw)

def container(children, styles):
    return {"t": "Container", "id": nid(), "styles": styles, "p": {"children": children}}

def col(children, gap="16px", styles=None):
    s = [{"prop": "lfDisplay", "value": "flex"},
         {"prop": "flexDirection", "value": "column"},
         {"prop": "gap", "value": gap},
         {"prop": "width", "value": "100%"}]
    if styles:
        s.extend(styles)
    return container(children, s)

def row(children, gap="10px", align="center", justify=None, wrap=False, styles=None):
    s = [{"prop": "lfDisplay", "value": "flex"},
         {"prop": "flexDirection", "value": "row"},
         {"prop": "gap", "value": gap},
         {"prop": "alignItems", "value": align},
         {"prop": "width", "value": "100%"}]
    if justify:
        s.append({"prop": "justifyContent", "value": justify})
    if wrap:
        s.append({"prop": "flexWrap", "value": "wrap"})
    if styles:
        s.extend(styles)
    return container(children, s)

def html(content, styles=None):
    return {"t": "HtmlElement", "id": nid(), "p": {"content": content},
            "styles": (styles or [{"prop": "width", "value": "100%"}])}

def section(children, styles, layout=""):
    return {"t": "Section", "id": nid(), "styles": styles,
            "p": {"layout": layout, "dividerPosition": ["top"], "horizontalFlip": False,
                  "embedded_video": {"src": "", "video_size": "stretch",
                                     "video_position": "center"},
                  "children": children}}

def pad(t=None, r=None, b=None, l=None):
    o = {}
    for k, v in (("top", t), ("right", r), ("bottom", b), ("left", l)):
        if v is not None:
            o[k] = "%spx" % v
    return o

# QA: LF emits an alt attribute but never populates it. The Image block honours
# p["alt"], so every content image carries one; decorative plates carry alt="".
ALT = {
    "hero_left":  "A side sleeper asleep in the HLTH sleep mask with daylight in the room",
    "hero_right": "Five sleep masks held in two hands before testing",
    "rev1": "The HLTH Sleep Mask worn by a side sleeper in a daylit room",
    "rev2": "The Manta Sleep Mask with its adjustable eye cups",
    "rev3": "The Manta PRO sleep mask with C-shaped eye cups",
    "rev4": "The MZOO sleep mask with 3D contoured memory foam cups",
    "rev5": "The Alaska Bear mulberry silk sleep mask",
    "buybox": "The HLTH Sleep Mask photographed flat",
    "logo": "TechUnboxed",
}

def image(key, h=None, mh=None, w="100%", mw=None, radius=None, fit="cover",
          styles=None, title_attr=None, alt=None):
    m = IMG[key]
    st = [{"prop": "width", "value": w},
          {"prop": "maxWidth", "value": "100%"},
          {"prop": "objectFit", "value": fit},
          {"prop": "lfDisplay", "value": "block"}]
    if h:
        st.append({"prop": "height", "value": h})
    if radius:
        st.append({"prop": "borderRadius", "value": radius})
    if styles:
        st.extend(styles)
    if mh:
        st.append({"prop": "height", "value": mh, "media": 767})
    if mw:
        st.append({"prop": "width", "value": mw, "media": 767})
    p = {"src_id": m["src_id"], "src_uid": m["src_uid"], "src": m["src"],
         "alt": ALT.get(key, "") if alt is None else alt}
    if title_attr:
        p["title"] = title_attr
    return {"t": "Image", "id": nid(), "p": p, "styles": st}

# ======================================================= shared copy (verbatim)
BREADCRUMB = [("Home", INK), (">", GREY_CRUMB), ("Sleep", INK), (">", GREY_CRUMB),
              ("Best Sleep Masks of 2026", RED)]
BYLINE_NAME = "James Whitfield"
LAST_UPDATED = "Last updated October 23, 2026"
IMAGE_CREDIT = "(Image credit: James Whitfield / TechUnboxed)"
RANK_H2 = "How the 5 masks ranked"
KICKER = "THE RESULTS"

H1_A = "I Tried 5 Sleep Masks To Force Myself To Sleep. Here's What Happened."
SUB_A = ('Every mask says "total blackout". Then I rolled on my side and light poured '
         'in at the nose. The fix was one detail most brands skip.')
H1_B = ("We Tested The Top 5 Blackout Sleep Masks Under £75. Only One Passed The "
        "Side-Sleeper Test.")
SUB_B = ('Every mask says "total blackout". Most of them failed the moment I rolled on '
         "my side. The winner wasn't the one I expected.")

# Variant A intro -- 983:2630. Four separate paragraphs (figma node had them as
# \n breaks inside one TEXT node, but a bare \n -> <br> carries no vertical gap,
# so it rendered as a wall of text -- see .claude/rules/page-copy.md. Split into
# one string per paragraph so each becomes its own node and inherits the
# surrounding col(gap="16px") spacing, same as INTRO_A_P3/P4/P5 already do.
INTRO_A_P1 = [
    "Getting eight hours of sleep isn’t always straightforward.",
    ('Especially when every mask claims to give you a "total blackout," but '
     "fails the moment your face hits the pillow. My sleep is sacred to me, "
     "especially working night shifts."),
    ("But every time I rolled onto my side, light poured in right at the "
     "bridge of my nose. Most masks look great in theory, but they skip a "
     "crucial structural detail that side sleepers actually need."),
    "I was desperate for a fix, so I put five top-rated masks to the test.",
]
INTRO_A_H1 = "The Problem With Most Sleep Masks"
INTRO_A_P2 = ("Most brands treat sleep masks like basic eye patches or luxury face "
              "wear, ignoring how your face presses against a pillow with:\n"
              "• Nose Gaps: Flat padding gaps near the nose as soon as you turn, "
              "letting blinding sunlight in.\n"
              "• Eye Pressure: Lack of contoured depth squashes your eyelids and "
              "eyelashes.\n"
              "• Poor Fit: Straps that slip or pinch the ears.")
INTRO_A_H2 = "How I Tested Each Sleep Mask"
INTRO_A_P3 = ("To find a mask that actually fixed these issues, I tested five masks "
              "for 35 days in a row. I wore each one for 7 days after my shifts, in "
              "bed, and even resting in my car.")
INTRO_A_P4 = ("I evaluated each mask against these criteria:\n"
              "✔️ Light Leakage: Does it hold a true blackout in any position?\n"
              "✔️ Eye Cup Depth: Is there space to blink without eye pressure?\n"
              "✔️ Nose Seal: Does it have the right contour to prevent light "
              "sneaking in?\n"
              "✔️ Breathable Material: Is it soft, hypoallergenic, and "
              "skin-friendly?\n"
              "✔️ Secure Fit: Does the strap stay put without pinching?")
INTRO_A_P5 = ("Here is what I discovered after 35 days of testing and the mask that "
              "finally fixed my sleep.")

# Variant B -- qualifier questions 983:3250 + intro 983:3254.
QUESTIONS_B = ["Do you sleep on your side?",
               "Does light sneak in at the nose by morning?",
               "Don't want to pay £67 to find out a mask doesn't work?"]
INTRO_B_P1 = ("Then this test is for you. We bought the 5 most popular blackout masks "
              "under £75, all with our own money: Manta, Manta PRO, MZOO, Alaska Bear "
              "and a £33 newcomer, the HLTH Sleep Mask.")
INTRO_B_P2 = ("I work nights and sleep by day, on my side. So I tested every mask the "
              "hard way: in daylight, with my cheek on the pillow.")
# PLACEHOLDER 4 -- [NUMBER] is unfilled in the design and stays unfilled.
INTRO_B_P3 = [("ib", "How we tested:"),
              ("ir", " each mask was worn for [NUMBER] days of daytime sleep. We "
                     "checked light at the nose and sides, pressure on the eyes and "
                     "lashes, whether it stayed on, comfort on your side, and the "
                     "price. No brand saw this article before it went live.")]
# PLACEHOLDER 5 -- [TO CONFIRM: ...] is unfilled in the design and stays unfilled.
INTRO_B_P4 = [("ib", "The winner: the HLTH Sleep Mask."),
              ("ir", " At £33, it [TO CONFIRM: result vs the others]. Here's how all "
                     "five stack up, and why.")]

REAL_TALK_H2 = "The Real Talk: What This Test Taught Me"
REAL_TALK = [
    [("bg", 'I went in thinking every mask was the same. They all say "total blackout." After '),
     ("bk", "35"),
     ("bg", " days of sleeping through daylight, on my side, I know they're not.")],
    [("bg", "The winner wasn't the priciest. At £33, HLTH beat a mask that costs more than twice as much. "),
     ("bk", "It was the only one that stayed dark on my side.")],
    [("jh", "The nose is where masks fail."),
     ("bg", " Most of the light I saw came in at the nose, not the sides. "),
     ("bk", "Four of the five masks let light in there.")],
    [("jh", "Side sleeping changes everything."),
     ("bg", " A mask that feels fine on your back can dig in or slide off once your cheek hits the pillow.")],
]
REAL_TALK_LAST = ("Your eyes need room. Deep cups mean nothing rests on your eyes or "
                  "lashes all night.")

# Buybox -- 983:2831. Placeholders 1 and 3 are hidden in Figma, shown here (decision 1).
BUY_BADGE = "★ #1 BEST OVERALL"
BUY_NAME = "HLTH Sleep Mask"
BUY_RATING_PLACEHOLDER = "★★★★★ [RATING] · [REVIEW COUNT] reviews"
# ⚠️ 2026-11-04: dynamic (convertible) pricing, per the standing rule that every
# TechUnboxed page gets this from now on. Our own figure is the live Shopify
# GBP price (handle `hlth-sleep-mask`, GET https://hlthtrack.com/api/prices?
# handle=hlth-sleep-mask -> £33.00 GB), tagged data-price="price" so the hosted
# script at hlthtrack.com/dynamic-currency.js can convert it per visitor.
# Competitor figures were USD in the original copy and had no GBP source to
# match, so they are converted at the same mid-market basis the converter
# itself uses (GET https://app.hlthtrack.com/api/fx, rate USD 1.341529 on
# 2026-11-04) and tagged data-fx-gbp -- editorial, not a quote, same basis
# already accepted for this treatment elsewhere (see CURRENCY_CONVERTER.md).
BUY_PRICE = '<span data-price="price">£33</span>'
BUY_RRP_PLACEHOLDER = "[RRP]"
BUY_TP_TEXT = [("tb", "Excellent"), ("tr", " "), ("ts", "[RATING]"), ("tr", " | "),
               ("ts", "[REVIEW COUNT]"), ("tr", " reviews on Trustpilot")]
# NOTE the double space after the tick -- it is in the node, so it is kept with &nbsp;
BUY_FEATURES = ["✓  Winged nose bridge for a light-tight seal",
                "✓  Slim 5mm sides for side sleepers",
                "✓  Deep 20mm eye cups, nothing on your lashes"]
BUY_CTA = "CHECK AVAILABILITY →"
BUY_GUARANTEE = "30-night guarantee"

FOOT_DISCLAIMER_H = "DISCLAIMER"
FOOT_DISCLAIMER = ("This is a sponsored article. Products were bought at retail and "
                   "tested by our editors. Prices and availability were checked on "
                   "October 23, 2026 and may change. Tech Unboxed may earn a "
                   "commission from links on this page.")
FOOT_COPY = "© 2026 TechUnboxed."
FOOT_LINKS = [("Terms", "tu-terms", "terms"), ("Privacy", "tu-priv", "priv"),
              ("Editorial standards", "tu-edit", "edit"),
              ("Affiliate policy", "tu-aff", "aff")]
SPONSORED = "SPONSORED ARTICLE"

REVIEWS = [
  {
   'img': 'rev1',
   'num': '#1 ',
   'name': 'HLTH Sleep Mask',
   'by': ' by HLTH',
   'price': 'Price: <span data-price="price">£33</span>',
   'subtitle': 'The One Built For Side Sleepers',
   'body': 'I\'ll be honest: I\'d never heard of HLTH before this test. What caught my eye was one line. They scanned 35 faces to shape it. Every mask says "total blackout." This one told me how it gets there.',
   'lead': 'How the HLTH Mask performed:',
   'bullets': [
     [('j', 'Blackout:'), ('li', ' '), ('lk', 'Pitch black, even at the nose')],
     [('j', 'Side sleeping:'), ('li', ' '), ('lk', 'Surprisingly no issues, even fully on my side')],
     [('j', 'Comfort:'), ('li', ' '), ('lk', 'So light I forgot I had it on (35g)')],
     [('j', 'Eye clearance:'), ('li', ' '), ('lk', 'Could blink freely (20mm cups)')],
     [('j', 'Stays on:'), ('li', ' '), ('lk', 'Still in place every single morning')],
     [('j', 'Ears:'), ('li', ' '), ('lk', 'No sore ears, even after 7 days')],
   ],
   'apart': [('j', 'What sets it apart:'), ('li', " The nose. Most masks leak there. HLTH's winged nose bridge was built from those 35 face scans to seal it. The strap also sits above your ears, not on them.")],
   'pros': [
     '✅ Built from 35 face scans',
     '✅ Winged nose bridge for light at the nose',
     '✅ 5mm tapered sides for side sleepers',
     '✅ 20mm-deep eye cups',
     '✅ Strap sits above the ears',
     '✅ 30-night guarantee',
   ],
   'cons': [
     '❌ Black only at launch',
     '❌ Not for face-down stomach sleepers',
   ],
   'bottom': [('j', 'Bottom line:'), ('bg', ' '), ('bk', 'It was the only mask that stayed dark at the nose when I slept on my side. It took one night to get used to the strap. After that, I forgot it was there.')],
  },
  {
   'img': 'rev2',
   'num': '#2 ',
   'name': 'Manta Sleep Mask',
   'by': ' by Manta Sleep',
   'price': 'Price: <span data-fx-gbp="29">£29</span>',
   'subtitle': 'Big Name, Back-Sleeper Fit',
   'body': 'Manta is the mask everyone talks about. The eye cups move and come off, so you can set them where you want. I wanted to know if that works when you sleep on your side.',
   'lead': 'How the Manta performed:',
   'bullets': [
     [('j', 'Blackout:'), ('lg', ' '), ('lk', 'Dark on my back, leaked at the nose on my side')],
     [('j', 'Side sleeping:'), ('lg', ' '), ('lk', 'Bulky. My pillow pushed it up')],
     [('j', 'Comfort:'), ('lg', ' '), ('lk', 'Cups pressed on my eyes by midday')],
     [('j', 'Eye clearance:'), ('lg', ' '), ('lk', 'Good room, after a few tries')],
     [('j', 'Stays on:'), ('lg', ' '), ('lk', 'Slid up on 2 of my 7 days')],
   ],
   'apart': [('j', 'What sets it apart:'), ('lg', " You can move the cups. That's handy if your face is hard to fit. But in my test, "), ('lk', 'the cups shifted when my cheek hit the pillow, and light got in at the nose'), ('lg', '.')],
   'pros': [
     '✅ Adjustable, removable eye cups',
     '✅ Strong blackout lying on your back',
     "✅ Lowest price of Manta's adult masks",
   ],
   'cons': [
     '❌ Reviewers report light at the nose',
     "❌ Reviewers say it's hard to side-sleep in",
     '❌ Some reviewers wake with it moved',
   ],
   'bottom': [('j', 'Bottom line:'), ('bg', ' '), ('bk', 'Great on your back. On your side, light got in at the nose.')],
  },
  {
   'img': 'rev3',
   'num': '#3 ',
   'name': 'Manta PRO',
   'by': ' by Manta Sleep',
   'price': 'Price: From <span data-fx-gbp="63">£63</span>',
   'subtitle': 'Made For Side Sleep, At More Than Twice The Price',
   'body': "Manta says the PRO's C-shaped cups are made for side sleep. It has perforated foam and a mesh strap. At more than twice the HLTH price, I expected it to win.",
   'lead': 'How the Manta PRO performed:',
   'bullets': [
     [('j', 'Blackout:'), ('lg', ' '), ('lk', 'Mostly dark, a little light at the nose')],
     [('j', 'Side sleeping:'), ('lg', ' '), ('lk', 'The cups dug into my cheek')],
     [('j', 'Comfort:'), ('lg', ' '), ('lk', 'Soft on my back, not on my side')],
     [('j', 'Eye clearance:'), ('lg', ' '), ('lk', 'Plenty of room for my eyes')],
     [('j', 'Stays on:'), ('lg', ' '), ('lk', 'Stayed put, but the strap hurt my ear')],
   ],
   'apart': [('j', 'What sets it apart:'), ('lg', ' The cup shape. Manta built it for side sleepers, and some reviewers love it. Others say the cups dig in. In my test, '), ('lk', 'I woke up to roll over more than once'), ('lg', '.')],
   'pros': [
     '✅ C-shaped eye cups made for side sleep',
     '✅ Perforated foam and mesh strap',
     '✅ Adjustable, removable eye cups',
   ],
   'cons': [
     '❌ More than twice the price of HLTH',
     '❌ Reviewers say the cups dig in on your side',
     '❌ Reviewers report strap pressure at the ears',
   ],
   'bottom': [('j', 'Bottom line:'), ('bg', ' '), ('bk', 'A good mask for back sleepers. On my side, it was not comfy enough.')],
  },
  {
   'img': 'rev4',
   'num': '#4 ',
   'name': 'MZOO Sleep Mask',
   'by': ' by MZOO',
   'price': 'Price: <span data-fx-gbp="13.41">£13.41</span>',
   'subtitle': 'Deep Foam, Bulky Sides',
   'body': "MZOO has 3D contoured memory foam cups. It's a popular budget pick. I wanted to see if the thick foam works when you sleep on your side.",
   'lead': 'How the MZOO performed:',
   'bullets': [
     [('j', 'Blackout:'), ('lg', ' '), ('lk', 'Light at the nose every day')],
     [('j', 'Side sleeping:'), ('lg', ' '), ('lk', 'Too thick to lie on')],
     [('j', 'Comfort:'), ('lg', ' '), ('lk', 'The strap pressed on my ears')],
     [('j', 'Eye clearance:'), ('lg', ' '), ('lk', 'Lots of room for my eyes')],
     [('j', 'Stays on:'), ('lg', ' '), ('lk', 'Slid on 4 of my 7 days')],
   ],
   'apart': [('j', 'What sets it apart:'), ('lg', ' Deep, padded cups at a budget price. The trade-off is bulk at the sides. In my test, '), ('lk', 'my pillow pushed it up, and sunlight came in at the nose'), ('lg', '.')],
   'pros': [
     '✅ 3D contoured memory foam cups',
     '✅ Budget price',
     '✅ Comes with earplugs and a pouch',
   ],
   'cons': [
     '❌ Reviewers report gaps at the nose',
     '❌ Reviewers call it too bulky for side sleepers',
     '❌ Reviewers say the strap digs into the ears',
   ],
   'bottom': [('j', 'Bottom line:'), ('bg', ' '), ('bk', 'Good value if you sleep on your back. Too bulky for side sleepers.')],
  },
  {
   'img': 'rev5',
   'num': '#5 ',
   'name': 'Alaska Bear Mulberry Silk Sleep Mask',
   'by': ' by Alaska Bear',
   'price': 'Price: <span data-fx-gbp="11.92">£11.92</span>',
   'subtitle': 'Soft Silk, Flat Fit',
   'body': "Alaska Bear is mulberry silk with an adjustable strap. It's light and cheap. But it has a flat design, so I wanted to see what that means for my eyes.",
   'lead': 'How the Alaska Bear performed:',
   'bullets': [
     [('j', 'Blackout:'), ('lg', ' '), ('lk', 'Light at the nose most days')],
     [('j', 'Side sleeping:'), ('lg', ' '), ('lk', 'Moved every time I rolled over')],
     [('j', 'Comfort:'), ('lg', ' '), ('lk', 'Silky soft, but flat on my lashes')],
     [('j', 'Eye clearance:'), ('lg', ' '), ('lk', 'None. It sat right on my eyes')],
     [('j', 'Stays on:'), ('lg', ' '), ('lk', 'Slipped off 3 times in 7 days')],
   ],
   'apart': [('j', 'What sets it apart:'), ('lg', " The silk and the price. It's soft and easy to pack. In my test, "), ('lk', 'light leaked in at the nose by midday'), ('lg', '.')],
   'pros': [
     '✅ Mulberry silk, soft on skin',
     '✅ Very cheap',
     '✅ Light enough for travel',
   ],
   'cons': [
     '❌ Flat design rests on your eyes',
     '❌ Reviewers report light at the nose',
     '❌ Reviewers say it slips off at night',
   ],
   'bottom': [('j', 'Bottom line:'), ('bg', ' '), ('bk', 'Soft and cheap, but it did not block light at the nose for me.')],
  },
]

def spacer8():
    """Figma 983:2632 / 983:2635 -- an 8px spacer frame between intro blocks."""
    return container([], [{"prop": "height", "value": "8px"},
                          {"prop": "width", "value": "100%"},
                          {"prop": "lfDisplay", "value": "block"}])


# ======================================================= page chrome
# Header 983:2577 -- full-bleed #1C1C1E bar, paddingTop 8, itemSpacing 10, centred.
# The frame is 94 tall against 8 + 16 + 10 + 42 of content, so the remaining 18 is
# reproduced as paddingBottom rather than a fixed height.
header = section(
    [col([text(SPONSORED, fs="10px", lh="16px", color=GREY_BD, ls="0.15em", auto=True,
               m={"fontSize": "13px"}),
          image("logo", w="166px", h="42px", fit="contain", title_attr="logo")],
         gap="10px", styles=[{"prop": "alignItems", "value": "center"}])],
    styles=[{"prop": "backgroundColor", "value": HEAD_BG},
            {"prop": "padding", "value": pad(8, 0, 18, 0)}])

# Footer 983:2864 -- #232326, paddingTop/Bottom 48, itemSpacing 14, centred, content
# column 720 wide (1440 less 360 either side).
def footer_link(label, target, el_id):
    return text('<a href="#%s" id="%s" style="color:#BDBDBD;text-decoration:none">%s</a>'
                % (target, el_id, esc(label)),
                fs="13px", lh="16px", color=GREY_BD, auto=True)

footer = section(
    [col([image("logo", w="166px", h="42px", fit="contain"),
          text(FOOT_DISCLAIMER_H, fs="12px", lh="16px", weight="700", color=WHITE,
               align="center"),
          text(esc(FOOT_DISCLAIMER), fs="12.5px", lh="20px", color=FOOT_TXT,
               align="center"),
          row([text(FOOT_COPY, fs="13px", lh="16px", weight="600", color=WHITE, auto=True)]
              + [footer_link(*l) for l in FOOT_LINKS],
              gap="10px", align="center", justify="center", wrap=True)],
         gap="14px",
         styles=[{"prop": "alignItems", "value": "center"},
                 {"prop": "maxWidth", "value": "720px"},
                 {"prop": "margin", "value": {"left": "auto", "right": "auto"}}])],
    styles=[{"prop": "backgroundColor", "value": FOOT_BG},
            {"prop": "padding", "value": pad(48, 16, 48, 16)}])

# ======================================================= article
kids = []

# Breadcrumb 983:2594 -- H, gap 4, wrap, centred. Plain text, not links (decision 4).
kids.append(row([text(esc(t), fs="14px", lh="17px", color=c, auto=True,
                      m={"fontSize": "15px", "lineHeight": "22px"})
                 for t, c in BREADCRUMB],
                gap="4px", align="center", wrap=True, justify="flex-start"))

# H1 983:2600 / 983:3224 -- the page's only h1.
kids.append(title(esc(H1_A if IS_A else H1_B), "40px", "46px", weight="800", color=INK,
                  font=SANS, level="1",
                  m={"fontSize": "24px", "lineHeight": "30px", "fontWeight": "900"}))

# Subhead 983:2601 / 983:3225 -- a standfirst, deliberately not a heading element.
kids.append(text(esc(SUB_A if IS_A else SUB_B), fs="28px", lh="34px", weight="700",
                 color=INK, m={"fontSize": "20px", "lineHeight": "27px"}))

# Tags + byline 983:2602 -- H, gap 10, wrap (counterAxisSpacing 10 == the same gap).
def tag(label, bg, fg):
    return container([text(esc(label), fs="13px", lh="26px", weight="700", color=fg,
                           auto=True)],
                     [{"prop": "backgroundColor", "value": bg},
                      {"prop": "borderRadius", "value": "6px"},
                      {"prop": "padding", "value": pad(6, 16, 6, 16)},
                      {"prop": "lfDisplay", "value": "flex"},
                      {"prop": "alignItems", "value": "center"},
                      {"prop": "width", "value": "fit-content"},
                      {"prop": "flexShrink", "value": "0"}])

kids.append(row([tag("Buying Guides", BLUE_TAG, WHITE),
                 tag("↗ Trending", LIME_TAG, INK_TAG),
                 text("By", fs="15px", lh="26px", color=BYLINE_LBL, auto=True),
                 text(esc(BYLINE_NAME), fs="15px", lh="26px", color=BYLINE_NM, auto=True)],
                gap="10px", align="center", wrap=True, justify="flex-start"))

kids.append(text(esc(LAST_UPDATED), fs="15px", lh="24px", color=GREY_UPD))

# Hero 983:2610 -- the split photo box (decision 7) plus its credit line, gap 16.
HERO_HTML = (
    '<div class="sm-hero">'
    '<div class="a"><img src="%s" alt="%s" title="hero" loading="eager" '
    'fetchpriority="high"></div>'
    '<div class="b"><img src="%s" alt="%s" loading="eager"></div>'
    '</div>') % (IMG["hero_left"]["src"], esc(ALT["hero_left"]),
                 IMG["hero_right"]["src"], esc(ALT["hero_right"]))
kids.append(col([html(HERO_HTML),
                 text(esc(IMAGE_CREDIT), fs="14px", lh="22px", color=MUTED,
                      m={"fontSize": "17px", "lineHeight": "28px"})],
                gap="16px"))

# Qualifier questions 983:3250 -- variant B only; the A frame (983:2626) is hidden.
if not IS_A:
    kids.append(col([text(esc(q), fs="17px", lh="23px", weight="700", color=INK,
                          m={"lineHeight": "27px"}) for q in QUESTIONS_B],
                    gap="20px", styles=[{"prop": "gap", "value": "16px", "media": 767}]))

# Intro copy 983:2630 / 983:3254
if IS_A:
    intro = [*(text(esc(p), color=BODY) for p in INTRO_A_P1),
             spacer8(),
             title(esc(INTRO_A_H1), "17px", "29px", weight="700", color=BODY, font=SANS,
                   level="2"),
             text(esc(INTRO_A_P2), color=BODY),
             spacer8(),
             title(esc(INTRO_A_H2), "17px", "29px", weight="700", color=BODY, font=SANS,
                   level="2"),
             text(esc(INTRO_A_P3), color=BODY),
             text(esc(INTRO_A_P4), color=BODY),
             text(esc(INTRO_A_P5), color=BODY)]
else:
    intro = [text(esc(INTRO_B_P1), color=BODY),
             text(esc(INTRO_B_P2), color=BODY),
             rich(INTRO_B_P3, fs="17px", lh="29px", color=BODY),
             rich(INTRO_B_P4, fs="17px", lh="29px", color=BODY)]
kids.append(col(intro, gap="16px"))

# ======================================================= the ranking
def review_card(r):
    heading = ('<span class="sm-jh">%s</span><span class="sm-nm">%s</span>'
               '<span class="sm-jh">%s</span>') % (esc(r["num"]), esc(r["name"]),
                                                   esc(r["by"]))
    jost = dict(fs="15px", lh="22px", weight="600", color=JINK, font=JOST,
                m={"fontSize": "14px", "lineHeight": "20px"})
    bask = dict(fs="16px", lh="27px", color=LBINK, font=BASK,
                m={"fontSize": "15px", "lineHeight": "25px"})

    bullets = []
    for runs in r["bullets"]:
        bullets.append(row(
            [text("▪", fs="10px", lh="27px", color=JINK, font=BASK,
                  m={"lineHeight": "25px"},
                  extra=[{"prop": "flexShrink", "value": "0"},
                         {"prop": "width", "value": "10px"}]),
             rich(runs, fs="15px", lh="27px", color=JINK, font=BASK,
                  m={"fontSize": "14px", "lineHeight": "25px"},
                  extra=[{"prop": "flex", "value": "1"},
                         {"prop": "minWidth", "value": "0"}])],
            gap="10px", align="flex-start",
            styles=[{"prop": "padding", "value": pad(l=20)},
                    {"prop": "padding", "value": pad(l=8), "media": 767}]))

    return col([
        title(heading, "16px", "23px", weight="400", color=None, font=BASK, level="3",
              m={"fontSize": "15px", "lineHeight": "22px"}),
        # NOT esc() -- r["price"] carries a deliberate data-price/data-fx-gbp
        # span for the dynamic-currency script, same pattern rich() already
        # uses for inline styling spans in this file.
        text(r["price"], **jost),
        image(r["img"], h="498px", mh="269px", radius="4px",
              styles=[{"prop": "backgroundColor", "value": PHOTO_BG}]),
        text(esc(r["subtitle"]), **jost),
        text(esc(r["body"]), **bask),
        text(esc(r["lead"]), **jost),
        col(bullets, gap="4px"),
        rich(r["apart"], fs="15px", lh="27px", color=JINK, font=BASK,
             m={"fontSize": "14px", "lineHeight": "25px"}),
        col([text(esc(p), **bask) for p in r["pros"]], gap="0px"),
        col([text(esc(c), **bask) for c in r["cons"]], gap="0px"),
        rich(r["bottom"], fs="16px", lh="27px", color=LBINK, font=BASK,
             m={"fontSize": "15px", "lineHeight": "25px"}),
    ], gap="18px", styles=[{"prop": "gap", "value": "14px", "media": 767}])

# "THE RESULTS" kicker 983:2952 / 983:3566 -- present ONLY in the mobile frames.
kicker = container(
    [text(esc(KICKER), fs="12px", lh="15px", weight="700", color=RED, ls="1.2px")],
    [{"prop": "width", "value": "100%"},
     {"prop": "lfDisplay", "value": "none"},
     {"prop": "lfDisplay", "value": "block", "media": 767}])

kids.append(col(
    [kicker,
     title(esc(RANK_H2), "30px", "36px", weight="900", color=INK, font=SANS, level="2",
           m={"fontSize": "24px", "lineHeight": "29px"})]
    + [review_card(r) for r in REVIEWS],
    gap="56px", styles=[{"prop": "gap", "value": "40px", "media": 767}]))

# ======================================================= The Real Talk 983:2824
kids.append(col(
    [title(esc(REAL_TALK_H2), "30px", "38px", weight="700", color=JINK, font=JOST,
           level="2", m={"fontSize": "24px", "lineHeight": "30px"})]
    + [rich(runs, fs="16px", lh="27px", color=LBINK, font=BASK,
            m={"fontSize": "15px", "lineHeight": "25px"}) for runs in REAL_TALK]
    + [text(esc(REAL_TALK_LAST), fs="16px", lh="27px", weight="600", color=JINK,
            font=JOST, m={"fontSize": "15px", "lineHeight": "25px"})],
    gap="18px",
    styles=[{"prop": "padding", "value": pad(t=40)},
            {"prop": "padding", "value": pad(t=28), "media": 767},
            {"prop": "gap", "value": "14px", "media": 767}]))

# ======================================================= Buybox 983:2831
def tp_stars():
    tile = ('<span style="display:inline-flex;align-items:center;justify-content:center;'
            'width:20px;height:20px;background:#00B67A;color:#ffffff;font-size:14px;'
            'font-weight:700;line-height:17px;font-family:%s">★</span>') % SANS
    return ('<span style="display:inline-flex;gap:2px;vertical-align:middle">%s</span>'
            % (tile * 5))

buy_details = col([
    container([text(esc(BUY_BADGE), fs="11px", lh="13px", weight="700", color=WHITE,
                    auto=True)],
              [{"prop": "backgroundColor", "value": RED},
               {"prop": "borderRadius", "value": "4px"},
               {"prop": "padding", "value": pad(4, 10, 4, 10)},
               {"prop": "lfDisplay", "value": "flex"},
               {"prop": "width", "value": "fit-content"}]),
    text(esc(BUY_NAME), fs="28px", lh="34px", weight="900", color=INK,
         m={"fontSize": "24px", "lineHeight": "29px"}),
    # PLACEHOLDER 1 -- hidden in Figma, shown here on purpose (decision 1).
    text(esc(BUY_RATING_PLACEHOLDER), fs="13px", lh="16px", weight="600", color=INK),
    row([text(BUY_PRICE, fs="30px", lh="36px", weight="900", color=RED, auto=True),
         # PLACEHOLDER 3 -- hidden in Figma, shown here, keeping the node's strikethrough.
         text('<span style="text-decoration:line-through">%s</span>'
              % esc(BUY_RRP_PLACEHOLDER),
              fs="16px", lh="19px", color=MUTED, auto=True)],
        gap="10px", align="center", justify="flex-start",
        styles=[{"prop": "width", "value": "fit-content"}]),
    col([row([html(tp_stars(), styles=[{"prop": "width", "value": "auto"},
                                       {"prop": "flexShrink", "value": "0"}]),
              row([text("★", fs="18px", lh="22px", weight="700", color=TP_GREEN,
                        auto=True),
                   text("Trustpilot", fs="15px", lh="18px", weight="700", color=INK,
                        auto=True)],
                  gap="3px", align="center",
                  styles=[{"prop": "width", "value": "fit-content"}])],
             gap="10px", align="center", justify="flex-start",
             styles=[{"prop": "width", "value": "fit-content"}]),
         # PLACEHOLDER 2 -- visible in the design, reproduced verbatim.
         rich(BUY_TP_TEXT, fs="13px", lh="16px", color=INK)],
        gap="6px"),
] + [text(esc(f).replace("  ", "&nbsp; "), fs="14px", lh="17px", color=BODY)
     for f in BUY_FEATURES] + [
    # CTA: a styled box, not a link -- the design gives no destination (decision 3).
    container([text(esc(BUY_CTA), fs="16px", lh="19px", weight="700", color=WHITE,
                    auto=True)],
              [{"prop": "backgroundColor", "value": RED},
               {"prop": "borderRadius", "value": "6px"},
               {"prop": "padding", "value": pad(16, 0, 16, 0)},
               {"prop": "lfDisplay", "value": "flex"},
               {"prop": "alignItems", "value": "center"},
               {"prop": "justifyContent", "value": "center"},
               {"prop": "width", "value": "100%"}]),
    text(esc(BUY_GUARANTEE), fs="12px", lh="15px", color=MUTED, align="center"),
], gap="10px", styles=[{"prop": "flex", "value": "1"},
                       {"prop": "minWidth", "value": "0"}])

kids.append(row(
    [image("buybox", w="250px", h="304px", mw="100%", mh="300px", radius="6px",
           styles=[{"prop": "flexShrink", "value": "0"}]),
     buy_details],
    gap="24px", align="flex-start",
    styles=[{"prop": "backgroundColor", "value": BUY_BG},
            {"prop": "borderStyle", "value": "solid"},
            {"prop": "borderColor", "value": RED},
            {"prop": "borderWidth", "value": "2px"},
            {"prop": "borderRadius", "value": "10px"},
            {"prop": "padding", "value": pad(24, 24, 24, 24)},
            {"prop": "flexDirection", "value": "column", "media": 767},
            {"prop": "gap", "value": "16px", "media": 767},
            {"prop": "padding", "value": pad(16, 16, 16, 16), "media": 767}]))

# Article frame 983:2593 -- V, itemSpacing 16, paddingTop 24 / Bottom 48, and a
# 388 side inset on desktop (the 664 column) that becomes a 16 gutter on mobile.
article = section(
    [col(kids, gap="16px",
         styles=[{"prop": "padding", "value": pad(r=16, l=16), "media": 767}])],
    styles=[{"prop": "backgroundColor", "value": WHITE},
            {"prop": "padding", "value": pad(24, 0, 48, 0)}],
    layout="boxed")

body = {"id": nid(), "t": "Root", "version": 11,
        "styles": [{"prop": "pageWidth", "value": "664px"},
                   {"prop": "backgroundColor", "value": WHITE}],
        "p": {"children": [header, article, footer]}}

# ---------------------------------------------------------------- sanity check
def _scan(nd, path="root"):
    bad = []
    if isinstance(nd, dict):
        if "t" in nd and "id" not in nd:
            bad.append(path + " missing id")
        for k, v in nd.items():
            if v is None:
                bad.append(path + "." + k + " None")
            bad += _scan(v, path + "." + str(k))
    elif isinstance(nd, list):
        for i, x in enumerate(nd):
            bad += _scan(x, path + "[%d]" % i)
    return bad

iss = _scan(body)
print("sanity issues:", len(iss))
for x in iss[:10]:
    print("  !", x)

# Every placeholder must survive into the body, on the variant that owns it.
def _plain(nd, out):
    """Every rendered string in the body, with tags stripped and entities decoded."""
    if isinstance(nd, dict):
        c = (nd.get("p") or {}).get("content")
        if isinstance(c, str):
            t = re.sub(r"<[^>]+>", "", c)
            t = (t.replace("&nbsp;", " ").replace("&quot;", '"').replace("&lt;", "<")
                  .replace("&gt;", ">").replace("&amp;", "&"))
            out.append(t)
        for v in nd.values():
            _plain(v, out)
    elif isinstance(nd, list):
        for v in nd:
            _plain(v, out)
    return out

_text = "\n".join(_plain(body, []))
MUST = [BUY_RATING_PLACEHOLDER, BUY_RRP_PLACEHOLDER,
        "Excellent [RATING] | [REVIEW COUNT] reviews on Trustpilot"]
if not IS_A:
    MUST += ["[NUMBER] days of daytime sleep", "[TO CONFIRM: result vs the others]"]
missing = [m for m in MUST if m not in _text]
if missing:
    raise SystemExit("placeholder(s) lost from the body: %r" % missing)
print("placeholders present:", len(MUST))

# ---------------------------------------------------------------- SEO
TITLE = H1_A if IS_A else H1_B
SEO_A = {
    "title": "I Tried 5 Sleep Masks For Side Sleepers: What Happened",
    "description": ("I wore five blackout sleep masks for 35 nights of daytime sleep, "
                    "on my side. Four leaked light at the nose. See which £33 mask "
                    "stayed pitch black until morning."),
    "keywords": ("best sleep mask, sleep mask for side sleepers, blackout sleep mask, "
                 "HLTH Sleep Mask, Manta Sleep review, Manta PRO, MZOO sleep mask, "
                 "Alaska Bear silk mask, sleep mask nose gap"),
    "social_image_uid": IMG["social"]["src_uid"],
}
SEO_B = {
    "title": "We Tested The Top 5 Blackout Sleep Masks Under £75",
    "description": ("We bought the 5 most popular blackout sleep masks under £75 and "
                    "slept on our side in daylight. Only one stayed dark at the nose, "
                    "and it costs just £33."),
    "keywords": ("blackout sleep mask, best sleep mask under 100, sleep mask for side "
                 "sleepers, HLTH Sleep Mask, Manta Sleep Mask, Manta PRO, MZOO, "
                 "Alaska Bear silk sleep mask, sleep mask comparison"),
    "social_image_uid": IMG["social"]["src_uid"],
}
SEO = SEO_A if IS_A else SEO_B
assert 140 <= len(SEO["description"]) <= 160, len(SEO["description"])

# QA: settings.seo emits og:* only, so X would show no card. Add the twitter:* tags
# explicitly, from the same values.
def _esc_attr(v):
    return v.replace("&", "&amp;").replace('"', "&quot;").replace("<", "&lt;").replace(">", "&gt;")

# Dynamic (convertible) pricing, mandatory on every new TechUnboxed page as of
# 2026-11-04. This is the PAGE TAG, not the inline logic block -- the logic
# itself is hosted at hlthtrack.com/dynamic-currency.js since 2026-09-27, and
# this snippet is a small anti-flash stub plus a deferred <script src> that
# loads it. See snippets/dynamic-currency-page-tag.html for why it is shaped
# this way (resilience over flash-prevention, fails safe to the GBP text
# already baked into the page).
DYNAMIC_CURRENCY_TAG = open(
    "snippets/dynamic-currency-page-tag.html", encoding="utf-8").read().strip()

CUSTOM_HTML = {
    "header": PERF + (
        '<meta name="twitter:card" content="summary_large_image">\n'
        '<meta name="twitter:title" content="%s">\n'
        '<meta name="twitter:description" content="%s">\n'
        '<meta name="twitter:image" content="%s">\n'
    ) % (_esc_attr(SEO["title"]), _esc_attr(SEO["description"]), IMG["social"]["src"])
    + DYNAMIC_CURRENCY_TAG + "\n",
    "footer": PERF_FOOTER}

# ---------------------------------------------------------------- write
guard(FUNNEL, STEP_SLUG)

existing = sgql(
    'query($q: String!){ funnels(first:1,query:$q){ edges { node { id starting_step_id '
    'steps { id uid slug title type settings visual { x y } } } } } }',
    {"q": "id:%s" % FUNNEL})["funnels"]["edges"][0]["node"]
existing_steps = existing["steps"]
collide = next((s for s in existing_steps if s["slug"] == STEP_SLUG), None)

step_node = {"slug": STEP_SLUG, "title": TITLE, "type": "article_page",
             "settings": {"custom_html": CUSTOM_HTML, "seo": SEO},
             "visual": VISUAL, "body": body}

if collide:
    others = [{"id": s["id"], "slug": s["slug"], "title": s["title"], "type": s["type"],
               "settings": s["settings"], "visual": s["visual"]}
              for s in existing_steps if s["slug"] != STEP_SLUG]
    step_id = collide["id"]
    new_steps = others + [dict(step_node, id=step_id, visual=collide["visual"])]
    print("redeploying existing step ->", step_id)
else:
    created = sgql('mutation($fid: ID!, $node: InputStep!){ createStep(funnel_id:$fid, '
                   'node:$node){ step { id uid } } }',
                   {"fid": FUNNEL, "node": step_node})["createStep"]["step"]
    step_id = created["id"]
    print("created detached step ->", created)
    # Siblings are echoed back unchanged. `settings` is non-null in InputUpdateStep,
    # so it has to be re-sent even though nothing about it changes; omitting it fails
    # the whole mutation and leaves the new step created-but-detached.
    new_steps = [{"id": s["id"], "slug": s["slug"], "title": s["title"],
                  "type": s["type"], "settings": s["settings"], "visual": s["visual"]}
                 for s in existing_steps]
    new_steps.append(dict(step_node, id=step_id))

node = {"published": True, "steps": new_steps}
# Variant A is the entry page. Variant B must never reassign it.
if IS_A:
    node["starting_step_id"] = step_id

r = sgql('mutation($id: ID!, $node: InputFunnel!){ updateFunnel(id:$id,node:$node){ id '
         'starting_step_id published steps { uid slug title } } }',
         {"id": FUNNEL, "node": node})
print("WROTE", json.dumps(r["updateFunnel"], indent=2))
print("LIVE  https://www.techunboxed.co/sleep-masks/%s" % STEP_SLUG)
