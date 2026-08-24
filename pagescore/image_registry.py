#!/usr/bin/env python3
"""
image_registry.py — Inventory every image used across the account's funnels, so
a "new" image can be matched against one that is ALREADY in the LF library
instead of uploading a near-duplicate.

The problem it solves: the same photo gets re-uploaded once per funnel, so the
media library fills with visually identical assets under different uids, and
page weight/cache locality suffer. Before uploading anything, check here first.

  build   walk every funnel's page bodies, collect Image blocks, fingerprint the
          bytes, write a registry JSON
  match   fingerprint local file(s) and report existing library images that are
          identical or visually near-identical

Matching uses two fingerprints, reported separately because they mean different
things:

  sha256  exact byte equality — the same file. A hit means reuse with zero risk.
  dhash   64-bit perceptual difference hash (row-wise gradient). Survives
          re-encoding, resizing and format changes, which is exactly the
          "similar looking image on another funnel" case. Hamming distance 0-4
          is effectively the same picture; 5-10 is a close variant (different
          crop/edit) worth a human look; >10 is unrelated.

dhash is a HEURISTIC. It compares low-frequency structure, so it can collide on
images that share a layout (two screenshots of the same UI, two flat logos on
white). Always eyeball a perceptual-only hit before reusing it.

  python3 image_registry.py build [--out DIR]
  python3 image_registry.py match FILE... [--registry PATH] [--threshold N]
"""
import argparse
import hashlib
import io
import json
import os
import sys
import urllib.parse
import urllib.request

import lf_api

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)                          # pagescore/ -> repo root
DEFAULT_OUT = os.path.join(ROOT, "funnels", "_registry")

try:
    from PIL import Image
except ImportError:
    Image = None


# ------------------------------------------------------------------ fingerprints
def dhash(data, size=8):
    """64-bit row-gradient perceptual hash as a hex string, or None if the bytes
    aren't a raster Pillow can open (SVGs, for instance)."""
    if Image is None:
        return None
    try:
        im = Image.open(io.BytesIO(data)).convert("L").resize(
            (size + 1, size), Image.LANCZOS)
    except Exception:
        return None
    bits = 0
    for y in range(size):
        for x in range(size):
            bits = (bits << 1) | int(im.getpixel((x, y)) > im.getpixel((x + 1, y)))
    return f"{bits:016x}"


def hamming(a, b):
    """Bit distance between two hex dhashes; None if either is missing."""
    if not a or not b:
        return None
    return bin(int(a, 16) ^ int(b, 16)).count("1")


def dimensions(data):
    if Image is None:
        return None
    try:
        return list(Image.open(io.BytesIO(data)).size)
    except Exception:
        return None


def fingerprint_bytes(data):
    return {"sha256": hashlib.sha256(data).hexdigest(),
            "dhash": dhash(data), "bytes": len(data),
            "dim": dimensions(data)}


# ------------------------------------------------------------------ build
def _session():
    tok = open(os.path.join(ROOT, ".session_token")).read().strip()
    acct = open(os.path.join(ROOT, ".lf_account")).read().strip()
    return tok, acct, lf_api.session_headers(acct)


def _walk_images(node, out):
    """Collect every Image block in a page body tree."""
    if not isinstance(node, dict):
        return
    p = node.get("p") or {}
    if node.get("t") == "Image" and p.get("src"):
        out.append({
            "src": p.get("src"), "src_id": p.get("src_id"),
            "src_uid": p.get("src_uid"), "alt": p.get("alt"),
            "styles": {s.get("prop"): s.get("value")
                       for s in (node.get("styles") or [])
                       if s.get("prop") in ("width", "height", "objectFit",
                                            "borderRadius")},
        })
    for child in (p.get("children") or []):
        _walk_images(child, out)


def _fetch(url, timeout=60):
    # LF filenames keep the original upload name, so a lot of these urls contain
    # spaces, parentheses and even '→'. urllib refuses them raw ("URL can't
    # contain control characters"), which silently drops those images from the
    # registry and makes match() report upload-new for an image we already have.
    # Percent-encode the path/query, leaving already-escaped sequences alone.
    parts = urllib.parse.urlsplit(url)
    url = urllib.parse.urlunsplit((
        parts.scheme, parts.netloc,
        urllib.parse.quote(parts.path, safe="/%"),
        urllib.parse.quote(parts.query, safe="=&%"), parts.fragment))
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return r.read()


