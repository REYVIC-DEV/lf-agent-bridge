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

## Log

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
