#!/usr/bin/env python3
"""TEST 3 — smartwatch-review advertorial DESKTOP (Figma node 5:48) as native LF
blocks. Content + exact styles measured from figwright. Real images exported from
the design and hosted in LF. Writes to the from-scratch funnel test3-smartwatch.
Mobile (node 5:979) is a later pass."""
import sys, os, json, uuid
sys.path.insert(0, '.')
import lf_api

tok = open('.session_token').read().strip()
ACCT = open('.lf_account').read().strip()
HH = {"account-id": ACCT, "version": "1",
      "Origin": "https://app.lightfunnels.com", "Referer": "https://app.lightfunnels.com/"}
def sgql(q, v=None): return lf_api.gql(tok, q, v, extra_headers=HH)
def nid(): return str(uuid.uuid4())

ids = json.load(open("/tmp/test3_ids.json"))
FUNNEL, STEP = ids["funnel"], ids["step"]
IMG = json.load(open("/tmp/test3_img_map.json"))
# header/footer custom-HTML scripts copied verbatim from the live TUB page (fun_vGqQYxn4H2i.../pb/9)
CUSTOM_HTML = json.load(open(os.path.join(os.path.dirname(__file__), "test3_custom_html.json")))
# --- performance: preload the LCP hero (matches LF's responsive srcset/sizes so no double-download)
#     + reserve its box inline so it doesn't shift after paint (kills the 0.151 CLS from the hero).
_HERO = IMG["hero"]["src"]
_CDN  = "https://assets.lightfunnels.com/cdn-cgi/image/width=%d,quality=80,format=auto/"
_SRCSET = ", ".join("%s%s %dw" % (_CDN % w, _HERO, w) for w in (384, 750, 1080, 1920, 3840))
# Preload the Inter woff2 weights used above the fold (400 body/caption, 800 headings, 900 H1).
# Without this, Inter loads at ~3.3s under slow-4G and swaps over the fallback font, reflowing the
# H1 + captions and pushing the hero down +36px -> a single 0.15 CLS shift that fails Agentic Browsing.
# The source (techunboxed) page preloads Inter 400/700 for exactly this reason; matching that -> CLS ~0.
_FONT_PRELOAD = "".join(
    '<link rel="preload" as="font" type="font/woff2" crossorigin '
    'href="/cf-fonts/s/inter/5.2.8/latin/%d/normal.woff2">\n' % w for w in (400, 800, 900)
)
# Real Inter faces. LF only emits these when a block's font is the PLAIN "Inter" token (a picked font);
# once we author the stack "Inter, InterFallback, sans-serif" LF stops recognising it and drops the Inter
# @font-face rules entirely -> the page would render forever in the fallback (Arial), never real Inter.
# So we declare the Inter faces ourselves (font-display:swap), matching the live V3 page's weight set.
_INTER_WEIGHTS = (400, 500, 600, 700, 800, 900)
_INTER_FACE = "<style>" + "".join(
    "@font-face{font-family:Inter;font-style:normal;font-weight:%d;font-display:swap;"
    "src:url(/cf-fonts/s/inter/5.2.8/latin/%d/normal.woff2) format('woff2')}" % (w, w)
    for w in _INTER_WEIGHTS
) + "</style>\n"
# Metric-matched fallback: before Inter loads (or while it swaps in under slow networks), text is
# rendered with local Arial/Liberation Sans SIZED to match Inter's metrics (Next.js Inter/Arial overrides).
# Text then wraps identically and line-boxes are the same height, so the Inter swap causes ZERO reflow.
# Inter faces (swap) + this fallback + the stack below = real Inter rendering AND ~0 CLS (matches V3).
_FALLBACK_FACE = (
    "<style>@font-face{font-family:InterFallback;src:local('Arial'),local('Liberation Sans'),local('Helvetica Neue');"
    "ascent-override:90.44%;descent-override:22.52%;line-gap-override:0%;size-adjust:107.12%}</style>\n"
)
PERF = (
    '<link rel="preload" as="image" fetchpriority="high" '
    'imagesrcset="%s" imagesizes="(min-width: 1280px) 50vw, 100vw">\n'
    '<style>img[title="hero"]{height:371px!important;width:100%%!important;object-fit:cover;aspect-ratio:auto}'
    '@media (max-width:767px){img[title="hero"]{height:210px!important}}</style>\n' % _SRCSET
    + _INTER_FACE
    + _FALLBACK_FACE
    + _FONT_PRELOAD
)
# font stack used on every text block: real Inter, then the metric-matched fallback, then generic sans
FONT = "Inter, InterFallback, sans-serif"
# put fetchpriority=high on the hero LCP img and clear it off the logo (LF misapplies it to the logo)
PERF_FOOTER = (
    '<script>(function(){function f(){var h=document.querySelector(\'img[title="hero"]\');'
    'if(h){h.setAttribute("fetchpriority","high");h.setAttribute("loading","eager");}'
    'var lg=document.querySelector(\'img[title="logo"]\');if(lg)lg.removeAttribute("fetchpriority");}'
    'if(document.readyState!=="loading")f();else document.addEventListener("DOMContentLoaded",f);})();</script>\n'
)
CH_OUT = {"header": PERF + CUSTOM_HTML["header"], "footer": PERF_FOOTER + CUSTOM_HTML["footer"]}
PDP = "https://hlthtrack.com/products/wearable-hlth-band"
TP  = "https://www.trustpilot.com/review/hlthtrack.com"

# ---- colors ----
DARK  = {"r":17,"g":24,"b":39,"a":1}     # #111827
FEAT  = {"r":55,"g":65,"b":81,"a":1}     # #374151
BODY  = {"r":75,"g":85,"b":99,"a":1}     # #4b5563
GRAY6 = {"r":107,"g":114,"b":128,"a":1}  # #6b7280
RED   = {"r":230,"g":58,"b":69,"a":1}    # #e63a45
WHITE = {"r":255,"g":255,"b":255,"a":1}
SPON  = {"r":189,"g":189,"b":189,"a":1}
BORDER= {"r":229,"g":231,"b":235,"a":1}  # #e5e7eb
DIVID = {"r":238,"g":240,"b":242,"a":1}  # #eef0f2
BANNER= {"r":40,"g":40,"b":43,"a":1}     # #28282b
REVBG = {"r":246,"g":246,"b":247,"a":1}  # #f6f6f7
GREEN = {"r":0,"g":182,"b":122,"a":1}    # #00b67a
FOOT  = {"r":35,"g":35,"b":38,"a":1}     # #232326
MUTE  = {"r":138,"g":143,"b":153,"a":1}
DIM   = {"r":155,"g":155,"b":159,"a":1}  # #9b9b9f footer disclaimer
NAVY  = {"r":25,"g":30,"b":42,"a":1}      # #191e2a  H2 color (live)
SLATE = {"r":87,"g":99,"b":122,"a":1}     # #57637a  BEST OVERALL text (live)

# live page: bold uses plain <b> (inherits the paragraph color), HLTH Band mentions are blue links to the PDP
def B(t): return '<b>%s</b>' % t
def lk(t): return '<a href="%s" target="_blank" style="color:#0075ff;text-decoration:underline">%s</a>' % (PDP, t)

