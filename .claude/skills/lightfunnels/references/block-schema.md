# Lightfunnels Page-Builder Block Schema (verified)

The target vocabulary for turning any design (Figma, a rendered web page, a
mockup) into a Lightfunnels page. Everything here was mined from 8,000+ real
nodes across live funnels — it is what the builder actually accepts, not a guess.

A page `body` is one tree: `Root → Section → Container → [content blocks]`.
Every node is `{"t": <type>, "id": <uuid4>, "styles": [{prop,value,...}], "p": {...}}`.
`p.children` holds child nodes. `id` must be a fresh uuid4 per node.

## Node types

| `t` | Role | Key `p` fields (besides `children`) |
|---|---|---|
| `Root` | Page root (exactly one) | — · style: `pageWidth` (e.g. `960px`), `version: 11` |
| `Section` | Full-width horizontal band | `layout` (`boxed`/`""`), `dividerPosition`, `horizontalFlip`, `embedded_video` |
| `Container` | Flex/grid box, nestable | `widthOption`, `heightOption`, `className` |
| `Title` | Heading (h1–h6) | `size` (`"1"`–`"6"`), `content` (HTML ok), `widthOption` |
| `Text` | Paragraph / rich text | `content` (HTML incl. `<a>`, `<b>`, `<span style>`), `widthOption` |
| `Image` | Image | `src_id`, `src_uid`, `src`, `alt`, `title` (see Images) |
| `BlockLink` | Button / linked box | `destination` (URL), `target` (`_blank`), `className` |
| `Link` | Inline text link | `destination`, `target` |
| `HtmlElement` | Raw HTML/JS embed | `content` (raw HTML string) |
| `Video` | Video | `src`, sizing styles |
| `Sticky` | Sticky wrapper | wraps children that pin on scroll |

## The layout model (this is the crux)

Lightfunnels **is flexbox/grid under the hood**. A `Container` only lays out
horizontally when it explicitly turns flex on. The prop that trips everyone up:

- **`lfDisplay`** — `block` (default, stacks) · `flex` · `grid`. **You must set
  `lfDisplay: flex` for `flexDirection`/`gap`/`alignItems` to do anything.**
  A row of `flexDirection: row` WITHOUT `lfDisplay: flex` renders stacked.
- `flexDirection` — `row` · `column`
- `justifyContent` — `flex-start` · `center` · `flex-end` · `space-between`
- `alignItems` — `flex-start` · `center` · `flex-end`
- `gap` — e.g. `16px` (space between children; replaces per-child margins)
- `flexWrap`, `columns` (grid), `gridColumnSpan`/`gridRowSpan` (on children)

**Row-card recipe** (thumbnail beside text — the pattern that failed until
`lfDisplay` was added):
```
Container[lfDisplay:flex, flexDirection:row, gap:16px, alignItems:center]
 ├─ Container[width:150px, flexShrink:0]      ← fixed-width thumb wrapper
 │    └─ Image[width:100%]
 └─ Container[lfDisplay:flex, flexDirection:column, gap:5px, flex:1, minWidth:0]
      ├─ Text  (kicker)
      ├─ Text  (title)
      └─ Text  (date)
```
Vertical stack (the default column): `Container[lfDisplay:flex, flexDirection:column, gap:16px]`.

## Style props (verified, by where they apply)

**Box / layout:** `lfDisplay`, `flexDirection`, `justifyContent`, `alignItems`,
`gap`, `flexWrap`, `flex`, `flexShrink`, `columns`, `width`, `maxWidth`,
`height`, `maxHeight`, `minWidth`, `padding`, `margin`.
**Type (Title/Text/BlockLink):** `fontFamily`, `fontSize`, `lineHeight`,
`fontWeight`, `letterSpacing`, `color`, `textAlign`, `textTransform`,
`whiteSpace`, `align`.
**Surface:** `backgroundColor`, `backgroundImage`, `backgroundPosition`,
`borderRadius`, `borderStyle`, `borderWidth`, `borderColor`, `boxShadow`,
`objectFit` (Image).

