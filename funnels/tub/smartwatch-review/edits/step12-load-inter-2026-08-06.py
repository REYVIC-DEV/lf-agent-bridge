#!/usr/bin/env python3
"""Declare the Inter @font-face rules on step 12 so the page actually renders Inter.

Problem being fixed: the only @font-face family on the page was `InterFallback`, so
every character rendered in the Arial-metric fallback and weight 800 was
synthesised — the "fonts look thin" symptom. Proven by canvas measurement: `Inter`
at 800 measured 185.5px, identical to a nonsense family name.

Cause: the blocks use the stack `Inter, InterFallback, sans-serif`, so LF asks
Google for a family literally named that. The returned faces are declared under the
whole string, which the stack's `Inter` token never matches — the page was
downloading 3 Inter woff2 (~71 KiB) it could not use.

Fix: declare the faces ourselves against the same-origin Cloudflare Fonts URLs, the
same ones LF/CF already emit, so the browser dedupes rather than double-fetching.
Weights from the body audit: 400 x231, 700 x33, 800 x20, 600 x20, 900 x1, plus 500
for safety (a declared-but-unused face costs nothing — it is only fetched on use).

Expected cost, stated up front: this is the change that took step 3 from
98-equivalent down to ~90, because real font bytes land on the critical path. The
71 KiB already being wasted becomes useful, and 600/700 additionally load.
"""
import json, sys
sys.path.insert(0, ".")
import lf_api

FUNNEL = "fun_vGqQYxn4H2i_traYYkh4w"
STEP = "step_0hL9bV7NUmyESdgkwY4Ih"
WEIGHTS = (400, 500, 600, 700, 800, 900)

faces = "\n".join(
    "@font-face{font-family:'Inter';font-style:normal;font-weight:%d;font-display:swap;"
    "src:url('/cf-fonts/s/inter/5.2.8/latin/%d/normal.woff2') format('woff2')}" % (w, w)
    for w in WEIGHTS)

BLOCK = """
<!-- PERF/FIDELITY: declare Inter ourselves.
     Without this the only @font-face family on the page is InterFallback, so every
     character renders in the Arial-metric fallback and weight 800 is synthesised
     (the "too thin" look). Cause: the blocks use the stack
     `Inter, InterFallback, sans-serif`, so LF asks Google for a family literally
     named that; the returned faces carry that whole string as their family name,
     which the stack's `Inter` token never matches — the page was fetching 3 Inter
     woff2 (~71 KiB) it could not use.
     These point at the same same-origin /cf-fonts/ URLs LF/CF already emit, so the
     browser dedupes instead of double-fetching. Removing them silently reverts the
     page to Arial. -->
<style>
%s
</style>
""" % faces

tok = open(".session_token").read().strip()
acct = open(".lf_account").read().strip()
h = lf_api.session_headers(acct)
node = lf_api.get_funnel_steps(tok, FUNNEL, extra_headers=h)
s = {x["uid"]: x for x in node["steps"]}[STEP]

st = s["settings"]
st = json.loads(st) if isinstance(st, str) else dict(st or {})
ch = dict(st.get("custom_html") or {})
hdr = ch.get("header") or ""
assert "font-family:'Inter'" not in hdr, "Inter faces already declared"
open("funnels/tub/smartwatch-review/settings/"
     "step12-custom_html-header.backup-2026-08-06.html", "w", encoding="utf-8").write(hdr)
ch["header"] = hdr.rstrip() + "\n" + BLOCK
st["custom_html"] = ch

b = s["body"]
lf_api.gql(tok, "mutation($id:ID!,$node:InputFunnel!){updateFunnel(id:$id,node:$node){id}}",
           {"id": FUNNEL, "node": {"steps": [{
               "id": STEP, "slug": s["slug"], "title": s["title"], "type": s["type"],
               "settings": st, "visual": s["visual"],
               "body": json.dumps(b) if isinstance(b, str) else b}]}}, extra_headers=h)
print(f"declared Inter {WEIGHTS}")
print(f"custom_html.header {len(hdr)} -> {len(ch['header'])} chars (backup saved)")
