---
categories:
  - "[[Web-Tech]]"
subjects:
  - "[[Lightfunnels]]"
focus_area: Five mobile fidelity defects, and the judge that should have caught them
page: "[[email-exclusive-mobile-fixes]]"
status: in-progress
created: 2026-08-26
commit: f89cf37
run_id: emailx-mobile-002
tags:
  - webforge
  - hlth-site
  - responsive
  - qa-judge
---

# 2026-08-26 — Five mobile fidelity defects, and the judge that should have caught them

Page: [[email-exclusive-mobile-fixes]] · Index: [[LF Page Pipeline]]

**Result:** 1 PASS, 0 FLAG, 0 FAIL

## What happened

Five defects reported against the mobile build, all real, all fixed. More usefully: all
five were invisible to the judge, and that is the part worth writing down.

## The five

| # | Reported as | Actually |
|---|---|---|
| 1 | wrist photo "didn't follow the display" | Wrong crop — CSS-cropped from the desktop asset |
| 2 | quote "too cramped, font looks off" | Set in Delight; the node is **Poppins Medium** |
| 3 | workshop photo "is cropped" | Wrong crop, same cause as 1 |
| 4 | product panel "shouldn't be zoomed" | Figma's asset is 4096×4096 square; mine was 952×1278 portrait |
| 5 | offer copy "didn't follow the layout" | Save chip wrapped to two lines; five solid stars where the design dims the fifth for 4.5 |

**On 2 — only H1/H2/H3 nodes are named `· set family to Delight Semi Bold`.** That suffix
is an instruction, and a node without it wants the font it actually has. `Quote` is
Poppins Medium. I had applied the brand face to it because the headings near it use one.

**On 1, 3 and 4 — a photo's crop is not a CSS property.** The two frames crop the same
photograph differently, and `object-cover` on the desktop file centre-crops, which is not
what the design did. Fixed by exporting each node's own render (figwright
`save_screenshots` at 3x) and art-directing with `<picture>`. Seven new files, 9.44 MB of
PNG in, 0.44 MB of webp out.

## Why the judge missed all of it — four separate holes

1. **Typography was never compared at all.** `walk_text_nodes` read font size and weight
   from a `style` dict. A figwright `get_node` dump puts them at the top level with
   `fontName` as `{family, style}`. So against the mobile dump every value was `None`,
   every comparison was skipped, and the diff returned a clean bill of health because it
   had nothing to compare. This is the worst kind of bug in a judge: it does not fail, it
   agrees with you.
2. **Family was never checked**, in either shape. Size, weight and colour can all be
   correct while the typeface is wrong — which is exactly defect 2.
3. **Nothing checked reflow.** A chip that is one line in the frame and two on the page
   has broken its own box, and no copy comparison notices.
4. **Nothing looked at pixels.** Right box, right file, right alt text, no 404 — and the
   wrong half of the photograph.

## What the judge does now

- Reads **both** Figma dump shapes, so size, weight, family and line-height actually get
  compared.
- Compares the **resolved font family**, reading `set family to X` out of the node name
  where the design says so.
- Compares **line count** — measured from real line boxes via Range rects, not
  height ÷ line-height, which counts a pill's padding as a second line.
- Compares **images as pixels** against the design's own node renders (`--crops`), after
  hiding fixed/sticky chrome, because an element screenshot otherwise captures the cookie
  banner sitting on top of the figure and reports it as a wrong crop.

### The threshold is calibrated, not guessed

Measured against this page's own before/after:

| | distance |
|---|---|
| correct crop | 0.001 – 0.002 |
| crop nobody noticed | 0.006 – 0.007 |
| **crop a human flagged** | **0.055 – 0.264** |

The first threshold I picked, 0.14, let the wrist photo through at 0.133 — one of the
three a human had just flagged. `IMG_PIXEL_TOL` is now **0.05**. A check that only ever
passes is worse than no check, so this was verified by running it against the old assets
and confirming it fails them.

## The loop

`web_qa.py --design SPEC@WIDTH` is now repeatable and takes a matching `--crops`, so one
command checks every breakpoint, text and images, and **a fidelity failure fails the
run** — the runbook passing is no longer enough:

```bash
python3 webforge/qa/web_qa.py /pages/email-exclusive \
  --design webforge/runs/emailx-mobile-001/design.json@390  --crops .../emailx-mobile-001/crops \
  --design webforge/runs/emailx-001/design-full.json@1440   --crops .../emailx-001/crops
```

Checking only the widest frame is how a mobile layout ships unlooked-at, which is what
happened here.

## Results

| Check | Result |
|---|---|
| `tsc --noEmit` / `npm run lint` | clean |
| Runbook | PASS every phase |
| Fidelity @ 1440 | **73/73 text, 7/7 images** |
| Fidelity @ 390 | 68 OK, 7/7 images; the 5 remaining findings are the 3 open questions |
| Overall | **FAIL** — correctly, on the unresolved £67.15 |

Also documented in `.claude/rules/figma-to-tailwind.md`: photos get exported per node and
art-directed, and a node name can be an instruction.

## Measured (emailx-mobile-002)

| Page | Verdict | Speed | Links | Meta | Mobile | Console | A11y |
|---|---|---|---|---|---|---|---|
| email-exclusive | **PASS** | SKIP | PASS | PASS | PASS | PASS | PASS |

Full findings: `pagescore/runs/emailx-mobile-002/findings.json`


## Needs a human answer

- [ ] Offer price — still open, and now the only thing failing the run: 1440w says £79 / Save 50%, 390w says £67.15 / Save 57%. web_qa returns FAIL until it is settled, which is correct.
- [ ] Trustpilot review count — 1440w '300+', 390w '272'. This is what makes the rating line wrap to two lines on mobile; at 272 it fits on one, exactly as the frame draws it.
- [ ] Banner chip label colour — 390w white, 1440w lime. Lime shipped.

## Next

- [ ] Answer the three above; the 390 diff should then reach 73/73 with 0 image mismatches, like the 1440 one already does.
- [ ] Run the same --crops check over the eleven techunboxed advertorials — none of them has ever had its photos compared to the design.

---

Written by `pagescore/session_note.py`. Runbook `pagescore/program.md`.
