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
import io
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


DECORATIVE_GLYPHS = set("★☆✓✔✕✖→←↑↓•·▪▸●○◆◇♦✦✧＋+-—–|/\\")


def is_decorative(chars):
    """True for a node that is a symbol, not copy."""
    t = (chars or "").strip()
    return bool(t) and len(t) <= 2 and all(c in DECORATIVE_GLYPHS for c in t)


# Figma names a weight; CSS numbers it.
FIGMA_WEIGHTS = {
    "thin": 100, "extralight": 200, "ultralight": 200, "light": 300,
    "regular": 400, "normal": 400, "book": 400, "medium": 500,
    "semibold": 600, "demibold": 600, "bold": 700, "extrabold": 800,
    "ultrabold": 800, "black": 900, "heavy": 900,
}


def dget(v, k, default=None):
    """figwright returns the string "MIXED" where a node mixes values."""
    return v.get(k, default) if isinstance(v, dict) else default


def weight_of(style_name):
    """`Poppins SemiBold Italic` -> 600. None when the node mixes styles."""
    if not isinstance(style_name, str):
        return None
    s = style_name.lower().replace(" ", "").replace("-", "").replace("italic", "")
    return FIGMA_WEIGHTS.get(s)


def family_matches(figma_family, css_family):
    """True when the browser resolved the family the design asked for.

    The live value is a whole stack (`Delight, Poppins, sans-serif`); only the first
    entry is what actually renders, and that is the one the design names. This is the
    check that catches a heading built with the wrong brand face -- invisible to a
    size/weight/colour comparison because those can all be right while the typeface
    is wrong.
    """
    if not figma_family or not css_family:
        return True
    first = css_family.split(",")[0].strip().strip('"\'').lower()
    want = figma_family.strip().lower()
    # next/font emits hashed aliases like `__Poppins_e8ce9c`; match on the stem.
    return want in first or first in want or want.replace(" ", "") in first.replace(" ", "")


def solid_fill(node):
    for fl in (node.get("fills") or []):
        if isinstance(fl, dict) and fl.get("type") == "SOLID" and fl.get("visible", True):
            return fl
    return None


def enclosing_box(ancestors):
    """The nearest painted box around a text node -- the chip, card or button it sits in.

    A design's geometry is mostly expressed on these: the pill behind a label, the
    dashed card behind the offer, the rule down the side of a pull quote. Anchoring to
    "the nearest ancestor with a fill or a stroke" gives a box that can be found the
    same way in the DOM, without trying to align two trees that do not correspond.
    """
    for a in reversed(ancestors):
        fill, stroke = solid_fill(a), (a.get("strokes") or [])
        if not fill and not stroke:
            continue
        sw = a.get("strokeWeight")
        if not isinstance(sw, (int, float)):
            # A one-sided rule -- the bar down a pull quote -- reports strokeWeight
            # "mixed" and puts the real number in strokeWeights.
            per_side = a.get("strokeWeights")
            if isinstance(per_side, dict):
                vals = [v for v in per_side.values() if isinstance(v, (int, float)) and v]
                sw = max(vals) if vals else None
        r = a.get("cornerRadius")
        return {
            "id": a.get("id"), "name": a.get("name"),
            "bg": hexcolor(fill) if fill else None,
            "radius": r if isinstance(r, (int, float)) else None,
            "border": (round(float(sw), 1) if isinstance(sw, (int, float)) and stroke
                       else (0 if not stroke else None)),
            "border_color": hexcolor(stroke[0]) if stroke and isinstance(stroke[0], dict)
            else None,
        }
    return None


def absolute_y(node, origin_y):
    """Figma dumps disagree on whether y is absolute.

    The REST/`get_design_context` shape carries `absoluteBoundingBox`, which already is.
    figwright's `get_node` reports x/y relative to the parent, so a Photo inside a
    Figure and a Product panel inside a card both report y=0. Anything that compares
    positions across nesting levels has to accumulate, or it is comparing two different
    coordinate systems and quietly getting nonsense.
    """
    box = node.get("absoluteBoundingBox")
    if isinstance(box, dict) and box.get("y") is not None:
        return float(box["y"])
    return float(origin_y) + float(node.get("y") or 0)


