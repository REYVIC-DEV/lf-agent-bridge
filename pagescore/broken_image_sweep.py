#!/usr/bin/env python3
"""
broken_image_sweep.py — find every image on every funnel whose asset no longer
resolves, and optionally repoint the affected blocks at a replacement.

Why this exists: an asset deleted from LF storage leaves the block in place and
the page still renders 200. Nothing in the page body changes, no console error
is raised server-side, and the only symptom is a broken-image glyph inside a
correctly-sized box. It is invisible to every check that is not "fetch the image
and look at the status code".

TWO FIELDS, and missing the second is the trap:

    p.src          the media-library reference (with p.src_id / p.src_uid)
    p.externalSrc  a raw URL, used when the image was not picked from the library

A block sourced externally has **src = null**, which looks like damage and is
not. The TechUnboxed header logo is one of these, so a sweep that only walks
p.src reports the logo as broken when it is fine, and misses it when it is not.

Both are collected here, and the fix writes back to whichever field the block
actually uses.

Usage
-----
    python3 pagescore/broken_image_sweep.py scan
    python3 pagescore/broken_image_sweep.py scan --json out.json
    python3 pagescore/broken_image_sweep.py apply --from <dead-url> --to <new-url>
    python3 pagescore/broken_image_sweep.py apply --from <dead-url> --to <new-url> --dry-run

`apply` writes only the steps that actually contain the dead URL, and sends only
those steps in updateFunnel — siblings survive by omission. Funnel-level fields
(name, slug, published, starting_step_id) are never sent and are asserted
unchanged afterwards.
"""
import argparse
import json
import os
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from collections import defaultdict

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, ROOT)
import lf_api  # noqa: E402

# ⚠ Never harvest asset urls with a bare regex over serialized JSON. LF keeps the
# ORIGINAL upload filename, so a large share of these contain spaces and
# parentheses ("Rectangle 40(2).png"); a \S+ pattern truncates at the space and
# the fragment 404s. A first pass reported 153 dead images of which 121 were
# this artifact. Urls are read structurally from the block instead, and from
# custom_html only through quote-delimited attributes, which cannot truncate.
ATTR_RE = re.compile(
    r"""(?:src|href|content)\s*=\s*["'](https://assets\.lightfunnels\.com/[^"']+)["']"""
    r"""|url\(\s*["']?(https://assets\.lightfunnels\.com/[^"')]+)["']?\s*\)""",
    re.I)
CDN_RE = re.compile(r"^https://assets\.lightfunnels\.com/cdn-cgi/image/[^/]+/(https?://.+)$")


def urls_in_html(html):
    """Asset urls from real HTML, taken from quoted attributes only."""
    for m in ATTR_RE.finditer(html or ""):
        u = m.group(1) or m.group(2)
        if u:
            yield u.strip()


# ----------------------------------------------------------------- auth
def creds():
    tok_f = os.path.join(ROOT, ".session_token")
    acct_f = os.path.join(ROOT, ".lf_account")
    if not os.path.exists(tok_f):
        sys.exit("No .session_token. Run: python3 lf.py login")
    tok = open(tok_f).read().strip()
    acct = open(acct_f).read().strip() if os.path.exists(acct_f) else None
    return tok, lf_api.session_headers(acct)


def go(fn, tries=5):
    """Retry the 502s Cloudflare throws in front of the LF API."""
    for _ in range(tries):
        try:
            return fn()
        except Exception as e:
            msg = str(e)
            if "expired" in msg.lower():
                sys.exit("Session expired. Run: python3 lf.py login")
            if "502" in msg or "Bad Gateway" in msg:
                print("    502, backing off 70s", flush=True)
                time.sleep(70)
                continue
            raise
    raise RuntimeError("gave up after repeated 502s")


# ----------------------------------------------------------------- probing
def probe(url, timeout=40):
    parts = urllib.parse.urlsplit(url)
    safe = urllib.parse.urlunsplit((
        parts.scheme, parts.netloc,
        urllib.parse.quote(parts.path, safe="/%:"),
        urllib.parse.quote(parts.query, safe="=&%"), parts.fragment))
    req = urllib.request.Request(safe, headers={"User-Agent": "Mozilla/5.0"})
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            return r.status, r.headers.get("content-type", ""), len(r.read(2048))
    except urllib.error.HTTPError as e:
        return e.code, str(e.reason)[:40], 0
    except Exception as e:
        return 0, str(e)[:60], 0


