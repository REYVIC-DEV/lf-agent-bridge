# Dynamic Currency on LightFunnels — build & QA guide

Handoff for whoever builds the funnel page. Goal: **one funnel serves every
country** — the displayed price auto-switches to the visitor's local currency,
pulled live from Shopify. No duplicate pages per country, no feature flag.

- **Script:** [`dynamic-currency-header-block.html`](dynamic-currency-header-block.html)
- **Price source:** `https://hlthtrack.com/api/prices` (see [`../../API-PRICES.md`](../../API-PRICES.md))

---

## How it works (30-second version)

1. The script reads the visitor's **country** — from `?country=XX` if present, else
   from the device **timezone**, else defaults to **GB**.
2. It fetches that country's real price from the Shopify-backed API.
3. It replaces the text of any element you tagged with `data-price="…"`.

Because the price comes straight from Shopify, **the ad always matches what
checkout charges**, and it updates automatically when a price changes in Shopify.

---

## Install — 2 steps

### 1. Tag the price elements on the page
Wrap each price in an element with a `data-price` attribute, and **type the normal
UK (GBP) price as the visible text** — that's the fallback everyone sees if
detection fails.

```html
<span data-price="price">£79</span>       <!-- the current price   (required) -->
<span data-price="compare">£158</span>     <!-- the was / RRP price  (optional) -->
<span data-price="discount">50%</span>      <!-- the % off            (optional) -->
```

- Put `data-price="price"` on **every** place the live price appears (hero, buy
  box, sticky bar, FAQ…). All of them get replaced.
- The tag can go on any element (`span`, `div`, `strong`…). Only its **text** is
  replaced — surrounding markup/styles are untouched.
- Don't put other text inside the tagged element (e.g. write
  `Only <span data-price="price">£79</span> today`, not
  `<span data-price="price">Only £79 today</span>`).

### 2. Paste the script
LightFunnels → **Workspace → Settings → Custom code → HEAD**, **after** the
PostHog init. Paste the full contents of `dynamic-currency-header-block.html`.
(It can also live on a single page's custom code if you only want it there.)

That's the whole build. Nothing else to configure.

---

## How to check it works (QA)

You don't need to travel or use a VPN — **force a country with `?country=`**:

| Open this URL | Price should show |
|---|---|
| `…/your-page?country=GB` | **£79.00** |
| `…/your-page?country=DE` | **€79.00** |
| `…/your-page?country=FR` | **€79.00** |
| `…/your-page?country=AU` | **A$147.00** |
| `…/your-page?country=CA` | **CA$119.00** |
| `…/your-page?country=HR` | **€60.65**  (intentionally different — see caveats) |
| `…/your-page?country=VN` | **£99.00**  (intentionally different — see caveats) |
| `…/your-page` (no param, UK visitor) | **£79** (unchanged) |

**Pass criteria:**
1. The tagged price text changes to the currency above.
2. `compare` and `discount` elements (if used) update too.
3. On a non-GB country there's **no long blank flash** — price appears within ~1s.
4. In the browser console, `posthog.get_property('funnel_country')` returns the
   country and `funnel_currency` the currency (confirms it's also feeding
   reporting).

**Timezone check (optional):** change your OS/browser timezone to
`Europe/Berlin`, reload with **no** param → price should show **€79.00**. Set it
back to `Europe/London` → **£79**.

---

## Optional: force a currency from the ad

You normally don't need this — timezone handles per-user detection. But if you run
an ad set that is **single-country**, you can hard-set it so there's zero guessing:
add to the ad's **URL parameters** field:

```
country=DE
```

Order of precedence: `?country=` **wins over** timezone, which wins over the GB
default. Works on Meta, Google, Taboola, Outbrain — any channel with a URL-params
field.

---

## Caveats (read before running ads in a new market)

- **US is not a market.** It's DRAFT in Shopify and returns an error, so US
  visitors fall back to the **GB / £79** display. Don't target the US from this.
- **Croatia (HR €60.65) and Vietnam (VN £99) are priced differently** from their
  currency neighbours — this is real (what Shopify charges), and flagged as
  unresolved in `API-PRICES.md`. The ad will show those exact prices. **Confirm
  the price is intended before spending in HR or VN.**
- **Display only / fail-safe.** Detection is timezone/IP based, so it can be off
  for travellers or locked-down browsers — but a wrong guess always degrades to
  the **GBP default**, never to a broken price, and the storefront charges the
  real currency regardless.
- **New market not switching?** It must exist in the API (`available: true`). The
  32 supported markets are listed in `API-PRICES.md`. If a country's timezone
  isn't in the script's map yet, it falls back to GB — tell the dev to add the
  timezone→country entry.

---

## Troubleshooting

| Symptom | Likely cause |
|---|---|
| Price never changes, even with `?country=DE` | Script not pasted, or pasted **before** `posthog.init`; or price element has no `data-price` attribute. |
| Only some prices change | A price instance is missing the `data-price` tag. Tag every occurrence. |
| Price element goes blank and stays blank | The tagged element contained extra text, or a network block on `hlthtrack.com`. The script self-reveals after 2.5s. |
| Shows £ for a non-UK country | That country's timezone isn't mapped (falls back to GB) — add it to `TZ_CC` in the script, or use `?country=`. |
| `funnel_country` missing in PostHog | PostHog not initialised on the page / script ran before init. |

---
_Price feed and market list: [`../../API-PRICES.md`](../../API-PRICES.md). Script: [`dynamic-currency-header-block.html`](dynamic-currency-header-block.html)._
