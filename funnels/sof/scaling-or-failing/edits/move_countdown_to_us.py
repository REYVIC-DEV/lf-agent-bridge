#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Move the Early Bird countdown from Bangkok midnight to US Pacific midnight.

THE ASK, 2026-10-30. The team: "lets have it run US timezone today as it is,
just timer needs to move", and "make the countdown US time daw". Early bird
keeps running through today; the price changes tomorrow instead of tonight.

    was   2026-10-30T16:59:59Z   = 30 Oct 23:59:59 Bangkok
    now   2026-10-31T06:59:59Z   = 30 Oct 23:59:59 Pacific
                                 = 31 Oct 14:59 Manila, 13:59 Bangkok

Pacific, not Eastern, because it is the later of the two US midnights and the
usual choice for a US deadline. 30 October 2026 is still PDT (UTC-7): US
daylight time does not end until 1 November.

THE "ENDS OCT 30" PILL IS STILL TRUE and is deliberately left alone. It is
still the 30th in US time, which is the timezone the deadline now runs on.

WHY THIS HAD TO HAPPEN TODAY. The page's own countdown script REMOVES the gold
bar at zero. Left alone, the bar vanishes at Bangkok midnight while the price
stays $1997 and the card still says ENDS OCT 30 -- early bird still for sale,
with no timer on it.

WHY THE STEP BODY AND NOT A HEADER SCRIPT. The countdown script reads the
deadline once, into a closure, from the `data-cd-ends` attribute in the served
HTML. A header script cannot reach that variable afterwards, so patching the
attribute later would be read too late and the bar would keep counting to the
old time. Changing the HTML is both the simplest fix and the only one the
existing script will actually obey.

The build-time digits in the HTML are left stale on purpose. They are already
stale -- they were rendered on 25 October -- and the page's script overwrites
them from the visitor's own clock on its first tick, before first paint.

ALSO UPDATED, BY HAND, NOT BY THIS SCRIPT: pagescore/build_sof_event.py holds
the same instant TWICE, in COUNTDOWN_ENDS and again as a literal datetime
inside countdown_html(). Both are moved in the same commit, or the next rebuild
of this page silently drags the deadline back to the old time.

Idempotent: a step already on the new instant is skipped.

    py funnels/sof/scaling-or-failing/edits/move_countdown_to_us.py            dry run
    py funnels/sof/scaling-or-failing/edits/move_countdown_to_us.py --apply
"""
import json
import os
import sys
import time
import urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", "..", "..", ".."))
sys.path.insert(0, ROOT)
os.chdir(ROOT)
import lf_api  # noqa: E402

FUNNEL = "fun_RoOL_WXDCAxK4hEk0v5xX"

# BOTH STEPS, and the second one is easy to miss. The sticky bar AND the gold
# countdown are built onto the contact page too, so moving the landing page
# alone leaves /event/contact counting to the old Bangkok midnight -- a timer
# at zero on one page and running on the other. That is exactly what the first
# run of this script did on 2026-10-30. It surfaced only because an unrelated
# marker count on the contact page dropped by one.
STEPS = [
    ("scaling-failing", "https://www.scalingorfailing.com/event/scaling-failing"),
    ("contact", "https://www.scalingorfailing.com/event/contact"),
]

OLD = 'data-cd-ends="2026-10-30T16:59:59Z"'
NEW = 'data-cd-ends="2026-10-31T06:59:59Z"'
PAIRS = [(OLD, NEW)]

APPLY = "--apply" in sys.argv

tok = open(".session_token").read().strip()
h = lf_api.session_headers(open(".lf_account").read().strip())

funnel = lf_api.get_funnel_steps(tok, FUNNEL, extra_headers=h)
print("funnel %s" % funnel.get("name"))

todo = []
for slug, url in STEPS:
    step = next(s for s in funnel["steps"] if s.get("slug") == slug)
    blob = json.dumps(step["body"])
    if json.dumps(NEW)[1:-1] in blob:
        print("  %-18s already on the new deadline, skipping" % slug)
        continue
    n = blob.count(json.dumps(OLD)[1:-1])
    if n != 1:
        sys.exit("ABORT: %s has %d copies of the old deadline, expected 1" % (slug, n))
    print("  %-18s one copy of the old deadline, will move" % slug)
    todo.append((slug, url, step))

if not todo:
    sys.exit("Nothing to do.")
print("  from %s" % OLD)
print("  to   %s" % NEW)

if not APPLY:
    sys.exit(os.linesep + "DRY RUN. Re-run with --apply to write.")

for slug, url, step in todo:
    bak = os.path.abspath(os.path.join(
        HERE, "..", "steps", "%s.pre-countdown-move-%s.json"
        % (slug, time.strftime("%Y-%m-%d"))))
    if not os.path.exists(bak):
        open(bak, "w", encoding="utf-8").write(json.dumps(step["body"], indent=2))
        print("backup -> %s" % os.path.relpath(bak, ROOT))
    # force=True: an HTML attribute is markup, and the no-force guard only
    # searches visible text, so it would reject this outright.
    r = lf_api.edit_step_bodies(tok, FUNNEL, PAIRS, extra_headers=h,
                                force=True, step_uids=[step["uid"]])
    print("%s written: %s" % (slug, json.dumps(r)))
    if r.get("steps_changed") != 1:
        sys.exit("ABORT: expected 1 step changed, got %r" % r.get("steps_changed"))

time.sleep(10)
for slug, url in STEPS:
    page = urllib.request.urlopen(urllib.request.Request(
        url + "?cb=%d" % time.time(),
        headers={"User-Agent": "Mozilla/5.0", "Cache-Control": "no-cache"}),
        timeout=90).read().decode("utf-8", "replace")
    print("")
    print("served check on %s" % url)
    print("  new deadline present : %s   (want True)" % (NEW in page))
    print("  old deadline gone    : %s   (want True)" % (OLD not in page))
    print("  countdown bar present: %s   (want True)" % ('class="sof-cd"' in page))
    print("  price still $1997    : %s   (want True on the landing page)" % ("$1997" in page))
