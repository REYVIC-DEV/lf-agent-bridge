# TechUnboxed — smartwatch-review (`fun_vGqQYxn4H2i_traYYkh4w`)

**12 steps, all individual advertorials** — they are not a sequence, so
`starting_step_id` matters and must be re-checked after every write.

| step | uid | slug | note |
|---|---|---|---|
| 3 | `step_-42yvjxEYUC-1yAzL9TKy` | `xI7j8mDEB` | **LIVE entry page** (`starting_step_id`) |
| 9 | `step_7KUV0Oh0ZnNTff5uYVBNA` | `LxcTvDN0X` | UK-V2.2 — source of the footer / `aff-*` ids / brand links |
| 11 | `step_HFrpGxiibhudWV1YLEMs1` | `0sAhHP7ki` | UK-V3 rebuild — staging twin of step 3 |

Live entry: https://www.techunboxed.co/smartwatch-review/xI7j8mDEB

Steps 3 and 11 are intentionally kept identical: 11 is where a change is proven
before it goes to 3.

## Invariants to assert after any write

`updateFunnel(steps:[...])` is a *partial* update — siblings survive by
omission — but a malformed payload can still damage what it does touch. After
every write, confirm:

- `len(steps) == 12`
- `starting_step_id == step_-42yvjxEYUC-1yAzL9TKy`, `published == True`
- per step 3 and 11: `aff-` ×9, `trustpilot` ×8, `hlthtrack.co.uk` ×15

Those `hlthtrack.com` hits that remain (3 per step) are Trustpilot review
**slugs**, not store links. Never bare-string-replace them — match on host only.

`body` comes back from `get_funnel_steps` as a **parsed object**, not a string.
Echo it back in the same shape; `json.dumps`-ing it first makes `updateFunnel`
fail with a bare `"Oops! Something went wrong"`.

## Log

- `2026-08-06` — **hand-written `<img>` for the three photo blocks.** Prompted by
  a PageSpeed "properly size images" report (3 files, 57.3 KiB est. savings).

  The report's framing was misleading in both directions:

  - The dimensions were not really the problem. The **origins were 1.7-2.0 MB
    PNGs** — photographs saved as PNG, 5,510K for the three. Visitors never
    fetched those, because LF routes images through the Cloudflare resizer, so
    the weight was invisible in the report. Re-encoded to WebP at 1400px:
    **5,510K → 239K (96% smaller)**, which only pays off on storage and cache
    misses, not in the score.
  - What *was* wrong is that LF's injected `sizes` is
    `(min-width: 1280px) 50vw, 100vw`. These images live in a **664px** container
    with 16px side padding, so `100vw` overstated the mobile width and the
    browser kept picking the 750w candidate for a ~358px slot.

  So the three `Image` blocks became `HtmlElement` blocks with a real `<img>`:
  `srcset` at 400/560/750/1000/1328w, `sizes="(min-width: 768px) 664px,
  calc(100vw - 32px)"`, `fetchpriority="high" loading="eager"` on the hero (the
  measured LCP element) and `loading="lazy"` on the two below-fold photos. Block
  **ids were preserved** so nothing referencing them breaks.

  **Keep the srcset pointed at `/cdn-cgi/image/`.** The first attempt pointed
  `src`/`srcset` straight at the uploaded WebPs and *regressed* LCP by ~1.0s,
  because the resizer answers `format=auto` with **AVIF** and a raw asset URL
  throws that away. Measured at 750w, same displayed size:

  | path | delivered |
  |---|---|
  | raw WebP asset | 50.4K webp |
  | `/cdn-cgi/image/…` from the old 2 MB PNG | 33.5K avif |
  | `/cdn-cgi/image/…` from the new 1400px WebP | **33.1K avif** |

  Latency was identical (~50ms, `cf-cache-status: HIT`) in all three. So the
  resizer is kept, and only its *origin* changed — same delivered bytes, 96%
  less at rest. Mobile now requests the **400w** candidate (hero 13.0K AVIF)
  instead of 750w (33.6K).

  The CSS in each block reproduces the old Image styles verbatim — `width:100%`,
  `height:371px`, `object-fit:cover`, `border-radius:10px`, and the `max-width:
  767px` override to 210px (hero) / 230px (sec1, sec2). Verified on the live
  page: 664×371 desktop, 351×210/230/230 mobile, 0 console errors, all three
  decode, both lazy images load on scroll.

  **Result — mobile Lighthouse, median of 5: 72 (spread 68-78) against a
  baseline of 75 (spread 73-80). Read that as flat, not as a win.** What did
  change is the opportunities list, now down to `server-response-time` alone
  (`uses-responsive-images` and `unused-javascript` both dropped out), and TBT
  at 330ms, the lowest recorded. Desktop was 99 and untested after this change.

  Backups: `steps/03-PRE-HTMLIMG.2026-08-06.json`,
  `steps/11-PRE-HTMLIMG.2026-08-06.json`.

  New library assets (label → 800w / 1400w):
  `tub-hero` `a875d8e5` / `2e657800` · `tub-sec1` `4fa0d467` / `7cc03385` ·
  `tub-sec2` `159e176e` / `a6fa18c4`. The 800w uploads are now unused — the
  resizer derives every candidate from the 1400w origin — but are kept as the
  fallback if the resizer is ever bypassed.

