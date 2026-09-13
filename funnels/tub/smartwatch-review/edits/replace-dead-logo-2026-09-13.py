#!/usr/bin/env python3
"""Repoint every block using the deleted hlth-logo.svg at the replacement logo.

The asset is gone from LF storage AND from the media library (paging all 750
library records finds no aa96818b). Pages still render 200 and the block is
intact, so the only symptom is a broken-image glyph - and only for visitors with
a cold cache, which is why it looked sudden and intermittent. Verified with
cache:'no-store', a cache-busted url, and a fresh Image element: all fail.

  dead  .../images_library/aa96818b-...-9efa09298dfa.hlth-logo.svg   404
  new   .../images_library/a71db2af-...-ce229944b9c4.png             200, 499x126

Dead block renders at 166x42 (3.95:1); the replacement is 3.96:1, so it drops in
without restyling.

WHY src_id/src_uid ARE REWRITTEN TOO: these blocks source from the media library,
so they carry src + src_id + src_uid. Rewriting src alone would leave both ids
pointing at the deleted record, and the editor resolves a library block from its
id - so the next save could pull the dead url straight back. The replacement's
record was looked up rather than guessed:

  img_NJS6xlEwFmNXWa4dRHsuE  /  _id 9978110

Safety: only steps that actually contain the dead url are sent, one step per
updateFunnel call, so siblings survive by omission. Funnel-level fields are never
included in the node and name/slug/published/starting_step_id are asserted
unchanged after every write.
"""
import json
import os
import sys
import time
from collections import defaultdict

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", "..", "..", ".."))
sys.path.insert(0, ROOT)
os.chdir(ROOT)
import lf_api  # noqa: E402

DEAD_ID = "aa96818b-73b8-41c6-9d66-9efa09298dfa"
NEW_SRC = ("https://assets.lightfunnels.com/cdn-cgi/image/"
           "width=1920,quality=80,format=auto/"
           "https://assets.lightfunnels.com/account-90380/images_library/"
           "a71db2af-954c-489e-967d-ce229944b9c4.png")
NEW_SRC_ID = 9978110
NEW_SRC_UID = "img_NJS6xlEwFmNXWa4dRHsuE"

DRY = "--dry-run" in sys.argv

tok = open(".session_token").read().strip()
acct = open(".lf_account").read().strip()
h = lf_api.session_headers(acct)

FQ = """query($id:ID!){node(id:$id){... on Funnel{
  name slug published starting_step_id steps{uid}}}}"""


def go(fn, tries=8):
    """Retry the two failures this API actually produces under a bulk edit.

    A first run died on `rate_limit_reached` after ~6 writes: the per-step
    invariant check was issuing a query before AND after every write, roughly
    tripling the call count for no extra safety. Invariants are now read once
    per funnel (see below) and the limiter is waited out rather than fought.
    """
    delay = 45
    for attempt in range(tries):
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
    raise RuntimeError("gave up after %d retries" % tries)


def patch(obj):
    """Rewrite dead references in place. Returns (n_blocks, n_html)."""
    nb = [0]
    nh = [0]

    def walk(x):
        if isinstance(x, dict):
            p = x.get("p") or {}
            if x.get("t") == "Image":
                for field in ("src", "externalSrc"):
                    v = p.get(field)
                    if isinstance(v, str) and DEAD_ID in v:
                        p[field] = NEW_SRC
                        if field == "src":
                            p["src_id"] = NEW_SRC_ID
                            p["src_uid"] = NEW_SRC_UID
                        nb[0] += 1
            c = p.get("content")
            if isinstance(c, str) and DEAD_ID in c:
                # an <img> inside rich text / HtmlElement
                import re as _re
                p["content"] = _re.sub(
                    r"https://assets\.lightfunnels\.com/[^\"')\s]*" + DEAD_ID + r"[^\"')\s]*",
                    NEW_SRC, c)
                nh[0] += 1
            for v in x.values():
                walk(v)
        elif isinstance(x, list):
            for v in x:
                walk(v)

    walk(obj)
    return nb[0], nh[0]


# ------------------------------------------------------------------ find
q = """query($first:Int){funnels(first:$first, query:"order_by:id order_dir:desc"){
  edges{node{id uid name slug published}}}}"""
funnels = [e["node"] for e in
           go(lambda: lf_api.gql(tok, q, {"first": 200}, extra_headers=h))["funnels"]["edges"]]
print("scanning %d funnels for the dead logo\n" % len(funnels))

