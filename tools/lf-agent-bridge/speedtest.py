#!/usr/bin/env python3
"""
speedtest.py — Automate Lighthouse runs against funnel pages and track the
numbers over time, so a speed regression shows up as a diff instead of a
surprise.

TWO BACKENDS, and the difference matters:

  --backend local  (default)  Lighthouse CLI driving the Chromium that Playwright
                              already installed. No API key, no quota.

  --backend psi                Google PageSpeed Insights API — the same engine,
                              run on Google's infrastructure. Keyless access is
                              rate-limited and returns HTTP 429 in practice;
                              pass --psi-key (free from the Google Cloud
                              console) for reliable use.

**Local scores are trustworthy only on an OTHERWISE IDLE MACHINE.** Lighthouse
throttles CPU relative to the host, so competing work wrecks the result. Measured
on one page, same URL, minutes apart:

  machine busy (npm installing)   desktop 70, mobile 49    TBT 670ms / 8180ms
  machine idle                    desktop 95, mobile 78    TBT 0ms / 310ms

Idle-machine desktop (94-95) lined up with the PageSpeed dashboard's 93, so the
absolute number IS usable — but only under that condition. Do not run a speed
test while a build, install or another agent task is going.

Variance control: `--runs N` takes the MEDIAN of N runs (Lighthouse's own
recommendation). Default 3 for local, 1 for psi (server-side is already stable).
Mobile is the noisier of the two — an idle-machine median of 3 still spread
67/78/80 — so treat small mobile movements as noise and prefer 5 runs when a
mobile delta matters.

  python3 speedtest.py URL [URL ...] [--form-factor mobile|desktop|both]
  python3 speedtest.py --from-workspace            # every funnel.json live_url
  python3 speedtest.py URL --backend psi --psi-key KEY
  python3 speedtest.py URL --compare              # diff against last saved run

History lands in funnels/_registry/speed/<host><path>.json as an append-only
list, so `--compare` can show what moved.
"""
import argparse
import json
import os
import re
import shutil
import statistics
import subprocess
import sys
import tempfile
import urllib.parse
import urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
HISTORY_DIR = os.path.join(ROOT, "funnels", "_registry", "speed")
FUNNELS_DIR = os.path.join(ROOT, "funnels")

METRICS = ["first-contentful-paint", "largest-contentful-paint",
           "total-blocking-time", "cumulative-layout-shift", "speed-index"]

# Playwright ships a Chromium we can reuse instead of requiring a system Chrome.
PW_CHROME = os.path.expanduser(
    "~/AppData/Local/ms-playwright/chromium-1234/chrome-win64/chrome.exe")


def _chrome_path():
    if os.environ.get("CHROME_PATH"):
        return os.environ["CHROME_PATH"]
    if os.path.exists(PW_CHROME):
        return PW_CHROME
    return None


def psi_key(explicit=None):
    """Resolve the PageSpeed API key: --psi-key, then $PAGESPEED_KEY, then
    PAGESPEED_KEY in the bridge's .env (which is gitignored).

    The key is a secret — never print it, never write it into history files.
    Without one, PSI answers 429 in practice: the keyless quota is shared and
    permanently exhausted.
    """
    if explicit:
        return explicit
    if os.environ.get("PAGESPEED_KEY"):
        return os.environ["PAGESPEED_KEY"]
    env = os.path.join(HERE, ".env")
    if os.path.exists(env):
        with open(env, encoding="utf-8") as fh:
            for line in fh:
                line = line.strip()
                if line.startswith("PAGESPEED_KEY="):
                    return line.split("=", 1)[1].strip().strip("'\"") or None
    return None


