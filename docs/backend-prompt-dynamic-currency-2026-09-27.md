# Backend session prompt — `country=auto` + hosted currency script

Paste the block below into a Claude Code session opened in
`C:\Users\Joshua Reyes\Documents\Codes\Work\Headless Shopify\HLTH NextTheme`.

Written 2026-09-27 from the Lightfunnels side (`LF_V2`), which is the consumer.

---

Two changes to `/api/prices` and the `hlthtrack.com` app. Both exist to stop
Lightfunnels advertorials needing a manual edit every time Shopify gains a market.

## Context — who consumes this and why it matters

Four live Lightfunnels advertorials on `techunboxed.co` localise their prices from
`hlthtrack.com/api/prices`. Two of them take paid traffic right now: the Google
advertorial at `/article/dMs4WkOYD` and the Meta one at
`/smartwatch-review/best-fitness-trackers-2026`.

Each page currently decides the visitor's country **in the browser, from
`Intl.DateTimeFormat().resolvedOptions().timeZone`**, against a hardcoded
IANA-zone → ISO-2 map. On 2026-09-27 Shopify went from 32 to 38 markets, adding
`AR BR CL CO MX PE US`. Every one is in the Americas and the map's only
`America/*` entries were Canada's, so **US, Mexican and Brazilian visitors
auto-detected as GB and were quoted pounds** on pages that had real local prices
waiting. Ecuador had the same gap since launch. Fixing it meant editing four
pages by hand.

That is the problem to remove. The browser should not be guessing a country that
the server already knows.

## Task 1 — support `?country=auto`

`GET /api/prices?products=all&country=auto` (and `?country=auto` on the
single-product form) should resolve the caller's country server-side and return
that market, exactly as if the ISO-2 code had been passed.

The app runs on Vercel, so the country is already on the request as
`x-vercel-ip-country` (`request.headers.get('x-vercel-ip-country')`, or
`request.geo?.country` depending on the runtime API in use — check the Next 16
docs in `node_modules/next/dist/docs/` rather than assuming, per `AGENTS.md`).

Behaviour:

- Resolve to an **enabled Shopify market** → return it, same shape as today.
- Header missing, or the resolved country is **not an enabled market** (a US
  visitor before today, or anyone in a country we do not sell to) → this is
  NORMAL, not an error. Prefer returning the **GB** market with a field naming
  what happened, e.g. `"resolvedCountry": "GB", "requestedCountry": "auto",
  "geoCountry": "JP", "fellBack": true`. Do **not** 400 — a 400 is what the
  current unknown-market path does and the page then shows GBP, which is the
  right outcome but tells the consumer nothing.
- Echo the resolved country in the body either way, so the page can register it
  for analytics instead of re-deriving it.

### ⚠️ The caching trap — this is the part that can do real damage

`country=auto` is **one URL that must return different content per visitor**.
The current response carries `Cache-Control: public, s-maxage=3600,
stale-while-revalidate=86400`, and Vercel's CDN keys on the URL. Ship this
naively and the CDN will serve **one country's prices to every other country** —
German euros to Americans, Philippine pesos to Britons.

That failure is worse than the bug being fixed: it is intermittent, depends on
which visitor warmed the cache in which region, and is close to unreproducible
from one desk.

So `country=auto` must do one of:

1. `Cache-Control: private, no-store` (payload is ~6 KB country-scoped — this is
   the simple, safe default), or
2. stay cacheable but `Vary: x-vercel-ip-country` **and** be verified to
   actually segment on the Vercel CDN, not just to send the header.

Explicit `?country=XX` requests keep the current caching — they are already
correctly keyed by URL. Do not change them.

## Task 2 — host the browser script at a stable URL

Serve the currency script from the app so the Lightfunnels pages can load it
instead of embedding it:

```html
<script src="https://hlthtrack.com/dynamic-currency.js" defer></script>
```

Source to publish: `snippets/dynamic-currency-header-block.html` in the `LF_V2` repo
(root). It is an HTML fragment — strip the surrounding comment banner and
`<script>` tags and publish the JS body. Ask for the current file; do not
reconstruct it.

- `public/dynamic-currency.js` is fine. Confirm `proxy.ts` does not rewrite or
  404 it — that file has host-keyed rules (`isPublicHost`) which already surprise
  people.
- `Content-Type: application/javascript; charset=utf-8`.
- **Do not send `immutable` or a year-long `max-age`.** The entire point is that
  one deploy updates every page, so it must actually propagate. Something like
  `public, max-age=300, s-maxage=3600, stale-while-revalidate=86400`.
