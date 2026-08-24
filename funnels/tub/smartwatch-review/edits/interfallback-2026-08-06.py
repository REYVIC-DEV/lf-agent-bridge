#!/usr/bin/env python3
"""Metric-matched InterFallback so the Inter swap reflows nothing. CLS -> 0.

Straight from .claude/skills/lightfunnels/references/performance.md (upstream,
verified there 89->98 mobile, CLS 0.151->0). Two halves, and both are required:

  1. the @font-face with ascent/descent/line-gap overrides + size-adjust, so the
     fallback occupies Inter's exact box  -> goes in header_scripts (<head>)
  2. every text block's fontFamily routed through `Inter, InterFallback,
     sans-serif` instead of bare `Inter`  -> this script

Confirms independently what we measured here: preload alone is not enough. Our
own preload made local CLS 0 but PSI still showed 0.158-0.163, because under
Google's throttling Inter lands after first paint regardless. The fallback makes
the swap a no-op instead of racing it.

RISK being tested on step 11 first: LF derives its Google Fonts request from the
fontFamily values, so a stack could make it request a family literally named
"Inter, InterFallback, sans-serif" and stop loading Inter at all. Upstream built
their page with the stack from the start; we are retrofitting a live page, so
verify the emitted request still contains Inter before touching step 3.
"""
import json, sys
sys.path.insert(0, ".")
import lf_api

FUNNEL = "fun_vGqQYxn4H2i_traYYkh4w"
STEPS = {3: "step_-42yvjxEYUC-1yAzL9TKy", 11: "step_HFrpGxiibhudWV1YLEMs1"}
STACK = "Inter, InterFallback, sans-serif"


def convert(body):
    n = [0]

    def walk(x):
        if isinstance(x, dict):
            for p in (x.get("styles") or []):
                # Match structurally on the styles prop, never as a bare substring:
                # "Inter" also appears inside copy and inside JetBrains Mono blocks.
                if isinstance(p, dict) and p.get("prop") == "fontFamily" \
                        and p.get("value") == "Inter":
                    p["value"] = STACK
                    n[0] += 1
            for v in x.values():
                walk(v)
        elif isinstance(x, list):
            for v in x:
                walk(v)

    walk(body)
    return n[0]


tok = open(".session_token").read().strip()
acct = open(".lf_account").read().strip()
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
    c = convert(body)
    print(f"step {idx}: fontFamily Inter -> stack on {c} declarations")
    assert c > 250, f"step {idx}: only {c} rewritten, expected ~307"
    payload.append({"id": uid, "slug": s["slug"], "title": s["title"],
                    "type": s["type"], "settings": s["settings"],
                    "visual": s["visual"],
                    "body": json.dumps(body) if was_str else body})

lf_api.gql(tok, "mutation($id:ID!,$node:InputFunnel!){updateFunnel(id:$id,node:$node){id}}",
           {"id": FUNNEL, "node": {"steps": payload}}, extra_headers=h)
print("write ok")
