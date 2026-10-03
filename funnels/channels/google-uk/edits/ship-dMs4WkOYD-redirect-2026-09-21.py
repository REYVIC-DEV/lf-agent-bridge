#!/usr/bin/env python3
"""Ship the winner of experiment 91531 by making the ENTRY page redirect unconditionally.

CONTEXT
    /article/comparison-1 is the ENTRY of the Google funnel and was the *control*
    arm of PostHog experiment 91531 (GOOGLE - Comparison-1 vs dMs4WkOYD). The
    ads point at it, so the winner cannot be shipped by swapping a URL - the
    entry page has to forward. That is the "redirect method".

WHY THE FLAG IS DROPPED RATHER THAN SET TO 100%
    The old snippet gated the redirect on getFeatureFlag("google-comparison1-v2").
    Rolling the flag to 100% test would also work, but it leaves the live page
    depending on an experiment flag that is now finished: anyone deactivating or
    cleaning up that flag silently sends 100% of paid Google traffic back to the
    losing page, with nothing on the page to explain why. An unconditional
    redirect has no such coupling, and it drops the 500ms exposure delay and the
    white anti-flash cover, which only existed to let the exposure event send
    before navigating. There is no exposure left to wait for.

WHY IT FIRES SYNCHRONOUSLY
    custom_html.header lands in <head>, so location.replace() there runs before
    first paint - no flash, so no cover needed. location.replace (not .href)
    keeps comparison-1 out of session history, so Back returns to Google rather
    than bouncing the visitor through the redirect again.

WHAT IS PRESERVED
    Every query param and the hash carry over. gclid and the UTMs are load
    bearing for Google Ads conversion attribution; dropping them would break
    reporting far more visibly than the redirect itself.

WHAT IS REMOVED
    The two <link rel=preload> image tags. They prefetched comparison-1's hero
    image, which no visitor will now see - they would be pure wasted bandwidth
    in front of a redirect. They are kept in the backup.

SAFETY
    - Full prior settings + the raw header string are written to steps/ first.
    - Only the one entry step is sent; siblings survive by omission.
    - body is read and sent back unchanged (LF's StepBody scalar round-trips as
      an object - never json.dumps it).
    - Funnel-level name/slug/published/starting_step_id and the step count are
      asserted unchanged after the write.
    - --dry-run prints the diff and writes the backups without calling the API.
"""
import json
import os
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", "..", "..", ".."))
sys.path.insert(0, ROOT)
os.chdir(ROOT)
import lf_api  # noqa: E402

FUNNEL = "fun_p9Y_FwGlQsaP5bpW70q5N"
ENTRY = "step_S_MvuvpXzokqMc1OW6dxs"          # /article/comparison-1
DEST_PATH = "/article/dMs4WkOYD"
DEST_URL = "https://www.techunboxed.co" + DEST_PATH
STAMP = "2026-09-21"
BACKUP_DIR = os.path.join(HERE, "..", "steps")

DRY = "--dry-run" in sys.argv

NEW_HEADER = """<script>
/* ============================================================================
   SHIPPED WINNER - /article/comparison-1 -> /article/dMs4WkOYD   (%(stamp)s)

   PostHog experiment 91531 "GOOGLE - Comparison-1 vs dMs4WkOYD" ended
   %(stamp)s. The 'test' arm (dMs4WkOYD) is shipped to 100%% of entry traffic.

   This page is the ENTRY of the funnel and the Google Ads final URLs still
   point at it, so it forwards rather than being replaced.

   NO FEATURE FLAG IS READ. The old snippet gated this on
   google-comparison1-v2; that flag is finished and must not be able to change
   what paid traffic sees. Deactivating or deleting it has no effect here.

   INTERIM: repoint the Google Ads final URLs at the destination below and
   then delete this whole block - the hop costs every visitor a round trip.

   Append ?noredirect=1 to view this page as it was.
   ============================================================================ */
(function () {
  var DEST_URL  = "%(dest)s";
  var DEST_PATH = "%(path)s";

  // Loop guard: never forward a page that is already the destination.
  if (window.location.pathname.indexOf(DEST_PATH) !== -1) return;

  // QA escape hatch.
  if (/[?&]noredirect=1/.test(window.location.search)) return;

  var url;
  try {
    // Carry over every query param and the hash. gclid + the UTMs drive Google
    // Ads conversion attribution; losing them breaks reporting, not the page.
    var dest = new URL(DEST_URL);
    new URLSearchParams(window.location.search).forEach(function (v, k) {
      dest.searchParams.set(k, v);
    });
    dest.hash = window.location.hash;
    url = dest.toString();
  } catch (e) {
    url = DEST_URL + window.location.search + window.location.hash;
  }

  // Synchronous, in <head>, before first paint - so no anti-flash cover is
  // needed. .replace keeps this page out of history: Back goes to Google.
  window.location.replace(url);
})();
</script>
""" % {"stamp": STAMP, "dest": DEST_URL, "path": DEST_PATH}


def go(fn, tries=8):
    delay = 45
    for _ in range(tries):
        try:
            return fn()
        except Exception as e:
            m = str(e)
            if "expired" in m.lower():
                sys.exit("Session expired. Run: python3 lf.py login")
            if "rate_limit" in m or "Rate limit" in m:
                print("    rate limited, waiting %ds" % delay, flush=True)
                time.sleep(delay)
                delay = min(delay * 2, 300)
                continue
            if "502" in m or "Bad Gateway" in m:
                print("    502, backing off 70s", flush=True)
                time.sleep(70)
                continue
            raise
    raise RuntimeError("gave up")


