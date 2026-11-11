# Scaling or Failing - Event

Event landing page for Scaling or Failing, December 7 to 8 2026, Bangkok,
Thailand. Powered by BestFulfill. ClickUp [z941aby19y].

| | |
|---|---|
| funnel | `fun_RoOL_WXDCAxK4hEk0v5xX` |
| funnel slug | `/event` |
| step | `step_5BIwggYOWxmrOPnAyaVPi`, slug `scaling-failing`, entry |
| URL | https://www.scalingorfailing.com/event/scaling-failing |
| Contact | https://www.scalingorfailing.com/event/contact |
| future domain | `scalingorfailing.com`, Eline registering it |
| design | Figma "Scaling or Failing · Hero" `VHQyCN1AzzuFao689DwlvL`, and a working copy in the 99 Commerce file that figwright reads |
| reference | https://geekout-events.com/2026/greece/#ticket |

## Decisions already made

**Checkout is Whova, linked out.** The reference site runs no checkout of its own:
hand-written static HTML on nginx, no CMS, no cart, zero forms, zero payment
iframes. Its entire commerce surface is one external link repeated twice, to
`whova.com/portal/registration/...`, opened in a new tab. We do the same, so
there is nothing to build here. Topi supplies our Whova URL once our application
is approved; until then every ticket CTA points at a placeholder.

**Nav items are in-page anchors**, not destinations. About, Speakers, Topics,
Get Ticket and Contact scroll to their sections, exactly as Geekout's `#ticket`
does. Only the ticket buttons leave the page.

**Speakers are TBA placeholders, as drawn.** The linked Figma file has ten named
speaker captions (Neil Patel, Ryan Holiday, Ryan Deiss, Oli Gardner, Mark Joyner,
Robin Duan, Eric Siu and others) sitting loose on the canvas OUTSIDE Frame 1.
They are not placed in the design, so they are not built. Joshua's call.

## Ten sections, in order

Header (sticky early bird bar + nav), Hero, Stats, Speakers, Formats, You Decide,
Topics, Tickets, Sponsor, Footer. Frame 1 is desktop 1920, Frame 2 is mobile 390.
Two designs, not one that reflows.

Tickets: EARLY BIRD $1,997 and VIP $6,497.

## How the funnel was created, and the traps it hit

`createFunnel` returns a funnel with **no steps and published=False**, so three
calls are needed, not one:

1. `createFunnel` - name, slug, `funnel_steps: ["article_page"]`, currency USD.
2. `createStep` - returns a step that **`funnel.steps` does not list**. It is
   detached, and a detached step does not render.
3. `updateFunnel` with that step in `steps`, plus `starting_step_id` and
   `published: true`. `InputUpdateStep` wants the whole step, not a patch:
   `id`, `slug`, `title`, `type`, `settings`, `visual`.

⚠️ **The step has no `product_id`.** Elsewhere in this account a step without one
accepted writes and never re-rendered them, with no error anywhere. There is no
product to attach here, since tickets are sold on Whova. If an edit saves but the
live page does not change, that is the first thing to check.

## The URL, and why the funnel slug is `event`

**On the live domain this reads `scalingorfailing.com/event/`.**

Lightfunnels always serves `/<funnel-slug>/<step-slug>`, and in this account the
funnel slug is unavoidable: **no funnel here has a store attached**, so domains
bind at workspace level rather than per funnel. The funnel slug was
`scaling-or-failing`, which on the event's own domain would have read
`scalingorfailing.com/scaling-or-failing/event` - the brand said twice.

So the funnel slug is now `event` and the step is the ENTRY step, which makes the
funnel root the canonical URL. The step slug stays `event` too, so
`LF_ALLOW_REDEPLOY=event` and the builder's `STEP_SLUG` are unchanged.

Side effects, both harmless but worth knowing:

- `/event/event` serves the same page as `/event/`. Inherent to LF: an entry step
  is reachable at both the funnel root and its own slug. `/event/` is canonical.
- `/scaling-or-failing/` now **404s**. Nothing had been linked to it.
- `/event/event-v2` is a leftover from the first build, which shipped to a new slug
  because the builder correctly refused to authorise its own redeploy. There is no
  `deleteStep` mutation, so it cannot be removed through the API.

## Smooth scroll

Lenis, funnel level in `header_scripts`, 3,417 chars taken from the smooth-scroll
section of `snippets/tracker-header-meta-block.html` - **not** the whole tracker
block. The full header carries HLTH's Taboola, Outbrain and Aimerce pixels and the
HLTH PostHog projects, which have no business firing on a separate event brand.
Asserted at install time that no tracking code came with it; the served page
confirms `posthog=0`.

⚠️ So this funnel has **no analytics at all**. Same silent gap that bit the
over-60s funnel. A deliberate choice, not an oversight, but it needs a decision
before the page takes traffic.

Verified live: desktop 1440 has `html.lenis`, the library loaded and
`scroll-behavior: auto`, and an anchor click eases (2992 -> 5986 toward 6254).
Mobile 390 never downloads the library and keeps native smooth scrolling.

### Correction: a domain has a HOME FUNNEL, so the funnel slug drops out

A domain in Lightfunnels carries a **Home Funnel** setting (Settings > Domains:
`www.techunboxed.co` has "Home Funnel: TUB - Top 5 h trackers-v2 - META - LIVE").
The funnel assigned there resolves at the domain ROOT, so its slug never appears
in the path. That is the piece missing from the reasoning above - "no funnel has a
store attached" was true but led to the wrong conclusion.

So once `scalingorfailing.com` exists and this funnel is set as its home funnel:

    scalingorfailing.com/         entry step
    scalingorfailing.com/event    the step by its own slug

The funnel slug stops mattering for the live domain. The rename to `event` is
harmless either way, and the step slug `event` was right from the start. Joshua is
assigning the domain himself once Eline has registered it.

### Step renamed to `scaling-failing`, 2026-10-07

`/event/event` duplicated a segment. The step is now `scaling-failing`, so the
staging URL reads `/event/scaling-failing` and `/event/event` 404s. The entry
page is unaffected at `/event/`.

**This changes the redeploy variable**: it is now
`LF_ALLOW_REDEPLOY=scaling-failing`, and the builder's `STEP_SLUG` default moved
with it. Once scalingorfailing.com is set as this funnel's HOME FUNNEL the funnel
slug leaves the path anyway and the entry sits at the domain root, so the step
slug only ever shows on the staging domain.


## Own domain, 2026-10-14

The funnel URL was repointed to `www.scalingorfailing.com/event` in the
Lightfunnels dashboard. Both pages answer there now:

    https://www.scalingorfailing.com/event/scaling-failing
    https://www.scalingorfailing.com/event/contact

⚠️ `www.techunboxed.co/event/*` STILL SERVES THE SAME PAGES. Both domains are
attached to the account, so nothing stopped answering when the funnel URL
changed; the new host was added, the old one was not removed. Two hostnames
serving one page is a duplicate-content problem the moment either gets
indexed or linked from an ad. Decide whether techunboxed.co should 301 to
scalingorfailing.com, or stop serving this funnel at all.

The domain spelling is `scalingorfailing.com`. A contact address was given
once as `hello@scailingorfailing.com`, with an i; that spelling is wrong.

## Tazapay added as a fourth sponsor, 2026-11-02

Joshua: *"taza pay logo added new frame pasted on figma"*. Frame **1033:3**,
same shape as 2026-10-31's, one brand added in the two places sponsors appear:
the **marquee** (1033:103 / 1033:806) and the **partner row** (1033:653 /
1033:1344), which went from two plates to three.

Applied by `edits/add_tazapay.py --logo <1033-675.svg> --apply`, 15 replacements,
every one asserted to hit exactly once. Built to the **sof-v3** test step first,
checked at 14 widths, then promoted to both live steps.

### The partner row is now WIDER than the plate above it, on desktop

Three 280 plates with two 20 gaps is 880, against the BestFulfill plate's 760.
The frame centres the 760 inside the 880, so the row overhangs by 60 each side
(x 4/3 = 80 here). On 2026-10-31 the row was deliberately made to **split** the
plate's width so it sat flush; **that rule does not survive a third plate.**
Desktop now carries its own `max-width:1173px` instead of inheriting the
plate's 1013. Mobile still sits flush, because its own frame draws 341 of 342.

### The other three marquee logos had drifted, and only a fourth one showed it

bf and oc are 1.5-3% bigger in the new frame than in the old one. Invisible on
its own, wrong beside a logo that is right: on the test step Tazapay and Suits
rendered at 0.977 of their frame size while bf and oc rendered at 0.957 and
0.946, because those two were still set from the **previous** frame. Corrected
to 479x74 and 272x50 desktop, 121x22 mobile; all four now land within 0.971 to
0.977. **The plate logos did not move**, which is what says the designer
re-placed the marquee row rather than rescaling the brand marks.

### Two things that break if you only add the logo

**The loop duration is what sets the speed.** A fourth logo makes one sequence
longer, so the same duration scrolls it faster. Held at the ~60px/s the ticker
has always run at: mobile 695px -> 11.5s, desktop 1674px -> 28s. Verified the
track is exactly 2x the sequence at both widths, which is what makes the -50%
seam invisible.

