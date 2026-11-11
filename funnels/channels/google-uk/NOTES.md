# Google funnels - UK (`google-uk`)

**LF id:** `fun_p9Y_FwGlQsaP5bpW70q5N` · **live:** yes · **slug:** `article`
**entry:** `comparison-1` → https://www.techunboxed.co/article/comparison-1

Google-traffic advertorials on the TechUnboxed masthead. 14 steps. The Google Ads
final URLs point at the ENTRY step, which is why shipping a winner here means
making the entry forward rather than swapping a URL.

## Steps that matter

| slug | what |
|---|---|
| `comparison-1` | **ENTRY.** Ad destination. Now a 100% redirect to `dMs4WkOYD` |
| `dMs4WkOYD` | the live winner. Receives all Google paid traffic |
| `dMs4WkOYD-fx` | `noindex` copy of the winner, carrying the dynamic-currency work |
| `jFrY0DhRi` | "HLTH vs Smartwatch". Also carries dynamic currency since 2026-10-29 |

## Log

- `2026-10-29` — **Smooth scroll died whenever the cursor sat over a video.** Ryan:
  *"it's jumpy and not smooth."* Script: `pagescore/fix_lenis_video_pointer.py`
  (cross-funnel, so it lives in `pagescore/`, not here). Rollback:
  `pagescore/header_backups/article.pre-video-pointer-2026-10-29.html`.

  **A cross-origin iframe swallows the wheel.** The browser does not deliver wheel
  events from an embedded site up to the page embedding it, so Lenis never heard
  the wheel while the pointer was over a Cloudflare Stream video and the browser
  fell back to its own instant scroll. Measured on the live page, same wheel tick,
  only the cursor position different: **58 scroll positions drawn over the text,
  2 over a video.** All four videos. The videos are 382px wide against a 416px
  text column, so close to half the article's width was a band where the easing
  silently switched off and the page teleported.

  Fix is one CSS rule inserted into the funnel's `header_scripts`, next to the
  inlined Lenis CSS:
  `html.lenis iframe[src*="cloudflarestream.com"][src*="controls=false"] { pointer-events: none; }`
  Verified live after the write: 2 → 47-58 positions on all four, videos still
  playing (sampled the same pixel region 1.2s apart and it changed), currency
  tags still 4/6, one pre-existing console error and no new one.

  ⚠️ **The selector carries its own guards, which is why it cannot break a video.**
  `html.lenis` means desktop only and only while Lenis is actually running —
  confirmed inert at 390px, where `<html>` has no class and the iframes compute
  `pointer-events: auto`. `controls=false` means only a decorative muted autoplay
  loop with nothing to click; a video a visitor is meant to operate keeps its
  pointer with no list to maintain. All 43 Cloudflare videos in the account were
  checked first and every one is `controls=false`.

  ⚠️ **Three funnels got it, and the other two could not be browser-verified.**
  `Native funnels - UK` carries three videos on `zQkAffXHg`, but that step
  client-side redirects to `Od-Yphefq` before anything renders, so no visitor
  reaches them; the rule is installed and serving on all three of its steps.
  `Garlic Funnel` has 33 videos on `lp-1` and no `preferred_domain`, so it has no
  URL to test — read-back from the API is the only proof there.
  `LISTICLES [ON DEV]` has 10 videos across 3 pages and was deliberately SKIPPED:
  it carries no Lenis at all, so there is no easing to break.

  ⚠️ **`snippets/` was NOT updated, so a NEW funnel will have the bug again.**
  The two tracker snippets are byte-exact reference copies and all three live
  headers already differ from them (google-uk 28,924 chars against the snippet's
  26,796), which is also why this was a surgical insert rather than an overwrite:
  writing a snippet over any of these would have reverted everything since
  2026-10-04.

