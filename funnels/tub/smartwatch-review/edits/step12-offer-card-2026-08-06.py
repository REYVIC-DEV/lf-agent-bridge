#!/usr/bin/env python3
"""Bring step 12's offer card to the Figma frame (557:6514). Built from the design,
not copied from another step.

Measured from Figma, not eyeballed from the screenshot:

  Border  557:6515  strokeWeight 2, dashPattern [6,4], stroke #000000,
                    cornerRadius 6            -> ours was SOLID, radius 20
  Badge   557:6559  #E63A45, cornerRadius 7, padding 7/16, Inter ExtraBold
                    16px / line-height 28.8   -> height 42.8 ~= its 43px frame
          557:6558  absolute, 670 wide, primaryAxisAlignItems CENTER, y = -22
                    -> horizontally centred, 22px of 43 above the top edge
  TP row  557:6518  [hairline] [text + logo] [hairline], centred, 237 wide
                    -> ours had the text at width:100%, which shoved the logo to
                       the far right instead of sitting next to it

Three changes:

1. Card e368fdc2: borderStyle solid -> dashed, borderRadius 20px -> 6px.
2. Badge e2b4bf9c: textAlign left -> center, and margin {top:-44px, bottom:44px}.
   The -44 lifts it from y=22 (inside the 22px padding) to y=-22, exactly Figma's
   offset; the +44 gives the flow back the same 44px so nothing below moves. LF
   exposes `margin` as an object and has no position/transform prop, so this is
   the available mechanism. Span padding 5px/14px -> 7px/16px and line-height
   24 -> 28.8px so the badge is 43px tall like the frame.
3. TP row 71410521: justifyContent center; text c409efac width 100% -> auto so it
   no longer expands. The two 5x1px Figma hairlines are omitted deliberately —
   they are invisible at render size.
"""
import json, sys
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

log = []

def setprop(styles, prop, value):
    for st in styles:
        if isinstance(st, dict) and st.get("prop") == prop and "media" not in st:
            st["value"] = value
            return "updated"
    styles.append({"prop": prop, "value": value})
    return "added"

def walk(x):
    if isinstance(x, dict):
        pid = str(x.get("id", ""))[:8]
        sty = x.get("styles")

        if pid == "e368fdc2":                                  # the card
            cur = {st["prop"]: st["value"] for st in sty if isinstance(st, dict)}
            assert cur.get("borderStyle") == "solid", cur.get("borderStyle")
            assert cur.get("borderRadius") == "20px", cur.get("borderRadius")
            setprop(sty, "borderStyle", "dashed")
            setprop(sty, "borderRadius", "6px")
            log.append("card: border dashed, radius 6px")

        elif pid == "e2b4bf9c":                                # LAUNCH SALE badge
            p = x.get("p") or {}
            c = p["content"]
            assert "padding:5px 14px" in c, c[:80]
            c = c.replace("padding:5px 14px", "padding:7px 16px", 1)
            c = c.replace("font-weight:800", "font-weight:800;line-height:28.8px", 1)
            p["content"] = c
            setprop(sty, "textAlign", "center")
            setprop(sty, "margin", {"top": "-44px", "bottom": "44px"})
            log.append("badge: centred, raised 44px, 7/16 padding + 28.8 line-height")

        elif pid == "71410521":                                # Trustpilot row
            setprop(sty, "justifyContent", "center")
            log.append("tp row: justifyContent center")

        elif pid == "c409efac":                                # 'Rated Excellent...'
            cur = {st["prop"]: st["value"] for st in sty if isinstance(st, dict)}
            assert cur.get("width") == "100%", cur.get("width")
            setprop(sty, "width", "auto")
            setprop(sty, "flexShrink", "0")
            log.append("tp text: width auto (was 100%, pushing the logo right)")

        for v in x.values():
            walk(v)
    elif isinstance(x, list):
        for v in x:
            walk(v)

walk(body)
assert len(log) == 4, log
for line in log:
    print(" ", line)

lf_api.gql(tok, "mutation($id:ID!,$node:InputFunnel!){updateFunnel(id:$id,node:$node){id}}",
           {"id": FUNNEL, "node": {"steps": [{
               "id": STEP, "slug": s["slug"], "title": s["title"], "type": s["type"],
               "settings": s["settings"], "visual": s["visual"],
               "body": json.dumps(body) if was else body}]}}, extra_headers=h)
print("write ok")
