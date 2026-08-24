# API guidelines

Every HTTP route this app exposes, how each one authenticates, and the rules for adding another.

This dashboard is **gated by default**: `proxy.ts`'s matcher covers everything except a short,
deliberate exemption list, so a new route under `app/api/` is behind the session cookie unless
somebody decides otherwise. That default is the point. This file exists so the next exemption is a
decision with a written test behind it, rather than a line somebody added to make a fetch work.

---

## The routes that exist

| Route | Methods | Who calls it | How it authenticates |
|---|---|---|---|
| `/api/auth/login`, `/api/auth/login/google` | GET | a person signing in | n/a — starts the OAuth flow |
| `/api/auth/callback`, `/api/auth/callback/google` | GET | Google | the OAuth code exchange |
| `/api/auth/logout` | POST | a signed-in person | the session cookie |
| `/api/cron/dispute-alerts` | GET | Vercel Cron | `Authorization: Bearer $CRON_SECRET` |
| `/api/cron/judgeme` | GET | Vercel Cron | `Authorization: Bearer $CRON_SECRET` |
| `/api/webhooks/trustpilot` | GET, POST | Trustpilot | shared secret **in the query string** (see below) |
| `/api/webhooks/shopify-disputes` | GET, POST | Shopify | HMAC-SHA256, `SHOPIFY_DISPUTES_WEBHOOK_SECRET` |
| **`/api/fx`** | **GET, OPTIONS** | **the techunboxed.co advertorial** | **none — public by design** |

Everything else in the app is a page behind `requireViewAccess`, not an API.

---

## Four categories, four different rules

The exemption list in `proxy.ts` is not one idea. Each entry is there for its own reason, and
mixing them up is how a hole gets opened by analogy.

**1. `api/auth/*` — exempt or it deadlocks.** Gating the sign-in endpoints behind sign-in is a
redirect loop. Nothing to decide.

**2. `api/webhooks/*` — exempt because the gate would fail SILENTLY.** A third-party sender has no
cookie, so a gated webhook receives a **307 to `/login`**, and a redirect is not an error. The
sender's dashboard shows the delivery as having gone somewhere, the route never executes, and the
only symptom is an alert that never arrives.

⚠️ **So every route under it must authenticate itself, and must FAIL CLOSED when its secret is
unset.** An unconfigured webhook rejects everything. One missing environment variable must never
turn a route into an open relay.

⚠️ `/api/webhooks/trustpilot` carries its secret **in the URL**, and that is forced rather than
chosen: Trustpilot's Integrations screen offers a bare URL field and no header configuration. The
consequences are written into that file — the token is in Vercel's request logs, the comparison is
length-then-constant-time, and the endpoint is deliberately worth almost nothing to an attacker. If
that route ever gains a side effect, the auth has to be revisited **first**.

**3. `api/cron/*` — exempt because Vercel Cron holds no cookie.** Authenticates with
`Authorization: Bearer $CRON_SECRET`. ⚠️ A bad token gets a **404, not a 401**: an unauthenticated
prober learns nothing about whether the path exists.

**4. `api/fx` — exempt because the CALLER IS A THIRD-PARTY PAGE.** The only public *data* route.
See below, because this is the category most likely to grow and the one worth being strict about.

---

## Adding a public route

The test is **what it returns**, never how convenient the exemption would be.

`/api/fx` returns a list of currency codes and mid-market FX rates. There is no customer, order,
revenue, traffic or identity figure in it, so a stranger reading it learns nothing that is ours.
That is the whole argument for exempting it. Apply the same test to anything new, and if the answer
is "it would be fine as long as nobody looks too closely", the answer is no.

Then:

- **Keep the exemption narrow.** `api/fx`, not `api/public/*`. A prefix makes the next public
  endpoint an act of forgetting instead of a decision, which is exactly the property being
  protected. One line in the matcher per deliberate route.
- **Say so at the top of the route file.** `app/api/fx/route.ts` opens by stating that it is public,
  why that is safe, and that nothing needing protection may be added to the response. That note is
  the thing a future edit has to argue with.
- **Never return internal error detail.** `WarehouseError` carries the view name and can carry a
  PostgREST message. A public route answers `{ "error": "rates unavailable" }` and logs the rest.
- **Cache it.** `/api/fx` uses `s-maxage=3600, stale-while-revalidate=86400`. Serving from our own
  CDN is usually the *reason* the route exists: it turns one request per pageview into one request
  per day against whatever sits upstream.

