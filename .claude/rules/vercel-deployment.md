# Verification and deployment

> **Not in use yet.** The harness is local-only right now: it builds, serves on
> localhost, and stops. Nothing here runs. This document is the plan for when the
> project does start deploying — gates 1, 2 and 4 already apply locally; gates 3 and 5
> are the parts that are switched off.

Nothing reaches production without passing every gate below, in order. Each gate is
cheap relative to the one after it, so a failure costs the least possible time.

```
  typecheck → build → deploy PREVIEW → QA the preview URL → promote to production
     ~5s        ~30s        ~45s            ~2 min              ~15s
```

## Gate 1 — types

```bash
npx tsc --noEmit
```

Must be clean. Not "only warnings", not "only in files I did not touch". A generated
component that does not typecheck is not a component.

## Gate 2 — build

```bash
npm run build
```

Catches what `tsc` cannot: bad imports, server/client boundary violations, missing
`"use client"`, invalid metadata, failed static generation. A green typecheck and a red
build is normal and means the code is wrong.

## Gate 3 — preview deploy

```bash
npx vercel --yes            # NOT --prod
```

Prints a unique preview URL. **This is the deployment that gets QA'd.**

Deploying straight to `--prod` means the public sees the page before anything has
checked it. Preview URLs are the reason this pipeline can iterate safely at all — unlike
the Lightfunnels side of this repo, where the publish toggle *is* the deploy and there is
no staging. Do not skip preview because a change looks small.

## Gate 4 — QA the preview URL

Reuse the judges already in this repo. They take a URL and know nothing about the
platform behind it, so they work unchanged against a Vercel preview:

```bash
python3 pagescore/qa_runner.py <preview-url> --run-id <run-id>
python3 pagescore/design_diff.py <figma-dump.json> <preview-url> --out pagescore/runs/<run-id>
```

`qa_runner.py` covers redirects, PageSpeed, links, meta and social tags, four viewports,
console errors and accessibility, against `pagescore/program.md`. `design_diff.py` proves
the page matches the Figma frame — copy that never made it, copy that was retyped rather
than copied, typography that does not match the node.

Any **FAIL** stops the pipeline here. Fix and redeploy a new preview.

## Gate 5 — promote

```bash
npx vercel --prod --yes
```

Only after gate 4 is clean. Promoting an already-built preview is near-instant and
serves the exact artifact that was tested — not a rebuild that might differ.

## Rollback

```bash
npx vercel rollback           # previous production deployment
npx vercel ls                 # find a specific one
```

Vercel keeps every deployment immutable, so rollback is instant and total. Use it the
moment production looks wrong; diagnose afterwards, not while users are on a broken page.

## Environment

- `vercel login` once per machine; CI uses `VERCEL_TOKEN`.
- Secrets go in Vercel project env vars, never in the repo. `NEXT_PUBLIC_*` is shipped
  to the browser — anything else is server-only.
- `.vercel/` is generated and gitignored.
