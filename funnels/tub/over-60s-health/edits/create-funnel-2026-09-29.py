#!/usr/bin/env python3
"""Create the over-60s health funnel that the two Meta lead-swap tests live in.

ONE FUNNEL, TWO TESTS. Matches the tub-allsmartring-meta precedent, which holds
two separate test trios (oura-vs-hlth/-v2/-v3 and smart-ring-era-*/-v2/-v3) in a
single funnel. Both of these are over-60s health, different angles:

    V-B (gadgets)     ClickUp z941abwj4k  2-way, control + B5   <- building now
    V-A (smartwatch)  ClickUp z941abwj4j  control + A1 (+A3)    <- later

Each test gets its OWN entry step, its own redirect snippet and its own PostHog
experiment. A funnel has one starting_step_id, but that only sets the canvas
entry - ads point at a specific step URL, so a second test's entry is just a
normal step. The smart-ring funnel already works that way.

⚠️ THE FUNNEL IS CREATED PUBLISHED, DELIBERATELY.
   A brand-new funnel starts unpublished, which makes its pages unreachable -
   and the QA runbook measures a LIVE url. PSI fetches from Google's servers and
   ?preview=true is not a substitute. So an unpublished funnel cannot be QA'd at
   all. Publishing a funnel with no steps and no traffic risks nothing existing.

⚠️ EVERY PAGE SHIPS noindex,nofollow UNTIL A HUMAN HAS LOOKED.
   Published means publicly reachable, and these are half-built advertorials on
   an indexed domain. The noindex comes off as a deliberate, separate step after
   review - never as part of a build.
"""
import json
import os
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", "..", "..", ".."))
sys.path.insert(0, ROOT)
os.chdir(ROOT)
import lf_api  # noqa: E402

NAME = "TUB - Over-60s health - Meta"
SLUG = "over-60s-health"
CURRENCY = "GBP"
LANG = "en"

DRY = "--dry-run" in sys.argv

tok = open(".session_token").read().strip()
acct = open(".lf_account").read().strip()
h = lf_api.session_headers(acct)


def go(fn, tries=6):
    delay = 30
    for _ in range(tries):
        try:
            return fn()
        except Exception as e:
            m = str(e)
            if "expired" in m.lower():
                sys.exit("Session expired. Run: python3 lf.py login")
            if "rate_limit" in m or "Rate limit" in m:
                time.sleep(delay)
                delay = min(delay * 2, 240)
                continue
            if isinstance(e, (ConnectionResetError, ConnectionError, OSError)) or \
                    "502" in m or "10054" in m or "forcibly closed" in m:
                time.sleep(15)
                continue
            raise
    raise RuntimeError("gave up")


# ---- refuse to collide with an existing slug ---------------------------------
Q = """query($first:Int,$q:String!){funnels(first:$first,query:$q){
  edges{node{uid name slug published}}}}"""
existing = [e["node"] for e in go(lambda: lf_api.gql(
    tok, Q, {"first": 200, "q": "order_by:id order_dir:desc"},
    extra_headers=h))["funnels"]["edges"]]
clash = [f for f in existing if f["slug"] == SLUG]
if clash:
    print("slug %r already exists: %s (%s)" % (SLUG, clash[0]["name"], clash[0]["uid"]))
    sys.exit("Nothing created. Reuse it or pick another slug.")
print("%d funnels; slug %r is free" % (len(existing), SLUG))

if DRY:
    sys.exit("DRY RUN - would create %r / %r" % (NAME, SLUG))

# ---- create ------------------------------------------------------------------
# createFunnel takes InputCreateFunnel!, NOT InputFunnel! - updateFunnel uses
# the latter, and reusing it here fails with a bare type-position error.
M = """mutation($node:InputCreateFunnel!){createFunnel(node:$node){id uid name slug published}}"""
f = go(lambda: lf_api.gql(tok, M, {"node": {
    "name": NAME, "slug": SLUG, "funnel_steps": ["article_page"],
    "currency": CURRENCY, "lang": LANG,
}}, extra_headers=h))["createFunnel"]
print("created: %s | %s | /%s | published=%s" % (
    f.get("uid") or f.get("id"), f["name"], f["slug"], f.get("published")))

fid = f.get("uid") or f.get("id")

# ---- publish so the runbook can reach the pages ------------------------------
if not f.get("published"):
    go(lambda: lf_api.gql(
        tok, "mutation($id:ID!,$node:InputFunnel!){updateFunnel(id:$id,node:$node){id published}}",
        {"id": fid, "node": {"published": True}}, extra_headers=h))
    print("published (empty funnel, no traffic at risk)")

# ---- verify ------------------------------------------------------------------
time.sleep(2)
FQ = """query($id:ID!){node(id:$id){... on Funnel{
  uid name slug published starting_step_id steps{uid slug}}}}"""
n = go(lambda: lf_api.gql(tok, FQ, {"id": fid}, extra_headers=h))["node"]
print("\nverified: name=%r slug=%r published=%s steps=%d" % (
    n["name"], n["slug"], n["published"], len(n["steps"])))
assert n["slug"] == SLUG and n["published"] is True

meta = {
    "lf_id": fid, "name": NAME, "slug": SLUG, "published": True,
    "created": "2026-09-29", "created_by": "page-pipeline / over-60s build",
    "workspace": "tub",
    "admin_url": "https://app.lightfunnels.com/admin/funnel/%s/workflow" % fid,
    "public_base": "https://www.techunboxed.co/%s/" % SLUG,
    "holds_tests": {
        "V-B gadgets 2-way": "https://app.clickup.com/t/z941abwj4k",
        "V-A smartwatch": "https://app.clickup.com/t/z941abwj4j",
    },
}
with open(os.path.join(HERE, "..", "funnel.json"), "w", encoding="utf-8") as fh:
    json.dump(meta, fh, indent=2)
print("\nADMIN : %s" % meta["admin_url"])
print("PUBLIC: %s<step-slug>" % meta["public_base"])
