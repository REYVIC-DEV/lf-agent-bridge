#!/usr/bin/env python3
"""Stop the flush image covering the card's rounded dashed corners.

Measured: card border-box left 16.0 with a 2px border, so the inner edge is at
18.0 — and the image panel starts at exactly 18.0. It is NOT overlapping the
border's straight edges. The problem is only the corners: the panel had
borderRadius 0 while the card has 6px, so its square corner fills the area where
the dashed border curves, which reads as the image cutting through the border.

The inner radius of a 6px border-radius with a 2px border is 6 - 2 = 4px, so 4px
on the panel (and the image inside it) follows the card's curve exactly. The
panel's right corners sit against the white text column on white card
background, so rounding them too is invisible — no need for per-corner values,
which LF may not accept as a multi-value string anyway.

`overflow:hidden` on the card would also clip the image to the rounded shape, but
it would equally clip the LAUNCH SALE badge, which deliberately extends 22px above
the card. Rejected for that reason.
"""
import json, sys
sys.path.insert(0, "tools/lf-agent-bridge")
import lf_api

FUNNEL = "fun_vGqQYxn4H2i_traYYkh4w"
STEP = "step_0hL9bV7NUmyESdgkwY4Ih"
TARGETS = {"c91eba78": "image panel", "2e0df6c9": "image"}

tok = open("tools/lf-agent-bridge/.session_token").read().strip()
acct = open("tools/lf-agent-bridge/.lf_account").read().strip()
h = lf_api.session_headers(acct)
node = lf_api.get_funnel_steps(tok, FUNNEL, extra_headers=h)
s = {x["uid"]: x for x in node["steps"]}[STEP]
was = isinstance(s["body"], str)
body = json.loads(s["body"]) if was else s["body"]

hit = []

def walk(x):
    if isinstance(x, dict):
        pid = str(x.get("id", ""))[:8]
        if pid in TARGETS:
            sty = x.setdefault("styles", [])
            found = False
            for st in sty:
                if isinstance(st, dict) and st.get("prop") == "borderRadius" and "media" not in st:
                    assert st["value"] == "0px", f"{pid}: expected 0px, found {st['value']}"
                    st["value"] = "4px"
                    found = True
            if not found:
                sty.append({"prop": "borderRadius", "value": "4px"})
            hit.append(f"{TARGETS[pid]} ({pid}) -> 4px")
        for v in x.values():
            walk(v)
    elif isinstance(x, list):
        for v in x:
            walk(v)

walk(body)
assert len(hit) == 2, hit
for l in hit:
    print("  " + l)

lf_api.gql(tok, "mutation($id:ID!,$node:InputFunnel!){updateFunnel(id:$id,node:$node){id}}",
           {"id": FUNNEL, "node": {"steps": [{
               "id": STEP, "slug": s["slug"], "title": s["title"], "type": s["type"],
               "settings": s["settings"], "visual": s["visual"],
               "body": json.dumps(body) if was else body}]}}, extra_headers=h)
print("write ok")
