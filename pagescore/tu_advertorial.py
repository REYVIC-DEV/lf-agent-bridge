#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""TechUnboxed advertorial engine -- the machinery every page on this template shares.

Four live advertorials sit on top of this (V-B control + B5, V-A control + A1), and
they share more than styling: the same Gelasio/Inter stacks, the same zero-CLS font
recipe, the same LF write sequence, the same currency-tagging contract, the same
guard. Duplicating that per page is how a compliance fix lands on three pages out of
four, so it lives here once.

WHAT IS *NOT* HERE, deliberately: page chrome, the article body and the footer. Those
carry copy, and copy is read per design frame by node id -- V-A's support bar and
V-B's are separate Figma nodes that happen to say the same thing today. Each variant
module builds its own from its own dump, which is the "measure, don't guess" rule.
(The chrome copy IS currently identical across the two designs. Sharing it is a real
opportunity, but it means one module owning four live pages' legal text, so it is
flagged for a human rather than done on the way past.)

CONFIGURE BEFORE USE. `configure(img_map, alt_map)` supplies the page's own image
library and alt text; the image helpers read them. A variant module calls it at import.

LENIS IS NO LONGER HANDLED HERE. Smooth scroll ships inside the funnel-level tracker
header (`snippets/tracker-header-meta-block.html`), which every funnel carries, so a
per-step copy would be a SECOND Lenis: two libraries from two CDNs running two rAF
loops against one scrollTop. The per-step block and its `lenis=` switch were removed
on 2026-10-04. Nothing here installs smooth scroll; the funnel header does.
"""
import sys, os, json, uuid, re
import html as _html
sys.path.insert(0, '.')
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import lf_api
from deploy_guard import guard

tok = open('.session_token').read().strip() if os.path.exists('.session_token') else ''
ACCT = open('.lf_account').read().strip() if os.path.exists('.lf_account') else ''
HH = {"account-id": ACCT, "version": "1",
      "Origin": "https://app.lightfunnels.com", "Referer": "https://app.lightfunnels.com/"}
def sgql(q, v=None): return lf_api.gql(tok, q, v, extra_headers=HH)
def nid(): return str(uuid.uuid4())

FUNNEL = os.environ.get("VB_FUNNEL", "fun_Z6I8-bN5nVJ_SwGgR9WWK")
PAGE_BASE = "https://www.techunboxed.co/over-60s-health/"

# ---- per-page configuration -------------------------------------------------
IMG, ALT = {}, {}

def configure(img_map, alt_map):
    """Point the image helpers at this page's uploaded assets and alt text."""
    global IMG, ALT
    IMG, ALT = img_map, alt_map


# ---- destinations (decision 1) ----
PDP       = "https://hlthtrack.co.uk/products/wearable-hlth-band"
BLOG      = "https://blog.techunboxed.co/"
CAT       = "https://blog.techunboxed.co/category/%s/"
WITHINGS  = "https://www.withings.com/uk/en/sleep-analyzer"
OURA      = "https://ouraring.com/"
TAKINGCARE = "https://taking.care/"
OXIMETER  = CAT % "health-tech"

# ---- fonts ----
SERIF = "GelasioText, Georgia, serif"          # Figma "Gelasio"
SANS  = "Inter, InterFallback, sans-serif"     # Figma "Inter" (and the "SF Pro" support note, decision 3)

# ---- colours (measured off the nodes; floats x255 were exact integers) ----
def rgb(hx):
    hx = hx.lstrip("#")
    return {"r": int(hx[0:2], 16), "g": int(hx[2:4], 16), "b": int(hx[4:6], 16), "a": 1}

