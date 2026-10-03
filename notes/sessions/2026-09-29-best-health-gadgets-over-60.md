---
categories:
  - "[[Web-Tech]]"
subjects:
  - "[[Lightfunnels]]"
focus_area: V-B over-60s gadgets: control + B5 lead swap built
page: "[[best-health-gadgets-over-60]]"
status: in-progress
created: 2026-09-29
commit: 950a590
run_id: vb-b5-2026-09-29
tags:
  - lightfunnels
  - qa
---

# 2026-09-29 — V-B over-60s gadgets: control + B5 lead swap built

Page: [[best-health-gadgets-over-60]] · Index: [[LF Page Pipeline]]

**Result:** 0 PASS, 1 FLAG, 0 FAIL

## What happened

Built both arms of the V-B over-60s gadgets lead-swap test (ClickUp z941abwj4k)
into a new funnel, from Figma via figwright.

- funnel `fun_Z6I8-bN5nVJ_SwGgR9WWK` "TUB - Over-60s health - Meta" (`over-60s-health`)
- control `best-health-gadgets-over-60` (entry) - Figma `850:1487`
- variant `best-health-gadgets-over-60-v2` (B5) - lead from `850:1943` / `850:1957`

Funnel created PUBLISHED while empty: a new funnel is otherwise unreachable and
the runbook measures a live url. Both pages ship `noindex,nofollow` until a
human has looked.

## What changed

Both live, 200, one h1 each, 28 currency tags each, 0 console errors. PH renders
2,450 / 4,900 pesos with no pounds left on either page; GB untouched.

The builder refactored rather than forked: a shared engine emits everything
below the lead, and `verify_shared_identical()` fails the build if the two arms
differ. That is the guarantee this test needs - a lead swap is only a lead swap
if everything below it is byte-identical.

## What it found

design_diff, `?country=GB`, with `--accept`:

| | OK | ACCEPTED | RESTYLED | RETYPED | MISSING |
|---|---|---|---|---|---|
| control | 225 | 7 | 1 | 0 | 0 |
| B5 lead | 7 | 2 | 0 | 0 | 0 |
| B5 shared half | 219 | 14 | 0 | 0 | 0 |

qa_runner --skip-psi: 0 FAIL on both. The single FLAG is LF generating a Google
Fonts url from the literal family STACK (`Inter, InterFallback, sans-serif`),
which is not a family name - harmless, faces are self-hosted, shared with the
other TU pages.

**No PSI numbers this run: `PSI_API_KEY` is absent from `.env`.** Add one before
these take paid traffic.

### Three findings worth keeping

**Two of the builder's three post-deploy fixes did not take effect, and were
reported as done.** Verify a fix on the rendered page, not from the fact that
the code changed:

- the CLS fix targeted `img[title="photo"]`, an attribute no image on the page
  carries (content photos carry `title=""`). Changing the selector still did not
  put the rule into `document.styleSheets`.
- `maxWidth: 640px` IS in `comment_row()` but LF silently ignores that style
  prop - the column renders 662, so one comment wraps to 1 line where the design
  wraps to 2. The lone RESTYLED. Cosmetic, decorative comment section, left.

**The CLS problem did not exist.** Measured with a PerformanceObserver across a
full-page scroll: CLS = 0, zero layout shifts, all 7 photos loading at
naturalWidth 1440. LF's own classes already reserve the box. Three photos
measuring `height: 0` at an arbitrary moment was a proxy signal and produced a
wrong diagnosis that nearly cost a fix cycle. Measure the thing, not a correlate.

**`updateFunnel.steps` rejects any sibling sent without `settings`**
(`StepSettings!` is required). Latent on the control build - no siblings, so an
empty list passed - and it detonated on the very next page. Relatedly
`createStep` + `updateFunnel` is NOT atomic: a detached step is invisible to
`funnel.steps`, so a naive retry orphans one per attempt. The builder now parks
the new step id in `pagescore/.cache/_pending_step.json` between the calls.
The funnel holds exactly the two intended steps, verified.

Also fixed in tooling this session: `session_note.py` opened every file without
an encoding, so on win32 it died on any run whose findings contained a currency
symbol. And `pagescore`'s script-stripping regex did not terminate on an escaped
`<\/script>`, so it swallowed page bodies and reported zero tags on correct
pages - four false alarms before it was caught.

## What is still open

- the four questions above (CTA destinations, form backends, noindex, B5 byline)
- four money figures tagged but flagged, not decided: "Around 20 pounds"
  (converts to a falsely precise figure), "28.49 before VAT", the "560 over 3
  years" sum whose arithmetic stops reconciling after conversion, and a price
  inside a reader COMMENT that will silently change currency
- nothing committed; no push
- the PostHog experiment and the entry redirect are not set up - that is the CRO
  task z941abwj4k, and it starts after a human approves these pages

## Measured (vb-b5-2026-09-29)

| Page | Verdict | Speed | Links | Meta | Mobile | Console | A11y |
|---|---|---|---|---|---|---|---|
| best-health-gadgets-over-60-v2 | **FLAG** | SKIP | PASS | PASS | PASS | FLAG | PASS |

Full findings: `pagescore/runs/vb-b5-2026-09-29/findings.json`


## Needs a human answer

- [ ] CTA destinations: competitor buttons link out to withings.com / ouraring.com / taking.care. Should an HLTH advertorial link to competitors at all? Commercial call.
- [ ] Comment + newsletter forms have no backend. Decorative, or wire up before paid traffic?
- [ ] noindex,nofollow removal - when, and by whom?
- [ ] B5 keeps the byline (the card omits it, but omits all chrome). Drop it, or keep? Dropping makes the test measure lead angle AND author credibility.

## Next

- [ ] Human reviews both pages, then remove noindex and set up the PostHog 2-way + entry redirect

---

Written by `pagescore/session_note.py`. Runbook `pagescore/program.md`.
