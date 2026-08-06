#!/usr/bin/env python3
"""Match the offer card's right column to Figma 557:6517, measured per element.

  HEADING 557:6530   24.7px / lh 29.61 / letterSpacing -1.5 / Inter ExtraBold
                     "UP TO 50% OFF" #E63A45  +  "FOR\nA LIMITED TIME\nONLY!" #253319
                     Line breaks are HARD in the design (\n in `characters`), which
                     is why it is 3 lines there and 2 in ours.
                     Ours also had #7b0323 — the retired maroon, not the brand red.
  SUBTEXT 557:6532   10.5px / lh 13.46 / Inter Medium(500) / #000000  (ours: 13/18/400)
  BUTTON  557:6536   layoutSizingHorizontal FILL -> full column width,
                     padding 12/32/16/32, radius 10 (ours hugged its label at 11/14)
  PILL    557:6545   237 wide (FILL), radius 4, #E1C6CB80, vertical padding 9.08
                     Ours was an inline span hugging its text, so it could not span
                     the column; the pill styling moves onto the block itself.
  TP row  557:6518   two 5.19x1 dividers #0000001C, itemSpacing 8
"""
import json, re, sys
sys.path.insert(0, "tools/lf-agent-bridge")
import lf_api

FUNNEL = "fun_vGqQYxn4H2i_traYYkh4w"
STEP = "step_0hL9bV7NUmyESdgkwY4Ih"

tok = open("tools/lf-agent-bridge/.session_token").read().strip()
acct = open("tools/lf-agent-bridge/.lf_account").read().strip()
h = lf_api.session_headers(acct)
node = lf_api.get_funnel_steps(tok, FUNNEL, extra_headers=h)
s = {x["uid"]: x for x in node["steps"]}[STEP]
was = isinstance(s["body"], str)
body = json.loads(s["body"]) if was else s["body"]

def setp(sty, prop, value):
    for st in sty:
        if isinstance(st, dict) and st.get("prop") == prop and "media" not in st:
            st["value"] = value
            return
    sty.append({"prop": prop, "value": value})

def drop(sty, prop):
    for i in range(len(sty) - 1, -1, -1):
        if isinstance(sty[i], dict) and sty[i].get("prop") == prop and "media" not in sty[i]:
            del sty[i]

log = []

def walk(x):
    if isinstance(x, dict):
        pid = str(x.get("id", ""))[:8]
        p = x.get("p") or {}
        sty = x.setdefault("styles", [])

        if pid == "9e1d3664":                                   # heading
            assert "#7b0323" in p["content"], p["content"][:60]
            p["content"] = ('<span style="color:#e63a45">UP TO 50% OFF</span> '
                            '<span style="color:#253319">FOR<br>A LIMITED TIME<br>ONLY!</span>')
            setp(sty, "fontSize", "24.7px")
            setp(sty, "lineHeight", "29.61px")
            setp(sty, "letterSpacing", "-1.5px")
            log.append("heading: #e63a45 (was maroon #7b0323), hard breaks, 24.7/29.61/-1.5")

        elif pid == "23583eb6":                                  # subtext
            setp(sty, "fontSize", "10.5px")
            setp(sty, "lineHeight", "13.46px")
            setp(sty, "fontWeight", "500")
            setp(sty, "color", {"r": 0, "g": 0, "b": 0, "a": 1})
            log.append("subtext: 10.5/13.46, weight 500, #000")

        elif pid == "4c31a1e4":                                  # CTA button
            setp(sty, "width", "100%")
            setp(sty, "padding", {"top": "12px", "right": "32px",
                                  "bottom": "16px", "left": "32px"})
            log.append("button: full width, padding 12/32/16/32")

        elif pid == "7ae0ef64":                                  # pill
            c = p["content"]
            assert "background:rgba(225,198,203,.5)" in c, c[:80]
            # the pill must span the column, so its styling moves to the block
            c = re.sub(r'<span style="background:rgba\(225,198,203,\.5\);'
                       r'border-radius:4px;padding:3px 10px;([^"]*)"', r'<span style="\1"', c, count=1)
            p["content"] = c
            setp(sty, "backgroundColor", {"r": 225, "g": 198, "b": 203, "a": 0.5})
            setp(sty, "borderRadius", "4px")
            setp(sty, "padding", {"top": "9px", "bottom": "9px"})
            log.append("pill: full-width block, radius 4, #E1C6CB80, 9px vertical")

        for v in x.values():
            walk(v)
    elif isinstance(x, list):
        for v in x:
            walk(v)

walk(body)
assert len(log) == 4, log
for l in log:
    print("  " + l)

lf_api.gql(tok, "mutation($id:ID!,$node:InputFunnel!){updateFunnel(id:$id,node:$node){id}}",
           {"id": FUNNEL, "node": {"steps": [{
               "id": STEP, "slug": s["slug"], "title": s["title"], "type": s["type"],
               "settings": s["settings"], "visual": s["visual"],
               "body": json.dumps(body) if was else body}]}}, extra_headers=h)
print("write ok")