def _extract(lhr):
    """Pull the score, core metrics and opportunities out of a Lighthouse result."""
    audits = lhr.get("audits", {})
    out = {
        "score": round((lhr["categories"]["performance"].get("score") or 0) * 100),
        "metrics": {},
        "opportunities": [],
        "lighthouse": lhr.get("lighthouseVersion"),
        "benchmark_index": (lhr.get("environment") or {}).get("benchmarkIndex"),
    }
    for k in METRICS:
        a = audits.get(k) or {}
        out["metrics"][k] = {"value": a.get("numericValue"),
                             "display": a.get("displayValue")}
    for k, v in audits.items():
        det = v.get("details") or {}
        if det.get("type") == "opportunity" and (v.get("numericValue") or 0) > 0:
            out["opportunities"].append({
                "id": k, "title": v.get("title"),
                "display": v.get("displayValue"),
                "savings_ms": v.get("numericValue"),
                "savings_bytes": det.get("overallSavingsBytes"),
            })
    out["opportunities"].sort(key=lambda o: -(o.get("savings_ms") or 0))

    # Diagnostics that actually explained things in practice. A score alone never
    # says *why*; every real cause found on these funnels came from one of these:
    #   styleLayout blew up          -> a <style> tag inside <body>
    #   which element shifted        -> font swap, not the image PSI blames
    #   font bytes/count             -> critical-path contention
    diag = {}
    mt = ((audits.get("mainthread-work-breakdown") or {}).get("details") or {})
    if mt.get("items"):
        diag["mainthread_ms"] = {i.get("group"): round(i.get("duration") or 0)
                                 for i in mt["items"]}
    ls = ((audits.get("layout-shifts") or {}).get("details") or {})
    if ls.get("items"):
        diag["shift_elements"] = [
            {"selector": ((i.get("node") or {}).get("selector") or "")[:80],
             "score": round(i.get("score") or 0, 4)} for i in ls["items"]]
    nr = ((audits.get("network-requests") or {}).get("details") or {})
    if nr.get("items"):
        reqs = nr["items"]
        fonts = [r for r in reqs if "woff" in (r.get("url") or "")]
        imgs = [r for r in reqs if r.get("resourceType") == "Image"]
        diag["requests"] = len(reqs)
        diag["font_files"] = len(fonts)
        diag["font_kib"] = round(sum(r.get("transferSize") or 0 for r in fonts) / 1024)
        diag["image_kib"] = round(sum(r.get("transferSize") or 0 for r in imgs) / 1024)
        # Everything racing the first paint. LF Image blocks have no loading=lazy,
        # so this is usually the whole page.
        diag["image_kib_before_400ms"] = round(sum(
            r.get("transferSize") or 0 for r in imgs
            if (r.get("networkRequestTime") or 0) < 400) / 1024)
    tb = audits.get("total-byte-weight") or {}
    if tb.get("numericValue"):
        diag["total_kib"] = round(tb["numericValue"] / 1024)
    if diag:
        out["diagnostics"] = diag
    return out


