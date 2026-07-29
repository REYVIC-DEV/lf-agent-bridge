#!/usr/bin/env python3
"""
lf.py — Lightfunnels agent CLI. The primary interface for agentic coders.

Every command prints JSON to stdout and exits non-zero with the error on
stderr. Token resolution: --token flag > LF_ACCESS_TOKEN env > .env file.

PLATFORM LIMITS (verified live): app tokens CANNOT write page bodies
(`non_allowed_app_funnel_update`). Funnel creation with content therefore
goes through `duplicate`, and copy editing through the header-scripts text
patch (`edit`). See .claude/skills/lightfunnels/SKILL.md.

Commands:
  funnels [--first N] [--query Q]        list funnels
  funnel <funnel_id>                     funnel detail + steps (no bodies)
  duplicate <funnel_id> [--name N] [--slug S]   clone a funnel incl. pages
  create --name N --slug S               create EMPTY funnel shell (no pages)
  texts <funnel_id> [step_uid]           extract visible copy from page bodies
  edit <funnel_id> --replace "old==new" [...]   patch copy via header_scripts
  patch <funnel_id>                      show current patch map
  patch-clear <funnel_id>                remove the copy patch
  capture <funnel_id> <step_uid> <name>  archive step body -> templates/
  publish <funnel_id> [--off]            publish / unpublish
  rename <funnel_id> [--name N] [--slug S]
  delete <funnel_id> --yes               delete funnel (irreversible)
  templates                              list captured templates
  gql --query Q [--variables JSON]       raw GraphQL escape hatch
"""
import argparse
import json
import os
import sys

import lf_api

HERE = os.path.dirname(os.path.abspath(__file__))
TEMPLATES_DIR = os.path.join(HERE, "templates")


def _token(args):
    tok = getattr(args, "token", None) or os.environ.get("LF_ACCESS_TOKEN")
    if not tok:
        env_path = os.path.join(HERE, ".env")
        if os.path.exists(env_path):
            for line in open(env_path):
                line = line.strip()
                if line.startswith("LF_ACCESS_TOKEN"):
                    tok = line.split("=", 1)[1].strip().strip('"').strip("'")
    if not tok:
        sys.exit("No token. Pass --token, set LF_ACCESS_TOKEN, or run get_token.py "
                 "(see SKILL.md 'Auth' section).")
    return tok


def _account(args):
    return (getattr(args, "account_id", None) or os.environ.get("LF_ACCOUNT_ID")
            or (open(os.path.join(HERE, ".lf_account")).read().strip()
                if os.path.exists(os.path.join(HERE, ".lf_account")) else None))


def _session(args):
    """Resolve the browser session token (+ dashboard headers) for real
    page-body edits. Returns (token, headers). If there's no token yet but a
    saved login exists, refresh automatically."""
    path = os.path.join(HERE, ".session_token")
    tok = open(path).read().strip() if os.path.exists(path) else ""
    if not tok:
        if os.path.exists(os.path.join(HERE, ".lf_state.json")):
            import lf_session
            tok, acct = lf_session.refresh_token()
        else:
            sys.exit("No session yet. Run one-time login:\n  python3 lf.py login\n"
                     "(or paste a token: echo 'TOKEN' > .session_token)")
    acct = _account(args)
    if not acct:
        sys.exit("Session mode needs an account id. It's saved by `login`; "
                 "or pass --account-id / set LF_ACCOUNT_ID.")
    return tok, lf_api.session_headers(acct)


def _session_retry(args, fn):
    """Run a session call; on an auth failure, refresh the token once (if a
    saved login exists) and retry. `fn(token, headers)` does the work."""
    tok, hdrs = _session(args)
    try:
        return fn(tok, hdrs)
    except RuntimeError as e:
        msg = str(e).lower()
        auth_ish = any(k in msg for k in ("forbidden", "unauthenticated",
                                          "unauthorized", "401", "expired", "token"))
        if not auth_ish or not os.path.exists(os.path.join(HERE, ".lf_state.json")):
            raise
        import lf_session
        tok, _ = lf_session.refresh_token()
        return fn(tok, hdrs)


def _out(obj):
    print(json.dumps(obj, indent=2))


# ---------------------------------------------------------------- commands
def cmd_funnels(args):
    tok = _token(args)
    q = args.query or "order_by:id order_dir:desc"
    data = lf_api.gql(tok, """
      query Funnels($first: Int, $q: String!) {
        funnels(first: $first, query: $q) {
          count
          edges { node { id uid _id name slug published created_at } }
        }
      }""", {"first": args.first, "q": q})["funnels"]
    _out({"count": data["count"],
          "funnels": [e["node"] for e in data["edges"]]})


