# Contact form to email: implementation and handover

**For:** whoever picks up the Scaling or Failing site next.
**Written:** 2026-10-14.

The contact form at `https://www.scalingorfailing.com/event/contact` now posts
to n8n, which validates the submission and emails it to
`hello@scalingorfailing.com`. Before today the form was deliberately inert.

## Status

| Piece | State |
|---|---|
| n8n workflow `qDbixpOcwNHtaC3k` | **LIVE**, active, tested end to end |
| Gmail credential `V1JzSurTCcWagrsZ` "SOF - Gmail" | **LIVE**, OAuth, sends as hello@ |
| Contact step body, form markup | **LIVE**, and now produced by the builder |
| Funnel `header_scripts`, submit handler | **LIVE** |
| Privacy policy correction | **APPLIED** 2026-10-14, in the builder |
| Email redesigned as HTML, IP line removed | **APPLIED** 2026-10-14 |

## ⚠️ Read this before touching anything

**`pagescore/build_sof_event.py` is the source of truth for both page bodies.**
It rewrites the whole step body on every deploy, so anything it does not itself
produce is erased the next time either page is rebuilt — and these pages are
rebuilt every time the Figma frame changes, which has been several times a day.

The two scripts in `edits/` patched the DEPLOYED body. That worked, and then a
routine rebuild would have silently undone it: no error, no failed check, just a
dead form and a privacy policy that had started lying again.

So both of them have been folded into the builder:

- **`wire_contact_form.py`** → `contact_html()` now emits the `required`
  attributes, the `HONEYPOT` constant, the enabled submit button and the
  "Or email …" note. Byte for byte what the script wrote.
- **`fix_privacy_contact_form.py`** → the three privacy edits are in
  `PRIVACY_DOC`, and the privacy document has its own `PRIVACY_UPDATED` date
  constant so it can move without dragging the Terms date with it.

**Both scripts are now historical.** Do not run them. Their match strings no
longer exist in the deployed body, so they would refuse anyway, but the point is
that the builder is where a change belongs now.

The submit handler is the exception and stays where it is: `header_scripts` is
funnel level, the builder never touches it, and it already survives rebuilds.

### What the privacy correction says

Three edits, in both pages, because the legal block is in each page's footer:

1. Section 3 says the message is emailed to us and stored nowhere else.
   ⚠️ This sentence was edited TWICE on 2026-10-14. It first said the sender's
   IP address was emailed too, which was true of the original plain-text email.
   The email was then redesigned as HTML and the `Source IP` line dropped at
   Joshua's request, so the clause was removed from both the deployed body and
   `PRIVACY_DOC` in the builder. If the email ever starts carrying the IP again,
   this sentence has to come back.
2. Section 5 gains a bullet for the email and automation providers that carry
   the message.
3. The Privacy Policy is dated 14 October 2026. The Terms document is still
   9 October and must stay there — it did not change.

## The contract between site and n8n

Keep this if the page is ever rebuilt from the Figma design.

**Endpoint**

```
POST https://primary-production-f5243.up.railway.app/webhook/sof-contact
Content-Type: application/x-www-form-urlencoded
```

**Fields**

| Name | Rule |
|---|---|
| `name` | required, trimmed, capped at 120 chars |
| `email` | required, must look like an address, capped at 160 |
| `topic` | optional, must be one of `Tickets`, `Sponsorship`, `Speaking`, `Other` |
| `message` | required, capped at 5,000 chars |
| `website` | honeypot. Must exist and must stay empty. Any content drops the submission. |

**Response**, read by the page to decide what to print:

```json
{"ok": true,  "message": "Thanks, your message has been sent."}
{"ok": false, "message": "Please check the form and try again."}
```

A rejection returns HTTP 200 with `ok:false`. Do not treat the status code as
the signal, read `ok`.

## What was changed on the site, exactly

### 1. Contact step body

Step `step_NJL4g7GnXGFt6DOVdD6Jn`, slug `contact`. Originally five replacements
by `edits/wire_contact_form.py`; the same five are now produced by
`contact_html()` in the builder, which is what actually ships:

