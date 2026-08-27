---
categories:
  - "[[Web-Tech]]"
subjects:
  - "[[Lightfunnels]]"
focus_area: Mobile breakpoint for /pages/email-exclusive (Figma 271:169)
page: "[[email-exclusive-mobile]]"
status: in-progress
created: 2026-08-26
commit: f89cf37
run_id: emailx-mobile-001
tags:
  - webforge
  - hlth-site
  - responsive
  - figma
---

# 2026-08-26 — Mobile breakpoint for /pages/email-exclusive (Figma 271:169)

Page: [[email-exclusive-mobile]] · Index: [[LF Page Pipeline]]

**Result:** 1 PASS, 0 FLAG, 0 FAIL

## What happened

Built the mobile breakpoint of `/pages/email-exclusive` from Figma frame `271:169`
(390w) and folded it into the existing component as the **base** layer, with the
1440w frame (`271:15`) moved behind `md:`. No new component, no new route — the two
frames are the same page.

## The frames are the same page, with four exceptions

78 of 82 text nodes are byte-identical between the two frames. The four that differ
are content conflicts, not responsive variants:

| | 1440w | 390w |
|---|---|---|
| Price | `£79` | `£67.15` |
| Save chip | `Save 50% today` | `Save 57% today` |
| Reviews | `300+ reviews` | `272 reviews` |
| Byline | `By Topi Joonas · Co-founder, HLTH · 13 August 2026` | `By Topi Joonas · 13 August 2026` |

The byline is a genuine breakpoint decision, so it is handled responsively —
`· Co-founder, HLTH` is `hidden md:inline` and both frames are satisfied. The other
three are one value in one DOM and need a human; see the questions below.

## What changed in the component

29 measured replacements, each asserted to match exactly once before being applied.
Every previous "mobile" value in the file was a guess I made while building desktop —
all of them are now read off the 390w frame. The corrections were not small: the h1
was `34/42`, the frame says `32/40`; body copy was `18/30`, the frame says `17/28`;
the CTA was `60px` tall at `18px`, the frame says `52px` at `14px`.

Structural changes beyond type: figures crop **square** on mobile (`aspect-square
md:aspect-[var(--fig-ratio)]`) where desktop keeps each figure's own ratio; corner
radius 20 → 24; the offer card's product panel is 300px; card padding drops from
`p-10` to `px-5 pt-6 pb-7`.

## A judge defect this exposed

`design_diff.py` collected text from `display:none` elements. That is invisible on a
build with one layout and fatal on a responsive one — the hidden breakpoint's copy
counts as present, and the shown breakpoint's counts as missing. It reported the
responsive byline as MISSING for exactly this reason.

Fixed with a `rendered()` guard (`getClientRects().length`, plus `visibility` —
`offsetParent` gets `position:fixed` wrong) applied in all three walkers. The desktop
diff still returns 73/73 afterwards, so the fix cost nothing that was working.

## Results

| Check | Result |
|---|---|
| `tsc --noEmit` | clean |
| `npm run lint` | clean (0 warnings in this file) |
| Runbook (`web_qa.py`) | **PASS** every phase |
| Fidelity @ 390 vs `271:169` | 69 OK · 1 restyled · 2 retyped · 1 missing — all four are the known frame conflicts |
| Fidelity @ 1440 vs `271:15` | **73/73**, unchanged |
| Height @ 390 | 9160px live vs 9266px in Figma |
| Horizontal scroll | none at 1440 / 768 / 390 / 375 / 320 |

Screenshots verified by eye at 390 and 375 — all eight photos render, the square crops
land well, nothing overflows. The `1 Issue` badge in the dev overlay is Omnisend's
launcher failing to fetch settings from a localhost origin; it is site-wide and not
from this page.

## New tooling

`webforge/scripts/figma_spec.py` — flattens a figwright `get_node` dump into just the
properties that map onto Tailwind (layout mode, gap, padding, sizing, radius, fills,
strokes, effects, full typography). The 390w frame came in at 110KB of JSON; this
turns it into a table you can build from without ever reading a value off a screenshot.

## Measured (emailx-mobile-001)

| Page | Verdict | Speed | Links | Meta | Mobile | Console | A11y |
|---|---|---|---|---|---|---|---|
| email-exclusive | **PASS** | SKIP | PASS | PASS | PASS | PASS | PASS |

Full findings: `pagescore/runs/emailx-mobile-001/findings.json`


## Needs a human answer

- [ ] Offer price: the 1440w frame says £79 / Save 50% today, the 390w frame says £67.15 / Save 57% today (= £79 less the email 15%). One DOM serves both breakpoints, so one has to win. £79 is shipped for now — quoting £67.15 and charging £79 is a consumer-law problem, the reverse is not. Which is right?
- [ ] Trustpilot review count: 1440w says '300+ reviews', 390w says '272 reviews'. 300+ is shipped. Note this is what makes the rating line wrap to two lines on mobile — at 272 it fits on one, exactly as the frame shows. Still unresolved alongside the older 4.5 vs 4.6 score question.
- [ ] Banner chip label colour: the 390w frame renders 'EMAIL EXCLUSIVE' white on black, the 1440w frame renders it lime. Lime is shipped, since the article chip below it is lime on both frames. Is the white one intentional?

## Next

- [ ] Settle the three frame conflicts above, then re-run the 390 diff — it should go to 73/73 like the desktop one.
- [ ] Wire the CTA to the real 15% discount and decide whether the price should come from Shopify rather than being hardcoded from the frame.
- [ ] Still open from the desktop build: Delight-vs-Poppins for headings, the 4.5-vs-4.6 Trustpilot score, and whether /pages/email-exclusive should be indexable.

---

Written by `pagescore/session_note.py`. Runbook `pagescore/program.md`.
