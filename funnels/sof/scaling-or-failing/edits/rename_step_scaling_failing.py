#!/usr/bin/env python3
"""Rename the step slug `event` -> `scaling-failing`.

/event/event was a duplicated segment. /event/scaling-failing reads properly on
the staging domain, and once scalingorfailing.com is assigned as the funnel's
HOME FUNNEL the funnel slug drops out of the path entirely anyway, so the entry
page sits at the domain root regardless of what the step is called.

The step keeps its product_id, so the render flushes on write rather than going
stale.
"""
import os, sys, time, urllib.request
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", "..", "..", ".."))
sys.path.insert(0, ROOT); os.chdir(ROOT)
import lf_api

FUNNEL, STEP, NEW = "fun_RoOL_WXDCAxK4hEk0v5xX", "step_5BIwggYOWxmrOPnAyaVPi", "scaling-failing"
tok  = open(".session_token").read().strip()
acct = open(".lf_account").read().strip()
h    = lf_api.session_headers(acct)
Q = '''query($id:ID!){node(id:$id){... on Funnel{slug starting_step_id steps{
      uid slug title type product_id settings visual{x y} body}}}}'''

n = lf_api.gql(tok, Q, {"id": FUNNEL}, extra_headers=h)["node"]
s = [x for x in n["steps"] if x["uid"] == STEP][0]
assert n["starting_step_id"] == STEP, "this is not the entry step - stopping"
print("before: /%s/%s  (entry)" % (n["slug"], s["slug"]))

if s["slug"] != NEW:
    lf_api.gql(tok, "mutation($id:ID!,$node:InputFunnel!){updateFunnel(id:$id,node:$node){id}}",
        {"id": FUNNEL, "node": {"steps": [{
            "id": s["uid"], "slug": NEW, "title": s["title"], "type": s["type"],
            "settings": s["settings"], "visual": s["visual"],
            "product_id": s["product_id"], "body": s["body"]}]}}, extra_headers=h)
    time.sleep(10)

n = lf_api.gql(tok, Q, {"id": FUNNEL}, extra_headers=h)["node"]
entry = [x["slug"] for x in n["steps"] if x["uid"] == n["starting_step_id"]][0]
print("after : /%s/%s  (entry)  steps=%d" % (n["slug"], entry, len(n["steps"])))

for path in ["/%s/" % n["slug"], "/%s/%s" % (n["slug"], NEW), "/%s/event" % n["slug"]]:
    try:
        r = urllib.request.urlopen(urllib.request.Request(
            "https://www.techunboxed.co" + path + "?cb=%d" % time.time(),
            headers={"User-Agent": "Mozilla/5.0", "Cache-Control": "no-cache"}), timeout=90)
        b = r.read().decode("utf-8", "replace")
        print("  %-26s HTTP %s  h1=%d sections=%d" % (path, r.status, b.count("<h1"), b.count("sof-sec")))
    except Exception as e:
        print("  %-26s %s" % (path, str(e)[:34]))
