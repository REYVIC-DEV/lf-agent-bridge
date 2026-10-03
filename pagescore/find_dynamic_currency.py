#!/usr/bin/env python3
"""Find every step account-wide that has the dynamic-currency script installed.

Queries settings ONLY, never body. That is the whole trick: step bodies are
1-2 MB each and pulling them for 25+ funnels takes tens of minutes, while
settings alone comes back in seconds. custom_html lives in settings, so a
scan for installed page code never needs the body.

Reports, per hit: which script version is installed (single-product vs
products=all), how many timezone entries it carries, and whether the page
carries any data-price-handle tags - so a fleet-wide upgrade can be planned
without guessing which pages are behind.
"""
import json
import os
import re
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, ".."))
sys.path.insert(0, ROOT)
os.chdir(ROOT)
import lf_api  # noqa: E402

MARKER = "<!-- dynamic-currency -->"

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


FUNNELS = """query($first:Int){funnels(first:$first, query:"order_by:id order_dir:desc"){
  edges{node{uid name slug published}}}}"""
STEPS = """query($id:ID!){node(id:$id){... on Funnel{
  steps{uid slug title settings}}}}"""

funnels = [e["node"] for e in go(lambda: lf_api.gql(
    tok, FUNNELS, {"first": 200}, extra_headers=h))["funnels"]["edges"]]
print("scanning %d funnels (settings only, no bodies)\n" % len(funnels))

hits = []
for f in funnels:
    try:
        node = go(lambda f=f: lf_api.gql(tok, STEPS, {"id": f["uid"]}, extra_headers=h))["node"]
    except Exception as e:
        print("  !! %-40s %s" % (f["name"][:40], str(e)[:60]))
        continue
    for st in (node.get("steps") or []):
        ch = ((st.get("settings") or {}).get("custom_html") or {})
        hdr = (ch.get("header") or "") + (ch.get("footer") or "")
        if MARKER not in hdr and "var PRICES" not in hdr:
            continue
        tz = len(re.findall(r'"[A-Za-z_]+/[A-Za-z_/]+":"[A-Z]{2}"', hdr))
        hits.append({
            "funnel": f["name"], "funnel_uid": f["uid"], "funnel_slug": f["slug"],
            "published": f["published"], "step": st["uid"], "slug": st["slug"],
            "title": st.get("title") or "",
            "multiproduct": "products=all" in hdr,
            "tz_entries": tz,
            "has_prefix": "TZ_PREFIX" in hdr,
            "copies": hdr.count("var PRICES"),
            "noindex": "noindex" in hdr,
        })
        print("  HIT  %-34s %-28s multiproduct=%-5s tz=%-3d copies=%d%s" % (
            f["name"][:34], st["slug"][:28], hits[-1]["multiproduct"], tz,
            hits[-1]["copies"], "  [noindex]" if hits[-1]["noindex"] else ""))

print("\n%d step(s) across %d funnel(s) run the script" % (
    len(hits), len({x["funnel_uid"] for x in hits})))
out = os.path.join(HERE, "dynamic_currency_installs.json")
with open(out, "w", encoding="utf-8") as fh:
    json.dump(hits, fh, indent=2, ensure_ascii=False)
print("written: %s" % os.path.relpath(out, ROOT))

stale = [x for x in hits if x["tz_entries"] < 100]
print("\nNEEDS THE NEW MARKETS (fewer than 100 timezone rows): %d" % len(stale))
for x in stale:
    print("   %-34s %-28s  %s/%s" % (x["funnel"][:34], x["slug"][:28],
                                     x["funnel_slug"], x["slug"]))
