# Changelog

Changes made to **step 12** of `fun_vGqQYxn4H2i_traYYkh4w` (tub / smartwatch-review):
`TECHUNBOXED-UK-V4`, slug `randell-build`, uid `step_0hL9bV7NUmyESdgkwY4Ih`.

Live: https://www.techunboxed.co/smartwatch-review/randell-build

A freshly built UK advertorial. Nothing here was copied from another step — the only
reused values are asset URLs, the affiliate URLs from the funnel-level `AFFILIATE`
map, and the policy-modal markup, which exists nowhere else.

Earlier work on steps 3/11, the meta-uk funnel, the bridge tooling and the general
conventions all live in
[`funnels/tub/smartwatch-review/NOTES.md`](funnels/tub/smartwatch-review/NOTES.md)
and [`funnels/channels/meta-uk/NOTES.md`](funnels/channels/meta-uk/NOTES.md).

Backup taken before any edit: `steps/12-PRE-EDIT.2026-08-06.json`.
Edit scripts: `funnels/tub/smartwatch-review/edits/step12-*.py`

---

## 2026-08-06

**Every change below measured 98 before and after.** Link, markup and style edits
add no requests, so none of them cost anything.

### Links and content

| change | detail |
|---|---|
| **UK store host** | `hlthtrack.com` to `hlthtrack.co.uk`. **15 rewritten, 6 left alone** — those are `trustpilot.com/review/hlthtrack.com`, where the domain is the review-page *slug*, not a link. Applied with `lf.py edit --step`, scoped to step 12; DE/AU/CA/TH untouched. |
| **8 Amazon buttons** | all were `href="#"` — dead. Wired to the real affiliate URLs, 2 per product (Whoop / Apple Watch / Garmin / Fitbit), each carrying `tag=techunboxed04-20`. |
| **no `aff-*` class** | owner's call: with the URL on the button there is nothing for the header's replacer to do, so it gets no hook and performs one less runtime DOM mutation. |
| **breadcrumb** | `Home` to `blog.techunboxed.co`, `Wearables` to `/category/wearables`. Trailing crumb left unlinked — it is the current page. |
| **social icons** | removed. Four `<a href="#">` + `<svg>` with no visible text — 1,885 chars of dead links. |
| **footer policy links** | given the popup trigger ids (`terms`/`priv`/`edit`/`aff`) and the policy modal added. |
| **footer alignment** | centred. It was `left` because it used to share a flex row with the social icons. |
| **Trustpilot row** | made a link to `trustpilot.com/review/hlthtrack.com` (`target=_blank`). Figma names that node "Link - Untitled link", which is also why "Excellent" is underlined — it is the link affordance. |

**URLs came from the live `AFFILIATE` map, not from step 3.** Step 3's inline
destinations are **stale** — verified, all 8 differ from the live map — because the
header script overwrites them at runtime, so nobody notices they rot. Step 12 having
no class means its URLs must stay correct on their own; the mitigation is that `tag=`
is embedded, so attribution survives even if a deep link ages.

**The popup improves on step 3's copy.** Step 3 ships the modal's `<style>` inside
the body — the in-body-stylesheet pattern that cost step 3 2,703 ms of style recalc.
Here the 1,019-char `<style>` went into `settings.custom_html.header` and only markup
+ script are in the body, so **step 12 still has 0 in-body `<style>` tags.**

Two bugs found while wiring the triggers:

- The theme registers a click handler on **every** anchor and runs
  `document.querySelector(href)`, so a bare `href="#"` throws *"'#' is not a valid
  selector"*. Pre-existing — the page shipped 9 such links — but now on a path users
  click. Repointed each href at its overlay id.
- That alone made the theme **scroll to the overlay**. Fixed by moving the popup's own
  listener to the **capture phase** with `stopPropagation`, so it runs before the
  theme's handler. Verified: all four open with the right heading, no jump, Esc closes,
  0 console errors.

### Offer card to Figma frame `557:6514`

Built from measured Figma values, not eyeballed from a screenshot.

| element | Figma | was |
|---|---|---|
| border `557:6515` | 2px **dashed** `#000`, `dashPattern [6,4]`, radius **6** | solid, radius 20 |
| badge `557:6559` | `#E63A45`, radius 7, padding 7/16, Inter ExtraBold 16/28.8 = 43px tall | 5/14 padding, 33px |
| badge `557:6558` | absolute, centred, `y = -22` | left-aligned, inside the padding |
| image `557:6516` | at (2,2), fills the left half top-to-bottom | inset 22px, 300px tall, vertically centred |
| heading `557:6530` | `#E63A45`, **24.7/29.61, letterSpacing -1.5**, hard newline breaks = **3 lines** | **`#7b0323`** (retired maroon), 25/30, natural wrap = 2 lines |
| subtext `557:6532` | **10.5px / Medium 500 / `#000000`** | 13px / 400 / `#111827` |
| CTA `557:6536` | **FILL** the column, padding 12/32/16/32, radius 10 | hugged its label at 11/14 |
| pill `557:6545` | **237 wide**, radius 4, `#E1C6CB80`, 9.08 vertical padding | inline span hugging its text |
| TP text `557:6522` | per-run: "Excellent" **Bold + UNDERLINE**, all `#000`, lh 19.2 | all plain, `#111827`, lh 18 |

