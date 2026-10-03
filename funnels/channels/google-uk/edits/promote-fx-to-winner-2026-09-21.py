#!/usr/bin/env python3
"""Promote the dynamic-currency work from dMs4WkOYD-fx onto the LIVE winner.

dMs4WkOYD receives 100% of Google paid traffic. This is the one write in this
funnel that a mistake is immediately expensive on, so every claim below is
asserted rather than assumed.

WHAT MOVES, AND WHAT DELIBERATELY DOES NOT

    body      <- FROM THE TEST PAGE. The tagged one: 17 data-price
                 (16 band + 1 arm band), 5 compare, 38 data-fx-gbp.

    header    <- BUILT FROM THE LIVE PAGE'S OWN HEADER, not copied from the
                 test page, then the marker + script appended.

⚠️⚠️ WHY THE HEADER IS NOT COPIED: the test page's header begins with
    <meta name="robots" content="noindex,nofollow">, added so a byte-identical
    clone could not compete in search with the page earning the traffic.
    Copying that header onto the live page would DEINDEX the advertorial that
    every Google click lands on. Rebuilding from the live header makes that
    impossible rather than merely unlikely, and the result is asserted to
    contain no "noindex" at all.

    title/slug/seo/type/visual all stay the LIVE page's own. The test page's
    title is "... - FX TEST", which must never appear in the workflow.

THE INTEGRITY CHECK THAT MATTERS
    The test page is a copy taken at a point in time. If the live page had been
    edited since, promoting would silently revert that edit. So this does not
    just trust the copy: it STRIPS every tag span out of the test body and
    asserts the result is byte-identical to the live body. If they differ, the
    two have diverged and it refuses to write. That check is the whole reason
    this can be run safely.
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
SRC_SLUG = "dMs4WkOYD-fx"          # tagged staging copy
LIVE_SLUG = "dMs4WkOYD"            # the winner, all paid traffic
SCRIPT_FILE = os.path.join(ROOT, "snippets/dynamic-currency-header-block.html")
MARKER = "<!-- dynamic-currency -->"
BACKUP_DIR = os.path.join(HERE, "..", "steps")
STAMP = "2026-09-21"

EXPECT = {"price": 17, "compare": 5, "fx": 38, "handle": 1}

DRY = "--dry-run" in sys.argv

UNWRAP = re.compile(
    r'<span data-price="[^"]*"(?: data-price-handle="[^"]*")?>(.*?)</span>'
    r'|<span data-fx-gbp="[^"]*">(.*?)</span>')


def unwrap(html):
    """Remove the tag spans this project adds, leaving the original text."""
    prev = None
    out = html
    while prev != out:                       # spans are never nested, but loop
        prev = out                           # so a stray nesting cannot survive
        out = UNWRAP.sub(lambda m: m.group(1) if m.group(1) is not None else m.group(2), out)
    return out


def strip_tags_in_body(node):
    if isinstance(node, dict):
        p = node.get("p")
        if isinstance(p, dict) and isinstance(p.get("content"), str):
            p["content"] = unwrap(p["content"])
        for v in node.values():
            strip_tags_in_body(v)
    elif isinstance(node, list):
        for v in node:
            strip_tags_in_body(v)


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
            if isinstance(e, (ConnectionResetError, ConnectionError, OSError)) or \
                    "10054" in m or "forcibly closed" in m or "Connection reset" in m:
                print("    connection dropped, retrying in 20s", flush=True)
                time.sleep(20)
                continue
            raise
    raise RuntimeError("gave up")


tok = open(".session_token").read().strip()
acct = open(".lf_account").read().strip()
h = lf_api.session_headers(acct)

FQ = """query($id:ID!){node(id:$id){... on Funnel{
  name slug published starting_step_id steps{uid}}}}"""
pre_f = go(lambda: lf_api.gql(tok, FQ, {"id": FUNNEL}, extra_headers=h))["node"]
inv = {k: pre_f.get(k) for k in ("name", "slug", "published", "starting_step_id")}
n_steps = len(pre_f["steps"])

CACHE = os.path.join(BACKUP_DIR, "_cache-google-uk-steps.json")
node_all = go(lambda: lf_api.get_funnel_steps(tok, FUNNEL, extra_headers=h))
with io.open(CACHE, "w", encoding="utf-8") as fh:
    json.dump({"funnel": FUNNEL, "fetched_at": time.strftime("%Y-%m-%dT%H:%M:%S"),
               "steps": node_all["steps"]}, fh, ensure_ascii=False)

src = next(s for s in node_all["steps"] if s["slug"] == SRC_SLUG)
live = next(s for s in node_all["steps"] if s["slug"] == LIVE_SLUG)
print("source: %s (%s)" % (src["uid"], SRC_SLUG))
print("live  : %s (%s)  title=%r" % (live["uid"], LIVE_SLUG, live["title"]))

src_body = copy.deepcopy(src.get("body"))
sb = json.dumps(src_body, ensure_ascii=False)
got = {"price": sb.count('data-price=\\"price\\"'),
       "compare": sb.count('data-price=\\"compare\\"'),
       "fx": sb.count("data-fx-gbp="),
       "handle": sb.count("data-price-handle=")}
print("\nsource tags: %s" % got)
for k, want in EXPECT.items():
    assert got[k] == want, "%s is %d, expected %d" % (k, got[k], want)

live_body = live.get("body")
lb = json.dumps(live_body, ensure_ascii=False)
assert "data-price=" not in lb and "data-fx-gbp=" not in lb, \
    "the live page already carries tags - has this already been promoted?"

# ---- THE INTEGRITY CHECK -----------------------------------------------------
probe = copy.deepcopy(src_body)
strip_tags_in_body(probe)
same = json.dumps(probe, ensure_ascii=False, sort_keys=True) == \
    json.dumps(live_body, ensure_ascii=False, sort_keys=True)
print("\nunwrapped copy == live body: %s" % same)
if not same:
    a = json.dumps(probe, ensure_ascii=False, sort_keys=True)
    b = json.dumps(live_body, ensure_ascii=False, sort_keys=True)
    print("  lengths %d vs %d" % (len(a), len(b)))
    for i in range(min(len(a), len(b))):
        if a[i] != b[i]:
            print("  first difference at %d:\n    copy: %r\n    live: %r"
                  % (i, a[i - 90:i + 90], b[i - 90:i + 90]))
            break
    sys.exit("\nREFUSING TO WRITE. The live page has diverged from the copy, so "
             "promoting would silently revert whatever changed on it.")

# ---- header, built from the LIVE page ----------------------------------------
settings = copy.deepcopy(live.get("settings") or {})
ch = settings.get("custom_html") or {}
hdr = ch.get("header") or ""
ff = hdr.count("@font-face")
assert MARKER not in hdr, "live header already has the marker"
assert "noindex" not in hdr, "live header unexpectedly contains noindex"
script = io.open(SCRIPT_FILE, encoding="utf-8").read().strip()
new_hdr = hdr.rstrip() + "\n\n" + MARKER + "\n" + script + "\n"
ch["header"] = new_hdr
settings["custom_html"] = ch

print("\nheader: %d -> %d chars" % (len(hdr), len(new_hdr)))
print("  @font-face   %d -> %d" % (ff, new_hdr.count("@font-face")))
print("  marker       %d" % new_hdr.count(MARKER))
print("  script       %d" % new_hdr.count("var PRICES"))
print("  NOINDEX      %s  <-- must be False" % ("noindex" in new_hdr))
print("  products=all %s" % ("products=all" in new_hdr))
assert new_hdr.count("@font-face") == ff
assert new_hdr.count(MARKER) == 1 and new_hdr.count("var PRICES") == 1
assert "noindex" not in new_hdr, "REFUSING: would deindex the live advertorial"
assert "products=all" in new_hdr

# seo must survive untouched - it is the page's <title> and description
assert (settings.get("seo") or {}) == ((live.get("settings") or {}).get("seo") or {})

with io.open(os.path.join(BACKUP_DIR, "%s.pre-promote-%s.json" % (LIVE_SLUG, STAMP)),
             "w", encoding="utf-8") as fh:
    json.dump({"settings": live.get("settings"), "body": live.get("body"),
               "title": live.get("title"), "slug": live.get("slug")},
              fh, ensure_ascii=False)
print("\nbacked up the LIVE page pre-promotion")

if DRY:
    sys.exit("\nDRY RUN - nothing written.")

go(lambda: lf_api.gql(
    tok, "mutation($id:ID!,$node:InputFunnel!){updateFunnel(id:$id,node:$node){id}}",
    {"id": FUNNEL, "node": {"steps": [{
        "id": live["uid"], "slug": live["slug"], "title": live["title"],
        "type": live["type"], "settings": settings,
        "visual": live.get("visual"), "body": src_body}]}}, extra_headers=h))
print("WRITTEN to the live page.")

# ---- verify against the rendered page ----------------------------------------
time.sleep(5)
import urllib.request  # noqa: E402


def fetch(slug):
    req = urllib.request.Request("https://www.techunboxed.co/article/" + slug,
                                 headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=90) as r:
        return r.read().decode("utf-8", "replace")


page = fetch(LIVE_SLUG)
# strip BOTH <script> and HTML comments: the script carries its own selectors
# AND example markup in its comment banner, and both get counted otherwise.
m = re.sub(r"<script\b[^>]*>.*?</script>", " ", page, flags=re.S | re.I)
m = re.sub(r"<!--.*?-->", " ", m, flags=re.S)
print("\nLIVE page now:")
print("  data-price=\"price\"   %d (expect %d)" % (m.count('data-price="price"'), EXPECT["price"]))
print("  data-price=\"compare\" %d (expect %d)" % (m.count('data-price="compare"'), EXPECT["compare"]))
print("  data-fx-gbp          %d (expect %d)" % (m.count("data-fx-gbp="), EXPECT["fx"]))
print("  data-price-handle    %d (expect %d)" % (m.count("data-price-handle="), EXPECT["handle"]))
print("  script copies        %d" % page.count("var PRICES"))
print("  NOINDEX on live      %s  <-- must be False" % ("noindex" in page.lower()))
assert m.count('data-price="price"') == EXPECT["price"]
assert m.count('data-price="compare"') == EXPECT["compare"]
assert m.count("data-fx-gbp=") == EXPECT["fx"]
assert m.count("data-price-handle=") == EXPECT["handle"]
assert page.count("var PRICES") == 1
assert "noindex" not in page.lower(), "THE LIVE PAGE IS NOINDEXED - REVERT NOW"

post_f = go(lambda: lf_api.gql(tok, FQ, {"id": FUNNEL}, extra_headers=h))["node"]
bad = [k for k, v in inv.items() if post_f.get(k) != v]
print("  funnel invariants    %s" % ("OK" if not bad else "CHANGED %s" % bad))
print("  step count           %d (was %d)" % (len(post_f["steps"]), n_steps))
assert not bad and len(post_f["steps"]) == n_steps

print("\nQA: https://www.techunboxed.co/article/%s?country=PH" % LIVE_SLUG)
