#!/usr/bin/env python3
"""Full techunboxed article clone -> native LF blocks, LF-hosted images,
flex card rows. Creates a fresh step in the test funnel (falls back to
overwriting a page if a new linked step can't be made)."""
import sys, uuid, json, html as H2
sys.path.insert(0, '.')
import lf_api

tok = open('.session_token').read().strip()
ACCT = open('.lf_account').read().strip()
HH = {"account-id": ACCT, "version": "1",
      "Origin": "https://app.lightfunnels.com", "Referer": "https://app.lightfunnels.com/"}
def sgql(q, v=None): return lf_api.gql(tok, q, v, extra_headers=HH)
def nid(): return str(uuid.uuid4())

FUNNEL = "fun_PdvUZbSAynI6fAPzJSzWr"
seq = json.load(open("/tmp/tub_seq3.json"))
foot = json.load(open("/tmp/tub_footer.json"))
IMG = json.load(open("/tmp/img_map.json"))
HERO_URL = "https://framerusercontent.com/images/Yj1jbtEfyptIXnFb22CP6Xb0GA.png"

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

def text(content, size="16px", lh="26px", color=NB, weight="400"):
    return {"t": "Text", "id": nid(), "p": {"content": content},
        "styles": [{"prop": "fontFamily", "value": "Inter"}, {"prop": "color", "value": color},
            {"prop": "fontSize", "value": size}, {"prop": "lineHeight", "value": lh},
            {"prop": "fontWeight", "value": weight}, {"prop": "textAlign", "value": "left"},
            {"prop": "maxWidth", "value": "100%"}]}

def image(url, radius="12px", full=True):
    m = IMG.get(url)
    p = {"title": "image"}
    if m:
        p.update({"src_id": m["src_id"], "src_uid": m["src_uid"], "src": m["src"]})
    else:
        p["src"] = url
    st = [{"prop": "maxWidth", "value": "100%"}, {"prop": "borderRadius", "value": radius},
          {"prop": "objectFit", "value": "cover"}]
    if full:
        st.append({"prop": "width", "value": "100%"})
    return {"t": "Image", "id": nid(), "p": p, "styles": st}

def container(children, styles):
    return {"t": "Container", "id": nid(), "styles": styles, "p": {"children": children}}

def para_html(t, links):
    s = H2.escape(t)
    for l in links:
        lt = H2.escape(l["text"])
        if lt in s:
            s = s.replace(lt, '<a href="%s" style="color:#1a0dab;font-weight:600;word-break:break-word" target="_blank">%s</a>' % (H2.escape(l["href"]), lt), 1)
    return s

# ---- article ----
kids = [title("AI in The Home: The Smartest Devices of 2026", "1"),
        text('<span style="display:inline-block;background:#d62828;color:#ffffff;padding:3px 9px;border-radius:4px;font-size:12px;font-weight:700;vertical-align:middle">Smart Home</span>&nbsp;<span style="color:#5a5f69;font-size:14px;vertical-align:middle">By Oliver Hayes</span>')]
kids.append(image(HERO_URL))
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

# ---- footer cards ----
MONTHS = {'Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'}
def parse_card(c):
    ts = c["texts"]
    dt = [t for t in ts if t.isdigit() or t in MONTHS]
    rest = sorted([t for t in ts if t not in dt], key=len, reverse=True)
    return {"img": c["img"], "title": rest[0] if rest else "",
            "kicker": rest[1] if len(rest) > 1 else "", "date": " ".join(dt)}

def card(cd, meta=True):
    col = []
    if meta and cd["kicker"]:
        col.append(text(H2.escape(cd["kicker"].upper()), size="12px", lh="16px", color=RED, weight="700"))
    col.append(text("<b>%s</b>" % H2.escape(cd["title"]), size="17px", lh="23px", weight="700"))
    if meta and cd["date"]:
        col.append(text(H2.escape(cd["date"]), size="13px", lh="18px", color=GRAY))
    colc = container(col, [{"prop": "lfDisplay", "value": "flex"}, {"prop": "flexDirection", "value": "column"},
                           {"prop": "gap", "value": "5px"}, {"prop": "flex", "value": "1"}, {"prop": "minWidth", "value": "0"}])
    thumb = container([image(cd["img"], radius="8px")],
        [{"prop": "width", "value": "150px"}, {"prop": "maxWidth", "value": "150px"}, {"prop": "flexShrink", "value": "0"}])
    return container([thumb, colc],
        [{"prop": "lfDisplay", "value": "flex"}, {"prop": "flexDirection", "value": "row"},
         {"prop": "gap", "value": "16px"}, {"prop": "width", "value": "100%"},
         {"prop": "alignItems", "value": "center"}, {"prop": "padding", "value": {"top": "10px", "bottom": "10px"}}])

