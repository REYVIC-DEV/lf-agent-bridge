#!/usr/bin/env python3
"""TEST 2 — HLTH listicle (Figma node 1640:2196) as native LF blocks.
Text/layout + exact styles reconstructed from the Figma REST API. Real photos +
Trustpilot logo exported via REST and hosted in LF. Writes to the from-scratch
funnel fun_0xxSP4vzvsYLXJJ1Ap3wP."""
import json, uuid, lf_api

tok = open('.session_token').read().strip()
ACCT = open('.lf_account').read().strip()
HH = {"account-id": ACCT, "version": "1",
      "Origin": "https://app.lightfunnels.com", "Referer": "https://app.lightfunnels.com/"}
def sgql(q, v=None): return lf_api.gql(tok, q, v, extra_headers=HH)
def nid(): return str(uuid.uuid4())

ids = json.load(open("/tmp/test2_ids.json"))
FUNNEL, STEP, FSLUG = ids["funnel"], ids["step"], ids["slug"]
IMG  = json.load(open("/tmp/hlth_img_map.json"))   # hosted TECH UNBOXED logo
IMG2 = json.load(open("/tmp/test2_img_map.json"))  # real photos + tp_logo/tp_small/launch_img
PDP = "https://hlthtrack.com/products/wearable-hlth-band"

# ---- colors (from REST) ----
NAVY  = {"r":25,"g":30,"b":42,"a":1}
DARK  = {"r":17,"g":24,"b":39,"a":1}     # #111827
FEAT  = {"r":55,"g":65,"b":81,"a":1}     # #374151
BODY  = {"r":75,"g":85,"b":99,"a":1}     # #4b5563
GRAY6 = {"r":107,"g":114,"b":128,"a":1}  # #6b7280
RED   = {"r":230,"g":58,"b":69,"a":1}    # #e63a45
WHITE = {"r":255,"g":255,"b":255,"a":1}
SPON  = {"r":189,"g":189,"b":189,"a":1}
BORDER= {"r":229,"g":231,"b":235,"a":1}  # #e5e7eb table border
DIVID = {"r":238,"g":240,"b":242,"a":1}  # #eef0f2 row divider
BANNER= {"r":40,"g":40,"b":43,"a":1}     # #28282b
THUMB = {"r":241,"g":240,"b":236,"a":1}  # #f1f0ec
REVBG = {"r":246,"g":246,"b":247,"a":1}  # #f6f6f7
MAROON= {"r":123,"g":3,"b":35,"a":1}     # #7b0323
MUTE  = {"r":138,"g":143,"b":153,"a":1}
DIM   = {"r":150,"g":156,"b":168,"a":1}
GREEN = {"r":0,"g":182,"b":122,"a":1}
HLTHROW = {"r":240,"g":253,"b":246,"a":1}

def B(t): return '<span style="color:#191e2a;font-weight:600">%s</span>' % t
def L(t, href=PDP): return '<a href="%s" target="_blank" style="color:#e63946;font-weight:700;text-decoration:underline">%s</a>' % (href, t)

def title(content, size, fs, lh, mt=0, color=DARK, align="left"):
    st=[{"prop":"fontFamily","value":"Inter"},{"prop":"color","value":color},
        {"prop":"fontSize","value":fs},{"prop":"lineHeight","value":lh},
        {"prop":"fontWeight","value":"700"},{"prop":"textAlign","value":align},
        {"prop":"width","value":"100%"},{"prop":"maxWidth","value":"100%"}]
    if mt: st.append({"prop":"margin","value":{"top":"%spx"%mt}})
    _mfs={"1":("29px","36px"),"2":("22px","30px")}.get(size)
    if _mfs:
        st.append({"prop":"fontSize","value":_mfs[0],"media":767})
        st.append({"prop":"lineHeight","value":_mfs[1],"media":767})
    return {"t":"Title","id":nid(),"p":{"size":size,"content":content,"widthOption":"fill"},"styles":st}

def text(content, size="17px", lh="28px", color=FEAT, weight="400", align="left", italic=False, mw="100%", mcenter=False):
    st=[{"prop":"fontFamily","value":"Inter"},{"prop":"color","value":color},
        {"prop":"fontSize","value":size},{"prop":"lineHeight","value":lh},
        {"prop":"fontWeight","value":weight},{"prop":"textAlign","value":align},
        {"prop":"maxWidth","value":mw},{"prop":"width","value":"100%"}]
    if italic: st.append({"prop":"fontStyle","value":"italic"})
    if mcenter: st.append({"prop":"textAlign","value":"center","media":767})
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

def img_block(key, height=None, radius="12px", full=True, fit="cover"):
    m=IMG2[key]
    st=[{"prop":"maxWidth","value":"100%"},{"prop":"borderRadius","value":radius},
        {"prop":"objectFit","value":fit},{"prop":"lfDisplay","value":"block"}]
    if full: st.append({"prop":"width","value":"100%"})
    if height:
        st.append({"prop":"height","value":height})
        st.append({"prop":"height","value":"200px","media":767})
    return {"t":"Image","id":nid(),"p":{"title":key,"src_id":m["src_id"],"src_uid":m["src_uid"],"src":m["src"]},"styles":st}

