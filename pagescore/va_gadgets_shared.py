#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""V-A "health trackers for seniors" -- the two arms' shared half.

  pagescore/build_va_trackers_over60.py       CONTROL  best-health-tracker-over-60
  pagescore/build_va_trackers_over60_a1.py    A1       best-health-tracker-over-60-v2

Each builder supplies only its LEAD. Everything from the "We tested:" list down is
built here, once, and `verify_shared_identical()` fails the build if the two arms ever
diverge outside the lead -- the only way this stays a one-variable A/B test.

Page-agnostic machinery (helpers, colours, fonts, the zero-CLS font recipe, Lenis,
the currency contract, the guard and the LF write sequence) lives in
pagescore/tu_advertorial.py, shared with the V-B pages.

SOURCES (figwright only -- the Figma connector and REST API are retired here):
  control desktop   frame 850:562  (1440 x 12623)
  control mobile    frame 850:1029 (390 x 13679)  <- a REAL designed frame, not derived
  A1 lead           cards 850:1015 (760) and 850:1472 (390)

Unlike V-B, V-A has its own 390 frame, so every mobile value below is read from it
rather than borrowed.

COPY IS NEVER TYPED: pagescore/va_copy.py is generated from those four dumps, node id
-> exact `characters`, so a retype is structurally impossible.

