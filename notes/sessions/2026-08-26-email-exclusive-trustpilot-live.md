---
categories:
  - "[[Web-Tech]]"
subjects:
  - "[[Lightfunnels]]"
focus_area: Trustpilot figures read live, and a way to record a deliberate deviation
page: "[[email-exclusive-trustpilot-live]]"
status: in-progress
created: 2026-08-26
commit: f89cf37
run_id: emailx-mobile-009
tags:
  - hlth-site
  - webforge
  - qa-judge
---

# 2026-08-26 — Trustpilot figures read live, and a way to record a deliberate deviation

Page: [[email-exclusive-trustpilot-live]] · Index: [[LF Page Pipeline]]

**Result:** 1 PASS, 0 FLAG, 0 FAIL

## The question this answers

Two sessions of open question — "is the Trustpilot score 4.5 or 4.6?" — was already
answered in the repo, by the most recent commit on the branch:

> **f299cfa** Read Trustpilot score and review count live instead of hardcoding them

I had been carrying it as unresolved while the answer sat in `lib/trustpilot.ts`.

## What the site does

`getTrustpilot()` reads `app.hlthtrack.com/api/trustpilot` server-side, caches an hour,
times out at 3s, and **never throws and never returns null** — a failure yields a
last-known-good pair, so all thirteen call sites are a plain `await` with no error
branch. Four rules from the dashboard's `API.md`, three counter-intuitive:

1. **Print `score` (4.6), never `stars` (4.5).** `stars` is the half-star graphic. Their
   doc records this being got wrong once already.
2. A null `score` must not become a badge — fall back, never derive one from the mean.
3. `stale` is a **flag, not a refusal**: the count only grows, so a stale figure
   understates us.
4. Read it server-side and CORS never applies.

## So my component was wrong twice over

It hardcoded `4.5/5 · 300+ reviews`. **4.5 is the graphic, not the rating**, and the
count was one of four different hardcodes across the site (62 / 117+ / 182 / 300+)
against a real 355 — the exact drift that commit existed to end.

Now:

```tsx
const tp = await getTrustpilot()
<TrustpilotLink className="flex items-center gap-[6px] md:gap-2">
  <TrustpilotStars size={18} lastStarPct={tp.lastStarPct} />
  <span …>{tp.score}/5 · {tp.reviewsPlus} reviews on Trustpilot</span>
</TrustpilotLink>
```

Renders **4.6/5 · 350+ reviews on Trustpilot**, with the fifth star 60% filled — derived
from the score, per `TrustRating`'s warning that a 50% fill beside a printed 4.6 draws
4.5 and contradicts the number next to it. `reviewsPlus` keeps the ad-lander "300+"
idiom, floored so the claim never overstates.

`TrustpilotStars` gained `lastStarPct` (partial fill, matching `TrustRating`) replacing
the `score`/opacity prop added earlier — which reproduced exactly the trap that file
documents. Default is unchanged, so the other four callers render identically.

⚠️ The rating line now wraps to two lines at 390px, because "350+ reviews on Trustpilot"
is wider than the frame's "272 reviews". Left as is: the alternative is type below the
design's own spec.

## Accepted deviations

Live figures mean the page will never match the frame's hardcoded ones. A judge that
reports a settled question on every run gets ignored, so `design_diff --accept` takes a
JSON of `{node-id: why}`; those rows report as **ACCEPTED** with the reason in the report
and do not fail the run or reach `todo.md`. `frames.json` carries one per breakpoint.

## Three judge bugs this shook out

1. **A wrapper measured instead of the text.** Wrapping the rating in `TrustpilotLink`
   made the `<a>` — 16px/400, all inherited — match ahead of the 12px/500 span, and
   report three style deltas that did not exist. Interpolated copy makes this the common
   case: `{tp.score}/5 · …` is several text nodes, so the whole string exists only as an
   aggregate. Fixed by aggregating over `span` too and preferring the leaf, then the
   innermost wrapper.
2. **Identical copy paired by document order.** This design has "EMAIL EXCLUSIVE" twice —
   a white banner chip and a lime article chip. Order pairing is a coin flip and it
   flipped, reporting `weight 600 -> 700` and `weight 700 -> 600` at once. Now tied on
   style distance, which is what a reader would do.
3. **Images sampled before they loaded.** Against a cold dev server, an `<img>` inside a
   `<picture>` reports the fallback `src` and `naturalWidth` 0 — which read as "wrong
   file, did not load" and failed three photos at random. Now waits for
   `document.images.every(complete)`.

(1) and (2) were introduced by this session's own change and caught by re-running; (3)
was latent and would have produced intermittent red for no reason.

## Results

| | 1440px | 390px |
|---|---|---|
| Text | **72 OK + 1 accepted, 0 deltas** | 68 OK + 1 accepted |
| Images | **7/7** | **7/7** |
| Geometry | 0 | 0 |

`tsc` and `lint` clean. `todo.md` is down to the price conflict, `Save 57%`, the banner
chip colour, and one h2 that wraps to 2 lines instead of 3 because Delight is narrower
than the Poppins the frame was measured in.

## Measured (emailx-mobile-009)

| Page | Verdict | Speed | Links | Meta | Mobile | Console | A11y |
|---|---|---|---|---|---|---|---|
| email-exclusive | **PASS** | SKIP | PASS | PASS | PASS | PASS | PASS |

Full findings: `pagescore/runs/emailx-mobile-009/findings.json`


## Needs a human answer

- [ ] Offer price — 1440w £79 / Save 50%, 390w £67.15 / Save 57%. Now the ONLY thing failing the run, and the last of the three.

## Next

- [ ] Answer the price; 390 then reaches clean like 1440 already is.
- [ ] Consider whether the other four /pages advertorials still hardcode anything — this commit converted 13 components but those were not in its file list.

---

Written by `pagescore/session_note.py`. Runbook `pagescore/program.md`.
