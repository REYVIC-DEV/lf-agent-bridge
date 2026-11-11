#!/usr/bin/env python3
"""
lf_session.py — Keep a Lightfunnels dashboard session for agentic page edits.

Page-body writes require a real dashboard session; app tokens are platform-
blocked. Log in ONCE in a real browser and Playwright saves the session
(cookies + local storage) to .lf_state.json. Everything else reuses that.

  python3 lf_session.py login     # one-time: opens a real browser to log in
  python3 lf_session.py refresh   # headless: check the saved session still works

No password is ever stored, only the session data your browser already keeps.
Both files are gitignored.

⚠️ THE API IS COOKIE-AUTHENTICATED. IT STOPPED USING BEARER TOKENS.

Captured from a real browser on 2026-10-06, the dashboard's own call:

    POST services.lightfunnels.com/api/v2
    account-id: 90380 · version: 1 · lang: en-US · referer: app.lightfunnels.com
    (no Authorization header anywhere, and no token in localStorage either)

The credential is the `lf_session` cookie. This file used to wait for an
`Authorization: Bearer` header to go past and saved the token out of it. That
header no longer exists, so the wait could never end, and BOTH `login` and
`refresh` reported "Saved session expired" at every attempt no matter how
valid the session was. Hours went into re-logging-in against a session that
was fine. If a future change breaks auth again, check what the browser
actually sends before believing a message that says the session expired.

`.session_token` is kept only so older scripts that read it still find a file.
`lf_api.gql` ignores it whenever a cookie is available.
"""
import json
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


def _signed_in(page):
    """Read the dashboard's own idea of whether it is signed in.

    It writes `logged_in` and `active_account_id` into localStorage, which is a
    far steadier signal than sniffing network headers, and it survives the API
    changing how it authenticates.
    """
    try:
        return page.evaluate(
            "() => ({ok: localStorage.getItem('logged_in') === 'true',"
            " account: localStorage.getItem('active_account_id') || ''})")
    except Exception:
        return {"ok": False, "account": ""}


def _wait_signed_in(page, timeout_s):
    deadline = time.time() + timeout_s
    while time.time() < deadline:
        st = _signed_in(page)
        if st.get("ok") and st.get("account"):
            return st
        try:
            page.wait_for_timeout(500)
        except Exception:
            return None          # window closed under us
    return None


def _save(ctx, account):
    ctx.storage_state(path=STATE)
    os.chmod(STATE, 0o600)
    if account:
        with open(ACCT_FILE, "w") as f:
            f.write(str(account))
        os.chmod(ACCT_FILE, 0o600)
    if not os.path.exists(TOKEN_FILE):      # keep older scripts from crashing
        with open(TOKEN_FILE, "w") as f:
            f.write("cookie-auth")
        os.chmod(TOKEN_FILE, 0o600)


def login():
    """Open a real browser, let the human sign in, then save the session."""
    sync_playwright = _sync_playwright()
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        ctx = (browser.new_context(storage_state=STATE)
               if os.path.exists(STATE) else browser.new_context())
        page = ctx.new_page()
        page.goto(DASHBOARD, wait_until="domcontentloaded", timeout=120000)
        print("A browser window opened. Log in to Lightfunnels (including 2FA if any).")
        print("It saves by itself once the dashboard is signed in. Leave it open.")
        st = _wait_signed_in(page, timeout_s=300)
        if not st:
            browser.close()
            sys.exit("Did not see a signed-in dashboard in time. Re-run `login`.")
        _save(ctx, st["account"])
        browser.close()
    print("Saved session to .lf_state.json (account %s)." % open(ACCT_FILE).read())


def refresh_token():
    """Headless: confirm the saved session still works and re-save it.

    Returns (token, account) to keep the old call signature. The token is a
    placeholder: the cookies in .lf_state.json are what actually authenticate.
    """
    if not os.path.exists(STATE):
        raise RuntimeError("No saved session (.lf_state.json). Run: python3 lf.py login")
    sync_playwright = _sync_playwright()
    account = ""
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        ctx = browser.new_context(storage_state=STATE)
        page = ctx.new_page()
        try:
            page.goto(DASHBOARD, wait_until="domcontentloaded", timeout=60000)
            st = _wait_signed_in(page, timeout_s=45)
            if st:
                account = st["account"]
                _save(ctx, account)
        finally:
            browser.close()
    if not account:
        raise RuntimeError("Saved session is not signed in. Run: python3 lf.py login")
    return "cookie-auth", account


def check():
    """Prove the saved cookies actually answer, rather than trusting a flag."""
    sys.path.insert(0, HERE)
    import lf_api
    acct = open(ACCT_FILE).read().strip()
    h = lf_api.session_headers(acct)
    if "Cookie" not in h:
        sys.exit("No cookies in .lf_state.json. Run: python3 lf.py login")
    d = lf_api.gql("", '{funnels(first:1,query:""){edges{node{name}}}}',
                   {}, extra_headers=h)
    name = d["funnels"]["edges"][0]["node"]["name"]
    print("Session OK (account %s). First funnel: %s" % (acct, name))


def main():
    cmd = sys.argv[1] if len(sys.argv) > 1 else ""
    if cmd == "login":
        login()
    elif cmd == "refresh":
        tok, acct = refresh_token()
        print("Refreshed. Session saved (account %s)." % acct)
    elif cmd == "check":
        check()
    else:
        sys.exit("Usage: python3 lf_session.py [login|refresh|check]")


if __name__ == "__main__":
    main()