# ----------------------------------------------------------------- walking
def collect(body, sink, funnel, step):
    """Record every image URL in this body, tagged with the field it came from."""
    def add(url, field, block_id):
        if url and isinstance(url, str):
            sink[url.strip()].append({
                "funnel": funnel["name"], "funnel_uid": funnel["uid"],
                "step": step.get("slug"), "step_uid": step.get("uid"),
                "step_title": step.get("title"), "field": field,
                "block": str(block_id or "")[:8],
            })

    def walk(n):
        if isinstance(n, dict):
            if n.get("t") == "Image":
                p = n.get("p") or {}
                add(p.get("src"), "p.src", n.get("id"))
                add(p.get("externalSrc"), "p.externalSrc", n.get("id"))
            for v in n.values():
                walk(v)
        elif isinstance(n, list):
            for v in n:
                walk(v)

    walk(body)

    # HtmlElement / rich-text content is real HTML, so quoted attributes are
    # safe to read. Walk the nodes rather than the serialized JSON: json.dumps
    # escapes the quotes, and the attribute pattern would not match.
    def walk_html(n):
        if isinstance(n, dict):
            c = (n.get("p") or {}).get("content")
            if isinstance(c, str) and "assets.lightfunnels.com" in c:
                for u in urls_in_html(c):
                    add(u, "html content", n.get("id"))
            for v in n.values():
                walk_html(v)
        elif isinstance(n, list):
            for v in n:
                walk_html(v)

    walk_html(body)


def load_all(tok, h):
    q = """query($first:Int){funnels(first:$first, query:"order_by:id order_dir:desc"){
      count edges{node{id uid name slug published}}}}"""
    fl = go(lambda: lf_api.gql(tok, q, {"first": 200}, extra_headers=h))["funnels"]
    funnels = [e["node"] for e in fl["edges"]]
    print("funnels: %d" % len(funnels))
    sink = defaultdict(list)
    bodies = {}
    for f in funnels:
        try:
            node = go(lambda f=f: lf_api.get_funnel_steps(tok, f["uid"], extra_headers=h))
        except Exception as e:
            print("  !! %-40s %s" % (f["name"][:40], str(e)[:60]))
            continue
        steps = node.get("steps") or []
        bodies[f["uid"]] = (f, steps)
        for st in steps:
            if st.get("body") is not None:
                collect(st["body"], sink, f, st)
            stt = st.get("settings") or {}
            for key in ("header", "footer"):
                html = (stt.get("custom_html") or {}).get(key) or ""
                for u in urls_in_html(html):
                    sink[u].append({
                        "funnel": f["name"], "funnel_uid": f["uid"],
                        "step": st.get("slug"), "step_uid": st.get("uid"),
                        "step_title": st.get("title"),
                        "field": "settings.custom_html.%s" % key, "block": "",
                    })
        print("  %-46s %2d steps" % (f["name"][:46], len(steps)))
    return funnels, bodies, sink


# ----------------------------------------------------------------- scan
def cmd_scan(args):
    tok, h = creds()
    funnels, bodies, sink = load_all(tok, h)
    print("\ndistinct image urls: %d\nprobing...\n" % len(sink))

    rows = []
    for i, url in enumerate(sorted(sink), 1):
        st, ct, n = probe(url)
        origin = origin_st = None
        m = CDN_RE.match(url)
        if m:
            origin = m.group(1)
            origin_st = probe(origin)[0]
        ok = 200 <= st < 300
        rows.append({"url": url, "status": st, "ctype": ct, "origin": origin,
                     "origin_status": origin_st, "uses": sink[url]})
        if not ok:
            print("  DEAD %-4s %s" % (st, url[:100]))

    dead = [r for r in rows if not (200 <= r["status"] < 300)]
    print("\n%s" % ("=" * 72))
    print("DEAD IMAGES: %d of %d distinct urls" % (len(dead), len(rows)))
    print("=" * 72)
    for r in dead:
        print("\n%s" % r["url"])
        print("  status %s%s" % (r["status"],
              "  (origin %s)" % r["origin_status"] if r["origin"] else ""))
        by_funnel = defaultdict(list)
        for u in r["uses"]:
            by_funnel[u["funnel"]].append(u)
        for fname, us in sorted(by_funnel.items()):
            steps = sorted({(u["step"], u["step_title"]) for u in us})
            print("  %s — %d block(s) on %d step(s):" % (fname, len(us), len(steps)))
            for slug, title in steps:
                fields = sorted({u["field"] for u in us if u["step"] == slug})
                print("      %-28s %-34s %s" % (slug, (title or "")[:34], ",".join(fields)))

    if args.json:
        with open(args.json, "w", encoding="utf-8") as fh:
            json.dump(rows, fh, indent=2, ensure_ascii=False)
        print("\nwritten: %s" % args.json)
    return 0 if not dead else 1


