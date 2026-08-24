# Performance & PageSpeed (verified live 2026-08-06)

How to make a Lightfunnels page score well on PageSpeed Insights (PSI) / Lighthouse,
including the new **Agentic Browsing** category. All numbers below are from the
techunboxed smartwatch advertorial (`pagescore/build_test3.py`), measured against Google's real
PSI servers. Net result of this playbook: **mobile Performance 89 → 98, CLS 0.151 → 0,
Agentic Browsing 1/2 → 2/2**, desktop 100.

Everything here is injected through the page's **custom-HTML header/footer**
(step `settings.custom_html.{header,footer}`, written in session mode — see
`block-schema.md`). You cannot edit LF's framework CSS/`<head>`, so every fix is an
additive header/footer snippet or a change to how your blocks are authored.

## The scoring model (know what you're optimizing)

- Bands: red 0-49, orange 50-89, **green 90-100**. 90 is the bar.
- Weighted lab metrics (mobile): TBT 30%, **CLS 25%**, LCP 25%, FCP 10%, SI 10%.
  LF pages are JS-light so **TBT is ~0** and LCP/FCP/SI are usually fine — **CLS is
  almost always the one thing dragging the mobile score**. Desktop nearly always 100.
- **Agentic Browsing** (experimental, v150+): only **two scored checks** —
  1. *Accessibility tree is well-formed* (every visible interactive element has an
     accessible name), and
  2. *Cumulative Layout Shift* — and it treats **CLS as a HARD pass/fail at 0.1**.
     So CLS 0.15 only marks "needs improvement" in Performance (barely dents 90) but
     **fails** Agentic Browsing outright (1/2). Getting CLS < 0.1 fixes both at once.

## THE big one: font-swap CLS (this is what fails mobile)

**Root cause.** LF serves the **Inter** webfont with `font-display: swap` from
`/cf-fonts/s/inter/5.2.8/latin/<weight>/normal.woff2` (relative path, served on every
funnel domain). Block text is authored as `font-family: Inter` with **no usable
fallback**, so before Inter downloads the browser renders in its **default serif**
(Times) — wildly different metrics. Under PSI's slow-4G throttle Inter finishes
**~3.3 s in**, then swaps: the H1 reflows to an extra line (+36 px), captions wrap
1→2 lines, and the hero image is shoved down. That single reflow = the entire **0.15
CLS**. PSI blames the hero (`img.bvOhf`) but the hero is just the biggest thing that
*moved* — the culprit is the font.

**Preload alone is NOT enough.** Preloading the woff2 (below) makes it pass on a
fast machine but **still fails on Google's servers** — under their harsher network the
fonts still arrive after first paint and swap. You need the swap itself to cause **no
reflow**.

**The fix (two parts, both in the custom-HTML header):**

1. **Preload** the Inter weights used above the fold (so Inter usually wins the race):
   ```html
   <link rel="preload" as="font" type="font/woff2" crossorigin
         href="/cf-fonts/s/inter/5.2.8/latin/400/normal.woff2">
   <!-- repeat for each above-the-fold weight, e.g. 800 (headings) and 900 (H1) -->
   ```
   The `href` must **exactly** match the `@font-face src` URL (same subset+weight) or
   the browser double-downloads. `crossorigin` is required for fonts.

2. **Metric-matched fallback** so pre-swap text occupies Inter's *exact* box → the swap
   reflows nothing (industry-standard "adjustFontFallback", the Next.js Inter/Arial
   overrides). Define the face **and route every text block's font-family through it**:
   ```html
   <style>@font-face{font-family:InterFallback;
     src:local('Arial'),local('Liberation Sans'),local('Helvetica Neue');
     ascent-override:90.44%;descent-override:22.52%;line-gap-override:0%;size-adjust:107.12%}</style>
   ```
   Then author every text/title block with the stack **`Inter, InterFallback, sans-serif`**
   instead of `Inter` (in `pagescore/build_test3.py` this is the `FONT` constant used by
   `title()`/`text()` and the score helper). `local('Arial')` resolves to Liberation
   Sans on PSI's Linux env (metric-compatible), so the overrides hold there too.

   This also **improves FCP/SI** (text paints immediately in the matched fallback, no
   FOIT wait) — here FCP 2.1→1.7 s, SI 2.6→1.7 s as a bonus.