**The symbol has to be escaped before it goes in.** `LOGO_DEFS` is a single
quoted Python line, so the export's real newlines must become the two
characters `\n` or the builder dies with *"unterminated string literal"*.
It did, once; the script now escapes and asserts.

### A third plate took the breathing room out at 320

Three plates share the row, so each is ~90 wide at 320 against ~105 at 390, and
the Suits and Outcraft marks -- 84 and 90 wide, **fixed**, because Safari
collapses an svg that carries only a height -- ran into the plate edge. Fixed
with `max-width:calc(100% - 10px)` on `.sof-splate svg`: it keeps the explicit
width Safari needs and lets the viewBox scale the artwork down to fit. 10px is
slack the plate only has below ~368, so 375 and 390 still render at the
design's exact sizes. Confirmed unchanged at 360, 375, 390, 425 and 1440.

⚠️ Nothing here is verified on real iOS. The local browser is Chromium; the
Safari rule is applied from the lesson of 2026-10-31, not re-measured.

## A verifier for buttons and page identity, 2026-11-02

Joshua, after the contact page was found overwritten: *"it is best to test the
buttons everytime we change something as well as see if other page are still
the page they are before"*, and *"not just for SOF pages this can also happen
on other pages tho not much since this is our only pages that are 2, most are 1
since they are adverts"*.

**`pagescore/verify_pages.py`. Run it after every deploy.**

    py pagescore/verify_pages.py            every configured funnel
    py pagescore/verify_pages.py sof        one
    py pagescore/verify_pages.py sof --save re-baseline after an intended change

Two modes, because most funnels here are one page:

- **siblings** (SOF): identity is asserted. A page must have what only IT has
  AND lack what only its SIBLING has. The second half is the half that
  matters: the broken contact page carried the shared header and footer
  perfectly, so a presence-only check would have passed it.
- **drift** (one-page adverts): no sibling to be confused with, so identity is
  "the same page as last time". It fingerprints title, h1, section classes and
  the full link set, and diffs on later runs.

**It found a real broken button on its first run.** The mobile gold GET TICKET
in the header pointed at bare `#tickets`. The header is on BOTH pages and the
contact page has no tickets section, so on mobile that button did nothing.
`nav_href()` existed precisely to resolve this and the desktop cells all used
it; this one call site did not. Fixed, and verified from contact at 390 and
1440: both now land on `/event/scaling-failing#tickets` with the card in view.

⚠️ **THE FIRST VERSION CRIED WOLF AND THAT IS WORSE THAN NO CHECK.** It
reported 33 failures of which 30 were LinkedIn answering 999, plus 403/429 from
hosts that block robots, plus `mailto:`. A report that noisy gets skimmed and
the one real finding in it gets missed. Bot-protection codes are now counted
and reported as BLOCKED, `mailto:`/`tel:` are skipped, and a connection failure
is a WARNING rather than a failure, because this machine's DNS goes through a
WARP resolver and cannot distinguish "site is down" from "we cannot reach it".
`adcubator.com` (Jem's speaker link) is unreachable from here and needs a human
to say which it is.

## SOF_SLUG is not SOF_PAGE: the contact page was overwritten, 2026-11-02

**BROKEN then FIXED.** Joshua: *"the contact button does not work"*, then the
decisive detail, *"no it shows the event page not the contact page"*.

⚠️ **THERE ARE TWO ENV VARS AND THEY DO DIFFERENT JOBS.**

    SOF_PAGE=contact    WHICH PAGE'S CONTENT to build   (line 317)
    SOF_SLUG=<slug>     WHICH STEP to write it into     (line 313)

Promoting the announce bar on 2026-10-31 I ran `SOF_SLUG=contact`, believing it
selected the contact page. It does not: `PAGE` stayed at its default "event",
so **the EVENT page was built into the CONTACT step**. `/event/contact` then
served the landing page, and the n8n-wired contact form was gone from the site
entirely. The builder's own module docstring states the right variable on
**line 8** (`SOF_PAGE=contact`); I did not read it.

⚠️ **NOTHING IN MY CHECKS COULD SEE IT.** The link resolved 200, the click
navigated, the URL was right, the announce bar was correct, the page rendered
beautifully. Every check I had asked "did the write land" and "does the page
look right", and both were true. None asked **"is this the right page?"**. It
survived two full responsive sweeps.

Fixed with `SOF_PAGE=contact LF_ALLOW_REDEPLOY=contact`. Verified element-wise
rather than by substring: form present with name/email/message/website, send
enabled, n8n handler and endpoint present, and NO ticket card, marquee or
speaker elements. Journey re-tested at 1440 and 390, desktop nav and burger
menu: both land on /event/contact showing "Get in touch".

⚠️ **A THIRD SUBSTRING FALSE POSITIVE IN TWO DAYS.** The first restore check
reported `sof-tcard`, `sof-marqbar` and `sof-marq-logo` still on the contact
page. All were CSS: one stylesheet is shared by both pages, so every selector
for the landing page appears in the contact page's source. Element-precise
counts (`<svg class="sof-marq-logo`, `class="sof-tcard"`) are 0. Same shape as
`sof-tick` inside `sof-tickets`, `$1997` inside a comment, `mask-image` already
present. **On this page, never grep for a bare class name.**

**The check that was missing, now the rule:** after any deploy, assert the page
is the RIGHT page, not merely a working one. For contact that is "has
form.sof-form AND has no .sof-tcard"; for the landing page the reverse.

## Marquee logos blank on iOS, partner row realigned, 2026-10-31

**FIXED and LIVE.** Eline, on her phone: *"This is not loading"* against the
marquee, then *"in mobile, sponsors not loading and fix the measurement of the
sponsors below"*.

⚠️ **`width:auto` ON AN INLINE `<svg>` IS ZERO IN SAFARI AND CORRECT IN
CHROME.** The marquee logos were sized by HEIGHT only, with `width:auto`, and
their size came from the `<symbol>`'s viewBox. Chrome infers the width from
that viewBox; Safari collapses it to zero, so the band rendered as an empty
cream strip on iOS and looked perfect in every check I ran. **The partner
plates right below were fine the whole time, and that is what identified it**:
those have always carried an explicit width.

Each marquee logo now has an explicit width = its height x that SYMBOL's own
viewBox ratio (bf 560/87, suits 175/48, oc 189/35), so the artwork keeps its
proportions rather than inheriting the node box's padding. The sweep now
asserts every marquee logo has real width and height, which is the check that
would have caught this.

⚠️ **NOT VERIFIED ON A REAL iOS DEVICE** -- the local browser is Chromium, where
it never failed. The cause is inferred from the one structural difference
between the logos that broke and the ones that did not. If it is still blank on
her phone, that inference is wrong and it needs looking at with her device.

⚠️ **AN UNASSERTED REPLACEMENT SILENTLY HALF-APPLIED.** The same patch tried to
add an `xlink:href` fallback for pre-2018 Safari. Two of its three replacements
did not match, and because those lines carried no assertion -- unlike every
other edit in that script -- it failed silently, leaving ONE `<use>` with xlink
and the rest without, plus a dangling `xmlns:xlink`. Removed entirely: `<use
href>` has been supported since Safari 12 and the real cause was the width.
**Every replacement gets an assertion, or it is not a replacement.**

**The partner row now splits the plate's width.** The frame draws the two small
plates 136 wide under a 342 plate, so 136+10+136=282 floated 60px narrower than
the plate above and read as a mistake. They are now `flex:1` inside a row
capped at the plate's own max-width, so the row is always flush: one plate
above, two half-width below. Measured flush at all 17 widths.

⚠️ **This is my reading of Eline's "these can be aligned like 1:2:2"**, taken
with "fix the measurement". It deviates from the frame deliberately and is one
line to revert if she meant something else.

## Announce bar retitled, SPONSORED BY dropped, 2026-10-31

**APPLIED and LIVE** on both steps. Eline: *"Joshua the red bar at top"* with a
screenshot, and *"also joshua remove the sponsored by as well on the moving
sponsors"*. Joshua confirmed: *"moving sponsor is the marquee"*.

    announce bar   SECURE YOUR SEAT
                   -> 2 DAYS BEFORE AFFILIATE WORLD BANGKOK · LIMITED SPOTS
    marquee        the SPONSORED BY label and its rule are gone; logos only

⚠️ **The separator is the one character read off a screenshot**, not from a
node. `·` follows the page's own house style ("DAY 3 · INVITE ONLY",
"BANGKOK · DEC 7-8, 2026"). Worth confirming.

⚠️ **THE BAR WAS A FIXED 36px AND THE NEW LINE DOES NOT FIT IT.** At 14px the
text measures 407px against ~296px of usable width at 320. It wrapped to two
lines **inside** a 36px box with `overflow:hidden`, so 32px of text sat in a
36px bar: it passed a height check and a clipping check, and looked like an
orphaned "SPOTS" on every phone below 414. A generic sweep cannot catch this,
because nothing is technically broken.

Fixed with `min-height` instead of `height`, 5px of vertical padding and
`text-wrap:balance`. One line at 414 and up; two balanced lines below, bar 45px.
Shrinking the type to hold one line would have needed **10px at 320**, which is
not readable, so the bar grows instead.

