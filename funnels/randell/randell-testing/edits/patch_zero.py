#!/usr/bin/env python3
"""Let data-fx-gbp="0" render as a zero in the local currency.

fmt() refuses n <= 0 because a 0 in a PRICE renders a free product. That guard
stays exactly as it is for data-price. But a "GBP0" subscription cell is a
stated "no subscription", not a fetched price, and leaving it as GBP0 made one
table row read "EUR79 / GBP0 / EUR79" - three cells, two currencies, looks
broken. So 0 is formatted directly here rather than through fmt(), and takes no
"~": there is nothing approximate about zero.
"""
import io

p = "dynamic-currency-header-block.html"
s = open(p, encoding="utf-8").read()

old = """      gbp = parseFloat(els[i].getAttribute("data-fx-gbp"));
      if (!isFinite(gbp) || gbp <= 0) continue;
      out = fmt(Math.round(gbp * rate), cur);   // whole units: it is indicative
      // "~" on purpose. This is a MID-MARKET conversion of a rival's GBP RRP,
      // not a quote they would be charged, so it must not read as an exact
      // price. Drop the prefix only if someone decides that trade knowingly.
      if (out) els[i].textContent = "~" + out;"""

new = """      gbp = parseFloat(els[i].getAttribute("data-fx-gbp"));
      if (!isFinite(gbp) || gbp < 0) continue;
      if (gbp === 0) {
        // A "GBP0" subscription cell means "none". It still has to change
        // currency or the row reads "EUR79 / GBP0 / EUR79", and it takes no
        // "~" because there is nothing approximate about zero. Formatted
        // directly rather than through fmt(), whose <= 0 guard must stay in
        // force for data-price, where a 0 would render a free product.
        out = null;
        try {
          out = new Intl.NumberFormat(navigator.language || "en-GB",
            { style: "currency", currency: cur,
              maximumFractionDigits: 0 }).format(0);
        } catch (e) { out = null; }
        if (out) els[i].textContent = out;
        continue;
      }
      out = fmt(Math.round(gbp * rate), cur);   // whole units: it is indicative
      // "~" on purpose. This is a MID-MARKET conversion of a rival's GBP RRP,
      // not a quote they would be charged, so it must not read as an exact
      // price. Drop the prefix only if someone decides that trade knowingly.
      if (out) els[i].textContent = "~" + out;"""

assert old in s, "fx loop moved"
s = s.replace(old, new, 1)
open(p, "w", encoding="utf-8", newline="\n").write(s)
print("patched: fx now renders a zero in local currency, no tilde")
