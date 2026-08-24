#!/usr/bin/env python3
"""
design_diff.py -- is the built page actually 1:1 with the Figma design?

"Looks right" is not a QA result. This measures the two things a machine can
decide about fidelity, so the agent only has to judge what is genuinely visual:

  1. COPY   every TEXT node in the Figma frame must appear on the live page,
            verbatim -- same punctuation, same currency symbols, same casing.
            Missing copy and invented copy are the two most common build defects
            and neither is visible in a screenshot comparison.

  2. TYPE   for every line of copy that matched, the live element's computed
            font-size / weight / colour must equal the Figma node's. This is the
            "measure, don't guess" rule from figma-inspect.md, enforced after
            the fact instead of trusted.

Input is whatever JSON figwright already gave you -- `get_node`, `get_design_context`
or `scan_text_nodes` output, saved to a file. The walker finds TEXT nodes anywhere
in the tree, so you do not have to reshape it first.

  python3 pagescore/design_diff.py <figma.json> <live-url>
  python3 pagescore/design_diff.py <figma.json> <live-url> --viewport 390 --mobile
  python3 pagescore/design_diff.py <figma.json> <live-url> --out pagescore/runs/<id>

Writes design_diff.json + design_diff.md next to the run. Exits non-zero if any
copy is missing, so it can gate a pipeline step.
"""
import argparse
import difflib
import json
import os
import re
import sys
import unicodedata

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)

UA = ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/125.0 Safari/537.36")

# How close two strings must be before we call it "the same line, retyped".
FUZZY = 0.86
# Tolerances. Font size is authored in px and should match exactly; allow 1px for
# rounding between Figma's float and the browser's computed value.
SIZE_TOL_PX = 1.0
WEIGHT_TOL = 0          # a 700 authored as 600 is a real defect, not a rounding one


def norm(s):
    """Normalise for comparison only -- never for reporting. Reported strings stay
    verbatim so a £/– /— mismatch is still visible in the output."""
    s = unicodedata.normalize("NFKC", s or "")
    s = s.replace("’", "'").replace("‘", "'")
    s = s.replace("“", '"').replace("”", '"')
    s = re.sub(r"\s+", " ", s)
    return s.strip().lower()


def hexcolor(fill):
    c = (fill or {}).get("color") or {}
    if not c:
        return None
    return "#%02x%02x%02x" % tuple(
        max(0, min(255, round(c.get(k, 0) * 255))) for k in ("r", "g", "b"))


def walk_text_nodes(node, out, path=""):
    """Pull every TEXT node out of any Figma-shaped JSON, however it was produced."""
    if isinstance(node, list):
        for n in node:
            walk_text_nodes(n, out, path)
        return
    if not isinstance(node, dict):
        return
    name = node.get("name") or ""
    here = f"{path}/{name}" if name else path
    chars = node.get("characters")
    if isinstance(chars, str) and chars.strip():
        st = node.get("style") or {}
        fills = node.get("fills") or []
        solid = next((f for f in fills
                      if isinstance(f, dict)
                      and f.get("type") == "SOLID" and f.get("visible", True)), None)
        box = node.get("absoluteBoundingBox") or {}
        out.append({
            "id": node.get("id"), "path": here.lstrip("/"),
            "chars": chars,
            "font_size": st.get("fontSize"),
            "font_weight": st.get("fontWeight"),
            "line_height": st.get("lineHeightPx"),
            "align": st.get("textAlignHorizontal"),
            "color": hexcolor(solid),
            "y": box.get("y"), "x": box.get("x"),
            "w": box.get("width"), "h": box.get("height"),
        })
    for k in ("children", "nodes", "document", "root"):
        v = node.get(k)
        if isinstance(v, (list, dict)):
            walk_text_nodes(v, out, here)
    # get_nodes-style envelopes: {"<id>": {"document": {...}}}
    for k, v in node.items():
        if k in ("children", "nodes", "document", "root"):
            continue
        if isinstance(v, dict) and ("document" in v or "characters" in v
                                   or "children" in v):
            walk_text_nodes(v, out, here)