⚠️ `T("1027:384")` is no longer read, so the `v3_1027_282` dump frame holding
the two SPONSORED BY nodes is now unused. Left in place: it is harmless, and
`design_diff` will report the label as missing from the page, which is correct
and expected rather than a defect.

Re-swept both pages at 19 widths each, 38 checks, all clean.

## The Scalizard badge vanished on phones, 2026-10-31

**FIXED and LIVE.** Caused by the General Admission rename earlier the same
day, found by Joshua: *"what happened to this"*, a 425px screenshot with the
badge shrunk to a dot.

⚠️ **A COPY CHANGE SILENTLY BROKE A THIRD SECTION'S LAYOUT.** `.sof-ttop` set
`grid-template-columns:max-content minmax(0,1fr)`, and the comment above it
states the intent plainly: the title never wraps, the badge takes whatever is
left. That held while the title was "EARLY BIRD". "FULL ACCESS PASS" is
**290px unwrapped**, so column 1 claimed the entire row:

    375px viewport -> badge 0x0      390px -> badge 0x0
    425px          -> badge 30px     479px -> badge 91px

**0x0 at 375 and 390, the two commonest phone widths.** It shipped that way
this morning and nothing caught it: the copy was right, the colours were right,
the image was right, nothing 404'd, no console error. Only a measurement of the
rendered box shows it.

Fix inverts the rule: `minmax(0,1fr) auto` with the badge given a definite
96px, so the TITLE wraps into what is left. A title that wraps is a layout
choice; a badge that disappears is a bug. The 375-479 block's `max-width:96px`
override became redundant and was removed rather than left to drift.

⚠️ **MY SWEEP HAD THE WRONG SCOPE AND MISSED IT.** The 25-width sweep an hour
earlier checked only the two sections being rebuilt. The break was in a third
section, from a copy change made earlier the same day. **Sweep the page, not
the diff** -- a copy change can move any layout that sizes itself from text.
The sweep now covers the ticket card too: badge width, name/price/badge
escaping the card, and name over badge.

Re-swept live at **28 widths, 320 to 2560: all clean.** Badge 108 through the
phone band, 182-227 on tablet, 173-239 on desktop.

## Marquee and partners rebuilt from the V2 frame, 2026-10-31

**APPLIED and LIVE.** Patch: `edits/patch_marquee_and_partners.py`, then built
to a throwaway step, QA'd, and promoted:

    SOF_SLUG=sof-v3 py pagescore/build_sof_event.py                 test
    SOF_SLUG=scaling-failing LF_ALLOW_REDEPLOY=scaling-failing ...  promote

Joshua: *"make a separate step then build from there one everything is working
replace the live with the tested version"*. `/event/sof-v3` is the throwaway
and still exists; LF has no deleteStep.

New Figma frame "Scaling Or Failing V2" `1027:282`. Two sections changed, and
*"the ticket design on the figma is stale so dont pay any mind to it"*.

| | was | now |
|---|---|---|
| marquee | gold band, six phrases looping | cream band, SPONSORED BY over a red rule, the three sponsor logos looping |
| partners | MAIN PARTNER / POWERED BY 48 / one 368x105 plate | OUR PARTNERS / POWERED BY 70 / 760x200 plate + a new row of two 280x96 plates |

⚠️ **THE NEW FRAME IS 1440 WIDE. THE OLD ONE WAS 1920.** Every other section
was drawn at 1920 and renders inside the `.sof-scale` zoom that maps 1920 onto
1400, so a value read off the new frame is 3/4 of what the desktop CSS expects.
**Every desktop number is the measured value x 4/3.** Build it as drawn and
these two sections come out a quarter small while every string and every hex is
still correct, which no copy or colour check can see.