def cmd_funnel(args):
    _out(lf_api.get_funnel_meta(_token(args), args.funnel_id))


def cmd_duplicate(args):
    tok = _token(args)
    dup = lf_api.duplicate_funnel(tok, args.funnel_id)
    if args.name or args.slug:
        node = {}
        if args.name:
            node["name"] = args.name
        if args.slug:
            node["slug"] = args.slug
        lf_api.update_funnel_fields(tok, dup["id"], node)
        dup.update(node)
    _out(dup)


def cmd_create(args):
    created = lf_api.create_funnel(
        _token(args), args.name, args.slug,
        [s.strip() for s in (args.steps or "").split(",") if s.strip()],
        currency=args.currency, lang=args.lang,
        style_id=args.style_id, product_id=args.product_id)
    created["note"] = ("Funnel shell created. App tokens cannot add pages via "
                       "the API — add pages in the LF editor, or use "
                       "`duplicate` on a funnel that already has pages.")
    _out(created)


def cmd_texts(args):
    tok = _token(args)
    funnel = lf_api.get_funnel_steps(tok, args.funnel_id)
    out = []
    for s in funnel["steps"]:
        if args.step_uid and s["uid"] != args.step_uid and s["id"] != args.step_uid:
            continue
        out.append({"step_uid": s["uid"], "title": s["title"], "type": s["type"],
                    "texts": lf_api.extract_texts(s.get("body"))})
    _out({"funnel_id": args.funnel_id, "steps": out})


def cmd_edit(args):
    pairs = []
    for r in args.replace or []:
        if "==" not in r:
            sys.exit(f'Bad --replace value {r!r}; format is "old text==new text"')
        old, new = r.split("==", 1)
        pairs.append([old, new])
    if args.file:
        pairs.extend([k, v] for k, v in json.load(open(args.file)).items())
    if not pairs:
        sys.exit("Nothing to do: pass --replace and/or --file")

    if args.session:
        # REAL edit: rewrite the actual page body (persists in the LF editor).
        # Auto-refreshes the session token if it expired mid-run.
        res = _session_retry(args, lambda tok, hdrs: lf_api.edit_step_bodies(
            tok, args.funnel_id, pairs, extra_headers=hdrs, force=args.force))
        res["mode"] = "session (real body edit — saved to the page)"
        _out(res)
        return

    # App-token fallback: render-time text patch via header_scripts.
    tok = _token(args)
    if not args.force:
        funnel = lf_api.get_funnel_steps(tok, args.funnel_id)
        corpus = "\n".join(lf_api.visible_corpus(s.get("body"))
                           for s in funnel["steps"])
        missing = [old for old, _ in pairs if old not in corpus]
        if missing:
            sys.exit("Not found in any page body: " + json.dumps(missing)
                     + "\nRun `texts` and copy the exact string, or pass --force.")

    current = lf_api.get_header_scripts(tok, args.funnel_id)
    merged = {old: new for old, new in lf_api.read_patch_map(current)}
    for old, new in pairs:
        merged[old] = new
    replacements = [[o, n] for o, n in merged.items()]
    new_hs = lf_api.render_patch(current, replacements)
    lf_api.update_funnel_fields(tok, args.funnel_id, {"header_scripts": new_hs})
    _out({"funnel_id": args.funnel_id, "mode": "app (render-time header_scripts patch)",
          "patch_size": len(replacements), "replacements": replacements,
          "note": "Copy is patched at render time. The LF editor still shows the "
                  "original text. For real edits use --session."})


def cmd_patch(args):
    hs = lf_api.get_header_scripts(_token(args), args.funnel_id)
    _out({"funnel_id": args.funnel_id, "replacements": lf_api.read_patch_map(hs)})


def cmd_patch_clear(args):
    tok = _token(args)
    hs = lf_api.get_header_scripts(tok, args.funnel_id)
    lf_api.update_funnel_fields(tok, args.funnel_id,
                                {"header_scripts": lf_api.render_patch(hs, [])})
    _out({"funnel_id": args.funnel_id, "patch_cleared": True})


def cmd_capture(args):
    step = lf_api.get_step_body(_token(args), args.funnel_id, args.step_uid)
    os.makedirs(TEMPLATES_DIR, exist_ok=True)
    path = os.path.join(TEMPLATES_DIR, f"{args.name}.json")
    with open(path, "w") as f:
        json.dump(step, f, indent=2)
    _out({"captured": step["uid"], "type": step["type"], "saved_to": path})


def cmd_publish(args):
    _out(lf_api.publish_funnel(_token(args), args.funnel_id, not args.off))


