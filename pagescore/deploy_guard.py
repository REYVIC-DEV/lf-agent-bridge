#!/usr/bin/env python3
"""
deploy_guard.py -- refuse to overwrite a live page by accident.

On Lightfunnels the publish toggle IS the deploy mechanism. There is no staging,
so re-running a builder against an existing slug rewrites a page that is taking
paid traffic right now. An unsupervised run has already 503'd a live page here
once. This guard makes that failure mode impossible to reach silently.

Every builder calls `guard(funnel_id, slug)` before it writes. The rules:

  * slug does not exist yet          -> allowed, it is a new page
  * slug exists and is unpublished   -> allowed, nothing live is at risk
  * slug exists and IS published     -> BLOCKED unless the caller passes an
                                        explicit intent flag

Intent is expressed by the human, never inferred. Prefer the scoped form -- it
authorises ONE page, so a pipeline that is allowed to iterate on the page it just
built still cannot touch anything else:

  LF_ALLOW_REDEPLOY=smart-ring-v4 python3 pagescore/build_x.py    # that slug only
  LF_ALLOW_REDEPLOY=a-v2,b-v2     python3 pagescore/build_x.py    # a short list
  LF_ALLOW_REDEPLOY=1             python3 pagescore/build_x.py    # any slug (blunt)
  python3 pagescore/build_x.py --redeploy                          # same as =1, via argv

The scoped form is what a fix loop should use: the builder makes `page-v4`, QA finds
defects, and the fixer needs to redeploy `page-v4` repeatedly -- but must still be
unable to overwrite `page-v3` by a typo.

Usage inside a builder, right before the write:

    from deploy_guard import guard
    guard(FUNNEL, STEP_SLUG)      # raises SystemExit if the page is live

Check without building anything:

    python3 pagescore/deploy_guard.py <funnel_id> <slug>
"""
import json
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)

ALLOW_ENV = "LF_ALLOW_REDEPLOY"


def _funnel(funnel_id):
    """Read the funnel through the bridge. Read-only -- `lf.py funnel` is a query."""
    out = subprocess.run(
        [sys.executable, "lf.py", "funnel", funnel_id],
        cwd=ROOT, capture_output=True, text=True, timeout=90)
    if out.returncode != 0:
        raise RuntimeError(f"could not read funnel {funnel_id}: {out.stderr[-300:]}")
    return json.loads(out.stdout)


def status(funnel_id, slug):
    f = _funnel(funnel_id)
    steps = f.get("steps") or f.get("funnel", {}).get("steps", [])
    step = next((s for s in steps if s.get("slug") == slug), None)
    return {
        "funnel_id": funnel_id,
        "funnel_name": f.get("name"),
        "funnel_published": bool(f.get("published")),
        "slug": slug,
        "step_exists": step is not None,
        "step_id": (step or {}).get("id"),
        # A step is reachable by the public only if its funnel is published.
        "is_live": bool(f.get("published")) and step is not None,
    }


def allowed(slug, argv=None):
    """True only if the human authorised THIS page (or, bluntly, every page)."""
    argv = sys.argv if argv is None else argv
    if "--redeploy" in argv:
        return True
    val = (os.environ.get(ALLOW_ENV) or "").strip()
    if not val:
        return False
    if val == "1":
        return True
    return slug in {s.strip() for s in val.split(",") if s.strip()}


def guard(funnel_id, slug, argv=None):
    """Call before any write. Returns the status dict, or exits non-zero."""
    st = status(funnel_id, slug)
    if not st["step_exists"]:
        print(f"[guard] '{slug}' is new in {st['funnel_name']} -- safe to create.")
        return st
    if not st["is_live"]:
        print(f"[guard] '{slug}' exists but its funnel is unpublished -- safe to rebuild.")
        return st
    if allowed(slug, argv):
        print(f"[guard] '{slug}' is LIVE and redeploy was explicitly authorised. "
              f"Verify the page returns 200 immediately after this run.")
        return st
    sys.stderr.write(
        f"\n[guard] REFUSING TO WRITE.\n"
        f"  '{slug}' is a LIVE page in '{st['funnel_name']}' ({funnel_id}).\n"
        f"  Rebuilding it replaces what visitors are seeing right now, with no staging\n"
        f"  and no undo.\n\n"
        f"  If that is genuinely the intent, the human authorises this ONE page:\n"
        f"    {ALLOW_ENV}={slug} python3 {os.path.relpath(sys.argv[0], ROOT)}\n\n"
        f"  Otherwise build to a new slug instead.\n\n")
    raise SystemExit(2)


if __name__ == "__main__":
    if len(sys.argv) < 3:
        sys.exit(__doc__)
    print(json.dumps(status(sys.argv[1], sys.argv[2]), indent=2))