## LCP hero (keep it green)

LF misapplies `fetchpriority="high"` to the **logo**, not the LCP hero, and doesn't
reserve the hero's box. In the header, **preload the hero** matching LF's responsive
srcset/sizes (no double-download) and **reserve its height**; in the footer, move
`fetchpriority` onto the hero and off the logo:
```html
<!-- header -->
<link rel="preload" as="image" fetchpriority="high"
      imagesrcset="<the exact cdn-cgi width=384..3840 srcset>"
      imagesizes="(min-width: 1280px) 50vw, 100vw">
<style>img[title="hero"]{height:371px!important;width:100%;object-fit:cover}
  @media(max-width:767px){img[title="hero"]{height:210px!important}}</style>
<!-- footer -->
<script>/* set hero fetchpriority=high + loading=eager; removeAttribute fetchpriority on img[title=logo] */</script>
```
The hero carries a stable `title="hero"` — use it as the selector. (Height reserve
helps a little but does NOT fix the font-swap shift above; you need both.)

## Other wins

- **Lazy-load heavy media below the fold.** A 3+ MB autoplay `<video>` in the cost
  section: render it `preload="none"` with `data-lazysrc` and an IntersectionObserver
  (rootMargin ~400px) that sets `src`+`play()` on approach. Zero mp4 bytes until scrolled.
- **Name every interactive element** (Agentic Browsing accessibility check + a11y score):
  social-icon `<a>` with only an SVG inside needs `aria-label`. Audit: count visible
  `a,button,[role=button]` with no text/aria/title/alt → must be 0.
- `unused-css-rules` (~11 KiB) is **LF framework CSS** — not yours to strip; ignore it.

## Measure it RIGHT (do not trust a Playwright PerformanceObserver)

A naive Playwright `layout-shift` observer under-reports (scrolling counts as recent
input and excludes shifts; unthrottled loads batch everything before paint). Use these:

