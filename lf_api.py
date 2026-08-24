"""
lf_api.py - Low-level Lightfunnels GraphQL client.

Single endpoint, single auth header. Everything funnels through `gql()`.
No third-party deps (stdlib only) so an agent can run it on any box.
"""
import json
import urllib.request
import urllib.error

API_URL = "https://services.lightfunnels.com/api/v2"


def gql(access_token, query, variables=None, extra_headers=None):
    """
    POST a GraphQL query/mutation to Lightfunnels.

    Returns the parsed JSON response dict. Raises RuntimeError with the
    GraphQL `errors` block on failure so agents get actionable messages.

    `extra_headers` lets a caller add the dashboard/session headers
    (`account-id`, `version`, browser Origin) needed when driving the API
    with a browser session token instead of an app token.
    """
    body = json.dumps({"query": query, "variables": variables or {}}).encode("utf-8")
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json",
        "Accept": "application/json",
        # Cloudflare fronts the API and 403s the default Python-urllib UA.
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
                      "AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/125.0 Safari/537.36",
    }
    if extra_headers:
        headers.update(extra_headers)
    req = urllib.request.Request(
        API_URL,
        data=body,
        headers=headers,
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=60) as resp:
            data = json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        detail = e.read().decode("utf-8", "replace")
        raise RuntimeError(f"HTTP {e.code}: {e.reason} — {detail}") from e
    except urllib.error.URLError as e:
        raise RuntimeError(f"Network error: {e.reason}") from e

    if "errors" in data and data["errors"]:
        raise RuntimeError(f"GraphQL errors: {json.dumps(data['errors'], indent=2)}")
    return data.get("data")


# ---------------------------------------------------------------------------
# Capture: read a master step's opaque body so we can clone it later.
# ---------------------------------------------------------------------------
# ---------------------------------------------------------------------------
# Session mode: a browser session token (not an app token) can write page
# bodies, which app tokens cannot (verified 2026-07-22). It needs the same
# extra headers the Lightfunnels dashboard sends.
# ---------------------------------------------------------------------------
def session_headers(account_id):
    return {
        "account-id": str(account_id),
        "version": "1",
        "Origin": "https://app.lightfunnels.com",
        "Referer": "https://app.lightfunnels.com/",
    }


def get_funnel_steps(access_token, funnel_id, extra_headers=None):
    # NOTE: the schema has no singular `funnel(id:)` query — only the `funnels`
    # connection. Funnel IDs are opaque strings (e.g. "fun_..."), not ints.
    # We filter the connection down to the one funnel by id.
    q = """
    query FunnelSteps($q: String!) {
      funnels(first: 1, query: $q) {
        edges {
          node {
            id uid name slug
            steps {
              id uid _id slug title type
              body
              settings
              visual { x y }
              thumbnail { key url }
            }
          }
        }
      }
    }
    """
    edges = gql(access_token, q, {"q": f"id:{funnel_id}"},
                extra_headers=extra_headers)["funnels"]["edges"]
    if not edges:
        raise RuntimeError(f"Funnel {funnel_id} not found")
    return edges[0]["node"]


def get_funnel_meta(access_token, funnel_id):
    """Like get_funnel_steps but WITHOUT step bodies. Captured bodies can be
    10MB+, so anything that only needs slug/title/type/settings must use this."""
    q = """
    query FunnelMeta($q: String!) {
      funnels(first: 1, query: $q) {
        edges {
          node {
            id uid name slug published
            steps {
              id uid _id slug title type
              settings
              visual { x y }
            }
          }
        }
      }
    }
    """
    edges = gql(access_token, q, {"q": f"id:{funnel_id}"})["funnels"]["edges"]
    if not edges:
        raise RuntimeError(f"Funnel {funnel_id} not found")
    return edges[0]["node"]


def get_step_body(access_token, funnel_id, step_uid):
    """Return the raw (opaque) body + settings JSON of a single step."""
    steps = get_funnel_steps(access_token, funnel_id)["steps"]
    for s in steps:
        if s["uid"] == str(step_uid) or s["id"] == str(step_uid):
            return s
    raise RuntimeError(f"Step {step_uid} not found in funnel {funnel_id}")


