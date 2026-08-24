#!/usr/bin/env python3
"""Remap the 2 inline `font-weight:600` links to 700, killing the 4th font file.

After consolidating block-level weights, 600 survived on exactly two elements —
inline `<a style="...font-weight:600...">` inside Text.p.content, which a
styles-based walker never sees. Two elements were holding a whole ~24 KiB woff2
on the critical path.

Matched structurally: only inside a `p.content` string, only `font-weight:\s*600`.
Not a bare string replace over the body — `600` appears in colours, ids and copy.
Verified counts first: step 3 content had 700 x102, 800 x16, 400 x4, 600 x2, so
exactly 2 sites are expected to change per step.
"""
import json, re, sys
sys.path.insert(0, ".")
import lf_api

FUNNEL = "fun_vGqQYxn4H2i_traYYkh4w"
STEPS = {3: "step_-42yvjxEYUC-1yAzL9TKy", 11: "step_HFrpGxiibhudWV1YLEMs1"}
PAT = re.compile(r"(font-weight:\s*)600\b")


def convert(body):
    n = [0]

    def walk(x):
        if isinstance(x, dict):
            p = x.get("p")
            if isinstance(p, dict) and isinstance(p.get("content"), str):
                new, c = PAT.subn(r"\g<1>700", p["content"])
                if c:
                    p["content"] = new
                    n[0] += c
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
assert len(node["steps"]) == 12

payload = []
for idx, uid in STEPS.items():
    if only and str(idx) != only:
        continue
    s = by_uid[uid]
    was_str = isinstance(s["body"], str)
    body = json.loads(s["body"]) if was_str else s["body"]
    c = convert(body)
    print(f"step {idx}: inline font-weight:600 -> 700 on {c} site(s)")
    assert c == 2, f"step {idx}: expected 2, got {c}"
    payload.append({"id": uid, "slug": s["slug"], "title": s["title"],
                    "type": s["type"], "settings": s["settings"],
                    "visual": s["visual"],
                    "body": json.dumps(body) if was_str else body})

lf_api.gql(tok, "mutation($id:ID!,$node:InputFunnel!){updateFunnel(id:$id,node:$node){id}}",
           {"id": FUNNEL, "node": {"steps": payload}}, extra_headers=h)
print("write ok")
