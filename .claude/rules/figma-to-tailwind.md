# Figma auto-layout → Tailwind

The mapping is mechanical. Read the value off the node and look it up here — never
eyeball a screenshot and never approximate. If a measured value has no Tailwind step,
use an arbitrary value (`gap-[13px]`), do **not** round to the nearest step.

## Layout direction

| Figma | Tailwind |
|---|---|
| `layoutMode: HORIZONTAL` | `flex flex-row` |
| `layoutMode: VERTICAL` | `flex flex-col` |
| `layoutMode: NONE` | `relative` + absolutely positioned children |
| `layoutWrap: WRAP` | `flex-wrap` |
| `itemReverseZIndex: true` | `flex-row-reverse` / `flex-col-reverse` |

## Alignment

`primaryAxisAlignItems` runs **along** the layout direction → `justify-*`.
`counterAxisAlignItems` runs **across** it → `items-*`.

| Figma | Tailwind |
|---|---|
| `MIN` | `justify-start` / `items-start` |
| `CENTER` | `justify-center` / `items-center` |
| `MAX` | `justify-end` / `items-end` |
| `SPACE_BETWEEN` | `justify-between` |
| `BASELINE` (counter axis) | `items-baseline` |

## Spacing

| Figma | Tailwind |
|---|---|
| `itemSpacing: 16` | `gap-4` |
| `counterAxisSpacing: 12` (wrapped) | `gap-x-* gap-y-3` |
| `paddingTop/Right/Bottom/Left` equal | `p-<n>` |
| vertical == horizontal | `py-<n> px-<n>` |
| all four differ | `pt-* pr-* pb-* pl-*` |

Tailwind's scale is `4px × n`: `1`=4, `2`=8, `3`=12, `4`=16, `6`=24, `8`=32, `10`=40,
`12`=48, `16`=64. A measured 13px is `p-[13px]`, not `p-3`.

## Sizing

| Figma | Tailwind |
|---|---|
| `layoutSizingHorizontal: FILL` | `w-full` (or `flex-1` inside a row) |
| `layoutSizingHorizontal: HUG` | `w-auto` |
| `layoutSizingHorizontal: FIXED` | `w-[<width>px]` |
| `layoutSizingVertical: FILL` | `h-full` / `self-stretch` |
| `layoutSizingVertical: HUG` | `h-auto` |
| `layoutSizingVertical: FIXED` | `h-[<height>px]` |
| `layoutGrow: 1` | `grow` |
| `maxWidth` on the frame | `max-w-[<n>px]` |

**FILL inside a row is `flex-1`, not `w-full`.** `w-full` on a flex child that has
siblings overflows the row — this is the single most common conversion bug.

## Borders, radius, effects

| Figma | Tailwind |
|---|---|
| `cornerRadius: 12` | `rounded-xl` (8=`rounded-lg`, 16=`rounded-2xl`, 9999=`rounded-full`) |
| per-corner radii | `rounded-tl-* rounded-tr-* …` |
| `strokeWeight: 1` + stroke colour | `border border-<token>` |
| `strokeAlign: INSIDE` | default; `OUTSIDE` needs `outline` instead |
| `DROP_SHADOW` effect | `shadow-*`, or `shadow-[0_2px_8px_rgba(0,0,0,0.08)]` when it does not match a step |
| `opacity: 0.5` | `opacity-50` |
| `clipsContent: true` | `overflow-hidden` |

## Typography

Read `fontSize`, `fontWeight`, `lineHeightPx`, `letterSpacing` and map through
`design-tokens.md` — do not invent a scale.

| Figma | Tailwind |
|---|---|
| `fontSize: 16`, `lineHeightPx: 24` | `text-base leading-6` |
| `fontWeight: 700` | `font-bold` (400 `font-normal`, 500 `font-medium`, 600 `font-semibold`, 800 `font-extrabold`) |
| `letterSpacing: -0.32` on 16px | `tracking-[-0.02em]` |
| `textAlignHorizontal: CENTER` | `text-center` |
| `textCase: UPPER` | `uppercase` |
| `textDecoration: UNDERLINE` | `underline` |

Line height is authored in **px** in Figma and is a **ratio** in Tailwind's named steps.
When the ratio is not clean, use `leading-[24px]`.

## Responsive

Figma frames are fixed widths; Tailwind is mobile-first. A desktop frame at 1440 and a
mobile frame at 375 are **two designs**, not one that reflows. Build the mobile values
as the base and layer the desktop frame's values at `md:` / `lg:`.

Never let a desktop-only value be the base — that is how a layout breaks on phones,
which is where the traffic is.

## Photos are not a CSS problem

A frame's `Photo` node is a **box with an image fill**, and the fill has its own crop.
Two frames of the same page routinely crop the same photograph differently — the 1440w
frame at `720×460`, the 390w frame square and framed wider. `object-cover` on the
desktop asset cannot get to the mobile crop: it centre-crops, and the design did not.

So do not derive one breakpoint's photo from another's file. Export each node's own
render and art-direct between them:

```
figwright save_screenshots  nodeIds=["<Photo node id>", …]  scale=3  outDir=…/crops
```

```tsx
<picture className="contents">
  <source media="(min-width: 768px)" srcSet={desktopSrc} />
  <img src={mobileSrc} className="aspect-square md:aspect-[720/460] …" />
</picture>
```

`className="contents"` on the `<picture>` keeps the `<img>` as the flex item, so the
layout is identical to a bare `<img>`.

**This is invisible to every check that is not pixels.** The box is the right size, the
file is the right file, the alt text is right, nothing 404s, no console error. Only
`design_diff.py --crops` catches it. Run it.

## A node name can be an instruction

`H2 · set family to Delight Semi Bold` means the frame has **Poppins applied and Delight
intended** — the name is the instruction, the applied font is the placeholder. Build the
name.

The corollary matters more: a node **without** that suffix wants the font it actually
has. `Quote` is `Poppins Medium`, and setting it in the brand display face because the
headings nearby use one is a real defect — it reads heavier and tighter than the design,
and no size/weight/colour comparison will notice, because those are all still correct.

`design_diff.py` reads the instruction out of the node name and compares the resolved
family, so a wrong typeface now fails rather than passing quietly.

## FILL means stretch, and `items-center` cancels it

`layoutSizingHorizontal: FILL` is `w-full`, and it stays `w-full` inside a
`flex flex-col items-center`. Flex centring sizes children to their content, so a FILL
child silently shrinks to its text — the design says the box is 900 wide, the page makes
it 780, and because the text is centred anyway it looks right until a longer line wraps
where the design would not have.

Put `w-full` on the child rather than removing `items-center`, which other children may
need.

`design_diff.py` compares the width of every FILL node, which is how this one surfaced
on a page that had already passed 73/73 on copy and typography.
