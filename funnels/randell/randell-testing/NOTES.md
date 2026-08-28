# randell testing (`fun_f1IsXx3YnEA2UD2g91dAv`)

| step | uid | slug | note |
|---|---|---|---|
| 0 | `step_0J0wlCl2Z6O6Hfg1S-wkY` | `bh-advertorial-v1` | entry page (`starting_step_id`) — **not touched** |
| 1 | `step_SmIVoc258ZchgIHKzFlo-` | `bh-advertorial-v1-dyn` | copy of step 0 + dynamic currency |
| 2 | `step_JM0a30ybnkm3hpOE7-lSW` | `techunboxed-uk-v4` | copy of the **live** advertorial entry (`fun_vGqQYxn4H2i_traYYkh4w` `/pb/3`) + dynamic currency, both feeds |

Serves on **both** `www.techunboxed.co` and `99commerce.myecomsite.net`.
This funnel has **no PostHog** — `header_scripts` is empty, so the setup guide's
"paste after the PostHog init" does not apply; the script guards for its absence.

## Log

- `2026-08-24` — **new step `bh-advertorial-v1-dyn`: copy of the entry page with
  dynamic currency.** Created with `createStep` + `updateFunnel` (attach only the
  new step, so siblings survive by omission). `starting_step_id` deliberately
  unchanged — the original is still the live entry page.

  **What was tagged, and what wasn't.** The source page has exactly five money
  figures and **no competitor prices at all** — verified: zero mentions of Whoop,
  Oura, Apple, Fitbit or Garmin, no bare price numbers, and 16 images, so any
  comparison table is baked into artwork.

  | occurrence | tag |
  |---|---|
  | 4x "GET UP TO **£79** OFF HLTH BAND" | `data-price="savings"` |
  | 1x "Special **50% off** coupon…" | `data-price="discount"` |

  **The £79 is the SAVING, not the price** (`compareAt` 158 − `amount` 79). It only
  *looks* like the price because all 32 markets sit at exactly 50% off — checked
  against the API, `discountPct` is 50 in every one, so saving == price everywhere
  today. Tagged `savings` (computed as `compareAt - amount`) rather than `price` so
  it stays correct if a market's discount ever changes; `price` would silently
  start lying.

  **`dynamic-currency-header-block.html` did not exist in the repo** — the setup
  guide references it and `API-PRICES.md`, neither of which is here. Written from
  the guide's spec plus `.claude/skills/lightfunnels/references/CURRENCY_CONVERTER.md`'s safety rules, and installed in the step's own
  `settings.custom_html.header` (per-step, not funnel-level `header_scripts`).

  **Two feeds, deliberately separate:**
  - our product → `hlthtrack.com/api/prices`, the real Shopify per-market price.
    Uses the API's own `formatted` string, so we never format our own money.
  - competitors → `app.hlthtrack.com/api/fx`, mid-market, driving `[data-fx-gbp]`.
    Indicative only — never for our price.

  **CORS is the operational catch.** Measured:

  | endpoint | techunboxed.co | apex | 99commerce.myecomsite.net |
  |---|---|---|---|
  | `/api/prices` | `*` | `*` | `*` |
  | `/api/fx` | echoed | echoed | **no header — blocked** |

  So competitor conversion only works on the techunboxed origin, and `/api/prices`
  is slated to become restricted the same way. **QA on the techunboxed URL, not the
  preview domain.** Everything fails safe to the GBP text already in the markup.

  FX is only fetched when a `[data-fx-gbp]` element exists — otherwise it was a
  wasted cross-origin request on every non-GB pageview and a console CORS error on
  the preview domain. Verified: 0 FX requests, 0 console errors, price still
  converts.

  **QA matrix — matches the setup guide's expected table exactly:**

  | `?country=` | shown | | `?country=` | shown |
  |---|---|---|---|---|
  | GB | £79.00 | | AE | AED 385.00 |
  | DE | €79.00 | | HR | €60.65 (flagged odd) |
  | FR | €79.00 | | VN | £99.00 (flagged odd) |
  | AU | A$147.00 | | US | £79 (DRAFT → GBP fallback) |
  | CA | CA$119.00 | | ZZ (invalid) | £79 (default) |

  All four CTAs switch together, discount stays 50%, nothing left hidden, 0 console
  errors on techunboxed.