⚠️ **THE SAME LOGO SHIPS IN TWO COLOURS** — BestFulfill is navy in the marquee
and red `#C01400` on its plate. So each logo is ONE `<symbol>` with
`currentColor` and the colour is set in CSS where it is used. Checked first
that every `fill="white"` in the exports is a `<clipPath>` rect, never artwork.
One symbol per brand, taken from the PLATE export: Figma exported the marquee
Outcraft clipped (182x38 against its node's own 204x37), and the plate exports
are unclipped with aspect ratios matching to within 1.7%.

⚠️ **THE MARQUEE GOES BELOW THE NAVY STATS BAND, NOT ABOVE IT.** It replaced
the ticker, which sat between the hero and the stats, so it silently inherited
that slot and shipped there. Joshua: *"wrong placing for the marquee it should
be below the navy"*. The frame is unambiguous and should have been read first:
in 1027:283 the stats section 1027:354 runs y=998.0 to y=1196.2 and the marquee
1027:382 starts at exactly **1196.2**. Section order comes from the frame's own
y values, never from inheriting the slot of the thing being replaced.

⚠️ **THE SEPARATE STEP EARNED ITS KEEP IMMEDIATELY.** The rebuild put
**"GET EARLY BIRD TICKET" back on the desktop hero**. The live page had been
right because the bake matched on button TEXT and caught all three buttons; the
builder's COPY_EDITS only overrode the MOBILE hero node. The hero CTA is TWO
nodes, 949:1558 mobile and **949:1121 desktop**. Had this gone straight to
live, a sold-out-price page would have advertised early bird at the top.

⚠️ **A FLEX GAP ON THE BAND SPACED NOTHING.** `section()` wraps the markup in
`.sof-cap`, so `.sof-marqbar` has exactly ONE child and `gap` on it does
nothing. Measured 0px where the design says 14 / 29, and Joshua spotted it:
*"i saw on some screen this does not have space between them"*. The flex column
belongs on `.sof-marqbar > .sof-cap`.

⚠️ **THE EDGE FADE CANNOT BE A CREAM RECTANGLE HERE.** The frame draws it as a
gradient in the band's colour, which works on Figma's flat parchment and fails
on this page, which paints a real texture: it read as two pale patches with a
visible edge. It is now a `mask-image` on the strip, fading the LOGOS, which is
correct over any background and costs two fewer elements.

⚠️ **The band cream `#F7ECCE` came out of the fade gradient**, not the frame
fill, which is a parchment IMAGE. The opaque stop of a fade is the colour it
fades FROM. The constant is now unused, since the mask replaced it.

⚠️ **TWO SUBSTRING TRAPS, BOTH CAUGHT BY ASSERTIONS.** `sof-tick` is a
substring of **`sof-tickets`**, so asserting the ticker was gone reported the
TICKET section as leftover ticker. And `mask-image` was already in the builder
four times (`.sof-decide`, the hero), so an absolute count failed where a delta
was needed. Same shape as the `data-cd-ends` and `$1997` false positives.

The design dump gained a fourth frame `v3_1027_282` holding the two SPONSORED
BY nodes, so the label is still read from the node rather than typed, and
`design_diff` can check this section later. Backup:
`runs/sof-2026-10-21-v7/design.pre-v3-2026-10-31.json`.

⚠️ **SWEPT 25 WIDTHS, 320 TO 2560, BECAUSE THREE IS NOT A SWEEP.** Joshua
asked whether every screen size had been checked and the honest answer was no:
390, 768 and 1440 only. This repo has already shipped a bug that existed ONLY
between 768 and 991 (the Trustpilot overlap on jFrY0DhRi), where exactly those
widths prove nothing. The sweep checks, at every width: horizontal overflow,
the heading-to-logos gap, both partner plates staying on ONE row rather than
stacking, the marquee still sitting below the navy, and any child of either
section escaping its own bounds sideways.

All 25 clean. Gap 14 below 1024 and 15 to 21 above it (29px CSS through the
zoom). Plates side by side throughout. No bleed anywhere.

⚠️ **414 to 1023 uses the MOBILE sizes for both sections**, because the V2
frame only draws 390 and 1440 and there is no tablet frame to read. The main
plate therefore stays 342px until 1024. This is NOT a regression: the previous
build did the same (`max-width:368px` until 1024). Checked by eye at 900 and it
reads correctly, but if a tablet frame ever lands, this band is where it goes.

Verified live at 390, 768 and 1440: marquee gap 14 / 29, logos navy and the
plate logo red, two small plates, zero console errors, the Stripe link and the
contact form untouched.

## General Admission baked into the page, 2026-10-31

**APPLIED and LIVE.** `edits/bake_general_admission.py --apply`. Rollback is
one write each of `steps/scaling-failing.pre-bake-ga-2026-10-31.json`,
`steps/contact.pre-bake-ga-2026-10-31.json` and
`header_scripts.pre-bake-ga-2026-10-31.html`.

Joshua, once the flip had fired: *"now that it is live we can change it so it
does not apply with script but a permanent change"*, and *"countdown is done we
can make it permanent now"*.

The runtime flip was the right shape while the change was in the FUTURE and had
to happen at an exact instant with nobody awake. It is the wrong shape once the
instant has passed: the real copy is the copy, and a visitor should not need
JavaScript to be told the price. So the post-Early-Bird page is now written
into the page, and `sof-price-flip` is gone from `header_scripts`, which is
back to its pre-flip 8,045 chars.

The countdown bar is removed from BOTH bodies. The gold is painted on
`.sof-cd` itself, so dropping that one div leaves its section at **0px**,
measured, with no band.

⚠️ **`?eb=ended` and `?eb=live` died with the script.** They existed to preview
an unreleased state. There is no unreleased state now.

⚠️ **The two pages carry DIFFERENT countdown markup**, because the digits are
rendered at build time: the landing page said 36 MIN 09 SEC and contact said
35 MIN 29 SEC. One hardcoded `old` string would have matched one page and
silently missed the other, which is exactly how the deadline move went wrong
the day before. The script extracts the string from each body instead.

⚠️ **ORDER IS THE SAFETY, AND IT IS ONE-WAY.** Bodies first, then the served
HTML is checked, and the script is retired ONLY if that check passed. The other
way round leaves a window where the body still says Early Bird and nothing is
left to correct it. While both are in place they agree, so there is no visible
moment of change.

⚠️ **GREPPING A SERVED PAGE FOR A BARE STRING TESTS THE COMMENTARY TOO.** The
first run reported "$1997", "SAVE $1,000", "ENDS OCT 30" and "sof-cd-units"
all still present on BOTH pages, including "$1997" on contact, which has no
ticket card at all. Every one was a comment: two in the flip script's own
explanation of what it replaces, one in the page's CSS note deriving
1997 + 1000 = 2997, and the countdown's leftover CSS rules. A later run added
`data-cd-ends`, which the page's own footer script reads BY NAME and keeps
reading harmlessly. The body edits had landed perfectly every time. Checks are
now element-precise (`>$1997<`, `class="sof-cd"`), and the guard refusing to
retire the script on a failed check is what made three wrong readings cost
nothing.

**The builder was updated in the same breath**, or a rebuild would have quietly
restored Early Bird pricing. `pagescore/build_sof_event.py`: the gold strip
reads LIMITED SEATS, `ticket_card()` no longer emits the `--urgent` pill or the
`.sof-tcompare` element, and COPY_EDITS carries FINAL PRICE / FULL ACCESS PASS
/ $2997 / SECURE YOUR SEAT. Verified statically: 7 format placeholders against
7 arguments, emitting exactly the markup now live. `countdown_html()` needed
nothing; it already returns "" past the deadline.

The CSS for `.sof-tcompare`, `.sof-badge--urgent` and the countdown is left in
place, unused. Removing it is risk for no gain, and it is what a reinstated
Early Bird would need.

Verified live: both pages read right with zero DOM mutations in 2 seconds, so
the page is now genuinely static. `?ref=RONAK` still puts the affiliate code on
both buttons. Zero console errors.

## Countdown moved to US Pacific, 2026-10-30

**APPLIED and LIVE.** `edits/move_countdown_to_us.py --apply`. Rollback is one
write each of `steps/scaling-failing.pre-countdown-move-2026-10-30.json` and
`steps/contact.pre-countdown-move-2026-10-30.json`.

The Early Bird deadline was 23:59:59 **Bangkok** on 30 October. The team asked
for US time instead: *"lets have it run US timezone today as it is, just timer
needs to move"*. It is now 23:59:59 **US Pacific** on the same date.

    was   2026-10-30T16:59:59Z
    now   2026-10-31T06:59:59Z   = 31 Oct 14:59 Manila, 13:59 Bangkok

Pacific rather than Eastern because it is the later of the two US midnights.
30 October 2026 is still PDT; US daylight time does not end until 1 November.

**The "ENDS OCT 30" pill is still true and was deliberately left alone.** It is
still the 30th in the timezone the deadline now runs on.

⚠️ **THE CONTACT PAGE HAS ITS OWN COUNTDOWN, and the first run missed it.**
`build_sof_event.py` mounts both `promo_html()` and `countdown_html()` on BOTH
page variants, so `/event/contact` carries a second copy of the bar with its
own `data-cd-ends`. The first apply moved the landing page only, which would
have left a timer reading zero on one page and running on the other. It
surfaced by luck: an unrelated marker count on the contact page dropped by one.
Anything keyed on `data-cd-ends`, `.sof-promo` or `.sof-cd` is a TWO STEP edit.

⚠️ **The deadline lives in FOUR places and all four moved together.** Both step
bodies, plus `COUNTDOWN_ENDS` in `pagescore/build_sof_event.py` and a second
literal `datetime(2026, 10, 31, 6, 59, 59)` inside `countdown_html()`. Miss
either of the builder two and the next rebuild silently drags it back.

⚠️ **Why the step body and not `header_scripts`.** The page's own countdown
script reads the deadline ONCE into a closure, from the attribute in the served
HTML, and that script is inline at the end of `<body>`. A header script cannot
reach the variable afterwards, so patching the attribute from the header would
always be too late and the bar would keep counting to the old time.

Verified live on both pages: new instant served, old instant gone, bar renders
at 92px and counts, zero console errors, price untouched at $1997.

Verified after applying the flip, at `?eb=ended`: both pages show the whole
after state correctly at 1440 and at 390, no horizontal overflow, the
countdown bar gone, the contact form untouched, zero console errors. The
normal URL still shows the full Early Bird state. `?ref=JEM&eb=ended` proves
the flip and the affiliate rewrite do not fight: 8 DOM mutations in 2
seconds, which is exactly the countdown ticking its four digits, with the
promo code on both buttons and the new copy in place.

## Price flip when the timer hits zero, 2026-10-30

**APPLIED and LIVE 2026-10-30.** `edits/wire_price_flip.py --apply`. Rollback
is one write of `header_scripts.pre-price-flip-2026-10-30.html`.

Joshua applied it WITHOUT the Stripe link settled, knowingly: *"can we make
it auto if timer runs out we change the text, unfortunately no payment link
yet i will supply it later tho"*. So there is a standing deadline below.

Joshua: *"lets make it so after the timer the price visible would be the
compare."* At `2026-10-31T06:59:59Z` the page stops selling Early Bird by
itself, with nobody awake.

⚠️ **EARLY BIRD IS WRITTEN IN SEVEN PLACES.** Flipping only the number leaves a
card promising a $1,000 saving while charging full price. The copy the team
agreed in chat on 2026-10-30:

| where | now | after |
|---|---|---|
| `.sof-tbanner b` | LOWEST PRICE IT WILL EVER BE | LIMITED SEATS |
| `.sof-tname` | EARLY BIRD | FULL ACCESS PASS |
| `.sof-tprice` / `.sof-tcompare` | $1997, $2997 struck | $2997, no strike |
| `.sof-tbtn span` | GET EARLY BIRD TICKET | SECURE YOUR SEAT |
| `.sof-cta span` (hero, x2) | GET EARLY BIRD TICKET | SECURE YOUR SEAT |
| `.sof-promo span` (both pages) | GET EARLY BIRD TICKET & SAVE $1000 | SECURE YOUR SEAT |
| `.sof-badge` (first) | SAVE $1,000 | FINAL PRICE |
| `.sof-badge--urgent` | ENDS OCT 30 | removed |

The sticky bar and the pill wording were not named by the team and are
flagged to Joshua. The countdown bar is an eighth place and needs nothing;
it removes itself at zero.

⚠️ **ONE PILL HAS TO SURVIVE, AND THAT IS A LAYOUT FACT, NOT A TASTE ONE.**
Hiding both was the first attempt; Joshua: *"feels empty"*. Measured, he was
right. `.sof-ttop` is a three-row grid (pills / name / price) and the
Scalizard spans all three. The sticker is TALLER than the name and price
together, so hiding the pills does not collapse the row: the slack pools in
it, leaving **90px of dead space above the title**. Keeping one pill fills
the row the design drew and needs no CSS override at all, 90px down to 0.
"SAVE $1,000" cannot stay because it is false at full price, so the pill is
rewritten to "FINAL PRICE" and its `--urgent` sibling is hidden.

⚠️ **A COMMENT PLACED ONE LINE WRONG SILENTLY KILLED THE WHOLE RULE.** The
first reinstall put explanatory text AFTER a `*/` instead of inside the
comment. CSS does not error: the stray words swallowed the next selector, so
`display:none` stopped applying and both the old pill and the struck-through
price came back. Nothing in the apply output looked wrong. Only reading the
rendered page caught it. The script now ships a comment-balance check.

⚠️ **`--reinstall` replaces an installed block** instead of refusing, for
iterating on copy and layout. It cuts from the marker comment to the end of
`header_scripts`, which is safe ONLY because this block is appended last, and
it asserts that Lenis, the contact handler and the affiliate rewrite are not
inside what it is about to cut. The backup is never overwritten, so
`header_scripts.pre-price-flip-2026-10-30.html` stays genuinely pre-flip.

⚠️ **`?eb=ended` previews the after state on the live page**, `?eb=live` shows
the before state once the deadline has passed. That is the answer to Eline's
*"wala ba tayong di live na website para matest"*: there is no staging here and
this removes the need for one. Deliberately NOT remembered between pages, so a
preview cannot leak into a normal visit the way a sticky `?ref=` could.

⚠️ **No flash.** The script runs in `<head>` and sets a class on `<html>`
before the body exists; CSS holds the five changing strings at
`visibility:hidden` (not `display`, so nothing moves) until the swap has run.
Without it $1997 paints for a frame and then jumps.

⚠️ **TWO THINGS IT DOES NOT DO, and the first one costs money.**
1. ⚠️ **IT DOES NOT TOUCH THE STRIPE LINK, AND THAT IS NOW A HUMAN STEP
   ON A CLOCK.** Joshua, 2026-10-31, three minutes before the deadline:
   *"change of plans we would use the old link and eline would just change
   the product"*. So every button keeps
   `buy.stripe.com/3cIfZh0RM201aiyg01dby04` and Eline reprices that one link
   in Stripe. The page switches to $2997 by itself; the link does not.
   Until she has done it, the page asks $2997 and the checkout takes $1997.

   A General Admission link was supplied and wired for about ten minutes
   before the plan changed: `buy.stripe.com/aFa4gz1VQ4893Ua157dby08`, "SoF
   General Admission", $2,997.00, verified live, and the affiliate codes
   work on it (JEM gave $2,547.45, the same 15%). It is in this file's git
   history if the plan changes back.

   ⚠️ **If a link swap ever comes back, swap the PATH, never the whole
   href.** The affiliate script writes `?prefilled_promo_code=` onto these
   same anchors; replacing the href wipes an affiliate's code on every
   observer pass and the two scripts then overwrite each other forever.

   ⚠️ **The `--reinstall` cut guard cannot probe on
   `prefilled_promo_code`.** A previously installed price-flip block can
   name it in its own comments, and the guard then fires on our own text and
   refuses to write. It cost a minute of a three-minute window. The probe is
   `sof-affiliate-ref`, which is unique to the affiliate block.

2. It does not correct the Meta pixel. AddToCart and InitiateCheckout carry
   `value:1997` hardcoded in the page's own footer script, inside a closure a
   header write cannot reach. After the flip both under-report by $1000.
   Fixing it means a page rebuild.

## Affiliate promo codes via `?ref=`, 2026-10-30

**APPLIED and LIVE.** `edits/wire_affiliate_ref.py --apply`. Rollback is one write
of `header_scripts.pre-affiliate-2026-10-30.html`.

Seven affiliates each had their own Stripe link, identical but for the code on the
end. Instead of seven copies of the site, the page reads the code off its own URL:

    scalingorfailing.com/event/?ref=JEM
      -> every Stripe button becomes ...?prefilled_promo_code=JEM

**Joshua's two calls:** the parameter is `ref` and only `ref`; and ANY code is
accepted rather than a fixed list, so a new affiliate works the moment the code
exists in Stripe with no edit here.

Rewrites every anchor whose href starts with `https://buy.stripe.com/`, which is
three links today: `a.sof-promo` and `a.sof-tbtn` on the landing page, and
`a.sof-promo` on contact. Matching on the href rather than the class means a
fourth button added later is picked up for free.

**Checkout is Stripe now, not Whova.** The "Decisions already made" section above
still says Whova and is out of date on that point; only the privacy policy's
Whova references remain accurate.

⚠️ **The code is cleaned before it is used.** Uppercased, and accepted only as
1-40 chars of `A-Z 0-9 _ -`. Verified live that `<script>alert(1)</script>`,
`X&redirect=evil.com`, 60 characters and an empty `?ref=` all leave the plain
link untouched, while `?ref=  jem  ` correctly yields `JEM`. So a hostile value
cannot reshape the Stripe URL: it never reaches it.

⚠️ **The code is remembered in sessionStorage for the visit.** Without it the nav
trip to `/event/contact` and back would drop the code and the affiliate would
lose the sale. Verified: land with `?ref=GONZALO`, click CONTACT, come back to a
URL with no parameter, and both buttons still carry GONZALO. A later `?ref=DEE`
in the same tab overrides it. Session scope, so it dies with the tab.

⚠️ **A MutationObserver re-applies it, and it needs both its guards.** LF hydrates
blocks from JSON after load and can replace these anchors, which would silently
drop the code. A link already carrying the right code is skipped, so the pass
writes nothing and cannot re-trigger the observer, and the callback is debounced
to one run per animation frame, because an unthrottled document-wide observer
running `querySelectorAll` is itself a scroll-jank source on a page running
Lenis.

⚠️ **All seven codes were checked at Stripe, not assumed.** Every one is active
and gives exactly **15% off**: $1,997 subtotal, $1,697.45 due. An unknown code
just means no discount, which is the same outcome as a typo in a hand-made link.

⚠️ **Reading the Stripe page too early reports a false negative.** At 6 seconds
the checkout still showed the full ₱132,271.03 and looked like the code had been
ignored. The discount lands around 9 seconds. Wait before concluding a code is
dead.

## Contact form wired to n8n, 2026-10-14

The form was inert by design: no `action`, submit button `disabled`, and a note
saying "This form is not connected yet". It now posts to n8n workflow
`qDbixpOcwNHtaC3k`, which validates the submission and emails it to
`hello@scalingorfailing.com`.

    POST https://primary-production-f5243.up.railway.app/webhook/sof-contact

**APPLIED and LIVE 2026-10-14.** `edits/wire_contact_form.py --apply` ran, all
five replacements landed, and the full chain was tested: a real submission
reached hello@, and honeypot, bad-email and tampered-topic submissions were all
rejected before the mail node.

⚠️ **One job left:** the privacy policy on BOTH pages still says the form "is not
connected yet, so nothing typed into it is sent or stored anywhere". False now.
Fix written and dry-run clean, not applied:
`py funnels/sof/scaling-or-failing/edits/fix_privacy_contact_form.py --apply`.

Handover for the next session: `CONTACT-FORM-IMPLEMENTATION.md` in this folder.
n8n side: `../../../../N8N/documentation/sof-contact-form.md`.

Two writes, because the halves live in different places:

- **Step body** (`contact` only): drop `disabled`, mark name/email/message
  `required`, add an off-screen honeypot `website` field, reword the note.
- **Funnel `header_scripts`**: the submit handler, 2,118 chars appended after
  the Lenis block (3,418 -> 5,536). It has to be funnel level because that is
  the only script slot this account exposes, so it is guarded on
  `form.sof-form` and is inert on the landing page.

The POST is form-encoded on purpose. That is a CORS "simple request", so the
browser sends no preflight `OPTIONS`; n8n parses it into `body` just the same.

`wire_contact_form.py` archives the pre-edit body to
`steps/contact.pre-wire-<date>.json` before writing, and is idempotent: it stops
if it finds the honeypot in the body or the marker `sof-contact-form -> n8n` in
`header_scripts`.

## A native checkout, built while Stripe was held, 2026-11-03

Joshua: "there is a checkout step on the SOF funnel make a simple checkout
for me asap our stripe got held so we need this". The existing `checkout`
step on the main funnel (`fun_RoOL_WXDCAxK4hEk0v5xX`, slug `_f7tcJ5FS`) was
an empty, auto-generated LF `checkout_page` -- created at some earlier point,
never used, no product attached. Every ticket sale until now went through an
external Stripe Payment Link (`EB_HREF`), never through Lightfunnels' own
commerce system at all.

NOT actually blocked by Stripe being down. The funnel's real payment gateway
is `pg_eZsF6TBLT4dKdQBj3d70t`, "Airwallex: Tholding Limited" -- already
active, live, not test. Confirmed separately: Airwallex is already
processing real charges on the HLTH Shopify store, so the account itself is
verified; nobody had built an LF checkout for SOF before, that is all.

### Where it lives

A SEPARATE funnel, not the live one: `fun_MaCLh5DOqyw_f1Viin3Z_`, slug
`sof-checkout`, sharing the same domain (www.scalingorfailing.com) as the
main funnel.

    https://www.scalingorfailing.com/sof-checkout/buy-now    the buybox
    https://www.scalingorfailing.com/sof-checkout/checkout   the checkout

Product: `prod_2BrK1IFKYkRFeSIeDgFj7`, "Scaling or Failing 2026 -- Full
Access Pass", $2,997, matches the live ticket card exactly (949:1458 /
949:1459). `edits/attach_checkout_product.py` is a dead end, kept only as a
record -- see below.

