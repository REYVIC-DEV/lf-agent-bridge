---
categories:
  - "[[Web-Tech]]"
subjects:
  - "[[Lightfunnels]]"
focus_area: Scaling or Failing event page: build, 2 QA passes, 2 fix cycles
page: "[[scaling-or-failing-event]]"
status: blocked
created: 2026-10-06
commit: f33fc00
run_id: sof-2026-10-06-qa-v2
tags:
  - lightfunnels
  - qa
---

# 2026-10-06 — Scaling or Failing event page: build, 2 QA passes, 2 fix cycles

Page: [[scaling-or-failing-event]] · Index: [[LF Page Pipeline]]

**Result:** 0 PASS, 1 FLAG, 0 FAIL

## What happened

Built the Scaling or Failing event landing page from Figma into a brand-new published
Lightfunnels funnel, then ran the full pipeline: QA, fix, QA, fix. Ten sections,
desktop and mobile frames built as two designs rather than one reflow.

Two platform bugs had to be fixed before any of it could start.

**The Lightfunnels API moved to cookie auth.** The repo waited for an
`Authorization: Bearer` header to sniff a token out of, and that header no longer
exists: the dashboard authenticates with the `lf_session` cookie plus an
`account-id` header. So `lf.py login` and `lf.py refresh` both answered "Saved
session expired" at every attempt while the session was perfectly valid. Fixed in
`lf_api.py` and `lf_session.py`; `python lf_session.py check` now proves the API
answers rather than trusting a flag.

**A stale render served an empty page.** Two steps in the same funnel, neither with
a `product_id`, held byte-identical bodies. One served all 16 sections, the other
served none of them. The difference was history: a step rendered while empty keeps
serving that render, and later writes never reach it. Writing step metadata flushes
it. This corrects the earlier belief that `product_id` was the cause.

## What changed

- `pagescore/build_sof_event.py`, new, ten sections authored as HTML blocks with the
  stylesheet in `settings.custom_html.header`. The design is a poster: rotated
  hand-drawn lockups, text on a curve, layer blur, gradient washes, notched chips.
  None of that exists in LF's style-prop vocabulary. Cost: not editable block by
  block in the LF editor, the builder is the source of truth.
- `lf_api.py` - cookie auth, and `create_funnel` now forwards `extra_headers`.
- `lf_session.py` - sign-in detected from localStorage rather than header sniffing,
  which survives the next auth change. New `check` command.
- `pagescore/deploy_guard.py` - its session fallback hand-built headers without the
  cookie, so the guard could not run at all on a session-only machine.

## What it found

QA pass 1: FAIL. The page had a single `min-width:768px` breakpoint that jumped
straight into a layout authored for an 1800px frame, with fixed px that never
scaled. Everything from 768 to 1600 degraded and 768-992 was unusable. The ticket
block, the only place money is asked for, overflowed its button box by 233px at 768
and 65px at 1440; prices clipped mid-digit.

The harness said FLAG, not FAIL, on both passes. It was wrong both times:
`qa_runner.py` phase 4 only checks document-level horizontal scroll and every
container breaking here is `overflow:hidden`. Every real finding came from hand
measurement. **That is a gap in the runbook, not a one-off.**

Fix cycle 1 replaced the single breakpoint with a ladder and fixed all ten findings.
QA pass 2 confirmed them across 112 selector/width combinations, but found the fix
had introduced two regressions of its own: the hero lockup and CTA sat 90-100px off
axis across the whole new 768-1199 band, and the nav became a 570px dark island with
bare page background either side. Fix cycle 2 cleared both, verified live.

## What is still open

Three FAILs remain and every one needs a human, which is why this is blocked rather
than done:

1. **"SAVE $1,000" has no anchor price.** Implies a $2,997 regular price that appears
   nowhere on the page. An unsubstantiated savings claim is what ad review acts on.
2. **Privacy and Terms are plain text, not links.** The footer renders them as copy
   with zero `<a>` elements, and none of the 23 anchors points at a legal page. The
   link check scored 23/23 because it only inspects links that exist - the same blind
   spot as the overflow check. Compliance risk on a page selling $1,997 tickets.
3. **The hero claims 12 speakers; the grid holds 10.** Three named, seven TBA.

Design decisions also outstanding: the "SCALLING" typo drawn into the You Decide
artwork at ~100px; topic chip labels clipping below ~1652px (at 1200, 8 of 12 clip);
three cards rendering the literal word "PHOTO"; and the hero names and grid names
being six different people with no overlap and no labels.

The four ticket CTAs are parked on `#tickets` pending a Whova registration URL from
Topi. **The page cannot take paid traffic until that lands.**

Performance is entirely unmeasured. `PSI_API_KEY` is absent, so there is no
Lighthouse score, LCP, CLS or TBT for this page. Page weight, 0.30 MB, is the only
speed signal and it passes.

Also deliberately deviating from the design, and accepted: 768-1199 serves the mobile
layout centred in a 520px column, ticket cards stack at 1440 and 1600, and the footer
stacks from 1200-1419. The 1800px design simply does not hold at those widths.

## Measured (sof-2026-10-06-qa-v2)

| Page | Verdict | Speed | Links | Meta | Mobile | Console | A11y |
|---|---|---|---|---|---|---|---|
| event | **FLAG** | SKIP | PASS | PASS | PASS | PASS | FLAG |

Full findings: `pagescore/runs/sof-2026-10-06-qa-v2/findings.json`


## Needs a human answer

- [ ] What is the Early Bird regular price? SAVE $1,000 is claimed five times with no anchor price anywhere on the page.
- [ ] Where do Privacy and Terms point? They are plain text today, so the page has no reachable legal pages at all.
- [ ] Is it 12 speakers or 10? The hero stat says 12, the grid holds 10.

## Next

- [ ] Answer the blocked items, then one fix pass covers all of them at once.

---

Written by `pagescore/session_note.py`. Runbook `pagescore/program.md`.
