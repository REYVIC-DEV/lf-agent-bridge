"""
extract_techunboxed.py - Pull article content out of the Framer site
https://blog.techunboxed.co into clean structured data.

Framer server-renders content, so the article text is all in the HTML. Two
quirks we handle:
  1. Framer renders content twice (responsive breakpoint copies) -> we dedupe
     long text blocks, keeping first occurrence.
  2. Nav/footer/related-widgets are noise -> we trim to the article region.

Output (in ./extracted/):
  - <slug>.md    human-readable extraction (title, meta, ordered content)
  - <slug>.json  structured: {url, slug, title, description, image, category,
                 author, blocks:[{tag,text}], products:[...]}
  - index.json   list of all articles + metadata

Usage:
  python3 extract_techunboxed.py               # all articles from sitemap
  python3 extract_techunboxed.py <url> [<url>]  # specific article(s)
"""
import json
import os
import re
import sys
import html
import urllib.request
import urllib.error

SITEMAP = "https://blog.techunboxed.co/sitemap.xml"
UA = ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/125.0 Safari/537.36")
OUT_DIR = os.path.join(os.path.dirname(__file__), "extracted")

BLOCK_END = re.compile(
    r"(?i)</(p|div|h[1-6]|li|tr|section|article|header|footer|figcaption|blockquote)>")
BR = re.compile(r"(?i)<br\s*/?>")
TAG = re.compile(r"<[^>]+>")


def fetch(url):
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=60) as r:
        return r.read().decode("utf-8", "replace")


def meta(html_text, prop):
    for pat in (rf'<meta[^>]+property="{prop}"[^>]+content="([^"]*)"',
                rf'<meta[^>]+content="([^"]*)"[^>]+property="{prop}"',
                rf'<meta[^>]+name="{prop}"[^>]+content="([^"]*)"'):
        m = re.search(pat, html_text, re.I)
        if m:
            return html.unescape(m.group(1))
    return None


def article_urls():
    xml = fetch(SITEMAP)
    locs = re.findall(r"<loc>([^<]+)</loc>", xml)
    return [u for u in locs if "/article/" in u]


def to_blocks(html_text):
    """Turn body HTML into an ordered list of clean text lines."""
    # keep only <body> if present to drop <head> noise
    mb = re.search(r"(?is)<body[^>]*>(.*)</body>", html_text)
    h = mb.group(1) if mb else html_text
    h = BR.sub("\n", h)
    h = BLOCK_END.sub("\n", h)
    h = TAG.sub("", h)
    h = html.unescape(h)
    lines = []
    for raw in h.split("\n"):
        s = re.sub(r"\s+", " ", raw).strip()
        if s:
            lines.append(s)
    return lines


