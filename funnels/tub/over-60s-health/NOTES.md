# TUB - Over-60s health - Meta (`fun_Z6I8-bN5nVJ_SwGgR9WWK`)

Holds the over-60s health-gadget advertorial tests for the TechUnboxed brand.
Public base: https://www.techunboxed.co/over-60s-health/

## Steps

| slug | step id | what it is |
|---|---|---|
| `best-health-gadgets-over-60` | `step_eLPUkJVkow9fERayUgV5m` | V-B CONTROL. Funnel's `starting_step_id`. |
| `best-health-gadgets-over-60-v2` | `step_uVycPOTyXKD0EL-fpyEJl` | B5 "The one question". Lead swap only. NOT the entry page. |
| `best-health-tracker-over-60` | `step_kwP6unXldwoYPTE-Zm6Vw` | V-A CONTROL, smartwatch test. NOT the entry page. |
| `best-health-tracker-over-60-v2` | `step_Ext0gx8NLEFfPJDu3XPB0` | V-A A1 "Warning + hidden cost". Lead swap only. NOT the entry page. |

Both arms are built from one engine, `pagescore/vb_gadgets_shared.py`. Each builder
supplies only its lead; everything from the "We tested:" list down is built once, and
`verify_shared_identical()` fails the build if the two ever diverge outside the lead.
That is what keeps this a one-variable test.

---

## 2026-09-29 — V-B CONTROL built (run `vb-control-2026-09-29`)

