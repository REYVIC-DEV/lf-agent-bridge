#!/usr/bin/env python3
"""Build the full techunboxed article page (article body + footer category
cards) as native Lightfunnels blocks and write it to the test funnel."""
import sys, uuid, json, html as H2
sys.path.insert(0, '.')
import lf_api

tok = open('.session_token').read().strip()
HH = {"account-id": "90380", "version": "1",
      "Origin": "https://app.lightfunnels.com", "Referer": "https://app.lightfunnels.com/"}
def sgql(q, v=None): return lf_api.gql(tok, q, v, extra_headers=HH)
def nid(): return str(uuid.uuid4())

seq = json.load(open("/tmp/tub_seq3.json"))
foot = json.load(open("/tmp/tub_footer.json"))

NB = {"r": 10, "g": 10, "b": 10, "a": 1}
GRAY = {"r": 110, "g": 115, "b": 125, "a": 1}
RED = {"r": 214, "g": 40, "b": 40, "a": 1}
TITLE = {"1": ("40px", "48px", "0px", "-1.6px"), "2": ("30px", "42px", "22px", "normal"),
         "3": ("26px", "36px", "22px", "normal")}

def title(t, sz):
    fs, lh, mt, ls = TITLE[sz]
    return {"t": "Title", "id": nid(), "p": {"size": sz, "content": t, "widthOption": "fill"},
        "styles": [{"prop": "fontFamily", "value": "Inter", "boundTo": "static_heading_font"},
            {"prop": "color", "value": NB}, {"prop": "fontSize", "value": fs},
            {"prop": "lineHeight", "value": lh}, {"prop": "fontWeight", "value": "700"},
            {"prop": "letterSpacing", "value": ls}, {"prop": "textAlign", "value": "left"},
            {"prop": "maxWidth", "value": "100%"}, {"prop": "width", "value": "100%"},
            {"prop": "margin", "value": {"top": mt}}]}

def text(html, size="16px", lh="26px", color=NB, weight="400", extra=None):
    st = [{"prop": "fontFamily", "value": "Inter"}, {"prop": "color", "value": color},
          {"prop": "fontSize", "value": size}, {"prop": "lineHeight", "value": lh},
          {"prop": "fontWeight", "value": weight}, {"prop": "textAlign", "value": "left"},
          {"prop": "maxWidth", "value": "100%"}]
    if extra: st += extra
    return {"t": "Text", "id": nid(), "p": {"content": html}, "styles": st}

def image(src, w="100%", radius="12px"):
    return {"t": "Image", "id": nid(), "p": {"src": src, "title": "image"},
        "styles": [{"prop": "maxWidth", "value": "100%"}, {"prop": "width", "value": w},
            {"prop": "borderRadius", "value": radius}, {"prop": "margin", "value": {"top": "6px", "bottom": "10px"}}]}

def container(children, styles):
    return {"t": "Container", "id": nid(), "styles": styles, "p": {"children": children}}

def para_html(t, links):
    s = H2.escape(t)
    for l in links:
        lt = H2.escape(l["text"])
        if lt in s:
            s = s.replace(lt, '<a href="%s" style="color:#1a0dab;font-weight:600;word-break:break-word" target="_blank">%s</a>' % (H2.escape(l["href"]), lt), 1)
    return s

# ---- article body ----
hero = next((x["src"] for x in seq if x["type"] == "img"), None)
kids = [title("AI in The Home: The Smartest Devices of 2026", "1"),
        text('<span style="display:inline-block;background:#d62828;color:#ffffff;padding:3px 9px;border-radius:4px;font-size:12px;font-weight:700;vertical-align:middle">Smart Home</span>&nbsp;<span style="color:#5a5f69;font-size:14px;vertical-align:middle">By Oliver Hayes</span>')]
if hero:
    kids.append(image(hero))
for x in seq:
    if x["type"] == "img":
        continue
    t = x.get("text", "")
    if t in ("Smart Home", "By Oliver Hayes", "AI in The Home: The Smartest Devices of 2026"):
        continue
    if x["type"] in ("h2", "h3"):
        kids.append(title(t, x["type"][1]))
    elif x["type"] == "h1":
        kids.append(title(t, "2"))
    else:
        kids.append(text(para_html(t, x.get("links", []))))

# ---- footer: parse cards, group by category via Y ranges ----
MONTHS = {'Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'}
def parse_card(c):
    ts = c["texts"]
    date_tok = [t for t in ts if t.isdigit() or t in MONTHS]
    rest = [t for t in ts if t not in date_tok]
    rest.sort(key=len, reverse=True)
    return {"img": c["img"], "title": rest[0] if rest else "",
            "kicker": rest[1] if len(rest) > 1 else "",
            "date": " ".join(date_tok)}

