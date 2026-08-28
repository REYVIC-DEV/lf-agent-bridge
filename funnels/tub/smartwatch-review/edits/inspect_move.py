#!/usr/bin/env python3
"""Read-only recon before moving a step into the LIVE advertorial funnel.

Two things to pin down:
  1. Which field is the funnel-workflow label vs the page's <title>. The user
     wants the workflow label changed and the page title left alone.
  2. The destination's invariants, so the write can be checked against them:
     name, published, starting_step_id, step count, existing slugs.
"""
import json
import sys

sys.path.insert(0, ".")
import lf_api

SRC = "fun_f1IsXx3YnEA2UD2g91dAv"          # randell testing
SRC_STEP = "step_JM0a30ybnkm3hpOE7-lSW"    # techunboxed-uk-v4  (/pb/2)
DST = "fun_vGqQYxn4H2i_traYYkh4w"          # LIVE advertorial

tok = open(".session_token").read().strip()
acct = open(".lf_account").read().strip()
h = lf_api.session_headers(acct)

q = """query($id:ID!){node(id:$id){... on Funnel{
  name slug published starting_step_id
  steps{uid slug title type}}}}"""

for fid, label in ((SRC, "SOURCE  randell testing"), (DST, "DEST    live advertorial")):
    n = lf_api.gql(tok, q, {"id": fid}, extra_headers=h)["node"]
    print("=" * 78)
    print("%s  (%s)" % (label, fid))
    print("  name            : %r" % n.get("name"))
    print("  slug            : %r" % n.get("slug"))
    print("  published       : %s" % n.get("published"))
    print("  starting_step_id: %s" % n.get("starting_step_id"))
    print("  steps           : %d" % len(n["steps"]))
    for i, s in enumerate(n["steps"]):
        mark = "  <-- MOVING" if s["uid"] == SRC_STEP else ""
        star = " *START*" if s["uid"] == n.get("starting_step_id") else ""
        print("    [%2d] %-26s %-22s %-10s %r%s%s" % (
            i, s["uid"][:26], s["slug"], s["type"], s["title"][:38], star, mark))

# the moving step in detail: where does the page <title> actually live?
print("=" * 78)
node = lf_api.get_funnel_steps(tok, SRC, extra_headers=h)
s = {x["uid"]: x for x in node["steps"]}[SRC_STEP]
print("MOVING STEP: %s" % SRC_STEP)
print("  step.title  : %r   <- shown in the funnel workflow" % s["title"])
print("  step.slug   : %r" % s["slug"])
print("  step.type   : %r" % s["type"])
st = s.get("settings") or {}
print("  settings keys: %s" % sorted(st.keys()))
for k in ("seo", "meta", "page", "custom_html", "tracking"):
    v = st.get(k)
    if isinstance(v, dict):
        print("    settings[%r] keys: %s" % (k, sorted(v.keys())))
        for kk in ("title", "description", "page_title"):
            if kk in v:
                print("      settings[%r][%r] = %r" % (k, kk, str(v[kk])[:70]))
print("  body is %s" % type(s["body"]).__name__)
raw = s["body"] if isinstance(s["body"], str) else json.dumps(s["body"])
print("  tags in body: price=%d compare=%d discount=%d fx=%d" % (
    raw.count('data-price="price"') + raw.count('data-price=\\"price\\"'),
    raw.count('data-price="compare"') + raw.count('data-price=\\"compare\\"'),
    raw.count('data-price="discount"') + raw.count('data-price=\\"discount\\"'),
    raw.count("data-fx-gbp")))
hdr = (st.get("custom_html") or {}).get("header") or ""
print("  custom_html.header: %d chars, applyPrices=%d, @font-face=%d" % (
    len(hdr), hdr.count("function applyPrices"), hdr.count("@font-face")))