INK          = rgb("#1a1a1a")   # headings, nav, usernames, "Share on"
BODY         = rgb("#2b2e33")   # body copy, bullets, comment bodies
META         = rgb("#6b7078")   # byline, timestamps, fine print, footer links/legal
SUPPORT_TXT  = rgb("#6b6f76")   # support bar only -- NOT the same grey as META
PH_TXT       = rgb("#7a7e86")   # image-placeholder labels
PH_BG        = rgb("#d9dbdf")   # image-placeholder plate
HAIR         = rgb("#e6e7ea")   # every hairline + form borders
RED          = rgb("#e2483d")   # every CTA, and the current breadcrumb crumb
WHITE        = rgb("#ffffff")
SUPPORT_BG   = rgb("#f4f4f2")
SUPPORT_LINE = rgb("#e4e6e2")
PANEL        = rgb("#f5f6f7")   # promo bar + newsletter card (NOT #f5f5f7)
LOGO_BG      = rgb("#1c1c1e")
AVATAR_BG    = "#a8c9dd"
AVATAR_ICON  = "#4f7f9c"
SHARE_ICON   = "#6e6e6e"

# ============================ text helpers ===================================
def h(s):
    """HTML-escape, and preserve the design's multi-space runs (which HTML would
    collapse). design_diff normalises \\s+ so NBSP still compares equal, but the
    byline's field separators and the bullets' hanging indent are visual, so they
    are kept."""
    s = _html.escape(s, quote=False)
    return re.sub(r"  +", lambda m: " " + "&nbsp;" * (len(m.group(0)) - 1), s)

def money(s, *specs):
    """Wrap each figure in its OWN span containing only the figure.
    Every needle includes the £ so it can never match inside an attribute value."""
    for needle, attr in specs:
        assert "£" in needle, "needle must carry the £ so it cannot match an attribute"
        i = s.find(needle)
        assert i >= 0, "money needle %r not found in %r" % (needle, s)
        s = s[:i] + '<span %s>%s</span>' % (attr, needle) + s[i + len(needle):]
    return s

PRICE   = 'data-price="price"'      # our product, live from Shopify
COMPARE = 'data-price="compare"'
def FX(a): return 'data-fx-gbp="%s"' % a   # everything else, mid-market

def link(href, label, color="#6b7078", underline=False):
    return '<a href="%s" style="color:%s;text-decoration:%s">%s</a>' % (
        href, color, "underline" if underline else "none", label)

# ============================ node helpers ===================================
def _media(st, m):
    if m:
        for k, v in m.items():
            st.append({"prop": k, "value": v, "media": 767})

def title(content, fs, lh, weight="700", color=INK, align="left", ls=None, m=None,
          font=SERIF, level="2", mw="100%"):
    st = [{"prop": "fontFamily", "value": font}, {"prop": "color", "value": color},
          {"prop": "fontSize", "value": fs}, {"prop": "lineHeight", "value": lh},
          {"prop": "fontWeight", "value": weight}, {"prop": "textAlign", "value": align},
          {"prop": "width", "value": "100%"}, {"prop": "maxWidth", "value": mw}]
    if ls: st.append({"prop": "letterSpacing", "value": ls})
    _media(st, m)
    return {"t": "Title", "id": nid(), "p": {"size": level, "content": content,
                                             "widthOption": "fill"}, "styles": st}

def text(content, size="18px", lh="31px", color=BODY, weight="400", align="left",
         mw="100%", m=None, font=SANS, ls=None, width="100%"):
    st = [{"prop": "fontFamily", "value": font}, {"prop": "color", "value": color},
          {"prop": "fontSize", "value": size}, {"prop": "lineHeight", "value": lh},
          {"prop": "fontWeight", "value": weight}, {"prop": "textAlign", "value": align},
          {"prop": "maxWidth", "value": mw}, {"prop": "width", "value": width}]
    if ls: st.append({"prop": "letterSpacing", "value": ls})
    _media(st, m)
    return {"t": "Text", "id": nid(), "p": {"content": content}, "styles": st}

def hug_text(*a, **kw):
    kw.setdefault("width", "auto")
    kw.setdefault("mw", "100%")
    return text(*a, **kw)

def container(children, styles):
    return {"t": "Container", "id": nid(), "styles": styles, "p": {"children": children}}

