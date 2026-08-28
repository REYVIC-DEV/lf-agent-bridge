---
categories:
  - "[[Web-Tech]]"
subjects:
  - "[[Lightfunnels]]"
focus_area: README, SOP and ARCHITECTURE updated for the second target
page: "[[docs-webforge-sop]]"
status: done
created: 2026-08-26
commit: f89cf37
run_id: web-2026-08-26-2337
tags:
  - docs
  - webforge
  - sop
---

# 2026-08-26 — README, SOP and ARCHITECTURE updated for the second target

Page: [[docs-webforge-sop]] · Index: [[LF Page Pipeline]]

**Result:** 1 PASS, 0 FLAG, 0 FAIL

## What changed

All three docs described a repo that only had one target.

**`README.md`** — reframed from "Lightfunnels bridge" to "Figma → page, for two
targets", with the difference that matters stated up front: on Lightfunnels the publish
toggle *is* the deploy, on the website a push to `staging` is. New **webforge** section
covering why it is not a fork, the one command, the three files a run needs
(`frames.json`, `crops/`, `accepted.json`), a table of what the fidelity judge checks —
and what it does not.

**`SOP.md`** — kept the plain-English voice and added:
- a **pick-your-destination table** at the top, because the two flows diverge immediately
- **§ 4B** — the website workflow: both frames, say where the page goes, review, and the
  staging push that Claude asks about rather than performs
- **§ 4C** — what Claude checks and what it cannot, ending on the one that matters:
  *everything can pass and the page can still be wrong for what you're trying to do*
- new Do's/Don'ts, five troubleshooting rows, six glossary terms, and golden rules that
  now include "both frames, every time" and "say where the page goes before it's built"

**`docs/ARCHITECTURE.md`** — new § 3 for `webforge/`, sections renumbered, and the judges
table updated to say what `design_diff.py` actually covers now.

## Things I wrote down because they are easy to get wrong

**`/blog/template/…` 404s on the real site.** In the SOP as a Don't, in plain terms: you
cannot send email or ad traffic to that link. It is the single most expensive thing a
non-technical reader could get wrong here.

**"All checks passed" is not "ready to ship."** Said three times, in three registers,
because it is the failure mode this tooling makes *more* likely rather than less. The
judge compares the page to the drawing; it cannot tell you the drawing was right.

**"Fixed" is a contract, not a description.** `design_diff.py` was edited many times
today. The rule was never "this file does not change" — it is "this file is never changed
to make a particular run pass." Worth stating in ARCHITECTURE, since the file's history
contradicts the label at a glance.

## Honesty passes

Two things the docs now say plainly rather than implying they work:

- **`webforge/src/harness/*.ts` is not wired up.** It shells out to the `claude` CLI,
  which is not on PATH, so `GENERATE_CODE` cannot run. The build is driven by the
  page-pipeline skill instead; the harness is scaffolding.
- **`deploy:preview` / `deploy:prod` are unused.** Vercel is not in use.
- **`SOP.pdf` is stale** — a 29 July export against an SOP rewritten today. Flagged in
  ARCHITECTURE rather than left to mislead.

## Verified, not assumed

- Every script path named in the docs exists (7/7 checked).
- Every CLI flag named exists — `web_qa.py` has all of `--project --port --run-id
  --design --frames --accept --crops --prod --no-serve`; `design_diff.py` has
  `--viewport --mobile --out --accept --crops`.
- The `frames.json` example in the README is the real file, copied, not paraphrased.
- **The documented command was run exactly as written** and behaved as documented:
  runbook PASS on every phase, both breakpoints diffed, and an overall FAIL on the
  unresolved price — which is the documented behaviour, since a clean runbook does not
  pass the run.

## Measured (web-2026-08-26-2337)

| Page | Verdict | Speed | Links | Meta | Mobile | Console | A11y |
|---|---|---|---|---|---|---|---|
| email-exclusive | **PASS** | SKIP | PASS | PASS | PASS | PASS | PASS |

Full findings: `pagescore/runs/web-2026-08-26-2337/findings.json`


## Next

- [ ] Regenerate SOP.pdf from SOP.md — the PDF is a 29 July export and now nearly a month behind.
- [ ] Still open on the page itself: the £79 vs £67.15 price conflict between the two frames.

---

Written by `pagescore/session_note.py`. Runbook `pagescore/program.md`.
