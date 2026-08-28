#!/usr/bin/env python3
"""Remove the source step, completing the move.

There is no deleteStep mutation - only createStep exists for steps, and probing
confirmed deleteStep/deleteSteps/removeStep/archiveStep all absent. Removal goes
through InputFunnel.deleted_steps, which is how the dashboard does it.

Guards, because this is the destructive half:
  - asserts the step now EXISTS in the destination before removing it here, so
    the move cannot leave zero copies.
  - asserts the step is not this funnel's starting_step_id.
  - the node carries ONLY deleted_steps, so nothing else can change.
  - the full tagged body is already committed to git as the reversal path.
"""
import json
import sys
import time

sys.path.insert(0, ".")
import lf_api

SRC = "fun_f1IsXx3YnEA2UD2g91dAv"
SRC_STEP = "step_JM0a30ybnkm3hpOE7-lSW"
DST = "fun_vGqQYxn4H2i_traYYkh4w"
DST_STEP = "step_o3hE-N_cIOLHMOhl9bnml"

tok = open(".session_token").read().strip()
acct = open(".lf_account").read().strip()
h = lf_api.session_headers(acct)

q = """query($id:ID!){node(id:$id){... on Funnel{
  name published starting_step_id steps{uid slug title}}}}"""


def go(fn):
    for _ in range(5):
        try:
            return fn()
        except Exception as e:
            if "502" in str(e) or "Bad Gateway" in str(e):
                print("  502, backing off 70s")
                time.sleep(70)
                continue
            raise
    raise RuntimeError("gave up")


# the copy must exist and be intact before we remove the original
dst = go(lambda: lf_api.get_funnel_steps(tok, DST, extra_headers=h))
d = {x["uid"]: x for x in dst["steps"]}.get(DST_STEP)
assert d is not None, "destination copy missing - refusing to remove the source"
draw = d["body"] if isinstance(d["body"], str) else json.dumps(d["body"])
assert draw.count("data-fx-gbp") == 36, "destination copy incomplete"
assert d["slug"] == "dynamic-currency", d["slug"]
print("destination copy verified: %s / %r, 36 fx tags" % (DST_STEP, d["slug"]))

src_before = go(lambda: lf_api.gql(tok, q, {"id": SRC}, extra_headers=h))["node"]
start = src_before.get("starting_step_id")
uids = [x["uid"] for x in src_before["steps"]]
assert SRC_STEP in uids, "source step already gone"
assert SRC_STEP != start, "refusing to delete the funnel's entry page"
print("source before: %d steps, start=%s" % (len(src_before["steps"]), start))

go(lambda: lf_api.gql(
    tok, "mutation($id:ID!,$node:InputFunnel!){updateFunnel(id:$id,node:$node){id}}",
    {"id": SRC, "node": {"deleted_steps": [SRC_STEP]}}, extra_headers=h))
print("removed via deleted_steps")

src_after = go(lambda: lf_api.gql(tok, q, {"id": SRC}, extra_headers=h))["node"]
left = [x["uid"] for x in src_after["steps"]]
print("\nsource after: %d steps, start=%s" % (len(src_after["steps"]), src_after.get("starting_step_id")))
for x in src_after["steps"]:
    print("   %-26s %-22s %r" % (x["uid"][:26], x["slug"], x["title"][:40]))
assert SRC_STEP not in left, "step still present"
assert len(left) == len(uids) - 1, (len(left), len(uids))
assert src_after.get("starting_step_id") == start, "starting_step_id changed!"
assert src_after.get("name") == src_before.get("name"), "funnel name changed!"
assert src_after.get("published") == src_before.get("published"), "published changed!"
print("\nmove complete: 1 copy, in the live funnel")
