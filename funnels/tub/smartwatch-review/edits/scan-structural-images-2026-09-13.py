#!/usr/bin/env python3
"""Probe every image URL taken STRUCTURALLY from captured bodies.

The regex pass was unusable: LF keeps the original upload filename, so a third
of these urls contain spaces or parentheses ("Rectangle 40(2).png") and the
pattern truncated them into 404s. 121 false positives out of 153.

Reading p.src / p.externalSrc off the block instead gives the complete string
every time, which is the only way to tell a genuinely deleted asset from a
badly-parsed url.
"""
import json
import os
import re
import urllib.error
import urllib.parse
import urllib.request
from collections import defaultdict

SKIP = {".git", "node_modules", "__pycache__", ".playwright-mcp", ".venv", "venv", "webforge"}
SCRATCH = os.environ.get("SCRATCH", ".")

# url -> list of context dicts
uses = defaultdict(list)


def near(node, limit=2):
    out = []

    def w(x, dep=0):
        if dep > 4 or len(out) >= limit:
            return
        if isinstance(x, dict):
            c = (x.get("p") or {}).get("content")
            if isinstance(c, str):
                t = re.sub(r"<[^>]+>", "", c).strip()
                if t:
                    out.append(t[:30])
            for v in x.values():
                w(v, dep + 1)
        elif isinstance(x, list):
            for v in x:
                w(v, dep + 1)

    w(node)
    return " | ".join(out)


def walk(n, f, parent):
    if isinstance(n, dict):
        if n.get("t") == "Image":
            p = n.get("p") or {}
            dims = {}
            for s in (n.get("styles") or []):
                if s.get("prop") in ("width", "height", "maxWidth") and not s.get("media"):
                    dims[s["prop"]] = s.get("value")
            for field in ("src", "externalSrc"):
                v = p.get(field)
                if isinstance(v, str) and v.strip():
                    uses[v.strip()].append({
                        "file": f, "block": str(n.get("id", ""))[:8], "field": field,
                        "alt": p.get("alt") or "",
                        "dims": "%s x %s" % (dims.get("width", "?"), dims.get("height", "?")),
                        "near": near(parent) if parent is not None else "",
                    })
        nxt = n if n.get("t") else parent
        for v in n.values():
            walk(v, f, nxt)
    elif isinstance(n, list):
        for v in n:
            walk(v, f, parent)


files = []
for root, dirs, fns in os.walk("."):
    dirs[:] = [d for d in dirs if d not in SKIP]
    for fn in fns:
        if fn.endswith(".json"):
            files.append(os.path.join(root, fn))

for p in sorted(files):
    try:
        if os.path.getsize(p) < 500:
            continue
        d = json.load(open(p, encoding="utf-8"))
    except Exception:
        continue
    body = d.get("body", d) if isinstance(d, dict) else d
    if isinstance(body, str):
        try:
            body = json.loads(body)
        except Exception:
            continue
    walk(body, p.replace("\\", "/"), None)

print("distinct image urls (structural): %d" % len(uses))


def probe(url):
    parts = urllib.parse.urlsplit(url)
    u = urllib.parse.urlunsplit((
        parts.scheme, parts.netloc,
        urllib.parse.quote(parts.path, safe="/%:"),
        urllib.parse.quote(parts.query, safe="=&%"), parts.fragment))
    req = urllib.request.Request(u, headers={"User-Agent": "Mozilla/5.0"})
    try:
        with urllib.request.urlopen(req, timeout=35) as r:
            return r.status, r.headers.get("content-type", "")
    except urllib.error.HTTPError as e:
        return e.code, str(e.reason)[:30]
    except Exception as e:
        return 0, str(e)[:40]


rows = []
for i, url in enumerate(sorted(uses), 1):
    st, ct = probe(url)
    rows.append((st, ct, url))
    if not (200 <= st < 300):
        print("  DEAD %-4s %s" % (st, url[:110]))

dead = [r for r in rows if not (200 <= r[0] < 300)]
print("\n=== %d DEAD of %d ===" % (len(dead), len(rows)))
for st, ct, url in dead:
    print("\n%s  (%s)" % (url, st))
    ctx = uses[url]
    print("  %d block(s):" % len(ctx))
    seen = set()
    for c in ctx:
        key = (c["block"], c["file"])
        if key in seen:
            continue
        seen.add(key)
        print("    %-8s %-14s %-13s alt=%-18s near=%-24s %s" % (
            c["block"], c["field"], c["dims"], (c["alt"] or "")[:18],
            c["near"][:24], c["file"].split("/")[-1][:40]))

out = os.path.join(SCRATCH, "structural_scan.json")
with open(out, "w", encoding="utf-8") as fh:
    json.dump({"dead": [{"status": s, "url": u, "uses": uses[u]} for s, c, u in dead],
               "total": len(rows)}, fh, indent=2, ensure_ascii=False)
print("\nwritten:", out)
