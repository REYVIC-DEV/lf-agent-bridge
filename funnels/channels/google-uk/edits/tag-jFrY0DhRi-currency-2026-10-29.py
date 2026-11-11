#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Convertible pricing on /article/jFrY0DhRi ("HLTH vs Smartwatch").

Ryan asked for this page to carry convertible pricing, 2026-10-29. It is the
same job already shipped on `dMs4WkOYD` in this funnel, and a far smaller one:
that page carries 60 money figures, this one carries 10.

THE CLASSIFICATION, counted twice (block tree and rendered live page, both 10):

    GBP 79   x4  -> data-price="price"   OUR band. Shopify feed, exact, matches
                                         checkout. Bare data-price means the main
                                         band handle, which is what we sell here.
    GBP 500  x6  -> data-fx-gbp="500"    The smartwatch the author ditched. Not a
                                         real product we sell, so mid-market FX is
                                         the only available figure and is the
                                         correct one: it is editorial, not a quote.

There is no compare-at figure on this page, so no data-price="compare".

WHY A VALUE TABLE IS SAFE HERE. Only two distinct amounts exist and they never
swap roles: all four 79s are ours, all six 500s are the rival's. The counts are
asserted, so if the copy ever changes and a GBP 79 turns up meaning something
else, this fails loudly instead of quietly pricing a competitor from our
Shopify feed.

⚠️ THE COMMA TRAP, which this page actually contains. Block 3 reads
   "4. It Cost Me GBP 79, Not GBP 500". A lookahead of (?![\\d,]) rejects a
   figure followed by a comma outright, so that whole heading would match
   NOTHING and two of the ten figures would vanish silently. The lookahead below
   distinguishes the two roles a comma plays: ",\\d{3}" is a thousands separator
   and stays inside the number, any other comma ends it.

⚠️ WHAT GOES IN THE HEADER IS THE PAGE TAG, NOT THE INLINE BLOCK. Since
   2026-09-27 the logic lives at hlthtrack.com/dynamic-currency.js and the page
   installs a small stub plus a deferred <script src>. Verified against the live
   dMs4WkOYD, which serves exactly that and zero copies of "var PRICES". The old
   inline snippets/dynamic-currency-header-block.html is the SOURCE of that
   hosted file, not what any page runs. Installing it here would run two copies
   of the logic.

   This step's custom_html.header is EMPTY (0 chars), so there is no @font-face
   and no noindex tag to preserve. The GTM / PostHog / Lenis universal block
   lives at FUNNEL level in header_scripts and is untouched by this.

⚠️ THE OVERSTATED COMPARISON IS ACCEPTED, NOT NEW. Our band is a price-list
   override in PH, ZA, PL and HR while the GBP 500 watch converts at full
   mid-market, so in those four markets the page shows a bigger gap than the GBP
   reality (PH by ~2.7x). Joshua accepted this on 2026-09-21: "the conversion of
   the competitor prices are fine". Recorded so the next person does not think
   it is a bug. See CURRENCY_CONVERTER.md.

SCOPE: this one step. Joshua, 2026-10-29: just this page. The other 12 steps in
the funnel are untouched, and dMs4WkOYD must stay exactly as it is.

    py funnels/channels/google-uk/edits/tag-jFrY0DhRi-currency-2026-10-29.py --dry-run
    py funnels/channels/google-uk/edits/tag-jFrY0DhRi-currency-2026-10-29.py
