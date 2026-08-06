#!/usr/bin/env python3
"""Consolidate Inter to 3 weights so only 3 font files load. Design-faithful.

Each Inter weight is a separate ~24 KiB woff2 on the critical path. Measured
usage on step 3 showed two weights were nearly free to remove and one cheap:

    weight  elements  chars   -> action
    400     299       6847       keep
    500       3         26       -> 400   (~920 bytes of font per character)
    600      21        354       -> 700
    700     155       1416       keep
    800      38        675       keep
    900       1         81       -> 800   (a whole file for one headline)

25 elements change, 6 files -> 3 (~142 KiB -> ~71 KiB). Canvas-measured width
deltas were all ~1.2%: 500->400 -1.15%, 600->700 +0.72%, 900->800 -1.22%. At
12-17px the difference is invisible; the H1 at 40px is perceptible only in a
direct A/B.

Chosen over matching test3's exact loaded set {400,800,900}, which needs the same
3 files but changes 179 elements (700->800 across every bold run).

The six @font-face declarations in header_scripts are deliberately LEFT in place.
They cost nothing unless a weight is actually used, and removing them would make
any weight this script misses silently render in Arial — the regression caught on
step 11 earlier.
"""
import json, sys
sys.path.insert(0, "tools/lf-agent-bridge")
import lf_api

FUNNEL = "fun_vGqQYxn4H2i_traYYkh4w"
STEPS = {3: "step_-42yvjxEYUC-1yAzL9TKy", 11: "step_HFrpGxiibhudWV1YLEMs1"}
MAP = {"500": "400", "600": "700", "900": "800"}


def convert(body):
    hits = {}

    def walk(x):
        if isinstance(x, dict):
            for p in (x.get("styles") or []):
                if isinstance(p, dict) and p.get("prop") == "fontWeight":
                    v = str(p.get("value"))
                    if v in MAP:
                        p["value"] = MAP[v]
                        hits[v] = hits.get(v, 0) + 1
            for v in x.values():
                walk(v)
        elif isinstance(x, list):
            for v in x:
                walk(v)

    walk(body)
    return hits


tok = open("tools/lf-agent-bridge/.session_token").read().strip()
acct = open("tools/lf-agent-bridge/.lf_account").read().strip()
h = lf_api.session_headers(acct)
only = sys.argv[1] if len(sys.argv) > 1 else None

node = lf_api.get_funnel_steps(tok, FUNNEL, extra_headers=h)
by_uid = {s["uid"]: s for s in node["steps"]}
assert len(node["steps"]) == 12, f"expected 12 steps, got {len(node['steps'])}"

payload = []
for idx, uid in STEPS.items():
    if only and str(idx) != only:
        continue
    s = by_uid[uid]
    was_str = isinstance(s["body"], str)
    body = json.loads(s["body"]) if was_str else s["body"]
    hits = convert(body)
    print(f"step {idx}: remapped {sum(hits.values())} declarations {hits}")
    assert hits, f"step {idx}: nothing remapped"
    payload.append({"id": uid, "slug": s["slug"], "title": s["title"],
                    "type": s["type"], "settings": s["settings"],
                    "visual": s["visual"],
                    "body": json.dumps(body) if was_str else body})

lf_api.gql(tok, "mutation($id:ID!,$node:InputFunnel!){updateFunnel(id:$id,node:$node){id}}",
           {"id": FUNNEL, "node": {"steps": payload}}, extra_headers=h)
print("write ok")
