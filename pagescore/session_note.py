#!/usr/bin/env python3
"""
session_note.py -- write the session summary into the repo's Obsidian vault.

Every pipeline run ends with a note, so the next session starts from what the last
one learned instead of rediscovering it. The vault lives at `notes/` inside this repo
(open that folder in Obsidian, or add it as a vault) so nothing is written outside the
project.

Three kinds of note, linked to each other:

  notes/LF Page Pipeline.md        the map of content -- every session, newest first
  notes/pages/<slug>.md            one per page: its URL, builder, funnel, run history
  notes/sessions/<date>-<slug>.md  one per session: what was done, found, fixed, left

Wikilinks (`[[...]]`) connect them, so Obsidian's graph shows which sessions touched
which pages.

Usage:

  python3 pagescore/session_note.py \
      --slug bh-advertorial-v1 \
      --title "Legal modals + alt text" \
      --run-id 2026-08-21-fixpass \
      --body body.md                       # the prose you wrote; "-" reads stdin

  python3 pagescore/session_note.py --slug x --title y --body - <<'EOF'
  ## What happened
  ...
  EOF

Optional metadata: --url, --builder, --funnel, --status, --tag (repeatable),
--question (repeatable, things a human has to answer), --next (repeatable).
"""
import argparse
import json
import os
import re
import subprocess
import sys
from datetime import datetime

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
VAULT = os.path.join(ROOT, "notes")
MOC = os.path.join(VAULT, "LF Page Pipeline.md")

MOC_SEED = """---
categories:
  - "[[Web-Tech]]"
subjects:
  - "[[Lightfunnels]]"
focus_area: Figma to Lightfunnels page pipeline -- build, QA, fix, ship
status: living
---

# LF Page Pipeline

The map of content for every page built and QA'd through
`.claude/skills/page-pipeline`. Each session writes itself in here; each page keeps
its own note with its full history.

- Runbook: `pagescore/program.md`
- Mechanical judge: `pagescore/qa_runner.py`
- Design fidelity: `pagescore/design_diff.py`
- Live-page guard: `pagescore/deploy_guard.py`

## Pages

<!-- pages -->

## Sessions

<!-- sessions -->
"""

PAGE_SEED = """---
categories:
  - "[[Web-Tech]]"
subjects:
  - "[[Lightfunnels]]"
focus_area: {slug}
status: live
created: {today}
---

# {slug}

| | |
|---|---|
| URL | {url} |
| Builder | `{builder}` |
| Funnel | `{funnel}` |

Part of [[LF Page Pipeline]].

## Open questions

<!-- questions -->

## Session history

<!-- history -->
"""


def slugify(s):
    return re.sub(r"[^a-z0-9]+", "-", (s or "").lower()).strip("-")


def git_commit():
    try:
        return subprocess.check_output(["git", "rev-parse", "--short", "HEAD"],
                                       cwd=ROOT, stderr=subprocess.DEVNULL).decode().strip()
    except Exception:
        return "unknown"


def ensure_vault():
    os.makedirs(os.path.join(VAULT, "pages"), exist_ok=True)
    os.makedirs(os.path.join(VAULT, "sessions"), exist_ok=True)
    if not os.path.exists(MOC):
        open(MOC, "w").write(MOC_SEED)


def insert_after(path, marker, line):
    """Add a bullet under a marker, newest first, without duplicating it."""
    txt = open(path).read()
    if line.strip() in txt:
        return
    if marker not in txt:
        txt += f"\n{marker}\n"
    txt = txt.replace(marker, f"{marker}\n{line}", 1)
    open(path, "w").write(txt)


