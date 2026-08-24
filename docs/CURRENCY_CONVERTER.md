# Dynamic currency converter

How a page converts **any GBP figure that is not our own product's price** into
the visitor's local currency — competitor prices, editorial sums, "£0" cells.

It is a **converter and nothing more**. For our own product, use the Shopify feed
in [`PRODUCT_PRICE.md`](PRODUCT_PRICE.md); that one is exact and matches checkout.
This one is indicative and does not.

- **Script:** [`dynamic-currency-header-block.html`](../dynamic-currency-header-block.html)
  (one script drives both feeds; install and QA harness are in
  [`PRODUCT_PRICE.md`](PRODUCT_PRICE.md))

---

## ⚠️⚠️ Mid-market, and it will not match checkout

Shopify converts at its own rate with per-market rounding, and markets carrying a
price-list override do not use an FX conversion at all — there are 29 overrides on
one product band alone, and for those the override **is** the price.

**Correct for "about €89". Wrong as a promise of what anyone will be charged.**

An exact per-market figure needs the Storefront API with `@inContext(country:)`,
not this.

So: competitor RRPs, "we spent £1,581 testing" sums, and zero-cost cells — yes.
Our own product's price — **never**.

---

## The feed

```
GET https://app.hlthtrack.com/api/fx
```

```json
{
  "base": "GBP",
  "basis": "mid-market",
  "note": "Indicative only. Shopify checkout converts at its own rate and some markets have fixed local prices.",
  "as_of": "2026-08-24",
  "rates": { "AED": 5.010185, "EUR": 1.168156, "GBP": 1, "…": 0 }
}
```

Refreshed daily at **01:15 UTC**, reading the currency list from Shopify Markets
and the rates from an external provider. Cached at the CDN
(`s-maxage=3600, stale-while-revalidate=86400`), so a pageview normally costs
nothing upstream.

### Consumer rules — each one is why the page can fail safe

- **A currency with no rate is omitted, never sent as `null` or `0`.** So the page
  must bail on a non-number rather than multiply: `undefined` gives `NaN`, and a
  `0` renders a free product.
  ```js
  if (typeof rate !== "number" || !isFinite(rate) || rate <= 0) return;
  ```
- **`GBP` is present and is exactly `1`.** Skip the whole pass when the market
  currency is GBP — a UK visitor should trigger no request and see no change.
- **An empty result answers `503`, not `200 {}`.** A consumer cannot tell an empty
  object from "no currencies configured". Treat *any* failure as "leave the GBP
  text alone", which is why every tagged element ships with its GBP figure as
  visible fallback text.
- **`as_of` is the provider's date, not fetch time.** If it stops moving the data
  is stale even though the endpoint still answers — check it before blaming the
  page.

### Only fetch it if the page needs it

```js
if (document.querySelector("[data-fx-gbp]") && cur && cur !== "GBP") { … }
```

Otherwise it is a cross-origin request on every pageview for nothing, plus a
console CORS error on any non-allowlisted host.

---

## ⚠️ CORS: this endpoint is origin-locked

It echoes the caller's origin rather than sending `*`, with `Vary: Origin`, and
allows only the hosts the visitor might actually be on. Measured:

| endpoint | `techunboxed.co` | apex | preview domain (`*.myecomsite.net`) |
|---|---|---|---|
| `/api/prices` (our product) | `*` | `*` | `*` |
| `/api/fx` (this one) | echoed | echoed | **no header — blocked** |

**Consequence for QA: test on the real host.** On a preview domain the conversion
is blocked and fails safe to GBP, which looks identical to "the script is broken".
Our product price still converts there, because that feed sends `*` — so a page
where *only* competitor figures stay in GBP is almost always this, not a bug.

If a new host needs to work, it has to be added to the allowlist on the API side;
the browser sends the exact origin it has, so the apex and `www` are two entries.

---

## What to tag

Put the GBP amount in the attribute and the GBP text in the element. The attribute
is the source of truth for the maths; the text is the fallback.

