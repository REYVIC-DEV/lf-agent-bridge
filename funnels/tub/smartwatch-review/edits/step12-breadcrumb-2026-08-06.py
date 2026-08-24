#!/usr/bin/env python3
"""Link step 12's breadcrumb. Was three plain <span>s with no anchors.

Targets match step 3 (the URLs only — no markup copied):
    Home      -> https://blog.techunboxed.co/
    Wearables -> https://blog.techunboxed.co/category/wearables
    "Best Fitness Trackers of 2026" stays unlinked — it is the current page, and
    linking the trailing crumb to itself is the usual breadcrumb mistake.

`color:inherit` keeps the existing crumb colours, so this is purely additive:
the two words become clickable and nothing changes visually except the cursor.
"""
import json, sys
sys.path.insert(0, ".")
import lf_api

FUNNEL = "fun_vGqQYxn4H2i_traYYkh4w"
STEP = "step_0hL9bV7NUmyESdgkwY4Ih"
BLOCK = "b8284425"
A = 'cursor:pointer;color:inherit;text-decoration:none'
LINKS = {
    "Home": "https://blog.techunboxed.co/",
    "Wearables": "https://blog.techunboxed.co/category/wearables",
}

tok = open(".session_token").read().strip()
acct = open(".lf_account").read().strip()
h = lf_api.session_headers(acct)
node = lf_api.get_funnel_steps(tok, FUNNEL, extra_headers=h)
s = {x["uid"]: x for x in node["steps"]}[STEP]
was_str = isinstance(s["body"], str)
body = json.loads(s["body"]) if was_str else s["body"]

done = []

def walk(x):
    if isinstance(x, dict):
        if str(x.get("id", ""))[:8] == BLOCK:
            p = x.get("p") or {}
            c = p.get("content") or ""
            assert "Wearables" in c, f"unexpected block content: {c[:80]}"
            assert "<a " not in c, "breadcrumb already has anchors — aborting"
            new = c
            for word, url in LINKS.items():
                # only the exact crumb span, so the word can't be hit elsewhere
                old = f'>{word}</span>'
                assert old in new, f"crumb {word!r} not found"
                new = new.replace(old, f'><a href="{url}" style="{A}">{word}</a></span>', 1)
            p["content"] = new
            done.append(x["id"][:8])
        for v in x.values():
            walk(v)
    elif isinstance(x, list):
        for v in x:
            walk(v)

walk(body)
assert len(done) == 1, f"expected 1 block, matched {done}"
print("breadcrumb linked on", done[0])

lf_api.gql(tok, "mutation($id:ID!,$node:InputFunnel!){updateFunnel(id:$id,node:$node){id}}",
           {"id": FUNNEL, "node": {"steps": [{
               "id": STEP, "slug": s["slug"], "title": s["title"], "type": s["type"],
               "settings": s["settings"], "visual": s["visual"],
               "body": json.dumps(body) if was_str else body}]}}, extra_headers=h)
print("write ok")
