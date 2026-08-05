# Meta funnels - UK (`meta-uk`)

**LF id:** `fun_Z78qnXtnsXIf619roFNNU` · **live:** yes ·
**step 0:** https://www.techunboxed.co/meta-uk/v45g6ypE3

## What this is

Meta-traffic advertorial for the HLTH Band on the TechUnboxed masthead. Step 0
("Branded Hype Listicle") is the ad landing page; step 1 ("Founders Funnel") is
the second article.

Figma source of truth: file **99 Commerce** → page *Advertorials/Blogs* → frame
`537:458` "Branded Hype Listicle".

## Log

- `2026-08-03` — brought step 0 to 1:1 with the Figma frame. Edited **directly on
  the live funnel** (no duplicate) at the owner's instruction; original bodies for
  both steps backed up under `steps/*.backup-2026-08-03.json` first.

  **Images.** Only 2 of 4 actually differed from the design:
  - avatar `img_P84ZiG4gVSMPN5zLLHUdh` → `img_OwSMha6EndLKrnOisyn7-`. The old one
    was a 190x190 pre-cropped circle with **black corner artifacts** baked in;
    replaced with the clean 589x546 source (already in the library from the
    `article` funnel — reused, not re-uploaded).
  - photo 1 `img_PWBTesEwjjEOsLVFAZwaO` → `img_6J4unzBb1J9Fymp-l393Y`. Genuinely
    different content: the old image showed the app's *graph* view, the design
    shows the *list* view. Only new upload of the batch.
  - photos 2 and 3 left alone — verified **pixel-identical** to the design's
    rendered crops (dhash distance 0 at matching dimensions). Swapping them to
    the uncropped Figma sources would have changed the framing for no gain,
    because Figma's `CROP` fills carry an image transform LF can't reproduce
    (`objectFit` has no `object-position` equivalent).

  **How the crops were derived.** `save_image_fills` returns the *uncropped*
  original; the design's actual crop only exists in the composited render. So the
  image frames were screenshotted at 2x (`save_screenshots`), which reproduces
  the crop exactly — the results landed on 1400x1034 and 1400x934, matching both
  the Figma box ratios (517/700, 467/700) and the dimensions of the images
  already on the page. That confirms the page was originally built the same way.

  **Encoding.** Photo 1 shipped as WebP `quality=90`, 140 KB. Lossless was
  measured at 1283 KB — 17x the 76 KB the slot previously used — so lossless was
  rejected here as a page-speed regression; mean pixel error at q=90 is 1.37/255,
  not perceptible. Keep lossless for logos/flat graphics only.

  **Colors — 37 edits, full 1:1 with the design:**

  | was | now | what |
  |---|---|---|
  | `#000000` (11x) | `#191E2A` | headings / text |
  | `#4c4c4c` (9x) | `#191E2A` | body paragraphs |
  | `#0075ff` (9x) | `#E63946` | inline links (were blue) |
  | `#7b0323` (4x bg + 1 border) | `#E63946` | CTA buttons (were maroon) |
  | `#0f0f0f` (2x), `#28282b` (1x) | `#191E2A` | header / footer bars |

  Left untouched because they already matched Figma exactly: `#ffffff`,
  `#bdbdbd` (sponsored label), `#bcd9e4` (footer links), `#ffffff` @ 0.14
  (footer divider = `#FFFFFF24`).

  Verified live afterwards: zero stale colors remain, both steps intact, page
  renders correctly (`after-2026-08-03.jpeg`).

- `2026-08-03` (second pass) — **typography to 1:1.** The design is Inter
  throughout; the page had three substituted families:

  | was | now | where |
  |---|---|---|
  | PT Serif | Inter | H1 (x1), H2 (x6) |
  | Noto Serif Georgian | Inter | body paragraphs (x9) |
  | Roboto | Inter | BlockLink CTA wrappers (x9) |

  Plus: H1 `fontWeight` 600 → **700** (design is Inter Bold), and
  `letterSpacing` zeroed where the design has none — 1.9px on the H1, 1.08px on
  H2s, 0.58px on body copy and on the 4 CTA labels (25 family + 1 weight + 20
  tracking edits).

  Sizes and line-heights already matched exactly (40/52, 30/39, 18/31, 17/31)
  and were left alone. Theme-bound entries (`adsfheading_font`,
  `asssstatic_body_text_font` on the sticky bar and footer) were already Inter
  and were not touched. `JetBrains Mono` on the footer DISCLAIMER label is
  correct — the design uses it there.

  Verified on the live page via computed styles: **zero non-Inter text in the
  article**; H1 = `Inter 40px/700, lh 52px`; H2 = `Inter 30px/700, lh 39px`;
  inline links = `Inter 18px/700, lh 31px`; CTA = `Inter 17px/700, lh 31px`.
  The H1 also wraps on the same words as the Figma render. See
  `after-fonts-2026-08-03.jpeg`.

