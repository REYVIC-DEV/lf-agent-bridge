# webforge — Figma → a route in the Next.js site

The second target in this repo. Same designs, same judges as the Lightfunnels side; the
page lands in the **storefront repo** instead of in a funnel.

**Local-first by design.** Nothing deploys. Nothing is pushed unless you say so. The
whole loop runs against a dev server on your own machine.

---

## Setup (once)

### 1. Python dependencies

The bridge is dependency-free, but the judges drive a real browser and compare real
pixels:

```bash
cd lf-agent-bridge
pip3 install -r requirements.txt
python3 -m playwright install chromium      # ~130 MB, one time
```

Verified on **Python 3.9.6** with playwright 1.60 and Pillow 11.3.

### 2. The site repo, as a SIBLING of this one

```bash
cd ~
git clone https://github.com/hlthtrack/hlth-shopify-frontend.git hlth-site
cd hlth-site
git checkout staging          # NOT main — main is what production tracks
npm install
```

⚠️ **Clone it beside this repo, not inside it.** A repo inside a repo becomes a gitlink
(mode `160000`) and git will neither track its contents nor ignore it cleanly. If you do
put it under `webforge/`, `webforge/.gitignore` already blocks `site/` and `sites/` to
limit the damage — but a sibling is still correct.

The default path everything assumes is `~/hlth-site`. Anywhere else, pass `--project`.

Node 22 and npm 10 are what this was verified against.

### 3. Environment for the site

The site needs its own env file (Shopify, Appstle, Trustoo, Supabase). Ask whoever
maintains the storefront — **do not** invent one, and do not commit it.

> ⚠️ Check the site's ignore rules cover it before you ever stage anything there:
> `git check-ignore -v <the env file>`. A pattern like `.env*` does not match a filename
> without a leading dot, and a `git add -A` would then commit live credentials.
> **Always stage explicit paths in the site repo.**

### 4. Figma, via Figwright

Open the **Figma desktop app**, open the file, run **Plugins → Development → Figwright**,
and leave it connected. There is **no Figma API key and no Figma MCP** in this project —
figwright reads whatever file you have open, through the Plugin API, with no seat call
limit.

### 5. Check it works

```bash
cd lf-agent-bridge
python3 webforge/qa/web_qa.py /blog/template/article-template --project ~/hlth-site
```

It should start the dev server, run the runbook, and print a verdict. No `--frames` means
no fidelity diff — that is expected here; this is just proving the plumbing.

---

## The loop

```
ask the route → BUILD → QA → FIX → QA → session note → you look → offer the push
                        ↑______________|                                ↓
                         max 2 fix cycles                      staging, on a yes
```

Two steps are yours, not the agent's: **the route** at the start and **the push** at the
end.

### Step 1 — Settle the route first

The agent will ask, and it should: the design cannot tell it, because it is not a design
question. On `hlth-site`:

| Destination | Indexable | On `hlthtrack.com` | For |
|---|---|---|---|
| `app/[locale]/blog/template/<name>/` | `noindex, nofollow` | **404s** | reusable article / advertorial layouts |
| `app/[locale]/pages/<name>/` | indexable, `alternatesFor()` | serves | live campaign pages |
| top level (`cart`, `learn`, …) | indexable | serves | functional site areas |

⚠️ **`/blog/template/*` 404s on the production domain** — `proxy.ts` rewrites it, keyed on
the same predicate as robots/noindex. That is the guard working, but it also means **you
cannot send email or ad traffic there.** Promote the page first;
`.claude/rules/component-architecture.md` has the five-step checklist.

### Step 2 — Capture the design, every breakpoint

A desktop frame and a mobile frame are **two designs**, not one that reflows. Each needs
its own dump and its own node renders.

```
figwright get_node          nodeId=<frame id>            # → save to runs/<id>/design.json
figwright save_screenshots  nodeIds=[<Photo nodes>] scale=3 outDir=runs/<id>/crops
```

Then flatten the dump into something you can build from without ever reading a value off
a screenshot:

```bash
python3 webforge/scripts/figma_spec.py runs/<id>/design.json --out runs/<id>/spec.json
```

⚠️ **Photos are not a CSS problem.** The two frames routinely crop the same photograph
differently, and `object-cover` on the desktop asset cannot reach the mobile crop — it
centre-crops, and the design did not. Export each node's own render and art-direct with
`<picture>`. Without `crops/`, a photo is checked for box and aspect but **not for what it
actually shows**, which is how a page ships with every box correct and three photos
showing the wrong part of themselves.

### Step 3 — Write the manifest

`runs/<id>/frames.json` — so a breakpoint cannot be left off a command line:

```json
{
  "page": "/blog/template/email-exclusive",
  "project": "~/hlth-site",
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

`accepted.json` is optional — `{ "<figma-node-id>": "why" }` for deviations that are
**decisions, not defects**. On `email-exclusive` the Trustpilot figures are read live via
`getTrustpilot()`, so they will never match the frame's hardcoded ones. Recording that
stops it being reported forever; a judge that raises a settled question every run gets
ignored.

### Step 4 — Build

Read values off the dump, never off a screenshot. The mapping is mechanical and lives in
`.claude/rules/`:

| | |
|---|---|
| `figma-to-tailwind.md` | auto-layout → flex, spacing, sizing, type, responsive |
| `design-tokens.md` | the real colour situation — the token system is *not* the dominant practice |
| `component-architecture.md` | where files go, the v2/v3 split, what to reuse instead of rewriting |

**Mobile values are the base; desktop goes behind `md:`.** Never let a desktop-only value
be the base — that is how a layout breaks on phones, which is where the traffic is.

### Step 5 — Run the judge

```bash
python3 webforge/qa/web_qa.py /blog/template/email-exclusive \
  --project ~/hlth-site \
  --frames webforge/runs/<id>/frames.json