# m = dict of prop->value applied as a media:767 (<=767px, mobile) override
def _media(st, m):
    if m:
        for k,v in m.items(): st.append({"prop":k,"value":v,"media":767})

def title(content, fs, lh, weight="700", mt=0, color=DARK, align="left", ls=None, m=None):
    st=[{"prop":"fontFamily","value":FONT},{"prop":"color","value":color},
        {"prop":"fontSize","value":fs},{"prop":"lineHeight","value":lh},
        {"prop":"fontWeight","value":weight},{"prop":"textAlign","value":align},
        {"prop":"width","value":"100%"},{"prop":"maxWidth","value":"100%"}]
    if ls: st.append({"prop":"letterSpacing","value":ls})
    if mt: st.append({"prop":"margin","value":{"top":"%spx"%mt}})
    _media(st, m)
    return {"t":"Title","id":nid(),"p":{"size":"2","content":content,"widthOption":"fill"},"styles":st}

def text(content, size="17px", lh="29px", color=FEAT, weight="400", align="left", italic=False, mw="100%", m=None):
    st=[{"prop":"fontFamily","value":FONT},{"prop":"color","value":color},
        {"prop":"fontSize","value":size},{"prop":"lineHeight","value":lh},
        {"prop":"fontWeight","value":weight},{"prop":"textAlign","value":align},
        {"prop":"maxWidth","value":mw},{"prop":"width","value":"100%"}]
    if italic: st.append({"prop":"fontStyle","value":"italic"})
    _media(st, m)
    return {"t":"Text","id":nid(),"p":{"content":content},"styles":st}

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

def img_block(key, height=None, radius="10px", full=True, fit="cover", mh=None):
    m=IMG[key]
    st=[{"prop":"maxWidth","value":"100%"},{"prop":"borderRadius","value":radius},
        {"prop":"objectFit","value":fit},{"prop":"lfDisplay","value":"block"}]
    if full: st.append({"prop":"width","value":"100%"})
    if height: st.append({"prop":"height","value":height})
    if mh: st.append({"prop":"height","value":mh,"media":767})  # shorter mobile crop
    return {"t":"Image","id":nid(),"p":{"title":key,"src_id":m["src_id"],"src_uid":m["src_uid"],"src":m["src"]},"styles":st}

def inline_img(key, w, h, radius="0px"):
    m=IMG[key]
    return {"t":"Image","id":nid(),"p":{"title":key,"src_id":m["src_id"],"src_uid":m["src_uid"],"src":m["src"]},
        "styles":[{"prop":"width","value":w},{"prop":"height","value":h},{"prop":"objectFit","value":"contain"},
                  {"prop":"borderRadius","value":radius},{"prop":"lfDisplay","value":"block"},{"prop":"flexShrink","value":"0"}]}

def logo_img(w="166px", h="42px"):
    m=IMG["logo"]
    return {"t":"Image","id":nid(),"p":{"title":"logo","src":m["src"]},
        "styles":[{"prop":"width","value":w},{"prop":"height","value":h},{"prop":"maxWidth","value":"100%"},
                  {"prop":"objectFit","value":"contain"},{"prop":"lfDisplay","value":"block"}]}

STAR="★"
def tp_stars(rating, color, box=18):
    fs = 12 if box>=18 else 10
    half=round(rating*2)/2; full=int(half); hh=(half-full)==0.5
    out='<span style="display:inline-flex;gap:2px;vertical-align:middle">'
    tpl='<span style="display:inline-flex;align-items:center;justify-content:center;width:%dpx;height:%dpx;border-radius:3px;color:#fff;font-size:%dpx;background:%s">'+STAR+'</span>'
    for i in range(5):
        if i<full: bg=color
        elif i==full and hh: bg="linear-gradient(90deg,%s 50%%,#dcdce6 50%%)"%color
        else: bg="#dcdce6"
        out+=tpl%(box,box,fs,bg)
    return out+'</span>'

def button(label, href=PDP, bg=RED, fg=WHITE, full=False, size="14px", weight="600", radius="8px"):
    lab={"t":"Text","id":nid(),"p":{"content":label},
        "styles":[{"prop":"fontFamily","value":FONT},{"prop":"color","value":fg},
            {"prop":"fontSize","value":size},{"prop":"fontWeight","value":weight},
            {"prop":"lineHeight","value":"22px"},{"prop":"textAlign","value":"center"},
            {"prop":"whiteSpace","value":"nowrap"},{"prop":"maxWidth","value":"100%"}]}
    lw=container([lab],[{"prop":"lfDisplay","value":"flex"},{"prop":"alignItems","value":"center"},
        {"prop":"justifyContent","value":"center"},{"prop":"maxWidth","value":"100%"}])
    st=[{"prop":"backgroundColor","value":bg},{"prop":"borderRadius","value":radius},
        {"prop":"padding","value":{"top":"11px","bottom":"11px","left":"14px","right":"14px"}},
        {"prop":"lfDisplay","value":"flex"},{"prop":"alignItems","value":"center"},
        {"prop":"justifyContent","value":"center"}]
    if full: st.append({"prop":"width","value":"100%"})
    return {"t":"BlockLink","id":nid(),"p":{"destination":{"type":"static","value":href},
        "target":"_blank","widthOption":"auto","children":[lw]},"styles":st}

def feat(sign, txt):
    ic = ('<span style="color:#16a34a;font-weight:700">✓</span>' if sign
          else '<span style="color:#dc2626;font-weight:700">✗</span>')
    return text('%s&nbsp;<span style="color:#374151">%s</span>'%(ic, txt), size="13px", lh="20px", color=FEAT)

def caption(t="(Image credit: Marcus Pendleton / TechUnboxed)"):
    return text(t, size="14px", lh="22px", color=GRAY6, italic=True, m={"fontSize":"17px","lineHeight":"28px"})