### What actually blocked this, in order, each one found by testing rather than guessed

1. `checkout_page` does not render a payment form from a bare `product_id`.
   Tried both ways (updateFunnel after creation, product_id at createStep
   time): `Lightfunnels.product` stayed null client-side either way, read
   directly off the page's own embedded globals, not inferred.
   `attach_checkout_product.py` is this failed attempt, preserved as the
   record of what does NOT work.

2. The real mechanism, found by reading the account's one working checkout
   (the Garlic/Vitruevian supplement funnel, `fun__LKgKGNO4H6IoYoFN6RfK`): a
   `product_page` step carries the `product_id` and is the actual buybox;
   `checkout_page` carries `product_id: null` and is a hand-built block tree
   (BillingAddress / PaymentMethod / CheckoutSummary / ShippingRatesForm /
   OrderBump, ~20 block types) that reads whatever is in the cart. Built
   accordingly: `build_simple_checkout.py` writes a minimal product_page
   body and COPIES Garlic's checkout body verbatim (then de-brands it --
   see below).

3. `checkout_page` cannot be a funnel's `starting_step_id`
   (errors_wrong_starting_step_type). A `squeeze_page`-turned-`product_page`
   step goes first.

4. A new funnel has no `preferred_domain` and 404s on the shared domain
   until `InputFunnel.preferred_domain_id` is set to the SAME domain id the
   main funnel already uses (dom_9ciTn2rct15S93by6AME0). Multiple funnels
   can share one domain at different slugs.

