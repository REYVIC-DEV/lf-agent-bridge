#!/usr/bin/env python3
"""Build the HLTH advertorial (from Figma node 387:201) as native LF blocks
and write it into the starting step of fun_XHwV9fd9Z3FFyXPPfNot0 (session)."""
import json, uuid, lf_api

tok = open('.session_token').read().strip()
ACCT = open('.lf_account').read().strip()
HH = {"account-id": ACCT, "version": "1",
      "Origin": "https://app.lightfunnels.com", "Referer": "https://app.lightfunnels.com/"}
def sgql(q, v=None): return lf_api.gql(tok, q, v, extra_headers=HH)
def nid(): return str(uuid.uuid4())

FUNNEL = "fun_XHwV9fd9Z3FFyXPPfNot0"
STEP   = "step_YOQL2Poa2CEsaPD_D6pO4"
IMG = json.load(open("/tmp/hlth_img_map.json"))

# ---- colors ----
NAVY  = {"r": 25,  "g": 30,  "b": 42,  "a": 1}   # #191e2a
RED   = {"r": 230, "g": 57,  "b": 70,  "a": 1}   # #e63946
GREY  = {"r": 76,  "g": 76,  "b": 76,  "a": 1}   # #4c4c4c body
WHITE = {"r": 255, "g": 255, "b": 255, "a": 1}
SPON  = {"r": 189, "g": 189, "b": 189, "a": 1}   # #bdbdbd
BORDER= {"r": 246, "g": 246, "b": 246, "a": 1}   # #f6f6f6

# ---- links ----
PDP = "https://hlthtrack.com/products/wearable-hlth-band"
TP  = "https://www.trustpilot.com/review/hlthtrack.com"

# ---- inline HTML span helpers (match Figma text runs) ----
def B(t):  return '<span style="color:#191e2a;font-weight:600">%s</span>' % t
def L(t):  return '<a href="%s" target="_blank" style="color:#e63946;font-weight:700;text-decoration:underline">%s</a>' % (PDP, t)   # product name -> PDP
def LT(t): return '<a href="%s" target="_blank" style="color:#e63946;font-weight:700;text-decoration:underline">%s</a>' % (TP, t)   # Trustpilot

# ---- block builders ----
def title(content, size, fs, lh, mt=0, color=NAVY, align="left"):
    st = [{"prop": "fontFamily", "value": "Inter"}, {"prop": "color", "value": color},
          {"prop": "fontSize", "value": fs}, {"prop": "lineHeight", "value": lh},
          {"prop": "fontWeight", "value": "700"}, {"prop": "textAlign", "value": align},
          {"prop": "width", "value": "100%"}, {"prop": "maxWidth", "value": "100%"}]
    if mt: st.append({"prop": "margin", "value": {"top": "%spx" % mt}})
    return {"t": "Title", "id": nid(), "p": {"size": size, "content": content, "widthOption": "fill"}, "styles": st}

def text(content, size="18px", lh="31px", color=GREY, weight="400", align="left", italic=False, mw="100%"):
    st = [{"prop": "fontFamily", "value": "Inter"}, {"prop": "color", "value": color},
          {"prop": "fontSize", "value": size}, {"prop": "lineHeight", "value": lh},
          {"prop": "fontWeight", "value": weight}, {"prop": "textAlign", "value": align},
          {"prop": "maxWidth", "value": mw}, {"prop": "width", "value": "100%"}]
    if italic: st.append({"prop": "fontStyle", "value": "italic"})
    return {"t": "Text", "id": nid(), "p": {"content": content}, "styles": st}

def image(key, radius="0px", full=True, extra=None, height=None, mheight=None):
    m = IMG[key]
    p = {"title": key}
    if "src_id" in m:
        p.update({"src_id": m["src_id"], "src_uid": m["src_uid"], "src": m["src"]})
    else:
        p["src"] = m["src"]
    st = [{"prop": "maxWidth", "value": "100%"}, {"prop": "borderRadius", "value": radius},
          {"prop": "objectFit", "value": "cover"}, {"prop": "lfDisplay", "value": "block"}]
    if full: st.append({"prop": "width", "value": "100%"})
    if height:
        st.append({"prop": "height", "value": height})
        if mheight:
            st.append({"prop": "height", "value": mheight, "media": 767})
    if extra: st.extend(extra)
    return {"t": "Image", "id": nid(), "p": p, "styles": st}

