#!/usr/bin/env python3
"""Move the step-3/11-specific perf CSS out of funnel header_scripts into each
step's own settings.custom_html.header, and drop the two inert blocks.

Why: header_scripts is FUNNEL-level, so it applied to all 12 steps — 10 of which
are separate live advertorials that were explicitly out of scope. Verified they
were unharmed (step 7 rendered identically, 0 console errors), but the blast
radius was wrong and shouldn't be left that way.

Placement verified before moving: settings.custom_html.header renders inside
<head> (the pre-existing .read-more-content style from it sits at char 30153,
with </head> at 440153). That matters — if it landed in <body> this would
reintroduce the full-document style recalc that cost 2,703ms of styleLayout.

MOVED to step level (only steps 3 and 11 reference these):
  - the six `Inter` @font-face declarations
  - the metric-matched `InterFallback` @font-face
  - the block CSS (#tub-hero-img/#tub-sec1-img/#tub-sec2-img/#tub-offer-vid)

DROPPED entirely, both proven inert:
  - font preloads — stripped before reaching Lighthouse; real users already get
    these same-origin
  - preconnects to fonts.googleapis.com / fonts.gstatic.com — stripped by
    Cloudflare Fonts, never present in the served HTML

KEPT funnel-level (genuinely shared): GTM, PostHog, aimerce, the desktop-only
Lenis loader — everything from the GTM comment onward.

Steps 3 and 11 already have a custom_html.header (.read-more-content styles) and
a footer, so this APPENDS and preserves both.
"""
import json, sys
sys.path.insert(0, ".")
import lf_api

FUNNEL = "fun_vGqQYxn4H2i_traYYkh4w"
STEPS = {3: "step_-42yvjxEYUC-1yAzL9TKy", 11: "step_HFrpGxiibhudWV1YLEMs1"}
SP = sys.argv[1]
MODE = sys.argv[2]  # "steps" then "funnel"

hs_before = open(SP + "/hs-before-split.html", encoding="utf-8").read()
STEP_BLOCK = hs_before[819:4782]
assert STEP_BLOCK.lstrip().startswith("<!-- PERF: OWN INTER FACES")
assert "#tub-hero-img" in STEP_BLOCK and "InterFallback" in STEP_BLOCK
assert 'rel="preload"' not in STEP_BLOCK and "preconnect" not in STEP_BLOCK
GTM_AT = hs_before.find("<!-- Google Tag Manager")
assert GTM_AT == 5861, GTM_AT
FUNNEL_KEEP = hs_before[GTM_AT:]

tok = open(".session_token").read().strip()
acct = open(".lf_account").read().strip()
h = lf_api.session_headers(acct)
node = lf_api.get_funnel_steps(tok, FUNNEL, extra_headers=h)
by = {s["uid"]: s for s in node["steps"]}
# Do NOT assert a step COUNT: this funnel is shared, and a colleague added
# step 12 "TECHUNBOXED-UK-V4 (randell-build)" mid-session. Assert instead that
# the steps we intend to touch still exist — updateFunnel is a partial update,
# so unlisted siblings (including new ones) are preserved by omission.
for _i, _u in STEPS.items():
    assert _u in by, f"step {_i} ({_u}) not found in funnel"
print(f"funnel has {len(node['steps'])} steps; targeting {sorted(STEPS)}")

if MODE == "steps":
    payload = []
    for idx, uid in STEPS.items():
        s = by[uid]
        st = s["settings"]
        st = json.loads(st) if isinstance(st, str) else dict(st or {})
        ch = dict(st.get("custom_html") or {})
        existing = ch.get("header") or ""
        if "#tub-hero-img" in existing:
            print(f"step {idx}: already has the block — skipping")
            continue
        ch["header"] = existing.rstrip() + "\n\n" + STEP_BLOCK
        st["custom_html"] = ch
        print(f"step {idx}: header {len(existing)} -> {len(ch['header'])} chars, "
              f"footer preserved={'footer' in ch}")
        b = s["body"]
        payload.append({"id": uid, "slug": s["slug"], "title": s["title"],
                        "type": s["type"], "settings": st, "visual": s["visual"],
                        "body": json.dumps(b) if isinstance(b, str) else b})
    if payload:
        lf_api.gql(tok, "mutation($id:ID!,$node:InputFunnel!){updateFunnel(id:$id,node:$node){id}}",
                   {"id": FUNNEL, "node": {"steps": payload}}, extra_headers=h)
        print("steps written")

elif MODE == "funnel":
    q = """query($q:String!){funnels(first:1,query:$q){edges{node{header_scripts}}}}"""
    cur = lf_api.gql(tok, q, {"q": f"id:{FUNNEL}"},
                     extra_headers=h)["funnels"]["edges"][0]["node"]["header_scripts"]
    # only strip if the step-level copies are already in place
    for idx, uid in STEPS.items():
        st = by[uid]["settings"]
        st = json.loads(st) if isinstance(st, str) else (st or {})
        hdr = ((st.get("custom_html") or {}).get("header") or "")
        assert "#tub-hero-img" in hdr and "InterFallback" in hdr, \
            f"step {idx} is missing the step-level block — refusing to strip the funnel copy"
    lf_api.gql(tok, "mutation($id:ID!,$node:InputFunnel!){updateFunnel(id:$id,node:$node){id}}",
               {"id": FUNNEL, "node": {"header_scripts": FUNNEL_KEEP}}, extra_headers=h)
    print(f"funnel header_scripts {len(cur)} -> {len(FUNNEL_KEEP)} chars")
    for k in ("#tub-hero-img", "InterFallback", 'rel="preload"', "preconnect",
              "googletagmanager", "_lenisMain"):
        print(f"   {'still present' if k in FUNNEL_KEEP else 'removed      '}  {k}")
