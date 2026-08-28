#!/usr/bin/env python3
"""Give the dynamic-currency test page a slug that looks like the live pages.

"dynamic-currency" announces itself as an internal test in the URL bar and in
any ad's display URL. Every page in this funnel that actually takes traffic uses
an opaque 9-character slug instead - xI7j8mDEB, DzyMm0pUH, FsAAgEuAy, vEnUIeOJy,
9QSx_mKmh, nxR5Ub02b, LxcTvDN0X, KFOtZ2f0H, xNlR_CA6j - so one more of those is
indistinguishable from them.

The WORKFLOW LABEL stays "DYNAMIC CURRENCY (test)". That is where the test name
belongs: visible to us in the funnel, invisible to a visitor.

Only the slug changes. Everything else - body, settings, seo.title, custom_html -
is echoed back exactly as read, and the funnel's own invariants are never sent.
"""
import json
import secrets
import sys
import time

sys.path.insert(0, ".")
import lf_api

DST = "fun_vGqQYxn4H2i_traYYkh4w"
STEP = "step_o3hE-N_cIOLHMOhl9bnml"
OLD_SLUG = "dynamic-currency"

ALPHABET = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"

tok = open(".session_token").read().strip()
acct = open(".lf_account").read().strip()
h = lf_api.session_headers(acct)

q = """query($id:ID!){node(id:$id){... on Funnel{
  name slug published starting_step_id steps{uid slug title}}}}"""


def go(fn):
    for _ in range(5):
        try:
            return fn()
        except Exception as e:
            if "502" in str(e) or "Bad Gateway" in str(e):
                print("  502, backing off 70s")
                time.sleep(70)
                continue
            raise
    raise RuntimeError("gave up")


before = go(lambda: lf_api.gql(tok, q, {"id": DST}, extra_headers=h))["node"]
inv = {k: before.get(k) for k in ("name", "slug", "published", "starting_step_id")}
taken = {x["slug"] for x in before["steps"]}
print("funnel: %r  (%d steps)" % (inv["name"], len(before["steps"])))
print("sibling slugs: %s" % sorted(s for s in taken if len(s) == 9)[:6])

# 9 chars, matching the siblings; regenerate on the astronomically unlikely clash
for _ in range(50):
    new_slug = "".join(secrets.choice(ALPHABET) for _ in range(9))
    if new_slug not in taken:
        break
else:
    raise RuntimeError("could not find a free slug")

full = go(lambda: lf_api.get_funnel_steps(tok, DST, extra_headers=h))
s = {x["uid"]: x for x in full["steps"]}[STEP]
assert s["slug"] == OLD_SLUG, "unexpected current slug: %r" % s["slug"]
st = s.get("settings") or {}
seo_title = (st.get("seo") or {}).get("title")
raw = s["body"] if isinstance(s["body"], str) else json.dumps(s["body"])
fx = raw.count("data-fx-gbp")
hdr = (st.get("custom_html") or {}).get("header") or ""
print("\n%s -> %s   (title stays %r)" % (OLD_SLUG, new_slug, s["title"]))

go(lambda: lf_api.gql(
    tok, "mutation($id:ID!,$node:InputFunnel!){updateFunnel(id:$id,node:$node){id}}",
    {"id": DST, "node": {"steps": [{
        "id": STEP,
        "slug": new_slug,
        "title": s["title"],          # unchanged: the workflow label
        "type": s["type"],
        "settings": st,               # unchanged: seo.title + custom_html
        "visual": s.get("visual"),
        "body": s["body"],            # StepBody reads as an object; send the object
    }]}}, extra_headers=h))
print("slug updated")

after = go(lambda: lf_api.gql(tok, q, {"id": DST}, extra_headers=h))["node"]
for k in inv:
    same = inv[k] == after.get(k)
    print("  %-18s %-5s %r" % (k, "OK" if same else "CHANGED!", after.get(k)))
    assert same, k
assert len(after["steps"]) == len(before["steps"]), "step count changed"

d = {x["uid"]: x for x in go(lambda: lf_api.get_funnel_steps(tok, DST, extra_headers=h))["steps"]}[STEP]
draw = d["body"] if isinstance(d["body"], str) else json.dumps(d["body"])
dst_hdr = ((d.get("settings") or {}).get("custom_html") or {}).get("header") or ""
print("\n  slug        : %r" % d["slug"])
print("  title       : %r" % d["title"])
print("  page title  : %r" % ((d.get("settings") or {}).get("seo") or {}).get("title"))
print("  fx tags     : %d (was %d)" % (draw.count("data-fx-gbp"), fx))
print("  script      : applyPrices=%d  @font-face=%d" % (
    dst_hdr.count("function applyPrices"), dst_hdr.count("@font-face")))
assert d["slug"] == new_slug
assert d["title"] == s["title"]
assert ((d.get("settings") or {}).get("seo") or {}).get("title") == seo_title
assert draw.count("data-fx-gbp") == fx == 36
assert dst_hdr.count("function applyPrices") == 1
assert dst_hdr.count("@font-face") == 8
assert len(dst_hdr) == len(hdr)

print("\nURL: https://www.techunboxed.co/%s/%s" % (after["slug"], new_slug))
