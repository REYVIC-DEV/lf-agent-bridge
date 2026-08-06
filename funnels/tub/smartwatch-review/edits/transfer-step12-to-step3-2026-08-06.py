#!/usr/bin/env python3
"""Transfer step 12 (randell-build) onto step 3 — the LIVE entry page.

Step 3 is `starting_step_id`, so this is the page ad traffic lands on. What moves:

  body                     step 12's, wholesale — the Figma-matched offer card, the
                           wired Amazon buttons (direct URLs, no aff-* class), the
                           linked breadcrumb, the policy modal, the centred footer.
  settings.custom_html     step 12's — this is where the Inter @font-face block and
                           the popup CSS live, so it must travel with the body.
  settings.seo             **step 3's is KEPT.** It is the live, indexed URL; step 12
                           has no seo block and overwriting it would drop the live
                           page's title/description.
  slug / title / type      step 3's are KEPT — `xI7j8mDEB` is the live URL.

Deliberately dropped by the swap: step 3's aff-* classed buttons with their stale
inline Amazon URLs. Step 12 carries the current URLs directly and no class, so the
funnel header's replacer no longer participates. That is the owner's chosen model.
"""
import json, sys
sys.path.insert(0, "tools/lf-agent-bridge")
import lf_api

FUNNEL = "fun_vGqQYxn4H2i_traYYkh4w"
SRC = "step_0hL9bV7NUmyESdgkwY4Ih"   # step 12
DST = "step_-42yvjxEYUC-1yAzL9TKy"   # step 3, live entry

tok = open("tools/lf-agent-bridge/.session_token").read().strip()
acct = open("tools/lf-agent-bridge/.lf_account").read().strip()
h = lf_api.session_headers(acct)
node = lf_api.get_funnel_steps(tok, FUNNEL, extra_headers=h)
by = {s["uid"]: s for s in node["steps"]}
for u in (SRC, DST):
    assert u in by, f"missing step {u}"
src, dst = by[SRC], by[DST]

# back up the live step before touching it
json.dump(dst, open("funnels/tub/smartwatch-review/steps/"
                    "03-PRE-STEP12-TRANSFER.2026-08-06.json", "w"), indent=1)

src_st = src["settings"]; src_st = json.loads(src_st) if isinstance(src_st, str) else dict(src_st or {})
dst_st = dst["settings"]; dst_st = json.loads(dst_st) if isinstance(dst_st, str) else dict(dst_st or {})

new_st = dict(dst_st)                      # start from step 3 (keeps its seo)
new_st["custom_html"] = src_st.get("custom_html")   # take step 12's header+footer
assert new_st["custom_html"], "step 12 has no custom_html"
hdr = new_st["custom_html"].get("header") or ""
assert hdr.count("font-family:'Inter'") == 6, "Inter faces missing from the header being copied"
assert "seo" in new_st or "seo" not in dst_st, "seo handling wrong"

body = src["body"]
t = json.dumps(body) if not isinstance(body, str) else body
# unescape so HTML-attribute checks match (JSON stores id=\\"terms\\")
t = t.replace(chr(92) + chr(34), chr(34))
# sanity-check the payload we are about to put live
EXACT = {"hlthtrack.co.uk": 15, "amazon.com": 8, "aff-": 0, "<style>": 0}
ATLEAST = {'id="terms"': 1, "tu-overlay": 4, "trustpilot.com/review": 1}
for k, want in EXACT.items():
    got = t.count(k)
    assert got == want, f"body check failed: {k} = {got}, expected exactly {want}"
for k, want in ATLEAST.items():
    got = t.count(k)
    assert got >= want, f"body check failed: {k} = {got}, expected at least {want}"
print("body checks passed —", {**{k: t.count(k) for k in EXACT}, **{k: t.count(k) for k in ATLEAST}})

lf_api.gql(tok, "mutation($id:ID!,$node:InputFunnel!){updateFunnel(id:$id,node:$node){id}}",
           {"id": FUNNEL, "node": {"steps": [{
               "id": DST,
               "slug": dst["slug"], "title": dst["title"], "type": dst["type"],
               "settings": new_st, "visual": dst["visual"],
               "body": json.dumps(body) if isinstance(body, str) else body}]}},
           extra_headers=h)
print(f"transferred step 12 -> step 3 (slug kept: {dst['slug']}, title kept: {dst['title']!r})")