# category section Y starts (from the main footer grid, second occurrences)
SECTIONS = [("Smart Home", 10640, 11286), ("Laptops", 11286, 11922), ("Mobile", 11922, 12569),
            ("Audio", 12569, 13216), ("Health Tech", 13216, 13864), ("Wearables", 13864, 14635)]
yal = [parse_card(c) for c in foot["cards"] if 6900 <= c["y"] < 10640]

def card_block(cd, show_meta=True):
    col = []
    if show_meta and cd["kicker"]:
        col.append(text(H2.escape(cd["kicker"].upper()), size="12px", lh="16px", color=RED, weight="700"))
    col.append(text('<b>%s</b>' % H2.escape(cd["title"]), size="17px", lh="23px", color=NB, weight="700"))
    if show_meta and cd["date"]:
        col.append(text(H2.escape(cd["date"]), size="13px", lh="18px", color=GRAY))
    colc = container(col, [{"prop": "lfDisplay", "value": "flex"}, {"prop": "flexDirection", "value": "column"},
                           {"prop": "gap", "value": "5px"}, {"prop": "flex", "value": "1"},
                           {"prop": "minWidth", "value": "0"}])
    thumb_img = {"t": "Image", "id": nid(), "p": {"src": cd["img"], "title": "thumb"},
        "styles": [{"prop": "width", "value": "100%"}, {"prop": "maxWidth", "value": "100%"},
            {"prop": "borderRadius", "value": "8px"}, {"prop": "objectFit", "value": "cover"}]}
    thumb = container([thumb_img],
        [{"prop": "width", "value": "150px"}, {"prop": "maxWidth", "value": "150px"},
         {"prop": "flexShrink", "value": "0"}])
    return container([thumb, colc],
        [{"prop": "lfDisplay", "value": "flex"}, {"prop": "flexDirection", "value": "row"},
         {"prop": "gap", "value": "16px"}, {"prop": "width", "value": "100%"},
         {"prop": "alignItems", "value": "center"}, {"prop": "padding", "value": {"top": "10px", "bottom": "10px"}}])

# You may also like
if yal:
    kids.append(title("You may also like", "2"))
    for cd in yal:
        kids.append(card_block(cd, show_meta=False))
# category sections
for name, y0, y1 in SECTIONS:
    cards = [parse_card(c) for c in foot["cards"] if y0 <= c["y"] < y1]
    if not cards:
        continue
    kids.append(title(name, "2"))
    for cd in cards:
        kids.append(card_block(cd, show_meta=True))

body = {"id": nid(), "t": "Root", "version": 11, "styles": [{"prop": "pageWidth", "value": "960px"}],
    "p": {"children": [{"t": "Section", "id": nid(),
        "styles": [{"prop": "padding", "value": {"top": "24px", "bottom": "40px"}}],
        "p": {"layout": "", "dividerPosition": ["top"], "horizontalFlip": False,
              "embedded_video": {"src": "", "video_size": "stretch", "video_position": "center"},
              "children": [container(kids,
                  [{"prop": "maxWidth", "value": "928px"}, {"prop": "width", "value": "100%"},
                   {"prop": "margin", "value": {"left": "auto", "right": "auto"}},
                   {"prop": "flexDirection", "value": "column"}, {"prop": "gap", "value": "16px"}])]}}]}}

n = sgql('query($q: String!){ funnels(first:1,query:$q){ edges { node { slug steps { uid slug title type settings visual{x y} } } } } }', {"q": "id:fun_PdvUZbSAynI6fAPzJSzWr"})["funnels"]["edges"][0]["node"]
st = next(s for s in n["steps"] if s["uid"] == "step_ArxRibhU7WXI-WUPOiopz")
sgql('mutation($id: ID!, $node: InputFunnel!){ updateFunnel(id:$id,node:$node){ id } }',
    {"id": "fun_PdvUZbSAynI6fAPzJSzWr", "node": {"steps": [{"id": st["uid"], "slug": st["slug"],
        "title": "AI in the Home (full clone)", "type": st["type"], "settings": st["settings"],
        "visual": st["visual"], "body": body}]}})
from collections import Counter
print("built full page:", len(kids), "top-level blocks | you-may-also-like:", len(yal), "cards")
print("PREVIEW: https://99commerce.myecomsite.net/%s/%s?preview=true" % (n["slug"], st["slug"]))
