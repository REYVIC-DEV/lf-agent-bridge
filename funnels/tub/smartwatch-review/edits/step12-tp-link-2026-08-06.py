#!/usr/bin/env python3
"""Make the whole "Rated Excellent (4.5) on [Trustpilot]" row a link.

Figma names that node `557:6520` "Link - Untitled link", so text *and* logo are
one link target — which also explains why "Excellent" is underlined in the frame:
it is the link affordance.

Implemented by converting the row container 71410521 to a BlockLink rather than
wrapping the text in an inline <a>: the Trustpilot logo is a sibling Image block,
so an inline anchor inside the Text could never cover it. Children and styles are
preserved, so the flex centring stays as measured (50px inset each side, 6px gap).

Target matches the page's existing Trustpilot link exactly:
`https://www.trustpilot.com/review/hlthtrack.com`, target=_blank. Note the
`hlthtrack.com` here is the review-page **slug**, not a store host — it must NOT
be rewritten to .co.uk, which is why the UK domain pass deliberately left the 6
Trustpilot occurrences alone.
"""
import json, sys
sys.path.insert(0, ".")
import lf_api

FUNNEL = "fun_vGqQYxn4H2i_traYYkh4w"
STEP = "step_0hL9bV7NUmyESdgkwY4Ih"
ROW = "71410521"
URL = "https://www.trustpilot.com/review/hlthtrack.com"

tok = open(".session_token").read().strip()
acct = open(".lf_account").read().strip()
h = lf_api.session_headers(acct)
node = lf_api.get_funnel_steps(tok, FUNNEL, extra_headers=h)
s = {x["uid"]: x for x in node["steps"]}[STEP]
was = isinstance(s["body"], str)
body = json.loads(s["body"]) if was else s["body"]

done = []

def walk(x):
    if isinstance(x, dict):
        if str(x.get("id", ""))[:8] == ROW:
            assert x.get("t") == "Container", x.get("t")
            p = x.setdefault("p", {})
            kids = [c.get("t") for c in (p.get("children") or [])]
            assert kids == ["Text", "Image"], kids
            x["t"] = "BlockLink"
            p["destination"] = {"type": "static", "value": URL}
            p["target"] = "_blank"
            done.append(kids)
        for v in x.values():
            walk(v)
    elif isinstance(x, list):
        for v in x:
            walk(v)

walk(body)
assert len(done) == 1, done
print(f"row -> BlockLink, children preserved: {done[0]}")
print(f"  destination: {URL} (target=_blank)")

lf_api.gql(tok, "mutation($id:ID!,$node:InputFunnel!){updateFunnel(id:$id,node:$node){id}}",
           {"id": FUNNEL, "node": {"steps": [{
               "id": STEP, "slug": s["slug"], "title": s["title"], "type": s["type"],
               "settings": s["settings"], "visual": s["visual"],
               "body": json.dumps(body) if was else body}]}}, extra_headers=h)
print("write ok")
