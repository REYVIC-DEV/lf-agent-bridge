# Architecture

This repo holds five distinct subsystems. They share one Lightfunnels account
and two secrets (`.env`, `.session_token`), but otherwise don't depend on each
other. This doc maps what's where and why.

**Invocation convention**: every script in this repo (root, `pagescore/`,
`content/`) is written to be run **from the repo root** —
`python3 pagescore/build_test3.py`, not `cd pagescore && python3 build_test3.py`.
Secrets and caches are resolved relative to the working directory, so
running from elsewhere will silently look in the wrong place.

## 1. The bridge (repo root) — the actual product

`lf.py`, `lf_api.py`, `lf_session.py`, `get_token.py`, `server.py`,
`templates/`, `legacy/`.

This is what `README.md` and `AGENT.md` document: a dependency-free CLI any
agentic coder drives to list/create/edit/publish Lightfunnels funnels. It's
the stable, public interface — other tooling in this repo is built *on top*
of it, not the other way around. `docs/LIGHTFUNNELS_API.md` is its API
reference; `.claude/skills/lightfunnels/` is the Claude Code skill that wraps
it.

Secrets it reads (repo root, gitignored): `.env` (app token, `PSI_API_KEY`;
`FIGMA_TOKEN` is present but **retired** — Figma is read through the figwright
MCP only), `.session_token` + `.lf_account` (browser session, for real
page-body writes), `.lf_state.json` (saved Playwright session for
`lf_session.py`).

## 2. `pagescore/` — the autonomous performance-tuning loop

`benchmark.py`, `qa_runner.py`, `design_diff.py`, `deploy_guard.py`,
`session_note.py`, `program.md`, the `build_*.py` family, `create_test3.py`,
`host_test3*.py`, `runs/` (gitignored run artifacts), `.cache/` (gitignored
intermediates). `figma_rest.py` is **retired** — it refuses to run.

Modeled on `autoresearch/`'s train/evaluate split (see below):
`benchmark.py` is the **fixed judge** — it hits PSI/Lighthouse and appends to
`pagescore/benchmark_results.tsv`, and is never modified mid-run. The
`build_*.py`/`create_test3.py`/`host_test3*.py` scripts are the **mutable
side** — one-off scripts that build specific test funnels as native
Lightfunnels blocks (from Figma via the figwright MCP + `lf_api.py`), which get
iterated on and re-measured against the fixed harness. `program.md` is the
LANDING PAGE QA RUNBOOK — seven phases and their pass criteria.

The same fixed/mutable split now covers correctness as well as speed:

| Fixed (judges, never changed to make a run pass) | Mutable (what you iterate on) |
|---|---|
| `benchmark.py` — PSI / Lighthouse score | `build_*.py` — the pages |
| `qa_runner.py` — runbook phases 0,1,2,3,4,6 + a11y | |
| `design_diff.py` — Figma copy and typography vs live | |
| `program.md` — the criteria themselves | |

`deploy_guard.py` sits in front of every write: it refuses to overwrite a slug
that is live and published unless a human authorises that run explicitly with
`LF_ALLOW_REDEPLOY=1`. The publish toggle is the deploy mechanism on this
platform — there is no staging and no undo.

`session_note.py` writes each session into `notes/` (see § 5).

These scripts import `lf_api` from the repo root (`sys.path.insert(0, '.')`)
and read the bridge's secrets the same way the bridge itself does — they're
Lightfunnels API consumers, not a separate product.

## 3. `content/` — scraped source material

`extract_techunboxed.py`, `extracted/` (140+ scraped articles as `.md`/`.json`
+ `index.json`).

A standalone scraper for `blog.techunboxed.co`, used to source real
copy/structure when building advertorial-style pages in `pagescore/`. No
dependency on the bridge or on `pagescore/` — it only needs network access.

## 4. `autoresearch/` — external reference, not part of this product

A separately-cloned repo (has its own `.git`) kept for reference: its
`prepare.py`/`train.py`/`program.md` split (fixed-eval-harness vs.
mutable-training-loop, judged by a stable metric) is the pattern
`pagescore/benchmark.py` + `pagescore/build_*.py` + `pagescore/program.md`
deliberately mirror. It is not modified or executed as part of this project —
treat it as read-only prior art.

## 5. `notes/` — the Obsidian vault

An Obsidian vault inside the repo. `notes/LF Page Pipeline.md` is the map of
content; `notes/pages/<slug>.md` carries one note per page with its URL,
builder, funnel and full run history; `notes/sessions/<date>-<slug>.md` is
written at the end of every pipeline run by `pagescore/session_note.py`.
Verdicts in a session note are read straight out of that run's
`findings.json`, so a note cannot claim something the harness did not measure.
Open the `notes/` folder directly as a vault.

## Docs

- `README.md` / `AGENT.md` — the bridge's user-facing and agent-facing
  contracts (start here).
- `SOP.md` / `SOP.pdf` — a non-technical, step-by-step SOP for turning a
  Figma design into a published Lightfunnels page via Claude.
- `docs/LIGHTFUNNELS_API.md` — full GraphQL API reference + field-verified
  platform quirks.
- `.claude/skills/lightfunnels/` — the Claude Code skill (`SKILL.md` +
  `references/block-schema.md`, `figma-inspect.md`, `performance.md`).
- `.claude/skills/page-pipeline/` — the Build → QA → Fix → QA → Done
  orchestrator, driving the `lf-builder`, `lf-qa` and `lf-fixer` agents in
  `.claude/agents/`.