def walk_text_nodes(node, out, path="", ancestors=None, sibling_index=None,
                    origin_y=0.0, containers=None):
    """Pull every TEXT node out of any Figma-shaped JSON, however it was produced."""
    ancestors = ancestors or []
    if isinstance(node, list):
        for i, n in enumerate(node):
            walk_text_nodes(n, out, path, ancestors, i, origin_y, containers)
        return
    if not isinstance(node, dict):
        return
    name = node.get("name") or ""
    here = f"{path}/{name}" if name else path
    chars = node.get("characters")
    if isinstance(chars, str) and chars.strip() and is_decorative(chars):
        out.append({"id": node.get("id"), "path": here.lstrip("/"),
                    "chars": chars, "decorative": True})
    elif isinstance(chars, str) and chars.strip():
        # Two dump shapes reach this walker and they nest typography differently.
        # `get_design_context` / the REST export put it under `style`; figwright's
        # `get_node` puts it at the top level with `fontName` as a {family,style} pair.
        # Reading only the first shape silently left font_size None on a figwright
        # dump, which made every size/weight comparison below a no-op -- a judge that
        # returned PASS because it had nothing to compare.
        st = node.get("style") or {}
        fills = node.get("fills") or []
        solid = next((f for f in fills
                      if isinstance(f, dict)
                      and f.get("type") == "SOLID" and f.get("visible", True)), None)
        box = node.get("absoluteBoundingBox") or {}
        fname = node.get("fontName")
        family = st.get("fontFamily") or dget(fname, "family")
        weight = st.get("fontWeight")
        if weight is None:
            weight = weight_of(dget(fname, "style"))
        lh = st.get("lineHeightPx")
        if lh is None:
            lh = dget(node.get("lineHeight"), "value")
        out.append({
            "id": node.get("id"), "path": here.lstrip("/"),
            "chars": chars,
            "font_size": st.get("fontSize") or node.get("fontSize"),
            "font_weight": weight,
            "family": family,
            "line_height": lh,
            "align": st.get("textAlignHorizontal") or node.get("textAlignHorizontal"),
            "color": hexcolor(solid),
            "y": box.get("y", node.get("y")), "x": box.get("x", node.get("x")),
            "w": box.get("width", node.get("width")),
            "h": box.get("height", node.get("height")),
            # Geometry anchors. `sizing_h` matters because only a FILL/STRETCH node's
            # width is decided by its container -- a HUG node's width is decided by the
            # glyphs, so comparing it would just be measuring font rasterisation.
            "sizing_h": node.get("layoutSizingHorizontal"),
            "parent_id": (ancestors[-1].get("id") if ancestors else None),
            "sibling_index": sibling_index,
            "abs_y": absolute_y(node, origin_y),
            "ancestor_ids": [a.get("id") for a in ancestors if a.get("id")],
            "box": enclosing_box(ancestors),
        })
    kids = ancestors + [node] if node.get("id") else ancestors
    my_y = absolute_y(node, origin_y) if node.get("id") else origin_y
    if containers is not None and node.get("id") and node.get("children"):
        containers[node["id"]] = {
            "id": node["id"], "name": node.get("name"), "path": here.lstrip("/"),
            "abs_y": my_y, "h": node.get("height"),
            "parent_id": (ancestors[-1].get("id") if ancestors else None),
            "sibling_index": sibling_index,
            "dir": (node.get("layout") or {}).get("mode"),
        }
    for k in ("children", "nodes", "document", "root", "node"):
        v = node.get(k)
        if isinstance(v, (list, dict)):
            walk_text_nodes(v, out, here, kids, None, my_y, containers)
    # get_nodes-style envelopes: {"<id>": {"document": {...}}}
    for k, v in node.items():
        if k in ("children", "nodes", "document", "root", "node"):
            continue
        if isinstance(v, dict) and ("document" in v or "characters" in v
                                   or "children" in v):
            walk_text_nodes(v, out, here, kids, None, my_y, containers)


