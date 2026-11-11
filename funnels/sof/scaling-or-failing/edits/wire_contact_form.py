#!/usr/bin/env python3
"""Connect the Scaling or Failing contact form to n8n.

The form shipped deliberately inert: no action, submit button `disabled`, and a
note saying so, because there was nowhere to send it. There is now - n8n workflow
qDbixpOcwNHtaC3k, which validates the submission and emails it to
hello@scalingorfailing.com.

Two writes, because the two halves live in different places:

1. STEP BODY, contact step only - drop `disabled`, mark name/email/message
   `required`, add an off-screen honeypot field, and reword the "not connected"
   note into the status line the script writes into.

2. FUNNEL header_scripts - the submit handler. It has to be funnel level because
   that is the only script slot this account exposes, so it is guarded on
   `form.sof-form` and does nothing on the landing page.

The POST is form-encoded on purpose: that is a CORS "simple request", so the
browser sends no preflight OPTIONS, and n8n parses it into `body` just the same.

Non-ASCII characters in the page are written as \\u escapes here so the source
stays ASCII and cannot drift from the bytes actually in the body JSON.

Idempotent: re-running sees the honeypot and the marker and stops. The pre-edit
body is archived to steps/ first, so a revert is one write of that file.

    py funnels/sof/scaling-or-failing/edits/wire_contact_form.py            dry run
    py funnels/sof/scaling-or-failing/edits/wire_contact_form.py --apply
"""
import json, os, sys, time, urllib.request
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", "..", "..", ".."))
sys.path.insert(0, ROOT); os.chdir(ROOT)
import lf_api

FUNNEL = "fun_RoOL_WXDCAxK4hEk0v5xX"
STEP_SLUG = "contact"
URL = "https://www.scalingorfailing.com/event/contact"
ENDPOINT = "https://primary-production-f5243.up.railway.app/webhook/sof-contact"
MARK = "sof-contact-form -> n8n"

MDASH = u"—"
RARR = u"→"

HONEYPOT = (
    '<div aria-hidden="true" style="position:absolute;left:-9999px;top:auto;'
    'width:1px;height:1px;overflow:hidden"><label for="sof-website">Website</label>'
    '<input id="sof-website" name="website" type="text" tabindex="-1" autocomplete="off">'
    '</div>'
)

# Exact before/after pairs. edit_step_bodies does raw substring matching first,
# so these keep their surrounding markup.
PAIRS = [
    ('<input id="sof-name" name="name" type="text" placeholder="Your name">',
     '<input id="sof-name" name="name" type="text" placeholder="Your name" required>'),

    ('<input id="sof-email" name="email" type="email" placeholder="Your email">',
     '<input id="sof-email" name="email" type="email" placeholder="Your email" required>'),

    ('<textarea id="sof-message" name="message" rows="5" placeholder="How can we help?"></textarea>',
     '<textarea id="sof-message" name="message" rows="5" placeholder="How can we help?" required></textarea>'),

    # Honeypot is positioned off-screen rather than display:none, because bots
    # that skip hidden fields still fill an off-screen one. No new CSS class, so
    # the stylesheet in the header block stays untouched.
    ('<button class="sof-send" type="submit" disabled>SEND MESSAGE  ' + RARR + '</button>',
     HONEYPOT + '<button class="sof-send" type="submit">SEND MESSAGE  ' + RARR + '</button>'),

    ('<p class="sof-form-note">This form is not connected yet ' + MDASH + ' email us at '
     '<a href="mailto:hello@scalingorfailing.com">hello@scalingorfailing.com</a></p>',
     '<p class="sof-form-note">Or email '
     '<a href="mailto:hello@scalingorfailing.com">hello@scalingorfailing.com</a></p>'),
]

