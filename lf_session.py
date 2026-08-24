#!/usr/bin/env python3
"""
lf_session.py — Keep a Lightfunnels dashboard session for agentic page edits.

Page-body writes require a browser session token (app tokens are platform-
blocked). Instead of copying that token out of DevTools every time it expires,
log in ONCE in a real browser. Playwright saves the session (cookies + local
storage) to .lf_state.json. After that, `refresh` reuses that saved session
headlessly to capture a fresh token + account id and write them to
.session_token / .lf_account.

No password is ever stored — only the same session data your browser keeps.
Both files are gitignored.

  python3 lf_session.py login     # one-time: opens a real browser to log in
  python3 lf_session.py refresh   # headless: writes a fresh .session_token

The `login` window stays open until it sees the dashboard make an authenticated
API call (i.e. you're signed in), then saves and closes on its own.
"""
import os
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
STATE = os.path.join(HERE, ".lf_state.json")
TOKEN_FILE = os.path.join(HERE, ".session_token")
ACCT_FILE = os.path.join(HERE, ".lf_account")

DASHBOARD = "https://app.lightfunnels.com/admin/funnels"
API_MARKER = "services.lightfunnels.com/api/v2"


def _sync_playwright():
    try:
        from playwright.sync_api import sync_playwright
        return sync_playwright
    except ImportError:
        sys.exit("Playwright not installed. Run:\n"
                 "  pip3 install playwright && python3 -m playwright install chromium")


def _capture(page, timeout_s=90):
    """Attach a request listener that grabs the Authorization bearer token and
    account-id header off the dashboard's own api/v2 calls. Returns dict or None."""
    holder = {}

    def on_request(req):
        if API_MARKER not in req.url:
            return
        headers = req.headers  # lowercased keys
        auth = headers.get("authorization", "")
        if auth.lower().startswith("bearer ") and "token" not in holder:
            holder["token"] = auth.split(" ", 1)[1].strip()
            holder["account"] = headers.get("account-id", "")

    page.on("request", on_request)
    deadline = time.time() + timeout_s
    while time.time() < deadline and "token" not in holder:
        page.wait_for_timeout(400)
    return holder if "token" in holder else None


def _write(holder):
    with open(TOKEN_FILE, "w") as f:
        f.write(holder["token"])
    os.chmod(TOKEN_FILE, 0o600)
    if holder.get("account"):
        with open(ACCT_FILE, "w") as f:
            f.write(holder["account"])
        os.chmod(ACCT_FILE, 0o600)


def login():
    """Open a real browser, let the human sign in, then save the session +
    a first token. Blocks until the dashboard makes an authenticated call."""
    sync_playwright = _sync_playwright()
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        ctx = (browser.new_context(storage_state=STATE)
               if os.path.exists(STATE) else browser.new_context())
        page = ctx.new_page()
        page.goto(DASHBOARD, wait_until="domcontentloaded", timeout=120000)
        print("A browser window opened. Log in to Lightfunnels (including 2FA if any).")
        print("This will save automatically once you're on the dashboard. Waiting...")
        holder = _capture(page, timeout_s=300)
        if not holder:
            browser.close()
            sys.exit("Did not detect a signed-in session in time. Re-run `login`.")
        ctx.storage_state(path=STATE)
        os.chmod(STATE, 0o600)
        _write(holder)
        browser.close()
    print("Saved session to .lf_state.json and a fresh token to .session_token"
          + (f" (account {open(ACCT_FILE).read()})" if os.path.exists(ACCT_FILE) else ""))


def refresh_token():
    """Headless: reuse the saved session to capture a fresh token + account.
    Returns (token, account). Raises RuntimeError if the saved session is gone
    or expired (caller should prompt a re-login)."""
    if not os.path.exists(STATE):
        raise RuntimeError("No saved session (.lf_state.json). Run: python3 lf.py login")
    sync_playwright = _sync_playwright()
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        ctx = browser.new_context(storage_state=STATE)
        page = ctx.new_page()
        try:
            page.goto(DASHBOARD, wait_until="domcontentloaded", timeout=60000)
            holder = _capture(page, timeout_s=45)
            if holder:
                # persist the possibly-rotated session too
                ctx.storage_state(path=STATE)
        finally:
            browser.close()
    if not holder:
        raise RuntimeError("Saved session expired. Run: python3 lf.py login")
    _write(holder)
    return holder["token"], holder.get("account", "")


def main():
    cmd = sys.argv[1] if len(sys.argv) > 1 else ""
    if cmd == "login":
        login()
    elif cmd == "refresh":
        tok, acct = refresh_token()
        print(f"Refreshed. Token written to .session_token (account {acct}).")
    else:
        sys.exit("Usage: python3 lf_session.py [login|refresh]")


if __name__ == "__main__":
    main()
