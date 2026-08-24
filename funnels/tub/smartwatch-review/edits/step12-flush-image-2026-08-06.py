#!/usr/bin/env python3
"""Make the offer card's left image flush to the dashed border, per Figma.

In the frame the GIF sits at (2,2) — flush against the 2px stroke — fills the left
half top-to-bottom (`layoutSizingVertical: FILL`), and the badge container is
`layoutPositioning: ABSOLUTE`, so it consumes no flow height. Ours had the image
inset by three separate things: the card's 22px padding, the row's 20px gap, and
`alignItems:center` floating a fixed 300px image inside a taller row.

  card e368fdc2   padding 22 -> 0            (the image can now reach the border)
                  gap 14 -> 0                (else the badge row pushes it down)
  badge e2b4bf9c  margin {top:-22, bottom:-21}
                  With padding now 0 the old -44/+44 would sit 22px too high, and
                  it must also take ZERO flow height to keep the image at the top:
                  -22 + 43 - 21 = 0. Visual top lands at -22, matching Figma.
  row e78aa473    gap 20 -> 0, alignItems center -> stretch
  panel c91eba78  borderRadius 12 -> 0   (the card's 6px radius is the outer shape)
  image 2e0df6c9  borderRadius 12 -> 0, height 300px -> 100% so it fills the
                  stretched panel. The @767 override (320px) is left alone — when
                  the row wraps on mobile the panel has no height to inherit.
  text 2c731482   gains padding 20/28 so the copy is not against the border now
                  that the card has none. Figma insets its 237-wide content by 48
                  within a 333 column; ours is wider, so 28 is the proportionate
                  equivalent rather than a copied number.
"""
import json, sys
sys.path.insert(0, ".")
import lf_api

FUNNEL = "fun_vGqQYxn4H2i_traYYkh4w"
STEP = "step_0hL9bV7NUmyESdgkwY4Ih"

tok = open(".session_token").read().strip()
acct = open(".lf_account").read().strip()
h = lf_api.session_headers(acct)
node = lf_api.get_funnel_steps(tok, FUNNEL, extra_headers=h)
s = {x["uid"]: x for x in node["steps"]}[STEP]
was = isinstance(s["body"], str)
body = json.loads(s["body"]) if was else s["body"]

def setp(sty, prop, value, media=None):
    for st in sty:
        if isinstance(st, dict) and st.get("prop") == prop and st.get("media") == media:
            st["value"] = value
            return
    e = {"prop": prop, "value": value}
    if media:
        e["media"] = media
    sty.append(e)

PLAN = {
    "e368fdc2": [("padding", {"top": "0px", "bottom": "0px", "left": "0px", "right": "0px"}),
                 ("gap", "0px")],
    "e2b4bf9c": [("margin", {"top": "-22px", "bottom": "-21px"})],
    "e78aa473": [("gap", "0px"), ("alignItems", "stretch")],
    "c91eba78": [("borderRadius", "0px")],
    "2e0df6c9": [("borderRadius", "0px"), ("height", "100%")],
    "2c731482": [("padding", {"top": "20px", "bottom": "20px", "left": "28px", "right": "28px"})],
}
hit = []

def walk(x):
    if isinstance(x, dict):
        pid = str(x.get("id", ""))[:8]
        if pid in PLAN:
            sty = x.setdefault("styles", [])
            for prop, val in PLAN[pid]:
                setp(sty, prop, val)
            hit.append(pid)
        for v in x.values():
            walk(v)
    elif isinstance(x, list):
        for v in x:
            walk(v)

walk(body)
assert sorted(hit) == sorted(PLAN), f"matched {sorted(hit)}"
for p in PLAN:
    print(f"  {p}: {', '.join(k for k, _ in PLAN[p])}")

lf_api.gql(tok, "mutation($id:ID!,$node:InputFunnel!){updateFunnel(id:$id,node:$node){id}}",
           {"id": FUNNEL, "node": {"steps": [{
               "id": STEP, "slug": s["slug"], "title": s["title"], "type": s["type"],
               "settings": s["settings"], "visual": s["visual"],
               "body": json.dumps(body) if was else body}]}}, extra_headers=h)
print("write ok")
