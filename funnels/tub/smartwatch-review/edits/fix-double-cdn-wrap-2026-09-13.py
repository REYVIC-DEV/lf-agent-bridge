#!/usr/bin/env python3
"""Un-nest a double /cdn-cgi/image/ wrap introduced by the logo replacement.

MY BUG, and the reason to verify with a browser rather than by grepping HTML.

The replacement url supplied was already a Cloudflare transform:

    /cdn-cgi/image/width=1920,quality=80,format=auto/<origin>

Stored as a block's src it looked right, and the page HTML contained the new
asset id, so a text-level check passed. But LF applies its OWN transform to a
block src at render time, producing:

    /cdn-cgi/image/width=1080,.../ /cdn-cgi/image/width=1920,.../ <origin>

Cloudflare will not transform a transform, so every logo rendered 0x0 - the same
broken box the fix was meant to remove. That is exactly why the original blocks
stored the RAW library path: LF adds the wrapper itself.

This rewrites those srcs to the raw path and restores src_id/src_uid, which is
what an image picked from the media library in the editor looks like.
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

ASSET = "a71db2af-954c-489e-967d-ce229944b9c4"
RAW = ("https://assets.lightfunnels.com/account-90380/images_library/%s.png" % ASSET)
SRC_ID = 9978110
SRC_UID = "img_NJS6xlEwFmNXWa4dRHsuE"

DRY = "--dry-run" in sys.argv

tok = open(".session_token").read().strip()
acct = open(".lf_account").read().strip()
h = lf_api.session_headers(acct)

FQ = """query($id:ID!){node(id:$id){... on Funnel{
  name slug published starting_step_id steps{uid}}}}"""


def go(fn, tries=8):
    delay = 45
    for _ in range(tries):
        try:
            return fn()
        except Exception as e:
            m = str(e)
            if "expired" in m.lower():
                sys.exit("Session expired. Run: python3 lf.py login")
            if "rate_limit" in m or "Rate limit" in m:
                print("    rate limited, waiting %ds" % delay, flush=True)
                time.sleep(delay)
                delay = min(delay * 2, 300)
                continue
            if "502" in m or "Bad Gateway" in m:
                print("    502, backing off 70s", flush=True)
                time.sleep(70)
                continue
            raise
    raise RuntimeError("gave up")


def patch(obj):
    n = [0]

    def walk(x):
        if isinstance(x, dict):
            p = x.get("p") or {}
            if x.get("t") == "Image":
                for field in ("src", "externalSrc"):
                    v = p.get(field)
                    # only the ones we over-wrapped: our asset AND a cdn-cgi prefix
                    if isinstance(v, str) and ASSET in v and "cdn-cgi/image" in v:
                        p[field] = RAW
                        if field == "src":
                            p["src_id"] = SRC_ID
                            p["src_uid"] = SRC_UID
                        n[0] += 1
            for v in x.values():
                walk(v)
        elif isinstance(x, list):
            for v in x:
                walk(v)

    walk(obj)
    return n[0]


def still_wrapped(obj):
    """Count blocks whose OWN src is still a wrapped copy of our asset.

    Testing the serialized body for "cdn-cgi/image" was wrong: these pages carry
    dozens of other images that legitimately use a transform url, so the whole
    body always matches and the check fired on a correctly-fixed step.
    """
    bad = [0]

    def walk(x):
        if isinstance(x, dict):
            if x.get("t") == "Image":
                p = x.get("p") or {}
                for field in ("src", "externalSrc"):
                    v = p.get(field)
                    if isinstance(v, str) and ASSET in v and "cdn-cgi/image" in v:
                        bad[0] += 1
            for v in x.values():
                walk(v)
        elif isinstance(x, list):
            for v in x:
                walk(v)

    walk(obj)
    return bad[0]


q = """query($first:Int){funnels(first:$first, query:"order_by:id order_dir:desc"){
  edges{node{id uid name slug published}}}}"""
funnels = [e["node"] for e in
           go(lambda: lf_api.gql(tok, q, {"first": 200}, extra_headers=h))["funnels"]["edges"]]
print("scanning %d funnels for the double-wrapped logo\n" % len(funnels))

hits = []
for f in funnels:
    try:
        node = go(lambda f=f: lf_api.get_funnel_steps(tok, f["uid"], extra_headers=h))
    except Exception as e:
        print("  !! %-44s %s" % (f["name"][:44], str(e)[:60]))
        continue
    for st in node.get("steps") or []:
        blob = json.dumps(st.get("body"))
        if ASSET in blob and "cdn-cgi/image" in blob:
            hits.append((f, st))
            print("  HIT  %-42s %s" % (f["name"][:42], st.get("slug")))

if not hits:
    sys.exit("\nNothing double-wrapped. Nothing to do.")
print("\n%d step(s) across %d funnel(s)\n" % (len(hits), len({f["uid"] for f, _ in hits})))

pre_inv, done = {}, []
for f, st in hits:
    body = st.get("body")
    n = patch(body)
    still = still_wrapped(body)
    print("  %-40s %-28s fixed=%d%s" % (
        f["name"][:40], (st.get("slug") or "")[:28], n,
        "  STILL WRAPPED x%d!" % still if still else ""))
    assert not still, "double wrap survived on %s" % st.get("slug")
    if DRY:
        continue
    if f["uid"] not in pre_inv:
        pre = go(lambda f=f: lf_api.gql(tok, FQ, {"id": f["uid"]}, extra_headers=h))["node"]
        pre_inv[f["uid"]] = ({k: pre.get(k) for k in
                              ("name", "slug", "published", "starting_step_id")},
                             len(pre["steps"]))
    go(lambda: lf_api.gql(
        tok, "mutation($id:ID!,$node:InputFunnel!){updateFunnel(id:$id,node:$node){id}}",
        {"id": f["uid"], "node": {"steps": [{
            "id": st["uid"], "slug": st["slug"], "title": st["title"], "type": st["type"],
            "settings": st.get("settings") or {}, "visual": st.get("visual"), "body": body,
        }]}}, extra_headers=h))
    done.append((f, st))
    time.sleep(1.5)

print("\n%s %d step(s)" % ("would fix" if DRY else "FIXED", len(hits) if DRY else len(done)))
if not DRY:
    for fuid, (inv, nsteps) in pre_inv.items():
        post = go(lambda fuid=fuid: lf_api.gql(tok, FQ, {"id": fuid}, extra_headers=h))["node"]
        bad = [k for k, v in inv.items() if post.get(k) != v]
        print("  %-44s %s  steps %s" % ((inv["name"] or "")[:44],
              "OK" if not bad else "CHANGED %s" % bad,
              "OK" if len(post["steps"]) == nsteps else "CHANGED"))
        assert not bad and len(post["steps"]) == nsteps