LIVE_JS = r"""
() => {
  const out = [];
  const skip = new Set(['SCRIPT','STYLE','NOSCRIPT','SVG','PATH']);
  // Decorative glyphs are not copy. A tick in a bullet or a star in a rating strip is
  // aria-hidden precisely because the text beside it carries the meaning -- counting
  // it makes verbatim copy look retyped.
  const decorative = el => el.getAttribute && el.getAttribute('aria-hidden') === 'true';
  // A responsive build carries both breakpoints' copy in one DOM and hides the half it
  // is not showing. Text inside a display:none element is not on the page at this
  // viewport, so counting it makes the other breakpoint's copy look like a match here
  // and this breakpoint's look missing. getClientRects() is 0 for display:none while
  // still true for position:fixed, which offsetParent gets wrong.
  const rendered = el => {
    if (!el.getClientRects || el.getClientRects().length === 0) return false;
    const cs = getComputedStyle(el);
    return cs.visibility !== 'hidden' && cs.display !== 'none';
  };
  // How many lines a run actually occupies. Dividing a box's height by its
  // line-height counts padding as a line -- a 30px pill around one 18px line reads as
  // two. Range rects are the real line boxes; distinct tops are the real line count.
  // Ranging over a whole element also picks up rects from decorative and hidden
  // descendants -- a bullet's tick lands on its own top and inflates the count. Only
  // the text nodes the copy comparison itself sees are ranged.
  const visibleTextNodes = el => {
    const out = [];
    const rec = n => {
      if (n.nodeType === 3) { if (n.textContent.trim()) out.push(n); return; }
      if (n.nodeType !== 1 || skip.has(n.tagName) || decorative(n) || !rendered(n)) return;
      for (const c of n.childNodes) rec(c);
    };
    rec(el);
    return out;
  };
  const lineCount = target => {
    try {
      const nodes = target.nodeType === 3 ? [target] : visibleTextNodes(target);
      const tops = new Set();
      for (const n of nodes) {
        const rg = document.createRange();
        rg.selectNodeContents(n);
        for (const r of rg.getClientRects()) {
          if (r.width > 0 || r.height > 0) tops.add(Math.round(r.top));
        }
      }
      return tops.size || null;
    } catch (e) { return null; }
  };
  // The mirror of enclosing_box() on the Figma side: the nearest ancestor that
  // actually paints something. Capped at 6 levels so a page-level background never
  // stands in for a chip that has none.
  const alpha = c => { const m = /rgba?\([^)]*?,\s*([\d.]+)\)$/.exec(c || ''); return m ? parseFloat(m[1]) : 1; };
  const boxOf = el => {
    let n = el;
    for (let i = 0; i < 6 && n && n.nodeType === 1; i++, n = n.parentElement) {
      const cs = getComputedStyle(n);
      const painted = (cs.backgroundColor && cs.backgroundColor !== 'transparent'
                       && alpha(cs.backgroundColor) > 0)
                      || parseFloat(cs.borderTopWidth) > 0
                      || parseFloat(cs.borderLeftWidth) > 0;
      if (!painted) continue;
      const r = n.getBoundingClientRect();
      return {
        tag: n.tagName.toLowerCase(),
        bg: alpha(cs.backgroundColor) > 0 ? cs.backgroundColor : null,
        radius: parseFloat(cs.borderTopLeftRadius) || 0,
        border: Math.max(parseFloat(cs.borderTopWidth) || 0,
                         parseFloat(cs.borderLeftWidth) || 0),
        border_color: cs.borderTopColor,
        w: Math.round(r.width), h: Math.round(r.height)
      };
    }
    return null;
  };
  const depthOf = el => { let d = 0; for (let n = el; n; n = n.parentElement) d++; return d; };
  const walk = el => {
    if (skip.has(el.tagName) || decorative(el) || !rendered(el)) return;
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
          w: Math.round(r.width),
          h: Math.round(r.height),
          lines: lineCount(n),
          display: cs.display,
          box: boxOf(el),
          depth: depthOf(el)
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
        'p,h1,h2,h3,h4,h5,h6,li,td,th,a,button,figcaption,blockquote,div,span')) {
    if (skip.has(el.tagName) || decorative(el) || !rendered(el)) continue;
    // innerText includes aria-hidden descendants, so rebuild it from the visible text
    // nodes only. Otherwise a decorative tick or star prefixes every bullet and makes
    // verbatim copy look retyped.
    const visible = [];
    const collect = n => {
      if (n.nodeType === 3) { visible.push(n.textContent); return; }
      if (n.nodeType !== 1 || skip.has(n.tagName) || decorative(n) || !rendered(n)) return;
      for (const c of n.childNodes) collect(c);
    };
    collect(el);
    const t = visible.join('').replace(/\s+/g, ' ').trim();
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
      w: Math.round(r.width), h: Math.round(r.height), lines: lineCount(el),
      display: cs.display, box: boxOf(el), depth: depthOf(el)
    });
  }
  return out.concat(blocks);
}
"""


INSTRUCTED_FAMILY = re.compile(r"set family to\s+(.+?)\s*$", re.I)


def intended_family(fnode):
    """The family the design *means*, which is not always the one it has applied.

    This file's headings are named `H2 · set family to Delight Semi Bold` while the
    frame still has Poppins on them -- the name is the instruction and the applied
    font is the placeholder. Comparing against the applied font would report every
    correctly-built heading as wrong, so the name wins where it says so.
    """
    m = INSTRUCTED_FAMILY.search((fnode.get("path") or "").split("/")[-1])
    if m:
        # `Delight Semi Bold` names family + weight; the family is the leading word(s).
        words = m.group(1).split()
        # Strip a trailing weight, two-word forms ("Semi Bold") before one-word ones,
        # or "Semi" survives and the family reads as "Delight Semi".
        changed = True
        while changed and words:
            changed = False
            if len(words) > 1 and weight_of("".join(words[-2:])) is not None:
                words, changed = words[:-2], True
            elif weight_of(words[-1]) is not None:
                words, changed = words[:-1], True
        return " ".join(words) or None
    return fnode.get("family")


def style_distance(f, l):
    """How far a live run is from a Figma node in look alone, for tie-breaking.

    Only used to choose between candidates that already carry identical copy, so it
    never decides whether something matched -- only which of two identical strings is
    which. Colour dominates because it is the most reliable discriminator; size and
    weight are normalised so neither swamps the other.
    """
    d = 0.0
    if f.get("color") and l.get("color_hex"):
        d += 0.0 if f["color"] == l["color_hex"] else 3.0
    if f.get("font_size") and l.get("font_size"):
        d += min(abs(f["font_size"] - l["font_size"]) / 4.0, 2.0)
    if f.get("font_weight") and l.get("font_weight"):
        d += min(abs(f["font_weight"] - l["font_weight"]) / 200.0, 2.0)
    if l.get("aggregate"):
        d += 0.25          # a leaf is the tighter box, all else equal
    return d


def line_count(height, line_height):
    """How many lines a box of this height holds. None when either is unknown."""
    try:
        if not height or not line_height or line_height <= 0:
            return None
        return max(1, int(round(float(height) / float(line_height))))
    except (TypeError, ValueError):
        return None


def rgb_to_hex(c):
    m = re.match(r"rgba?\(([\d.]+),\s*([\d.]+),\s*([\d.]+)", c or "")
    if not m:
        return None
    return "#%02x%02x%02x" % tuple(round(float(m.group(i))) for i in (1, 2, 3))


