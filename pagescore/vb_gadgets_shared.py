#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""V-B "Health gadgets for over-60s" -- the two arms' shared half.

  pagescore/build_vb_gadgets_over60.py       CONTROL  best-health-gadgets-over-60
  pagescore/build_vb_gadgets_over60_b5.py    B5       best-health-gadgets-over-60-v2

Each builder supplies only its LEAD. Everything from the "We tested:" list down --
the five product blocks, Final word, the offer, share row, comments, both forms, the
newsletter, the site chrome and the footer -- is built here, once, and
`verify_shared_identical()` fails the build if the two arms ever diverge outside the
lead. That is the only way this stays a one-variable A/B test.

The page-agnostic machinery (helpers, colours, fonts, the zero-CLS font recipe, the
currency-tagging contract, the guard and the LF write sequence) lives in
pagescore/tu_advertorial.py and is shared with the V-A pages too. What stays HERE is
everything that carries copy, because copy is read per design frame by node id.

SOURCES (figwright only): control lead + whole shared body from frame 850:1487
(1440x13029); B5 lead from cards 850:1943 / 850:1957; mobile values for the shared
half from V-A's designed 390 page 850:1029, since V-B has no 390 frame of its own.

COPY IS NEVER TYPED: pagescore/vb_copy.py is generated from those dumps, node id ->
exact `characters`.