# ---------------------------------------------------------------------------
# Create: scaffold a new funnel with empty pages by StepType.
# ---------------------------------------------------------------------------
def create_funnel(access_token, name, slug, funnel_steps, currency="USD",
                  lang="en", style_id=None, product_id=None):
    """
    funnel_steps: list of StepType strings, e.g.
        ["squeeze_page", "checkout_page", "thank_you_page"]
    Returns the created funnel {id, uid, name, slug, steps:[...]}.
    """
    mutation = """
    mutation CreateFunnel($node: InputCreateFunnel!) {
      createFunnel(node: $node) {
        id uid _id name slug
        steps { id uid _id slug title type }
      }
    }
    """
    node = {
        "name": name,
        "slug": slug,
        "funnel_steps": funnel_steps,
        "currency": currency,
        "lang": lang,
    }
    if style_id is not None:
        node["style_id"] = style_id
    if product_id is not None:
        node["product_id"] = product_id
    return gql(access_token, mutation, {"node": node})["createFunnel"]


# ---------------------------------------------------------------------------
# Render: clone a captured body and swap {{tokens}}.
# ---------------------------------------------------------------------------
def render_template(captured_body, tokens):
    """
    captured_body: a JSON-serialisable object (dict/list/str) captured from
                   get_step_body(...). Opaque to us, but we can still do a
                   string token-swap because JSON is just text underneath.
    tokens: dict of { "HEADLINE": "New text", "SUBHEAD": "..." }
    Returns a new body object with all {{TOKEN}} / <<TOKEN>> replaced.
    """
    text = json.dumps(captured_body)
    for key, val in tokens.items():
        # json-encode the replacement so quotes/newlines can't corrupt the doc,
        # then strip the surrounding quotes since we splice into a JSON string.
        safe = json.dumps(str(val))[1:-1]
        text = text.replace("{{" + key + "}}", safe)
        text = text.replace("<<" + key + ">>", safe)
    return json.loads(text)


# ---------------------------------------------------------------------------
# Agentic editing: read the human-visible text out of an opaque body, and
# push targeted replacements back — no {{TOKENS}} required.
# ---------------------------------------------------------------------------
import re as _re

_SKIP_VALUE = _re.compile(
    r"^(https?://|//|#[0-9a-fA-F]{3,8}$|rgba?\(|data:|[A-Za-z0-9_\-]{22,}$"
    r"|-?\d+(\.\d+)?(px|em|rem|%|vh|vw)?$)"
)


def _looks_like_text(value):
    """Heuristic: keep strings a human would read on the page; drop URLs,
    colors, uids, css sizes and other machine values."""
    v = value.strip()
    if len(v) < 2 or not _re.search(r"[A-Za-z]", v):
        return False
    if _SKIP_VALUE.match(v):
        return False
    # single machine-ish word (identifier, class name) with no spaces
    if " " not in v and _re.fullmatch(r"[a-z0-9_\-./:@]+", v):
        return False
    return True


import html as _html

# Builder keys whose string values hold visible page copy. Verified against
# real captured bodies: rich text lives under `content` as HTML strings.
_COPY_KEYS = ("content", "text", "label", "placeholder", "button_text", "alt")


def _strip_tags(s):
    return _html.unescape(_re.sub(r"<[^>]+>", "", s)).strip()


