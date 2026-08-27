#!/usr/bin/env python3
"""
qa_runner.py -- the fixed, mechanical half of the LANDING PAGE QA RUNBOOK.

This is to `program.md` what `benchmark.py` is to a PageSpeed score: a judge that
MEASURES and never builds. It executes every part of phases 0, 1, 2, 3, 4 and 6
that a machine can decide on its own, and writes the result as JSON so the same
criteria are applied on every run, by every session, in the same way.

What it deliberately does NOT do: phase 5 (congruency) and the "does the social
image actually depict the offer" half of phase 3. Those need judgment, so they
are left to the QA agent, which reads this file's `findings.json` and adds them.

Usage (always from the repo root):

  python3 pagescore/qa_runner.py <url> [<url> ...]
  python3 pagescore/qa_runner.py <url> --run-id 2026-08-21-fixpass
  python3 pagescore/qa_runner.py <url> --after-publish     # wait out PSI's cold cache
  python3 pagescore/qa_runner.py <url> --skip-psi          # fast structural-only pass
  python3 pagescore/qa_runner.py --urls pagescore/runs/scope.txt

Output, per run:

  pagescore/runs/<run_id>/
    findings.json        every page, machine-checkable verdicts, one file
    report.md            the phase-1..6 summary table, ready to paste
    <page-key>/shots/*.png

Exit code is 0 unless a page FAILs, so it can gate a pipeline step.
"""
import argparse
import json
import os
import re
import ssl
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime, timezone

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
RUNS = os.path.join(HERE, "runs")
sys.path.insert(0, ROOT)
sys.path.insert(0, HERE)

import benchmark  # noqa: E402  -- the fixed speed judge, reused, not reimplemented

UA = ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/125.0 Safari/537.36")

# program.md pass criteria, in one place so they are never re-litigated per run.
THRESHOLDS = {
    "perf_pass": 90, "perf_flag": 80,
    "lcp_s": 2.5, "cls": 0.1, "tbt_ms": 200,
    "page_weight_mb": 2.0,
    "desc_min": 140, "desc_max": 160,
    "og_max_bytes": 1_000_000,
    "og_ratio": 1.91, "og_ratio_tol": 0.20,
    "viewports": [1440, 768, 375, 320],
}

# Sites that bot-block. program.md: a 403 from these is NOT a failure -- it is a
# manual-verification item that must appear in the report's LIMITATIONS section.
BOT_BLOCKED = ("trustpilot.com", "amazon.com", "amazon.de", "amazon.co.uk",
               "instagram.com", "x.com", "twitter.com", "facebook.com")


def now():
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def page_key(url):
    p = urllib.parse.urlparse(url)
    return (p.path.strip("/").replace("/", "__") or p.netloc.replace(".", "_"))


# ---------------------------------------------------------------- phase 0
def phase0_scope(url):
    """Record the redirect chain. Every hop is real latency on paid traffic."""
    ctx = ssl.create_default_context()
    hops, seen, cur = [], set(), url
    for _ in range(10):
        if cur in seen:
            hops.append({"url": cur, "status": "LOOP"})
            break
        seen.add(cur)
        req = urllib.request.Request(cur, headers={"User-Agent": UA}, method="GET")
        try:
            class NoRedirect(urllib.request.HTTPRedirectHandler):
                def redirect_request(self, *a, **k):
                    return None
            op = urllib.request.build_opener(NoRedirect,
                                             urllib.request.HTTPSHandler(context=ctx))
            with op.open(req, timeout=30) as r:
                hops.append({"url": cur, "status": r.status})
                break
        except urllib.error.HTTPError as e:
            hops.append({"url": cur, "status": e.code})
            loc = e.headers.get("Location")
            if e.code in (301, 302, 303, 307, 308) and loc:
                cur = urllib.parse.urljoin(cur, loc)
                continue
            break
        except Exception as e:
            hops.append({"url": cur, "status": "ERR", "error": str(e)[:200]})
            break
    final = hops[-1]["url"] if hops else url
    extra = max(0, len(hops) - 1)
    return {
        "requested_url": url, "final_url": final, "hops": hops,
        "redirect_count": extra,
        "verdict": "PASS" if extra == 0 else "FLAG",
        "note": "no redirect" if extra == 0 else f"{extra} redirect hop(s) before the page renders",
    }


