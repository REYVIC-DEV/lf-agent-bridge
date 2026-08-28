#!/usr/bin/env python3
"""
web_qa.py -- the QA entry point for a locally-served Next.js page.

It does NOT fork the runbook. `pagescore/program.md` stays the standard and
`pagescore/qa_runner.py` stays the judge, so a PASS here and a PASS on a Lightfunnels
page mean the same thing. What lives here is only what genuinely differs when the
target is a local dev server instead of a public storefront:

  * PageSpeed cannot reach localhost. Google fetches the URL from their own servers,
    so `--method psi` fails by definition. Speed is a deploy-time check; the local gate
    is structural.
  * A dev server has to be UP. Half the "failures" in a local run are really a server
    that was still compiling, or had died since the last run. This waits for it and says
    so plainly instead of reporting a page defect.
  * Dev-only noise is not a defect. HMR sockets, react-refresh, the Next dev overlay and
    the site's own `/api/collect` beacon all abort or 404 by design in dev.
  * A dev build is not what ships. `--prod` builds and serves the production output,
    which is the honest thing to measure -- dev is unminified, unbundled and slower.

Usage (from the repo root):

  python3 webforge/qa/web_qa.py /pages/email-exclusive --project ~/hlth-site
  python3 webforge/qa/web_qa.py /pages/email-exclusive --run-id emailx-001
  python3 webforge/qa/web_qa.py /pages/email-exclusive --design webforge/runs/emailx-001/design.json
  python3 webforge/qa/web_qa.py /pages/email-exclusive --prod       # build + next start
  python3 webforge/qa/web_qa.py http://localhost:3000/pages/x --no-serve   # already running
"""
import argparse
import json
import os
import subprocess
import sys
import time
import urllib.error
import urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
WEBFORGE = os.path.dirname(HERE)
REPO = os.path.dirname(WEBFORGE)
sys.path.insert(0, os.path.join(REPO, "pagescore"))

import qa_runner  # noqa: E402  -- the shared judge, imported not copied

# Requests a dev server makes that are not defects. Added to the shared beacon list
# rather than replacing it, so the storefront filters still apply.
DEV_NOISE = (
    "_next/webpack-hmr", "__nextjs", "react-refresh", "/_next/static/chunks/_error",
    "hot-update", "/api/collect", "__next_devtools", "on-demand-entries-ping",
)


def server_up(url, timeout=5):
    try:
        req = urllib.request.Request(url, headers={"User-Agent": qa_runner.UA})
        with urllib.request.urlopen(req, timeout=timeout) as r:
            return 200 <= r.status < 400
    except urllib.error.HTTPError as e:
        return e.code < 500
    except Exception:
        return False


def wait_for(url, seconds=90):
    deadline = time.time() + seconds
    while time.time() < deadline:
        if server_up(url):
            return True
        time.sleep(1)
    return False


def write_todo(run_dir, designs, page):
    """One list of everything to fix, across every breakpoint.

    The point of the loop is that nobody has to read four JSON files and work out what
    they have in common. A fixer -- human or agent -- reads this and nothing else.
    """
    lines = ["# To fix", ""]
    for f in page.get("findings", []):
        if f.get("verdict") == "FAIL":
            lines.append(f"- **runbook / {f.get('phase', '?')}** — {f.get('detail') or f.get('check')}")
    for spec in designs:
        spec_path, _, width = spec.partition("@")
        width = width or "1440"
        sub = run_dir if len(designs) == 1 else f"{run_dir}-{width}w"
        p = os.path.join(sub, "design_diff.json")
        if not os.path.exists(p):
            continue
        d = json.load(open(p))
        head = f"\n## {width}px — {os.path.basename(spec_path)}\n"
        body = []
        for r in d.get("rows", []):
            if r["status"] == "ACCEPTED":
                continue        # a decision already made, not work to do
            if r["status"] == "MISSING":
                body.append(f"- **copy missing** — `{r['figma']}`")
            elif r["status"] == "RETYPED":
                body.append(f"- **retyped** — design `{r['figma']}` / page `{r.get('live')}`")
            for delta in (r.get("deltas") or []):
                body.append(f"- {delta}  ·  `{(r['figma'] or '')[:48]}`")
        for r in d.get("images", []):
            for delta in (r.get("deltas") or []):
                body.append(f"- **image** {delta}  ·  `{os.path.basename(r.get('src') or r.get('path') or '')}`")
        for r in d.get("layout", []):
            body.append(f"- **spacing** {r['delta']}")
        if body:
            lines.append(head)
            lines += sorted(set(body))
    if len(lines) == 2:
        lines.append("Nothing. The page matches the design at every breakpoint checked.")
    with open(os.path.join(run_dir, "todo.md"), "w") as fh:
        fh.write("\n".join(lines) + "\n")