def read_live(url, viewport, mobile, want_images=False):
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
        # 60ms per step outran lazy loading and screenshotted blank images.
        pg.evaluate("() => new Promise(r => {let y=0;const t=setInterval(()=>{"
                    "window.scrollBy(0,600);y+=600;"
                    "if(y>document.body.scrollHeight){clearInterval(t);"
                    "window.scrollTo(0,0);r();}},220);})")
        pg.wait_for_timeout(1000)
        live = pg.evaluate(LIVE_JS)
        imgs, shots = [], {}
        if want_images:
            # Sample only once every image has actually decoded. Before it loads, an
            # <img> inside a <picture> reports the fallback `src` as its currentSrc and
            # a naturalWidth of 0 -- which reads as "wrong file, did not load" and made
            # this check fail at random against a cold dev server.
            try:
                pg.wait_for_function(
                    "() => [...document.images].every(i => i.complete)", timeout=20_000)
            except Exception:
                pass
            pg.wait_for_timeout(500)
            # An element screenshot captures whatever is painted over that region, so
            # a consent banner or sticky bar sitting on a figure reads as a wrong crop.
            # Anything fixed or sticky is site chrome -- a Figma figure never is -- so
            # it comes out for the pixel pass only.
            pg.evaluate("""() => {
              for (const el of document.querySelectorAll('body *')) {
                const p = getComputedStyle(el).position;
                if (p === 'fixed' || p === 'sticky') el.style.visibility = 'hidden';
              }
            }""")
            pg.wait_for_timeout(300)
            imgs = pg.evaluate(LIVE_IMG_JS)
            for im in imgs:
                try:
                    el = pg.query_selector(f'img[data-dd-img="{im["idx"]}"]')
                    if el:
                        shots[im["idx"]] = el.screenshot()
                except Exception:
                    pass
        b.close()
    for l in live:
        l["color_hex"] = rgb_to_hex(l["color"])
    return live, imgs, shots



# ---------------------------------------------------------------- geometry
# Copy, type and photos can all be right while the boxes around them are wrong: a card
# padded 40 where the design says 20, a chip with the wrong radius, a section on the
# wrong background. None of that shows up in a text comparison, and it is most of what
# "the layout is off" means when a human says it.
#
# These checks anchor to text that has ALREADY matched, so no attempt is made to align
# the two trees -- a matched line's own box and the painted box around it are both
# unambiguous on each side.
WIDTH_TOL_PX = 2      # a FILL node's width is its container's padding, restated
GAP_TOL_PX = 3        # gap to the previous sibling in the same Figma parent
RADIUS_TOL_PX = 2
BORDER_TOL_PX = 0.6


def geometry_deltas(f, l):
    """Box-level differences for one matched line. Empty when nothing is off."""
    out = []
    # 1. Width -- a FILL node's width IS its container's horizontal padding, restated,
    #    so comparing it catches wrong padding without mapping containers at all.
    #    Two cases have to be excluded or it reports noise instead:
    #      * a HUG node is as wide as its glyphs, so comparing it measures font
    #        rasterisation rather than layout;
    #      * an inline live element (a `<strong>` mid-paragraph) is also as wide as its
    #        glyphs, and an aggregate is "some element containing this text" -- often a
    #        wrapper larger than the design's text node, like an `<li>` standing in for
    #        a Benefit frame. Neither is the same box the design is describing.
    comparable = (str(f.get("sizing_h") or "").upper() in ("FILL", "STRETCH")
                  and not l.get("aggregate")
                  and l.get("display") not in ("inline", "inline-flex", None))
    if comparable and f.get("w") and l.get("w") \
            and abs(f["w"] - l["w"]) > WIDTH_TOL_PX:
        out.append(f"width {round(f['w'])} -> {round(l['w'])}")
    # 2. The painted box the line sits in.
    fb, lb = f.get("box"), l.get("box")
    if fb and lb:
        if fb.get("bg") and lb.get("bg"):
            live_bg = rgb_to_hex(lb["bg"])
            if live_bg and fb["bg"] != live_bg:
                out.append(f"{fb['name'] or 'box'} background {fb['bg']} -> {live_bg}")
        if fb.get("radius") is not None and lb.get("radius") is not None:
            # Figma writes a pill as 999; CSS writes it as 9999px. Both mean "fully
            # rounded", and a box shorter than its radius is a pill either way.
            fr, lr = fb["radius"], lb["radius"]
            pill = fr >= 100 and lr >= min(lb.get("h", 0), lb.get("w", 0)) / 2
            if not pill and abs(fr - lr) > RADIUS_TOL_PX:
                out.append(f"{fb['name'] or 'box'} radius {fr:g} -> {lr:g}")
        if fb.get("border") is not None and lb.get("border") is not None \
                and abs(fb["border"] - lb["border"]) > BORDER_TOL_PX:
            out.append(f"{fb['name'] or 'box'} border {fb['border']:g} -> {lb['border']:g}")
    return out


