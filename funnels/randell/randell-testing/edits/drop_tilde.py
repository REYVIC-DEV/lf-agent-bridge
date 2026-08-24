#!/usr/bin/env python3
"""Drop the "~" prefix from FX-converted figures. Requested by the user.

Recorded rather than silently removed, because API.md is explicit that /api/fx is
mid-market and "correct for 'about EUR89'; wrong as a promise of what the customer
will be charged". Without the prefix a converted rival RRP and the converted test
spend both read as exact figures. That is a knowing editorial trade, which is the
condition the original comment asked for.
"""
p = "dynamic-currency-header-block.html"
s = open(p, encoding="utf-8").read()

old = """      out = fmt(Math.round(gbp * rate), cur);   // whole units: it is indicative
      // "~" on purpose. This is a MID-MARKET conversion of a rival's GBP RRP,
      // not a quote they would be charged, so it must not read as an exact
      // price. Drop the prefix only if someone decides that trade knowingly.
      if (out) els[i].textContent = "~" + out;"""

new = """      out = fmt(Math.round(gbp * rate), cur);   // whole units: it is indicative
      // No "~" prefix: removed deliberately on request 2026-08-25. These are
      // still MID-MARKET conversions of GBP figures, so they are indicative and
      // will not match what a rival actually charges locally - the figure now
      // simply does not say so. Rounding to whole units is the only remaining
      // signal. Restore the prefix here if that ever needs stating again.
      if (out) els[i].textContent = out;"""

assert old in s, "fx write site moved"
s = s.replace(old, new, 1)
assert '"~" + out' not in s
open(p, "w", encoding="utf-8", newline="\n").write(s)
print("tilde removed")
