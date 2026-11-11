#!/usr/bin/env python3
"""Correct the privacy policy now that the contact form actually sends.

Section 3 said "The contact page has a form, which is not connected yet, so
nothing typed into it is sent or stored anywhere." That was true until
wire_contact_form.py ran on 2026-10-14. It is now false, and it is a statement
about personal data, so it cannot be left standing.

Three edits, applied to BOTH steps because the legal block is duplicated in each
page's footer:

1. Section 3, what this page does.
2. Section 5, who we share it with. A contact message now passes through our
   automation host and Gmail before it reaches a person.
3. The privacy policy's "last updated" date. Anchored on the Privacy Policy
   heading so the Terms date, which has not changed, is left alone.

Idempotent: stops if the new wording is already in place.

    py funnels/sof/scaling-or-failing/edits/fix_privacy_contact_form.py            dry run
    py funnels/sof/scaling-or-failing/edits/fix_privacy_contact_form.py --apply
"""
import json, os, sys, time, urllib.request
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", "..", "..", ".."))
sys.path.insert(0, ROOT); os.chdir(ROOT)
import lf_api

FUNNEL = "fun_RoOL_WXDCAxK4hEk0v5xX"
URLS = ["https://www.scalingorfailing.com/event/contact",
        "https://www.scalingorfailing.com/event/scaling-failing"]

PAIRS = [
    # 1. what this page does
    ("<p>The event page asks you for nothing. The contact page has a form, which is\n"
     "not connected yet, so nothing typed into it is sent or stored anywhere. Both\n"
     "pages set cookies and contact a few other services:</p>",

     "<p>The event page asks you for nothing. The contact page has a form. What you\n"
     "type into it is emailed to us so that we can reply, and is not stored anywhere\n"
     "else. Both pages set cookies and contact a few other services:</p>"),

    # 2. who we share it with
    ("<li>Professional advisers and authorities, where we are required to.</li>",

     "<li>Our email and automation providers, which carry your contact form message\n"
     "to us.</li>\n"
     "<li>Professional advisers and authorities, where we are required to.</li>"),

    # 3. privacy date only. The Terms doc carries the same meta line and the same
    #    date, so the heading has to be part of the match or both would move.
    ("<h3>Privacy Policy</h3>\n"
     '<p class="sof-legal-meta">Scaling or Failing &middot; Bangkok, Thailand '
     "&middot; 7 and 8 December 2026 &middot; Last updated 9 October 2026</p>",

     "<h3>Privacy Policy</h3>\n"
     '<p class="sof-legal-meta">Scaling or Failing &middot; Bangkok, Thailand '
     "&middot; 7 and 8 December 2026 &middot; Last updated 14 October 2026</p>"),
]

APPLY = "--apply" in sys.argv

tok = open(".session_token").read().strip()
h = lf_api.session_headers(open(".lf_account").read().strip())
funnel = lf_api.get_funnel_steps(tok, FUNNEL, extra_headers=h)

todo = []
for s in funnel["steps"]:
    blob = json.dumps(s.get("body"))
    if json.dumps(PAIRS[0][1])[1:-1] in blob:
        print("%-18s already corrected, skipping" % s["slug"])
        continue
    for old, _ in PAIRS:
        n = blob.count(json.dumps(old)[1:-1])
        if n != 1:
            sys.exit("ABORT: %s has %d of %r, expected 1" % (s["slug"], n, old[:60]))
    print("%-18s all %d replacements matched once" % (s["slug"], len(PAIRS)))
    todo.append(s)

if not todo:
    sys.exit("Nothing to do.")
if not APPLY:
    sys.exit("\nDRY RUN. Re-run with --apply to write.")

stamp = time.strftime("%Y-%m-%d")
for s in todo:
    bak = os.path.abspath(os.path.join(
        HERE, "..", "steps", "%s.pre-privacy-fix-%s.json" % (s["slug"], stamp)))
    open(bak, "w", encoding="utf-8").write(json.dumps(s["body"], indent=2))
    print("backup ->", bak)

# force=True: the match strings are markup, and the no-force guard searches
# visible text only, so it would reject every one of them.
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
    print("  'not connected yet'      : %s   (want False)" % ("not connected yet" in page))
    print("  new wording present      : %s   (want True)" % ("is emailed to us" in page))
    print("  automation bullet        : %s   (want True)" % ("automation providers" in page))
    print("  privacy updated 14 Oct   : %s   (want True)" % ("Last updated 14 October 2026" in page))
    print("  terms still 9 Oct        : %s   (want True)" % ("Last updated 9 October 2026" in page))
