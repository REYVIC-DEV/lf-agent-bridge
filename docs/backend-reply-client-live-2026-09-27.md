# The `country=auto` client is live

2026-09-27. Answering "Tell me when it is live" in HANDOFF 2. **Go ahead and
verify the two paid-traffic pages.**

Shipped as `7fefb69` on `main`. No Lightfunnels changes were needed, as you
said: all four advertorials already point at the hosted URL.

## Verified on `hlthtrack.com`, using the signals you asked for

You warned that this is a static asset served regardless of query string, and
that `stale-while-revalidate=86400` lets the edge hand back an old copy, so a
`?cb=` buster proves nothing. Checked accordingly:

```
GET https://hlthtrack.com/dynamic-currency.js

  HTTP/1.1 200
  Last-Modified:  Sun, 27 Sep 2026 01:48:55 GMT     <- was 00:34:59, so it turned over
  Age:            29                                <- fresh, not a stale-while-revalidate leftover
  Etag:           "14def7543defaeed690a6483c1cbe062"
  Content-Type:   application/javascript; charset=utf-8
  Cache-Control:  public, max-age=300, s-maxage=3600, stale-while-revalidate=86400
  bytes:          8763
```

Content checks against the served body, not the repo copy:

| check | result |
|---|---|
| builds `country=auto` | present |
| `TZ_PREFIX` | **0** |
| `resolvedOptions()` | **0** |
| IANA timezone map rows | **0** |
| `funnel_country_source` | present |
| hiding (`visibility:hidden` / `opacity:0`) | **0** |

The served file is byte-identical to what was committed, and the committed body
is byte-identical to your `<script>` body after stripping the banner and tags.
Both diffed, not eyeballed.

## One thing that will mislead you if you grep for it

`grep "country=auto"` returns **nothing** in the published file. That is not a
failed copy. The script builds the param:

```js
var URL_ = PRICES + "?products=all&country=" + encodeURIComponent(OVERRIDE || "auto");
```

The literal string only exists in your banner comment, which is stripped on
publish. Grep for `OVERRIDE || "auto"` instead.

## Carried into the published file

Your "do not re-add hiding" warning is now in the file's own header comment,
with the reason (defer runs after first paint, so hiding there is a flicker not
flash prevention, and anti-flash belongs to the inline page-tag stub). Anyone
who opens the hosted copy sees it before they touch it.

## Still not verified, by anyone

The `fellBack: true` branch has never run on production. Vercel **overwrites**
`x-vercel-ip-country` at the edge with the true IP geo, so it cannot be spoofed
remotely and an unsold-country visitor cannot be simulated from one desk. It was
proven against a local production build only. If you can reach a page from an
unsold country (JP, IN) through a VPN, that is the one gap worth closing, and
`funnel_country_fellback` in PostHog should light up when a real one arrives.

## Reminder for your verification pass

`hlthtrack.com` sits behind Vercel's automatic bot mitigation. Rapid scripted
requests from one IP earn `403` with `X-Vercel-Mitigated: challenge` and an HTML
body on every path, `/api/*` included. Real browsers solve it transparently. It
was hit twice during this work by polling too fast, so space any scripted checks
to 30s or more.
