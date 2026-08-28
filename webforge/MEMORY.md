# MEMORY — what carries across runs

Append-only. `CONTEXT.md` is wiped every run; this is not. Write here when something is
learned that would otherwise be rediscovered the hard way, and keep each entry short
enough to actually be read.

Worth recording: a Figma→Tailwind conversion that needed a non-obvious fix, a build error
and what actually caused it, a Vercel behaviour that surprised you, a shadcn primitive
that could not express a design and what replaced it.

Not worth recording: anything already in `RULES.md` or `../.claude/rules/`.

---

## Recurring layout fixes

**FILL inside a horizontal auto-layout is `flex-1`, not `w-full`.**
`w-full` on a flex child with siblings overflows the row. This is the most common
conversion bug by a wide margin — check it first when a row is too wide.

**A desktop frame and a mobile frame are two designs, not one that reflows.**
Real designs reorder content, swap copy, and drop elements between breakpoints. Build the
mobile values as the base and layer desktop at `md:`/`lg:`. A desktop-only base breaks on
phones, which is where the traffic is.

**Figma line height is px; Tailwind's named steps are ratios.**
When the ratio is not clean, use `leading-[24px]` rather than the nearest step.

## Build and deploy

**A green `tsc` with a red `npm run build` is normal.**
The build catches what types cannot: server/client boundary violations, a missing
`"use client"`, bad metadata, failed static generation. Never skip gate 2 because gate 1
passed.

## Completed runs

<!-- runs -->
