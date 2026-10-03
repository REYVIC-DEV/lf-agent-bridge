#!/usr/bin/env python3
"""Audit every published funnel's tracker against the two local reference copies.

THE TRACKER LIVES AT FUNNEL LEVEL, in `header_scripts` - the general header that
applies to every step. It is never installed per step. So this is one read per
funnel, and a funnel whose `header_scripts` has no `posthog.init` has no
analytics at all: the pages render, QA passes, and the experiment on them
collects nothing.

THERE ARE TWO SCRIPTS AND THEY ARE NOT INTERCHANGEABLE:

  snippets/tracker-header-meta-block.html    22,721  sha 2bcc3e350d  Meta / Native / rest
  snippets/tracker-header-google-block.html  26,748  sha 5d0bab814f  Google

They differ on 679 lines ignoring whitespace. The Google one is HARDCODED to
PostHog project 208779 (HTLH - GOOGLE); the Meta one SELF-SELECTS from the
detected traffic source, so `google` still reaches 208779 and everything else
lands in 194985 (HLTH - Native). They also wire the network pixels differently
(Taboola 14/13 refs against 5/4) and load Lenis differently.

⚠️ NEVER APPEND BLIND. Two `posthog.init` calls on one page duplicate every
event, which is worse than no tracking because it looks fine. Known offenders as
of 2026-10-04:
  - LISTICLES [ON DEV]              an older posthog-only block, funnel level
  - TUB - Top 5 h trackers-v3       two STEPS carry a stray per-step posthog
                                    (p8m5WBu3C, updated-3) - strip those first

Refresh the local copies from the live reference funnels with:
    python pagescore/check_tracker_headers.py --pull
"""
import hashlib
import io
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, ".."))
sys.path.insert(0, ROOT)
os.chdir(ROOT)
import lf_api  # noqa: E402

# (local file, reference funnel, expected sha1 prefix, label)
REFS = [
    ("snippets/tracker-header-meta-block.html",   "fun_vGqQYxn4H2i_traYYkh4w", "2bcc3e350d", "META"),
    ("snippets/tracker-header-google-block.html", "fun_p9Y_FwGlQsaP5bpW70q5N", "5d0bab814f", "GOOGLE"),
]

LIST = '{funnels(first:100,query:""){edges{node{id name slug published}}}}'
Q = "query($id:ID!){node(id:$id){... on Funnel{name header_scripts}}}"


def sha(s):
    return hashlib.sha1(s.encode("utf-8")).hexdigest()[:10]


def read_local(fn):
    # newline='' so the bytes are compared exactly as stored, with no translation
    return io.open(os.path.join(ROOT, fn), encoding="utf-8", newline="").read()


def main():
    tok = open(".session_token").read().strip()
    acct = open(".lf_account").read().strip()
    h = lf_api.session_headers(acct)

    if "--pull" in sys.argv:
        for fn, fid, expect, label in REFS:
            hs = lf_api.gql(tok, Q, {"id": fid}, extra_headers=h)["node"]["header_scripts"] or ""
            got = sha(hs)
            if got != expect:
                print("WARNING %s: reference drifted %s -> %s" % (label, expect, got))
            with io.open(os.path.join(ROOT, fn), "w", encoding="utf-8", newline="") as f:
                f.write(hs)
            print("pulled %-34s %6d chars sha=%s" % (fn, len(hs), got))
        return 0

    known = {}
    for fn, fid, expect, label in REFS:
        body = read_local(fn)
        got = sha(body)
        if got != expect:
            print("WARNING %s: local copy is %s, expected %s" % (fn, got, expect))
        known[got] = label
        print("reference %-7s %-34s %6d chars sha=%s" % (label, fn, len(body), got))
    print()

    problems = []
    rows = []
    for e in lf_api.gql(tok, LIST, {}, extra_headers=h)["funnels"]["edges"]:
        n = e["node"]
        if not n["published"]:
            continue
        hs = lf_api.gql(tok, Q, {"id": n["id"]}, extra_headers=h)["node"].get("header_scripts") or ""
        s = sha(hs)
        inits = hs.count("posthog.init")
        meta_body = read_local(REFS[0][0])
        goog_body = read_local(REFS[1][0])
        if s in known:
            kind = known[s]
        elif meta_body.strip() and meta_body.strip() in hs:
            # the reference plus something that was already there (e.g. an Aimerce
            # tag that was appended to rather than overwritten). Not a problem.
            kind = "META+extra"
        elif goog_body.strip() and goog_body.strip() in hs:
            kind = "GOOGLE+extra"
        elif not hs.strip():
            kind = "NONE"
        elif "GOOGLE FUNNELS" in hs:
            kind = "google-variant"
        elif inits:
            kind = "other-tracked"
        else:
            kind = "untracked-code"
        rows.append((kind, n["name"], n["slug"], len(hs), s, inits))

        archive = re.search(r"ARCHIVE", n["name"], re.I)
        if kind == "NONE" and not archive:
            problems.append("%s has NO tracker at all" % n["name"])
        elif kind == "untracked-code" and not archive:
            problems.append("%s has header code but no posthog.init" % n["name"])
        elif kind not in ("META", "GOOGLE", "META+extra", "GOOGLE+extra")                 and kind != "NONE" and not archive:
            problems.append("%s carries a non-reference tracker (sha %s) - compare before "
                            "appending, or it will double-init" % (n["name"], s))

    rows.sort(key=lambda r: (r[0], r[1]))
    print("%-15s %-42s %-26s %7s %-11s %s" % ("tracker", "funnel", "slug", "chars", "sha", "init"))
    for kind, name, slug, ln, s, inits in rows:
        print("%-15s %-42s %-26s %7d %-11s %d" % (kind, name[:42], slug[:26], ln, s, inits))

    print("\n%d published funnel(s); %d on the META reference, %d on GOOGLE" % (
        len(rows),
        sum(1 for r in rows if r[0] == "META"),
        sum(1 for r in rows if r[0] == "GOOGLE")))
    if problems:
        print("\n%d thing(s) to look at:" % len(problems))
        for p in problems:
            print("   -", p)
    else:
        print("\nNothing to look at.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
