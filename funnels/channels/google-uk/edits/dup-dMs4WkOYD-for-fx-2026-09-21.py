#!/usr/bin/env python3
"""Duplicate /article/dMs4WkOYD into a sibling test step for the currency work.

WHY A DUPE AND NOT AN EDIT IN PLACE
    dMs4WkOYD became the destination of the comparison-1 redirect this morning,
    so it now receives 100% of Google paid traffic. Tagging ~dozens of money
    figures and installing a head script on that page means every intermediate
    state is live on paid traffic. The dupe costs one API call and removes the
    entire class of risk; the tagged body gets promoted onto the winner only
    once it has been QA'd across markets.

⚠️ THE DUPE IS A PUBLIC PAGE ON AN INDEXED DOMAIN.
    A byte-identical copy of a live advertorial at a second URL is a duplicate-
    content competitor to the page we just sent all the paid traffic to. So the
    copy ships `<meta name="robots" content="noindex,nofollow">` prepended to its
    own custom_html.header. That is the ONLY difference from the source at
    creation time.

API NOTES, ALL LEARNED THE HARD WAY
    - `createStep` returns a CreateStep WRAPPER: select `{step{uid slug title}}`,
      not `{uid}`.
    - `body` is the StepBody custom scalar. It reads as a parsed object and must
      be sent back as one. json.dumps(...) is accepted and then fails with a bare
      "Oops! Something went wrong" naming no field.
    - `thumbnail` READS as {key,url} but InputStep.thumbnail is a String: send
      `.key`.
    - `step.title` is the workflow label; `settings.seo.title` is the page
      <title>. They are different things.
    - The follow-up `updateFunnel` lists ONLY the new step, so the other 13
      survive by omission. Omission does not delete.
"""
import copy
import json
import os
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", "..", "..", ".."))
sys.path.insert(0, ROOT)
os.chdir(ROOT)
import lf_api  # noqa: E402

FUNNEL = "fun_p9Y_FwGlQsaP5bpW70q5N"
SRC = "step_coYi_dsw6RtJtR111GjR8"          # /article/dMs4WkOYD, the live winner
NEW_SLUG = "dMs4WkOYD-fx"
NEW_TITLE = "We Spent GBP1,581 Testing The Top 5 - FX TEST"
NOINDEX = '<meta name="robots" content="noindex,nofollow">\n'

DRY = "--dry-run" in sys.argv

tok = open(".session_token").read().strip()
acct = open(".lf_account").read().strip()
h = lf_api.session_headers(acct)

FQ = """query($id:ID!){node(id:$id){... on Funnel{
  name slug published starting_step_id steps{uid slug}}}}"""


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


before = go(lambda: lf_api.gql(tok, FQ, {"id": FUNNEL}, extra_headers=h))["node"]
inv = {k: before.get(k) for k in ("name", "slug", "published", "starting_step_id")}
n_before = len(before["steps"])
print("funnel: %s | steps=%d | published=%s" % (inv["name"], n_before, inv["published"]))

existing = {s["slug"] for s in before["steps"]}
if NEW_SLUG in existing:
    sys.exit("slug %r already exists in this funnel - nothing to do." % NEW_SLUG)

node_all = go(lambda: lf_api.get_funnel_steps(tok, FUNNEL, extra_headers=h))
s = next((x for x in node_all["steps"] if x["uid"] == SRC), None)
assert s is not None, "source step %s not found" % SRC
assert s["slug"] == "dMs4WkOYD", "source slug changed: %r" % s["slug"]
print("source: %s | slug=%s | title=%r" % (SRC, s["slug"], s["title"]))

# Deep-copy so nothing we mutate can alias the source step still held in memory.
settings = copy.deepcopy(s.get("settings") or {})
body = copy.deepcopy(s.get("body"))

ch = settings.get("custom_html") or {}
hdr = ch.get("header") or ""
ff_before = hdr.count("@font-face")
if "noindex" not in hdr:
    ch["header"] = NOINDEX + hdr