def main():
    ap = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("path", help="a route like /pages/email-exclusive, or a full URL")
    ap.add_argument("--project", default=os.path.expanduser("~/hlth-site"))
    ap.add_argument("--port", type=int, default=3000)
    ap.add_argument("--run-id", default=None)
    ap.add_argument("--design", action="append", default=None, metavar="SPEC[@W]",
                    help="figwright dump, to also run the fidelity diff. Repeatable, "
                         "and a trailing @<width> pins the viewport -- a responsive "
                         "build has one frame per breakpoint and checking only the "
                         "widest one is how a mobile layout ships unlooked-at. "
                         "e.g. --design mobile.json@390 --design desktop.json@1440")
    ap.add_argument("--frames", default=None,
                    help="a frames.json listing every breakpoint the design draws "
                         "({frames:[{width, spec, crops}]}). Equivalent to spelling "
                         "out --design/--crops, but it lives next to the run so a "
                         "breakpoint cannot be forgotten off the command line.")
    ap.add_argument("--accept", action="append", default=None,
                    help="JSON of deviations that are decisions, not defects; one per "
                         "--design. Usually set in frames.json instead.")
    ap.add_argument("--crops", action="append", default=None,
                    help="directory of per-node PNG renders for the matching --design "
                         "(figwright save_screenshots, <node-id>.png). Without it a "
                         "photo is checked for box and aspect but not for crop.")
    ap.add_argument("--prod", action="store_true",
                    help="build and serve the production output instead of dev")
    ap.add_argument("--no-serve", action="store_true",
                    help="a server is already running; do not start one")
    args = ap.parse_args()

    if args.frames:
        manifest = json.load(open(args.frames))
        args.design = list(args.design or [])
        args.crops = list(args.crops or [])
        args.accept = list(getattr(args, "accept", None) or [])
        for fr in manifest.get("frames", []):
            args.design.append(f"{fr['spec']}@{fr['width']}")
            args.crops.append(fr.get("crops") or "")
            args.accept.append(fr.get("accept") or "")

    url = (args.path if "://" in args.path
           else f"http://localhost:{args.port}{args.path if args.path.startswith('/') else '/' + args.path}")
    run_id = args.run_id or time.strftime("web-%Y-%m-%d-%H%M")
    root = url.split("/", 3)[:3]
    root_url = "/".join(root) + "/"

    server = None
    if not args.no_serve and not server_up(root_url):
        if args.prod:
            print("  building production output…")
            b = subprocess.run(["npm", "run", "build"], cwd=args.project,
                               capture_output=True, text=True)
            if b.returncode != 0:
                sys.exit(f"build failed:\n{b.stdout[-2000:]}\n{b.stderr[-1000:]}")
        cmd = ["npm", "run", "start" if args.prod else "dev", "--", "--port", str(args.port)]
        print(f"  starting: {' '.join(cmd)}")
        server = subprocess.Popen(cmd, cwd=args.project, start_new_session=True,
                                  stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    try:
        if not wait_for(url):
            sys.exit(
                f"\n{url} never answered.\n"
                f"  That is a server problem, not a page defect -- nothing was measured.\n"
                f"  Check the project builds: cd {args.project} && npm run dev\n")
        print(f"  serving: {url}")

        # Dev-only chatter joins the shared beacon filter rather than replacing it.
        qa_runner.BEACON_HOSTS = tuple(qa_runner.BEACON_HOSTS) + DEV_NOISE

        class Opts:
            method = "lighthouse"
            skip_psi = True          # PSI cannot fetch localhost. Not negotiable.
            after_publish = False
            no_shots = False
            note = f"webforge local ({'prod' if args.prod else 'dev'} server)"

        run_dir = os.path.join(REPO, "pagescore", "runs", run_id)
        os.makedirs(run_dir, exist_ok=True)
        page = qa_runner.qa_page(url, run_dir, Opts())

        run = {"run_id": run_id, "started": qa_runner.now(),
               "runbook": "pagescore/program.md", "target": "local next server",
               "mode": "prod" if args.prod else "dev",
               "thresholds": qa_runner.THRESHOLDS, "pages": [page],
               "finished": qa_runner.now()}
        run["summary"] = {v: (1 if page["verdict"] == v else 0)
                          for v in ("PASS", "FLAG", "FAIL")}
        with open(os.path.join(run_dir, "findings.json"), "w") as f:
            json.dump(run, f, indent=2)
        with open(os.path.join(run_dir, "report.md"), "w") as f:
            f.write(qa_runner.render_report(run))

        fidelity_failed = False
        for i, spec in enumerate(args.design or []):
            spec_path, _, width = spec.partition("@")
            width = width or "1440"
            mobile = int(width) < 768
            sub = run_dir if len(args.design) == 1 else f"{run_dir}-{width}w"
            os.makedirs(sub, exist_ok=True)
            print(f"\n  fidelity vs {os.path.basename(spec_path)} @ {width}px:")
            cmd = [sys.executable, os.path.join(REPO, "pagescore", "design_diff.py"),
                   spec_path, url, "--viewport", width, "--out", sub]
            if mobile:
                cmd.append("--mobile")
            crops = (args.crops or [])
            if i < len(crops) and crops[i]:
                cmd += ["--crops", crops[i]]
            acc = (args.accept or [])
            if i < len(acc) and acc[i]:
                cmd += ["--accept", acc[i]]
            if subprocess.run(cmd, cwd=REPO).returncode:
                fidelity_failed = True

        write_todo(run_dir, args.design or [], page)
        verdict = page["verdict"]
        if fidelity_failed and verdict != "FAIL":
            verdict = "FAIL"
            print("\n  the runbook passed but the page does not match the design.")
        print(f"\n  {verdict}  ->  pagescore/runs/{run_id}/")
        print("  speed is NOT measured locally -- PSI cannot fetch localhost.")
        sys.exit(1 if verdict == "FAIL" else 0)
    finally:
        if server is not None:
            try:
                os.killpg(os.getpgid(server.pid), 15)
            except Exception:
                pass


if __name__ == "__main__":
    main()