- `2026-10-29` — **Trustpilot link overlapped the paragraph above it on `jFrY0DhRi`,
  but ONLY between 768px and 991px wide.** Section 9: "That's what tipped me over
  the edge." and "Read Trustpilot reviews" drawn on top of each other, 18px
  overlap measured at a 973px viewport. Script:
  `fix-jFrY0DhRi-tp-overlap-2026-10-29.py`. Rollback:
  `steps/jFrY0DhRi.pre-overlap-fix-2026-10-29.json`.

  **A BREAKPOINT MISMATCH, not a spacing value.** Block `c633f9b4` set
  `gridColumnSpan: auto` at **991** but cancelled its `margin-top: -40px` only at
  **767**. So across a 224px band the grid had already collapsed to one column
  while the pull was still applied. Its two siblings in the same article
  (`fba0fed7` at -30px, `5cdb135b` at -75px, the very paragraph it collided with)
  both reset at 991, which is what identified the intended value. Fix was to move
  that one override from 767 to 991.

  ⚠️ **This is the shape of bug that survives a normal check.** Desktop was fine
  and phone was fine; only the tablet band was broken, so testing 390 and 1440
  proves nothing here. Verified after the fix at 761, 973 and 1433: zero
  overlapping text blocks anywhere on the page, and the -40px still active above
  991 where the desktop layout relies on it.

  ⚠️ **The videos mount lazily and a full-page screenshot taken too early shows
  four EMPTY columns.** Sections 3, 6, 8 and 9 are Cloudflare Stream blocks, not
  images. They only attach their iframe once scrolled into view, so an immediate
  `fullPage` capture renders them as blank 382x382 placeholders and looks exactly
  like four missing images. Scroll the whole page first, then capture. Half an
  hour went into "missing images" that were never missing.

- `2026-10-29` — **dynamic currency on `jFrY0DhRi`.** Ryan's request. 10 money
  figures, two distinct values, counted twice (block tree and rendered page both
  gave 10): `£79` x4 → `data-price="price"` (our band, Shopify feed, exact) and
  `£500` x6 → `data-fx-gbp="500"` (the smartwatch the author ditched: editorial,
  so mid-market FX is the only figure available and the right one). No
  compare-at on this page. Script: `tag-jFrY0DhRi-currency-2026-10-29.py`.
  Rollback: `steps/jFrY0DhRi.pre-tag-2026-10-29.json`.
  QA'd on the real host at `?country=PH` (₱2,450 / ₱42,543), `?country=GB`
  (unchanged £79 / £500) and `?country=DE` (€79 / €597). Nothing overflowed at
  390px and no element stayed hidden.
  ⚠️ **This step's `custom_html.header` was EMPTY before this** — the GTM /
  PostHog / Lenis universal block is funnel-level `header_scripts`, so an empty
  step header is normal here and is not a missing-tracking signal.
  ⚠️ **Installed the PAGE TAG, not the inline block.** Since 2026-09-27 the
  logic is hosted at `hlthtrack.com/dynamic-currency.js`; the header carries only
  the anti-flash stub and a deferred `<script src>`. `tag-dMs4WkOYD-fx-2026-09-21.py`
  predates that and installs the inline version — do not copy it verbatim.
  The install assertion must count the `<script src=` string, **not** the url:
  `dynamic-currency.js` appears twice in one correct copy because the comment
  names it too, exactly the way `api/prices` did in the old block.

- `2026-09-21` — **ended PostHog experiment 91531** and shipped the `test` arm.
  Conclusion recorded as `inconclusive`: the primary metric (orders) was +37%
  but only 78.2% chance to win, total revenue differed by GBP 119 over 33 days,
  and the two significant results both went AGAINST the variant (CTA CTR -22.6%,
  AOV -24.7%). Shipped as a business call, not a statistical win.
  Ship method: `edits/ship-dMs4WkOYD-redirect-2026-09-21.py` replaced the
  flag-gated redirect on `comparison-1` with an unconditional one. The PostHog
  flag `google-comparison1-v2` is NO LONGER READ by the page, so deactivating it
  cannot affect live traffic. Rollback: `steps/comparison-1.custom_html_header.pre-ship-*.html`.
  ⚠️ Interim. Repoint the Google Ads final URLs at `/article/dMs4WkOYD` and
  delete the redirect block so visitors stop paying for the extra hop.

