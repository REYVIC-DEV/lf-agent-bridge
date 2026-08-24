#!/usr/bin/env python3
"""Complete inventory of every money figure on the step and its tag state.

Distinguishes data-price (ours, Shopify) / data-fx-gbp (competitor, FX) /
UNTAGGED, per figure rather than per block, so a block holding both an our-price
and a competitor price is not reported as simply "tagged".

Text only: an earlier pass matched width:50% inside inline STYLES, so the scan
strips attributes before looking for figures.
"""
import json, re, sys
sys.path.insert(0, ".")
import lf_api

FUNNEL = "fun_f1IsXx3YnEA2UD2g91dAv"
STEP = "step_JM0a30ybnkm3hpOE7-lSW"
P = "£"
MONEY = re.compile(P + r"[\d,]+(?:\.\d{2})?")

tok = open(".session_token").read().strip()
acct = open(".lf_account").read().strip()
h = lf_api.session_headers(acct)
node = lf_api.get_funnel_steps(tok, FUNNEL, extra_headers=h)
s = {x["uid"]: x for x in node["steps"]}[STEP]
body = json.loads(s["body"]) if isinstance(s["body"], str) else s["body"]

rows = []


def state_of(content, fig_start):
    """Which enclosing span, if any, wraps the figure at fig_start."""
    before = content[:fig_start]
    # nearest unclosed <span ...> before the figure
    opens = [m for m in re.finditer(r"<span\b[^>]*>", before)]
    closes = before.count("</span>")
    if len(opens) > closes:
        tagm = opens[-1].group(0)   # innermost span still open at the figure
        if 'data-price="price"' in tagm:
            return "price"
        if 'data-price="compare"' in tagm:
            return "compare"
        if 'data-price="savings"' in tagm:
            return "savings"
        if "data-fx-gbp" in tagm:
            return "fx"
    return "UNTAGGED"


def walk(x):
    if isinstance(x, dict):
        bid = str(x.get("id", ""))[:8]
        c = (x.get("p") or {}).get("content")
        if isinstance(c, str) and P in c:
            for m in MONEY.finditer(c):
                rows.append((bid, m.group(0), state_of(c, m.start())))
        for v in x.values():
            walk(v)
    elif isinstance(x, list):
        for v in x:
            walk(v)


walk(body)
from collections import Counter
print("total money figures in text:", len(rows))
print("by state:", dict(Counter(r[2] for r in rows)))
print()
print("UNTAGGED:")
for bid, fig, st in rows:
    if st == "UNTAGGED":
        print("  [%s] %s" % (bid, fig))
