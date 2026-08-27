---
categories:
  - "[[Web-Tech]]"
subjects:
  - "[[Lightfunnels]]"
focus_area: email-exclusive moved to /blog/template, and the routing rule written down
page: "[[email-exclusive-route-move]]"
status: in-progress
created: 2026-08-26
commit: f89cf37
run_id: emailx-template-002
tags:
  - hlth-site
  - routing
  - webforge
---

# 2026-08-26 — email-exclusive moved to /blog/template, and the routing rule written down

Page: [[email-exclusive-route-move]] · Index: [[LF Page Pipeline]]

**Result:** 1 PASS, 0 FLAG, 0 FAIL

## What moved

| | From | To |
|---|---|---|
| Route | `app/[locale]/pages/email-exclusive/` | `app/[locale]/blog/template/email-exclusive/` |
| Component | `components/figma/` | `components/email-exclusive/` |

The route is now `noindex, nofollow` and `alternatesFor()` is gone, matching its four
siblings in the gallery. It is listed in `/blog/template`'s index, filling a hole that
page calls out itself: all four campaign advertorials left on 2026-08-20 to become live
ad destinations, so no long-form example remained.

`components/figma/` was my own invention and broke the documented convention —
`components/` is grouped by the route it serves (`article-template/`,
`blog-collection/`, `aura/`), never by where the design came from. Origin is the one axis
nobody searches by.

## ⚠️ This path is not reachable in production

`/blog/template/*` is hidden five ways, and the fifth catches people out: `proxy.ts`
rewrites it to a non-existent path on the real store domains, keyed on `isPublicHost` —
the same predicate as robots/noindex. It renders on localhost and the Vercel alias and
**404s on `hlthtrack.com`**.

So **email traffic cannot be sent here.** Promoting it is the move those four made, and
the route's docstring and `.claude/rules/component-architecture.md` both spell out the
five steps.

## Written down, which was the point

`.claude/rules/component-architecture.md` gained a **"Where a design's route goes"**
section: the three destinations, what each means for indexability and production
reachability, the five ways the gallery is hidden, the promotion checklist, and the
component-folder rule.

**Corrected later the same session.** I first wrote that section as a default — *"default
an article design to `/blog/template/`"* — and was told to scratch it: *"the better way is
to always ask where to put or where path before doing anything."* Right, and a default is
still a guess. The route on this one page was corrected twice
(`/email-exclusive` → `/pages/email-exclusive` → `/blog/template/email-exclusive`), which
is the evidence for asking rather than for a smarter default.

The table stays, because an answer still has to be acted on. What went is me picking.
`page-pipeline/SKILL.md` now asks for the route before stage 1, and if no answer comes it
builds the component and stops at the route — the component is identical either way, so
waiting costs nothing. Saved as a durable preference in memory.

## Verified

| | |
|---|---|
| `tsc --noEmit` / `npm run lint` | clean |
| `npm run build` | succeeds |
| Runbook | **PASS** every phase |
| 1440 — text / images / geometry | **72 OK + 1 accepted · 7/7 · 0** |
| 390 — text / images / geometry | 68 OK + 1 accepted · 7/7 · 0 |
| Gallery index links it | yes |
| `noindex, nofollow` served | yes, confirmed in the production build |

One regression I caused and fixed: rewriting the route trimmed the meta description to
110 chars and phase 3 flagged it. Restored to 151, and deliberately stating no price —
the two frames disagree and a meta description is the worst place to bake an unsettled
figure, because it is what search and social quote back at you.

## A pre-existing thing this surfaced

In a **production build**, `/pages/definitely-not-a-real-page` returns **HTTP 200** with
the branded not-found body. Every missing `/pages/<handle>` is a soft 404. Not caused by
this move — a nonsense handle behaves identically — and it lives in
`app/[locale]/pages/[handle]`, which serves the whole Shopify pages surface, so it is
flagged rather than touched.

## Measured (emailx-template-002)

| Page | Verdict | Speed | Links | Meta | Mobile | Console | A11y |
|---|---|---|---|---|---|---|---|
| email-exclusive | **PASS** | SKIP | PASS | PASS | PASS | PASS | PASS |

Full findings: `pagescore/runs/emailx-template-002/findings.json`


## Needs a human answer

- [ ] Offer price — the 1440w frame says £79 / Save 50%, the 390w frame says £67.15 / Save 57%. Still the only fidelity failure, and now explicitly a template-content question rather than a live-offer one.
- [ ] Soft 404 on /pages/* (pre-existing, not from this move): a missing Shopify handle returns HTTP 200 with the branded not-found body, in a production build. Every /pages/<anything> is a soft 404. Worth a look — it is in app/[locale]/pages/[handle], which serves the whole Shopify pages surface, so I have not touched it.

## Next

- [ ] If this becomes a live email campaign: git mv to app/[locale]/pages/email-exclusive, drop the noindex, restore alternatesFor(), add an entry to lib/ad-landers.ts so the template path 308s, and re-run the manifest.

---

Written by `pagescore/session_note.py`. Runbook `pagescore/program.md`.