def run_local(url, form_factor, runs):
    lh = shutil.which("lighthouse") or shutil.which("lighthouse.cmd")
    if not lh:
        sys.exit("lighthouse not found. Install: npm install -g lighthouse")
    chrome = _chrome_path()
    env = dict(os.environ)
    if chrome:
        env["CHROME_PATH"] = chrome

    results = []
    for i in range(runs):
        tmp = os.path.join(tempfile.gettempdir(), f"lh-{os.getpid()}-{i}.json")
        cmd = [lh, url, "--only-categories=performance", "--quiet",
               "--output=json", f"--output-path={tmp}",
               "--chrome-flags=--headless=new --no-sandbox --disable-gpu"]
        if form_factor == "desktop":
            cmd.append("--preset=desktop")
        else:
            cmd += ["--form-factor=mobile", "--screenEmulation.mobile"]
        subprocess.run(cmd, env=env, capture_output=True, timeout=600)
        if not os.path.exists(tmp):
            print(f"  ! run {i+1} produced no output (skipped)", file=sys.stderr)
            continue
        with open(tmp, encoding="utf-8") as fh:
            results.append(_extract(json.load(fh)))
        os.unlink(tmp)

    if not results:
        raise RuntimeError(f"all {runs} lighthouse runs failed for {url}")
    # Median run = the one whose score is the median, so metrics stay internally
    # consistent (averaging metrics across runs would invent a run that never
    # happened).
    results.sort(key=lambda r: r["score"])
    med = results[len(results) // 2]
    med["runs"] = len(results)
    med["scores_all"] = sorted(r["score"] for r in results)
    return med


def run_psi(url, form_factor, key=None):
    key = psi_key(key)
    params = {"url": url, "strategy": form_factor, "category": "performance"}
    if key:
        params["key"] = key
    api = ("https://www.googleapis.com/pagespeedonline/v5/runPagespeed?"
           + urllib.parse.urlencode(params))
    req = urllib.request.Request(api, headers={"User-Agent": "Mozilla/5.0"})
    try:
        with urllib.request.urlopen(req, timeout=240) as r:
            data = json.load(r)
    except urllib.error.HTTPError as e:
        if e.code == 429:
            raise RuntimeError(
                "PSI rate-limited (429). Keyless quota is shared and usually "
                "exhausted — pass --psi-key, or use --backend local.") from e
        raise RuntimeError(f"PSI HTTP {e.code}: {e.read()[:200]!r}") from e
    out = _extract(data["lighthouseResult"])
    out["runs"] = 1
    return out


def _history_path(url):
    p = urllib.parse.urlsplit(url)
    name = re.sub(r"[^A-Za-z0-9._-]", "_", (p.netloc + p.path).strip("/")) or "root"
    return os.path.join(HISTORY_DIR, name + ".json")


def _load_history(url):
    path = _history_path(url)
    if os.path.exists(path):
        with open(path, encoding="utf-8") as fh:
            return json.load(fh)
    return []


def _save_history(url, entry):
    os.makedirs(HISTORY_DIR, exist_ok=True)
    hist = _load_history(url)
    hist.append(entry)
    with open(_history_path(url), "w", encoding="utf-8") as fh:
        json.dump(hist, fh, indent=2)


def workspace_urls():
    """Every live_url recorded in a funnels/**/funnel.json."""
    found = []
    for dirpath, _dirs, files in os.walk(FUNNELS_DIR):
        if "funnel.json" not in files:
            continue
        with open(os.path.join(dirpath, "funnel.json"), encoding="utf-8") as fh:
            try:
                data = json.load(fh)
            except ValueError:
                continue
        for u in ([data.get("live_url")] if isinstance(data.get("live_url"), str)
                  else (data.get("live_url") or [])):
            if u:
                found.append((data.get("slug") or os.path.basename(dirpath), u))
    return found


def _fmt_delta(now, prev, lower_is_better=True, unit=""):
    if prev is None or now is None:
        return ""
    d = now - prev
    if abs(d) < 1e-9:
        return "  (no change)"
    better = (d < 0) if lower_is_better else (d > 0)
    return f"  ({'+' if d > 0 else ''}{d:.0f}{unit} {'better' if better else 'WORSE'})"


def report(label, url, res, prev=None):
    print(f"\n{label}  {url}")
    prev_score = prev.get("score") if prev else None
    line = f"  score {res['score']}"
    if res.get("scores_all") and len(res["scores_all"]) > 1:
        line += f"   (median of {res['runs']}: {res['scores_all']})"
    if prev_score is not None:
        line += _fmt_delta(res["score"], prev_score, lower_is_better=False)
    print(line)
    for k in METRICS:
        m = res["metrics"].get(k) or {}
        p = ((prev or {}).get("metrics", {}).get(k) or {}).get("value")
        unit = "" if k == "cumulative-layout-shift" else "ms"
        d = _fmt_delta(m.get("value"), p, lower_is_better=True, unit=unit)
        print(f"    {k:26} {str(m.get('display')):>10}{d}")
    d = res.get("diagnostics") or {}
    if d:
        bits = []
        if d.get("total_kib") is not None:
            bits.append(f"{d['total_kib']} KiB total")
        if d.get("font_files") is not None:
            bits.append(f"{d['font_files']} fonts/{d.get('font_kib', 0)} KiB")
        if d.get("image_kib_before_400ms") is not None:
            bits.append(f"{d['image_kib_before_400ms']} KiB imgs <400ms")
        if bits:
            print("    payload: " + "  ".join(bits))
        if d.get("mainthread_ms"):
            top = sorted(d["mainthread_ms"].items(), key=lambda x: -x[1])[:3]
            print("    main-thread: " + "  ".join(f"{k} {v}ms" for k, v in top))
        for s in (d.get("shift_elements") or [])[:3]:
            print(f"    shift {s['score']:.4f}  {s['selector']}")
    if res["opportunities"]:
        print("    opportunities:")
        for o in res["opportunities"][:5]:
            kb = (f", {o['savings_bytes']/1024:.0f} KiB"
                  if o.get("savings_bytes") else "")
            print(f"      - {str(o['title'])[:48]:50} {o.get('display')}{kb}")


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("urls", nargs="*")
    ap.add_argument("--from-workspace", action="store_true",
                    help="test every live_url in funnels/**/funnel.json")
    ap.add_argument("--backend", default=None, choices=["local", "psi"],
                    help="default: psi when a key is resolvable (ground truth), "
                         "else local")
    ap.add_argument("--psi-key",
                    help="overrides $PAGESPEED_KEY and PAGESPEED_KEY in "
                         "tools/lf-agent-bridge/.env")
    ap.add_argument("--form-factor", default="mobile",
                    choices=["mobile", "desktop", "both"])
    ap.add_argument("--runs", type=int, default=None,
                    help="local only: median of N runs (default 3)")
    ap.add_argument("--compare", action="store_true",
                    help="diff against the last saved run and don't save")
    ap.add_argument("--no-save", action="store_true")
    args = ap.parse_args()

    targets = [(None, u) for u in args.urls]
    if args.from_workspace:
        targets += workspace_urls()
    if not targets:
        sys.exit("Pass at least one URL, or --from-workspace "
                 "(needs live_url in a funnel.json).")

    # Prefer PSI when a key is available: it runs on Google's hardware, so the
    # number is comparable to what anyone else sees. Local Lighthouse throttles
    # relative to this machine and is worthless while editors/browsers are open —
    # measured here, TBT climbed 340 -> 660 -> 960ms across three consecutive runs
    # purely from accumulated background load.
    have_key = bool(psi_key(args.psi_key))
    if args.backend is None:
        args.backend = "psi" if have_key else "local"

    runs = args.runs if args.runs is not None else (3 if args.backend == "local" else 1)
    factors = ["mobile", "desktop"] if args.form_factor == "both" else [args.form_factor]

    if args.backend == "local":
        print("backend: local lighthouse — scores are calibrated to THIS machine; "
              "compare deltas, not absolutes." +
              ("" if have_key else " No PAGESPEED_KEY found; --backend psi would "
                                  "otherwise give comparable absolute scores."),
              file=sys.stderr)
    else:
        print(f"backend: PSI (Google's servers){'' if have_key else ' — NO KEY, expect 429'}",
              file=sys.stderr)

    exit_code = 0
    for slug, url in targets:
        for ff in factors:
            label = f"[{ff}]" + (f" {slug}" if slug else "")
            try:
                res = (run_local(url, ff, runs) if args.backend == "local"
                       else run_psi(url, ff, args.psi_key))
            except (RuntimeError, subprocess.TimeoutExpired) as e:
                print(f"\n{label}  {url}\n  FAILED: {e}", file=sys.stderr)
                exit_code = 1
                continue
            res["form_factor"] = ff
            res["backend"] = args.backend
            res["url"] = url

            hist = [h for h in _load_history(url)
                    if h.get("form_factor") == ff and h.get("backend") == args.backend]
            report(label, url, res, hist[-1] if hist else None)
            if not (args.compare or args.no_save):
                _save_history(url, res)
    sys.exit(exit_code)


if __name__ == "__main__":
    main()