def col(children, gap="6px", styles=None, align=None, width="100%"):
    s = [{"prop": "lfDisplay", "value": "flex"}, {"prop": "flexDirection", "value": "column"},
         {"prop": "gap", "value": gap}, {"prop": "width", "value": width}]
    if align: s.append({"prop": "alignItems", "value": align})
    if styles: s.extend(styles)
    return container(children, s)

def rowf(children, gap="16px", align="center", justify=None, styles=None, wrap=False,
         width="100%"):
    s = [{"prop": "lfDisplay", "value": "flex"}, {"prop": "flexDirection", "value": "row"},
         {"prop": "gap", "value": gap}, {"prop": "alignItems", "value": align},
         {"prop": "width", "value": width}]
    if justify: s.append({"prop": "justifyContent", "value": justify})
    if wrap: s.append({"prop": "flexWrap", "value": "wrap"})
    if styles: s.extend(styles)
    return container(children, s)

def hr(width="100%"):
    """The `hr` RECTANGLE: 1px #e6e7ea, no radius, no stroke."""
    return container([], [{"prop": "width", "value": width}, {"prop": "height", "value": "1px"},
                          {"prop": "backgroundColor", "value": HAIR},
                          {"prop": "lfDisplay", "value": "block"}])

def raw(html_str, width="100%", styles=None):
    st = [{"prop": "width", "value": width}]
    if styles: st.extend(styles)
    return {"t": "HtmlElement", "id": nid(), "p": {"content": html_str}, "styles": st}

# ---- images -----------------------------------------------------------------
# LF emits an alt attribute but never fills it; the Image block honours p["alt"], so
# the alt map passed to configure() is what actually reaches the page.

def img(key, height=None, mheight=None, radius="6px", fit="cover", title_attr=None,
        width="100%", extra=None):
    m = IMG[key]
    st = [{"prop": "width", "value": width}, {"prop": "maxWidth", "value": "100%"},
          {"prop": "borderRadius", "value": radius}, {"prop": "objectFit", "value": fit},
          {"prop": "lfDisplay", "value": "block"}]
    if height: st.append({"prop": "height", "value": height})
    if mheight: st.append({"prop": "height", "value": mheight, "media": 767})
    if extra: st.extend(extra)
    p = {"src": m["src"], "alt": ALT.get(key, "")}
    if m.get("src_id"):  p["src_id"] = m["src_id"]
    if m.get("src_uid"): p["src_uid"] = m["src_uid"]
    if title_attr: p["title"] = title_attr
    return {"t": "Image", "id": nid(), "p": p, "styles": st}

def logo_img(w="166.21px", hgt="42px"):
    m = IMG["logo"]
    return {"t": "Image", "id": nid(),
            "p": {"title": "logo", "src": m["src"], "alt": ALT["logo"]},
            "styles": [{"prop": "width", "value": w}, {"prop": "height", "value": hgt},
                       {"prop": "maxWidth", "value": "100%"},
                       {"prop": "objectFit", "value": "contain"},
                       {"prop": "lfDisplay", "value": "block"}]}

def product_image(key):
    """The `placeholder * X` frames are 720x405 (16:9) at desktop and 350x196.875
    (also 16:9) at 390, radius 6, with the real image on TOP of a grey plate. One
    asset, aspect-locked -- no fixed px height, so it scales with the column.

    title="photo" exists ONLY as a CSS hook (same trick as the already-proven
    title="hero"/title="logo" in the sibling builders). LF's Image block emits no
    width/height and lazy-loads, so until each photo decodes its box is 0px tall and
    everything below it jumps -- measured live: five of these read h:0 while
    complete:false. The rule in PERF reserves the 16:9 box up front.
    Done through an attribute selector rather than a new `aspectRatio` style prop,
    because an unproven style prop is the riskiest thing to ship on this renderer."""
    return img(key, radius="6px", fit="cover", title_attr="photo",
               extra=[{"prop": "backgroundColor", "value": PH_BG}])

