#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""After ANY page change: do the buttons still work, and is each page still the
page it was?

JOSHUA, 2026-11-02: "it is best to test the buttons everytime we change
something as well as see if other page are still the page they are before",
and "not just for SOF pages this can also happen on other pages tho not much
since this is our only pages that are 2, most are 1 since they are adverts."

WHY THIS EXISTS. A deploy aimed at the Scaling or Failing contact step was
given the wrong env var and wrote the EVENT page into it. `/event/contact`
served the landing page for two days and the n8n contact form was off the site
entirely. Nothing being run could see it: the link resolved 200, the click
navigated, the URL was right, the page rendered perfectly, and it passed two
full responsive sweeps. Every check asked "did the write land" and "does this
look right", and both were true. **None asked "is this the RIGHT page?"**

TWO MODES, BECAUSE MOST FUNNELS HERE ARE ONE PAGE.

  SIBLINGS  A funnel with two or more pages can have one overwritten by
            another. Identity is then an assertion: the page has what only IT
            has AND lacks what only its SIBLING has. The second half is the
            half that matters -- the broken contact page carried the shared
            header and footer perfectly well, so presence alone passed it.

  DRIFT     A one-page advert has no sibling to be confused with, so identity
            is "the same page it was yesterday". The fingerprint below is
            stored on `--save` and compared on every later run: title, h1,
            section classes and the full link set. A rewrite, a lost section
            or a changed destination all show up as a diff.

⚠️ MARKERS MUST BE ELEMENT-PRECISE, NEVER BARE CLASS NAMES. Pages in one
funnel share ONE stylesheet, so every selector for page A appears in page B's
source as CSS. Grepping for `sof-tcard` finds it on the contact page and always
will. That false positive has fired four times on this project (`sof-tick`
inside `sof-tickets`, `$1997` inside a comment, `mask-image` already present,
and the three class names on the contact page), so anchor every marker to
markup: `class="..."`, `<svg class=`, `name="..."`.

⚠️ SOCIAL SITES BLOCK ROBOTS AND THAT IS NOT A BROKEN LINK. LinkedIn answers
999, some hosts answer 403 or 429 to anything that is not a browser. The first
run of this reported 30 "broken" links that were all perfectly fine, which is
worse than no check at all: a report that cries wolf gets ignored and the one
real finding in it gets missed. Those codes are reported as BLOCKED, and only
404/410 and connection failures count as broken.

    py pagescore/verify_pages.py                 check every configured funnel
    py pagescore/verify_pages.py sof             check one
    py pagescore/verify_pages.py sof --save      re-baseline after an intended change
