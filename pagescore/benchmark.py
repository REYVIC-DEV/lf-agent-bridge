#!/usr/bin/env python3
"""
benchmark.py -- the fixed performance-evaluation harness for LF pages.

Ground truth in the same sense as autoresearch/prepare.py's evaluate_bpb: this
file MEASURES, it does not build. build_*.py (build_test3.py, build_full.py,
...) are the "train.py" side -- you iterate on those, duplicating funnels and
patching header_scripts to chase a better score. This script stays untouched
across iterations so every run is judged by the same yardstick, and every
result lands in one append-only log (BENCHMARK_TSV) so a run can be compared
against the baseline recorded before you started changing anything.

Scoring model (see .claude/skills/lightfunnels/references/performance.md):
  - PSI/Lighthouse performance score: red 0-49, orange 50-89, green 90-100.
  - CLS is the metric that almost always drags an LF mobile score down
    (Inter font-swap reflow). Agentic Browsing hard-fails at CLS >= 0.1
    regardless of the overall performance score.
  - Ground truth is Google's real PSI API (--method psi, default). Local
    Lighthouse (--method lighthouse) is faster for iteration but can under-
    report CLS on a fast machine because fonts arrive before the swap would
    have happened -- don't trust a lighthouse-only PASS over a psi FAIL.

Usage:
  python3 benchmark.py <url> [<url2> ...]                 # PSI, mobile+desktop
  python3 benchmark.py <url> --strategy mobile             # one strategy only
  python3 benchmark.py <url> --method lighthouse           # local Lighthouse
  python3 benchmark.py <url> --note "v3 duplicate, pre-fix"
  python3 benchmark.py --show                              # print the log
  python3 benchmark.py --show --url <url>                  # filter the log

Needs PSI_API_KEY in .env (or the environment) for --method psi. Without a
key, falls back to local Lighthouse if the `lighthouse` CLI is on PATH
(npx --yes lighthouse@latest is fetched on first use).
"""
import argparse
import json
import os
import subprocess
import sys
import tempfile
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime, timezone

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
BENCHMARK_TSV = os.path.join(HERE, "benchmark_results.tsv")

PSI_ENDPOINT = "https://www.googleapis.com/pagespeedonline/v5/runPagespeed"
STRATEGIES = ("mobile", "desktop")
GREEN_THRESHOLD = 90
CLS_HARD_FAIL = 0.1

TSV_COLUMNS = [
    "timestamp", "url", "strategy", "method", "performance",
    "cls", "lcp_s", "fcp_s", "si_s", "tbt_ms", "agentic_pass",
    "commit", "note",
]


def psi_api_key(env_path=os.path.join(ROOT, ".env")):
    key = os.environ.get("PSI_API_KEY")
    if not key and os.path.exists(env_path):
        for line in open(env_path):
            if line.startswith("PSI_API_KEY="):
                key = line.split("=", 1)[1].strip().strip('"').strip("'")
    return key


def git_commit():
    try:
        out = subprocess.check_output(
            ["git", "rev-parse", "--short", "HEAD"], cwd=HERE, stderr=subprocess.DEVNULL
        )
        return out.decode().strip()
    except Exception:
        return "unknown"


def _audit_value(audits, audit_id, key="numericValue", divisor=1.0):
    a = audits.get(audit_id)
    if not a or a.get(key) is None:
        return None
    return a[key] / divisor


def _agentic_pass(categories, cls):
    """Best-effort: use Lighthouse's own Agentic Browsing category if PSI
    returned one, else derive from the documented hard rule (CLS < 0.1)."""
    for cat_id, cat in (categories or {}).items():
        if "agentic" in cat_id.lower():
            score = cat.get("score")
            return score is not None and score >= 1.0
    if cls is None:
        return None
    return cls < CLS_HARD_FAIL


def _parse_lighthouse_result(data):
    lr = data["lighthouseResult"] if "lighthouseResult" in data else data
    audits = lr.get("audits", {})
    categories = lr.get("categories", {})
    perf_score = categories.get("performance", {}).get("score")
    cls = _audit_value(audits, "cumulative-layout-shift")
    metrics = {
        "performance": round(perf_score * 100) if perf_score is not None else None,
        "cls": cls,
        "lcp_s": _audit_value(audits, "largest-contentful-paint", divisor=1000.0),
        "fcp_s": _audit_value(audits, "first-contentful-paint", divisor=1000.0),
        "si_s": _audit_value(audits, "speed-index", divisor=1000.0),
        "tbt_ms": _audit_value(audits, "total-blocking-time"),
        "agentic_pass": _agentic_pass(categories, cls),
    }
    return metrics


def fetch_psi(url, strategy, api_key):
    params = {
        "url": url,
        "key": api_key,
        "strategy": strategy,
        "category": "PERFORMANCE",
    }
    full_url = f"{PSI_ENDPOINT}?{urllib.parse.urlencode(params)}"
    req = urllib.request.Request(full_url)
    try:
        with urllib.request.urlopen(req, timeout=90) as r:
            data = json.loads(r.read())
    except urllib.error.HTTPError as e:
        body = e.read().decode(errors="replace")
        raise RuntimeError(f"PSI HTTP {e.code}: {body[:300]}")
    return _parse_lighthouse_result(data)