def inline_img(key, w, h, radius="0px"):
    m=IMG2[key]
    return {"t":"Image","id":nid(),"p":{"title":key,"src_id":m["src_id"],"src_uid":m["src_uid"],"src":m["src"]},
        "styles":[{"prop":"width","value":w},{"prop":"height","value":h},{"prop":"objectFit","value":"contain"},
                  {"prop":"borderRadius","value":radius},{"prop":"lfDisplay","value":"block"},{"prop":"flexShrink","value":"0"}]}

def logo_img(w="200px", h="50px"):
    m=IMG["logo"]
    return {"t":"Image","id":nid(),"p":{"title":"logo","src":m["src"]},
        "styles":[{"prop":"width","value":w},{"prop":"height","value":h},{"prop":"maxWidth","value":"100%"},
                  {"prop":"objectFit","value":"contain"},{"prop":"lfDisplay","value":"block"}]}

STAR = "★"
def tp_stars(rating, color, box=18):
    """Trustpilot-style colored star boxes with half-star rounding."""
    fs = 12 if box>=18 else 11
    half=round(rating*2)/2; full=int(half); hh=(half-full)==0.5
    out='<span style="display:inline-flex;gap:2px;vertical-align:middle">'
    tpl='<span style="display:inline-flex;align-items:center;justify-content:center;width:%dpx;height:%dpx;border-radius:3px;color:#fff;font-size:%dpx;background:%s">'+STAR+'</span>'
    for i in range(5):
        if i<full: bg=color
        elif i==full and hh: bg="linear-gradient(90deg,%s 50%%,#dcdce6 50%%)"%color
        else: bg="#dcdce6"
        out+=tpl%(box,box,fs,bg)
    return out+'</span>'

def button(label, href=PDP, bg=RED, fg=WHITE, full=False, size="14px"):
    lab={"t":"Text","id":nid(),"p":{"content":label},
        "styles":[{"prop":"fontFamily","value":"Inter"},{"prop":"color","value":fg},
            {"prop":"fontSize","value":size},{"prop":"fontWeight","value":"600"},
            {"prop":"lineHeight","value":"22px"},{"prop":"textAlign","value":"center"},
            {"prop":"whiteSpace","value":"nowrap"},{"prop":"maxWidth","value":"100%"}]}
    lw=container([lab],[{"prop":"lfDisplay","value":"flex"},{"prop":"alignItems","value":"center"},
        {"prop":"justifyContent","value":"center"},{"prop":"maxWidth","value":"100%"}])
    st=[{"prop":"backgroundColor","value":bg},{"prop":"borderRadius","value":"8px"},
        {"prop":"padding","value":{"top":"11px","bottom":"11px","left":"14px","right":"14px"}},
        {"prop":"lfDisplay","value":"flex"},{"prop":"alignItems","value":"center"},
        {"prop":"justifyContent","value":"center"}]
    if full: st.append({"prop":"width","value":"100%"})
    return {"t":"BlockLink","id":nid(),"p":{"destination":{"type":"static","value":href},
        "target":"_blank","widthOption":"auto","children":[lw]},"styles":st}

# ---------------- CARD (table row) ----------------
def card(c, last=False):
    mid=[]
    if c.get("badge"):
        mid.append(text('<span style="color:#f5a623;font-weight:700;font-size:12px;letter-spacing:.5px">%s</span>'%c["badge"], size="12px", lh="19px", mcenter=True))
    mid.append(text(c["name"], size="24px", lh="28px", color=DARK, weight="700", mcenter=True))
    mid.append(inline_img("tp_logo","69px","22px"))
    mid.append(text(tp_stars(c["tp"], c["star"], 18)
        + '&nbsp;&nbsp;<span style="color:#111827;font-weight:700;font-size:13px;vertical-align:middle">%s</span>'%c["tp"],
        size="13px", lh="22px", mcenter=True))
    feats=[text(f, size="16px", lh="22px", color=FEAT) for f in c["features"]]
    mid.append(col(feats, gap="4px", styles=[{"prop":"margin","value":{"top":"6px"}}]))
    midcol=col(mid, gap="8px", styles=[{"prop":"flex","value":"1"},{"prop":"minWidth","value":"0"},{"prop":"alignItems","value":"center","media":767}])

    thumb=container([img_block(c["img"], height="76px", radius="8px", fit="contain")],
        [{"prop":"width","value":"76px"},{"prop":"flexShrink","value":"0"},
         {"prop":"backgroundColor","value":WHITE},{"prop":"borderRadius","value":"8px"},
         {"prop":"width","value":"100%","media":767},{"prop":"maxWidth","value":"280px","media":767}])

    right=[text("OUR SCORE", size="11px", lh="16px", color=GRAY6, align="center"),
           text('<span style="font-size:32px;font-weight:800;color:#111827">%s</span><span style="font-size:15px;color:#6b7280">/10</span>'%c["score"], size="32px", lh="34px", align="center"),
           button(c["button"], href=c.get("href","#"), full=True)]
    price = c["price"] if not c.get("strike") else '%s <span style="text-decoration:line-through;color:#9ca3af;font-weight:400;font-size:14px">%s</span>'%(c["price"], c["strike"])
    right.append(text(price, size="16px", lh="24px", color=DARK, weight="700", align="center"))
    right.append(text(c["delivery"], size="12px", lh="16px", color=GRAY6, align="center"))
    rightcol=col(right, gap="8px", styles=[{"prop":"width","value":"160px"},{"prop":"flexShrink","value":"0"},
        {"prop":"alignItems","value":"center"},{"prop":"justifyContent","value":"flex-start"},
        {"prop":"width","value":"100%","media":767},{"prop":"maxWidth","value":"340px","media":767}])

    st=[{"prop":"backgroundColor","value":WHITE},
        {"prop":"padding","value":{"top":"20px","bottom":"20px","left":"20px","right":"20px"}}]
    if not last:
        st+=[{"prop":"borderStyle","value":"solid"},{"prop":"borderColor","value":DIVID},{"prop":"borderWidth","value":"0px 0px 1px 0px"}]
    else:
        st.append({"prop":"borderRadius","value":"0px 0px 12px 12px"})
    # desktop card is hidden on phones; a dedicated mobile card (card_mobile) renders instead
    st+=[{"prop":"lfDisplay","value":"none","media":767}]
    return rowf([thumb, midcol, rightcol], styles=st, gap="16px", align="flex-start")