# ---------------- CARD (desktop 3-column row) ----------------
def card(c, last=False):
    # contain (not cover) so portrait thumbs like the Fitbit aren't cut off at the top
    thumb=container([img_block(c["img"], height="76px", radius="8px", fit="contain")],
        [{"prop":"width","value":"76px"},{"prop":"flexShrink","value":"0"},{"prop":"borderRadius","value":"8px"},
         {"prop":"backgroundColor","value":WHITE},{"prop":"overflow","value":"hidden"}])
    mid=[]
    lblcol = "#57637a" if c.get("badgegreen") else "#4b5563"  # live: BEST OVERALL is #57637a (slate), not green
    lbl_html = c["label"]
    if lbl_html.startswith("★ "):  # gold star + slate text
        lbl_html = '<span style="color:#f4b400">★</span> <span style="color:%s">%s</span>'%(lblcol, lbl_html[2:])
    else:
        lbl_html = '<span style="color:%s">%s</span>'%(lblcol, lbl_html)
    mid.append(text('<span style="font-weight:800;font-size:13px;letter-spacing:.5px">%s</span>'%lbl_html, size="13px", lh="19px"))
    mid.append(text(c["name"], size="17px", lh="24px", color=DARK, weight="700"))
    mid.append(text(tp_stars(c["tp"], c["star"], 18)
        + '&nbsp;&nbsp;<span style="color:#111827;font-weight:700;font-size:13px;vertical-align:middle">%s</span>'%c["tp"],
        size="13px", lh="22px"))
    mid.append(text('<a href="%s" target="_blank" style="color:#5f5e5a;text-decoration:none;font-size:12px">See reviews on Trustpilot →</a>'%TP, size="12px", lh="18px", color={"r":95,"g":94,"b":90,"a":1}))
    feats=[feat(s,t) for (s,t) in c["features"]]
    mid.append(col(feats, gap="4px", styles=[{"prop":"margin","value":{"top":"6px"}}]))
    midcol=col(mid, gap="7px", styles=[{"prop":"flex","value":"1"},{"prop":"minWidth","value":"0"}])

    right=[text("OUR SCORE", size="11px", lh="16px", color=GRAY6, align="center"),
           text('<span style="font-size:30px;font-weight:800;color:#111827">%s</span><span style="font-size:14px;color:#6b7280">/10</span>'%c["score"], size="30px", lh="34px", align="center"),
           button(c["button"], href=c.get("href","#"), full=True)]
    price = c["price"] if not c.get("strike") else '%s <span style="text-decoration:line-through;color:#9ca3af;font-weight:400;font-size:16px">%s</span>'%(c["price"], c["strike"])
    right.append(text(price, size="16px", lh="24px", color=DARK, weight="700", align="center"))
    right.append(text(c["delivery"], size="12px", lh="16px", color=GRAY6, align="center"))
    rightcol=col(right, gap="8px", styles=[{"prop":"width","value":"150px"},{"prop":"flexShrink","value":"0"},
        {"prop":"alignItems","value":"center"},{"prop":"justifyContent","value":"flex-start"}])

    st=[{"prop":"backgroundColor","value":WHITE},
        {"prop":"padding","value":{"top":"20px","bottom":"20px","left":"20px","right":"20px"}},
        {"prop":"lfDisplay","value":"none","media":767}]  # desktop 3-col row hidden on phones (dual-DOM)
    if not last:
        st+=[{"prop":"borderStyle","value":"solid"},{"prop":"borderColor","value":DIVID},{"prop":"borderWidth","value":"0px 0px 1px 0px"}]
    else:
        st.append({"prop":"borderRadius","value":"0px 0px 12px 12px"})
    return rowf([thumb, midcol, rightcol], styles=st, gap="16px", align="flex-start")

# ---------------- MOBILE CARD (single centered column, matches node 5:979) ----------------
# order: badge(card1 only) -> name 24px -> OUR SCORE+score -> image(centered) ->
#        Trustpilot logo+stars -> features(left) -> full-width button -> price -> delivery
def mcard(c, last=False):
    inner=[]
    if c["label"].startswith("★ "):  # only card 1 carries a badge on mobile
        lblcol = "#57637a" if c.get("badgegreen") else "#4b5563"
        inner.append(text('<span style="color:#f4b400">★</span> <span style="color:%s;font-weight:800;font-size:13px;letter-spacing:.5px">%s</span>'%(lblcol, c["label"][2:]),
                          size="13px", lh="20px", align="center"))
    inner.append(text(c["name"], size="24px", lh="30px", color=DARK, weight="700", align="center"))
    inner.append(text('<span style="color:#6b7280;font-size:11px;letter-spacing:.5px;vertical-align:middle">OUR SCORE</span>&nbsp;&nbsp;'
                      '<span style="font-size:30px;font-weight:800;color:#111827;vertical-align:middle">%s</span>'
                      '<span style="font-size:14px;color:#6b7280">/10</span>'%c["score"], size="30px", lh="34px", align="center"))
    # centered ~square thumbnail (contain + white bg so portrait shots like Fitbit aren't cropped)
    inner.append(container([img_block(c["img"], height="188px", radius="8px", fit="contain")],
        [{"prop":"width","value":"200px"},{"prop":"maxWidth","value":"100%"},{"prop":"backgroundColor","value":WHITE},
         {"prop":"borderRadius","value":"8px"},{"prop":"overflow","value":"hidden"},{"prop":"margin","value":{"left":"auto","right":"auto"}}]))
    # Trustpilot logo + stars + rating (centered)
    inner.append(col([
        container([inline_img("tp_logo","116px","28px")],[{"prop":"lfDisplay","value":"flex"},{"prop":"justifyContent","value":"center"},{"prop":"width","value":"100%"}]),
        text(tp_stars(c["tp"], c["star"], 18)+'&nbsp;&nbsp;<span style="color:#111827;font-weight:700;font-size:13px;vertical-align:middle">%s</span>'%c["tp"], size="13px", lh="22px", align="center"),
    ], gap="6px", styles=[{"prop":"alignItems","value":"center"}]))
    # features (left-aligned)
    inner.append(col([feat(s,t) for (s,t) in c["features"]], gap="5px", styles=[{"prop":"width","value":"100%"},{"prop":"margin","value":{"top":"4px"}}]))
    # full-width button
    inner.append(button(c["button"], href=c.get("href","#"), full=True, size="14px", weight="600", radius="6px"))
    # price + strike, centered
    price = c["price"] if not c.get("strike") else '%s <span style="text-decoration:line-through;color:#9ca3af;font-weight:400;font-size:16px">%s</span>'%(c["price"], c["strike"])
    inner.append(text(price, size="16px", lh="24px", color=DARK, weight="700", align="center"))
    inner.append(text(c["delivery"], size="12px", lh="16px", color=GRAY6, align="center"))

    st=[{"prop":"lfDisplay","value":"none"},{"prop":"lfDisplay","value":"flex","media":767},  # hidden on desktop, shown on phones
        {"prop":"flexDirection","value":"column"},{"prop":"gap","value":"10px"},
        {"prop":"alignItems","value":"center"},{"prop":"width","value":"100%"},
        {"prop":"backgroundColor","value":WHITE},
        {"prop":"padding","value":{"top":"18px","bottom":"18px","left":"16px","right":"16px"}}]
    if not last:
        st+=[{"prop":"borderStyle","value":"solid"},{"prop":"borderColor","value":DIVID},{"prop":"borderWidth","value":"0px 0px 1px 0px"}]
    else:
        st.append({"prop":"borderRadius","value":"0px 0px 12px 12px"})
    return {"t":"Container","id":nid(),"styles":st,"p":{"children":inner}}