def gap_deltas(rows):
    """Gap between adjacent matched lines that share a Figma parent.

    Figma reports x/y relative to the parent, so only siblings are comparable -- but
    siblings are exactly where a wrong `gap` or margin shows. The measurement is local
    (previous sibling's bottom to this one's top), so it does not accumulate drift and
    a line that wrapped differently does not poison the lines after it.
    """
    by_parent = {}
    for r in rows:
        if r["status"] == "MISSING" or r.get("live_y") is None \
                or r.get("sibling_index") is None:
            continue
        pid = r.get("parent_id")
        if pid:
            by_parent.setdefault(pid, []).append(r)
    for kids in by_parent.values():
        kids.sort(key=lambda r: r["sibling_index"])
        for prev, cur in zip(kids, kids[1:]):
            # Only genuinely adjacent children. With a gap in between -- a sibling that
            # is a frame, so its own text matched under a different parent -- the
            # "gap" is really the height of everything unmatched between them, and
            # reporting that as a spacing defect is noise.
            if cur["sibling_index"] != prev["sibling_index"] + 1:
                continue
            fgap = cur["figma_y"] - (prev["figma_y"] + prev["figma_h"])
            lgap = cur["live_y"] - (prev["live_y"] + prev["live_h"])
            if fgap < -1 or lgap < -1:      # overlapping or inline; not a stack
                continue
            if abs(fgap - lgap) > GAP_TOL_PX:
                cur.setdefault("deltas", []).append(
                    f"gap above {round(fgap)} -> {round(lgap)}")
                if cur["status"] == "OK":
                    cur["status"] = "RESTYLED"


COVER_TOL_PX = 6      # how closely matched text must reach a container's own edges


def container_gap_deltas(rows, containers):
    """Spacing BETWEEN containers -- the section gaps a text-only check cannot see.

    A wrong `gap` on the article column shows up nowhere in a text comparison: every
    line inside every block is still correct, and the blocks are simply closer
    together. So each container's live extent is taken from the matched copy inside it,
    and consecutive siblings are compared.

    The guard matters as much as the check. A container's live extent is only
    trustworthy when the matched text actually reaches its top and bottom edges -- if a
    block opens with a photo, the text starts below it and the measured gap would
    include the photo's height. Where the copy does not cover the container, the gap is
    not reported at all rather than reported wrongly.
    """
    live, fig = {}, {}
    for r in rows:
        if r["status"] == "MISSING" or r.get("live_y") is None:
            continue
        top, bot = r["live_y"], r["live_y"] + (r.get("live_h") or 0)
        ftop = r.get("figma_abs_y")
        fbot = (ftop + (r.get("figma_h") or 0)) if ftop is not None else None
        for aid in (r.get("ancestor_ids") or []):
            e = live.setdefault(aid, [top, bot])
            e[0], e[1] = min(e[0], top), max(e[1], bot)
            if ftop is not None:
                g = fig.setdefault(aid, [ftop, fbot])
                g[0], g[1] = min(g[0], ftop), max(g[1], fbot)

    def covered(cid):
        c, g = containers.get(cid), fig.get(cid)
        if not c or not g or c.get("h") is None:
            return False
        return (abs(g[0] - c["abs_y"]) <= COVER_TOL_PX
                and abs(g[1] - (c["abs_y"] + c["h"])) <= COVER_TOL_PX)

    by_parent = {}
    for cid, c in containers.items():
        if c.get("parent_id") and cid in live and c.get("sibling_index") is not None:
            by_parent.setdefault(c["parent_id"], []).append(c)
    out = []
    for kids in by_parent.values():
        parent = containers.get(kids[0]["parent_id"]) or {}
        # These gaps are measured top-to-bottom. In a horizontal row the design's gap
        # runs the other way, and if the row wraps the vertical distance is a wrap
        # artefact rather than a spacing decision.
        if parent.get("dir") and parent["dir"] != "VERTICAL":
            continue
        kids.sort(key=lambda c: c["sibling_index"])
        for a, b in zip(kids, kids[1:]):
            if b["sibling_index"] != a["sibling_index"] + 1:
                continue
            if not (covered(a["id"]) and covered(b["id"])):
                continue
            fgap = b["abs_y"] - (a["abs_y"] + (a["h"] or 0))
            lgap = live[b["id"]][0] - live[a["id"]][1]
            if fgap < -1 or lgap < -1:
                continue
            if abs(fgap - lgap) > GAP_TOL_PX:
                out.append({
                    "status": "RESTYLED", "path": b["path"],
                    "between": [a.get("name"), b.get("name")],
                    "delta": f"gap between {a.get('name')} and {b.get('name')} "
                             f"{round(fgap)} -> {round(lgap)}",
                })
    return out


# ---------------------------------------------------------------- images
# Copy and typography can both be perfect while a photo shows the wrong part of
# itself. That is not a CSS bug you can spot in a class list -- the box is the right
# size, the file is the right file, and only the crop is wrong. So the design's own
# node renders are the reference, and the live element is compared to them as pixels.
IMG_ASPECT_TOL = 0.03      # 3% -- a differing aspect ratio is a box defect
# Mean absolute grey difference over a 64x64 downsample, 0..1. Calibrated against the
# email-exclusive build on 2026-08-26, where six photos were shipped centre-cropped
# from the desktop asset and three of those were wrong enough for a human to notice:
#
#   correct crop (asset rendered from the node)   0.001 - 0.002
#   crop a human did not notice                   0.006 - 0.007
#   crop a human DID flag as wrong                0.055 - 0.264
#
# The gap between "right" and "reported by a human" is two orders of magnitude, so the
# line sits low. An earlier 0.14 let the wrist photo through at 0.133 -- it was one of
# the three the human flagged, which is the whole reason this check exists.
IMG_PIXEL_TOL = 0.05