- No CORS headers needed — a classic `<script src>` is not a CORS request. The
  script's own `fetch` calls to `/api/prices` and `/api/fx` are already
  origin-locked to `techunboxed.co` and must stay that way.

Once this URL is live, the Lightfunnels side swaps four page headers to the tag
above in one pass. **Tell the LF_V2 side when it ships** — until then the pages
keep their embedded copy, and pointing them at a 404 would drop every non-UK
visitor back to pounds.

## Do NOT change

These are consumed by live pages and a change breaks them silently:

- The existing request forms: bare, `?country=XX`, `?handle=X`, `?products=all`,
  `?products=all&country=XX`.
- Both response shapes — single-product `{handle,title,markets,byCurrency}` and
  `products=all` `{generatedAt,missing,products,errors}`.
- Field names and types. `amount`/`compareAt` are **strings**; `formatted` is
  Shopify's own per-market string the pages render verbatim; `available:false`
  means the page keeps its GBP fallback; `multiPriced` means `amount` is the
  cheapest variant and the page must say "from"; `inconsistent` on a `byCurrency`
  row flags markets sharing a currency at different prices (currently EUR, where
  Croatia is €60.65 against €79 — deliberate).
- The origin lock on both endpoints.
- 400 on an explicitly-requested unknown market. Pages rely on it failing safe.

## Verification before calling it done

```bash
npx tsc --noEmit && npm run lint          # both must exit 0; there is no test runner
```

Then, against a preview deployment:

1. `?products=all&country=GB` — unchanged shape, unchanged caching.
2. `?products=all&country=auto` — returns a market, echoes the resolved country.
3. `?products=all&country=auto` **from two different countries** — different
   currencies come back. A VPN or a `curl` with a spoofed `x-vercel-ip-country`
   proves the resolution; proving the CDN does not cross-serve needs two real
   regions, or `no-store`.
4. `?products=all&country=US` — still 200, `$74.95` (US went live 2026-09-26).
5. `?products=all&country=ZZ` — still 400 `unknown market`.
6. `curl -I https://<preview>/dynamic-currency.js` — 200, JS content-type, not
   `immutable`.
7. `Origin: https://evil.example` on `/api/prices` — still no
   `Access-Control-Allow-Origin`.

Report which of these you actually ran. Number 3 is the one worth being honest
about, because it is the one that is awkward to test and the one that hurts.

---

# FOLLOW-UP, 2026-09-27 (after the first change shipped)

`country=auto` works correctly, but it **removed all caching and every pageview
now hits Shopify.** Measured against production:

    ?country=auto   x-vercel-cache: MISS, MISS, MISS   generatedAt changes every call
    ?country=PH     x-vercel-cache: HIT,  HIT,  HIT    one generatedAt, 11 minutes old

That is my fault, not a misread of the brief: I asked for `no-store` and you
shipped exactly that. The brief conflated two separate concerns.

- **The CDN must not cross-serve countries.** `no-store` on the RESPONSE solves
  this and must stay. One URL returning per-visitor content is still the hazard.
- **Shopify must not be called per pageview.** `no-store` also threw this away.
  Explicit `?country=XX` is CDN-cached, so Shopify currently sees at most one
  call per country per hour regardless of traffic. Under `auto` it would see one
  per pageview, on pages taking paid traffic, against Storefront API rate limits.

## The fix: cache at the ORIGIN, not at the edge

Keep the response `private, no-store`. Cache the per-country Shopify result
server-side, keyed by country, ~3600s - Next 16 `fetch(..., { next: {
revalidate: 3600, tags: ['prices', 'prices:' + cc] } })` or the equivalent
`use cache` / `cacheLife` form. Read the Cache Components guidance in
`node_modules/next/dist/docs/` rather than assuming the API; this repo is Next 16
and `fetch` is NOT cached by default.

Then `auto` resolves the country, reads a warm server cache, and returns an
uncacheable response. Shopify load returns to one call per country per hour.

**Smaller alternative if that is awkward:** add `GET /api/geo` returning just
`{"country":"PH"}`, uncached and ~20 bytes. The page calls it, then calls the
existing CDN-cached `?country=PH`. Two round trips, but today's caching is
preserved exactly and nothing about `/api/prices` changes.

## Verify