def build(args):
    tok, acct, h = _session()
    funnels = lf_api.gql(tok, """
      query { funnels(first: 100, query: "order_by:id order_dir:desc") {
        edges { node { id name slug } } } }""", {}, extra_headers=h)["funnels"]["edges"]
    funnels = [e["node"] for e in funnels]
    print(f"scanning {len(funnels)} funnels...", file=sys.stderr)

    # url -> record (a url may be reused across many funnels/steps)
    by_url = {}
    for f in funnels:
        try:
            detail = lf_api.get_funnel_steps(tok, f["id"], extra_headers=h)
        except RuntimeError as e:
            print(f"  ! {f['slug']}: {e}", file=sys.stderr)
            continue
        for step in detail.get("steps") or []:
            found = []
            _walk_images(step.get("body"), found)
            for im in found:
                rec = by_url.setdefault(im["src"], {
                    "src": im["src"], "src_id": im["src_id"],
                    "src_uid": im["src_uid"], "used_by": [],
                })
                rec["used_by"].append({
                    "funnel_id": f["id"], "slug": f["slug"], "name": f["name"],
                    "step_uid": step["uid"], "step_title": step.get("title"),
                    "alt": im["alt"], "styles": im["styles"],
                })
        print(f"  {f['slug']}: {len(detail.get('steps') or [])} steps", file=sys.stderr)

    print(f"fingerprinting {len(by_url)} unique images...", file=sys.stderr)
    for i, (url, rec) in enumerate(sorted(by_url.items()), 1):
        try:
            rec.update(fingerprint_bytes(_fetch(url)))
        except Exception as e:
            rec["error"] = str(e)
            print(f"  ! {i}: {url[-40:]}: {e}", file=sys.stderr)

    os.makedirs(args.out, exist_ok=True)
    path = os.path.join(args.out, "images.json")
    registry = {
        "account": acct,
        "funnels_scanned": len(funnels),
        "unique_images": len(by_url),
        "images": sorted(by_url.values(), key=lambda r: -len(r["used_by"])),
    }
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(registry, fh, indent=2)

    dupes = _perceptual_clusters(registry["images"])
    print(f"\nwrote {path}", file=sys.stderr)
    print(f"{len(by_url)} unique urls across {len(funnels)} funnels; "
          f"{len(dupes)} near-duplicate cluster(s) already in the library",
          file=sys.stderr)
    for c in dupes:
        print("  cluster: " + ", ".join(x["src_uid"] or "?" for x in c), file=sys.stderr)
    print(json.dumps({"registry": path, "unique_images": len(by_url),
                      "funnels_scanned": len(funnels),
                      "near_duplicate_clusters": len(dupes)}, indent=2))


def _perceptual_clusters(images, threshold=4):
    """Group library images that are already near-identical to each other."""
    seen, clusters = set(), []
    for i, a in enumerate(images):
        if i in seen or not a.get("dhash"):
            continue
        group = [a]
        for j, b in list(enumerate(images))[i + 1:]:
            if j in seen or not b.get("dhash"):
                continue
            d = hamming(a["dhash"], b["dhash"])
            if d is not None and d <= threshold:
                group.append(b)
                seen.add(j)
        if len(group) > 1:
            clusters.append(group)
    return clusters


# ------------------------------------------------------------------ match
def match(args):
    with open(args.registry, encoding="utf-8") as fh:
        registry = json.load(fh)
    images = registry["images"]
    results = []
    for path in args.files:
        with open(path, "rb") as fh:
            fp = fingerprint_bytes(fh.read())
        exact = [im for im in images if im.get("sha256") == fp["sha256"]]
        near = []
        for im in images:
            d = hamming(fp["dhash"], im.get("dhash"))
            if d is not None and d <= args.threshold and im not in exact:
                near.append((d, im))
        near.sort(key=lambda x: x[0])
        results.append({
            "file": path, "sha256": fp["sha256"], "dhash": fp["dhash"],
            "dim": fp["dim"], "bytes": fp["bytes"],
            "exact_match": [{"src_uid": im["src_uid"], "src_id": im["src_id"],
                             "src": im["src"],
                             "used_by": [u["slug"] for u in im["used_by"]]}
                            for im in exact],
            "near_matches": [{"distance": d, "src_uid": im["src_uid"],
                              "src_id": im["src_id"], "src": im["src"],
                              "dim": im.get("dim"),
                              "used_by": [u["slug"] for u in im["used_by"]]}
                             for d, im in near[:5]],
            "verdict": ("reuse-exact" if exact else
                        "review-near" if near else "upload-new"),
        })
    print(json.dumps(results, indent=2))
    for r in results:
        print(f"{os.path.basename(r['file'])}: {r['verdict']}"
              + (f" -> {r['exact_match'][0]['src_uid']}" if r["exact_match"] else "")
              + (f" ({len(r['near_matches'])} near)" if r["near_matches"] else ""),
              file=sys.stderr)


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)

    p = sub.add_parser("build"); p.set_defaults(fn=build)
    p.add_argument("--out", default=DEFAULT_OUT)

    p = sub.add_parser("match"); p.set_defaults(fn=match)
    p.add_argument("files", nargs="+")
    p.add_argument("--registry", default=os.path.join(DEFAULT_OUT, "images.json"))
    p.add_argument("--threshold", type=int, default=10,
                   help="max dhash Hamming distance to report (default 10)")

    args = ap.parse_args()
    try:
        args.fn(args)
    except RuntimeError as e:
        sys.exit(f"ERROR: {e}")


if __name__ == "__main__":
    main()
