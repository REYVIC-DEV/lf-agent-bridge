#!/usr/bin/env python3
"""Give every live TechUnboxed funnel the site favicon.

WHY THIS EXISTS
---------------
The favicon is NOT header code. It is a funnel-level field, `favicon_id`, and
LF renders it into each step's <head> as <link rel="icon">. Grepping
header_scripts and step custom_html for "favicon" finds nothing on any of the
27 funnels, which reads as "no favicon anywhere" and is wrong -- two funnels
had one all along, set through the field.

On 2026-10-08 a sweep found 2 of 27 funnels carrying a favicon:
  Google funnels - UK (/article)  img_H_5N7Xpw7rdSj9Y7Gl1f0  <- TechUnboxed
  Garlic Funnel (/aged-garlic)    img_gmDfAC2I6kiSBycImeIzn  <- its own brand
Every other funnel serves `<link rel="icon" href="data:image/x-icon;,">` -- an
EMPTY data URI, which is LF's placeholder. That is worse than nothing: it is a
valid icon declaration, so the browser honours it and never falls back to
/favicon.ico. (techunboxed.co/favicon.ico 404s anyway, so there is no fallback
to reach.)

SCOPE -- confirmed with Joshua on 2026-10-08: live TechUnboxed funnels only.
Deliberately NOT included:
  archives, [DUPLICATE]s, test funnels   nobody sees them
  Garlic Funnel                          different brand, already has its own
  Scaling or Failing - Event             moving to scalingorfailing.com
  Oregano Advertorials                   serves on techunboxed.co but is a
                                         separate product brand -- flagged to
                                         Joshua rather than assumed
Every funnel below was verified to serve on www.techunboxed.co with a matching
canonical before being listed here, so this is one site getting one icon.

WHAT PROPAGATION ACTUALLY LOOKS LIKE
-----------------------------------
`favicon_id` is funnel-level, so NO step write is needed -- on a funnel whose
renders are healthy the live <head> picks it up within seconds. Do not reach
for a flush.

The exception is a step with a frozen render. `hlth-band` kept serving the old
head for minutes after the field was set, and an identity step-write did not
move it either -- nor did an HTML-comment marker written into
settings.custom_html.header, which never appeared in the served page at all
while being correct in storage. It caught up on its own later. So a page that
has not updated yet is not proof the write failed: read storage before
assuming anything, and give it time before writing more.

USAGE
  python apply_favicon_2026-10-08.py                    # dry run, shows plan
  python apply_favicon_2026-10-08.py --apply --only hlth-band
  python apply_favicon_2026-10-08.py --apply
"""
import argparse, os, sys, time, urllib.request, urllib.error, ssl

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
sys.path.insert(0, ROOT); os.chdir(ROOT)
import lf_api

FAVICON_ID = "img_H_5N7Xpw7rdSj9Y7Gl1f0"
STORE = "https://www.techunboxed.co"

# (funnel_id, name, funnel_slug, a step slug to verify the rendered <head> with)
TARGETS = [
    ("fun_Z6I8-bN5nVJ_SwGgR9WWK", "TUB - Over-60s health - Meta",      "over-60s-health",           "best-health-gadgets-over-60"),
    ("fun_ZDkBMKGJqa6LE7150tkr0", "TUB - BH Advertorial",              "tub-bh-advertorial",        "bh-advertorial-v1"),
    ("fun_AK6-INP-0n_sq0TYQKi9L", "Google II Broad comparison",        "google-ii-broad-comparison","top-5-fitness-trackers-ranked-2026"),
    ("fun_hLmlmrbjeoGf3UZZvBEHY", "TUB - All smart ring - Meta",       "tub-allsmartring-meta",     "oura-vs-hlth"),
    ("fun_9Fa3N-u0R585oqWjg59fH", "TUB - Top 5 h trackers-v2 - META",  "HH3xh83_r",                 "gWWRJ9q3C"),
    ("fun_Z78qnXtnsXIf619roFNNU", "Meta funnels - UK",                 "meta-uk",                   "v45g6ypE3"),
    ("fun_UK-PeZ5kAFhnpBkWvo9jo", "HLTH BAND REVIEWS",                 "hlthbandreviews",           "2sp_4HUWe"),
    ("fun_B2PKx4t5Pat-ZkpCN7tPI", "Native funnels - UK",               "blog-post",                 "zQkAffXHg"),
    ("fun_GVmQMYaPpyTFiz6TONHBH", "LISTICLES [ON DEV]",                "QyoDsEoUk",                 "p8m5WBu3C-2"),
    ("fun_c_BuhpZK4YmBBIWlUrpOg", "TUB - Top 5 h trackers-v3 NATIVE",  "smartwatch-review-n",       "gWWRJ9q3C"),
    ("fun_IHHQNJZLuWVq_co-WLO5f", "TWO - Native - Topi v1 - LIVE",     "review-1",                  "n0aEeyt1d"),
    ("fun_68JsdhE4gAghe37jFY7ez", "TWO - 1st party review - heart",    "top-heart-trackers",        "top-4-heart-trackers"),
    ("fun_fJOgB3rYUaqNW6uaNxYVB", "TUB - Heart tracker comparison UK", "top-5-heart-trackers",      "zJioA3kyI"),
    ("fun_CtnFEQDBqMy3LIbFBRnlk", "hlth-band",                         "hlth-band",                 "nrnOX83Bs"),
    ("fun_vGqQYxn4H2i_traYYkh4w", "TUB - Top 5 h trackers-v2 LIVE",    "smartwatch-review",         "gWWRJ9q3C"),
]