def srcset(key, widths=(384, 640, 750, 1080, 1440)):
    src = IMG[key]["src"]
    return ", ".join("%s%s %dw" % (_CDN % w, src, w) for w in widths)

def hero_picture(key, ratio, mobile_key=None, mobile_ratio=None, alt_key=None, radius="6px"):
    """The article hero, as a <picture>.

    `ratio` is (w, h) from the node -- the box is reserved from it, so the hero can
    never shift. Pass `mobile_key`/`mobile_ratio` ONLY when the design crops the hero
    differently at 390: that is art direction, and object-fit on the desktop file
    centre-crops where the design did not, so it needs its own asset. A <picture>
    fetches exactly one of them; two lfDisplay-toggled <img>s would fetch both.

      control  720x371 (1.94:1) desktop, 16:9 mobile  -> two assets
      B5       720x336 at BOTH widths (targetAspectRatio 720:336 on the 390 card
               too)                                    -> one asset, no <source>

    height:auto is load-bearing, not tidiness. The width/height ATTRIBUTES on an <img>
    are presentational hints that set the `height` PROPERTY, and aspect-ratio is only
    consulted when the other dimension is auto. Without it the control hero rendered
    350x371 at 390px -- the 16:9 override was applied and ignored (measured live)."""
    alt = _html.escape(ALT[alt_key or key], quote=True)
    dw, dh = ratio
    # NB: no %-formatting across these literals -- CSS is full of `%}` and `%{`, which
    # the % operator reads as a broken conversion spec. Concatenate instead.
    css = ('<style>picture.vb-hero,picture.vb-hero img{display:block;width:100%}'
           'picture.vb-hero img{height:auto;border-radius:' + radius + ';object-fit:cover;'
           'background:#d9dbdf;aspect-ratio:' + str(dw) + '/' + str(dh) + '}')
    if mobile_ratio:
        css += ('@media(max-width:767px){picture.vb-hero img{aspect-ratio:'
                + str(mobile_ratio[0]) + '/' + str(mobile_ratio[1]) + '}}')
    css += '</style>'
    html = css + '<picture class="vb-hero">'
    if mobile_key:
        html += ('<source media="(min-width:768px)" srcset="' + srcset(key)
                 + '" sizes="720px">')
        img_key = mobile_key
        sizes = "100vw"
    else:
        img_key = key
        sizes = "(min-width: 768px) 720px, 100vw"
    html += ('<img src="' + IMG[img_key]["src"] + '" srcset="' + srcset(img_key)
             + '" sizes="' + sizes + '" width="%d" height="%d" alt="' % (dw, dh) + alt
             + '" title="hero" fetchpriority="high" decoding="async"></picture>')
    return raw(html)

def hero_preload(key, mobile_key=None):
    """LCP preload. With two crops it must be one link per breakpoint -- a single
    preload would warm the wrong file for half the traffic."""
    if mobile_key:
        return ('<link rel="preload" as="image" fetchpriority="high" '
                'media="(min-width: 768px)" imagesrcset="%s" imagesizes="720px">\n'
                '<link rel="preload" as="image" fetchpriority="high" '
                'media="(max-width: 767px)" imagesrcset="%s" imagesizes="100vw">\n'
                % (srcset(key), srcset(mobile_key)))
    return ('<link rel="preload" as="image" fetchpriority="high" imagesrcset="%s" '
            'imagesizes="(min-width: 768px) 720px, 100vw">\n' % srcset(key))