# ---------------------------------------------------------------- phase 1
def phase1_speed(url, method="psi", after_publish=False, skip=False, note=""):
    if skip:
        return {"skipped": True, "verdict": "SKIP", "note": "--skip-psi"}
    if after_publish:
        # Publishing purges the storefront cache; PSI's first read after a deploy
        # under-reports by ~20 points. Warm the URL, then let it settle.
        try:
            urllib.request.urlopen(
                urllib.request.Request(url, headers={"User-Agent": UA}), timeout=60).read()
        except Exception:
            pass
        time.sleep(30)
    out = {}
    for strategy in ("mobile", "desktop"):
        try:
            m = benchmark.evaluate(url, strategy, method)
            benchmark.record(url, strategy, method, m, note or "qa_runner", now())
            out[strategy] = m
        except Exception as e:
            out[strategy] = {"error": str(e)[:300]}
    mob = out.get("mobile", {})
    perf, cls = mob.get("performance"), mob.get("cls")
    lcp, tbt = mob.get("lcp_s"), mob.get("tbt_ms")
    fails, flags = [], []
    if perf is None:
        flags.append("mobile performance unavailable")
    elif perf < THRESHOLDS["perf_flag"]:
        fails.append(f"mobile performance {perf}")
    elif perf < THRESHOLDS["perf_pass"]:
        flags.append(f"mobile performance {perf}")
    if lcp is not None and lcp > THRESHOLDS["lcp_s"]:
        fails.append(f"LCP {lcp:.2f}s")
    if cls is not None and cls >= THRESHOLDS["cls"]:
        fails.append(f"CLS {cls:.3f}")
    if tbt is not None and tbt > THRESHOLDS["tbt_ms"]:
        flags.append(f"TBT {tbt:.0f}ms")
    out["verdict"] = "FAIL" if fails else ("FLAG" if flags else "PASS")
    out["note"] = "; ".join(fails + flags) or (
        f"mobile {perf}, LCP {lcp:.2f}s, CLS {cls:.3f}" if perf is not None else "")
    return out


# ---------------------------------------------------------------- phase 2
def check_link(href):
    if href.startswith("mailto:") or href.startswith("tel:"):
        return {"status": "n/a", "kind": "protocol"}
    req = urllib.request.Request(href, headers={"User-Agent": UA}, method="GET")
    try:
        with urllib.request.urlopen(req, timeout=25) as r:
            return {"status": r.status, "final": r.url}
    except urllib.error.HTTPError as e:
        return {"status": e.code, "final": href}
    except Exception as e:
        return {"status": "000", "error": str(e)[:120]}