### CORS

⚠️ **CORS is not a security control.** It is enforced by the browser, so it stops another *site*
embedding a response and does nothing whatsoever about a script, a curl, or a server. It is fine to
rely on for keeping an endpoint pointed at its one job. It is never what protects a secret — if a
response needs protecting, it needs auth, not an allowlist.

Two mechanics that are easy to get wrong:

- **Echo the caller's origin, do not send `*`.** A wildcard lets any site read it.
- ⚠️ **`Vary: Origin` is required whenever you echo.** Without it a CDN can hand the header it
  cached for one origin to a different one, which either leaks access or blocks a legitimate caller
  depending on which was cached first.
- **Allow every host the visitor might actually be on.** `/api/fx` allows `www.techunboxed.co` *and*
  the apex, because the browser sends the exact origin it has. A CORS rejection surfaces as a
  console error in someone else's page, not as anything visible from here.

---

## Writing to the warehouse

Routes and Edge Functions do not write to `app.*` directly, and cannot: **PostgREST exposes only
`public`**.

- Tables live in `app`, RLS on, no policies, so the service role is the only thing that can read
  them.
- `public` holds exactly two kinds of object: `dash_*` read views and `app_*` write functions.
- Every writer goes through an `app_*` RPC — there are around twenty (`app_cs_shift_start`,
  `app_trustpilot_review_upsert`, `app_shopify_dispute_upsert`, `app_fx_rate_upsert`, …).

⚠️ **A missing wrapper fails quietly.** `app.cs_shift_backfill_eod_ends()` was unreachable for a
while and the caller reported `eod_recovered_days: null` — a backfill that never runs looks
identical to one with nothing to do. Print what a writer wrote, and check the number.

**Validate in the RPC, not only in the caller.** The guards belong where every caller meets them:
refuse an empty list that would wipe a catalogue, refuse a partial capture whose parts do not sum,
refuse a zero that would render as a real figure. Raise with the offending values in the message —
a log that names only a constraint gets the same broken input retried.

---

## Reading the warehouse

- `lib/db.ts` (`fromView`) is the reader. It is `server-only`, paged, and **throws rather than
  returning empty**, so a failed read renders an error instead of a page of zeros.
- Reads are cached 300s and tagged, so `revalidateTag` clears the lot.
- Numbers arrive from PostgREST as **strings** for any Postgres `numeric`. Put them through `n()`
  from `lib/metrics.ts`; `"82.95" + 1` is the bug that prevents.
- ⚠️ The service-role key bypasses RLS on the entire raw event stream. It stays server-side and is
  never `NEXT_PUBLIC_*`.

---

## Scheduled work: Vercel Cron or a Supabase Edge Function?

Both are in use, and the split is not arbitrary.

- **Edge Function** when the job talks to a third party, runs long, or self-chains — `posthog-sync`
  runs ~110s per invocation, `fx-sync` and `shopify-disputes-sync` hold API credentials. Triggered
  by pg_cron.
- **Vercel Cron route** when the job is a short piece of app logic that wants this app's libraries.
- **Plain SQL on pg_cron** when no network call is needed at all — `cs-shift-eod-backfill-hourly`
  calls an `app` function directly, with no HTTP hop, no anon key in a migration, and none of the
  ambiguity below.

⚠️⚠️ **`net.http_post` IS DISPATCH-ONLY.** A pg_cron job goes green when the request is **accepted**,
not when the sync succeeds. A green job history proves nothing. Read the freshness view the job
feeds — `dash_coverage`, `dash_dispute_freshness`, `dash_shop_currency_coverage` — and have the
function answer a non-200 on failure so its own logs carry the truth.

⚠️ **The bearer token in a pg_cron command must not be written into a migration file.** Every
existing job embeds a literal service key in `cron.job.command`. Derive a new job's command from an
existing one *inside the database* instead, so the secret never reaches a file, a terminal, or a
chat:

```sql
select cron.schedule('my-job', '15 1 * * *',
  replace(command, 'posthog-experiments-sync', 'my-function'))
from cron.job where jobname = 'cro-posthog-experiments-hourly';
```

---

## `/api/fx` in particular

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