- `2026-09-21` — **dynamic currency on `dMs4WkOYD-fx`.** 60 money figures:
  16 `data-price="price"`, 5 `data-price="compare"`, 38 `data-fx-gbp`,
  1 left in GBP. Script installed behind a `<!-- dynamic-currency -->` marker.
  QA'd at `?country=PH` (₱2,450 / ₱4,900), `?country=GB` (unchanged £79 / £158),
  `?country=DE` (€79 / €158). Zero console errors in all three.

## Traps this funnel has already produced

**Reading one page costs ten minutes.** There is no single-step query -
`node(id: <step id>)` resolves to null - so `get_funnel_steps` pulls all 14 step
bodies, ~10.4 MB. Use `edits/cache-step-body.py` once, then `--from-cache`.
For READ-ONLY inspection prefer the live URL: it is HTML, it is seconds, and it
is what is actually served. Joshua's suggestion, and it immediately paid off.

**Count money figures from two independent sources before trusting the number.**
The first inventory said 57. The tagger said 60 and looked like it was
over-matching. Relaxing the assertion to match the code would have shipped
whichever one was broken. The block tree and the rendered page agree at 60.

**A comma plays two roles.** `(?![\d,])` rejects `£79,` outright, so
`"£79, once."` matched NOTHING and two whole blocks were invisible. The
reference doc warns about the opposite failure (swallowing the comma). The
pattern must treat `,\d{3}` as a thousands separator and any other comma as the
end of the number: `(?!\d|[.,]\d)`.

**A sentence-ending period is not part of the number.** `(?![\d,.])` refused
`£14.95.`, `£79.` and `£158.`

**`£79.99` contains `£79`.** Fitbit's price would be tagged as our band by any
naive find/replace. On PH that is ₱6,719 vs our ₱2,450 - a visibly wrong number,
but only visible in one market.

**Verification traps, both self-inflicted and both hit:**
- `json.dumps` escapes the quotes, so asserting `data-price="price"` is in the
  dumped body ALWAYS fails. Match the attribute name.
- The installed script contains its own selectors as literal text, so counting
  the rendered page gives 17/6 for a correct 16/5. Strip `<script>` first.
  `data-fx-gbp` is unaffected because the script writes it without the `=`.
- `api/prices` appears TWICE in one copy of the script. Count `var PRICES` to
  test for a duplicate install.

## Open

- **`£14.95`, the bicep strap — now solvable.** It is `hlth-arm-band`
  ("Sport Knit Arm Band"), and as of 2026-09-21 `/api/prices?products=all`
  serves it in all 32 markets: PH ₱465, ZA R186, HR €10.95, DE €14.95. So it can
  be priced EXACTLY rather than left in GBP. Mid-market would have said ~₱1,255
  in PH, so the converter would have been wrong by nearly 3x — leaving it in
  pounds was the right call while it was the only option.
  ⚠️ Still blocked on a script change: `snippets/dynamic-currency-header-block.html`
  fetches the single-product feed and drives one product's tags. It needs to
  request `products=all` and honour a handle-scoped tag, e.g.
  `<span data-price="price" data-price-handle="hlth-arm-band">£14.95</span>`.
  Until then the figure stays in GBP on `dMs4WkOYD-fx`.
- **Promotion.** `dMs4WkOYD-fx` is proven; the winner is still untagged. Either
  copy the tagged body onto `dMs4WkOYD`, or repoint the redirect at the copy
  (which would need its `noindex` removed first).
- **Override distortion.** Our price in PH/ZA/PL/HR is a Shopify price-list
  override while competitors convert at full mid-market, so the comparison
  overstates our advantage - PH by ~2.7x. Joshua 2026-09-21: *"the conversion of
  the competitor prices are fine"*, so this is accepted, not outstanding.
