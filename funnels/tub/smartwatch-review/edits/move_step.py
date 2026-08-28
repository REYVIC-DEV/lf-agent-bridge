#!/usr/bin/env python3
"""Move techunboxed-uk-v4 into the LIVE advertorial funnel as a dynamic-currency test.

  from  fun_f1IsXx3YnEA2UD2g91dAv  step_JM0a30ybnkm3hpOE7-lSW  (/pb/2)
  to    fun_vGqQYxn4H2i_traYYkh4w  (live: TUB - Top 5 h trackers-v2 - META - LIVE)

Renames the FUNNEL-WORKFLOW label (step.title) and deliberately leaves the PAGE
title (settings.seo.title, "RANKED: The best health trackers...") untouched -
those are two different fields and the user asked for the former only.

Writing into a live funnel, so:
  - createStep + updateFunnel listing ONLY the new step. Siblings survive by
    omission; the 14 existing steps are never sent.
  - name, slug, published and starting_step_id are never included in the node,
    so they cannot be changed. All four are asserted unchanged afterwards.
  - the source step is backed up to the repo first, post-tagging, so the move is
    reversible. The committed baseline is PRE-tagging and would not restore this.

This script only COPIES. Removing the source is a separate, later step.
"""
import json
import os
import sys
import time

sys.path.insert(0, ".")
import lf_api

SRC = "fun_f1IsXx3YnEA2UD2g91dAv"
SRC_STEP = "step_JM0a30ybnkm3hpOE7-lSW"
DST = "fun_vGqQYxn4H2i_traYYkh4w"

NEW_TITLE = "DYNAMIC CURRENCY (test)"   # workflow label; matches sibling convention
NEW_SLUG = "dynamic-currency"

BACKUP = "funnels/randell/randell-testing/steps/02-techunboxed-uk-v4.tagged.json"

tok = open(".session_token").read().strip()
acct = open(".lf_account").read().strip()
h = lf_api.session_headers(acct)


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
    raise RuntimeError("gave up after 502 retries")


# ---------------------------------------------------------------- source
src_node = go(lambda: lf_api.get_funnel_steps(tok, SRC, extra_headers=h))
s = {x["uid"]: x for x in src_node["steps"]}[SRC_STEP]

raw = s["body"] if isinstance(s["body"], str) else json.dumps(s["body"])
counts = dict(
    price=raw.count('data-price="price"') + raw.count('data-price=\\"price\\"'),
    compare=raw.count('data-price="compare"') + raw.count('data-price=\\"compare\\"'),
    discount=raw.count('data-price="discount"') + raw.count('data-price=\\"discount\\"'),
    fx=raw.count("data-fx-gbp"),
)
assert counts == {"price": 11, "compare": 3, "discount": 2, "fx": 36}, counts

st = s.get("settings") or {}
hdr = (st.get("custom_html") or {}).get("header") or ""
assert hdr.count("function applyPrices") == 1, "expected exactly one script copy"
assert hdr.count("@font-face") == 8, hdr.count("@font-face")
seo_title = (st.get("seo") or {}).get("title")
print("source verified: tags %s, script x1, @font-face x8" % counts)
print("page title (must not change): %r" % seo_title)

os.makedirs(os.path.dirname(BACKUP), exist_ok=True)
with open(BACKUP, "w", encoding="utf-8", newline="\n") as fh:
    json.dump(s, fh, indent=2, ensure_ascii=False)
print("backed up post-tagging state -> %s" % BACKUP)

# ---------------------------------------------------------------- destination before
q = """query($id:ID!){node(id:$id){... on Funnel{
  name slug published starting_step_id steps{uid slug title visual{x y}}}}}"""
before = go(lambda: lf_api.gql(tok, q, {"id": DST}, extra_headers=h))["node"]
inv = {k: before.get(k) for k in ("name", "slug", "published", "starting_step_id")}
slugs = {x["slug"] for x in before["steps"]}
print("\ndest before: %d steps, start=%s" % (len(before["steps"]), inv["starting_step_id"]))
assert NEW_SLUG not in slugs, "slug %r already used in destination" % NEW_SLUG

# ---------------------------------------------------------------- create
# place the card clear of the 14 existing ones instead of at the source's
# coordinates, which would land it on top of another step in the canvas
ys = [(x.get("visual") or {}).get("y") for x in before["steps"]]
xs = [(x.get("visual") or {}).get("x") for x in before["steps"]]
ys = [v for v in ys if isinstance(v, (int, float))]
xs = [v for v in xs if isinstance(v, (int, float))]
place = {"x": (min(xs) if xs else 0.0), "y": (max(ys) + 240.0 if ys else 0.0)}

