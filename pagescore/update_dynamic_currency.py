#!/usr/bin/env python3
"""Re-install the dynamic-currency script on every step that already runs it.

Header-only. The body is never read and never sent.

WHY THAT MATTERS: a step body here is 1-2 MB, so the read-modify-write cycle
these scripts have been using costs ~10 minutes per page. custom_html lives in
`settings`, so a header swap needs no body at all - IF LightFunnels treats an
omitted `body` on InputStep as "leave it alone" rather than "set it to null".

⚠️ THAT IS AN ASSUMPTION ABOUT A WRITE API, AND A WRONG GUESS BLANKS A PAGE.
So --probe runs it against ONE step and verifies the rendered page still has
its content afterwards. Nothing else runs until that comes back clean.

Usage:
    python pagescore/update_dynamic_currency.py --probe <slug>
    python pagescore/update_dynamic_currency.py --only <slug> [<slug> ...]
    python pagescore/update_dynamic_currency.py --all
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

SCRIPT_FILE = os.path.join(ROOT, "snippets/dynamic-currency-header-block.html")
MARKER = "<!-- dynamic-currency -->"
INSTALLS = os.path.join(HERE, "dynamic_currency_installs.json")
BACKUPS = os.path.join(HERE, "header_backups")
MIN_TZ = 100          # the new map has 105; the old one had 53

tok = open(".session_token").read().strip()
acct = open(".lf_account").read().strip()
h = lf_api.session_headers(acct)
SCRIPT = io.open(SCRIPT_FILE, encoding="utf-8").read().strip()
assert len(re.findall(r'"[A-Za-z_]+/[A-Za-z_/]+":"[A-Z]{2}"', SCRIPT)) >= MIN_TZ
assert "TZ_PREFIX" in SCRIPT and "products=all" in SCRIPT


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
                print("    rate limited, waiting %ds" % delay, flush=True)
                time.sleep(delay)
                delay = min(delay * 2, 240)
                continue
            if isinstance(e, (ConnectionResetError, ConnectionError, OSError)) or \
                    "502" in m or "10054" in m or "forcibly closed" in m:
                time.sleep(15)
                continue
            raise
    raise RuntimeError("gave up")


STEPS = """query($id:ID!){node(id:$id){... on Funnel{
  steps{uid slug title type visual{x y} settings}}}}"""
MUT = "mutation($id:ID!,$node:InputFunnel!){updateFunnel(id:$id,node:$node){id}}"


def fetch_live(funnel_slug, slug):
    url = "https://www.techunboxed.co/%s/%s" % (funnel_slug, slug)
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=90) as r:
        return url, r.read().decode("utf-8", "replace")


def markup_only(html):
    """The page's OWN markup, with the installed script's text removed.

    ⚠️ Counting data-price on the raw page counts the SCRIPT, not the page.
    The old script carried '[data-price="price"]' as a CSS selector; the new
    one carries two <span data-price=...> EXAMPLES in its comment banner. So a
    correct header swap reads as "price tags 1 -> 2" and looks like body
    damage. Strip <script> blocks AND html comments before counting anything.
    """
    h = re.sub(r"<script\b[^>]*>.*?<\\?/script>", " ", html, flags=re.S | re.I)
    return re.sub(r"<!--.*?-->", " ", h, flags=re.S)


def update(rec, probe=False):
    print("\n=== %s / %s ===" % (rec["funnel_slug"], rec["slug"]))
    url, before_html = fetch_live(rec["funnel_slug"], rec["slug"])
    bm = markup_only(before_html)
    before = {"bytes": len(before_html),
              "price": bm.count('data-price="price"'),
              "fx": bm.count("data-fx-gbp=")}
    print("  live before: %d bytes, price=%d fx=%d" % (
        before["bytes"], before["price"], before["fx"]))

    node = go(lambda: lf_api.gql(tok, STEPS, {"id": rec["funnel_uid"]},
                                 extra_headers=h))["node"]
    st = next(s for s in node["steps"] if s["uid"] == rec["step"])
    settings = st.get("settings") or {}
    ch = settings.get("custom_html") or {}
    hdr = ch.get("header") or ""
    assert MARKER in hdr, "marker missing on %s" % rec["slug"]
    ff = hdr.count("@font-face")
    had_noindex = "noindex" in hdr

    os.makedirs(BACKUPS, exist_ok=True)
    with io.open(os.path.join(BACKUPS, "%s.%s.header.bak.html" % (
            rec["funnel_slug"], rec["slug"])), "w", encoding="utf-8") as fh:
        fh.write(hdr)

    new_hdr = hdr.split(MARKER)[0].rstrip() + "\n\n" + MARKER + "\n" + SCRIPT + "\n"
    ch["header"] = new_hdr
    settings["custom_html"] = ch

    tz_new = len(re.findall(r'"[A-Za-z_]+/[A-Za-z_/]+":"[A-Z]{2}"', new_hdr))
    print("  header %d -> %d | @font-face %d->%d | tz %d | copies %d | noindex %s" % (
        len(hdr), len(new_hdr), ff, new_hdr.count("@font-face"), tz_new,
        new_hdr.count("var PRICES"), "noindex" in new_hdr))
    assert new_hdr.count("@font-face") == ff, "font-face lost"
    assert new_hdr.count(MARKER) == 1 and new_hdr.count("var PRICES") == 1
    assert tz_new >= MIN_TZ
    assert ("noindex" in new_hdr) == had_noindex, "noindex state changed"

    if "--dry-run" in sys.argv:
        print("  DRY RUN - not written")
        return

    # NOTE: no "body" key. That is the entire point; --probe proves it is safe.
    go(lambda: lf_api.gql(tok, MUT, {"id": rec["funnel_uid"], "node": {"steps": [{
        "id": st["uid"], "slug": st["slug"], "title": st["title"],
        "type": st["type"], "settings": settings, "visual": st.get("visual"),
    }]}}, extra_headers=h))
    print("  written")

    time.sleep(5)
    _, after_html = fetch_live(rec["funnel_slug"], rec["slug"])
    am = markup_only(after_html)
    after = {"bytes": len(after_html),
             "price": am.count('data-price="price"'),
             "fx": am.count("data-fx-gbp=")}
    grew = after["bytes"] - before["bytes"]
    print("  live after : %d bytes (%+d) price=%d fx=%d" % (
        after["bytes"], grew, after["price"], after["fx"]))
    print("  tz rows live: %d | TZ_PREFIX: %s | products=all: %s" % (
        len(re.findall(r'"[A-Za-z_]+/[A-Za-z_/]+":"[A-Z]{2}"', after_html)),
        "TZ_PREFIX" in after_html, "products=all" in after_html))

    # THE BODY-SURVIVED CHECK. The page must still carry all its tagged
    # figures; only the header should have grown.
    assert after["price"] == before["price"], \
        "BODY DAMAGED: price tags %d -> %d" % (before["price"], after["price"])
    assert after["fx"] == before["fx"], \
        "BODY DAMAGED: fx tags %d -> %d" % (before["fx"], after["fx"])
    assert after["bytes"] > before["bytes"] * 0.9, \
        "BODY DAMAGED: page shrank from %d to %d" % (before["bytes"], after["bytes"])
    assert len(re.findall(r'"[A-Za-z_]+/[A-Za-z_/]+":"[A-Z]{2}"', after_html)) >= MIN_TZ
    print("  OK - body intact, new market map live")


recs = json.load(io.open(INSTALLS, encoding="utf-8"))
by_slug = {r["slug"]: r for r in recs}

if "--probe" in sys.argv:
    slug = sys.argv[sys.argv.index("--probe") + 1]
    update(by_slug[slug], probe=True)
    print("\nPROBE CLEAN: an omitted body leaves the page intact.")
elif "--only" in sys.argv:
    for slug in sys.argv[sys.argv.index("--only") + 1:]:
        if slug.startswith("--"):
            break
        update(by_slug[slug])
elif "--all" in sys.argv:
    for r in recs:
        update(r)
else:
    sys.exit(__doc__)
print("\ndone")
