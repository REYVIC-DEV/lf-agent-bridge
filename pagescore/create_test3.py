#!/usr/bin/env python3
"""Create the 'Test 3' funnel from scratch (session recipe) and save its ids.
Writes an empty article_page shell; build_test3.py fills the body."""
import sys, json, os, uuid
sys.path.insert(0, '.')
import lf_api

tok = open('.session_token').read().strip()
ACCT = open('.lf_account').read().strip()
HH = {"account-id": ACCT, "version": "1",
      "Origin": "https://app.lightfunnels.com", "Referer": "https://app.lightfunnels.com/"}
def sgql(q, v=None): return lf_api.gql(tok, q, v, extra_headers=HH)
def nid(): return str(uuid.uuid4())

body = {"id": nid(), "t": "Root", "version": 11,
        "styles": [{"prop": "pageWidth", "value": "960px"},
                   {"prop": "backgroundColor", "value": {"r": 255, "g": 255, "b": 255, "a": 1}}],
        "p": {"children": []}}

# 1. create empty funnel
f = sgql('mutation($node: InputCreateFunnel!){ createFunnel(node:$node){ id uid name slug steps{id} } }',
         {"node": {"name": "Test 3", "slug": "test3-smartwatch",
                   "funnel_steps": ["article_page"], "currency": "USD", "lang": "en"}})
FID = f["createFunnel"]["id"]; FSLUG = f["createFunnel"]["slug"]
print("funnel:", FID, FSLUG)

# 2. create the step (detached)
s = sgql('mutation($funnel_id: ID!, $node: InputStep!){ createStep(funnel_id:$funnel_id, node:$node){ step{ id uid slug title type } } }',
         {"funnel_id": FID, "node": {"slug": "article", "title": "Smartwatch review",
                                     "type": "article_page", "settings": {},
                                     "visual": {"x": 100, "y": 100}, "body": body}})
step = s["createStep"]["step"]; SID = step["id"]
print("step:", SID, step["uid"])

# 3. attach into the workflow so it renders
u = sgql('mutation($id: ID!, $node: InputFunnel!){ updateFunnel(id:$id, node:$node){ id starting_step_id steps{uid slug} } }',
         {"id": FID, "node": {"starting_step_id": SID,
                              "steps": [{"id": SID, "slug": "article", "title": "Smartwatch review",
                                         "type": "article_page", "settings": {},
                                         "visual": {"x": 100, "y": 100}, "body": body}]}})
print("attached:", u["updateFunnel"]["steps"])

ids = {"funnel": FID, "step": SID, "step_uid": step["uid"], "slug": FSLUG}
json.dump(ids, open("/tmp/test3_ids.json", "w"))
CACHE = os.path.join(os.path.dirname(__file__), ".cache")
os.makedirs(CACHE, exist_ok=True)
json.dump(ids, open(os.path.join(CACHE, "test3_ids.json"), "w"))
print("saved ids:", ids)
