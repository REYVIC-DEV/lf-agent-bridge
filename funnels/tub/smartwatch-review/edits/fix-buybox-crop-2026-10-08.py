#!/usr/bin/env python3
"""Stop the buy box image cropping its app badges on mobile.

The Image block carried TWO height props - `100%` and `320px` - and the 320px
one won. With `width:100%` that makes the box 347x320 on a 390 phone: wider than
tall. The source is square (1080x1080) and `objectFit:cover` fills the width, so
27px came off the height, 13.5px of it from the bottom, which is exactly where
the App Store and Google Play badges sit.

Setting height to `auto` lets a square source render square at whatever width the
card gives it, so cover has nothing left to crop. No new style prop is
introduced: `auto` is an ordinary value on a prop the block already has, which
keeps us clear of the SSR's 503-on-unknown-prop behaviour.

Verified in the live DOM before writing, at 430 / 412 / 375 / 320: square at
every width, 0px cropped, no horizontal overflow, badges fully visible.

MEASURED AFTER THE WRITE: desktop did NOT change. It still renders 290x323 and
still trims ~16.5px off each SIDE, because a different rule sets its height. So
this fix is mobile-only, which is the safer outcome than the one anticipated
here, but the desktop side-crop is a real pre-existing defect that remains open.

Live after the write: 320 -> 277x277, 390 -> 347x347, both square, 0px cropped,
no horizontal overflow, 0 console errors.
"""
import io, json, os, sys, time
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", "..", "..", ".."))
sys.path.insert(0, ROOT); os.chdir(ROOT)
import lf_api

FUNNEL = "fun_vGqQYxn4H2i_traYYkh4w"
SLUG   = "best-fitness-trackers-2026"
BLOCK  = "2e0df6c9-3845-4266-ba46-3ab47ecbd8d9"
BACKUP = os.path.join(HERE, "..", "steps", "%s.pre-buybox-fix-2026-10-08.json" % SLUG)
APPLY  = "--apply" in sys.argv

tok = open(".session_token").read().strip()
acct = open(".lf_account").read().strip()
h = lf_api.session_headers(acct)
Q = '''query($id:ID!){node(id:$id){... on Funnel{steps{
      uid slug title type product_id settings visual{x y} body}}}}'''

n = lf_api.gql(tok, Q, {"id": FUNNEL}, extra_headers=h)["node"]
s = [x for x in n["steps"] if x["slug"] == SLUG][0]

found = []
def walk(node):
    if isinstance(node, dict):
        if node.get("id") == BLOCK:
            found.append(node)
        for v in node.values(): walk(v)
    elif isinstance(node, list):
        for v in node: walk(v)
walk(s["body"])
assert len(found) == 1, "expected exactly one buybox image block, got %d" % len(found)
img = found[0]

heights = [st for st in img.get("styles") or [] if st.get("prop") == "height"]
print("before:", [st.get("value") for st in heights])
assert any(st.get("value") == "320px" for st in heights), "the 320px height is gone - stop and re-read"

io.open(BACKUP, "w", encoding="utf-8").write(json.dumps(s, indent=1))
print("backed up step -> %s (%d bytes)" % (os.path.relpath(BACKUP, ROOT), os.path.getsize(BACKUP)))

for st in heights:
    if st.get("value") == "320px":
        st["value"] = "auto"
print("after :", [st.get("value") for st in heights])

if not APPLY:
    sys.exit("(dry run - nothing written)")

lf_api.gql(tok, "mutation($id:ID!,$node:InputFunnel!){updateFunnel(id:$id,node:$node){id}}",
    {"id": FUNNEL, "node": {"steps": [{
        "id": s["uid"], "slug": s["slug"], "title": s["title"], "type": s["type"],
        "settings": s["settings"], "visual": s["visual"],
        "product_id": s["product_id"], "body": s["body"]}]}}, extra_headers=h)
print("WRITTEN")
time.sleep(10)

import urllib.request
b = urllib.request.urlopen(urllib.request.Request(
    "https://www.techunboxed.co/smartwatch-review/%s?cb=%d" % (SLUG, time.time()),
    headers={"User-Agent": "Mozilla/5.0", "Cache-Control": "no-cache"}), timeout=90
    ).read().decode("utf-8", "replace")
print("served: %d bytes | '320px' near the image: %s" % (len(b), "320px" in b))