# ---------------- DATA ----------------
CARDS=[
 {"img":"prod1","star":"#00b67a","badgegreen":True,"label":"★ BEST OVERALL","name":"1. HLTH Band 1.0","tp":4.5,"score":"9.9","button":"View at HLTH","href":PDP,
  "price":"£79","strike":"£158","delivery":"Delivery 3-5 business days","features":[
   (1,"No subscription or locked features"),(1,"Confirmed 30-day battery life"),
   (1,"Tracks blood pressure, RHR, HRV &amp; SpO2"),(1,"Full sleep stages (deep, REM, light)"),
   (1,"Multi-wavelength PPG"),(1,"Adaptive Power Management"),(1,"Lightweight 18g, screen-free design"),
   (1,"Water resistant (1ATM)"),(0,"New Company – Frequently sold out"),(0,"No built-in GPS (uses your phone)")]},
 {"img":"prod2","star":"#ffce00","label":"The subscription one","name":"2. Whoop 5.0 Peak","tp":3.2,"score":"9.0","button":"VISIT AMAZON","href":"#",
  "price":"£229/yr","delivery":"2-3 Day Prime Delivery","features":[
   (1,"Excellent recovery &amp; strain analytics"),(1,"Comfortable screen-free band"),
   (1,"Tracks HRV, sleep &amp; SpO2"),(1,"Multi-wavelength PPG"),(0,"£229 per year, every single year"),
   (0,"Device stops working if you cancel"),(0,"Blood pressure locked to £359 tier"),
   (0,"Widespread 5.0 heart-rate complaints")]},
 {"img":"prod3","star":"#ff3722","label":"The smartwatch one","name":"3. Apple Watch SE 3","tp":1.8,"score":"7.9","button":"VISIT AMAZON","href":"#",
  "price":"£219","delivery":"7-12 Day Shipping","features":[
   (1,"Best-in-class app &amp; smart features"),(1,"Great communication options"),
   (1,"Accurate heart rate &amp; built-in GPS"),(1,"Sleep apnea alerts &amp; wrist temperature"),
   (0,"No ECG, no blood oxygen, no BP at all"),(0,"Needs an iPhone to work"),
   (0,"Nightly charging breaks sleep tracking"),(0,"We found ourselves checking it constantly")]},
 {"img":"prod4","star":"#ff3722","label":"The sports one","name":"4. Garmin Vivoactive 6","tp":1.5,"score":"7.5","button":"VISIT AMAZON","href":"#",
  "price":"£269","delivery":"2-3 Day Prime Delivery","features":[
   (1,"Reliable GPS &amp; sports modes"),(1,"Accurate fitness tracking"),(1,"7-day battery"),
   (1,"Free garmin connect app"),(0,"£250 one-time investment"),(0,"Clunky app interface"),
   (0,"No blood pressure monitoring"),(0,"No onboard ECG or altimeter"),
   (0,"No speaker/mic for calls"),(0,"Bulky and uncomfortable for sleep")]},
 {"img":"prod5","star":"#ff3722","label":"The mainstream one","name":"5. Fitbit Charge 6","tp":1.6,"score":"5.9","button":"VISIT AMAZON","href":"#",
  "price":"£79.99","strike":"£139.99","delivery":"2-3 Day Prime Delivery","features":[
   (1,"Onboard ECG &amp; SpO2"),(1,"Compact, lightweight band"),(1,"Built-in GPS + swimproof"),
   (0,"Privacy concerns after google acquisition"),(0,"Sleep score &amp; readiness behind £9.99/mo Premium"),
   (0,"Real battery only 2–5 days"),(0,"No blood pressure monitoring"),(0,"GPS was hit or miss"),
   (0,"Data loss in google migration")]},
]

SECTIONS=[
 {"h":"Why We Picked The HLTH Band As The Winner?","img":"sec1","paras":[
  "The " + lk("HLTH Band") + " stands out for its simplicity and serious health credentials. It consistently matched devices costing " + B("three to five times more") + ", and its Multi-Wavelength PPG sensor, a step up from the single-wavelength sensors in most budget bands, delivers continuous readings of blood pressure, heart rate, HRV, and resting heart rate around the clock.",
  "It's one of the only bands on the market offering " + B("blood pressure readings without a subscription,") + " the kind of long-term picture you can actually take to your doctor, free, every single day. And it tracks full sleep stages across a " + B("confirmed 30-day battery life,") + " 30 nights of uninterrupted sleep data that the Apple Watch, Fitbit, and Garmin simply can't match with their nightly charging.",
  "Normally, this level of monitoring comes locked behind a £229-per-year membership or a smartwatch that dies every night. The " + lk("HLTH Band") + " is the exception. At " + B("£79,") + " it's the most capable screen-free health tracker we tested, serious health data in a device light enough to forget you're wearing."]},
 {"h":"We Expected It To Crack Under Testing. It Didn't.","img":"sec2","paras":[
  "When we unboxed the " + lk("HLTH Band") + ", the first thing we noticed was the weight. At " + B("18 grams,") + " it sits on your wrist like a rubber bracelet. After a week switching between the Apple Watch and Garmin, putting it back on felt like taking a weight off.",
  "But comfort means nothing without accuracy, so we tested the claim that matters most: blood pressure. Every cardiologist we consulted agreed that a single spot reading tells you almost nothing, because blood pressure moves constantly with stress, movement, food, and sleep. " + B("Only an extended trend provides a real signal.") + " So we ran a comparison against a medical-grade cuff under resting conditions, and the " + lk("HLTH Band") + " came within the recommended ±10 mmHg, consistently, across multiple sessions.",
  "That matters because a cuff catches one moment. The " + lk("HLTH Band") + " reads all day, while you work, sleep, and recover, and that continuous picture shows you patterns a single reading never can. No other device in our test offered continuous blood pressure monitoring at any price, except Whoop, locked behind their £349-per-year tier."]},
 {"h":"I Didn't Expect To Still Be Wearing It 30 Days Later","img":"sec3","paras":[
  "I'll be honest. When we started this test, I assumed the " + lk("HLTH Band") + " would be the first device I put back in the box. A new company, a £79 price tag, no screen, no brand name anyone would recognise at a dinner party. Every instinct said this underdog would quietly disappoint.",
  "But " + B("thirty days later it's still on my wrist.") + " I wore it through back-to-back work weeks, flights, gym sessions, and holidays full of bad sleep, " + B("without it ever needing a charge.") + " Sleep stages explained why some mornings felt broken despite eight hours in bed, blood pressure trends helped explain my daily brain fog, and trustworthy heart rate averages let me finally spot the changes I needed to make.",
  "What I learned is simple. The device that actually helps your health isn't always the most expensive one. " + B("It's the one you'll keep wearing long enough to get the data.") + " And as a 47-year-old trying to understand whether my body is aging well or aging fast, this is the first tracker that actually helped."]},
 {"h":"The App Actually Won Me Over","img":"sec4","paras":[
  "HLTH took a different route than most of the big brands here. Instead of making the app look as cool and complicated as possible, the app that powers the " + lk("HLTH Band") + " is built to be " + B("extremely easy to read and understand.") + " Open it and you get one clean daily view. Heart rate, blood pressure trend, sleep, and stress, all on one screen, in plain English. Tap any metric and you're there. No wall of graphs, no digging through menus.",
  "That sounds like a small thing until you've lived with the alternatives. The real value shows up after a few weeks, when the app turns months of readings into " + B("simple trend lines anyone can follow,") + " so you can see how your sleep, stress, and blood pressure move together over time. You don't need to be an athlete or a data nerd to know exactly where you stand."]},
 {"h":"The Bicep Strap Is A Great Addition","img":"sec5","paras":[
  "Here's a simple rule about wrist wearables that the big brands don't talk about much: " + B("the less the sensor moves, the more accurate your readings are.") + " Your wrist is the busiest joint you have. It twists, flexes, and swings with every step, and all that movement is noise the sensor has to fight through.",
  "Your bicep barely moves by comparison. That's what makes the bicep strap such a smart addition to the " + lk("HLTH Band") + ". Clip the same band to your upper arm for a run or a workout and it sits steady against the muscle, which means " + B("steadier readings when your body is working hardest.") + " We wore it on the wrist day to day and switched to the bicep for training, and it's the setup we'd recommend."]},
]

