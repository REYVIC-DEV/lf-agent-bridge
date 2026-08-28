# Product price on a Lightfunnels page

How a page shows **our own product's price** in the visitor's local currency,
taken live from Shopify so the ad can never drift from what checkout charges.

One funnel serves every country — no duplicate pages per market, no feature flag.

- **Script:** [`dynamic-currency-header-block.html`](../../../../dynamic-currency-header-block.html)
- **Converting anything that is *not* our product** (competitor prices, editorial
  sums): [`CURRENCY_CONVERTER.md`](CURRENCY_CONVERTER.md). Different feed,
  different guarantees — do not mix them up.

---

## Two feeds, and getting them the right way round is the whole job

A page calls two endpoints. They are **not** interchangeable, and this is the one
mistake that costs money.

| | **our product** (this doc) | **everything else** |
|---|---|---|
| tag | `data-price="…"` | `data-fx-gbp="79"` |
| endpoint | `hlthtrack.com/api/prices` | `app.hlthtrack.com/api/fx` |
| what it is | the **real Shopify price** for that market | a **mid-market conversion** |
| exact? | **yes — it is what checkout charges** | **no. indicative only** |

⚠️ **Never price our own product through the converter.** It is mid-market, and
Shopify converts at its own rate with per-market rounding — plus many markets
carry a price-list override where the override *is* the price and no conversion
happens at all. A page that converted its own price would quote figures checkout
does not charge.

---

## The feed

```
GET https://hlthtrack.com/api/prices
```

```json
{
  "handle": "…", "title": "…", "generatedAt": "…", "errors": [],
  "markets": [
    { "country": "DE", "name": "Germany", "currency": "EUR",
      "amount": "79.00", "compareAt": "158.00", "discountPct": 50,
      "formatted": "€79.00", "available": true,
      "currencyMismatch": false, "expectedCurrency": "EUR" }
  ],
  "byCurrency": { }
}
```

32 markets at the time of writing. `ACAO: *`, so it is callable from any origin —
unlike the converter, which is origin-locked.

**Use `formatted`, do not format our money yourself.** It is Shopify's own string
for that market, so rounding and symbol placement are already right.

Field rules that matter on the page:

- **`available: false`, or a country absent entirely → no price.** Fall back to
  the GBP text already in the markup. Never substitute a converted figure.
- **`amount` and `compareAt` are strings.** `"79.00" + 1` is the bug that prevents.
- **`discountPct`** drives a "50% OFF" badge.
- **`currencyMismatch`** flags a market whose currency is not what the country
  should use — worth surfacing rather than displaying blindly.

---

## What to tag

Type the normal **GBP** figure as the visible text. That is the fallback every
visitor sees if detection fails, so the page is never blank or wrong — only
un-localised.

```html
<span data-price="price">£79</span>       <!-- the live price       (required) -->
<span data-price="compare">£158</span>    <!-- the was / RRP        (optional) -->
<span data-price="savings">£79</span>     <!-- compareAt − amount   (optional) -->
<span data-price="discount">50%</span>    <!-- the % off            (optional) -->
```

- Tag **every** occurrence — hero, buy box, comparison table, sticky bar, FAQ,
  body copy. All of them are replaced.
- Only the element's **text** is replaced; surrounding markup and styles are
  untouched. Where a figure already sits in a styled `<span>`, put the attribute
  **on that span** rather than nesting another inside it.
- Never put other text inside a tagged element. Write
  `Only <span data-price="price">£79</span> today`, not
  `<span data-price="price">Only £79 today</span>` — the whole text is replaced.
- ⚠️ **`savings` is not `price`.** It is `compareAt − amount`, computed. It only
  *looks* like the price while every market sits at exactly the same discount —
  true today, not a promise. Tag a saving as `savings` or it starts lying
  silently the day one market's discount changes.

### Tagging inside a page body

A Lightfunnels page body is block JSON, and text lives in each block's
`p.content` as HTML.

⚠️ **Match positionally, never find/replace.** One block routinely holds two
figures needing *different* feeds — a headline carrying an editorial sum *and* our
price. Find matches with a regex, then rewrite **right-to-left** so earlier
offsets stay valid.

Three traps, all hit for real:

| trap | what happens |
|---|---|
| `json.dumps` escapes `£` to `£` (`ensure_ascii=True`) | a currency regex over the dumped body matches **nothing at all** |
| `\d{1,3}%` also matches `width:50%` | tags a star-rating **inline style** instead of text — match text only |
| `£[\d,]+` swallows a trailing comma | `"£79, no subscription"` → the comma lands inside the replaced span and disappears on the first write |

Inventory the figures and **assert the count** before writing. A page reaching 50
tagged figures is normal; discovering the tenth one after launch is not.

---

## Installing the script

Paste the full contents of
[`dynamic-currency-header-block.html`](../../../../dynamic-currency-header-block.html)
into the step's **own** custom code — `settings.custom_html.header`, which renders
in `<head>`.

