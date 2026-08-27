---
name: page-pipeline
description: Build a Lightfunnels page from a Figma design and take it to shippable — Build → QA → Fix → QA → Done — using the lf-builder, lf-qa and lf-fixer agents and the pagescore/program.md runbook. Use when the user gives a Figma design to turn into a page, or asks to QA and fix existing live pages.
---

# Figma → live page, end to end

```
 ask the route → BUILD → QA → FIX → QA → session note → human looks → offer the push
                          ↑______________|                                    ↓
                           max 2 fix cycles                            staging, on a yes
```

Two of those steps are the human's, not yours: **the route** at the start and **the
push** at the end. Everything between is yours to run.

The judge is `pagescore/program.md` plus `pagescore/qa_runner.py`, and it does not change
between cycles — so "better" means better against the same yardstick, not a moved
goalpost. Same split as `benchmark.py` versus the builders: **what measures is never
what changes.**

## What the human says, and what they need ready

> "Build the *Ranked Comparison* frame into funnel `fun_xxx` as `top-5-v4`, then run the
> runbook on it."

They need exactly one thing open: **Figma, with the Figwright plugin running**
(Plugins → Development → Figwright, shows *Connected*). Everything else is yours.

If the funnel or slug is missing from the request, ask for them — those two are the only
decisions that cannot be inferred safely.

## Preflight — all of it, before stage 1

```bash
python3 pagescore/deploy_guard.py <funnel_id> <slug>   # is the target already live?
python3 lf.py funnels >/dev/null && echo "bridge ok"    # app token valid
grep -q PSI_API_KEY .env && echo "psi key present"      # else QA runs --skip-psi
```

Then `mcp__figwright__ping`. If it fails, the human must act — the file has to be open
with the plugin running. **Never fall back to the Figma MCP connector or the REST API**;
both are retired here and rate-limited to the point of stalling a build halfway. Say what
is needed and stop.

**Load the `lightfunnels` skill yourself, and instruct each agent to load it too.** It is
the contract for every write: the two auth modes and which one can actually write a page
body, the create-a-step recipe, cache behaviour, token hygiene. Building without it burns
a cycle on a platform refusal that looks like a permissions bug and is not.

### Settle the redeploy authorisation now, not mid-loop

The builder creates a new slug inside a **published** funnel, so the page is live the
moment it exists. The fixer then has to redeploy that same slug on every fix cycle — and
the guard will block it, correctly, every time.

So ask the human once, up front, naming the page:

> "The fixer will need to redeploy `top-5-v4` during the loop. Authorise that one page?"

Then scope it to that slug and nothing else:

```bash
LF_ALLOW_REDEPLOY=top-5-v4 python3 pagescore/build_top5_v4.py
```

Never widen it to `LF_ALLOW_REDEPLOY=1`, and never set it without being asked. If a
finding turns out to need a *different* page changed, stop and ask again.

## Stage 1 — BUILD

Delegate to **`lf-builder`** with: the Figma file and frame, the funnel id, the new slug,
the closest existing builder to model on, the run id, and an explicit instruction to load
the `lightfunnels` skill first.

It measures the frame node by node through figwright, copies text verbatim, and produces
`pagescore/build_<name>.py`. It ships the standing requirements as part of the build, not
as polish: one `h1`, full `settings.seo` with a 1200×630 social image, `twitter:*` tags,
`alt` on every content image, the font-preload + `InterFallback` block, no `href="#"`,
`overflow-wrap: anywhere` on rich text.

It saves the frame dump to `pagescore/runs/<run-id>/design.json` — **stage 2 cannot check
fidelity without it.**

**Ask for the route before writing a line.** Not after the build, not in the summary.
The design does not say where the page goes, because it is not a design question — it is
a question about what the page is for. On hlth-site the destinations differ in whether
the page is indexable and whether it is reachable on the production domain at all, so
guessing either publishes something private or hides something meant to take traffic.
This has been got wrong twice on one page. The table of destinations is in
`.claude/rules/component-architecture.md`; it is there to act on an answer, not to infer
one.

If no answer comes, build the component and stop at the route. The component is identical
either way, so waiting costs nothing and leaves nothing to undo.

**Where to build so QA can reach it.** The runbook measures a live URL; PSI fetches the
page from Google's servers and `?preview=true` is not a substitute (the preview banner
inflates CLS and that URL caches hardest). So the default is **a new slug in a funnel
that is already published** — reachable immediately, nothing existing touched, guard
enforced.

