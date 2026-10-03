# snippets/

Reference copies of the HTML blocks that get installed into Lightfunnels. These are
the **source of truth for comparison**, so an install can be checked by sha instead of
by eye, and so a drift between what we think is live and what actually is shows up as
a diff rather than as a silent behaviour change.

Pulled from the live funnels on 2026-10-04.

| file | chars | sha1 | installs into |
|---|---|---|---|
| `tracker-header-meta-block.html` | 22,721 | `2bcc3e350d` | funnel `header_scripts` — Meta / Native / everything that is not Google |
| `tracker-header-google-block.html` | 26,748 | `5d0bab814f` | funnel `header_scripts` — Google funnels only |
| `dynamic-currency-header-block.html` | — | — | the hosted script's source; published to `hlthtrack.com/dynamic-currency.js` |
| `dynamic-currency-page-tag.html` | — | — | a step's `settings.custom_html.header` |

## The tracker lives at FUNNEL level

`header_scripts` is the general header that applies to every step, and that is where
the tracker always lives. Never per step. A funnel whose `header_scripts` carries no
`posthog.init` has no analytics at all, and nothing about the page looks wrong.

## There are TWO tracker scripts and they are not interchangeable

679 differing lines ignoring whitespace. The Google block is **hardcoded** to PostHog
project 208779 (HTLH - GOOGLE); the Meta block **self-selects** from the detected
traffic source, so `google` still reaches 208779 and everything else lands in 194985
(HLTH - Native). They also wire Taboola and Outbrain differently (14/13 references
against 5/4), and load Lenis differently — Google unconditionally, Meta lazily and on
desktop only.

## Never append blind

Two `posthog.init` calls on one page duplicate every event, which is worse than no
tracking because it looks healthy. Check for an existing copy first. Known cases as of
2026-10-04, both deliberately left alone:

- `LISTICLES [ON DEV]` carries an older posthog-only block at funnel level.
- `TUB - Top 5 h trackers-v3 - NATIVE - LIVE` has a stray **per-step** posthog on
  steps `p8m5WBu3C` and `updated-3`. Strip those before installing funnel level.

## Checking and refreshing

```bash
python pagescore/check_tracker_headers.py           # audit every published funnel
python pagescore/check_tracker_headers.py --pull    # refresh these copies from live
```

## Lenis

There is no separate Lenis file any more. `lenis-smooth-scroll-block.html` and
`lenis-funnel-header-block.html` were deleted on 2026-10-04: smooth scroll ships
inside the tracker header, so every page that has the tracker already has exactly one
copy. A per-step block would be a second library running a second rAF loop against the
same scrollTop, which is the bug that was fixed on the over-60s pages. `tu_advertorial`
no longer has a `lenis=` switch, and `footer_html()` asserts none creeps back.