# ---------------- MOBILE CARD (single centered column, exact Figma mobile order) ----------------
# Figma mobile (node 3:841) stacks each card: badge -> name -> OUR SCORE -> image(188x186)
# -> Trustpilot(logo+stars+rating) -> features -> full-width CTA -> price/delivery, all centered.
def card_mobile(c, last=False):
    kids=[]
    if c.get("badge"):
        kids.append(text('<span style="color:#f5a623;font-weight:700;font-size:13px;letter-spacing:.5px">%s</span>'%c["badge"],
                         size="13px", lh="21px", align="center"))
    kids.append(text(c["name"], size="24px", lh="28px", color=(NAVY if c.get("badge") else DARK), weight="700", align="center"))
    # OUR SCORE row
    kids.append(text('<span style="color:#6b7280;font-size:11px;font-weight:400;letter-spacing:.5px;vertical-align:middle">OUR SCORE</span>'
        '&nbsp;&nbsp;<span style="font-size:30px;font-weight:800;color:#111827;vertical-align:middle">%s</span>'
        '<span style="font-size:14px;color:#6b7280;vertical-align:middle">/10</span>'%c["score"],
        size="30px", lh="34px", align="center"))
    # product image ~ square, centered, white bg (contain avoids the Fitbit top-crop)
    img=container([img_block(c["img"], height="210px", radius="8px", full=True, fit="contain")],
        [{"prop":"width","value":"100%"},{"prop":"maxWidth","value":"240px"},
         {"prop":"backgroundColor","value":WHITE},{"prop":"borderRadius","value":"8px"}])
    kids.append(img)
    # Trustpilot: logo on top, colored stars + rating below (centered)
    kids.append(inline_img("tp_logo","110px","35px"))
    kids.append(text(tp_stars(c["tp"], c["star"], 18)
        + '&nbsp;&nbsp;<span style="color:#111827;font-weight:700;font-size:13px;vertical-align:middle">%s</span>'%c["tp"],
        size="13px", lh="22px", align="center"))
    # features (left-aligned block, full width)
    feats=[text(f, size="14px", lh="20px", color=FEAT) for f in c["features"]]
    kids.append(col(feats, gap="10px", styles=[{"prop":"margin","value":{"top":"4px"}}]))
    # full-width CTA
    kids.append(button(c["button"], href=c.get("href","#"), full=True, size="16px"))
    # price / delivery, centered
    price = c["price"] if not c.get("strike") else '%s <span style="text-decoration:line-through;color:#9ca3af;font-weight:400;font-size:14px">%s</span>'%(c["price"], c["strike"])
    kids.append(text(price, size="18px", lh="24px", color=NAVY, weight="800", align="center"))
    kids.append(text(c["delivery"], size="12px", lh="16px", color=GRAY6, align="center"))

    st=[{"prop":"backgroundColor","value":WHITE},
        {"prop":"padding","value":{"top":"18px","bottom":"18px","left":"16px","right":"16px"}},
        {"prop":"alignItems","value":"center"},
        {"prop":"lfDisplay","value":"none"},                      # hidden on desktop
        {"prop":"lfDisplay","value":"flex","media":767}]          # shown on phones
    if not last:
        st+=[{"prop":"borderStyle","value":"solid"},{"prop":"borderColor","value":DIVID},{"prop":"borderWidth","value":"0px 0px 1px 0px"}]
    else:
        st.append({"prop":"borderRadius","value":"0px 0px 12px 12px"})
    return col(kids, gap="14px", styles=st)