If the design must be its own brand-new funnel, that funnel starts unpublished and the
page is unreachable, so QA cannot run. Say so and let the human choose: publish the new
funnel (no existing traffic is at risk), or build into a published funnel and move it
later. Never QA a preview URL and report the numbers as production.

**Gate:** the page returns 200 at its real URL.

## Stage 2 — QA

Delegate to **`lf-qa`**. It is read-only against production.

**Scope it to the one page you just built.** Name the URL explicitly in the task. The
agent will not fan out on its own, but do not invite it to — a funnel's other steps are
not under review, and each extra page costs roughly 80 seconds of PSI time for a result
nobody asked for.

```bash
python3 pagescore/qa_runner.py <url> --run-id <run-id>
python3 pagescore/design_diff.py pagescore/runs/<run-id>/design.json <url> \
  --viewport 390 --mobile --crops pagescore/runs/<run-id>/crops \
  --out pagescore/runs/<run-id>
```

For a locally-served build, one command covers every breakpoint:

```bash
python3 webforge/qa/web_qa.py <route> --frames webforge/runs/<run-id>/frames.json
```

`frames.json` names each breakpoint the design draws, its Figma node, its dump and its
crops — so a breakpoint cannot be left off a command line. The run writes
**`pagescore/runs/<run-id>/todo.md`**: every runbook FAIL, every copy and typography
delta, every wrong photo and every wrong gap, merged across breakpoints into one list.
That file is the handoff to stage 3; nothing else has to be read.

**Once per breakpoint, and always with `--crops`.** A design with a desktop frame and a
mobile frame is two designs, and a diff run only at 1440 says nothing about the layout
most of the traffic sees. `--crops` is a directory of the design's own node renders:

```
figwright save_screenshots  nodeIds=[<every Photo / image node>]  scale=3
                            outDir=pagescore/runs/<run-id>/crops
```

Without it, photos are compared for box and aspect only — which is exactly how a page
ships with every box correct and three photos showing the wrong part of themselves.
Copy, type and geometry can all be right while the picture is wrong.

The harness decides phases 0, 1, 2, 3, 4, 6 and accessibility. The agent adds phase 5
congruency — prices that must agree, headline arithmetic that must reconstruct, link
labels that must match their destinations, claims that must not contradict the page's own
disclaimer — and judges whether the social image is actually on-message.

**Gate:** read `todo.md` (or `findings.json` on Lightfunnels). Any **FAIL** goes to
stage 3. **FLAG**s are a judgment call — fix what is cheap, carry the rest into the
session note.

A clean runbook is not a pass. `web_qa.py` fails the run when the page does not match
the design, because "loads fine, scores well, wrong layout" is the exact state this
pipeline exists to prevent.

### What the fidelity judge covers, so you know what it does not

| | |
|---|---|
| Copy, verbatim | every TEXT node |
| Type | size, weight, colour, **family**, and line count |
| Boxes | width of FILL nodes, background, radius, border |
| Spacing | gap to the previous sibling, and between containers |
| Photos | loaded, aspect, and the **actual crop** vs the node render |

Not covered, and still a human's eye: letter-spacing, text-align, shadows, hover and
focus states, animation, and anything below the fold of a state the crawler never
reaches. Look at a screenshot before calling a page done — three photos once rendered
blank while every automated gate was green.

## Stage 3 — FIX

Delegate to **`lf-fixer`** with the QA handoff, the scoped `LF_ALLOW_REDEPLOY` value, and
the same instruction to load the `lightfunnels` skill first.

It edits builders, never the LF editor, batches by template, deploys one template at a
time, and confirms 200 after each write.

**It may not invent facts.** Prices, ratings, health claims, discounts and headline
numbers belong to the client. When a finding needs one, the fixer collects the question,
finishes everything else, and hands the list back. A guessed price on a live advertorial
is worse than a flagged one.

## Stage 4 — QA again

Same command, `--run-id <run-id>-v2`, plus `--after-publish`.

That flag matters: publishing purges the storefront cache, so PSI's first read after a
deploy under-reports by roughly 20 points and replays one cached analysis on rapid
repeats. A score that drops right after a deploy is usually the cache. Warm it, wait,
re-measure — then decide whether it is a regression.

Diff the two `findings.json` files and state what actually changed.

## Stop conditions

Stop and hand back when any of these is true. Do not keep cycling.

1. **Clean** — no FAIL, remaining FLAGs accepted. → DONE.
2. **Two fix cycles done** and FAILs remain. Something structural is wrong and a third
   pass will not find it.
