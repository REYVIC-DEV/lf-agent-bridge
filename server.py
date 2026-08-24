"""
server.py - The agent-facing bridge.

Run:  python3 server.py
Then any agentic coder (Claude Code, Codex, Cursor, a shell) can:

  1. CAPTURE a master page built in the Lightfunnels editor:
     curl -s localhost:8787/capture -X POST -H 'Content-Type: application/json' \
       -d '{"token":"<LF_TOKEN>","funnel_id":123456,"step_uid":"abc","name":"squeeze_master"}'
        -> saves templates/squeeze_master.json  (the opaque body, captured verbatim)

  2. BUILD a variant funnel by cloning + token-swapping those masters:
     curl -s localhost:8787/build -X POST -H 'Content-Type: application/json' -d @variant.json

The agent NEVER invents page structure. It only reuses Lightfunnels' own
JSON (captured in step 1) and swaps {{TOKENS}}. That is the only reliable
path given body/settings are opaque scalars.

Set LF_ACCESS_TOKEN in the environment to omit "token" from every call.
"""
import json
import os
import urllib.parse
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

import lf_api

TEMPLATES_DIR = os.path.join(os.path.dirname(__file__), "templates")
os.makedirs(TEMPLATES_DIR, exist_ok=True)


def _token(req_body):
    return req_body.get("token") or os.environ.get("LF_ACCESS_TOKEN")


def _save_template(name, payload):
    path = os.path.join(TEMPLATES_DIR, f"{name}.json")
    with open(path, "w") as f:
        json.dump(payload, f, indent=2)
    return path


def _load_template(name):
    path = os.path.join(TEMPLATES_DIR, f"{name}.json")
    if not os.path.exists(path):
        raise RuntimeError(f"Template '{name}' not captured. Run /capture first.")
    with open(path) as f:
        return json.load(f)


class Handler(BaseHTTPRequestHandler):
    def _send(self, code, obj):
        self.send_response(code)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(json.dumps(obj).encode("utf-8"))

    def _body(self):
        length = int(self.headers.get("Content-Length", 0))
        if not length:
            return {}
        return json.loads(self.rfile.read(length).decode("utf-8"))

    def do_GET(self):
        parsed = urllib.parse.urlparse(self.path)
        if parsed.path == "/health":
            return self._send(200, {"status": "ok"})
        if parsed.path == "/templates":
            files = [f[:-5] for f in os.listdir(TEMPLATES_DIR) if f.endswith(".json")]
            return self._send(200, {"templates": files})
        if parsed.path == "/funnels":
            qs = urllib.parse.parse_qs(parsed.query)
            token = qs.get("token", [os.environ.get("LF_ACCESS_TOKEN", "")])[0]
            try:
                data = lf_api.list_funnels(token)
                return self._send(200, data)
            except RuntimeError as e:
                return self._send(502, {"error": str(e)})
        return self._send(404, {"error": "not found"})

    def do_POST(self):
        parsed = urllib.parse.urlparse(self.path)
        try:
            body = self._body()
            if parsed.path == "/capture":
                token = _token(body)
                step = lf_api.get_step_body(token, body["funnel_id"], body["step_uid"])
                path = _save_template(body["name"], step)
                return self._send(200, {"captured": step["uid"], "saved_to": path,
                                        "type": step["type"],
                                        "tokens_found": _find_tokens(step.get("body"))})

            if parsed.path == "/build":
                token = _token(body)
                pages = body["pages"]
                page_types = [p["type"] for p in pages]
                created = lf_api.create_funnel(
                    token, body["funnel_name"], body["slug"], page_types,
                    currency=body.get("currency", "USD"),
                    lang=body.get("lang", "en"),
                    style_id=body.get("style_id"),
                    product_id=body.get("product_id"),
                )
                steps = created["steps"]
                if len(steps) != len(pages):
                    raise RuntimeError("Step count mismatch between pages and created funnel")
                results = []
                for page, step in zip(pages, steps):
                    if page.get("template"):
                        tpl = _load_template(page["template"])
                        rendered = lf_api.render_template(tpl.get("body"), page.get("tokens", {}))
                        settings = tpl.get("settings")
                    else:
                        rendered = page.get("body")  # raw body pass-through
                        settings = page.get("settings")
                    upd = lf_api.update_step(
                        token, created["id"], step["uid"], rendered,
                        title=page.get("title", step.get("title")),
                        slug=page.get("slug"),
                        settings=settings,
                    )
                    results.append({"step": step["uid"], "type": step["type"], "updated": True})
                if body.get("publish"):
                    lf_api.publish_funnel(token, created["id"], True)
                return self._send(200, {
                    "funnel_id": created["id"],
                    "funnel_uid": created["uid"],
                    "slug": created["slug"],
                    "published": bool(body.get("publish")),
                    "steps_updated": results,
                })

            return self._send(404, {"error": "not found"})
        except (RuntimeError, KeyError, ValueError) as e:
            return self._send(400, {"error": str(e)})


def _find_tokens(body):
    """Best-effort: surface {{TOKEN}} placeholders already in a captured body
    so the agent knows what it can safely swap."""
    import re
    text = json.dumps(body)
    return sorted(set(re.findall(r"\{\{([A-Z0-9_]+)\}\}", text)))


def main():
    port = int(os.environ.get("PORT", 8787))
    server = ThreadingHTTPServer(("127.0.0.1", port), Handler)
    print(f"LF agent bridge listening on http://127.0.0.1:{port}")
    print("Endpoints: /health /capture /build /templates /funnels")
    server.serve_forever()


if __name__ == "__main__":
    main()