def phase2_links(dom_links, raw_html, base_url=None):
    """dom_links: [{href, text, id}] harvested from the RENDERED page.

    program.md's rule set, applied verbatim: 2xx/redirect-to-2xx passes; 4xx/5xx
    fails; href="#" or javascript:void(0) on a real link fails; a 403 from a
    bot-protected host is a manual-check item, not a failure.
    """
    dead_anchor, results, manual = [], [], []
    ids_on_page = set(re.findall(r'id="([^"]+)"', raw_html or ""))
    seen = {}
    for l in dom_links:
        href = (l.get("href") or "").strip()
        label = (l.get("text") or "").strip()[:60]
        if not href or href == "#" or href.lower().startswith("javascript:"):
            dead_anchor.append({"label": label, "href": href})
            continue
        # Resolve relative hrefs against the page. Without this a normal "/path"
        # link raises "unknown url type" and takes the whole run down.
        if base_url and not href.startswith("#") and "://" not in href \
                and not href.startswith(("mailto:", "tel:", "javascript:")):
            href = urllib.parse.urljoin(base_url, href)
        if href.startswith("#"):
            # An in-page anchor is only real if the target exists (our legal
            # modals are #tu-terms style overlays that DO exist in the DOM).
            target = href[1:]
            if target and (target in ids_on_page or l.get("resolves")):
                results.append({"href": href, "label": label,
                                "status": "anchor-ok", "verdict": "PASS"})
            else:
                dead_anchor.append({"label": label, "href": href})
            continue
        seen.setdefault(href, []).append(label)

    for href, labels in seen.items():
        try:
            r = check_link(href)
        except Exception as e:
            r = {"status": "000", "error": str(e)[:120]}
        host = urllib.parse.urlparse(href).netloc.lower()
        blocked = any(b in host for b in BOT_BLOCKED)
        row = {"href": href, "labels": sorted(set(labels)), **r, "bot_blocked": blocked}
        st = r.get("status")
        if isinstance(st, int) and 200 <= st < 400:
            row["verdict"] = "PASS"
        elif blocked:
            row["verdict"] = "MANUAL"
            manual.append(href)
        elif st == "n/a":
            row["verdict"] = "PASS"
        else:
            row["verdict"] = "FAIL"
        results.append(row)

    hard_fails = [r for r in results if r.get("verdict") == "FAIL"]
    # program.md: a 403 from a bot-protected host is NOT a failure. It is a
    # limitation to disclose, so it must never hold the pipeline at FLAG forever.
    verdict = "FAIL" if (dead_anchor or hard_fails) else "PASS"
    parts = []
    if dead_anchor:
        parts.append(f'{len(dead_anchor)} dead link(s) (href="#" / javascript:)')
    if hard_fails:
        parts.append(f"{len(hard_fails)} broken URL(s)")
    ok = len([r for r in results if r.get("verdict") == "PASS"])
    tail = f" ({len(manual)} bot-blocked, verify in a browser)" if manual else ""
    return {"checked": len(results), "passing": ok, "dead_anchors": dead_anchor,
            "broken": hard_fails, "manual_check": manual, "all": results,
            "verdict": verdict,
            "note": ("; ".join(parts) or f"{ok}/{len(results)} pass") + tail}


# ---------------------------------------------------------------- phase 3
def phase3_meta(meta, raw_html):
    """meta: the rendered-DOM head inventory + h1 list, from the browser."""
    issues, flags = [], []
    title = (meta.get("title") or "").strip()
    desc = (meta.get("description") or "").strip()
    og = meta.get("og", {})
    tw = meta.get("twitter", {})
    h1s = meta.get("h1", [])

    if not title:
        issues.append("no <title>")
    if not desc:
        issues.append("no meta description")
    elif desc.lower() == title.lower():
        issues.append("meta description repeats the title")
    elif not (THRESHOLDS["desc_min"] <= len(desc) <= THRESHOLDS["desc_max"]):
        flags.append(f"meta description {len(desc)} chars (target {THRESHOLDS['desc_min']}-{THRESHOLDS['desc_max']})")

    if len(h1s) == 0:
        issues.append("no h1 (a styled div does not count)")
    elif len(h1s) > 1:
        issues.append(f"{len(h1s)} h1 tags")

    og_img = og.get("image")
    og_info = {}
    if not og_img:
        issues.append("no og:image")
    else:
        og_info = probe_image(og_img)
        if og_info.get("status") != 200:
            issues.append(f"og:image returns {og_info.get('status')}")
        else:
            if og_info.get("bytes", 0) > THRESHOLDS["og_max_bytes"]:
                issues.append(f"og:image {og_info['bytes']/1024:.0f} KB (limit 1 MB)")
            w, h = og_info.get("width"), og_info.get("height")
            if w and h:
                ratio = w / h
                if abs(ratio - THRESHOLDS["og_ratio"]) > THRESHOLDS["og_ratio_tol"]:
                    issues.append(f"og:image {w}x{h} (ratio {ratio:.2f}, want ~1.91)")
    if not og.get("title"):
        flags.append("no og:title")
    if not tw.get("card"):
        flags.append("no twitter:card (settings.seo emits og:* only)")

    # The one-headline rule: title / og:title / on-page h1 must carry one message.
    STOP = {"the", "a", "an", "that", "is", "in", "of", "and", "to", "for", "s"}

    def toks(s):
        return {w for w in re.sub(r"[^a-z0-9 ]+", " ", (s or "").lower()).split()
                if w and w not in STOP}
    if h1s and title:
        a, b = toks(h1s[0]), toks(title)
        if a and b and len(a & b) / min(len(a), len(b)) < 0.7:
            flags.append("title tag and on-page h1 carry different messages")

    return {"title": title, "title_len": len(title), "description": desc,
            "description_len": len(desc), "og": og, "twitter": tw,
            "h1": h1s, "h1_count": len(h1s), "og_image": og_info,
            "issues": issues, "flags": flags,
            "verdict": "FAIL" if issues else ("FLAG" if flags else "PASS"),
            "note": "; ".join(issues + flags) or "title, description, og:image and one h1 all present"}