def extract_texts(body, max_len=500):
    """Walk the opaque body JSON and return the visible page copy:
    [{key, text, html}] for every copy-key string value. `text` is the
    tag-stripped version — the string a visitor actually sees, and the exact
    form the `edit` command matches against."""
    found, seen = [], set()

    def walk(node):
        if isinstance(node, dict):
            for k, v in node.items():
                if k in _COPY_KEYS and isinstance(v, str):
                    txt = _strip_tags(v)
                    if txt and _re.search(r"[A-Za-z0-9]", txt) and txt not in seen:
                        seen.add(txt)
                        found.append({"key": k, "text": txt[:max_len]})
                else:
                    walk(v)
        elif isinstance(node, list):
            for v in node:
                walk(v)

    walk(body)
    # fallback for page types that use a different structure
    if not found:
        def walk2(node):
            if isinstance(node, dict):
                for v in node.values():
                    walk2(v)
            elif isinstance(node, list):
                for v in node:
                    walk2(v)
            elif isinstance(node, str) and _looks_like_text(node):
                t = _strip_tags(node)
                if t and t not in seen:
                    seen.add(t)
                    found.append({"key": "?", "text": t[:max_len]})
        walk2(body)
    return found


def visible_corpus(body):
    """One big string of all visible copy in a body — used to validate that
    an `edit` replacement target really exists on the page."""
    return "\n".join(t["text"] for t in extract_texts(body, max_len=100000))


def replace_in_strings(body, replacements):
    """Replace substrings ONLY inside string values (never keys, never
    structure) of the opaque body JSON.

    replacements: list of (old, new) pairs. Returns (new_body, counts) where
    counts maps each `old` to the number of string values it was found in.
    Raises if any `old` matched nothing, so agents fail loudly on typos.
    """
    counts = {old: 0 for old, _ in replacements}

    def walk(node):
        if isinstance(node, dict):
            return {k: walk(v) for k, v in node.items()}
        if isinstance(node, list):
            return [walk(v) for v in node]
        if isinstance(node, str):
            out = node
            for old, new in replacements:
                if old in out:
                    counts[old] += 1
                    out = out.replace(old, new)
            return out
        return node

    new_body = walk(body)
    missing = [old for old, n in counts.items() if n == 0]
    if missing:
        raise RuntimeError(
            "No match found for replacement target(s): "
            + json.dumps(missing)
            + " — run the `texts` command and copy the exact current text."
        )
    return new_body, counts


# ---------------------------------------------------------------------------
# Update: push a rendered body into a step.
# ---------------------------------------------------------------------------
def update_step(access_token, funnel_id, step_uid, rendered_body, title=None,
                slug=None, settings=None, step_type=None):
    """
    ⚠️ PLATFORM-BLOCKED for app tokens (verified 2026-07-22): updateFunnel
    rejects the `steps` property for third-party apps with
    `non_allowed_app_funnel_update` ("Apps are not allowed to update: steps,
    deleted_steps, styles, smart_sections"). Kept only in case Lightfunnels
    lifts the restriction. Use duplicate_funnel + header_scripts patching
    (render_patch) instead.
    """
    mutation = """
    mutation UpdateFunnel($id: ID!, $node: InputFunnel!) {
      updateFunnel(id: $id, node: $node) {
        id
        steps { uid slug title type }
      }
    }
    """
    # updateFunnel requires the full step shape (slug/title/type/settings/visual)
    # on every step in the input, so always read the live step and echo back
    # anything the caller didn't override.
    cur = None
    for s in get_funnel_meta(access_token, funnel_id)["steps"]:
        if s["uid"] == str(step_uid) or s["id"] == str(step_uid):
            cur = s
            break
    if cur is None:
        raise RuntimeError(f"Step {step_uid} not found in funnel {funnel_id}")
    step = {
        "id": str(step_uid),
        "body": rendered_body,
        "title": title if title is not None else cur["title"],
        "slug": slug if slug is not None else cur["slug"],
        "type": step_type if step_type is not None else cur["type"],
        "settings": settings if settings is not None else cur["settings"],
    }
    # InputStepVisual is {x, y}; a secondary validator requires it present.
    vis = cur.get("visual")
    if vis is not None:
        step["visual"] = {"x": vis.get("x"), "y": vis.get("y")}
    node = {"steps": [step]}
    return gql(access_token, mutation, {"id": funnel_id, "node": node})["updateFunnel"]


