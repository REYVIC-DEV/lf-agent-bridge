#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Harden the `?ref=` -> Whop retarget: `promoCode` must be the FIRST query
param or Whop ignores it.

JOSHUA, 2026-11-11: tested by hand -- a link with an existing `?session=...`
param and `&promoCode=...` appended after it does NOT apply the discount.
Whop only reads the code when it is the first param in the query string
(most likely: it only applies a promo when CREATING a session, and a URL
that already carries `session=` just resumes that existing session,
ignoring whatever comes after).

Our own buttons are safe today -- their stored hrefs
(`https://whop.com/checkout/plan_.../`) carry no query string at all, so
`u.searchParams.set('promoCode', code)` naturally lands it as the only,
first param. But that was luck, not a guarantee: the moment any OTHER
param is ever added to one of these hrefs (a UTM tag, anything), `.set()`
appends `promoCode` after it and the discount silently stops applying --
exactly the invisible, looks-fine-but-loses-revenue failure mode this
codebase keeps a list of. Hardening it now so that can't happen later.

Changes `apply()` in the already-installed `?ref=` script
(`retarget_affiliate_ref_to_whop-2026-11-11.py`) to rebuild each href's
query string with `promoCode` forced first and everything else appended
after, rather than relying on URLSearchParams.set()'s "append if new"
behaviour. No other part of the script changes.

    py funnels/sof/scaling-or-failing/edits/force_promocode_first_param-2026-11-11.py
    py funnels/sof/scaling-or-failing/edits/force_promocode_first_param-2026-11-11.py --apply
"""
import io
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", "..", "..", ".."))
sys.path.insert(0, ROOT)
os.chdir(ROOT)
import lf_api

FUNNEL = "fun_RoOL_WXDCAxK4hEk0v5xX"
MARK = "sof-affiliate-ref"

OLD_APPLY = (
    "  function apply() {\n"
    "    var links = document.querySelectorAll('a[href^=\"' + PREFIX + '\"]');\n"
    "    for (var i = 0; i < links.length; i++) {\n"
    "      var a = links[i], u;\n"
    "      try { u = new URL(a.href); } catch (e) { continue; }\n"
    "      /* Already right: skip, so this pass writes nothing to the DOM and cannot\n"
    "         re-trigger the observer below. */\n"
    "      if (u.searchParams.get(FIELD) === code) continue;\n"
    "      u.searchParams.set(FIELD, code);\n"
    "      a.href = u.toString();\n"
    "    }\n"
    "  }"
)
NEW_APPLY = (
    "  function apply() {\n"
    "    var links = document.querySelectorAll('a[href^=\"' + PREFIX + '\"]');\n"
    "    for (var i = 0; i < links.length; i++) {\n"
    "      var a = links[i], u;\n"
    "      try { u = new URL(a.href); } catch (e) { continue; }\n"
    "      /* FIELD must be the FIRST query param or Whop ignores it -- confirmed\n"
    "         2026-11-11: an existing ?session=... ahead of it makes the code\n"
    "         silently not apply. So the query string is rebuilt with FIELD first\n"
    "         every time, rather than appended with searchParams.set(), which\n"
    "         would only put it first when there was nothing else on the link. */\n"
    "      var rest = new URLSearchParams(u.search);\n"
    "      rest.delete(FIELD);\n"
    "      var restStr = rest.toString();\n"
    "      var newSearch = FIELD + '=' + encodeURIComponent(code) + (restStr ? '&' + restStr : '');\n"
    "      /* Already right: skip, so this pass writes nothing to the DOM and cannot\n"
    "         re-trigger the observer below. */\n"
    "      if (u.search.slice(1) === newSearch) continue;\n"
    "      u.search = newSearch;\n"
    "      a.href = u.toString();\n"
    "    }\n"
    "  }"
)

Q = """
query HS($q: String!) {
  funnels(first: 1, query: $q) { edges { node { id header_scripts } } }
}
"""
MUT = """
mutation SetHS($id: ID!, $node: InputFunnel!) {
  updateFunnel(id: $id, node: $node) { id }
}
"""

APPLY = "--apply" in sys.argv


def main():
    ACCT = open(".lf_account").read().strip()
    HH = lf_api.session_headers(ACCT)
    edges = lf_api.gql(None, Q, {"q": "id:%s" % FUNNEL}, extra_headers=HH)["funnels"]["edges"]
    assert edges, "funnel not found"
    cur = edges[0]["node"].get("header_scripts") or ""

    assert MARK in cur, "marker %r not found" % MARK
    hits = cur.count(OLD_APPLY)
    assert hits == 1, "expected 1 occurrence of the old apply() body, found %d" % hits

    print("old apply() found once, ready to harden")

    if not APPLY:
        print("\ndry run. pass --apply to write.")
        return

    bak = os.path.abspath(os.path.join(HERE, "..", "header_scripts.pre-promocode-first-2026-11-11.html"))
    with io.open(bak, "w", encoding="utf-8", newline="") as fh:
        fh.write(cur)
    print("backup -> %s" % os.path.relpath(bak, ROOT))

    new = cur.replace(OLD_APPLY, NEW_APPLY)
    assert new.count(MARK) == 1
    assert OLD_APPLY not in new
    assert NEW_APPLY in new

    lf_api.gql(None, MUT, {"id": FUNNEL, "node": {"header_scripts": new}}, extra_headers=HH)
    back = lf_api.gql(None, Q, {"q": "id:%s" % FUNNEL}, extra_headers=HH)["funnels"]["edges"][0]["node"].get("header_scripts") or ""
    assert back == new, "read-back differs from what was sent"
    print("header_scripts written and read back identical: %d -> %d chars" % (len(cur), len(new)))


main()
