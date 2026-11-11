#!/usr/bin/env python3
"""Create the Scaling or Failing event funnel, published, with one article page.

Published on purpose: an unpublished funnel's page is unreachable, and the QA
runbook measures a live URL. No existing traffic is at risk because the funnel
is brand new.
"""
import os, sys, time
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE); os.chdir(HERE)
import lf_api

NAME = "Scaling or Failing - Event"
SLUG = "scaling-or-failing"
APPLY = "--apply" in sys.argv

tok  = open(".session_token").read().strip()
acct = open(".lf_account").read().strip()
h    = lf_api.session_headers(acct)
assert "Cookie" in h, "no cookies in .lf_state.json - run: python lf.py login"

# Refuse to make a second funnel if one already exists under this name or slug.
q = '{funnels(first:100,query:""){edges{node{id name slug published}}}}'
existing = [e["node"] for e in lf_api.gql(tok, q, {}, extra_headers=h)["funnels"]["edges"]]
clash = [n for n in existing if n["slug"] == SLUG or n["name"] == NAME]
if clash:
    for c in clash:
        print("ALREADY EXISTS: %s  /%s  published=%s  %s" % (c["name"], c["slug"], c["published"], c["id"]))
    sys.exit(0)

print("will create: %r  slug=/%s  currency=USD  steps=['article_page']" % (NAME, SLUG))
if not APPLY:
    sys.exit("(dry run - nothing created)")

f = lf_api.create_funnel(tok, NAME, SLUG, ["article_page"],
                         currency="USD", lang="en", extra_headers=h)
print("created funnel %s" % f["id"])
for s in f.get("steps") or []:
    print("   step %s  slug=%s  type=%s" % (s.get("uid"), s.get("slug"), s.get("type")))

time.sleep(2)
n = lf_api.gql(tok, '''query($id:ID!){node(id:$id){... on Funnel{
      id name slug published starting_step_id
      steps{uid slug title type product_id}}}}''',
      {"id": f["id"]}, extra_headers=h)["node"]
print("\nread back: %s  /%s  published=%s" % (n["name"], n["slug"], n["published"]))
for s in n["steps"]:
    print("   %-26s %-14s product_id=%r%s" % (
        s["slug"], s["type"], s["product_id"],
        "  <== ENTRY" if s["uid"] == n["starting_step_id"] else ""))