SECTIONS = [("Smart Home", 10640, 11286), ("Laptops", 11286, 11922), ("Mobile", 11922, 12569),
            ("Audio", 12569, 13216), ("Health Tech", 13216, 13864), ("Wearables", 13864, 14635)]
yal = [parse_card(c) for c in foot["cards"] if 6900 <= c["y"] < 10640]
if yal:
    kids.append(title("You may also like", "2"))
    for cd in yal:
        kids.append(card(cd, meta=False))
for name, y0, y1 in SECTIONS:
    cards = [parse_card(c) for c in foot["cards"] if y0 <= c["y"] < y1]
    if not cards:
        continue
    kids.append(title(name, "2"))
    for cd in cards:
        kids.append(card(cd, meta=True))

body = {"id": nid(), "t": "Root", "version": 11, "styles": [{"prop": "pageWidth", "value": "960px"}],
    "p": {"children": [{"t": "Section", "id": nid(),
        "styles": [{"prop": "padding", "value": {"top": "24px", "bottom": "40px"}}],
        "p": {"layout": "boxed", "dividerPosition": ["top"], "horizontalFlip": False,
              "embedded_video": {"src": "", "video_size": "stretch", "video_position": "center"},
              "children": [container(kids,
                  [{"prop": "maxWidth", "value": "928px"}, {"prop": "width", "value": "100%"},
                   {"prop": "margin", "value": {"left": "auto", "right": "auto"}},
                   {"prop": "lfDisplay", "value": "flex"}, {"prop": "flexDirection", "value": "column"},
                   {"prop": "gap", "value": "16px"}])]}}]}}

# ---- make a fresh step, else fall back to overwriting one page ----
def steps_now():
    n = sgql('query($q: String!){ funnels(first:1,query:$q){ edges { node { slug steps { uid slug } } } } }', {"q": f"id:{FUNNEL}"})["funnels"]["edges"][0]["node"]
    return n["slug"], {s["uid"]: s["slug"] for s in n["steps"]}

slug0, before = steps_now()
new_id = "step_" + uuid.uuid4().hex[:21]
new_slug = "ai-home-full-" + uuid.uuid4().hex[:5]
try:
    sgql('mutation($id: ID!, $node: InputFunnel!){ updateFunnel(id:$id,node:$node){ id } }',
        {"id": FUNNEL, "node": {"steps": [{"id": new_id, "slug": new_slug,
            "title": "AI in the Home (full, side by side)", "type": "article_page",
            "settings": {}, "visual": {"x": 1300, "y": 100}, "body": body}]}})
    _, after = steps_now()
    if new_id in after:
        target, tslug, how = new_id, after[new_id], "created new linked step"
    else:
        raise RuntimeError("new step did not attach")
except RuntimeError:
    # fallback: overwrite the native-rebuild page
    target = "step_ArxRibhU7WXI-WUPOiopz"
    cur = sgql('query($q: String!){ funnels(first:1,query:$q){ edges { node { steps { uid slug type settings visual{x y} } } } } }', {"q": f"id:{FUNNEL}"})["funnels"]["edges"][0]["node"]
    st = next(s for s in cur["steps"] if s["uid"] == target)
    sgql('mutation($id: ID!, $node: InputFunnel!){ updateFunnel(id:$id,node:$node){ id } }',
        {"id": FUNNEL, "node": {"steps": [{"id": target, "slug": st["slug"],
            "title": "AI in the Home (full, side by side)", "type": st["type"],
            "settings": st["settings"], "visual": st["visual"], "body": body}]}})
    tslug, how = st["slug"], "overwrote existing page (new step won't attach via API)"

from collections import Counter
print(how)
print("blocks:", dict(Counter(k["t"] for k in kids)), "total", len(kids))
print("PREVIEW:", f"https://99commerce.myecomsite.net/{slug0}/{tslug}?preview=true")