def run_lighthouse(url, strategy):
    if subprocess.call(
        ["which", "lighthouse"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL
    ) != 0 and subprocess.call(
        ["which", "npx"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL
    ) != 0:
        raise RuntimeError("neither `lighthouse` nor `npx` found on PATH")

    with tempfile.TemporaryDirectory() as tmp:
        out_path = os.path.join(tmp, "report.json")
        cmd = [
            "npx", "--yes", "lighthouse@latest", url,
            "--only-categories=performance",
            "--output=json", f"--output-path={out_path}",
            "--chrome-flags=--headless=new",
            "--quiet",
        ]
        if strategy == "mobile":
            cmd += ["--form-factor=mobile", "--screenEmulation.mobile"]
        else:
            cmd += ["--form-factor=desktop", "--screenEmulation.disabled",
                    "--preset=desktop"]
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=180)
        if result.returncode != 0 or not os.path.exists(out_path):
            raise RuntimeError(f"lighthouse failed: {result.stderr[-500:]}")
        with open(out_path) as f:
            data = json.load(f)
    return _parse_lighthouse_result(data)


def evaluate(url, strategy, method):
    """The one function every benchmark run goes through. Ground truth."""
    if method == "psi":
        key = psi_api_key()
        if not key:
            raise RuntimeError(
                "PSI_API_KEY not set (env or .env) -- use --method lighthouse instead"
            )
        return fetch_psi(url, strategy, key)
    if method == "lighthouse":
        return run_lighthouse(url, strategy)
    raise ValueError(f"unknown method: {method}")


def band(performance):
    if performance is None:
        return "?"
    if performance >= GREEN_THRESHOLD:
        return "GREEN"
    if performance >= 50:
        return "orange"
    return "red"


def fmt(v, suffix="", digits=2):
    if v is None:
        return "n/a"
    return f"{v:.{digits}f}{suffix}"


def print_result(url, strategy, method, m):
    agentic = {True: "PASS", False: "FAIL", None: "n/a"}[m["agentic_pass"]]
    print(
        f"{url} [{strategy}/{method}] "
        f"perf={m['performance']} ({band(m['performance'])}) "
        f"CLS={fmt(m['cls'], digits=3)} "
        f"LCP={fmt(m['lcp_s'], 's')} FCP={fmt(m['fcp_s'], 's')} "
        f"SI={fmt(m['si_s'], 's')} TBT={fmt(m['tbt_ms'], 'ms', 0)} "
        f"AgenticBrowsing={agentic}"
    )


def record(url, strategy, method, m, note, timestamp):
    is_new = not os.path.exists(BENCHMARK_TSV)
    with open(BENCHMARK_TSV, "a") as f:
        if is_new:
            f.write("\t".join(TSV_COLUMNS) + "\n")
        row = [
            timestamp, url, strategy, method,
            "" if m["performance"] is None else str(m["performance"]),
            "" if m["cls"] is None else f"{m['cls']:.4f}",
            "" if m["lcp_s"] is None else f"{m['lcp_s']:.2f}",
            "" if m["fcp_s"] is None else f"{m['fcp_s']:.2f}",
            "" if m["si_s"] is None else f"{m['si_s']:.2f}",
            "" if m["tbt_ms"] is None else f"{m['tbt_ms']:.0f}",
            "" if m["agentic_pass"] is None else str(m["agentic_pass"]),
            git_commit(),
            note.replace("\t", " ") if note else "",
        ]
        f.write("\t".join(row) + "\n")


def show(url_filter=None):
    if not os.path.exists(BENCHMARK_TSV):
        print("no benchmark_results.tsv yet -- run a benchmark first")
        return
    with open(BENCHMARK_TSV) as f:
        lines = f.read().splitlines()
    if not lines:
        print("benchmark_results.tsv is empty")
        return
    header = lines[0]
    print(header)
    for line in lines[1:]:
        if url_filter and url_filter not in line:
            continue
        print(line)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("urls", nargs="*", help="page URL(s) to benchmark")
    ap.add_argument("--strategy", choices=STRATEGIES, help="default: both mobile and desktop")
    ap.add_argument("--method", choices=("psi", "lighthouse"), default="psi")
    ap.add_argument("--note", default="", help="free-text note recorded alongside the result")
    ap.add_argument("--no-record", action="store_true", help="print only, don't append to the log")
    ap.add_argument("--show", action="store_true", help="print benchmark_results.tsv and exit")
    ap.add_argument("--url", dest="show_url_filter", default=None, help="with --show, filter rows containing this substring")
    args = ap.parse_args()

    if args.show:
        show(args.show_url_filter)
        return

    if not args.urls:
        ap.error("at least one URL is required (or use --show)")

    strategies = [args.strategy] if args.strategy else list(STRATEGIES)
    timestamp = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

    exit_code = 0
    for url in args.urls:
        for strategy in strategies:
            try:
                m = evaluate(url, strategy, args.method)
            except Exception as e:
                print(f"{url} [{strategy}/{args.method}] ERROR: {e}", file=sys.stderr)
                exit_code = 1
                continue
            print_result(url, strategy, args.method, m)
            if not args.no_record:
                record(url, strategy, args.method, m, args.note, timestamp)

    sys.exit(exit_code)


if __name__ == "__main__":
    main()
