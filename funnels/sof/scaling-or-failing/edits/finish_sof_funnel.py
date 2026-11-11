#!/usr/bin/env python3
"""createFunnel leaves the funnel empty and unpublished. Add the step, attach it
as the entry, then publish.

createStep and updateFunnel are NOT atomic: a step that is created but never
listed in updateFunnel exists detached and is invisible to funnel.steps, so the
page simply does not render. Hence the read-back at every stage.
"""
import os, sys, time
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE); os.chdir(HERE)
import lf_api

FUNNEL = "fun_RoOL_WXDCAxK4hEk0v5xX"
SLUG   = "scaling-or-failing"
TITLE  = "Scaling or Failing - Bangkok, December 7 to 8 2026"
APPLY  = "--apply" in sys.argv

tok  = open(".session_token").read().strip()
acct = open(".lf_account").read().strip()
h    = lf_api.session_headers(acct)

Q = '''query($id:ID!){node(id:$id){... on Funnel{
       id name slug published starting_step_id
       steps{uid slug title type product_id}}}}'''
n = lf_api.gql(tok, Q, {"id": FUNNEL}, extra_headers=h)["node"]
print("before: %s  /%s  published=%s  steps=%d" % (n["name"], n["slug"], n["published"], len(n["steps"])))

if not APPLY:
    sys.exit("(dry run - nothing written)")

if not any(s["slug"] == SLUG for s in n["steps"]):
    node = {"slug": SLUG, "title": TITLE, "type": "article_page",
            "settings": {}, "visual": {"x": 90, "y": 90}}
    r = lf_api.gql(tok,
        "mutation($funnel_id:ID!,$node:InputStep!){createStep(funnel_id:$funnel_id,node:$node)"
        "{step{uid slug title type}}}",
        {"funnel_id": FUNNEL, "node": node}, extra_headers=h)["createStep"]["step"]
    print("created step %s (%s)" % (r["uid"], r["slug"]))
    time.sleep(2)
    n = lf_api.gql(tok, Q, {"id": FUNNEL}, extra_headers=h)["node"]

step = [s for s in n["steps"] if s["slug"] == SLUG][0]

if n["starting_step_id"] != step["uid"] or not n["published"]:
    lf_api.gql(tok,
        "mutation($id:ID!,$node:InputFunnel!){updateFunnel(id:$id,node:$node){id}}",
        {"id": FUNNEL, "node": {"starting_step_id": step["uid"], "published": True}},
        extra_headers=h)
    print("set entry step and published")
    time.sleep(3)

n = lf_api.gql(tok, Q, {"id": FUNNEL}, extra_headers=h)["node"]
print("\nafter: %s  /%s  published=%s" % (n["name"], n["slug"], n["published"]))
for s in n["steps"]:
    print("   %-24s %-14s product_id=%r%s" % (
        s["slug"], s["type"], s["product_id"],
        "  <== ENTRY" if s["uid"] == n["starting_step_id"] else ""))
print("\nURL: https://www.techunboxed.co/%s/%s" % (n["slug"], SLUG))
