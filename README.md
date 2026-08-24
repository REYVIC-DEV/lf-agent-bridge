# Lightfunnels ↔ Agentic Coder Bridge (lf-agent-bridge)

A dependency-free CLI + Claude Code **skill** that lets an agentic coder
(Claude Code, Codex, Cursor, …) create and edit Lightfunnels funnels
programmatically — instead of manual editing in the Lightfunnels UI.

## What an agent can do — two modes

Lightfunnels treats a permanent **app token** differently from a temporary
**browser session token** (both verified live). The bridge uses each for what
it's good at:

| Goal | App token (`.env`) | Session token (`--session`) |
|---|---|---|
| List / read funnels & page copy | ✅ | ✅ |
| Rename, slug, publish, delete | ✅ | ✅ |
| Create a funnel with real pages (`duplicate`) | ✅ | ✅ |
| **Edit page copy for real** (saved to the page, shows in editor) | ❌ | ✅ |
| Add a new page (`createStep`) | ❌ | ✅ |
| Edit copy render-time only (`header_scripts` patch) | ✅ | ✅ |

App tokens are blocked from writing page bodies
(`non_allowed_app_funnel_update`) — that's a platform rule for third-party
apps. A **session token** (copied from the LF dashboard's own network requests)
is not an app, so it writes real page bodies — the same access the LF editor
has. This is how AI page-studio apps like Pixelier work: they use your login
session. Trade-off: session tokens expire; the app token is permanent.

So: app token for structure (duplicate/publish/rename), `--session` for real
copy edits. The old render-time `header_scripts` patch is still there as a
no-session fallback (inspectable via `patch`, reversible via `patch-clear`), but
it only shows on the live page, not in the editor.

## Setup

```bash
python3 get_token.py --client-id <ID> --client-secret <SECRET>   # one-time OAuth → .env
python3 lf.py funnels                                            # smoke test
```

Run everything from the project root. The scripts resolve `.env` and the session
files next to themselves (in ``), so cwd doesn't matter —
except for the ad-hoc `build_*.py` / `figma_rest.py` scripts, which read them
from the current directory (`cd the repo root` first).

Get `client_id`/`client_secret` from a [Partners area](https://partners.lightfunnels.com/)
app (Configurations tab). The token is permanent — keep `.env` out of git.

### Session token (only needed for real page-copy edits)

1. Log into `app.lightfunnels.com`, open DevTools → **Network** → filter **Fetch/XHR**.
2. Click around (e.g. open Funnels) so a request to `services.lightfunnels.com/api/v2` appears.
3. Open that request → **Headers** → copy the value after `Authorization: bearer `,
   and note the `account-id` header.
4. Save it locally (never commit): `echo 'PASTE_TOKEN' > .session_token`
5. Use it: `python3 lf.py edit <funnel_id> --session --account-id <ACCT> --replace "old==new"`

Session tokens expire — if `--session` starts failing with auth errors, re-grab it.

## Usage

```bash
python3 lf.py duplicate fun_XXXX --name "Sleep V3" --slug sleep-v3   # new variant
python3 lf.py publish <new_id> --off                                 # dups inherit published!
python3 lf.py texts <new_id>                                         # read the copy
python3 lf.py edit <new_id> --replace "Old headline==New headline"   # change it
python3 lf.py publish <new_id>                                       # go live
```

Run `python3 lf.py --help` for all commands.

## For the agentic coder

- **Claude Code**: the `lightfunnels` skill (`.claude/skills/lightfunnels/SKILL.md`)
  loads automatically when you ask for funnel work.
- **Other agents**: point them at `AGENT.md`.

## Layout

The bridge itself lives at the repo root; everything built on top of it is
grouped into its own directory. See `docs/ARCHITECTURE.md` for the full map.

- `lf.py` — agent-facing CLI (all commands, JSON output)
- `lf_api.py` — GraphQL client + primitives (duplicate, text extraction, patch engine)
- `lf_session.py` — keeps a browser session alive for page-body writes
- `get_token.py` — one-command OAuth flow → `.env`
- `server.py` — legacy HTTP wrapper around the bridge (see `legacy/`)
- `docs/LIGHTFUNNELS_API.md` — full API knowledge base + **Field-Verified Addendum**
  (platform limits, undocumented mutations, quirks found by live testing)
- `docs/ARCHITECTURE.md` — map of every subsystem in this repo
- `docs/PRODUCT_PRICE.md` — our product's price in the visitor's currency,
  live from Shopify (`data-price`): **exact, matches checkout**. Tagging,
  install, QA per market
- `docs/CURRENCY_CONVERTER.md` — converting any *other* GBP figure
  (`data-fx-gbp`): competitor prices, editorial sums. **Mid-market,
  indicative only** — never our own price
- `.claude/skills/lightfunnels/SKILL.md` — the Claude Code skill
- `funnels/` — local funnel workspaces (funnel.json, NOTES.md, steps/, texts/,
  edits/); see `funnels/README.md`
- `templates/` — archived page bodies (`capture` output; read-only reference)
- `legacy/` — the old HTTP-server bridge (its write path predates the platform
  restriction and does not work)
- `pagescore/` — the autonomous page-performance-tuning loop (`benchmark.py`
  ground-truth harness + `build_*.py` iteration scripts), run from the repo
  root, e.g. `python3 pagescore/benchmark.py <url>`
- `content/` — scraped source material (`extract_techunboxed.py` +
  `extracted/`) used as raw copy/structure input when building new pages
- `autoresearch/` — an unrelated external reference project (its own git repo)
  that `pagescore/program.md`'s autonomous-loop design is modeled on
