#!/usr/bin/env python3
"""Flush the stale render on the `event` step by writing step metadata.

The two steps hold BYTE-IDENTICAL bodies, yet /event served none of the content
while /event-v2 served all of it. The difference is history, not data: `event`
had already been rendered while it was empty, and kept serving that render.
`event-v2` was created after the content existed, so its first render was right.

A metadata write is the known way to bust it. `product_id` is the field that
worked elsewhere in this account. prod_8Bx8YDUlacGSfOHEMCXgD is titled
"TechUnboxed" and is the generic product every advertorial here carries, not a
specific item, and this page displays no product data at all (tickets are sold
on Whova), so attaching it changes nothing a visitor sees.
"""
import os, sys, time, json, urllib.request
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", "..", "..", ".."))
sys.path.insert(0, ROOT); os.chdir(ROOT)
import lf_api

FUNNEL, STEP, PROD = "fun_RoOL_WXDCAxK4hEk0v5xX", "step_5BIwggYOWxmrOPnAyaVPi", "prod_8Bx8YDUlacGSfOHEMCXgD"
URL = "https://www.techunboxed.co/scaling-or-failing/event"
tok  = open(".session_token").read().strip()
acct = open(".lf_account").read().strip()
h    = lf_api.session_headers(acct)
Q = '''query($id:ID!){node(id:$id){... on Funnel{steps{
      uid slug title type product_id settings visual{x y} body}}}}'''

def served():
    r = urllib.request.urlopen(urllib.request.Request(
        URL + "?cb=%d" % time.time(),
        headers={"User-Agent": "Mozilla/5.0", "Cache-Control": "no-cache"}), timeout=90)
    b = r.read().decode("utf-8", "replace")
    return len(b), b.count("sof-sec"), b.count("<h1")

print("before: bytes=%d sof-sec=%d h1=%d" % served())

n = lf_api.gql(tok, Q, {"id": FUNNEL}, extra_headers=h)["node"]
s = [x for x in n["steps"] if x["uid"] == STEP][0]
lf_api.gql(tok, "mutation($id:ID!,$node:InputFunnel!){updateFunnel(id:$id,node:$node){id}}",
    {"id": FUNNEL, "node": {"steps": [{
        "id": s["uid"], "slug": s["slug"], "title": s["title"], "type": s["type"],
        "settings": s["settings"], "visual": s["visual"],
        "product_id": PROD, "body": s["body"]}]}}, extra_headers=h)
print("attached product_id=%s" % PROD)
time.sleep(12)
print("after : bytes=%d sof-sec=%d h1=%d" % served())
