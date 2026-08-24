#!/usr/bin/env python3
"""Wire step 12's eight dead "VISIT AMAZON" buttons to real affiliate URLs.

They all pointed at `#`. Step 3 already solves this with BOTH mechanisms, and
this mirrors it exactly:

  1. `destination` = the full Amazon URL, tag=techunboxed04-20 already embedded.
     This is what actually earns commission, and it works with JS disabled, with
     the header script blocked by an ad blocker, and for crawlers.
  2. `className` = the matching `aff-*` key. The funnel's header script re-asserts
     the URL from its AFFILIATE map on load, so a URL can still be rotated in one
     place later without editing eight buttons.

Belt and braces on purpose: the class alone leaves the button dead whenever the
script does not run, which on affiliate traffic is a non-trivial slice.

Product mapping derived from document order and cross-checked two ways — the
comparison table at the top and the numbered detail sections below both yield the
same pairing, two buttons per product:

    9.0/10 + "2. Whoop 5.0 Peak"       -> aff-whoop
    7.9/10 + "3. Apple Watch SE 3"     -> aff-apple-watch
    7.5/10 + "4. Garmin Vivoactive 6"  -> aff-garmin
    5.9/10 + "5. Fitbit Charge 6"      -> aff-fitbit

Nothing is copied from another step: only the URL values are reused, taken from
the funnel-level AFFILIATE map that already governs every other step.
"""
import json, sys
sys.path.insert(0, ".")
import lf_api

FUNNEL = "fun_vGqQYxn4H2i_traYYkh4w"
STEP = "step_0hL9bV7NUmyESdgkwY4Ih"
AFF = json.load(open(sys.argv[1] + "/aff.json", encoding="utf-8"))

# 8-char id prefix -> affiliate key
MAP = {
    "a4c90efd": "aff-whoop",       "58c2832b": "aff-whoop",
    "d659e494": "aff-apple-watch", "44459cd0": "aff-apple-watch",
    "63cb7e08": "aff-garmin",      "2bcef022": "aff-garmin",
    "9c79cde4": "aff-fitbit",      "bd947d7d": "aff-fitbit",
}

tok = open(".session_token").read().strip()
acct = open(".lf_account").read().strip()
h = lf_api.session_headers(acct)
node = lf_api.get_funnel_steps(tok, FUNNEL, extra_headers=h)
by = {s["uid"]: s for s in node["steps"]}
assert STEP in by, "step 12 not found"
s = by[STEP]
was_str = isinstance(s["body"], str)
body = json.loads(s["body"]) if was_str else s["body"]

hits = []

def walk(x):
    if isinstance(x, dict):
        if x.get("t") in ("BlockLink", "Link"):
            key = MAP.get(str(x.get("id", ""))[:8])
            if key:
                p = x.setdefault("p", {})
                d = p.get("destination")
                before = d.get("value") if isinstance(d, dict) else d
                assert before == "#", f"{x['id'][:8]}: expected '#', found {before!r}"
                if isinstance(d, dict):
                    d["value"] = AFF[key]
                else:
                    p["destination"] = {"type": "static", "value": AFF[key]}
                p["className"] = key
                p.setdefault("target", "_blank")
                hits.append((x["id"][:8], key))
        for v in x.values():
            walk(v)
    elif isinstance(x, list):
        for v in x:
            walk(v)

walk(body)
assert len(hits) == 8, f"expected 8 buttons, wired {len(hits)}: {hits}"
for i, k in hits:
    print(f"  {i} -> {k}")

lf_api.gql(tok, "mutation($id:ID!,$node:InputFunnel!){updateFunnel(id:$id,node:$node){id}}",
           {"id": FUNNEL, "node": {"steps": [{
               "id": STEP, "slug": s["slug"], "title": s["title"], "type": s["type"],
               "settings": s["settings"], "visual": s["visual"],
               "body": json.dumps(body) if was_str else body}]}}, extra_headers=h)
print("write ok")