def edit_step_bodies(access_token, funnel_id, replacements, extra_headers=None,
                     force=False, step_uids=None):
    """REAL page-copy edit (session token only). Reads every step, replaces
    text inside the actual page body JSON, and writes changed steps back via
    updateFunnel.steps. Unlike the header_scripts patch, this persists to the
    real page (visible in the LF editor, good for SEO).

    replacements: list of (old, new). Returns a summary dict.
    Verified non-destructive: updateFunnel upserts steps by id, so unedited
    steps are left untouched.
    """
    funnel = get_funnel_steps(access_token, funnel_id, extra_headers=extra_headers)
    steps = funnel["steps"]

    # Scope to specific steps. Essential on a multi-market funnel: this account
    # has one funnel holding UK/DE/AU/CA/TH advertorials as sibling steps, so a
    # blanket domain or copy replace would rewrite the wrong market's links.
    if step_uids:
        want = set(step_uids)
        steps = [s for s in steps if s["uid"] in want or s["id"] in want]
        missing_steps = want - {s["uid"] for s in steps} - {s["id"] for s in steps}
        if missing_steps:
            raise RuntimeError(f"step(s) not in funnel {funnel_id}: {sorted(missing_steps)}")

    if not force:
        corpus = "\n".join(visible_corpus(s.get("body")) for s in steps)
        missing = [old for old, _ in replacements if old not in corpus]
        if missing:
            raise RuntimeError(
                "Not found in any page body: " + json.dumps(missing)
                + " — run `texts` and copy the exact string, or pass force=True.")

    changed, counts = [], {old: 0 for old, _ in replacements}
    for s in steps:
        if s.get("body") is None:
            continue
        new_body, c = _apply_to_body(s["body"], replacements)
        hit = sum(c.values())
        if hit:
            for k, v in c.items():
                counts[k] += v
            changed.append({
                "id": s["uid"], "slug": s["slug"], "title": s["title"],
                "type": s["type"], "settings": s["settings"],
                "visual": s["visual"], "body": new_body,
            })

    if not changed:
        return {"funnel_id": funnel_id, "steps_changed": 0, "replacements": counts}

    mutation = """
    mutation EditBodies($id: ID!, $node: InputFunnel!) {
      updateFunnel(id: $id, node: $node) { id steps { uid } }
    }
    """
    gql(access_token, mutation, {"id": funnel_id, "node": {"steps": changed}},
        extra_headers=extra_headers)
    return {"funnel_id": funnel_id, "steps_changed": len(changed),
            "replacements": counts,
            "edited_steps": [c["id"] for c in changed]}


def _apply_to_body(body, replacements):
    """Replace text inside string values of one body. Two match strategies,
    tried in order per value:
      1. raw substring — `old` appears literally (keeps surrounding markup).
      2. block match — the value's tag-stripped text equals `old`; the whole
         value is replaced with `new`. Handles copy stored with inline HTML
         (e.g. a headline wrapped in <font>/<div>/<b>), where the visible text
         never matches the raw string.
    Returns (new_body, counts). Never raises on no-match (caller aggregates)."""
    counts = {old: 0 for old, _ in replacements}

    def walk(node):
        if isinstance(node, dict):
            return {k: walk(v) for k, v in node.items()}
        if isinstance(node, list):
            return [walk(v) for v in node]
        if isinstance(node, str):
            out = node
            stripped = _strip_tags(out) if "<" in out else None
            for old, new in replacements:
                if old in out:                                   # 1. raw
                    counts[old] += 1
                    out = out.replace(old, new)
                elif stripped is not None and old.strip() == stripped.strip():
                    counts[old] += 1                              # 2. whole block
                    out = new
                    stripped = _strip_tags(out) if "<" in out else out
            return out
        return node

    return walk(body), counts


def publish_funnel(access_token, funnel_id, published=True):
    mutation = """
    mutation Pub($id: ID!, $node: InputFunnel!) {
      updateFunnel(id: $id, node: $node) { id published }
    }
    """
    return gql(access_token, mutation,
               {"id": funnel_id, "node": {"published": published}})["updateFunnel"]