REVIEWS=[
 ("Matches my pricier band","Sleep and HRV data line up with my old band that cost three times as much. Battery really does last weeks.","Verified buyer"),
 ("Better than anything else","The HLTH band is fantastic. Simple pairing and so many things it can do, better than anything on the market.","Matt"),
 ("No monthly fees","Does everything the big brands do without the price tag or the monthly fees.","Verified buyer"),
 ("I forget it's on","So light I forget it's on. Finally a tracker I actually keep wearing.","Verified buyer"),
 ("Easy setup","Set up in minutes and the app is clean and easy to read.","Verified buyer"),
 ("Really helpful team","Had a quick question and support replied within the hour. Really helpful team.","J. Porras, 5 days ago"),
 ("Arrived next day","Ordered in the evening and it arrived the next day. Packaging was lovely too.","Verified buyer"),
 ("Everyday essential","A practical tracker for everyday use. Monitors heart rate, sleep, stress, HRV and blood oxygen. Highly recommend.","Joanna"),
 ("Everything included","Love that everything is included. Simple, discreet and comfortable to wear day and night.","Verified buyer"),
]

COST_ROWS=[
 ["Whoop 5.0 Peak","£229","£229","£458","Mandatory"],
 ["Apple Watch SE 3","£219","£0","£219","No"],
 ["Fitbit Charge 6","£260","£120","£380","Optional"],
 ["Garmin Vivoactive 6","£250","£0","£250","No"],
 ["HLTH Band","£79","£0","£79","No"],
]

# ---------------- ASSEMBLE ----------------
def para(t): return text(t, size="17px", lh="29px", color=FEAT)

kids=[]
# breadcrumb
kids.append(text('<span style="color:#111827">Home</span> <span style="color:#9ca3af">&gt;</span> <span style="color:#111827">Wearables</span> <span style="color:#9ca3af">&gt;</span> <span style="color:#e63a45">Best Fitness Trackers of 2026</span>', size="14px", lh="22px", color=DARK, m={"fontSize":"15px"}))
# H1 + sub-headline  (live mobile: H1 24/30 wt900 ; sub 20/27)
kids.append(title("We Spent £1,581 Testing The Top 5 Fitness Trackers of 2026. The £79 Outsider Won.","40px","46px",weight="800",ls="-0.5px",m={"fontSize":"24px","lineHeight":"30px","fontWeight":"900"}))
kids.append(text("The newcomer tracks what a £399 watch can't, costs £79 on sale, and runs a month on one charge.", size="28px", lh="34px", color=DARK, weight="700", m={"fontSize":"20px","lineHeight":"27px"}))
# meta row
META=('<span style="display:inline-flex;align-items:center;gap:10px;flex-wrap:wrap">'
  '<span style="display:inline-flex;align-items:center;background:#1d6fe0;color:#fff;font-weight:700;font-size:13px;letter-spacing:.5px;padding:6px 12px;border-radius:6px">Buying Guides</span>'
  '<span style="display:inline-flex;align-items:center;gap:5px;background:#e8f462;color:#000;font-weight:700;font-size:13px;letter-spacing:.5px;padding:6px 12px;border-radius:6px">'
  '<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="#000" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="22 7 13.5 15.5 8.5 10.5 2 17"/><polyline points="16 7 22 7 22 13"/></svg>Trending</span>'
  '<span style="color:#1e1e1e;font-size:15px">By </span><a href="#" style="color:#0085ff;font-size:15px;text-decoration:underline">Marcus Pendleton</a>'
  '</span>')
kids.append(text(META, size="13px", lh="26px"))
kids.append(text("Last updated July 18, 2026", size="15px", lh="24px", color={"r":120,"g":120,"b":120,"a":1}))
# hero
kids.append(img_block("hero", height="371px", mh="210px"))
kids.append(caption())
# intro hooks
for q in ["Looking to accurately track and improve your health?",
          "Want a reliable fitness tracker that follows your blood pressure, heart rate, and sleep without monthly subscriptions?",
          "Searching for a simple, comfortable tracker built for everyday people?"]:
    kids.append(text(B(q), size="17px", lh="27px", color=DARK))
kids.append(para("If you nodded yes to any of these, you've come to the right place. We spent £1,581 to properly test the most popular trackers against the new tracker that's going viral in the UK."))
kids.append(para(B("Ever since the HLTH Band launched in April,") + " it's been the tracker readers keep asking us about. And I test wearables for a living, so I've learned the hard way that hype and quality are rarely the same thing."))
kids.append(para("Our testing revealed what many of us already know. " + B("Most expensive is not always the best.") + " The newcomer won on the things that matter: data accuracy, battery life, and total cost of ownership, without locking a single feature behind monthly fees."))
kids.append(para('<b style="color:#111827">How we tested:</b> we wore every band day and night for a full month. We compared readings side by side across the same days, logged sleep against how we actually felt each morning, ran every battery flat, added up the true two-year cost of each device including subscriptions, and lived with each one through work, gym sessions, and travel.'))
kids.append(text('<b>The winner: The %s</b> The £79 newcomer beat every big name in this test. Here\'s how all five stack up, and why.'%lk("HLTH Band."), size="17px", lh="29px", color=FEAT))

# best-picks ranked box
banner=container([text("The best picks reviewed by Tech Unboxed", size="16px", lh="26px", color=WHITE, weight="600", m={"fontSize":"22px","lineHeight":"29px","fontWeight":"800"})],
    [{"prop":"backgroundColor","value":BANNER},{"prop":"borderRadius","value":"12px 12px 0px 0px"},
     {"prop":"padding","value":{"top":"15px","bottom":"15px","left":"20px","right":"20px"}},{"prop":"width","value":"100%"}])
# dual-DOM: desktop 3-col card (hidden @767) + mobile centered card (shown @767) per product
table_rows=[banner]
for i,c in enumerate(CARDS):
    _last=(i==len(CARDS)-1)
    table_rows.append(card(c, last=_last))
    table_rows.append(mcard(c, last=_last))
kids.append(container(table_rows,[{"prop":"width","value":"100%"},{"prop":"borderStyle","value":"solid"},
    {"prop":"borderColor","value":BORDER},{"prop":"borderWidth","value":"1px"},
    {"prop":"borderRadius","value":"12px"},{"prop":"margin","value":{"top":"16px"}}]))

# editorial sections
H2M={}   # live mobile keeps 32px section headings (no shrink) — empty dict = no media override
for sec in SECTIONS:
    kids.append(title(sec["h"],"32px","37px",mt=24,weight="800",color=NAVY,m=H2M))
    kids.append(img_block(sec["img"], height="371px", mh="230px"))
    kids.append(caption())
    for p in sec["paras"]:
        kids.append(para(p))