"""
import io
import json
import os
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
BASELINE = os.path.join(HERE, ".cache", "page_fingerprints.json")
UA = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
      "Cache-Control": "no-cache"}

# A funnel is a list of pages. `must_have` / `must_not_have` are only needed
# where a funnel has siblings that could be written over each other.
SITES = {
    "sof": {
        "label": "Scaling or Failing",
        "pages": [
            {"url": "https://www.scalingorfailing.com/event/",
             "name": "landing (entry)",
             "must_have": ['class="sof-tcard"', 'sof-sec sof-marqbar',
                           '>OUR PARTNERS<', '<svg class="sof-marq-logo',
                           'class="sof-splate'],
             "must_not_have": ['class="sof-form"', 'name="website"']},
            {"url": "https://www.scalingorfailing.com/event/scaling-failing",
             "name": "landing (by slug)",
             "must_have": ['class="sof-tcard"', 'sof-sec sof-marqbar'],
             "must_not_have": ['class="sof-form"']},
            {"url": "https://www.scalingorfailing.com/event/contact",
             "name": "contact",
             "must_have": ['class="sof-form"', 'name="website"',
                           'class="sof-send"', 'webhook/sof-contact'],
             "must_not_have": ['class="sof-tcard"', '<svg class="sof-marq-logo']},
            {"url": "https://www.scalingorfailing.com/event/thank-you",
             "name": "thank-you (post-Whop-payment redirect)",
             "must_have": ['Cu in Bangkok!', 'mailto:hello@scalingorfailing.com'],
             "must_not_have": ['class="sof-tcard"', 'class="sof-form"']},
        ],
    },
    # One-page adverts: no siblings, so no identity markers -- drift only.
    "tub": {
        "label": "TechUnboxed adverts",
        "pages": [
            {"url": "https://www.techunboxed.co/article/jFrY0DhRi", "name": "hlth vs smartwatch"},
            {"url": "https://www.techunboxed.co/article/dMs4WkOYD", "name": "google winner"},
        ],
    },
}

# Codes that mean "a robot asked", not "this link is dead".
BLOCKED = {401, 403, 405, 429, 999}


def get(url):
    req = urllib.request.Request(
        url + ("&" if "?" in url else "?") + "cb=%d" % time.time(), headers=UA)
    r = urllib.request.urlopen(req, timeout=90)
    return r.getcode(), r.read().decode("utf-8", "replace")


def head(url):
    for method in ("HEAD", "GET"):
        try:
            req = urllib.request.Request(url, headers=UA, method=method)
            return urllib.request.urlopen(req, timeout=40).getcode()
        except urllib.error.HTTPError as e:
            if e.code in BLOCKED and method == "HEAD":
                continue
            return e.code
        except Exception:
            return 0
    return 0


def fingerprint(html):
    """What the page IS, in a form a diff can speak about."""
    title = re.search(r"<title[^>]*>(.*?)</title>", html, re.S)
    h1 = re.search(r"<h1[^>]*>(.*?)</h1>", html, re.S)
    strip = lambda s: re.sub(r"\s+", " ", re.sub(r"<[^>]+>", "", s or "")).strip()
    # section classes are the page's skeleton: losing one is losing a section
    secs = sorted(set(re.findall(r'class="sof sof-sec ([a-z0-9 \-]+)"', html)))
    return {
        "title": strip(title.group(1) if title else ""),
        "h1": strip(h1.group(1) if h1 else "")[:120],
        "sections": secs,
        "links": sorted(set(re.findall(r'<a [^>]*href="([^"]+)"', html))),
    }


def diff(old, new):
    out = []
    for k in ("title", "h1"):
        if old.get(k) != new.get(k):
            out.append("%s changed: %r -> %r" % (k, old.get(k), new.get(k)))
    for k in ("sections", "links"):
        a, b = set(old.get(k) or []), set(new.get(k) or [])
        for x in sorted(a - b):
            out.append("%s GONE: %s" % (k[:-1], x))
        for x in sorted(b - a):
            out.append("%s NEW : %s" % (k[:-1], x))
    return out


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    save = "--save" in sys.argv
    names = args or list(SITES)

    base = {}
    if os.path.exists(BASELINE):
        base = json.load(io.open(BASELINE, encoding="utf-8"))

    fails, warns = [], []
    for name in names:
        site = SITES[name]
        print("\n##### %s (%s)" % (site["label"], name))
        for pg in site["pages"]:
            url = pg["url"]
            print("\n=== %s  (%s)" % (url, pg["name"]))
            try:
                code, html = get(url)
            except Exception as e:
                fails.append("%s unreachable: %s" % (url, e))
                print("  UNREACHABLE: %s" % e)
                continue
            print("  HTTP %s, %d bytes" % (code, len(html)))
            if code != 200:
                fails.append("%s returned HTTP %s" % (url, code))
                continue

            # 1. identity, where there is a sibling to be confused with
            for m in pg.get("must_have", []):
                ok = m in html
                print("  has    %-32s %s" % (m[:32], "OK" if ok else "MISSING"))
                if not ok:
                    fails.append("%s is missing %r" % (url, m))
            for m in pg.get("must_not_have", []):
                ok = m not in html
                print("  lacks  %-32s %s" % (m[:32], "OK" if ok else "WRONG PAGE"))
                if not ok:
                    fails.append("%s contains %r, which belongs to its sibling" % (url, m))

            # 2. the buttons
            hrefs = sorted(set(re.findall(r'<a [^>]*href="([^"]+)"', html)))
            ids = set(re.findall(r'id="([^"]+)"', html))
            nA = nI = nE = nBlocked = 0
            for h in hrefs:
                if h.startswith("#"):
                    nA += 1
                    if h != "#" and h[1:] not in ids:
                        fails.append("%s: anchor %s has no matching id on this page" % (url, h))
                        print("    anchor %-26s NO TARGET" % h)
                elif h.split(":")[0].lower() in ("mailto", "tel", "sms", "javascript"):
                    # not fetchable, and not a button that can 404
                    continue
                elif h.startswith("/") or h.startswith(urllib.parse.urlsplit(url).scheme):
                    full = urllib.parse.urljoin(url, h)
                    c = head(full)
                    if c in BLOCKED:
                        nBlocked += 1
                    elif c == 0:
                        warns.append("%s: link %s could not be reached from here "
                                     "(DNS/VPN, not proven dead)" % (url, h))
                        print("    link   %-26s UNREACHABLE from here" % h[:26])
                    elif not (200 <= c < 400):
                        fails.append("%s: link %s -> HTTP %s" % (url, h, c))
                        print("    link   %-26s HTTP %s BROKEN" % (h[:26], c))
                    nI += 1
                else:
                    c = head(h)
                    if c in BLOCKED:
                        nBlocked += 1
                    elif c == 0:
                        warns.append("%s: external %s could not be reached from here "
                                     "(DNS/VPN, not proven dead)" % (url, h[:60]))
                        print("    ext    %-40s UNREACHABLE from here" % h[:40])
                    elif not (200 <= c < 400):
                        fails.append("%s: external %s -> HTTP %s" % (url, h[:60], c))
                        print("    ext    %-40s HTTP %s BROKEN" % (h[:40], c))
                    nE += 1
            print("  links: %d anchors, %d internal, %d external (%d blocked by bot "
                  "protection, not checked)" % (nA, nI, nE, nBlocked))

            # 3. drift against the last known-good shape
            fp = fingerprint(html)
            old = base.get(url)
            if old is None:
                print("  drift: no baseline yet%s" % ("" if save else " (run --save to set one)"))
            else:
                d = diff(old, fp)
                if not d:
                    print("  drift: none, identical shape to the baseline")
                else:
                    for line in d:
                        print("    DRIFT %s" % line)
                        warns.append("%s: %s" % (url, line))
            if save:
                base[url] = fp

    if save:
        os.makedirs(os.path.dirname(BASELINE), exist_ok=True)
        io.open(BASELINE, "w", encoding="utf-8").write(
            json.dumps(base, indent=1, ensure_ascii=False))
        print("\nbaseline saved: %s" % os.path.relpath(BASELINE, HERE))

    print("\n" + "=" * 64)
    if warns and not save:
        print("DRIFT since the baseline (%d). Intended? re-run with --save." % len(warns))
        for w in warns:
            print("  ~ %s" % w)
    if fails:
        print("FAILED (%d):" % len(fails))
        for f in fails:
            print("  - %s" % f)
        sys.exit(1)
    print("Every page is the right page, and every link resolves.")


main()