3. **Blocked on facts** — everything left needs a number or an approval only a human has.
4. **A deploy broke the page** — a 503, or a verdict that got worse. Stop immediately,
   say what changed, and do not deploy again until it is understood.

**Never report DONE while a FAIL is open.** Name the failures and why they stand.

## Stage 5 — the session note, always

Even when the run failed. A blocked session with its questions written down is what makes
the next one fast.

```bash
python3 pagescore/session_note.py \
  --slug <page-slug> --title "<what this session was>" \
  --run-id <run-id> --url <url> --builder pagescore/build_<name>.py \
  --funnel <funnel_id> --status done|in-progress|blocked \
  --question "<something only a human can answer>" \
  --next "<the obvious next step>" \
  --body - <<'MD'
## What happened
## What changed
## What it found
## What is still open
MD
```

Writes into `notes/` — an Obsidian vault inside the repo. Creates
`notes/sessions/<date>-<slug>.md`, keeps `notes/pages/<slug>.md` with the page's full run
history, and links both from `notes/LF Page Pipeline.md`. Verdicts come straight out of
`findings.json`, so a note cannot claim something that was not measured.

## Stage 6 — offer the push, never take it

Once the page is clean and **the human has said it looks right**, ask one question:

> The page is passing. Push these changes to `staging`?

Ask it; do not act on it. A push is outward-facing and someone else's branch — the
approval has to be for this push, not inherited from approving the page. Silence is not a
yes, and "the page looks good" is not a yes either: it approves the page, not publishing
it.

**Do not offer it before the human has looked.** A green run means the checks passed, not
that the page is right — the judge does not read letter-spacing, hover states, or whether
the offer is the one anyone agreed to. Stage 6 comes after a human's eye, not instead of
one.

### Before pushing, in this order

**1. Stage explicit paths. Never `git add -A`, never `git add .`**

The site repo carries at least one untracked env file whose name does **not** match its
`.gitignore` pattern — `.env*` misses a filename with no leading dot — so a blanket add
commits live credentials. This is not hypothetical; check it each time:

```bash
git status --short | grep -iE 'env|secret|token|\.key$|credential'
```

Anything that lists, verify with `git check-ignore -v <file>` and fix the ignore rule
**before** staging anything. Then name every path explicitly:

```bash
git add app/[locale]/blog/template/email-exclusive components/email-exclusive \
        public/email-exclusive components/TrustpilotStars.tsx
git status --short          # read it; anything unexpected is a stop
```

**2. Confirm the branch.** `git status -sb` — expect `## staging...origin/staging`.
**Never push to `main`**; `origin/HEAD` points there and it is not ours to move. If the
branch is anything else, stop and ask.

**3. Show the human what will land** — `git diff --cached --stat` — before the push, not
after.

**4. Then push.**

```bash
git commit -m "<what the page is, and which Figma frames it came from>"
git push origin staging
```

### What does not go in the commit

Run artefacts. `pagescore/runs/*`, `webforge/runs/*` and the Figma dumps are evidence for
one run, not source — they belong to this repo, not the site's. The site commit is the
route, the component and the assets, and nothing else.

## When it goes wrong

| Symptom | What it actually is |
|---|---|
| `non_allowed_app_funnel_update` | App token cannot write page bodies. Use `--session`. Not a scope problem — do not retry. |
| Step created but the page does not render | `updateFunnel` was never called to attach it. The step exists detached. |
| Guard refuses to write | Working as designed. Build to a new slug, or get that one page authorised. |
| Page 503s after a deploy | A style prop the SSR rejects. Stop, revert that prop, deploy alone. See `block-schema.md`. |
| PSI score drops ~20 points right after a deploy | Cold cache. Warm the URL, wait, re-measure. |
| PSI returns identical numbers on rapid repeats | It is replaying one cached analysis. Wait longer. |
| figwright not responding | Human task — file open, plugin running. Never switch Figma paths. |
| Session token errors mid-run | `python3 lf.py refresh`, then `python3 lf.py login` if that fails. |
| Every check on a page is red | Check it is published and reachable first. |

## Running it unattended

Safe to leave alone **only** because of the guard. Keep all six:

- new slugs only, so nothing live is at risk
- redeploy authorisation scoped to one named page
- one template per deploy, verified at 200
- stop at two fix cycles
- never invent a fact — collect the question instead
- **stage 6 does not run unattended.** An unattended run ends at the session note. A push
  needs a human who has looked at the page and said so, and neither half of that can be
  supplied by the run itself.

Anything that would overwrite an unauthorised page, spend money, or state a number the
client has not confirmed stops and asks.