SCRIPT = ("""
<!-- %s
     Submits the contact form. Funnel level because header_scripts is the only
     script slot this account exposes, so it is guarded on form.sof-form and is
     inert on every other page in the funnel. -->
<script>
(function () {
  var ENDPOINT = '%s';
  function wire() {
    var form = document.querySelector('form.sof-form');
    if (!form || form.getAttribute('data-sof-wired')) return;
    form.setAttribute('data-sof-wired', '1');
    var btn = form.querySelector('.sof-send');
    var note = form.querySelector('.sof-form-note');
    var label = btn ? btn.innerHTML : '';
    var noteHTML = note ? note.innerHTML : '';
    function say(html, bad) {
      if (!note) return;
      note.innerHTML = html;
      note.style.color = bad ? '#B3261E' : '';
    }
    form.addEventListener('submit', function (e) {
      e.preventDefault();
      if (form.reportValidity && !form.reportValidity()) return;
      // Form-encoded: a CORS simple request, so the browser sends no preflight
      // OPTIONS. n8n still parses it into body.
      var data = new URLSearchParams(new FormData(form));
      if (btn) { btn.disabled = true; btn.innerHTML = 'SENDING&hellip;'; }
      say(noteHTML);
      fetch(ENDPOINT, { method: 'POST', body: data })
        .then(function (r) { return r.json().catch(function () { return { ok: r.ok }; }); })
        .then(function (j) {
          if (!j || j.ok !== true) throw new Error('rejected');
          form.reset();
          if (btn) btn.innerHTML = 'SENT';        // left disabled: no double send
          say('Thanks. Your message is with us, we reply within 24 hours.');
        })
        .catch(function () {
          if (btn) { btn.disabled = false; btn.innerHTML = label; }
          say('That did not send. Please email ' +
              '<a href="mailto:hello@scalingorfailing.com">hello@scalingorfailing.com</a>.', true);
        });
    });
  }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', wire);
  else wire();
})();
</script>
""".strip()) % (MARK, ENDPOINT)

APPLY = "--apply" in sys.argv

tok = open(".session_token").read().strip()
acct = open(".lf_account").read().strip()
h = lf_api.session_headers(acct)

funnel = lf_api.get_funnel_steps(tok, FUNNEL, extra_headers=h)
step = next(s for s in funnel["steps"] if s.get("slug") == STEP_SLUG)
blob = json.dumps(step["body"])
print("funnel %s / step %s (%s)" % (funnel.get("name"), step["uid"], STEP_SLUG))

# ---- 1. check the body edits will all land, before writing anything -------
body_todo = "sof-website" not in blob
if body_todo:
    for old, _ in PAIRS:
        n = blob.count(json.dumps(old)[1:-1])
        if n != 1:
            sys.exit("ABORT: expected exactly 1 of %r in the body, found %d" % (old[:70], n))
    print("body: all %d replacements matched exactly once" % len(PAIRS))
else:
    print("body: honeypot already present, skipping")

# ---- 2. header_scripts ---------------------------------------------------
Q = 'query($id:ID!){node(id:$id){... on Funnel{name header_scripts}}}'
cur = (lf_api.gql(tok, Q, {"id": FUNNEL}, extra_headers=h)["node"].get("header_scripts") or "")
scripts_todo = MARK not in cur
if scripts_todo:
    new_scripts = (cur.rstrip() + "\n\n" + SCRIPT + "\n") if cur.strip() else SCRIPT + "\n"
    print("header_scripts: %d -> %d chars" % (len(cur), len(new_scripts)))
else:
    print("header_scripts: handler already present, skipping")

if not body_todo and not scripts_todo:
    sys.exit("Nothing to do.")
if not APPLY:
    sys.exit("\nDRY RUN. Re-run with --apply to write.")

if body_todo:
    bak = os.path.abspath(os.path.join(
        HERE, "..", "steps", "contact.pre-wire-%s.json" % time.strftime("%Y-%m-%d")))
    open(bak, "w", encoding="utf-8").write(json.dumps(step["body"], indent=2))
    print("backup ->", bak)
    # force=True: the `old` strings are markup, and the no-force guard only
    # searches visible text, so it would reject every one of them.
    r = lf_api.edit_step_bodies(tok, FUNNEL, PAIRS, extra_headers=h,
                                force=True, step_uids=[step["uid"]])
    print("body written:", json.dumps(r))
    if r.get("steps_changed") != 1:
        sys.exit("ABORT: expected 1 step changed, got %r" % r.get("steps_changed"))

if scripts_todo:
    lf_api.gql(tok, "mutation($id:ID!,$node:InputFunnel!){updateFunnel(id:$id,node:$node){id}}",
               {"id": FUNNEL, "node": {"header_scripts": new_scripts}}, extra_headers=h)
    print("header_scripts written")

time.sleep(10)
page = urllib.request.urlopen(urllib.request.Request(
    URL + "?cb=%d" % time.time(),
    headers={"User-Agent": "Mozilla/5.0", "Cache-Control": "no-cache"}), timeout=90
    ).read().decode("utf-8", "replace")
print("\nserved check on " + URL)
print("  button still disabled  : %s   (want False)" % ('type="submit" disabled' in page))
print("  honeypot present       : %s   (want True)" % ("sof-website" in page))
print("  handler present        : %s   (want True)" % (MARK in page))
print("  endpoint present       : %s   (want True)" % (ENDPOINT in page))
print("  'not connected yet'    : %s   (want False)" % ("not connected yet" in page))
