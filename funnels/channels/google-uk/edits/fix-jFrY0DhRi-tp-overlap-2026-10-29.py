#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Stop the Trustpilot link overlapping the paragraph above it on /article/jFrY0DhRi.

Joshua spotted it at 980px wide on 2026-10-29: in section 9 ("The Reviews Are
Crazy Good") the line "That's what tipped me over the edge." and the link
"Read Trustpilot reviews" are drawn on top of each other. Measured overlap at a
973px viewport: 18px.

THE CAUSE IS A BREAKPOINT MISMATCH, not a spacing value.

Block c633f9b4 (the Container holding the link) carries:

    gridColumnSpan  "2"                 base
    gridColumnSpan  "auto"      @991    layout collapses to one column here
    margin          top -40px           base
    margin          top   0px   @767    but the pull is only cancelled here

So between 768px and 991px the grid has already gone single-column while the
-40px pull is still applied, and the link gets yanked up into the paragraph.
Below 768 it is fine, above 991 it is fine. A 224px-wide band of viewports is
broken, which is why it survived desktop and phone checks.

ITS OWN SIBLINGS PROVE THE INTENDED VALUE. The two other negatively-pulled
text blocks in this article reset at 991, matching the grid:

    fba0fed7  margin -30px base, 0px @991
    5cdb135b  margin -75px base, 0px @991   (the paragraph it collides with)
    c633f9b4  margin -40px base, 0px @767   <-- the odd one out

THE FIX is to move that one override from 767 to 991 so the margin is cancelled
at the same width the layout changes. Nothing else: not the -40px itself, which
is correct above 991 and is what keeps the link tucked under the copy on
desktop, and not the two Containers that carry -18px with no override at all
("Sell-Out Risk" bars), which behave the same at every width and are left alone.

⚠️ RE-FETCH BEFORE WRITING. The cache this reads is rewritten by
cache-step-body.py. An older cache predates the dynamic-currency tagging done
earlier the same day, and writing a stale body would silently strip all ten
data-price / data-fx-gbp spans. The guard below refuses to run unless the body
it is about to write still carries them.

    py funnels/channels/google-uk/edits/fix-jFrY0DhRi-tp-overlap-2026-10-29.py --dry-run
    py funnels/channels/google-uk/edits/fix-jFrY0DhRi-tp-overlap-2026-10-29.py
"""
import copy
import io
import json
import os
import re
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", "..", "..", ".."))
sys.path.insert(0, ROOT)
os.chdir(ROOT)
import lf_api  # noqa: E402

FUNNEL = "fun_p9Y_FwGlQsaP5bpW70q5N"
TARGET_SLUG = "jFrY0DhRi"
PROTECTED = ("dMs4WkOYD", "dMs4WkOYD-fx", "comparison-1")
BLOCK_ID = "c633f9b4-1cf1-447c-b6f4-4bfc2213c056"
OLD_MEDIA = 767
NEW_MEDIA = 991
STEPS_DIR = os.path.join(HERE, "..", "steps")
CACHE = os.path.join(STEPS_DIR, "_cache-google-uk-steps.json")
STAMP = "2026-10-29"

DRY = "--dry-run" in sys.argv


def go(fn, tries=8):
    delay = 45
    for _ in range(tries):
        try:
            return fn()
        except Exception as e:
            m = str(e)
            if "expired" in m.lower():
                sys.exit("Session expired. Refresh .session_token.")
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


tok = open(".session_token").read().strip()
acct = open(".lf_account").read().strip()
h = lf_api.session_headers(acct)

with io.open(CACHE, encoding="utf-8") as fh:
    cached = json.load(fh)
print("cache fetched: %s" % cached["fetched_at"])
step = next((s for s in cached["steps"] if s["slug"] == TARGET_SLUG), None)
if step is None:
    sys.exit("step %r not found" % TARGET_SLUG)
assert step["slug"] not in PROTECTED, "refusing to touch a protected step"
print("target: %s | slug=%s" % (step["uid"], step["slug"]))

body = copy.deepcopy(step.get("body"))

# ⚠️ STALE-CACHE GUARD. Writing a body fetched before the currency pass would
# remove every tag it added, and nothing about the write would look wrong.
pre = json.dumps(body, ensure_ascii=False)
n_price = pre.count('data-price=')
n_fx = pre.count('data-fx-gbp=')
print("currency tags in the body about to be written: price=%d fx=%d" % (n_price, n_fx))
assert n_price == 4 and n_fx == 6, (
    "This cache predates the dynamic-currency pass (expected 4 price + 6 fx, got "
    "%d + %d). Re-run cache-step-body.py before writing." % (n_price, n_fx))

# ------------------------------------------------------------------ patch
hits = []


def walk(n):
    if isinstance(n, dict):
        if n.get("id") == BLOCK_ID:
            hits.append(n)
        for v in n.values():
            walk(v)
    elif isinstance(n, list):
        for v in n:
            walk(v)


walk(body)
assert len(hits) == 1, "expected exactly one block %s, found %d" % (BLOCK_ID, len(hits))
block = hits[0]

print("\nblock %s (%s): %s" % (BLOCK_ID[:8], block.get("t"),
                               re.sub(r"<[^>]+>", " ", json.dumps(block.get("p"), ensure_ascii=False))[:60]))
print("  styles before:")
for s in block["styles"]:
    if s.get("prop") in ("margin", "gridColumnSpan"):
        print("    %-15s media=%-5s %s" % (s["prop"], s.get("media"),
                                           json.dumps(s.get("value"), ensure_ascii=False)))

changed = 0
for s in block["styles"]:
    if s.get("prop") == "margin" and s.get("media") == OLD_MEDIA:
        s["media"] = NEW_MEDIA
        changed += 1
assert changed == 1, "expected one margin override at media=%d, changed %d" % (OLD_MEDIA, changed)

print("  styles after:")
for s in block["styles"]:
    if s.get("prop") in ("margin", "gridColumnSpan"):
        print("    %-15s media=%-5s %s" % (s["prop"], s.get("media"),
                                           json.dumps(s.get("value"), ensure_ascii=False)))

# The base pull must survive: it is what the desktop layout relies on.
base = [s for s in block["styles"]
        if s.get("prop") == "margin" and s.get("media") is None]
assert len(base) == 1 and base[0]["value"].get("top") == "-40px", \
    "the base -40px pull was lost"
# And the override must now sit on the same breakpoint as the grid change.
grid = [s for s in block["styles"]
        if s.get("prop") == "gridColumnSpan" and s.get("media") is not None]
assert grid and grid[0]["media"] == NEW_MEDIA, \
    "grid breakpoint is %r, margin override no longer matches it" % (grid[0]["media"],)

post = json.dumps(body, ensure_ascii=False)
assert post.count('data-price=') == 4 and post.count('data-fx-gbp=') == 6, \
    "the patch disturbed the currency tags"

# ------------------------------------------------------------------ backup
os.makedirs(STEPS_DIR, exist_ok=True)
backup = os.path.join(STEPS_DIR, "%s.pre-overlap-fix-%s.json" % (TARGET_SLUG, STAMP))
with io.open(backup, "w", encoding="utf-8") as fh:
    json.dump({"settings": step.get("settings"), "body": step.get("body")},
              fh, ensure_ascii=False)
print("\nbacked up -> %s" % os.path.relpath(backup, ROOT))

if DRY:
    sys.exit("\nDRY RUN - nothing written.")

go(lambda: lf_api.gql(
    tok, "mutation($id:ID!,$node:InputFunnel!){updateFunnel(id:$id,node:$node){id}}",
    {"id": FUNNEL, "node": {"steps": [{
        "id": step["uid"], "slug": step["slug"], "title": step["title"],
        "type": step["type"], "settings": step.get("settings"),
        "visual": step.get("visual"), "body": body}]}}, extra_headers=h))
print("WRITTEN.")

# ------------------------------------------------------------------ verify
time.sleep(5)
import urllib.request  # noqa: E402

req = urllib.request.Request(
    "https://www.techunboxed.co/article/" + TARGET_SLUG,
    headers={"User-Agent": "Mozilla/5.0"})
with urllib.request.urlopen(req, timeout=90) as r:
    page = r.read().decode("utf-8", "replace")

markup = re.sub(r"<script\b[^>]*>.*?</script>", " ", page, flags=re.S | re.I)
print("\nread-back from the LIVE page:")
print("  data-price=\"price\"  %d  (want 4)" % markup.count('data-price="price"'))
print("  data-fx-gbp=         %d  (want 6)" % markup.count("data-fx-gbp="))
assert markup.count('data-price="price"') == 4, "currency tags lost"
assert markup.count("data-fx-gbp=") == 6, "currency tags lost"
# The 767 rule for this block should be gone from the served CSS.
print("  '-40px' still served  %s" % ("-40px" in page))
print("\nNow re-check the overlap at 980px wide, which is the band that was broken.")
