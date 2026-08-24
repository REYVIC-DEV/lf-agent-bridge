#!/usr/bin/env python3
"""
RETIRED -- do not use. Nothing in this repo imports it; it is kept only as a
record of how the REST path worked.

This project reads Figma through the figwright MCP (`mcp__figwright__*`), which
talks to the Figma Plugin API locally and has no seat cap. The REST API here is
per-seat rate limited: a View/Collab seat gets roughly SIX Tier-1 calls a MONTH
(GET file / nodes / images), and a 429 has been observed with Retry-After of
~4.6 days. One accidental call can block design work for the rest of the week.

If figwright will not connect, the fix is for the human to open the file in
Figma with the Figwright plugin running -- not to fall back to this module.

See .claude/skills/lightfunnels/references/figma-inspect.md.
"""
import os
import sys

if os.environ.get("FIGMA_REST_I_KNOW_ITS_RETIRED") != "1":
    sys.stderr.write(
        "\nfigma_rest.py is RETIRED in this project -- use the figwright MCP.\n"
        "It burns a per-month API quota that takes ~4.6 days to recover.\n"
        "If you genuinely need it, the human sets "
        "FIGMA_REST_I_KNOW_ITS_RETIRED=1.\n\n")
    raise SystemExit(2)

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