### Value formats (important)
- **Colors are objects, not hex:** `{"r":10,"g":10,"b":10,"a":1}`. (Inside HTML
  `content` strings you may use `#hex`/`rgb()` normally.)
- **Sizes are CSS strings:** `"16px"`, `"100%"`, `"720px"`, `"fit-content"`.
- **`padding`/`margin` are objects:** `{"top":"12px","right":"24px","bottom":"12px","left":"24px"}` (any subset).
- **Enums:** `lfDisplay`∈{block,flex,grid}; `flexDirection`∈{row,column};
  `justifyContent`∈{flex-start,center,flex-end,space-between};
  `alignItems`∈{flex-start,center,flex-end}; `objectFit`∈{contain,cover};
  `textAlign`∈{left,center,right}; `fontWeight`∈{300,400,500,600,700,800,normal};
  `textTransform`∈{uppercase}; `borderStyle`∈{solid,dashed}.
- **Responsive:** add `"media": 991` (or 767) to a style entry to override it at
  that breakpoint. Multiple entries of the same prop with different `media` stack.
  **Verified mobile pattern** (`media: 767`): to reflow a desktop row-card into a
  stacked mobile card, override on the row `flexDirection: column` + `alignItems:
  center`; make fixed-width children full width (`width: 100%` @767 on the thumb
  wrapper and the right column); center text with `textAlign: center` @767; shrink
  headings (`fontSize`/`lineHeight` @767) and table cells (`fontSize` + smaller
  `padding` @767); a `flexWrap: wrap` grid (reviews) collapses to one column when
  each card also has `width: 100%` @767. LF honors these on the live storefront.
  Note: `media` only restyles the SAME content — it cannot swap different copy per
  breakpoint (a design with distinct mobile text needs a separate mobile page).
- **Dual-DOM breakpoint toggle (verified) — when a mobile design REORDERS content
  that CSS reflow can't produce.** `media` reflow only works when desktop and mobile
  share one DOM order; a row→column stack keeps children in the same sequence. If the
  mobile Figma *interleaves* pieces differently — e.g. the ranked-card mobile order is
  `badge → name → score → IMAGE → trustpilot → features → button → price`, where the
  image sits mid-stack but is a separate LEFT column on desktop — no `order`/reflow of
  the 3-column desktop DOM can reach it (CSS `order` only reorders siblings within one
  flex container, and the image would have to split the middle column). The fix: build
  BOTH cards and toggle with `lfDisplay`. Desktop card root gets
  `{"prop":"lfDisplay","value":"none","media":767}` (hidden on phones); the mobile
  card root gets base `{"prop":"lfDisplay","value":"none"}` +
  `{"prop":"lfDisplay","value":"flex","media":767}` (hidden on desktop, shown on
  phones). Interleave them in the DOM (`[desktop, mobile]` per item); only one renders
  per breakpoint, dividers/rounded-last-row work in each. Costs duplicate DOM but lets
  each breakpoint match its own Figma frame exactly. Used for the TEST 2 listicle
  cards (desktop node 2:108 = 3-col row, mobile node 3:841 = 1-col centered stack).