# ---- buttons -----------------------------------------------------------------
def button(label_html, href, size="17px", lh="24px", pad=None, mfull=True):
    """Desktop: HUG (content-width). 390: FILL, per V-A (every in-article CTA flips
    layoutSizingHorizontal HUG -> FILL at 390)."""
    pad = pad or {"top": "14px", "right": "28px", "bottom": "14px", "left": "28px"}
    lab = {"t": "Text", "id": nid(), "p": {"content": label_html},
           "styles": [{"prop": "fontFamily", "value": SANS}, {"prop": "color", "value": WHITE},
                      {"prop": "fontSize", "value": size}, {"prop": "lineHeight", "value": lh},
                      {"prop": "fontWeight", "value": "700"},
                      {"prop": "textAlign", "value": "center"},
                      {"prop": "maxWidth", "value": "100%"}]}
    wrap = container([lab], [{"prop": "lfDisplay", "value": "flex"},
                             {"prop": "alignItems", "value": "center"},
                             {"prop": "justifyContent", "value": "center"},
                             {"prop": "maxWidth", "value": "100%"}])
    st = [{"prop": "backgroundColor", "value": RED}, {"prop": "borderRadius", "value": "6px"},
          {"prop": "padding", "value": pad},
          {"prop": "lfDisplay", "value": "flex"}, {"prop": "alignItems", "value": "center"},
          {"prop": "justifyContent", "value": "center"},
          {"prop": "width", "value": "fit-content"}]
    if mfull:
        st.append({"prop": "width", "value": "100%", "media": 767})
    return {"t": "BlockLink", "id": nid(),
            "p": {"destination": {"type": "static", "value": href}, "target": "_blank",
                  "widthOption": "auto", "children": [wrap]}, "styles": st}

# ============================ perf: fonts, CLS, LCP ==========================
# Gelasio, renamed to GelasioText so Lightfunnels' own font proxy does not hijack the
# family and serve one file for both weights (verified bug, documented at length in
# build_ranked_comparison.py). Single-weight Google queries give genuinely different
# static files, so bold is real.
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
    '</style>\n')

_CDN = "https://assets.lightfunnels.com/cdn-cgi/image/width=%d,quality=80,format=auto/"
_FONT_PRELOAD = "".join(
    '<link rel="preload" as="font" type="font/woff2" crossorigin '
    'href="/cf-fonts/s/inter/5.2.8/latin/%d/normal.woff2">\n' % w for w in (400, 500, 700, 800))
_INTER_FACE = "<style>" + "".join(
    "@font-face{font-family:Inter;font-style:normal;font-weight:%d;font-display:swap;"
    "src:url(/cf-fonts/s/inter/5.2.8/latin/%d/normal.woff2) format('woff2')}" % (w, w)
    for w in (400, 500, 600, 700, 800)) + "</style>\n"
# Metric-matched fallback -- without it Inter's font-display:swap reflow lands CLS
# near 0.15 and fails Agentic Browsing outright (references/performance.md).
_FALLBACK_FACE = (
    "<style>@font-face{font-family:InterFallback;src:local('Arial'),local('Liberation Sans'),"
    "local('Helvetica Neue');ascent-override:90.44%;descent-override:22.52%;"
    "line-gap-override:0%;size-adjust:107.12%}</style>\n")

PERF = (
    GELASIO_HEAD
    + '<style>'
      # A long unbroken citation URL sets an intrinsic width wider than the column and
      # pans the whole page sideways at 320px. This is the fix program.md names.
      '.wys{overflow-wrap:anywhere}'
      # Reserve every content photo's box before it decodes -- see product_image().
      # ⚠️ Was img[title="photo"], which matched NOTHING: the LF Image block
      # never receives that title, so the CLS reservation silently did not
      # apply and below-fold photos still measured height:0 until decode.
      # The content photos are exactly the imgs with an EMPTY title (the
      # logo and hero carry title="logo"/"hero" as their own hooks), so
      # title="" is a precise discriminator - and unlike title="photo" it
      # adds no hover tooltip.
      'img[title=""]{aspect-ratio:16/9;height:auto;width:100%;object-fit:cover}'
      '</style>\n'
    + _INTER_FACE + _FALLBACK_FACE + _FONT_PRELOAD)

