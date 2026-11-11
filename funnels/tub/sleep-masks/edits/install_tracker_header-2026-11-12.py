#!/usr/bin/env python3
"""Install the mandatory GTM+PostHog+Lenis tracker header on the sleep-mask funnel.

`py pagescore/check_tracker_headers.py` found `TUB - Sleep mask comparison - Meta`
(fun_lqsXwH8BnCdqs44RJzEEf, slug `sleep-masks`) carrying NONE -- 0 chars in
funnel-level `header_scripts`, sha da39a3ee5e (the empty-string hash). That
means both live pages (best-sleep-masks-side-sleepers / -v2) have shipped with
zero analytics and no Lenis smooth scroll since the funnel was created -- the
standing rule in .claude/rules/lf-advertorial-pages.md section 3 was missed
when this funnel was set up.

This funnel is Meta channel ("- Meta" in its own name, Meta ad traffic per
NOTES), so it gets the Meta/Native reference block, not the Google one -- see
.claude/skills/lightfunnels/SKILL.md and pagescore/check_tracker_headers.py's
own docstring for why the two are not interchangeable.

The tracker lives at FUNNEL level only (never per step), so this is one write,
not one per page -- both A/B steps pick it up for free.

    py funnels/tub/sleep-masks/edits/install_tracker_header-2026-11-12.py              # dry run
    py funnels/tub/sleep-masks/edits/install_tracker_header-2026-11-12.py --apply
"""
import argparse
import hashlib
import io
import os
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", "..", "..", ".."))
sys.path.insert(0, ROOT)
os.chdir(ROOT)
import lf_api  # noqa: E402

FUNNEL = "fun_lqsXwH8BnCdqs44RJzEEf"   # TUB - Sleep mask comparison - Meta, slug sleep-masks
REFERENCE = "snippets/tracker-header-meta-block.html"
REFERENCE_SHA = "2bcc3e350d"

Q = 'query($id:ID!){node(id:$id){... on Funnel{id name slug published header_scripts}}}'
M = 'mutation($id:ID!,$node:InputFunnel!){updateFunnel(id:$id,node:$node){id header_scripts}}'


def sha(s):
    return hashlib.sha1(s.encode("utf-8")).hexdigest()[:10]


def read_local(fn):
    # newline='' so the bytes are compared exactly as stored, with no translation
    return io.open(os.path.join(ROOT, fn), encoding="utf-8", newline="").read()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true", help="write; otherwise dry run")
    a = ap.parse_args()

    tok = open(".session_token").read().strip()
    acct = open(".lf_account").read().strip()
    h = lf_api.session_headers(acct)

    block = read_local(REFERENCE)
    block_sha = sha(block)
    if block_sha != REFERENCE_SHA:
        sys.exit("local reference drifted (%s, expected %s) -- run "
                  "pagescore/check_tracker_headers.py --pull first" % (block_sha, REFERENCE_SHA))

    n = lf_api.gql(tok, Q, {"id": FUNNEL}, extra_headers=h)["node"]
    cur = n.get("header_scripts") or ""
    if "posthog.init" in cur:
        sys.exit("funnel already carries a tracker (posthog.init present, %d chars) -- "
                  "this is not the empty case this script was written for. Stop and "
                  "compare before overwriting." % len(cur))
    if cur.strip():
        sys.exit("header_scripts is non-empty (%d chars) but has no posthog.init -- "
                  "read it first, do not blindly overwrite." % len(cur))

    print("PLAN  %-36s header_scripts: %d chars -> %d chars (sha %s)"
          % (n["name"][:36], len(cur), len(block), block_sha))
    if not a.apply:
        print("dry run -- pass --apply to write")
        return

    lf_api.gql(tok, M, {"id": FUNNEL, "node": {"header_scripts": block}}, extra_headers=h)
    time.sleep(2.5)
    after = lf_api.gql(tok, Q, {"id": FUNNEL}, extra_headers=h)["node"].get("header_scripts") or ""
    after_sha = sha(after)
    ok = "OK " if after_sha == REFERENCE_SHA else "BAD"
    print("%s  stored %d chars, sha %s" % (ok, len(after), after_sha))
    if ok == "BAD":
        sys.exit(1)
    print("\nVerify on the live pages (not just storage):")
    print("  https://www.techunboxed.co/sleep-masks/best-sleep-masks-side-sleepers")
    print("  https://www.techunboxed.co/sleep-masks/best-sleep-masks-side-sleepers-v2")
    print("  grep for googletagmanager + posthog.init in the served HTML, and in a "
          "browser confirm document.documentElement.classList.contains('lenis').")


if __name__ == "__main__":
    main()
