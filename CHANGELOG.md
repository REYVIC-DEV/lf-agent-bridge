# Changelog

Dated log of changes made to live Lightfunnels pages and to the bridge tooling.
Per-funnel detail (measurements, rejected options, reasoning) lives in each
workspace's `NOTES.md`; this file is the index of *what changed where*.

Account `90380`. Funnel ids are the opaque `fun_…` strings.

---

## 2026-08-06 — `fun_vGqQYxn4H2i_traYYkh4w` (tub / smartwatch-review)

A single funnel holding **13 independent advertorials as sibling steps** (UK, DE,
AU, CA, TH + variants) — not a sequence. `starting_step_id` is step 3, which is
the live entry page.

Detail: [`funnels/tub/smartwatch-review/NOTES.md`](funnels/tub/smartwatch-review/NOTES.md)

### Page changes

| step | slug | what changed |
|---|---|---|
| **3** (live entry) | `xI7j8mDEB` | all of the perf work below |
| **11** (staging twin) | `0sAhHP7ki` | same as step 3 — proving ground, kept identical |
| **12** (Randell build) | `randell-build` | store-host links only (see below) |
| 0,1,2,4–10 | — | **not edited** |

**Step 3 + 11 — performance passes**

1. **Three photo blocks → hand-written `<img>`.** LF's `Image` block exposes no
   `srcset`/`sizes`/`loading`/`fetchpriority`. Origins were 1.7–2.0 MB PNGs
   (photographs saved as PNG); re-encoded to WebP at 1400px, **5,510K → 239K**.
   Mobile now requests the 400w AVIF (13K) instead of 750w (34K). srcset points at
   `/cdn-cgi/image/` deliberately — bypassing the resizer loses AVIF and *cost*
   ~1.0s LCP on the first attempt.
2. **Offer video: 3,256 KiB → 0 on load.** `autoplay` overrides
   `preload="metadata"`, so a 6.3s clip 14 screens below the fold downloaded in
   full. Now IntersectionObserver-attached, re-encoded 1328×742 H.264 CRF 30
   (403 KiB, SSIM 0.9888), poster through the resizer (107 → 16 KiB).
   **Total payload 3,869 → 1,310 KiB.** Two `<source>` elements are load-bearing —
   see NOTES.
3. **Block CSS moved out of `<body>` into `<head>`.** Four in-body `<style>` tags
   (self-inflicted in pass 1–2) each forced a full-document style recalc:
   **styleLayout 2,703 → ~190 ms, TBT 430 → 0 ms, PSI 81 → 92.**