Prefer per-step over funnel-level `header_scripts` unless every step needs it: a
funnel can hold a dozen market-specific advertorials as sibling steps, and
funnel-level code hits all of them.

⚠️ **APPEND to that header, never replace it.** It commonly carries the page's
`@font-face` declarations. Overwrite it and the page silently drops to a fallback
system font — this happened once and went unnoticed because the page still
*looked* finished.

⚠️ **Write a marker so installs are idempotent:**

```html
<!-- dynamic-currency -->
```

Split on the marker, then append. Without one, a second install **appends a second
copy of the script**. Both copies fetch and both write the same nodes, so the
figure a visitor sees depends on which response lands last — and they can differ.

After installing, assert on the result: exactly **1** copy of the script, and the
**same** `@font-face` count as before.

---

## Formatting the script applies

- **Trailing `.00` is trimmed.** `€79.00` → `€79`. A price cell in a comparison
  table can be 44px wide on a 390px screen, where `€268.00` overruns its column by
  ~21px and collides with the next cell. Trimming also keeps our price at the width
  the design was built around. A genuinely fractional price survives untouched —
  `€60.65`, `€9.99`. Handles the de-DE `268,00 €` ordering too.
- **A zero is refused for `data-price`.** `fmt()` returns null for `n <= 0`,
  because a zero in a price renders a free product.
- **Nothing stays hidden.** A reveal timer (2.5s) guarantees the GBP fallback
  appears even if the fetch never returns.
- **A GB visitor sees no flash.** Hiding only happens when the detected country is
  not the default, so UK traffic never has anything to reveal.

---

## QA

No VPN needed — force a country with `?country=`:

| URL | shows |
|---|---|
| `?country=GB` | `£79` / `£158` — untouched |
| `?country=DE` | `€79` / `€158` |
| `?country=FR` | `€79` |
| `?country=AU` | `A$147` / `A$294` |
| `?country=CA` | `CA$119` |
| `?country=HR` | `€60.65` / `€121.30` — intentionally different, see caveats |
| `?country=PH` | `₱2,450` — a price-list override, not a conversion |
| `?country=VN` | `£99` — VN's market currency **is GBP** |
| `?country=US` | `£79` — absent from the feed, so nothing changes |
| no param, UK visitor | `£79` unchanged |

**Pass criteria**

1. Every tagged figure changes; **none still begins with `£`** on a non-GBP market.
2. No blanks, no `NaN`, no `undefined`, no stray `0`.
3. Nothing left hidden after the reveal timer.
4. On GB, nothing is hidden **at 0ms** — a UK visitor must see no flash at all.
5. **No cell overflows its column at 390px.** Check mobile, not desktop: on one
   page at 929px only 2 cells overflowed by 1–2px, while 12 were colliding at
   390px.
6. 0 console errors.

**Precedence:** `?country=` beats timezone, timezone beats the default. For a
single-country ad set, put `country=DE` in the ad's URL-parameters field.

⚠️ **PageSpeed cannot see any of this.** Lightfunnels serves a stripped page to
the `Chrome-Lighthouse` user agent with all custom code removed, so a PSI run
never measures the script. Verify in a real browser.

---

## Caveats

- **A country absent from the feed changes nothing.** It is not `available: false`
  — the lookup simply finds no market, no currency is resolved, and the page
  renders exactly as authored, in GBP.
- **A market can be priced in GBP.** VN is, so a VN visitor sees no conversion
  anywhere on the page. Correct, not a failure.
- **Some markets are priced out of line with their currency neighbours** (HR at
  €60.65 against €79 elsewhere in the euro zone). That is what Shopify charges.
  Confirm it is intended before spending there.
- **Display only, fail-safe.** Timezone detection can be wrong for travellers, but
  a wrong guess degrades to the GBP default and the storefront charges the real
  currency regardless.
- **A new market not switching** must be `available: true` in the feed; if its
  timezone is not in the script's `TZ_CC` map it falls back to the default — add
  the entry.

---

## Troubleshooting

| Symptom | Likely cause |
|---|---|
| Nothing changes, even with `?country=DE` | Script not installed on **this step**, or the element has no `data-price` |
| Only some figures change | An occurrence is untagged — inventory every figure and assert the count |
| An element goes blank and stays blank | It contained extra text besides the figure, or `hlthtrack.com` is blocked. Self-reveals after 2.5s |
| The figure flickers between two values | **Two copies of the script installed** — check for exactly one |
| Page renders in the wrong font after install | The header was **replaced** instead of appended, dropping `@font-face` |
| Our price converts but competitor figures don't | That is the converter, and it is origin-locked — see [`CURRENCY_CONVERTER.md`](CURRENCY_CONVERTER.md) |
| A price shows as `0` or free | Something bypassed `fmt()`'s `<= 0` guard — never let a computed zero reach `data-price` |
