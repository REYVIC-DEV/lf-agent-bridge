#!/usr/bin/env python3
"""Remove the IP address clause from privacy section 3.

Sequence of events, so this is not confusing later:

  2026-10-14 am  fix_privacy_contact_form.py ran. It wrote "What you type into
                 it, together with the IP address you send it from, is emailed
                 to us", which was correct: the email n8n sent carried a
                 "Source IP" line.
  2026-10-14 pm  The email was redesigned as HTML and the Source IP line was
                 dropped at Joshua's request. The policy now over-discloses: it
                 claims we collect something we no longer collect.

This removes the clause. One replacement, both steps, because the legal block is
duplicated in each page's footer. Idempotent.

    py funnels/sof/scaling-or-failing/edits/drop_ip_from_privacy.py            dry run
    py funnels/sof/scaling-or-failing/edits/drop_ip_from_privacy.py --apply
"""
import json, os, sys, time, urllib.request
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", "..", "..", ".."))
sys.path.insert(0, ROOT); os.chdir(ROOT)
import lf_api

FUNNEL = "fun_RoOL_WXDCAxK4hEk0v5xX"
URLS = ["https://www.scalingorfailing.com/event/contact",
        "https://www.scalingorfailing.com/event/scaling-failing"]

OLD = ("<p>The event page asks you for nothing. The contact page has a form. What you\n"
       "type into it, together with the IP address you send it from, is emailed to us\n"
       "so that we can reply, and is not stored anywhere else. Both pages set cookies\n"
       "and contact a few other services:</p>")
NEW = ("<p>The event page asks you for nothing. The contact page has a form. What you\n"
       "type into it is emailed to us so that we can reply, and is not stored anywhere\n"
       "else. Both pages set cookies and contact a few other services:</p>")

PAIRS = [(OLD, NEW)]
APPLY = "--apply" in sys.argv

tok = open(".session_token").read().strip()
h = lf_api.session_headers(open(".lf_account").read().strip())
funnel = lf_api.get_funnel_steps(tok, FUNNEL, extra_headers=h)

todo = []
for s in funnel["steps"]:
    blob = json.dumps(s.get("body"))
    if json.dumps(NEW)[1:-1] in blob:
        print("%-18s already corrected, skipping" % s["slug"])
        continue
    n = blob.count(json.dumps(OLD)[1:-1])
    if n != 1:
        sys.exit("ABORT: %s has %d matches, expected 1. The wording has drifted; "
                 "re-read the live body before editing." % (s["slug"], n))
    print("%-18s matched once" % s["slug"])
    todo.append(s)

if not todo:
    sys.exit("Nothing to do.")
if not APPLY:
    sys.exit("\nDRY RUN. Re-run with --apply to write.")

stamp = time.strftime("%Y-%m-%d-%H%M")
for s in todo:
    bak = os.path.abspath(os.path.join(
        HERE, "..", "steps", "%s.pre-drop-ip-%s.json" % (s["slug"], stamp)))
    open(bak, "w", encoding="utf-8").write(json.dumps(s["body"], indent=2))
    print("backup ->", bak)

# force=True: the match string is markup, and the no-force guard searches
# visible text only, so it would reject it.
r = lf_api.edit_step_bodies(tok, FUNNEL, PAIRS, extra_headers=h, force=True,
                            step_uids=[s["uid"] for s in todo])
print("written:", json.dumps(r))
if r.get("steps_changed") != len(todo):
    sys.exit("ABORT: expected %d steps changed, got %r" % (len(todo), r.get("steps_changed")))

time.sleep(10)
for u in URLS:
    page = urllib.request.urlopen(urllib.request.Request(
        u + "?cb=%d" % time.time(),
        headers={"User-Agent": "Mozilla/5.0", "Cache-Control": "no-cache"}), timeout=90
        ).read().decode("utf-8", "replace")
    print("\n" + u)
    print("  IP clause gone   : %s   (want True)" % ("IP address you send it from" not in page))
    print("  new wording      : %s   (want True)" % ("type into it is emailed to us" in page))