# cost section
kids.append(title("How Much Is This Actually Going To Cost You?","32px","37px",mt=24,weight="800",color=NAVY,m=H2M))
# live page shows an autoplay/loop/muted product video here (Shopify CDN mp4), not a static image
COST_VIDEO="https://cdn.shopify.com/videos/c/o/v/e8121868d6304a34bdb191a9b1e36fac.mp4"
# lazy-load the 3.2MB video: poster shows immediately, mp4 only downloads when scrolled near (saves initial bandwidth)
kids.append({"t":"HtmlElement","id":nid(),"p":{"content":
    '<video class="lf-lazy-cost-video" data-lazysrc="%s" autoplay loop muted playsinline preload="none" '
    'style="width:100%%;border-radius:10px;display:block" poster="%s"></video>'
    '<script>(function(){function init(){var v=document.querySelector(".lf-lazy-cost-video");'
    'if(!v||!v.dataset.lazysrc)return;var load=function(){if(v.getAttribute("src"))return;'
    'v.src=v.dataset.lazysrc;v.load();var p=v.play();if(p&&p.catch)p.catch(function(){});};'
    'if("IntersectionObserver"in window){var io=new IntersectionObserver(function(es){'
    'es.forEach(function(e){if(e.isIntersecting){load();io.disconnect();}});},{rootMargin:"400px"});io.observe(v);}else{load();}}'
    'if(document.readyState!=="loading")init();else document.addEventListener("DOMContentLoaded",init);})();</script>'
    %(COST_VIDEO, IMG["sec6"]["src"])},
    "styles":[{"prop":"width","value":"100%"}]})
kids.append(caption("(Video credit: Marcus Pendleton / TechUnboxed)"))
kids.append(para("That depends entirely on which device you choose, and it's worth doing the maths."))
HDR={"r":107,"g":114,"b":128,"a":1}; HLTHTBL={"r":243,"g":250,"b":246,"a":1}
COLW=["2.5","1","1","1.7","1.8"]
# mobile column proportions (Figma: Device 83 / Year 50 / Year 50 / Total 51 / Sub 102)
_MFLEX={"2.5":"1.7","1":"1","1.7":"1","1.8":"2"}
def cell(t, w, bold=False, color=FEAT, align="center"):
    return container([text(t, size="15px", lh="21px", color=color, weight="700" if bold else "400", align=align, m={"fontSize":"14px","lineHeight":"19px"})],
        [{"prop":"flex","value":w},{"prop":"flex","value":_MFLEX.get(w,w),"media":767},
         {"prop":"padding","value":{"top":"14px","bottom":"14px","left":"12px","right":"10px"}},
         {"prop":"padding","value":{"top":"10px","bottom":"10px","left":"6px","right":"5px"},"media":767},
         {"prop":"minWidth","value":"0"}])
tbl=[rowf([cell("Device",COLW[0],bold=True,color=HDR,align="left"),cell("Year 1",COLW[1],bold=True,color=HDR),
          cell("Year 2",COLW[2],bold=True,color=HDR),cell("2-Year Total",COLW[3],bold=True,color=HDR),
          cell("Subscription",COLW[4],bold=True,color=HDR)], gap="0px", align="center",
          styles=[{"prop":"borderStyle","value":"solid"},{"prop":"borderColor","value":BORDER},{"prop":"borderWidth","value":"0px 0px 1px 0px"}])]
for r_ in COST_ROWS:
    hl = r_[0]=="HLTH Band"
    rst=[{"prop":"width","value":"100%"}]
    if hl: rst+=[{"prop":"backgroundColor","value":HLTHTBL},{"prop":"borderRadius","value":"0px 0px 10px 10px"}]
    else: rst+=[{"prop":"borderStyle","value":"solid"},{"prop":"borderColor","value":DIVID},{"prop":"borderWidth","value":"0px 0px 1px 0px"}]
    cc = DARK if hl else FEAT
    tbl.append(rowf([cell(r_[0],COLW[0],bold=hl,color=cc,align="left"),cell(r_[1],COLW[1],bold=hl,color=cc),
                    cell(r_[2],COLW[2],bold=hl,color=cc),cell(r_[3],COLW[3],bold=hl,color=cc),
                    cell(r_[4],COLW[4],bold=hl,color=cc)], gap="0px", align="center", styles=rst))
# live table has NO outer border/box — just horizontal row dividers
kids.append(container(tbl,[{"prop":"width","value":"100%"},{"prop":"margin","value":{"top":"8px"}}]))

# update box (red-bordered) — internal "For Sidra" note intentionally omitted
kids.append(container([text('<b style="color:#e63a45">Update:</b> The £79 price is a launch sale price, down from £158. We last checked at the beginning of July 2026 and the discount was still live. HLTH makes the band in small batches and earlier batches have sold out, so click below to check current availability before this one goes.', size="16px", lh="26px", color={"r":0,"g":0,"b":0,"a":1})],
    [{"prop":"backgroundColor","value":{"r":253,"g":236,"b":236,"a":1}},{"prop":"borderStyle","value":"solid"},
     {"prop":"borderColor","value":RED},{"prop":"borderWidth","value":"1px"},
     {"prop":"borderRadius","value":"10px"},{"prop":"padding","value":{"top":"14px","bottom":"14px","left":"16px","right":"16px"}},
     {"prop":"width","value":"100%"},{"prop":"margin","value":{"top":"10px"}}]))
kids.append(para("While it's the least expensive device we tested, nothing about its performance felt cheap. The data it delivered over 30 days made every device above it feel like an overcomplicated answer to a simple question. And every " + lk("HLTH Band") + " comes with a " + B("30-day money-back guarantee,") + " so there's no risk in finding out for yourself."))
kids.append(container([button("CHECK DISCOUNT AVAILABILITY →", href=PDP, full=True, size="15px", weight="700")],
    [{"prop":"width","value":"100%"},{"prop":"padding","value":{"top":"6px","bottom":"6px"}}]))
kids.append(text('<a href="%s" target="_blank" style="color:#1868dd;font-weight:600;text-decoration:underline">Click here to lock in the UK-exclusive 50%% OFF sale price before this batch sells out →</a>'%PDP, size="17px", lh="27px", align="center"))

# reviews
kids.append(title("What HLTH Band customers are saying?","32px","37px",mt=24,weight="800",color=NAVY,m=H2M))
kids.append(para("Before you take our word for it, here's one of the best ways to check whether any product is actually good: its Trustpilot page. Reviews there are very hard for a company to game. Trustpilot runs automatic fraud detection, verifies reviewers, flags suspicious patterns, and openly penalises firms caught manipulating their scores. A rating built from real buyers is a signal no ad campaign can buy."))
kids.append(text('Rated <b style="color:#191919">4.5</b> / 5 based on <b style="color:#191919">+80</b> reviews. Showing 5 star reviews.', size="14px", lh="22px", color={"r":110,"g":110,"b":120,"a":1}, m={"fontSize":"17px","lineHeight":"28px"}))
rev_cards=[]
for (ti,bo,au) in REVIEWS:
    rc=col([
        rowf([text(tp_stars(5,"#00b67a",16), size="13px", lh="16px"),
             text('<span style="color:#6b7280">✓ Verified</span>', size="12px", lh="16px", align="right")],
            gap="8px", justify="space-between", align="center"),
        text(ti, size="14px", lh="20px", color={"r":25,"g":25,"b":25,"a":1}, weight="800"),
        text(bo, size="17px", lh="25px", color=BODY),
        text(au, size="12px", lh="18px", color=DARK, weight="600"),
    ], gap="8px", styles=[{"prop":"backgroundColor","value":REVBG},{"prop":"borderRadius","value":"8px"},
        {"prop":"padding","value":{"top":"14px","bottom":"14px","left":"16px","right":"16px"}},
        {"prop":"width","value":"31%"},{"prop":"minWidth","value":"200px"},
        {"prop":"width","value":"100%","media":767}])   # single column on mobile
    rev_cards.append(rc)
