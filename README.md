# lf-agent-bridge — Figma → page, for two different targets

A dependency-free CLI + Claude Code **skills** that let an agentic coder
(Claude Code, Codex, Cursor, …) build a page from a Figma design and prove it
matches — instead of rebuilding it by hand.

There are two places a page can land, and they share one judge:

| | Target | Built by | Deployed by |
|---|---|---|---|
| **Lightfunnels** | a funnel step on `lightfunnels.com` | `pagescore/build_*.py` | the publish toggle — there is no staging |
| **webforge** | a route in the Next.js storefront (`~/hlth-site`) | a component + route, by hand | a push to `staging`, on your say-so |

`pagescore/program.md` is the runbook and `pagescore/qa_runner.py` +
`pagescore/design_diff.py` are the judges. **Neither is forked per target** — a PASS
means the same thing on both, which is the whole reason they live in one repo. See
[webforge](#webforge--figma--the-nextjs-site) below.

## What an agent can do — two modes

Lightfunnels treats a permanent **app token** differently from a temporary
**browser session token** (both verified live). The bridge uses each for what
it's good at:

| Goal | App token (`.env`) | Session token (`--session`) |
|---|---|---|
| List / read funnels & page copy | ✅ | ✅ |
| Rename, slug, publish, delete | ✅ | ✅ |
| Create a funnel with real pages (`duplicate`) | ✅ | ✅ |
| **Edit page copy for real** (saved to the page, shows in editor) | ❌ | ✅ |
| Add a new page (`createStep`) | ❌ | ✅ |
| Edit copy render-time only (`header_scripts` patch) | ✅ | ✅ |

App tokens are blocked from writing page bodies
(`non_allowed_app_funnel_update`) — that's a platform rule for third-party
apps. A **session token** (copied from the LF dashboard's own network requests)
is not an app, so it writes real page bodies — the same access the LF editor
has. This is how AI page-studio apps like Pixelier work: they use your login
session. Trade-off: session tokens expire; the app token is permanent.

So: app token for structure (duplicate/publish/rename), `--session` for real
copy edits. The old render-time `header_scripts` patch is still there as a
no-session fallback (inspectable via `patch`, reversible via `patch-clear`), but
it only shows on the live page, not in the editor.

## Setup

The bridge itself is **dependency-free** — standard library only:

```bash
python3 get_token.py --client-id <ID> --client-secret <SECRET>   # one-time OAuth → .env
python3 lf.py funnels                                            # smoke test
```

The **judges** are not: they drive a real browser and compare real pixels. Needed for
`qa_runner.py`, `design_diff.py` and anything under `webforge/`:

```bash
pip3 install -r requirements.txt
python3 -m playwright install chromium      # ~130 MB, one time
```

Both are imported lazily, so `lf.py` keeps working with neither installed. Verified on
Python 3.9.6, Node 22, npm 10.

Run everything from the project root. The scripts resolve `.env` and the session
files next to themselves (at the repo root), so cwd doesn't matter — except for
the ad-hoc `build_*.py` / `figma_rest.py` scripts, which read them from the
current directory (`cd` to the repo root first).

Get `client_id`/`client_secret` from a [Partners area](https://partners.lightfunnels.com/)
app (Configurations tab). The token is permanent — keep `.env` out of git.

### Session token (only needed for real page-copy edits)

1. Log into `app.lightfunnels.com`, open DevTools → **Network** → filter **Fetch/XHR**.
2. Click around (e.g. open Funnels) so a request to `services.lightfunnels.com/api/v2` appears.
3. Open that request → **Headers** → copy the value after `Authorization: bearer `,
   and note the `account-id` header.
4. Save it locally (never commit): `echo 'PASTE_TOKEN' > .session_token`
5. Use it: `python3 lf.py edit <funnel_id> --session --account-id <ACCT> --replace "old==new"`

Session tokens expire — if `--session` starts failing with auth errors, re-grab it.

## Usage

```bash
python3 lf.py duplicate fun_XXXX --name "Sleep V3" --slug sleep-v3   # new variant
python3 lf.py publish <new_id> --off                                 # dups inherit published!
python3 lf.py texts <new_id>                                         # read the copy
python3 lf.py edit <new_id> --replace "Old headline==New headline"   # change it
python3 lf.py publish <new_id>                                       # go live
```

Run `python3 lf.py --help` for all commands.

## webforge — Figma → the Next.js site

`webforge/` builds a Figma design into a route in the **storefront repo**, cloned
separately at `~/hlth-site`. It is **local-first**: nothing deploys, and nothing is
pushed unless you say so.

📖 **Setup and the full workflow: [`webforge/README.md`](webforge/README.md)** — clone the
site as a sibling, install the browser the judges drive, capture both breakpoints, build,
check, push. What follows here is the short version.

### Why it is not its own repo

Measured rather than assumed: ~80% of the QA machinery is target-agnostic. Redirects,
links, meta tags, viewports, console errors, accessibility and the entire design-fidelity
diff take a URL and know nothing about what served it. A fork would drift, and "matches
the design" would quietly come to mean two different things.

So `webforge/qa/web_qa.py` **imports** `pagescore/qa_runner.py` rather than copying it,
and shells out to `pagescore/design_diff.py`. It owns only what genuinely differs when
the target is a dev server:

- **PageSpeed cannot fetch localhost** — Google fetches from their own servers, so speed
  is a deploy-time check and `--skip-psi` is forced.
- **A dev server has to be up** — it waits for it, and says so plainly rather than
  reporting a page defect.
- **Dev-only noise is not a defect** — HMR sockets, react-refresh, the Next dev overlay
  and the site's own `/api/collect` beacon all abort by design.
- **A dev build is not what ships** — `--prod` builds and serves the production output.

### The one command

```bash
python3 webforge/qa/web_qa.py /blog/template/email-exclusive \
  --project ~/hlth-site \
  --frames webforge/runs/<run-id>/frames.json
```

That runs the runbook, then the fidelity diff **once per breakpoint**, and writes
`pagescore/runs/<run-id>/todo.md` — every failure, merged, in one list. **A clean runbook
does not pass the run:** if the page does not match the design, the run fails. "Loads
fine, scores well, wrong layout" is the state this exists to prevent.

### The three files a run needs

`frames.json` — every breakpoint the design draws, so one cannot be left off a command
line:

```json
{
  "page": "/blog/template/email-exclusive",
  "frames": [
    { "node": "271:169", "label": "mobile",  "width": 390,
      "spec": "webforge/runs/emailx-mobile-001/design.json",
      "crops": "webforge/runs/emailx-mobile-001/crops",
      "accept": "webforge/runs/emailx-mobile-001/accepted.json" },
    { "node": "271:15",  "label": "desktop", "width": 1440,
      "spec": "webforge/runs/emailx-001/design-full.json",
      "crops": "webforge/runs/emailx-001/crops",
      "accept": "webforge/runs/emailx-mobile-001/accepted.json" }
  ]
}
```

`crops/` — the design's own node renders, `<node-id>.png`. **Without these, photos are
checked for box and aspect but not for what they actually show**, which is how a page
ships with every box correct and three photos showing the wrong part of themselves:

```
figwright save_screenshots  nodeIds=[<every Photo / image node>]  scale=3
                            outDir=webforge/runs/<run-id>/crops
```

`accepted.json` — deviations that are **decisions, not defects**, keyed by Figma node id
with the reason. The Trustpilot figures on `email-exclusive` are read live via
`getTrustpilot()`, so they will never match the frame's hardcoded ones; that is recorded
here rather than reported forever. A judge that raises a settled question every run gets
ignored.

### What the fidelity judge checks

| | |
|---|---|
| Copy | every TEXT node, verbatim |
| Type | size, weight, colour, **family**, and line count |
| Boxes | width of FILL nodes, background, corner radius, border |
| Spacing | gap to the previous sibling, and between containers |
| Photos | loaded, aspect ratio, and the **actual crop** against the node render |

**Not checked, and still your eyes:** letter-spacing, text-align, shadows, hover and
focus states, animation. Look at a screenshot before calling a page done — three photos
once rendered blank while every automated gate was green.

Thresholds are calibrated against real before/after, not guessed. `IMG_PIXEL_TOL` is
`0.05`: a correct crop measures 0.001–0.002, one a human flagged measures 0.055–0.264.

### Gates in `~/hlth-site`

There is **no test runner**. Two commands are the entire safety net, and both must exit 0:

```bash
npx tsc --noEmit
npm run lint
```

### Not wired up

- **`webforge/src/harness/*.ts`** — a state machine that would drive the build end to end.
  It shells out to the `claude` CLI, which is **not on PATH**, so the `GENERATE_CODE`
  stage cannot run. The build is done by the agent under
  `.claude/skills/page-pipeline/SKILL.md` instead; the harness is scaffolding for later.
- **`deploy:preview` / `deploy:prod`** in `webforge/package.json` — Vercel is not in use.
  `.claude/rules/vercel-deployment.md` is the plan for when it is, and says so at the top.

## For the agentic coder

- **Claude Code**: the `lightfunnels` skill (`.claude/skills/lightfunnels/SKILL.md`)
  loads automatically when you ask for funnel work.
- **Other agents**: point them at `AGENT.md`.

## Layout

The bridge itself lives at the repo root; everything built on top of it is
grouped into its own directory. See `docs/ARCHITECTURE.md` for the full map.

- `requirements.txt` — the two dependencies the judges need (the bridge needs none)
- `webforge/README.md` — **setup + full workflow for the Next.js target**
- `lf.py` — agent-facing CLI (all commands, JSON output)
- `lf_api.py` — GraphQL client + primitives (duplicate, text extraction, patch engine)
- `lf_session.py` — keeps a browser session alive for page-body writes
- `get_token.py` — one-command OAuth flow → `.env`
- `server.py` — legacy HTTP wrapper around the bridge (see `legacy/`)
- `docs/LIGHTFUNNELS_API.md` — full API knowledge base + **Field-Verified Addendum**
  (platform limits, undocumented mutations, quirks found by live testing)
- `docs/ARCHITECTURE.md` — map of every subsystem in this repo
- `.claude/skills/lightfunnels/references/PRODUCT_PRICE.md` — our product's
  price in the visitor's currency, live from Shopify (`data-price`):
  **exact, matches checkout**. Tagging, install, QA per market
- `.claude/skills/lightfunnels/references/CURRENCY_CONVERTER.md` — converting
  any *other* GBP figure (`data-fx-gbp`): competitor prices, editorial sums.
  **Mid-market, indicative only** — never our own price
- `.claude/skills/lightfunnels/SKILL.md` — the Claude Code skill
- `funnels/` — local funnel workspaces (funnel.json, NOTES.md, steps/, texts/,
  edits/); see `funnels/README.md`
- `templates/` — archived page bodies (`capture` output; read-only reference)
- `legacy/` — the old HTTP-server bridge (its write path predates the platform
  restriction and does not work)
- `pagescore/` — the runbook and the judges, shared by both targets. `program.md` is the
  runbook; `qa_runner.py` runs it mechanically; `design_diff.py` proves a page matches its
  Figma frame; `benchmark.py` is the PSI/CWV ground truth; `deploy_guard.py` refuses
  writes to live published slugs; `build_*.py` are the Lightfunnels builders. Run from the
  repo root, e.g. `python3 pagescore/benchmark.py <url>`
- `webforge/` — the Next.js target: `qa/web_qa.py` (the local QA entry point),
  `scripts/figma_spec.py` (flattens a figwright dump into the properties that map onto
  Tailwind), `runs/<id>/` (design dumps, node crops, manifests), and `src/harness/`
  (not wired up — see above)
- `.claude/rules/` — how to build for `hlth-site`: `figma-to-tailwind.md`,
  `design-tokens.md`, `component-architecture.md`, `vercel-deployment.md`
- `notes/` — an Obsidian vault: one note per session and per page, wikilinked
- `content/` — scraped source material (`extract_techunboxed.py` +
  `extracted/`) used as raw copy/structure input when building new pages
- `autoresearch/` — an unrelated external reference project (its own git repo)
  that `pagescore/program.md`'s autonomous-loop design is modeled on
