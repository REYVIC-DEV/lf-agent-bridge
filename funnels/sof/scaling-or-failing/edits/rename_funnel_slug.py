#!/usr/bin/env python3
"""Rename the funnel slug scaling-or-failing -> event.

The URL is always /<funnel-slug>/<step-slug>: no funnel in this account has a
store attached, so domains bind at workspace level and the funnel slug is always
a path segment. On scalingorfailing.com that made the old slug redundant
(scalingorfailing.com/scaling-or-failing/event).

With the funnel slug `event` and the step as the ENTRY step, the canonical URL
is the funnel root: scalingorfailing.com/event/ — which is what was asked for.
The step slug stays `event` so LF_ALLOW_REDEPLOY and the builder's STEP_SLUG
need no change.
"""
import os, sys, time, urllib.request
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", "..", "..", ".."))
sys.path.insert(0, ROOT); os.chdir(ROOT)
import lf_api

FUNNEL, NEW = "fun_RoOL_WXDCAxK4hEk0v5xX", "event"
tok  = open(".session_token").read().strip()
acct = open(".lf_account").read().strip()
h    = lf_api.session_headers(acct)

# a slug collision would silently take the other funnel's URL
clash = [e["node"] for e in lf_api.gql(
    tok, '{funnels(first:100,query:""){edges{node{id name slug}}}}', {}, extra_headers=h
    )["funnels"]["edges"] if e["node"]["slug"] == NEW and e["node"]["id"] != FUNNEL]
if clash:
    sys.exit("SLUG TAKEN by %s - pick another" % clash[0]["name"])
print("slug '%s' is free" % NEW)

Q = 'query($id:ID!){node(id:$id){... on Funnel{name slug published starting_step_id steps{uid slug}}}}'
n = lf_api.gql(tok, Q, {"id": FUNNEL}, extra_headers=h)["node"]
print("before: /%s/%s" % (n["slug"], [s["slug"] for s in n["steps"] if s["uid"] == n["starting_step_id"]][0]))

lf_api.gql(tok, "mutation($id:ID!,$node:InputFunnel!){updateFunnel(id:$id,node:$node){id}}",
           {"id": FUNNEL, "node": {"slug": NEW}}, extra_headers=h)
time.sleep(8)
n = lf_api.gql(tok, Q, {"id": FUNNEL}, extra_headers=h)["node"]
entry = [s["slug"] for s in n["steps"] if s["uid"] == n["starting_step_id"]][0]
print("after : /%s/%s   published=%s" % (n["slug"], entry, n["published"]))

for path in ["/%s/" % n["slug"], "/%s/%s" % (n["slug"], entry), "/scaling-or-failing/"]:
    u = "https://www.techunboxed.co" + path
    try:
        r = urllib.request.urlopen(urllib.request.Request(
            u + "?cb=%d" % time.time(),
            headers={"User-Agent": "Mozilla/5.0", "Cache-Control": "no-cache"}), timeout=90)
        b = r.read().decode("utf-8", "replace")
        print("  %-34s HTTP %s  %7db  h1=%d" % (path, r.status, len(b), b.count("<h1")))
    except Exception as e:
        print("  %-34s %s" % (path, str(e)[:40]))
