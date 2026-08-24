#!/usr/bin/env python3
"""Tag the copied page's prices: ours from Shopify, competitors via FX.

Explicit id -> tag map, no heuristics. Two earlier scans showed why that matters:
a naive `\d{1,3}%` match hit `width:50%` inside inline STYLES on the star-rating
blocks, and `json.dumps` had escaped every `£` to \u00a3 so a currency regex
found nothing at all.

OURS (data-price, driven by hlthtrack.com/api/prices — the real Shopify price):
  d9dc0534 / 2211c87c   "£79 <s>£158</s>"  -> price + compare (desktop + mobile)
  68ceabfc / 41201986   "£79"              -> price (comparison-table cells)
  8f45ef23              inline prose       -> price + compare
  095e8bc1 / 9e1d3664   "50% OFF"          -> discount

COMPETITORS (data-fx-gbp, driven by app.hlthtrack.com/api/fx — mid-market):
  the comparison table cells and the spec bullets only. Editorial prose sums
  (the £1,581 test spend, "a £399 watch", "£349") are deliberately LEFT in GBP:
  they are the cost of our own test and rhetorical asides, not figures a shopper
  compares, and converting a sum of past purchases reads as nonsense.
  £0 cells are skipped — they mean "none", not a price.
"""
import json, re, sys
sys.path.insert(0, ".")
import lf_api

FUNNEL = "fun_f1IsXx3YnEA2UD2g91dAv"
STEP = "step_JM0a30ybnkm3hpOE7-lSW"

# ours: block id -> list of (find, tag)
OURS = {
    "d9dc0534": [("£79", "price"), ("£158", "compare")],
    "2211c87c": [("£79", "price"), ("£158", "compare")],
    "68ceabfc": [("£79", "price")],
    "41201986": [("£79", "price")],
    "8f45ef23": [("£79", "price"), ("£158", "compare")],
    "095e8bc1": [("50%", "discount")],
    "9e1d3664": [("50%", "discount")],
}
# competitors: block id -> list of GBP figures to convert, in order of appearance
COMP = {
    "27ecab49": ["229"], "eb292aa7": ["229"],
    "0415a24b": ["359"], "be07c909": ["359"],
    "07519a75": ["229"], "7c36c746": ["229"],
    "14257eb8": ["219"], "01067a56": ["219"],
    "69408cc6": ["250"], "f5dd3381": ["250"],
    "6c24db1e": ["269"], "50f29095": ["269"],
    "ed6c29b3": ["9.99"], "80db826a": ["9.99"],
    "3f05179c": ["79.99", "139.99"], "e91a944b": ["79.99", "139.99"],
    "e293eba2": ["229"], "754c6563": ["229"], "75f26ff7": ["458"],
    "85c2bfcc": ["219"], "7d52236b": ["219"],
    "d03645b9": ["260"], "13dbf8c1": ["120"], "8c08bf95": ["380"],
    "8d5167d6": ["250"], "d3a84181": ["250"],
}

tok = open(".session_token").read().strip()
acct = open(".lf_account").read().strip()
h = lf_api.session_headers(acct)
node = lf_api.get_funnel_steps(tok, FUNNEL, extra_headers=h)
s = {x["uid"]: x for x in node["steps"]}[STEP]
was = isinstance(s["body"], str)
body = json.loads(s["body"]) if was else s["body"]

done_ours, done_comp, missed = [], [], []

def tag_ours(c, bid):
    for find, tag in OURS[bid]:
        if 'data-price="%s"' % tag in c:
            continue
        # £158 already sits in its own styled <span>: put the attribute on it
        m = re.search(r'<span (style="[^"]*")>(' + re.escape(find) + r')</span>', c)
        if m:
            c = c.replace(m.group(0),
                          '<span data-price="%s" %s>%s</span>' % (tag, m.group(1), find), 1)
        else:
            if find not in c:
                missed.append((bid, find)); continue
            c = c.replace(find, '<span data-price="%s">%s</span>' % (tag, find), 1)
        done_ours.append((bid, tag))
    return c

def tag_comp(c, bid):
    for gbp in COMP[bid]:
        lit = "£" + gbp
        if 'data-fx-gbp="%s"' % gbp in c:
            continue
        if lit not in c:
            missed.append((bid, lit)); continue
        c = c.replace(lit, '<span data-fx-gbp="%s">%s</span>' % (gbp, lit), 1)
        done_comp.append((bid, gbp))
    return c

def walk(x):
    if isinstance(x, dict):
        bid = str(x.get("id", ""))[:8]
        p = x.get("p") or {}
        c = p.get("content")
        if isinstance(c, str):
            if bid in OURS:
                p["content"] = tag_ours(c, bid)
            elif bid in COMP:
                p["content"] = tag_comp(c, bid)
        for v in x.values():
            walk(v)
    elif isinstance(x, list):
        for v in x:
            walk(v)

walk(body)
print("ours tagged  :", len(done_ours), dict((t, sum(1 for _, x in done_ours if x == t))
                                            for t in ("price", "compare", "discount")))
print("comps tagged :", len(done_comp))
assert not missed, "figures not found: %s" % missed
assert len(done_ours) == 10, done_ours   # 2+2+1+1+2+1+1
assert len(done_comp) == 28, len(done_comp)

lf_api.gql(tok, "mutation($id:ID!,$node:InputFunnel!){updateFunnel(id:$id,node:$node){id}}",
           {"id": FUNNEL, "node": {"steps": [{
               "id": STEP, "slug": s["slug"], "title": s["title"], "type": s["type"],
               "settings": s["settings"], "visual": s["visual"],
               "body": json.dumps(body) if was else body}]}}, extra_headers=h)
print("write ok")