kids.append(rowf(rev_cards, gap="12px", wrap=True, align="stretch"))
kids.append(para("Read through enough of them and the same things keep coming up. People love how light the band is, that the battery genuinely lasts weeks instead of days, and that their heart rate, blood pressure trend, and sleep all live in one simple app. The other theme is money: no subscription, no locked features, nothing to pay after the £79. Several buyers mention it matches wearables that cost them three times as much."))
kids.append(text('<a href="%s" target="_blank" style="color:#00b67a;font-weight:600;text-decoration:none">See more reviews at trustpilot →</a>'%TP, size="14px", lh="22px", align="center"))

# launch-sale promo (GIF left, copy right, black border)
badge=text('<span style="background:#e63a45;color:#fff;padding:5px 14px;border-radius:7px;font-size:16px;font-weight:800;letter-spacing:.3px">LAUNCH SALE</span>', size="16px", lh="24px")
promo_left=container([img_block("launch", height="300px", radius="12px", mh="320px")],
    [{"prop":"width","value":"44%"},{"prop":"minWidth","value":"260px"},{"prop":"flexShrink","value":"0"},
     {"prop":"width","value":"100%","media":767},{"prop":"minWidth","value":"0","media":767},
     {"prop":"backgroundColor","value":{"r":241,"g":247,"b":240,"a":1}},{"prop":"borderRadius","value":"12px"}])
promo_content=col([
    rowf([text('Rated Excellent (4.5) on', size="12px", lh="18px", color=DARK), inline_img("tp_logo","70px","17px")], gap="6px", align="center"),
    text('<span style="color:#7b0323">UP TO 50% OFF</span> <span style="color:#253319">FOR A LIMITED TIME ONLY!</span>', size="25px", lh="30px", color=DARK, weight="800", align="center"),
    text("With 30 day risk-free trial, you have nothing to lose.", size="13px", lh="18px", color=DARK, align="center"),
    container([button("TRY IT RISK-FREE →", href=PDP, full=False, size="15px", weight="800", radius="10px")],
        [{"prop":"lfDisplay","value":"flex"},{"prop":"justifyContent","value":"center"},{"prop":"width","value":"100%"}]),
    text('<span style="background:rgba(225,198,203,.5);border-radius:4px;padding:3px 10px;color:#111827;font-size:11px"><span style="color:#e63946;font-weight:700">Sell-Out Risk: High</span> &nbsp;|&nbsp; <span style="font-weight:600">FREE shipping</span></span>', size="11px", lh="18px", align="center"),
    text("Try it today with a 30-Day Money Back Guarantee!", size="11px", lh="16px", color={"r":87,"g":99,"b":122,"a":1}, align="center"),
], gap="12px", styles=[{"prop":"flex","value":"1"},{"prop":"minWidth","value":"0"},{"prop":"justifyContent","value":"center"}])
promo=col([badge, rowf([promo_left, promo_content], gap="20px", align="center", wrap=True)],
    gap="14px", styles=[{"prop":"backgroundColor","value":WHITE},{"prop":"borderStyle","value":"solid"},
    {"prop":"borderColor","value":{"r":0,"g":0,"b":0,"a":1}},{"prop":"borderWidth","value":"2px"},{"prop":"borderRadius","value":"20px"},
    {"prop":"padding","value":{"top":"22px","bottom":"22px","left":"22px","right":"22px"}},{"prop":"margin","value":{"top":"16px"}}])
kids.append(promo)

article_col = container(kids,
    [{"prop":"maxWidth","value":"664px"},{"prop":"width","value":"100%"},
     {"prop":"margin","value":{"left":"auto","right":"auto"}},
     {"prop":"padding","value":{"left":"16px","right":"16px"},"media":767},  # mobile page gutter
     {"prop":"lfDisplay","value":"flex"},{"prop":"flexDirection","value":"column"},{"prop":"gap","value":"16px"}])

# header (full-bleed dark bar)
header={"t":"Section","id":nid(),
    "styles":[{"prop":"backgroundColor","value":{"r":28,"g":28,"b":30,"a":1}},{"prop":"padding","value":{"top":"8px","bottom":"18px"}}],
    "p":{"layout":"","dividerPosition":["top"],"horizontalFlip":False,
         "embedded_video":{"src":"","video_size":"stretch","video_position":"center"},
         "children":[col([
             text("SPONSORED ARTICLE", size="10px", lh="16px", color=SPON, align="center", m={"fontSize":"13px"}),
             container([logo_img()],[{"prop":"lfDisplay","value":"flex"},{"prop":"justifyContent","value":"center"},
                 {"prop":"width","value":"100%"},{"prop":"margin","value":{"top":"10px"}}]),
         ], gap="0px", styles=[{"prop":"alignItems","value":"center"},{"prop":"letterSpacing","value":"1.5px"}])]}}

DISCLAIMER=("This product is a general wellness and fitness device. It is not a medical device and is not intended to "
 "diagnose, treat, cure, or prevent any disease or health condition, including any heart condition. Its readings "
 "(including heart rate, heart rate variability, blood pressure, and blood oxygen) are estimates for general wellness "
 "purposes only, are not clinically validated, and should not be relied upon for any medical decision. Do not use this "
 "device to detect, monitor, or manage any medical condition. It is not a substitute for professional medical advice, "
 "examination, diagnosis, or treatment, or for medical-grade monitoring equipment. Always consult a qualified physician "
 "or healthcare provider with any questions about your health, before making health decisions, and if you experience "
 "symptoms such as chest pain, shortness of breath, or dizziness — seek emergency care immediately. Individual results may vary.")
