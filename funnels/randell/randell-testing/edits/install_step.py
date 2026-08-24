#!/usr/bin/env python3
"""Install/refresh the currency script on one step. Usage: install_step.py <step_uid>

APPEND after a marker, never replace the whole header: it carries the Inter
@font-face declarations the page depends on. Idempotent - a second run swaps
the script rather than stacking a duplicate copy.
"""
import sys, time
sys.path.insert(0, ".")
import lf_api

FUNNEL = "fun_f1IsXx3YnEA2UD2g91dAv"
STEP = sys.argv[1]
MARK = "<!-- dynamic-currency -->"

script = open("dynamic-currency-header-block.html", encoding="utf-8").read()
tok = open(".session_token").read().strip()
acct = open(".lf_account").read().strip()
h = lf_api.session_headers(acct)

def go(fn):
    for a in range(5):
        try:
            return fn()
        except Exception as e:
            if "502" in str(e) or "Bad Gateway" in str(e):
                print("  502, backing off"); time.sleep(70); continue
            raise
    raise RuntimeError("gave up after 502 retries")

node = go(lambda: lf_api.get_funnel_steps(tok, FUNNEL, extra_headers=h))
s = {x["uid"]: x for x in node["steps"]}[STEP]
st = s["settings"]; ch = st.setdefault("custom_html", {})
head = ch.get("header") or ""
had_inter = "@font-face" in head
before = len(head)
head = head.split(MARK)[0].rstrip() if MARK in head else head
ch["header"] = head + "\n" + MARK + "\n" + script
if had_inter:
    assert "@font-face" in ch["header"], "lost the font faces - refusing"
print("%s: header %d -> %d, inter=%s" % (s["slug"], before, len(ch["header"]), had_inter))

go(lambda: lf_api.gql(tok,
    "mutation($id:ID!,$node:InputFunnel!){updateFunnel(id:$id,node:$node){id}}",
    {"id": FUNNEL, "node": {"steps": [{
        "id": STEP, "slug": s["slug"], "title": s["title"], "type": s["type"],
        "settings": st, "visual": s["visual"], "body": s["body"]}]}},
    extra_headers=h))
print("installed")