# ----------------------------------------------------------------- apply
def swap_in_body(body, old, new):
    """Replace old->new in p.src / p.externalSrc / html. Returns (body, count)."""
    n = [0]

    def walk(x):
        if isinstance(x, dict):
            if x.get("t") == "Image":
                p = x.get("p") or {}
                for field in ("src", "externalSrc"):
                    v = p.get(field)
                    if isinstance(v, str) and old in v:
                        p[field] = v.replace(old, new)
                        n[0] += 1
                        # the library ids describe the OLD asset; an external url
                        # does not use them, so clear them rather than leave a
                        # reference that no longer matches what renders.
                        if field == "externalSrc":
                            for k in ("src_id", "src_uid"):
                                if p.get(k) is not None:
                                    p[k] = None
            p = x.get("p") or {}
            c = p.get("content")
            if isinstance(c, str) and old in c:
                p["content"] = c.replace(old, new)
                n[0] += 1
            for v in x.values():
                walk(v)
        elif isinstance(x, list):
            for v in x:
                walk(v)

    walk(body)
    return body, n[0]


def cmd_apply(args):
    old, new = args.from_url, args.to_url
    st, ct, _ = probe(new)
    if not (200 <= st < 300):
        sys.exit("Replacement url is not reachable (%s %s) — refusing." % (st, ct))
    print("replacement OK: %s %s\n" % (st, ct))

    tok, h = creds()
    funnels, bodies, sink = load_all(tok, h)

    targets = [u for u in sink.get(old, [])]
    if not targets:
        # the dead url may appear only as a substring (e.g. wrapped by a cdn-cgi
        # transform), so fall back to a substring match across collected urls
        targets = [u for url, us in sink.items() if old in url for u in us]
    if not targets:
        sys.exit("No block references %r — nothing to do." % old)

    steps = sorted({(t["funnel_uid"], t["step_uid"]) for t in targets})
    print("%d block reference(s) across %d step(s)\n" % (len(targets), len(steps)))

    changed = 0
    for fuid, suid in steps:
        f, all_steps = bodies[fuid]
        s = {x["uid"]: x for x in all_steps}[suid]
        body = s.get("body")
        settings = s.get("settings") or {}

        body2, nb = (swap_in_body(body, old, new) if body is not None else (body, 0))
        nh = 0
        ch = settings.get("custom_html") or {}
        for key in ("header", "footer"):
            html = ch.get(key)
            if isinstance(html, str) and old in html:
                ch[key] = html.replace(old, new)
                nh += 1
        if not (nb or nh):
            continue

        print("  %-34s %-24s body=%d custom_html=%d" % (
            f["name"][:34], (s.get("slug") or "")[:24], nb, nh))
        if args.dry_run:
            changed += 1
            continue

        q = """query($id:ID!){node(id:$id){... on Funnel{
          name slug published starting_step_id steps{uid}}}}"""
        pre = go(lambda: lf_api.gql(tok, q, {"id": fuid}, extra_headers=h))["node"]
        inv = {k: pre.get(k) for k in ("name", "slug", "published", "starting_step_id")}

        go(lambda: lf_api.gql(
            tok, "mutation($id:ID!,$node:InputFunnel!){updateFunnel(id:$id,node:$node){id}}",
            {"id": fuid, "node": {"steps": [{
                "id": suid, "slug": s["slug"], "title": s["title"], "type": s["type"],
                "settings": settings, "visual": s.get("visual"), "body": body2,
            }]}}, extra_headers=h))

        post = go(lambda: lf_api.gql(tok, q, {"id": fuid}, extra_headers=h))["node"]
        for k, v in inv.items():
            assert post.get(k) == v, "%s changed on %s: %r -> %r" % (k, fuid, v, post.get(k))
        assert len(post["steps"]) == len(pre["steps"]), "step count changed on %s" % fuid
        changed += 1

    print("\n%s %d step(s)" % ("would update" if args.dry_run else "updated", changed))
    if not args.dry_run:
        st2, _, _ = probe(new)
        print("replacement still resolving: %s" % st2)
    return 0


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)

    p = sub.add_parser("scan", help="probe every image on every funnel")
    p.add_argument("--json", help="write full results here")
    p.set_defaults(fn=cmd_scan)

    p = sub.add_parser("apply", help="repoint blocks from a dead url to a new one")
    p.add_argument("--from", dest="from_url", required=True)
    p.add_argument("--to", dest="to_url", required=True)
    p.add_argument("--dry-run", action="store_true")
    p.set_defaults(fn=cmd_apply)

    args = ap.parse_args()
    sys.exit(args.fn(args))


if __name__ == "__main__":
    main()
