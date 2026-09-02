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

## Harness environment (added 2026-09-02)

**`have()` was blind on Windows, and it reported the `claude` CLI missing when it was
installed.** The probe ran `execFileSync("command", ["-v", cmd], { shell: "/bin/sh" })`.
Node on win32 cannot use `/bin/sh` as a shell, so the call threw for EVERY binary and
`have()` returned false for all of them — `node` and `npx` included, proven by probe:

```
platform: win32
  claude    old=false new=true
  node      old=false new=true
  npx       old=false new=true
  not-real  old=false new=false
```

That is what failed run `2026-09-01T10-31` at GENERATE_CODE with "The `claude` CLI is not
on PATH", on a machine where `where claude` resolves `...\.localin\claude.exe`. Fixed
in `src/harness/harness.ts` — `where` on win32, `command -v` elsewhere. If a future
"tool not installed" message appears on Windows, check the probe before the tool.

## Target-repo rules that were WRONG in CLAUDE.md (corrected 2026-09-02)

All three were verified by measurement against the target repo, not by reading it once:

1. **"Never a raw hex"** — false for this repo. Only six `hlth-*` tokens exist, and
   `components/` measures **1,567 raw-hex arbitrary classes vs 189 token uses**. The v3
   and article designs use ~30 colours with no token. Raw hex IS the house style for
   design-specific values; inventing tokens would break the "no second token set" rule.
2. **"Compose classes with `cn()` from `src/lib/utils`"** — there is no `cn()` and no
   `src/` in the target repo. The same page said "There is no `src/` directory" four
   lines earlier, so the file contradicted itself.
3. **"`next/image` for images"** — the repo sets `images.loader: 'custom'` and
   deliberately does NOT use Vercel's optimizer; content images are plain `<img>` with an
   `eslint-disable`. Product imagery goes through the Shopify loader.

**Lesson for this harness: the target repo's own `CLAUDE.md` outranks this one, and where
the two disagree, MEASURE the repo and fix this file.** A confidently-worded rule that
does not match the codebase produces confidently-wrong components.

## design_diff.py had a UTF-8 bug that faked failures (found + fixed 2026-09-02)

`json.load(open(args.spec))` had no encoding, so on Windows Python used the cp1252
locale default for a UTF-8 design dump. Every non-ASCII character arrived as mojibake
and the copy check reported a FALSE difference:

```
figma  'How much higher womenâ€™s average resting heart rate ...'
live   'How much higher women’s average resting heart rate ...'
-> RETYPED, similarity 0.944, on strings that were identical
```

Fixed in four places: the spec read, the `--accept` read, and both report writes (the
.md was being emitted as cp1252, so the report itself was unreadable in a UTF-8 tool).
**These designs are full of curly apostrophes, em dashes and currency symbols, so on
Windows this quietly poisoned the one check the tool exists to perform.** If a copy
diff shows a near-1.0 similarity on what looks like the same string, suspect encoding
before suspecting the build.

## Use --accept for deliberate deviations, or the signal decays

A documented, intentional divergence otherwise shows as RESTYLED forever and the run
is permanently amber, which trains everyone to ignore it. Record it in an accept file
with the REASON and the run goes green with an ACCEPTED count. Example that earned it:
the article CTA's pill label is Inter Bold 700 in Figma, but Inter is not loaded on v3
routes and `lib/fonts.ts` ships Poppins at 400/500/600, so it renders Poppins SemiBold.

## A sweep is per-breakpoint, not per-page

Desktop and mobile are two designs. On the HLTH article blocks the stat card steps
11/40/16 -> 10/28/14 and the CTA headline 22 -> 20, body 16 -> 15, so one spec cannot
cover both and a desktop-only pass would have missed any mobile type regression
entirely. Run `--viewport 390 --mobile` as its own pass with its own spec.

Result of the first full sweep (54 design_diff runs, 14 articles x 2 blocks x 2
breakpoints, ~188 node checks): every string verbatim, every size/weight/colour
correct, only the one accepted font deviation. Driver kept at
`hlth-shopify-frontend/.scratch/fidelity/sweep.py`.

## Completed runs

<!-- runs -->