NOTE: smooth scroll is not installed per step. It ships inside the funnel-level
tracker header, so these pages already have exactly one copy. The `lenis=` switch and
the per-step block were removed on 2026-10-04.
"""
import sys, os
sys.path.insert(0, '.')
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import json
import tu_advertorial as TU
from tu_advertorial import *                      # helpers, colours, fonts, writer
from vb_copy import COPY as C

IMG = json.load(open("pagescore/.cache/vb_img_map.json"))

# LF emits an alt attribute but never fills it; the Image block honours p["alt"].
ALT = {
    "featured": "A group of over-60s testers with the five health gadgets on a table",
    "featured_mobile": "A group of over-60s testers with the five health gadgets on a table",
    # B5's lead card carries its OWN hero (node 850:1951, a different source file from
    # the control's 850:1531 -- confirmed by pixel diff, not by the filename).
    "featured_b5": ("The five tested health gadgets laid out on a wooden table: the "
                    "Withings sleep pad, a fingertip pulse oximeter, the HLTH Band and "
                    "a fall-alarm base unit"),
    "hlth_band": "The HLTH Band, a screen-free health band, shown on a plain background",
    "withings": "The Withings Sleep Analyzer pad that slips under a mattress",
    "oura": "The Oura Ring 4 titanium smart ring",
    "taking_care": "The Taking Care Digital Fall Alarm pendant and its base unit",
    "oximeter": "A fingertip pulse oximeter clipped to a finger showing a reading",
    "hlth_wrist": "The HLTH Band worn on an older person's wrist",
    "avatar_1": "TechUnboxed",
    "logo": "TechUnboxed",
}
TU.configure(IMG, ALT)

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

# --- support bar (850:1488) : #f4f4f2, 1px #e4e6e2 top+bottom, pad 9/12 -------
support_bar = section(
    [text(h(C["850:1489"]), size="13px", lh="18px", color=SUPPORT_TXT, align="center")],
    [{"prop": "backgroundColor", "value": SUPPORT_BG},
     {"prop": "borderStyle", "value": "solid"}, {"prop": "borderColor", "value": SUPPORT_LINE},
     {"prop": "borderWidth", "value": "1px 0px 1px 0px"},
     {"prop": "padding", "value": {"top": "9px", "bottom": "9px", "left": "12px", "right": "12px"}}])

# --- logo bar (850:1490) : #1c1c1e, pad 14/28, logo 166.21x42 centred ---------
logo_bar = section(
    [container([logo_img()], [{"prop": "lfDisplay", "value": "flex"},
                              {"prop": "justifyContent", "value": "center"},
                              {"prop": "alignItems", "value": "center"},
                              {"prop": "width", "value": "100%"}])],
    [{"prop": "backgroundColor", "value": LOGO_BG},
     {"prop": "padding", "value": {"top": "14px", "bottom": "14px", "left": "28px", "right": "28px"}}])

# --- nav (850:1504) : 8 items, Inter Medium 15/21, gap 28, centred ------------
# ABSENT at 390 in V-A -- the whole band is deleted, no hamburger, no scroller.
NAV = [("850:1505", None), ("850:1506", CAT % "buying-guides"), ("850:1507", CAT % "laptops"),
       ("850:1508", CAT % "mobile"), ("850:1509", CAT % "smart-home"), ("850:1510", CAT % "audio"),
       ("850:1511", CAT % "health-tech"), ("850:1512", CAT % "wearables")]
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

# --- promo bar (850:1514) : row at 1440, COLUMN at 390 (V-A 850:1046) --------
promo = section(
    [rowf([hug_text(money(h(C["850:1515"]), ("£79", PRICE), ("£158", COMPARE)),
                    size="15px", lh="20px", color=INK, weight="500",
                    m={"textAlign": "center"}),
           button('Claim my discount', PDP, size="14px", lh="18px",
                  pad={"top": "9px", "right": "18px", "bottom": "9px", "left": "18px"},
                  mfull=False)],
          gap="16px", justify="center", align="center",
          styles=[{"prop": "flexDirection", "value": "column", "media": 767},
                  {"prop": "gap", "value": "10px", "media": 767}])],
    [{"prop": "backgroundColor", "value": PANEL},
     {"prop": "padding", "value": {"top": "12px", "bottom": "12px", "left": "20px", "right": "20px"}},
     {"prop": "padding", "value": {"top": "14px", "bottom": "14px", "left": "20px", "right": "20px"},
      "media": 767}])

# --- breadcrumb (850:1519) : pad 0/360 on 1440 == the article column's text edge
CRUMB = [("850:1520", INK, "400", BLOG), ("850:1521", META, "400", None),
         ("850:1522", INK, "400", CAT % "wearables"), ("850:1523", META, "400", None),
         ("850:1524", RED, "500", None)]
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
def stack(lead_id, body_ids, gap="6px", lead_color=INK, lead_weight="700"):
    """The `stack` FRAME: VERTICAL, pad 0, gap 6, a bold lead line + body or a `list`
    (itself VERTICAL gap 6). Bullets are literal '*  ' text, not <ul> markers."""
    lead = text(h(C[lead_id]), weight=lead_weight, color=lead_color)
    if isinstance(body_ids, str):
        return col([lead, text(h(C[body_ids]))], gap=gap)
    return col([lead, col([text(h(C[b])) for b in body_ids], gap="6px")], gap=gap)

# ---- the five product blocks ------------------------------------------------
# (h2, image key, sub-head, [(lead, body_or_list)...], price line, CTA label, href)
PRODUCTS = [
    dict(h2="850:1555", key="hlth_band", sub="850:1559",
         prose=[("850:1561", "850:1562"), ("850:1564", "850:1565")],
         price="850:1566",
         lists=[("850:1568", ["850:1570", "850:1571", "850:1572", "850:1573"]),
                ("850:1575", ["850:1577", "850:1578", "850:1579", "850:1580"]),
                ("850:1582", ["850:1584", "850:1585"])],
         cta="850:1587", href=PDP),
    dict(h2="850:1590", key="withings", sub="850:1594",
         prose=[("850:1596", "850:1597"), ("850:1599", "850:1600")],
         price="850:1601",
         lists=[("850:1603", ["850:1605", "850:1606", "850:1607", "850:1608"]),
                ("850:1610", ["850:1612", "850:1613", "850:1614"]),
                ("850:1616", ["850:1618", "850:1619", "850:1620"])],
         cta="850:1622", href=WITHINGS),
    dict(h2="850:1625", key="oura", sub="850:1629",
         prose=[("850:1631", "850:1632"), ("850:1634", "850:1635")],
         price="850:1636",
         lists=[("850:1638", ["850:1640", "850:1641", "850:1642", "850:1643"]),
                ("850:1645", ["850:1647", "850:1648"]),
                ("850:1650", ["850:1652", "850:1653", "850:1654"])],
         cta="850:1656", href=OURA),
    dict(h2="850:1659", key="taking_care", sub="850:1663",
         prose=[("850:1665", "850:1666"), ("850:1668", "850:1669")],
         price="850:1670",
         lists=[("850:1672", ["850:1674", "850:1675", "850:1676", "850:1677"]),
                ("850:1679", ["850:1681", "850:1682", "850:1683"]),
                ("850:1685", ["850:1687", "850:1688", "850:1689"])],
         cta="850:1691", href=TAKINGCARE),
    dict(h2="850:1694", key="oximeter", sub="850:1698",
         prose=[("850:1700", "850:1701"), ("850:1703", "850:1704")],
         price="850:1705",
         lists=[("850:1707", ["850:1709", "850:1710", "850:1711", "850:1712"]),
                ("850:1714", ["850:1716", "850:1717", "850:1718"]),
                ("850:1720", ["850:1722", "850:1723", "850:1724"])],
         cta="850:1726", href=OXIMETER),
]

# Currency tagging, per node id. Our own band goes through the Shopify price feed;
# every competitor / editorial figure through the mid-market converter. Never mixed.
MONEY = {
    "850:1566": [("£79", PRICE), ("£158", COMPARE)],
    "850:1601": [("£129.95", FX("129.95"))],
    "850:1620": [("£129.95", FX("129.95"))],
    "850:1636": [("£349", FX("349")), ("£5.99", FX("5.99"))],
    "850:1652": [("£560", FX("560")), ("£349", FX("349")), ("£5.99", FX("5.99"))],
    "850:1670": [("£69.99", FX("69.99")), ("£28.49", FX("28.49"))],
    "850:1687": [("£28.49", FX("28.49")), ("£69.99", FX("69.99"))],
    "850:1705": [("£20", FX("20"))],
    "850:1716": [("£20", FX("20"))],
    "850:1730": [("£79", PRICE)],
    "850:1740": [("£79", PRICE), ("£158", COMPARE)],
    "850:1750": [("£79", PRICE)],
    "850:1876": [("£79", PRICE)],
    "850:1939": [("£79", PRICE), ("£158", COMPARE), ("£129.95", FX("129.95")),
                 ("£69.99", FX("69.99")), ("£28.49", FX("28.49"))],
}

def copy_html(node_id):
    """Escaped, space-preserved, and currency-tagged where the inventory says so."""
    s = h(C[node_id])
    if node_id in MONEY:
        s = money(s, *MONEY[node_id])
    return s

def tagged_text(node_id, **kw):
    return text(copy_html(node_id), **kw)

def stack_tagged(lead_id, body_ids, lead_color=INK, lead_weight="700"):
    lead = text(h(C[lead_id]), weight=lead_weight, color=lead_color)
    return col([lead, col([tagged_text(b) for b in body_ids], gap="6px")], gap="6px")

def shared_article_kids(page_url):
    """Everything from "We tested:" down. Byte-identical between the two pages --
    the ONLY thing that varies is `page_url`, which the share buttons link to, and
    a share link that pointed at the other variant would corrupt the test."""
    kids = []
    # "We tested:" / "We looked at:" -- lead lines here are Regular #2b2e33, not Bold
    kids.append(stack("850:1539", ["850:1541", "850:1542", "850:1543", "850:1544", "850:1545"],
                      lead_color=BODY, lead_weight="400"))
    kids.append(stack("850:1547", ["850:1549", "850:1550", "850:1551", "850:1552"],
                      lead_color=BODY, lead_weight="400"))
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
            kids.append(col([text(h(C[lead]), weight="700", color=INK), tagged_text(bod)], gap="6px"))
        kids.append(tagged_text(p["price"]))
        for lead, items in p["lists"]:
            kids.append(stack_tagged(lead, items))
        kids.append(button(h(C[p["cta"]]), p["href"]))
        kids.append(hr())

    # ---- Final word --------------------------------------------------------------
    kids.append(title(h(C["850:1728"]), "26px", "33px", font=SERIF, color=INK,
                      m={"fontSize": "22px", "lineHeight": "28px"}))
    for i in ("850:1729", "850:1730", "850:1731"):
        kids.append(tagged_text(i))
    kids.append(hr())

    # ---- offer (850:1733) : gap 18, no box -- it reads as part of the article ----
    # The offer CTA is FILL at BOTH widths (720x56 / 350x56) and one size up: 19/24,
    # padding 16/28. Every other in-article CTA is 17/24, padding 14/28, hug->fill.
    offer_cta = button(money(h(C["850:1749"]), ("£79", PRICE)), PDP,
                       size="19px", lh="24px",
                       pad={"top": "16px", "right": "28px", "bottom": "16px", "left": "28px"})
    offer_cta["styles"] = [s for s in offer_cta["styles"] if s["prop"] != "width"]
    offer_cta["styles"].append({"prop": "width", "value": "100%"})

    kids.append(col([
        title(h(C["850:1734"]), "26px", "33px", font=SERIF, color=INK,
              m={"fontSize": "22px", "lineHeight": "28px"}),
        product_image("hlth_wrist"),
        text(h(C["850:1738"])),
        col([tagged_text(i) for i in ("850:1740", "850:1741", "850:1742", "850:1743",
                                      "850:1744", "850:1745", "850:1746", "850:1747")], gap="6px"),
        offer_cta,
        tagged_text("850:1750", size="14px", lh="20px", color=META),
    ], gap="18px"))

    # ---- share row (850:1751) : "Share on" + 4 icons, gap 12 / icons gap 16 -----
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
        % (h(C["850:1752"]), _icons)))

    # ---- comments (850:1762) ----------------------------------------------------
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
        inner = [hug_text(name_html or h(C[name_id]), size="15px", lh="20px", color=INK, weight="700")]
        if date_id:
            inner.append(hug_text(h(C[date_id]), size="13px", lh="18px", color=META))
        inner.append(tagged_text(body_id, size="16px", lh="26px", color=BODY))
        if reply_id:
            inner.append(hug_text(h(C[reply_id]), size="13px", lh="18px", color=META))
        return inner

    def comment_row(avatar, stack_children, pad=None, extra_children=None, maxw="640px"):
        # The design's comment text stack is 640 FIXED inside a HUG row (44 avatar + 14 gap
        # + 640 = 698, i.e. 22px short of the 720 column). Plain flex:1 gives 662 and the
        # longer comment bodies then wrap to one line where the design wraps to two --
        # caught by design_diff's line-count check, invisible to everything else.
        # At 390 the remaining width is 292, well under the cap, so it still fills.
        body_col = col(stack_children, gap="4px",
                       styles=[{"prop": "flex", "value": "1"}, {"prop": "minWidth", "value": "0"},
                               {"prop": "maxWidth", "value": maxw}])
        if extra_children:
            body_col["p"]["children"].extend(extra_children)
        return rowf([avatar, body_col], gap="14px", align="flex-start",
                    styles=[{"prop": "padding", "value": pad or
                             {"top": "18px", "right": "0px", "bottom": "18px", "left": "0px"}}])

    # the nested reply that lives inside the pat1951 row -- name + body only, no date,
    # no "Reply" link, and a real photo avatar
    nested_reply = comment_row(
        avatar_photo(),
        comment_stack(None, None, "850:1829", None, name_html=h(C["850:1828"])),
        pad={"top": "14px", "right": "0px", "bottom": "0px", "left": "0px"},
        maxw="580px")   # the reply's own stack is 580 in the design, not 640

    COMMENTS = [
        ("850:1771", "850:1772", "850:1773", "850:1774", None),
        ("850:1783", "850:1784", "850:1785", "850:1786", None),
        ("850:1795", "850:1796", "850:1797", "850:1798", None),
        ("850:1807", "850:1808", "850:1809", "850:1810", None),
        ("850:1819", "850:1820", "850:1821", "850:1822", nested_reply),
        ("850:1838", "850:1839", "850:1840", "850:1841", None),
        ("850:1850", "850:1851", "850:1852", "850:1853", None),
        ("850:1862", "850:1863", "850:1864", "850:1865", None),
        ("850:1874", "850:1875", "850:1876", "850:1877", None),
    ]
    comment_kids = [title(h(C["850:1763"]), "24px", "30px", font=SERIF, color=INK,
                          m={"fontSize": "21px", "lineHeight": "26px"})]
    for n, d, b, r, nested in COMMENTS:
        comment_kids.append(comment_row(avatar_generic(), comment_stack(n, d, b, r),
                                        extra_children=[nested] if nested else None))
        comment_kids.append(hr())
    # "Show more comments (6)" is a TEXT node in the design and there are no further six
    # comments to show, so it stays text (decision 2).
    comment_kids.append(hug_text(h(C["850:1879"]), size="15px", lh="20px", color=INK, weight="700"))
    kids.append(col(comment_kids, gap="0px"))

    # ---- leave a comment (850:1880) : decorative (decision 2) -------------------
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

    post_btn = container([container([text(h(C["850:1893"]), size="17px", lh="24px", color=WHITE,
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
        title(h(C["850:1881"]), "20px", "26px", font=SANS, weight="800", color=INK, level="3",
              m={"fontSize": "17px", "lineHeight": "22px"}),
        text(h(C["850:1882"]), size="14px", lh="20px", color=META),
        field("850:1884", "120px"),
        field("850:1887", "48px"),
        field("850:1890", "48px"),
        post_btn,
    ], gap="14px"))

    # ---- newsletter (850:1894) : #f5f6f7 card, radius 10, pad 32/24, gap 10 -----
    sub_btn = container([container([text(h(C["850:1900"]), size="16px", lh="22px", color=WHITE,
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
        title(h(C["850:1895"]), "24px", "30px", font=SERIF, color=INK, align="center",
              m={"fontSize": "21px", "lineHeight": "26px"}),
        text(h(C["850:1896"]), size="16px", lh="24px", color=META),
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
        {"prop": "padding", "value": {"top": "32px", "right": "24px", "bottom": "32px", "left": "24px"}}])
    kids.append(newsletter)

    return kids

# ============================ footer =========================================
FOOT_A = [("850:1906", CAT % "wearables"), ("850:1907", CAT % "smart-home"),
          ("850:1908", CAT % "audio"), ("850:1909", None), ("850:1910", CAT % "laptops"),
          ("850:1911", CAT % "health-tech"), ("850:1912", CAT % "buying-guides")]
# Terms / Privacy / Editorial standards / Affiliate policy carry the ids the shared
# modal handler in tu_legal_modals.html listens for (decision 1).
FOOT_B = [("850:1915", None, None), ("850:1916", None, None),
          ("850:1917", "#tu-edit", "edit"), ("850:1918", None, None),
          ("850:1919", "#tu-terms", "terms"), ("850:1920", "#tu-priv", "priv"),
          ("850:1921", "#tu-aff", "aff")]

def foot_heading(i):
    return hug_text(h(C[i]), size="13px", lh="18px", color=INK, weight="700", ls="0.08em")

def foot_link(i, href, el_id=None):
    if href is None:
        return hug_text(h(C[i]), size="14px", lh="20px", color=META)
    idattr = ' id="%s"' % el_id if el_id else ""
    return hug_text('<a href="%s"%s style="color:#6b7078;text-decoration:none">%s</a>'
                    % (href, idattr, h(C[i])), size="14px", lh="20px", color=META)

col_a = col([foot_heading("850:1905")] + [foot_link(i, hrf) for i, hrf in FOOT_A],
            gap="8px", styles=[{"prop": "maxWidth", "value": "350px"}])
col_b = col([foot_heading("850:1914")] + [foot_link(i, hrf, eid) for i, hrf, eid in FOOT_B],
            gap="8px", styles=[{"prop": "maxWidth", "value": "350px"}])
logo_plate = container([logo_img()],
                       [{"prop": "width", "value": "220px"}, {"prop": "height", "value": "60px"},
                        {"prop": "backgroundColor", "value": LOGO_BG},
                        {"prop": "borderRadius", "value": "6px"},
                        {"prop": "lfDisplay", "value": "flex"},
                        {"prop": "alignItems", "value": "center"},
                        {"prop": "justifyContent", "value": "center"},
                        {"prop": "flexShrink", "value": "0"}])
col_c = col([logo_plate, text(h(C["850:1937"]), size="14px", lh="20px", color=META)],
            gap="14px", styles=[{"prop": "maxWidth", "value": "350px"}])

footer_row = rowf([col_a, col_b, col_c], gap="30px", align="flex-start",
                  styles=[{"prop": "flexDirection", "value": "column", "media": 767},
                          {"prop": "gap", "value": "28px", "media": 767}])

legal = col([tagged_text("850:1939", size="12.5px", lh="20px", color=META),
             text(h(C["850:1940"]), size="12.5px", lh="20px", color=META),
             text(h(C["850:1941"]), size="12.5px", lh="20px", color=META),
             text(h(C["850:1942"]), size="12.5px", lh="20px", color=META)], gap="10px")

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

    body = {"id": nid(), "t": "Root", "version": 11,
            "styles": [{"prop": "pageWidth", "value": "760px"},
                       {"prop": "backgroundColor", "value": WHITE}],
            "p": {"children": [support_bar, logo_bar, nav, rule_under_nav, promo, rule(),
                               breadcrumb, rule(), article, rule(), footer]}}

    return body


def verify_shared_identical(page_url_a, page_url_b):
    """Bind this module's shared half to the engine's structural comparison."""
    return TU.verify_shared_identical(shared_article_kids, page_url_a, page_url_b)
