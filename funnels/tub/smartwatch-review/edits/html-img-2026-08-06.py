#!/usr/bin/env python3
"""Replace three oversized-PNG Image blocks with responsive HtmlElement <img>.

Why HtmlElement and not the Image block: LF's Image schema exposes no srcset,
no sizes, no loading and no fetchpriority. Those four attributes are exactly
what the "properly size images" and "LCP request discovery" reports are asking
for, so raw HTML is the only way to set them.

Why the srcset points at /cdn-cgi/image/ rather than the asset directly:
measured on the live host, the Cloudflare resizer answers `format=auto` with
**AVIF** — 33.6K at 750w where the raw WebP is 50.4K. Serving the asset
directly costs ~17K on the LCP image and throws AVIF away. Going through the
resizer keeps AVIF *and* lets us request the exact widths the layout needs.

The origins are the small re-encoded WebPs (106K/78K/55K at 1400px) rather than
the 1.7-2.0 MB PNGs they replaced, so a cache miss is cheap too. Delivered
bytes are the same either way (33.1K vs 33.5K at 750w).

The CSS reproduces the Image block's styles verbatim (width 100%, fixed
height, object-fit cover, radius 10px) including the 767px height override, so
the layout is unchanged.
"""
import json
import os
import sys

sys.path.insert(0, "tools/lf-agent-bridge")
import lf_api  # noqa: E402

FUNNEL = "fun_vGqQYxn4H2i_traYYkh4w"
SP = sys.argv[1]
STEPS = {3: "step_-42yvjxEYUC-1yAzL9TKy", 11: "step_HFrpGxiibhudWV1YLEMs1"}

up = json.load(open(os.path.join(SP, "uploaded.json")))

# block id -> (asset label, css id, desktop height, mobile height, is_lcp)
PLAN = {
    "66bf8fce-ea96-41a7-8926-34323e7fab32": ("tub-hero", "tub-hero-img", "371px", "210px", True),
    "68a783f5-b3b0-47b5-a675-29a807f00a6a": ("tub-sec1", "tub-sec1-img", "371px", "230px", False),
    "4fb34f0f-708a-4569-8749-a8195d04205c": ("tub-sec2", "tub-sec2-img", "371px", "230px", False),
}

# Container is maxWidth 664px, with 16px side padding under 767px. Desktop
# therefore needs 664 (DPR1) / 1328 (DPR2); a 390px phone needs 358 / 716.
SIZES = "(min-width: 768px) 664px, calc(100vw - 32px)"
WIDTHS = [400, 560, 750, 1000, 1328]
FALLBACK_W = 750
CF = "https://assets.lightfunnels.com/cdn-cgi/image/width={w},quality=80,format=auto/{origin}"


def cf(origin, w):
    return CF.format(w=w, origin=origin)


def html_for(label, css_id, h_desk, h_mob, is_lcp):
    origin = up[label]["1400"]["src"]
    srcset = ", ".join(f"{cf(origin, w)} {w}w" for w in WIDTHS)
    # The LCP image must be eager + high priority; the other two sit well below
    # the fold, so lazy keeps them out of the initial load entirely.
    prio = 'fetchpriority="high" loading="eager"' if is_lcp else 'loading="lazy"'
    return (
        f'<style>\n'
        f'#{css_id}{{display:block;width:100%;max-width:100%;height:{h_desk};'
        f'object-fit:cover;border-radius:10px;}}\n'
        f'@media (max-width:767px){{#{css_id}{{height:{h_mob};}}}}\n'
        f'</style>\n'
        f'<img id="{css_id}"\n'
        f'  src="{cf(origin, FALLBACK_W)}"\n'
        f'  srcset="{srcset}"\n'
        f'  sizes="{SIZES}"\n'
        f'  width="1400" height="781" alt=""\n'
        f'  {prio} decoding="async">\n'
    )


def convert(body):
    """Swap matching nodes in place, whatever type they currently are, so this
    is idempotent and can be re-run to revise the markup."""
    hit = []

    def walk(n):
        if isinstance(n, dict):
            for v in n.values():
                walk(v)
        elif isinstance(n, list):
            for i, v in enumerate(n):
                if isinstance(v, dict) and v.get("id") in PLAN:
                    label, css_id, hd, hm, lcp = PLAN[v["id"]]
                    n[i] = {
                        "t": "HtmlElement",
                        "id": v["id"],
                        "p": {"content": html_for(label, css_id, hd, hm, lcp)},
                        "styles": [{"prop": "maxWidth", "value": "100%"}],
                    }
                    hit.append(v["id"])
                else:
                    walk(v)

    walk(body)
    return hit


def main():
    tok = open("tools/lf-agent-bridge/.session_token").read().strip()
    acct = open("tools/lf-agent-bridge/.lf_account").read().strip()
    h = lf_api.session_headers(acct)

    node = lf_api.get_funnel_steps(tok, FUNNEL, extra_headers=h)
    by_uid = {s["uid"]: s for s in node["steps"]}
    assert len(node["steps"]) == 12, f"expected 12 steps, got {len(node['steps'])}"

    only = sys.argv[2] if len(sys.argv) > 2 else None
    payload = []
    for idx, uid in STEPS.items():
        if only and str(idx) != only:
            continue
        s = by_uid[uid]
        was_str = isinstance(s["body"], str)
        body = json.loads(s["body"]) if was_str else s["body"]
        hit = convert(body)
        print(f"step {idx} {uid}: converted {len(hit)} blocks -> {hit}")
        assert len(hit) == 3, f"step {idx}: expected 3 conversions, got {len(hit)}"
        # Echo `body` back in whatever shape the API handed it to us.
        payload.append({"id": uid, "slug": s["slug"], "title": s["title"],
                        "type": s["type"], "settings": s["settings"],
                        "visual": s["visual"],
                        "body": json.dumps(body) if was_str else body})

    lf_api.gql(tok,
               "mutation($id:ID!,$node:InputFunnel!){updateFunnel(id:$id,node:$node){id}}",
               {"id": FUNNEL, "node": {"steps": payload}}, extra_headers=h)
    print("write ok")


if __name__ == "__main__":
    main()
