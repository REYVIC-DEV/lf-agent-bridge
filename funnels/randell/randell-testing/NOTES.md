# randell testing (`fun_f1IsXx3YnEA2UD2g91dAv`)

| step | uid | slug | note |
|---|---|---|---|
| 0 | `step_0J0wlCl2Z6O6Hfg1S-wkY` | `bh-advertorial-v1` | entry page (`starting_step_id`) — **not touched** |
| 1 | `step_SmIVoc258ZchgIHKzFlo-` | `bh-advertorial-v1-dyn` | copy of step 0 + dynamic currency |

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
  the guide's spec plus `API.md`'s safety rules, and installed in the step's own
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

## Open

- **Competitor prices have nothing to convert yet.** `[data-fx-gbp]` is implemented
  and tested-by-construction but unused, because the page carries no competitor
  figures as text. Needs either a comparison block added (which competitors, and
  their GBP RRPs) or confirmation that they live in the artwork — in which case
  they cannot be made dynamic without rebuilding those images as text.