settings["custom_html"] = ch
assert ch["header"].count("@font-face") == ff_before, "font-face count changed"
print("header: %d -> %d chars, @font-face %d (unchanged), noindex added"
      % (len(hdr), len(ch["header"]), ff_before))

# Place the new card below the lowest existing one so the workflow stays readable.
ys = [(x.get("visual") or {}).get("y") for x in node_all["steps"]]
xs = [(x.get("visual") or {}).get("x") for x in node_all["steps"]]
ys = [v for v in ys if isinstance(v, (int, float))]
xs = [v for v in xs if isinstance(v, (int, float))]
place = {"x": (min(xs) if xs else 0.0), "y": (max(ys) + 240.0 if ys else 0.0)}

new_node = {"slug": NEW_SLUG, "title": NEW_TITLE, "type": s["type"],
            "settings": settings, "visual": place, "body": body}
for k in ("thumbnail", "product_id", "template", "disable_token_redirection"):
    v = s.get(k)
    if v is None:
        continue
    if k == "thumbnail" and isinstance(v, dict):
        v = v.get("key")
        if not v:
            continue
    new_node[k] = v

print("\nnew step: slug=%r title=%r at %s" % (NEW_SLUG, NEW_TITLE, place))
print("  body blocks carried: %d top-level" % (
    len(body) if isinstance(body, list) else len(body or {})))

if DRY:
    sys.exit("\nDRY RUN - nothing created.")

created = go(lambda: lf_api.gql(
    tok,
    "mutation($funnel_id:ID!,$node:InputStep!)"
    "{createStep(funnel_id:$funnel_id,node:$node){step{uid slug title}}}",
    {"funnel_id": FUNNEL, "node": new_node}, extra_headers=h))["createStep"]["step"]
new_uid = created["uid"]
print("\ncreated %s slug=%r" % (new_uid, created["slug"]))

time.sleep(1.5)
go(lambda: lf_api.gql(
    tok, "mutation($id:ID!,$node:InputFunnel!){updateFunnel(id:$id,node:$node){id}}",
    {"id": FUNNEL, "node": {"steps": [{
        "id": new_uid, "slug": NEW_SLUG, "title": NEW_TITLE, "type": s["type"],
        "settings": settings, "visual": place, "body": body}]}}, extra_headers=h))
print("attached via updateFunnel (only the new step listed)")

# ------------------------------------------------------------------ verify
time.sleep(2)
after = go(lambda: lf_api.gql(tok, FQ, {"id": FUNNEL}, extra_headers=h))["node"]
bad = [k for k, v in inv.items() if after.get(k) != v]
print("\nfunnel invariants: %s" % ("OK" if not bad else "CHANGED %s" % bad))
print("steps: %d -> %d" % (n_before, len(after["steps"])))
assert not bad, "funnel fields changed: %s" % bad
assert len(after["steps"]) == n_before + 1, "expected exactly one new step"
assert after["starting_step_id"] == inv["starting_step_id"], "ENTRY MOVED"

node2 = go(lambda: lf_api.get_funnel_steps(tok, FUNNEL, extra_headers=h))
new = next(x for x in node2["steps"] if x["uid"] == new_uid)
src2 = next(x for x in node2["steps"] if x["uid"] == SRC)
same_body = json.dumps(new.get("body"), sort_keys=True) == json.dumps(
    src2.get("body"), sort_keys=True)
print("copy == source body: %s" % same_body)
print("source untouched   : %s" % (json.dumps(src2.get("body"), sort_keys=True)
                                   == json.dumps(body, sort_keys=True)))
newhdr = ((new.get("settings") or {}).get("custom_html") or {}).get("header") or ""
print("copy has noindex   : %s" % ("noindex" in newhdr))
print("copy @font-face    : %d (source %d)" % (newhdr.count("@font-face"), ff_before))
assert same_body and "noindex" in newhdr

print("\nTEST URL: https://www.techunboxed.co/article/%s" % NEW_SLUG)
print("LIVE winner untouched: https://www.techunboxed.co/article/dMs4WkOYD")