LEGAL_MODALS = open("pagescore/tu_legal_modals.html", encoding="utf-8").read()
PERF_FOOTER = (
    # The LF storefront theme emits maximum-scale=1, which blocks pinch-zoom. There is
    # no per-step viewport knob, so rewrite the tag at runtime.
    '<script>(function(){var v=document.querySelector("meta[name=viewport]");'
    'if(v&&/maximum-scale/.test(v.content))'
    'v.setAttribute("content","width=device-width, initial-scale=1");})();</script>\n'
    '<script>(function(){function f(){var hs=document.querySelectorAll(\'img[title="hero"]\');'
    'for(var i=0;i<hs.length;i++){hs[i].setAttribute("fetchpriority","high");hs[i].setAttribute("loading","eager");}'
    'var lg=document.querySelectorAll(\'img[title="logo"]\');'
    'for(var j=0;j<lg.length;j++)lg[j].removeAttribute("fetchpriority");}'
    'if(document.readyState!=="loading")f();else document.addEventListener("DOMContentLoaded",f);})();</script>\n'
) + LEGAL_MODALS

def footer_html():
    """The step's footer custom_html.

    No smooth scroll here. Lenis ships inside the funnel-level tracker header that
    every funnel carries, so each page already has exactly one copy. A per-step block
    would be a SECOND library running a second rAF loop against the same scrollTop,
    which is what happened on the over-60s pages before 2026-10-04. Asserted rather
    than assumed."""
    out = PERF_FOOTER
    assert "lenis" not in out.lower(), "a per-step lenis crept back into the footer"
    return out

# ============================ page chrome ====================================
def section(children, styles, layout=""):
    return {"t": "Section", "id": nid(), "styles": styles,
            "p": {"layout": layout, "dividerPosition": ["top"], "horizontalFlip": False,
                  "embedded_video": {"src": "", "video_size": "stretch",
                                     "video_position": "center"},
                  "children": children}}

def page_col(children, gap="20px", maxw="760px", pad=None, align=None):
    """The article column: 760 wide, 20px side gutter (identical at 390 -- V-A keeps
    the same 20px gutter, it just drops the 760 cap), 20px vertical rhythm."""
    st = [{"prop": "maxWidth", "value": maxw}, {"prop": "width", "value": "100%"},
          {"prop": "margin", "value": {"left": "auto", "right": "auto"}},
          {"prop": "padding", "value": pad or {"left": "20px", "right": "20px"}},
          {"prop": "lfDisplay", "value": "flex"}, {"prop": "flexDirection", "value": "column"},
          {"prop": "gap", "value": gap}]
    if align: st.append({"prop": "alignItems", "value": align})
    return container(children, st)


# ============================ checks =========================================
def _scan(nd, path="root"):
    bad = []
    if isinstance(nd, dict):
        if "t" in nd and "id" not in nd: bad.append(path + " missing id")
        for k, v in nd.items():
            if v is None: bad.append(path + "." + k + " None")
            bad += _scan(v, path + "." + str(k))
    elif isinstance(nd, list):
        for i, x in enumerate(nd): bad += _scan(x, path + "[%d]" % i)
    return bad

def verify(body, expect):
    """expect = (price, compare, fx) -- the hand inventory of every money figure on
    this page. Asserted, because discovering an untagged figure after launch is the
    failure mode this counts against."""
    iss = _scan(body)
    print("sanity issues:", len(iss))
    for x in iss[:10]: print("  !", x)
    assert not iss, "structural problem in the body tree"

    dump = json.dumps(body, ensure_ascii=False)
    # json.dumps escapes the quotes inside every HTML attribute, so search a copy with
    # them unescaped -- counting on the raw dump silently finds zero and the whole
    # inventory assertion becomes a no-op. That bug was live for one run.
    flat = dump.replace('\\"', '"')
    h1s = dump.count('"size": "1"')
    assert h1s == 1, "expected exactly one h1, found %d" % h1s
    assert 'href="#"' not in flat, 'a dead href="#" reached the body'
    got = (flat.count('data-price="price"'), flat.count('data-price="compare"'),
           flat.count("data-fx-gbp="))
    print("currency tags -> price:%d compare:%d fx:%d" % got)
    assert got == tuple(expect), (
        "currency inventory changed: got %s, expected %s -- re-inventory before writing"
        % (got, tuple(expect)))
    return dump