5. A new funnel has no `active_payment_methods` either, even once the steps
   and domain are right -- confirmed by decoding the page's own embedded
   GraphQL request context, which showed "paymentGateways":[]. Fixed with
   the SAME ChannelPaymentGatewayInput shape read off the working funnel
   (id, pm_amount_adjustment_direction: "extra", pm_amount_adjustment_type:
   "percentage", pm_amount_adjustment_value: 0, settings: {}).

6. The product needs at least one option group, or createProduct rejects it
   ("Some options are missing") -- there is no such thing as a plain,
   option-less product on this platform. Gave it one ("Ticket" -> "Full
   Access Pass") and a hidden ProductOptionRow / ProductOptionLabel /
   SelectComponent trio on the buybox so the single value auto-resolves
   without showing the shopper a pointless one-option dropdown.

7. `action: "add-to-cart"` SWALLOWS `destination` entirely, on every shape
   tried -- {"type":"step"} (Garlic's own button's exact value), and the
   ":scheme://:host/:funnel/:step(id)" dynamic template (copied verbatim
   from the account's upsell "Add to my order" button). Both filled the
   cart cookie correctly on every click (read back directly, confirmed
   working) but never navigated, with no console or Sentry error either.
   Cloning Garlic's ENTIRE 1.7MB landing page onto this product confirmed
   why those two forms exist there: that page's buy button sits behind a
   PriceBundle quantity-discount widget this ticket has no use for, and
   copying it wholesale just disabled the button outright (our product has
   no price bundles). Fix: no `action` key at all, a plain `destination:
   {"type":"static", "value": "<absolute checkout URL>"}`. Ordinary link
   semantics, not the special add-to-cart handler.

### De-branding the borrowed checkout body

Six blocks removed from the copied 165KB tree, each located by walking for
its exact block type or exact copy string (never a blind substring
replace), each verified against its full subtree before cutting, so nothing
adjacent (the Repeater that reads the cart, the Subtotal/Total block,
PaymentMethod, the Pay Now Button -- all plain siblings of what got cut) was
at risk: `edits/clean_checkout_copy.py`.

  - a BlockLink to the Vitruevian logo, pointed at vitruevian.com
    (build_simple_checkout.py, done first -- the one thing a substring
    search for "Vitruevian" actually found)
  - the "Shipping method" heading + a ShippingRatesForm charging a
    hardcoded $10.09 -- wrong on its face for a digital ticket
  - an OrderBump offering a "Bluetooth Alarm Clock Temperature" -- a
    DIFFERENT PRODUCT of theirs, not ours
  - a fake "Due to high demand your order is reserved for: 00:00" timer,
    stuck at zero
  - the supplement trust badges, THREE separate copies found in three
    different containers ("+150,000 Customers" / "30-Day Guarantee" /
    "Fast Shipping" / "Secure Checkout" at the page top; "Excellent /
    150,000 Reviews / over 150k shipped products / 30-Day Satisfaction
    Guarantee / 3rd-Party Lab Tested Softgels" inside the form column AND
    again inside CheckoutSummary)

### The footer links were dead, not just mislabelled

Found by reading every link's actual href, not by looking at the label.
Four ("Refund policy", "Shipping", "Privacy policy", "Terms of service")
were a dynamic destination naming STEP IDS THAT EXIST IN GARLIC'S FUNNEL,
NOT THIS ONE -- every one resolved to ".../sof-checkout/undefined", a dead
link. "Contact" was worse: a static link straight to
https://99brands1.myshopify.com/pages/contact, an unrelated Shopify store.
This ticket funnel has no policy pages of its own, so the four dead ones
were REMOVED rather than pointed at content that does not exist; Contact
now goes to the real, already-live /event/contact.

### Verified, and what is NOT yet verified

Clicked through live in a real browser, repeatedly, after every change:
buy-now -> add to cart -> checkout, item + $2,997-equivalent shows correctly
in the order summary, Airwallex renders as the payment method, 0 console
errors on the final version (one earlier run showed 1, from Airwallex's own
report-only CSP notice, unrelated to anything built here).

NOT done:
  - Nothing on the live page points here yet. The real "SECURE YOUR SEAT"
    button and the promo bar still point at the dead Stripe link (EB_HREF).
    Swapping that is a deliberate, separate step, held back on purpose
    until Joshua signs off -- real customer traffic, first time this exact
    payment path has ever been used.
  - No real transaction has been completed. Everything above is confirmed
    through the point of reaching the Pay Now button with the right item
    and the right gateway selected; nobody has clicked Pay Now with a real
    card.
  - No thank_you_page. Garlic's funnel has one; this does not. A missing
    confirmation screen is a far smaller problem than a payment form that
    mischarges someone, so it was left for later rather than rushed.
  - The product has no image -- shows as a blank thumbnail in the order
    summary. Cosmetic, not blocking.
  - Currency displays in PHP (geo-based, e.g. "PHP 189,922.91" for the
    $2,997 ticket). Confirmed this is NOT specific to this build: the same
    behavior is already live on Garlic's own working checkout drawer, shown
    PHP from this same visitor IP. Platform behavior, not a defect
    introduced here -- flagged for Joshua rather than assumed fixed.

### Switched to Joshua's own product, and collapsed the stopover page, 2026-11-03

Joshua: "change product to the one i created" -- `prod_p4MkRss_YruVzCqlVb5z8`,
"SoF General Admission", $2,997, a real uploaded image. Checked before
switching: zero option groups and zero variants in the GraphQL read (the
opposite of `prod_2BrK1IFKYkRFeSIeDgFj7`, which NEEDED one because
`createProduct` rejects a bare `options: []`) -- created through the
dashboard rather than the API, which apparently does not hit that rule. A
real add-to-cart click still resolved a genuine numeric variant id
(4301675370, confirmed twice), so the product works despite reading as
option-less.

Then: "so it does not need to go to this page and direct to checkout" /
"no we need no hop in between" -- the two-click flow (real button -> a
small buybox page -> checkout) was not the end state wanted. ONE TRIED-AND-
REVERTED APPROACH, kept here as a record of what does NOT work: flipping the
sof-v3 step's own type to `product_page` with `product_id` set directly on
it. The page rendered perfectly (step type has no visible effect on a
custom HTML body), but clicking ANY outbound link on it -- regardless of
its own href -- got intercepted and redirected to a DIFFERENT FUNNEL's
entry step, with the WRONG product attached, and a "No variant is selected"
error. The mechanism is "this whole step broadcasts its own product on any
exit", not "this one link adds to cart"; not controllable per-button, so
not usable here. Reverted (type back to `article_page`, product_id back to
`null`) before anything else was tried.

**What actually worked**: the cart is nothing more than a cookie,
`lf_609354_cart`, read back in the exact shape confirmed by real add-to-cart
clicks:

    {"body":[{"price_bundle":null,"variants":[
        {"quantity":1,"id":4301675370,
         "payment_settings":{"type":null,"cycle":null}}]}]}

So the real page's own two buttons (`a.sof-promo`, `a.sof-tbtn`) got an
`onclick` that writes this cookie directly, then the anchor's own
unmodified `href` carries the SAME click straight to
`/sof-checkout/checkout` -- one click, nothing platform-managed to
mis-fire, both verified in a real browser with the cart cookie cleared
first:

    `edits/wire_one_click.py` -- scoped to the sof-v3 TEST step only via
    `step_uids`, same pattern as every other single-step edit in this file.
    Finds the exact anchor markup in the real (unescaped) `content` string
    values, not in a `json.dumps`'d blob, which double-escapes every
    quote and was the first version's bug (0 matches, silently).

Not yet done: the live page's two buttons still point at the dead Stripe
link. This whole mechanism is proven on the TEST clone only.

### Checkout polish and discount codes, 2026-11-03

- **Express checkout removed.** `ExpressCheckout2` plus its "Express
  checkout / OR" label-and-divider row rendered empty (no Apple/Google Pay
  available in this context) -- both containers cut from `CheckoutSummary`
  entirely rather than leaving a dead gap.
- **Theme match.** The funnel's own style palette
  (`static_primary_color_buttons_links` etc., read/write via
  `Funnel.styles` / `InputFunnel.styles`) was generic LF blue; set to the
  site's navy (#041C32) and gold (#FCCF44). Two buttons had the color
  HARDCODED rather than palette-bound (`Pay Now`, the mobile-accordion
  `Apply`) and needed a direct edit instead. Added a navy header band with
  the SOF logo to all three steps (checkout, buy-now, buy-test).
- **The "needs padding" fix was real the second time, not the first.** The
  first attempt (the header's own bottom padding) only ever LOOKED like it
  fixed the gap -- on mobile, the stacked Order Summary sits above Contact
  and created the illusion of space. Desktop's 2-column layout exposed the
  real bug: the form column's OWN `padding.top` was hardcoded to `0px` in
  BOTH its base and its `media:991` style rules. Set to `38px` desktop /
  `21px` mobile, matching the container's own left/right/bottom scale.
  Checked at both breakpoints, not just one, which is what caught this.
- **41 Stripe discount codes + TOPI1000 + OCTBKK50 mirrored**, source:
  `N8N/documentation/stripe-discount-codes-2026-11-03.md`. All 43 scoped to
  `prod_p4MkRss_YruVzCqlVb5z8` (this is the one gap Stripe's setup has that
  LF's doesn't: none of Stripe's 5 coupons has a product restriction, so a
  code meant for this ticket also works on $15,000 consulting calls there).
  TOPI1000 kept exactly as Stripe has it (no cap, no expiry) and OCTBKK50
  included despite being unused/possibly orphaned -- both Joshua's explicit
  call, not a default. `edits/setup_discounts.py`. Verified live: `TOPI`
  applied correctly, 15% off computed exactly.

### Quantity adjuster, 2026-11-03

Joshua: "is it possible quantity adjuster on the checkout". Checked before
building: checkout's own order summary (`Repeater` under `CheckoutSummary`)
is Container/Image/Text only, read-only, no +/- of its own. But the
quantity IN THE CART COOKIE genuinely drives the price, not just the "1"
badge -- hand-writing `quantity:2` into the cookie and reloading checkout
showed the subtotal exactly double. So the control has to live on the BUY
page, and it can.

Rebuilt buy-test's buybox as one raw `HtmlElement` (−/qty/+ buttons, a
`<span id="sof-qty">`, the buy link reading that span's value at click
time) rather than LF Button/Container/Text blocks, because the block
tree's own `id`s do not survive into the rendered DOM -- they get hashed
into generated classNames, confirmed by inspecting a live page's compiled
output, so `getElementById` would have had nothing to find. Real, plain
HTML renders exactly as written; it is the same mechanism the actual event
page's own buttons already use (`wire_one_click.py`). `edits/
add_quantity_adjuster.py`.

Verified live end to end: set quantity to 3 on buy-test, landed on
checkout showing 569,768.74 -- exactly 3x the single-ticket price -- and
the cart cookie read back `"quantity":3`. Only on buy-test so far;
buy-now/the live page do not have this yet.

### Quantity stepper moved ONTO the checkout page, and two real bugs it surfaced

Joshua, right after the above: "oh cant it be on the checkout itself?",
then after seeing it: "oh it needs to refresh" (confirming the reload
approach, not reporting a problem), then "okay but if it refresh make
sure what is typed on the fields are not lost on refresh".

Added a second stepper directly on the checkout page (`edits/
add_checkout_quantity.py`), inserted as a new sibling ABOVE
`CheckoutSummary` inside its own column (checked first: that column's
only existing child was CheckoutSummary itself, so nothing shared gets
displaced). Same mechanism as the buy-page version: edit the cart cookie,
`location.reload()`.

**Bug 1, shipped first, caught by actually looking at the page (not just
the saved tree data):** the onclick handlers were `function(){...}()` --
a bare `function` keyword at statement-start is a declaration, which
requires a name, so the whole handler failed to parse and its text LEAKED
onto the page as visible text next to the Quantity label. A
function-as-statement needs to be wrapped in parens to read as an
expression: `(function(){...})()`. Fixed, redeployed, confirmed working:
clicking + on the checkout page itself now reloads to the correct
quantity and the correctly multiplied total.

**Bug 2, the one the field-preservation request actually ran into:**
brought back Garlic's own field-autosave script
(`edits/add_field_autosave.py`, `settings.custom_html.footer`, scoped to
this step) -- save every named field to localStorage on input, restore on
load. Fields still did not survive the reload. Found by direct testing,
not by inspecting code: the restored value held for 4+ seconds then
vanished, which is the textbook sign of React's controlled-input tracker
not seeing the write (`el.value = x` bypasses the overridden prototype
setter React installs to tell real input from programmatic patches, so a
later unrelated re-render puts React's own -- still empty -- state back).
Fixed with the standard workaround: write through
`Object.getOwnPropertyDescriptor(HTMLInputElement.prototype,"value").set`
instead of the plain property.

That alone did not fully fix it either -- First/Last name and Address now
survive correctly, confirmed by direct testing, but Email specifically
kept resetting. Joshua: "is it possible to delay the email a little bit
more" -- tested directly rather than assumed: extended the restore retry
schedule from topping out at 6s to a continuously-observed 45s, still
never once took. That ruled delay out on its own: **the stored value was
already empty before the reload even happened.** Confirmed by stubbing
`location.reload` and inspecting `localStorage` right after the quantity
button's own click handler ran, before any navigation -- `"shipping.
email":""` was already there. Something clears the field's DOM value at
(or just before) the moment of the click itself, and the autosave
script's normal blur-triggered save dutifully persists that already-wrong
state. No amount of delayed RESTORE fixes a value that was never
correctly SAVED.

**Fix:** stopped relying on the blur handler for this one moment. The
quantity button's own onclick now snapshots every named field straight
into the same `lf_checkout_data` key, synchronously, in the same tick as
the click, before touching the cart cookie or calling
`location.reload()` -- `SNAPSHOT_JS` in `add_checkout_quantity.py`.
Verified live, twice, with different values each time (including the "−"
button, which clamps to a minimum of 1 rather than going to 0): Email,
First name, Last name all survive the reload correctly now.

### A second, separate buy step: n8n generates the Airwallex link, 2026-11-04

Joshua, after watching the above: "wait what if i have api access on
airwallex?", then "I plan to make a n8n endpoint we can call that will
generate the links itself so no api key is on LF, lets try to make new
steps for this specific scenario".

This changes the architecture, not just the plumbing: if Airwallex's own
hosted payment page collects contact and card details, NONE of the
Lightfunnels checkout machinery above is needed for this flow -- no cart
cookie, no cloned `checkout_page`, no field-autosave script, none of the
bugs those needed fixing. One page, one button, one outbound call to n8n,
a redirect to whatever URL comes back. Built as a genuinely SEPARATE step
(`buy-link`, not a change to `buy-now`/`buy-test`/`checkout`) so the
already-working cart-based flow stays intact and comparable.

    https://www.scalingorfailing.com/sof-checkout/buy-link

`edits/add_n8n_link_step.py`. Plain `article_page`, no `product_id`, no LF
cart involvement at all -- just an `HtmlElement` with a quantity stepper and
a button that POSTs `product=sof-general-admission&quantity=N`
(form-encoded, same CORS-simple-request reasoning as the contact form) to
`https://primary-production-f5243.up.railway.app/webhook/sof-payment-link`
and redirects to whatever `{"ok":true,"url":...}` comes back.

⚠️ **The n8n side does not exist yet.** The webhook path is a guess matched
to the contact-form's own naming convention, not confirmed. Full contract
-- request/response shape, why the price is computed server-side and never
trusted from the browser, validation posture, what is still undecided
(which Airwallex API, what a successful payment redirects to, duplicate-
click handling) -- written up in
`N8N/documentation/sof-payment-link-TODO.md` for whenever that workflow
gets built.

Verified the page itself end to end against the NOT-YET-REAL endpoint:
quantity adjusts correctly, clicking the button disables it, shows "One
moment...", the fetch fails exactly as expected against a URL nothing
answers at, and the page recovers cleanly -- inline error message, button
re-enabled, quantity untouched. That failure path is exactly what proves
the error handling works; it was not a bug to fix.

### Superseded within the hour: "okay we would just be using whop", 2026-11-04

All of the above -- the n8n contract, the Airwallex plan -- was live for
well under a day before Joshua settled on Whop instead, with a real
checkout link already in hand:
`https://whop.com/checkout/plan_9fd3QJCm3n9sM`.

Checked before wiring anything, in a real browser, not assumed from the
URL: a complete, working, ALREADY BRANDED checkout ("Scaling or Failing"
name and logo -- pulled from Whop's own account settings, nothing this
project set up) for "SoF Full Access Pass", $2,997, one-time payment,
Google Pay / Apple Pay / card. **No quantity control anywhere on it**,
confirmed by searching the rendered page's own text for the word, not
guessed from a screenshot. That one fact is what made the final shape
simple: a plan checkout with one fixed price needs none of the machinery
built up to this point.

**The real page's two buttons (`sof-v3` test step) now point straight at
that Whop link, plain `href`, no `onclick`, nothing else** --
`edits/wire_whop_link.py`. This is the SAME pattern the page's ticket
button always used for the original Stripe link (`EB_HREF`) before any of
today's work started; Whop replaces Stripe in that exact slot. Verified
live: clicked the real ticket button, landed on a genuine Whop checkout
session in one hop, no stopover page, no reload, no restored fields to
worry about, because there is no local form left to lose anything from.

**Everything else built today for this problem (buy-now, buy-test,
checkout, buy-link, the n8n contract doc) is now set aside, not deleted.**
None of it is wrong -- each piece solved the specific problem it was built
for, in order, as the real constraint kept changing (Stripe down -> needs
an LF-native checkout -> needs Joshua's own product -> needs no hop in
between -> needs survive-a-reload -> needs no API key on LF -> needs no
quantity because Whop doesn't have one). Kept as the record of that chain
and as a fallback if Whop ever stops being the answer, but the live
integration going forward is the one-line href above.

### Thank-you page, and discount codes moved to Whop's own, 2026-11-04

A real redirect target was needed for after a Whop payment --
`add_thank_you_step.py` built one at `/event/thank-you` on the main funnel
(not the sof-checkout test funnel, since this needs a permanent URL Whop's
own dashboard can point a post-payment redirect at). Copy settled through
a few rounds with Joshua: no mention that invites are sent by hand, no
em dash, "Back to the event page" linking to the bare domain, headline
exactly "Cu in Bangkok!" per his screenshot, Scalizard mascot in place of
a generic checkmark. **Pointing Whop's own redirect setting at this URL is
a Whop dashboard action, not something this repo can do -- no Whop API key
is configured anywhere here.**

Also: LF's 42 native discount codes (`setup_discounts.py`) are superseded
now that payment runs through Whop, which has its own native promo-code
field on checkout. Verified working with a real code (JEM, 15% off) against
the live Whop checkout -- exact math, clean rejection on an invalid code.
The LF codes and the `sof-checkout` test funnel are left in place, same
"set aside, not deleted" reasoning as above.

### New sponsors from the "Build 1" Figma frame: Whop and an unnamed monogram, 2026-11-04

Two more brands pasted into the same marquee + partner-plate pattern as
every earlier sponsor addition: **Whop** (apt, since it is also the new
payment processor) and a logo Figma itself only labels **"Sponsor S"** --
an ornate monogram with no wordmark next to it. Joshua confirmed there is
no name to give it ("there is nothing to give it is an image so just
extract it"), so it is traced from the vector geometry and labelled
"Sponsor S" throughout, the same thing the design file calls it.

Both are solid navy `#041C32` like every other mark here, so they got the
same one-colour `currentColor` symbol treatment. The marquee gained both
logos at the end of its loop (gap and per-breakpoint speed recomputed from
the new, longer sequence -- 14.7s mobile / 36.2s desktop, up from 11.5s /
28s). `edits/add_whop_sponsor_s.py` has the exact measurements and the
symbol-building code.

**First attempt was wrong and Joshua caught it from a screenshot:** both
new logos were appended to the existing flat `.sof-sponsors` row (the same
simplification already in place for Suits/Outcraft/Tazapay since
2026-11-02). But the "Build 1" frame actually draws FOUR separate tiers --
Diamond (BestFulfill), Platinum (Outcraft, solo), Gold (Suits/Whop/
"Sponsor S" together) and Silver (Tazapay, solo) -- each its own centred
row with a uniform gap between tiers. Flattening all five non-BestFulfill
sponsors into one row, which is what shipped first, was never right against
the actual design; it only wasn't visibly wrong until there were two tiers'
worth of brands crammed into what should have been three separate rows.

Fixed by rebuilding `sponsor_html()` into the four tiers Figma actually
draws: Outcraft and Tazapay got their own solo rows back (new `.sof-tier` /
`.sof-tplate` classes), and `.sof-sponsors` now holds only the three Gold
plates it was always meant to. Re-measuring Suits' logo in its real
Gold-tier box (400x139 desktop, not the old shared row's smaller box) grew
it from 233x64 to 304x83 -- correctly bigger, since the Gold-tier plate
itself is bigger than the flat row's item ever was.

Verified on a disposable test step (`sof-sponsor-test`) on both desktop and
mobile before promoting, both before and after the tier fix. Live on
`scaling-failing` as of this entry.

### ⚠️ Caught by the verifier: rebuilding this file had silently reverted the live ticket link to Stripe, 2026-11-04

`build_sof_event.py`'s own `EB_HREF` constant was still the dead Stripe
link. The Whop switch earlier in the day was applied as a RUNTIME PATCH on
the deployed page body (`edits/wire_whop_link_live.py`), never as a change
to this constant -- the comment above it even said "when the URL lands,
change this one constant," and that step was skipped. Rebuilding the page
for the sponsor-tier fix above regenerated the body from source and
silently put the live ticket button back on Stripe, with no error and no
visual difference to catch by eye.

`pagescore/verify_pages.py` caught it as a link DRIFT the moment it ran
(`whop.com... GONE`, `buy.stripe.com... NEW`) -- this is exactly the kind
of mistake that checker exists to catch, and it worked. Fixed two things
together: `EB_HREF` now IS the Whop URL (`STRIPE_EB_HREF` kept alongside
it for the revert path), and the Meta AddToCart/InitiateCheckout tracking
script -- which matched `buy.stripe.com` only -- now matches `whop.com`
too. That tracking gap is older than today's mistake: it had been silently
not firing for every real ticket click since the original Whop switch, and
was only found while fixing the href.

Re-verified live afterward: both the ticket button (2 occurrences on
`scaling-failing`) and the contact page's promo bar (1 occurrence) serve
the Whop link again, zero Stripe hrefs anywhere.

**Lesson for next time:** any live state applied as a runtime patch
(`edit_step_bodies` string-replace) rather than a builder-source change is
one unrelated rebuild away from silently reverting. When a patch like this
is confirmed as the real live state, fold it into the builder's own
constants in the same sitting, not "whenever".

### 2026-11-06 — Slash sponsor logo
Exported selected V2 Figma logo 1067:1254 with Figwright save_screenshots (3x PNG). Replaced shared old S symbol in the marquee and sponsor cross, updated accessible name and responsive dimensions in per-step header CSS. Tested on sof-sponsor-test, applied only to scaling-failing, and verified saved body/settings. Builder source updated to preserve the replacement on rebuild. Backup: steps/pre-slash-2026-11-06.json. Verification screenshots: assets/slash-2026-11-06/.

### Split-pay link added, and Whop DOES read a promo code off the URL -- `promoCode`, not documented, 2026-11-11

Added a second Whop plan (`plan_fkxLUG1tlaOdO`, 2 payments of $1,498.50) as a
plain text link under the main button (`.sof-tsplit`), same pattern as the
existing `.sof-tbtn`. Mocked three placement options first, Joshua picked
the plain-text one. Live on `scaling-failing` only (`contact` has no ticket
card). Builder source (`build_sof_event.py`) updated to match.

**Corrects the 2026-11-04 entry above** ("Whop has its own native promo-code
field" -- true, but incomplete): Whop's hosted checkout *also* reads a code
straight off its own URL and auto-applies it before the buyer sees the
price, with no login and no iframe embed needed. We spent real time
confirming this does NOT exist (Whop's docs never document it, and five
guessed param names -- `promo`, `code`, `coupon`, `d`,
`prefilled_promo_code`, Stripe's own name -- all failed empirically on the
live checkout). The real name, found by Joshua googling rather than reading
docs: **`promoCode`**, exact case.
`whop.com/checkout/plan_9fd3QJCm3n9sM?promoCode=JEM` discounts to $2,547.45
on a plain redirect, no embed.

**It must be the FIRST query param, or Whop ignores it.** Confirmed by hand:
a link that already carries `?session=...` with `&promoCode=...` appended
after it does not discount. Most likely explanation: Whop only reads the
code when CREATING a session; a URL that already has `session=` just
resumes that existing session and whatever comes after is never looked at.

Retargeted the existing `?ref=` affiliate script
(`edits/wire_affiliate_ref.py`, 2026-10-30) rather than writing a new one --
it already did exactly this mechanism for Stripe (`?ref=` on our own URL ->
rewrite every button whose href starts with the payment host) and had been
a dead no-op since the Whop migration, still matching `buy.stripe.com` and
`prefilled_promo_code`. Two follow-up edits, in order:
1. `edits/retarget_affiliate_ref_to_whop-2026-11-11.py` -- `PREFIX` ->
   `https://whop.com/checkout/`, `FIELD` -> `promoCode`.
2. `edits/force_promocode_first_param-2026-11-11.py` -- hardened `apply()`
   to rebuild the query string with `FIELD` forced first always, rather
   than `searchParams.set()`, which only lands it first when the href has
   no other params yet. Our own hrefs are clean today, so this was pre-empting
   a silent, revenue-losing regression the moment any other param ever
   joins one of these links, not fixing a live bug.

Both live in the funnel's `header_scripts` (not a per-step field -- this is
shared across every step). Verified: `?ref=JEM` on the live page rewrites
all three Whop links (promo bar, full price, split-pay) to
`?promoCode=JEM` with nothing after it, and the Whop checkout shows the
15%-off price on each. Backups: `header_scripts.pre-whop-retarget-2026-11-11.html`,
`header_scripts.pre-promocode-first-2026-11-11.html`.

A sof-v3 experiment tried the OTHER documented auto-apply path first --
Whop's embedded checkout (Elements SDK), which has a real `promoCode`
option but only as a JS argument to `checkout.create()`, mountable only as
an inline iframe (modal), never as a redirect, and with no `.url`/`.redirect()`
escape hatch. Built and proved working (our own button triggers it, modal
opens, discount applies, close/reopen works via `destroy()` then a fresh
`create()`), then reverted once the plain `promoCode` URL param made the
whole embed unnecessary. `edits/try_embedded_checkout-2026-11-11.py` is kept
as a reference if a true inline checkout is ever wanted on this page.