- **Mobile build checklist (from a dedicated mobile Figma frame).** First read the
  mobile frame in full (it's tall — parse via subagent, see `figma-inspect.md`), then:
  1. **Page gutter** — the mobile column is inset (~28px in a 375 frame). Add
     `{"prop":"padding","value":{"left":"22px","right":"22px"},"media":767}` on the
     article column. Keep full-bleed bars (dark sponsored/logo header) OUTSIDE that
     padded column so they still span edge-to-edge.
  2. **Same content, different layout → `media:767` reflow** (row→column, full-width
     children, `textAlign:center`, shrink headings/table cells).
  3. **Reordered/interleaved content → dual-DOM toggle** (above).
  4. **Swapped copy → dual-DOM.** e.g. desktop meta = category pills; mobile = plain
     byline (`3:861`). `media` can't change text, only style.
  5. **Dropped element → hide it,** don't delete: add `lfDisplay:none @767` to the
     desktop-only block (e.g. the yellow "[Update: stock limited]" urgency box, absent
     from the mobile frame `3:1209`). Grep the parsed mobile dump to confirm absence.
  6. **Match the table's REAL cell font + column widths — don't shrink to fit.** The
     mobile Figma table (`3:1263`) uses **14px** cells and deliberately wraps headers/long
     names (`Year\n1`, `Whoop\n5.0`, `Garmin\nVivoactive\n6`). Shrinking the font (e.g. to
     11px) to force everything single-line *diverges* from the design — reproduce the 14px
     and let it wrap. Match column proportions to the Figma cell widths (Device 83 / Year 51
     / Year 51 / Total 51 / Subscription 102 → flex `1.6/1/1/1/2`), or the widest header
     ("Subscription") gets squeezed. Set the row `alignItems:center` so single-line values
     center vertically against 2–3-line device names.
  7. **Verify at 390px** with a device-emulated Playwright shot + section crops, and
     assert desktop-only blocks are actually hidden (`getComputedStyle().display`).
- **Theme binding:** `"boundTo": "static_heading_font"` (etc.) ties a value to the
  funnel's global style. Fine to omit and set explicit values.

### Node cheat-sheets
- **Title:** `p:{size:"1".."6", content, widthOption:"fill"}` + `fontSize`,
  `lineHeight`, `fontWeight`, `letterSpacing`, `color`, `textAlign`, `margin`.
- **Text:** `p:{content}` — `content` accepts inline HTML: `<a href style>`,
  `<b>`, `<span style="color:#d62828">`. Use this for inline links, bold runs,
  colored pills, mixed formatting on one line.
- **BlockLink (button):** `p:{destination, target}` + `backgroundColor`, `color`,
  `borderRadius`, `padding`, `fontWeight`, `width:"fit-content"`, and
  `lfDisplay:flex, alignItems:center, justifyContent:center` to center its label.

## Images — must be LF-hosted to lay out correctly

External `src` (e.g. hotlinked from another CDN) **renders full-width and breaks
flex rows.** LF-hosted images carry `src_id` + `src_uid`
(`https://assets.lightfunnels.com/account-<acct>/images_library/...`) and size
correctly.

Two ways to get an image into the library (both session mode). Map the result
into an `Image` block: `src_id = _id` · `src_uid = uid` (`img_...`) · `src = path`.

**A. From a public URL (verified, preferred for web/Framer sources):**
```graphql
mutation($url: String!) { importImage(url: $url) { id _id uid title path key } }
```
Helpers: `lf_api.import_image(token, url, extra_headers)`, `lf_api.image_block_from(result)`.

**B. From a local file (Figma exports, generated images, auth-gated sources):**
presigned upload via `getSignedUrls`.
1. `getSignedUrls(inputs: [{ name, owner: ResourceOwner, resourceType: ResourceType2, contentType }]) → [{ url, fields }]`
2. HTTP POST the file bytes to `url` with the returned `fields` (S3-style form POST).
3. Read back the image's `id`/`uid` from the library for the block.
Use A whenever a public URL exists; B only when the file is local.

## Writing a page (mechanics)

- Real edits require **session mode** (`edit --session`, `duplicate`, `createStep`
  via the session token). App tokens cannot write bodies. See SKILL.md.
- Write whole steps via `updateFunnel { steps: [...] }` (session). `steps` is
  `[InputUpdateStep]` — it **only UPDATES steps that already exist** (matched by
  `id`); a brand-new `id` is silently a no-op. Send only changed steps; siblings
  are preserved (verified).
- A malformed `body` → generic `Oops! Something went wrong` (not a permission
  error). Validate structure against this reference.

### Brand-new funnel from scratch (verified recipe, session mode)

`createFunnel` makes an **empty** funnel (`steps: []`), and `updateFunnel.steps`
can't create the first step. The working 3-step recipe:

1. `createFunnel(node:{name, slug, funnel_steps:["article_page"], currency, lang})`
   → funnel id (steps empty).
2. `createStep(funnel_id, node: InputStep{slug,title,type,settings:{},visual:{x,y},body})`
   → returns `{ step { id uid _id ... } }` (query the `step` subfield — the
   mutation returns a `CreateStep` wrapper, not a `Step`). The step now EXISTS but
   is **not yet in the funnel's workflow graph** (`funnel.steps` still empty, the
   canvas shows nothing).
