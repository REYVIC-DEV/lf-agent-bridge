#!/usr/bin/env python3
"""One-off: rename ONLY the V2 step's slug to force a fresh storefront render
(known LF caching quirk on brand-new step URLs). Fetches V2's current
settings/body/visual first and resends them unchanged alongside the new slug,
so this is a pure rename, no content change. The `steps` array below
references ONLY the V2 step id -- the V1 step (step_ez7sidd3Dknpc-Z-4vhg0,
actively worked on in another session) is never referenced or touched.
"""
import sys, os, json
sys.path.insert(0, '.')
import lf_api

tok = open('.session_token').read().strip()
ACCT = open('.lf_account').read().strip()
HH = {"account-id": ACCT, "version": "1",
      "Origin": "https://app.lightfunnels.com", "Referer": "https://app.lightfunnels.com/"}
def gql(q, v=None): return lf_api.gql(tok, q, v, extra_headers=HH)

FUNNEL = "fun_hLmlmrbjeoGf3UZZvBEHY"
STEP = "step_1G8JSgYhh7AMR0LJgl5tV"
NEW_SLUG = "oura-vs-hlth-band-v2"

cur = gql('''query($q: String!){ funnels(first:1, query:$q){ edges { node { steps { id uid slug title type settings body visual { x y } } } } } }''',
    {"q": f"id:{FUNNEL}"})["funnels"]["edges"][0]["node"]["steps"]
v2 = next(s for s in cur if s["id"] == STEP or s["uid"] == STEP)
print("current V2 slug:", v2["slug"], "id:", v2["id"])

r = gql('''mutation($id: ID!, $node: InputFunnel!){ updateFunnel(id:$id,node:$node){ id published steps { uid slug } } }''',
    {"id": FUNNEL, "node": {"published": True,
        "steps": [{"id": v2["id"], "slug": NEW_SLUG, "title": v2["title"], "type": v2["type"],
            "settings": v2["settings"], "body": v2["body"], "visual": v2["visual"]}]}})
print(json.dumps(r, indent=2))