def probe_image(url):
    try:
        req = urllib.request.Request(url, headers={"User-Agent": UA})
        with urllib.request.urlopen(req, timeout=30) as r:
            data = r.read()
            out = {"status": r.status, "bytes": len(data), "url": url}
    except urllib.error.HTTPError as e:
        return {"status": e.code, "url": url}
    except Exception as e:
        return {"status": "000", "url": url, "error": str(e)[:120]}
    try:
        from PIL import Image
        import io
        im = Image.open(io.BytesIO(data))
        out["width"], out["height"] = im.size
    except Exception:
        pass
    return out


# ---------------------------------------------------------------- report
def verdict_of(page):
    order = {"FAIL": 3, "FLAG": 2, "PASS": 1, "SKIP": 0, "MANUAL": 2}
    worst = max((order.get(v.get("verdict", "SKIP"), 0)
                 for v in page["phases"].values()), default=1)
    return {3: "FAIL", 2: "FLAG", 1: "PASS", 0: "PASS"}[worst]


PHASE_LABEL = {
    "phase0": "Scope / redirects", "phase1": "Speed (mobile+desktop)",
    "phase2": "Links", "phase3": "Headline, meta and social",
    "phase4": "Responsiveness", "phase6": "Console and errors",
    "a11y": "Accessibility / agentic",
}


def render_report(run):
    L = [f"# Landing page QA -- {run['run_id']}", "",
         f"Runbook: `pagescore/program.md`. Mechanical phases by `pagescore/qa_runner.py`, {run['started']}.",
         f"Phase 5 (congruency) and social-image on-message are judgment calls and are not in this file.", ""]
    for p in run["pages"]:
        L += [f"## {p['final_url']}", "", f"**Verdict: {p['verdict']}**", "",
              "| Check | Result | Notes |", "|---|---|---|"]
        for k in ("phase0", "phase1", "phase2", "phase3", "phase4", "phase6", "a11y"):
            ph = p["phases"].get(k)
            if not ph:
                continue
            L.append(f"| {PHASE_LABEL[k]} | {ph.get('verdict','?')} | {ph.get('note','')} |")
        L.append("")
        d = p["phases"].get("phase2", {})
        if d.get("dead_anchors"):
            L += ["**Dead links**", "", "| Label | href |", "|---|---|"]
            L += [f"| {x['label']} | `{x['href']}` |" for x in d["dead_anchors"][:40]] + [""]
        if d.get("broken"):
            L += ["**Broken URLs**", "", "| Status | href | Seen as |", "|---|---|---|"]
            L += [f"| {x['status']} | `{x['href']}` | {', '.join(x['labels'])[:60]} |"
                  for x in d["broken"][:40]] + [""]
        if d.get("manual_check"):
            L += ["**Verify manually (bot-protected, not a failure)**", ""]
            L += [f"- {u}" for u in d["manual_check"]] + [""]
        v = p["phases"].get("phase4", {})
        for row in v.get("viewports", []):
            if row.get("overflow"):
                L.append(f"- Overflow at {row['width']}px: pans {row.get('scroll_x',0)}px; "
                         f"widest element `{row.get('culprit','?')}`")
        L.append("")
    return "\n".join(L)