3. `updateFunnel(id, node:{ starting_step_id: <step.id>, steps:[ InputUpdateStep{
   id:<step.id>, slug, title, type, settings:{}, visual:{x,y}, body } ] })`
   → registers the step into the workflow. Now `funnel.steps` lists it and the
   page renders. (Set `starting_step_id` so it's the entry page.)

To overwrite an existing page later, just repeat step 3 with the new `body`.

## Images from a local file — presigned upload (verified)

`importImage(url)` needs a public URL and **times out on very large images**
(20MB+ Figma originals). For local files (Figma exports, resized web images):

1. Resize/compress first (the S3 policy caps uploads at **5 MB**). `sips -Z 1400
   in.png --out out.png` works with no deps.
2. `getSignedUrls(inputs:[{name, owner:"account", resourceType:"images_library",
   contentType}])` → `[{ url, fields }]`.
3. POST `multipart/form-data` to `url` with **all `fields` first, then a `file`
   field last** (S3 form POST). Success = HTTP 204.
4. The object is now at `https://assets.lightfunnels.com/<fields.key>`. Call
   `importImage(<that CDN url>)` — small + same-CDN, so it's fast — to get the
   `{_id, uid, path}` record for the `Image` block (`src_id`/`src_uid`/`src`).

## BlockLink (button) label — it's a CHILD, not `p.content`

A CTA renders as an **empty pill** if you set the label via `p.content`. Real
structure (verified): the label lives in `p.children`.
```
BlockLink  p:{ destination:{type:"static", value:"<url>"}, target:"_blank",
               widthOption:"auto", children:[ <label> ] }
           styles:[ backgroundColor, borderRadius, padding, lfDisplay:flex,
                    alignItems:center, justifyContent:center ]
  └─ Container[lfDisplay:flex, alignItems:center, justifyContent:center]
       └─ Text  content:"GET UP TO £79 OFF"  (color/fontWeight/textTransform here)
```
Note `destination` is an **object** `{type:"static", value}`, not a plain string.

## Images in fixed-height crops (match a design's cropped boxes)

A design usually shows a photo inside a fixed-height box with `object-fit:cover`.
Rendering the raw image at `width:100%` lets a portrait source balloon to full
height. Reproduce the crop: `Image` styles `width:100%` + `height:"<box>px"` +
`objectFit:"cover"` + `lfDisplay:"block"`. Add a `media:767` height override for a
shorter mobile crop.

## Design → Lightfunnels mapping (quick table)

| Source (Figma auto-layout / CSS) | Lightfunnels |
|---|---|
| Auto-layout frame / flex container | `Container` + `lfDisplay:flex` |
| Direction horizontal / vertical | `flexDirection: row` / `column` |
| Gap / item spacing | `gap` |
| Align / justify | `alignItems` / `justifyContent` |
| Fixed width child | wrapper `Container[width:Npx, flexShrink:0]` |
| Fill container child | `flex:1, minWidth:0` |
| Heading text style | `Title` (`size` + `fontSize`/`lineHeight`/`fontWeight`) |
| Body text style | `Text` (`fontSize`/`lineHeight`/`fontWeight`/`color`) |
| Inline link / bold / colored span | HTML inside `Text.content` |
| Button / CTA | `BlockLink` (bg, radius, padding, `destination`) |
| Image fill / fit | `Image` + `objectFit: cover` / `contain` (LF-hosted) |
| Color token | `{r,g,b,a}` object |
| Section / page band | `Section` (`layout:"boxed"` to constrain width) |
| Breakpoint override | duplicate style entry with `media: 991`/`767` |