"""
import copy
import io
import json
import os
import re
import sys
import time
from collections import Counter

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", "..", "..", ".."))
sys.path.insert(0, ROOT)
os.chdir(ROOT)
import lf_api  # noqa: E402

FUNNEL = "fun_p9Y_FwGlQsaP5bpW70q5N"
TARGET_SLUG = "jFrY0DhRi"
PROTECTED = ("dMs4WkOYD", "dMs4WkOYD-fx", "comparison-1")
TAG_FILE = os.path.join(ROOT, "snippets", "dynamic-currency-page-tag.html")
MARKER = "<!-- dynamic-currency -->"
STEPS_DIR = os.path.join(HERE, "..", "steps")
CACHE = os.path.join(STEPS_DIR, "_cache-google-uk-steps.json")
STAMP = "2026-10-29"

DRY = "--dry-run" in sys.argv

OURS_PRICE = {"79"}
EXPECT = {"price": 4, "fx": 6}

# A pound sign may be literal or an entity; a space may be real or nbsp.
POUND = r"(?:£|&pound;|&#163;)"
GAP = r"(?:\s|&nbsp;)*"
AMOUNT = r"\d{1,3}(?:,\d{3})*(?:\.\d{1,2})?"
# The lookahead rejects only a CONTINUATION of the number, never a sentence
# comma or period. [.,]\d also stops GBP 79 matching inside GBP 79.99.
MONEY = re.compile(POUND + GAP + "(" + AMOUNT + r")(?!\d|[.,]\d)")
TAGSPLIT = re.compile(r"(<[^>]+>)")


def classify(raw):
    n = raw.replace(",", "")
    if n in OURS_PRICE:
        return ('data-price="price"', "price")
    return ('data-fx-gbp="%s"' % n, "fx")


def tag_html(content, counts):
    """Wrap every money figure in the TEXT of `content`, never inside a tag."""
    parts = TAGSPLIT.split(content)
    for i, part in enumerate(parts):
        if not part or part.startswith("<"):
            continue                                   # a tag: never touch
        matches = list(MONEY.finditer(part))
        if not matches:
            continue
        # Right-to-left so earlier offsets stay valid as the string grows.
        for m in reversed(matches):
            attr, kind = classify(m.group(1))
            counts[kind] += 1
            part = (part[:m.start()]
                    + '<span %s>%s</span>' % (attr, m.group(0))
                    + part[m.end():])
        parts[i] = part
    return "".join(parts)


def walk(node, counts):
    if isinstance(node, dict):
        p = node.get("p")
        if isinstance(p, dict):
            c = p.get("content")
            if isinstance(c, str) and MONEY.search(c):
                p["content"] = tag_html(c, counts)
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

# Reading over the API costs ~10 minutes (this funnel has no single-step query),
# so use the cache written by cache-step-body.py. It was refreshed immediately
# before this run; re-run that script if this one is replayed later.
with io.open(CACHE, encoding="utf-8") as fh:
    cached = json.load(fh)
print("cache fetched: %s" % cached["fetched_at"])
step = next((s for s in cached["steps"] if s["slug"] == TARGET_SLUG), None)
if step is None:
    sys.exit("step %r not found" % TARGET_SLUG)
assert step["slug"] not in PROTECTED, "refusing to touch a protected step"
print("target: %s | slug=%s | title=%s" % (step["uid"], step["slug"], step["title"]))

body = copy.deepcopy(step.get("body"))
settings = copy.deepcopy(step.get("settings") or {})

# IDEMPOTENCY, checked on the ORIGINAL body. A second run would wrap each
# already-tagged figure in a second span, and the script rewrites the outer
# element's whole textContent with the inner span still inside it.
pre = json.dumps(body, ensure_ascii=False)
if "data-price=" in pre or "data-fx-gbp=" in pre:
    sys.exit("ALREADY tagged. Re-running would double-wrap. Restore from "
             "steps/%s.pre-tag-*.json first." % TARGET_SLUG)

# ------------------------------------------------------------------ tag
counts = Counter()
walk(body, counts)
total = counts["price"] + counts["fx"]
print("\ntagged: price=%d fx=%d (total %d)" % (counts["price"], counts["fx"], total))
for k, want in sorted(EXPECT.items()):
    got = counts[k]
    print("  %-6s %3d  %s" % (k, got, "OK" if got == want
                              else "MISMATCH (expected %d)" % want))
    assert got == want, "%s count %d != %d - copy changed, re-inventory" % (k, got, want)

# json.dumps ESCAPES THE QUOTES, so asserting on data-price="price" always
# fails. Match the attribute NAME, which needs no quoting.
blob = json.dumps(body, ensure_ascii=False)
assert "data-price=" in blob and "data-fx-gbp=" in blob, "nothing was tagged"
# Every tagged span must close straight after its figure: no nesting, and no
# copy swallowed into an element whose textContent gets replaced.
bad = re.findall(r'<span data-(?:price|fx-gbp)="[^"]*">(?:(?!</span>).){40,}',
                 blob.replace('\\"', '"'))
assert not bad, "a tagged span holds more than a figure: %r" % (bad[:1],)

# ------------------------------------------------------------------ header
ch = settings.get("custom_html") or {}
hdr = ch.get("header") or ""
ff_before = hdr.count("@font-face")
if MARKER in hdr:
    sys.exit("marker already present - script installed. Nothing to do.")
tag = io.open(TAG_FILE, encoding="utf-8").read().strip()
new_hdr = (hdr.rstrip() + "\n\n" + tag + "\n") if hdr.strip() else (tag + "\n")
ch["header"] = new_hdr
settings["custom_html"] = ch

# ⚠️ Count the SCRIPT TAG, not the url. "dynamic-currency.js" appears twice in
# one correct copy of the page tag - once in the explanatory comment and once in
# the src - so counting the url reports two installs of a single clean one. The
# same trap as "api/prices" in the old inline block, which is why that one
# counts "var PRICES" instead.
SRC_TAG = '<script src="https://hlthtrack.com/dynamic-currency.js"'
print("\nheader: %d -> %d chars" % (len(hdr), len(new_hdr)))
print("  @font-face     %d -> %d" % (ff_before, new_hdr.count("@font-face")))
print("  marker count   %d" % new_hdr.count(MARKER))
print("  script tags    %d  (url text appears %dx, comment included)"
      % (new_hdr.count(SRC_TAG), new_hdr.count("dynamic-currency.js")))
print("  stub           %d" % new_hdr.count("data-dc-stub"))
print("  inline logic   %d  (must be 0 - the logic is hosted)"
      % new_hdr.count("var PRICES"))
assert new_hdr.count("@font-face") == ff_before, "font-face lost"
assert new_hdr.count(MARKER) == 1
assert new_hdr.count(SRC_TAG) == 1, "script tag not installed exactly once"
assert new_hdr.count("data-dc-stub") == 1, "anti-flash stub missing"
assert new_hdr.count("var PRICES") == 0, "inline block installed by mistake"

# ------------------------------------------------------------------ backup
os.makedirs(STEPS_DIR, exist_ok=True)
backup = os.path.join(STEPS_DIR, "%s.pre-tag-%s.json" % (TARGET_SLUG, STAMP))
with io.open(backup, "w", encoding="utf-8") as fh:
    json.dump({"settings": step.get("settings"), "body": step.get("body")},
              fh, ensure_ascii=False)
print("\nbacked up pre-tag body + settings -> %s" % os.path.relpath(backup, ROOT))

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
# Against the RENDERED page, not another 10-minute API read: it is seconds, and
# it proves what is actually SERVED rather than what is stored.
time.sleep(5)
import urllib.request  # noqa: E402

BASE = "https://www.techunboxed.co/article/"


def fetch(slug):
    req = urllib.request.Request(BASE + slug, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=90) as r:
        return r.read().decode("utf-8", "replace")


page = fetch(TARGET_SLUG)
# Strip <script> before counting: the stub carries "[data-price],[data-fx-gbp]"
# as literal text and would inflate the counts.
markup = re.sub(r"<script\b[^>]*>.*?</script>", " ", page, flags=re.S | re.I)
got = {"price": markup.count('data-price="price"'),
       "fx": markup.count("data-fx-gbp=")}
print("\nread-back from the LIVE page:")
for k in ("price", "fx"):
    print("  %-6s %3d  %s" % (k, got[k], "OK" if got[k] == EXPECT[k]
                              else "MISMATCH (expected %d)" % EXPECT[k]))
print("  script tags    %d" % page.count(SRC_TAG))
print("  stub           %d" % page.count("data-dc-stub"))
print("  inline logic   %d" % page.count("var PRICES"))
for k in ("price", "fx"):
    assert got[k] == EXPECT[k], "%s rendered %d, expected %d" % (k, got[k], EXPECT[k])
assert page.count(SRC_TAG) == 1, "script tag not served exactly once"
assert page.count("data-dc-stub") == 1, "anti-flash stub not served"
assert page.count("var PRICES") == 0, "inline logic leaked onto the page"

# The neighbours in this funnel must be untouched.
win = fetch("dMs4WkOYD")
win_markup = re.sub(r"<script\b[^>]*>.*?</script>", " ", win, flags=re.S | re.I)
print("  dMs4WkOYD still 17/38: %s" % (
    win_markup.count('data-price="price"') == 17
    and win_markup.count("data-fx-gbp=") == 38))
assert win_markup.count('data-price="price"') == 17, "the winner page changed"

print("\nQA:")
for c in ("PH", "GB", "DE"):
    print("  %s?country=%s" % (BASE + TARGET_SLUG, c))