# ---------------------------------------------------------------- browser pass
# Phases 2 (rendered DOM), 3 (rendered head), 4 (viewports) and 6 (console) all
# need one real browser. Do them in a single page load per viewport.

HARVEST_JS = r"""
() => {
  const links = [...document.querySelectorAll('a[href]')].map(a => ({
    href: a.getAttribute('href'),
    text: (a.innerText || a.getAttribute('aria-label') || '').trim(),
    resolves: a.getAttribute('href').startsWith('#')
      ? !!document.getElementById(a.getAttribute('href').slice(1)) : null
  }));
  const m = n => (document.querySelector(`meta[name="${n}"]`) || {}).content || '';
  const p = n => (document.querySelector(`meta[property="${n}"]`) || {}).content || '';
  const og = {}, tw = {};
  document.querySelectorAll('meta[property^="og:"]').forEach(
    e => og[e.getAttribute('property').slice(3)] = e.content);
  document.querySelectorAll('meta[name^="twitter:"]').forEach(
    e => tw[e.getAttribute('name').slice(8)] = e.content);
  // Accessibility / Agentic Browsing: every visible interactive element needs a name.
  const named = e => (e.innerText || '').trim() || e.getAttribute('aria-label')
    || e.getAttribute('title') || [...e.querySelectorAll('img[alt]')].some(i => i.alt.trim());
  const unnamed = [...document.querySelectorAll('a,button,[role=button]')]
    .filter(e => e.offsetParent !== null && !named(e))
    .map(e => e.outerHTML.slice(0, 120));
  const imgs = [...document.querySelectorAll('img')];
  // Rendered but blank: in the layout, finished loading, zero intrinsic size.
  const broken = imgs.filter(i => i.offsetParent !== null && i.complete && i.naturalWidth === 0)
    .map(i => ({ src: (i.currentSrc || i.src || i.getAttribute('src') || '').split('?')[0],
                 alt: i.getAttribute('alt') || '' }));
  // Identify each unlabelled image well enough to fix it in the builder:
  // LF's p.title lands on the title attribute and is the stable handle.
  const noalt = imgs.filter(i => i.offsetParent !== null
      && !(i.getAttribute('alt') || '').trim()
      && i.naturalWidth > 40 && i.naturalHeight > 40)
    .map(i => {
      const h = i.closest('section,div');
      const near = h ? (h.innerText || '').trim().split('\n')[0].slice(0, 50) : '';
      return {
        file: (i.currentSrc || i.src).split('/').pop().split('?')[0].slice(0, 60),
        title: i.getAttribute('title') || '',
        size: i.naturalWidth + 'x' + i.naturalHeight,
        in_link: !!i.closest('a'),
        near: near
      };
    });
  const vp = (document.querySelector('meta[name=viewport]') || {}).content || '';
  const res = performance.getEntriesByType('resource')
    .reduce((s, r) => s + (r.transferSize || 0), 0);
  const nav = (performance.getEntriesByType('navigation')[0] || {}).transferSize || 0;
  return {
    links, title: document.title, description: m('description'),
    canonical: (document.querySelector('link[rel=canonical]') || {}).href || '',
    og, twitter: tw,
    h1: [...document.querySelectorAll('h1')].map(h => h.innerText.trim()),
    h2count: document.querySelectorAll('h2').length,
    lang: document.documentElement.lang || '',
    viewport_meta: vp,
    zoom_blocked: /maximum-scale\s*=\s*1|user-scalable\s*=\s*(no|0)/.test(vp),
    unnamed_interactive: unnamed, images_total: imgs.length, images_no_alt: noalt,
    images_broken: broken,
    weight_bytes: res + nav,
    text: document.body.innerText
  };
}
"""