node = {
    "slug": NEW_SLUG,
    "title": NEW_TITLE,          # the workflow label
    "type": s["type"],
    "settings": st,              # carries seo (page title) + custom_html untouched
}
for k in ("visual", "thumbnail", "product_id", "template",
          "disable_token_redirection"):
    v = s.get(k)
    if v is None:
        continue
    # thumbnail READS as {key, url} but InputStep.thumbnail is a String - send
    # the key. Same generated preview image, so the workflow card still shows one.
    if k == "visual":
        v = place
    if k == "thumbnail" and isinstance(v, dict):
        v = v.get("key")
        if not v:
            continue
    node[k] = v
# StepBody is a custom scalar; it READS as a parsed object and must be sent
# back that way. Sending json.dumps(...) fails with a bare
# "Oops! Something went wrong" that names no field.
node["body"] = s["body"]

created = go(lambda: lf_api.gql(
    tok,
    "mutation($funnel_id:ID!,$node:InputStep!){createStep(funnel_id:$funnel_id,node:$node){step{uid slug title}}}",
    {"funnel_id": DST, "node": node}, extra_headers=h))["createStep"]["step"]
new_uid = created["uid"]
print("created %s  slug=%r  title=%r" % (new_uid, created["slug"], created["title"]))

# ---------------------------------------------------------------- attach (only the new step)
go(lambda: lf_api.gql(
    tok, "mutation($id:ID!,$node:InputFunnel!){updateFunnel(id:$id,node:$node){id}}",
    {"id": DST, "node": {"steps": [{
        "id": new_uid, "slug": NEW_SLUG, "title": NEW_TITLE, "type": s["type"],
        "settings": st, "visual": place,
        "body": s["body"]}]}}, extra_headers=h))
print("attached via updateFunnel (only the new step listed)")

# ---------------------------------------------------------------- verify
after = go(lambda: lf_api.gql(tok, q, {"id": DST}, extra_headers=h))["node"]
inv_after = {k: after.get(k) for k in ("name", "slug", "published", "starting_step_id")}
print("\n--- destination invariants ---")
for k in inv:
    same = inv[k] == inv_after[k]
    print("  %-18s %-5s %r" % (k, "OK" if same else "CHANGED!", inv_after[k]))
    assert same, "%s changed: %r -> %r" % (k, inv[k], inv_after[k])
print("  steps %d -> %d" % (len(before["steps"]), len(after["steps"])))
assert len(after["steps"]) == len(before["steps"]) + 1

new = [x for x in after["steps"] if x["uid"] == new_uid]
assert new, "new step not attached"
print("  new step attached: %r / %r" % (new[0]["slug"], new[0]["title"]))

# body + settings landed intact?
dst_full = go(lambda: lf_api.get_funnel_steps(tok, DST, extra_headers=h))
d = {x["uid"]: x for x in dst_full["steps"]}[new_uid]
draw = d["body"] if isinstance(d["body"], str) else json.dumps(d["body"])
dc = dict(
    price=draw.count('data-price="price"') + draw.count('data-price=\\"price\\"'),
    compare=draw.count('data-price="compare"') + draw.count('data-price=\\"compare\\"'),
    discount=draw.count('data-price="discount"') + draw.count('data-price=\\"discount\\"'),
    fx=draw.count("data-fx-gbp"),
)
dhdr = ((d.get("settings") or {}).get("custom_html") or {}).get("header") or ""
dseo = ((d.get("settings") or {}).get("seo") or {}).get("title")
print("\n--- copied step ---")
print("  tags        : %s  %s" % (dc, "OK" if dc == counts else "MISMATCH"))
print("  script      : applyPrices=%d  @font-face=%d" % (
    dhdr.count("function applyPrices"), dhdr.count("@font-face")))
print("  page title  : %r  %s" % (dseo, "UNCHANGED" if dseo == seo_title else "CHANGED!"))
assert dc == counts and dhdr.count("function applyPrices") == 1
assert dhdr.count("@font-face") == 8
assert dseo == seo_title

print("\nURL: https://www.techunboxed.co/%s/%s" % (after["slug"], NEW_SLUG))
print("new_uid=%s" % new_uid)
