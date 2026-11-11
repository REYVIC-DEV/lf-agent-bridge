#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Stop Cloudflare Stream videos from killing Lenis smooth scroll.

RYAN, 2026-10-29: "it's jumpy and not smooth" on /article/jFrY0DhRi.

THE CAUSE. A browser does not deliver wheel events from a cross-origin iframe up
to the page embedding it. Lenis listens on the page, so while the cursor sits
over a Cloudflare Stream video it never hears the wheel, and the browser falls
back to its own instant scroll. Measured on the live page, same wheel tick, only
the cursor position different:

    cursor over the article text   58 scroll positions drawn   smooth ease
    cursor over a video             2 scroll positions drawn   400px teleport

Four videos on that page, in the left column, 382px wide against a 416px text
column. So nearly half the article's width is a band where smooth scroll silently
switches off, and a read down the page jerks four times.

THE FIX. Let the pointer pass through the iframe, which hands the wheel back to
Lenis. Verified in the live page before this script was written: 2 positions
became 48-58 on all four videos.

WHY IT CANNOT BREAK A VIDEO. The selector carries its own two guards:

  html.lenis ...   only when Lenis is actually running. Lenis stamps `lenis` on
                   <html> and only on desktop, so on mobile and touch the rule
                   does not apply and the videos keep normal pointer behaviour.
  [src*="controls=false"]
                   only a video with NO controls - a decorative muted autoplay
                   loop with nothing to click. A video a visitor is meant to
                   operate keeps its pointer, automatically, with no list to
                   maintain.

Every Cloudflare video in the account was checked before this was written: 43 of
them across 6 pages, and all 43 are controls=false. There is no clickable one to
break.

WHO GETS IT. Only funnels that have BOTH Lenis and a Cloudflare video:

    Google funnels - UK    article/jFrY0DhRi     4 videos   Ryan's page
    Native funnels - UK    blog-post/zQkAffXHg   3 videos
    Garlic Funnel          aged-garlic/lp-1     33 videos   no public domain yet

  NOT LISTICLES [ON DEV], which has 10 videos across 3 pages but carries no
  Lenis at all - nothing there to make jumpy, so nothing to fix.

WARNING - SURGICAL INSERT, NOT AN OVERWRITE. The three headers are NOT the same
file and none matches snippets/ byte for byte: google-uk is 28,924 chars against
the snippet's 26,796, Native UK is 22,323 and still loads Lenis unconditionally,
Garlic is 22,721. Writing a snippet over any of them would silently revert
whatever has changed since 2026-10-04. So this reads each funnel's OWN live
header, inserts one line, and proves byte-for-byte that nothing else moved.

    py pagescore/fix_lenis_video_pointer.py --dry-run
    py pagescore/fix_lenis_video_pointer.py