Things that only measuring caught:

- **The badge must take zero flow height.** Figma marks its container
  `layoutPositioning: ABSOLUTE`; LF has no `position` prop, so
  `margin {top:-24px, bottom:-19px}` reproduces it — `-24 + 43 - 19 = 0`. It straddles
  the top edge without pushing the image down. Verified 22px above.
- **`line-height` does nothing to an inline element.** The badge stayed 33px until the
  span became `display:inline-block`; then 43px, matching the frame.
- **`<u>` is reset by LF's CSS.** The underline only took as an inline
  `style="text-decoration:underline"`.
- **`zIndex` is not a supported LF style prop** — it came back `auto`. Not needed in
  the end: the badge already paints above the image.
- **The Trustpilot logo was a 1000x318 PNG (ratio 3.14) in a 70x17 box (ratio 4.12)**,
  so `objectFit:contain` letterboxed it — fitting by height to ~53px and leaving ~17px
  of dead space, which is what made the logo look detached from the text. Swapped to
  the SVG the frame specifies: exact ratio, gap now 6px, **71.5 to 4.9 KiB**.
- **"Flush" had three separate causes**, not one: the card's 22px padding, the row's
  20px gap, and `alignItems:center` floating a fixed-height image in a taller row.
- **The image was covering the rounded corners, not the edges.** Card border-box left
  16.0 with a 2px border = inner edge 18.0, and the panel started at exactly 18.0.
  Only the corners were wrong: panel `borderRadius 0` against the card's `6px`. The
  inner radius of a 6px radius with a 2px border is **4px**; set that and the curve
  matches. `overflow:hidden` would also have clipped it, but would equally clip the
  badge extending 22px above — rejected for that reason, not overlooked.
- **The heading's maroon `#7b0323`** is the pre-rebrand red that the meta-uk colour
  pass retired months earlier, still sitting in this build.

Deliberately not replicated: Figma's two 5.19x1 `#0000001C` hairlines flanking the
Trustpilot line (invisible at render size) and its separate 24x24 arrow icon in the
CTA — ours uses a text arrow.

Verified desktop and at 390px: card 351px, badge centred and 22px above the edge
without overflowing, image stacks flush at 2px, heading and button inside with a 30px
inset, **no horizontal scroll**, 0 console errors.

### Measured

| | step 12 | step 3 (reference) |
|---|---|---|
| PSI mobile | **98** | 90 |
| FCP / SI | 1.7 s / 1.7 s | 2.9 s / 2.9 s |
| LCP | 2.1 s | 2.9 s |
| TBT | 0 ms | 0 ms |
| CLS | **0** | 0.001 |
| payload | 1,073 KiB | 402 KiB |
| font bytes | **0** | 70 KiB |

Step 12 carries **2.7x the payload** of step 3 and still scores 8 points higher —
bytes are not the constraint on these pages, fonts on the critical path are.

## Open: step 12 is not rendering Inter at all

The "fonts look thin" observation is real and has a specific cause. **The only
`@font-face` family declared on the page is `InterFallback`** — there is no `Inter`
face — so every character renders in the Arial-metric fallback, and at weight 800
Arial has no ExtraBold, so the browser synthesises it.

Proof by canvas measurement: `Inter` at 800 measures **185.5px, identical to a
nonsense font name** (control 185.5), while `InterFallback` measures 200.9.

Meanwhile the page **still downloads 3 Inter woff2 (~71 KiB) it cannot use**, because
the stack makes LF request
`family=Inter,+InterFallback,+sans-serif:400,800,900,700,600,500` and the returned
faces are declared under that whole string, which the stack's `Inter` token never
matches. **Paying for the fonts, getting Arial.**

`test3-smartwatch/article-v10` has the same bug, so **both of those 98 scores are
measured on pages that are not rendering Inter.** Steps 3/11 avoid it only because
they carry explicit `Inter` `@font-face` declarations in `custom_html.header`.

The fix is those same declarations, for weights 400/600/700/800/900. The trade, which
is why it is still undecided:

| | now | fixed |
|---|---|---|
| renders in | Arial-metric fallback | **real Inter** |
| font bytes | 71 KiB **wasted** | ~119 KiB, used |
| likely PSI | 98 | **~90**, the way step 3 went |
