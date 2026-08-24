---
categories:
  - "[[Web-Tech]]"
subjects:
  - "[[Lightfunnels]]"
focus_area: Build 235:958 into new 'randell testing' funnel + QA
page: "[[bh-advertorial-v1]]"
status: blocked
created: 2026-08-24
commit: 1c70fa0
run_id: randell-testing-20260824
tags:
  - lightfunnels
  - qa
---

# 2026-08-24 — Build 235:958 into new 'randell testing' funnel + QA

Page: [[bh-advertorial-v1]] · Index: [[LF Page Pipeline]]

**Result:** 0 PASS, 1 FLAG, 0 FAIL

## What happened
Built Figma frame 235:958 ("Branded Hype Advertorial V1", HLTH file, 1440x5499 + mobile companion 235:1098) into a brand-new funnel "randell testing" (fun_f1IsXx3YnEA2UD2g91dAv, slug randell-testing), published, step bh-advertorial-v1 as starting step. Modeled on build_bh_advertorial_v1.py (built from same-named node 217:395) but verified all 34 text nodes against 235:958 — 3 real differences found and shipped from 235:958 (straight apostrophe in s5, uniform #191E2A on "In Partnership With HLTH", JetBrains Mono DISCLAIMER label). All 8 images pixel-identical to bh_advertorial_img_map.json cache, reused.

## What changed
One fix cycle (LF_ALLOW_REDEPLOY scoped to bh-advertorial-v1 only): (1) s5 teardown link aria-label "Untitled link" -> "See the HLTH Band offer" via className s5-offer-link + footer-script setAttribute (LF hardcodes the aria-label in the storefront bundle; no block prop feeds it); (2) header+footer logo alt="" -> alt="TechUnboxed". Both verified in rendered DOM post-hydration. User then scoped remaining work to QA-only on this page — no further fixes.

## What it found
QA v1: PSI 99 mobile / 100 desktop, CLS 0.000, 0 broken links, design_diff 0 MISSING / 0 RETYPED (2 RESTYLED = stale node-level fills, verified false positives). QA v2 (--after-publish, cache-warm): PSI 97/100 (delta = run noise, not cold-cache signature), a11y no-alt 7 -> 5, both fixes verified. ONE STANDING FAIL: "protect your heart" + "scientifically proven... heart events at night" contradict the page's own disclaimer ("Do not use this device to detect, monitor, or manage any medical condition") — copy is verbatim in the design, so blocked on human wording. Also: ALL 4 CTA BlockLinks announce "Untitled link" to screen readers (platform-wide LF defect, present on sibling funnels too); tooling fix landed in design_diff.py (tolerate fills:"mixed", substring containment pass).

## What is still open
- Copy FAIL wording (human).
- CTA aria-label rewrite (cheap, same pattern as s5) — awaiting go-ahead.
- JetBrains Mono webfont decision; social icon destinations or removal.
- Trustpilot 4.6 not verified at source (bot-blocked; destination JSON-LD says 4.62/475). GBP list price £158 implied but unverifiable from this geo (PH store shows exact 50% pattern).

## Measured (randell-testing-20260824)

| Page | Verdict | Speed | Links | Meta | Mobile | Console | A11y |
|---|---|---|---|---|---|---|---|
| bh-advertorial-v1 | **FLAG** | PASS | PASS | PASS | PASS | FLAG | FLAG |

Full findings: `pagescore/runs/randell-testing-20260824/findings.json`


## Needs a human answer

- [ ] Replacement wording for 'protect your heart' (and 'scientifically proven... heart events' in section 3): verbatim from Figma 235:958 but contradicts the page's own disclaimer — design/compliance owner must choose.
- [ ] Should the 4 CTA BlockLinks get the same aria-label rewrite as the s5 link? LF hardcodes aria-label='Untitled link' on every BlockLink anchor platform-wide.
- [ ] Load real JetBrains Mono for the DISCLAIMER label via header <link>? Currently fallback monospace (LF's Google Fonts CSS request is ORB-blocked, pre-existing).
- [ ] Footer social icons (IG/YouTube/RSS/X) are non-clickable images — link them (need destinations) or drop them?

## Next

- [ ] On approved wording: fix copy in build_randell_testing.py, redeploy with LF_ALLOW_REDEPLOY=bh-advertorial-v1, re-QA with --after-publish

---

Written by `pagescore/session_note.py`. Runbook `pagescore/program.md`.
