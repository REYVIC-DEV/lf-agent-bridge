#!/usr/bin/env python3
"""Install the house Lenis block on the Scaling or Failing funnel.

FUNNEL LEVEL, in header_scripts, never per step: that is where smooth scroll
lives on this account, and a per-step copy would be a second library running a
second rAF loop against one scrollTop.

Lenis normally arrives as part of the mandatory tracker header. This funnel is a
separate event brand on its own future domain, so the tracker block is NOT
installed here - it carries HLTH's Taboola/Outbrain/Aimerce pixels and the HLTH
PostHog projects, which have no business firing on an event page. Only the
smooth-scroll section is taken. If this funnel should also report into HLTH's
analytics, that is a separate decision and a separate install.

It matters here beyond feel: every nav item is an in-page anchor, and Lenis is
what makes those eased rather than jump cuts. Desktop only - mobile already does
momentum scrolling natively and the library is not even downloaded there.
"""
import io, os, re, sys, time, urllib.request
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", "..", "..", ".."))
sys.path.insert(0, ROOT); os.chdir(ROOT)
import lf_api

FUNNEL = "fun_RoOL_WXDCAxK4hEk0v5xX"
URL = "https://www.techunboxed.co/scaling-or-failing/event"
SRC = os.path.join(ROOT, "snippets", "tracker-header-meta-block.html")
MARK = "<!-- Smooth scroll"

lines = io.open(SRC, encoding="utf-8", newline="").read().split("\n")
start = next(i for i, l in enumerate(lines) if MARK in l)
end = next(i for i, l in enumerate(lines[start:], start) if l.strip() == "</script>")
block = "\n".join(lines[start:end + 1]).strip()
assert block.startswith(MARK), "block does not start at the marker"
assert "unpkg.com/lenis@1" in block and "pointer: coarse" in block
assert block.count("<script>") == 1 and block.count("</script>") == 1
assert "posthog" not in block.lower() and "googletagmanager" not in block.lower(), \
    "tracker code leaked into the lenis extract"
print("extracted lenis block: %d chars (lines %d-%d of the tracker header)"
      % (len(block), start + 1, end + 1))

tok = open(".session_token").read().strip()
acct = open(".lf_account").read().strip()
h = lf_api.session_headers(acct)
Q = 'query($id:ID!){node(id:$id){... on Funnel{name header_scripts}}}'
n = lf_api.gql(tok, Q, {"id": FUNNEL}, extra_headers=h)["node"]
cur = n.get("header_scripts") or ""
print("funnel %s: header_scripts=%d chars" % (n["name"], len(cur)))
if "lenis" in cur.lower():
    sys.exit("Lenis already present. Nothing to do.")

new = (cur.rstrip() + "\n\n" + block + "\n") if cur.strip() else (block + "\n")
lf_api.gql(tok, "mutation($id:ID!,$node:InputFunnel!){updateFunnel(id:$id,node:$node){id}}",
           {"id": FUNNEL, "node": {"header_scripts": new}}, extra_headers=h)
print("installed: %d -> %d chars" % (len(cur), len(new)))

time.sleep(10)
b = urllib.request.urlopen(urllib.request.Request(
    URL + "?cb=%d" % time.time(),
    headers={"User-Agent": "Mozilla/5.0", "Cache-Control": "no-cache"}), timeout=90
    ).read().decode("utf-8", "replace")
print("served: lenis refs=%d  unpkg=%d  html.lenis rule=%d  posthog=%d"
      % (b.lower().count("lenis"), b.count("unpkg.com/lenis"),
         b.count("html.lenis"), len(re.findall("posthog", b, re.I))))
