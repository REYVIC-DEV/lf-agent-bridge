---
name: lightfunnels
description: Create, edit, and manage Lightfunnels funnels agentically via the GraphQL API. Use when the user wants to create a funnel, duplicate/clone a funnel, edit funnel or page copy, publish/unpublish, or anything mentioning Lightfunnels. Replaces manual editing in the Lightfunnels UI.
---

# Lightfunnels agent bridge

Drive Lightfunnels with `lf.py` (project root). Every command prints JSON.
Full API reference: `docs/LIGHTFUNNELS_API.md` (§ "Field-Verified Addendum"
documents behavior discovered by live testing that the official docs omit).

**Building or cloning page layouts?** Read
`references/block-schema.md` FIRST. It is the verified Lightfunnels block
vocabulary (node types, style props, the `lfDisplay:flex` layout model, image
hosting) plus a design→LF mapping table. Author page bodies from it — never
guess builder props. When translating a Figma design, pull structure via the
Figma MCP (auto-layout maps directly to LF's flex model), then map to LF blocks
using that reference.

**Inspecting a design in full detail?** Read
[references/figma-inspect.md](references/figma-inspect.md) — the measure-don't-guess
method (walk nodes for exact colors/fonts/geometry/auto-layout, deep-read the specific
element, export assets) plus the three ways to read a Figma file and their limits.

**Doing mobile responsiveness from a separate mobile Figma frame?** The mobile frame is
tall — parse the whole node in a subagent, then match it (don't eyeball). Mobile is NOT
just desktop reflowed: it reorders content (→ dual-DOM `lfDisplay` toggle), swaps copy,
drops elements (hide with `lfDisplay:none @767`), adds a page gutter, and keeps table
cells at their REAL font (don't shrink to force single-line). Full method +
measure/verify checklist: `figma-inspect.md` ("Long/tall mobile frames", "Per-breakpoint
differences") and `block-schema.md` ("Mobile build checklist"). Verify at 390px with a
device-emulated Playwright shot cropped into sections.

**Figma access is seat-limited — know the options.** All three official-ish paths:
- **figwright MCP** (`@figwright/mcp` + its Figma plugin) — reads the file you have
  **open** via the Plugin API, **no seat cap**, effectively unlimited. **Preferred for
  heavy/iterative inspection.** `.mcp.json` is already configured in this project; the
  human installs the plugin (repo's latest release → Figma → Plugins → Development →
  Import plugin from manifest…) and runs it with the file open (127.0.0.1:3055).
- **Figma REST API** (`figma_rest.py`, `FIGMA_TOKEN` in `.env`, scope *File content =
  Read-only*): `get_nodes(key, ids)` = geometry/auto-layout/fills/typography;
  `export_images(key, ids, scale=2)` = render URLs for any frame. Then
  `lf_api.upload_local_image(session_token, path, HH)` hosts each in the LF library.
  **But a View seat gets only ~6/month on Tier-1 (file/nodes/images)** — 429 `Retry-After`
  seen at ~4.6 days. Batch ids into one call; spend sparingly.
- **Figma MCP** (`get_design_context`) — rich but its per-seat tool-call cap hits fast.

fileKey + nodeId come from the design URL (`?node-id=1640-2196` → `1640:2196`).

Also in that reference (all verified live): **local image upload** (resize →
`getSignedUrls` → S3 POST → `importImage` the CDN url), the **BlockLink label is
a child node** (not `p.content`, or the button renders as an empty pill), and
**fixed-height image crops** (`height` + `objectFit:cover`) to match a design's
cropped photo boxes.

**Preview gotcha:** the storefront caches each preview URL, so after a session
write the change can lag a few minutes on the SAME url. Preview at the
step-slug url `https://<store>/<funnel-slug>/<step-slug>?preview=true` (the
funnel-root url caches hardest); renaming the step slug forces an instant fresh
render. Publishing purges the cache.

```bash
python3 lf.py <command> ...        # run from the lf-agent-bridge directory
```

## TWO MODES — read first

There are two ways to authenticate, with very different powers (both verified
live 2026-07-22):

**App-token mode (default).** The permanent OAuth token in `.env`. Can read
everything and write funnel *settings* (name, slug, publish, header_scripts),
but **cannot write page bodies** — `updateFunnel.steps` and `createStep` are
refused with `non_allowed_app_funnel_update` / Forbidden. This is a platform
rule for third-party apps, not a scope issue; don't retry or work around it.

**Session mode (`--session`).** A browser **session token** is NOT treated as an
app, so it **can write real page bodies** — the same access the LF editor has.
This is how AI page-studio apps (e.g. Pixelier) work: you use the login session.

Session tokens expire, so the bridge keeps one alive without re-copying:

```bash
python3 lf.py login     # ONE-TIME: opens a real browser, you sign in (2FA ok).
                        # Saves the session to .lf_state.json (no password stored).
python3 lf.py refresh   # headless: reuses that session to write a fresh token.
```

After `login`, `edit --session` **auto-refreshes** the token if it expired
mid-run (retries once). The account id is captured by `login` too, so you don't
need `--account-id` after that. If refresh says the session expired, run `login`
again. (Manual fallback still works: `echo 'TOKEN' > .session_token`.)

Capability matrix:

| Action | App token | Session (`--session`) |
|---|---|---|
| Read funnels/pages | ✅ | ✅ |
| Rename / slug / publish / delete | ✅ | ✅ |
| `duplicate` a funnel | ✅ | ✅ |
| **Edit page copy (real, persists in editor)** | ❌ | ✅ |
| Add a new page (`createStep`) | ❌ | ✅ |
| Edit copy at render-time only (`header_scripts`) | ✅ | ✅ |

So: use the **app token** for everything structural (duplicate, publish,
rename), and add **`--session`** when you need to actually change page copy.
Layout/image/section changes beyond text are possible in session mode by
manipulating the body JSON, but are not yet wrapped in a command — do them in
the LF editor unless the user asks to go deeper.

## Auth (once)

Token resolution: `--token` flag → `LF_ACCESS_TOKEN` env → `.env` file.
If no token exists, the human runs the OAuth flow once:

```bash
python3 get_token.py --client-id <ID> --client-secret <SECRET>   # from partners.lightfunnels.com → app → Configurations
```

Saves a **permanent** token to `.env`. Never print, log, or commit it.

## Core workflows

### 1. Inspect

```bash
python3 lf.py funnels                    # list funnels (id, name, slug, published)
python3 lf.py funnel <funnel_id>         # one funnel + steps (uid, slug, title, type)
```

`<funnel_id>` is the opaque id, e.g. `fun_UK-PeZ5kAFhnpBkWvo9jo`.

### 2. Create a funnel

**(a) Duplicate a master** — fastest when a good template exists:

```bash
python3 lf.py duplicate <master_funnel_id> --name "Sleep V3" --slug sleep-v3
```

Clones every page. Duplicates inherit `published` from the source — run
`publish --off` right after if it shouldn't be live yet.

**(b) Brand-new from scratch (session)** — verified 3-step recipe, use when
building a fresh page (e.g. from a Figma design), no master needed:

1. `createFunnel` → funnel id (comes back with `steps: []`).
2. `createStep(funnel_id, node)` → read the `step { id }` subfield. The step now
   EXISTS but is detached (not yet on the canvas).
3. `updateFunnel(id, { starting_step_id: <id>, steps:[ {id, slug, title, type,
   settings:{}, visual, body} ] })` → attaches it into the workflow so it renders.

Full mechanics + copy-paste example: `references/block-schema.md` §
"Brand-new funnel from scratch". (The bare `create` command still makes an empty
shell; prefer the recipe above or `build_*.py`-style scripts for real pages.)

### 3. Edit page copy (the agentic-editing loop)

```bash
python3 lf.py texts <funnel_id>                        # all visible copy, per step

# REAL edit (recommended) — persists to the page, shows in the LF editor:
python3 lf.py edit <funnel_id> --session --account-id <ACCT> \
  --replace "Customer Reviews==Verified Buyer Reviews" \
  --replace "Get My Plan==Start Tonight"

# Render-time-only fallback (app token, no session needed):
python3 lf.py edit <funnel_id> --replace "Old==New"
python3 lf.py patch <funnel_id>                        # show render-time patch
python3 lf.py patch-clear <funnel_id>                  # remove render-time patch
```

- `--replace` is `"exact current text==new text"`, repeatable; bulk via
  `--file edits.json` (`{"old": "new", ...}`).
- **Run `texts` first and copy the exact string.** `edit` validates every
  target against the real page copy and fails loudly on no-match (`--force`
  to override, e.g. for text split across HTML tags).
- `--session` rewrites the actual page body (verified non-destructive — only
  the steps that contain a match are touched; siblings are preserved). It needs
  `.session_token` + `--account-id` (or `LF_ACCOUNT_ID`). If it fails with an
  auth/`Oops` error, the session token likely expired — re-grab it.
- Without `--session`, edits are a render-time `header_scripts` patch: they show
  on the live page but NOT in the LF editor. Prefer `--session` for real work.

### 4. Publish / manage

```bash
python3 lf.py publish <funnel_id>          # go live  (confirm with user first)
python3 lf.py publish <funnel_id> --off
python3 lf.py rename <funnel_id> --name "New name" --slug new-slug
python3 lf.py delete <funnel_id> --yes     # IRREVERSIBLE — explicit user confirmation required
```

### Escape hatch

Anything else (products, orders, discounts, …) via raw GraphQL — look up the
shape in `docs/LIGHTFUNNELS_API.md` first:

```bash
python3 lf.py gql --query 'query { products(first: 5, query: "") { edges { node { id title } } } }'
```

Undocumented-but-working: `duplicateFunnel(funnel_id)`, `importFunnel(code)`.
GraphQL `__type` introspection works; `__schema` is blocked.

## Hard rules

1. **Step bodies are writable only in `--session` mode.** With the app token
   they're platform-blocked — don't retry. Real copy edits → `edit --session`;
   render-only edits → `edit`.
2. **`texts` before `edit`.** Copy exact strings; never guess page copy.
3. **Confirm before `publish` and `delete`.** Duplicates of published funnels
   start published — unpublish them unless told otherwise.
4. **Token hygiene.** Never echo the app token OR the session token into logs,
   output, or commits. `.session_token` and `.env` stay local (gitignored).
   The session token = being logged in as the user; treat it as sensitive.
5. **Test destructive/body edits on a duplicate first**, not on a live funnel.
6. On GraphQL errors read the `key` field (e.g. `errors_dup_slug` = slug taken).
   Common keys: `docs/LIGHTFUNNELS_API.md` § Errors.
