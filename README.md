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
python3 tools/lf-agent-bridge/get_token.py --client-id <ID> --client-secret <SECRET>   # one-time OAuth → .env
python3 tools/lf-agent-bridge/lf.py funnels                                            # smoke test
```

Run everything from the project root. The scripts resolve `.env` and the session
files next to themselves (in `tools/lf-agent-bridge/`), so cwd doesn't matter —
except for the ad-hoc `build_*.py` / `figma_rest.py` scripts, which read them
from the current directory (`cd tools/lf-agent-bridge` first).

Get `client_id`/`client_secret` from a [Partners area](https://partners.lightfunnels.com/)
app (Configurations tab). The token is permanent — keep `.env` out of git.

### Session token (only needed for real page-copy edits)

1. Log into `app.lightfunnels.com`, open DevTools → **Network** → filter **Fetch/XHR**.
2. Click around (e.g. open Funnels) so a request to `services.lightfunnels.com/api/v2` appears.
3. Open that request → **Headers** → copy the value after `Authorization: bearer `,
   and note the `account-id` header.
4. Save it locally (never commit): `echo 'PASTE_TOKEN' > .session_token`
5. Use it: `python3 tools/lf-agent-bridge/lf.py edit <funnel_id> --session --account-id <ACCT> --replace "old==new"`

Session tokens expire — if `--session` starts failing with auth errors, re-grab it.

## Usage

```bash
python3 tools/lf-agent-bridge/lf.py duplicate fun_XXXX --name "Sleep V3" --slug sleep-v3   # new variant
python3 tools/lf-agent-bridge/lf.py publish <new_id> --off                                 # dups inherit published!
python3 tools/lf-agent-bridge/lf.py texts <new_id>                                         # read the copy
python3 tools/lf-agent-bridge/lf.py edit <new_id> --replace "Old headline==New headline"   # change it
python3 tools/lf-agent-bridge/lf.py publish <new_id>                                       # go live
```

Run `python3 tools/lf-agent-bridge/lf.py --help` for all commands.

## For the agentic coder

- **Claude Code**: the `lightfunnels` skill (`.claude/skills/lightfunnels/SKILL.md`)
  loads automatically when you ask for funnel work.
- **Other agents**: point them at `AGENT.md`.

## Layout

Root holds only the agent-facing files; the bridge itself lives in `tools/`.

```
.claude/skills/lightfunnels/   the Claude Code skill (SKILL.md + references/)
.mcp.json                      figwright MCP server config
AGENT.md                       same contract for non-Claude agents
funnels/                       local funnel workspaces — see funnels/README.md
├─ _template/                  skeletons: workspace.json + funnel/
└─ <workspace>/<funnel-slug>/  funnel.json, NOTES.md, steps/, texts/, edits/
tools/lf-agent-bridge/
├─ lf.py                       agent-facing CLI (all commands, JSON output)
├─ lf_api.py                   GraphQL client + primitives (duplicate, text extraction, patch engine)
├─ lf_session.py               browser-session login/refresh (optional playwright)
├─ get_token.py                one-command OAuth flow → .env
├─ figma_rest.py               Figma REST helpers (get_nodes / export_images)
├─ build_*.py                  ad-hoc page builders (run from this directory)
├─ docs/LIGHTFUNNELS_API.md    full API knowledge base + Field-Verified Addendum
│                              (platform limits, undocumented mutations, live-tested quirks)
├─ SOP.md / SOP.pdf            operating procedure
├─ templates/                  archived page bodies (capture output; gitignored)
└─ legacy/                     old HTTP-server bridge (write path predates the
                               platform restriction and does not work)
```