- `2026-08-25` — **`techunboxed-uk-v4`: the live advertorial entry copied in, with
  BOTH feeds live and every figure on the page converting.** This page answers the
  open question below: unlike `bh-advertorial-v1` it carries its competitor
  comparison as **text**, so `[data-fx-gbp]` finally has something to convert.

  Copied from `fun_vGqQYxn4H2i_traYYkh4w` `/pb/3` (slug `xI7j8mDEB`). Source
  integrity asserted **before** copying — `hlthtrack.co.uk`x15, `amazon.com`x8,
  `aff-`x0, in-body `<style>`x0, `tu-overlay`x6, and 6 Inter `@font-face`
  declarations in `custom_html.header` (without those the copy renders in Arial —
  see the step-1 defect below). The live funnel was **read only**.

  **Every money figure on the page is tagged: 50 of 50.**

  | what | tag | n |
  |---|---|---|
  | our price (buy box x2, table Year 1 + 2-Year Total, H1, subhead, 4x prose) | `data-price="price"` | 11 |
  | struck-through RRP x2 + prose "down from" | `data-price="compare"` | 3 |
  | "UP TO 50% OFF", "UK-exclusive 50% OFF" | `data-price="discount"` | 2 |
  | competitor prices, spec bullets, the GBP1,581 test spend, GBP0 cells | `data-fx-gbp` | 36 |

  Verified live: 11/3/2/36 elements found in the DOM, and on `?country=DE`
  **zero** figures still begin with a GBP sign — no blanks, no `NaN`, no
  `undefined`.

  **Two feeds, and which figure belongs to which is the whole design.** Ours comes
  from `hlthtrack.com/api/prices` (real Shopify, must match checkout, uses the
  API's own `formatted` string). Everything else goes through
  `app.hlthtrack.com/api/fx`, which is mid-market and, per `.claude/skills/lightfunnels/references/CURRENCY_CONVERTER.md`, "correct for
  'about EUR89'; wrong as a promise of what the customer will be charged" — so
  those render with a leading `~`. Our own price never gets the prefix.

  **Tagging was positional, never find/replace.** Three blocks hold two figures
  needing *different* feeds — the H1 carries the GBP1,581 test spend *and* our
  GBP79 — so a substring replace would have tagged the wrong one. Matches are
  rewritten right-to-left so earlier offsets stay valid. Two earlier scans had
  already shown how this bites: a `\d{1,3}%` pattern matched `width:50%` inside
  inline **styles** on the star-rating blocks, and `json.dumps` escapes every GBP
  sign to `\u00a3`, so a currency regex over the dumped body finds nothing at all.
  A third trap: `[\d,]+` swallowed the comma in "GBP79, no subscription", and
  tagging that span would have deleted the comma the moment a price was written.

  **GBP0 subscription cells convert too.** Left in GBP, one table row read
  "EUR79 / GBP0 / EUR79" — three cells, two currencies, looks broken. They are
  formatted directly rather than through `fmt()`, whose `<= 0` guard has to stay in
  force for `data-price` where a zero really would render a free product, and they
  take no `~` because nothing about zero is approximate.

  **A rendering bug the desktop viewport hid.** At 929px only 2 cells overflowed,
  by 1-2px. At **390px — actual traffic — 12 figures overran a 44px price cell by
  ~21px** and collided into `~EUR268.00~EUR268.00~EUR535.00`, unreadable. Fixed by
  trimming a trailing `.00`, which carries no information on a rounded indicative
  figure: 12 overflows -> 1, by 2px. It also returns our own price to `EUR79` /
  `EUR158`, the exact widths the design was built around. A genuinely fractional
  price is untouched — HR still shows `EUR60.65` and `EUR121.30`, and Fitbit's
  `GBP9.99/mo` keeps its decimals. The de-DE `268,00 EUR` ordering is handled too.

  **QA on `www.techunboxed.co/randell-testing/techunboxed-uk-v4`:**

  | `?country=` | ours | compare | everything else |
  |---|---|---|---|
  | GB | `GBP79`, never hidden at 0ms | `GBP158` | **untouched** — GBP1,581 and GBP0 as authored |
  | DE | `EUR79` | `EUR158` | `EUR1,847` `EUR466` `EUR268` `EUR419`, `EUR0` |
  | AU | `A$147` | `A$294` | `A$436` `A$684` `A$417` |
  | HR | `EUR60.65` | `EUR121.30` | decimals preserved |

  DE/AU/HR match the setup guide's expected figures exactly. 0 console errors, no
  horizontal page scroll, 1 residual 2px cell overflow.

  **Two defects found on step 1 while refreshing it** — the repo holds one script
  installed onto two steps, so leaving step 1 on the older copy would have meant
  the file no longer described what was deployed:

  1. **Two copies of the script were running.** The first install wrote no marker,
     so the marker-split appended a second copy instead of replacing it. Both
     fetched and both wrote the same nodes, so the displayed figure depended on
     which response landed last — and only one copy had the `.00` trim. A byte map
     of the header proved the old copy was the whole `0..7254` range.
  2. **That step had `@font-face` x0 while its source has x7** — the copy had been
     rendering in Arial since it was made, so it was never 1:1.

  Both fixed in one write, rebuilding the header as *source header + marker + one
  script*. Verified after: exactly 1 `applyPrices` and 7 font faces on step 1, 1
  and 8 on step 2, and Inter now measurably renders — canvas advance 240.4 against
  a 208.9 nonsense-font control, because `document.fonts` and
  `document.fonts.check()` both lie here, one blind to cross-origin CSS and the
  other true for undeclared families. All 4 `savings` tags still render `EUR79`.

  Installs are now idempotent by marker, so re-running swaps the script instead of
  stacking a second copy.

## Open

- ~~**Competitor prices have nothing to convert yet.**~~ **Answered** by
  `techunboxed-uk-v4` (2026-08-25), which carries its comparison as text — 36
  figures now convert. Still true of `bh-advertorial-v1`, where any comparison
  table is baked into artwork.

- ~~**The `~` prefix is an editorial call.**~~ **Removed on request 2026-08-25**,
  deployed to both steps and verified live: 0 tildes on the page. The figures are
  still mid-market conversions, so they remain indicative and will not match what
  a rival charges locally — the page simply no longer says so, and rounding to
  whole units is the only remaining signal. This makes the distortion item below
  matter more, not less, because a converted rival RRP now reads as a firm price.
  Restore the prefix at the `applyFx` write site if that ever needs stating.

- ⚠️ **The comparison table overstates our price advantage in override markets.**
  Found from a PH pageview showing `~PHP133,070`. Our price is a real Shopify
  figure and in several markets that is a **price-list override**, not an FX
  conversion — `.claude/skills/lightfunnels/references/CURRENCY_CONVERTER.md` warns there are 29 of them. Competitor figures, by
  contrast, are converted from GBP at full mid-market. Where the override is much
  cheaper than the FX equivalent, the rival is converted at full price while we
  are not, and the gap on the page stops matching the gap in the UK:

  | market | our price | as % of its mid-market equivalent | table shows | UK reality | overstated by |
  |---|---|---|---|---|---|
  | PH | PHP2,450 | 37% | 7.9x | 2.9x | **2.7x** |
  | ZA | ZAR980 | 57% | 5.1x | 2.9x | **1.8x** |
  | PL | PLN260 | 65% | 4.4x | 2.9x | **1.5x** |
  | HR | EUR60.65 | 66% | 4.4x | 2.9x | **1.5x** |

  The other 26 markets sit at 1.0-1.3x, which is noise. EC runs the other way
  (USD135 = 125% of mid-market, so it *understates* at 0.8x).

  Every individual figure is defensible — a GBP229 Whoop really is about
  PHP19,275 at mid-market, and it is marked `~`. The distortion is in the
  **comparison**, which is a claim about relative price, so this is an
  advertising-accuracy question rather than a display bug. It cannot be fixed by
  arithmetic: our price has to stay the real checkout figure, and the rivals' real
  local prices are not something we hold. The options are to disclose, to leave
  competitor figures in GBP labelled as UK RRP, or not to run these four markets
  against this table. **Decide before spending in PH, ZA, PL or HR.**

- **Competitor GBP figures are hardcoded in `data-fx-gbp`.** They are a snapshot of
  what rivals charged when the page was written, and nothing re-checks them. If a
  rival cuts its price the table is wrong in GBP first and in every currency after.

- **The GBP1,581 test spend converts as an indicative figure.** It is a real sum we
  paid in GBP, so `~EUR1,847` is a conversion of a true statement rather than a
  claim we spent euros. Converting it was a deliberate call (the alternative left
  one headline reading "GBP1,581 ... EUR79", which looks like a bug).

- **This funnel has no PostHog**, so the setup guide's pass criterion 4
  (`posthog.get_property('funnel_country')`) cannot be met here — `window.posthog`
  is `undefined` on both steps. The script guards for it; 0 console errors
  confirmed. Reporting attribution would need PostHog added to the funnel first.