```html
<span data-fx-gbp="229">£229</span>       <!-- a competitor's RRP -->
<span data-fx-gbp="1581">£1,581</span>    <!-- an editorial sum -->
<span data-fx-gbp="9.99">£9.99</span>     <!-- fractional is fine -->
<span data-fx-gbp="0">£0</span>           <!-- a "no subscription" cell -->
```

Same tagging discipline as the product price — match **positionally**, never
find/replace, because one block often holds both an `fx` figure and a `price`
figure. The three traps (`£` escaping, `width:50%`, comma-swallowing) are in
[`PRODUCT_PRICE.md`](PRODUCT_PRICE.md#tagging-inside-a-page-body).

**Decide what is editorial and leave it alone deliberately.** Not every GBP number
should convert — but be consistent within a sentence. A headline reading
"We Spent £1,581 … The €79 Outsider Won" mixes currencies in one breath and reads
as a bug, so either both convert or neither does.

---

## Formatting

- **Rounded to whole units.** These are indicative; decimals imply precision the
  figure does not have.
- **`£0` converts to a local zero** (`€0`) rather than staying in GBP. Left alone
  it made one table row read `€79 / £0 / €79` — three cells, two currencies, which
  reads as broken. It is formatted directly, **not** through `fmt()`, whose
  `<= 0` guard has to stay in force for `data-price` where a zero would render a
  free product.
- **No approximation marker.** A leading `~` was used at first — `~€268` — so a
  mid-market figure could not be read as a firm quote. It was **removed on
  request**; the figures are still conversions, the page simply no longer says so,
  and rounding is the only remaining signal. Restore it at the `applyFx` write
  site if that ever needs stating again.
- **Watch width.** A converted figure is usually wider than its GBP original.
  Check at **390px**, not desktop: on one page at 929px only 2 cells overflowed by
  1–2px while 12 were colliding at 390px.

---

## ⚠️ The one problem the contract cannot solve

Both feeds are individually correct and still combine into a **misleading
comparison**.

Our price is real, and in several markets it is a price-list override.
Competitor figures are converted at full mid-market. Where the override is much
cheaper than its FX equivalent, the rival converts at full price and we do not, so
the gap shown on the page stops matching the gap in GBP:

| market | our price as % of its mid-market equivalent | page shows | GBP reality | overstated by |
|---|---|---|---|---|
| PH | 37% | 7.9× | 2.9× | **2.7×** |
| ZA | 57% | 5.1× | 2.9× | **1.8×** |
| PL | 65% | 4.4× | 2.9× | **1.5×** |
| HR | 66% | 4.4× | 2.9× | **1.5×** |

The other 26 markets sit at 1.0–1.3×, which is noise. One market runs the other
way and *understates* at 0.8×.

Each figure on its own is defensible — a £229 rival really is about ₱19,275 at
mid-market. The distortion is in the **comparison**, which is a claim about
relative price, so it is an advertising-accuracy question rather than a display
bug. **It cannot be fixed by arithmetic:** our price has to stay the real checkout
figure, and we do not hold rivals' actual local prices — scaling them by our own
override factor would invent prices that do not exist.

Realistic options: disclose it, keep competitor figures in GBP labelled as UK RRP,
or don't run a price-comparison table in those markets. **Decide before spending
in PH, ZA, PL or HR.**

A script in this repo — `funnels/randell/randell-testing/edits/override_gap.py` —
re-derives this table from the two live APIs, so it can be re-checked whenever
prices move. Worth re-running before opening a new market.

---

## Also worth knowing

- **Converted competitor figures are hardcoded snapshots** in `data-fx-gbp`. They
  are what rivals charged when the page was written, and nothing re-checks them.
  If a rival cuts its price, the table is wrong in GBP first and in every currency
  after.
- **CORS is not a security control.** It is enforced by the browser, so it stops
  another *site* reading the response and does nothing about a script, a curl or a
  server. Fine for keeping an endpoint pointed at its one job; never what protects
  anything.
- **This endpoint is public by design.** It returns currency codes and rates —
  no customer, order, revenue or identity data — which is the whole argument for
  it being callable from a funnel page at all.