def _skeleton(node):
    """The body with every uuid stripped, so two builds of the same tree compare equal.
    Node ids are fresh per run by design; everything else must not be."""
    if isinstance(node, dict):
        return {k: _skeleton(v) for k, v in sorted(node.items()) if k != "id"}
    if isinstance(node, list):
        return [_skeleton(x) for x in node]
    return node

def verify_shared_identical(build_shared, page_url_a, page_url_b):
    """Prove the shared half really is shared. `build_shared` is the variant module's
    shared_article_kids(page_url); it is called twice, once per page url, and the two
    structures are compared with the share links normalised out. If a future edit makes
    the two arms differ anywhere but the lead, this fails at build time instead of
    quietly turning the A/B test into a two-variable experiment."""
    a = json.dumps(_skeleton(build_shared(page_url_a)), ensure_ascii=False)
    b = json.dumps(_skeleton(build_shared(page_url_b)), ensure_ascii=False)
    a_norm = a.replace(page_url_a, "<PAGE_URL>")
    b_norm = b.replace(page_url_b, "<PAGE_URL>")
    assert a_norm == b_norm, "the shared body is NOT identical between the two pages"
    print("shared body identical: yes (%d chars, share links normalised)" % len(a_norm))
    return a_norm


# ============================ head / SEO =====================================
PAGE_TAG = open("snippets/dynamic-currency-page-tag.html", encoding="utf-8").read()
# Deliberate: the funnel is published so QA can reach the page, and this is an
# advertorial on an indexed domain. Removing it is a separate, explicit step.
ROBOTS = '<meta name="robots" content="noindex,nofollow">\n'

def _esc(v):
    return (v.replace("&", "&amp;").replace('"', "&quot;")
             .replace("<", "&lt;").replace(">", "&gt;"))

def build_head(seo, og, hero_key, hero_mobile_key=None):
    assert 140 <= len(seo["description"]) <= 160, (
        "meta description is %d chars, must be 140-160" % len(seo["description"]))
    # settings.seo emits og:* only, so without these X shows no card at all.
    twitter = ('<meta name="twitter:card" content="summary_large_image">\n'
               '<meta name="twitter:title" content="%s">\n'
               '<meta name="twitter:description" content="%s">\n'
               '<meta name="twitter:image" content="%s">\n'
               ) % (_esc(seo["title"]), _esc(seo["description"]), og["src"])
    header = ROBOTS + PERF + hero_preload(hero_key, hero_mobile_key) + twitter + PAGE_TAG
    # The header is rebuilt whole every run, so the currency install cannot accumulate
    # -- assert it anyway. A second copy makes the displayed price a race between two
    # fetches, and APPENDING to a header that already carries one is exactly how that
    # happens elsewhere in this account.
    assert header.count("<!-- dynamic-currency -->") == 1, "dynamic-currency installed twice"
    assert header.count("@font-face") >= 7, "the @font-face block was lost from the header"
    return {"header": header, "footer": footer_html()}

# ============================ write ==========================================
# createStep + updateFunnel is not atomic and a detached step cannot be looked up, so
# the id is parked on disk between the two calls. Local scratch only -- no token ever
# goes here.
_PENDING = os.path.join(os.path.dirname(os.path.abspath(__file__)), ".cache",
                        "_pending_step.json")

def _pending_all():
    try:
        return json.load(open(_PENDING, encoding="utf-8"))
    except Exception:
        return {}

def _pending_read(slug):
    return _pending_all().get("%s|%s" % (FUNNEL, slug))