def walk_image_nodes(node, out, path=""):
    """Every Figma node painted with an image fill, in document order."""
    if isinstance(node, list):
        for n in node:
            walk_image_nodes(n, out, path)
        return
    if not isinstance(node, dict):
        return
    name = node.get("name") or ""
    here = f"{path}/{name}" if name else path
    fills = node.get("fills")
    if isinstance(fills, list) and any(
            isinstance(f, dict) and f.get("type") == "IMAGE" and f.get("visible", True)
            for f in fills):
        box = node.get("absoluteBoundingBox") or {}
        w = box.get("width", node.get("width"))
        h = box.get("height", node.get("height"))
        if w and h:
            out.append({"id": node.get("id"), "path": here.lstrip("/"),
                        "name": name, "w": round(w), "h": round(h),
                        "y": box.get("y", node.get("y")) or 0})
    for k in ("children", "nodes", "document", "root", "node"):
        v = node.get(k)
        if isinstance(v, (list, dict)):
            walk_image_nodes(v, out, here)
    for k, v in node.items():
        if k in ("children", "nodes", "document", "root", "node", "fills"):
            continue
        if isinstance(v, dict) and ("document" in v or "children" in v or "fills" in v):
            walk_image_nodes(v, out, here)


LIVE_IMG_JS = r"""
() => {
  const out = [];
  document.querySelectorAll('img').forEach((im, i) => {
    const r = im.getBoundingClientRect();
    if (r.width < 24 || r.height < 24) return;          // icons and spacers
    const cs = getComputedStyle(im);
    if (cs.display === 'none' || cs.visibility === 'hidden') return;
    im.setAttribute('data-dd-img', String(i));
    out.push({
      idx: i,
      src: (im.currentSrc || im.src || '').split('?')[0],
      w: Math.round(r.width), h: Math.round(r.height),
      y: Math.round(r.top + window.scrollY),
      natural: [im.naturalWidth, im.naturalHeight],
      fit: cs.objectFit, radius: cs.borderRadius
    });
  });
  return out.sort((a, b) => a.y - b.y);
}
"""


def _grey64(path_or_bytes):
    from PIL import Image
    im = (Image.open(path_or_bytes) if not isinstance(path_or_bytes, (str, bytes))
          else Image.open(io.BytesIO(path_or_bytes) if isinstance(path_or_bytes, bytes)
                          else path_or_bytes))
    return im.convert("L").resize((64, 64), Image.BILINEAR)


def pixel_distance(a, b):
    """Mean absolute grey difference, 0 (identical) .. 1 (inverted)."""
    ga, gb = _grey64(a), _grey64(b)
    pa, pb = ga.load(), gb.load()
    total = 0
    for y in range(64):
        for x in range(64):
            total += abs(pa[x, y] - pb[x, y])
    return total / (64 * 64 * 255)


def compare_images(figma_imgs, live_imgs, crops_dir, shots):
    """Pair design image nodes with live <img>s in document order and compare."""
    # Document order, not y: figwright reports x/y relative to the parent, so a Photo
    # inside a Figure and a Product panel inside a card both report y=0 and sorting on
    # it can reorder the pairing. The walker already emits in document order, which is
    # the order the DOM renders in.
    rows = []
    for i, fnode in enumerate(figma_imgs):
        row = {"figma_id": fnode["id"], "path": fnode["path"],
               "figma_w": fnode["w"], "figma_h": fnode["h"], "deltas": []}
        if i >= len(live_imgs):
            row["status"] = "MISSING"
            rows.append(row)
            continue
        l = live_imgs[i]
        row.update({"src": l["src"], "live_w": l["w"], "live_h": l["h"],
                    "natural": l["natural"]})
        if l["natural"][0] == 0:
            row["deltas"].append("did not load")
        fa, la = fnode["w"] / fnode["h"], (l["w"] / l["h"] if l["h"] else 0)
        if la and abs(fa - la) / fa > IMG_ASPECT_TOL:
            row["deltas"].append(f"aspect {fa:.2f} -> {la:.2f}")
        crop = os.path.join(crops_dir or "", f"{fnode['id'].replace(':', '-')}.png")
        shot = shots.get(l["idx"])
        if crops_dir and os.path.exists(crop) and shot:
            d = pixel_distance(crop, shot)
            row["pixel_distance"] = round(d, 3)
            if d > IMG_PIXEL_TOL:
                row["deltas"].append(
                    f"shows a different crop than the design (distance {d:.2f})")
        row["status"] = "RESTYLED" if row["deltas"] else "OK"
        rows.append(row)
    for extra in live_imgs[len(figma_imgs):]:
        rows.append({"status": "EXTRA", "src": extra["src"],
                     "live_w": extra["w"], "live_h": extra["h"], "deltas": []})
    return rows


