# Building LF advertorial pages (TechUnboxed, Scaling or Failing, and similar)

Applies to every `pagescore/build_*.py` builder that ships a TechUnboxed, SOF,
or other advertorial-style funnel page — not the hlth-site Next.js app
(`.claude/rules/component-architecture.md` and friends cover that).

## 1. Body copy: every real paragraph is its own node

A text wall — several sentences that are clearly separate paragraphs, run
together with no visible gap between them — is a shipped bug, not a styling
nit. Caught on `best-sleep-masks-side-sleepers` (fixed 2026-11-12,
`pagescore/build_sleep_masks.py`): four paragraphs were written as one Python
string joined by bare `\n`, which `esc()` turns into `<br>`. A `<br>` inside
one `Text` node carries no vertical gap — only the `col(..., gap="16px")`
*between* sibling nodes does. The result read as one unbroken block, while
the Figma design showed clear paragraph breaks.

**The fix pattern, not a one-off patch:**

- When a block of copy is several distinct paragraphs, write it as a **list
  of strings** (one per paragraph) and render each as its own `text()` /
  `rich()` call inside the same `col([...], gap=...)`. The container's gap
  then spaces them correctly, same as any other sibling element.
- Do **not** concatenate multiple paragraphs into one string with `\n` and
  rely on `esc()`'s `<br>` conversion to separate them. That conversion
  exists for soft line-breaks, not paragraph breaks.
- **Exception:** a short lead sentence immediately followed by a tight
  bullet/checklist (`• item\n• item`) is normal editorial style and does not
  need blank-line spacing between the lead and the list — only genuine
  paragraph-to-paragraph breaks need the split-into-nodes treatment.

Before marking any advertorial page done, scroll its intro/body copy at the
live URL and visually confirm paragraph breaks are real gaps, not just
wrapped lines. Plain-text extraction (`get_page_text`, `curl`) cannot catch
this — `<br>` and a blank paragraph look identical once HTML is stripped, so
this has to be checked on the rendered page.

## 2. Dynamic (convertible) pricing is mandatory on every new page

Every money figure on every new TechUnboxed / SOF / advertorial page ships
tagged for the dynamic-currency script from the first draft, not as a
later retrofit. This was Joshua's standing instruction (2026-11-04,
referencing ClickUp task z941abzmhy) and it is restated here so it lives in
the repo, not only in session memory.

- Our own price → `data-price="price"` (and `data-price="compare"` for a
  struck-through was-price), reading the live Shopify figure — never typed
  by hand. Check the feed first: `GET https://hlthtrack.com/api/prices?handle=<handle>`
  (or `?products=all` to see the whole current catalogue).
- A competitor or editorial figure → `data-fx-gbp="<amount>"`, converted at
  the day's mid-market rate (see `.claude/skills/lightfunnels/references/CURRENCY_CONVERTER.md`).
- Convert **every** money mention in the prose/SEO to match the page's base
  currency, even figures that aren't tagged — a stray `$100` next to a
  tagged `£33` reads as broken.
- Append `snippets/dynamic-currency-page-tag.html` into the step's
  `settings.custom_html.header` (check for the `<!-- dynamic-currency -->`
  marker first — a second install double-registers the stub). The funnel's
  own tracker block (GTM/PostHog/Lenis) is separate and goes at the funnel
  level, not here.
- Bake the tags into the **builder script's own string constants**, not a
  one-off runtime patch on the live body — a patch applied outside the
  builder source is one unrelated rebuild away from silently reverting.
- If the page is drafted in a currency other than GBP, stop and ask before
  tagging it — `data-fx-gbp` assumes the untouched copy already reads right
  for a GB visitor, so tagging a $-written page as if those were GBP figures
  mis-prices every market, not just the ones being added.

`pagescore/build_sleep_masks.py` is the current reference implementation for
both rules above — read its intro-copy section and its buybox/review-card
pricing section before starting a new builder.

## 3. Every funnel needs the tracker header, GTM + PostHog + Lenis

A new funnel gets the house universal header installed in its **funnel-level**
`header_scripts` before any page is built — not per step, and not optional.
Without it the page has zero analytics (no GTM, no PostHog) even though it
renders and passes QA, which is exactly the failure mode that let two PostHog
experiments sit "ready" while recording nothing.

- The block also carries **Lenis** smooth scroll (desktop only — mobile
  already scrolls natively). It lives in the funnel header, not in a
  per-step script: a page that also installs its own Lenis runs two rAF
  loops against the same `scrollTop`.
- Two tracker variants exist and are not interchangeable — Meta/Native/
  everything else vs. Google (different PostHog project wiring, different
  pixel counts). Pick by the funnel's channel.
- Canonical copies are kept in the repo so an install is checked by sha, not
  by eye: `snippets/tracker-header-meta-block.html`,
  `snippets/tracker-header-google-block.html`, `snippets/README.md`. Audit
  with `python pagescore/check_tracker_headers.py` before installing — it
  flags a funnel that already carries an older variant or a double
  `posthog.init`, both unsafe to just append to.
- Verify in a browser, not in the stored HTML: `document.documentElement
  .classList.contains('lenis')`, `window.__lenis`, and that GTM/PostHog
  actually fire on the served page.