def _pending_write(slug, step_id):
    d = _pending_all(); d["%s|%s" % (FUNNEL, slug)] = step_id
    os.makedirs(os.path.dirname(_PENDING), exist_ok=True)
    json.dump(d, open(_PENDING, "w", encoding="utf-8"), indent=1)

def _pending_clear(slug):
    d = _pending_all()
    if d.pop("%s|%s" % (FUNNEL, slug), None) is not None:
        json.dump(d, open(_PENDING, "w", encoding="utf-8"), indent=1)

def deploy(slug, page_title, seo, body, custom_html, visual, make_starting=False):
    """Create the step if new, else update it in place. Sibling steps are echoed back
    untouched: updateFunnel.steps is a partial update matched by id, so anything a
    colleague added since survives by omission of its body.

    make_starting is opt-in. The funnel's entry page is a real routing decision, and a
    second variant must never silently steal it from the control."""
    guard(FUNNEL, slug)

    existing = sgql(
        'query($q: String!){ funnels(first:1,query:$q){ edges { node { id published '
        'starting_step_id steps { id uid slug title type settings visual { x y } } } } } }',
        {"q": "id:%s" % FUNNEL})["funnels"]["edges"][0]["node"]
    steps = existing["steps"]
    collide = next((s for s in steps if s["slug"] == slug), None)

    step = {"slug": slug, "title": page_title, "type": "article_page",
            "settings": {"custom_html": custom_html, "seo": seo},
            "visual": visual, "body": body}

    # Every sibling must be echoed back with `settings` AND `visual`: InputUpdateStep
    # declares settings as StepSettings!, so omitting it rejects the whole mutation.
    # This only shows up once the funnel has a second step -- the first build sends an
    # empty sibling list and passes, and the failure then lands on the NEXT page.
    others = [{"id": s["id"], "slug": s["slug"], "title": s["title"], "type": s["type"],
               "settings": s["settings"], "visual": s["visual"]}
              for s in steps if s["slug"] != slug]

    if collide:
        step_id = collide["id"]
        new_steps = others + [dict(step, id=step_id, visual=collide["visual"])]
        print("redeploying existing step ->", step_id)
    else:
        # A brand-new step comes back DETACHED -- createStep alone leaves it off the
        # workflow graph and the page does not render. The updateFunnel below attaches it.
        #
        # The pair is not atomic, and a detached step is INVISIBLE to `funnel.steps`,
        # so if the attach fails a naive retry calls createStep again and leaves an
        # orphan behind every time. Remember the id until the attach lands, so a retry
        # re-attaches the step we already made instead of minting another.
        step_id = _pending_read(slug)
        if step_id:
            print("reusing the detached step from a previous failed attach ->", step_id)
        else:
            created = sgql(
                'mutation($fid: ID!, $node: InputStep!){ createStep(funnel_id:$fid, node:$node)'
                '{ step { id uid } } }', {"fid": FUNNEL, "node": step})["createStep"]["step"]
            step_id = created["id"]
            print("created detached step ->", created)
            _pending_write(slug, step_id)
        new_steps = others + [dict(step, id=step_id)]

    node = {"steps": new_steps}
    prior_start = existing["starting_step_id"]
    if make_starting or not prior_start:
        node["starting_step_id"] = step_id
        print("setting starting_step_id ->", step_id)
    else:
        print("leaving starting_step_id on", prior_start, "-- this page is not the entry page")

    r = sgql('mutation($id: ID!, $node: InputFunnel!){ updateFunnel(id:$id,node:$node)'
             '{ id starting_step_id published steps { id uid slug title } } }',
             {"id": FUNNEL, "node": node})["updateFunnel"]
    print("WROTE", json.dumps(r, indent=2))
    _pending_clear(slug)          # attached: the step is discoverable again
    assert any(s["slug"] == slug for s in r["steps"]), \
        "the step did not land in the workflow -- it is still detached and will not render"
    if not make_starting and prior_start:
        assert r["starting_step_id"] == prior_start, (
            "starting_step_id moved to this page -- the control must keep it")
    return r


