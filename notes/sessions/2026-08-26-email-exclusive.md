---
categories:
  - "[[Web-Tech]]"
subjects:
  - "[[Lightfunnels]]"
focus_area: Figma 271:15 built into hlth-site, local only
page: "[[email-exclusive]]"
status: done
created: 2026-08-26
commit: f89cf37
run_id: emailx-webqa
tags:
  - webforge
  - figma
  - nextjs
---

# 2026-08-26 — Figma 271:15 built into hlth-site, local only

Page: [[email-exclusive]] · Index: [[LF Page Pipeline]]

**Result:** 1 PASS, 0 FLAG, 0 FAIL

## What was built

Figma frame `271:15` ("Email Exclusive · Article · 1440w", 8293px tall) as
`components/figma/EmailExclusiveArticle.tsx` plus the route at
`app/[locale]/pages/email-exclusive/page.tsx`. Seven images exported and converted to
webp: **5.8 MB → 0.58 MB**.

Nothing was deployed, nothing pushed, no git command run.

## Result

| Check | Result |
|---|---|
| Design fidelity | **73/73 exact** — 0 missing, 0 retyped, 0 restyled |
| `npx tsc --noEmit` | clean |
| `npm run lint` | clean |
| Runbook (structural) | **PASS** on every phase |
| Live height | 8255px vs the frame's 8293px |

Speed is unmeasured: PageSpeed fetches from Google's servers and cannot reach
localhost. That is a deploy-time check.

## What reading the codebase first prevented

Three assumptions from the earlier rules were wrong and would have produced a broken
or badly-fitting component:

- **No `src/` directory.** Code is at `components/`, `app/`, `lib/`.
- **No shadcn/ui**, no `tailwind.config.ts`. Tailwind v4, CSS-first, with `hlth-*`
  brand tokens in an `@theme` block.
- **A blanket "no hardcoded hex" rule was wrong here.** The codebase has ~1,536
  arbitrary hex utilities against ~439 token uses, across 245 of 386 files. Banning hex
  would have made the component look nothing like its neighbours. The rule became a
  decision ladder instead: token if one exists, lowercase arbitrary utility for the
  fourteen de facto colours, stop and flag anything genuinely new. All seven colours in
  this design already existed in the codebase.

## The bug that only showed up on screen

Every gate passed while **three photos and the product panel rendered blank.**

`next.config.ts` installs a custom Shopify-CDN image loader that applies to every
`next/image` on the site, and it does not implement `width` for non-Shopify sources —
so a local `/public` asset silently renders at 0×0. No HTTP error, no console error,
nothing in the build. The repo already knows this: `HeroV3`, `HypeListicleHero` and the
footer wordmark all use a raw `<img>` with a file-level
`eslint-disable @next/next/no-img-element` and a stated reason. Switched to that
pattern and all 8 images render.

**Measurements passing is not the same as the page being right.** Looking at the
screenshot is what caught it.

## Judge fixes this run

Four real defects in the harness, all found by running it against something new:

1. **Crashed on relative hrefs.** Every Lightfunnels page emitted absolute URLs, so
   `/products/hlth-band` raised "unknown url type" and took the whole run down.
2. **Broken images were invisible.** The alt-text audit filtered on
   `naturalWidth > 40`, so a blank image was skipped rather than reported — the page
   passed "alt text present" with three blank photos on it.
3. **Screenshots outran lazy loading.** A 60ms scroll step meant the shot came back
   with blank images and the report claimed a defect the page did not have.
4. **Decorative glyphs counted as copy.** A `✓` in a bullet and `★` in a rating strip
   are icons drawn as text; comparing them reported a defect on every correct build.

## webforge has its own QA entry point now

`webforge/qa/web_qa.py`. It does **not** fork the runbook — `program.md` stays the
standard and `qa_runner.py` stays the judge, so a PASS here means what a PASS on a
Lightfunnels page means. It only owns what genuinely differs locally: waiting for the
dev server and saying so when it never comes up (rather than reporting a page defect),
filtering dev-only chatter, forcing `--skip-psi` because PSI cannot reach localhost,
and a `--prod` mode that builds and serves the production output.

## Measured (emailx-webqa)

| Page | Verdict | Speed | Links | Meta | Mobile | Console | A11y |
|---|---|---|---|---|---|---|---|
| email-exclusive | **PASS** | SKIP | PASS | PASS | PASS | PASS | PASS |

Full findings: `pagescore/runs/emailx-webqa/findings.json`


## Needs a human answer

- [ ] Headings: the Figma nodes are named 'set family to Delight Semi Bold' but the frame has Poppins applied. I used .font-display (Delight). Confirm?
- [ ] Trustpilot says 4.5/5 in the design; TrustpilotStars' docstring says 4.6 and the last commit reads the score live. Which is right here?
- [ ] Should /pages/email-exclusive be indexable? Its four sibling advertorials are, but this one is a subscriber-only discount and would compete with the PDP.

## Next

- [ ] Wire the CTA to the real 15% discount, and decide whether the price should come from Shopify rather than the design

---

Written by `pagescore/session_note.py`. Runbook `pagescore/program.md`.
