#!/usr/bin/env python3
"""Move the 4 hand-written block stylesheets out of the body and into <head>.

Why: PSI put step 3 at 81 vs 90 for the structurally-identical test3 page, and
the entire gap was main-thread styleLayout — **2,703ms vs 271ms** — with
scriptEvaluation at 10ms on both. The pages are otherwise the same size
(11,754 vs 11,695 px tall, 1,393 vs 1,291 elements, 1,001 vs 970 CSS rules).

The one structural difference: step 3 had **5 `<style>` tags inside `<body>`**
and test3 had **0**. A stylesheet inserted mid-parse invalidates and recomputes
styles for the whole document parsed so far, so five of them scattered through a
1,393-element page means five full-document style recalcs.

Four of those five came from the HtmlElement blocks written earlier today
(hero/sec1/sec2 images + offer video). This moves their CSS into
`header_scripts`, which LF renders in `<head>`, and leaves only the markup in
the body. The rules are all id-scoped, so putting them funnel-wide is harmless:
they only match on the steps that actually contain those ids.

The 5th in-body style (`.tu-overlay`, the policy-modal block) is pre-existing and
is left alone here — same mechanism, but it is not part of today's changes.
"""
import json
import re
import sys

sys.path.insert(0, ".")
import lf_api  # noqa: E402

FUNNEL = "fun_vGqQYxn4H2i_traYYkh4w"
STEPS = {3: "step_-42yvjxEYUC-1yAzL9TKy", 11: "step_HFrpGxiibhudWV1YLEMs1"}
BLOCKS = {
    "66bf8fce-ea96-41a7-8926-34323e7fab32",  # hero
    "68a783f5-b3b0-47b5-a675-29a807f00a6a",  # sec1
    "4fb34f0f-708a-4569-8749-a8195d04205c",  # sec2
    "6db7ded9-245f-499b-b78a-8ba1ea86e513",  # offer video
}

HEAD_CSS = """<!-- PERF: block CSS lives HERE, not in the body. Moved 2026-08-06.
     These four rule sets used to sit in <style> tags inside the page body, one
     per HtmlElement block. Each in-body stylesheet forces a full-document style
     recalculation at parse time, and the four of them cost ~2.4s of main-thread
     styleLayout on a Moto G Power (2,703ms vs 271ms for an otherwise identical
     page) — worth 9 PSI points. Keep new block CSS in this file, never inline
     in a block. All rules are id-scoped so they no-op on steps without them. -->
<style>
#tub-hero-img,#tub-sec1-img,#tub-sec2-img{display:block;width:100%;max-width:100%;height:371px;object-fit:cover;border-radius:10px;}
@media (max-width:767px){#tub-hero-img{height:210px;}#tub-sec1-img,#tub-sec2-img{height:230px;}}
#tub-offer-vid{width:100%;height:auto;aspect-ratio:1328/742;border-radius:10px;display:block;background:#000;}
</style>

"""


def strip_style(content):
    """Remove a leading <style>...</style> block from an HtmlElement's content."""
    return re.sub(r"^\s*<style>.*?</style>\s*", "", content, flags=re.S)


def convert(body):
    hit = []

    def walk(n):
        if isinstance(n, dict):
            if n.get("id") in BLOCKS and n.get("t") == "HtmlElement":
                p = n.get("p") or {}
                before = p.get("content") or ""
                after = strip_style(before)
                if after != before:
                    p["content"] = after
                    hit.append(n["id"])
            for v in n.values():
                walk(v)
        elif isinstance(n, list):
            for v in n:
                walk(v)

    walk(body)
    return hit


def main():
    tok = open(".session_token").read().strip()
    acct = open(".lf_account").read().strip()
    h = lf_api.session_headers(acct)

    node = lf_api.get_funnel_steps(tok, FUNNEL, extra_headers=h)
    by_uid = {s["uid"]: s for s in node["steps"]}
    assert len(node["steps"]) == 12, f"expected 12 steps, got {len(node['steps'])}"

    payload = []
    for idx, uid in STEPS.items():
        s = by_uid[uid]
        was_str = isinstance(s["body"], str)
        body = json.loads(s["body"]) if was_str else s["body"]
        hit = convert(body)
        print(f"step {idx}: stripped in-body <style> from {len(hit)} blocks -> {hit}")
        assert len(hit) == 4, f"step {idx}: expected 4, got {len(hit)}"
        payload.append({"id": uid, "slug": s["slug"], "title": s["title"],
                        "type": s["type"], "settings": s["settings"],
                        "visual": s["visual"],
                        "body": json.dumps(body) if was_str else body})

    q = """query($q:String!){funnels(first:1,query:$q){edges{node{header_scripts}}}}"""
    hs = lf_api.gql(tok, q, {"q": f"id:{FUNNEL}"},
                    extra_headers=h)["funnels"]["edges"][0]["node"]["header_scripts"] or ""
    assert "#tub-hero-img" not in hs, "head CSS already present — aborting"
    new_hs = HEAD_CSS + hs

    lf_api.gql(tok,
               "mutation($id:ID!,$node:InputFunnel!){updateFunnel(id:$id,node:$node){id}}",
               {"id": FUNNEL, "node": {"steps": payload, "header_scripts": new_hs}},
               extra_headers=h)
    print(f"write ok — header_scripts {len(hs)} -> {len(new_hs)}")


if __name__ == "__main__":
    main()
