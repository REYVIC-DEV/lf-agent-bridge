#!/usr/bin/env python3
"""Pull the aside blocks and Keep-exploring cards out of an article frame dump.

The Learn article designs add three things the parked drafts do not have: a stat card,
a product CTA, and the Keep-exploring cards. Each is a named node in the frame, so the
copy can be read out of the design rather than retyped from a diff listing (retyping is
how a curly apostrophe becomes a straight one and the fidelity check reports RETYPED
forever).

  python3 webforge/scripts/extract_article_blocks.py <design-dump.json> [--json]

Anchoring: each block sits among the article's own content blocks as a sibling, so what
matters for insertion is the text of the block BEFORE it. That is emitted as `after`, and
it is what lets the insertion be positional rather than guessed.

⚠️ The CTA's destination is encoded in the node NAME (`Aside · Product CTA → /path`), but
it is NOT authoritative: the designer's frames say `/collections/...` while Joshua asked
for the band PDP directly ("can you point cta directly to the main band why did you even
point it to collections"). It is reported here so the divergence is visible, not so it
gets used.
"""
import argparse
import io
import json
import sys

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")


def walk(node, depth=0, parent=None):
    yield node, depth, parent
    for child in node.get("children") or []:
        yield from walk(child, depth + 1, node)


def texts(node):
    """Every TEXT descendant's characters, in document order."""
    out = []
    for n, _, _ in walk(node):
        if n.get("type") == "TEXT":
            c = (n.get("characters") or "").strip()
            if c:
                out.append(c)
    return out


def first_text(node):
    t = texts(node)
    return t[0] if t else None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("dump")
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()

    root = json.load(open(args.dump, encoding="utf-8"))
    root = root.get("node", root)

    # Find the container whose children are the article's content blocks: the parent of
    # the Block · Stat / Block · Product CTA nodes.
    block_parents = {}
    for n, _, parent in walk(root):
        nm = n.get("name") or ""
        if nm.startswith("Block · ") and parent is not None:
            block_parents.setdefault(parent["id"], parent)

    out = {"stats": [], "cta": None, "related": [], "blocks_order": []}

    for parent in block_parents.values():
        kids = parent.get("children") or []
        for i, k in enumerate(kids):
            nm = k.get("name") or ""
            # the text of the preceding sibling is the insertion anchor
            prev = None
            for j in range(i - 1, -1, -1):
                t = texts(kids[j])
                if t:
                    prev = t[-1]
                    break

            if nm == "Block · Stat":
                aside = next((c for c in walk(k) if (c[0].get("name") or "") == "Aside · Stat"), None)
                t = texts(aside[0]) if aside else texts(k)
                if len(t) >= 3:
                    out["stats"].append({"label": t[0], "value": t[1], "body": t[2], "after": prev})
            elif nm == "Block · Product CTA":
                aside = next((c for c in walk(k)
                              if (c[0].get("name") or "").startswith("Aside · Product CTA")), None)
                node = aside[0] if aside else k
                t = texts(node)
                href = None
                anm = node.get("name") or ""
                if "→" in anm:
                    href = anm.split("→", 1)[1].strip()
                if len(t) >= 4:
                    out["cta"] = {"eyebrow": t[0], "heading": t[1], "body": t[2],
                                  "ctaLabel": t[3], "figma_href": href, "after": prev}

    # Keep exploring. The cards are NOT children of the heading; heading and cards sit
    # inside one Container under a Section. Rather than guess at that nesting, take every
    # TEXT in the section in document order, drop the heading, and chunk the rest in
    # threes: each card is exactly (category, meta, title). Verified on what-is-hrv,
    # which yields ['Keep exploring', 'The Science','HRV','Reading Your HRV Scores',
    # 'The Science','Benchmarks','HRV By Age And Sex'].
    section = None
    for n, _, parent in walk(root):
        if n.get("type") == "TEXT" and (n.get("characters") or "").strip() == "Keep exploring":
            # climb to the nearest ancestor that holds more than just the heading
            chain = [p for x, _, p in walk(root) if x.get("id") == n["id"] and p]
            cur = chain[0] if chain else None
            while cur is not None:
                if len(texts(cur)) > 1:
                    section = cur
                    break
                nxt = [p for x, _, p in walk(root) if x.get("id") == cur["id"] and p]
                cur = nxt[0] if nxt else None
            break
    if section is not None:
        t = texts(section)
        rest = t[1:] if t and t[0] == "Keep exploring" else t
        if len(rest) % 3:
            print("  ⚠️  %d Keep-exploring texts is not a multiple of 3; cards may be "
                  "mis-grouped" % len(rest), file=sys.stderr)
        for i in range(0, len(rest) - 2, 3):
            out["related"].append({"category": rest[i], "meta": rest[i + 1], "title": rest[i + 2]})

    if args.json:
        print(json.dumps(out, indent=2, ensure_ascii=False))
        return

    print("STAT CARDS: %d" % len(out["stats"]))
    for s in out["stats"]:
        print("  label : %s" % s["label"])
        print("  value : %s" % s["value"])
        print("  body  : %s" % s["body"][:100])
        print("  after : %s" % (s["after"] or "")[-70:])
    print()
    print("PRODUCT CTA: %s" % ("yes" if out["cta"] else "NONE"))
    if out["cta"]:
        for k in ("eyebrow", "heading", "body", "ctaLabel", "figma_href"):
            print("  %-11s %s" % (k, (out["cta"][k] or "")[:100]))
        print("  %-11s %s" % ("after", (out["cta"]["after"] or "")[-70:]))
    print()
    print("KEEP EXPLORING: %d card(s)" % len(out["related"]))
    for r in out["related"]:
        print("  %-16s %-18s %s" % (r["category"][:16], r["meta"][:18], r["title"][:50]))


if __name__ == "__main__":
    main()