def collapse_runs(lines):
    """Remove immediately-repeated contiguous segments (Framer emits the same
    block twice for responsive breakpoints). Keeps one copy."""
    n = len(lines)
    i = 0
    out = []
    while i < n:
        found = 0
        for L in range((n - i) // 2, 1, -1):
            if lines[i:i + L] == lines[i + L:i + 2 * L]:
                found = L
                break
        if found:
            out.extend(lines[i:i + found])
            i += 2 * found
        else:
            out.append(lines[i])
            i += 1
    return out


def dedupe(lines):
    """Framer emits responsive duplicates. Drop repeat long blocks (keep 1st)
    and collapse adjacent identical short lines."""
    seen_long = set()
    out = []
    for s in lines:
        if len(s) >= 40:
            if s in seen_long:
                continue
            seen_long.add(s)
            out.append(s)
        else:
            if out and out[-1] == s:
                continue
            out.append(s)
    return out


# noise lines to drop (nav, footer, chrome)
NOISE = re.compile(
    r"^(Home|Menu|Search|Subscribe|Submit|No spam\.|Categories|Follow|Share|"
    r"Buying Guides|Mobile|Wearables|Audio|Smart Home|Laptops|Health Tech|"
    r"Copyright|©|All rights reserved|Privacy|Terms|Cookie)",
    re.I)


def trim_article(lines, title):
    """Start at the article title; stop at the newsletter/footer boundary."""
    start = 0
    for i, s in enumerate(lines):
        if title and title[:30].lower() in s.lower():
            start = i
            break
    end = len(lines)
    for i in range(start, len(lines)):
        if re.search(r"get the best of techunboxed|in your inbox", lines[i], re.I):
            end = i
            break
    body = lines[start:end]
    return [s for s in body if not NOISE.match(s)]


def parse_products(lines):
    """Best-effort structured pull for listicle/review pages. Each product
    block starts at a 'Rating:' or a price line near a name heading."""
    products = []
    cur = None
    for i, s in enumerate(lines):
        mrate = re.match(r"^Rating:\s*(.+)$", s)
        mprice = re.match(r"^\$\s?([\d,]+(?:\.\d+)?)", s)
        mstand = re.match(r"^Standout feature:\s*(.+)$", s, re.I)
        if mrate:
            # the heading just above is usually "Name: Tagline"
            name = lines[i - 1] if i > 0 else None
            if cur:
                products.append(cur)
            cur = {"name": name, "rating": mrate.group(1).strip(),
                   "price": None, "standout": None, "pros": [], "cons": [],
                   "take": []}
        elif cur is not None:
            if mprice and not cur["price"]:
                cur["price"] = s
            elif mstand:
                cur["standout"] = mstand.group(1).strip()
            elif s.lower() == "check now!":
                pass
    if cur:
        products.append(cur)
    return products


def extract(url):
    h = fetch(url)
    slug = url.rstrip("/").split("/")[-1]
    title = meta(h, "og:title") or ""
    title = re.sub(r"\s*\|\s*TechUnboxed\s*$", "", title)
    desc = meta(h, "og:description")
    image = meta(h, "og:image")
    lines = trim_article(dedupe(collapse_runs(to_blocks(h))), title)
    products = parse_products(lines)
    return {
        "url": url,
        "slug": slug,
        "title": title,
        "description": desc,
        "image": image,
        "word_count": sum(len(x.split()) for x in lines),
        "blocks": lines,
        "products": products,
    }


def write_md(a):
    lines = [f"# {a['title']}", ""]
    if a["description"]:
        lines += [f"> {a['description']}", ""]
    lines += [f"- Source: {a['url']}"]
    if a["image"]:
        lines += [f"- Hero image: {a['image']}"]
    if a["products"]:
        lines += [f"- Products detected: {len(a['products'])}"]
    lines += ["", "---", ""]
    lines += a["blocks"]
    return "\n".join(lines) + "\n"


def main():
    os.makedirs(OUT_DIR, exist_ok=True)
    urls = sys.argv[1:] or article_urls()
    print(f"Extracting {len(urls)} article(s)...")
    index = []
    for i, url in enumerate(urls, 1):
        try:
            a = extract(url)
        except Exception as e:
            print(f"  [{i}/{len(urls)}] FAIL {url}: {e}")
            continue
        with open(os.path.join(OUT_DIR, a["slug"] + ".json"), "w") as f:
            json.dump(a, f, indent=2)
        with open(os.path.join(OUT_DIR, a["slug"] + ".md"), "w") as f:
            f.write(write_md(a))
        index.append({k: a[k] for k in
                      ("slug", "title", "description", "image", "url",
                       "word_count")} | {"products": len(a["products"])})
        print(f"  [{i}/{len(urls)}] {a['slug']}  "
              f"({a['word_count']} words, {len(a['products'])} products)")
    with open(os.path.join(OUT_DIR, "index.json"), "w") as f:
        json.dump(index, f, indent=2)
    print(f"\nDone. {len(index)} articles -> {OUT_DIR}/")


if __name__ == "__main__":
    main()