tok = open(".session_token").read().strip()
acct = open(".lf_account").read().strip()
h = lf_api.session_headers(acct)

FQ = """query($id:ID!){node(id:$id){... on Funnel{
  name slug published starting_step_id steps{uid}}}}"""

pre = go(lambda: lf_api.gql(tok, FQ, {"id": FUNNEL}, extra_headers=h))["node"]
inv = {k: pre.get(k) for k in ("name", "slug", "published", "starting_step_id")}
nsteps = len(pre["steps"])
print("funnel: %s | slug=%s | published=%s | steps=%d" % (
    inv["name"], inv["slug"], inv["published"], nsteps))
assert inv["starting_step_id"] == ENTRY, (
    "entry step moved: expected %s, funnel says %s" % (ENTRY, inv["starting_step_id"]))

node = go(lambda: lf_api.get_funnel_steps(tok, FUNNEL, extra_headers=h))
step = next((s for s in node["steps"] if s["uid"] == ENTRY), None)
assert step is not None, "entry step %s not found" % ENTRY
assert step["slug"] == "comparison-1", "entry slug changed: %s" % step["slug"]

settings = step.get("settings") or {}
ch = settings.get("custom_html") or {}
old_header = ch.get("header") or ""

# ---- invariants on what we are replacing -------------------------------------
# Refuse to run twice, and refuse to run against a page that is not the one this
# script was written for: a blind overwrite of an unrecognised header would
# silently discard whoever edited it in between.
if DEST_PATH in old_header and "getFeatureFlag" not in old_header:
    sys.exit("Already shipped - header has no flag gate and points at the destination.")
assert "getFeatureFlag" in old_header, (
    "entry header does not contain the experiment snippet; refusing to overwrite.\n"
    "First 300 chars:\n%s" % old_header[:300])

# ---- backups -----------------------------------------------------------------
os.makedirs(BACKUP_DIR, exist_ok=True)
hdr_path = os.path.join(BACKUP_DIR, "comparison-1.custom_html_header.pre-ship-%s.html" % STAMP)
set_path = os.path.join(BACKUP_DIR, "comparison-1.settings.pre-ship-%s.json" % STAMP)
with open(hdr_path, "w", encoding="utf-8") as fh:
    fh.write(old_header)
with open(set_path, "w", encoding="utf-8") as fh:
    json.dump(settings, fh, indent=2, ensure_ascii=False)
print("backed up header  -> %s  (%d chars)" % (os.path.relpath(hdr_path, ROOT), len(old_header)))
print("backed up settings-> %s" % os.path.relpath(set_path, ROOT))

print("\n--- replacing %d chars with %d chars ---" % (len(old_header), len(NEW_HEADER)))
print("  flag CALL removed:      %s -> %s   (name stays in the comment, by design)" % (
    "getFeatureFlag" in old_header, "getFeatureFlag" in NEW_HEADER))
print("  preload tags removed:   %d -> %d" % (
    old_header.count("rel=\"preload\"") + old_header.count("rel=preload"),
    NEW_HEADER.count("rel=\"preload\"") + NEW_HEADER.count("rel=preload")))
print("  destination present:    %s" % (DEST_URL in NEW_HEADER))

if DRY:
    print("\n--- NEW HEADER ---")
    print(NEW_HEADER)
    sys.exit("\nDRY RUN - nothing written to Lightfunnels.")

ch["header"] = NEW_HEADER
settings["custom_html"] = ch

go(lambda: lf_api.gql(
    tok, "mutation($id:ID!,$node:InputFunnel!){updateFunnel(id:$id,node:$node){id}}",
    {"id": FUNNEL, "node": {"steps": [{
        "id": step["uid"],
        "slug": step["slug"],
        "title": step["title"],
        "type": step["type"],
        "settings": settings,
        "visual": step.get("visual"),
        "body": step.get("body"),      # unchanged; StepBody scalar, send the object
    }]}}, extra_headers=h))
print("\nWRITTEN.")

# ---- verify ------------------------------------------------------------------
time.sleep(2)
post = go(lambda: lf_api.gql(tok, FQ, {"id": FUNNEL}, extra_headers=h))["node"]
bad = [k for k, v in inv.items() if post.get(k) != v]
print("funnel invariants: %s | steps %s" % (
    "OK" if not bad else "CHANGED %s" % bad,
    "OK" if len(post["steps"]) == nsteps else "CHANGED %d -> %d" % (nsteps, len(post["steps"]))))
assert not bad and len(post["steps"]) == nsteps

node2 = go(lambda: lf_api.get_funnel_steps(tok, FUNNEL, extra_headers=h))
s2 = next(s for s in node2["steps"] if s["uid"] == ENTRY)
h2 = ((s2.get("settings") or {}).get("custom_html") or {}).get("header") or ""
body_same = json.dumps(s2.get("body")) == json.dumps(step.get("body"))
print("read-back: header==written %s | flag call gone %s | dest present %s | body unchanged %s" % (
    h2 == NEW_HEADER, "getFeatureFlag" not in h2, DEST_URL in h2, body_same))
assert h2 == NEW_HEADER and "getFeatureFlag" not in h2 and DEST_URL in h2
assert body_same, "step body changed - investigate before trusting this write"
print("\nDone. Verify in a browser: %s" % ("https://www.techunboxed.co/article/comparison-1"))