"""
import hashlib
import io
import os
import re
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, ".."))
sys.path.insert(0, ROOT)
os.chdir(ROOT)
import lf_api  # noqa: E402

BACKUPS = os.path.join(HERE, "header_backups")
STAMP = "2026-10-29"
DRY = "--dry-run" in sys.argv

TARGETS = [
    ("fun_p9Y_FwGlQsaP5bpW70q5N", "Google funnels - UK", "article"),
    ("fun_B2PKx4t5Pat-ZkpCN7tPI", "Native funnels - UK", "blog-post"),
    ("fun__LKgKGNO4H6IoYoFN6RfK", "Garlic Funnel", "aged-garlic"),
]

MARKER = "lenis-video-pointer"
RULE = (
    "\n"
    "  /* " + MARKER + ": a cross-origin iframe swallows the wheel, so Lenis goes deaf\n"
    "     while the cursor is over a Cloudflare video and the browser instant-scrolls\n"
    "     instead of easing. Measured on /article/jFrY0DhRi 2026-10-29: 58 positions\n"
    "     drawn per wheel tick over text, 2 over a video. Passing the pointer through\n"
    "     hands the wheel back to Lenis. Guarded twice - html.lenis so it is desktop\n"
    "     only and only while Lenis runs, controls=false so a video with controls a\n"
    "     visitor is meant to click keeps its pointer. */\n"
    '  html.lenis iframe[src*="cloudflarestream.com"][src*="controls=false"]'
    " { pointer-events: none; }\n"
)

# The last line of the inlined Lenis CSS. Anchored on the selector only, so a
# change in spacing or in the declaration does not make the insert miss.
ANCHOR = re.compile(r"^[ \t]*html\.lenis\.lenis-stopped\b[^\n]*\n", re.M)

Q = "query($id:ID!){node(id:$id){... on Funnel{name header_scripts}}}"
MUT = "mutation($id:ID!,$node:InputFunnel!){updateFunnel(id:$id,node:$node){id}}"

tok = open(".session_token").read().strip()
acct = open(".lf_account").read().strip()
h = lf_api.session_headers(acct)


def sha(s):
    return hashlib.sha1(s.encode("utf-8")).hexdigest()[:10]


def go(fn, tries=6):
    delay = 30
    for _ in range(tries):
        try:
            return fn()
        except Exception as e:
            m = str(e)
            if "expired" in m.lower():
                sys.exit("Session expired. Run: py lf.py login")
            if "rate_limit" in m or "Rate limit" in m:
                print("    rate limited, waiting %ds" % delay, flush=True)
                time.sleep(delay)
                delay = min(delay * 2, 240)
                continue
            if "502" in m or "Bad Gateway" in m:
                time.sleep(60)
                continue
            raise
    raise RuntimeError("gave up")


def patch(fid, name, slug):
    print("\n=== %s  (%s)" % (name, fid))
    node = go(lambda: lf_api.gql(tok, Q, {"id": fid}, extra_headers=h))["node"]
    old = node.get("header_scripts") or ""
    print("  live name  : %s" % node.get("name"))
    print("  header     : %d chars  sha=%s" % (len(old), sha(old)))

    if MARKER in old:
        print("  ALREADY INSTALLED - skipping")
        return "skip"

    # Lenis must actually be in this header, or the rule has nothing to help.
    assert "html.lenis" in old, "no Lenis CSS in this header"
    hits = ANCHOR.findall(old)
    assert len(hits) == 1, "expected 1 lenis-stopped line, found %d" % len(hits)

    m = ANCHOR.search(old)
    new = old[:m.end()] + RULE + old[m.end():]

    # WARNING - PROVE NOTHING ELSE MOVED. Remove exactly what was inserted and the
    # result must be the original, byte for byte. This is the whole safety argument
    # for editing a header that matches no snippet.
    assert new.replace(RULE, "", 1) == old, "the insert disturbed surrounding bytes"
    assert len(new) == len(old) + len(RULE)
    assert new.count(MARKER) == 1
    assert new.count("pointer-events: none") == old.count("pointer-events: none") + 1
    # The tracker must survive untouched - a broken tracker still looks healthy.
    for probe in ("posthog.init", "gtm.start", "<style", "</style>", "new Lenis"):
        assert new.count(probe) == old.count(probe), "%s count changed" % probe
    print("  new header : %d chars  sha=%s  (+%d)" % (len(new), sha(new), len(RULE)))
    print("  inserted after: %s" % hits[0].strip())

    os.makedirs(BACKUPS, exist_ok=True)
    bak = os.path.join(BACKUPS, "%s.pre-video-pointer-%s.html" % (slug, STAMP))
    with io.open(bak, "w", encoding="utf-8", newline="") as fh:
        fh.write(old)
    print("  backed up  -> %s" % os.path.relpath(bak, ROOT))

    if DRY:
        print("  DRY RUN - not written")
        return "dry"

    go(lambda: lf_api.gql(tok, MUT, {"id": fid, "node": {"header_scripts": new}},
                          extra_headers=h))
    time.sleep(4)
    back = go(lambda: lf_api.gql(tok, Q, {"id": fid},
                                 extra_headers=h))["node"]["header_scripts"] or ""
    assert back == new, "read-back differs from what was sent (%s vs %s)" % (sha(back), sha(new))
    print("  WRITTEN and read back identical.")
    return "ok"


res = {}
for fid, name, slug in TARGETS:
    res[name] = patch(fid, name, slug)
print("\n%s" % ("DRY RUN" if DRY else "DONE"))
for k, v in res.items():
    print("  %-24s %s" % (k, v))