- `2026-08-06` (second pass) — **the offer video: 3,256 KiB → 0 on load.**
  Prompted by "Avoid enormous network payloads — 3,869 KiB". One line item was
  84% of the page.

  `ffprobe` on it: **1934x1080, 30fps, 6.3s, 4.23 Mbps H.264, no audio track**,
  rendering at **351x196** and sitting **14 screens below the fold**. Three
  independent faults:

  | fault | fix | effect |
  |---|---|---|
  | downloaded on load — `autoplay` overrides `preload="metadata"` | sources attached by IntersectionObserver (`rootMargin: 400px`) | 3,256 KiB out of the initial load |
  | 1934px @ 4.23 Mbps for a 664px slot | re-encode 1328x742 H.264 CRF 30 | 3,256 KiB → **403 KiB** when it does load |
  | poster was a raw 107 KiB JPG (`poster` gets no LF srcset injection) | route through the resizer at 750w | 107 → **16.1 KiB** AVIF |

  Encoder comparison, SSIM against the 1328-downscaled original — **VP9 lost to
  H.264 on this clip**, so there is no WebM source and no need for one:

  | encode | size | SSIM |
  |---|---|---|
  | h264 1328 crf26 | 635.0 KiB | 0.9925 |
  | **h264 1328 crf30** | **402.8 KiB** | **0.9888** |
  | h264 1328 crf32 | 326.7 KiB | 0.9862 |
  | h264 1000 crf26 | 400.6 KiB | 0.9896 |
  | vp9 1328 crf34 | 750.2 KiB | — |
  | vp9 1328 crf38 | 555.3 KiB | — |

  **The two `<source>` elements are load-bearing — do not collapse to one
  `src`.** The LF media library accepts an MP4 (`upload_local_image` with
  `content_type="video/mp4"` works) but serves it as **`content-type:
  image/mp4`**. Chromium sniffs the container and plays it — verified
  readyState 4, 1328x742, playing — but WebKit is stricter about media
  Content-Type and could not be tested here (no WebKit engine installed
  locally), and iOS is a large share of this funnel's traffic. So the original
  Shopify MP4 is listed second, with its correct `video/mp4`. Browsers walk the
  source list on load failure, so the worst case for a strict browser is exactly
  the old behaviour.

  Shopify offers no smaller progressive rendition — checked. There is an HLS
  master at `/videos/c/vp/<hash>/<hash>.m3u8` with 1080p/720p/480p variants, but
  those are segment playlists, and native HLS in `<video>` is Safari-only;
  Chrome would need hls.js, which costs more JS than it saves.

  `width`/`height` attributes plus `aspect-ratio: 1328/742` were added so the box
  is 351x196 before the poster arrives — with `preload="none"` and no
  dimensions it would otherwise start at the UA default 300x150 and shift.

  **Result: total payload 3,869 KiB → 1,310 KiB (−66%).** Verified on the live
  page: 0 MP4 requests at the top of the page, 0 sources attached; on scroll it
  attaches both, plays from the LF copy, one request, box unchanged, 0 console
  errors. Mobile Lighthouse score stayed flat at **71 (spread 66-74)** — this
  audit is *Unscored*, so that is expected; the win is real bandwidth, not the
  number.

  After this, the payload is **majority third-party JavaScript**: GTM +
  2x gtag = 484 KiB, PostHog = 166 KiB, i.e. 650 KiB of the remaining 1,310.
  That is tag-manager configuration, not reachable from the page body.