⚠️⚠️ **MID-MARKET, AND IT WILL NOT MATCH CHECKOUT.** Shopify converts at its own rate with per-market
rounding, and markets carrying a price-list override do not use an FX conversion at all — there are
29 overrides on the band alone, and for those the override **is** the price. Correct for
"about €89"; wrong as a promise of what the customer will be charged. An exact per-market figure
needs the Storefront API with `@inContext(country:)`.

Consumer notes:

- **A currency with no rate is omitted, never sent as `null` or `0`**, and named in `missing`. Page
  JS multiplies by whatever it receives, and a zero renders a free product.
- **`GBP` is present and is exactly `1`.** It is never fetched from the provider.
- **An empty result answers `503`, not `200` with `{}`** — a consumer cannot tell an empty object
  from "no currencies configured", and would show nothing rather than falling back to GBP.
- **`as_of` is the provider's date, not our fetch time.** If it stops moving, the sync is stale even
  though the endpoint still answers.

Filled daily at **01:15 UTC** by the `fx-sync` Edge Function (pg_cron `fx-sync-daily`), which reads
the currency list from Shopify Markets and the rates from `open.er-api.com`. Health lives in
`public.dash_shop_currency_coverage`: `missing_rate > 0` means the advertorial is offering a
currency it cannot convert.
---

## How a Lightfunnels page uses this

Everything above describes the dashboard app. From a funnel page we consume
**exactly one route from this file** — `/api/fx` — plus `/api/prices`, which is
documented separately in `API-PRICES.md` (not in this repo). The build guide is
[`DYNAMIC_CURRENCY.md`](DYNAMIC_CURRENCY.md).

**The split is the important part:**

| | `/api/prices` | `/api/fx` (this file) |
|---|---|---|
| what it is | our product's **real Shopify price** per market | a **mid-market currency converter** |
| page tag | `data-price="…"` | `data-fx-gbp="79"` |
| exact? | **yes — it is what checkout charges** | **no. indicative only** |
| used for | our price, RRP, saving, discount % | competitor prices, editorial sums, `£0` cells |

`/api/fx` is **only ever a converter**. It must never drive our own product
price: the note in `/api/fx in particular` above — mid-market, per-market
rounding, 29 price-list overrides where the override *is* the price — is exactly
why. A page that converted its own price with it would quote figures checkout
does not charge.

### The consumer rules, as they land on a page

The guarantees stated above are what let the page fail safe, so the page-side code
mirrors each one:

- **A currency with no rate is omitted, never `0` or `null`.** The page bails on a
  non-number instead of multiplying — `undefined` gives `NaN`, and a `0` renders a
  free product.
- **`GBP` is present and exactly `1`.** The page skips the whole FX pass when the
  market currency is GBP, so a UK visitor triggers no request and sees no change.
- **An empty result answers `503`, not `200 {}`.** The page treats any failure as
  "leave the GBP text alone", which is why every tagged element ships with its GBP
  figure as visible fallback text.
- **`as_of` is the provider's date.** A stale date means the sync is stale even
  though the endpoint answers — worth checking before blaming the page.

Only fetched when a `[data-fx-gbp]` element exists on the page. Otherwise it is a
cross-origin request on every pageview for nothing, and a console CORS error on
any non-allowlisted host.

### CORS, measured

The `Allow every host the visitor might actually be on` rule above has a
consequence worth writing down, because it decides where QA is valid:

| endpoint | `techunboxed.co` | apex | preview domain (`*.myecomsite.net`) |
|---|---|---|---|
| `/api/prices` | `*` | `*` | `*` |
| `/api/fx` | echoed | echoed | **no header — blocked** |

So competitor conversion works **only** on the techunboxed origins. On a preview
domain it is blocked and fails safe to GBP, which looks identical to "the script
is broken". **QA on the real host.** `/api/prices` is slated to become restricted
the same way, at which point the preview domain stops converting anything.

### The one thing the contract cannot protect against

Both feeds are individually correct and still combine into a misleading
**comparison**. Our price is real and often an override; competitor figures are
converted at full mid-market. Where the override is much cheaper than its FX
equivalent, the page overstates our advantage — PH by 2.7x, ZA 1.8x, PL and HR
1.5x, against a 2.9x gap in GBP. This is not an API bug and cannot be fixed by
arithmetic: our price has to stay the real checkout figure, and we do not hold
rivals' actual local prices. See the caveats in
[`DYNAMIC_CURRENCY.md`](DYNAMIC_CURRENCY.md); an exact per-market figure would
need the Storefront API with `@inContext(country:)`, as noted above.