Three `?country=auto` calls a few seconds apart should return the **same**
`generatedAt` (served from the origin cache) while still carrying
`Cache-Control: private, no-store` and `x-vercel-cache: MISS`. Same `generatedAt`
with `MISS` is the goal: the EDGE is not caching, the ORIGIN is.

## Status on the Lightfunnels side

The pages are being moved to `hlthtrack.com/dynamic-currency.js` now, but they
still call `?country=XX` and keep full CDN caching. **Do not publish a version
that uses `country=auto` until the origin cache is in place** - it would put a
Shopify call on every pageview of two paid-traffic advertorials.

---

# HANDOFF 2, 2026-09-27 — publish the `country=auto` client

Your API half is done and verified from this side:

    ?products=all&country=auto  ->  resolvedCountry=PH geoCountry=PH
                                    fellBack=false  ->  PHP2,450.00

The remaining half is the BROWSER SCRIPT, which now lives in your repo. The
hosted copy is still the pre-auto version - `Last-Modified: Sun, 27 Sep 2026
00:34:59 GMT`, 105 timezone rows, zero `country=auto` - because it was published
before this was written.

## One file to copy

    FROM  C:\Users\Joshua Reyes\Documents\Codes\Work\LF_V2\snippets/dynamic-currency-header-block.html
    TO    C:\Users\Joshua Reyes\Documents\Codes\Work\Headless Shopify\HLTH NextTheme\hlth-shopify-frontend\public\dynamic-currency.js

Strip the leading `<!-- ... -->` comment banner and the enclosing `<script>` /
`</script>` tags; publish the JS body, same as last time. Then deploy. **No
Lightfunnels page changes** - all four advertorials already load the hosted url,
which is the entire reason it was hosted.

## What changed in it

- **The 105-row IANA timezone map is DELETED**, along with `TZ_PREFIX` and the
  `Intl...resolvedOptions().timeZone` lookup. 14,549 -> 11,362 bytes. This is the
  point of the exercise: that map had no `America/*` rows except Canada's, so
  when Shopify went 32 -> 38 markets every new market was quoted in pounds.
- **`?country=auto` when there is no override**, and it reads `resolvedCountry`
  from your response rather than re-deriving anything.
- **An explicit `?country=XX` still pins that country**, deliberately, because
  that url is shared-cacheable while `auto` is `no-store`. QA links and any ad
  link pinning a market therefore cost the origin nothing.
- **PostHog now registers `funnel_country_source` (`param`|`geo`) and
  `funnel_country_fellback`**, so an unsold-country fallback is visible in
  analytics instead of looking like a GB visitor.
- ⚠️ **The script no longer hides anything.** It used to hide tagged figures as
  its first action, which only worked while it was inline in `<head>`. Loaded
  with `defer` it runs AFTER first paint, so hiding there would hide prices the
  visitor can already see and then reveal them - a flicker, not flash
  prevention. Anti-flash is now owned by a small inline stub in the page tag
  (`snippets/dynamic-currency-page-tag.html` in LF_V2), which is the only part that runs
  before paint. **Do not re-add hiding to this file.**

## Tested here, against real payloads

The actual file was run against live `/api/prices` and `/api/fx` responses with
a minimal DOM. All assertions pass:

| case | result |
|---|---|
| no `?country=` | requests `country=auto`, honours `resolvedCountry` -> PHP2,450 / PHP4,900 / 50% |
| `data-price-handle="hlth-arm-band"` | PHP465 |
| `hlth-care-plus` without `data-price-from` | refused, stays GBP7.95 |
| `hlth-care-plus` with `data-price-from` | PHP244.95 (its own monthly, not the yearly PHP2,460.95) |
| unknown handle | keeps its GBP text |
| `?country=PH` override | uses the cacheable per-country url, not `auto` |
| prices endpoint 400 | all 11 tagged figures keep their GBP text |

It has NOT been tested end to end on a live page, because the pages run your
hosted copy. That check is mine to run once you deploy.

## Tell me when it is live

I will then verify on the two paid-traffic pages that prices still resolve, that
`country=auto` is the request actually going out, and that no timezone map
remains in production. Until then the pages keep running the old script, which
works - so there is no rush and no outage if this waits.

⚠️ Note for whoever verifies: `hlthtrack.com/dynamic-currency.js` is a static
asset, so Vercel serves it **regardless of query string** - a `?cb=` buster does
NOT force a fresh copy, and with `stale-while-revalidate=86400` the edge can
serve an old one after a deploy. Check `Last-Modified` and `Age`, not just the
body, before concluding a deploy did not take.
