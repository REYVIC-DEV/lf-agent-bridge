#!/usr/bin/env python3
"""Delete the leftover `event-v2` step.

It exists because the first build shipped to a spare slug: the builder correctly
refused to authorise its own redeploy onto the live `event` page. Once the build
was promoted to `event`, this became a full duplicate of the page serving 200.

There is no deleteStep mutation - deleteStep/deleteSteps/removeStep/archiveStep
are all absent. Removal goes through `InputFunnel.deleted_steps`, which is what
the dashboard uses.

Guards, because this is destructive and irreversible through the API:
  - the step must NOT be starting_step_id
  - the KEEPER step must exist, be the entry, and be serving the real page
  - the full step record is written to steps/ first, as the reversal path
  - the node carries ONLY deleted_steps, so nothing else can change
"""
import io, json, os, sys, time, urllib.request
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", "..", "..", ".."))
sys.path.insert(0, ROOT); os.chdir(ROOT)
import lf_api

FUNNEL = "fun_RoOL_WXDCAxK4hEk0v5xX"
DOOMED = "step_Wl7z21c5B9Fdkg4YzXLzV"   # event-v2
KEEPER = "step_5BIwggYOWxmrOPnAyaVPi"   # event, the entry
BACKUP = os.path.join(HERE, "..", "steps", "event-v2.pre-delete-2026-10-06.json")
APPLY = "--apply" in sys.argv

tok  = open(".session_token").read().strip()
acct = open(".lf_account").read().strip()
h    = lf_api.session_headers(acct)
Q = '''query($id:ID!){node(id:$id){... on Funnel{slug starting_step_id steps{
      uid slug title type product_id settings visual{x y} body}}}}'''

n = lf_api.gql(tok, Q, {"id": FUNNEL}, extra_headers=h)["node"]
by = {s["uid"]: s for s in n["steps"]}
print("funnel /%s, %d step(s): %s" % (n["slug"], len(n["steps"]),
      ", ".join("%s%s" % (s["slug"], "*" if s["uid"] == n["starting_step_id"] else "")
                for s in n["steps"])))

assert DOOMED in by, "event-v2 is already gone"
assert KEEPER in by, "the keeper step is missing - stopping"
assert n["starting_step_id"] != DOOMED, "refusing to delete the ENTRY step"
assert n["starting_step_id"] == KEEPER, "entry is not the keeper - stopping"

# the keeper must actually be serving the real page before anything is removed
u = "https://www.techunboxed.co/%s/?cb=%d" % (n["slug"], time.time())
b = urllib.request.urlopen(urllib.request.Request(
    u, headers={"User-Agent": "Mozilla/5.0", "Cache-Control": "no-cache"}), timeout=90
    ).read().decode("utf-8", "replace")
assert b.count("<h1") == 1 and b.count("sof-sec") > 10, \
    "the keeper is not serving the built page - stopping"
print("keeper /%s/ serves the real page (h1=1, %d sections)" % (n["slug"], b.count("sof-sec")))

io.open(BACKUP, "w", encoding="utf-8").write(json.dumps(by[DOOMED], indent=1))
print("backed up event-v2 -> %s (%d bytes)" % (os.path.relpath(BACKUP, ROOT),
                                               os.path.getsize(BACKUP)))
if not APPLY:
    sys.exit("(dry run - nothing deleted)")

lf_api.gql(tok, "mutation($id:ID!,$node:InputFunnel!){updateFunnel(id:$id,node:$node){id}}",
           {"id": FUNNEL, "node": {"deleted_steps": [DOOMED]}}, extra_headers=h)
print("deleted")
time.sleep(8)

n = lf_api.gql(tok, Q, {"id": FUNNEL}, extra_headers=h)["node"]
print("\nafter: %d step(s): %s" % (len(n["steps"]),
      ", ".join(s["slug"] for s in n["steps"])))
for path in ["/%s/" % n["slug"], "/%s/event" % n["slug"], "/%s/event-v2" % n["slug"]]:
    try:
        r = urllib.request.urlopen(urllib.request.Request(
            "https://www.techunboxed.co" + path + "?cb=%d" % time.time(),
            headers={"User-Agent": "Mozilla/5.0", "Cache-Control": "no-cache"}), timeout=90)
        print("  %-20s HTTP %s" % (path, r.status))
    except Exception as e:
        print("  %-20s %s" % (path, str(e)[:40]))
