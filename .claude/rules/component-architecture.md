# hlth-site component architecture

Measured from the repo on 2026-08-25 — 322 components under `components/`, 386 `.tsx`
files including `app/`. Match these patterns; a generated component that is technically
correct but shaped unlike its neighbours is still wrong.

## Where files go

There is **no `src/` directory.** The tree is:

```
app/          App Router routes + globals.css
components/   322 components, grouped by feature/route
lib/          shopify client, fonts, i18n, identity, analytics
fonts/        self-hosted Delight-SemiBold.woff2
public/
```

`components/` is grouped **by the page it serves**, not by component type — `home/`,
`product/`, `cart/`, `about/`, `blog/`, `contact/`, `science/`, `care/`. Truly shared
pieces sit flat at the top (`Money.tsx`, `LocalizedLink.tsx`, `JsonLd.tsx`).

## The v3 split — the biggest structural fact

Many features exist twice: `components/home/` and `components/home/v3/`,
`components/product/` and `components/product/v3/`. v3 is the newer brand; v2 is what
much of the live store still runs.

They differ in more than styling — **v3 carries the brand fonts, v2 stays on Inter**, and
the font vars only exist on the v3 route subtree. So:

- Putting a v3 component on a v2 route silently renders it in Inter.
- `.font-display` / `.font-body` outside the v3 subtree resolve to `var(--font-sans)`.

**Before writing a component, establish which side it belongs to** and put it in the
matching folder. Ask if the design does not make it obvious.

## Conventions, as actually practised

| Convention | Reality |
|---|---|
| Exports | **Named**, 316 of 322 files. Only 2 default exports. |
| Server vs client | 139 of 322 are `'use client'` — 43%. Server is the default. |
| One component per file | Yes, named for the file. |
| Props | Explicit `interface`, no implicit `any`. |

`'use client'` goes on **the smallest leaf that needs it**, never a whole section for one
interactive control. The site's `CLAUDE.md` documents the split-the-island pattern and
points at PDP v3 as the reference. Marking a section client because one button inside it
has an `onClick` puts all the surrounding static copy on the hydration path.

## Reuse before you write

These already exist and are widely imported. A generated component that re-implements
one is wrong even if it renders correctly:

| Component | Imported by | Use it for |
|---|---|---|
| `LocalizedLink` | 48 files | **Every internal link.** The store is multi-locale; a raw `next/link` drops the market prefix. |
| `Money` | 29 files | **Every price.** Store currency is GBP and formatting is locale-aware. |
| `JsonLd` | 17 files | Structured data. |
| `TrustpilotLink` | 10 | Trustpilot link-out. |
| `PlainLink` | 5 | Non-localized links. |
| `TrustpilotStars` | 3 | The rating star strip. |
| `PriorityFillImage` | 2 | LCP `fill` images. |
| `AutoplayVideo` | 2 | Autoplaying video with the right attributes. |

Two of those are not optional. **Prices go through `Money`** and **internal links go
through `LocalizedLink`** — hardcoding either breaks a market silently, which is the kind
of bug that shows up as lost revenue in one country rather than as a broken page.

Before writing anything new, search `components/` for what the design element already is.
322 files is a lot of prior art.

## Next 16 is not the Next.js you remember

`AGENTS.md` warns this explicitly, and the site's `CLAUDE.md` repeats it: **read the
relevant guide in `node_modules/next/dist/docs/` before writing Next code.** Known
divergences from training data:

- `fetch` is **not cached by default** — every call opts in with `revalidate` + cache
  `tags`.
- `proxy.ts` at the repo root, not the middleware you may expect.
- Turbopack is the bundler.

## The gates

There is **no test runner.** Two commands are the entire automated safety net:

```bash
npx tsc --noEmit
npm run lint
```

Both must exit 0. A red one is not a warning — it is the whole net.

## Where a design's route goes — ASK, do not infer

**Ask for the path before writing anything.** Not after the component builds, not as a
note in the summary — before. This is the one decision that has been got wrong twice on
the same page: first built at `app/[locale]/email-exclusive`, corrected to
`/pages/email-exclusive`, corrected again to `/blog/template/email-exclusive`. Nothing in
the design says which, because it is not a design question — it is a question about what
the page is *for*, and only the person commissioning it knows that.

It is also not a cheap mistake to fix later. The destinations differ in whether the page
is **indexable** and whether it is **reachable on the production domain at all**, so a
wrong guess either publishes something that should have stayed private or hides something
that was meant to take traffic.

Measured from the repo on 2026-08-26 — this table is here so the answer can be acted on,
not so it can be guessed from:

| Destination | Indexable | On `hlthtrack.com` | What lives there |
|---|---|---|---|
| `app/[locale]/blog/template/<name>/` | `noindex, nofollow` | **404s** | Reusable article / advertorial layouts |
| `app/[locale]/pages/<name>/` | indexable, `alternatesFor()` | serves | Live campaign pages and Shopify-style pages |
| top level (`cart`, `products`, `learn`, …) | indexable | serves | Functional site areas |

If the answer does not arrive, build the component and stop at the route — the component
is identical either way, so nothing is wasted by waiting, and there is nothing to undo.

### `/blog/template/` is hidden five ways, and the fifth surprises people

`noindex, nofollow` · absent from the sitemap · `Disallow: /blog/template/` in robots.txt
· unlinked from the site · **and rewritten to a non-existent path on the real store
domains** (`proxy.ts`, keyed on `isPublicHost` — the same predicate as robots/noindex).

So it renders on the Vercel alias and localhost and **404s on `hlthtrack.com`**. A 404
there is the guard working, not a broken build. It also means **you cannot send email or
ad traffic at a `/blog/template/*` URL** — move the page to `/pages/` first. That is the
move all four campaign advertorials made on 2026-08-20, and `lib/ad-landers.ts` still
drives the 308s from their old template paths.

### Promoting a template to a live page

1. `git mv` the route directory to `app/[locale]/pages/<name>/`.
2. Drop `robots: { index: false, follow: false }`.
3. Restore `alternates: alternatesFor(PATH, locale)` — the sibling landers all carry
   canonical + hreflang.
4. Add an entry to `lib/ad-landers.ts` so the old path 308s rather than 404s.
5. Re-run the QA manifest against the new URL; nothing about the component changes.

### Component folder follows the route, not the tool that made it

`components/<route-name>/` — `article-template/`, `blog-collection/`, `aura/`,
`email-exclusive/`. **Not** a folder named after where the design came from: a
`components/figma/` groups by origin, which is the one axis nobody ever searches by, and
it drifts from the 322 files around it the moment a second design lands.
