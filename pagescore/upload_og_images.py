#!/usr/bin/env python3
"""Upload the purpose-cut 1200x630 social images into the LF media library and write
pagescore/.cache/og_img_map.json with the {src_id,src_uid,src} record per page key.

Why these exist: the QA run found six pages sharing one og:image, three pages sharing a
2.0 MB file, one page using the byline author's 300x278 headshot as its share card, and
one 900x1600 portrait in a 1.91:1 slot. Each crop here is cut from a full-resolution
asset already in the library (see pagescore/.cache/og_src/ and the ASSIGN table in the
QA notes), sized to exactly 1200x630 and compressed under 300 KB.

Idempotent: keys already present in the map are skipped, so a re-run is free.
"""
import sys, os, json
sys.path.insert(0, '.')
import lf_api

tok = open('.session_token').read().strip()
ACCT = open('.lf_account').read().strip() if os.path.exists('.lf_account') else ''
HH = {"account-id": ACCT, "version": "1",
      "Origin": "https://app.lightfunnels.com", "Referer": "https://app.lightfunnels.com/"}

SRC_DIR = "pagescore/.cache/og_src"
OUT = "pagescore/.cache/og_img_map.json"
KEYS = ["bh-v1", "bh-v2", "bh-v3", "oura-v1", "oura-v2", "oura-v3",
        "sre-v1", "sre-v2", "sre-v3", "top5"]

result = json.load(open(OUT)) if os.path.exists(OUT) else {}
for key in KEYS:
    if key in result:
        print("skip (already uploaded):", key); continue
    fpath = os.path.join(SRC_DIR, key + ".jpg")
    print("uploading", key, "<-", fpath)
    rec = lf_api.upload_local_image(tok, fpath, extra_headers=HH, content_type="image/jpeg")
    result[key] = rec
    print("  ->", rec["src"])
    json.dump(result, open(OUT, "w"), indent=2)

json.dump(result, open(OUT, "w"), indent=2)
print("DONE ->", OUT, "|", len(result), "images")