def run_summary(run_id):
    """Pull the machine verdicts straight out of the QA run, so the note cannot
    disagree with what was actually measured."""
    fj = os.path.join(HERE, "runs", run_id, "findings.json")
    if not os.path.exists(fj):
        return None, []
    run = json.load(open(fj))
    lines = ["", f"## Measured ({run_id})", "",
             "| Page | Verdict | Speed | Links | Meta | Mobile | Console | A11y |",
             "|---|---|---|---|---|---|---|---|"]
    for p in run.get("pages", []):
        ph = p.get("phases", {})
        def v(k):
            return ph.get(k, {}).get("verdict", "-")
        name = p.get("final_url", "").rstrip("/").split("/")[-1]
        lines.append(f"| {name} | **{p.get('verdict','?')}** | {v('phase1')} | "
                     f"{v('phase2')} | {v('phase3')} | {v('phase4')} | "
                     f"{v('phase6')} | {v('a11y')} |")
    lines += ["", f"Full findings: `pagescore/runs/{run_id}/findings.json`", ""]
    return run.get("summary"), lines


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--slug", required=True, help="the page this session was about")
    ap.add_argument("--title", required=True, help="what the session was, in a few words")
    ap.add_argument("--body", default="-", help="markdown file, or - for stdin")
    ap.add_argument("--run-id", default=None)
    ap.add_argument("--url", default="")
    ap.add_argument("--builder", default="")
    ap.add_argument("--funnel", default="")
    ap.add_argument("--status", default="done",
                    choices=["done", "in-progress", "blocked"])
    ap.add_argument("--tag", action="append", default=[])
    ap.add_argument("--question", action="append", default=[],
                    help="something only a human can answer; repeatable")
    ap.add_argument("--next", dest="nexts", action="append", default=[])
    args = ap.parse_args()

    ensure_vault()
    today = datetime.now().strftime("%Y-%m-%d")
    slug = slugify(args.slug)
    body = sys.stdin.read() if args.body == "-" else open(args.body).read()

    # --- page note -------------------------------------------------------
    page_path = os.path.join(VAULT, "pages", f"{slug}.md")
    if not os.path.exists(page_path):
        open(page_path, "w").write(PAGE_SEED.format(
            slug=slug, today=today, url=args.url or "-",
            builder=args.builder or "-", funnel=args.funnel or "-"))

    # --- session note ----------------------------------------------------
    base = f"{today}-{slug}"
    n, sess_path = 1, os.path.join(VAULT, "sessions", f"{base}.md")
    while os.path.exists(sess_path):
        n += 1
        sess_path = os.path.join(VAULT, "sessions", f"{base}-{n}.md")
    sess_name = os.path.basename(sess_path)[:-3]

    summary, measured = run_summary(args.run_id) if args.run_id else (None, [])
    tags = args.tag or ["lightfunnels", "qa"]

    out = [
        "---",
        "categories:",
        '  - "[[Web-Tech]]"',
        "subjects:",
        '  - "[[Lightfunnels]]"',
        f"focus_area: {args.title}",
        f"page: \"[[{slug}]]\"",
        f"status: {args.status}",
        f"created: {today}",
        f"commit: {git_commit()}",
        f"run_id: {args.run_id or '-'}",
        "tags:",
    ] + [f"  - {t}" for t in tags] + [
        "---", "",
        f"# {today} — {args.title}",
        "",
        f"Page: [[{slug}]] · Index: [[LF Page Pipeline]]",
        "",
    ]
    if summary:
        out.append(f"**Result:** {summary.get('PASS',0)} PASS, "
                   f"{summary.get('FLAG',0)} FLAG, {summary.get('FAIL',0)} FAIL")
        out.append("")
    out.append(body.strip())
    out += measured

    if args.question:
        out += ["", "## Needs a human answer", ""]
        out += [f"- [ ] {q}" for q in args.question]
    if args.nexts:
        out += ["", "## Next", ""]
        out += [f"- [ ] {x}" for x in args.nexts]
    out += ["", "---", "",
            f"Written by `pagescore/session_note.py`. "
            f"Runbook `pagescore/program.md`.", ""]
    open(sess_path, "w").write("\n".join(out))

    # --- backlinks -------------------------------------------------------
    insert_after(page_path, "<!-- history -->",
                 f"- {today} — [[{sess_name}]] — {args.title} ({args.status})")
    if args.question:
        for q in args.question:
            insert_after(page_path, "<!-- questions -->", f"- [ ] {q} — [[{sess_name}]]")
    insert_after(MOC, "<!-- sessions -->",
                 f"- {today} — [[{sess_name}]] — {args.title} → [[{slug}]]")
    insert_after(MOC, "<!-- pages -->", f"- [[{slug}]]")

    print(os.path.relpath(sess_path, ROOT))
    print(os.path.relpath(page_path, ROOT))
    print(os.path.relpath(MOC, ROOT))


if __name__ == "__main__":
    main()
