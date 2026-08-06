#!/usr/bin/env python3
"""Match the Trustpilot line to Figma text node 557:6522, per-run.

Its `fontName` is "mixed" and `textDecoration` "mixed" — the styling is per
segment, which a screenshot cannot tell you and a plain-text copy loses:

    "Rated "      Inter Regular 12px  #000000  NONE
    "Excellent"   Inter Bold    12px  #000000  UNDERLINE   <- we had it plain
    " (4.5) on "  Inter Regular 12px  #000000  NONE

Also fixes two values that were close-but-wrong: colour #111827 -> #000000 and
line-height 18px -> 19.2px (Figma's exact value).
"""
import json, re, sys
sys.path.insert(0, "tools/lf-agent-bridge")
import lf_api

FUNNEL = "fun_vGqQYxn4H2i_traYYkh4w"
STEP = "step_0hL9bV7NUmyESdgkwY4Ih"
BLOCK = "c409efac"

tok = open("tools/lf-agent-bridge/.session_token").read().strip()
acct = open("tools/lf-agent-bridge/.lf_account").read().strip()
h = lf_api.session_headers(acct)
node = lf_api.get_funnel_steps(tok, FUNNEL, extra_headers=h)
s = {x["uid"]: x for x in node["steps"]}[STEP]
was = isinstance(s["body"], str)
body = json.loads(s["body"]) if was else s["body"]

done = []

def walk(x):
    if isinstance(x, dict):
        if str(x.get("id", ""))[:8] == BLOCK:
            p = x.get("p") or {}
            c = p.get("content") or ""
            plain = re.sub(r"<[^>]+>", "", c)
            assert "Excellent" in plain, plain[:60]
            assert "<b>" not in c and "<u>" not in c, f"already styled: {c[:80]}"
            # bold + underline only the word, leaving the rest as-is
            c = c.replace("Excellent", "<b><u>Excellent</u></b>", 1)
            p["content"] = c
            sty = x.setdefault("styles", [])
            for st in sty:
                if not isinstance(st, dict) or "media" in st:
                    continue
                if st.get("prop") == "color":
                    st["value"] = {"r": 0, "g": 0, "b": 0, "a": 1}
                elif st.get("prop") == "lineHeight":
                    st["value"] = "19.2px"
            done.append(c)
        for v in x.values():
            walk(v)
    elif isinstance(x, list):
        for v in x:
            walk(v)

walk(body)
assert len(done) == 1, done
print("  content:", done[0])
print("  color -> #000000, lineHeight -> 19.2px")

lf_api.gql(tok, "mutation($id:ID!,$node:InputFunnel!){updateFunnel(id:$id,node:$node){id}}",
           {"id": FUNNEL, "node": {"steps": [{
               "id": STEP, "slug": s["slug"], "title": s["title"], "type": s["type"],
               "settings": s["settings"], "visual": s["visual"],
               "body": json.dumps(body) if was else body}]}}, extra_headers=h)
print("write ok")