Built from Figma frame `850:1487` ("Health gadgets for over-60s — V-B · Tested with
over-60s, mixed gadgets", 1440×13029) on the "Advertorials/Blogs" page, read through
figwright. V-B has **no 390 frame**, so every mobile value came from V-A's designed 390
page, node `850:1029` — same template, same chrome, same stack/hr/price/button
vocabulary.

- builder: `pagescore/build_vb_gadgets_over60.py`
- copy table (generated, never typed): `pagescore/vb_copy.py`
- design dump: `pagescore/runs/vb-control-2026-09-29/design.json`
- mobile reference dump: `pagescore/runs/vb-control-2026-09-29/design_mobile_va.json`
- images: `pagescore/.cache/vb_img_map.json` (8 uploaded + the logo reused from the
  library, where it was already serving every other TechUnboxed advertorial)

This was the funnel's first step, so the write used the 3-call recipe:
`createStep` (leaves it detached) → `updateFunnel` with `starting_step_id` + the steps
list, which is what actually attaches it.

**`noindex,nofollow` is deliberately in this step's header.** The funnel is published so
QA can reach the page; this is a half-built advertorial on an indexed domain. Taking it
off is a separate, deliberate change — never part of a build.

### Verified live

| check | result |
|---|---|
| HTTP | 200 (not 503), three consecutive loads |
| `design_diff.py` vs the frame, `?country=GB` | 0 MISSING, 0 RETYPED, 225 OK, 7 accepted, 1 RESTYLED |
| `qa_runner.py --skip-psi` | no FAIL (1 FLAG, see below) |
| 390px device-emulated | h1 28/32, h2 22/28, h3 19/24, body 18/31, gutter 20, CTAs full-width 350, nav band absent, no horizontal scroll |
| dynamic currency | GB/DE/AU all convert, 28 figures each, nothing left hidden, 0 console errors |

The QA FLAG is one blocked request: Lightfunnels auto-generates a Google Fonts URL from
the literal font-family *stack* (`Inter, InterFallback, sans-serif`), which is not a
family name, so it 404s/ORBs. Harmless — every face on this page is self-hosted through
our own `@font-face` — and it is platform behaviour shared with the other TU pages, not
something this build introduced.

### Known: three fixes sit in the builder but NOT yet on the live page

The deploy guard correctly refuses to overwrite a live page without per-page human
authorisation, so these are coded and dry-run clean but undeployed:

1. **Mobile hero height.** `<img width/height>` attributes are presentational hints that
   set the `height` property, so `aspect-ratio` was ignored and the hero rendered
   350×371 at 390px instead of 350×197. Fixed with `height:auto`.
2. **Comment text column.** Design is 640px inside a hugging 698px row; flex:1 gave 662
   and one comment then wrapped to 1 line where the design wraps to 2 (the single
   remaining `design_diff` RESTYLED). Capped at 640 (580 for the nested reply).
3. **Lazy-image CLS.** LF's Image block emits no width/height and lazy-loads, so
   below-fold photos measured `height: 0` until they decoded and everything under them
   jumped. Every content photo now reserves its 16:9 box via `img[title="photo"]`.

To land them, a human authorises exactly this page:

```bash
LF_ALLOW_REDEPLOY=best-health-gadgets-over-60 python3 pagescore/build_vb_gadgets_over60.py
```

Then re-check 200, and re-run `design_diff.py` with `?country=GB` (without the country
pin the live currency script has already converted every figure and the copy check
reports false MISSING/RETYPED on all 28 of them).

---

## 2026-09-29 — B5 arm built (run `vb-b5-2026-09-29`)

Second and last page of this test. **A lead swap and nothing else.**

Source: Figma cards `850:1943` (760×1109) and `850:1957` (390×1280), "B5 · The one
question", read through figwright. Dumps at
`pagescore/runs/vb-b5-2026-09-29/design.json` and `design_mobile.json`.

- builder: `pagescore/build_vb_gadgets_over60_b5.py`
- shared engine: `pagescore/vb_gadgets_shared.py`

### The refactor (done first, so the two arms cannot drift)

`build_vb_gadgets_over60.py` was ~1000 lines; it is now ~90 and only holds the control
lead. Everything else moved to `vb_gadgets_shared.py`. **The control was not
redeployed** — the refactored builder was proved to emit byte-identical output first:
body (uuids stripped) identical across all 15,608 lines, header identical at 8,601
bytes, footer at 11,088, `seo` identical. So the refactor is invisible to the live
control page.

### What changed in the lead

| | control | B5 |
|---|---|---|
| h1 | `850:1527` | `850:1947` "Before You Buy Any Health Gadget For Someone Over 60, Ask This One Question" |
| deck | — | `850:1948` Gelasio **Regular** 20/30 → 17/26, `#6b7078` |
| byline | `850:1528` | `850:1528` — **kept**, see decision below |
| hero | 720×371 desktop + 16:9 mobile, two assets | 720×336 at **both** widths, one asset, a different photograph |
| body paras | 6 (`850:1532`–`1537`) | 5 (`850:1952`–`1956`), first two Inter Bold |

Not built, deliberately: the `angle` chip `850:1944/1958` ("B5 · THE ONE QUESTION"),
the 1px rule under it, and the grey "FEATURED IMAGE" placeholder label. Figma
annotations, not page content — verified absent from the live HTML (0 occurrences of
"B5 ·").

### Verified live

| check | result |
|---|---|
| HTTP | 200 on B5, 200 on the control, 200 on the funnel root |
| `design_diff` vs the B5 lead card, `?country=GB` | 0 MISSING, 0 RETYPED, **0 RESTYLED**, 7 OK + 2 accepted |
| `design_diff` vs the control frame (shared half), `?country=GB` | 219 OK, 0 MISSING, 0 RETYPED, 0 RESTYLED |
| `qa_runner --skip-psi` | no FAIL (same benign Google-Fonts ORB flag as the control) |
| shared body identity | asserted at build time, 129,590 chars, share links normalised |
| 390px | h1 28/32, deck 17/26 Gelasio w400, byline 14/20, hero 350×163 (720:336), gutter 20, CTA 350, nav absent, no h-scroll |
| dynamic currency | GB 28 figures untouched; DE and PH fully converted, **0 pounds left**, nothing hidden, 0 console errors |
| `starting_step_id` | still the control — asserted by the writer after the mutation |

### Two platform bugs fixed in the writer while doing this

1. **`updateFunnel.steps` rejects a sibling sent without `settings`** (`StepSettings!`
   is required). This could not show up on the control build, because that funnel had
   no siblings yet — it detonated on the very next page. Siblings are now echoed back
   with `settings` and `visual` in both the create and redeploy paths.
2. **`createStep` + `updateFunnel` is not atomic, and a detached step is invisible to
   `funnel.steps`** — so when the attach failed above, a naive retry called
   `createStep` again and would have orphaned a step on every attempt. The new step id
   is now parked in `pagescore/.cache/_pending_step.json` between the two calls and
   cleared once the attach lands, so a retry re-attaches the step that already exists.
   The one orphan from the failed run was recovered this way, not abandoned.
   The writer also now asserts the step actually appears in the returned workflow.

---

## 2026-09-29 — V-A smartwatch test built: control + A1 (runs `va-control-2026-09-29`, `va-a1-2026-09-29`)

Second A/B pair in this funnel. A3 was not built — no copy exists for it.

- builders: `pagescore/build_va_trackers_over60.py`, `pagescore/build_va_trackers_over60_a1.py`
- V-A engine: `pagescore/va_gadgets_shared.py`   · copy: `pagescore/va_copy.py`
- design: `pagescore/runs/va-control-2026-09-29/design.json` (850:562, 1440) and
  `design_mobile.json` (850:1029, 390 — a **real designed frame**, nothing derived);
  A1 cards at `pagescore/runs/va-a1-2026-09-29/`

### New: a common engine under all four pages

`pagescore/tu_advertorial.py` now holds everything page-agnostic — helpers, colours,
fonts, the zero-CLS font recipe, Lenis, the currency contract, the guard and the LF
write sequence. Both `vb_gadgets_shared.py` and `va_gadgets_shared.py` import it.

**The two live V-B pages were NOT redeployed.** The refactor was proved invisible
first: body (uuids stripped), header, footer and `seo` all byte-identical to what is
deployed, for both V-B steps. Re-checked after every subsequent engine change.

What deliberately stays per-variant: page chrome, the article body and the footer,
because those carry copy and copy is read per design frame by node id. The chrome copy
is in fact identical between the V-A and V-B designs today — sharing it is a real
opportunity, but it would put four live pages' legal text behind one module, so it is
flagged rather than done in passing.

### New standing requirement: Lenis smooth scroll, desktop only

a per-step Lenis block (since deleted) installed into each step's OWN
`settings.custom_html.footer` behind a `<!-- lenis-smooth-scroll -->` marker. Never
funnel-level — this funnel holds four advertorials and funnel-level code ships to all.

Gated on `(min-width: 1024px) and (pointer: fine)` and declines under
`prefers-reduced-motion` — capability, not a UA string. Loaded async from a pinned
jsdelivr version (Lenis is not on cdnjs), fails silent to native scroll. It also
mirrors `body.style.overflow = hidden` into `lenis.stop()` so the legal modals actually
lock the page, which they otherwise would not with Lenis owning the scroll.

**Opt-in** (`build_head(..., lenis=True)`), so adopting the engine could not change the
already-verified V-B pages. They pick it up on their next authorised redeploy.

Measured live:

| | `__lenis` | `data-lenis-active` | script fetched | wheel behaviour |
|---|---|---|---|---|
| V-A control @1440 | yes | 1 | yes | 0 → 318 after 2 frames → 1794 settled (eased) |
| V-A A1 @1440 | yes | 1 | yes | 0 → 357 after 2 frames → 1798 settled (eased) |
| V-B control @1440 | no | — | no | 0 → 0 → 0 (Lenis off, as intended) |
| both V-A @390 | no | — | **no** | native |

At 390 the script is never even requested — the gate declines before loading.

### Images: 8 uploaded, 2 reused

Checked the library first. The five product shots on the live `top-5-fitness-trackers`
page are square studio thumbnails; V-A's are 16:9 lifestyle photos, and they differ by
96–160 mean per-channel, so none was reusable. Uploaded: hero, HLTH Band, Oura, Apple,
Fitbit, Garmin, HLTH-on-wrist, OG.
**Reused:** the TechUnboxed logo, and the author-reply avatar — V-A's `850:898` is
**pixel-identical** (difference 0.0) to V-B's `850:1826`, already in the library.

The brief warned V-A's fills are CROP where V-B's were FILL, and that a crop is art
direction. Measured: both breakpoints are 16:9 and the desktop and mobile renders of
the two CROP nodes are identical (0.2 and 0.3 / 255), so one asset per image is
correct and a second would be pure weight. The hero (FILL) and the HLTH Band product
shot (CROP) are two renders of the *same* source file and differ by 84.5 — two assets.

### Verified live

| check | control | A1 |
|---|---|---|
| HTTP | 200 | 200 |
| `design_diff` @1440, `?country=GB`, `--accept` | 224 OK, 0 MISSING, 0 RETYPED, 1 RESTYLED | 7 OK, 0/0/0 |
| `design_diff` @390 vs the real 390 frame | 216 OK, 0 MISSING, 0 RETYPED, 0 RESTYLED | n/a (lead card is desktop+390, checked at 1440) |
| `qa_runner --skip-psi` | no FAIL | no FAIL |
| shared body identity | asserted at build, 127,673 chars | same |
| currency | 29 tags (8 price / 4 compare / 17 fx) | 35 tags (9 / 4 / 22) |
| 390 | h1 28/32, deck 24/28 Inter Bold, hero 350×197 **radius 0**, product 350×197 radius 6, gutter 20, CTA 350, nav absent, no h-scroll | h1 28/32, hero 350×197, no angle chip, CTA 350, gutter 20 |

Funnel ends with **4 steps**, published, `starting_step_id` still the V-B control.

### Open items

1. **The V-A h1 differs between its own two frames.** 1440 (`850:603`) reads "We tested
   **the** 5 top-rated health trackers for seniors."; the 390 frame (`850:1060`) drops
   "the". Built the 1440 wording, which the brief also specified. One word, one frame —
   needs reconciling in Figma.
2. **A1's card has its own hero and it is a different photograph.** Built the control's
   on explicit instruction, but the premise ("the lead swap does not change the image")
   does not hold: `850:1023` vs `850:606` differ by 47.2/255 — same subject and
   arrangement, different setting (indoors on wood vs outdoors against foliage), and a
   different aspect (720×336 vs 720×405). One-line change to switch.
3. The control's sub-deck is built as an `h2`. Exactly one `h1` and a11y passes, but it
   means the first `h2` on the page is a deck rather than a section heading. Worth a
   decision next time either arm is redeployed.
4. One `design_diff` RESTYLED on the control: `850:610` wraps to 1 line live where the
   design wraps to 2 — font-metric, at the correct 720 column width.

## ⚠️ Renders can go stale, and a write is not proof it shipped (2026-09-29)

Storage and the served page went out of sync on this funnel, in both directions,
and neither a query-string buster nor `published: true` (already true) fixed it.

| | stored | served |
|---|---|---|
| V-A steps | one Lenis, per-step | TWO: per-step **plus** the removed funnel-level block |
| V-B steps | one Lenis, per-step | none, and byte-identical to the pre-deploy render |

The V-A pages keep serving a funnel-level `header_scripts` block that is **0 chars
in the API**, injected at byte ~4,599 (the `<head>`), while responses carry
`Cache-Control: no-cache, no-store` so Cloudflare is not the culprit. Read as a
PUBLISHED SNAPSHOT of funnel-level config: a step CREATE renders fresh, but
funnel-level edits need a real publish cycle.

⚠️ Earlier the same day, step-level `custom_html.header` edits DID render
instantly (the hosted-script swap). These `custom_html.footer` edits did not.
So "step writes always render" is not a rule to rely on either.

**The levers that actually work**, per the lightfunnels skill: a publish toggle
(off then on - funnel-wide, briefly 404s every step) or renaming a step slug
(per step, changes the public url). Both are deliberate acts on live urls, so
neither is something to do unattended once a url has been shared.

**The lesson worth keeping: verify on the RENDERED page, not on the write
succeeding.** A 200 from `updateFunnel` and a correct read-back of `settings`
both passed here while the page served something else entirely.

---

## 2026-09-29 — the stale-render mystery, solved: no product attached

Every edit after the initial build saved to storage and never reached the live
page. Read-backs were correct, republishing did nothing, Cloudflare was sending
`no-cache, no-store`, and the bodies were byte-identical to what we intended.
Joshua identified the cause: **the four steps had no product attached.**

```
                                     product_id      renders edits?
TUB - Over-60s health - Meta (ours)  None (all 4)    no
Google funnels - UK                  prod_8Bx8…XgD   yes
TUB - All smart ring - Meta          prod_8Bx8…XgD   yes
```

One step, one field, nothing else changed:

```
BEFORE  bytes=735338  lenis=0   jsdelivr=0
        product_id = prod_8Bx8YDUlacGSfOHEMCXgD
AFTER   bytes=745861  lenis=52  jsdelivr=1
```

Root cause is in `edits/create-funnel-2026-09-29.py:91` — `create_funnel(...)`
was called with `funnel_steps: ["article_page"]` and no `product_id`, so the
auto-created step had none and the three clones inherited that.

Guard added: `lf_api.assert_steps_renderable(tok, funnel_id, headers)` raises and
names any step without a product. Call it at the end of a build.

**Do not over-generalise.** A sweep of 26 funnels found 12 with product-less
steps, and the dynamic-currency installs on two of them serve exactly what is
stored — so a missing product does not universally block rendering. What is
established: these steps would not render until a product was attached, and did
immediately after. Treat it as required hygiene for new steps and as the first
thing to check when storage and the live page disagree.

### Lenis, as it actually ended up

`header_scripts` on this funnel is **empty** — the funnel-level house block from
`edits/apply-lenis-2026-09-29.py` never persisted. The V-A pages appeared to have
a double install only because they were serving a stale render that still
contained it. Final state is one Lenis per page, from the per-step footer block,
identical across all four.

The per-step block was missing a fix the house block carries: the LF theme sets
`scroll-behavior: smooth` on `<html>`, which fights Lenis for `scrollTop` and
intermittently prevents reaching the bottom of the page. Stock `dist/lenis.css`
does not address it. Added to the per-step Lenis block and pushed to all
four steps:

```css
html:not(.lenis){scroll-behavior:smooth}
html.lenis{scroll-behavior:auto !important}
```

Verified in-browser, not just in the HTML:

| | 1440px | 390px |
|---|---|---|
| `html` class | `lenis` | none |
| `window.__lenis` | present | absent |
| computed `scroll-behavior` | `auto` | `smooth` |
| lenis library requested | yes | **no** |
| scroll to bottom | 9850 of 9850, gap 0 | native |

## 2026-09-29 — the mandatory universal header was missing entirely

Caught by Joshua asking whether the universal header was applied. It was not:
`header_scripts` on this funnel was **0 chars**, so the four pages served
**`gtm=0 posthog=0`** while the reference page served `gtm=2 posthog=32`.

**Both experiments were already built and marked ready against pages with no
PostHog on them.** Neither could ever have recorded an exposure. Nothing surfaces
this — the pages render, QA passes, and the experiment sits in PostHog looking
healthy while collecting nothing.

Installed the canonical block (22,720 chars, `sha1 d03fabfd58`) copied from
`TUB - All smart ring - Meta` (`fun_hLmlmrbjeoGf3UZZvBEHY`) — byte-identical
across that funnel, `TUB- BH Adventorial` and `Google II Broad comparison`.

Because that header carries its own Lenis (unpkg), the per-step Lenis block was
removed from all four footers (16,567 → 11,089 chars each). One library, one rAF
loop, and it converges on house practice.

Verified in-browser at 1440px:

```
posthog  loaded, distinct_id set, token phc_zeYhTnuJUv... = HLTH - Native (194985)
         api_host eu.i.posthog.com, __FF_SRC = "default"
gtm      dataLayer present, google_tag_manager loaded
lenis    active, html.lenis, scroll-behavior auto, 1 library (unpkg)
scroll   10106 of 10106, gap 0
```

194985 is the project both experiments live in (98411 gadgets/B5, 98491
trackers/A1), so the token on the page and the experiments now match. The header
self-selects: `google` → 208779, everything else → 194985 catch-all.

### Local reference has drifted from live — Joshua's call

`Work/Posthog/shared-tracking/workspace-header/lf-header-tracking-universal-v2.html`
is 22,315 chars and differs from the live block in both directions: local has the
newer AiMerce **custom-pixel** build (deferred, `#aimerce-trackjs` guard), live
has the newer **lazy desktop-only Lenis** loader. Neither is strictly ahead.
Which AiMerce build is canonical touches Google Ads conversion tagging
(`gtagCid=AW-17959134159`), so it is not a tidy-up — raised, not acted on.

## 2026-10-02 — store links moved from hlthtrack.co.uk to hlthtrack.com

Joshua's rule: a page running dynamic currency sends its store clicks to
`hlthtrack.com`. The page prices 38 markets off
`hlthtrack.com/api/prices?country=auto`, so a UK-shaped destination contradicts
what the visitor was just shown.

**Not an incident — `.co.uk` resolved correctly.** Measured 2026-10-02:
`.co.uk/products/…` 307s to `.com/products/…`, which 307s to the geo path, and
`fbclid`, `gclid` and every `utm_*` survive both hops unchanged. The cost was one
extra cross-domain round trip on paid mobile traffic, plus a dependency on that
redirect continuing to exist.

Applied across all **8** dynamic-currency pages — the four here plus
`dMs4WkOYD`, `dMs4WkOYD-fx`, `best-fitness-trackers-2026` and
`bh-advertorial-v1-dyn`. 58 links changed; stored and served now agree on every
one, with the currency script still present.

⚠️ `pagescore/dynamic_currency_installs.json` lists only 4 pages and is stale —
it predates the over-60s build, which is why the real count was 8, not 7.

### The prose citation was deliberately left alone

`.co.uk` appears in two roles. The replace matched the **full URL**
(`https://hlthtrack.co.uk/products/wearable-hlth-band`), never the bare host, so
it could not touch the other one:

> Sources. Prices checked 22 September 2026: HLTH Band, hlthtrack.co.uk (£79…)

That is a factual claim about where prices were checked, on the four over-60s
pages (one each). Rewriting it to `.com` would make the citation false rather
than consistent, so it stays. Assertions enforced this: after the swap, remaining
`hlthtrack.co.uk` count had to equal the prose count exactly, and the byte delta
had to equal 2 × links.

**Update, same day:** Joshua confirmed `.co.uk` and `.com` are the same store, so
the source-citation concern above does not apply — rewriting the host keeps the
citation true. The four prose occurrences were changed too. All 62 occurrences
across the 8 pages are now `.com`, and the served pages read
"Prices checked 22 September 2026: HLTH Band, hlthtrack.com (£79)".

**Superseded 2026-10-04.** Per-step Lenis is gone. Smooth scroll ships inside the
funnel-level tracker header that every funnel now carries, so a per-step copy would
be a second library on one scrollTop. `edits/apply-lenis-2026-09-29.py` and both
Lenis block files were deleted, and `tu_advertorial` no longer has a `lenis=` switch.
Reference copies of what IS installed now live in `snippets/`.