- `2026-08-06` (third pass) — **CLS 0.151 → 0. It was the webfont, not images.**

  Prompted by "Image elements do not have explicit width and height", which
  **was a red herring**. That audit flagged exactly two SVGs — the footer
  disclaimer logo (`0753ba23`) and an arrow icon (`d9f20df4`) — and both sit at
  y≈16,441 and y≈16,661 on a 17,391px page, i.e. **20 screens below the fold**.
  They cannot shift anything, they are absent from Lighthouse's own shift
  attribution, and the audit is marked *Unscored*. Fixing them would have
  changed nothing.

  The real cause came out of the trace (`lighthouse --save-assets`, then reading
  `LayoutShift` events). **One shift, score 0.1507 — the entire page CLS:**

  ```
  t=+559ms  score=0.1507
    node 160  y 411 -> 447   h 24        (byline / "Last updated")
    node 162  y 451 -> 487   h 210       (hero image)
    node 163  y 677 -> 713   h 28 -> 56  (image caption: 1 line -> 2 lines)
    node 164  y 721 -> 785   h 54 -> 38
  ```

  Heights unchanged on the hero, everything below the byline displaced **+36px**,
  and the caption **re-wrapped from one line to two**. That is text reflow, and
  the devtools log lines up exactly: six Inter woff2 files finish at
  **519-522ms**, the shift fires at **559ms**.

  The chain: LF's theme requests Google Fonts, Cloudflare Fonts rewrites it to
  self-hosted `/cf-fonts/s/inter/5.2.8/latin/<weight>/normal.woff2`, and the
  browser only requests those **after CSSOM + layout (~395ms)** — so the swap
  always lands after first paint. Six weights at ~24 KiB = **142 KiB of font**.

  Fix: two `<link rel="preload" as="font" crossorigin>` tags at the very top of
  `header_scripts`, for **400 and 700** — measured as carrying essentially all
  above-the-fold text (400 ×101 nodes, 700 ×62; 800 ×11, 600 ×5, 900 ×1 are
  marginal, and preloading more competes with the LCP image for bandwidth).
  `crossorigin` is required even though the fonts are same-origin, because fonts
  are always fetched in CORS mode — without it the preload would not match and
  the file would download twice.

  **Result: CLS 0.151 → 0**, reproduced on two separate 5-run medians.

  Note this is a **funnel-level** change, so it applies to all 12 steps, not just
  step 3. It is beneficial everywhere (every step uses Inter) and cannot break a
  step — a preload that goes unused only wastes bytes.

  ⚠ **The score numbers from this pass are unusable.** TBT climbed monotonically
  340 → 660 → 960ms across three consecutive runs while the machine accumulated
  60 chrome/node processes (one node at 3.1 GB) from my own Lighthouse and
  Playwright runs. Per `speedtest.py`'s own warning, local scores are only valid
  on an idle machine. CLS is the exception worth trusting here — it is a layout
  property, largely CPU-independent, and it hit exactly 0 twice. **Re-run
  `speedtest.py --runs 5` on an idle machine to get a real score.**

