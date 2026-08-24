#!/usr/bin/env python3
"""Repair bh-advertorial-v1-dyn's header.

Two defects, one write:

1. TWO copies of the currency script were installed. The first install used no
   marker, so the marker-split in install_step.py could not find it and simply
   appended a second copy. Both fetch and both write the same nodes, so the
   displayed price depended on which response landed last - and only one copy
   has trimZeros. Byte map proved the old copy is the whole 0..7254 range.

2. That header carries NO @font-face, while its source step bh-advertorial-v1
   has 7. The copy has been rendering in Arial, so it was never 1:1.

Rebuilt as: the source step's header (the Inter block) + marker + ONE script.
"""
import sys, time
sys.path.insert(0, ".")
import lf_api

FUNNEL = "fun_f1IsXx3YnEA2UD2g91dAv"
SRC = "step_0J0wlCl2Z6O6Hfg1S-wkY"      # bh-advertorial-v1, the entry
DST = "step_SmIVoc258ZchgIHKzFlo-"      # bh-advertorial-v1-dyn
MARK = "<!-- dynamic-currency -->"

script = open("dynamic-currency-header-block.html", encoding="utf-8").read()
tok = open(".session_token").read().strip()
acct = open(".lf_account").read().strip()
h = lf_api.session_headers(acct)

def go(fn):
    for _ in range(5):
        try:
            return fn()
        except Exception as e:
            if "502" in str(e) or "Bad Gateway" in str(e):
                print("  502, backing off"); time.sleep(70); continue
            raise
    raise RuntimeError("gave up")

node = go(lambda: lf_api.get_funnel_steps(tok, FUNNEL, extra_headers=h))
by = {x["uid"]: x for x in node["steps"]}
src_head = by[SRC]["settings"]["custom_html"]["header"]
assert src_head.count("@font-face") == 7, src_head.count("@font-face")
assert "applyPrices" not in src_head, "source unexpectedly carries the script"

d = by[DST]
new_head = src_head.rstrip() + "\n" + MARK + "\n" + script
assert new_head.count("function applyPrices") == 1
assert new_head.count("function trimZeros") == 1
assert new_head.count("@font-face") == 7
print("header %d -> %d  (1 script, 7 font faces)" % (
    len(d["settings"]["custom_html"]["header"]), len(new_head)))

d["settings"]["custom_html"]["header"] = new_head
go(lambda: lf_api.gql(tok,
    "mutation($id:ID!,$node:InputFunnel!){updateFunnel(id:$id,node:$node){id}}",
    {"id": FUNNEL, "node": {"steps": [{
        "id": DST, "slug": d["slug"], "title": d["title"], "type": d["type"],
        "settings": d["settings"], "visual": d["visual"], "body": d["body"]}]}},
    extra_headers=h))
print("repaired")