```

Writes `pagescore/runs/<run-id>/todo.md` — every failure across every breakpoint, in one
list. **A clean runbook does not pass the run:** if the page does not match the design,
the run fails.

Useful flags: `--prod` (build and serve production output), `--no-serve` (a server is
already running), `--port`, `--run-id`, and `--design SPEC@WIDTH` / `--crops` / `--accept`
if you would rather spell out breakpoints than use a manifest.

### Step 6 — The site's own gates

There is **no test runner**. Two commands are the entire safety net, and both must exit 0:

```bash
cd ~/hlth-site && npx tsc --noEmit && npm run lint
```

### Step 7 — Look at it yourself

Open `http://localhost:3000<route>`. Resize narrow for mobile.

**Do this even when everything passed.** Three photos once rendered blank while every
automated gate was green — only the screenshot caught it. And the checks compare the page
to the drawing; they cannot tell you the drawing was right for the campaign.

### Step 8 — The push, offered not taken

Once you say the page is right, the agent asks whether to push to `staging`. It does not
push on its own, and "the page looks good" is not read as "push it" — those are two
separate answers. Never `main`.

---

## What the fidelity judge covers

| | |
|---|---|
| Copy | every TEXT node, verbatim — missing, and retyped-not-copied |
| Type | size, weight, colour, **family**, and line count |
| Boxes | width of FILL nodes, background, corner radius, border |
| Spacing | gap to the previous sibling, and between containers |
| Photos | loaded, aspect ratio, and the **actual crop** vs the node render |

Plus the whole runbook: redirects, links, meta and social tags, four viewports, console
errors, page weight, accessibility.

**Not covered, and still your eyes:** letter-spacing, text-align, shadows, hover and
focus states, animation — and whether the page is *right*, as opposed to faithful.

Thresholds are calibrated against measured before/after, not guessed. `IMG_PIXEL_TOL` is
`0.05`: a correct crop measures 0.001–0.002, one a human flagged measures 0.055–0.264.

---

## Why this is not its own repo

Measured, not assumed: ~80% of the QA machinery takes a URL and knows nothing about what
served it. So `qa/web_qa.py` **imports** `pagescore/qa_runner.py` and shells out to
`pagescore/design_diff.py` rather than forking either. It owns only the genuine local
differences:

- **PageSpeed cannot fetch localhost** — Google fetches from their own servers, so
  `--skip-psi` is forced and speed is a deploy-time check.
- **A dev server has to be up** — it waits, and says so plainly rather than reporting a
  page defect.
- **Dev-only noise is not a defect** — HMR sockets, react-refresh, the dev overlay and the
  site's own `/api/collect` beacon all abort by design.
- **A dev build is not what ships** — hence `--prod`.

Two forked copies of a 700-line judge would drift until a PASS meant two different things.

---

## Files

| | |
|---|---|
| `qa/web_qa.py` | the QA entry point |
| `scripts/figma_spec.py` | figwright dump → the properties that map onto Tailwind |
| `runs/<id>/` | per-run evidence: dump, `crops/`, `frames.json`, `accepted.json`. **Gitignored** |
| `CLAUDE.md`, `RULES.md`, `CONTEXT.md`, `MEMORY.md`, `PROGRESS.md` | the harness's own context files |
| `src/harness/*.ts` | **not wired up** — see below |

### Not wired up

- **`src/harness/harness.ts` + `state-machine.ts`.** A state machine intended to drive the
  build end to end. It shells out to the `claude` CLI, which is not on PATH here, so the
  `GENERATE_CODE` stage cannot run. The build is driven by
  `.claude/skills/page-pipeline/SKILL.md` instead. The harness is scaffolding for later,
  kept because the stage model is right even though it cannot execute.
- **`deploy:preview` / `deploy:prod`** in `package.json`. Vercel is **not in use**.
  `.claude/rules/vercel-deployment.md` is the plan for when it is, and says so at the top.

---

## Troubleshooting

| Problem | Cause / fix |
|---|---|
| `ERR_CONNECTION_RESET`, or the run hangs on "serving" | Two dev servers fighting over the port. `lsof -ti:3000 \| xargs kill -9`, then rerun. |
| Images reported "did not load" or as the wrong file | Sampled before decode on a cold server. The judge waits for `document.images.every(complete)`; if it still happens, the server is unusually slow — rerun. |
| Fidelity fails but the page looks right | Read `todo.md`. Usually the frames disagree with each other, and that is a question for a human, not a defect. |
| A finding recurs and is intentional | Add it to `accepted.json` with the reason. |
| A photo passes box and aspect but looks wrong | You are running without `--crops`. Export the node renders. |
| `figwright` tools error | The Figma desktop app must be open with the plugin running. `figwright ping` reports it. |
| `get_node` output "exceeds maximum allowed tokens" | Expected on a big frame — it is written to a file. Process it with `scripts/figma_spec.py`; never paste it into context. |
