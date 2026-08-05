#!/usr/bin/env python3
"""
image_prep.py — Right-size + compress an image before it goes to the
Lightfunnels media library.

Why this exists: Figma originals are huge (4096px, tens of MB) and the LF
presigned-upload policy caps a file at 5 MB. Uploading the raw original either
fails outright or ships a 20 MB asset to every page visitor.

Two stages, deliberately separate:

  1. RESIZE — downscale the long edge to `max_px` (Lanczos), skipped when the
     image is already small enough. An image only needs ~2x its rendered CSS
     size to look sharp on a retina screen, so a 700px-wide article photo needs
     ~1400px, not 4096px. This is where nearly all the saving comes from.

  2. COMPRESS — codec chosen by CONTENT TYPE. "Always lossless" is wrong here:

       --mode photo    lossy WebP (default quality 90, method 6)
       --mode graphic  lossless WebP (method 6, exact)

     Lossless WebP on a 1400px photograph lands ~1.3 MB, while the photos
     already live on these funnels are 27-76 KB. Defaulting to lossless would
     ship a ~17x weight regression on a hero image and defeat the whole point.
     Measured on a real 1400x1034 advertorial photo: 140 KB at q90 vs 1283 KB
     lossless, mean pixel error 1.37/255 (~0.5%) — not perceptible.

     Logos, flat graphics, UI screenshots and anything with hard edges or text
     go the other way: use `graphic`, where lossy ringing would actually show.

For photo mode this reports the measured mean/max pixel error against the
resized source, so the "not perceptible" claim is checked rather than asserted.

  python3 image_prep.py <in> [more ...] --out DIR [--mode photo|graphic]
                        [--max-px 1400] [--quality 90]
"""
import argparse
import json
import os
import sys

try:
    from PIL import Image, ImageChops, ImageStat
except ImportError:
    sys.exit("Pillow required. Run: python3 -m pip install Pillow")

# 5 MB presigned-policy ceiling, minus headroom for the multipart envelope.
LF_UPLOAD_LIMIT = 5 * 1024 * 1024
SAFE_LIMIT = int(LF_UPLOAD_LIMIT * 0.94)


def _save(im, path, mode, quality, fmt="webp"):
    """Write `im` to `path`. `mode` picks the codec: photo = lossy, graphic =
    lossless. PNG is always lossless regardless of mode."""
    if fmt == "png":
        im.save(path, "PNG", optimize=True, compress_level=9)
    elif mode == "graphic":
        # lossless=True ignores `quality`; method=6 = slowest/smallest search.
        im.save(path, "WEBP", lossless=True, method=6, exact=True)
    else:
        im.save(path, "WEBP", quality=quality, method=6)


def _error_vs(reference, path):
    """Mean/max per-channel pixel error between the resized source and the
    encoded file. Returns None for lossless (where it is 0 by construction)."""
    try:
        got = Image.open(path).convert("RGB")
        ref = reference.convert("RGB")
        if got.size != ref.size:
            return None
        diff = ImageChops.difference(ref, got)
        st = ImageStat.Stat(diff)
        return {"mean": round(sum(st.mean) / len(st.mean), 3),
                "max": max(st.extrema[i][1] for i in range(len(st.extrema)))}
    except Exception:
        return None


def prepare(src, out_dir, max_px=1400, mode="photo", quality=90, fmt="webp",
            limit=SAFE_LIMIT):
    """Resize (if needed) then compress `src` into `out_dir`.

    Raises RuntimeError if the result still exceeds `limit` after stepping the
    resolution down, so a caller never silently uploads something the policy
    will reject.
    """
    os.makedirs(out_dir, exist_ok=True)
    src_bytes = os.path.getsize(src)
    im = Image.open(src)
    src_w, src_h = im.size

    if im.mode not in ("RGB", "RGBA", "L"):
        im = im.convert("RGBA" if "A" in im.mode else "RGB")
    # Lossy WebP has no alpha advantage here and RGBA can surface halos on a
    # flattened background; keep alpha only when the source actually uses it.
    if im.mode == "RGBA" and not any(px < 255 for px in im.getchannel("A").getdata()):
        im = im.convert("RGB")

    resized = False
    if max_px and max(im.size) > max_px:
        scale = max_px / float(max(im.size))
        im = im.resize((max(1, round(im.width * scale)),
                        max(1, round(im.height * scale))), Image.LANCZOS)
        resized = True

    base = os.path.splitext(os.path.basename(src))[0]
    out = os.path.join(out_dir, f"{base}.{fmt}")
    _save(im, out, mode, quality, fmt)

    # Over the cap: for a photo drop quality first (cheap, invisible at these
    # levels); for a graphic the only honest lever is fewer pixels.
    q = quality
    while os.path.getsize(out) > limit and mode == "photo" and q > 60:
        q -= 10
        _save(im, out, mode, q, fmt)
    steps = 0
    while os.path.getsize(out) > limit and max(im.size) > 400:
        im = im.resize((max(1, round(im.width * 0.85)),
                        max(1, round(im.height * 0.85))), Image.LANCZOS)
        _save(im, out, mode, q, fmt)
        resized = True
        steps += 1

    out_bytes = os.path.getsize(out)
    if out_bytes > limit:
        raise RuntimeError(
            f"{src}: {out_bytes} bytes still exceeds the {limit} upload cap at "
            f"{im.width}x{im.height}. Crop the source or lower --quality.")

    rec = {
        "src": src, "out": out, "format": fmt, "mode": mode,
        "lossless": mode == "graphic" or fmt == "png",
        "quality": None if (mode == "graphic" or fmt == "png") else q,
        "src_dim": [src_w, src_h], "out_dim": list(im.size),
        "src_bytes": src_bytes, "out_bytes": out_bytes,
        "saved_pct": round(100 * (1 - out_bytes / src_bytes), 1) if src_bytes else None,
        "resized": resized, "extra_downsteps": steps,
    }
    if not rec["lossless"]:
        rec["pixel_error"] = _error_vs(im, out)
    return rec


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("inputs", nargs="+")
    ap.add_argument("--out", required=True, help="output directory")
    ap.add_argument("--mode", default="photo", choices=["photo", "graphic"],
                    help="photo = lossy WebP (default); graphic = lossless, for "
                         "logos/flat art/screenshots with hard edges or text")
    ap.add_argument("--max-px", type=int, default=1400,
                    help="cap the long edge (0 = never resize; default 1400)")
    ap.add_argument("--quality", type=int, default=90,
                    help="WebP quality for --mode photo (default 90)")
    ap.add_argument("--format", default="webp", choices=["webp", "png"],
                    help="container (png is always lossless)")
    args = ap.parse_args()

    results = [prepare(p, args.out, args.max_px, args.mode, args.quality,
                       args.format) for p in args.inputs]
    print(json.dumps(results, indent=2))
    tin = sum(r["src_bytes"] for r in results)
    tout = sum(r["out_bytes"] for r in results)
    kind = "lossless" if results[0]["lossless"] else f"lossy q{args.quality}"
    print(f"\n{len(results)} file(s): {tin/1e6:.2f} MB -> {tout/1e6:.2f} MB "
          f"({100*(1-tout/tin):.1f}% smaller, {kind})", file=sys.stderr)
    for r in results:
        if r.get("pixel_error"):
            print(f"  {os.path.basename(r['out'])}: mean pixel error "
                  f"{r['pixel_error']['mean']}/255", file=sys.stderr)


if __name__ == "__main__":
    main()