def import_image(access_token, url, extra_headers=None):
    """Import an image from any URL into the LF media library (session token).
    Returns the LF image dict. Map into an Image block as:
        src_id  = result["_id"]      (numeric)
        src_uid = result["uid"]      ("img_...")
        src     = result["path"]     (assets.lightfunnels.com URL)
    LF-hosted images size correctly in flex rows; external hotlinks do not."""
    mutation = """
    mutation ImportImage($url: String!) {
      importImage(url: $url) { id _id uid title path key resource_type }
    }
    """
    return gql(access_token, mutation, {"url": url},
               extra_headers=extra_headers)["importImage"]


def image_block_from(img):
    """Build the src fields for an Image block from an import_image result."""
    return {"src_id": img["_id"], "src_uid": img["uid"], "src": img["path"]}


def duplicate_funnel(access_token, funnel_id, extra_headers=None):
    """Full server-side clone of a funnel INCLUDING all pages/content.
    This is the only way an app token can produce a funnel with real pages —
    the platform forbids apps from writing step bodies (see PLATFORM LIMITS
    in SKILL.md).

    `extra_headers` must be passed in session mode (`session_headers(account_id)`);
    without it a session token is rejected with `errors_fix_version`.

    NOTE: the clone inherits `published` from the source, so unpublish it right
    away unless you mean it to be live."""
    mutation = """
    mutation Dup($fid: ID!) {
      duplicateFunnel(funnel_id: $fid) {
        id uid _id name slug published
        steps { id uid _id slug title type }
      }
    }
    """
    return gql(access_token, mutation, {"fid": funnel_id},
               extra_headers=extra_headers)["duplicateFunnel"]


# ---------------------------------------------------------------------------
# Copy patching via header_scripts.
#
# Apps cannot write step bodies (platform rule: non_allowed_app_funnel_update),
# but they CAN write the funnel-level `header_scripts`. We inject one managed
# <script> that swaps exact text strings in the rendered DOM. The replacement
# map is stored base64-encoded on the tag so later edits can merge with it.
# ---------------------------------------------------------------------------
import base64 as _b64

_PATCH_RE = _re.compile(
    r'<script id="lf-agent-patch" data-map="([^"]*)">.*?</script>\s*', _re.S)

_PATCH_JS = """<script id="lf-agent-patch" data-map="%(b64)s">
(function(){
  var R = JSON.parse(atob(document.getElementById('lf-agent-patch').getAttribute('data-map')));
  function apply(root){
    if (!root) return;
    var w = document.createTreeWalker(root, NodeFilter.SHOW_TEXT), n;
    while ((n = w.nextNode())) {
      var t = n.nodeValue, o = t;
      for (var i = 0; i < R.length; i++) {
        if (t.indexOf(R[i][0]) !== -1) t = t.split(R[i][0]).join(R[i][1]);
      }
      if (t !== o) n.nodeValue = t;
    }
  }
  function run(){ apply(document.body); }
  if (document.readyState !== 'loading') run();
  else document.addEventListener('DOMContentLoaded', run);
  new MutationObserver(run).observe(document.documentElement,
    {childList: true, subtree: true});
})();
</script>"""


def read_patch_map(header_scripts):
    """Return the replacement list currently stored in header_scripts."""
    m = _PATCH_RE.search(header_scripts or "")
    if not m:
        return []
    try:
        return json.loads(_b64.b64decode(m.group(1)).decode("utf-8"))
    except Exception:
        return []


def render_patch(header_scripts, replacements):
    """Return new header_scripts with the managed patch block set to
    `replacements` ([[old, new], ...]). Empty list removes the block.
    Non-patch content in header_scripts is preserved."""
    rest = _PATCH_RE.sub("", header_scripts or "").rstrip()
    if not replacements:
        return rest
    b64 = _b64.b64encode(
        json.dumps(replacements, ensure_ascii=False).encode("utf-8")).decode("ascii")
    block = _PATCH_JS % {"b64": b64}
    return (rest + "\n" + block) if rest else block


