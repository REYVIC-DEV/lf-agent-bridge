#!/usr/bin/env python3
"""Fetch one step's body ONCE and cache it on disk.

The LF API has no single-step query - `node(id: <step id>)` resolves to null -
so reading one page means pulling all 13 step bodies in the funnel, roughly
15-20 MB, which takes ten minutes. Paying that on every debugging iteration is
why this file exists. Fetch once, then analyse locally as many times as needed.

    python cache-step-body.py                 # fetch + cache
    python cache-step-body.py --check         # report the cache, no network

The cache is a debugging artifact, not a backup: it is the page as it was at
fetch time, so re-fetch before any write that depends on it being current.
"""
import io
import json
import os
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", "..", "..", ".."))
sys.path.insert(0, ROOT)
os.chdir(ROOT)

FUNNEL = "fun_p9Y_FwGlQsaP5bpW70q5N"
CACHE = os.path.join(HERE, "..", "steps", "_cache-google-uk-steps.json")


def cache_path():
    return os.path.abspath(CACHE)


def load():
    """Return {slug: step} from the cache, or None."""
    p = cache_path()
    if not os.path.exists(p):
        return None
    with io.open(p, encoding="utf-8") as fh:
        d = json.load(fh)
    return d


def main():
    if "--check" in sys.argv:
        d = load()
        if not d:
            sys.exit("no cache at %s" % cache_path())
        print("cached %s (%d steps), fetched %s" % (
            os.path.relpath(cache_path(), ROOT), len(d["steps"]), d["fetched_at"]))
        for s in d["steps"]:
            print("  %-28s %-24s body %d bytes" % (
                s["slug"], s["uid"], len(json.dumps(s.get("body")))))
        return

    sys.path.insert(0, ROOT)
    import lf_api  # noqa: E402
    tok = open(".session_token").read().strip()
    acct = open(".lf_account").read().strip()
    h = lf_api.session_headers(acct)

    t = time.time()
    print("fetching all step bodies (expect several minutes)...", flush=True)
    node = lf_api.get_funnel_steps(tok, FUNNEL, extra_headers=h)
    print("fetched in %.0fs" % (time.time() - t))

    out = {"funnel": FUNNEL,
           "fetched_at": time.strftime("%Y-%m-%dT%H:%M:%S"),
           "steps": node["steps"]}
    os.makedirs(os.path.dirname(cache_path()), exist_ok=True)
    with io.open(cache_path(), "w", encoding="utf-8") as fh:
        json.dump(out, fh, ensure_ascii=False)
    print("cached %d steps -> %s (%.1f MB)" % (
        len(node["steps"]), os.path.relpath(cache_path(), ROOT),
        os.path.getsize(cache_path()) / 1e6))


if __name__ == "__main__":
    main()