OVERFLOW_JS = r"""
() => {
  const doc = document.documentElement;
  const overflow = doc.scrollWidth > window.innerWidth;
  window.scrollTo(50, 0);
  const sx = window.scrollX;
  window.scrollTo(0, 0);
  let culprit = null, worst = 0;
  if (overflow) {
    for (const el of document.querySelectorAll('*')) {
      const r = el.getBoundingClientRect();
      const over = r.right - window.innerWidth;
      if (over > worst && r.width > 0) {
        worst = over;
        culprit = (el.tagName.toLowerCase()
          + (el.id ? '#' + el.id : '')
          + (el.className && typeof el.className === 'string'
             ? '.' + el.className.trim().split(/\s+/).slice(0, 2).join('.') : ''))
          + ' :: ' + (el.innerText || '').trim().slice(0, 60);
      }
    }
  }
  return {overflow, scroll_x: sx, doc_width: doc.scrollWidth,
          win_width: window.innerWidth, culprit, overhang: Math.round(worst)};
}
"""


def browser_pass(url, out_dir, viewports=None, shots=True):
    from playwright.sync_api import sync_playwright
    viewports = viewports or THRESHOLDS["viewports"]
    shot_dir = os.path.join(out_dir, "shots")
    os.makedirs(shot_dir, exist_ok=True)
    console, failed, harvest = [], [], None
    vp_rows = []

    with sync_playwright() as pw:
        browser = pw.chromium.launch()
        for i, w in enumerate(viewports):
            mobile = w <= 767
            ctx = browser.new_context(
                viewport={"width": w, "height": 900},
                device_scale_factor=2 if mobile else 1,
                is_mobile=mobile, has_touch=mobile, user_agent=UA)
            page = ctx.new_page()
            page.on("console", lambda m: console.append(
                {"type": m.type, "text": m.text[:300]}) if m.type == "error" else None)
            page.on("pageerror", lambda e: console.append(
                {"type": "pageerror", "text": str(e)[:300]}))
            page.on("requestfailed", lambda r: failed.append(
                {"url": r.url[:200], "reason": (r.failure or "")[:120]}))
            page.on("response", lambda r: failed.append(
                {"url": r.url[:200], "status": r.status}) if r.status >= 400 else None)
            try:
                page.goto(url, wait_until="networkidle", timeout=90_000)
            except Exception:
                page.goto(url, wait_until="domcontentloaded", timeout=90_000)
            page.wait_for_timeout(2500)
            # Scroll end to end -- lazy content and its errors only appear then.
            # Dwell at each step: a fast scroll outruns lazy loading, so the shot comes
            # back with blank images and the report claims a defect the page does not
            # have. 250ms per step is enough for the request to finish.
            page.evaluate("() => new Promise(r => {let y=0;const t=setInterval(()=>{"
                          "window.scrollTo(0,y);y+=700;"
                          "if(y>document.body.scrollHeight){clearInterval(t);"
                          "window.scrollTo(0,0);r();}},250);})")
            page.wait_for_timeout(3000)
            row = page.evaluate(OVERFLOW_JS)
            row["width"] = w
            if shots:
                sp = os.path.join(shot_dir, f"{w}.png")
                try:
                    page.screenshot(path=sp, full_page=(w in (1440, 375)))
                    row["screenshot"] = os.path.relpath(sp, ROOT)
                except Exception:
                    pass
            vp_rows.append(row)
            if i == 0:
                harvest = page.evaluate(HARVEST_JS)
            ctx.close()
        browser.close()

    over = [r for r in vp_rows if r["overflow"] and r["scroll_x"] > 0]
    p4 = {"viewports": vp_rows,
          "verdict": "FAIL" if over else "PASS",
          "note": ("no horizontal scroll at 1440/768/375/320" if not over else
                   "; ".join(f"{r['width']}px pans {r['scroll_x']}px "
                             f"({r.get('overhang')}px overhang)" for r in over))}

    seen, uniq = set(), []
    for c in console:
        k = (c["type"], c["text"][:120])
        if k not in seen:
            seen.add(k)
            uniq.append(c)
    fseen, funiq, beacons = set(), [], 0
    for f in failed:
        # Dedupe by host+path: cache-busting query params make every load "new".
        k = f["url"].split("?")[0]
        if k in fseen:
            continue
        fseen.add(k)
        if is_beacon(f):
            beacons += 1
            continue
        funiq.append(f)
    weight_mb = (harvest or {}).get("weight_bytes", 0) / 1e6
    p6 = {"console_errors": uniq, "failed_requests": funiq,
          "beacons_aborted": beacons, "page_weight_mb": round(weight_mb, 2),
          "verdict": "FAIL" if uniq else ("FLAG" if funiq else "PASS"),
          "note": (f"{len(uniq)} console error(s)" if uniq else "no console errors")
                  + (f"; {len(funiq)} failed request(s)" if funiq else "")
                  + (f"; page weight {weight_mb:.2f} MB" if weight_mb else "")}
    if weight_mb > THRESHOLDS["page_weight_mb"] and p6["verdict"] == "PASS":
        p6["verdict"] = "FLAG"
        p6["note"] += f" (over the {THRESHOLDS['page_weight_mb']} MB budget)"
    return harvest, p4, p6