def match(figma_nodes, live_nodes):
    """Match each Figma line to a live line: exact first, then closest fuzzy."""
    pool = {}
    for i, l in enumerate(live_nodes):
        pool.setdefault(norm(l["text"]), []).append(i)
    # Where several live elements carry the same text, the tightest one is the real
    # text box: a leaf run first, then the INNERMOST wrapper. Otherwise a wrapper gets
    # measured instead of the text -- wrapping a rating in TrustpilotLink put the `<a>`
    # (16px/400, all inherited) ahead of the 12px/500 span inside it and produced three
    # style deltas that did not exist. Interpolated copy makes this the common case: the
    # span's text is several JSX expressions, so the whole string exists only as an
    # aggregate and there is no leaf to prefer.
    for k in pool:
        pool[k].sort(key=lambda i: (bool(live_nodes[i].get("aggregate")),
                                    -(live_nodes[i].get("depth") or 0)))
    used, rows = set(), []
    live_keys = list(pool.keys())

    for f in figma_nodes:
        raw = f["chars"] or ""
        # A hard line break in Figma is a visual break at ONE fixed width. Reproducing
        # it in HTML would break at every other width, so flowing text is the correct
        # build -- try the whole string first and accept it as a match.
        if "\n" in raw:
            joined = norm(raw.replace("\n", " "))
            hit = next((c for c in pool.get(joined, []) if c not in used), None)
            if hit is None:
                near = difflib.get_close_matches(joined, live_keys, n=1, cutoff=0.95)
                if near:
                    hit = next((c for c in pool.get(near[0], []) if c not in used), None)
            if hit is not None:
                used.add(hit)
                rows.append({"figma": raw.replace("\n", " "), "figma_id": f["id"],
                             "path": f["path"], "font_size": f["font_size"],
                             "font_weight": f["font_weight"], "color": f["color"],
                             "match": "reflowed", "score": 1.0, "deltas": [],
                             "live": live_nodes[hit]["text"], "status": "OK"})
                continue
        # Otherwise compare per visual line.
        for line in [x for x in raw.split("\n") if x.strip()]:
            key = norm(line)
            idx, how, score = None, None, 1.0
            # A page can carry the same words twice in different styles -- this design
            # has "EMAIL EXCLUSIVE" as both a white banner chip and a lime article chip.
            # Taking the first free candidate pairs them by document order, which is a
            # coin flip; pairing on style is deterministic and is what a reader would do.
            free = [c for c in pool.get(key, []) if c not in used]
            if len(free) > 1:
                free.sort(key=lambda c: style_distance(f, live_nodes[c]))
            if free:
                idx, how = free[0], "exact"
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
                if not family_matches(intended_family(f), l.get("family")):
                    deltas.append("family %s -> %s"
                                  % (f["family"], l["family"].split(",")[0].strip()))
                # A node that wraps onto a different number of lines than the frame is
                # a layout defect, not a copy one: a chip that was one line in the
                # design and is two on the page has broken its own box. Comparing line
                # COUNT rather than raw px keeps this quiet about font-metric noise.
                fl = line_count(f.get("h"), f.get("line_height"))
                ll = l.get("lines") or line_count(l.get("h"), l.get("line_height"))
                if fl and ll and fl != ll:
                    deltas.append(f"wraps to {ll} line(s), design has {fl}")
                row["figma_lines"], row["live_lines"] = fl, ll
                deltas += geometry_deltas(f, l)
                row.update({"parent_id": f.get("parent_id"),
                            "sibling_index": f.get("sibling_index"),
                            "figma_y": f.get("y"), "figma_h": f.get("h"),
                            "figma_abs_y": f.get("abs_y"),
                            "ancestor_ids": f.get("ancestor_ids"),
                            "figma_w": f.get("w"), "live_w": l.get("w"),
                            "live_y": l.get("y"), "live_h": l.get("h")})
                row["deltas"] = deltas
                row["status"] = ("RETYPED" if how == "fuzzy"
                                 else ("RESTYLED" if deltas else "OK"))
            rows.append(row)

    gap_deltas(rows)
    for r in rows:
        if r.get("deltas") and r["status"] == "OK":
            r["status"] = "RESTYLED"
    extra = [live_nodes[i]["text"] for i in range(len(live_nodes))
             if i not in used and not live_nodes[i].get("aggregate")]
    return rows, extra


