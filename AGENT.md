# AGENT.md — Driving the Lightfunnels bridge

For any agentic coder (Claude Code loads this automatically via the
`lightfunnels` skill in `.claude/skills/lightfunnels/SKILL.md` — this file is
the same contract for Codex/Cursor/others).

## Interface

```bash
python3 lf.py <command> ...      # from the project root; prints JSON
```

The bridge lives in ``; the project root holds only the
agent files (`.claude/`, `.mcp.json`, `AGENT.md`, `README.md`).

Funnel working copies live in `funnels/<workspace>/<funnel-slug>/` (a workspace
groups related funnels — one brand/store/campaign). Captured page bodies go in
`steps/`, `texts` snapshots in `texts/`, edit sets in `edits/`. Start one by
copying `funnels/_template/funnel/`. Convention: `funnels/README.md`.

Token: `--token` flag > `LF_ACCESS_TOKEN` env > `.env`. One-time setup:
`python3 get_token.py --client-id <ID> --client-secret <SECRET>`.

`lf.py`, `lf_session.py` and `get_token.py` read/write `.env`, `.session_token`,
`.lf_state.json` and `.lf_account` **next to themselves** (inside
``), so they work from any cwd. The ad-hoc scripts
(`build_*.py`, `figma_rest.py`) read those from the current directory — `cd
the repo root` first.

## TWO MODES (verified live 2026-07-22)

- **App token** (`.env`, permanent): reads + funnel settings (name/slug/publish/
  header_scripts) + `duplicate`. **Cannot** write page bodies —
  `updateFunnel.steps`/`createStep` are blocked (`non_allowed_app_funnel_update`).
- **Session token** (`.session_token`, from the LF dashboard, temporary): NOT an
  app, so it **can** write real page bodies. Use `edit --session --account-id <id>`.
  Session tokens expire — re-grab from DevTools when calls start failing.

Therefore:
- **Create funnel with pages** → `duplicate` an existing funnel (full clone).
- **Edit page copy for real** → `edit --session` (persists in the LF editor).
- **Edit copy render-time only** → `edit` (app token, `header_scripts` patch).
- **Layout/image/section changes** → LF editor (session-mode body-JSON edits are
  possible but not yet wrapped in a command).

## Commands

```bash
python3 lf.py funnels                                  # list
python3 lf.py funnel <funnel_id>                       # detail + steps
python3 lf.py duplicate <funnel_id> --name N --slug S  # clone incl. pages
python3 lf.py texts <funnel_id> [step_uid]             # extract visible copy
python3 lf.py edit <funnel_id> --session --account-id <id> --replace "old==new"   # REAL edit
python3 lf.py edit <funnel_id> --replace "old==new"    # render-time patch (app token)
python3 lf.py patch <funnel_id>                        # show render-time patch
python3 lf.py patch-clear <funnel_id>                  # remove render-time patch
python3 lf.py publish <funnel_id> [--off]
python3 lf.py rename <funnel_id> --name N --slug S
python3 lf.py delete <funnel_id> --yes                 # IRREVERSIBLE
python3 lf.py create --name N --slug S                 # EMPTY shell only
python3 lf.py capture <funnel_id> <step_uid> <name> [--out DIR]   # archive body JSON
python3 lf.py gql --query '...' [--variables '{}']     # escape hatch
```

## HARD RULES

1. `texts` before `edit` — copy the exact string; `edit` fails loudly on
   no-match by design.
2. Confirm with the user before `publish` and `delete`. Duplicates inherit
   `published` from the source — unpublish fresh duplicates unless told
   otherwise.
3. Test body edits (`edit --session`) on a `duplicate` first, not a live funnel.
4. Both tokens are secret: never log or commit the app token OR the session
   token (`.session_token` = logged in as the user). Keep them local.
5. API reference: `docs/LIGHTFUNNELS_API.md` (incl. Field-Verified Addendum,
   which documents the app-token vs session-token difference).