def container(children, styles):
    return {"t": "Container", "id": nid(), "styles": styles, "p": {"children": children}}

def cta():
    label = {"t": "Text", "id": nid(),
        "p": {"content": "GET UP TO £79 OFF HLTH BAND"},
        "styles": [{"prop": "fontFamily", "value": "Inter"}, {"prop": "color", "value": WHITE},
            {"prop": "fontSize", "value": "17px"}, {"prop": "fontWeight", "value": "700"},
            {"prop": "lineHeight", "value": "31px"}, {"prop": "textTransform", "value": "uppercase"},
            {"prop": "textAlign", "value": "center"}, {"prop": "whiteSpace", "value": "nowrap"},
            {"prop": "maxWidth", "value": "100%"}]}
    labelwrap = container([label],
        [{"prop": "lfDisplay", "value": "flex"}, {"prop": "alignItems", "value": "center"},
         {"prop": "justifyContent", "value": "center"}, {"prop": "maxWidth", "value": "100%"}])
    btn = {"t": "BlockLink", "id": nid(),
        "p": {"destination": {"type": "static", "value": PDP}, "target": "_blank",
              "widthOption": "auto", "children": [labelwrap]},
        "styles": [{"prop": "backgroundColor", "value": RED},
            {"prop": "borderRadius", "value": "10px"},
            {"prop": "padding", "value": {"top": "18px", "bottom": "18px", "left": "40px", "right": "40px"}},
            {"prop": "minWidth", "value": "350px"},
            {"prop": "borderStyle", "value": "solid"}, {"prop": "borderWidth", "value": "2px"},
            {"prop": "borderColor", "value": BORDER},
            {"prop": "lfDisplay", "value": "flex"}, {"prop": "alignItems", "value": "center"},
            {"prop": "justifyContent", "value": "center"}]}
    return container([btn],
        [{"prop": "lfDisplay", "value": "flex"}, {"prop": "justifyContent", "value": "center"},
         {"prop": "width", "value": "100%"},
         {"prop": "padding", "value": {"top": "20px", "bottom": "10px"}}])

# ---- author card ----
def author_card():
    avatar = image("avatar", radius="50%", full=False,
        extra=[{"prop": "width", "value": "95px"}, {"prop": "height", "value": "95px"}])
    avwrap = container([avatar], [{"prop": "width", "value": "95px"}, {"prop": "flexShrink", "value": "0"}])
    col = container([
        text("By", size="14px", lh="20px", color=NAVY, weight="300"),
        text("CHRIS KOWALSKI", size="13.8px", lh="20px", color=NAVY, weight="700"),
        text("June 28, 2026", size="13.5px", lh="20px", color=NAVY, weight="400"),
        text("In Partnership With HLTH", size="13.2px", lh="20px", color=NAVY, weight="300"),
    ], [{"prop": "lfDisplay", "value": "flex"}, {"prop": "flexDirection", "value": "column"},
        {"prop": "flex", "value": "1"}, {"prop": "minWidth", "value": "0"},
        {"prop": "padding", "value": {"left": "12px"}}])
    return container([avwrap, col],
        [{"prop": "lfDisplay", "value": "flex"}, {"prop": "flexDirection", "value": "row"},
         {"prop": "alignItems", "value": "center"}, {"prop": "width", "value": "100%"},
         {"prop": "gap", "value": "0px"}, {"prop": "margin", "value": {"top": "6px", "bottom": "6px"}}])

