"""
get_token.py - One-command Lightfunnels OAuth flow (no token needed to start).

You can't avoid a human step: you must create a Partners app in the browser
to get a client_id + client_secret. Everything AFTER that is automated here.

Flow this script runs:
  1. Prints + opens the consent screen URL in your browser.
  2. You log in (if needed) and click "Accept".
  3. Lightfunnels redirects to your whitelisted redirect_uri with ?code=XXX.
     - Default: a tiny local server catches it automatically (recommended).
     - Or pass --manual to copy the code from the browser URL bar yourself.
  4. Script exchanges code -> permanent access_token and saves it to .env.

Usage:
  python3 get_token.py --client-id 9461... --client-secret abc...
  python3 get_token.py --client-id 9461... --client-secret abc... --manual
  python3 get_token.py --client-id 9461... --client-secret abc... --scope "funnels,products"

Then set the token for the bridge:
  export LF_ACCESS_TOKEN="$(grep LF_ACCESS_TOKEN .env | cut -d= -f2)"
"""
import argparse
import json
import os
import threading
import urllib.error
import urllib.parse
import urllib.request
import webbrowser
import http.server

CONSENT_URL = "https://app.lightfunnels.com/admin/oauth"
TOKEN_URL = "https://api.lightfunnels.com/oauth/access_token"
REDIRECT_URI = "http://127.0.0.1:8788/callback"

# Shared slot the callback handler fills and the main thread waits on.
_auth_code = None


class _CallbackHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        global _auth_code
        query = urllib.parse.urlparse(self.path).query
        params = urllib.parse.parse_qs(query)
        if "code" in params:
            _auth_code = params["code"][0]
            self._respond(200, "Authorization complete. You can close this tab.")
        else:
            self._respond(400, "No code in callback: " + self.path)
        self.close_connection = True

    def _respond(self, code, msg):
        body = msg.encode("utf-8")
        self.send_response(code)
        self.send_header("Content-Type", "text/plain")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, *args):
        pass  # quiet


def _exchange(client_id, client_secret, code):
    body = json.dumps({
        "client_id": client_id,
        "client_secret": client_secret,
        "code": code,
    }).encode("utf-8")
    req = urllib.request.Request(
        TOKEN_URL,
        data=body,
        headers={
            "Content-Type": "application/json",
            "Accept": "application/json",
            # Cloudflare in front of the API 403s the default Python-urllib UA.
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
                          "AppleWebKit/537.36 (KHTML, like Gecko) "
                          "Chrome/125.0 Safari/537.36",
        },
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=60) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        detail = e.read().decode("utf-8", "replace")
        raise RuntimeError(f"HTTP {e.code} from {TOKEN_URL}: {detail}") from e


def _save_env(token):
    env_path = os.path.join(os.path.dirname(__file__), ".env")
    with open(env_path, "w") as f:
        f.write(f'LF_ACCESS_TOKEN="{token}"\n')
    return env_path


def main():
    ap = argparse.ArgumentParser(description="Lightfunnels OAuth token helper")
    ap.add_argument("--client-id", required=True, help="From Partners app Configurations tab")
    ap.add_argument("--client-secret", required=True, help="From Partners app Configurations tab")
    ap.add_argument("--scope",
                    default="funnels,products,orders,customers,discounts,"
                            "analytics,settings,contact_form_data",
                    help="Comma-separated scopes (default: all documented scopes)")
    ap.add_argument("--redirect-uri", default=REDIRECT_URI,
                    help="Must match a whitelisted URI in your app config")
    ap.add_argument("--manual", action="store_true",
                    help="Don't run a local server; paste the code from the URL bar")
    args = ap.parse_args()

    consent = (f"{CONSENT_URL}?client_id={urllib.parse.quote(args.client_id)}"
               f"&redirect_uri={urllib.parse.quote(args.redirect_uri)}"
               f"&scope={urllib.parse.quote(args.scope)}&state=lfbridge")

    print("\nOpen this consent URL (also opening in browser):\n")
    print("  " + consent + "\n")
    try:
        webbrowser.open(consent)
    except Exception:
        pass

    code = None
    if args.manual:
        code = input("After accepting, copy the 'code' value from the browser URL "
                     "(...?code=XXX) and paste it here:\n> ").strip()
    else:
        print("Waiting for the OAuth redirect on", args.redirect_uri, "...")
        # Parse host/port from redirect uri
        parsed = urllib.parse.urlparse(args.redirect_uri)
        host = parsed.hostname or "127.0.0.1"
        port = parsed.port or 8788
        srv = http.server.ThreadingHTTPServer((host, port), _CallbackHandler)
        srv.timeout = 0.5
        for _ in range(600):  # ~5 min wait
            srv.handle_request()
            if _auth_code:
                break
        srv.server_close()
        code = _auth_code

    if not code:
        print("ERROR: no authorization code captured. Did you accept the consent screen?")
        return

    try:
        result = _exchange(args.client_id, args.client_secret, code)
    except Exception as e:
        print("ERROR exchanging code for token:", e)
        return

    token = result.get("access_token")
    if not token:
        print("ERROR: no access_token in response:", json.dumps(result, indent=2))
        return

    env_path = _save_env(token)
    print("\n✅ Permanent access token obtained and saved to:", env_path)
    print("   Token:", token[:12] + "…(truncated)")
    print("\nNext: start the bridge and point it at this token:")
    print("   export LF_ACCESS_TOKEN=\"" + token + "\"")
    print("   python3 server.py")


if __name__ == "__main__":
    main()
