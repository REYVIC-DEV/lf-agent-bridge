#!/usr/bin/env python3
"""Rebuild the offer video block: lazy-load it, shrink it, and shrink its poster.

The block was 3,256 KiB of the page's 3,869 KiB total — 84% — for a 6.3s muted
loop that sits **14 screens below the fold** and renders at 351x196 on mobile.
Three separate faults, fixed independently:

1. It downloaded on page load. `preload="metadata"` was already set, but
   `autoplay` overrides it — Chrome fetches the whole file to satisfy autoplay.
   Now the sources are attached by an IntersectionObserver, so the bytes are not
   requested until the reader is within 400px of the video.

2. The file was 1934x1080 at 4.23 Mbps for a 664 CSS px slot. Re-encoded to
   1328x742 H.264 CRF 30: 3,256 KiB -> 403 KiB, mean SSIM 0.9888 against the
   downscaled original.

3. The poster was a raw 107 KiB JPG. `poster` takes a single URL and gets no
   srcset injection from LF, so it was serving full size. Routed through the
   Cloudflare resizer at 750w it is 16.1 KiB AVIF.

**Why there are two <source> elements.** The re-encoded file is in the LF media
library, which serves it as `content-type: image/mp4` — the library is
image-oriented and does not special-case video. Chromium sniffs the container
and plays it (verified: readyState 4, 1328x742, playing). WebKit is stricter
about media Content-Type and could not be tested here, and iOS is a large share
of this funnel's traffic. So the original Shopify MP4 — correct `video/mp4`,
untouched — is listed as a second source. Browsers walk the source list on load
failure, so a browser that rejects the first gets exactly today's behaviour.
Never collapse this to a single `src`.
"""
import json
import sys

sys.path.insert(0, ".")
import lf_api  # noqa: E402

FUNNEL = "fun_vGqQYxn4H2i_traYYkh4w"
STEPS = {3: "step_-42yvjxEYUC-1yAzL9TKy", 11: "step_HFrpGxiibhudWV1YLEMs1"}
BLOCK = "6db7ded9-245f-499b-b78a-8ba1ea86e513"

PRIMARY = ("https://assets.lightfunnels.com/account-90380/images_library/"
           "89a09ebb-ffe8-4bd2-9981-5bcb017a31c2.mp4")
FALLBACK = "https://cdn.shopify.com/videos/c/o/v/e8121868d6304a34bdb191a9b1e36fac.mp4"
POSTER_ORIGIN = ("https://assets.lightfunnels.com/account-90380/images_library/"
                 "cbb3d1d6-c878-4426-ac99-d516136e44c3.jpg")
POSTER = ("https://assets.lightfunnels.com/cdn-cgi/image/"
          f"width=750,quality=80,format=auto/{POSTER_ORIGIN}")

CONTENT = f"""<style>
#tub-offer-vid{{width:100%;height:auto;aspect-ratio:1328/742;border-radius:10px;display:block;background:#000;}}
</style>
<video id="tub-offer-vid" width="1328" height="742"
  autoplay loop muted playsinline preload="none"
  poster="{POSTER}"
  data-src="{PRIMARY}"
  data-fallback="{FALLBACK}"></video>
<script>
(function () {{
  var v = document.getElementById('tub-offer-vid');
  if (!v) return;
  var done = false;
  function load() {{
    if (done) return;
    done = true;
    // Two sources, not one: the browser falls through to the Shopify original
    // if it refuses the LF copy's image/mp4 content-type. See swap_video.py.
    [v.dataset.src, v.dataset.fallback].forEach(function (u) {{
      var s = document.createElement('source');
      s.type = 'video/mp4';
      s.src = u;
      v.appendChild(s);
    }});
    v.load();
    var p = v.play();
    if (p && p.catch) p.catch(function () {{}});
  }}
  if ('IntersectionObserver' in window) {{
    var io = new IntersectionObserver(function (es) {{
      for (var i = 0; i < es.length; i++) {{
        if (es[i].isIntersecting) {{ io.disconnect(); load(); return; }}
      }}
    }}, {{rootMargin: '400px 0px'}});
    io.observe(v);
  }} else {{
    load();
  }}
}})();
</script>
"""


def convert(body):
    hit = []

    def walk(n):
        if isinstance(n, dict):
            for v in n.values():
                walk(v)
        elif isinstance(n, list):
            for i, v in enumerate(n):
                if isinstance(v, dict) and v.get("id") == BLOCK:
                    n[i] = {"t": "HtmlElement", "id": BLOCK,
                            "p": {"content": CONTENT},
                            "styles": [{"prop": "width", "value": "100%"}]}
                    hit.append(BLOCK)
                else:
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

    only = sys.argv[1] if len(sys.argv) > 1 else None
    payload = []
    for idx, uid in STEPS.items():
        if only and str(idx) != only:
            continue
        s = by_uid[uid]
        was_str = isinstance(s["body"], str)
        body = json.loads(s["body"]) if was_str else s["body"]
        hit = convert(body)
        print(f"step {idx} {uid}: converted {len(hit)}")
        assert len(hit) == 1, f"step {idx}: expected 1 conversion, got {len(hit)}"
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
