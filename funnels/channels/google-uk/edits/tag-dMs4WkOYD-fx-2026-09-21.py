#!/usr/bin/env python3
"""Tag every money figure on the FX TEST step and install the currency script.

Runs against `dMs4WkOYD-fx` ONLY. It refuses to run against `dMs4WkOYD`, which
is the live winner taking 100% of Google paid traffic.

THE CLASSIFICATION, from the 2026-09-21 count of 60 figures:

    £79     x16  -> data-price="price"     OUR band, Shopify feed, exact
    £158    x5   -> data-price="compare"   OUR was-price
    £14.95  x1   -> LEFT IN GBP            our bicep strap: ours, so the mid-market
                                           converter must not price it, but
                                           /api/prices only carries the band's
                                           handle so there is no exact figure
                                           either. Neither feed is correct, so it
                                           stays honest rather than localised.
    everything else x38 -> data-fx-gbp     competitors + editorial sums

WHY A VALUE TABLE IS SAFE HERE
    All 16 £79 are ours, all 5 £158 are ours, and no competitor figure collides
    on those two values. The script ASSERTS each count, so if the copy changes
    and a £79 appears meaning something else, it fails loudly instead of quietly
    pricing a competitor with our Shopify feed.

    ⚠️ COUNT FROM TWO SOURCES BEFORE TRUSTING A NUMBER. The first pass asserted
    57 and was wrong; the tagger found 60 and looked like it was over-matching.
    The tempting fix - relax the assertion to whatever the code produced - would
    have shipped whichever of the two was broken. Walking the block tree AND
    counting the rendered live page agree at 60, and that agreement is the only
    reason these numbers can be trusted.

⚠️ £79.99 CONTAINS £79. Fitbit's price would be tagged as our band by any naive
   find/replace, quoting £79 where the page says £79.99. The amount pattern ends
   in (?!\\d|[.,]\\d) so £79 cannot match inside £79.99, and matches are rewritten
   RIGHT-TO-LEFT so earlier offsets stay valid.

⚠️ A SENTENCE-ENDING PERIOD IS NOT PART OF THE NUMBER. The first version of this
   lookahead was (?![\\d,.]), which refused "£14.95.", "£79." and "£158." and so
   found 54 of the 57 figures. Diffing the block JSON against the RENDERED live
   page is what surfaced it, and it is the cheaper check of the two.

⚠️ REPLACE ONLY IN TEXT, NEVER INSIDE A TAG. The content is HTML; splitting on
   tags keeps the pattern away from attributes and urls.

⚠️ WRAP THE FIGURE IN ITS OWN SPAN. The script replaces the tagged element's
   whole textContent, so the tagged element must contain the figure and nothing
   else. Wrapping guarantees that; tagging an existing span that also holds copy
   would delete the copy.

⚠️ £0 GOES THROUGH FX, NOT data-price. fmt() refuses n <= 0 for a price because a
   zero renders a free product; the FX path formats a real zero, which is what a
   "no year-2 subscription" cell means.
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
TARGET_SLUG = "dMs4WkOYD-fx"
FORBIDDEN_SLUG = "dMs4WkOYD"
SCRIPT_FILE = os.path.join(ROOT, "snippets/dynamic-currency-header-block.html")
MARKER = "<!-- dynamic-currency -->"
BACKUP_DIR = os.path.join(HERE, "..", "steps")
STAMP = "2026-09-21"

DRY = "--dry-run" in sys.argv

OURS_PRICE = {"79"}
OURS_COMPARE = {"158"}
SKIP = {"14.95"}                       # our strap; see the docstring

# Confirmed by TWO independent sources on 2026-09-21: walking the block tree,
# and counting the rendered live page. Both give 60.
#
# ⚠️ The first inventory said 57 and was WRONG. Its lookahead was (?![\d,]),
#    which rejects a figure followed by a COMMA, so "£79, once." matched nothing
#    at all and two whole blocks were invisible:
#        "£79, once. Over two years the Whoop costs £458, ..."
#        "For £79, once, that's not a hard call."
#    The reference doc warns that £[\d,]+ SWALLOWS a trailing comma; this is the
#    same trap from the other side, where the figure is dropped instead. The
#    pattern below distinguishes the two roles a comma plays: ",\d{3}" is a
#    thousands separator and stays inside the number, any other comma ends it.
EXPECT = {"price": 16, "compare": 5, "fx": 38, "skip": 1}

# A pound sign may be literal or an entity; a space may be a real space or nbsp.
POUND = r"(?:£|&pound;|&#163;)"
GAP = r"(?:\s|&nbsp;)*"
AMOUNT = r"\d{1,3}(?:,\d{3})*(?:\.\d{1,2})?"
# ⚠️ The lookahead must reject only a CONTINUATION of the number, not a
# sentence-ending period. `(?![\d,.])` refused "£14.95." / "£79." / "£158."
# and silently lost 3 of the 57 figures; caught by diffing against the
# rendered live page. `[.,]\d` keeps £79 from matching inside £79.99.
MONEY = re.compile(POUND + GAP + "(" + AMOUNT + r")(?!\d|[.,]\d)")
TAGSPLIT = re.compile(r"(<[^>]+>)")


def classify(raw):
    n = raw.replace(",", "")
    if n in SKIP:
        return None
    if n in OURS_PRICE:
        return ('data-price="price"', "price")
    if n in OURS_COMPARE:
        return ('data-price="compare"', "compare")
    return ('data-fx-gbp="%s"' % n, "fx")


def tag_html(content, counts):
    """Wrap every money figure in the text of `content`. Returns new html."""
    parts = TAGSPLIT.split(content)
    for i, part in enumerate(parts):
        if not part or part.startswith("<"):
            continue                                    # a tag: never touch
        matches = list(MONEY.finditer(part))
        if not matches:
            continue
        for m in reversed(matches):                     # right-to-left
            c = classify(m.group(1))
            if c is None:
                counts["skip"] += 1
                continue
            attr, kind = c
            counts[kind] += 1
            part = part[:m.start()] + '<span %s>%s</span>' % (attr, m.group(0)) + part[m.end():]
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


tok = open(".session_token").read().strip()
acct = open(".lf_account").read().strip()
h = lf_api.session_headers(acct)

# Reading costs ten minutes over the API (no single-step query exists), so allow
# the cache written by cache-step-body.py. Safe here because nothing else edits
# this funnel; re-cache first if that stops being true.
CACHE = os.path.join(BACKUP_DIR, "_cache-google-uk-steps.json")
if "--from-cache" in sys.argv and os.path.exists(CACHE):
    with io.open(CACHE, encoding="utf-8") as fh:
        cached = json.load(fh)
    print("reading from cache fetched %s" % cached["fetched_at"])
    node_all = {"steps": cached["steps"]}
else:
    node_all = go(lambda: lf_api.get_funnel_steps(tok, FUNNEL, extra_headers=h))
step = next((s for s in node_all["steps"] if s["slug"] == TARGET_SLUG), None)
if step is None:
    sys.exit("step %r not found - run dup-dMs4WkOYD-for-fx first." % TARGET_SLUG)
assert step["slug"] != FORBIDDEN_SLUG, "refusing to touch the live winner"
print("target: %s | slug=%s" % (step["uid"], step["slug"]))

body = copy.deepcopy(step.get("body"))
settings = copy.deepcopy(step.get("settings") or {})

# IDEMPOTENCY, checked on the ORIGINAL body. Running twice would wrap each
# already-tagged figure in a second span (tag_html splits tags out, so the inner
# "£79" is still bare text to it), and nested tags mean the outer one's
# textContent gets rewritten with the inner one still inside. Catch it here,
# where the state is unambiguous, rather than trying to spot nesting afterwards.
pre = json.dumps(body, ensure_ascii=False)
if "data-price=" in pre or "data-fx-gbp=" in pre:
    sys.exit("This step is ALREADY tagged. Re-running would double-wrap. "
             "Restore from steps/%s.pre-tag-*.json first." % TARGET_SLUG)

# ------------------------------------------------------------------ tag
counts = Counter()
walk(body, counts)
print("\ntagged: price=%d compare=%d fx=%d skipped=%d (total %d)" % (
    counts["price"], counts["compare"], counts["fx"], counts["skip"],
    counts["price"] + counts["compare"] + counts["fx"] + counts["skip"]))
for k, want in EXPECT.items():
    got = counts[k]
    flag = "OK" if got == want else "MISMATCH (expected %d)" % want
    print("  %-8s %3d  %s" % (k, got, flag))
    assert got == want, "%s count %d != expected %d - copy changed, re-inventory" % (
        k, got, want)

# ⚠️ json.dumps ESCAPES THE QUOTES: data-price="price" is stored in the dumped
# string as data-price=\"price\". Asserting on the unescaped form always fails,
# the same way a £ regex over a dumped body matches nothing because ensure_ascii
# turned it into £. Match on the attribute NAME, which needs no quoting.
blob = json.dumps(body, ensure_ascii=False)
assert "data-price=" in blob and "data-fx-gbp=" in blob, "nothing was tagged"
# Every tagged span must close immediately after its figure - no nesting, and
# no copy swallowed into a tagged element (whose textContent gets replaced).
import re as _re  # noqa: E402
bad = _re.findall(r'<span data-(?:price|fx-gbp)="[^"]*">(?:(?!</span>).){40,}',
                  blob.replace('\\"', '"'))
assert not bad, "a tagged span holds more than a figure: %r" % (bad[:1],)

# ------------------------------------------------------------------ header
ch = settings.get("custom_html") or {}
hdr = ch.get("header") or ""
ff_before = hdr.count("@font-face")
if MARKER in hdr:
    sys.exit("marker already present - script installed. Nothing to do.")
script = io.open(SCRIPT_FILE, encoding="utf-8").read().strip()
new_hdr = hdr.rstrip() + "\n\n" + MARKER + "\n" + script + "\n"
ch["header"] = new_hdr
settings["custom_html"] = ch

print("\nheader: %d -> %d chars" % (len(hdr), len(new_hdr)))
print("  @font-face   %d -> %d  %s" % (ff_before, new_hdr.count("@font-face"),
                                       "OK" if new_hdr.count("@font-face") == ff_before
                                       else "CHANGED!"))
print("  marker count %d" % new_hdr.count(MARKER))
print("  noindex kept %s" % ("noindex" in new_hdr))
assert new_hdr.count("@font-face") == ff_before, "font-face lost - would drop to system font"
assert new_hdr.count(MARKER) == 1
# ⚠️ Count "var PRICES", not "api/prices": the url appears TWICE in one copy
# of the script (comment header + the const), so counting it reports two
# copies of a single correct install.
assert new_hdr.count("var PRICES") == 1, "more than one copy of the script"

os.makedirs(BACKUP_DIR, exist_ok=True)
with io.open(os.path.join(BACKUP_DIR, "%s.pre-tag-%s.json" % (TARGET_SLUG, STAMP)),
             "w", encoding="utf-8") as fh:
    json.dump({"settings": step.get("settings"), "body": step.get("body")},
              fh, ensure_ascii=False)
print("\nbacked up pre-tag body + settings")

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
# Verify against the RENDERED page, not another 10-minute API read. It is
# seconds instead of minutes, and it proves what is actually SERVED rather than
# what is stored - which is the thing that matters and the stricter check.
time.sleep(4)
import urllib.request  # noqa: E402

BASE = "https://www.techunboxed.co/article/"


def fetch(slug):
    req = urllib.request.Request(BASE + slug, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=90) as r:
        return r.read().decode("utf-8", "replace")


page = fetch(TARGET_SLUG)

# ⚠️ STRIP <script> BEFORE COUNTING. The installed script contains its own
# selectors as literal text - '[data-price="price"]' and '[data-price="compare"]'
# - so counting the raw page reports 17 and 6 for a correct 16 and 5. It does
# NOT affect data-fx-gbp, because the script writes that one as [data-fx-gbp]
# with no "=", which is exactly why only two of the three counts looked wrong.
markup = re.sub(r"<script\b[^>]*>.*?</script>", " ", page, flags=re.S | re.I)
got = {
    "price": markup.count('data-price="price"'),
    "compare": markup.count('data-price="compare"'),
    "fx": markup.count("data-fx-gbp="),
}
print("\nread-back from the LIVE page:")
for k in ("price", "compare", "fx"):
    print("  %-8s %3d  %s" % (k, got[k], "OK" if got[k] == EXPECT[k]
                              else "MISMATCH (expected %d)" % EXPECT[k]))
print("  script copies   %d" % page.count("var PRICES"))
print("  marker          %d" % page.count(MARKER))
print("  @font-face      %d (stored had %d)" % (page.count("@font-face"), ff_before))
print("  noindex kept    %s" % ("noindex" in page))
for k in ("price", "compare", "fx"):
    assert got[k] == EXPECT[k], "%s rendered %d, expected %d" % (k, got[k], EXPECT[k])
assert page.count("var PRICES") == 1, "script installed more than once"

# £14.95 must still be in pounds: it is ours, and neither feed can price it.
assert "£14.95" in page or "14.95" in page, "the strap price vanished"

# The live winner must carry NO tags at all.
win = fetch(FORBIDDEN_SLUG)
print("  live winner clean: %s" % (win.count("data-price=") == 0
                                   and win.count("data-fx-gbp=") == 0))
assert win.count("data-price=") == 0 and win.count("data-fx-gbp=") == 0, \
    "THE LIVE WINNER WAS MODIFIED"

print("\nQA: https://www.techunboxed.co/article/%s?country=PH" % TARGET_SLUG)
