---
categories:
  - "[[Web-Tech]]"
subjects:
  - "[[Lightfunnels]]"
focus_area: Polished the agents and skill for production
page: "[[page-pipeline]]"
status: done
created: 2026-08-24
commit: 1c70fa0
run_id: -
tags:
  - pipeline
  - tooling
---

# 2026-08-24 — Polished the agents and skill for production

Page: [[page-pipeline]] · Index: [[LF Page Pipeline]]

## What changed

Rewrote `lf-builder`, `lf-qa`, `lf-fixer` and the `page-pipeline` skill for production
use, and closed two holes that would have shown up on the first real run.

**Hole 1 — the fix loop could not run.** The builder creates a new slug inside a
published funnel, so the page is live the moment it exists. The fixer then has to
redeploy that same slug on every cycle, and the guard blocked it every time. Correct
behaviour, unusable loop.

Fixed by scoping authorisation to a named page instead of a blanket switch:

```
LF_ALLOW_REDEPLOY=top-5-v4   # that page only
LF_ALLOW_REDEPLOY=a-v2,b-v2  # a short list
LF_ALLOW_REDEPLOY=1          # any page (blunt, discouraged)
```

The fix loop can now iterate freely on the page it just built while still being unable
to touch the one next to it. The pipeline asks the human for this once at preflight,
naming the page, rather than hitting it mid-loop.

**Hole 2 — QA had nothing to measure.** A brand-new funnel starts unpublished, so the
page is unreachable and the runbook cannot run. The skill now documents the default
(a new slug inside an already-published funnel, reachable immediately, nothing existing
touched) and says explicitly never to QA a `?preview=true` URL and report the numbers
as production.

## What else went in

- Both writing agents now load the `lightfunnels` skill as step zero. Without it a build
  tries the app token, gets `non_allowed_app_funnel_update`, and burns a cycle on what
  looks like a permissions bug and is not — page bodies are only writable in
  `--session` mode.
- `lf-qa` returns a short structured handoff the fixer can act on, rather than only a
  prose report.
- `lf-fixer` gained an explicit six-step loop and a rule against fixing beyond the
  findings, so a regression stays traceable.
- The builder now saves the frame dump to `pagescore/runs/<run-id>/design.json`, which
  is what makes the 1:1 check possible at all.
- A troubleshooting table in the skill maps each symptom to what it actually is —
  platform refusals, detached steps, cold PSI cache, SSR-crashing props.

## Still open

The eleven existing builders do not call `guard()`. Re-running one still overwrites its
live page unchecked. One line per file, left alone because the instruction was not to
modify what is already built.

## Needs a human answer

- [ ] Should the eleven existing build_*.py scripts get the guard() call added, so re-running one cannot silently overwrite its live page?

## Next

- [ ] First real production run: a Figma frame into a published funnel under a new slug

---

Written by `pagescore/session_note.py`. Runbook `pagescore/program.md`.
