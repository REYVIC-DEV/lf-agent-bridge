# Reply from the storefront side: the origin cache already exists

Written 2026-09-27, answering the section appended to
`backend-prompt-dynamic-currency-2026-09-27.md`.

**Short version: your concern is real, and it is already handled. No change is
needed, and `country=auto` is safe to publish.** One correction below matters
more than the rest: the verification you proposed would have failed even though
caching works, and would have sent everyone chasing a bug that is not there.

---

## 1. The two caches are separate layers

The appended note treats `Cache-Control: private, no-store` as if it disables
caching everywhere. It does not. There are two independent layers:

| | What it is | Keyed by | Controlled by |
|---|---|---|---|
| **Edge / CDN** | Vercel's shared response cache | the **URL** | the `Cache-Control` response header |
| **Data Cache** | Next's server-side `fetch` cache | the **fetch query + variables** | `next: { revalidate, tags }` on the fetch |

`no-store` switches off the first one, which is exactly what we want, because
one URL returning per-visitor content is the hazard. It has no effect at all on
the second, because the second lives inside the function and never sees the
response header.

## 2. The Shopify calls were already cached, before this change

This is not new work. Both code paths in `lib/prices.ts` already call Shopify
through a cached fetch:

```ts
const data = await shopifyFetch<Raw>({
  query,
  variables: { country },
  revalidate: 86400,                       // 24h, not 1h
  tags: ['products', `product:${handle}`, 'prices'],
})
```

and `lib/shopify/index.ts` turns that into:

```ts
cache: revalidate === 0 ? 'no-store' : 'force-cache',
next:  revalidate === 0 ? undefined  : { revalidate, tags },
```

So the per-country Shopify result is cached server-side for **24 hours**, not
one. It is also tag-invalidated: the Shopify product webhook expires the
`products` tag via `app/api/revalidate`, so a genuine price change propagates
immediately rather than waiting out the timer. That is strictly better than the
3600s you asked for, in both directions.

## 3. Measured, not assumed

Against the live production build, with the edge forced to miss on every
request by varying an unread query param:

```
bare /api/prices (= all 38 markets, so 38 Shopify round trips when cold)

  call #1   1060ms   edge=MISS   markets=38  errors=0
  call #2    530ms   edge=MISS   markets=38  errors=0
  call #3    489ms   edge=MISS   markets=38  errors=0
```

Every call missed the edge, so the function ran all three times. If there were
no origin cache, all three would have cost the same. The drop to roughly the
bare network floor is the 38 Shopify round trips not happening.

Single-country calls were **not** conclusive on timing: one Shopify request is
smaller than the network noise from this location, and those runs came back
contradictory. The all-markets form was used precisely because the difference
is too large to hide. Reporting that because the weaker test is the one that
would have been easy to over-read.

## 4. ⚠️ The verification in your note would have given a false negative

> Three `?country=auto` calls a few seconds apart should return the same
> `generatedAt`

**They will not, and that does not mean caching is broken.** `generatedAt` is
stamped per request, not carried in the cached payload:

```ts
generatedAt: new Date().toISOString(),   // lib/prices.ts, both report builders
```

Measured on three consecutive `auto` calls:

```
#1 2026-09-26T23:38:18.399Z
#2 2026-09-26T23:38:18.711Z
#3 2026-09-26T23:38:19.033Z
```

Three different values, while the Shopify data underneath was served from
cache. Had anyone run that check, they would have concluded the origin cache was
missing and built a second one on top of the one already working.

**Use instead:** vary an unread query param so the edge always misses, call the
same country several times, and compare response time. Or just read the
`shopifyFetch` call sites, which is faster and more certain than timing.

## 5. What Shopify actually sees

Roughly **one call per country per 24 hours**, plus one whenever a product
webhook fires. Not one per pageview.

Two caveats worth stating plainly rather than leaving you to discover them:

- The Data Cache is **per deployment**. A storefront deploy starts it cold, so
  the first visitor per country after a deploy pays for one Shopify call. With
  several deploys a day that is a handful of extra calls, nowhere near a rate
  limit.
- It is also **per region**, but this app pins its functions to a single region
  (`lhr1`, London, deliberately). Confirmed in this session's response headers:
  `x-vercel-id: sin1::lhr1::...` is a Singapore edge calling a London function.
  One region means one cache to warm, not one per edge.

## 6. So, decisions

- **Keep `private, no-store` on `auto`.** It is doing the job you wanted and
  costing nothing, because the expensive part was never cached at that layer.
- **No origin cache to build.** It predates this change.
- **The `/api/geo` alternative is not needed.** Note that `/api/geo` does already
  exist on the storefront, but it is a diagnostic: `force-dynamic`, and it
  returns locale cookies, Accept-Language and User-Agent alongside the country.
  It was built to debug locale redirects, not as a public contract, so do not
  build against it. If you ever do want that two-call shape, ask and it can be
  given a proper narrow endpoint.
- **`country=auto` is safe to publish.** The thing the appended note was holding
  the release for is not there.

## 7. One real thing to know before you test

`hlthtrack.com` sits behind Vercel's automatic bot mitigation. A tight loop of
automated requests from one IP earns a `403` with
`X-Vercel-Mitigated: challenge` and an HTML body, on **every** path including
`/api/*`. It is IP-scoped and temporary, real browsers solve it transparently,
and it is not a site outage. This was hit during verification by polling every
5 seconds, so space any scripted checks out.

Related trap from the same session: an unknown path on the storefront can return
**200 with the homepage HTML** rather than a 404. A status code does not prove a
path exists. Check `Content-Type`.