- `2026-08-03` (third pass) — **avatar back to a true circle.** Two faults, both
  introduced/exposed by swapping in the clean 589x546 source:
  - `borderRadius: 40px` on a 95px box is a squircle, not a circle. Figma's node
    `537:539` has `cornerRadius: 47.5` — exactly half the width. Set to `47.5px`.
  - **no `objectFit`**, and the new source is 589x546, *not* square. With explicit
    `width`/`height` the browser default is `object-fit: fill`, so the face was
    being **distorted**. Figma's fill is `scaleMode: FILL`; set `objectFit: cover`.

  The old 190x190 avatar hid this because it was already square (and had the
  black corners baked in) — so nothing stretched and 40px looked passable.
  Verified via computed style on the live page: 95x95 box, `border-radius 47.5px`
  (>= half the width), `object-fit: cover`. See `avatar-circle-2026-08-03.png`.

  Note `47.5px` is exact rather than `50%` because there are no responsive
  overrides on this block; if a `media` width override is ever added, switch to
  `50%` so it stays circular.

- `2026-08-04` — **store links `hlthtrack.com` → `hlthtrack.co.uk`.** 5 rewritten
  (4 `BlockLink.destination` + 1 inline `<a href>`, all in Branded Hype Listicle).

  **8 occurrences deliberately left alone.** They are Trustpilot review URLs —
  `https://www.trustpilot.com/review/hlthtrack.com` — where `hlthtrack.com` is
  the review-page *slug*, not a link to the store. Rewriting them would point at
  a Trustpilot profile that may not exist. All 7 hits in Founders Funnel are of
  this kind (6 destinations + 1 inline href), which is why that step shows 0
  changes.

  Rule used: rewrite only where `hlthtrack.com` is the URL **host** —
  `(https?://(?:www\.)?)hlthtrack\.com(?![a-zA-Z0-9-])`. Structurally it cannot
  match a `/review/hlthtrack.com` path segment, so a plain find/replace of the
  bare string must never be used here. Manifest:
  `edits/hlthtrack-couk-2026-08-04.json`.

  Verified on the live page: 23 links total, **0** `hlthtrack.com` hosts,
  13 `hlthtrack.co.uk` (LF's `iref`/PostHog tracking params preserved),
  1 Trustpilot URL intact.

## Account-wide scope (NOT done — needs a decision)

`hlthtrack.com` appears **516 times across 17 funnels / 45 steps**. Only this
funnel was changed. Do not blanket-replace, for three reasons found while
scoping:

1. Many of those 516 are **Trustpilot slugs**, not store links (in this funnel
   alone it was 8 of 13). Use the host-only rule.
2. `hlthtrack.co.uk` **already appears 223x**, so the migration is partly done —
   whatever drives it is inconsistent, not simply un-started.
3. `hlthtrack.de` appears **12x**. The domain is market-specific and the account
   has DE / Finland / Meta variants, so forcing `.co.uk` onto a non-UK funnel
   would send that traffic to the wrong store.

Biggest offenders if a wider pass is wanted: `hlthbandreviews` + its duplicate
`yH3ZZFzU9` (68 each), `smartwatch-review` + `smartwatch-review-n` (27 each),
`hlth-review` (22).

## Known remaining gaps

1. **`SPONSORED ARTICLE` label** — the design specifies **SF Pro** 11px; the page
   uses Inter 11px (tracking 1px matches). SF Pro is an Apple system font with no
   webfont licence. A `-apple-system, system-ui` stack would render real SF Pro
   on Apple devices but Segoe UI on Windows and Roboto on Android, i.e.
   inconsistent across the traffic. Left as Inter deliberately.

2. **The design's body-text colour is internally inconsistent, and this page was
   normalised.** In the Figma frame 5 of 7 paragraphs are `#191E2A` but two
   (sections 2 and 3) are `#4C4C4C`, and the blockquote body is `#7C7C7C`. The
   colour pass mapped every `#4c4c4c` to `#191E2A`, so the page is now uniform.
   That reads as intended-but-unstated rather than literal 1:1 — restoring the
   split would reintroduce the inconsistency. Flagged for a decision.

## Rollback

```bash
python3 - <<'EOF'
import json, sys
sys.path.insert(0, "tools/lf-agent-bridge"); import lf_api
tok=open("tools/lf-agent-bridge/.session_token").read().strip()
acct=open("tools/lf-agent-bridge/.lf_account").read().strip()
h=lf_api.session_headers(acct)
s=json.load(open("funnels/channels/meta-uk/steps/0-step_CtC9RNhvNF2YytxGNYEMj.backup-2026-08-03.json"))
lf_api.gql(tok, "mutation($id:ID!,$node:InputFunnel!){updateFunnel(id:$id,node:$node){id}}",
  {"id":"fun_Z78qnXtnsXIf619roFNNU","node":{"steps":[{"id":s["uid"],"slug":s["slug"],
   "title":s["title"],"type":s["type"],"settings":s["settings"],"visual":s["visual"],
   "body":s["body"]}]}}, extra_headers=h)
EOF
```