# ---- blockquote ----
def blockquote():
    inner = text('<b style="color:#191e2a">The result?</b> '
                 '<span style="color:#7c7c7c;font-weight:500">Battery life that lasts up to 30 days on a single '
                 'charge. Whether you’re a busy professional, new parent, or retiree, I think we can all '
                 'appreciate this feature.</span>',
                 size="17px", lh="31px", color=GREY, italic=True)
    return container([inner],
        [{"prop": "borderStyle", "value": "solid"}, {"prop": "borderColor", "value": RED},
         {"prop": "borderWidth", "value": "0px 0px 0px 3px"},
         {"prop": "padding", "value": {"left": "19px", "right": "16px", "top": "2px", "bottom": "2px"}},
         {"prop": "width", "value": "100%"}])

# ---- assemble article column ----
kids = []
kids.append(title("The Screenless Health Tracker That's Outselling Smartwatches in the UK",
                  "1", "40px", "52px"))
kids.append(author_card())

kids.append(text(
    "As a longevity optimiser who’s always on the hunt for smarter, more " + B("affordable ways to take care of my body") +
    ", the search for a trusted tracker almost never stops. I've been wearing a smartwatch every day for the last four "
    "years and was never able to fully trust the data. But the " + L("HLTH band") + " – a " + B("screenless wearable") +
    " that only tracks health, is the first one to change that. It's rated 4.6 on " + LT("Trustpilot") +
    " and has sold out three times since its release in the UK this April."))

kids.append(text("Here's why I'm putting my " + B("smartwatch in the drawer") + " — and why you might want to do the same."))

# Section 1
kids.append(title("1. It takes 288 readings a day", "2", "30px", "39px", mt=32))
kids.append(image("sec1_phone", height="532px", mheight="230px"))
kids.append(text(
    "Most wearables take a few readings an hour, then fill the gaps with estimates. " + L("HLTH Band") + " takes " +
    B("288 readings ") + "a day across " + B("blood pressure, heart rate, HRV, sleep and more.") +
    " Plus its algorithm filters out noise automatically, so only clean data reaches your trends.<br><br>" +
    B("More readings means more accuracy. And more accuracy means you're seeing what's actually happening in your body.")))

# Section 2
kids.append(title("2. No slimy subscriptions or hidden fees", "2", "30px", "39px", mt=32))
kids.append(text(
    "This is the one that made me " + B("double-take.") + " While most trackers charge you to rent your own health data "
    "and bury it in fine print, " + L("HLTH band") + " is a one-time purchase. The app is " + B("completely free") +
    ", and all your data – blood pressure trends, heart rate, HRV, sleep stages – is accessible from day one.<br><br>"
    "When you see the quality of the device and the data, the price genuinely feels like they've made a mistake."))
kids.append(cta())

# Section 3
kids.append(title("3. Comfortable design you actually sleep in", "2", "30px", "39px", mt=32))
kids.append(image("sec3_wrist", height="532px", mheight="300px"))
kids.append(text(
    L("HLTH Band") + " weighs under " + B("18 grams (less than 30 pence!)") + ", and uses non-itchy flexible material for "
    "the band that feels like nothing. That makes it easy to " + B("sleep with or wear for any occasion") +
    " without looking like you’re sick or even wearing a health tracker. This isn’t just a cool design choice; "
    "it’s " + B("scientifically proven") + " that most heart events and health issues happen at night. So nightly "
    "tracking is even more important than day time tracking."))

# Section 4
kids.append(title("4. Proven 30 day battery life", "2", "30px", "39px", mt=32))
kids.append(text(
    "We all know that daily wear is key to finding our real baseline and avoiding health issues, but keeping trackers "
    "on is tricky when the battery dies daily. Enter " + L("HLTH Band’s") + " " + B("Flow Sense Intelligent routing feature.") +
    " Their advanced sensor watches your vitals and provides real-time adjustment to battery power, to prevent it from "
    "draining too fast."))
kids.append(blockquote())
kids.append(cta())

# Section 5
kids.append(title("5. Trend readings every 5 minutes", "2", "30px", "39px", mt=32))
kids.append(image("sec5_screen", height="480px", mheight="210px"))
kids.append(text(
    "Many devices on the market only take some readings at night or space them hours apart to save battery for screens. " +
    L("HLTH Band's") + " continuous " + B("tracking spaces out readings as low as every 5 minutes,") +
    " making it easier than ever to see how your " + B("food, sleep, workouts, and lifestyle habits") +
    " impact your health. So any changes you make can be seen quickly in your numbers."))