# ---------------- DATA ----------------
CARDS=[
 {"img":"prod1","star":"#00b67a","name":"1. HLTH Band","badge":"★ BEST OVERALL","tp":4.4,"score":"9.9","button":"VISIT HLTH","href":PDP,
  "price":"£79","strike":"£158","delivery":"4-7 Day Delivery","features":[
   "✅ No subscription or locked features","✅ Confirmed 30-day Battery life",
   "✅ Tracks blood pressure, RHR, HRV & Sp02","✅ Full sleep stages (deep, REM, light)",
   "✅ Multi-wavelength PPG","✅ Adaptive Power Management","✅ Lightweight 18g, screen-free design",
   "✅ Waterproof 1ATM rating","❌ New Company – Frequently sold out","❌ No built-in GPS (uses phone)"]},
 {"img":"prod2","star":"#ffce00","name":"2. Whoop 5.0","tp":3.2,"score":"9.0","button":"VISIT AMAZON","href":"#",
  "price":"£349/yr","delivery":"2-3 Day Prime Delivery","features":[
   "✅ Excellent recovery & strain analytics","✅ Comfortable screen-free band",
   "✅ Tracks HRV, sleep & SpO2","✅ Multi-wavelength PPG","❌ £169–£349 per year annual fees",
   "❌ Device stops working if you cancel","❌ Real battery only 4–7 days (not 14)",
   "❌ Blood pressure locked to £359 tier","❌ Widespread 5.0 heart-rate complaints"]},
 {"img":"prod3","star":"#ff8622","name":"3. Apple Watch Series 10","tp":1.8,"score":"7.9","button":"VISIT SITE","href":"#",
  "price":"£399","delivery":"7-12 Day Shipping","features":[
   "✅ Best-in-class app & smart features","✅ Great communication options",
   "✅ Onboard ECG & accurate heart rate","✅ Built-in GPS","❌ £399 one-time investment",
   "❌ Requires nightly charging","❌ Hypertension alerts only, no BP",
   "❌ Nightly charging breaks sleep tracking","❌ iPhone only, no android",
   "❌ We found ourselves checking it constantly"]},
 {"img":"prod4","star":"#ff8622","name":"4. Garmin Vivoactive 6","tp":1.5,"score":"7.5","button":"VISIT AMAZON","href":"#",
  "price":"£250","delivery":"2-3 Day Prime Delivery","features":[
   "✅ Reliable GPS & sports modes","✅ Accurate fitness tracking","✅ ~7-day battery",
   "✅ Free garmin connect app","❌ £250 one-time investment","❌ Clunky app interface",
   "❌ No blood pressure monitoring","❌ No onboard ECG or altimeter",
   "❌ No speaker/mic for calls","❌ Bulky and uncomfortable for sleep"]},
 {"img":"prod5","star":"#ff8622","name":"5. Fitbit Charge 6","tp":1.6,"score":"5.9","button":"VISIT AMAZON","href":"#",
  "price":"£79.99","strike":"£139.99","delivery":"2-3 Day Prime Delivery","features":[
   "✅ Onboard ECG & SpO2","✅ Compact, lightweight band","✅ Built-in GPS + swimproof",
   "❌ Privacy concerns after google acquisition","❌ Sleep score & readiness behind £9.99/mo Premium",
   "❌ Real battery only 2–5 days","❌ No blood pressure monitoring","❌ GPS was hit or miss",
   "❌ Data loss in google migration"]},
]