hits = []   # (funnel, step)
for f in funnels:
    try:
        node = go(lambda f=f: lf_api.get_funnel_steps(tok, f["uid"], extra_headers=h))
    except Exception as e:
        print("  !! %-44s %s" % (f["name"][:44], str(e)[:60]))
        continue
    for st in node.get("steps") or []:
        blob = json.dumps(st.get("body")) + json.dumps(st.get("settings") or {})
        if DEAD_ID in blob:
            hits.append((f, st))
            print("  HIT  %-42s %-28s %s" % (
                f["name"][:42], (st.get("slug") or "")[:28], (st.get("title") or "")[:30]))

if not hits:
    sys.exit("\nNo step references the dead logo. Nothing to do.")
print("\n%d affected step(s) across %d funnel(s)\n" % (
    len(hits), len({f["uid"] for f, _ in hits})))

# ------------------------------------------------------------------ write
done = []
pre_inv = {}
for f, st in hits:
    body = st.get("body")
    settings = st.get("settings") or {}
    nb, nh = patch(body)
    ns = 0
    ch = settings.get("custom_html") or {}
    for key in ("header", "footer"):
        v = ch.get(key)
        if isinstance(v, str) and DEAD_ID in v:
            import re
            ch[key] = re.sub(
                r"https://assets\.lightfunnels\.com/[^\"')\s]*" + DEAD_ID + r"[^\"')\s]*",
                NEW_SRC, v)
            ns += 1

    left = DEAD_ID in (json.dumps(body) + json.dumps(settings))
    print("  %-40s %-26s blocks=%d html=%d custom=%d%s" % (
        f["name"][:40], (st.get("slug") or "")[:26], nb, nh, ns,
        "   STILL PRESENT!" if left else ""))
    assert not left, "dead id survived the patch on %s" % st.get("slug")

    if DRY:
        continue

    # Invariants are per FUNNEL, not per step, so read them once and verify once
    # at the end. Doing it around every write tripled the request count and is
    # what hit the rate limiter on the first run.
    if f["uid"] not in pre_inv:
        pre = go(lambda f=f: lf_api.gql(tok, FQ, {"id": f["uid"]}, extra_headers=h))["node"]
        pre_inv[f["uid"]] = ({k: pre.get(k) for k in
                              ("name", "slug", "published", "starting_step_id")},
                             len(pre["steps"]))

    go(lambda: lf_api.gql(
        tok, "mutation($id:ID!,$node:InputFunnel!){updateFunnel(id:$id,node:$node){id}}",
        {"id": f["uid"], "node": {"steps": [{
            "id": st["uid"], "slug": st["slug"], "title": st["title"], "type": st["type"],
            "settings": settings, "visual": st.get("visual"), "body": body,
        }]}}, extra_headers=h))
    done.append((f, st))
    time.sleep(1.5)   # stay under the limiter rather than discovering it again

print("\n%s %d step(s)" % ("would update" if DRY else "UPDATED", len(hits) if DRY else len(done)))

if not DRY:
    print("\n--- funnel invariants ---")
    for fuid, (inv, nsteps) in pre_inv.items():
        post = go(lambda fuid=fuid: lf_api.gql(tok, FQ, {"id": fuid}, extra_headers=h))["node"]
        bad = [k for k, v in inv.items() if post.get(k) != v]
        same_count = len(post["steps"]) == nsteps
        print("  %-44s %s  steps %s" % (
            (inv["name"] or "")[:44],
            "OK" if not bad else "CHANGED: %s" % bad,
            "OK" if same_count else "CHANGED (%d -> %d)" % (nsteps, len(post["steps"]))))
        assert not bad, "funnel fields changed: %s" % bad
        assert same_count, "step count changed on %s" % inv["name"]

    print("\n--- re-reading to confirm the dead id is gone account-wide ---")
    remaining = 0
    for f in funnels:
        try:
            node = go(lambda f=f: lf_api.get_funnel_steps(tok, f["uid"], extra_headers=h))
        except Exception:
            continue
        for st in node.get("steps") or []:
            blob = json.dumps(st.get("body")) + json.dumps(st.get("settings") or {})
            if DEAD_ID in blob:
                remaining += 1
                print("  STILL THERE: %s / %s" % (f["name"], st.get("slug")))
    print("  remaining references: %d" % remaining)
    print("\nUpdated pages:")
    for f, st in done:
        print("  %-42s %s" % (f["name"][:42], st.get("slug")))
