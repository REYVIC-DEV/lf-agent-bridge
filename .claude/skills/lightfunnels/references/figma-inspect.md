# Inspecting a Figma design in full detail (measure, don't guess)

> **Golden rule: ALWAYS match the node.** Read the exact value from the Figma node and
> reproduce it — font size, weight, line-height, color, padding, gap, radius, box size,
> column width, wrap behavior. **Never approximate, round, or substitute** a value because
> it's "close enough," and **never change a design value to make something fit** (e.g. do
> not shrink a 14px table cell to 11px so text stops wrapping). If content doesn't fit at
> the node's real values, fix the *layout* (column widths/flex proportions, container
> width, gutter), not the design's typography. When a value looks off, re-read the node
> before overriding it. Verify the measured values against the live render, then reconcile
> any difference back to what the node actually says.

To reproduce a design 1:1 as Lightfunnels blocks you must read the **actual values**
of every element — colors, fonts, sizes, gaps, paddings, radii, per-state colors —
and export the assets you can't recreate. This is the method used to build the HLTH
advertorial and the "top-5 fitness trackers" listicle. Pair it with
[block-schema.md](block-schema.md) (the LF target vocabulary).

## Three ways to read a Figma file — pick by seat/limits

| Source | How | Limit reality |
|---|---|---|
| **figwright MCP** (preferred for heavy/iterative work) | Figma **Plugin API** via a local plugin + `@figwright/mcp`. Reads the file you have **open** in the desktop app. | **No seat cap** — local, effectively unlimited. Works on Figma free tier. Needs the plugin running + file open. |
| **Figma REST API** (`figma_rest.py`) | `X-Figma-Token` PAT. `get_nodes` (styles/geometry) + `export_images` (render any frame). | **Seat-capped.** A **View/Collab seat** gets only ~**6/month** on Tier-1 endpoints (GET file / nodes / images). 429 returns `Retry-After` — observed **~4.6 days**. Dev/Full seat = 10–20/min. |
| **Figma MCP** (`get_design_context`/`get_metadata`) | Official Anthropic Figma connector. Rich reference code + screenshot. | **Seat-capped tool calls** — a View seat hits `reached the Figma MCP tool call limit` fast. |

Practical rule: **use figwright for the detailed, back-and-forth inspection** (dozens of
node reads + asset exports). Fall back to REST only for a few precise reads when
figwright isn't set up, and spend that tiny budget carefully (batch ids into one call).

**figwright setup:** `.mcp.json` → `{"mcpServers":{"figwright":{"command":"npx","args":["-y","@figwright/mcp@latest"]}}}`;
install the plugin from the repo's latest GitHub release (Figma desktop → Menu → Plugins →
Development → Import plugin from manifest…), run **Plugins → Development → Figwright** with the
target file open (it connects on `127.0.0.1:3055` and shows *Connected*), reload the agent, test with `ping`.

## What to extract for every element

Walk the node tree and, per node, record:

- **Geometry** — `absoluteBoundingBox` (x, y, width, height). Reveals fixed sizes
  (e.g. a 76×76 thumbnail, an 18×18 star box) and true reading widths.
- **Layout (→ LF flex)** — `layoutMode` (`HORIZONTAL`/`VERTICAL` → `flexDirection`
  row/column), `itemSpacing` (→ `gap`), `paddingTop/Right/Bottom/Left` (→ `padding`),
  `primaryAxisAlignItems`/`counterAxisAlignItems` (→ `justifyContent`/`alignItems`).
- **Fills** — SOLID `color` → hex → LF `{r,g,b,a}`. `type: IMAGE` means it's a photo
  (export it, don't recreate). Note gradients.
- **Strokes** — border `color` + `strokeWeight` → `borderColor`/`borderWidth`.
- **`cornerRadius`** → `borderRadius`.
- **Text** — `characters` (verbatim copy) + `style`: `fontSize`, `lineHeightPx`,
  `fontWeight`, `letterSpacing`, `textAlignHorizontal`, and the fill color.

Order of operations: **structure first** (metadata/shallow walk to get node ids and
grouping), then **deep-read the specific element** you're matching (the star strip, the
table wrapper, one card, one review). Verify values *before* building.

