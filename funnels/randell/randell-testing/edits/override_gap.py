#!/usr/bin/env python3
"""How far does each market's real Shopify price sit from its mid-market
equivalent, and what does that do to the comparison table?

Our price comes from Shopify (real, per-market, often a price-list override).
Competitor figures are converted from GBP at mid-market. Where an override is
much cheaper than the FX equivalent, the table overstates our advantage: the
rival is converted at full mid-market while we are not.
"""
import json
import urllib.request

def get(url, origin=None):
    req = urllib.request.Request(url)
    if origin:
        req.add_header("Origin", origin)
    return json.load(urllib.request.urlopen(req, timeout=30))

prices = get("https://hlthtrack.com/api/prices")
fx = get("https://app.hlthtrack.com/api/fx", "https://www.techunboxed.co")
rates = fx["rates"]

GBP_PRICE = 79.0      # our UK price, the basis of every hardcoded competitor figure
RIVAL_GBP = 229.0     # Whoop, the headline comparison in the table

rows = []
for m in prices.get("markets", []):
    cur, cc = m.get("currency"), m.get("country")
    if not m.get("available") or cur == "GBP":
        continue
    rate = rates.get(cur)
    amt = float(m["amount"])
    if not rate:
        rows.append((cc, cur, amt, None, None, None, "NO FX RATE"))
        continue
    fx_equiv = GBP_PRICE * rate          # what our price would be at mid-market
    ours_ratio = amt / fx_equiv          # <1 means the override is cheaper
    rival_local = RIVAL_GBP * rate       # what the table shows for the rival
    gap_local = rival_local / amt        # apparent multiple on the page
    gap_uk = RIVAL_GBP / GBP_PRICE       # the real UK multiple, 2.9x
    rows.append((cc, cur, amt, ours_ratio, gap_local, gap_local / gap_uk, ""))

rows.sort(key=lambda r: (r[3] is None, r[3] if r[3] is not None else 0))

print("UK reality: GBP79 vs GBP229 = %.1fx" % (RIVAL_GBP / GBP_PRICE))
print()
print("%-4s %-4s %12s %9s %12s %9s" % (
    "cc", "cur", "our price", "vs FX", "table gap", "distortion"))
print("-" * 60)
for cc, cur, amt, ratio, gap, dist, note in rows:
    if note:
        print("%-4s %-4s %12.2f  %s" % (cc, cur, amt, note))
        continue
    flag = "  <== " if dist and dist >= 1.5 else ""
    print("%-4s %-4s %12.2f %8.0f%% %11.1fx %8.1fx%s" % (
        cc, cur, amt, ratio * 100, gap, dist, flag))

bad = [r for r in rows if r[5] and r[5] >= 1.5]
print()
print("markets where the table overstates our advantage by >=1.5x: %d of %d" % (
    len(bad), len([r for r in rows if r[5]])))
if bad:
    print("  " + ", ".join("%s(%.1fx)" % (r[0], r[5]) for r in bad))