# Beacons that abort when the page is torn down. Not defects -- filtering them is
# what keeps "failed requests" a signal instead of 19 lines of noise every run.
BEACON_HOSTS = ("analytics.google.com", "google-analytics.com", "doubleclick.net",
                "google.com/ccm", "googletagmanager.com", "facebook.com/tr",
                "aimerce.ai", "/lfevents", "/api/collect", "connect.facebook.net", "tiktok.com",
                "bing.com", "clarity.ms", "snap.com", "pinterest.com")


def is_beacon(rec):
    u = rec.get("url", "")
    return (rec.get("reason", "").startswith("net::ERR_ABORTED")
            and any(h in u for h in BEACON_HOSTS))


def a11y_block(h):
    issues, flags = [], []
    if h.get("images_broken"):
        issues.append(f"{len(h['images_broken'])} image(s) render blank "
                      f"(loaded, zero intrinsic size)")
    if h.get("unnamed_interactive"):
        issues.append(f"{len(h['unnamed_interactive'])} interactive element(s) with no accessible name")
    if h.get("images_no_alt"):
        flags.append(f"{len(h['images_no_alt'])} content image(s) with no alt text")
    if h.get("zoom_blocked"):
        flags.append("viewport meta blocks pinch-zoom (maximum-scale=1 / user-scalable=no)")
    if not h.get("lang"):
        flags.append("<html> has no lang attribute")
    return {"lang": h.get("lang"), "viewport_meta": h.get("viewport_meta"),
            "unnamed_interactive": h.get("unnamed_interactive", []),
            "images_no_alt": h.get("images_no_alt", []),
            "images_broken": h.get("images_broken", []),
            "images_total": h.get("images_total"),
            "verdict": "FAIL" if issues else ("FLAG" if flags else "PASS"),
            "note": "; ".join(issues + flags) or "named controls, alt text present, zoom allowed"}


def raw_html(url):
    try:
        req = urllib.request.Request(url, headers={"User-Agent": UA})
        with urllib.request.urlopen(req, timeout=45) as r:
            return r.read().decode("utf-8", "replace")
    except Exception:
        return ""