LIVE_JS = r"""
() => {
  const out = [];
  const skip = new Set(['SCRIPT','STYLE','NOSCRIPT','SVG','PATH']);
  const walk = el => {
    if (skip.has(el.tagName)) return;
    for (const n of el.childNodes) {
      if (n.nodeType === 3 && n.textContent.trim()) {
        const cs = getComputedStyle(el);
        const r = el.getBoundingClientRect();
        out.push({
          text: n.textContent.trim(),
          tag: el.tagName.toLowerCase(),
          font_size: parseFloat(cs.fontSize),
          font_weight: parseInt(cs.fontWeight, 10),
          line_height: parseFloat(cs.lineHeight) || null,
          color: cs.color,
          align: cs.textAlign,
          family: cs.fontFamily,
          y: Math.round(r.top + window.scrollY),
          x: Math.round(r.left),
          w: Math.round(r.width)
        });
      } else if (n.nodeType === 1) walk(n);
    }
  };
  walk(document.body);
  // LF splits a single design line across inline <b>/<span> runs, so a verbatim
  // Figma line often has no single matching text node. Emit each block element's
  // aggregate innerText as a second candidate so intact copy is not reported as
  // retyped just because the DOM chopped it up.
  const blocks = [];
  for (const el of document.querySelectorAll(
        'p,h1,h2,h3,h4,h5,h6,li,td,th,a,button,figcaption,blockquote,div')) {
    if (skip.has(el.tagName)) continue;
    const t = (el.innerText || '').trim();
    if (!t || t.length > 2000) continue;
    if (el.children.length === 0 && !t.includes('\n')) continue;   // leaf runs are already covered
    const cs = getComputedStyle(el), r = el.getBoundingClientRect();
    blocks.push({
      text: t, tag: el.tagName.toLowerCase(), aggregate: true,
      font_size: parseFloat(cs.fontSize),
      font_weight: parseInt(cs.fontWeight, 10),
      line_height: parseFloat(cs.lineHeight) || null,
      color: cs.color, align: cs.textAlign, family: cs.fontFamily,
      y: Math.round(r.top + window.scrollY), x: Math.round(r.left),
      w: Math.round(r.width)
    });
  }
  return out.concat(blocks);
}
"""


def rgb_to_hex(c):
    m = re.match(r"rgba?\(([\d.]+),\s*([\d.]+),\s*([\d.]+)", c or "")
    if not m:
        return None
    return "#%02x%02x%02x" % tuple(round(float(m.group(i))) for i in (1, 2, 3))


def read_live(url, viewport, mobile):
    from playwright.sync_api import sync_playwright
    with sync_playwright() as pw:
        b = pw.chromium.launch()
        ctx = b.new_context(viewport={"width": viewport, "height": 900},
                            device_scale_factor=2 if mobile else 1,
                            is_mobile=mobile, has_touch=mobile, user_agent=UA)
        pg = ctx.new_page()
        try:
            pg.goto(url, wait_until="networkidle", timeout=90_000)
        except Exception:
            pg.goto(url, wait_until="domcontentloaded", timeout=90_000)
        pg.wait_for_timeout(2500)
        pg.evaluate("() => new Promise(r => {let y=0;const t=setInterval(()=>{"
                    "window.scrollBy(0,900);y+=900;"
                    "if(y>document.body.scrollHeight){clearInterval(t);"
                    "window.scrollTo(0,0);r();}},60);})")
        pg.wait_for_timeout(1000)
        live = pg.evaluate(LIVE_JS)
        b.close()
    for l in live:
        l["color_hex"] = rgb_to_hex(l["color"])
    return live


def match(figma_nodes, live_nodes):
    """Match each Figma line to a live line: exact first, then closest fuzzy."""
    pool = {}
    for i, l in enumerate(live_nodes):
        pool.setdefault(norm(l["text"]), []).append(i)
    used, rows = set(), []
    live_keys = list(pool.keys())

    for f in figma_nodes:
        # A Figma text node can hold several visual lines; compare per line.
        for line in [x for x in (f["chars"] or "").split("\n") if x.strip()]:
            key = norm(line)
            idx, how, score = None, None, 1.0
            for cand in pool.get(key, []):
                if cand not in used:
                    idx, how = cand, "exact"
                    break
            if idx is None:
                near = difflib.get_close_matches(key, live_keys, n=3, cutoff=FUZZY)
                for nk in near:
                    for cand in pool.get(nk, []):
                        if cand not in used:
                            idx, how = cand, "fuzzy"
                            score = difflib.SequenceMatcher(None, key, nk).ratio()
                            break
                    if idx is not None:
                        break
            contained = None
            if idx is None:
                # LF splits one long design paragraph across many inline runs, so
                # neither a leaf run nor an under-300-char aggregate can equal it.
                # Verbatim copy is still verifiable: the normalised design line
                # must appear as an exact substring of a block's full innerText.
                # (Exact containment only -- retyped copy still fails this.)
                for l in live_nodes:
                    if l.get("aggregate") and key and key in norm(l["text"]):
                        contained = l
                        break
            row = {"figma": line, "figma_id": f["id"], "path": f["path"],
                   "font_size": f["font_size"], "font_weight": f["font_weight"],
                   "color": f["color"], "match": how, "score": round(score, 3)}
            if idx is None and contained is not None:
                row["match"] = "contained"
                row["live"] = contained["text"][:120]
                row["tag"] = contained["tag"]
                row["status"] = "OK"
            elif idx is None:
                row["status"] = "MISSING"
            else:
                used.add(idx)
                l = live_nodes[idx]
                row["live"] = l["text"]
                row["live_font_size"] = l["font_size"]
                row["live_font_weight"] = l["font_weight"]
                row["live_color"] = l["color_hex"]
                row["tag"] = l["tag"]
                deltas = []
                if f["font_size"] and l["font_size"] and \
                        abs(f["font_size"] - l["font_size"]) > SIZE_TOL_PX:
                    deltas.append(f"size {f['font_size']:g} -> {l['font_size']:g}")
                if f["font_weight"] and l["font_weight"] and \
                        abs(f["font_weight"] - l["font_weight"]) > WEIGHT_TOL:
                    deltas.append(f"weight {f['font_weight']} -> {l['font_weight']}")
                if f["color"] and l["color_hex"] and f["color"] != l["color_hex"]:
                    deltas.append(f"colour {f['color']} -> {l['color_hex']}")
                row["deltas"] = deltas
                row["status"] = ("RETYPED" if how == "fuzzy"
                                 else ("RESTYLED" if deltas else "OK"))
            rows.append(row)

    extra = [live_nodes[i]["text"] for i in range(len(live_nodes))
             if i not in used and not live_nodes[i].get("aggregate")]
    return rows, extra


