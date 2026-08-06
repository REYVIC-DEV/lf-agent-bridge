#!/usr/bin/env python3
"""Drop the dead Roboto font: 6 BlockLink wrappers -> Inter.

The page requests Roboto (~22 KiB, one of 8 font files on the critical path) but
**renders no visible text in it**. Verified on the live page by walking every
leaf element's computed fontFamily: Inter 517, JetBrains Mono 1 ("Disclaimer"),
Roboto 0. All six declarations are on `BlockLink` wrappers whose Container/Text
children set their own family, so the wrapper's font never reaches a glyph.

This matters because the page is bandwidth-bound at first paint: 473 of 521 KiB
is requested in the first 400ms, and whether the fonts beat the images decides
CLS (0 vs 0.163) and LCP (1.8 vs 3.1s) — a 84-93 score swing. Every font file
removed from that window makes the good outcome more likely.

Same fix already applied to meta-uk, where the identical pattern was 9 wrappers.
"""
import json, sys
sys.path.insert(0, "tools/lf-agent-bridge")
import lf_api

FUNNEL = "fun_vGqQYxn4H2i_traYYkh4w"
STEPS = {3: "step_-42yvjxEYUC-1yAzL9TKy", 11: "step_HFrpGxiibhudWV1YLEMs1"}


def convert(body):
    hit = []

    def walk(x):
        if isinstance(x, dict):
            for p in (x.get("styles") or []):
                if isinstance(p, dict) and p.get("prop") == "fontFamily" \
                        and p.get("value") == "Roboto":
                    p["value"] = "Inter"
                    hit.append((x.get("t"), x.get("id", "")[:8]))
            for v in x.values():
                walk(v)
        elif isinstance(x, list):
            for v in x:
                walk(v)

    walk(body)
    return hit


tok = open("tools/lf-agent-bridge/.session_token").read().strip()
acct = open("tools/lf-agent-bridge/.lf_account").read().strip()
h = lf_api.session_headers(acct)
node = lf_api.get_funnel_steps(tok, FUNNEL, extra_headers=h)
by_uid = {s["uid"]: s for s in node["steps"]}
assert len(node["steps"]) == 12, f"expected 12 steps, got {len(node['steps'])}"

payload = []
for idx, uid in STEPS.items():
    s = by_uid[uid]
    was_str = isinstance(s["body"], str)
    body = json.loads(s["body"]) if was_str else s["body"]
    hit = convert(body)
    print(f"step {idx}: Roboto -> Inter on {len(hit)} blocks {hit}")
    assert len(hit) == 6, f"step {idx}: expected 6, got {len(hit)}"
    payload.append({"id": uid, "slug": s["slug"], "title": s["title"],
                    "type": s["type"], "settings": s["settings"],
                    "visual": s["visual"],
                    "body": json.dumps(body) if was_str else body})

lf_api.gql(tok, "mutation($id:ID!,$node:InputFunnel!){updateFunnel(id:$id,node:$node){id}}",
           {"id": FUNNEL, "node": {"steps": payload}}, extra_headers=h)
print("write ok")