-------------------------------------------------------------------------------------
DECISIONS
-------------------------------------------------------------------------------------
1. LINK DESTINATIONS. The dumps carry no hrefs at all, so each is a decision:
   HLTH CTAs + promo pill -> the PDP; Oura -> ouraring.com and Fitbit -> fitbit.com
   (both named in this page's own Sources paragraph); Apple -> apple.com/uk's Watch SE
   page; Garmin -> garmin.com/en-GB (the Vivoactive 6 product URL 404s today, so the
   CTA points at the manufacturer's UK home rather than a dead link). Nav and footer
   category labels link only to the blog categories that actually return 200; the rest
   stay plain text, exactly as the design has them (TEXT nodes, no href) -- so nothing
   is dead and nothing is invented. Terms / Privacy / Editorial standards / Affiliate
   policy open the existing legal modals.

2. THE TWO FORMS ARE DECORATIVE, as in V-B: empty input frames, no placeholder text,
   no submit target and no backend. Built as styled boxes, not <form>/BlockLink, so
   there is no dead button. Same for "Show more comments (6)".

3. "SF Pro" on the support note (850:564) is the only node on the page not in Inter or
   Gelasio. Treated as an un-reset Figma default and routed through the Inter stack,
   matching the identical bar on the three sibling TechUnboxed advertorials.

4. THE HERO HAS NO CORNER RADIUS. It is a BARE RECTANGLE (850:606 desktop, 850:1063
   at 390) at radius 0, unlike every product image, which sits in a `placeholder`
   frame at radius 6. Reproduced as measured rather than normalised.

5. ONE ASSET PER IMAGE, NO ART DIRECTION. The brief warned that V-A's fills are CROP
   where V-B's were FILL, and a crop is art direction. Measured: both breakpoints are
   16:9 (720x405 / 350x197) and the desktop and mobile renders of the two CROP nodes
   are pixel-identical (mean difference 0.2 and 0.3 / 255). So a single asset per
   image is correct here and a second would be pure weight.
   The hero (850:606, FILL) and the HLTH Band product shot (850:632, CROP) are two
   different renders of the SAME source file and differ by 84.5 -- they are two
   assets, not one reused twice.

6. SMOOTH SCROLL is not installed per step. It ships inside the funnel-level tracker
   header, so both V-A pages already have exactly one copy. The per-step block was
   removed on 2026-10-04; a second copy would run two rAF loops on one scrollTop.
"""
import sys, os
sys.path.insert(0, '.')
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import json
import tu_advertorial as TU
from tu_advertorial import *                      # helpers, colours, fonts, writer
from va_copy import COPY as C

IMG = json.load(open("pagescore/.cache/va_img_map.json"))

# LF emits an alt attribute but never fills it; the Image block honours p["alt"].
ALT = {
    "va_hero": ("Four health trackers worn on two older wrists: a Garmin Vivoactive, an "
                "Apple Watch, the HLTH Band and a Fitbit Charge"),
    "va_hlth_band": "The HLTH Band, a screen-free health band, worn on an older wrist",
    "va_oura": "The Oura Ring 4 titanium smart ring",
    "va_apple": "The Apple Watch SE 3 on a wrist",
    "va_fitbit": "The Fitbit Charge 6 fitness band on a wrist",
    "va_garmin": "The Garmin Vivoactive 6 sports watch on a wrist",
    "va_hlth_wrist": "The HLTH Band worn on an older person's wrist",
    "avatar_1": "TechUnboxed",
    "logo": "TechUnboxed",
}
TU.configure(IMG, ALT)

# ---- destinations (decision 1) ----
APPLE  = "https://www.apple.com/uk/apple-watch-se/"
FITBIT = "https://www.fitbit.com/global/uk/products/trackers/charge6"
GARMIN = "https://www.garmin.com/en-GB/"

# ============================ page chrome ====================================
# --- support bar (850:563) : #f4f4f2, 1px #e4e6e2 top+bottom, pad 9/12 -------
support_bar = section(
    [text(h(C["850:564"]), size="13px", lh="18px", color=SUPPORT_TXT, align="center")],
    [{"prop": "backgroundColor", "value": SUPPORT_BG},
     {"prop": "borderStyle", "value": "solid"}, {"prop": "borderColor", "value": SUPPORT_LINE},
     {"prop": "borderWidth", "value": "1px 0px 1px 0px"},
     {"prop": "padding", "value": {"top": "9px", "bottom": "9px", "left": "12px", "right": "12px"}}])

# --- logo bar (850:565) : #1c1c1e, pad 14/28, logo 166.21x42 centred ---------
logo_bar = section(
    [container([logo_img()], [{"prop": "lfDisplay", "value": "flex"},
                              {"prop": "justifyContent", "value": "center"},
                              {"prop": "alignItems", "value": "center"},
                              {"prop": "width", "value": "100%"}])],
    [{"prop": "backgroundColor", "value": LOGO_BG},
     {"prop": "padding", "value": {"top": "14px", "bottom": "14px", "left": "28px", "right": "28px"}}])

# --- nav (850:579) : 8 items, Inter Medium 15/21, gap 28, centred ------------
# The whole band is DELETED at 390 in the designed mobile frame -- no hamburger, no
# scroller, nothing replaces it. Hidden rather than dropped so the DOM stays one tree.
NAV = [("850:580", None), ("850:581", CAT % "buying-guides"), ("850:582", CAT % "laptops"),
       ("850:583", CAT % "mobile"), ("850:584", CAT % "smart-home"), ("850:585", CAT % "audio"),
       ("850:586", CAT % "health-tech"), ("850:587", CAT % "wearables")]
nav = section(
    [rowf([hug_text(h(C[i]) if href is None else link(href, h(C[i]), "#1a1a1a"),
                    size="15px", lh="21px", color=INK, weight="500")
           for i, href in NAV],
          gap="28px", justify="center", wrap=True)],
    [{"prop": "backgroundColor", "value": WHITE},
     {"prop": "padding", "value": {"top": "13.5px", "bottom": "13.5px", "left": "12px", "right": "12px"}},
     {"prop": "lfDisplay", "value": "none", "media": 767}])

def rule():
    return section([hr()], [{"prop": "padding", "value": {"top": "0px", "bottom": "0px"}}])

rule_under_nav = section([hr()], [{"prop": "padding", "value": {"top": "0px", "bottom": "0px"}},
                                  {"prop": "lfDisplay", "value": "none", "media": 767}])

# --- promo bar (850:589) : row at 1440, COLUMN at 390 (850:1046), gap 16 -> 10
promo = section(
    [rowf([hug_text(money(h(C["850:590"]), ("£79", PRICE), ("£158", COMPARE)),
                    size="15px", lh="20px", color=INK, weight="500",
                    m={"textAlign": "center"}),
           button(h(C["850:592"]), PDP, size="14px", lh="18px",
                  pad={"top": "9px", "right": "18px", "bottom": "9px", "left": "18px"},
                  mfull=False)],
          gap="16px", justify="center", align="center",
          styles=[{"prop": "flexDirection", "value": "column", "media": 767},
                  {"prop": "gap", "value": "10px", "media": 767}])],
    [{"prop": "backgroundColor", "value": PANEL},
     {"prop": "padding", "value": {"top": "12px", "bottom": "12px", "left": "20px", "right": "20px"}},
     {"prop": "padding", "value": {"top": "14px", "bottom": "14px", "left": "20px", "right": "20px"},
      "media": 767}])

# --- breadcrumb (850:594) : pad 0/360 on 1440 == the article column's text edge
CRUMB = [("850:595", INK, "400", BLOG), ("850:596", META, "400", None),
         ("850:597", INK, "400", CAT % "wearables"), ("850:598", META, "400", None),
         ("850:599", RED, "500", None)]
breadcrumb = section(
    [page_col([rowf([hug_text(h(C[i]) if href is None else link(href, h(C[i]), "#1a1a1a"),
                              size="15px", lh="21px", color=c, weight=w,
                              m={"fontSize": "13px"})
                     for i, c, w, href in CRUMB],
                    gap="6px", align="center", wrap=True,
                    styles=[{"prop": "gap", "value": "4px", "media": 767}])],
              gap="0px")],
    [{"prop": "backgroundColor", "value": WHITE},
     {"prop": "padding", "value": {"top": "13.5px", "bottom": "13.5px"}},
     {"prop": "padding", "value": {"top": "10px", "bottom": "10px"}, "media": 767}])

# ============================ shared article body ===========================
# Currency inventory, per node id. Our own band goes through the Shopify price feed;
# every competitor and editorial figure through the mid-market converter. Never mixed
# -- the converter does not match checkout, so pricing our own product with it would
# quote figures we do not charge.
MONEY = {
    "850:590":  [("£79", PRICE), ("£158", COMPARE)],           # promo bar
    "850:640":  [("£79", PRICE), ("£158", COMPARE)],           # HLTH price line
    "850:675":  [("£349", FX("349")), ("£5.99", FX("5.99"))],  # Oura
    "850:681":  [("£5.99", FX("5.99"))],
    "850:691":  [("£560", FX("560")), ("£349", FX("349")), ("£5.99", FX("5.99"))],
    "850:709":  [("£219", FX("219"))],                          # Apple
    "850:743":  [("£9.99", FX("9.99"))],                        # Fitbit Premium
    "850:744":  [("£79.99", FX("79.99")), ("£139.99", FX("139.99")), ("£9.99", FX("9.99"))],
    "850:750":  [("£9.99", FX("9.99"))],
    "850:760":  [("£9.99", FX("9.99"))],
    "850:776":  [("£269", FX("269"))],                          # Garmin
    "850:777":  [("£269", FX("269"))],
    "850:794":  [("£269", FX("269"))],
    "850:802":  [("£79", PRICE)],                               # Final word
    "850:812":  [("£79", PRICE), ("£158", COMPARE)],            # offer bullet
    "850:821":  [("£79", PRICE)],                               # offer CTA label
    "850:822":  [("£79", PRICE)],                               # offer fine print
    "850:924":  [("£6", FX("6"))],                              # a reader comment
    "850:948":  [("£79", PRICE)],                               # a reader comment
    "850:1011": [("£79", PRICE), ("£158", COMPARE)],            # Sources
    # ---- A1 lead only (the control lead carries no money at all) ----
    "850:1020": [("£219", FX("219"))],
    "850:1025": [("£219", FX("219")), ("£79.99", FX("79.99")),
                 ("£9.99", FX("9.99")), ("£440", FX("440"))],
    "850:1028": [("£79", PRICE)],
}

def copy_html(node_id):
    """Escaped, multi-space-preserved, and currency-tagged where the inventory says so."""
    s = h(C[node_id])
    if node_id in MONEY:
        s = money(s, *MONEY[node_id])
    return s

def tagged_text(node_id, **kw):
    return text(copy_html(node_id), **kw)

def stack(lead_id, body_ids, lead_color=INK, lead_weight="700"):
    """The `stack` FRAME: VERTICAL, pad 0, gap 6 -- a lead line plus body text or a
    `list` frame (itself VERTICAL gap 6). Bullets are literal '*  ' text with TWO
    spaces, not <ul> markers."""
    lead = text(h(C[lead_id]), weight=lead_weight, color=lead_color)
    if isinstance(body_ids, str):
        return col([lead, tagged_text(body_ids)], gap="6px")
    return col([lead, col([tagged_text(b) for b in body_ids], gap="6px")], gap="6px")

# ---- the five product blocks ------------------------------------------------
PRODUCTS = [
    dict(h2="850:629", key="va_hlth_band", sub="850:633",
         prose=[("850:635", "850:636"), ("850:638", "850:639")],
         price="850:640",
         lists=[("850:642", ["850:644", "850:645", "850:646", "850:647"]),
                ("850:649", ["850:651", "850:652", "850:653", "850:654"]),
                ("850:656", ["850:658", "850:659"])],
         cta="850:661", href=PDP),
    dict(h2="850:664", key="va_oura", sub="850:668",
         prose=[("850:670", "850:671"), ("850:673", "850:674")],
         price="850:675",
         lists=[("850:677", ["850:679", "850:680", "850:681", "850:682"]),
                ("850:684", ["850:686", "850:687"]),
                ("850:689", ["850:691", "850:692", "850:693"])],
         cta="850:695", href=OURA),
    dict(h2="850:698", key="va_apple", sub="850:702",
         prose=[("850:704", "850:705"), ("850:707", "850:708")],
         price="850:709",
         lists=[("850:711", ["850:713", "850:714", "850:715", "850:716"]),
                ("850:718", ["850:720", "850:721", "850:722"]),
                ("850:724", ["850:726", "850:727", "850:728"])],
         cta="850:730", href=APPLE),
    dict(h2="850:733", key="va_fitbit", sub="850:737",
         prose=[("850:739", "850:740"), ("850:742", "850:743")],
         price="850:744",
         lists=[("850:746", ["850:748", "850:749", "850:750", "850:751"]),
                ("850:753", ["850:755", "850:756"]),
                ("850:758", ["850:760", "850:761"])],
         cta="850:763", href=FITBIT),
    dict(h2="850:766", key="va_garmin", sub="850:770",
         prose=[("850:772", "850:773"), ("850:775", "850:776")],
         price="850:777",
         lists=[("850:779", ["850:781", "850:782", "850:783", "850:784"]),
                ("850:786", ["850:788", "850:789", "850:790"]),
                ("850:792", ["850:794", "850:795", "850:796"])],
         cta="850:798", href=GARMIN),
]

def shared_article_kids(page_url):
    """Everything from "We tested:" down. Byte-identical between the two arms -- the
    ONLY thing that varies is `page_url`, which the share buttons link to, and a share
    link pointing at the other variant would corrupt the test."""
    kids = []
    # "We tested:" / "We looked at:" -- BOLD here and coloured #2b2e33, unlike the
    # per-product labels below which are bold #1a1a1a. Measured, not normalised.
    kids.append(stack("850:613", ["850:615", "850:616", "850:617", "850:618", "850:619"],
                      lead_color=BODY, lead_weight="700"))
    kids.append(stack("850:621", ["850:623", "850:624", "850:625", "850:626"],
                      lead_color=BODY, lead_weight="700"))
    kids.append(hr())

    for p in PRODUCTS:
        # product header stack: gap 18 (not 6) -- h2 / image / sub-head
        kids.append(col([
            title(h(C[p["h2"]]), "26px", "33px", font=SERIF, color=INK,
                  m={"fontSize": "22px", "lineHeight": "28px"}),
            product_image(p["key"]),
            title(h(C[p["sub"]]), "21px", "27px", font=SERIF, color=INK, level="3",
                  m={"fontSize": "19px", "lineHeight": "24px"}),
        ], gap="18px"))
        for lead, bod in p["prose"]:
            kids.append(col([text(h(C[lead]), weight="700", color=INK), tagged_text(bod)],
                            gap="6px"))
        kids.append(tagged_text(p["price"]))
        for lead, items in p["lists"]:
            kids.append(stack(lead, items))
        kids.append(button(h(C[p["cta"]]), p["href"]))
        kids.append(hr())

    # ---- Final word ---------------------------------------------------------
    kids.append(title(h(C["850:800"]), "26px", "33px", font=SERIF, color=INK,
                      m={"fontSize": "22px", "lineHeight": "28px"}))
    for i in ("850:801", "850:802", "850:803"):
        kids.append(tagged_text(i))
    kids.append(hr())

    # ---- offer (850:805) : gap 18, no box -- it reads as part of the article --
    # This CTA is FIXED full width at both breakpoints and one size up (19/24,
    # padding 16/28); every in-article CTA above is 17/24, 14/28, hug -> fill.
    offer_cta = button(copy_html("850:821"), PDP, size="19px", lh="24px",
                       pad={"top": "16px", "right": "28px", "bottom": "16px", "left": "28px"})
    offer_cta["styles"] = [s for s in offer_cta["styles"] if s["prop"] != "width"]
    offer_cta["styles"].append({"prop": "width", "value": "100%"})

    kids.append(col([
        title(h(C["850:806"]), "26px", "33px", font=SERIF, color=INK,
              m={"fontSize": "22px", "lineHeight": "28px"}),
        product_image("va_hlth_wrist"),
        text(h(C["850:810"])),
        col([tagged_text(i) for i in ("850:812", "850:813", "850:814", "850:815",
                                      "850:816", "850:817", "850:818", "850:819")], gap="6px"),
        offer_cta,
        tagged_text("850:822", size="14px", lh="20px", color=META),
    ], gap="18px"))

    # ---- share row (850:823) : "Share on" + 4 icons, gap 12 / icons gap 16 ---
    _SHARE_PATHS = {
        "Facebook": (10, 16, "M9.285 9h-2.57v7H3.858V9H2v-2.2h1.858V4.87C3.858 2.9 5.02 2 6.94 2c.92 0 1.7.07 1.93.1v2.24H7.53c-1.04 0-1.24.5-1.24 1.22V6.8h2.48L8.43 9z"),
        "Twitter": (16, 16, "M12.6 0h2.454l-5.36 6.126L16 14.63H11.06L7.19 9.573 2.77 14.63H.313l5.733-6.553L0 0h5.063l3.5 4.628zm-.86 13.16h1.36L4.32 1.394H2.86z"),
        "Pinterest": (12, 16, "M6.02 0C2.7 0 .91 2.13.91 4.45c0 1.08.6 2.42 1.56 2.85.15.07.22.04.25-.1l.21-.83c.02-.07 0-.13-.05-.2a2.86 2.86 0 0 1-.58-1.72c0-1.98 1.55-3.9 4.19-3.9 2.28 0 3.88 1.5 3.88 3.64 0 2.42-1.27 4.1-2.92 4.1-.91 0-1.6-.73-1.38-1.63.26-1.08.78-2.24.78-3.02 0-.7-.39-1.28-1.19-1.28-.94 0-1.7.94-1.7 2.2 0 .8.28 1.35.28 1.35L3.1 12.66c-.3 1.25-.04 2.78-.02 2.93.01.09.13.11.18.04.08-.1 1.1-1.34 1.44-2.57.1-.35.57-2.16.57-2.16.28.52 1.1.97 1.98.97 2.6 0 4.37-2.33 4.37-5.45C11.62 2.06 9.6 0 6.02 0"),
        "LinkedIn": (14, 16, "M3.15 14V5.32H.24V14zM1.69 4.13c1.01 0 1.65-.66 1.65-1.49C3.32 1.79 2.7 1.13 1.71 1.13S.04 1.79.04 2.64c0 .83.63 1.49 1.63 1.49zM4.76 14h2.91V9.15c0-.26.02-.52.1-.7.2-.52.68-1.06 1.49-1.06 1.05 0 1.47.79 1.47 1.95V14h2.91V9c0-2.66-1.43-3.9-3.33-3.9-1.56 0-2.24.87-2.62 1.46h.02V5.32H4.76c.04.81 0 8.68 0 8.68z"),
    }
    _SHARE_URLS = {
        "Facebook": "https://www.facebook.com/sharer/sharer.php?u=" + page_url,
        "Twitter":  "https://twitter.com/intent/tweet?url=" + page_url,
        "Pinterest": "https://pinterest.com/pin/create/button/?url=" + page_url,
        "LinkedIn": "https://www.linkedin.com/sharing/share-offsite/?url=" + page_url,
    }
    _icons = "".join(
        '<a href="%s" target="_blank" rel="noopener" aria-label="Share on %s" '
        'style="display:inline-flex;align-items:center;line-height:0">'
        '<svg width="%d" height="%d" viewBox="0 0 %d %d" fill="%s" aria-hidden="true">'
        '<path d="%s"/></svg></a>' % (_SHARE_URLS[k], k, w, hgt, w, hgt, SHARE_ICON, d)
        for k, (w, hgt, d) in _SHARE_PATHS.items())
    kids.append(raw(
        '<div style="display:flex;align-items:center;gap:12px">'
        '<span style="font-family:Inter,InterFallback,sans-serif;font-size:15px;line-height:20px;'
        'font-weight:500;color:#1a1a1a">%s</span>'
        '<span style="display:flex;align-items:center;gap:16px">%s</span></div>'
        % (h(C["850:824"]), _icons)))

    # ---- comments (850:834) -------------------------------------------------
    # Nine 44x44 avatar FRAMEs at cornerRadius 22 -- there is not one ELLIPSE in the
    # whole file. Eight are a flat #a8c9dd disc with a stroked person glyph; only the
    # author reply carries a photo, on a #d9dbdf plate.
    AVATAR_SVG = (
        '<svg width="44" height="44" viewBox="0 0 44 44" aria-hidden="true" '
        'style="display:block;border-radius:22px">'
        '<rect width="44" height="44" rx="22" fill="%s"/>'
        '<circle cx="22" cy="18.333" r="3.667" fill="none" stroke="%s" stroke-width="1.4667"/>'
        '<path d="M14.667 30.25v-1.833a3.667 3.667 0 0 1 3.667-3.667h7.333a3.667 3.667 0 0 1 3.666 3.667v1.833" '
        'fill="none" stroke="%s" stroke-width="1.4667" stroke-linecap="round"/></svg>'
    ) % (AVATAR_BG, AVATAR_ICON, AVATAR_ICON)

    def avatar_generic():
        return container([raw(AVATAR_SVG, width="44px")],
                         [{"prop": "width", "value": "44px"}, {"prop": "flexShrink", "value": "0"}])

    def avatar_photo():
        return container([img("avatar_1", radius="22px", fit="cover", width="44px",
                              height="44px")],
                         [{"prop": "width", "value": "44px"}, {"prop": "flexShrink", "value": "0"}])

    def comment_stack(name_id, date_id, body_id, reply_id, name_html=None):
        inner = [hug_text(name_html or h(C[name_id]), size="15px", lh="20px",
                          color=INK, weight="700")]
        if date_id:
            inner.append(hug_text(h(C[date_id]), size="13px", lh="18px", color=META))
        inner.append(tagged_text(body_id, size="16px", lh="26px", color=BODY))
        if reply_id:
            inner.append(hug_text(h(C[reply_id]), size="13px", lh="18px", color=META))
        return inner

    def comment_row(avatar, stack_children, pad=None, extra_children=None, maxw="640px"):
        # The design's text stack is 640 FIXED inside a HUG row (44 + 14 + 640 = 698,
        # i.e. 22px short of the 720 column). Plain flex:1 gives 662 and the longer
        # bodies then wrap one line short of the design. At 390 the space left is 292,
        # well under the cap, so it still fills.
        body_col = col(stack_children, gap="4px",
                       styles=[{"prop": "flex", "value": "1"}, {"prop": "minWidth", "value": "0"},
                               {"prop": "maxWidth", "value": maxw}])
        if extra_children:
            body_col["p"]["children"].extend(extra_children)
        return rowf([avatar, body_col], gap="14px", align="flex-start",
                    styles=[{"prop": "padding", "value": pad or
                             {"top": "18px", "right": "0px", "bottom": "18px", "left": "0px"}}])

    # The author reply inside the sue1959 row: name + body only, no date line and no
    # "Reply" link, a photo avatar, and a 580-wide stack rather than 640.
    nested_reply = comment_row(
        avatar_photo(),
        comment_stack(None, None, "850:901", None, name_html=h(C["850:900"])),
        pad={"top": "14px", "right": "0px", "bottom": "0px", "left": "0px"},
        maxw="580px")

    COMMENTS = [
        ("850:843", "850:844", "850:845", "850:846", None),
        ("850:855", "850:856", "850:857", "850:858", None),
        ("850:867", "850:868", "850:869", "850:870", None),
        ("850:879", "850:880", "850:881", "850:882", None),
        ("850:891", "850:892", "850:893", "850:894", nested_reply),
        ("850:910", "850:911", "850:912", "850:913", None),
        ("850:922", "850:923", "850:924", "850:925", None),
        ("850:934", "850:935", "850:936", "850:937", None),
        ("850:946", "850:947", "850:948", "850:949", None),
    ]
    comment_kids = [title(h(C["850:835"]), "24px", "30px", font=SERIF, color=INK,
                          m={"fontSize": "21px", "lineHeight": "26px"})]
    for n, d, b, r, nested in COMMENTS:
        comment_kids.append(comment_row(avatar_generic(), comment_stack(n, d, b, r),
                                        extra_children=[nested] if nested else None))
        comment_kids.append(hr())
    # A TEXT node in the design, and there are no further six comments to show, so it
    # stays text rather than becoming a control that does nothing (decision 2).
    comment_kids.append(hug_text(h(C["850:951"]), size="15px", lh="20px", color=INK, weight="700"))
    kids.append(col(comment_kids, gap="0px"))

    # ---- leave a comment (850:952) : decorative (decision 2) ------------------
    def field(label_id, box_h):
        return col([text(h(C[label_id]), size="14px", lh="18px", color=META),
                    container([], [{"prop": "width", "value": "100%"},
                                   {"prop": "height", "value": box_h},
                                   {"prop": "backgroundColor", "value": WHITE},
                                   {"prop": "borderStyle", "value": "solid"},
                                   {"prop": "borderColor", "value": HAIR},
                                   {"prop": "borderWidth", "value": "1px"},
                                   {"prop": "borderRadius", "value": "6px"},
                                   {"prop": "lfDisplay", "value": "block"}])], gap="6px")

    post_btn = container([container([text(h(C["850:965"]), size="17px", lh="24px", color=WHITE,
                                          weight="700", align="center", width="auto")],
                                    [{"prop": "lfDisplay", "value": "flex"},
                                     {"prop": "alignItems", "value": "center"},
                                     {"prop": "justifyContent", "value": "center"}])],
                         [{"prop": "backgroundColor", "value": RED},
                          {"prop": "borderRadius", "value": "6px"},
                          {"prop": "padding", "value": {"top": "14px", "right": "28px",
                                                        "bottom": "14px", "left": "28px"}},
                          {"prop": "lfDisplay", "value": "flex"},
                          {"prop": "alignItems", "value": "center"},
                          {"prop": "justifyContent", "value": "center"},
                          {"prop": "width", "value": "fit-content"},
                          {"prop": "width", "value": "100%", "media": 767}])

    kids.append(col([
        title(h(C["850:953"]), "20px", "26px", font=SANS, weight="800", color=INK, level="3",
              m={"fontSize": "17px", "lineHeight": "22px"}),
        text(h(C["850:954"]), size="14px", lh="20px", color=META),
        field("850:956", "120px"),
        field("850:959", "48px"),
        field("850:962", "48px"),
        post_btn,
    ], gap="14px"))

    # ---- newsletter (850:966) : #f5f6f7 card, radius 10, pad 32/24, gap 10 ----
    sub_btn = container([container([text(h(C["850:972"]), size="16px", lh="22px", color=WHITE,
                                         weight="700", align="center", width="auto")],
                                   [{"prop": "lfDisplay", "value": "flex"},
                                    {"prop": "alignItems", "value": "center"},
                                    {"prop": "justifyContent", "value": "center"}])],
                        [{"prop": "backgroundColor", "value": RED},
                         {"prop": "borderRadius", "value": "6px"},
                         {"prop": "padding", "value": {"top": "12px", "right": "20px",
                                                       "bottom": "12px", "left": "20px"}},
                         {"prop": "lfDisplay", "value": "flex"},
                         {"prop": "alignItems", "value": "center"},
                         {"prop": "justifyContent", "value": "center"},
                         {"prop": "flexShrink", "value": "0"},
                         {"prop": "width", "value": "100%", "media": 767}])

    newsletter = container([
        title(h(C["850:967"]), "24px", "30px", font=SERIF, color=INK, align="center",
              m={"fontSize": "21px", "lineHeight": "26px"}),
        text(h(C["850:968"]), size="16px", lh="24px", color=META),
        rowf([container([], [{"prop": "width", "value": "330px"},
                             {"prop": "height", "value": "46px"},
                             {"prop": "backgroundColor", "value": WHITE},
                             {"prop": "borderStyle", "value": "solid"},
                             {"prop": "borderColor", "value": HAIR},
                             {"prop": "borderWidth", "value": "1px"},
                             {"prop": "borderRadius", "value": "6px"},
                             {"prop": "lfDisplay", "value": "block"},
                             {"prop": "width", "value": "100%", "media": 767}]),
              sub_btn],
             gap="10px", align="center", justify="center", width="auto",
             styles=[{"prop": "flexDirection", "value": "column", "media": 767},
                     {"prop": "width", "value": "100%", "media": 767}]),
    ], [{"prop": "lfDisplay", "value": "flex"}, {"prop": "flexDirection", "value": "column"},
        {"prop": "gap", "value": "10px"}, {"prop": "alignItems", "value": "center"},
        {"prop": "width", "value": "100%"},
        {"prop": "backgroundColor", "value": PANEL},
        {"prop": "borderRadius", "value": "10px"},
        {"prop": "padding", "value": {"top": "32px", "right": "24px",
                                      "bottom": "32px", "left": "24px"}}])
    kids.append(newsletter)

    return kids

# ============================ footer (850:974) ===============================
FOOT_A = [("850:978", CAT % "wearables"), ("850:979", CAT % "smart-home"),
          ("850:980", CAT % "audio"), ("850:981", None), ("850:982", CAT % "laptops"),
          ("850:983", CAT % "health-tech"), ("850:984", CAT % "buying-guides")]
# Terms / Privacy / Editorial standards / Affiliate policy carry the ids the shared
# modal handler in tu_legal_modals.html listens for.
FOOT_B = [("850:987", None, None), ("850:988", None, None),
          ("850:989", "#tu-edit", "edit"), ("850:990", None, None),
          ("850:991", "#tu-terms", "terms"), ("850:992", "#tu-priv", "priv"),
          ("850:993", "#tu-aff", "aff")]

def foot_heading(i):
    return hug_text(h(C[i]), size="13px", lh="18px", color=INK, weight="700", ls="0.08em")

def foot_link(i, href, el_id=None):
    if href is None:
        return hug_text(h(C[i]), size="14px", lh="20px", color=META)
    idattr = ' id="%s"' % el_id if el_id else ""
    return hug_text('<a href="%s"%s style="color:#6b7078;text-decoration:none">%s</a>'
                    % (href, idattr, h(C[i])), size="14px", lh="20px", color=META)

col_a = col([foot_heading("850:977")] + [foot_link(i, hrf) for i, hrf in FOOT_A],
            gap="8px", styles=[{"prop": "maxWidth", "value": "350px"}])
col_b = col([foot_heading("850:986")] + [foot_link(i, hrf, eid) for i, hrf, eid in FOOT_B],
            gap="8px", styles=[{"prop": "maxWidth", "value": "350px"}])
logo_plate = container([logo_img()],
                       [{"prop": "width", "value": "220px"}, {"prop": "height", "value": "60px"},
                        {"prop": "backgroundColor", "value": LOGO_BG},
                        {"prop": "borderRadius", "value": "6px"},
                        {"prop": "lfDisplay", "value": "flex"},
                        {"prop": "alignItems", "value": "center"},
                        {"prop": "justifyContent", "value": "center"},
                        {"prop": "flexShrink", "value": "0"}])
col_c = col([logo_plate, text(h(C["850:1009"]), size="14px", lh="20px", color=META)],
            gap="14px", styles=[{"prop": "maxWidth", "value": "350px"}])

footer_row = rowf([col_a, col_b, col_c], gap="30px", align="flex-start",
                  styles=[{"prop": "flexDirection", "value": "column", "media": 767},
                          {"prop": "gap", "value": "28px", "media": 767}])

legal = col([tagged_text("850:1011", size="12.5px", lh="20px", color=META),
             text(h(C["850:1012"]), size="12.5px", lh="20px", color=META),
             text(h(C["850:1013"]), size="12.5px", lh="20px", color=META),
             text(h(C["850:1014"]), size="12.5px", lh="20px", color=META)], gap="10px")

footer = section(
    [container([footer_row, legal],
               [{"prop": "maxWidth", "value": "1180px"}, {"prop": "width", "value": "100%"},
                {"prop": "margin", "value": {"left": "auto", "right": "auto"}},
                {"prop": "lfDisplay", "value": "flex"},
                {"prop": "flexDirection", "value": "column"},
                {"prop": "gap", "value": "30px"}])],
    [{"prop": "padding", "value": {"top": "40px", "right": "130px", "bottom": "30px", "left": "130px"}},
     {"prop": "padding", "value": {"top": "40px", "right": "20px", "bottom": "30px", "left": "20px"},
      "media": 767}])

def assemble(lead_kids, page_url):
    """lead + shared body -> the full page Root."""
    kids = list(lead_kids) + shared_article_kids(page_url)
    article_col = page_col(kids, gap="20px",
                           pad={"top": "14px", "right": "20px", "bottom": "60px", "left": "20px"})
    article = section([article_col],
                      [{"prop": "backgroundColor", "value": WHITE},
                       {"prop": "padding", "value": {"top": "0px", "bottom": "0px"}}])
    return {"id": nid(), "t": "Root", "version": 11,
            "styles": [{"prop": "pageWidth", "value": "760px"},
                       {"prop": "backgroundColor", "value": WHITE}],
            "p": {"children": [support_bar, logo_bar, nav, rule_under_nav, promo, rule(),
                               breadcrumb, rule(), article, rule(), footer]}}

def verify_shared_identical(page_url_a, page_url_b):
    """Bind this module's shared half to the engine's structural comparison."""
    return TU.verify_shared_identical(shared_article_kids, page_url_a, page_url_b)
