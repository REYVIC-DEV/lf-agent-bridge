#!/usr/bin/env python3
"""Inventory every money figure on /article/dMs4WkOYD before tagging it.

Read-only. Writes a JSON inventory to steps/ so the tagging pass can assert a
count rather than discover a missed figure after launch.

⚠️ Never inventory by regex over json.dumps(body): ensure_ascii escapes the
pound sign to \\u00a3 and a currency regex then matches NOTHING. Walk the block
tree and read p.content as real text.

⚠️ A percent regex must run over TEXT ONLY. `\\d{1,3}%` happily matches
`width:50%` inside an inline style and would tag a star rating.
"""
import io
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", "..", "..", ".."))
sys.path.insert(0, ROOT)
os.chdir(ROOT)
import lf_api  # noqa: E402

FUNNEL = "fun_p9Y_FwGlQsaP5bpW70q5N"
STEP = "step_coYi_dsw6RtJtR111GjR8"          # /article/dMs4WkOYD
OUT = os.path.join(HERE, "..", "steps", "dMs4WkOYD.currency-inventory-2026-09-21.json")

# Money in the visible text. Kept deliberately tight:
#   - the trailing (?![\d,]) stops a match halfway through a longer number
#   - the comma group does NOT allow a trailing comma, so "£79, no subscription"
#     keeps its comma outside the match
MONEY = re.compile(r"£\s?\d{1,3}(?:,\d{3})*(?:\.\d{2})?(?![\d,])")
PCT = re.compile(r"\b\d{1,3}\s?%")
TAGGED = re.compile(r"data-(price|fx-gbp)=")


def strip_tags(html):
    """Visible text only, so inline styles cannot be mistaken for copy."""
    s = re.sub(r"<(script|style)\b[^>]*>.*?</\1>", " ", html or "", flags=re.S | re.I)
    s = re.sub(r"<[^>]+>", " ", s)
    s = (s.replace("&nbsp;", " ").replace("&amp;", "&")
          .replace("&pound;", "£").replace("&#163;", "£"))
    return re.sub(r"\s+", " ", s).strip()


def walk(node, out, path="root"):
    if isinstance(node, dict):
        t = node.get("t")
        p = node.get("p") or {}
        c = p.get("content")
        if isinstance(c, str) and c.strip():
            text = strip_tags(c)
            money = MONEY.findall(text)
            pcts = PCT.findall(text)
            if money or pcts:
                out.append({
                    "block_id": str(node.get("id", ""))[:12],
                    "type": t,
                    "path": path,
                    "money": money,
                    "pct": pcts,
                    "already_tagged": bool(TAGGED.search(c)),
                    "text": text[:220],
                    "raw_len": len(c),
                })
        for k, v in node.items():
            walk(v, out, path + "." + str(k) if k in ("c", "children") else path)
    elif isinstance(node, list):
        for i, v in enumerate(node):
            walk(v, out, path)


tok = open(".session_token").read().strip()
acct = open(".lf_account").read().strip()
h = lf_api.session_headers(acct)

node = lf_api.get_funnel_steps(tok, FUNNEL, extra_headers=h)
step = next(s for s in node["steps"] if s["uid"] == STEP)
print("step: %s | slug=%s | title=%s" % (STEP, step["slug"], step["title"]))

settings = step.get("settings") or {}
ch = settings.get("custom_html") or {}
hdr = ch.get("header") or ""
print("\ncustom_html.header: %d chars" % len(hdr))
print("  @font-face declarations : %d" % hdr.count("@font-face"))
print("  dynamic-currency marker : %s" % ("<!-- dynamic-currency -->" in hdr))
print("  mentions data-price     : %s" % ("data-price" in hdr))
print("  <script> blocks         : %d" % hdr.count("<script"))

rows = []
walk(step.get("body"), rows)

n_money = sum(len(r["money"]) for r in rows)
n_pct = sum(len(r["pct"]) for r in rows)
print("\n%d block(s) carry money or a percentage" % len(rows))
print("  GBP figures : %d" % n_money)
print("  percentages : %d" % n_pct)
print("  already tagged blocks: %d" % sum(1 for r in rows if r["already_tagged"]))

from collections import Counter  # noqa: E402
print("\n--- distinct GBP figures ---")
for val, n in Counter(m for r in rows for m in r["money"]).most_common():
    print("  %-12s x%d" % (val, n))
print("\n--- distinct percentages ---")
for val, n in Counter(p for r in rows for p in r["pct"]).most_common():
    print("  %-12s x%d" % (val, n))

print("\n--- every block, in document order ---")
for i, r in enumerate(rows, 1):
    print("\n%2d. %-10s %-12s tagged=%s" % (i, r["type"], r["block_id"], r["already_tagged"]))
    if r["money"]:
        print("    money: %s" % ", ".join(r["money"]))
    if r["pct"]:
        print("    pct  : %s" % ", ".join(r["pct"]))
    print("    text : %s" % r["text"])

os.makedirs(os.path.dirname(OUT), exist_ok=True)
with io.open(OUT, "w", encoding="utf-8") as fh:
    json.dump({"step": STEP, "slug": step["slug"],
               "header_chars": len(hdr), "font_face": hdr.count("@font-face"),
               "installed": "<!-- dynamic-currency -->" in hdr,
               "n_money": n_money, "n_pct": n_pct, "blocks": rows},
              fh, indent=2, ensure_ascii=False)
print("\nwritten: %s" % os.path.relpath(OUT, ROOT))
