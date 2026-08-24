#!/usr/bin/env python3
"""Step 12 footer polish: centre the row, and stop the theme throwing on href="#".

1. CENTRE. Block 5eeedf5b had `textAlign: left` for desktop and already
   `center` @767. It used to share a flex row with the social icons, so left was
   right then; with the icons gone it is the only child (flex:1) and the design
   calls for centred. Only the desktop entry changes — the mobile override was
   already correct.

2. href="#" -> href="#tu-terms" etc. The theme registers its own click handler on
   every anchor and runs `document.querySelector(a.getAttribute('href'))`, so a
   bare "#" throws `'#' is not a valid selector`. Pre-existing (the page shipped 9
   such links) but these four are now actually clicked, so it fired on every
   policy click. Pointing each at its overlay id gives the theme a real element to
   find. The popup's own handler still calls preventDefault, so nothing scrolls —
   verified after.
"""
import json, sys
sys.path.insert(0, ".")
import lf_api

FUNNEL = "fun_vGqQYxn4H2i_traYYkh4w"
STEP = "step_0hL9bV7NUmyESdgkwY4Ih"
BLOCK = "5eeedf5b"
OVERLAY = {"terms": "tu-terms", "priv": "tu-priv", "edit": "tu-edit", "aff": "tu-aff"}

tok = open(".session_token").read().strip()
acct = open(".lf_account").read().strip()
h = lf_api.session_headers(acct)
node = lf_api.get_funnel_steps(tok, FUNNEL, extra_headers=h)
s = {x["uid"]: x for x in node["steps"]}[STEP]
was = isinstance(s["body"], str)
body = json.loads(s["body"]) if was else s["body"]

log = {"hrefs": 0, "align": 0}

def walk(x):
    if isinstance(x, dict):
        # scope by block id — 'id="terms"' also appears in the popup block's comment
        if str(x.get("id", ""))[:8] == BLOCK:
            p = x.get("p") or {}
            c = p["content"]
            for tid, ov in OVERLAY.items():
                old = f'<a href="#" id="{tid}"'
                assert old in c, f"{tid}: {old!r} not found"
                c = c.replace(old, f'<a href="#{ov}" id="{tid}"', 1)
                log["hrefs"] += 1
            p["content"] = c
            for st in (x.get("styles") or []):
                # desktop entry only; the @767 override is already center
                if st.get("prop") == "textAlign" and "media" not in st:
                    assert st["value"] == "left", f"unexpected {st['value']!r}"
                    st["value"] = "center"
                    log["align"] += 1
        for v in x.values():
            walk(v)
    elif isinstance(x, list):
        for v in x:
            walk(v)

walk(body)
assert log == {"hrefs": 4, "align": 1}, log
print("hrefs repointed:", log["hrefs"], "| desktop textAlign -> center")

lf_api.gql(tok, "mutation($id:ID!,$node:InputFunnel!){updateFunnel(id:$id,node:$node){id}}",
           {"id": FUNNEL, "node": {"steps": [{
               "id": STEP, "slug": s["slug"], "title": s["title"], "type": s["type"],
               "settings": s["settings"], "visual": s["visual"],
               "body": json.dumps(body) if was else body}]}}, extra_headers=h)
print("write ok")
