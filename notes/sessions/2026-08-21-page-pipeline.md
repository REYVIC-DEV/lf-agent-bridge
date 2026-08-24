---
categories:
  - "[[Web-Tech]]"
subjects:
  - "[[Lightfunnels]]"
focus_area: Built the Figma to live page pipeline
page: "[[page-pipeline]]"
status: done
created: 2026-08-21
commit: 1c70fa0
run_id: smoke-test
tags:
  - lightfunnels
  - tooling
  - pipeline
---

# 2026-08-21 — Built the Figma to live page pipeline

Page: [[page-pipeline]] · Index: [[LF Page Pipeline]]

**Result:** 0 PASS, 1 FLAG, 0 FAIL

## What happened

Turned the ad-hoc build-and-QA process into a repeatable pipeline. Nothing live was
touched — every live page was read, never written.

## What was built

**Judges (fixed — never changed to make a run pass)**

| File | Does |
|---|---|
| `pagescore/qa_runner.py` | Runbook phases 0, 1, 2, 3, 4, 6 plus accessibility, mechanically. Writes `findings.json`, `report.md`, screenshots, `page_text.txt`. |
| `pagescore/design_diff.py` | Figma vs live: copy that never made it onto the page, copy that was retyped instead of copied, typography that does not match the node. |
| `pagescore/deploy_guard.py` | Refuses to write to a slug that is live and published, unless a human authorises that run with `LF_ALLOW_REDEPLOY=1`. |
| `pagescore/session_note.py` | Writes this note. Pulls verdicts from `findings.json` so a note cannot claim something that was not measured. |

**Agents** — `lf-builder` (figwright → `build_*.py`), `lf-qa` (read-only judge),
`lf-fixer` (applies findings in verified batches).

**Orchestrator** — `.claude/skills/page-pipeline`, running
Build → QA → Fix → QA → Done with a two-cycle stop condition.

## What changed in the skill

Figma is now read through **figwright only**. The Figma MCP connector and the REST
API path are retired: the connector is denied in `settings.local.json`, and
`pagescore/figma_rest.py` refuses to run. Both were per-seat rate limited, which is
what made them unusable for a real build — a View seat gets about six REST calls a
month and a 429 takes roughly 4.6 days to clear.

## What the harness found on its first run

Two real defects on `bh-advertorial-v1`, neither previously recorded:

- Lightfunnels builds its Google Fonts URL from the whole CSS font stack, so it
  requests `family=Inter,+InterFallback,+sans-serif` — two families that do not
  exist. Blocked by ORB on every page load. Platform bug, not a builder bug.
- Seven content images still render with no `alt` text.

## Calibration notes

The harness cried wolf three times before it was trusted, and each was fixed rather
than tolerated: analytics beacons abort by design at page teardown and were being
counted as broken requests; a title-versus-h1 check compared string prefixes and
flagged two phrasings of the same headline; and copy split across inline elements
looked retyped when it was intact. A judge that over-reports gets ignored, which is
worse than not having one.

## Measured (smoke-test)

| Page | Verdict | Speed | Links | Meta | Mobile | Console | A11y |
|---|---|---|---|---|---|---|---|
| bh-advertorial-v1 | **FLAG** | SKIP | PASS | PASS | PASS | FLAG | FLAG |

Full findings: `pagescore/runs/smoke-test/findings.json`


## Needs a human answer

- [ ] Should the eleven existing build_*.py scripts get the guard() call added, so re-running one cannot silently overwrite its live page?

## Next

- [ ] First real run: give the pipeline a Figma frame and a new slug

---

Written by `pagescore/session_note.py`. Runbook `pagescore/program.md`.