## Compact node inspector (REST or figwright JSON)

```python
def rgba(c): return "#%02x%02x%02x"%(round(c['r']*255),round(c['g']*255),round(c['b']*255)) if c else None
def fills(n):
    o=[]
    for f in (n.get("fills") or []):
        if not f.get("visible",True): continue
        o.append("IMG" if f.get("type","").startswith("IMAGE") else rgba(f.get("color")))
    return o
def bb(n):
    b=n.get("absoluteBoundingBox") or {}; return round(b.get("width",0)),round(b.get("height",0))
def walk(n,d=0,maxd=6):
    if d>maxd: return
    t=n.get("type"); w,h=bb(n); p=[]
    if n.get("layoutMode"): p.append("%s gap=%s pad=%s/%s/%s/%s"%(n["layoutMode"][:1],n.get("itemSpacing"),n.get("paddingTop"),n.get("paddingRight"),n.get("paddingBottom"),n.get("paddingLeft")))
    fl=fills(n);  p += ["f="+",".join(fl)] if fl and fl!=["#ffffff"] else []
    ss=n.get("strokes") or []
    if ss and n.get("strokeWeight"): p.append("stroke=%s/%s"%(rgba(ss[0].get("color")),n["strokeWeight"]))
    if n.get("cornerRadius"): p.append("r=%s"%round(n["cornerRadius"]))
    if t=="TEXT":
        s=n.get("style",{}); p.append("TXT '%s' %s/%s w%s %s %s"%(n.get("characters","")[:24],s.get("fontSize"),round(s.get("lineHeightPx",0)),s.get("fontWeight"),rgba((n.get('fills') or [{}])[0].get('color')),s.get("textAlignHorizontal")))
    if t=="TEXT" or (fl and fl!=["#ffffff"]) or n.get("layoutMode") or ss:
        print("  "*d+f"{t}[{n.get('name','')[:20]}] {w}x{h} "+" ".join(map(str,p)))
    for c in n.get("children",[]) or []: walk(c,d+1,maxd)
```

## Long / tall mobile frames — analyze the WHOLE thing, don't rush

A full mobile page frame (e.g. a 375×12000+ advertorial) is huge: `get_node` on it
returns **hundreds of KB** and figwright/Read will refuse it ("exceeds maximum allowed
tokens", saved to a `tool-results/*.txt` file). Do **not** eyeball a screenshot and guess
— take the time to read every node and confirm its attributes. Proven method:

1. **Pull the whole frame node** (`mcp__figwright__get_node <mobileFrameId>`). When it
   overflows, it's written to a `.txt` — note the path.
2. **Parse it in a subagent**, not your main context. Hand the subagent the file path and
   tell it to `json.loads` + walk the tree with the inspector above, returning a
   **complete top-to-bottom ordered spec**: every section's width/x-offset/bg/padding/
   radius, every TEXT node's *verbatim* `characters` + size/weight/color/align, image
   box sizes, layout direction + gaps, and badges/pills/stars/buttons with exact colors.
   Be explicit it must read 100% of the file and quote text verbatim (a vague "summarize"
   loses detail). This keeps the 500KB dump out of your context but still measures it all.
3. **Deep-read the specific sub-nodes you're matching** with a scoped `get_node` (one
   card, the table wrapper, the byline) — those are small and fit inline. Use
   `search_nodes {name:"BEST OVERALL"}` to jump straight to an element and get its id +
   parent chain, then walk up (`get_node` on the parentId) to see the card's layout.
4. **Compare desktop vs mobile frames explicitly.** The mobile frame's node ids differ
   from desktop's; read BOTH card containers to learn what genuinely changes per
   breakpoint (order, which elements are dropped, copy). See "per-breakpoint differences"
   below — these drive `media`-override vs dual-DOM decisions.

## Verify the built page at the real breakpoint (don't trust "it should reflow")

