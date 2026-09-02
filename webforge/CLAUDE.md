# webforge — Figma → Vercel

A self-contained Next.js project and the automation harness that drives it. It lives
inside the `lf-agent-bridge` repo so it can reuse that repo's QA judges, but it shares no
runtime code with the Lightfunnels side and does not affect it.

## Commands

```bash
# the whole pipeline, against your local site
npm run harness -- --project ~/hlth-site \
  --figma-url <url> --component-name <Name>

npm run harness -- ... --dry-run      # print every command, execute nothing
npm run harness -- ... --no-serve     # stop after the build
npm run harness -- ... --skip-qa      # build and serve, skip the QA gate
```

Local only. Nothing is deployed, nothing is pushed, and the harness runs no git command.

## The pipeline

```
INIT → FETCH_FIGMA → GENERATE_CODE → TYPE_CHECK → BUILD_PROJECT → LOCAL_PREVIEW
```

`src/harness/harness.ts` drives it, `src/harness/state-machine.ts` writes each
transition into `PROGRESS.md` as it happens.

`TYPE_CHECK` runs both `npx tsc --noEmit` and `npm run lint` — the target repo has no
test runner, so those two are its only automated gates. `LOCAL_PREVIEW` builds, serves
on localhost, and runs this repo's QA judges against that URL.

PageSpeed cannot reach `localhost` (Google fetches the URL from their own servers), so
the local gate is structural only: links, meta, four viewports, console errors,
accessibility, and the design-fidelity diff. Speed is a deploy-time check.

## Reading the design

**figwright only** (`mcp__figwright__*`). It reads the file the human has open in Figma
through the plugin and has no seat cap. The Figma MCP connector and the Figma REST API
are retired across this whole repo — both are per-seat rate limited to the point of
stalling a build halfway. If figwright will not connect, that is a human task: the file
must be open with Plugins → Development → Figwright running. Say so and stop; never
guess at a design because a tool was unavailable.

Measure, do not guess. Read the exact value from the node — font size, weight,
line-height, colour, padding, gap, radius, box size — and reproduce it. Never round a
measured value to a nearer Tailwind step, and never change a design value to make
content fit. Copy is verbatim, including punctuation and currency symbols.

## The target project

`~/hlth-site` (`hlth-shopify-frontend`) — **Next 16.2.4, React 19, Tailwind v4**, a
headless Shopify storefront. Its own `CLAUDE.md` is the authority on it and outranks
this file; read that first. It warns that this Next version has breaking changes versus
training data — read `node_modules/next/dist/docs/` before writing Next code.

There is **no `src/` directory**, **no shadcn/ui**, and **no `tailwind.config.ts`**.

## Component conventions

- **Generated components go in `components/figma/`** — one file per Figma frame, named
  for the frame.
- **Colours: `.claude/rules/design-tokens.md` is the authority — read it, do not
  paraphrase it here.** Short version: a token covers the fill → use the token; otherwise
  use the arbitrary utility (`bg-[#07060f]`), lowercase.
  ⚠️ Corrected 2026-09-02. This bullet used to read "Never a raw hex", which contradicted
  `design-tokens.md` in the same repo — that file measures ~439 token utilities against
  ~1,536 arbitrary-hex ones across 245 of 386 files and states plainly that "a blanket
  'never write a hex' rule is wrong here". Independently re-measured in `components/`
  before changing this: 1,567 arbitrary-hex classes against 189 `hlth-*` uses. Only six
  tokens exist, while the v3 and article designs use ~30 colours with no token, so the old
  rule forced either a wrong colour or ~30 invented tokens — and inventing tokens breaks
  hard rule 2. Never round a measured colour to a nearby token.
- **Fonts are the `.font-display` / `.font-body` utilities** — and they only resolve on
  the v3 route subtree. Read the font section of the site's `CLAUDE.md` before touching
  them; there are three documented traps there that have already cost real time.
- **Reuse what exists** — `Money`, `LocalizedLink`, `TrustpilotStars`,
  `PriorityFillImage`. Re-implementing one of those is wrong even if it renders.
- Server Components by default. `"use client"` only when the file actually needs state,
  effects, or browser APIs — and put it on the smallest component that needs it, not the
  page.
- ~~Compose classes with `cn()` from `src/lib/utils`.~~ ⚠️ **Removed 2026-09-02: there is
  no `cn()` helper and no `src/` directory in the target repo** — this file says so itself
  four lines above, so the rule contradicted its own page. Compose with a template literal
  or a ternary, the way the existing components do.
- **Images: plain `<img>` for content/editorial, `next/image` only for product imagery.**
  ⚠️ Corrected 2026-09-02 — "always `next/image`" is wrong here. The target repo sets
  `images.loader: 'custom'` with `lib/shopify-image-loader.ts` and **deliberately does not
  use Vercel's image optimizer**; content images are intentionally plain `<img>` carrying
  an `eslint-disable @next/next/no-img-element`. Follow the target repo's own convention
  block, which is the authority. `priority` still belongs on the LCP image only.
- `next/font` for fonts — it self-hosts and generates a metric-matched fallback, which
  removes font-swap layout shift at the source.
- Named exports. One component per file. Props typed with an explicit `interface`, no
  implicit `any`.

## Hard rules

Full list in `RULES.md`. The three that get broken most:

1. **Match the design's measured value exactly** — colour, size, spacing, radius. Use an
   `hlth-*` token where one exists, a raw hex where one does not (see the colours bullet
   above; this rule previously said "no hardcoded hex colours", which was wrong for this
   repo). Never round a measured value to a nearer Tailwind step, and never change a
   design value to make content fit.
2. **No parallel system** — no shadcn, no `tailwind.config.ts`, no second token set. This
   is also why you do NOT invent new colour tokens for one-off design values.
3. **`npx tsc --noEmit` and `npm run lint` must both be clean.**

## Reusing the repo's QA

The judges take a URL and know nothing about the platform behind it, so they work
unchanged here — same standard applied to a Vercel page and a Lightfunnels page, which is
the point:

```bash
python3 ../pagescore/qa_runner.py http://localhost:3000 --run-id <run-id> --skip-psi
python3 ../pagescore/design_diff.py <figma-dump.json> http://localhost:3000
```

The runbook itself is `../pagescore/program.md`.

## Execution memory

- `CONTEXT.md` — the active run: Figma URL, component, phase, error traces. Overwritten
  each run.
- `PROGRESS.md` — live checklist, written by the state machine.
- `MEMORY.md` — what carries across runs: recurring layout fixes, decisions, gotchas.
  Append here when something is learned; this is the file that makes the next run faster.
