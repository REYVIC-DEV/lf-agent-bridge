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
| `benchmark.py` — PSI / Lighthouse score | `build_*.py` — the Lightfunnels pages |
| `qa_runner.py` — runbook phases 0,1,2,3,4,6 + a11y | `~/hlth-site` components + routes |
| `design_diff.py` — copy, type, boxes, spacing and photo crops vs the frame | |
| `program.md` — the criteria themselves | |

⚠️ "Fixed" is a contract, not a description of the file's history. `design_diff.py` was
edited repeatedly while it was being **calibrated** — the rule is that it is never edited
to make a particular run pass. Every threshold in it is justified against measured
before/after, and its guards exist because an over-reporting judge gets ignored, which is
worse than none.

`deploy_guard.py` sits in front of every write: it refuses to overwrite a slug
that is live and published unless a human authorises that run explicitly with
`LF_ALLOW_REDEPLOY=1`. The publish toggle is the deploy mechanism on this
platform — there is no staging and no undo.

`session_note.py` writes each session into `notes/` (see § 5).

These scripts import `lf_api` from the repo root (`sys.path.insert(0, '.')`)
and read the bridge's secrets the same way the bridge itself does — they're
Lightfunnels API consumers, not a separate product.

## 3. `webforge/` — the second target: Figma → the Next.js site

The same designs, built into the storefront repo (cloned separately at `~/hlth-site`)
instead of into Lightfunnels. **Local-first**: nothing deploys, and nothing is pushed
without a human saying so.

| | |
|---|---|
| `qa/web_qa.py` | The QA entry point. **Imports** `pagescore/qa_runner.py` and shells out to `design_diff.py` — it does not fork either |
| `scripts/figma_spec.py` | Flattens a figwright `get_node` dump into just the properties that map onto Tailwind |
| `runs/<id>/` | Per-run evidence: `design.json` (the dump), `crops/` (node renders), `frames.json` (the breakpoint manifest), `accepted.json` (deliberate deviations) |
| `src/harness/` | **Not wired up.** A state machine that shells out to the `claude` CLI, which is not on PATH. The build is driven by `.claude/skills/page-pipeline/SKILL.md` instead |
| `README.md` | setup + the full workflow — start there for this target |

**Why one repo and not a fork.** Measured, not assumed: ~80% of the QA machinery takes a
URL and knows nothing about what served it. `web_qa.py` owns only the genuine local
differences — PSI cannot fetch localhost, a dev server has to be waited for, dev-only
console noise is not a defect, and a dev build is not what ships. Duplicating 700 lines of
judge would let the two drift until a PASS meant two different things.

**The two targets differ in exactly one dangerous way.** On Lightfunnels the publish
toggle *is* the deploy — no staging, no undo, which is why `deploy_guard.py` exists. On
`hlth-site` there is a `staging` branch and a review step, so the risk moves from "wrote
over a live page" to "pushed something nobody looked at" — hence stage 6 of the pipeline
skill asks before pushing, and never runs unattended.

`.claude/rules/` holds the build knowledge for this target: `figma-to-tailwind.md`,
`design-tokens.md`, `component-architecture.md` (including where a route goes — ask, do
not infer) and `vercel-deployment.md` (not in use yet, and says so).

## 4. `content/` — scraped source material

`extract_techunboxed.py`, `extracted/` (140+ scraped articles as `.md`/`.json`
+ `index.json`).

A standalone scraper for `blog.techunboxed.co`, used to source real
copy/structure when building advertorial-style pages in `pagescore/`. No
dependency on the bridge or on `pagescore/` — it only needs network access.

## 5. `autoresearch/` — external reference, not part of this product

A separately-cloned repo (has its own `.git`) kept for reference: its
`prepare.py`/`train.py`/`program.md` split (fixed-eval-harness vs.
mutable-training-loop, judged by a stable metric) is the pattern
`pagescore/benchmark.py` + `pagescore/build_*.py` + `pagescore/program.md`
deliberately mirror. It is not modified or executed as part of this project —
treat it as read-only prior art.

## 6. `notes/` — the Obsidian vault

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
- `SOP.md` / `SOP.pdf` — a non-technical, step-by-step SOP for turning a Figma
  design into a page, for **both** targets: § 4 is Lightfunnels, § 4B is the
  website, § 4C is what the checks do and do not cover.
  ⚠️ `SOP.pdf` is a stale export of an earlier `SOP.md` — regenerate it or ignore it.
- `docs/LIGHTFUNNELS_API.md` — full GraphQL API reference + field-verified
  platform quirks.
- `.claude/skills/lightfunnels/` — the Claude Code skill (`SKILL.md` +
  `references/block-schema.md`, `figma-inspect.md`, `performance.md`).
- `.claude/skills/page-pipeline/` — the orchestrator:
  `ask the route → BUILD → QA → FIX → QA → session note → human looks → offer the push`,
  driving the `lf-builder`, `lf-qa` and `lf-fixer` agents in `.claude/agents/`. Two steps
  belong to the human — the route at the start, the push at the end — and neither runs
  unattended.
- `.claude/rules/` — how to build for `hlth-site`: Figma→Tailwind mapping, the real
  colour/type situation, component architecture and where a route goes, and the
  (not-yet-used) Vercel deployment plan.