kids.append(cta())

# Final
kids.append(title("Ready to keep better watch of your health with HLTH Band?", "2", "30px", "39px", mt=32))
kids.append(text("From the continuous tracking and tight intervals to 30 day battery and comfortable design, " +
    L("HLTH Band") + " is packed with features that make health tracking smarter, more accurate, and more affordable.",
    color=NAVY))
kids.append(text("If you’re ready to keep a better eye on your health, protect your heart, and save money doing it. " +
    L("HLTH Band") + " is the partner you’ve been waiting for. Now, THIS is one launch worth getting excited about.",
    color=NAVY))
kids.append(cta())
kids.append(text('<i>Special <a href="%s" target="_blank" style="color:inherit;font-weight:700;text-decoration:underline">50%% off coupon</a> valid for UK customers only while supplies last</i>' % PDP,
    size="18px", lh="28px", color=NAVY, align="center", italic=True))

article_col = container(kids,
    [{"prop": "maxWidth", "value": "720px"}, {"prop": "width", "value": "100%"},
     {"prop": "margin", "value": {"left": "auto", "right": "auto"}},
     {"prop": "lfDisplay", "value": "flex"}, {"prop": "flexDirection", "value": "column"},
     {"prop": "gap", "value": "18px"}])

# ---- header (dark band: SPONSORED ARTICLE + logo) ----
header = {"t": "Section", "id": nid(),
    "styles": [{"prop": "backgroundColor", "value": NAVY},
               {"prop": "padding", "value": {"top": "8px", "bottom": "20px"}}],
    "p": {"layout": "", "dividerPosition": ["top"], "horizontalFlip": False,
          "embedded_video": {"src": "", "video_size": "stretch", "video_position": "center"},
          "children": [container([
              text("SPONSORED ARTICLE", size="11px", lh="18px", color=SPON, weight="400", align="center"),
              container([image("logo", full=False, extra=[{"prop": "width", "value": "200px"}, {"prop": "height", "value": "50px"}])],
                        [{"prop": "lfDisplay", "value": "flex"}, {"prop": "justifyContent", "value": "center"},
                         {"prop": "width", "value": "100%"}, {"prop": "margin", "value": {"top": "10px"}}]),
          ], [{"prop": "lfDisplay", "value": "flex"}, {"prop": "flexDirection", "value": "column"},
              {"prop": "alignItems", "value": "center"}, {"prop": "width", "value": "100%"},
              {"prop": "letterSpacing", "value": "1px"}])]}}

MUTE = {"r": 138, "g": 143, "b": 153, "a": 1}   # disclaimer label
DIM  = {"r": 150, "g": 156, "b": 168, "a": 1}   # disclaimer body

DISCLAIMER = ("This product is a general wellness and fitness device. It is not a medical device and is not "
    "intended to diagnose, treat, cure, or prevent any disease or health condition, including any heart condition. "
    "Its readings (including heart rate, heart rate variability, blood pressure, and blood oxygen) are estimates for "
    "general wellness purposes only, are not clinically validated, and should not be relied upon for any medical "
    "decision. Do not use this device to detect, monitor, or manage any medical condition. It is not a substitute for "
    "professional medical advice, examination, diagnosis, or treatment, or for medical-grade monitoring equipment. "
    "Always consult a qualified physician or healthcare provider with any questions about your health, before making "
    "health decisions, and if you experience symptoms such as chest pain, shortness of breath, or dizziness — seek "
    "emergency care immediately. Individual results may vary.")

