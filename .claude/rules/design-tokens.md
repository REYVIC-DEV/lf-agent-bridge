# Colour and type in hlth-site

Measured from the repo on 2026-08-25, not assumed. **Next 16, React 19, Tailwind v4.**
There is no shadcn/ui and no `tailwind.config.ts` — Tailwind v4 is configured in CSS.

## What the token system actually is

`app/globals.css` has an `@theme` block. Tailwind v4 turns each `--color-*` entry into
utilities automatically — `--color-hlth-green` gives `text-hlth-green`, `bg-hlth-green`,
`border-hlth-green`.

```css
@theme {
  --font-sans: var(--font-inter), ui-sans-serif, system-ui, …;
  --color-hlth-green:    #4af59f;   /* 33 uses */
  --color-hlth-green-80: #4ade80;   /*  0 uses — defined, never used */
  --color-hlth-gray:     #8a95a3;   /* 26 */
  --color-hlth-black:    #000000;   /* 68 */
  --color-hlth-white:    #ffffff;   /* 55 */
  --color-hlth-border:   #1f2937;   /* 15 */
  --hlth-header-h: 65px;            /* v3 header, read back by HeaderV3 */
}
```

One more custom property is published from JS at runtime, not from `@theme`:
**`--hlth-sticky-bar-h`** — the bottom sticky bar's height varies with layout, so it is
measured and set from script. `--hlth-header-h` is its static counterpart at the top.

## The thing you must know before writing any colour

**The token system is not the dominant practice in this codebase.**

| | Uses |
|---|---|
| `hlth-*` token utilities | ~439 |
| Arbitrary hex utilities (`bg-[#07060f]`) | **~1,536**, across 245 of 386 files |
| Distinct hex values in use | **209** |

So a blanket "never write a hex" rule is wrong here — it would produce components that
look nothing like the 245 files around them. The real problem is not that hex is used;
it is that **fourteen colours are used like tokens without being tokens**:

| Colour | Uses | What it is |
|---|---|---|
| `#07060f` | 550 | Primary near-black. Also `body { color }` in globals.css |
| `#737276` | 95 | Mid gray, secondary text |
| `#d0ed29` | 91 | Lime accent |
| `#020203` | 57 | Deepest black |
| `#f5f5f7` | 53 | Light surface |
| `#fafafa` | 35 | Lighter surface |
| `#63821a` | 30 | Dark lime |
| `#55545e` | 29 | Gray |
| `#121212` | 27 | Near-black |
| `#3c3b45` | 26 | Gray |
| `#ececee` | 20 | Hairline / surface |
| `#c6c5cc` | 19 | Gray |
| `#8fa614` | 17 | Mid lime |
| `#ddddde` | 16 | Hairline |

⚠️ **The same colour is written two ways.** `#07060f` appears 510 times lowercase and
248 times uppercase. `#d0ed29` is 72/63. `#f5f5f7` is 51/23. Grep for one spelling and
you miss a third of the usages.

## The decision ladder — follow it in order

1. **A token covers it → use the token.** A Figma fill of `#4AF59F` is `hlth-green`,
   not a new colour. Check `@theme` first; the palette is small.
2. **It is one of the fourteen above → use the arbitrary utility, lowercase.**
   `bg-[#07060f]`, never `bg-[#07060F]`. This matches ~1,500 neighbouring usages and is
   the right call until someone tokenizes them.
3. **It is a genuinely new colour → stop and flag it.** Do not add a 210th distinct hex.
   Either it maps to something above, or it is a design decision a human should make.

**Always write hex lowercase.** The codebase is split; generated code should not add to
the mess.

## Worth proposing, not doing unasked

The top four (`#07060f`, `#737276`, `#d0ed29`, `#f5f5f7` — 789 uses between them) are
obvious `@theme` candidates. Tokenizing them is a repo-wide refactor with real risk
across 245 files, so it is a human's call, not something a generation run does on the
side. Raise it; don't act on it.

## Type

Fonts come through `next/font` in `lib/fonts.ts`, surfaced as two utilities in
`app/globals.css`:

- `.font-display` → **Delight SemiBold** (self-hosted, `fonts/Delight-SemiBold.woff2`)
- `.font-body` → **Poppins** (400/500/600)

Both resolve `var(--font-delight, var(--font-sans))` **at the element**, inside
`@layer utilities`. Everything outside the v3 subtree falls back to **Inter**.

⚠️ **Three traps, all documented in the site's own `CLAUDE.md` after costing real time:**

1. Brand fonts are **v3-only** — applied at the v3 route level. Using `.font-display`
   outside that subtree silently renders Inter and reads as a CSS bug.
2. Defining the font vars in `@theme` (`:root`) **does not work** — it silently fell
   back to Inter. They must resolve at the element.
3. `next/font` preloads a face in a route's **module graph**, not one actually rendered.
   Importing `lib/fonts` from a shared component leaks ~42 KB onto every route that
   imports it — measured, partly fixed, still leaking via `cart/v3/CartV3Mount.tsx`.
   Do not make it worse.

Sizes map onto Tailwind's default scale; a design size with no step is an arbitrary
value (`text-[17px]`). Never round the design to fit the scale.

## The visual ground truth is the live site

The site's `CLAUDE.md` says it plainly: **`hlthtrack.com` is the visual ground truth.**
Where the Figma frame and the live site disagree, that is a question for a human — not
something to resolve by quietly picking one.
