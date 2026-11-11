#!/usr/bin/env python3
"""Resize the Figma image-fill exports and upload them into the LF media library.

Run from the repo root.  Writes pagescore/.cache/sleep_img_map.json, which
build_sleep_masks.py reads -- so the upload happens once, not on every deploy.
"""
import os, sys, json
sys.path.insert(0, '.')
from PIL import Image
import lf_api

RUN = "pagescore/runs/sleep-mask-2026-10-26"
CROPS = os.path.join(RUN, "crops")
TMP = os.path.join(CROPS, "_upload")
OUT = "pagescore/.cache/sleep_img_map.json"

tok = open('.session_token').read().strip()
ACCT = open('.lf_account').read().strip()
HH = {"account-id": ACCT, "version": "1",
      "Origin": "https://app.lightfunnels.com", "Referer": "https://app.lightfunnels.com/"}

# key -> (source file, target width, kind)
#  widths are ~2x the largest rendered box so a retina screen is covered and
#  nothing is upscaled; JPEG for photographs, PNG for the flat-colour logo.
SRC = {
    "hero_left":  ("7eb8210f29e9fa681cbcb18f828315959137b54d.png", 1200, "jpg"),
    "hero_right": ("2c661ed70a44db38e319b3a17008d2083ae33d51.png",  900, "jpg"),
    "rev1":       ("4253d0258bdc87ac544441a7e7899a5591d99822.png", 1400, "jpg"),
    "rev2":       ("909e5e04847e95b59de2e754ad2c11f427002202.png", 1400, "jpg"),
    "rev3":       ("eca1d9709dc197217c640dd51ac63772601f0990.png", 1400, "jpg"),
    "rev4":       ("3a69d6d0e48f6a285115856982df02eb29e74104.png", 1400, "jpg"),
    "rev5":       ("f8f32eebf0b07d4cc1812aef45d825ce1081ce8b.png", 1400, "jpg"),
    "buybox":     ("02d403d2e63c80b511bfd5601f6e3e257ab46eb4.png",  900, "jpg"),
    "logo":       ("983-2579.png", 498, "png"),
}


def prep():
    os.makedirs(TMP, exist_ok=True)
    made = {}
    for key, (fn, w, kind) in SRC.items():
        im = Image.open(os.path.join(CROPS, fn))
        if im.width > w:
            im = im.resize((w, round(im.height * w / im.width)), Image.LANCZOS)
        dst = os.path.join(TMP, "%s.%s" % (key, kind))
        if kind == "jpg":
            im.convert("RGB").save(dst, "JPEG", quality=85, optimize=True, progressive=True)
        else:
            im.save(dst, "PNG", optimize=True)
        made[key] = dst
        print("%-11s %sx%s  %.0f KB" % (key, im.width, im.height, os.path.getsize(dst) / 1024))

    # OG/social card: 1200x630 centre crop of the hero photograph, which is what
    # the page is actually about (a tester asleep on their side in the mask).
    im = Image.open(os.path.join(CROPS, SRC["hero_left"][0])).convert("RGB")
    tw, th = 1200, 630
    s = max(tw / im.width, th / im.height)
    im = im.resize((round(im.width * s), round(im.height * s)), Image.LANCZOS)
    left = (im.width - tw) // 2
    top = (im.height - th) // 2
    im = im.crop((left, top, left + tw, top + th))
    dst = os.path.join(TMP, "social.jpg")
    im.save(dst, "JPEG", quality=86, optimize=True, progressive=True)
    made["social"] = dst
    print("%-11s %sx%s  %.0f KB" % ("social", tw, th, os.path.getsize(dst) / 1024))
    return made


def main():
    made = prep()
    cache = json.load(open(OUT)) if os.path.exists(OUT) else {}
    for key, path in made.items():
        if key in cache:
            print("skip (cached)", key)
            continue
        ct = "image/png" if path.endswith(".png") else "image/jpeg"
        rec = lf_api.upload_local_image(tok, path, extra_headers=HH, content_type=ct)
        cache[key] = rec
        json.dump(cache, open(OUT, "w"), indent=1)
        print("uploaded", key, rec["src"])
    print("wrote", OUT)


if __name__ == "__main__":
    main()