SOCIAL_SVG = (
 '<div style="display:flex;gap:14px;align-items:center">'
 '<a href="#" style="display:inline-flex"><svg width="20" height="20" viewBox="0 0 24 24" fill="#1877f2"><path d="M24 12a12 12 0 1 0-13.9 11.9v-8.4H7v-3.5h3.1V9.4c0-3 1.8-4.7 4.5-4.7 1.3 0 2.7.2 2.7.2v3h-1.5c-1.5 0-2 .9-2 1.9v2.2h3.4l-.5 3.5h-2.9V24A12 12 0 0 0 24 12z"/></svg></a>'
 '<a href="#" style="display:inline-flex"><svg width="20" height="20" viewBox="0 0 24 24" fill="#ff0000"><path d="M23.5 6.2a3 3 0 0 0-2.1-2.1C19.5 3.6 12 3.6 12 3.6s-7.5 0-9.4.5A3 3 0 0 0 .5 6.2 31 31 0 0 0 0 12a31 31 0 0 0 .5 5.8 3 3 0 0 0 2.1 2.1c1.9.5 9.4.5 9.4.5s7.5 0 9.4-.5a3 3 0 0 0 2.1-2.1A31 31 0 0 0 24 12a31 31 0 0 0-.5-5.8zM9.6 15.6V8.4l6.3 3.6-6.3 3.6z"/></svg></a>'
 '<a href="#" style="display:inline-flex"><svg width="20" height="20" viewBox="0 0 24 24" fill="#e1306c"><path d="M12 2.2c3.2 0 3.6 0 4.9.1 1.2.1 1.8.3 2.2.4.6.2 1 .5 1.4.9.4.4.7.8.9 1.4.2.4.4 1 .4 2.2.1 1.3.1 1.7.1 4.9s0 3.6-.1 4.9c-.1 1.2-.3 1.8-.4 2.2-.2.6-.5 1-.9 1.4-.4.4-.8.7-1.4.9-.4.2-1 .4-2.2.4-1.3.1-1.7.1-4.9.1s-3.6 0-4.9-.1c-1.2-.1-1.8-.3-2.2-.4-.6-.2-1-.5-1.4-.9-.4-.4-.7-.8-.9-1.4-.2-.4-.4-1-.4-2.2C2.2 15.6 2.2 15.2 2.2 12s0-3.6.1-4.9c.1-1.2.3-1.8.4-2.2.2-.6.5-1 .9-1.4.4-.4.8-.7 1.4-.9.4-.2 1-.4 2.2-.4C8.4 2.2 8.8 2.2 12 2.2zm0 3.2A6.6 6.6 0 1 0 12 18.6 6.6 6.6 0 0 0 12 5.4zm0 10.9A4.3 4.3 0 1 1 12 7.7a4.3 4.3 0 0 1 0 8.6zm6.8-11.2a1.5 1.5 0 1 1-3 0 1.5 1.5 0 0 1 3 0z"/></svg></a>'
 '<a href="#" style="display:inline-flex"><svg width="18" height="18" viewBox="0 0 24 24" fill="#ffffff"><path d="M18.2 2h3.3l-7.2 8.3L23 22h-6.6l-5.2-6.8L5.3 22H2l7.7-8.8L1.3 2H8l4.7 6.2L18.2 2zm-1.2 18h1.8L7.1 3.9H5.2L17 20z"/></svg></a>'
 '<a href="#" style="display:inline-flex"><svg width="18" height="18" viewBox="0 0 24 24" fill="#ee802f"><path d="M4.4 4.4A15.6 15.6 0 0 1 20 20h-3A12.6 12.6 0 0 0 4.4 7.4V4.4zm0 5.6A10 10 0 0 1 14.4 20h-3A7 7 0 0 0 4.4 13V10zm2.1 6.9a2.1 2.1 0 1 1 0 4.2 2.1 2.1 0 0 1 0-4.2z"/></svg></a>'
 '</div>')