def qa_page(url, run_dir, args):
    key = page_key(url)
    out_dir = os.path.join(run_dir, key)
    os.makedirs(out_dir, exist_ok=True)
    print(f"\n=== {url}")

    p0 = phase0_scope(url)
    final = p0["final_url"]
    print(f"  phase 0  {p0['verdict']}  {p0['note']}")

    harvest, p4, p6 = browser_pass(final, out_dir, shots=not args.no_shots)
    print(f"  phase 4  {p4['verdict']}  {p4['note']}")
    print(f"  phase 6  {p6['verdict']}  {p6['note']}")

    html = raw_html(final)
    p2 = phase2_links(harvest.get("links", []), html, base_url=final)
    print(f"  phase 2  {p2['verdict']}  {p2['note']}")

    p3 = phase3_meta(harvest, html)
    print(f"  phase 3  {p3['verdict']}  {p3['note']}")

    pa = a11y_block(harvest)
    print(f"  a11y     {pa['verdict']}  {pa['note']}")

    p1 = phase1_speed(final, method=args.method, after_publish=args.after_publish,
                      skip=args.skip_psi, note=args.note)
    print(f"  phase 1  {p1['verdict']}  {p1.get('note','')}")

    page = {"requested_url": url, "final_url": final, "key": key,
            "phases": {"phase0": p0, "phase1": p1, "phase2": p2, "phase3": p3,
                       "phase4": p4, "phase6": p6, "a11y": pa},
            "body_text": harvest.get("text", "")[:200_000]}
    page["verdict"] = verdict_of(page)
    # The page's own copy, saved so the congruency pass (phase 5) reads text, not pixels.
    with open(os.path.join(out_dir, "page_text.txt"), "w") as f:
        f.write(harvest.get("text", ""))
    print(f"  VERDICT  {page['verdict']}")
    return page


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("urls", nargs="*")
    ap.add_argument("--urls", dest="url_file", help="file with one URL per line")
    ap.add_argument("--run-id", default=None)
    ap.add_argument("--method", default="psi", choices=["psi", "lighthouse"])
    ap.add_argument("--skip-psi", action="store_true", help="structural phases only (fast)")
    ap.add_argument("--after-publish", action="store_true",
                    help="warm the URL and wait 30s -- PSI under-reports on a cold cache")
    ap.add_argument("--no-shots", action="store_true")
    ap.add_argument("--note", default="")
    args = ap.parse_args()

    urls = list(args.urls)
    if args.url_file:
        urls += [l.strip() for l in open(args.url_file)
                 if l.strip() and not l.startswith("#")]
    if not urls:
        ap.error("give at least one URL, or --urls <file>")

    run_id = args.run_id or datetime.now().strftime("%Y-%m-%d-%H%M")
    run_dir = os.path.join(RUNS, run_id)
    os.makedirs(run_dir, exist_ok=True)
    run = {"run_id": run_id, "started": now(), "runbook": "pagescore/program.md",
           "thresholds": THRESHOLDS, "pages": []}
    for u in urls:
        try:
            run["pages"].append(qa_page(u, run_dir, args))
        except Exception as e:
            import traceback
            traceback.print_exc()
            run["pages"].append({"requested_url": u, "final_url": u, "key": page_key(u),
                                 "verdict": "FAIL", "phases": {},
                                 "error": str(e)[:400]})
    run["finished"] = now()
    run["summary"] = {v: len([p for p in run["pages"] if p["verdict"] == v])
                      for v in ("PASS", "FLAG", "FAIL")}

    fj = os.path.join(run_dir, "findings.json")
    with open(fj, "w") as f:
        json.dump(run, f, indent=2)
    rm = os.path.join(run_dir, "report.md")
    with open(rm, "w") as f:
        f.write(render_report(run))
    print(f"\n{run['summary']}")
    print(f"findings -> {os.path.relpath(fj, ROOT)}")
    print(f"report   -> {os.path.relpath(rm, ROOT)}")
    sys.exit(1 if run["summary"]["FAIL"] else 0)


if __name__ == "__main__":
    main()