def get_header_scripts(access_token, funnel_id):
    q = """
    query HS($q: String!) {
      funnels(first: 1, query: $q) { edges { node { id header_scripts } } }
    }
    """
    edges = gql(access_token, q, {"q": f"id:{funnel_id}"})["funnels"]["edges"]
    if not edges:
        raise RuntimeError(f"Funnel {funnel_id} not found")
    return edges[0]["node"].get("header_scripts") or ""


def update_funnel_fields(access_token, funnel_id, node):
    """Generic updateFunnel for top-level fields (name, slug, published, ...).
    See InputFunnel in docs/LIGHTFUNNELS_API.md for the allowed keys."""
    mutation = """
    mutation UpdateFunnelFields($id: ID!, $node: InputFunnel!) {
      updateFunnel(id: $id, node: $node) { id uid name slug published }
    }
    """
    return gql(access_token, mutation,
               {"id": funnel_id, "node": node})["updateFunnel"]


def delete_funnels(access_token, funnel_ids):
    """Delete one or more funnels. IRREVERSIBLE — callers must confirm."""
    mutation = """
    mutation DeleteFunnels($items: [ID!]!) {
      deleteFunnels(items: $items)
    }
    """
    return gql(access_token, mutation, {"items": list(funnel_ids)})["deleteFunnels"]


def list_funnels(access_token, first=20):
    q = """
    query Funnels($first: Int) {
      funnels(first: $first, query: "order_by:id order_dir:desc") {
        count
        edges { node { id uid name slug published } }
      }
    }
    """
    return gql(access_token, q, {"first": first})["funnels"]


def upload_local_image(access_token, filepath, extra_headers=None, content_type="image/png"):
    """Upload a LOCAL image file into the LF media library (session token) via the
    presigned S3 flow, then importImage the resulting CDN url to get a proper record.
    Returns {"src_id","src_uid","src"} ready to drop into an Image block.

    Note: the presigned policy caps uploads at 5 MB — resize first if larger
    (e.g. `sips -Z 1400 in.png --out out.png`). See references/block-schema.md.
    """
    import os, uuid as _uuid, urllib.request as _u, urllib.error as _e
    name = "lf-" + _uuid.uuid4().hex[:8] + "-" + os.path.basename(filepath)
    sign = """mutation($inputs:[UploadFormInput!]!){ getSignedUrls(inputs:$inputs){ url fields } }"""
    form = gql(access_token, sign, {"inputs": [{"name": name, "owner": "account",
              "resourceType": "images_library", "contentType": content_type}]},
              extra_headers=extra_headers)["getSignedUrls"][0]
    fields = form["fields"]
    boundary = "----lf" + _uuid.uuid4().hex
    pre = b""
    for k, v in fields.items():
        pre += ("--%s\r\nContent-Disposition: form-data; name=\"%s\"\r\n\r\n%s\r\n" % (boundary, k, v)).encode()
    pre += ("--%s\r\nContent-Disposition: form-data; name=\"file\"; filename=\"f\"\r\nContent-Type: %s\r\n\r\n" % (boundary, content_type)).encode()
    with open(filepath, "rb") as fh:
        payload = pre + fh.read() + ("\r\n--%s--\r\n" % boundary).encode()
    req = _u.Request(form["url"], data=payload, method="POST",
                     headers={"Content-Type": "multipart/form-data; boundary=%s" % boundary})
    try:
        with _u.urlopen(req, timeout=180) as r:
            status = r.status
    except _e.HTTPError as ex:
        raise RuntimeError("S3 upload failed %s: %s" % (ex.code, ex.read().decode("utf-8", "replace")[:200]))
    if status not in (200, 201, 204):
        raise RuntimeError("S3 upload unexpected status %s" % status)
    cdn = "https://assets.lightfunnels.com/" + fields["key"]
    im = import_image(access_token, cdn, extra_headers=extra_headers)
    return {"src_id": im["_id"], "src_uid": im["uid"], "src": im["path"]}
