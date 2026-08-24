#!/usr/bin/env python3
"""Upload the new Figma exports for build_ranked_comparison.py into the LF image
library (session mode) and write pagescore/.cache/rc_img_map.json with the
{src_id,src_uid,src} record per key, merged with reused keys from the existing
hlth_v3_img_map.json (avatar_byline, avatar_author, logo)."""
import sys, os, json
sys.path.insert(0, '.')
import lf_api

tok = open('.session_token').read().strip()
ACCT = open('.lf_account').read().strip() if os.path.exists('.lf_account') else ''
HH = {"account-id": ACCT, "version": "1",
      "Origin": "https://app.lightfunnels.com", "Referer": "https://app.lightfunnels.com/"}

RESIZED = "pagescore/.cache/rc_resized"

# key -> (filename, content_type)
FILES = {
    "hero":              ("42f725e59e19ee23770aa1abed3e8721c7c2b192.jpg", "image/jpeg"),
    "hlth_thumb":        ("d157be09335dc463b3636745c65dd9b522474dfa.png", "image/png"),
    "whoop_thumb":       ("918bb1e574b57e62cf342d301078d8789c580f99.png", "image/png"),
    "apple_thumb":       ("5406039ca4d37f46f05b662425f55cdc3bc93267.png", "image/png"),
    "garmin_thumb":      ("f66655bac8cdb7dcff8de0b05fc58813f313daa2.png", "image/png"),
    "fitbit_thumb":      ("f9bd6aa337051a91f6b935ef6f5f77db72c39f9e.png", "image/png"),
    "why_hlth_won":      ("aa8c3c9651a3eeeb6d84ccdf21277bceb68af4c8.jpg", "image/jpeg"),
    "cuff_test":         ("b1c0bcad8dd6804cd410ce0f7b642ce2dab0327e.jpg", "image/jpeg"),
    "app_home":          ("453694996c23a1772f4aa67cfbadd7bb02142e93.jpg", "image/jpeg"),
    "app_bp":            ("3429403d5e40d6515ca998c3de9f5f79d5a00c81.jpg", "image/jpeg"),
    "app_sleep":         ("9d9e7cdbf941a69225098e472c971238207900ef.jpg", "image/jpeg"),
    "bicep_strap":       ("5b51dc12be629ee57df1bbba92a689aa904988a9.jpg", "image/jpeg"),
    "cost_video_still":  ("0ae97d40c9ecebb45bd7666867c007a491f32414.jpg", "image/jpeg"),
    "trustpilot_shot":   ("6190a7cd473dd8f40a481f2984eac44011f256a1.png", "image/png"),
    "closing_lifestyle": ("343b3e51fb203c061840e5b8a5ec8de21062a9c0.jpg", "image/jpeg"),
}

out_path = "pagescore/.cache/rc_img_map.json"
result = {}
if os.path.exists(out_path):
    result = json.load(open(out_path))

for key, (fname, ctype) in FILES.items():
    if key in result:
        print("skip (already uploaded):", key)
        continue
    fpath = os.path.join(RESIZED, fname)
    print("uploading", key, "<-", fpath)
    rec = lf_api.upload_local_image(tok, fpath, extra_headers=HH, content_type=ctype)
    rec["figma_node"] = fname
    result[key] = rec
    print("  ->", rec["src"])
    json.dump(result, open(out_path, "w"), indent=2)

# merge in reused keys from the v3 map (same asset, no re-upload)
v3 = json.load(open("pagescore/.cache/hlth_v3_img_map.json"))
for key in ("avatar_byline", "avatar_author", "logo"):
    if key not in result:
        result[key] = v3[key]

json.dump(result, open(out_path, "w"), indent=2)
print("DONE ->", out_path)
print(json.dumps(result, indent=2))
