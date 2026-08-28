# Hard constraints

Violations fail the build. They are not style preferences — each one exists because
breaking it produces code that cannot be themed, cannot be regenerated, or does not run.

## 0. The project's own instructions outrank these

`hlth-site/CLAUDE.md` and the `AGENTS.md` it imports are the authority on that codebase.
These rules cover one thing only: how a Figma frame becomes markup. Where they disagree,
the project wins — and its conventions were earned by measurement, not preference.

That file also warns that **this is Next 16 + React 19, not the Next.js in your training
data**. Read the relevant guide in `node_modules/next/dist/docs/` before writing Next
code.

## 1. No hardcoded colours

No hex, `rgb()`, `hsl()` literal, or named colour anywhere in `components/` or `app/`.
Every colour resolves to an `hlth-*` token.

```tsx
// ✗
<div className="bg-[#4af59f] text-[#000000] border-[#1f2937]" />
<div style={{ color: "#4AF59F" }} />

// ✓
<div className="bg-hlth-green text-hlth-black border-hlth-border" />
```

Hex belongs in exactly one place: the `@theme` block in `app/globals.css`. Check it
first — the palette is small and a near-match usually IS the token. A Figma fill of
`#4AF59F` is `hlth-green`, not a new colour. If it is genuinely new, add it to `@theme`
with an `hlth-` prefixed role name, then use the utility. Method:
`../.claude/rules/design-tokens.md`.

Exempt: `app/globals.css`, and `fill`/`stroke` inside an imported SVG asset.

## 2. Do not invent a parallel system

There is **no shadcn/ui** in this project and **no `tailwind.config.ts`** — Tailwind v4
is configured in CSS. Do not add either, do not introduce `cva`/`cn()` conventions the
codebase does not already use, and do not create a second set of design tokens beside
the `hlth-*` ones.

Reuse what exists. `components/` already has `Money`, `LocalizedLink`, `TrustpilotStars`,
`PriorityFillImage` and more — a generated component that re-implements one of those is
wrong even if it renders correctly.

## 3. TypeScript and lint must be clean

```bash
npx tsc --noEmit    # gate 1
npm run lint        # gate 2
```

Both exit 0 before anything is built. **This repo has no test runner** — these two are
the only automated gates it has, so a red one is not a warning, it is the whole safety
net. No exceptions for "unrelated" errors.

- No `any`, implicit or explicit. Use `unknown` and narrow it.
- No `@ts-ignore`. `@ts-expect-error` is allowed only with a comment saying why and what
  removes it.
- Every component's props are an explicit `interface`.
- `strict: true` stays on.

## 4. Local only

This harness builds and serves on localhost. It does not deploy, does not push, and runs
no git command. Reviewing the result and deciding what happens to it is a human's job.

## 5. Design values are measured, not estimated

Every size, colour, spacing and radius comes from a figwright node read. A value that
looks close is wrong. If content does not fit at the design's real values, fix the
layout — column widths, flex proportions, container width — never the typography.

Copy is verbatim: exact punctuation, currency symbols, casing, and dash characters.

## 6. Accessibility is part of "done"

- Every interactive element has an accessible name.
- Every `<img>` / `next/image` has meaningful `alt`, or `alt=""` when decorative.
- Exactly one `<h1>` per page; heading levels do not skip.
- Interactive targets are at least 44×44px.
- Text meets WCAG AA contrast (4.5:1 body, 3:1 large).

## 7. Secrets never enter the repo

Env vars live in Vercel project settings. `NEXT_PUBLIC_*` is shipped to the browser —
everything else is server-only. `.env*` and `.vercel/` are gitignored.
