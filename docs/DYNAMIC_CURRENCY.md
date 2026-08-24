# Dynamic currency on a Lightfunnels page — build & QA

One funnel serves every country: the figures on the page switch to the visitor's
local currency. No duplicate pages per country, no feature flag.

- **Script:** [`dynamic-currency-header-block.html`](../dynamic-currency-header-block.html)
- **Worked example:** `funnels/randell/randell-testing/` — two steps wired this
  way, with the QA numbers and every trap hit along the way.

---

## Two feeds, and getting them the right way round is the whole job

The page calls **two different endpoints**, and they are not interchangeable.
Mixing them up is the one mistake that actually costs money.

| | **our product** | **everything else** |
|---|---|---|
| tag | `data-price="…"` | `data-fx-gbp="79"` |
| endpoint | `hlthtrack.com/api/prices` | `app.hlthtrack.com/api/fx` |
| what it is | the **real Shopify price** for that market | a **mid-market currency conversion** |
| exact? | **yes — it is what checkout charges** | **no. indicative only** |
| use for | our price, RRP, saving, discount % | competitor prices, editorial sums, `£0` cells |

**`/api/prices` is the only one that may be used for our own price.** It returns
Shopify's own `formatted` string, so the page never formats our money itself and
the ad cannot drift from checkout. When a price changes in Shopify, the page
follows with no redeploy.

**`/api/fx` is a converter and nothing more.** Per
[`HLTHTRACK_API.md`](HLTHTRACK_API.md) it is mid-market, and Shopify converts at
its own rate with per-market rounding — plus 29 markets carry a price-list
override where the override *is* the price and no conversion happens at all. So
it is right for "about €89" and wrong as a promise of what anyone will be
charged. Never point it at our product.

---

## How it works

1. Read the visitor's **country** — `?country=XX` if present, else the device
   **timezone** (`TZ_CC` map), else **GB**.
2. Fetch that country's real price from `/api/prices` and write every
   `[data-price]` element.
3. If any `[data-fx-gbp]` element exists, fetch `/api/fx` and convert those from
   GBP. Skipped entirely when the market is GBP, and skipped when the page has no
   such element — otherwise it is a wasted cross-origin request on every pageview.

Everything degrades to the GBP text already in the markup: unknown country,
offline, CORS failure, 503, missing rate. A wrong guess never produces a broken
price.

---

## Install on the builder

### 1. Tag the figures in the page body

Type the normal **GBP** figure as the visible text — that is the fallback everyone
sees if detection fails.

```html
<!-- ours: real Shopify price -->
<span data-price="price">£79</span>       <!-- the live price      (required) -->
<span data-price="compare">£158</span>    <!-- the was / RRP       (optional) -->
<span data-price="savings">£79</span>     <!-- compareAt − amount  (optional) -->
<span data-price="discount">50%</span>    <!-- the % off           (optional) -->

<!-- anything else denominated in GBP: converted, indicative -->
<span data-fx-gbp="229">£229</span>       <!-- a competitor's RRP -->
<span data-fx-gbp="1581">£1,581</span>    <!-- an editorial sum -->
<span data-fx-gbp="0">£0</span>           <!-- a "no subscription" cell -->
```

- Tag **every** occurrence — hero, buy box, comparison table, sticky bar, FAQ,
  prose. All of them are replaced.
- Only the element's **text** is replaced; surrounding markup and styles are
  untouched. So put the attribute **on an existing styled span** where one exists
  rather than nesting another.
- Never put other text inside a tagged element. Write
  `Only <span data-price="price">£79</span> today`, not
  `<span data-price="price">Only £79 today</span>`.
- **`savings` is not `price`.** It is `compareAt − amount`, computed. It only
  looks like the price while every market sits at exactly 50% off — true today,
  not a promise. Tag a saving as `savings` or it will silently start lying.

⚠️ **Tag positionally, never with find/replace.** A page body is block JSON, and
one block routinely holds two figures needing *different* feeds — a headline
carrying an editorial sum *and* our price. Match with a regex, then rewrite
**right-to-left** so earlier offsets stay valid. Three traps, all hit for real:

| trap | what happens |
|---|---|
| `json.dumps` escapes `£` to `£` (`ensure_ascii=True`) | a currency regex over the dumped body finds **nothing at all** |
| `\d{1,3}%` matches `width:50%` | tags a star-rating **inline style**, not text — match text only |
| `£[\d,]+` swallows a trailing comma | `"£79, no subscription"` → the comma lands inside the replaced span and vanishes on first write |

### 2. Install the script

Paste the full contents of
[`dynamic-currency-header-block.html`](../dynamic-currency-header-block.html)
into the step's **own** custom code (`settings.custom_html.{header}`), which
renders in `<head>`. Prefer this over funnel-level `header_scripts` unless every
step in the funnel needs it — a funnel here can hold a dozen market-specific
advertorials as sibling steps.

⚠️ **APPEND, never replace that header.** It commonly carries the page's
`@font-face` declarations. Overwrite it and the page silently drops to Arial —
this happened once and went unnoticed because the copy still *looked* finished.

⚠️ **Write a marker so the install is idempotent.** Without one, a second install
**appends a second copy of the script**. Both copies fetch and both write the same
nodes, so the figure displayed depends on which response lands last. Split on the
marker, then append:

```html
<!-- dynamic-currency -->
```

After installing, assert on the result: exactly **1** `applyPrices` and the
**same** `@font-face` count as before.

---

## Formatting rules the script applies

- **Trailing `.00` is trimmed.** `€79.00` → `€79`. A price cell in a comparison
  table can be 44px on a 390px screen, where `€268.00` overruns its column by
  ~21px and collides with the next cell. Trimming also keeps our price at the
  width the design was built around. A genuinely fractional price is untouched:
  `€60.65`, `€9.99` survive. Handles the de-DE `268,00 €` ordering too.
- **Converted figures round to whole units** — they are indicative.
- **`£0` converts to a local zero** (`€0`), with no approximation marker. Left in
  GBP it made one table row read `€79 / £0 / €79`, which reads as a bug. It is
  formatted directly, *not* through `fmt()`, whose `<= 0` guard has to stay in
  force for `data-price` where a zero would render a free product.
- **A missing FX rate bails.** The API omits a currency rather than sending `0` or
  `null`; multiplying by `undefined` gives `NaN` and a `0` renders a free product.

---

## QA

No VPN needed — force a country with `?country=`. Values below are what a
correctly wired page shows.

| URL | ours | converted figures |
|---|---|---|
| `?country=GB` | `£79` / `£158` | **untouched**, still GBP |
| `?country=DE` | `€79` / `€158` | `€268`, `€0` |
| `?country=FR` | `€79` | — |
| `?country=AU` | `A$147` / `A$294` | `A$436` |
| `?country=CA` | `CA$119` | — |
| `?country=HR` | `€60.65` / `€121.30` | decimals preserved |
| `?country=PH` | `₱2,450` | `₱19,275`, `₱0` |
| `?country=VN` | `£99` | **nothing converts** — VN is priced in GBP, so the FX pass is skipped |
| `?country=US` | `£79` | **nothing converts** — US is absent from the feed entirely |
| no param, UK visitor | `£79` unchanged | unchanged |

**Pass criteria**

1. Every tagged figure changes; **none still begins with `£`** on a non-GB market.
2. No blanks, no `NaN`, no `undefined`, no stray `0`.
3. Nothing is left hidden — the reveal timer guarantees it after 2.5s.
4. On GB nothing is hidden **at 0ms**: a UK visitor must see no flash at all.
5. No cell overflows its column at **390px**. Check mobile, not desktop — at
   929px only 2 cells overflowed by 1–2px while 12 were colliding at 390px.
6. 0 console errors.

⚠️ **QA on the real host, not the preview domain.** `/api/fx` echoes only the
`techunboxed.co` origins, so competitor conversion is CORS-blocked anywhere else
and fails safe to GBP — which looks like "the script is broken".