def footer():
    logo = container([image("logo", full=False, extra=[{"prop": "width", "value": "200px"}, {"prop": "height", "value": "50px"}])],
        [{"prop": "lfDisplay", "value": "flex"}, {"prop": "justifyContent", "value": "center"}, {"prop": "width", "value": "100%"}])
    disc_label = text("DISCLAIMER", size="11px", lh="16px", color=MUTE, weight="700", align="center")
    disc_body = text(DISCLAIMER, size="12px", lh="20px", color=DIM, align="center",
        mw="820px")
    divider = container([], [{"prop": "width", "value": "100%"}, {"prop": "height", "value": "1px"},
        {"prop": "backgroundColor", "value": {"r": 255, "g": 255, "b": 255, "a": 0.1}},
        {"prop": "margin", "value": {"top": "24px", "bottom": "18px"}}])
    left = text('© 2026 TechUnboxed.&nbsp;&nbsp;&nbsp;'
                '<a href="#" style="color:#9aa0ab;text-decoration:none">Terms</a>&nbsp;&nbsp;'
                '<a href="#" style="color:#9aa0ab;text-decoration:none">Privacy</a>&nbsp;&nbsp;'
                '<a href="#" style="color:#9aa0ab;text-decoration:none">Editorial standards</a>&nbsp;&nbsp;'
                '<a href="#" style="color:#9aa0ab;text-decoration:none">Affiliate policy</a>',
                size="12px", lh="18px", color=DIM, align="left", mw="100%")
    social = {"t": "HtmlElement", "id": nid(), "p": {"content": SOCIAL_SVG}, "styles": [{"prop": "flexShrink", "value": "0"}]}
    bottom = container([container([left], [{"prop": "flex", "value": "1"}, {"prop": "minWidth", "value": "0"}]), social],
        [{"prop": "lfDisplay", "value": "flex"}, {"prop": "flexDirection", "value": "row"},
         {"prop": "alignItems", "value": "center"}, {"prop": "justifyContent", "value": "space-between"},
         {"prop": "gap", "value": "20px"}, {"prop": "width", "value": "100%"}])
    col = container([logo, disc_label, disc_body], [{"prop": "lfDisplay", "value": "flex"},
        {"prop": "flexDirection", "value": "column"}, {"prop": "alignItems", "value": "center"},
        {"prop": "gap", "value": "14px"}, {"prop": "width", "value": "100%"}, {"prop": "maxWidth", "value": "900px"},
        {"prop": "margin", "value": {"left": "auto", "right": "auto"}}])
    outer = container([col, divider, bottom], [{"prop": "lfDisplay", "value": "flex"},
        {"prop": "flexDirection", "value": "column"}, {"prop": "width", "value": "100%"},
        {"prop": "maxWidth", "value": "900px"}, {"prop": "margin", "value": {"left": "auto", "right": "auto"}}])
    return {"t": "Section", "id": nid(),
        "styles": [{"prop": "backgroundColor", "value": NAVY},
                   {"prop": "padding", "value": {"top": "48px", "bottom": "28px"}}],
        "p": {"layout": "boxed", "dividerPosition": ["top"], "horizontalFlip": False,
              "embedded_video": {"src": "", "video_size": "stretch", "video_position": "center"},
              "children": [outer]}}

article = {"t": "Section", "id": nid(),
    "styles": [{"prop": "backgroundColor", "value": WHITE},
               {"prop": "padding", "value": {"top": "40px", "bottom": "56px"}}],
    "p": {"layout": "boxed", "dividerPosition": ["top"], "horizontalFlip": False,
          "embedded_video": {"src": "", "video_size": "stretch", "video_position": "center"},
          "children": [article_col]}}

body = {"id": nid(), "t": "Root", "version": 11,
        "styles": [{"prop": "pageWidth", "value": "960px"}, {"prop": "backgroundColor", "value": WHITE}],
        "p": {"children": [header, article, footer()]}}

# ---- write ----
r = sgql('mutation($id: ID!, $node: InputFunnel!){ updateFunnel(id:$id,node:$node){ id steps { uid slug title } } }',
    {"id": FUNNEL, "node": {"steps": [{"id": STEP, "slug": "hlth-page",
        "title": "HLTH advertorial", "type": "article_page", "settings": {},
        "visual": {"x": 100, "y": 100}, "body": body}]}})
n = sgql('query($q: String!){ funnels(first:1,query:$q){ edges { node { slug steps { uid slug } } } } }',
         {"q": f"id:{FUNNEL}"})["funnels"]["edges"][0]["node"]
print("WROTE:", json.dumps(r["updateFunnel"]["steps"], indent=2))
print("blocks in article column:", len(kids))
print("PREVIEW:", f"https://99commerce.myecomsite.net/{n['slug']}/{n['steps'][0]['slug']}?preview=true")
