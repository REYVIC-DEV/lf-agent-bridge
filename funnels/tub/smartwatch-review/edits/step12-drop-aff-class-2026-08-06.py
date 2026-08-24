#!/usr/bin/env python3
"""Drop the aff-* className from step 12, keeping the direct Amazon URLs.

Rationale (owner's call): with the URL already on the button there is nothing for
the header's replacer to do, so don't give it a hook. One less runtime DOM
mutation, and the link is correct in the served HTML — works with JS disabled,
with the script blocked by an ad blocker, and for crawlers.

The trade-off, stated plainly: the funnel-level AFFILIATE map stops being the
single source of truth for THIS step. Rotating a product URL later means editing
these buttons, not one line in the header. That is exactly how step 3's inline
URLs went stale — verified: all 8 of step 3's destinations no longer match the
live map. The mitigation is that attribution does not rot even if the deep link
does: `tag=techunboxed04-20` is in the URL, so a stale link still earns.

URLs were read from the LIVE header_scripts AFFILIATE map (not from step 3's
stale bodies) and each was verified equal to its map value before this ran.
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
was_str = isinstance(s["body"], str)
body = json.loads(s["body"]) if was_str else s["body"]

dropped = []

def walk(x):
    if isinstance(x, dict):
        if x.get("t") in ("BlockLink", "Link"):
            p = x.get("p") or {}
            cls = p.get("className")
            if isinstance(cls, str) and cls.startswith("aff-"):
                d = p.get("destination")
                dv = d.get("value") if isinstance(d, dict) else d
                # never strip the hook off a button that has no real link
                assert dv and dv != "#" and "amazon." in dv, \
                    f"{x['id'][:8]}: refusing to drop {cls} — destination is {dv!r}"
                p.pop("className")
                dropped.append((x["id"][:8], cls))
        for v in x.values():
            walk(v)
    elif isinstance(x, list):
        for v in x:
            walk(v)

walk(body)
assert len(dropped) == 8, f"expected 8, got {len(dropped)}"
for i, c in dropped:
    print(f"  {i}  dropped {c}  (direct URL kept)")

lf_api.gql(tok, "mutation($id:ID!,$node:InputFunnel!){updateFunnel(id:$id,node:$node){id}}",
           {"id": FUNNEL, "node": {"steps": [{
               "id": STEP, "slug": s["slug"], "title": s["title"], "type": s["type"],
               "settings": s["settings"], "visual": s["visual"],
               "body": json.dumps(body) if was_str else body}]}}, extra_headers=h)
print("write ok")
