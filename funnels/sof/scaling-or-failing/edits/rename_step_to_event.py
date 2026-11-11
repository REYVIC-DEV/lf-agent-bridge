#!/usr/bin/env python3
"""Rename the step slug from scaling-or-failing to event.

/scaling-or-failing/scaling-or-failing was redundant. The entry step also serves
at the funnel root, so the clean URL is unaffected either way.
"""
import os, sys, time
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", "..", "..", ".."))
sys.path.insert(0, ROOT); os.chdir(ROOT)
import lf_api

FUNNEL, STEP, NEW = "fun_RoOL_WXDCAxK4hEk0v5xX", "step_5BIwggYOWxmrOPnAyaVPi", "event"
tok  = open(".session_token").read().strip()
acct = open(".lf_account").read().strip()
h    = lf_api.session_headers(acct)
Q = '''query($id:ID!){node(id:$id){... on Funnel{slug starting_step_id
      steps{uid slug title type product_id settings visual{x y}}}}}'''

n = lf_api.gql(tok, Q, {"id": FUNNEL}, extra_headers=h)["node"]
s = [x for x in n["steps"] if x["uid"] == STEP][0]
print("before: /%s/%s" % (n["slug"], s["slug"]))
if s["slug"] != NEW:
    lf_api.gql(tok, "mutation($id:ID!,$node:InputFunnel!){updateFunnel(id:$id,node:$node){id}}",
        {"id": FUNNEL, "node": {"steps": [{
            "id": s["uid"], "slug": NEW, "title": s["title"], "type": s["type"],
            "settings": s["settings"], "visual": s["visual"],
            "product_id": s["product_id"]}]}}, extra_headers=h)
    time.sleep(3)
n = lf_api.gql(tok, Q, {"id": FUNNEL}, extra_headers=h)["node"]
for x in n["steps"]:
    print("after : /%s/%s%s" % (n["slug"], x["slug"],
          "  <== ENTRY" if x["uid"] == n["starting_step_id"] else ""))