- `name`, `email` and `message` inputs gained `required`
- an off-screen honeypot `<div>` holding `input[name=website]` was inserted
  immediately before the submit button
- `<button class="sof-send" type="submit" disabled>` lost its `disabled`
- the note `This form is not connected yet — email us at …` became `Or email …`

The honeypot is positioned off-screen rather than `display:none`, because bots
that skip hidden fields still fill an off-screen one. It uses an inline style
and no new class, so the stylesheet in the header block was not touched.

### 2. Funnel `header_scripts`

The submit handler, about 2,100 chars appended after the existing Lenis block
(3,418 → 5,536 chars). Marker comment: `sof-contact-form -> n8n`.

It has to be funnel level, because `header_scripts` is the only script slot this
account exposes. It is therefore guarded on `document.querySelector('form.sof-form')`
and returns immediately on the landing page.

What it does: intercepts submit, runs `reportValidity()`, posts the form,
disables the button and shows `SENDING…`, then on success resets the form,
leaves the button disabled reading `SENT` so the message cannot be sent twice,
and writes a thank-you into `.sof-form-note`. On any failure it restores the
button and tells the visitor to email hello@ instead.

## Two deliberate choices, do not "fix" them

**The POST is form-encoded, not JSON.** `application/x-www-form-urlencoded` is a
CORS *simple request*, so the browser sends no preflight `OPTIONS`. Switching to
JSON would trigger one, and then the webhook has to answer `OPTIONS` correctly
as well. n8n parses form-encoding into `body` exactly the same way.

**The webhook still sets `allowedOrigins: '*'`.** The *response* needs the CORS
header or the page cannot read whether the send worked. Note that n8n only emits
that header when the request carries an `Origin`; a curl test without one shows
no header and that is not a fault. Verified live: a request with
`Origin: https://www.scalingorfailing.com` comes back with a matching
`access-control-allow-origin`.

## Verifying

From anywhere:

```bash
curl -s -X POST https://primary-production-f5243.up.railway.app/webhook/sof-contact \
  -H 'Origin: https://www.scalingorfailing.com' \
  --data-urlencode 'name=Test' \
  --data-urlencode 'email=you@example.com' \
  --data-urlencode 'topic=Other' \
  --data-urlencode 'message=hello'
```

Expect `{"ok":true,...}` and an email at hello@. Swap in `-d 'website=x'` and it
must come back `ok:false` with no email sent.

On the page itself: the submit button must not be disabled on load, and viewing
source must show both `sof-website` and `sof-contact-form -> n8n`.

## Reverting

**To take the form offline**, edit the builder and redeploy, not the step body:
put `disabled` back on the submit button in `contact_html()` and drop the
`HONEYPOT`. A step-body patch would last until the next rebuild.

`steps/contact.pre-wire-2026-10-14.json` is the archived pre-wiring body. It
predates several frame updates, so it is a record of what changed, not something
to write back — restoring it would roll the page back to the 14 October design.

The `header_scripts` handler is removed by deleting the block between the
`sof-contact-form -> n8n` marker and its closing `</script>`; leave the Lenis
block above it alone. That one is still a direct funnel edit, because the
builder does not manage that field.

## Traps hit while building this, in case they recur

- **A Set node drops everything it is not told to keep.** The `Validate` code
  originally read `$input.first().json.body`, but its input is the `Config` Set
  node, so body and headers were gone and every submission was rejected as empty.
  It now reads `$('Contact form webhook').first().json`. The failure was silent:
  the workflow reported success and simply rejected everything.
- **`PUT /workflows/{id}` replaces the whole node.** Redeploying from the build
  script stripped the Gmail credential off the node and deactivated the workflow,
  with no warning. The credential id is now pinned in the build script.
- **n8n resolves a credential by name.** There is no credential list endpoint in
  the public API, but `credentials: { gmailOAuth2: { name: 'SOF - Gmail' } }` on
  a `PUT` resolves and the response comes back with the id filled in. That is the
  only way found to attach a credential without opening the UI.

Full n8n-side notes: `../../../../N8N/documentation/sof-contact-form.md`.
