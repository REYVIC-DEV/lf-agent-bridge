#!/usr/bin/env python3
"""Tag the 14 remaining money figures. User: "all currency lets convert".

Positional, not find/replace: three of these blocks hold TWO figures that need
DIFFERENT feeds (the H1 carries the GBP1,581 test spend AND our GBP79), so a
substring replace would tag the wrong one. Matches are rewritten right-to-left
so earlier offsets stay valid.

The regex deliberately excludes a trailing comma. An earlier scan reported the
figure in "GBP79, no subscription" as "GBP79," because [\\d,]+ swallowed it, and
tagging that span would have put the comma inside the replaced text - so the
comma would vanish the moment a price was written in.

GBP0 subscription cells are converted too, not skipped. Left alone they would
read "EUR79 / GBP0 / EUR79" across one table row, which looks like a bug. The
fmt() guard that refuses <= 0 stays in force for data-price, where a zero really
would render a free product; it is only relaxed for data-fx-gbp, where 0 is a
stated "no subscription" rather than a fetched price.
"""
import json, re, sys
sys.path.insert(0, ".")
import lf_api

FUNNEL = "fun_f1IsXx3YnEA2UD2g91dAv"
STEP = "step_JM0a30ybnkm3hpOE7-lSW"
P = "£"
MONEY = re.compile(P + r"\d{1,3}(?:,\d{3})*(?:\.\d{2})?")

# block id -> tag per figure, IN DOCUMENT ORDER within that block.
# "price"/"compare" = ours (Shopify). "fx" = converted from GBP (indicative).
PLAN = {
    "bb0b6f5f": ["fx", "price"],    # H1: "We Spent GBP1,581 ... The GBP79 Outsider Won."
    "d38022a8": ["fx", "price"],    # sub: "a GBP399 watch can't, costs GBP79 on sale"
    "d273aa4d": ["fx"],             # the GBP1,581 test spend again
    "80ba0401": ["price"],          # "The GBP79 newcomer beat every big name"
    "a3c5b8a3": ["fx", "price"],    # "GBP229-per-year membership" ... "GBP79, no ..."
    "a19f501e": ["fx"],             # GBP349 competitor tier
    "ee53f086": ["price"],          # "a GBP79 price tag"
    "49939732": ["price"],          # review prose
    "550332de": ["fx"],             # GBP0 subscription cell
    "3b0379b7": ["fx"],
    "c6800237": ["fx"],
}

tok = open(".session_token").read().strip()
acct = open(".lf_account").read().strip()
h = lf_api.session_headers(acct)
node = lf_api.get_funnel_steps(tok, FUNNEL, extra_headers=h)
s = {x["uid"]: x for x in node["steps"]}[STEP]
was = isinstance(s["body"], str)
body = json.loads(s["body"]) if was else s["body"]

seen, applied = set(), []


def retag(c, bid):
    tags = PLAN[bid]
    ms = list(MONEY.finditer(c))
    assert len(ms) == len(tags), "%s: %d figures but %d tags: %s" % (
        bid, len(ms), len(tags), [m.group(0) for m in ms])
    assert "data-price=" not in c and "data-fx-gbp" not in c, bid + " already tagged"
    for m, tag in reversed(list(zip(ms, tags))):
        lit = m.group(0)
        if tag == "fx":
            gbp = lit.replace(P, "").replace(",", "")
            attr = 'data-fx-gbp="%s"' % gbp
        else:
            attr = 'data-price="%s"' % tag
        c = c[:m.start()] + '<span %s>%s</span>' % (attr, lit) + c[m.end():]
        applied.append((bid, lit, tag))
    return c


def walk(x):
    if isinstance(x, dict):
        bid = str(x.get("id", ""))[:8]
        p = x.get("p") or {}
        c = p.get("content")
        if isinstance(c, str) and bid in PLAN and bid not in seen:
            seen.add(bid)
            p["content"] = retag(c, bid)
        for v in x.values():
            walk(v)
    elif isinstance(x, list):
        for v in x:
            walk(v)


walk(body)
missing = set(PLAN) - seen
assert not missing, "blocks not found: %s" % missing
assert len(applied) == 14, applied

from collections import Counter
print("newly tagged:", dict(Counter(t for _, _, t in applied)))
raw = json.dumps(body)
print("totals now  : price=%d compare=%d fx=%d" % (
    raw.count('data-price=\\"price\\"') + raw.count('data-price="price"'),
    raw.count('data-price=\\"compare\\"') + raw.count('data-price="compare"'),
    raw.count("data-fx-gbp")))

lf_api.gql(tok, "mutation($id:ID!,$node:InputFunnel!){updateFunnel(id:$id,node:$node){id}}",
           {"id": FUNNEL, "node": {"steps": [{
               "id": STEP, "slug": s["slug"], "title": s["title"], "type": s["type"],
               "settings": s["settings"], "visual": s["visual"],
               "body": json.dumps(body) if was else body}]}}, extra_headers=h)
print("write ok")