Q = 'query($id:ID!){node(id:$id){... on Funnel{id name slug published favicon_id}}}'
M = 'mutation($id:ID!,$node:InputFunnel!){updateFunnel(id:$id,node:$node){id favicon_id}}'

_CTX = ssl.create_default_context(); _CTX.check_hostname = False; _CTX.verify_mode = ssl.CERT_NONE


def served_icon(fslug, sslug):
    """Read <link rel=icon> out of the LIVE page, cache-busted.

    The field being set is not proof the visitor sees it: LF serves a cached
    render per step, so a metadata write can sit in storage while the old head
    keeps going out. Only the served HTML settles it.
    """
    import re
    url = "%s/%s/%s?cb=%d" % (STORE, fslug, sslug, time.time())
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0",
                                                   "Cache-Control": "no-cache"})
        with urllib.request.urlopen(req, timeout=60, context=_CTX) as r:
            html = r.read(300000).decode("utf-8", "replace")
    except Exception as e:
        return "ERR %s" % str(e)[:60]
    m = re.search(r'<link[^>]+rel=["\'][^"\']*icon[^"\']*["\'][^>]+href=["\']([^"\']+)', html, re.I)
    return m.group(1) if m else "(none)"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true", help="write; otherwise dry run")
    ap.add_argument("--only", help="limit to one funnel slug")
    ap.add_argument("--verify-only", action="store_true", help="just read served icons")
    a = ap.parse_args()

    tok  = open(".session_token").read().strip()
    acct = open(".lf_account").read().strip()
    h    = lf_api.session_headers(acct)

    targets = [t for t in TARGETS if not a.only or t[2] == a.only]
    if not targets:
        sys.exit("no target matches --only %s" % a.only)

    if a.verify_only:
        for fid, name, fslug, sslug in targets:
            print("%-36s %s" % (name[:36], served_icon(fslug, sslug)))
        return

    changed = []
    for fid, name, fslug, sslug in targets:
        n = lf_api.gql(tok, Q, {"id": fid}, extra_headers=h)["node"]
        cur = n.get("favicon_id") or "-"
        if cur == FAVICON_ID:
            print("SKIP %-36s already set" % name[:36]); continue
        if not a.apply:
            print("PLAN %-36s %s -> %s" % (name[:36], cur, FAVICON_ID)); continue
        lf_api.gql(tok, M, {"id": fid, "node": {"favicon_id": FAVICON_ID}}, extra_headers=h)
        # The API rate-limits at roughly this cadence; a 15-funnel run hit
        # "rate_limit_reached" on the last read-back without this.
        time.sleep(2.5)
        after = lf_api.gql(tok, Q, {"id": fid}, extra_headers=h)["node"].get("favicon_id")
        time.sleep(2.5)
        ok = "OK " if after == FAVICON_ID else "BAD"
        print("%s  %-36s stored=%s" % (ok, name[:36], after))
        changed.append((name, fslug, sslug))

    if changed:
        print("\nwaiting 15s for the render to flush, then reading live pages")
        time.sleep(15)
        for name, fslug, sslug in changed:
            print("  %-36s %s" % (name[:36], served_icon(fslug, sslug)))


if __name__ == "__main__":
    main()