def render(rows, extra, url, spec_path, viewport):
    miss = [r for r in rows if r["status"] == "MISSING"]
    retyped = [r for r in rows if r["status"] == "RETYPED"]
    restyled = [r for r in rows if r["status"] == "RESTYLED"]
    ok = [r for r in rows if r["status"] == "OK"]
    acc = [r for r in rows if r["status"] == "ACCEPTED"]
    L = ["# Design fidelity -- Figma vs live", "",
         f"- Design: `{spec_path}`", f"- Live: {url} @ {viewport}px",
         f"- {len(ok)} exact, {len(restyled)} restyled, {len(retyped)} retyped, "
         f"{len(miss)} missing, {len(extra)} on the page but not in the design."
         + (f" {len(acc)} accepted." if acc else ""), ""]
    if acc:
        L += ["## Accepted deviations", "",
              "The page deliberately does not follow the frame here.", "",
              "| Figma says | Page says | Why |", "|---|---|---|"]
        for r in acc:
            L.append(f"| {r['figma']} | {r.get('live') or '--'} | "
                     f"{r.get('accepted_reason', '')} |")
        L.append("")
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
    ap.add_argument("--accept", default=None,
                    help="JSON {\"<figma-node-id>\": \"why\"} of deviations that are "
                         "decisions rather than defects -- a figure the page reads "
                         "live where the frame hardcodes it, say. Listed in the report "
                         "with the reason, and does not fail the run. A judge that "
                         "reports a settled question every time gets ignored.")
    ap.add_argument("--crops", default=None,
                    help="directory of per-node PNG renders (figwright "
                         "save_screenshots, named <node-id>.png). Without it images "
                         "are only checked for box and aspect, not for crop.")
    args = ap.parse_args()

    # ⚠️ encoding="utf-8" is REQUIRED, not tidiness. Without it Python uses the
    # locale default, which on Windows is cp1252, and every non-ASCII character in
    # the design JSON arrives as mojibake: a curly apostrophe (UTF-8 E2 80 99) reads
    # back as "â€™". The live side comes from Playwright and is decoded correctly, so
    # the two never match and the tool reports a FALSE "retyped" for copy that is in
    # fact verbatim. Measured 2026-09-02 on an HLTH article: figma
    # 'How much higher womenâ€™s ...' vs live 'How much higher women’s ...',
    # similarity 0.944, verdict RETYPED, when the strings were identical.
    # These designs are full of curly apostrophes, em dashes and currency symbols,
    # so on Windows this silently poisoned the copy check.
    spec = json.load(open(args.spec, encoding="utf-8"))
    all_nodes, containers = [], {}
    walk_text_nodes(spec, all_nodes, containers=containers)
    figma = [n for n in all_nodes if not n.get("decorative")]
    decorative = [n for n in all_nodes if n.get("decorative")]
    if not figma:
        sys.exit(f"no TEXT nodes found in {args.spec} -- is this a figwright dump?")
    print(f"{len(figma)} text node(s) in the design"
          + (f"  (+{len(decorative)} decorative glyph(s), not compared as copy)"
             if decorative else ""))

    figma_imgs = []
    walk_image_nodes(spec, figma_imgs)
    live, live_imgs, shots = read_live(args.url, args.viewport, args.mobile,
                                       want_images=bool(figma_imgs))
    print(f"{len(live)} text run(s) on the live page")

    img_rows = compare_images(figma_imgs, live_imgs, args.crops, shots) \
        if figma_imgs else []
    if img_rows:
        bad = [r for r in img_rows if r["status"] not in ("OK",)]
        print(f"{len(figma_imgs)} image node(s) in the design, "
              f"{len(live_imgs)} on the page"
              + (f" -- {len(bad)} mismatched" if bad else " -- all match")
              + ("" if args.crops else "  (no --crops: boxes compared, not pixels)"))

    rows, extra = match(figma, live)
    # utf-8 for the same reason as the spec read above: an accepted-deviation
    # reason is prose and will contain non-ASCII sooner or later.
    accepted = json.load(open(args.accept, encoding="utf-8")) if args.accept else {}
    for r in rows:
        why = accepted.get(r.get("figma_id"))
        if why and r["status"] != "OK":
            r["accepted_reason"] = why
            r["was"] = r["status"]
            r["status"] = "ACCEPTED"
    if accepted:
        n = len([r for r in rows if r["status"] == "ACCEPTED"])
        print(f"{n} accepted deviation(s) -- design deliberately not followed")
    layout_rows = container_gap_deltas(rows, containers)
    if layout_rows:
        print(f"{len(layout_rows)} spacing mismatch(es) between containers")
    out_dir = args.out or os.path.join(HERE, "runs", "design-diff")
    os.makedirs(out_dir, exist_ok=True)
    payload = {"spec": args.spec, "url": args.url, "viewport": args.viewport,
               "rows": rows, "extra_on_page": extra,
               "decorative_glyphs": [{"id": n["id"], "chars": n["chars"]}
                                     for n in decorative],
               "images": img_rows,
               "layout": layout_rows,
               "summary": {s: len([r for r in rows if r["status"] == s])
                           for s in ("OK", "ACCEPTED", "RESTYLED", "RETYPED",
                                     "MISSING")},
               "image_summary": {s: len([r for r in img_rows if r["status"] == s])
                                 for s in ("OK", "RESTYLED", "MISSING", "EXTRA")}}
    with open(os.path.join(out_dir, "design_diff.json"), "w", encoding="utf-8") as f:
        json.dump(payload, f, indent=2)
    md = render(rows, extra, args.url, args.spec, args.viewport)
    if decorative:
        md += (f"\n## Decorative glyphs (not compared)\n\n"
               f"{len(decorative)} node(s) in the design hold only a symbol "
               f"({', '.join(sorted({n['chars'].strip() for n in decorative}))}). "
               f"A correct build renders these as styled elements rather than text, so "
               f"they are excluded from the copy comparison.\n")
    # The .md carries the design's own copy, so it must be written as utf-8 —
    # otherwise the report itself is cp1252 on Windows and every curly apostrophe
    # renders as a replacement character in any UTF-8 reader.
    with open(os.path.join(out_dir, "design_diff.md"), "w", encoding="utf-8") as f:
        f.write(md)
    print(json.dumps(payload["summary"]))
    if img_rows:
        print("images:", json.dumps(payload["image_summary"]))
        for r in img_rows:
            if r["deltas"]:
                print("  %-28s %s" % (os.path.basename(r.get("src") or r["path"]),
                                      "; ".join(r["deltas"])))
    print("->", os.path.relpath(out_dir, ROOT))
    for r in layout_rows:
        print("  " + r["delta"])
    bad_imgs = sum(1 for r in img_rows if r["status"] in ("MISSING",) or r["deltas"])
    sys.exit(1 if (payload["summary"]["MISSING"] or bad_imgs) else 0)


if __name__ == "__main__":
    main()