⚠️ **PageSpeed cannot see any of this.** Lightfunnels serves a stripped page to
the `Chrome-Lighthouse` UA with all custom code removed, so a PSI run never
measures the script. Use a real browser.

**PostHog** (optional): `posthog.get_property('funnel_country')` and
`funnel_currency` confirm it is feeding reporting. The script guards for PostHog's
absence — some funnels have none, in which case this check simply cannot be met.

---

## Force a currency from the ad

For a single-country ad set, add to the ad's **URL parameters** field:

```
country=DE
```

Precedence: `?country=` beats timezone, timezone beats the GB default. Works on
any channel with a URL-params field.

---

## Caveats — read before running ads in a new market

- ⚠️ **A comparison table can overstate our advantage.** Our price is real and in
  several markets is a price-list **override**; competitor figures are converted
  at full mid-market. Where the override is much cheaper than its FX equivalent,
  the rival converts at full price and we do not, so the gap on the page stops
  matching the gap in GBP:

  | market | ours as % of mid-market | table shows | GBP reality | overstated |
  |---|---|---|---|---|
  | PH | 37% | 7.9× | 2.9× | **2.7×** |
  | ZA | 57% | 5.1× | 2.9× | **1.8×** |
  | PL | 65% | 4.4× | 2.9× | **1.5×** |
  | HR | 66% | 4.4× | 2.9× | **1.5×** |

  The other 26 markets sit at 1.0–1.3×. It cannot be fixed by arithmetic: our
  price must stay the real checkout figure and we do not hold rivals' local
  prices. Decide how to handle it before spending in those four.
  `funnels/randell/randell-testing/edits/override_gap.py` re-derives this table
  from the two live APIs.
- **US is not a market** — DRAFT in Shopify and **absent from the feed**, not
  merely `available: false`. The market lookup finds nothing, so no currency is
  resolved and the FX pass is skipped too: a US visitor sees the page exactly as
  authored, in GBP. Don't target the US from this.
- **HR (€60.65) and VN (£99) are priced differently** from their currency
  neighbours. Real, and what Shopify charges. Confirm it is intended before
  spending there. VN's market currency **is GBP**, so a VN visitor sees no
  conversion anywhere on the page — which is correct, not a failure.
- **Display only, fail-safe.** Timezone detection can be wrong for travellers, but
  a wrong guess degrades to GBP and the storefront charges the real currency
  regardless.
- **New market not switching?** It must be `available: true` in the feed. If its
  timezone is not in `TZ_CC`, it falls back to GB — add the entry.
- **Converted competitor figures are hardcoded snapshots** in `data-fx-gbp`.
  Nothing re-checks them. If a rival cuts its price, the table is wrong in GBP
  first and in every currency after.

---

## Troubleshooting

| Symptom | Likely cause |
|---|---|
| Nothing changes, even with `?country=DE` | Script not installed on **this step**, or the element has no `data-price` / `data-fx-gbp` |
| Only some figures change | An occurrence is untagged. Inventory every figure and assert the count |
| An element goes blank and stays blank | It contained extra text, or `hlthtrack.com` is blocked. Self-reveals after 2.5s |
| Our price converts, competitors do not | `/api/fx` CORS — you are not on a `techunboxed.co` origin |
| Shows `£` for a non-UK country | That timezone is not in `TZ_CC`; add it or use `?country=` |
| The figure flickers between two values | **Two copies of the script installed.** Check for exactly one `applyPrices` |
| Page renders in Arial after install | The header was **replaced** instead of appended, dropping `@font-face` |
| Table cells collide | Check at 390px; a converted figure is wider than the GBP original |

---
_Price feed and market list: `API-PRICES.md` (not in this repo). Converter
contract: [`HLTHTRACK_API.md`](HLTHTRACK_API.md). Script:
[`dynamic-currency-header-block.html`](../dynamic-currency-header-block.html)._
