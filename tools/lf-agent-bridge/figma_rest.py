"""
figma_rest.py - Read Figma designs via the official REST API (no MCP, stdlib only).

Why this exists: the Figma *MCP* server caps tool calls per seat (a "View seat"
on Professional hits a hard limit fast). The Figma REST API has its own, far more
generous limits and is completely independent of that cap. With one personal
access token (scope: File content -> Read-only) you can read the full node tree
(geometry, auto-layout, fills/colors, typography, components) AND export any
frame to PNG/SVG. That is everything needed to rebuild a design as LF blocks.

Token: create at Figma -> Settings -> Security -> Personal access tokens
(File content = Read-only). Store as FIGMA_TOKEN in .env (gitignored). Never log it.

Endpoints used:
  GET /v1/files/:key/nodes?ids=A,B   -> node JSON (style/geometry/text/layout)
  GET /v1/images/:key?ids=A,B&format=png&scale=2  -> {id: temporary render URL}
  GET /v1/files/:key/nodes           -> full subtree

fileKey + nodeId come from a Figma URL:
  https://www.figma.com/design/:fileKey/:name?node-id=1640-2196
  -> fileKey, nodeId "1640:2196" (dash becomes colon).
"""
import json, os, urllib.request, urllib.parse, urllib.error

API = "https://api.figma.com/v1"


def token(env_path=".env"):
    t = os.environ.get("FIGMA_TOKEN")
    if not t and os.path.exists(env_path):
        for line in open(env_path):
            if line.startswith("FIGMA_TOKEN="):
                t = line.split("=", 1)[1].strip().strip('"').strip("'")
    if not t:
        raise RuntimeError("FIGMA_TOKEN not set (env or .env)")
    return t


def _get(url, tok, retries=5):
    import time
    req = urllib.request.Request(url, headers={"X-Figma-Token": tok})
    for attempt in range(retries):
        try:
            with urllib.request.urlopen(req, timeout=120) as r:
                return json.loads(r.read())
        except urllib.error.HTTPError as e:
            if e.code == 429 and attempt < retries - 1:
                time.sleep(5 * (attempt + 1))  # 5,10,15,20s backoff on rate limit
                continue
            raise RuntimeError("Figma REST %s: %s" % (e.code, e.read().decode("utf-8", "replace")[:300]))


def get_nodes(file_key, node_ids, tok=None, geometry=False):
    """Return {node_id: node_document} for the given ids."""
    tok = tok or token()
    ids = ",".join(node_ids)
    url = "%s/files/%s/nodes?ids=%s%s" % (API, file_key, urllib.parse.quote(ids),
                                          "&geometry=paths" if geometry else "")
    data = _get(url, tok)
    return {k: v["document"] for k, v in data["nodes"].items() if v}


def export_images(file_key, node_ids, tok=None, fmt="png", scale=2):
    """Return {node_id: temporary_render_url}. URLs expire (~hours) — download now."""
    tok = tok or token()
    ids = ",".join(node_ids)
    url = "%s/images/%s?ids=%s&format=%s&scale=%s" % (API, file_key, urllib.parse.quote(ids), fmt, scale)
    return _get(url, tok)["images"]


def download(url, dest):
    urllib.request.urlretrieve(url, dest)
    return dest