SECTIONS=[
 {"h":"After Spending £1,581 On Fitness Trackers, The HLTH Band Was Worth Every Penny","img":"sec1","paras":[
  "The HLTH Band stands out in the market due to its simplicity and serious health credentials. Establishing a new standard for everyday fitness tracking in 2026, it consistently matched devices costing three to five times more across every metric.",
  "A standout feature of the HLTH Band is its Multi-Wavelength PPG sensor – the same technology found in clinical-grade monitoring equipment. It delivers continuous, reliable readings of blood pressure, heart rate, HRV, and resting heart rate around the clock.",
  "It's one of the only bands on the market offering blood pressure readings without a subscription. The kind of data your doctor actually cares about, completely free, every single day.",
  "It delivers full sleep stage tracking across a confirmed 30-day battery life. That's 30 nights of uninterrupted sleep data that the Apple Watch, Fitbit, and Garmin simply cannot match without daily charging.",
  "Normally, this level of monitoring comes locked behind a £229-per-year membership or built into a £399 smartwatch. The HLTH Band is the exception. At £79, it's the most capable screen-free health tracker we tested. That's serious health data in a device light enough to forget you're wearing."]},
 {"h":"We Expected It To Crack Under Testing. It Didn't.","img":"sec2","paras":[
  "When we unboxed the HLTH Band, the first thing we noticed was the weight. At 18 grams, it sits on your wrist like a rubber bracelet. After a week switching between the Apple Watch and Garmin, putting it back on felt like taking a weight off.",
  "But comfort means nothing without accuracy. So we tested the claim that matters most: blood pressure.",
  "Every cardiologist we consulted agreed. A single spot reading tells you almost nothing. Blood pressure fluctuates constantly with stress, movement, food, and sleep. Only an extended trend provides a real signal.",
  "We ran a comparison against a medical-grade cuff under resting conditions. The HLTH Band came within the recommended ±10 mmHg, consistently, across multiple sessions.",
  "That matters because a cuff catches one moment. The HLTH Band reads all day, while you work, sleep, and recover. That continuous picture is what reveals dangerous patterns, like the overnight dip doctors specifically look for. No other device in our test group offered continuous blood pressure monitoring at any price. Except Whoop, locked behind their £349-per-year tier."]},
 {"h":"I Didn't Expect To Still Be Wearing It 30 Days Later","img":"sec3","paras":[
  "I'll be honest. When we started this test, I assumed the HLTH Band would be the first device I put back in the box.",
  "A new company, a £79 price tag, no screen, doesn't even tell the time. No brand name anyone would recognise at a dinner party. Every instinct said this underdog would quietly disappoint.",
  "But thirty days later it's still on my wrist, and not because I forgot to switch back.",
  "I wore it through back-to-back work weeks, flights, gym sessions, and holidays full of bad sleep, without it ever needing a charge. Accurate sleep stages explained why certain mornings felt broken despite eight hours in bed. Blood pressure trends across weeks helped explain my daily brain fog. And with trustworthy heart rate averages, I could finally spot changes I needed to make.",
  "What I learned is simple. The device that actually helps your health isn't always the most expensive. It's the one you'll keep wearing long enough to get the data."]},
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

COST_COLS=["Device","Year 1","Year 2","Total","Subscription"]
COST_ROWS=[
 ["Whoop 5.0","£349","£349","£698","Mandatory"],
 ["Apple Watch","£399","£0","£399","No"],
 ["Fitbit Charge 6","£260","£120","£380","Feature paywall"],
 ["Garmin Vivoactive 6","£250","£0","£250","No"],
 ["HLTH Band","£79","£0","£79","Never"],
]

# ---------------- ASSEMBLE ----------------
def para(t): return text(t, size="17px", lh="28px", color=DARK)

kids=[]
kids.append(text('<span style="color:#111827">Home</span>&nbsp;&nbsp;<span style="color:#9ca3af">&gt;</span>&nbsp;&nbsp;<span style="color:#111827">Wearables</span>&nbsp;&nbsp;<span style="color:#9ca3af">&gt;</span>&nbsp;&nbsp;<span style="color:#e63a45">Best Fitness Trackers of 2026</span>', size="14px", lh="22px", color=DARK))
kids.append(title("We Spent £1,581 Testing The Top 5 Fitness Trackers of 2026. The £158 Outsider Won.","1","36px","46px"))
META=('<span style="display:inline-flex;align-items:center;gap:10px;flex-wrap:wrap">'
  '<span style="display:inline-flex;align-items:center;background:#1d6fe0;color:#fff;font-weight:700;font-size:13px;letter-spacing:.5px;padding:6px 12px;border-radius:6px">Buying Guides</span>'
  '<span style="display:inline-flex;align-items:center;gap:5px;background:#e8f462;color:#000;font-weight:700;font-size:13px;letter-spacing:.5px;padding:6px 12px;border-radius:6px">'
  '<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="#000" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="22 7 13.5 15.5 8.5 10.5 2 17"/><polyline points="16 7 22 7 22 13"/></svg>Trending</span>'
  '<span style="color:#1e1e1e;font-size:15px">By </span><a href="#" style="color:#0085ff;font-size:15px;text-decoration:underline">Marcus Pendleton</a>'
  '</span>')
# meta row — desktop shows category pills; mobile (Figma 3:861) shows a plain byline
meta_desktop=col([text(META, size="13px", lh="26px"),
                  text("Last updated May 20, 2026", size="15px", lh="24px", color={"r":120,"g":120,"b":120,"a":1})],
                 gap="10px", styles=[{"prop":"lfDisplay","value":"none","media":767}])
BYLINE=('<span style="color:#6b7280">By </span>'
        '<span style="color:#111827;font-weight:600">Marcus Pendleton</span>'
        '<span style="color:#6b7280">&nbsp;&nbsp;|&nbsp;&nbsp;Contributions from Kate Smith&nbsp;&nbsp;|&nbsp;&nbsp;Last updated June 2026</span>')
meta_mobile=container([text(BYLINE, size="13px", lh="21px", color=GRAY6)],
    [{"prop":"width","value":"100%"},{"prop":"flexDirection","value":"column"},
     {"prop":"borderStyle","value":"solid"},{"prop":"borderColor","value":DIVID},{"prop":"borderWidth","value":"0px 0px 1px 0px"},
     {"prop":"padding","value":{"bottom":"12px"}},
     {"prop":"lfDisplay","value":"none"},{"prop":"lfDisplay","value":"flex","media":767}])
kids.append(meta_desktop)
kids.append(meta_mobile)
kids.append(img_block("hero", height="360px"))
for q in ["Looking to accurately track and improve your health?",
          "Want a reliable fitness tracker that follows your blood pressure, heart rate, and sleep without monthly subscriptions?",
          "Searching for a simple, comfortable tracker built for everyday people?"]:
    kids.append(text(B(q), size="17px", lh="26px", color=DARK))
kids.append(para("If you nodded yes to any of these, you've come to the right place. We spent £1,581 to meticulously test the top fitness trackers from " + B("Whoop, Fitbit, Garmin, Apple") + " and other leading brands, bought from Amazon, Currys, and direct from each brand's website."))
kids.append(para("Our testing revealed a surprising divide in the market, and one band truly stood out. This device exceeded our expectations and challenged everything we thought we knew about what a tracker can do for you long term."))
kids.append(para("The top-rated tracker comes from an outsider, paving the way for cutting-edge, affordable everyday health technology. It excels in data accuracy, battery life, and total cost of ownership, without locking a single feature behind monthly fees."))
kids.append(para("Read on for our full comparison. Discover which model claimed the top spot, and why it might be the smartest health buy you make this year."))

# ranked cards as a bordered TABLE (dark banner header + rows w/ dividers)
banner=container([text("The best picks reviewed by Tech Unboxed", size="16px", lh="26px", color=WHITE, weight="700", align="center")],
    [{"prop":"backgroundColor","value":BANNER},{"prop":"borderRadius","value":"12px 12px 0px 0px"},
     {"prop":"padding","value":{"top":"15px","bottom":"15px","left":"16px","right":"16px"}},{"prop":"width","value":"100%"}])
table_rows=[banner]
for i,c in enumerate(CARDS):
    lastc = (i==len(CARDS)-1)
    table_rows.append(card(c, last=lastc))          # desktop 3-col (hidden < 768px)
    table_rows.append(card_mobile(c, last=lastc))   # mobile 1-col (hidden >= 768px)
kids.append(container(table_rows,[{"prop":"width","value":"100%"},{"prop":"borderStyle","value":"solid"},
    {"prop":"borderColor","value":BORDER},{"prop":"borderWidth","value":"1px"},
    {"prop":"borderRadius","value":"12px"},{"prop":"margin","value":{"top":"16px"}}]))

# article sections
for i, sec in enumerate(SECTIONS):
    kids.append(title(sec["h"],"2","28px","37px", mt=24))
    kids.append(img_block(sec["img"], height="360px"))
    for p in sec["paras"]:
        kids.append(para(p))
    if i==2:
        kids.append(container([text('<b style="color:#191e2a">As a 47-year-old trying to understand whether my body is aging well or aging fast, this is the first tracker that actually helped.</b>', size="18px", lh="28px", color=NAVY, italic=True)],
            [{"prop":"borderStyle","value":"solid"},{"prop":"borderColor","value":RED},
             {"prop":"borderWidth","value":"0px 0px 0px 3px"},
             {"prop":"padding","value":{"left":"19px","top":"4px","bottom":"4px"}},{"prop":"width","value":"100%"}]))
        kids.append(img_block("quote", height="360px"))

# cost table
kids.append(title("How Much Is This Actually Going To Cost You?","2","28px","37px", mt=24))
kids.append(para("That depends entirely on which device you choose, and it's worth doing the maths."))
# column flex = Figma mobile widths (Device 83 / Year 51 / Year 51 / Total 51 / Sub 102)
COLW=["1.6","1","1","1","2"]
def cell(t, w, bold=False, color=FEAT, align="center"):
    # mobile matches Figma 3:1263 exactly: 14px cells (not shrunk), tight 8px h-padding
    tx=text(t, size="15px", lh="20px", color=color, weight="700" if bold else "400", align=align)
    tx["styles"].append({"prop":"fontSize","value":"14px","media":767})
    tx["styles"].append({"prop":"lineHeight","value":"18px","media":767})
    return container([tx],
        [{"prop":"flex","value":w},{"prop":"padding","value":{"top":"13px","bottom":"13px","left":"12px","right":"10px"}},
         {"prop":"padding","value":{"top":"9px","bottom":"9px","left":"8px","right":"8px"},"media":767},{"prop":"minWidth","value":"0"}])
HDR={"r":35,"g":35,"b":38,"a":1}; HLTHTBL={"r":243,"g":250,"b":246,"a":1}
RULE={"r":199,"g":199,"b":199,"a":1}; LIGHTRULE={"r":236,"g":238,"b":240,"a":1}; OUTLINE={"r":0,"g":0,"b":0,"a":0.15}
tbl=[rowf([cell("Device",COLW[0],bold=True,color=HDR,align="left"),cell("Year 1",COLW[1],bold=True,color=HDR),
          cell("Year 2",COLW[2],bold=True,color=HDR),cell("Total",COLW[3],bold=True,color=HDR),
          cell("Subscription",COLW[4],bold=True,color=HDR)], gap="0px", align="center",
          styles=[{"prop":"borderStyle","value":"solid"},{"prop":"borderColor","value":RULE},{"prop":"borderWidth","value":"0px 0px 2px 0px"}])]
for r_ in COST_ROWS:
    hl = r_[0]=="HLTH Band"
    rst=[{"prop":"width","value":"100%"}]
    if hl: rst+=[{"prop":"backgroundColor","value":HLTHTBL},{"prop":"borderRadius","value":"0px 0px 10px 10px"}]
    else: rst+=[{"prop":"borderStyle","value":"solid"},{"prop":"borderColor","value":LIGHTRULE},{"prop":"borderWidth","value":"0px 0px 1px 0px"}]
    cc = DARK if hl else FEAT
    tbl.append(rowf([cell(r_[0],COLW[0],bold=hl,color=cc,align="left"),cell(r_[1],COLW[1],bold=hl,color=cc),
                    cell(r_[2],COLW[2],bold=hl,color=cc),cell(r_[3],COLW[3],bold=hl,color=cc),
                    cell(r_[4],COLW[4],bold=hl,color=cc)], gap="0px", align="center", styles=rst))
kids.append(container(tbl,[{"prop":"width","value":"100%"},{"prop":"borderStyle","value":"solid"},
    {"prop":"borderColor","value":OUTLINE},{"prop":"borderWidth","value":"1px"},{"prop":"borderRadius","value":"10px"}]))

# update note — desktop-only urgency box; absent from the mobile Figma (3:1209), so hidden < 768px
kids.append(container([text('<b>[Update: As of DD/MM/YYY, due to the response to this review, stock is limited. You\'ll need to click below to check current availability and activate the introductory discount before it closes.]</b>', size="15px", lh="24px", color=NAVY)],
    [{"prop":"backgroundColor","value":{"r":255,"g":249,"b":230,"a":1}},{"prop":"borderStyle","value":"solid"},
     {"prop":"borderColor","value":{"r":240,"g":200,"b":90,"a":1}},{"prop":"borderWidth","value":"1px"},
     {"prop":"borderRadius","value":"8px"},{"prop":"padding","value":{"top":"14px","bottom":"14px","left":"16px","right":"16px"}},
     {"prop":"width","value":"100%"},{"prop":"margin","value":{"top":"8px"}},
     {"prop":"lfDisplay","value":"none","media":767}]))
kids.append(para("While it's the least expensive device we tested, nothing about its performance felt cheap. The data it delivered over 30 days made every device above it feel like an overcomplicated answer to a simple question."))

# CTA
kids.append(para("Plus, every HLTH Band comes with a " + B("30-day money-back guarantee") + ", so there's no risk in finding out for yourself."))
kids.append(container([button("CHECK DISCOUNT AVAILABILITY →", href=PDP, full=True, size="16px")],
    [{"prop":"width","value":"100%"},{"prop":"padding","value":{"top":"6px","bottom":"6px"}}]))
kids.append(text('<a href="%s" target="_blank" style="color:#191e2a;font-weight:600;text-decoration:underline">Click here to save your £79 Off UK Introductory Offer before it expires.</a>'%PDP, size="14px", lh="20px", color=NAVY, align="center"))

# reviews
kids.append(text("What HLTH Band customers are saying?", size="30px", lh="38px", color=DARK, weight="700", align="center"))
kids.append(text('<span style="color:#00b67a;font-weight:700">'+STAR+' Trustpilot</span>', size="16px", lh="26px", align="center"))
kids.append(text("Rated 4.4 / 5 based on 80+ reviews. Showing 5-star reviews.", size="13px", lh="21px", color=GRAY6, align="center"))
rev_cards=[]
for (ti,bo,au) in REVIEWS:
    rc=col([
        rowf([text(tp_stars(5,"#00b67a",16), size="13px", lh="16px"),
             text('<span style="color:#00b67a;font-weight:600">✓ Verified</span>', size="12px", lh="16px", align="right")],
            gap="8px", justify="space-between", align="center"),
        text(ti, size="14px", lh="20px", color=DARK, weight="700"),
        text(bo, size="16px", lh="23px", color=BODY),
        text(au, size="12px", lh="18px", color=DARK, weight="600"),
    ], gap="8px", styles=[{"prop":"backgroundColor","value":REVBG},{"prop":"borderRadius","value":"8px"},
        {"prop":"padding","value":{"top":"16px","bottom":"16px","left":"16px","right":"16px"}},
        {"prop":"width","value":"31%"},{"prop":"minWidth","value":"200px"},{"prop":"width","value":"100%","media":767}])
    rev_cards.append(rc)
kids.append(rowf(rev_cards, gap="14px", wrap=True, align="stretch"))
kids.append(text('<a href="%s" target="_blank" style="color:#e63946;font-weight:700;text-decoration:underline">See more reviews on Trustpilot →</a>'%PDP, size="14px", lh="20px", align="center"))

# launch-sale promo (horizontal card + maroon tab)
badge=text('<span style="background:#7b0323;color:#fff;padding:4px 12px;border-radius:5px;font-size:12px;font-weight:800;letter-spacing:.5px">LAUNCH SALE</span>', size="12px", lh="20px")
promo_left=container([img_block("launch_img", height="270px", radius="10px")],
    [{"prop":"width","value":"42%"},{"prop":"minWidth","value":"240px"},{"prop":"flexShrink","value":"0"},
     {"prop":"width","value":"100%","media":767},{"prop":"minWidth","value":"0","media":767}])
promo_content=col([
    rowf([inline_img("tp_small","64px","14px"), text('Rated Excellent (4.4) on <b>Trustpilot</b>', size="12px", lh="18px", color=FEAT)], gap="6px", align="center"),
    text("UP TO 50% OFF FOR A LIMITED TIME ONLY!", size="22px", lh="28px", color=DARK, weight="800"),
    text("With 30 day risk-free trial, you have nothing to lose.", size="14px", lh="20px", color=FEAT),
    container([button("TRY IT RISK-FREE →", href=PDP, full=False, size="15px")],
        [{"prop":"lfDisplay","value":"flex"},{"prop":"justifyContent","value":"flex-start"},{"prop":"width","value":"100%"}]),
    text('<span style="color:#e63946;font-weight:700">Sell-Out Risk: High</span> &nbsp;|&nbsp; <span style="color:#191e2a;font-weight:600">FREE shipping</span>', size="12px", lh="18px"),
    text("Try it today with a 30-Day Money Back Guarantee!", size="12px", lh="18px", color=GRAY6),
], gap="10px", styles=[{"prop":"flex","value":"1"},{"prop":"minWidth","value":"0"}])
promo=col([badge, rowf([promo_left, promo_content], gap="20px", align="center", wrap=True,
        styles=[{"prop":"flexDirection","value":"column","media":767}])],
    gap="14px", styles=[{"prop":"backgroundColor","value":WHITE},{"prop":"borderStyle","value":"solid"},
    {"prop":"borderColor","value":BORDER},{"prop":"borderWidth","value":"1px"},{"prop":"borderRadius","value":"14px"},
    {"prop":"padding","value":{"top":"22px","bottom":"22px","left":"22px","right":"22px"}},{"prop":"margin","value":{"top":"16px"}}])
kids.append(promo)

article_col = container(kids,
    [{"prop":"maxWidth","value":"760px"},{"prop":"width","value":"100%"},
     {"prop":"margin","value":{"left":"auto","right":"auto"}},
     {"prop":"lfDisplay","value":"flex"},{"prop":"flexDirection","value":"column"},{"prop":"gap","value":"16px"},
     # mobile gutter (Figma has ~28px left/right page padding on the whole article)
     {"prop":"padding","value":{"left":"22px","right":"22px"},"media":767}])

# header
header={"t":"Section","id":nid(),
    "styles":[{"prop":"backgroundColor","value":BANNER},{"prop":"padding","value":{"top":"8px","bottom":"20px"}}],
    "p":{"layout":"","dividerPosition":["top"],"horizontalFlip":False,
         "embedded_video":{"src":"","video_size":"stretch","video_position":"center"},
         "children":[col([
             text("SPONSORED ARTICLE", size="11px", lh="18px", color=SPON, align="center"),
             container([logo_img()],[{"prop":"lfDisplay","value":"flex"},{"prop":"justifyContent","value":"center"},
                 {"prop":"width","value":"100%"},{"prop":"margin","value":{"top":"10px"}}]),
         ], gap="0px", styles=[{"prop":"alignItems","value":"center"},{"prop":"letterSpacing","value":"1px"}])]}}

# footer (reuse page-1)
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
    lbl=text("DISCLAIMER", size="11px", lh="16px", color=MUTE, weight="700", align="center")
    body=text(DISCLAIMER, size="12px", lh="20px", color=DIM, align="center", mw="820px")
    div=container([],[{"prop":"width","value":"100%"},{"prop":"height","value":"1px"},
        {"prop":"backgroundColor","value":{"r":255,"g":255,"b":255,"a":0.1}},{"prop":"margin","value":{"top":"24px","bottom":"18px"}}])
    left=text('© 2026 TechUnboxed.&nbsp;&nbsp;&nbsp;<a href="#" style="color:#9aa0ab;text-decoration:none">Terms</a>&nbsp;&nbsp;'
              '<a href="#" style="color:#9aa0ab;text-decoration:none">Privacy</a>&nbsp;&nbsp;'
              '<a href="#" style="color:#9aa0ab;text-decoration:none">Editorial standards</a>&nbsp;&nbsp;'
              '<a href="#" style="color:#9aa0ab;text-decoration:none">Affiliate policy</a>', size="12px", lh="18px", color=DIM)
    colc=col([logo,lbl,body],gap="14px",styles=[{"prop":"alignItems","value":"center"},{"prop":"maxWidth","value":"900px"},
        {"prop":"margin","value":{"left":"auto","right":"auto"}}])
    outer=col([colc,div,left],gap="0px",styles=[{"prop":"maxWidth","value":"900px"},{"prop":"margin","value":{"left":"auto","right":"auto"}}])
    return {"t":"Section","id":nid(),"styles":[{"prop":"backgroundColor","value":BANNER},
        {"prop":"padding","value":{"top":"48px","bottom":"28px"}}],
        "p":{"layout":"boxed","dividerPosition":["top"],"horizontalFlip":False,
             "embedded_video":{"src":"","video_size":"stretch","video_position":"center"},"children":[outer]}}

article={"t":"Section","id":nid(),
    "styles":[{"prop":"backgroundColor","value":WHITE},{"prop":"padding","value":{"top":"36px","bottom":"48px"}}],
    "p":{"layout":"boxed","dividerPosition":["top"],"horizontalFlip":False,
         "embedded_video":{"src":"","video_size":"stretch","video_position":"center"},"children":[article_col]}}

body={"id":nid(),"t":"Root","version":11,
    "styles":[{"prop":"pageWidth","value":"960px"},{"prop":"backgroundColor","value":WHITE}],
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
    {"id":FUNNEL,"node":{"steps":[{"id":STEP,"slug":"listicle-v12","title":"HLTH listicle","type":"article_page",
        "settings":{},"visual":{"x":100,"y":100},"body":body}]}})
print("WROTE", r["updateFunnel"]["steps"])
print("article blocks:", len(kids))