After writing, screenshot the LIVE storefront with a device-emulated browser and read it
back — LF's flex reflow does not always match your mental model. Playwright (python is
installed):

```python
pg=b.new_page(viewport={"width":390,"height":844},device_scale_factor=2,is_mobile=True)
pg.goto(url,wait_until="networkidle"); pg.wait_for_timeout(2500)
pg.screenshot(path="m.png",full_page=True)         # full_page can be 25000+px tall
```

A full-page mobile shot is too tall to read at once — **crop it into sections** with
`sips -c <h> <w> --cropOffset <top> 0 m.png --out part.png` and Read each crop. Also
assert visibility programmatically, e.g. check a desktop-only box is hidden on mobile:
`pg.evaluate("...getComputedStyle(el).display!=='none' && el.offsetParent!==null")`.
Rename the step slug each rebuild (`...-v2, -v3`) so the storefront serves a fresh render.

## Per-breakpoint differences (mobile is NOT just desktop reflowed)

Real designs change *content and structure* between the desktop and mobile frames, not
only styling. Confirmed on the HLTH listicle (desktop node `2:108` vs mobile `3:841`):

- **Reordered card** — desktop 3-col `image | details | score/cta`; mobile 1-col centered
  `badge → name → OUR SCORE → image → trustpilot → features → cta → price`. The image sits
  mid-stack on mobile. CSS reflow can't produce this → **dual-DOM toggle** (build both,
  `lfDisplay:none`/`flex` at `media:767`). See block-schema.md.
- **Swapped copy** — desktop meta row = colored category pills ("Buying Guides" / "Trending");
  mobile (node `3:861`) = a plain byline "By **Marcus Pendleton** | Contributions from Kate
  Smith | Last updated June 2026". Different text ⇒ dual-DOM, not a `media` restyle.
- **Dropped element** — the yellow "[Update: … stock is limited]" urgency box exists on
  desktop but is **absent** from the mobile frame (`3:1209`). Grep the parsed dump for its
  text/color to confirm absence, then hide it on mobile with `lfDisplay:none` @767.
- **Page gutter** — the mobile frame has ~28px left/right padding on the content column
  (375 frame → 319 column). Add it as `padding:{left,right} media:767` on the article
  column; keep full-bleed bars (sponsored/logo header) outside that padded column.

## Assets: export, don't recreate

Logos, product shots, screenshots, gifs, icon lockups → export the node
(`figma_rest.export_images(key,[id],scale=2)` or figwright's screenshot/asset export),
download, then `lf_api.upload_local_image(session_token, path, session_headers)` to host it
in the LF library and get `{src_id,src_uid,src}` for an `Image` block. Resize >5 MB first
(`sips -Z 1400`). Small recreatable marks (colored star boxes, pills) can be HTML in a
`Text`, but match the measured color/size exactly.

## Pitfalls learned (verify these specifically)

- **A "heading" may be a banner.** Measure its fill — e.g. the listicle's "best picks"
  line is a `#28282b` bar with white 16px text, not a plain `Title`.
- **Tables = one bordered box + rows, not separate cards.** Outer `Container`
  (`border 1px #e5e7eb`, `radius 12`) wrapping a header row + rows with a 1px bottom
  divider (`#eef0f2`); the individual rows have stroke-weight 0.
- **Rating stars are colored by score.** Trustpilot bands seen: 4.4→`#00b67a`,
  3.2→`#ffce00`, 1.8/1.6/1.5→`#ff8622`; empty box `#dcdce6`. Fill uses **half-star
  rounding** (`round(rating*2)/2`); render a half box with a 50% gradient.
- **An image node taller than its display box crops** with `objectFit:cover` (the Fitbit
  76×93 shot in a 76×76 box lost its top). Use `objectFit:contain` + a white wrapper when
  the source isn't the box's aspect ratio.
- **Badges are often plain colored text, not pills** (e.g. "★ BEST OVERALL" is `#f5a623`
  text, no background).
- **Copy verbatim.** Text node `characters` includes exact punctuation (£, –, —, %, ✅, ❌).