def cmd_rename(args):
    node = {}
    if args.name:
        node["name"] = args.name
    if args.slug:
        node["slug"] = args.slug
    if not node:
        sys.exit("Pass --name and/or --slug")
    _out(lf_api.update_funnel_fields(_token(args), args.funnel_id, node))


def cmd_delete(args):
    if not args.yes:
        sys.exit("Refusing to delete without --yes (irreversible).")
    _out({"deleted": lf_api.delete_funnels(_token(args), [args.funnel_id])})


def cmd_templates(args):
    files = sorted(f[:-5] for f in os.listdir(TEMPLATES_DIR)
                   if f.endswith(".json")) if os.path.isdir(TEMPLATES_DIR) else []
    _out({"templates": files})


def cmd_gql(args):
    variables = json.loads(args.variables) if args.variables else {}
    _out(lf_api.gql(_token(args), args.query, variables))


def cmd_login(args):
    import lf_session
    lf_session.login()


def cmd_refresh(args):
    import lf_session
    tok, acct = lf_session.refresh_token()
    _out({"refreshed": True, "account": acct, "token_written": ".session_token"})


# ---------------------------------------------------------------- wiring
def main():
    ap = argparse.ArgumentParser(prog="lf.py", description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--token", help="LF access token (else env/.env)")
    sub = ap.add_subparsers(dest="cmd", required=True)

    p = sub.add_parser("funnels");  p.set_defaults(fn=cmd_funnels)
    p.add_argument("--first", type=int, default=20)
    p.add_argument("--query", help='e.g. "published:true order_by:id"')

    p = sub.add_parser("funnel");   p.set_defaults(fn=cmd_funnel)
    p.add_argument("funnel_id")

    p = sub.add_parser("duplicate"); p.set_defaults(fn=cmd_duplicate)
    p.add_argument("funnel_id"); p.add_argument("--name"); p.add_argument("--slug")

    p = sub.add_parser("create");   p.set_defaults(fn=cmd_create)
    p.add_argument("--name", required=True)
    p.add_argument("--slug", required=True)
    p.add_argument("--steps", default="blank_page",
                   help="StepType list hint (pages are NOT created — see note)")
    p.add_argument("--currency", default="USD")
    p.add_argument("--lang", default="en")
    p.add_argument("--style-id", dest="style_id")
    p.add_argument("--product-id", dest="product_id")

    p = sub.add_parser("texts");    p.set_defaults(fn=cmd_texts)
    p.add_argument("funnel_id"); p.add_argument("step_uid", nargs="?")

    p = sub.add_parser("edit");     p.set_defaults(fn=cmd_edit)
    p.add_argument("funnel_id")
    p.add_argument("--replace", action="append",
                   help='"exact old text==new text" (repeatable)')
    p.add_argument("--file", help='JSON file of {"old": "new", ...}')
    p.add_argument("--force", action="store_true",
                   help="skip validation against page bodies")
    p.add_argument("--session", action="store_true",
                   help="REAL body edit via browser session token (.session_token). "
                        "Persists to the page. Without this, uses the render-time patch.")
    p.add_argument("--account-id", dest="account_id",
                   help="account-id header for --session (or set LF_ACCOUNT_ID)")

    p = sub.add_parser("patch");    p.set_defaults(fn=cmd_patch)
    p.add_argument("funnel_id")

    p = sub.add_parser("patch-clear"); p.set_defaults(fn=cmd_patch_clear)
    p.add_argument("funnel_id")

    p = sub.add_parser("capture");  p.set_defaults(fn=cmd_capture)
    p.add_argument("funnel_id"); p.add_argument("step_uid"); p.add_argument("name")

    p = sub.add_parser("publish");  p.set_defaults(fn=cmd_publish)
    p.add_argument("funnel_id"); p.add_argument("--off", action="store_true")

    p = sub.add_parser("rename");   p.set_defaults(fn=cmd_rename)
    p.add_argument("funnel_id"); p.add_argument("--name"); p.add_argument("--slug")

    p = sub.add_parser("delete");   p.set_defaults(fn=cmd_delete)
    p.add_argument("funnel_id"); p.add_argument("--yes", action="store_true")

    p = sub.add_parser("templates"); p.set_defaults(fn=cmd_templates)

    p = sub.add_parser("gql");      p.set_defaults(fn=cmd_gql)
    p.add_argument("--query", required=True); p.add_argument("--variables")

    p = sub.add_parser("login");    p.set_defaults(fn=cmd_login)   # one-time browser login
    p = sub.add_parser("refresh");  p.set_defaults(fn=cmd_refresh) # headless token refresh

    args = ap.parse_args()
    try:
        args.fn(args)
    except RuntimeError as e:
        sys.exit(f"ERROR: {e}")


if __name__ == "__main__":
    main()