- **Ground truth — PSI API** (needs a key; user supplies, treat as sensitive, don't commit):
  ```
  https://www.googleapis.com/pagespeedonline/v5/runPagespeed?url=<enc>&key=<KEY>&category=PERFORMANCE&strategy=mobile
  ```
  Parse `lighthouseResult.audits`: `cumulative-layout-shift.displayValue`, and the
  **`layout-shifts`** audit's `details.items[].node.selector` for the culprit. `fetchTime`
  confirms it fetched the fresh page. Runs live each call (each ~20-40 s).
- **Real Lighthouse locally** (v13+, faster iteration; Chrome path = Playwright's Chromium):
  ```
  CHROME_PATH="<...chromium...>/Google Chrome for Testing" npx --yes lighthouse@latest <url> \
    --form-factor=mobile --screenEmulation.mobile \
    --only-audits=cumulative-layout-shift,layout-shifts --output=json --chrome-flags="--headless=new"
  ```
  Caveat: on a low-latency machine fonts arrive fast, so local Lighthouse may show CLS 0
  even when PSI shows 0.15. To reproduce Google's **late-font** condition locally, use a
  **delayed-font harness**: Playwright mobile (412×823, DPR 1.75) + CDP
  `Emulation.setCPUThrottlingRate{rate:4}` + `Network.emulateNetworkConditions` (slow 4G)
  + `ctx.route("**/cf-fonts/**/*.woff2", delay 3s)`, install a `buffered` layout-shift
  observer, **do not scroll**, wait past the swap, read accumulated CLS. Delaying the
  woff2 by 3 s reproduces the ~0.15; the metric-matched fallback drives it to 0 there and
  on PSI. (Harness lived at `scratchpad/repro.py`.)
- To read the exact shift mechanics, capture `LayoutShift` **sources** (`previousRect`
  vs `currentRect` per node) — that's how you prove "hero moved +36 px, didn't resize."

## Gotchas

- **`?preview=true` inflates CLS** — the preview banner ("You're in preview mode") pushes
  content down ~63 px. PSI tests the **non-preview** production URL; measure that.
- **Storefront caches the preview URL** a few minutes after a session write; the
  production URL updates fast (verified via `curl` of the served HTML). PSI's `fetchTime`
  + font request priority (`VeryHigh` = preload honored) confirm Google saw your update.
- Keep the **URL/slug stable** once shared with teammates — these fixes never require a
  slug change.

## ⚠ Traps found the hard way (verified live 2026-08-06, techunboxed smartwatch-review)

**LF serves a STRIPPED page to the `Chrome-Lighthouse` UA — so a PSI score is not
your page.** Same URL, two user agents:

| marker | real Chrome | Chrome-Lighthouse |
|---|---|---|
| HTML size | 900 K | **282 K** |
| our `@font-face` block | 6 | **0** |
| GTM / PostHog / Lenis | present | **0** |
| custom CSS (`custom_html.header`) | present | **0** |

Not CDN staleness — no `cf-cache-status`/`age` headers and stable across repeated
fetches. Consequence: **anything you put in `header_scripts` or
`settings.custom_html` is invisible to PSI**, so a change there cannot be validated
by the score, in either direction. Treat **CrUX field data as the truth** and use
PSI only for the LF-generated part of the page. (Contradicts "Ground truth — PSI
API" above; both are true — PSI is the right harness for what it can see.)

**Cloudflare Fonts also varies by UA.** It rewrites Google Fonts to same-origin
`/cf-fonts/…` for real browsers but **skips the rewrite for `Chrome-Lighthouse`**,
and strips `preconnect`/`preload` tags for it. Two consequences: a font
`preconnect` you add will not appear in the page PSI measures, and PSI sees two
extra origins (googleapis → gstatic) that real users never pay for.

**The `Inter, InterFallback, sans-serif` stack silently breaks real Inter.** LF
derives its Google Fonts request from block `fontFamily` values, so the stack makes
it ask Google for a family *literally named* `Inter, InterFallback, sans-serif`. The
returned faces carry that whole string as their family name, which the stack's
`Inter` token never matches. Symptom: the page downloads Inter woff2 it **cannot
use** and renders everything in the Arial-metric fallback — weight 800 gets
synthesised, which reads as "fonts look thin".

Detect it with a canvas measurement, not `document.fonts` (blind to cross-origin
stylesheets) and not `document.fonts.check()` (returns `true` for undeclared
families):

```js
const c = document.createElement('canvas').getContext('2d');
const w = f => { c.font = f; return c.measureText('UP TO 50% OFF').width; };
w('800 24.7px Inter') === w('800 24.7px NoSuchFontZZZ')   // true => Inter is NOT loaded
```

Fix: declare the faces yourself in `settings.custom_html.header`, against the
same-origin URLs LF/CF already emit so the browser dedupes:

```css
@font-face{font-family:'Inter';font-style:normal;font-weight:700;font-display:swap;
  src:url('/cf-fonts/s/inter/5.2.8/latin/700/normal.woff2') format('woff2')}
```

**Never put a `<style>` inside a block.** A stylesheet inserted mid-body
invalidates and recomputes styles for the whole document parsed so far. Four of
them on a 1,393-element page cost **2,703 ms of `styleLayout`** and 430 ms TBT
(PSI 81). Moving the same CSS to `settings.custom_html.header` — which renders in
`<head>`, verified — took it to ~190 ms and PSI 92. Note `overflow:hidden` on a
card is not a substitute fix if anything (a badge) is meant to overhang it.

**The asset library cannot host webfonts.** `upload_local_image` accepts a `.woff2`
and returns it byte-intact, but `assets.lightfunnels.com` sends **no
`Access-Control-Allow-Origin`**, and fonts are always fetched in CORS mode — so it
is blocked on a custom domain. MP4 uploads *do* work, though served as
`content-type: image/mp4` (Chromium sniffs the container; WebKit is stricter, so
keep a correctly-typed `<source>` as a fallback).

**Style props that silently do nothing:** `zIndex` (not supported — computes to
`auto`); `line-height` on an inline element (make the span `display:inline-block`);
`<u>` (reset by LF's CSS — use an inline `style="text-decoration:underline"`).

**`objectFit:contain` letterboxes a mismatched ratio.** A 1000×318 logo (3.14) in a
70×17 box (4.12) fits by height to ~53px and leaves ~17px of dead space that reads
as a spacing bug. Check the asset ratio against the box before adjusting gaps.
