#!/usr/bin/env python3
"""Replace each page's EMBEDDED currency script with the hosted <script src> tag.

After this, hlthtrack.com/dynamic-currency.js is what the pages run, so a change
to the logic is a storefront deploy and touches no Lightfunnels page at all.
That is the entire point: today's market update cost four page edits.

⚠️ SOURCE OF TRUTH MOVES. snippets/dynamic-currency-header-block.html in this repo stays
the source, but editing it no longer changes what any page runs until it is
re-copied into hlth-shopify-frontend/public/ and deployed. If the two drift, the
pages run something that cannot be found by grepping this repo.

Header-only write: `body` is never read or sent. Proven safe by probe on
2026-09-21 (an omitted body leaves the page intact), which is also why this
takes seconds rather than the ten minutes a body round-trip costs.

WHAT REPLACES WHAT
    everything from the <!-- dynamic-currency --> marker to the end of the
    header  ->  the contents of snippets/dynamic-currency-page-tag.html
    Everything BEFORE the marker - @font-face rules, any noindex - is kept
    verbatim and asserted unchanged.
"""
import io
import json
import os
import re
import sys
import time
import urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, ".."))
sys.path.insert(0, ROOT)
os.chdir(ROOT)
import lf_api  # noqa: E402

TAG_FILE = os.path.join(ROOT, "snippets/dynamic-currency-page-tag.html")
HOSTED = "https://hlthtrack.com/dynamic-currency.js"
MARKER = "<!-- dynamic-currency -->"
INSTALLS = os.path.join(HERE, "dynamic_currency_installs.json")
BACKUPS = os.path.join(HERE, "header_backups")

TAG = io.open(TAG_FILE, encoding="utf-8").read().strip()
assert TAG.startswith(MARKER), "the tag file must begin with the marker"
assert HOSTED in TAG and "defer" in TAG
assert "var PRICES" not in TAG, "the tag must not carry the logic"

tok = open(".session_token").read().strip()
acct = open(".lf_account").read().strip()
h = lf_api.session_headers(acct)

STEPS = """query($id:ID!){node(id:$id){... on Funnel{
  steps{uid slug title type visual{x y} settings}}}}"""
MUT = "mutation($id:ID!,$node:InputFunnel!){updateFunnel(id:$id,node:$node){id}}"
UA = {"User-Agent": ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                     "(KHTML, like Gecko) Chrome/140.0 Safari/537.36")}


def go(fn, tries=6):
    delay = 30
    for _ in range(tries):
        try:
            return fn()
        except Exception as e:
            m = str(e)
            if "expired" in m.lower():
                sys.exit("Session expired. Run: python3 lf.py login")
            if "rate_limit" in m or "Rate limit" in m:
                time.sleep(delay)
                delay = min(delay * 2, 240)
                continue
            if isinstance(e, (ConnectionResetError, ConnectionError, OSError)) or \
                    "502" in m or "10054" in m or "forcibly closed" in m:
                time.sleep(15)
                continue
            raise
    raise RuntimeError("gave up")


def fetch(funnel_slug, slug):
    url = "https://www.techunboxed.co/%s/%s" % (funnel_slug, slug)
    req = urllib.request.Request(url, headers=UA)
    with urllib.request.urlopen(req, timeout=90) as r:
        return r.read().decode("utf-8", "replace")


def markup_only(html):
    """Page markup with script bodies and comments removed.

    Counting data-price on the raw page counts the SCRIPT's own text: the old
    inline copy carried selectors and example markup in its banner. That mistake
    has produced three false alarms in this project already.
    """
    x = re.sub(r"<script\b[^>]*>.*?<\\?/script>", " ", html, flags=re.S | re.I)
    return re.sub(r"<!--.*?-->", " ", x, flags=re.S)


def swap(rec):
    print("\n=== %s / %s ===" % (rec["funnel_slug"], rec["slug"]))
    before_html = fetch(rec["funnel_slug"], rec["slug"])
    bm = markup_only(before_html)
    before = {"price": bm.count('data-price="price"'), "fx": bm.count("data-fx-gbp=")}
    print("  tagged figures before: price=%d fx=%d" % (before["price"], before["fx"]))

    node = go(lambda: lf_api.gql(tok, STEPS, {"id": rec["funnel_uid"]},
                                 extra_headers=h))["node"]
    st = next(s for s in node["steps"] if s["uid"] == rec["step"])
    settings = st.get("settings") or {}
    ch = settings.get("custom_html") or {}
    hdr = ch.get("header") or ""
    assert MARKER in hdr, "no marker on %s" % rec["slug"]
    keep = hdr.split(MARKER)[0].rstrip()
    ff = keep.count("@font-face")
    noindex = "noindex" in keep

    os.makedirs(BACKUPS, exist_ok=True)
    with io.open(os.path.join(BACKUPS, "%s.%s.pre-hosted.html" % (
            rec["funnel_slug"], rec["slug"])), "w", encoding="utf-8") as fh:
        fh.write(hdr)

    new_hdr = keep + "\n\n" + TAG + "\n"
    ch["header"] = new_hdr
    settings["custom_html"] = ch

    print("  header %d -> %d chars  (inline logic removed)" % (len(hdr), len(new_hdr)))
    print("  @font-face %d kept | noindex %s kept | marker %d | var PRICES %d | src %d" % (
        new_hdr.count("@font-face"), "noindex" in new_hdr, new_hdr.count(MARKER),
        new_hdr.count("var PRICES"), new_hdr.count(HOSTED)))
    assert new_hdr.count("@font-face") == ff, "font-face lost"
    assert ("noindex" in new_hdr) == noindex, "noindex state changed"
    assert new_hdr.count(MARKER) == 1
    assert new_hdr.count("var PRICES") == 0, "inline logic survived"
    assert new_hdr.count(HOSTED) == 1

    if "--dry-run" in sys.argv:
        print("  DRY RUN - not written")
        return

    go(lambda: lf_api.gql(tok, MUT, {"id": rec["funnel_uid"], "node": {"steps": [{
        "id": st["uid"], "slug": st["slug"], "title": st["title"],
        "type": st["type"], "settings": settings, "visual": st.get("visual"),
    }]}}, extra_headers=h))
    print("  written")

    time.sleep(6)
    after_html = fetch(rec["funnel_slug"], rec["slug"])
    am = markup_only(after_html)
    after = {"price": am.count('data-price="price"'), "fx": am.count("data-fx-gbp=")}
    print("  tagged figures after : price=%d fx=%d" % (after["price"], after["fx"]))
    print("  hosted tag present   : %s" % (HOSTED in after_html))
    print("  inline logic gone    : %s" % ("var PRICES" not in after_html))
    print("  anti-flash stub      : %s" % ("data-dc-stub" in after_html))
    assert after["price"] == before["price"], "tagged figures changed - body damaged"
    assert after["fx"] == before["fx"], "tagged figures changed - body damaged"
    assert HOSTED in after_html and "var PRICES" not in after_html
    print("  OK")


recs = json.load(io.open(INSTALLS, encoding="utf-8"))
by_slug = {r["slug"]: r for r in recs}
args = [a for a in sys.argv[1:] if not a.startswith("--")]
targets = [by_slug[s] for s in args] if args else recs
for r in targets:
    swap(r)
print("\ndone - %d page(s)" % len(targets))
