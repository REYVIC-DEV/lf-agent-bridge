#!/usr/bin/env python3
"""Upload the real V2 hero + heart-tracking images (exported from Figma nodes
36:44 and 36:274, verified against the design screenshot) into the LF media
library, and patch the hlth_v2 image manifest in place with the new records.
Read-only w.r.t. the funnel itself -- no createStep/updateFunnel call here.
"""
import sys, json
sys.path.insert(0, '.')
import lf_api

tok = open('.session_token').read().strip()
ACCT = open('.lf_account').read().strip()
HH = {"account-id": ACCT, "version": "1",
      "Origin": "https://app.lightfunnels.com", "Referer": "https://app.lightfunnels.com/"}

MANIFEST = "/private/tmp/claude-501/-Users-randellbenedictcalilung-lf-agent-bridge/7431a924-4bd6-4204-ba0e-20295bef73dd/scratchpad/hlth_v2_img_map.json"
ASSETS = "/private/tmp/claude-501/-Users-randellbenedictcalilung-lf-agent-bridge/7431a924-4bd6-4204-ba0e-20295bef73dd/scratchpad/v2_qa/real_assets"

targets = {
    "hero": ASSETS + "/resized_66688fcc3c1a738cd759f3539bb5eb5b45feab30.png",
    "heart_bp": ASSETS + "/resized_4f06a59dc760bc6c926e0ef000cbeb9dbe3590f5.png",
}

manifest = json.load(open(MANIFEST))
for key, path in targets.items():
    rec = lf_api.upload_local_image(tok, path, extra_headers=HH)
    print(key, "->", rec)
    manifest[key] = rec

json.dump(manifest, open(MANIFEST, "w"), indent=2)
print("manifest updated:", MANIFEST)