def render(rows, extra, url, spec_path, viewport):
    miss = [r for r in rows if r["status"] == "MISSING"]
    retyped = [r for r in rows if r["status"] == "RETYPED"]
    restyled = [r for r in rows if r["status"] == "RESTYLED"]
    ok = [r for r in rows if r["status"] == "OK"]
    L = ["# Design fidelity -- Figma vs live", "",
         f"- Design: `{spec_path}`", f"- Live: {url} @ {viewport}px",
         f"- {len(ok)} exact, {len(restyled)} restyled, {len(retyped)} retyped, "
         f"{len(miss)} missing, {len(extra)} on the page but not in the design.", ""]
    if miss:
        L += ["## Copy in the design that is not on the page", "",
              "| Figma text | Node | Where |", "|---|---|---|"]
        L += [f"| {r['figma'][:80]} | `{r['figma_id']}` | {r['path'][:50]} |"
              for r in miss] + [""]
    if retyped:
        L += ["## Copy that was retyped, not copied", "",
              "| Design says | Page says | Similarity |", "|---|---|---|"]
        L += [f"| {r['figma'][:60]} | {r.get('live','')[:60]} | {r['score']} |"
              for r in retyped] + [""]
    if restyled:
        L += ["## Typography that does not match the node", "",
              "| Text | Difference |", "|---|---|"]
        L += [f"| {r['figma'][:55]} | {'; '.join(r['deltas'])} |"
              for r in restyled] + [""]
    if extra:
        L += ["## On the page but not in the design", "",
              "Site chrome, legal text and disclaimers legitimately live here.",
              "Anything else is invented copy and needs a decision.", ""]
        L += [f"- {t[:100]}" for t in extra[:60]] + [""]
    return "\n".join(L)


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("spec", help="figwright JSON dump of the design frame")
    ap.add_argument("url", help="the live page to compare it against")
    ap.add_argument("--viewport", type=int, default=1440)
    ap.add_argument("--mobile", action="store_true")
    ap.add_argument("--out", default=None, help="directory for the two output files")
    args = ap.parse_args()

    spec = json.load(open(args.spec))
    figma = []
    walk_text_nodes(spec, figma)
    if not figma:
        sys.exit(f"no TEXT nodes found in {args.spec} -- is this a figwright dump?")
    print(f"{len(figma)} text node(s) in the design")

    live = read_live(args.url, args.viewport, args.mobile)
    print(f"{len(live)} text run(s) on the live page")

    rows, extra = match(figma, live)
    out_dir = args.out or os.path.join(HERE, "runs", "design-diff")
    os.makedirs(out_dir, exist_ok=True)
    payload = {"spec": args.spec, "url": args.url, "viewport": args.viewport,
               "rows": rows, "extra_on_page": extra,
               "summary": {s: len([r for r in rows if r["status"] == s])
                           for s in ("OK", "RESTYLED", "RETYPED", "MISSING")}}
    with open(os.path.join(out_dir, "design_diff.json"), "w") as f:
        json.dump(payload, f, indent=2)
    md = render(rows, extra, args.url, args.spec, args.viewport)
    with open(os.path.join(out_dir, "design_diff.md"), "w") as f:
        f.write(md)
    print(json.dumps(payload["summary"]))
    print("->", os.path.relpath(out_dir, ROOT))
    sys.exit(1 if payload["summary"]["MISSING"] else 0)


if __name__ == "__main__":
    main()
