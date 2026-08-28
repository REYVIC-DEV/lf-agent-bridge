---
categories:
  - "[[Web-Tech]]"
subjects:
  - "[[Lightfunnels]]"
focus_area: Geometry checking: the judge now compares boxes, spacing and crops
page: "[[email-exclusive-geometry-judge]]"
status: in-progress
created: 2026-08-26
commit: f89cf37
run_id: emailx-mobile-003
tags:
  - webforge
  - qa-judge
  - hlth-site
---

# 2026-08-26 — Geometry checking: the judge now compares boxes, spacing and crops

Page: [[email-exclusive-geometry-judge]] · Index: [[LF Page Pipeline]]

**Result:** 1 PASS, 0 FLAG, 0 FAIL

## Why

"I don't want to always point out the defects." Fair. The judge checked copy,
typography and photos; it did not check a single box. Padding, gaps, backgrounds, radii
and borders were all invisible to it, which is most of what "the layout is off" means.

## What it compares now

| | |
|---|---|
| **Width of FILL nodes** | a FILL node's width *is* its container's horizontal padding, restated — so wrong padding is caught without mapping the two trees at all |
| **The painted box around a line** | background, corner radius, border width — the chip, card or button the copy sits in |
| **Gap to the previous sibling** | local, so it neither accumulates drift nor is poisoned by a line that wrapped |
| **Gap between containers** | the section spacing a text-anchored check cannot see |

Container spacing needed **absolute coordinates**, which exposed a latent bug: figwright
reports x/y relative to the parent, so a Photo inside a Figure and a Product panel inside
a card both report `y=0`. Anything comparing positions across nesting levels was
comparing two coordinate systems. The walker now accumulates.

## The guards are the work

A geometry check that reports noise gets ignored, which is worse than not having one.
The first run produced 8 findings, 5 of them false. Each needed a specific exclusion:

- **HUG nodes** are as wide as their glyphs — comparing them measures font
  rasterisation, not layout.
- **Inline live elements**: a `<strong>` mid-paragraph is 92px wide where the design node
  is 342. Not the same box.
- **Aggregates**: an `<li>` standing in for a Benefit *frame* is 302 where the text node
  is 272. Also not the same box.
- **Non-adjacent siblings**: pairing two matched lines with unmatched content between
  them measures the height of what is in between, not a gap.
- **Horizontal rows**: a vertical distance in a wrapping row is a wrap artefact, not a
  spacing decision.
- **Containers the copy does not cover**: if a block opens with a photo, the text starts
  below it and the measured gap would include the photo. Not reported rather than
  reported wrongly.

After the guards: **zero findings on a correct page, at both breakpoints.**

## Proving it fails

Same discipline as the pixel threshold — a check that only ever passes is worthless. Four
defects were injected deliberately and all four were caught:

| Injected | Caught as |
|---|---|
| offer card padding 20 → 40 | `width 302 -> 260`, `width 198 -> 156` |
| save chip pill → 6px radius | `Save chip radius 999 -> 6` |
| pull-quote rule 4px → 1px | `width 314 -> 317` |
| article column gap 40 → 24 | `gap between Block and Block 40 -> 24` |

## It immediately found a real one

On **desktop**, which had been passing 73/73:

> `We'll invite you to test the HLTH Band risk-free` — width 900 → 780

`flex flex-col items-center` sizes children to their content, so the two offer-header
nodes the design marks `FILL` never stretched to their 900px. It looked right because the
text is centred anyway — until a longer line wraps where the design would not have. Fixed
with `w-full`; desktop is back to 73/73 with geometry active.

## The loop

```bash
python3 webforge/qa/web_qa.py /pages/email-exclusive \
  --frames webforge/runs/emailx-mobile-001/frames.json
```

`frames.json` names every breakpoint the design draws — node, width, dump, crops — so one
cannot be left off a command line. The run writes **`todo.md`**: runbook failures, copy,
typography, boxes, spacing and photos, merged across breakpoints into one list. That is
the handoff to the fix stage; nothing else has to be read.

A clean runbook no longer passes the run. `web_qa` fails when the page does not match the
design, because "loads fine, scores well, wrong layout" is the state this exists to stop.

## Still not covered

Letter-spacing, text-align, shadows, hover and focus states, animation. And looking at a
screenshot is still not optional — three photos once rendered blank while every gate was
green.

## Results

| Check | Result |
|---|---|
| tsc / lint | clean |
| Runbook | PASS |
| 1440 — text / images / geometry | **73/73 · 7/7 · 0** |
| 390 — text / images / geometry | 68 OK · **7/7** · **0** |
| Overall | FAIL, correctly, on the unresolved £67.15 |

## Measured (emailx-mobile-003)

| Page | Verdict | Speed | Links | Meta | Mobile | Console | A11y |
|---|---|---|---|---|---|---|---|
| email-exclusive | **PASS** | SKIP | PASS | PASS | PASS | PASS | PASS |

Full findings: `pagescore/runs/emailx-mobile-003/findings.json`


## Needs a human answer

- [ ] Offer price — 1440w £79 / Save 50%, 390w £67.15 / Save 57%. Still the only thing failing the run.
- [ ] Trustpilot review count — 1440w '300+', 390w '272'. This is what wraps the rating line onto two lines on mobile.
- [ ] Banner chip label colour — 390w white, 1440w lime. Lime shipped.

## Next

- [ ] Answer the three above; the 390 diff then reaches 73/73 like 1440 already does.
- [ ] Run --frames over the eleven techunboxed advertorials — none has ever had photos or geometry compared to a design.

---

Written by `pagescore/session_note.py`. Runbook `pagescore/program.md`.
