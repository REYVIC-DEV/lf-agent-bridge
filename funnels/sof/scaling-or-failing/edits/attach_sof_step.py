#!/usr/bin/env python3
"""Attach the detached step to the funnel, make it the entry, and publish.

createStep returns a step that funnel.steps does not list. Only updateFunnel
with the step in `steps` attaches it. InputUpdateStep wants the whole step, not
a patch: id, slug, title, type, settings, visual.
"""
import os, sys, time
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE); os.chdir(HERE)
import lf_api

FUNNEL = "fun_RoOL_WXDCAxK4hEk0v5xX"
STEP   = "step_5BIwggYOWxmrOPnAyaVPi"
SLUG   = "scaling-or-failing"
TITLE  = "Scaling or Failing - Bangkok, December 7 to 8 2026"

tok  = open(".session_token").read().strip()
acct = open(".lf_account").read().strip()
h    = lf_api.session_headers(acct)

Q = '''query($id:ID!){node(id:$id){... on Funnel{
       id name slug published starting_step_id
       steps{uid slug title type product_id}}}}'''

node = {
    "steps": [{"id": STEP, "slug": SLUG, "title": TITLE, "type": "article_page",
               "settings": {}, "visual": {"x": 90, "y": 90}}],
    "starting_step_id": STEP,
    "published": True,
}
lf_api.gql(tok, "mutation($id:ID!,$node:InputFunnel!){updateFunnel(id:$id,node:$node){id}}",
           {"id": FUNNEL, "node": node}, extra_headers=h)
print("attached, set as entry, published")
time.sleep(3)

n = lf_api.gql(tok, Q, {"id": FUNNEL}, extra_headers=h)["node"]
print("\n%s  /%s  published=%s  steps=%d" % (n["name"], n["slug"], n["published"], len(n["steps"])))
for s in n["steps"]:
    print("   %-24s %-14s product_id=%r%s" % (
        s["slug"], s["type"], s["product_id"],
        "  <== ENTRY" if s["uid"] == n["starting_step_id"] else ""))