4. **Metric-matched `InterFallback` + `Inter, InterFallback, sans-serif` stack**
   (from upstream's `references/performance.md`): **CLS 0.151 → 0.001.**
5. **Six explicit `Inter` `@font-face` declarations** — required, because the stack
   makes LF request a bogus family and real Inter collapsed to 400/500/800,
   silently rendering ~52 blocks in Arial.
6. **Dead Roboto webfont removed** — was downloading, rendered zero visible text.
7. **Inter 6 weights → 3** (400/700/800): `500→400`, `600→700`, `900→800`.
   ~71 KiB saved **for real users**; no effect on the PSI score (see caveat).
8. **Scoped to step level.** Items 3–6 were briefly in funnel-level
   `header_scripts`, i.e. live on all 12 steps including 10 out-of-scope
   advertorials (verified unharmed). Now in `settings.custom_html.header` on steps
   3 and 11 only. Font preloads and preconnects **dropped** — proven inert.

**Step 12 — content wiring** (all measured at **98 before and after**, every time)

| change | detail |
|---|---|
| 8 Amazon buttons | were `href="#"` — dead. Wired to the real affiliate URLs, 2 per product (Whoop / Apple Watch / Garmin / Fitbit), all carrying `tag=techunboxed04-20`. |
| no `aff-*` class | owner's call: with the URL on the button there is nothing for the header's replacer to do, so it gets no hook. One less runtime DOM mutation. |
| breadcrumb | `Home` → `blog.techunboxed.co`, `Wearables` → `/category/wearables`. Trailing crumb left unlinked (it is the current page). |
| social icons | removed — four `<a href="#">`+`<svg>` with no visible text, 1,885 chars of dead links. |
| footer policy links | given the popup trigger ids (`terms`/`priv`/`edit`/`aff`) and the policy modal added. |
| footer alignment | centred; it was `left` because it used to share a flex row with the social icons. |

**URLs came from the live `AFFILIATE` map, not from step 3.** Step 3's inline
destinations are **stale** — verified, all 8 differ from the live map — because the
header script overwrites them at runtime, so nobody notices they rot. Step 12
having no class means its URLs must stay correct on their own; the mitigation is
that `tag=` is embedded, so attribution survives even if a deep link ages.

**The popup improves on step 3's copy.** Step 3 ships the modal's `<style>` inside
the body — the same in-body-stylesheet pattern that cost it 2,703 ms of style
recalc. Here the 1,019-char `<style>` went into `settings.custom_html.header` and
only markup + script are in the body, so **step 12 still has 0 in-body `<style>`
tags.**

Two bugs found and fixed while wiring the triggers:
- The theme registers a click handler on every anchor and runs
  `document.querySelector(href)`, so a bare `href="#"` throws *"'#' is not a valid
  selector"*. Pre-existing (the page shipped 9 such links) but now on a path users
  click. Repointed each href at its overlay id.
- That alone made the theme **scroll to the overlay**. Fixed by moving the popup's
  own listener to the **capture phase** with `stopPropagation`, so it runs before
  the theme's handler. Verified: all four open with the right heading, no jump, Esc
  closes, 0 console errors.

**Step 12 — offer card rebuilt to Figma frame `557:6514`**

Built from measured Figma values, not copied from another step and not eyeballed
from the screenshot:

| element | Figma | ours before |
|---|---|---|
| border `557:6515` | 2px **dashed** `#000`, `dashPattern [6,4]`, radius **6** | solid, radius 20 |
| badge `557:6559` | `#E63A45`, radius 7, padding 7/16, Inter ExtraBold 16/28.8 → 43px tall | 5/14 padding, 33px tall |
| badge `557:6558` | absolute, centred, `y = -22` | left-aligned, inside the padding |
| image `557:6516` | at (2,2), fills the left half top-to-bottom | inset 22px, 300px tall, vertically centred |
| TP text `557:6522` | per-run: "Excellent" **Bold + UNDERLINE**, all `#000`, lh 19.2 | all plain, `#111827`, lh 18 |

Notes on the non-obvious parts:

- **The badge takes zero flow height.** Figma marks its container
  `layoutPositioning: ABSOLUTE`; LF has no `position` prop, so `margin
  {top:-24px, bottom:-19px}` reproduces it — `-24 + 43 - 19 = 0`, so it straddles
  the top edge without pushing the image down. Verified at 22px above the edge.
- **`line-height` does nothing to an inline element**, so the badge stayed 33px
  until the span became `display:inline-block` — then 43px, matching the frame.
- **`<u>` is reset by LF's CSS.** The underline only took as an inline
  `style="text-decoration:underline"`.
- **The Trustpilot logo was a 1000×318 PNG (ratio 3.14) in a 70×17 box (ratio
  4.12)**, so `objectFit:contain` letterboxed it — fitting by height to ~53px and
  leaving ~17px of dead space, which is what made the logo look detached from the
  text. Swapped to the SVG the frame actually specifies: exact ratio, gap now 6px,
  and **71.5 KiB → 4.9 KiB**.
- "Flush" needed three separate causes removed: the card's 22px padding, the row's
  20px gap, and `alignItems:center` floating a fixed-height image in a taller row.
  Verified: 2px on left/top/bottom — exactly Figma's (2,2) inside the 2px stroke.

Still **98** after every step (measured twice each time); payload 1,066 → 1,073 KiB
net of the 66 KiB logo saving and the added modal.

**Step 12 — store-host links**

`hlthtrack.com` → `hlthtrack.co.uk` on a UK page that was pointing at the .com
store. **15 rewritten, 6 left alone** — those are
`trustpilot.com/review/hlthtrack.com`, where the domain is the review-page *slug*,
not a link. Applied with `lf.py edit --step`, scoped to step 12; DE/AU/CA/TH
untouched. **No content or layout was copied from any other step.**
PSI before **98** → after **98** (twice): a link rewrite adds no bytes and no
requests. Edit set:
[`edits/step12-uk-store-host-2026-08-06.json`](funnels/tub/smartwatch-review/edits/step12-uk-store-host-2026-08-06.json)

### Result

| | step 3 | step 12 |
|---|---|---|
| PSI mobile | **88–90** (was 66 at session start) | **98** |
| CLS | 0.001 (was 0.151) | 0 |
| TBT | 0 ms (was 540) | 0 ms |
| payload | 402 KiB (was 3,869) | 1,066 KiB |

**Why step 3 plateaus at 88–90 while step 12 hits 98 — it is not the page.**
Cloudflare Fonts rewrites fonts to same-origin `/cf-fonts/` for real browsers but
**skips the rewrite for the `Chrome-Lighthouse` UA**, and strips our preload and
preconnect tags for it. PSI therefore measures an un-rewritten page with two extra
origins (googleapis CSS → gstatic woff2), ~450–600 ms of handshake each under
Slow-4G. That is the observed **bimodal FCP: 2.87s ×4 vs 1.85s ×1** — a discrete
cost, not noise. Step 12 dodges it only because it ships no webfont bytes to PSI at
all. **Real-user CrUX already passes CWV: LCP 0.9s, INP 112ms, CLS 0.**

### Known remaining

- **JetBrains Mono: ~21 KiB + its own origin fetch for the single word
  "Disclaimer".** Worst byte-per-character on the page; undecided.
- Two footer SVGs lack `width`/`height` — 20 screens below the fold, zero CLS
  impact, cosmetic only.
- Stale `b221e6c8` preloads on steps 8 and 9 — pre-existing, those steps are out
  of scope.

---

## 2026-08-06 — `fun_Z78qnXtnsXIf619roFNNU` (channels / meta-uk)

Detail: [`funnels/channels/meta-uk/NOTES.md`](funnels/channels/meta-uk/NOTES.md)

- Step 0 brought to 1:1 with Figma: 2 images swapped, **37 colour edits**,
  **46 typography edits**, avatar restored to a true circle (`objectFit: cover` +
  `borderRadius: 47.5px` — a non-square source in a 95px box was being distorted).
- `hlthtrack.com` → `hlthtrack.co.uk`: **5 rewritten, 8 left alone** (Trustpilot
  slugs). Host-only rule.
- Image weight 245.4K → 192.2K. The hero had been uploaded at q90 by mistake —
  2.4× a neighbouring image at identical dimensions.
- **Not** rolled out account-wide: `hlthtrack.com` appears 516× across 17 funnels,
  many are Trustpilot slugs, `.co.uk` already appears 223×, and `hlthtrack.de`
  appears 12× — a blanket replace would send non-UK traffic to the wrong store.

---

## Tooling

New in `tools/lf-agent-bridge/`:

- **`image_prep.py`** — resize + compress before upload. Codec by content type:
  `--mode photo` (lossy WebP) / `--mode graphic` (lossless). Reports measured
  mean/max pixel error; enforces the 5 MB presigned cap.
- **`image_registry.py`** — `build`/`match` an account-wide image index
  (sha256 exact + dhash perceptual) so a near-identical asset is reused rather
  than re-uploaded.
- **`speedtest.py`** — Lighthouse/PSI runner with history and `--compare`.
  Resolves `PAGESPEED_KEY` from `--psi-key` → `$PAGESPEED_KEY` → `.env`, and
  **defaults to PSI whenever a key resolves**, because local Lighthouse throttles
  relative to this machine: TBT measured 340 → 660 → 960 ms across three
  consecutive runs of an unchanged page, purely from background load. Extracts the
  diagnostics that actually explain things — main-thread breakdown, layout-shift
  selectors, font/image bytes.

Changed:

- **`lf.py texts --session`** — `texts` is the documented before-state for `edit`,
  but it could not run in this project at all: there is no app token in `.env`, and
  a session token additionally needs the dashboard headers, so it failed with
  `errors_fix_version`.
- **`lf.py edit --step <uid>`** (+ `lf_api.edit_step_bodies(step_uids=…)`) —
  **essential on a multi-market funnel.** Without it, `edit` rewrites every step
  containing the string, which here would have pushed UK links onto the DE, AU, CA
  and TH advertorials.
- **`lf_api.duplicate_funnel(extra_headers=…)`** — the last mutation that could not
  take session headers. Also documents that a clone inherits `published`.
- **`lf.py capture --out DIR`** — archive a step body into a workspace instead of
  `templates/`.

## Conventions worth keeping

- **Never assert a step *count*.** This funnel is shared; a colleague added step 12
  mid-session and a hardcoded `== 12` failed on a healthy funnel. Assert that the
  steps you intend to touch exist — `updateFunnel` is a partial update, so unlisted
  siblings survive by omission.
- **`body` comes back parsed, not a string.** Echo it back in the same shape;
  `json.dumps`-ing it first makes `updateFunnel` fail with a bare
  `"Oops! Something went wrong"`.
- **Never bare-string-replace a domain.** Classify each occurrence by role first —
  host vs review slug — and match structurally.
- **Never put a `<style>` inside an LF block.** Block CSS goes in
  `settings.custom_html.header`, which renders in `<head>`.
- **Prove it on step 11 before step 3.** Every change in this log that reached the
  live page went there first; three real regressions were caught that way.