- `2026-08-06` (fourth pass) — **PSI 81 → 87-92. The cause was in-body `<style>`
  tags, and I had added four of them myself.**

  Triggered by a fair question: why did `test3-smartwatch/article-v10` score
  **90** while step 3 scored lower, given near-identical structure?

  **How to measure this properly — use PSI through Playwright, not the API.**
  The PSI *API* is rate-limited to 429 without a key. But `pagespeed.web.dev`
  works fine in a browser, and the full Lighthouse result is exposed on the page
  as **`window.__LIGHTHOUSE_MOBILE_JSON__`** (and `__LIGHTHOUSE_DESKTOP_JSON__`).
  Navigate, wait for the text "Diagnose performance issues", then read that
  global — every audit, unthrottled by this machine's load. This is the only
  reliable way to score these pages; local Lighthouse here is worthless while
  editors and browsers are open.
  ⚠ Read the score from the LHR global, **not** the DOM. The gauges near the top
  of the PSI page are *field* CrUX data (28-day, origin-wide) and the visible
  `100` was Best Practices — I misread it as Performance before checking.

  Apples-to-apples, PSI lab, Lighthouse 13.4.1 / Moto G Power / Slow 4G:

  | | test3 = **90** | step 3 = **81** |
  |---|---|---|
  | FCP | 2.1 s | 2.3 s |
  | LCP | 2.5 s | 2.6 s |
  | TBT | 0 ms | **430 ms** |
  | CLS | 0.151 | 0 |
  | SI | 2.1 s | 4.1 s |
  | main-thread | **0.4 s** | **3.7 s** |
  | └ styleLayout | **271 ms** | **2,703 ms** |
  | └ scriptEvaluation | 6 ms | 10 ms |
  | bytes | 1,187 KiB | 521 KiB |

  So it was never JS, images, third-party or the domain (TTFB 612 vs 617 ms, and
  **neither** page's PSI run executed the tracking stack). It was **style
  recalculation**. The pages are otherwise twins:

  | | test3 | step 3 |
  |---|---|---|
  | page height | 11,695 px | 11,754 px |
  | elements | 1,291 | 1,393 |
  | CSS rules | 970 | 1,001 |
  | **`<style>` in `<body>`** | **0** | **5** |

  A stylesheet inserted mid-parse invalidates and recomputes styles for the whole
  document parsed so far. Five of them scattered through a 1,393-element page is
  five full-document recalcs — 2.7s of it. **Four of the five were mine**, one per
  HtmlElement block written earlier the same day.

  Fix: moved all four rule sets into `header_scripts` (rendered in `<head>`),
  leaving only markup in the body. Rules are id-scoped, so funnel-wide placement
  no-ops on steps that lack those ids.

  | | before | after |
  |---|---|---|
  | styleLayout | 2,703 ms | **164 / 191 ms** |
  | main-thread | 3.7 s | **0.3 / 0.4 s** |
  | TBT | 430 ms | **0 ms** |
  | score | 81 | **92, then 87** |

  **Rule going forward: never put a `<style>` inside an HtmlElement block.** Put
  block CSS in `header_scripts`. The one remaining in-body style is `.tu-overlay`
  (policy modals), pre-existing — moving it should be worth a little more.

  ⚠ **Correction to the third pass: CLS is _not_ durably fixed.** It reads
  0.158-0.163 again. The earlier "CLS 0" was real but partly an artifact — style
  recalc delayed first paint so long that the fonts had already landed, hiding
  the swap. Removing that bottleneck made the page paint sooner and re-exposed
  it. The preload still helps (fonts start at 177 ms instead of 395 ms) but is
  **not sufficient on its own**.

  Every `@font-face` on the page is `font-display: swap`, across **six Inter
  weights** (400/500/600/700/800/900, ~142 KiB), all used above the fold — under
  Slow 4G they cannot all land before paint, so a reflow is guaranteed. Options,
  none free:
  - `font-display: optional` — guarantees CLS 0, but on slow connections that
    pageview renders in the fallback font. A brand call, not a technical one.
  - Cut the weight count in the theme's Google Fonts request. Fewer files land
    sooner. **`Roboto` is also being downloaded and never used** — the design is
    Inter throughout.
  - Metric-matched fallback via `size-adjust`.

- `2026-08-06` (fifth pass) — **adopted upstream's metric-matched InterFallback.
  CLS 0 for real this time; step 3 stops swinging.**

  Merged `upstream/main` (`1c70fa0`), which added
  `.claude/skills/lightfunnels/references/performance.md`. It independently reached
  the same diagnosis recorded in the third/fourth passes above — the +36px H1
  reflow, the caption wrapping 1->2 lines, "PSI blames the hero but the hero is
  just the biggest thing that *moved*", and "preload alone is NOT enough" — and
  supplied the piece that was missing here: a **metric-matched fallback**.

  Two halves, both required:
  1. `@font-face{font-family:InterFallback; src:local('Arial')...;
     ascent-override:90.44%;descent-override:22.52%;line-gap-override:0%;
     size-adjust:107.12%}` in `header_scripts`.
  2. Every block's `fontFamily` routed through **`Inter, InterFallback,
     sans-serif`** (313 declarations per step). The fallback then occupies Inter's
     exact box, so the swap reflows nothing rather than racing first paint.

  **A retrofit hazard upstream does not hit, caught on step 11 first.** LF derives
  its Google Fonts request from block `fontFamily` values. With the stack in place
  it asked Google for a family literally named `Inter, InterFallback, sans-serif`,
  and real Inter collapsed to weights 400/500/800 only — **600 and 700 stopped
  loading and ~52 blocks silently rendered in Arial.** Fixed by declaring the Inter
  faces ourselves in `header_scripts` against the same-origin
  `/cf-fonts/s/inter/5.2.8/latin/<w>/normal.woff2` URLs. Upstream builds pages with
  the stack from the start, so their request never went through this transition.

  **Unexpected bonus:** the non-rewritten request returns Google's **variable**
  Inter — one 48 KiB file covering every weight, replacing five 24 KiB static
  files. Fonts **186 KiB -> 70 KiB**, page **521 KiB -> 403 KiB**.

  **Measured on PSI (step 11 as the A/B twin, three runs):**

  | | step 3 before | step 11 with fallback |
  |---|---|---|
  | score | 84 / 87 / 92 / 93 | **90 / 90 / 90** |
  | CLS | 0.158-0.163 | **0 / 0.001** |
  | FCP, SI | 1.8-2.4 s | 2.9 s |
  | bytes | 521 KiB | 403 KiB |

  The trade is explicit: FCP/SI lose a few points because the font now comes from
  a third origin, CLS gains the full 25, and **the score stops swinging**. A
  `preconnect` to `fonts.gstatic.com` was tried to win the FCP back and made **no
  difference** — the handshake was not the bottleneck. The hint is left in place as
  harmless.

  Verified on step 3 after applying: rendering pixel-identical (same H1 line
  breaks, same caption wrap), hero 664x371, 0 console errors, 12 steps,
  `starting_step_id` intact, `aff-` x9 / `trustpilot` x8 / `.co.uk` x15 unchanged.

## Known remaining gaps

1. ~~**CLS 0.151 on mobile.**~~ **Fixed** in the third pass above — it was the
   webfont swap, not images. My earlier guess here (that it came from ~24 `Image`
   blocks lacking intrinsic dimensions) was **wrong**; the trace shows a single
   shift caused by text reflow. Left visible as a reminder to read the trace
   before theorising about CLS.
2. **Two SVGs still have no `width`/`height`** (`0753ba23` footer logo,
   `d9f20df4` arrow icon). They are 20 screens below the fold and contribute
   nothing to CLS, so this is cosmetic — it only silences an *Unscored*
   diagnostic. Not worth a live-page write on its own; fold it into the next
   edit that touches those blocks.
3. **`alt` is empty on all three.** The `Image` blocks carried no `alt` either,
   so this is not a regression, but it is a real accessibility/SEO gap and the
   markup is now hand-written, so it is trivial to fill in once someone can
   describe the photos accurately.
3. **Unused JavaScript ~323 KiB.** Third-party (aimerce, gtag, PostHog); not
   addressable from the page body.
4. **Stale `b221e6c8` preloads still on steps 8 and 9.** Pre-existing, and those
   steps are untouched — no authorisation to edit them.
