#!/usr/bin/env python3
"""Upgrade dMs4WkOYD-fx to the multi-product price feed, and price the strap.

TWO CHANGES, both on the FX TEST step only:

  1. Swap the installed dynamic-currency script for the version that calls
     /api/prices?products=all&country=XX and honours data-price-handle.
  2. Tag the one remaining GBP figure - GBP14.95, the Sport Knit Arm Band -
     as data-price="price" data-price-handle="hlth-arm-band".

WHY THE STRAP COULD NOT BE TAGGED BEFORE
    It is OUR product, so the mid-market converter must not price it, but the
    old feed carried only the band's handle so there was no exact figure
    either. Neither feed was correct and it stayed in GBP. products=all now
    serves it: PH 465, ZA 186, HR 10.95, DE 14.95. Mid-market would have said
    ~PHP1,255 in PH, so converting it would have been wrong by nearly 3x.

⚠️ THE RE-WRAP TRAP, which is why this is not just "run the tagger again".
    Every other figure is ALREADY wrapped in a span. tag_html splits on tags,
    so the text INSIDE an existing span - "GBP79" - is still bare text to the
    matcher and a second pass would wrap all 60 figures a second time. Nested
    tags break the script outright: it replaces the outer element's whole
    textContent, so the inner span is destroyed and the figure is written
    twice over. This script therefore matches ONLY 14.95, and skips any match
    whose immediately preceding tag is already a data-price span.

⚠️ THE HEADER IS REBUILT FROM THE MARKER, NOT APPENDED TO.
    Appending would leave two copies of the script racing to write the same
    nodes. Everything before the marker - including the 10 @font-face rules and
    the noindex - is preserved verbatim; everything from the marker on is
    replaced.
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
TARGET_SLUG = "dMs4WkOYD-fx"
FORBIDDEN_SLUG = "dMs4WkOYD"
SCRIPT_FILE = os.path.join(ROOT, "snippets/dynamic-currency-header-block.html")
MARKER = "<!-- dynamic-currency -->"
BACKUP_DIR = os.path.join(HERE, "..", "steps")
STAMP = "2026-09-21"

STRAP_AMOUNT = "14.95"
STRAP_HANDLE = "hlth-arm-band"
STRAP_ATTR = 'data-price="price" data-price-handle="%s"' % STRAP_HANDLE

# unchanged by this pass; asserted so a regression shows up here
EXPECT_EXISTING = {"price": 16, "compare": 5, "fx": 38}

DRY = "--dry-run" in sys.argv

POUND = r"(?:£|&pound;|&#163;)"
GAP = r"(?:\s|&nbsp;)*"
AMOUNT = r"\d{1,3}(?:,\d{3})*(?:\.\d{1,2})?"
MONEY = re.compile(POUND + GAP + "(" + AMOUNT + r")(?!\d|[.,]\d)")
TAGSPLIT = re.compile(r"(<[^>]+>)")


def tag_strap(content, counts):
    parts = TAGSPLIT.split(content)
    for i, part in enumerate(parts):
        if not part or part.startswith("<"):
            continue
        matches = [m for m in MONEY.finditer(part) if m.group(1) == STRAP_AMOUNT]
        if not matches:
            continue
        prev = parts[i - 1] if i > 0 else ""
        if "data-price" in prev:
            counts["already"] += 1        # inside an existing tag: leave alone
            continue
        for m in reversed(matches):       # right-to-left keeps offsets valid
            part = (part[:m.start()]
                    + '<span %s>%s</span>' % (STRAP_ATTR, m.group(0))
                    + part[m.end():])
            counts["strap"] += 1
        parts[i] = part
    return "".join(parts)


def walk(node, counts):
    if isinstance(node, dict):
        p = node.get("p")
        if isinstance(p, dict):
            c = p.get("content")
            if isinstance(c, str) and STRAP_AMOUNT in c:
                p["content"] = tag_strap(c, counts)
        for v in node.values():
            walk(v, counts)
    elif isinstance(node, list):
        for v in node:
            walk(v, counts)


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
            # The ~10 MB all-steps response gets its socket reset mid-stream
            # often enough to matter. It is transient and the request is a
            # read, so retrying is always safe.
            if isinstance(e, (ConnectionResetError, ConnectionError, OSError))                     or "10054" in m or "forcibly closed" in m                     or "Connection reset" in m or "timed out" in m:
                print("    connection dropped, retrying in 20s", flush=True)
                time.sleep(20)
                continue
            raise
    raise RuntimeError("gave up")


tok = open(".session_token").read().strip()
acct = open(".lf_account").read().strip()
h = lf_api.session_headers(acct)

CACHE = os.path.join(BACKUP_DIR, "_cache-google-uk-steps.json")
if "--from-cache" in sys.argv and os.path.exists(CACHE):
    with io.open(CACHE, encoding="utf-8") as fh:
        _c = json.load(fh)
    print("reading from cache fetched %s" % _c["fetched_at"])
    node_all = {"steps": _c["steps"]}
else:
    node_all = go(lambda: lf_api.get_funnel_steps(tok, FUNNEL, extra_headers=h))
    # Refresh the cache on every live read, so a dry run pays the ten minutes
    # once and the real run that follows it reuses the SAME bytes. Previously a
    # dry run and its apply were two separate fetches of the same ~10 MB, which
    # is both slow and a second chance for the socket to drop.
    with io.open(CACHE, "w", encoding="utf-8") as fh:
        json.dump({"funnel": FUNNEL,
                   "fetched_at": time.strftime("%Y-%m-%dT%H:%M:%S"),
                   "steps": node_all["steps"]}, fh, ensure_ascii=False)
    print("cache refreshed")
step = next((s for s in node_all["steps"] if s["slug"] == TARGET_SLUG), None)
assert step is not None, "step %r not found" % TARGET_SLUG
assert step["slug"] != FORBIDDEN_SLUG
print("target: %s | slug=%s" % (step["uid"], step["slug"]))

body = copy.deepcopy(step.get("body"))
settings = copy.deepcopy(step.get("settings") or {})

pre = json.dumps(body, ensure_ascii=False)
before = {"price": pre.count('data-price=\\"price\\"'),
          "compare": pre.count('data-price=\\"compare\\"'),
          "fx": pre.count("data-fx-gbp=")}
print("existing tags: %s" % before)
for k, want in EXPECT_EXISTING.items():
    assert before[k] == want, "%s is %d, expected %d - page changed" % (k, before[k], want)

# ------------------------------------------------------------------ strap
from collections import Counter  # noqa: E402
counts = Counter()
walk(body, counts)
print("\nstrap tagged: %d   (already inside a tag: %d)" % (counts["strap"], counts["already"]))
assert counts["strap"] == 1, "expected exactly one GBP14.95, tagged %d" % counts["strap"]

post = json.dumps(body, ensure_ascii=False)
after = {"price": post.count('data-price=\\"price\\"'),
         "compare": post.count('data-price=\\"compare\\"'),
         "fx": post.count("data-fx-gbp=")}
print("tags now     : %s" % after)
# the strap adds one more data-price="price"; nothing else may move
assert after["price"] == before["price"] + 1, "price tags moved unexpectedly"
assert after["compare"] == before["compare"] and after["fx"] == before["fx"]
assert post.count("data-price-handle=") == 1, "handle tag count wrong"

# ------------------------------------------------------------------ header
ch = settings.get("custom_html") or {}
hdr = ch.get("header") or ""
ff_before = hdr.count("@font-face")
assert MARKER in hdr, "marker missing - was the script ever installed?"
head_part = hdr.split(MARKER)[0].rstrip()
script = io.open(SCRIPT_FILE, encoding="utf-8").read().strip()
new_hdr = head_part + "\n\n" + MARKER + "\n" + script + "\n"
ch["header"] = new_hdr
settings["custom_html"] = ch

print("\nheader: %d -> %d chars" % (len(hdr), len(new_hdr)))
print("  @font-face      %d -> %d" % (ff_before, new_hdr.count("@font-face")))
print("  marker          %d" % new_hdr.count(MARKER))
print("  script copies   %d" % new_hdr.count("var PRICES"))
print("  noindex kept    %s" % ("noindex" in new_hdr))
print("  products=all    %s" % ("products=all" in new_hdr))
print("  MAIN_HANDLE     %s" % ("wearable-hlth-band" in new_hdr))
assert new_hdr.count("@font-face") == ff_before, "font-face lost"
assert new_hdr.count(MARKER) == 1 and new_hdr.count("var PRICES") == 1
assert "noindex" in new_hdr and "products=all" in new_hdr

with io.open(os.path.join(BACKUP_DIR, "%s.pre-multiproduct-%s.json" % (TARGET_SLUG, STAMP)),
             "w", encoding="utf-8") as fh:
    json.dump({"settings": step.get("settings"), "body": step.get("body")},
              fh, ensure_ascii=False)
print("\nbacked up pre-upgrade body + settings")

if DRY:
    sys.exit("\nDRY RUN - nothing written.")

go(lambda: lf_api.gql(
    tok, "mutation($id:ID!,$node:InputFunnel!){updateFunnel(id:$id,node:$node){id}}",
    {"id": FUNNEL, "node": {"steps": [{
        "id": step["uid"], "slug": step["slug"], "title": step["title"],
        "type": step["type"], "settings": settings,
        "visual": step.get("visual"), "body": body}]}}, extra_headers=h))
print("WRITTEN.")

# ------------------------------------------------------------------ verify
time.sleep(4)
import urllib.request  # noqa: E402
BASE = "https://www.techunboxed.co/article/"


def fetch(slug):
    req = urllib.request.Request(BASE + slug, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=90) as r:
        return r.read().decode("utf-8", "replace")


page = fetch(TARGET_SLUG)
# strip <script> first: the script carries its own selectors as literal text
markup = re.sub(r"<script\b[^>]*>.*?</script>", " ", page, flags=re.S | re.I)
print("\nLIVE page:")
print("  data-price=\"price\"    %d (expect %d)" % (
    markup.count('data-price="price"'), EXPECT_EXISTING["price"] + 1))
print("  data-price-handle     %d (expect 1)" % markup.count("data-price-handle="))
print("  data-fx-gbp           %d (expect %d)" % (
    markup.count("data-fx-gbp="), EXPECT_EXISTING["fx"]))
print("  script copies         %d" % page.count("var PRICES"))
print("  products=all present  %s" % ("products=all" in page))
assert markup.count('data-price="price"') == EXPECT_EXISTING["price"] + 1
assert markup.count("data-price-handle=") == 1
assert markup.count("data-fx-gbp=") == EXPECT_EXISTING["fx"]
assert page.count("var PRICES") == 1

win = fetch(FORBIDDEN_SLUG)
print("  live winner clean     %s" % (win.count("data-price=") == 0))
assert win.count("data-price=") == 0, "THE LIVE WINNER WAS MODIFIED"

print("\nQA: https://www.techunboxed.co/article/%s?country=PH" % TARGET_SLUG)