def footer():
    logo=container([logo_img()],[{"prop":"lfDisplay","value":"flex"},{"prop":"justifyContent","value":"center"},{"prop":"width","value":"100%"}])
    lbl=text("DISCLAIMER", size="12px", lh="16px", color=WHITE, weight="700", align="center")
    body=text(DISCLAIMER, size="12.5px", lh="20px", color=DIM, align="center", mw="820px")
    div=container([],[{"prop":"width","value":"100%"},{"prop":"height","value":"1px"},
        {"prop":"backgroundColor","value":{"r":255,"g":255,"b":255,"a":0.15}},{"prop":"margin","value":{"top":"24px","bottom":"18px"}}])
    left=text('<span style="color:#fff;font-weight:600">© 2026 TechUnboxed.</span>&nbsp;&nbsp;&nbsp;<a href="#" style="color:#bdbdbd;text-decoration:none">Terms</a>&nbsp;&nbsp;'
              '<a href="#" style="color:#bdbdbd;text-decoration:none">Privacy</a>&nbsp;&nbsp;'
              '<a href="#" style="color:#bdbdbd;text-decoration:none">Editorial standards</a>&nbsp;&nbsp;'
              '<a href="#" style="color:#bdbdbd;text-decoration:none">Affiliate policy</a>', size="13px", lh="20px", color=DIM, mw="100%")
    SOCIAL=('<span style="display:inline-flex;align-items:center;gap:14px">'
      '<a href="#" aria-label="Instagram" style="display:inline-flex"><svg width="20" height="20" viewBox="0 0 24 24" fill="#e1306c"><path d="M12 2.2c3.2 0 3.6 0 4.9.07 1.17.05 1.8.25 2.23.42.56.22.96.48 1.38.9.42.42.68.82.9 1.38.17.42.37 1.06.42 2.23.06 1.27.07 1.65.07 4.85s0 3.58-.07 4.85c-.05 1.17-.25 1.8-.42 2.23-.22.56-.48.96-.9 1.38-.42.42-.82.68-1.38.9-.42.17-1.06.37-2.23.42-1.27.06-1.65.07-4.85.07s-3.58 0-4.85-.07c-1.17-.05-1.8-.25-2.23-.42-.56-.22-.96-.48-1.38-.9-.42-.42-.68-.82-.9-1.38-.17-.42-.37-1.06-.42-2.23C2.21 15.58 2.2 15.2 2.2 12s0-3.58.07-4.85c.05-1.17.25-1.8.42-2.23.22-.56.48-.96.9-1.38.42-.42.82-.68 1.38-.9.42-.17 1.06-.37 2.23-.42C8.42 2.21 8.8 2.2 12 2.2zm0 3.05A6.75 6.75 0 1 0 18.75 12 6.75 6.75 0 0 0 12 5.25zm0 11.13A4.38 4.38 0 1 1 16.38 12 4.38 4.38 0 0 1 12 16.38zm6.96-11.4a1.58 1.58 0 1 1-1.58-1.57 1.58 1.58 0 0 1 1.58 1.57z"/></svg></a>'
      '<a href="#" aria-label="YouTube" style="display:inline-flex"><svg width="22" height="22" viewBox="0 0 24 24" fill="#ff0000"><path d="M23.5 6.2a3 3 0 0 0-2.1-2.1C19.5 3.6 12 3.6 12 3.6s-7.5 0-9.4.5A3 3 0 0 0 .5 6.2 31.4 31.4 0 0 0 0 12a31.4 31.4 0 0 0 .5 5.8 3 3 0 0 0 2.1 2.1c1.9.5 9.4.5 9.4.5s7.5 0 9.4-.5a3 3 0 0 0 2.1-2.1A31.4 31.4 0 0 0 24 12a31.4 31.4 0 0 0-.5-5.8zM9.6 15.6V8.4l6.2 3.6z"/></svg></a>'
      '<a href="#" aria-label="RSS feed" style="display:inline-flex"><svg width="19" height="19" viewBox="0 0 24 24" fill="#ee802f"><circle cx="4.4" cy="19.6" r="2.4"/><path d="M2 9.5v3.1a8.9 8.9 0 0 1 8.9 8.9H14A11.99 11.99 0 0 0 2 9.5zm0-5.5v3.1c8.2 0 14.9 6.7 14.9 14.9H20A18 18 0 0 0 2 4z"/></svg></a>'
      '<a href="#" aria-label="X" style="display:inline-flex"><svg width="18" height="18" viewBox="0 0 24 24" fill="#ffffff"><path d="M18.9 2H22l-7.2 8.3L23.3 22h-6.6l-5.2-6.8L5.6 22H2.5l7.7-8.8L1 2h6.8l4.7 6.2zm-1.1 18h1.7L7.3 3.8H5.5z"/></svg></a>'
      '</span>')
    social=text(SOCIAL, size="13px", lh="20px", mw="auto")
    for nd in (left, social):  # let them sit at opposite ends instead of each taking full width
        for s in nd["styles"]:
            if s["prop"]=="width": s["value"]="auto"
        nd["styles"].append({"prop":"flexShrink","value":"0"})
    left["styles"].append({"prop":"flex","value":"1"})
    left["styles"].append({"prop":"textAlign","value":"center","media":767})
    bottom=rowf([left, social], gap="16px", justify="space-between", align="center", wrap=True,
                styles=[{"prop":"flexDirection","value":"column","media":767},
                        {"prop":"alignItems","value":"center","media":767},{"prop":"gap","value":"14px","media":767}])
    colc=col([logo,lbl,body],gap="14px",styles=[{"prop":"alignItems","value":"center"},{"prop":"maxWidth","value":"900px"},
        {"prop":"margin","value":{"left":"auto","right":"auto"}}])
    outer=col([colc,div,bottom],gap="0px",styles=[{"prop":"maxWidth","value":"900px"},{"prop":"margin","value":{"left":"auto","right":"auto"}}])
    return {"t":"Section","id":nid(),"styles":[{"prop":"backgroundColor","value":FOOT},
        {"prop":"padding","value":{"top":"48px","bottom":"28px","left":"40px","right":"40px"}},
        {"prop":"padding","value":{"top":"40px","bottom":"24px","left":"28px","right":"28px"},"media":767}],
        "p":{"layout":"boxed","dividerPosition":["top"],"horizontalFlip":False,
             "embedded_video":{"src":"","video_size":"stretch","video_position":"center"},"children":[outer]}}

article={"t":"Section","id":nid(),
    "styles":[{"prop":"backgroundColor","value":WHITE},{"prop":"padding","value":{"top":"22px","bottom":"48px"}}],
    "p":{"layout":"boxed","dividerPosition":["top"],"horizontalFlip":False,
         "embedded_video":{"src":"","video_size":"stretch","video_position":"center"},"children":[article_col]}}

body={"id":nid(),"t":"Root","version":11,
    "styles":[{"prop":"pageWidth","value":"720px"},{"prop":"backgroundColor","value":WHITE}],
    "p":{"children":[header, article, footer()]}}

def _scan(nd,path="root"):
    bad=[]
    if isinstance(nd,dict):
        if "t" in nd and "id" not in nd: bad.append(path+" missing id")
        for k,v in nd.items():
            if v is None: bad.append(path+"."+k+" None")
            bad+=_scan(v,path+"."+str(k))
    elif isinstance(nd,list):
        for i,x in enumerate(nd): bad+=_scan(x,path+f"[{i}]")
    return bad
iss=_scan(body); print("sanity issues:", len(iss)); [print("  !",x) for x in iss[:8]]

r=sgql('mutation($id: ID!, $node: InputFunnel!){ updateFunnel(id:$id,node:$node){ id steps { uid slug } } }',
    {"id":FUNNEL,"node":{"steps":[{"id":STEP,"slug":"article-v10","title":"Smartwatch review","type":"article_page",
        "settings":{"custom_html":CH_OUT},"visual":{"x":100,"y":100},"body":body}]}})
print("WROTE", r["updateFunnel"]["steps"])
print("article blocks:", len(kids))
