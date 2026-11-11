#!/usr/bin/env python3
"""
"Scaling or Failing" — Bangkok, December 7–8 2026 — event landing page.

Target : funnel fun_RoOL_WXDCAxK4hEk0v5xX ("Scaling or Failing - Event"), step
         slug `event` (type article_page, the funnel's ENTRY step).
Live   : https://www.scalingorfailing.com/event/scaling-failing
Contact: https://www.scalingorfailing.com/event/contact  (SOF_PAGE=contact)

The funnel moved onto its own domain on 2026-10-14. It still answers on
www.techunboxed.co/event/* as well, because that domain is also attached
to the account, so the same page is currently reachable at two hostnames.
Design : Figma file "99 Commerce", page "Advertorials/Blogs".
           Frame 1  node 870:6    desktop, 1920 x 9720
           Frame 2  node 870:433  mobile,  390  x 7567
         Read with figwright `get_design_context` at detail:"full", one section
         at a time, plus `scan_text_nodes` for the verbatim copy. Never a
         screenshot, never an estimate. Raw dump: pagescore/runs/sof-2026-10-06/
         design.json (both frames, every TEXT node with its resolved type).

================================================================================
DECISION 1 — this page is authored as HTML blocks, not as native LF blocks.
================================================================================
Every other builder in this repo (build_ranked_comparison.py and friends) is an
article: a single text column where LF's Title/Text/Image blocks map one-to-one
onto the design. This design is a poster. In ten sections it uses rotated
hand-drawn display lockups with outside strokes, three stacked TEXT_PATH layers
on a curve, a 60px layer blur behind the host names, four multi-stop gradient
washes, tiled paper textures, a notched chip with a triangular corner tab, and
"3D lip" buttons built from two offset rounded rectangles.

None of that is expressible in LF's style-prop vocabulary, and the repo's own
hard-won list of props that have 503'd this SSR (maxWidth:none, alignItems:
baseline, overflow, boxShadow, className on a p, quoted font names) is exactly
the list you would have to go shopping in to try. The established escape hatch
here is an HtmlElement carrying real markup with inline CSS — already used for
the half-star gradient, the cost-table scroll wrapper and the video poster in
build_ranked_comparison.py. This file takes that one step further: one Section
per design section, each holding one HtmlElement, with the whole stylesheet in
the step's own settings.custom_html.header.

What that buys, beyond fidelity: real `@media` queries. Mobile here is NOT
desktop reflowed — see DECISION 2 — and LF's `media:767` prop override cannot
express a 5-column grid becoming a 2-column one, a 5-item nav becoming a
hamburger, or two different strings of body copy.

What it costs: the page is not editable block-by-block in the LF editor. For a
one-off event page whose source of truth is this script, that is the right
trade. Copy edits go here and get redeployed, not hand-typed into the canvas.

================================================================================
DECISION 2 — mobile is a separate DOM where the design is a separate design.
================================================================================
Per-section verdict, measured off frame 870:433 rather than assumed:
  Header       separate DOM  — 5 nav items become a hamburger + GET TICKET
  Hero         separate DOM  — wrapper dropped, wash/shade z-order flips, the
                               blurred "Names shade" is dropped, Powered-by is
                               regrouped, Hosts move from the right to the foot
  Stats        media override
  Speakers     one DOM, CSS grid — 5x2 becomes 2x5; the Figma "grid line"
                               rectangles are reproduced as grid gaps over a
                               tinted container, which is what they draw
  Formats      one DOM + swapped title art — the single-line title lockup
                               becomes two stacked lockups on mobile
  You Decide   separate DOM  — the headline artwork has NO mobile counterpart,
                               and the intro COPY DIFFERS (see OPEN QUESTION 1)
  Topics       one DOM, CSS grid — 4-up becomes 2-up
  Tickets      one DOM + swapped title art — side-by-side becomes stacked, and
                               the VIP sticker is desktop-only
  Sponsor      media override
  Footer       one DOM — the nav row becomes a column

================================================================================
DECISION 3 — scale. Build 1:1 at the design's own width; fix the LAYOUT below it.
================================================================================
The desktop frame is 1920 wide with 120px gutters, so every measured value is
reproduced verbatim and the page is pixel-exact at 1920. Below that the gutters
stay at 120 and the content column shrinks (max-width:1680, width:100%), display
artwork is width:100%/height:auto so it scales, and card grids keep the design's
gaps while the columns narrow. Typography is never touched — the rule is fix the
container, not the type. The one place the design's own arithmetic does not
close is the Formats section: three 552px cards with 24px gaps need 1704px, so
its right gutter is 96, not 120. Reproduced as drawn.

AMENDED after the 2026-10-06 QA run (pagescore/runs/sof-2026-10-06-qa). The
above held down to about 1200 and no further. A single breakpoint at 768 handed
the 1920 frame's type -- 88px prices, 54px button labels, 42.6px nav cells --
to a 768px viewport, and the page was only correct at ~1800: the Early Bird
button label overran its box by 25px at 1600, 65px at 1440, 233px at 768; the
badge row needed 665px inside a 472px card; the footer row was 444px over. The
breakpoint ladder is now:

    <= 346      the hero CTA label ramps down from 27px      <-- 2026-10-07
    <= 374      mobile frame, three containers tightened (gutter/hero/card pad)
                plus the host strip's bleed brought to the same 12px gutter
    375 - 767   mobile frame, 870:433, verbatim
    <= 767      the "You Decide" plate serves the MOBILE crop  <-- 2026-10-07
    <= 1023     the "You Decide" plate serves the MOBILE crop
    768 - 1023  mobile frame centred in a 520px column
    >= 1024     desktop frame, 918:77, every measured value verbatim, scaled
                by zoom = (available width / 1920) up to 1919  <-- 2026-10-14
    >= 1920     that same frame at 1:1, which is what design_diff measures
    >= 1420     the footer's single row (needs ~1300px of content)
    >= 1650     the chip label is the design's own 58.6px
    >= 1760     the ticket cards side by side (needs 1460px of content column)
    >= 1921     the three bleed sections' CONTENT caps at the 1920 frame,
                bands still edge to edge                       <-- 2026-10-08

The rule is unchanged and is the reason none of this touched a font-size: fix
the container, never the type. At 1920 the rendered page is pixel-identical to
before the amendment apart from one bold bullet (870:407, which the DESKTOP
frame always had bold -- the mobile frame's 870:816 does not, so the weight is
set in the >=1200 block only).

AMENDED AGAIN 2026-10-07 (pagescore/runs/sof-fidelity-2026-10-07 and
sof-sweep-2026-10-07). Two of the three rows marked above are the first places
on this page where the container had nothing left to give and the TYPE had to
move: the topic chip panel is a fixed quarter of the content column and the
hero CTA at 320 is already full-bleed. Both are gated so they cannot reach
either design-diff viewport -- 1920 and 390 are byte-identical, verified as a
full-page pixel diff with an empty bbox at 1920 and a diff confined to the
800px "You Decide" plate at 390.

================================================================================
DECISION 4 — "Scaling Lockup" is a bespoke font we do not have.
================================================================================
13 nodes use a custom family called "Scaling Lockup" that is installed in the
designer's Figma and is not a webfont we can ship.
  * Where it is ARTWORK (the hero SCALING/OR/FAILING lockup, desktop and
    mobile), it is exported from the node at 3x and placed as an image, so it is
    pixel-identical. The h1 carries the real words as rendered-but-clipped text
    at the node's own font-size and colour, so the headline is real text for
    search engines and screen readers and the artwork is what you see. This is
    standard image replacement, not hidden text.
  * Where it is INTERACTIVE TEXT (the nav labels: ABOUT / SPEAKERS / TOPICS /
    GET TICKET / CONTACT at 42.6px desktop, MENU / GET TICKET at 18px mobile) it
    MUST stay real text — an image nav is a dead link to a crawler and to
    assistive tech. Those are set in Barlow Condensed Black, which is the
    design's own display sans (it sets the ticket names, the chip labels, the
    section sublines and POWERED BY), at the node's exact size, colour and
    letter-spacing. The letterforms are a substitution. See UNREAD VALUES.

================================================================================
DECISION 5 — links.
================================================================================
Every nav item is an in-page anchor, per the brief:
    ABOUT -> #about (the "You Decide" section, which is what the page says
             Scaling or Failing is), SPEAKERS -> #speakers, TOPICS -> #topics,
             GET TICKET -> #tickets, CONTACT -> #contact (the footer, the only
             place on the page carrying brand/partner contact detail).
Ticket CTAs are NOT wired to a checkout: Whova has not issued the registration
URL yet. The promo-strip CTA, the hero CTA and BOTH ticket card buttons all
pointed at #tickets until 2026-10-14, when the Stripe payment links landed.
They are EB_HREF and VIP_HREF. The nav's GET TICKET scrolls, and since
2026-10-15 so does the HERO button: Topi asked for it, and it stops a cold
visitor landing on a $1,997 checkout before seeing what the ticket holds.
The header promo bar still goes straight to Early Bird.
No href="#" anywhere on the page.

================================================================================
DECISION 6 — the mobile hamburger opens something the design does not draw.
================================================================================
The mobile nav is a hamburger + "MENU" label with no menu panel anywhere in the
frame, and ABOUT / SPEAKERS / TOPICS / CONTACT exist nowhere else in the mobile
header. A control that opens nothing is a defect, so MENU toggles a panel
holding those four links plus GET TICKET, styled in the design's own language
(navy #0B1A32 plate, cream Fira Sans Condensed Bold labels at the footer nav's
size and letter-spacing, cream hairlines). It is a CSS :checked toggle — no
JavaScript, so it works server-rendered and with JS off. Flagged as drawn-by-me.

================================================================================
NOT BUILT, deliberately
================================================================================
  * The ten named speaker captions (Neil Patel, Ryan Holiday, Ryan Deiss, Oli
    Gardner, Mark Joyner, Robin Duan, Eric Siu and others) sit LOOSE ON THE
    CANVAS OUTSIDE frame 870:6. They are not placed in the design and are not
    pulled in — Joshua's explicit decision. The ten speaker cards are built
    exactly as the frame draws them: three named (Gonzalo, Ronak Shah, Alex
    Fedotoff) and seven "TBA / Announced soon".
  * Node 870:432 "image 1", a loose 1254x1254 rectangle parked below the footer
    inside frame 870:6. It is the source asset for the VIP card's sticker
    (870:415, same 1254x1254 aspect), parked on the canvas, not a page element.
  * 870:264 and 870:690 ("Headline · ARE YOU SCALING OR FAILING?") and 870:301
    ("Title (vector backup)") are visible:false in Figma. Hidden means hidden.

================================================================================
UNREAD VALUES — what the nodes do not say, and what was used instead
================================================================================
  1. "Scaling Lockup" letterforms for the nav (DECISION 4). Substituted with
     Barlow Condensed Black at the node's exact size/colour/letter-spacing.
  2. The topic chip's corner radii. The chip is a VECTOR path, so Figma exposes
     no cornerRadius. Measured off a 2x render of node 870:306: outer 16px,
     inner panel 6px (desktop); scaled to 7px/3px on mobile, where the chip is
     167x57 against the desktop 408x134.
  3. The chip tab is a right-triangle filling the panel's top-left corner. Its
     silhouette is read from the same render; its box (59.19x51.22 desktop,
     24.25x21.92 mobile) and fill are measured from the node.
  4. The Topics heading is three stacked TEXT_PATH layers and TEXT_PATH carries
     no `characters` in the Figma API. The copy is recoverable only from the
     layer name, "Let's talk topics". Placed as artwork; the h2 and the alt text
     use that wording.
  5. Nothing in frame 870:7 marks the header as sticky, so it is built as drawn:
     a static band at the top of the page. See OPEN QUESTION 3.

================================================================================
OPEN QUESTIONS for a human — do not guess these
================================================================================
  1. The "You Decide" intro copy DIFFERS between the two frames. Desktop
     (870:288) says "...our underground community since 2024." Mobile (870:714)
     says "...our underground community for over two years." Both are built, each
     at its own breakpoint, because inventing a reconciliation is not this
     script's call. design_diff WILL report one of them missing at whichever
     viewport it runs — that finding is real and it is this discrepancy.
  2. RESOLVED 2026-10-14 by the V4 frame. The desktop "You Decide" headline
     artwork read "ARE YOU / SCALLING / OR FAILING?" — two Ls — in the
     TEXT_PATH node and its layer name, through four frames. It was reproduced
     exactly as drawn, with the h2 and alt text carrying the correct spelling
     so the typo never reached search engines. The designer fixed the vector
     (918:477 is now spelled SCALING) and the artwork was re-exported.
  3. The date separator is inconsistent on the same page: the hero date (870:26,
     870:450) uses "•" U+2022, the tickets date (870:374, 870:783) and the footer
     (870:425) use "·" U+00B7. Reproduced exactly per node.
  4. The header is labelled "sticky early-bird bar + nav" in the brief but
     nothing in the node says sticky, and the desktop header is 232px tall — a
     quarter of a 1080 viewport. Built static.
  5. RESOLVED 2026-10-10 -- it was a missing lockup, confirmed by Joshua.
     The mobile frame 870:686 runs "YOU DECIDE:" to y=62 and then nothing
     until the body at y=264: a 202px empty band where the headline should be.
     This build scales the headline artwork into that space instead, so the
     gap is 24px rather than 202px.
     The live page is therefore DELIBERATELY not 1:1 with the mobile frame
     here, and design_diff comparing against 870:433 will keep saying so.
     That finding is expected. Do not "fix" it by removing the headline --
     the frame is the thing that is wrong, and hiding the artwork leaves a
     ~400px empty beige band, which is how this was found the first time.
  6. The legal popup (section 9b) needed FOUR facts only the organiser has,
     and they render in gold with a dashed underline so they cannot ship
     unnoticed. The contact email was supplied on 2026-10-14 and is now filled
     in from CONTACT_EMAIL, leaving THREE: the organiser's legal entity, its
     registered address, and the governing law. Count them on the live page
     with `document.querySelectorAll('.sof-legal-tbc').length` — it should
     reach 0 before tickets go on sale. Five nodes today, because the entity
     and address each appear in both documents and the law appears once.
     Two further things a human has to decide rather than inherit:
       - REFUNDS. The terms say non-refundable with a free name transfer up to
         14 days out. That is the standard position for a paid event, not an
         instruction from anyone, and it is a commercial commitment.
       - COOKIE CONSENT. The page sets an `lfbid` identifier lasting about a
         year, plus session and cart cookies, and calls Google Fonts, unpkg and
         Sentry. There is no cookie banner. The privacy policy now DESCRIBES
         all of it accurately, but describing is not consent, and the audience
         for a Bangkok event includes the EU and UK.
  7. There is NO MOBILE FRAME for the 2026-10-09 rework. 904:108 is a 1920
     desktop and the only other frames are the ORIGINAL pair. So the ticker,
     the Mission Map, Who it's for and the FAQ have mobile layouts I designed,
     not ones anyone drew: the day cards and the two Who-it's-for cards stack,
     the FAQ runs full width, and the ticker keeps scrolling at a smaller size
     and a shorter duration. Confirmed with Joshua on 2026-10-09 as the way to
     proceed, but a 390 frame would replace every one of those decisions.
  8. The speaker name 909:2919 reads "Gonzalo FernAndez Martin" -- a capital A
     mid-word, and no accents on either word. Reproduced verbatim like all copy
     here. If it should be "Fernandez" or "Fernandez Martin" with accents, the
     node needs fixing in Figma; this script will not second-guess a name.
  9. The ticket prices are set in PRICEDOWN in the new frame, the GTA face, in
     #9ed88e. The colour and the figures are reproduced, but Pricedown is not a
     webfont and we do not have the file, so they render in the display face.
     Either licence and self-host it, or export the two prices as artwork.
     Until then the page is right about everything except the typeface.

================================================================================
WHERE THIS SHIPPED
================================================================================
STEP_SLUG defaults to `scaling-failing` (renamed from `event` on 2026-10-07, since
/event/event duplicated a segment). deploy_guard refuses to
write it because it is a LIVE page in a PUBLISHED funnel, and authorising a
redeploy is a human's call that an agent may not make for itself. So this run
shipped to a NEW sibling slug instead -- reachable, QA-able, and nothing
existing was touched:

    SOF_SLUG=event-v2 python3 pagescore/build_sof_event.py

To put it on the intended `event` URL, a human runs:

    LF_ALLOW_REDEPLOY=event python3 pagescore/build_sof_event.py

Creating a sibling deliberately does NOT touch `starting_step_id`: repointing a
published funnel's entry changes what /scaling-or-failing/ serves to real
traffic, which is also not this script's call.
"""
import json
import os
import sys
import uuid

sys.path.insert(0, '.')
import lf_api                                                      # noqa: E402
from deploy_guard import guard                                     # noqa: E402

tok = open('.session_token').read().strip()
ACCT = open('.lf_account').read().strip()
HH = lf_api.session_headers(ACCT)


def sgql(q, v=None):
    return lf_api.gql(tok, q, v, extra_headers=HH)


def nid():
    return str(uuid.uuid4())


FUNNEL = os.environ.get("SOF_FUNNEL", "fun_RoOL_WXDCAxK4hEk0v5xX")
STEP_SLUG = os.environ.get("SOF_SLUG", "scaling-failing")
# SOF_PAGE=contact builds the contact page into the same funnel instead of the
# event page. Declared here rather than beside the body assembly because
# nav_href() reads it while rendering the header, which happens first.
PAGE = os.environ.get("SOF_PAGE", "event")
# 2026-10-09: a THIRD frame landed, 904:108, a reworked 1920 desktop. The dump
# keeps the two original frames and adds it, so every node id both old and new
# sections cite still resolves and no copy has to be retyped. 209 text nodes in
# the new frame, zero id collisions with the old two (checked when it was
# written). There is NO new mobile frame -- see OPEN QUESTION 7.
RUN = "sof-2026-10-21-v7"

IMG = json.load(open("pagescore/.cache/sof_img_map.json"))
DESIGN = json.load(open("pagescore/runs/%s/design.json" % RUN, encoding="utf-8"))

# Until Whova approves the registration page there is no checkout URL. Every
# ticket CTA on the page points at the tickets section instead of a dead link.
# When the URL lands, change this one constant.
# Which button carries which link matters more than anything else on this
# page: a VIP button on the Early Bird link undercharges by $4,500 and
# nothing on the page would look wrong.
#
#   EB_HREF   the ticket checkout
#   VIP_HREF  the $6,497 VIP (unused, see below)
#
# CTA_HREF stays as the in-page anchor and is used only where the button is
# not a purchase: the nav's "GET TICKET", which should show someone both
# tiers rather than choosing one for them.
#
# ⚠️ 2026-11-04: EB_HREF is Whop, not Stripe. Stripe was held, so Joshua
# switched the live buttons to a Whop checkout
# (`edits/wire_whop_link_live.py`) as a RUNTIME PATCH on the deployed page
# body -- this constant was never updated to match. Rebuilding from this
# file (as a sponsor-logo change later the same day did, with no other
# reason to touch the ticket link) silently reverted the live button back
# to the dead Stripe link. Fixed by making Whop the actual source of truth
# here, so the next unrelated rebuild cannot regress it again.
# `edits/revert_to_stripe_live.py` is the ready, tested path back to Stripe
# if Whop is ever dropped -- update EB_HREF here too when that happens.
CTA_HREF = "#tickets"
EB_HREF = "https://whop.com/checkout/plan_9fd3QJCm3n9sM"
STRIPE_EB_HREF = "https://buy.stripe.com/3cIfZh0RM201aiyg01dby04"
# Whop's own split-pay plan for the same $2997 pass: 2 payments of $1,498.50.
# Joshua pasted this with a `?session=chs_...` suffix, which is a one-time
# checkout session from whenever that screenshot was taken, not a durable
# public link -- stripped here so every visitor gets their own session.
# Promo codes are a Whop dashboard setting per plan, not something this repo
# can set: confirm the existing code's eligible-plans list also covers this
# plan id (plan_fkxLUG1tlaOdO), or "all plans" is already chosen.
SPLIT_HREF = "https://whop.com/checkout/plan_fkxLUG1tlaOdO/"
# UNUSED since 2026-10-21. The VIP ticket left the tickets section and Day 3
# became invite only, so nothing on the page points here any more. Kept
# because the payment link is still live at Stripe and VIP may come back.
VIP_HREF = "https://buy.stripe.com/3cIcN55822013UaeVXdby05"

# The public contact address, supplied 2026-10-14. Joshua gave it first as
# "scailing" and then corrected the spelling to "scaling", which is also the
# domain the funnel now serves from -- so the mailbox and the site match.
#
# It is NOT in the Figma frames. It is on the contact page because that page's
# form has nowhere to post yet, so without a visible address it offers a visitor
# no way to reach anyone, and in the two legal documents because a privacy
# policy has to name a way to exercise a data right.
#
# It is deliberately NOT in the footer. It was for one deploy on 2026-10-14 and
# Joshua took it out: the frame draws no address there, and the footer is the
# one block that appears on every page, so an addition to it is a change to the
# whole site rather than to one page.
#
# Change it here and the contact page and both documents follow.
CONTACT_EMAIL = "hello@scalingorfailing.com"


def u(key):
    """CDN url for an uploaded asset."""
    return IMG[key]["src"]


# --------------------------------------------------------------------------
# Copy comes out of the Figma dump by node id, never retyped. A typo'd en-dash
# or a straightened curly quote is a design_diff RETYPED finding, and the only
# way to be sure is to not type it at all.
# --------------------------------------------------------------------------
_TEXT = {}
# A node whose line mixes weights or colours reports fontName:"mixed" and
# carries the real runs in `segments`. Keep them: reading only `characters`
# is what flattened the bold lead-in on the You Decide intro.
_SEGS = {}
for _frame in DESIGN["frames"].values():
    for _n in _frame:
        _TEXT[_n["id"]] = _n["characters"]
        if _n.get("segments"):
            _SEGS[_n["id"]] = _n["segments"]


def esc(s):
    return (s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
             .replace('"', "&quot;"))


def T(node_id):
    """Verbatim copy from the Figma node, HTML-escaped."""
    return esc(_TEXT[node_id])


_WEIGHT_NAME = {"Thin": 100, "ExtraLight": 200, "Light": 300,
                "Regular": 400, "Medium": 500, "SemiBold": 600,
                "Bold": 700, "ExtraBold": 800, "Black": 900}


def _seg_weight(seg):
    fn = seg.get("fontName") or {}
    vs = fn.get("variationSettings") or {}
    if "wght" in vs:
        return int(vs["wght"])
    return _WEIGHT_NAME.get(fn.get("style", "Regular"), 400)


def Tseg(node_id):
    """Copy with the node's own BOLDER runs wrapped in <strong>.

    Figma hands a mixed-weight line back as `segments`; the flat `characters`
    string has no idea which words were heavier. Anything above the line's
    lightest weight becomes <strong>, which is the semantic element as well as
    the visual one, so the emphasis survives for a screen reader too.

    Falls back to Tbr when the node has one weight, or when COPY_EDITS has
    replaced the text -- the stored runs describe the OLD string and slicing
    the new one by them would cut it in the wrong place.
    """
    segs = _SEGS.get(node_id)
    if not segs or _TEXT[node_id] != "".join(sg["characters"] for sg in segs):
        return Tbr(node_id)
    weights = [_seg_weight(sg) for sg in segs]
    if len(set(weights)) < 2:
        return Tbr(node_id)
    base = min(weights)
    out = []
    for sg, w in zip(segs, weights):
        chunk = esc(sg["characters"])
        out.append("<strong>%s</strong>" % chunk if w > base else chunk)
    return "".join(out).replace("\u2028", "<br>").replace("\n", "<br>")


def Tbr(node_id):
    """Verbatim copy with the node's own hard line breaks (\\n and U+2028)
    turned into <br>. Whitespace-collapsing in HTML would otherwise silently
    reflow a line the designer broke on purpose."""
    s = esc(_TEXT[node_id])
    return s.replace(" ", "<br>").replace("\n", "<br>")


# ==========================================================================
# FONTS — the design uses ten families. Nine come from Google Fonts as single
# weight-isolated woff2 files (verified live: each url below is the latin
# subset Google serves for that exact weight, so a "Black" really is a Black
# and not a proxy serving one variable file for every weight — the failure
# mode build_ranked_comparison.py documents for LF's own /cf-fonts proxy).
# Inter keeps the proven LF-hosted path plus the metric-matched InterFallback
# from references/performance.md, which is the zero-CLS recipe.
# ==========================================================================
# NOTE: each url below is the **latin** subset. Google's css2 response lists
# several subsets per family and the latin one is NOT first -- taking the first
# url you see hands you vietnamese or cyrillic, which loads fine, reports
# `status: "loaded"`, passes `document.fonts.check()`, and then silently renders
# nothing because it has no Latin glyphs. That cost a round of this build: the
# page looked like it was in Barlow Condensed and was actually in Times.
GF = {
    "League Spartan|700": "https://fonts.gstatic.com/s/leaguespartan/v15/kJEnBuEW6A0lliaV_m88ja5Twtx8BWhtkDVmjZvMGYPZA81dNA6MzbxG.woff2",
    "Fira Sans Condensed|700": "https://fonts.gstatic.com/s/firasanscondensed/v11/wEOsEADFm8hSaQTFG18FErVhsC9x-tarWU3IuMR0cjRYhY8.woff2",
    "Fira Sans Extra Condensed|700": "https://fonts.gstatic.com/s/firasansextracondensed/v11/NaPPcYDaAO5dirw6IaFn7lPJFqXmS-M9Atn3wgda3USLr3i-oWR9e2U.woff2",
    "Barlow Condensed|900": "https://fonts.gstatic.com/s/barlowcondensed/v13/HTxwL3I-JCGChYJ8VI-L6OO_au7B45L0z3bWuYMBYro.woff2",
    # Added 2026-10-25 for the countdown bar, which sets its label and
    # digits in Barlow Condensed BOLD and its small caps in Barlow Bold.
    # Only the Black cut above existed, and 900 where the design says 700
    # is a visible difference at 42px. Latin subsets, from the Google
    # Fonts API, both verified 200.
    "Barlow Condensed|700": "https://fonts.gstatic.com/s/barlowcondensed/v13/HTxwL3I-JCGChYJ8VI-L6OO_au7B46r2z3bWuQ.woff2",
    "Barlow|700": "https://fonts.gstatic.com/s/barlow/v13/7cHqv4kjgoGqM7E3t-4s51os.woff2",
    "Fira Mono|700": "https://fonts.gstatic.com/s/firamono/v16/N0bS2SlFPv1weGeLZDtondvHnvfUS5NBBA.woff2",
    "Archivo Black|400": "https://fonts.gstatic.com/s/archivoblack/v23/HTxqL289NzCGg4MzN6KJ7eW6CYyF_jzx13E.woff2",
    "Arimo|400": "https://fonts.gstatic.com/s/arimo/v36/P5sfzZCDf9_T_3cV7NCUECyoxNk37cxcABrBdwcoaaQw.woff2",
    "Passion One|900": "https://fonts.gstatic.com/s/passionone/v20/Pby6FmL8HhTPqbjUzux3JEMS0U7vyJc-u28z.woff2",
}
_GF_FACES = "".join(
    "@font-face{font-family:'%s';font-style:normal;font-weight:%s;font-display:swap;"
    "src:url(%s) format('woff2')}" % (k.split("|")[0], k.split("|")[1], v)
    for k, v in GF.items())

_INTER_WEIGHTS = (400, 500, 600, 700, 800, 900)
_INTER_FACE = "".join(
    "@font-face{font-family:Inter;font-style:normal;font-weight:%d;font-display:swap;"
    "src:url(/cf-fonts/s/inter/5.2.8/latin/%d/normal.woff2) format('woff2')}" % (w, w)
    for w in _INTER_WEIGHTS)
# Metric-matched local fallback. Without it Inter's swap reflows the body copy
# and CLS lands near 0.15, which fails Agentic Browsing outright.
_INTER_FALLBACK = (
    "@font-face{font-family:InterFallback;src:local('Arial'),local('Liberation Sans'),"
    "local('Helvetica Neue');ascent-override:90.44%;descent-override:22.52%;"
    "line-gap-override:0%;size-adjust:107.12%}")

_PRELOAD = "".join(
    '<link rel="preload" as="font" type="font/woff2" crossorigin href="%s">\n' % GF[k]
    for k in ("Barlow Condensed|900", "Fira Sans Condensed|700")) + "".join(
    '<link rel="preload" as="font" type="font/woff2" crossorigin '
    'href="/cf-fonts/s/inter/5.2.8/latin/%d/normal.woff2">\n' % w for w in (500, 700))

# LCP: the hero plate is the largest paint on both breakpoints.
_HERO_PRELOAD = (
    '<link rel="preload" as="image" fetchpriority="high" href="%s" '
    'media="(min-width: 768px)">\n'
    '<link rel="preload" as="image" fetchpriority="high" href="%s" '
    'media="(max-width: 767px)">\n' % (u("hero_desktop"), u("hero_mobile")))

SANS = "Inter, InterFallback, Arial, sans-serif"
DISPLAY = "Barlow Condensed, Arial Narrow, sans-serif"
COND = "Fira Sans Condensed, Arial Narrow, sans-serif"
XCOND = "Fira Sans Extra Condensed, Arial Narrow, sans-serif"
MONO = "Fira Mono, ui-monospace, monospace"
# Plain Barlow, not the condensed cut: the countdown small caps only.
BARLOW = "Barlow, Arial, sans-serif"
BODY_SANS = "Arimo, Arial, sans-serif"

# ==========================================================================
# STYLESHEET. Written mobile-first: the base rules are frame 870:433 at 390,
# the `@media (min-width:768px)` block is frame 870:6 at 1920. Image urls are
# injected by token replacement so the CSS stays readable and brace-safe.
# ==========================================================================
CSS = r"""
.sof,.sof *{box-sizing:border-box}
.sof{font-family:__SANS__;color:#041C32;-webkit-font-smoothing:antialiased;
     text-rendering:optimizeLegibility}
.sof :where(img){display:block;max-width:100%;height:auto}
/* :where() keeps this at zero specificity, so a later single-class rule such as
   .sof-navcell still wins its own colour. `.sof a` would outrank it (0,1,1 vs
   0,1,0) and silently paint every nav label navy-on-navy. */
.sof :where(a){color:inherit;text-decoration:none}
.sof :where(p){margin:0}
.sof :where(h1,h2){margin:0;font-weight:inherit;font-size:inherit;line-height:inherit}
/* Rendered, but clipped to nothing: image-replaced display type keeps its real
   words, at the node's real size and colour, for crawlers and screen readers. */
.sof-vh{position:absolute!important;width:1px;height:1px;margin:-1px;padding:0;
        border:0;clip-path:inset(50%);white-space:nowrap;overflow-wrap:anywhere}
/* The h1's words at the hero lockup node's own size and colour, per breakpoint. */
.sof-h1 .a{font-size:91.76px;color:#FCCF44}
.sof-h1 .b{font-size:38.34px;color:#FBEFD6}
.sof-h1 .c{font-size:90px;color:#FBEFD6}
.sof-sec{position:relative;width:100%;overflow:hidden;padding-left:24px;padding-right:24px}
/* Inert below 1024 -- it is from 1024 up that this becomes the 1400 cap.
   position:relative at every width on purpose: the hero and You Decide
   plates are absolutely positioned and used to resolve against .sof-sec.
   Anchoring them here is what caps the ARTWORK as well as the text. */
.sof-cap{position:relative;width:100%}
.sof-in{position:relative;width:100%;max-width:1680px;margin:0 auto}
/* Display artwork: Figma renders a node WITH its outside strokes, so the png is
   a little wider than the node box. Widths below are the measured render
   extent (raw px / export scale), not the node box, with the bleed split. */
.sof-art{display:block;width:100%;margin:0 auto}
.sof-art img{width:100%}
.sof-rich{overflow-wrap:anywhere}
/* The brand name leads the You Decide intro in Bold 700 against the
   paragraph's Medium 500. See Tseg(). */
.sof-decide-body strong{font-weight:700}
.sof-grad{background:linear-gradient(90deg,#A3051B 0%,#D14A14 100%)}

/* ===================== 1 · HEADER (870:7 / 870:434) ===================== */
/* 36 and 14 flat, at every width. The bar is mounted scale=False so these
   are real pixels, not design pixels the zoom then rescales. Its wrapper must
   also opt out of the 1920 cap, or the cap would size a box that nothing is
   scaling back down. */
.sof-promobar > .sof-cap{width:100%;padding-left:0;padding-right:0}
/* ⚠️ min-height, NOT height. The bar was a fixed 36px, which fitted
   "SECURE YOUR SEAT" and does not fit Eline's 2026-10-31 line: at 14px it
   measures 407px and the bar is ~296px of usable width at 320, so it wraps
   to two lines below 414. Fixed at 36px with overflow:hidden that wrap was
   still INSIDE the box (32px of text in 36px), so it passed a height check
   and looked like an orphaned "SPOTS" on every phone. Shrinking the type
   to fit one line would need 10px at 320, which is not readable, so the
   bar grows instead and text-wrap:balance splits the two lines evenly. */
.sof-promo{display:flex;align-items:center;justify-content:center;
  min-height:36px;padding:5px 0;
  background:linear-gradient(90deg,#A3051B 0%,#D14A14 100%);overflow:hidden}
.sof-promo span{font-family:League Spartan,Arial,sans-serif;font-weight:700;
  font-size:14px;line-height:1.25;color:#FBEFD6;text-align:center;
  padding:0 12px;text-wrap:balance}

/* COUNTDOWN BAR (982:985 mobile / 982:466 desktop).
   Mounted scale=False, so every length here is a REAL pixel and the bar is
   the same size at 390 and at 2560. Mobile values are the base; the 768 rule
   swaps in the desktop frame's. Nothing between them interpolates, because
   the two frames are not a ratio of each other. */
.sof-cdbar > .sof-cap{width:100%;padding-left:0;padding-right:0}
.sof-cd{display:flex;align-items:center;justify-content:center;gap:10px;
  height:78px;padding:12px 10px;background:#fccf44;overflow:hidden}
.sof-cd-lab{display:flex;flex-direction:column;align-items:flex-start}
.sof-cd-lab b{font-family:__DISPLAY__;font-weight:700;font-size:25px;
  line-height:27px;letter-spacing:.01em;color:#171b2d}
.sof-cd-lab i{font-family:__BARLOW__;font-weight:700;font-size:8.5px;
  line-height:10px;letter-spacing:.03em;color:#963426;font-style:normal}
.sof-cd-units{display:flex;align-items:center;gap:3px}
.sof-cd-u{display:flex;flex-direction:column;align-items:center;
  justify-content:center;width:50px;height:54px;border-radius:8px;
  background:#171b2d}
/* tabular-nums, or the SEC column jitters on every tick */
.sof-cd-u b{font-family:__DISPLAY__;font-weight:700;font-size:30px;
  line-height:30px;color:#f0e8d6;font-variant-numeric:tabular-nums}
.sof-cd-u i{font-family:__BARLOW__;font-weight:700;font-size:8.5px;
  line-height:10px;letter-spacing:.06em;color:#e2c768;font-style:normal}
.sof-cd-c{font-family:__DISPLAY__;font-weight:700;font-size:18px;
  line-height:1;color:#171b2d}
@media (min-width:768px){
  .sof-cd{height:92px;padding:12px 0;gap:40px}
  .sof-cd-lab{gap:2px}
  .sof-cd-lab b{font-size:42px;line-height:40px}
  .sof-cd-lab i{font-size:14px;line-height:17px}
  .sof-cd-units{gap:6px}
  .sof-cd-u{width:74px;height:68px;border-radius:10px;gap:2px}
  .sof-cd-u b{font-size:40px;line-height:40px}
  .sof-cd-u i{font-size:11px;line-height:13px;letter-spacing:.08em}
  .sof-cd-c{font-size:24px}
}
.sof-nav{display:flex;height:58px;background:#0B1A32;overflow:hidden}
.sof-navcell{display:flex;align-items:center;justify-content:center;height:100%;
  font-family:__DISPLAY__;font-weight:900;font-size:18px;letter-spacing:0.5px;
  color:#FBEFD6;cursor:pointer;line-height:1}
.sof-navcell--rule{border-right:2px solid #FBEFD6}
.sof-navcell--gold{color:#FCCF44}
.sof-nav-m{width:100%}
.sof-nav-m .sof-navcell{flex:0 0 50%;gap:10px}
.sof-nav-d{display:none}
.sof-burger{display:inline-block;width:22px;height:16px;position:relative;flex:0 0 22px}
.sof-burger i{position:absolute;left:0;height:3px;background:#fff;display:block}
.sof-burger i:nth-child(1){top:0;width:22px}
.sof-burger i:nth-child(2){top:6.5px;width:22px}
.sof-burger i:nth-child(3){top:13px;width:15px}
.sof-menu-cb{position:absolute;opacity:0;width:0;height:0;pointer-events:none}
.sof-menu{display:none;background:#0B1A32;border-top:2px solid #FBEFD626}
.sof-menu-cb:checked ~ .sof-menu{display:block}
.sof-menu a{display:block;padding:14px 24px;font-family:__COND__;font-weight:700;
  font-size:14px;letter-spacing:.08em;color:#FBEFD6;border-bottom:1px solid #FBEFD626}
.sof-menu a:last-child{border-bottom:0}
.sof-menu a.sof-gold{color:#FCCF44}

/* ========= 2b · SPONSOR LOGO MARQUEE (1027:382 / 1027:1043) =============
   Replaces the six-phrase gold ticker, which the new frame deletes outright.

   Desktop numbers are the 1440 frame's x 4/3, because this build's desktop CSS
   is in 1920 units and is zoomed onto 1400 by .sof-scale. See the patch script
   for why that conversion is the whole ballgame.

   The seam is solved exactly as the ticker solved it: two identical sequences,
   animate to -50%, and the inter-sequence gap lives INSIDE the sequence as
   padding-right. A track-level gap makes the track 2S+G, and -50% then lands
   half a gap short on every cycle. */
.sof-marqbar{padding:22px 0;border-bottom:2px solid #041C32;overflow:hidden}
/* The flex column lives on .sof-cap, NOT on .sof-marqbar: section() wraps
   the markup in .sof-cap, so the band has exactly one child and a gap on
   it spaces nothing. Measured 0px against the design's 14. */
.sof-marqbar > .sof-cap{display:flex;flex-direction:column;
  align-items:center;gap:14px;overflow:hidden}
.sof-marq-win{position:relative;width:100%;overflow:hidden}
.sof-marq-track{display:flex;align-items:center;width:max-content;
  animation:sof-marq 14.7s linear infinite;will-change:transform}
.sof-marq-seq{display:flex;align-items:center;flex:0 0 auto;
  gap:40px;padding-right:40px}
/* Height only: each symbol's own viewBox keeps its proportion, which is what
   lets one symbol serve both the marquee and the plate. */
/* ⚠️ EXPLICIT WIDTH, NEVER width:auto. An inline <svg> carrying only a
   height is sized from its viewBox by Chrome and collapsed to ZERO by
   Safari, so the marquee rendered as an empty cream strip on iOS while
   looking perfect here. Eline, 2026-10-31: "This is not loading". The
   partner plates below it were fine throughout, because those have always
   carried an explicit width -- which is what identified the cause.
   Each width is the height x that SYMBOL's own viewBox ratio
   (bf 560/87=6.437, suits 175/48=3.646, oc 189/35=5.400), so the artwork
   keeps its proportions rather than matching the node box's padding. */
.sof-marq-logo{display:block;flex:0 0 auto;color:#041C32}
.sof-marq-logo--bf{width:212px;height:33px}
.sof-marq-logo--suits{width:95px;height:26px}
.sof-marq-logo--oc{width:121px;height:22px}
.sof-marq-logo--taza{width:107px;height:25px}
.sof-marq-logo--s{width:71.522px;height:24.7px}
.sof-marq-logo--whop{width:95px;height:21px}
@keyframes sof-marq{from{transform:translateX(0)}
                    to{transform:translateX(-50%)}}
/* The frame draws the fade as a gradient in the band's own cream. That works
   on a flat fill and FAILS here, because this page paints a parchment
   texture: a flat cream rectangle over it reads as two pale patches with a
   visible edge. Masking the strip fades the LOGOS instead, so it is correct
   over any background and costs two fewer elements. */
.sof-marq-win{-webkit-mask-image:linear-gradient(90deg,transparent 0,
    #000 56px,#000 calc(100% - 56px),transparent 100%);
  mask-image:linear-gradient(90deg,transparent 0,
    #000 56px,#000 calc(100% - 56px),transparent 100%)}
/* A band sliding forever is exactly what this setting is for. */
@media (prefers-reduced-motion:reduce){
  .sof-marq-track{animation:none}
}

/* ========== 6b · MISSION MAP (904:452, new on 2026-10-09) ===============
   Three day cards of DIFFERENT heights, top aligned, 528 wide with 48 gaps
   (3*528 + 2*48 = 1680, the content column exactly). Day 3 is drawn apart
   from the other two: a gold 4px border instead of a cream 2px one, a red
   chip instead of a gold one, and a gold heading instead of cream.

   It used to be a paid upgrade, which is where the gold came from. It has
   been invite only since 2026-10-21: the upgrade button and its Stripe link
   went then, and the last two lines of copy describing it as a purchasable
   tier went on 2026-10-24. The gold treatment stays because the card is
   still the special one; the modifier is --gold now, after what it does,
   because the old name was after a product that no longer exists.

   Heights come from the content, so the cards are NOT stretched to match --
   `align-items:flex-start`. Stretching them would put a long empty tail under
   day 3, which is the shortest and the one being sold.

   Paint opacities are from the frame, not guessed: row descriptions 0.70,
   the footnote 0.55, the intro 0.85, everything else solid. They read as
   three different greys and are one colour at three alphas. */
.sof-mission{background:#0b1a32;padding-top:64px;padding-bottom:64px}
.sof-mission .sof-in{display:flex;flex-direction:column;align-items:center}
.sof-meyebrow{display:flex;align-items:center;gap:12px;width:100%;
  justify-content:center}
.sof-meyebrow i{display:block;height:2px;background:#fccf44;flex:0 1 80px}
.sof-meyebrow span{font-family:__COND__;font-weight:700;font-size:14.3px;
  letter-spacing:.18em;color:#fbefd6;text-transform:uppercase;white-space:nowrap}
.sof-mission .sof-art{max-width:560px;margin:18px auto 0}
.sof-mission-intro{font-family:__SANS__;font-weight:500;font-size:15px;
  line-height:1.5;text-align:center;color:#fbefd6;opacity:.85;
  max-width:620px;margin:16px auto 0}
.sof-days{display:flex;flex-direction:column;align-items:stretch;gap:20px;
  width:100%;margin-top:28px}
.sof-day{display:flex;flex-direction:column;gap:14px;
  background:#0f304f;border:2px solid #fbefd6;border-radius:24px;padding:24px}
.sof-day--gold{background:#132f4a;border:4px solid #fccf44}
.sof-daychip{display:inline-flex;align-items:center;align-self:flex-start;
  font-family:__COND__;font-weight:700;font-size:14px;letter-spacing:.1em;
  color:#041c32;background:#fccf44;border:3px solid #041c32;border-radius:30px;
  padding:6px 14px;white-space:nowrap}
.sof-daychip--gold{background:#d10721;color:#ffffff}
.sof-day-h{font-family:__DISPLAY__;font-weight:900;font-size:30px;
  line-height:1.05;color:#fbefd6;margin:0}
.sof-day--gold .sof-day-h{color:#fccf44}
.sof-slots{display:flex;flex-direction:column}
/* One column now that the time cell is gone, so the title and detail get the
   slot's full width -- 444 at 1920, which is what the frame gives them. */
.sof-slot{display:block;
  padding:14px 0;border-bottom:1px solid #fbefd626}
.sof-slot:last-child{border-bottom:0}
.sof-slot-t{display:none;flex:0 0 auto;font-family:__MONO__;font-weight:700;font-size:22px;
  line-height:1.3;color:#fccf44;padding-top:2px}
.sof-slot-b{flex:1 1 auto;min-width:0}
.sof-slot-h{font-family:__DISPLAY__;font-weight:700;font-size:22px;
  line-height:105%;color:#fbefd6;margin:0}
/* The after party's sponsor mark, beside the row rather than under it.
   Every opaque pixel of the asset is one ink, #be1e19, and the card behind it
   is #0f304f -- red on navy, the lowest-contrast pairing on the page. So the
   mark sits on a plate rather than straight on the card. Cream #fbefd6 is
   already this card's border and text; the dark border is the day chip's,
   verbatim. Plate 120x36 here, against the 128 the row leaves beside
   "Last call, Bangkok style." */
.sof-slot--bf{display:flex;align-items:center;gap:12px}
.sof-slot--bf .sof-slot-b{flex:1 1 auto;min-width:0}
.sof-bfplate{display:flex;align-items:center;justify-content:center;
  flex:0 0 auto;background:#fbefd6;border:2px solid #041c32;border-radius:12px;
  padding:7px 10px}
.sof-slot-bf{display:block;height:18px;width:auto}
.sof-slot-d{font-family:__SANS__;font-weight:500;font-size:13px;
  line-height:140%;color:#fbefd6;opacity:.7;margin:4px 0 0}
.sof-mission-note{font-family:__SANS__;font-weight:500;font-size:12px;
  line-height:1.5;text-align:center;color:#fbefd6;opacity:.55;margin:24px auto 0}

/* ===== 9c · WHO IT'S FOR (904:551) + FAQ (904:624), new 2026-10-09 =====
   Two columns that are deliberately inverted: "You're in if" is a LIGHT card
   on the navy section, "Skip it if" is a dark one. That inversion is the whole
   point of the section, so the two share a class and differ by a modifier
   rather than being one card styled twice. */
.sof-who{background:#0b1a32;padding-top:64px;padding-bottom:64px}
.sof-who .sof-in{display:flex;flex-direction:column;align-items:center}
.sof-who .sof-art{max-width:520px;margin:18px auto 0}
.sof-wgrid{display:flex;flex-direction:column;gap:20px;width:100%;margin-top:28px}
.sof-wcard{display:flex;flex-direction:column;gap:14px;
  background:#f7f7f5;border:5px solid #fbefd6;border-radius:28px;padding:26px 24px}
.sof-wcard--skip{background:#041c32}
.sof-whead{font-family:__DISPLAY__;font-weight:900;font-size:34px;line-height:1.05;
  color:#041c32;margin:0}
.sof-wcard--skip .sof-whead{color:#fbefd6}
.sof-wrow{display:flex;align-items:flex-start;gap:12px;
  font-family:__SANS__;font-weight:500;font-size:15px;line-height:1.4;
  color:#041c32;margin:0}
.sof-wcard--skip .sof-wrow{color:#fbefd6}
/* The tick and the cross are the only thing telling the two lists apart once
   you are reading a row rather than a heading, so they carry the colour. */
.sof-wrow i{flex:0 0 22px;width:22px;height:22px;display:flex;align-items:center;
  justify-content:center;border-radius:999px;font-style:normal;font-weight:700;
  font-size:13px;line-height:1;background:#63821a;color:#f7f7f5;margin-top:1px}
.sof-wcard--skip .sof-wrow i{background:#d10721;color:#ffffff}
.sof-wcta{display:inline-flex;align-items:center;justify-content:center;gap:10px;
  align-self:center;font-family:__COND__;font-weight:700;font-size:19px;
  color:#041c32;background:#fccf44;border:3px solid #041c32;border-radius:999px;
  padding:14px 24px;margin-top:24px;white-space:nowrap}

.sof-faq{background:#041c32;padding-top:64px;padding-bottom:64px}
.sof-faq .sof-in{display:flex;flex-direction:column;align-items:center}
.sof-faq .sof-art{max-width:520px;margin:18px auto 0}
.sof-faqlist{display:flex;flex-direction:column;gap:12px;width:100%;
  max-width:1200px;margin-top:28px}
/* <details> gives the open/close for free: no JavaScript, keyboard operable,
   and findable by the browser's own in-page search even while collapsed. */
.sof-faqitem{background:#0b1a32;border:2px solid #fbefd640;border-radius:16px;
  overflow:hidden}
.sof-faqitem[open]{border-color:#fccf44}
.sof-faqq{display:flex;align-items:center;justify-content:space-between;gap:16px;
  font-family:__DISPLAY__;font-weight:700;font-size:19px;line-height:1.2;
  color:#fbefd6;cursor:pointer;padding:16px 18px;list-style:none}
.sof-faqq::-webkit-details-marker{display:none}
.sof-faqq::after{content:"+";flex:0 0 30px;width:30px;height:30px;display:flex;
  align-items:center;justify-content:center;font-family:__COND__;font-weight:700;
  font-size:20px;line-height:1;color:#041c32;background:#fccf44;border-radius:999px}
.sof-faqitem[open] .sof-faqq::after{content:"\2013"}
.sof-faqa{font-family:__SANS__;font-weight:500;font-size:14px;line-height:1.5;
  color:#fbefd6;opacity:.8;margin:0;padding:0 18px 18px}
.sof-faqtail{font-family:__SANS__;font-weight:500;font-size:13px;line-height:1.5;
  text-align:center;color:#fbefd6;opacity:.7;margin:20px auto 0}

/* 4 · speakers — the new frame fills eight of the ten plates with real
   photographs; the last two stay as the "?" placeholder. */
.sof-spk-photo{display:block;width:100%;aspect-ratio:336/328;object-fit:cover}
/* DERIVED, not measured: 21.019 x (28 / 41.3).

   AND THAT IS FINE, which is worth stating once here because it governs every
   mobile decision on this page. Joshua's direction, 2026-10-15:

       THE DESKTOP FRAME IS THE DESIGN. MOBILE FOLLOWS ITS CONVENTIONS.

   The mobile frame is not re-pasted when the desktop one is, so it lags. It is
   a POSITIONING reference -- how things stack, what the gutters are, where a
   photo crops -- and nothing more. Any convention the desktop frame
   establishes applies at both breakpoints, scaled, even where the mobile frame
   does not show it yet. The speaker grid's navy bed and border are the worked
   example: desktop has them, the mobile frame predates them, and mobile gets
   them anyway at half the stroke.

   In practice the page renders the DESKTOP frame's text at both breakpoints
   (SPEAKERS_V2 cites desktop node ids). A mobile design_diff run reporting the
   speakers' copy as wrong is the two frames being out of step, not the page.
   */
.sof-spk-name{font-family:__DISPLAY__;font-weight:900;font-size:14.25px;
  line-height:1.05;color:#fbefd6;margin:0}
/* Names are sized per card in BOTH frames, because the longer ones would not
   otherwise hold a line. Mobile numbers come from 909:3845, the first real
   mobile frame this page has had; everything mobile before it was invented. */
/* V3 drops the gold TBA treatment: an unannounced plate reads in the same
   cream as a named one, and only the '?' and 'Announcing soon' set it
   apart. */
.sof-spk-name--tba{color:#fbefd6}
.sof-spk-role{font-family:__BODY__;font-weight:400;font-size:11.196px;line-height:1.3;
  color:#fbefd6;margin:4px 0 0}
.sof-spk-role--tba{opacity:.6}

/* ===================== CONTACT PAGE (909:3267) =========================
   A header, one card, a footer. Measured off the frame: body padding 140/160,
   card 880 wide with 56 of padding and a 4px #050d1a edge, fields 760 wide
   stacked 28 apart, inputs 64 tall (the message box 180) with a 2px #0b1a32
   edge and a 12 radius.

   THE FORM SENDS, since 2026-10-14. It POSTs form-encoded to the n8n webhook,
   which validates it and emails hello@scalingorfailing.com. The handler lives
   in the funnel's header_scripts because that is the only script slot this
   account exposes; it is guarded on form.sof-form and inert elsewhere.

   .sof-send[disabled] below is still used: the handler disables the button
   while sending, and leaves it disabled reading SENT afterwards so a message
   cannot go twice.

   Contract, endpoint, revert path and the traps hit while building it:
   funnels/sof/scaling-or-failing/CONTACT-FORM-IMPLEMENTATION.md

   There is no mobile contact frame, so everything below 768 is derived: the
   card goes full width inside the page gutter and the type steps down. Those
   are decisions, not measurements. */
.sof-contact{background:#041C32;padding-top:56px;padding-bottom:64px}
.sof-contact .sof-in{display:flex;flex-direction:column;align-items:center}
.sof-contact .sof-art{max-width:560px;margin:0 auto}
.sof-contact-sub{font-family:__SANS__;font-weight:400;font-size:15px;
  line-height:1.5;text-align:center;color:#FBEFD6;opacity:.85;
  max-width:620px;margin:14px auto 0}
.sof-form{width:100%;max-width:880px;margin:28px auto 0;
  background:#FBEFD6;border:4px solid #050d1a;border-radius:24px;padding:24px;
  display:flex;flex-direction:column;gap:18px}
.sof-field{display:flex;flex-direction:column;gap:10px}
.sof-field label{font-family:__SANS__;font-weight:500;font-size:13px;
  letter-spacing:.06em;color:#041C32}
.sof-field input,.sof-field select,.sof-field textarea{
  width:100%;height:52px;background:#FFFFFF;border:2px solid #0B1A32;
  border-radius:12px;padding:0 16px;font-family:__SANS__;font-weight:400;
  font-size:15px;color:#041C32;appearance:none}
.sof-field textarea{height:150px;padding:14px 16px;resize:vertical;line-height:1.5}
.sof-field input::placeholder,.sof-field textarea::placeholder{color:#041C3273}
/* The frame draws the topic field as a closed select with its own caret, so
   the native one is removed and redrawn to match. */
.sof-select{position:relative}
.sof-select::after{content:"\25BE";position:absolute;right:18px;bottom:16px;
  font-size:14px;color:#041C32;pointer-events:none}
.sof-field select:invalid{color:#041C3273}
/* The frame's placeholder is the whole option list as one string, 40
   characters, and at 390 it ran under the drawn caret. Reserve the caret's
   column and clip with an ellipsis rather than behind the arrow. */
.sof-field select{padding-right:42px;text-overflow:ellipsis}
@media (min-width:768px){.sof-field select{padding-right:calc(52 * var(--u))}}
.sof-send{display:flex;align-items:center;justify-content:center;gap:10px;
  width:100%;font-family:__COND__;font-weight:700;font-size:20px;
  color:#041C32;background:#FCCF44;border:3px solid #041C32;border-radius:999px;
  padding:14px 24px;margin-top:4px;cursor:pointer}
/* Disabled until it has somewhere to send. Shown, not hidden: the page is
   complete apart from delivery, and a greyed button says that plainly. */
.sof-send[disabled]{opacity:.55;cursor:not-allowed}
.sof-form-note a{color:#041C32;text-decoration:underline;font-weight:700}
.sof-form-note{font-family:__SANS__;font-weight:500;font-size:12px;
  line-height:1.5;text-align:center;color:#041C3299;margin:0}

@media (min-width:768px){
  .sof-contact{padding-top:calc(140 * var(--u));padding-bottom:calc(160 * var(--u))}
  .sof-contact{--u:1px}
  .sof-contact .sof-art{max-width:calc(1163 * var(--u))}
  .sof-contact-sub{font-size:calc(26 * var(--u));max-width:calc(960 * var(--u));
    margin-top:calc(28 * var(--u))}
  .sof-form{max-width:calc(880 * var(--u));padding:calc(56 * var(--u));
    gap:calc(28 * var(--u));margin-top:calc(28 * var(--u));
    border-width:calc(4 * var(--u));border-radius:calc(24 * var(--u))}
  .sof-field label{font-size:calc(20 * var(--u))}
  .sof-field input,.sof-field select,.sof-field textarea{
    height:calc(64 * var(--u));padding:0 calc(20 * var(--u));
    font-size:calc(20 * var(--u));border-radius:calc(12 * var(--u))}
  .sof-field textarea{height:calc(180 * var(--u));padding:calc(18 * var(--u)) calc(20 * var(--u)) 0}
  .sof-select::after{right:calc(20 * var(--u));bottom:calc(20 * var(--u));
    font-size:calc(20 * var(--u))}
  .sof-send{font-size:calc(45.9 * var(--u));padding:calc(22 * var(--u)) calc(30 * var(--u))}
  .sof-form-note{font-size:calc(16 * var(--u))}
}
@supports (container-type: inline-size) {
  @media (min-width:768px) and (max-width:1919px){
    .sof-contact{container-type:inline-size}
    .sof-contact{--u:calc(100cqw / 1920)}
  }
}

/* ===================== 2 · HERO (870:21 / 870:446) ===================== */
.sof-hero{background:#FCECC7}
.sof-hero-pic{display:contents}
.sof-hero-plate{position:absolute;inset:0;width:100%;height:100%;object-fit:cover}
.sof-hero-wash,.sof-hero-shade{position:absolute;left:0;right:0;pointer-events:none}
/* mobile z-order: art -> wash -> shade (desktop flips, see the media block) */
.sof-hero-wash{top:0;bottom:0;background:linear-gradient(180deg,
  #FCECC7F0 0%,#FCECC7E0 42%,#FCECC773 55%,#FCECC700 66%);z-index:1}
.sof-hero-shade{left:0;right:0;bottom:0;height:200px;background:linear-gradient(180deg,
  #061A2C00 0%,#061A2CBF 100%);z-index:2}
.sof-hero-m{position:relative;z-index:3;padding:41px 25px 0;min-height:844px}
.sof-hero-d{display:none}
.sof-date{font-family:__COND__;font-weight:700;font-size:18.5px;color:#041C32;
  text-align:center;width:100%;max-width:329px;margin:0 auto;line-height:1.2}
/* render 322.33 wide vs a 310 node box -> 6.17 of stroke bleed each side.
   auto side margins: the 390 frame puts all of this box's slack on the right,
   which reads as centred at exactly 390 and as left-shifted on every wider
   phone. The 0.17px nudge the frame has is inside the stroke bleed anyway. */
.sof-lockup{width:322.33px;max-width:100%;margin:10px auto 0}
.sof-lockup img{width:100%}
.sof-tag{display:flex;align-items:center;justify-content:center;width:100%;
  max-width:274px;height:30px;margin:3px auto 0;border-radius:15px;
  background:linear-gradient(90deg,#A3051B 0%,#D14A14 100%);
  border:2px solid #FBEFD6;box-shadow:0 3px 7px #0000004D;overflow:hidden}
.sof-tag span{font-family:Archivo Black,Arial Black,sans-serif;font-weight:400;
  font-size:9.661px;letter-spacing:1.8px;color:#FFFFFF;line-height:1;white-space:nowrap}
/* auto side margins for the same reason as .sof-lockup: at 390 the 341px cap
   fills the 340px column so flush-left looked right, and at 430 it left 64px
   of slack on one side. */
.sof-cta{position:relative;display:block;width:100%;max-width:341px;height:61px;
  margin:11px auto 0}
.sof-cta i{position:absolute;left:0;right:0;top:4.8px;height:56px;border-radius:28px;
  background:#041C32}
.sof-cta span{position:absolute;left:0;right:0;top:0;height:56px;border-radius:28px;
  background:#FCCF44;border:3px solid #041C32;display:flex;align-items:center;
  justify-content:center;font-family:__COND__;font-weight:700;font-size:27px;
  color:#041C32;line-height:1;white-space:pre}
.sof-pow{display:flex;align-items:center;width:100%;max-width:263px;height:34px;
  margin:14px auto 0;gap:4px}
.sof-pow b{font-family:__MONO__;font-weight:700;font-size:12px;letter-spacing:.5px;
  color:#041C32;line-height:1}
.sof-pow img{width:182px;height:34px;object-fit:contain;margin-left:auto}
.sof-hosts{display:flex;justify-content:space-between;align-items:flex-start;
  width:calc(100% + 34px);margin:336px -17px 0;padding:0 5px}
.sof-hosts span{font-family:__XCOND__;font-weight:700;font-size:15.5px;
  letter-spacing:-0.1px;color:#FBEFD6;line-height:19px;white-space:nowrap;
  text-shadow:0 4px 14.7px #063B67}

/* ===================== 3 · STATS (870:46 / 870:470) ===================== */
.sof-stats{background:#0B1A32;border-top:1px solid #FBEFD659;
  border-bottom:1px solid #FBEFD659}
.sof-stats-row{display:flex;justify-content:center;align-items:flex-start;
  gap:10.33px;padding:24px 0 23.2px}
.sof-stat{width:116.67px;height:74.8px;display:flex;flex-direction:column;
  align-items:center;padding-top:12.11px}
.sof-stat .sof-num{height:32.09px}
.sof-stat .sof-lab{height:12.75px;margin-top:7.23px}
.sof-stat img{height:100%;width:auto}
.sof-statdiv{align-self:center;width:1px;height:62px;background:#FBEFD659;flex:0 0 1px}

/* ===================== 4 · SPEAKERS (870:66 / 870:490) ================= */
.sof-speakers{padding-top:64px;padding-bottom:64px}
.sof-speakers .sof-art{max-width:343px;margin-left:0}
/* The Figma "Grid line" rectangles are internal only (the 4/6px outside stroke
   is the same colour as the fill, so it paints nothing). Reproduced as grid
   gaps over a tinted container. minmax(0,1fr) is load-bearing: a plain 1fr is
   minmax(auto,1fr) and a nowrap label would blow the column past its share. */
/* The gap IS the line: #fbefd6 at 50%, per 918:866 and its siblings.

   The navy bed and the border come from the DESKTOP frame, not this one. The
   mobile frame has neither -- it predates them -- and Joshua's direction is
   that mobile follows the desktop's conventions rather than its own stale
   copy. Without the navy underneath, half-cream composites over the section's
   cream and the separators read as near-white.

   3px border, not the desktop's 6: the mobile card is 171 against 336, so
   every stroke on this page halves with it. */
.sof-grid{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:2px;
  background-color:#0B1A32;
  background-image:linear-gradient(0deg,#FBEFD680,#FBEFD680);
  outline:3px solid #0B1A32;margin-top:32px}
.sof-card{background:#0B1A32;display:flex;flex-direction:column;overflow:hidden;
  min-height:232px}
/* An ODD number of cards in two columns leaves one orphan, and the empty
   half-cell shows the grid background as a grey block that reads as a missing
   card. This rule gives the orphan the whole row instead.

   It does not fire today -- twelve cards divide by two since the three TBA
   seats were removed on 2026-10-22 -- but it is kept as insurance for the
   next odd count. It matches only `:last-child:nth-child(odd)`, so it has no
   effect at all on an even grid. */
@media (max-width:1023px){
  .sof-grid > .sof-card:last-child:nth-child(odd){grid-column:1 / -1}
  /* and its photo keeps the ROW height rather than scaling with the doubled
     width: two cards plus the 2px gap is 344 of design width against a 160
     tall photo, so 344/160 lands it level with its neighbours. Without this
     the orphan is twice as tall as every card above it. */
  .sof-grid > .sof-card:last-child:nth-child(odd) .sof-photo{aspect-ratio:344/160}
}
.sof-photo{position:relative;width:100%;aspect-ratio:171/160;background:#0F304F;
  display:flex;align-items:center;justify-content:center;
  border-bottom:2px solid #FCECC759}
.sof-photo b{font-family:__MONO__;font-weight:700;font-size:10px;letter-spacing:2px;
  color:#FCECC766;line-height:1}
.sof-photo em{font-family:Passion One,Impact,sans-serif;font-weight:900;font-size:72px;
  font-style:normal;color:#FCECC72E;line-height:1}
/* All three numbers measured off the mobile card, now 949:1753: the role's
   box ends 22 above the bottom, and the text insets 12.21 from each side.
   The sides were 16, which left 138 of measure for a role the frame draws at
   144 -- so the longest one wrapped to a second line. */
.sof-card-foot{padding:12px 12px 22px}
.sof-name{height:12.9px;display:block}
.sof-name img{height:100%;width:auto}
.sof-co{font-family:__BODY__;font-weight:400;font-size:11px;color:#FBEFD6;
  margin-top:6px;line-height:1.2}
.sof-co--tba{color:#FBEFD699}

/* ===================== 5 · FORMATS (870:214 / 870:638) ================= */
.sof-formats{background:#0B1A32;padding-top:64px;padding-bottom:64px}
.sof-eyebrow{display:flex;align-items:center;gap:12px}
.sof-eyebrow b{font-family:__COND__;font-weight:700;font-size:13px;
  letter-spacing:.28em;color:#FBEFD6;line-height:1.2;white-space:nowrap}
/* The rule is 96px as drawn, but it is the ONLY shrinkable thing in this row:
   the label is nowrap by design, so `flex:0 1` lets the rule give way instead
   of the row clipping. At the design width it is still exactly 96. */
.sof-eyebrow i{display:block;height:2px;width:96px;flex:0 1 96px;min-width:0;
  background:linear-gradient(90deg,#A3051B 0%,#D14A14 100%)}
.sof-t-d{display:none}
.sof-t-m{display:block}
.sof-ftitle{margin-top:16px}
.sof-ftitle .sof-art{margin-left:0;margin-right:auto}
.sof-ft1{max-width:342px}
.sof-ft2{max-width:255px;margin-top:10px}
.sof-subline{font-family:__DISPLAY__;font-weight:900;font-size:18px;line-height:110%;
  color:#FBEFD6;margin-top:16px}
.sof-fcards{display:grid;grid-template-columns:minmax(0,1fr);gap:16px;margin-top:32px}
.sof-fcard{background:#041C32;border:2px solid #FBEFD6;border-radius:16px;
  overflow:hidden;display:flex;flex-direction:column}
.sof-fcard-img{position:relative;width:100%;aspect-ratio:342/200}
.sof-fcard-img img{width:100%;height:100%;object-fit:cover}
.sof-fcard-img i{position:absolute;left:0;right:0;bottom:0;height:6px;
  background:linear-gradient(90deg,#A3051B 0%,#D14A14 100%)}
.sof-fcard-body{padding:24px}
.sof-fkick{font-family:__COND__;font-weight:700;font-size:12px;letter-spacing:.2em;
  color:#FCCF44;line-height:1.2}
.sof-fhead{font-family:__DISPLAY__;font-weight:900;font-size:28px;line-height:96%;
  color:#FBEFD6;margin-top:12px}
.sof-fbody{font-family:__SANS__;font-weight:500;font-size:14px;line-height:145%;
  color:#FBEFD6D9;margin-top:12px;overflow-wrap:anywhere}

/* ===================== 6 · YOU DECIDE (870:261 / 870:686) ============== */
/* The vertical padding is on the CAP, not the section -- same reason as the
   1024 block. On the section it inset .sof-cap, and the lizard plate is
   positioned against the cap, so the artwork was pushed down with it: at
   390 it started 220 from the top instead of the 180 the design asks for,
   and ran 40 past the bottom where overflow:hidden cut it off, leaving a
   band of paper texture above it. On the cap the plate resolves against a
   padding box that starts at the section's top edge, so 180 means 180 and
   180 + 800 lands exactly on the section's 980. */
.sof-decide{background:#FCECC7 url(__TEX_PAPER__) repeat;background-size:1024px 1024px;
  min-height:980px}
/* min-height:inherit so the cap FILLS the band rather than stopping at its
   own content. .sof-decide-wash is top:0;bottom:0 and is therefore sized
   by the cap: left to shrink-wrap, the cream fade came out 520 tall in a
   980 section at 390 and 592 in 864 at 768, roughly half the gradient the
   design draws. Before .sof-cap existed the wash resolved against the
   section and got the full height; this restores that. The artwork is
   unaffected either way -- it carries an explicit height. */
.sof-sec.sof-decide{padding-left:0;padding-right:0}
.sof-decide > .sof-cap{padding:40px 0;min-height:inherit}
/* Below 1024 the cap's side padding is dropped and the gutter moves here,
   so the plate can run to both edges while the copy stays inset. */
.sof-decide .sof-in{padding-left:24px;padding-right:24px}
/* display:contents so the <picture> generates no box and the <img> keeps the
   section (.sof-sec is position:relative) as its containing block -- the same
   mechanism .sof-hero-pic uses for the hero plate. */
.sof-decide-pic{display:contents}
.sof-decide-bg{position:absolute;left:0;right:0;top:180px;bottom:0;width:100%;
  height:800px;object-fit:cover}
.sof-decide-wash{position:absolute;left:0;right:0;top:0;bottom:0;pointer-events:none;
  background:linear-gradient(180deg,#FCECC7 0%,#FCECC7ED 45%,#FCECC78C 61.48%,
  #FCECC700 66%)}
.sof-decide .sof-in{z-index:2}
.sof-kicker{font-family:__COND__;font-weight:700;font-size:18px;letter-spacing:.02em;
  color:#041C32;line-height:1.2}
/* The h2 itself is NEVER hidden -- it carries the sr-only heading text, and a
   display:none h2 takes that heading away from a screen reader and drops the
   page from 6 rendered h2s to 5. Only the artwork inside it is per-breakpoint,
   and below 768 it scales rather than disappearing: hiding it left a ~400px
   empty beige band where the 202px intro margin had reserved its space. */
.sof-decide-head{margin:0}
.sof-decide-art{display:block;width:100%;margin:0}
.sof-decide-body{font-family:__SANS__;font-weight:500;font-size:15.5px;
  line-height:22px;letter-spacing:-0.003em;color:#041C32;overflow-wrap:anywhere}
.sof-decide-intro{margin-top:24px}
.sof-decide-promise{margin-top:16px}
.sof-only-d{display:none}
.sof-only-m{display:block}

/* ===================== 7 · TOPICS (870:299 / 870:716) ================== */
.sof-topics{background:#0D1422 url(__TEX_DARK__) repeat;background-size:1024px 1024px;
  padding-top:58px;padding-bottom:50.76px}
.sof-topics .sof-art{max-width:344px;margin-left:0}
.sof-subtitle{font-family:__DISPLAY__;font-weight:900;font-size:15.5px;
  line-height:118%;letter-spacing:.6px;color:#FBEFD6;text-align:center;
  width:100%;max-width:297px;margin:5.63px auto 0}
.sof-chips{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:8.19px 8px;
  margin-top:28px}
.sof-chip{position:relative;background:#061A2C;border:1.085px solid #FBEFD6;
  border-radius:7px;padding:4.46px;aspect-ratio:167/57.34}
.sof-chip-panel{position:relative;overflow:hidden;border-radius:3px;height:100%;
  background:#FBEFD6 url(__TEX_PAPER__) repeat;background-size:512px 512px;
  display:flex;align-items:center;justify-content:center}
.sof-chip-tab{position:absolute;left:0;top:0;width:24.25px;height:21.92px;
  clip-path:polygon(0 0,100% 0,0 100%)}
.sof-chip-tab--y{background:#FCCF44}
.sof-chip-tab--r{background:#D10721}
.sof-chip-label{position:relative;font-family:__DISPLAY__;font-weight:900;
  font-size:24.45px;line-height:100%;letter-spacing:-0.015em;color:#041C32;
  text-align:center;white-space:nowrap}

/* ===================== 8 · TICKETS (870:370 / 870:782) ================= */
/* Speakers, Tickets and Sponsor are painted with the parchment texture --
   one image, three sections, full bleed, FILL in the frame. The flat cream
   stays as the background-color underneath: it is what shows before the
   image arrives, and it is the colour the texture mostly is, so there is
   no flash. */
.sof-speakers,.sof-tickets,.sof-sponsor{
  background-color:#FCECC7;background-image:url(__PARCHMENT__);
  background-size:cover;background-position:center;background-repeat:no-repeat}
.sof-tickets{padding-top:61.5px;padding-bottom:64px}
.sof-ttitle .sof-art{margin:0 auto}
/* 918:1063, the mobile title frame, is 317.51 wide including its 5.43 of
   padding. One line, one image. */
.sof-ttitle .sof-art{max-width:317.51px}
/* Rule, text, rule -- 918:1066 on mobile, 923:2046 on desktop. Navy rules,
   not the red-to-orange gradient the Formats eyebrow uses; this one is its own
   thing and gets its own class rather than borrowing that one. */
.sof-teyebrow{display:flex;align-items:center;justify-content:center;gap:6px;
  margin:0}
/* flex:0 1 with min-width:0 so the rules SHRINK rather than push the row off
   the page. The label is nowrap and at 320 it alone takes 295 of the 296
   available, so there is nothing left for the rules -- better they vanish
   than that the row overflows. The Formats eyebrow does the same. */
.sof-teyebrow i{display:block;flex:0 1 14px;min-width:0;width:14px;height:2px;
  background:#041C32}
.sof-teyebrow b{font-family:__COND__;font-weight:700;font-size:10.5px;
  letter-spacing:.28em;color:#041C32;line-height:1.2;white-space:nowrap}
/* 28% tracking puts a trailing space after the last letter in CSS, which Figma
   does not draw; pulling it back keeps the right-hand rule where the frame has
   it. */
.sof-teyebrow b{margin-right:-.28em}
.sof-ttitle{margin-top:14px}
.sof-tdate{font-family:__MONO__;font-weight:700;font-size:13.99px;letter-spacing:.02em;
  color:#041C32;text-align:center;margin-top:4px;line-height:1.2}
/* 909:3159, new in V3: a line under the date. */
.sof-REMOVED-tkicker{font-family:__COND__;font-weight:700;font-size:10.5px;letter-spacing:.08em;
  text-transform:uppercase;text-align:center;color:#041C32;margin:8px 0 0}
/* ONE card now. 949:1953 is 342 x 549 with the stub a 148-tall band across
   the bottom; 949:1454 is 1200 x 640 with the mark in a column on the right.
   Same two parts, stacked one way or the other -- but both on the card's
   cream now, with no panel and no perforation between them. */
/* The frame strokes this 2.74 on three sides and 10.97 on the bottom -- a
   4:1 lip, where the live card ran 3.6:1. padding-top clears the banner:
   36 of strip plus 20 of air at real size. */
.sof-tcard{position:relative;display:flex;flex-direction:column;
  background:#FBEFD6;border:1.68px solid #041C32;border-bottom-width:6.72px;
  border-radius:11.74px;overflow:hidden;margin-top:29px;
  padding:56px 20px 20px}
/* 982:1426 at real size; the 1024 rule swaps in the 1440 frame's values
   multiplied by 4/3, because above 1024 these are design px under the zoom. */
.sof-tbanner{position:absolute;left:0;right:0;top:0;display:flex;
  align-items:center;justify-content:center;gap:9px;height:36px;
  background:#fccf44;margin:0}
.sof-tbanner b{font-family:__BARLOW__;font-weight:700;font-size:15px;
  line-height:18px;letter-spacing:.06em;color:#041c32}
.sof-tcheck{display:flex;align-items:center;justify-content:center;
  width:18px;height:18px;border-radius:4px;background:#6ba35e;flex:none}
.sof-tcheck svg{width:9px;height:6.5px;display:block}
/* The pills are 191 wide, the title 180, and the card's inner measure is 300
   at 390 and 270 at 320. So the mark can share a row with the TITLE
   (180+12+96=288) but never with the PILLS (191+12+96=299 against 300 is a
   one-pixel miss, and 320 is nowhere close). Hence: pills span both columns,
   the mark sits beside the title and the price. Desktop has room for all
   three beside it and swaps the areas rather than the markup. */
/* ⚠️ COLUMN 1 WAS max-content, AND THAT RULE DIED WITH THE TITLE.
   The intent above -- title never wraps, badge takes whatever is left --
   held while the title was "EARLY BIRD". On 2026-10-31 it became
   "FULL ACCESS PASS", which is 290px unwrapped, so column 1 claimed the
   whole row and the badge was handed the remainder: 0x0 at 375 and 390,
   30px at 425. Invisible on the two commonest phone widths.
   Inverted deliberately: the badge gets a definite column and the title
   wraps into what is left. A title that wraps is a layout choice; a badge
   that disappears is a bug. */
.sof-ttop{display:grid;grid-template-columns:minmax(0,1fr) auto;
  grid-template-areas:"badges badges" "name mark" "price mark";
  column-gap:12px;align-items:start}
/* The Scalizard mark sits on the card's own cream, not on a panel. The badge
   asset is transparent and its outermost ring is #031622; against the navy
   stub that used to be here (#041C32) the outline vanished and the mark read
   as a bare gold ring. Cream is what the reference draws it on, and the
   outline reads against it. */
.sof-tmark{grid-area:mark;align-self:center;display:flex;min-width:0;
  align-items:center;justify-content:center}
/* One row: the V2 strings are short enough to share it (about
   226px of pills against about 318px of measure at 390), which
   is how the frame draws them. wrap, so a 320 phone or a longer
   string drops to two rows instead of overflowing. */
.sof-badges{grid-area:badges;display:flex;flex-direction:row;
  flex-wrap:wrap;align-items:center;gap:8px}
.sof-badge{display:inline-flex;align-items:center;justify-content:center;height:28px;
  padding:0 16px;border-radius:14px;
  background:linear-gradient(90deg,#A3051B 0%,#D14A14 100%);
  font-family:__COND__;font-weight:700;font-size:12px;letter-spacing:.08em;
  color:#FFFFFF;line-height:1;white-space:nowrap}
/* V2: badge 2 carries the same red gradient as badge 1 and is set apart
   by a stroke rather than by colour. It inherits the gradient from
   .sof-badge, so only the stroke is declared. */
.sof-badge--urgent{border:2px solid #041c32}
.sof-tname{grid-area:name;font-family:__DISPLAY__;font-weight:900;
  font-size:44px;line-height:90%;
  letter-spacing:-0.02em;color:#041C32;margin-top:16px}
/* GTA cash. Every colour sampled from Joshua's mock rather than guessed:
   green #b3d497, outline #0c0f0a, compare grey #787a7c, strike #b3442c,
   underline #6c96f6.

   ⚠️ THE FACE IS NOT RIGHT AND CANNOT BE. The mock is set in Pricedown, the
   GTA logo font. It is not a webfont and we do not have the file, so this is
   Barlow Condensed Black wearing Pricedown's colours. The weight, the green
   and the hard black extrusion carry most of the feel; the letterforms do
   not. Licence and self-host Pricedown, or export the two prices as artwork,
   and this rule can drop the fallback.

   The outline is eight text-shadows at the compass points rather than
   -webkit-text-stroke, because a text stroke is painted CENTRED on the glyph
   edge and eats into a heavy face like this one until the counters close up.
   The ninth shadow is the offset that gives it depth. */
/* One line, as both frames draw it: 918:534 + 918:550 on desktop and
   918:1025 + 918:1041 on mobile. The gap is the measured distance between
   them and `center` is their measured alignment -- each sits ~6px inside the
   price's cap height top and bottom. */
.sof-tpricerow{grid-area:price;display:flex;align-items:center;
  gap:15.8px;margin-top:4px;
  flex-wrap:wrap}
.sof-tprice{font-family:__DISPLAY__;font-weight:900;font-size:46.103px;line-height:90%;
  letter-spacing:-0.01em;color:#9ed88e;
  text-shadow:
    -2px -2px 0 #0c0f0a,  2px -2px 0 #0c0f0a,
    -2px  2px 0 #0c0f0a,  2px  2px 0 #0c0f0a,
     0   -2px 0 #0c0f0a,  0    2px 0 #0c0f0a,
    -2px  0   0 #0c0f0a,  2px  0   0 #0c0f0a,
     5px  5px 0 #0c0f0a}

/* "Was" price. Not in the Figma frame at all -- it is derived from the badge
   the design DOES carry, "SAVE $1,000 · EARLY BIRD", so 1997 + 1000 = 2997.
   If the saving ever changes, this number has to change with it. */
/* It lives in .sof-tpricerow now, so the row's align-items:center places it
   and nothing stretches it. It was previously a direct child of .sof-tcard, a
   flex COLUMN, where align-items:stretch pulled it to the full card width
   whatever its display was -- the blue rule then ran the width of the card and
   the rotated strike swept diagonally across the whole of it. */
/* #041c32 at 55%, which is what the node carries -- navy over cream reads as
   the grey in the design. Written as an 8-digit hex rather than `opacity`,
   because opacity on the element would fade the red strike with it.

   No border-bottom. The build used to draw a blue 3px rule under this price;
   nothing in either frame draws one. */
.sof-tcompare{position:relative;display:inline-block;
  font-family:__DISPLAY__;font-weight:900;font-size:29.34px;line-height:1;
  letter-spacing:-0.01em;color:#041C328C;margin:0}
/* The strike is a rotated bar, not text-decoration: line-through cannot be
   angled or given its own colour and thickness independently of the text. */
/* A rotated bar, not text-decoration: line-through cannot be angled, nor
   given its own colour, thickness and rounded ends. The numbers are the
   Strike rectangle's: #db1a1f, 8.9% of the font size thick, overhanging the
   text by 6.3% each side, fully rounded ends, 10 degrees. CSS rotation is
   clockwise-positive where Figma's is counterclockwise, hence -10. */
.sof-tcompare::after{content:"";position:absolute;left:-6.3%;right:-6.3%;
  top:46%;height:2.62px;border-radius:1.57px;background:#db1a1f;
  transform:rotate(-10deg);pointer-events:none}
.sof-tlist{list-style:none;margin:24px 0 0;padding:0}
.sof-tlist li{position:relative;padding-left:18px;font-family:__SANS__;
  font-weight:500;font-size:15px;line-height:1.2;color:#041C32;margin-top:10px;
  overflow-wrap:anywhere}
.sof-tlist li:first-child{margin-top:0}
.sof-tlist li::before{content:"";position:absolute;left:0;top:5px;width:8px;height:8px;
  border-radius:50%;background:linear-gradient(90deg,#A3051B 0%,#D14A14 100%)}
/* .sof-tmore's rules are gone with it. The element left the markup several
   frames ago; its CSS stayed, and the `margin-top:auto` in it was what pinned
   the ticket buttons to one line -- so the pin silently stopped working. If a
   "more info" line ever comes back, give it fresh rules. */
/* width:auto, not width:100%: the card's own padding is the gutter now, so
   the button simply fills what is left of the card's inner measure. */
.sof-tbtn{position:relative;display:block;width:auto;max-width:none;height:64px;
  margin:24px 0 0}
.sof-tbtn i{position:absolute;left:0;right:0;top:4px;height:60px;border-radius:30px;
  background:#041C32}
.sof-tbtn span{position:absolute;left:0;right:0;top:0;height:60px;border-radius:30px;
  background:#FCCF44;border:3px solid #041C32;display:flex;align-items:center;
  justify-content:center;font-family:__COND__;font-weight:700;font-size:22.65px;
  color:#041C32;line-height:1;white-space:pre}
/* The split-pay option: a plain link under the button rather than a second
   button, so the one real CTA on the card keeps all the visual weight. */
.sof-tsplit{text-align:center;margin:14px 0 0;font-family:__SANS__;
  font-weight:500;font-size:14px;color:#041C32}
.sof-tsplit a{color:#041C32;font-weight:700;text-decoration:underline}
/* The Scalizard badge sits ON the stub now, not floated over the card, so it
   is a flex child rather than absolutely positioned. -8 degrees in both
   frames. */
/* Fills whatever the title leaves rather than taking a fixed size, so the
   title can never be squeezed into wrapping and the badge is as big as the
   width allows. 160 is the cap: the tablet block starts at 164 at 480, and
   without a cap this would reach 188 at 479 and then jump down. */
/* 8 degrees, as the frame places it (982:915). On the <img> rather than
   its flex parent, so the rotation does not move the layout box. */
.sof-sticker{transform:rotate(8deg);
  display:block;width:96px;max-width:96px;height:auto;
  aspect-ratio:1/1;transform:rotate(-8deg);flex:0 1 auto}

/* ===================== 9 · SPONSOR (870:416 / 870:828) ================= */
/* Cream, not navy: 918:579 and 918:1070 are both #fcecc7, the same cream
   as the Tickets band above. The frame paints a parchment texture over it;
   this build renders every cream band flat, as Tickets already does. */
.sof-sponsor{padding-top:64px;padding-bottom:64px;text-align:center}
.sof-partner{font-family:__COND__;font-weight:700;font-size:13px;letter-spacing:.28em;
  color:#a3051b;line-height:1.2}
.sof-sponsor-rule{width:48px;height:3px;margin:8px auto 0;
  background:linear-gradient(90deg,#A3051B 0%,#D14A14 100%)}
.sof-powered{font-family:__DISPLAY__;font-weight:900;font-size:48px;line-height:92%;
  letter-spacing:-0.01em;color:#041C32;margin-top:13px}
/* Navy at 6% fill and 18% stroke, per 918:584 -- the plate reads as a tint
   of the cream it sits on, which is why it had to flip with the band. */
.sof-plate{width:100%;max-width:342px;height:124px;margin:40px auto 0;
  border-radius:16px;background:#041C320F;border:1px solid #041C322E;
  display:flex;align-items:center;justify-content:center}
.sof-plate .sof-plate-logo{width:280px;height:43px;color:#C01400}
/* NEW 2026-10-31 (1027:902 / 1027:1551): the smaller partners, which the
   previous frame did not have at all. Figma draws them as FOUR tiers --
   Diamond (BestFulfill, the big plate above), Platinum (Outcraft, solo),
   Gold (Suits/Whop/"Sponsor S" together) and Silver (Tazapay, solo) -- each
   its own centred row with a uniform gap between tiers (24px here, 96px at
   the x4/3 desktop breakpoint). Tazapay joined as the solo Silver plate on
   2026-11-02 (1033:674 / 1033:1365); Whop and the unnamed "Sponsor S"
   monogram (the Figma layer's own name -- no wordmark, no brand name given)
   joined the Gold row on 2026-11-04 (1062:1609 / 1062:1618 desktop,
   1062:2348 / 1062:2357 mobile). An earlier version of this flattened all
   five into one row, which was wrong against the actual frame -- fixed here. */
.sof-tier{display:flex;justify-content:center;margin-top:24px}
.sof-tplate{border-radius:16px;background:#041C320F;border:1px solid #041C322E;
  display:flex;align-items:center;justify-content:center}
.sof-tplate svg{display:block;color:#041C32}
.sof-tplate--oc{width:166px;height:76px}
.sof-tplate--oc svg{width:140px;height:26px}
.sof-tplate--taza{width:109px;height:42px}
.sof-tplate--taza svg{width:89px;height:21px}
/* The Gold row (Suits/Whop/Sponsor S) is the only tier with more than one
   plate, so it keeps its own flex row rather than the solo .sof-tier/
   .sof-tplate pair above. Measured flush at 341 (3 plates of 107 + 2 gaps
   of 10), which happens to equal the old two-brand row's width -- the
   frame's own numbers, not a rule carried over from that version. */
.sof-sponsors{display:flex;align-items:center;justify-content:center;
  gap:10px;margin-top:24px;width:100%;max-width:341px;
  margin-left:auto;margin-right:auto}
.sof-splate{flex:1;min-width:0;height:60px;border-radius:16px;
  background:#041C320F;border:1px solid #041C322E;
  display:flex;align-items:center;justify-content:center}
.sof-splate svg{display:block;color:#041C32;max-width:calc(100% - 10px)}
.sof-splate--suits svg{width:85px;height:23px}
.sof-splate--whop svg{width:85px;height:19px}
.sof-splate--s svg{width:85px;height:29.355px}

/* ===================== 10 · FOOTER (870:422 / 870:834) ================= */
.sof-footer{background:#070E1A;border-top:2px solid #FBEFD626;padding-top:40px;
  padding-bottom:40px}
.sof-footer-in{display:flex;flex-direction:column;align-items:flex-start}
.sof-fbrand{font-family:__DISPLAY__;font-weight:900;font-size:16px;
  letter-spacing:.02em;color:#FBEFD6;line-height:1.2}
.sof-fdate{font-family:__MONO__;font-weight:700;font-size:7px;letter-spacing:.06em;
  color:#FBEFD6;opacity:.6;margin-top:6px;line-height:1.2}
.sof-fnav{display:flex;flex-direction:column;align-items:flex-start;gap:12px;
  margin-top:28px}
.sof-fnav a{font-family:__COND__;font-weight:700;font-size:10px;letter-spacing:.08em;
  color:#FBEFD6;line-height:1.2}
.sof-fnav a.sof-gold{color:#FCCF44}
.sof-fcopy{font-family:__SANS__;font-weight:500;font-size:8px;color:#FBEFD6;
  opacity:.5;margin-top:28px;line-height:1.2;overflow-wrap:anywhere}

/* ======================================================================== */
/* SMALL SCREENS BELOW THE MOBILE FRAME — 390 is the narrowest width the     */
/* design was drawn at, and three boxes on it are sized in px that do not    */
/* survive it: the page gutter, the hero gutter and the ticket card pad.     */
/* Shrinking those three containers (never the type) clears the clipping at  */
/* 320 and at 360; 375, which measured clean already, is untouched.          */
/* ======================================================================== */
@media (max-width:374px){
  .sof-sec{padding-left:12px;padding-right:12px}
  .sof-hero-m{padding-left:12px;padding-right:12px}
  /* The card carries the padding now and nothing inside it adds more --
     when both did, the measure shrank twice over and the button's label
     overflowed its own pill at 320. The inner measure here is 270, so the
     mark steps down to 72 and the gap to 8: 180 of title + 8 + 72 = 260,
     which leaves 10. At 96 it would not fit. */
  .sof-tcard{padding:12px}
  /* the gutter this band uses lives on the cap, not the section */
  .sof-decide .sof-in{padding-left:12px;padding-right:12px}
  /* No fixed size here any more: the badge takes what the title leaves,
     which is 82 at 320. A fixed 72 was both smaller than it needed to be and
     blind to the actual measure.

     The cap is here because this band is ROOMIER than the one above it: the
     section gutter doubles at 375 and the card's padding goes 12 -> 20, so
     the card drops from 346 at 370 to 327 at 375. Uncapped, the badge would
     reach 132 at 370 and then fall to 93 one pixel later. 96 holds it level
     across that line. */
  .sof-ttop{column-gap:8px}
  /* The host strip deliberately bleeds past the hero gutter -- 17px each side
     against the 390 frame's ~25px gutter, so the strip sits ~8px inside the
     viewport. This block tightens that gutter to 12px and the 17px bleed then
     overshot it: the strip measured -5.0..325.0 at 320, -5.0..365.0 at 360 and
     -5.0..379.0 at 374, with the hero's overflow:hidden eating 5px of its edge
     padding and the outer names' text-shadow at both ends. Bring the bleed
     into line with the tightened gutter -- 12px, so the strip starts exactly
     at the viewport edge and its own 5px padding is what insets the names.
     The three names set 297.3px at 320 against 310px of content here, so
     space-between still has 12.7px to distribute and nothing is severed.
     375 and up keep the design's own 17px and are untouched. */
  .sof-hosts{width:calc(100% + 24px);margin-left:-12px;margin-right:-12px}
  /* The hero CTA label is 294.39px at 27px and the button's content box is
     the viewport minus the 12px gutters minus its 3px borders -- 290px at 320.
     Nothing is cut today (overflow is visible and no ancestor clips) but the
     label lands 0.8px inside the box, so a fallback face for the U+2192 arrow
     would sever it. The container is already full-width, so this is the one
     place the type has to give. min() keeps the design's 27px everywhere it
     fits and only ramps below ~347px: 24px at 320, where the label sets
     261.7px inside 290px -- 14px of clearance each side. */
  .sof-cta span{font-size:min(27px,calc(11.1vw - 11.5px))}
}

/* ======================================================================== */
/* TABLET — 768 to 1023.                                                   */
/* The desktop frame is 1920 and its type is authored for it: 88px prices,   */
/* 54px button labels, 42.6px nav cells, 46px card headings. None of that    */
/* fits a 768-1023 content column, which is what made this range unusable --  */
/* the old breakpoint handed it the 1920 layout at 40% of the width.         */
/* So the MOBILE design serves this range instead, centred in a 520px        */
/* column: it is a complete, measured layout whose every box is fluid, and   */
/* the hero <picture> already swaps to the landscape plate above 767. The    */
/* desktop block below now starts at 1200, which is the narrowest width at   */
/* which the 1920 frame's containers still hold (verified per section).      */
/* ======================================================================== */
/* ---- 8b | tablet: 480 to 1023 ---------------------------------------
   The card has no max-width below 768, so it grew to 672 at a 720 viewport
   and snapped back to 520 at 768. Meanwhile the mark stayed 96 and the title
   stayed 44, both mobile sizes, until 1024. The result was up to 354px of
   dead cream between the title and the mark.

   Capping the card at the 520 it already takes from 768 up removes the snap,
   and the desktop grid areas plus a mark that scales with the grid spend the
   width that is left. The pills are 191 wide and have to keep fitting the
   left column, which is what sets the 480 floor: below it, the mobile layout
   stays. */
@media (min-width:480px) and (max-width:1023px){
  .sof-tcard{max-width:520px;margin-left:auto;margin-right:auto}
  .sof-ttop{grid-template-areas:"badges mark" "name mark" "price mark";
    grid-template-columns:minmax(0,1fr) 42%;column-gap:16px}
  .sof-tmark{align-self:center}
  /* Fills its column rather than taking a fixed size, so it tracks the card
     instead of stranding it. 42% of 478 is 200, which is close enough to the
     155 the desktop badge renders at under the 1024 zoom that the crossing
     does not read as a jump. */
  .sof-sticker{width:100%;height:auto;max-width:220px;aspect-ratio:1/1}
}

@media (min-width:768px) and (max-width:1023px){
  .sof-sec{padding-left:max(24px,calc((100% - 520px)/2));
           padding-right:max(24px,calc((100% - 520px)/2))}
  /* Two hero boxes are sized in px with no auto margin. At 390 the column is
     342px wide, so left-align READS as centred -- in this 570px column it does
     not, and both sat ~90-100px off the axis every sibling centres on. Centre
     them here, and drop the lockup's -0.17px stroke-bleed nudge, which is a
     correction for the 390 column only. 390 and 1200+ keep their own margins. */
  .sof-menu a{padding-left:max(24px,calc((100% - 520px)/2));
              padding-right:max(24px,calc((100% - 520px)/2))}
  .sof-stats-row{gap:40px}
  /* The You Decide plate keeps the MOBILE artwork in this band, and that crop
     is PORTRAIT -- 506x900, sky and skyline down to about 60%, then the
     lizard in the car. Its box here was a FIXED 800px tall while the width
     ran to 1199, so object-fit:cover scaled by the width (x2.37 at 1199) and
     only 37% of the height survived. Centred, that was a strip of skyline
     with the top of a pair of sunglasses at the bottom edge.

     Two changes, and the height is the one doing the work. Tying it to the
     width keeps the SAME half of the artwork in frame at every size in the
     band instead of less and less of it, and bottom-anchoring spends what is
     still cropped on sky, which carries nothing. 0.89 x width shows the lower
     half: the lizard sits at ~71% down the file, so it lands comfortably
     inside the frame rather than on its edge.

     Scoped to this band on purpose: below 768 the crop is in the box it was
     drawn for, and from 1200 the landscape artwork takes over. */
  /* No min-height and no forced plate height any more: below 1024 the plate
     is in the flow under the copy, so the section is as tall as its content
     and the plate keeps its own aspect. */
  /* the 520 column, on the cap so the plate still spans the full band */
  .sof-decide .sof-in{padding-left:max(24px,calc((100% - 520px)/2));
    padding-right:max(24px,calc((100% - 520px)/2))}

}

/* ---- You Decide, 480 to 1023: artwork UNDER the copy ------------------
   PHONES ARE NOT IN HERE. Below 480 the section keeps the frame's overlay,
   copy over the plate, which Topi confirmed was already right -- the
   original complaint was the plate's WIDTH, not the overlap. Stacking it
   on a phone left a tall band of empty sky above the car.
   The plate was absolutely positioned at top:180 with the copy sitting over
   its faded top edge. Eline, 2026-10-23: nothing should touch the image. An
   offset cannot guarantee that -- the copy's height changes with the width,
   so any fixed top is wrong at some size.

   So the plate leaves the stacking and joins the flow, ordered AFTER the
   copy. The gap is then a margin that cannot be overrun, whatever the copy
   does. The wash goes with it: it exists to fade the image behind the text,
   and there is no longer any text over the image.

   The gutters move from the cap to .sof-in so the plate still runs to both
   screen edges while the copy keeps its inset -- the same split that made the
   artwork full bleed in the first place. */
@media (min-width:480px) and (max-width:1023px){
  .sof-decide{min-height:0}
  .sof-decide > .sof-cap{display:flex;flex-direction:column;
    padding:40px 0 0;min-height:0}
  /* order only. The GUTTER is set per band further up: 24 at the base, 12
     below 375, and the centred 520 column from 768. Setting it here too
     would beat all three, which is what flattened the tablet band back to
     a 24px gutter. */
  .sof-decide .sof-in{order:1}
  .sof-decide-bg{position:static;order:2;width:100%;height:auto;
    max-height:none;margin-top:28px;object-fit:contain;
    -webkit-mask-image:linear-gradient(180deg,transparent 0,#000 16%);
            mask-image:linear-gradient(180deg,transparent 0,#000 16%)}
  /* The fade is a MASK on the image now, not the full-section wash. The wash
     was a cream gradient painted over the top of the plate while the plate
     sat behind the copy; with the plate moved below the copy it had nothing
     to fade and was switched off, which took the soft top edge with it.
     Masking the image instead keeps the same look and cannot drift out of
     register, because it is the image's own edge rather than a second box
     positioned over it. */
  .sof-decide-wash{display:none}
}

/* The mobile plate is a 506x900 portrait. At phone widths its natural height
   is the crop as drawn -- 694 at 390. Wider, the same ratio runs away: 960
   tall at 540, 1364 at 768, 1820 at 1023, which made the section 1547, 2049
   and 2639 tall. From 480 up it keeps that picture but takes a capped height,
   anchored to the BOTTOM so the car and the lizard stay in frame instead of
   the sky. */
@media (min-width:480px) and (max-width:1023px){
  .sof-decide-bg{height:min(62vh,620px);object-fit:cover;
    object-position:50% 100%}
}

/* ======================================================================== */
/* HEADER + HERO: the 1920 composition, SCALED, from 768 up.                */
/*                                                                          */
/* These two left the 1200 block on 2026-10-10. Everything else on the page */
/* keeps the ladder -- grids reflow, and a 5-up speaker grid scaled to 768  */
/* would be 134px cards -- but the header and the hero are not grids. They  */
/* are one drawn composition, and between 768 and 1023 the page used to     */
/* serve the MOBILE one: a 390-wide PORTRAIT artwork in a 1024-wide window. */
/* Full bleed it covered by the long side and showed a strip of sky and the */
/* tops of three heads; capped at the 570 column it was a narrow island     */
/* with cream down both sides of a 1024 screen. Neither is the design.      */
/*                                                                          */
/* A portrait image cannot fill a landscape window. The landscape one can,  */
/* and it already scales, so it runs the whole way down to 768 now. At 768  */
/* --u is 0.4: the hero is 435 tall, the lockup 279 wide, the button label  */
/* 21.6px. Small, but the design's own proportions, edge to edge, with all  */
/* three men and their names where the frame puts them.                     */
/*                                                                          */
/* The header comes along so the two never disagree again -- a burger menu  */
/* over a desktop hero was the exact mismatch this started from.            */
/* ======================================================================== */
@media (min-width:768px){
  /* One DESIGN pixel, and the element cqw measures. Both are bleed sections
     with no padding, so 100cqw is the full viewport width -- on a padded box
     it would be the content width and every number would come out short. */
  .sof-head,.sof-hero{--u:1px}

  /* 1 · header */
  /* Capped contents, bleeding band: padding, not max-width, because these
     elements carry their own background. Inert below 1400, and inside the
     1024-1919 zoom the 1400 is DESIGN pixels, so it holds its proportion. */
  /* 58px flat, the height it already had on a phone and the one that read
     right. The design's 144 is a 1920-frame number and only made sense while
     the header was being scaled down with the page; unscaled it rendered
     77-108px across the desktop range, which Topi called massive. */
  .sof-nav{height:58px}
  .sof-nav-m,.sof-menu,.sof-menu-cb:checked ~ .sof-menu{display:none}
  .sof-nav-d{display:flex;width:100%;
    padding:0 max(0px,calc((100% - 1400px)/2))}
  .sof-nav-d .sof-navcell{font-size:18px;letter-spacing:0}
  .sof-nav-d .sof-navcell--rule{border-right-width:2px}
  /* measured cell widths 348 / 416 / 322 / 435 / 399 of 1920 */
  .sof-nav-d .sof-navcell:nth-child(1){flex:348 0 0}
  .sof-nav-d .sof-navcell:nth-child(2){flex:416 0 0}
  .sof-nav-d .sof-navcell:nth-child(3){flex:322 0 0}
  .sof-nav-d .sof-navcell:nth-child(4){flex:435 0 0}
  .sof-nav-d .sof-navcell:nth-child(5){flex:399 0 0}

  /* 2 · hero — desktop paints art -> shade -> wash (mobile flips the top two)

     EVERY length below is `N * var(--u)`, where --u is one DESIGN pixel. At
     1920 it is exactly 1px and this block is the frame verbatim, unchanged.
     Below 1920 it shrinks, and the whole hero -- art, lockup, button, the
     host names and the blurred plate behind them -- scales together.

     WHY, because "fix the container, never the type" says otherwise and this
     is the documented exception. The hero is a 1920-wide COMPOSITION: three
     men arranged across the right of the artwork, each with his name under
     him, beside a 672px text column. object-fit:cover in a shorter box crops
     the sides, and at 1200 that removed Topi completely while the names --
     separately positioned, so they did not move -- carried on pointing at
     where he used to be. "TOPI HEINONEN" labelled empty sky.

     No anchor fixes that. Measured at 1200: centre loses Topi, `right` loses
     Ryan and Nick behind the lockup, 78% still loses Ryan. 1200px of a 1920
     composition minus a 672 text column leaves room for one man. The only way
     to keep all three is to stop cropping and scale, which is what this does.

     It also makes baking the names into the artwork unnecessary: they scale
     with the art, so they stay under their man at every width, and they stay
     real selectable text rather than pixels. */
  .sof-hero-m{display:none}
  .sof-hero-d{display:block;position:relative;z-index:3;
    min-height:calc(1088 * var(--u));
    padding:calc(118 * var(--u)) calc(120 * var(--u)) 0}
  .sof-hero-wash{z-index:2;background:linear-gradient(90deg,
    #FCECC7F2 0%,#FCECC7E5 30%,#FCECC773 44%,#FCECC700 56%)}
  .sof-hero-shade{z-index:1;height:calc(288 * var(--u))}
  .sof-hero-col{width:100%;max-width:calc(760 * var(--u))}
  .sof-date{font-size:calc(36 * var(--u));max-width:calc(760 * var(--u));
    margin-left:calc(-44 * var(--u))}
  /* render 696.67 wide vs a 672.39 node box -> 12.14 of stroke bleed each side */
  .sof-lockup{width:calc(696.67 * var(--u));
    margin:calc(-9 * var(--u)) 0 0 calc(-12.14 * var(--u))}
  .sof-tag{max-width:calc(672 * var(--u));height:calc(72 * var(--u));
    border-radius:calc(37.5 * var(--u));border-width:calc(4 * var(--u));
    margin:calc(-36 * var(--u)) 0 0;
    box-shadow:0 calc(6 * var(--u)) calc(14 * var(--u)) #0000004D}
  .sof-tag span{font-size:calc(24.543 * var(--u));letter-spacing:calc(3.8 * var(--u))}
  .sof-cta{max-width:calc(672 * var(--u));height:calc(120 * var(--u));
    margin-top:calc(48 * var(--u))}
  .sof-cta i{top:calc(8 * var(--u));height:calc(112 * var(--u));
    border-radius:calc(56 * var(--u))}
  .sof-cta span{height:calc(112 * var(--u));border-radius:calc(56 * var(--u));
    border-width:calc(6 * var(--u));font-size:calc(54 * var(--u))}
  .sof-pow{max-width:calc(576 * var(--u));height:calc(80 * var(--u));
    margin:calc(40 * var(--u)) 0 0;gap:calc(15 * var(--u));justify-content:flex-start}
  .sof-pow b{font-size:calc(18 * var(--u))}
  .sof-pow img{width:calc(448 * var(--u));height:calc(80 * var(--u));margin-left:0}
  .sof-hosts{position:absolute;right:0;bottom:calc(16 * var(--u));
    width:calc(1064 * var(--u));max-width:100%;margin:0;
    padding:calc(16 * var(--u)) calc(43 * var(--u)) calc(16 * var(--u)) calc(16 * var(--u));
    z-index:4}
  .sof-hosts span{font-size:calc(41 * var(--u));letter-spacing:calc(-0.2 * var(--u));
    line-height:calc(49 * var(--u))}
  .sof-hero-shadeblur{position:absolute;right:calc(-64 * var(--u));
    top:calc(944 * var(--u));width:calc(1104 * var(--u));height:calc(192 * var(--u));
    border-radius:calc(95 * var(--u));background:#061A2C99;
    filter:blur(calc(60 * var(--u)));z-index:3;display:block}

}

@supports (container-type: inline-size) {
  @media (min-width:768px) and (max-width:1919px){
    .sof-head,.sof-hero{container-type:inline-size}
    .sof-head,.sof-hero{--u:calc(100cqw / 1920)}
  }
}

/* ======================================================================== */
/* THE DESKTOP DESIGN, SCALED — 1024 and up.                                */
/*                                                                          */
/* Every length in the block below is a 1920-frame pixel. Between 1024 and  */
/* 1919 the section is zoomed by (available width / 1920), which makes one  */
/* CSS px inside it exactly one design px, so the frame arrives whole at    */
/* any laptop width instead of being re-fitted per breakpoint. At 1920 the  */
/* zoom rule does not match and the numbers below are literal.              */
/*                                                                          */
/* cqw, not vw: vw counts the scrollbar and would zoom ~1.5% too big, which */
/* is a horizontal scrollbar at every width.                                */
/* ======================================================================== */
.sof-scale{container-type:inline-size}
/* THE 1400 CAP, and the zoom that carries it.

   The 1920 design is scaled to fit the viewport, with a CEILING of 1400 on
   the numerator: below 1400 of viewport the design fills the screen exactly
   as it always did, and from 1400 up the scale stops growing.

   The ceiling alone caps everything in the subtree, backgrounds included,
   which is not wanted. So the section keeps width:100% -- under the zoom
   that resolves to viewport / zoom design px and renders the full viewport,
   so the band bleeds -- and `.sof-cap` inside it is pinned to the design's
   own 1920, which the zoom lands on exactly 1400.

   The gutters live on the wrapper, not the section. At 1440 the section is
   1975 design px wide and 120 each side would leave 1735, narrower than the
   wrapper's 1920, so the wrapper would overflow and clip. */
@media (min-width:1024px){
  .sof-scale > .sof-sec{zoom:calc(min(100cqw, 1400px) / 1920px);
    padding-left:0;padding-right:0}
  .sof-cap{width:1920px;margin-left:auto;margin-right:auto;
    padding-left:120px;padding-right:120px}
  .sof-sec--bleed > .sof-cap{padding-left:0;padding-right:0}
  /* The header paints its bands on .sof-promo and .sof-nav, not on the
     section, so a 1400 wrapper would cap those backgrounds. Full-width
     wrapper here; the contents are capped by the 1400 padding those two
     already carry. */
  .sof-head > .sof-cap{width:100%;padding-left:0;padding-right:0}
  /* The hero runs to the screen edge again, on its own. Every other section
     keeps the 1400 cap; this one was drawn as a full-bleed plate and the cap
     put cream down both sides of it. */
  .sof-hero > .sof-cap{width:100%;padding-left:0;padding-right:0}
  /* The marquee is 5151px and was clipped by the section. The wrapper has to
     clip it now, or the words run past 1400 to the screen edge. */
  /* 1704, not 1680: three 552 cards and two 24 gaps. The frame fits it by
     taking 24 off this one section's right gutter. */
  .sof-formats > .sof-cap{padding-right:96px}
}

/* ======================================================================== */
/* DESKTOP — frame 918:77, 1920 wide. Every value below is measured off     */
/* that frame; nothing here is a scaled-up guess at the mobile numbers.      */
/* ======================================================================== */
@media (min-width:1024px){
  .sof-sec{padding-left:120px;padding-right:120px}
  .sof-h1 .a{font-size:204.74px}
  .sof-h1 .b{font-size:85.55px}
  .sof-h1 .c{font-size:200px}

  /* 9c · who it's for — 904:551 verbatim: 2 x 816 + 48 = 1680. */
  .sof-who{padding-top:120px;padding-bottom:120px}
  .sof-who .sof-art{max-width:1321px;margin-top:28px}
  .sof-wgrid{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));
    align-items:start;gap:48px;margin-top:36px}
  .sof-wcard{gap:24px;padding:52px 56px;border-radius:28px}
  .sof-whead{font-size:72px}
  .sof-wrow{gap:18px;font-size:26px}
  .sof-wrow i{flex-basis:32px;width:32px;height:32px;font-size:18px;margin-top:2px}
  .sof-wcta{font-size:45.9px;padding:20px 38px;margin-top:36px}

  /* 9d · faq — 904:624, list is 1200 of the 1680 column. */
  .sof-faq{padding-top:120px;padding-bottom:120px}
  .sof-faq .sof-art{max-width:1323px;margin-top:28px}
  .sof-faqlist{gap:16px;margin-top:36px}
  .sof-faqq{font-size:38px;padding:26px 32px}
  .sof-faqq::after{flex-basis:48px;width:48px;height:48px;font-size:30px}
  .sof-faqa{font-size:21px;padding:0 32px 30px}
  .sof-faqtail{font-size:20px;margin-top:28px}

  /* 4 · speakers type at the frame's own sizes */
  /* 28, measured off every name node in the speaker grid. One size now that
     the names are uppercase -- see the note on SPEAKERS_V2.

     max-width is how the frame builds the two boxes differently: the NAME is a
     fixed 288-wide box with textAutoResize HEIGHT, so a long one wraps inside
     it, while the ROLE hugs its own text. "GONZALO MARTIN" is 288 wide and
     wraps to two lines in the frame; the card foot gives 289.6 here, so
     without this it sat on one. Capping the name alone keeps the role's full
     measure, which is what stops "Performance Creative Queen" wrapping. */
  .sof-spk-name{font-size:28px;max-width:288px}
  .sof-spk-role{font-size:22px;margin-top:6px}

  /* 6b · mission map — frame 904:452 verbatim at 1920. */
  .sof-mission{padding-top:120px;padding-bottom:120px}
  .sof-meyebrow{gap:20px}
  .sof-meyebrow i{flex-basis:170px}
  .sof-meyebrow span{font-size:26px;letter-spacing:.1em}
  .sof-mission .sof-art{max-width:1148px;margin-top:28px}
  .sof-mission-intro{font-size:24px;max-width:960px;margin-top:28px}
  /* 3 x 528 + 2 x 48 = 1680, the content column exactly. */
  /* stretch, not start: the frame draws all three day cards at 528x616, the
     same height, however much is in them -- Day 2 has four slots, Day 3 has
     two and a button. align-items:start let each one hug its content and the
     row came out ragged. */
  .sof-days{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));
    align-items:stretch;gap:48px;margin-top:28px}
  .sof-day{min-width:0;gap:20px;padding:40px;border-radius:24px}
  .sof-daychip{font-size:20px;padding:8px 18px}
  .sof-day-h{font-size:48px}
  .sof-slot{padding:18px 0}
  .sof-slot-h{font-size:32px}
  .sof-slot-d{font-size:17px;margin-top:6px}
  /* 34 tall is 181 wide, so the plate is 215 against the 232 the row
     leaves. Border and radius step up with the card's, as the chip's do. */
  .sof-slot--bf{gap:16px}
  .sof-bfplate{border-width:3px;border-radius:16px;padding:10px 14px}
  .sof-slot-bf{height:34px}
  .sof-mission-note{font-size:18px;margin-top:28px}

  /* 2b · ticker — the 904:148 band verbatim: 104 tall, 6px rules, 52px type,
     34px stars, 36px gaps. The 22s base duration would crawl over a sequence
     this much wider, so it scales with it. */
  /* 2b · sponsor logo marquee — the 1440 frame's values x 4/3 */
  .sof-marqbar{padding:53px 0;border-bottom-width:4px}
  .sof-marqbar > .sof-cap{gap:29px}
        .sof-marq-seq{gap:117px;padding-right:117px}
  .sof-marq-logo--bf{width:479px;height:74px}
  .sof-marq-logo--suits{width:215px;height:59px}
  .sof-marq-logo--oc{width:272px;height:50px}
  .sof-marq-logo--taza{width:241px;height:56px}
  .sof-marq-logo--s{width:121.037px;height:41.8px}
  .sof-marq-logo--whop{width:214px;height:47px}
  .sof-marq-track{animation-duration:36.2s}
  .sof-marq-win{-webkit-mask-image:linear-gradient(90deg,transparent 0,
      #000 267px,#000 calc(100% - 267px),transparent 100%);
    mask-image:linear-gradient(90deg,transparent 0,
      #000 267px,#000 calc(100% - 267px),transparent 100%)}

  /* 3 · stats */
  .sof-stats{background:#041C32;border-top-width:2px;border-bottom-width:2px}
  /* 79, not the design's 160. The two dividers are flex items, so the row
     is stat 272 + gap + rule 2 + gap, four times over. 2*79 + 2 = 160 puts
     each rule centred in the design's gap and lands the three blocks on
     the frame's x=392 / 824 / 1256. At 160 the row measured 1460 instead
     of 1136 and 300+ sat 162px too far left. */
  .sof-stats-row{gap:79px;padding:46px 0}
  .sof-stat{width:272px;height:176px;padding-top:24px}
  .sof-stat .sof-num{height:75.5px}
  .sof-stat .sof-lab{height:30px;margin-top:20.5px}
  .sof-statdiv{width:2px;height:128px;flex:0 0 2px;background:#FBEFD659}

  /* 4 · speakers */
  .sof-speakers{padding-top:120px;padding-bottom:120px}
  .sof-speakers .sof-art{max-width:961px;margin:0 auto}
  /* Two layers, as 923:1776 stacks them: the grid's navy fill, then the
     cream-at-50% grid lines over it. Half cream over navy is the blue-grey the
     design draws; half cream over the section's cream -- which is what this
     was doing -- is near-white.

     outline, not border: the 6px stroke is aligned OUTSIDE in the frame, and a
     border would take 12px out of the 1680 column and shrink every card. */
  /* FOUR across, not the frame's five: twelve speakers in 4 x 3, per
     ClickUp z941abzgdq. The cards come out 417 wide against the frame's 336
     and the photo's 336/328 ratio scales with them. design_diff will flag
     the grid until the frame is updated to match. */
  .sof-grid{grid-template-columns:repeat(4,minmax(0,1fr));gap:4px 3px;
    outline-width:6px;margin-top:64px}
  .sof-card{min-height:432px}
  .sof-photo{aspect-ratio:336/328;border-bottom-color:#FBEFD659}
  .sof-photo b{font-size:16px;letter-spacing:3px;color:#FBEFD666}
  .sof-photo em{font-size:150px;color:#FBEFD62E}
  /* 22, where the frame measures 24. The frame's cards sit flush at 336 and
     this build separates them with a 3px grid gap instead, which costs each
     card 2.4px. At 24 the longest role, "Performance Creative Queen" at 287px,
     was 1.4px over its 285.6px measure and wrapped to a second line -- the
     frame has it on one. Giving the two padding pixels back is invisible and
     fixes the container rather than the type. */
  /* 17 of padding-bottom, measured off the one card in the frame whose name
     wraps: Gonzalo's (921:1357) is 452 tall with the role's box ending at 435.
     Every other card has 28px under its role for free, because min-height:432
     is more than its content needs -- but Gonzalo's two-line name fills the
     card exactly, so with padding-bottom:0 his role sat ON the bottom edge
     while the fourteen around it had 28. A card must not depend on having
     slack it may not have. */
  .sof-card-foot{padding:14px 22px 17px}
  .sof-name{height:25.8px}
  .sof-co{font-size:22px;margin-top:6px}

  /* 5 · formats — the design's own arithmetic puts the third 552px card at
     x=1824, so this one section's right gutter is 96, not 120. As drawn. */

  /* Portrait beside the copy once there is room for both.
     260 wide against a 380 floor, not 300 in an 880 box: the box's height is
     set by the copy, so a wide box made a SHORT box, and the portrait got
     cropped to a letterbox strip. Narrowing the dialog to 720 puts the copy
     at roughly 46 characters a line instead of 60, which is both a better
     measure to read and tall enough for the portrait to read as one. */
  .sof-spk-doc{grid-template-columns:260px minmax(0,1fr);min-height:380px}
  /* max-height:none, or the 25vh phone cap keeps applying and the portrait
     stops short of the column it is supposed to fill. */
  .sof-spk-figure{height:100%;max-height:none;object-fit:cover}
  .sof-spk-copy{padding:36px}
  .sof-spk-modal-name{font-size:44px}
  .sof-spk-bio p{font-size:17px}
  .sof-spk-i{width:26px;height:26px;font-size:15px;margin-left:10px}
  /* Measured 1.5 design px high at this size; 1px of nudge lands it on centre
     (dy -0.04 of a design pixel). On the span, so the disc stays a circle. */
  .sof-spk-i span{position:relative;top:1px}
  .sof-formats{padding-top:120px;padding-bottom:120px}
  .sof-formats .sof-in{max-width:1704px}
  .sof-eyebrow{gap:21px}
  .sof-eyebrow b{font-size:26px}
  .sof-eyebrow i{height:3px;width:224px;flex:0 1 224px}
  .sof-t-d{display:block}
  .sof-t-m{display:none}
  .sof-ftitle{margin-top:29.44px}
  .sof-ftitle .sof-art{max-width:1522.33px}
  .sof-subline{font-size:34px;letter-spacing:.01em;line-height:1.2;margin-top:34.47px}
  .sof-fcards{grid-template-columns:repeat(3,minmax(0,1fr));gap:24px;margin-top:31px}
  .sof-fcard{border-width:3px;border-radius:24px;min-height:664px}
  .sof-fcard-img{aspect-ratio:552/320}
  .sof-fcard-img i{height:8px}
  .sof-fcard-body{padding:32px}
  .sof-fkick{font-size:20px}
  .sof-fhead{font-size:46px;letter-spacing:.01em;margin-top:16px}
  .sof-fbody{font-size:20px;letter-spacing:-0.003em;margin-top:16px}

  /* 6 · you decide */
  /* The padding moved from the SECTION to the cap on 2026-10-22. On the
     section it inset .sof-cap, and the lizard plate is positioned against
     the cap, so the artwork was inset with it and a band of paper texture
     showed above and below it.

     On the cap the band runs flush: an absolutely positioned child resolves
     against its ancestor's PADDING box, so .sof-decide-bg (top:0;height:100%)
     still fills the cap edge to edge while the copy keeps its 135 offset.
     min-height comes along, or the cap would collapse to the copy's height
     and leave texture under it. */
  /* Full width, so the plate can reach the right-hand edge. */
  .sof-decide > .sof-cap{width:100%;padding:135px 120px;min-height:1168px}
  .sof-decide-bg{top:0;height:100%}
  /* No wash. The plate's own left edge is faded instead -- see the mask on
     .sof-decide-bg. A wash is a second box laid over the art and has to be
     kept in register with it; a mask is the art's own edge and cannot drift. */
  .sof-decide-wash{display:none}
  /* Bleeds RIGHT, dissolves LEFT. The plate runs to the right-hand edge of
     the screen, and its left edge fades out so there is no seam where the
     artwork meets the cream and the copy keeps a clean ground.
     Opaque by 46%: the longest line of copy ends at 41-45% of the band at
     every desktop width, so the text is always over the transparent part. */
  /* Anchored RIGHT at 87 per cent of the band. Joshua, 2026-10-23: zoom is
     acceptable, overlap is not.

     Solved, not guessed. The car's leading edge sits 41 per cent into the
     plate, so right-anchored at width W it lands at viewport - 0.59W, and
     the longest line of copy ends at 41-46 per cent of the viewport. Setting
     W to 87 per cent of the band makes both sides grow at nearly the same
     rate, so the clearance is almost constant instead of opening up:

        vw      plate        car    copy ends   clearance
       1024    891 (0.64x)    498      415         +83
       1440   1253 (0.89x)    701      588        +113
       1920   1670 (1.19x)    934      828        +106
       2560   2227 (1.59x)   1246     1148         +98
       3440   2993 (2.14x)   1674     1588         +86

     The car is drawn larger on a wide screen -- 1.6x at 2560 -- which is the
     trade accepted here. The alternatives were measured and both were worse:
     width:100 per cent puts the car at 41 per cent of the viewport, straight
     into the copy, and a fixed width leaves 550px of empty cream in the
     middle at 2560. The frame itself has only 6px of clearance, so some
     deviation from it is unavoidable either way. */
  .sof-decide-bg{left:auto;right:0;width:87%;max-width:none;transform:none;
    -webkit-mask-image:linear-gradient(90deg,transparent 0,#000 46%);
            mask-image:linear-gradient(90deg,transparent 0,#000 46%)}
  .sof-kicker{font-size:37px}
  /* Group 10's node box starts at x=-59.91, outside the frame, and the section
     clips it. The export is the VISIBLE 927.67px, so it hangs off the content
     column's left edge by exactly the 120px gutter. */
  .sof-decide-art{width:min(927.67px,calc(100% + 120px));
    margin:-21px 0 0 -120px}
  .sof-decide-body{font-size:29px;line-height:40px;letter-spacing:-0.005em;
    max-width:700px}
  .sof-decide-intro{margin-top:25.33px}
  .sof-decide-promise{margin-top:23px}
  .sof-only-d{display:block}
  .sof-only-m{display:none}

  /* 7 · topics */
  .sof-topics{background-color:#041C32;padding-top:116px;padding-bottom:134px}
  .sof-topics .sof-art{max-width:1550.67px;margin:0 auto}
  /* The node box is 1245 and this line measures 1246 in Chrome at the node's
     own 41px / 2.2px tracking -- one pixel over, so it wrapped to two lines.
     The fix is the container, never the type: the box goes to 1280 (still well
     inside the 1680 column) and the line stays single, as drawn. */
  .sof-subtitle{font-size:41px;line-height:100%;letter-spacing:2.2px;max-width:1280px;
    margin-top:49.21px}
  .sof-chips{grid-template-columns:repeat(4,minmax(0,1fr));gap:23.64px 16px;
    margin-top:31.77px}
  .sof-chip{background:#041C32;border-width:2.6px;border-radius:16px;
    padding:10.93px;aspect-ratio:408/133.985}
  .sof-chip-panel{border-radius:6px;background-size:1024px 1024px}
  .sof-chip-tab{width:59.19px;height:51.22px}
  .sof-chip-label{font-size:58.6px}

  /* 8 · tickets */
  .sof-tickets{padding-top:120px;padding-bottom:120px}
  /* 918:572 is 702 wide at the 1920 frame. This read 1129.67 from V2's
     "Get your ticket today" lockup and was never updated when V3 changed the
     heading, which is why it shipped 61% oversized. */
  .sof-ttitle .sof-art{max-width:702px}
  .sof-teyebrow{gap:20px}
  .sof-teyebrow i{flex:0 1 96px;min-width:0;width:96px;height:3px}
  .sof-teyebrow b{font-size:26px}
  .sof-ttitle{margin-top:28px}
  .sof-tdate{font-size:31.03px;letter-spacing:.04em;margin-top:1px}
  /* SIDE BY SIDE ONLY WHERE THE CARD IS WIDE ENOUGH FOR THE DESIGN'S TYPE.
     Measured at 1920: the Early Bird button label sets 602px at 54px, and the
     badge row sets 666px. A card has 48px of padding each side and a 4px
     border, so a two-up row needs 2x(602+104)+48 = 1460px of content column --
     i.e. a 1700px viewport at the design's 120px gutters -- gated at 1760 so
     the narrowest two-up card still has ~30px of slack rather than nought.
     Below that the two columns starve the only place on the page that asks
     for money: at 1440 the label overran its button by 65px and "PRICE
     INCREASES ANY DAY!" was cut to "PRICE INCREAS". Fix the container, never
     the type.
     Stacked, the card keeps the 816px width the design gives it at 1920 and
     centres, rather than stretching to a 1200px box the type was never drawn
     for -- so the card's inner measure is identical to the design's. */
  /* The card stays a column: it is .sof-ttop that becomes the row. 1200 wide
     and centred, which is what x=360 in a 1920 frame comes to. */
  /* 1440-frame values x 4/3. See the ticket-card note: above 1024 every px
     here is a 1920 design px that the zoom scales back down. */
  .sof-tbanner{height:72px;gap:18px}
  .sof-tbanner b{font-size:36px;line-height:43px}
  .sof-tcheck{width:36px;height:36px;border-radius:8px}
  .sof-tcheck svg{width:18px;height:13px}
  /* padding-top clears the 72px banner (94.17 x 4/3); the bottom lip is
     the frame's 10.97 x 4/3 against 2.74 x 4/3 on the other three sides.
     These live here, not in a rule above, because this one sets `padding`
     and `border-bottom-width` and would override anything earlier. */
  .sof-tcard{width:1200px;max-width:100%;
    margin:34px auto 0;border-width:3.66px;border-bottom-width:14.63px;
    border-radius:28px;min-height:640px;padding:125.56px 56px 56px}
  /* Same grid, different areas: there is room for the pills beside the mark
     here, so they take the left column with the name and the price instead
     of a row of their own. 1088 of inner measure less the 360 column leaves
     728 on the left, which is the measure the type was drawn for. */
  .sof-ttop{grid-template-columns:minmax(0,1fr) 360px;
    grid-template-areas:"badges mark" "name mark" "price mark";
    column-gap:0}
  /* Top aligned, so the badge starts level with the promo pills opposite it
     as the reference draws it. The column is 360 against a 290 badge; at 330
     the badge was squeezed to 283 wide against 290 tall and the coin came out
     slightly oval, which nothing but a measurement catches. */
  .sof-tmark{align-self:start}
  /* max-width:none, or the base 160 cap clamps it. */
  .sof-sticker{width:290px;height:290px;max-width:none}
  /* The badge row is the one row that can legitimately become two: both badges
     keep their drawn size and the second drops under the first. At 1920 the
     card is 712 wide against a 666 row, so it stays on one line as drawn. */
  .sof-badges{flex-direction:row;align-items:center;gap:16px;flex-wrap:wrap}
  .sof-badge{height:44px;border-radius:22px;padding:0 46px;font-size:20px}
  .sof-badge--urgent{padding:0 24px;border-width:3px}
  .sof-tname{font-size:88px;margin-top:20px}
  .sof-tpricerow{gap:28px;margin-top:8px}
  .sof-tprice{font-size:88px;
    text-shadow:
      -6px -6px 0 #0c0f0a,  6px -6px 0 #0c0f0a,
      -6px  6px 0 #0c0f0a,  6px  6px 0 #0c0f0a,
       0   -6px 0 #0c0f0a,  0    6px 0 #0c0f0a,
      -6px  0   0 #0c0f0a,  6px  0   0 #0c0f0a,
      12px 12px 0 #0c0f0a}
  .sof-tcompare{font-size:56px}
  .sof-tcompare::after{height:5px;border-radius:3px}
  /* TWO columns on desktop: the frame puts the dots at x=56 and 426 of a
     1200 card, which is a 2-up grid of the 728 body measure. */
  /* The list is a card child now, so it runs the full 1088 rather than the
     728 body measure plus a 40px negative margin. Both columns stay left
     aligned at 0 and 370, so no bullet moves -- only the second column's
     unused right-hand slack changes. */
  .sof-tlist{display:grid;grid-template-columns:370px minmax(0,1fr);
    column-gap:0;row-gap:15px;margin:40px 0 0}
  .sof-tlist li{font-size:24px;padding-left:28px;margin-top:0}
  .sof-tlist li::before{width:12px;height:12px;top:9px}
  /* No max-width and no margin-top:auto any more. The button is the card's
     own child, so it runs the full 1200 less the card's 56 padding = 1088. */
  .sof-tbtn{height:112px;margin:40px 0 0}
  .sof-tbtn i{top:8px;height:104px;border-radius:52px}
  .sof-tbtn span{height:104px;border-radius:52px;border-width:6px;font-size:54px;
    letter-spacing:.01em}
  .sof-tsplit{font-size:20px;margin-top:20px}

  /* 9 · sponsor — the 1440 frame's values x 4/3. The eyebrow stays 26:
     19 x 4/3 is 25.33, which after the zoom differs by a quarter pixel. */
  .sof-sponsor{padding-top:120px;padding-bottom:120px}
  .sof-partner{font-size:26px}
  .sof-sponsor-rule{width:93px;margin-top:16px}
  .sof-powered{font-size:93px;margin-top:29px}
  .sof-plate{max-width:1013px;height:267px;border-radius:32px;border-width:2px;
    margin-top:107px}
  .sof-plate .sof-plate-logo{width:747px;height:115px}
  .sof-tier{margin-top:96px}
  .sof-tplate{border-radius:32px;border-width:2px}
  .sof-tplate--oc{width:480px;height:165px}
  .sof-tplate--oc svg{width:384px;height:70px}
  .sof-tplate--taza{width:333px;height:115px}
  .sof-tplate--taza svg{width:237px;height:55px}
  /* 944 x 4/3 = 1259 (3 plates of 400 + 2 gaps of 29), the Gold tier's own
     width -- not the Diamond plate's 1013, which this row no longer shares
     with Outcraft or Tazapay now that those are their own solo tiers. */
  .sof-sponsors{gap:29px;margin-top:96px;max-width:1259px}
  .sof-splate{height:139px;border-radius:32px;border-width:2px}
  .sof-splate--suits svg{width:304px;height:83px}
  .sof-splate--whop svg{width:304px;height:67px}
  .sof-splate--s svg{width:247.094px;height:85.333px}

  /* 10 · footer — type only. The single ROW the design draws needs 971px of
     content column (brand + five nav links + the nowrap copyright, measured),
     which a 120px-guttered page does not have until 1280. It is gated below;
     until then the footer keeps the mobile stack, which is what it is for. */
  .sof-footer{padding-top:64px;padding-bottom:64px}
  .sof-fbrand{font-size:32px}
  .sof-fdate{font-size:14px;margin-top:8px}
  .sof-fnav a{font-size:20px}
  .sof-fcopy{font-size:16px}
}

/* The design's footer row, once the column is wide enough to hold it. Every
   item in the row is a single line in the design, so they are nowrap here and
   the gate is the width at which all four fit side by side -- below it the
   row wrapped "SCALING OR / FAILING" and "GET / TICKET" onto two lines. */
@media (min-width:1024px){
  .sof-footer-in{flex-direction:row;align-items:flex-start;justify-content:space-between}
  .sof-fbrand,.sof-fdate,.sof-fnav a{white-space:nowrap}
  .sof-fnav{flex-direction:row;align-items:center;justify-content:center;gap:40px;
    margin-top:8px;flex:1}
  .sof-fcopy{margin-top:8px;text-align:right;white-space:nowrap}
}

/* The "You Decide" artwork is one image with its own cream fade painted into
   its left third, and at 1920 that fade is exactly what the body copy sits on.
   Below 1920 `object-fit:cover` scales the plate to the section height and
   crops it horizontally, which walks that fade off the copy column and leaves
   navy #041c32 text on the bright yellow car -- at 1440 "countless",
   "seven-figure days.", "private." and "big time." were substantially lost.
   This scrim continues the artwork's own fade over the copy column wherever
   the crop has taken it away. At the design's native width it is not rendered
   at all, so 1920 is untouched. */
/* removed: the You Decide wash -- the artwork no longer crops, so there is nothing to fade over */


/* TOPIC CHIPS BETWEEN 1200 AND 1649 — the one place the "fix the container,
   never the type" rule has no container left to fix.
   The chip grid is 4 columns of the content column, so the panel a label sits
   in is a linear function of the viewport, measured not assumed:
       panel(W) = 0.25W - 98      (202 at 1200, 302 at 1600, 382 at 1920)
   The label is `white-space:nowrap` under `overflow:hidden` and CENTRED, so it
   loses characters at BOTH ends. ADVERTORIALS sets 316.5px at the design's
   58.6px, which needs panel >= 316.5 -- i.e. W >= 1658. Below that, 8 of the
   12 chips were cut at 1200 and four stopped reading as words: ADVERTORIALS
   rendered "VERTORIA", TIKTOK SHOPS "KTOK SHO", NATIVE ADS "ATIVE AD",
   OPERATIONS "PERATION".
   There is no Figma frame between 390 and 1920, so the design says nothing
   about these widths; making the labels readable here implements the design
   rather than departing from it. The grid stays 4-up and the labels stay on
   one nowrap line -- only the size is fluid:
       font(W) = 0.96 x 58.6/316.5 x panel(W) = 4.4436vw - 17.42px
   i.e. the largest size at which the widest label still fits its panel, times
   a 4% margin so a sub-pixel rounding or a scrollbar-narrowed column cannot
   put it back over the edge. 35.90px at 1200, 55.85px at 1649.
   GATED BOTH WAYS ON PURPOSE. 1920 and 390 are the two design-diff viewports
   and both currently score zero size deltas, so this rule must not reach
   either: the media query floors it at 1200 (below that the mobile frame's
   24.45px rule owns the chips) and caps it at 1649, and the min() is a second
   belt that can never resolve above the design's own 58.6px whatever `vw`
   reports. Declared after the >=1200 block so source order wins -- a media
   query adds no specificity. */
/* removed: the 1200-1657 chip-label rule -- chips sit at design size under the zoom now */


/* removed: the two-up ticket row and the equal-height min-height. The
   2026-10-21 frame has one ticket, so there is no second card to sit
   beside or line up with. The @media wrapper went with them.  */

/* Full-bleed bands: the header, the hero plate and the navy stats strip run
   edge to edge at every width, so they opt out of the page gutter. Declared
   LAST so it beats the gutter rule inside the desktop media block (a media
   query adds no specificity -- only source order decides). */
.sof-sec--bleed{padding-left:0;padding-right:0}

/* ===================== CAP AT THE 1920 DESIGN FRAME =====================
   Added 2026-10-08 after the page was seen on a monitor wider than the frame.
   Everything that measures off .sof-in already stopped at 1680 and centred, so
   the body of the page was fine. The three sections that opt OUT of the gutter
   (.sof-sec--bleed) did not: their CONTENT kept growing with the viewport.

   At 2560 that put the nav's five cells -- which carry the design's own
   348/416/322/435/399 proportions of 1920 -- across 2560 instead, and the hero
   is worse than stretched: .sof-hero-plate is object-fit:cover, so a wider box
   does not squash the artwork, it scales it up and crops the top and bottom
   away. The three men got bigger and the skyline above them was cut off, while
   the lockup beside them stayed 120px from the viewport edge instead of 120px
   from the frame. Nothing overflowed and nothing looked broken in isolation --
   it read as "strange" because the capped body and the uncapped bands
   disagreed about how wide the page was.

   What is capped is the CONTENT; the colour bands still run edge to edge,
   which is the normal way to do this and avoids a boxed-in page. The hero's
   gutters land on .sof-hero's own #FCECC7, which is the cream the artwork
   fades into anyway, so the join is invisible.

   Gated at 1921 so every width the design was verified at -- 1920 and below,
   including both design_diff viewports -- is byte-identical to before. */
@media (min-width:1921px){
  /* The nav is ONE element -- <nav class="sof-nav sof-nav-d"> -- so it carries
     both the navy band and the five cells. Capping its WIDTH boxed the band and
     put cream down both sides, which looked more broken than the stretch did.
     Padding it inward instead keeps the band edge to edge (matching the promo
     bar above it) while the cells lay out across the design's 1920, which is
     what their 348/416/322/435/399 flex bases are proportions of.
     box-sizing:border-box (line ~373) is what makes width:100% + padding land
     the content box on exactly the figure below.

     box-sizing:border-box (line ~373) is what makes width:100% + padding land
     the content box on exactly the figure below -- 1400 since 2026-10-22, to
     match the .sof-promo above it and the .sof-in below. The band itself
     still bleeds; only the cells are pulled in. */
  .sof-nav-d{padding-left:max(0px,calc((100% - 1400px)/2));
             padding-right:max(0px,calc((100% - 1400px)/2))}
  .sof-hero-d{max-width:1920px;margin-left:auto;margin-right:auto}
  /* These three are absolutely positioned against .sof-hero, not against
     .sof-hero-d, so auto margins cannot reach them -- they need re-anchoring.
     max-width:none undoes the global `.sof :where(img){max-width:100%}`. */
  /* The hero is full bleed again, so its plates fill the band rather than
     stopping at the design's 1920 -- pinned there they rendered 1400 wide in
     a 2560 band and put the cream back down both sides.

     .sof-decide-bg is NOT in that list: You Decide still caps with the rest
     of the page, so its plate keeps the 1920 treatment. */
  .sof-hero-plate,.sof-hero-wash,.sof-hero-shade{
    left:0;right:0;width:100%;max-width:none;transform:none}
  /* Above 1920 the base rule's growth formula already holds. */
}

/* ⚠️ EVERY full-bleed plate on this page belongs in the rule above. There are
   two: the hero's and .sof-decide-bg, the lizard. The second was missed on the
   first pass because .sof-decide is NOT one of the three sof-sec--bleed
   sections -- it takes the normal gutter, and only its ARTWORK bleeds, so
   looking at the bleed sections did not find it. At 2560 it was a 1920x1080
   file in a 2560 box, upscaled 33% and cropped by object-fit:cover, exactly
   the hero's failure.

   The check that finds these is natural width vs rendered width, not which
   section they sit in:

       document.querySelectorAll('img')  ->  rect.width >= innerWidth
                                         ->  compare naturalWidth

   Its wash needs no entry: .sof-decide-wash is display:none from 1920 up
   (set in the 1200-1919 block), so above the cap there is nothing to anchor.
   The paper and dark textures need no entry either -- they are `repeat` at a
   fixed background-size, so they tile instead of scaling. */

/* ===================== LEGAL POPUP (Terms / Privacy) =====================
   Opened from the two words in the footer copy line, which the design draws as
   plain text and which had no destination at all until now.

   NO JAVASCRIPT. Three radios sharing one name drive it, exactly the mechanism
   the burger menu already uses (.sof-menu-cb): `off` is checked at load, and
   the two labels in the footer check `terms` or `privacy`, which both reveals
   the dialog and selects which document shows. The close button and the scrim
   are labels pointing back at `off`. One radio group gives open/closed AND the
   tab state in a single mechanism, which a checkbox pair cannot.

   `data-lenis-prevent` on the scrolling panel is load-bearing: Lenis takes the
   wheel over the whole document, so without it a scroll inside the dialog
   scrolls the PAGE behind it. The funnel's header CSS already ships the
   matching `html.lenis [data-lenis-prevent]{overscroll-behavior:contain}`
   rule, so the attribute is all that is needed here. The Lenis instance itself
   is a local `var` in that header script and is not reachable from the page,
   which is why the background lock below is CSS and not lenis.stop(). */
/* ============ 4b · SPEAKER BIO MODAL (ClickUp, Ryan's format) ============
   Dormant until SPEAKER_BIOS has entries: with none, no trigger and no
   dialog is rendered and none of this matches anything. */
/* FIXED, not absolute. Activating a <label> focuses its radio, and the
   browser scrolls a focused element into view -- with the radios living in
   the footer section, opening a bio from the speaker grid threw the page to
   the bottom and closing it left you there. Pinned to the viewport the
   radio is always already in view, so there is nothing to scroll to. */
.sof-spk-r{position:fixed;top:0;left:0;opacity:0;width:0;height:0;
  pointer-events:none}
/* The trigger over the portrait. A layer, not a wrapper, so the card's markup
   and grid behaviour are untouched; only a card with a bio gets one. */
.sof-card--bio{position:relative}
.sof-spk-hit{position:absolute;left:0;right:0;top:0;bottom:0;cursor:pointer;
  z-index:3}
.sof-card--bio .sof-card-foot{position:relative;z-index:4}
/* The day chip, made round. 2px of optical nudge on the glyph because the
   lowercase i sits high in its box. */
.sof-spk-i{display:inline-flex;align-items:center;justify-content:center;
  flex:0 0 auto;width:22px;height:22px;margin-left:8px;border-radius:50%;
  background:#FCCF44;border:2px solid #041C32;color:#041C32;cursor:pointer;
  font-family:__COND__;font-weight:700;font-size:13px;line-height:1;
  vertical-align:middle}
/* The glyph, not the line box, has to look centred: a lowercase i's ink sits
   high in its line box. The correction is per size and measured, not eyeballed
   -- at the mobile 13px it already lands dead centre, so the nudge lives in
   the 768 block with the 15px step that needs it. */
.sof-spk-hit:focus-visible,.sof-spk-i:focus-visible,.sof-spk-x:focus-visible{
  outline:3px solid #FCCF44;outline-offset:2px}

.sof-spk-modal{display:none;position:fixed;inset:0;z-index:9999;
  align-items:center;justify-content:center;padding:24px}
.sof-spk-r:not(#sof-spk-none):checked ~ .sof-spk-modal{display:flex}
/* NO html{overflow:hidden} LOCK HERE, deliberately, unlike the legal dialog.
   Measured on the live page: applying it moved the scroll position on its own
   -- 1826 to 1573 at 390, about 100px at 1920 -- with the document height
   unchanged, and once the root is overflow:hidden a scrollTo cannot put it
   back. So opening a bio threw you up the page and closing it left you there.

   overscroll-behavior:contain does the part that actually matters: a wheel or
   a swipe over the dialog scrolls the dialog's own copy and stops there
   rather than chaining to the page underneath. The page can still be scrolled
   from the scrim, which is a far smaller problem than losing your place. */
.sof-spk-modal,.sof-spk-box{overscroll-behavior:contain}
.sof-spk-scrim{position:absolute;inset:0;background:#020203D9;cursor:pointer}
/* .sof-tcard's treatment: cream, navy border, heavy bottom edge, 28 radius. */
.sof-spk-box{position:relative;display:flex;flex-direction:column;
  width:100%;max-width:720px;max-height:94vh;overflow:hidden;
  background:#FBEFD6;border:4px solid #041C32;border-bottom-width:12px;
  border-radius:28px}
.sof-spk-x{position:absolute;top:14px;right:14px;z-index:2;
  display:flex;align-items:center;justify-content:center;
  width:36px;height:36px;border-radius:50%;cursor:pointer;
  background:#041C32;color:#FBEFD6;border:0;
  font-family:__SANS__;font-weight:700;font-size:22px;line-height:1}
.sof-spk-doc{display:none}
.sof-spk-box{overflow-y:auto;-webkit-overflow-scrolling:touch}
/* The portrait is capped against the VIEWPORT, not left to run square at
   100% width. Measured with the longest bio open: at 100% it took ~52% of
   the box and pushed the copy out of view on shorter phones -- 145px of
   scroll on an iPhone SE (375x667), 34 on a 360x800 Android, none on a
   390x844. object-position keeps the face when the crop bites. */
.sof-spk-figure{display:block;width:100%;height:auto;max-height:25vh;
  object-fit:cover;object-position:50% 22%;background:#0F304F}
.sof-spk-copy{padding:20px}
.sof-spk-modal-name{font-family:__DISPLAY__;font-weight:900;font-size:34px;
  line-height:1.05;letter-spacing:-0.01em;color:#041C32;margin:0;
  text-transform:uppercase}
.sof-spk-modal-role{display:inline-flex;align-items:center;margin:10px 0 0;
  padding:5px 12px;border-radius:20px;background:#FCCF44;
  border:2px solid #041C32;font-family:__COND__;font-weight:700;
  font-size:13px;letter-spacing:.06em;color:#041C32;text-transform:uppercase}
.sof-spk-bio{margin-top:16px}
.sof-spk-bio p{font-family:__SANS__;font-weight:500;font-size:15px;
  line-height:1.45;color:#041C32;margin:0 0 10px}
.sof-spk-bio p:last-child{margin-bottom:0}
/* The placeholder reads as a status, not as the bio: muted and italic so a
   reviewer can tell at a glance which speakers still need copy. */
.sof-spk-soon{font-style:italic;opacity:.6}
/* Navy on cream, the same pairing as the close button and the ticket button,
   so these read as part of the dialog rather than as browser links. */
.sof-spk-links{display:flex;flex-wrap:wrap;gap:8px;margin-top:14px}
.sof-spk-link{display:inline-flex;align-items:center;padding:7px 14px;
  border-radius:999px;background:#041C32;color:#FBEFD6;text-decoration:none;
  font-family:__COND__;font-weight:700;font-size:13px;letter-spacing:.04em;
  text-transform:uppercase;line-height:1}
.sof-spk-link:focus-visible{outline:3px solid #FCCF44;outline-offset:2px}

/* ---- the modal's two-column layout, from 768 up ----------------------
   It used to live in the 1024 block, so tablets kept the phone layout: a
   720-wide box with a 712-wide portrait squashed to a 256-tall strip.

   The portrait is positioned ABSOLUTE rather than left as a grid item.
   `height:100%` on a grid item resolves against the row, the row is auto, so
   the percentage fell back to the image's own height and the portrait stopped
   short of the column -- 260x254 in a 396-tall box. Against a relatively
   positioned .sof-spk-doc the percentage has something definite to resolve
   against and the portrait fills its side properly. */
@media (min-width:768px){
  .sof-spk-doc{position:relative;grid-template-columns:260px minmax(0,1fr);
    min-height:380px}
  .sof-spk-figure{position:absolute;left:0;top:0;width:260px;height:100%;
    max-height:none;border-radius:0;object-fit:cover}
  .sof-spk-copy{grid-column:2;padding:28px}
  .sof-spk-modal-name{font-size:38px}
  .sof-spk-bio p{font-size:16px}
  .sof-spk-i{width:26px;height:26px;font-size:15px;margin-left:10px}
  .sof-spk-i span{position:relative;top:1px}
}
/* Short viewports, where the portrait is what pushes the copy out of reach.
   Keyed on HEIGHT, not width: a 360x800 phone is fine and a 360x640 is not,
   so width tells you nothing here. Measured with every bio open -- the worst
   is Alex's at 449 characters. 30vh left 41px of scroll at 640 and 2px at
   667; 22vh clears both. */
/* Short viewports. Keyed on HEIGHT, not width: a 360x800 phone is fine and a
   360x640 is not, so width tells you nothing here.

   Eline's bios grew to 626 characters and the link row was added under them,
   which put the longest ones back off the bottom -- 108px at 360x640. Rather
   than shrink the type until it is hard to read, this borrows the DESKTOP
   arrangement: a small portrait beside the copy instead of a banner above it.
   That is where the height was going -- a full-width portrait is ~45% of a
   640 screen, a 96px one is 15%. */
@media (max-height:700px){
  .sof-spk-doc{grid-template-columns:84px minmax(0,1fr);align-items:start}
  .sof-spk-figure{max-height:none;height:84px;border-radius:0}
  .sof-spk-copy{padding:14px 16px}
  .sof-spk-modal{padding:10px}
  .sof-spk-modal-name{font-size:26px}
  .sof-spk-bio p{font-size:14px;line-height:1.35;margin-bottom:6px}
  .sof-spk-bio{margin-top:12px}
  .sof-spk-links{margin-top:10px}
  .sof-spk-link{padding:6px 11px;font-size:12px}
}
/* One rule per seat, to 24: a seat added later cannot end up with a
   trigger that opens nothing. Rules for ids that do not exist match
   nothing. */
#sof-spk-0:checked ~ .sof-spk-modal .sof-spk-doc--0{display:grid}
#sof-spk-1:checked ~ .sof-spk-modal .sof-spk-doc--1{display:grid}
#sof-spk-2:checked ~ .sof-spk-modal .sof-spk-doc--2{display:grid}
#sof-spk-3:checked ~ .sof-spk-modal .sof-spk-doc--3{display:grid}
#sof-spk-4:checked ~ .sof-spk-modal .sof-spk-doc--4{display:grid}
#sof-spk-5:checked ~ .sof-spk-modal .sof-spk-doc--5{display:grid}
#sof-spk-6:checked ~ .sof-spk-modal .sof-spk-doc--6{display:grid}
#sof-spk-7:checked ~ .sof-spk-modal .sof-spk-doc--7{display:grid}
#sof-spk-8:checked ~ .sof-spk-modal .sof-spk-doc--8{display:grid}
#sof-spk-9:checked ~ .sof-spk-modal .sof-spk-doc--9{display:grid}
#sof-spk-10:checked ~ .sof-spk-modal .sof-spk-doc--10{display:grid}
#sof-spk-11:checked ~ .sof-spk-modal .sof-spk-doc--11{display:grid}
#sof-spk-12:checked ~ .sof-spk-modal .sof-spk-doc--12{display:grid}
#sof-spk-13:checked ~ .sof-spk-modal .sof-spk-doc--13{display:grid}
#sof-spk-14:checked ~ .sof-spk-modal .sof-spk-doc--14{display:grid}
#sof-spk-15:checked ~ .sof-spk-modal .sof-spk-doc--15{display:grid}
#sof-spk-16:checked ~ .sof-spk-modal .sof-spk-doc--16{display:grid}
#sof-spk-17:checked ~ .sof-spk-modal .sof-spk-doc--17{display:grid}
#sof-spk-18:checked ~ .sof-spk-modal .sof-spk-doc--18{display:grid}
#sof-spk-19:checked ~ .sof-spk-modal .sof-spk-doc--19{display:grid}
#sof-spk-20:checked ~ .sof-spk-modal .sof-spk-doc--20{display:grid}
#sof-spk-21:checked ~ .sof-spk-modal .sof-spk-doc--21{display:grid}
#sof-spk-22:checked ~ .sof-spk-modal .sof-spk-doc--22{display:grid}
#sof-spk-23:checked ~ .sof-spk-modal .sof-spk-doc--23{display:grid}
.sof-legal-r{position:absolute;opacity:0;width:0;height:0;pointer-events:none}
.sof-legal{display:none;position:fixed;inset:0;z-index:9999;
  align-items:center;justify-content:center;padding:16px}
#sof-legal-terms:checked ~ .sof-legal,
#sof-legal-privacy:checked ~ .sof-legal{display:flex}
/* Stop the page moving behind an open dialog. :has() is unsupported in older
   browsers, where the dialog simply scrolls over a scrollable page: degraded,
   not broken, so it needs no fallback. */
html:has(#sof-legal-terms:checked),
html:has(#sof-legal-privacy:checked){overflow:hidden}
.sof-legal-scrim{position:absolute;inset:0;background:#020203D9;
  backdrop-filter:blur(3px);cursor:pointer}
.sof-legal-box{position:relative;display:flex;flex-direction:column;
  width:100%;max-width:880px;max-height:86vh;
  background:#0D1422 url(__TEX_DARK__) repeat;background-size:1024px 1024px;
  border:2px solid #FBEFD6;border-radius:20px;overflow:hidden;
  box-shadow:0 24px 64px #000000A6}
.sof-legal-head{display:flex;align-items:center;justify-content:space-between;
  gap:12px;padding:14px 14px 14px 16px;background:#041C32;
  border-bottom:2px solid #FBEFD640;flex:0 0 auto}
.sof-legal-tabs{display:flex;gap:8px}
.sof-legal-tab{display:flex;align-items:center;justify-content:center;
  font-family:__DISPLAY__;font-weight:900;font-size:15px;letter-spacing:.5px;
  line-height:1;color:#FBEFD6;background:#0B1A32;cursor:pointer;
  padding:9px 14px;border:2px solid #FBEFD640;border-radius:999px}
#sof-legal-terms:checked ~ .sof-legal .sof-legal-tab--t,
#sof-legal-privacy:checked ~ .sof-legal .sof-legal-tab--p{
  color:#041C32;background:#FCCF44;border-color:#FCCF44}
.sof-legal-x{flex:0 0 36px;width:36px;height:36px;display:flex;
  align-items:center;justify-content:center;font-family:__DISPLAY__;
  font-weight:900;font-size:22px;line-height:1;color:#FBEFD6;cursor:pointer;
  background:#0B1A32;border:2px solid #FBEFD640;border-radius:999px}
.sof-legal-body{flex:1 1 auto;overflow-y:auto;-webkit-overflow-scrolling:touch;
  overscroll-behavior:contain;padding:22px 20px 28px}
.sof-legal-doc{display:none}
#sof-legal-terms:checked ~ .sof-legal .sof-legal-doc--t,
#sof-legal-privacy:checked ~ .sof-legal .sof-legal-doc--p{display:block}
.sof-legal-doc h3{font-family:__DISPLAY__;font-weight:900;font-size:28px;
  line-height:1.05;letter-spacing:.5px;color:#FCCF44;margin:0}
.sof-legal-meta{font-family:__COND__;font-weight:700;font-size:11px;
  letter-spacing:.08em;text-transform:uppercase;color:#FBEFD6A6;
  margin:8px 0 0}
.sof-legal-doc h4{font-family:__DISPLAY__;font-weight:900;font-size:16px;
  letter-spacing:.3px;color:#FBEFD6;margin:22px 0 6px}
.sof-legal-doc p,.sof-legal-doc li{font-family:__BODY__;font-weight:400;
  font-size:14px;line-height:22px;color:#E8E4D8;margin:0 0 8px}
.sof-legal-doc ul{margin:0 0 8px;padding-left:18px}
.sof-legal-doc li{margin:0 0 5px}
.sof-legal-doc strong{color:#FBEFD6;font-weight:700}
/* The only link inside either document. Gold to match the dialog's other
   actionable things, and break-anywhere because a 25-character address in a
   14px column at 320 has nowhere else to go. */
.sof-legal-mail{color:#FCCF44;font-weight:700;text-decoration:underline;
  text-underline-offset:2px;overflow-wrap:anywhere}
/* Facts only the organiser can supply. Gold so they cannot be shipped by
   accident, and one class so they are countable from the rendered page. */
.sof-legal-tbc{color:#FCCF44;font-weight:700;background:#FCCF441A;
  border-bottom:1px dashed #FCCF44;padding:0 3px;border-radius:3px}
/* The two words in the footer copy line. They stay inline in the sentence the
   design drew, so the copy design_diff compares is byte for byte unchanged. */
.sof-legal-open{color:#FCCF44;cursor:pointer;text-decoration:underline;
  text-underline-offset:2px}
@media (min-width:1024px){
  .sof-legal{padding:32px}
  .sof-legal-box{max-width:1000px;border-radius:24px}
  .sof-legal-head{padding:18px 18px 18px 22px}
  .sof-legal-tab{font-size:20px;padding:11px 20px}
  .sof-legal-x{flex-basis:44px;width:44px;height:44px;font-size:26px}
  .sof-legal-body{padding:32px 36px 40px}
  .sof-legal-doc h3{font-size:40px}
  .sof-legal-meta{font-size:14px}
  .sof-legal-doc h4{font-size:21px;margin:30px 0 8px}
  .sof-legal-doc p,.sof-legal-doc li{font-size:17px;line-height:27px}
  .sof-legal-doc ul{padding-left:22px}
}
"""

CSS = (CSS
       .replace("__SANS__", SANS)
       .replace("__PARCHMENT__", u("parchment"))
       .replace("__DISPLAY__", DISPLAY)
       .replace("__COND__", COND)
       .replace("__XCOND__", XCOND)
       .replace("__MONO__", MONO)
       .replace("__BARLOW__", BARLOW)
       .replace("__BODY__", BODY_SANS)
       .replace("__TEX_DARK__", u("texture_dark"))
       .replace("__TEX_PAPER__", u("texture_paper")))


# ==========================================================================
# HTML builders. One function per design section; each returns the inner
# markup of a single LF HtmlElement.
# ==========================================================================
def art(src, alt, cls=""):
    """A display lockup that Figma draws as outlined vectors or a bespoke
    face. Placed as the exported node at 3x, with the words in alt."""
    return ('<span class="sof-art %s"><img src="%s" alt="%s" loading="lazy" '
            'decoding="async"></span>' % (cls, src, esc(alt)))


# ------------------------------------------------------------- 1 · header
# The new frame keeps all five labels including TOPICS, but deletes the Topics
# section they used to point at. Rather than drop a label the design still
# draws, TOPICS now anchors the Mission Map, which is where the subjects
# actually live now ("Creative teardown", "Channel deep dives", and the rest).
# Joshua's call on 2026-10-09 was to remove the section; the repoint is mine.
# The two steps' own URLs. One constant each because the nav and the footer
# both render from NAV, and BOTH pages render the same NAV.
EVENT_URL = "/event/scaling-failing"
CONTACT_URL = "/event/contact"

NAV = [("ABOUT", "#about", False), ("SPEAKERS", "#speakers", False),
       ("TOPICS", "#topics", False), ("GET TICKET", "#tickets", True),
       ("CONTACT", CONTACT_URL, False)]


def nav_href(href):
    """An in-page anchor, resolved for the page actually being built.

    Four of NAV's five entries are anchors into sections the EVENT page has.
    The contact page has none of them, so on that page they have to carry the
    event page's URL or they do nothing -- which is exactly what they did.

    Absolute paths (CONTACT) and anything else pass through untouched.
    """
    if PAGE != "event" and href.startswith("#"):
        return EVENT_URL + href
    return href


# 30 Oct 2026, 23:59:59 US PACIFIC (PDT, UTC-7) -- moved there 2026-10-30 on
# the team's call ("lets have it run US timezone today as it is, just timer
# needs to move"). It was 23:59:59 BANGKOK until then, which would have
# expired the same evening. 30 Oct is still PDT; US daylight time ends 1 Nov.
# In local terms the new instant is 31 Oct 14:59 Manila / 13:59 Bangkok.
# Kept as a UTC instant so it means the same thing wherever it is read --
# the browser compares against its own clock, not its own calendar.
# The ticket card badge "ENDS OCT 30" is the same fact; move both together.
COUNTDOWN_ENDS = "2026-10-31T06:59:59Z"
_CD_UNITS = (("d", "DAYS"), ("h", "HRS"), ("m", "MIN"), ("s", "SEC"))


def countdown_html():
    """The gold Early Bird bar, or nothing at all once the deadline passes.

    Returns "" after the deadline so a build run on 31 October does not ship
    a timer reading zero. The script does the same job for a tab that was
    already open; see the module note on why both are needed.

    The digits are rendered with the remaining time AT BUILD TIME rather than
    as placeholders, so the bar is correct in the HTML itself -- for the first
    paint before the script runs, and for anyone without JavaScript, where a
    slightly stale number still beats four dashes. The script corrects it on
    the next frame and every second after.
    """
    import datetime
    end = datetime.datetime(2026, 10, 31, 6, 59, 59,
                            tzinfo=datetime.timezone.utc)
    left = int((end - datetime.datetime.now(datetime.timezone.utc))
               .total_seconds())
    if left <= 0:
        return ""
    at = (left // 86400, left // 3600 % 24, left // 60 % 60, left % 60)
    cells = []
    for i, (key, lab) in enumerate(_CD_UNITS):
        if i:
            cells.append('<span class="sof-cd-c" aria-hidden="true">:</span>')
        cells.append('<span class="sof-cd-u"><b data-cd="%s">%02d</b>'
                     '<i>%s</i></span>' % (key, at[i], lab))
    return (
        '<div class="sof-cd" data-cd-ends="%s">'
        '<span class="sof-cd-lab"><b>EARLY BIRD</b>'
        '<i>PRICING ENDS SOON</i></span>'
        '<span class="sof-cd-units">%s</span>'
        '</div>' % (COUNTDOWN_ENDS, "".join(cells)))


def promo_html():
    """The announcement bar, built as its own section.

    Separate from header_html so it can be mounted with scale=False: inside
    the .sof-scale zoom its height and type scale with the page, and the ask
    was for a constant 36px bar with 14px text at every width.
    """
    return ('<a class="sof-promo" href="%s"><span>%s</span></a>'
            % (EB_HREF, T("949:1090")))


def header_html():
    cells = []
    for i, (label, href, gold) in enumerate(NAV):
        cls = "sof-navcell"
        if i < len(NAV) - 1:
            cls += " sof-navcell--rule"
        if gold:
            cls += " sof-navcell--gold"
        cells.append('<a class="%s" href="%s">%s</a>'
                     % (cls, nav_href(href), label))
    menu = "".join(
        '<a href="%s"%s>%s</a>'
        % (nav_href(href), ' class="sof-gold"' if gold else "", label)
        for label, href, gold in NAV)
    return (
        '<input type="checkbox" id="sof-menu" class="sof-menu-cb" '
        'aria-hidden="true" tabindex="-1">'
        '<nav class="sof-nav sof-nav-d" aria-label="Main">%s</nav>'
        '<nav class="sof-nav sof-nav-m" aria-label="Main">'
        '<label class="sof-navcell sof-navcell--rule" for="sof-menu">'
        '<span class="sof-burger" aria-hidden="true"><i></i><i></i><i></i></span>'
        '%s</label>'
        '<a class="sof-navcell sof-navcell--gold" href="%s">%s</a></nav>'
        '<div class="sof-menu">%s</div>'
    # ⚠️ nav_href, NOT a bare CTA_HREF. The desktop cells already go through
    # it; this mobile gold button did not, so on the CONTACT page its
    # GET TICKET pointed at "#tickets", a section that page does not have,
    # and tapping it did nothing. The header is on BOTH pages, so every
    # anchor in it has to be resolved for the page being built.
    ) % ("".join(cells), T("949:1539"), nav_href(CTA_HREF),
         T("949:1541"), menu)


# --------------------------------------------------------------- 2 · hero
def hero_h1():
    """The page's single h1. The headline is drawn in "Scaling Lockup", a
    bespoke face we cannot ship, so the artwork is the exported node and the
    words live here as clipped-but-rendered text at the node's own font size
    and colour (set per breakpoint in CSS). Standard image replacement: the
    headline is real text for crawlers and screen readers, the artwork is what
    you see, and the two lockup <img>s are alt="" because this carries the
    words already.

    870:29 genuinely contains "SCALINg" with a lowercase g, because the bespoke
    display face draws a stylised glyph there and the designer typed what the
    lockup looks like. That is a fact about the ARTWORK, not about the word, and
    this is the page's real headline text -- the one string on the page where
    verbatim-from-Figma is the wrong rule. The word is "SCALING"; everywhere
    else on the page it is already spelled that way. design_diff will report
    this node as retyped; that report is the fix, not a defect."""
    return ('<h1 class="sof-vh sof-h1">'
            '<span class="a">SCALING</span> <span class="b">%s</span> '
            '<span class="c">%s</span></h1>'
            % (T("949:1114"), T("949:1113")))


def hero_lockup(desktop):
    key = "lockup_hero" if desktop else "lockup_hero_m"
    return ('<div class="sof-lockup"><img src="%s" alt="" fetchpriority="high" '
            'decoding="async"></div>' % u(key))


def hero_html():
    cta = ('<a class="sof-cta" href="%s"><i aria-hidden="true"></i>'
           '<span>%s</span></a>')
    # mobile stack (870:446)
    mobile = (
        '<div class="sof-hero-m">'
        '<p class="sof-date">%s</p>'
        '%s'
        '<div class="sof-tag"><span>%s</span></div>'
        + cta % (CTA_HREF, T("949:1558")) +
        '<div class="sof-pow"><b>%s</b>'
        '<img src="%s" alt="BestFulfill" loading="lazy" decoding="async"></div>'
        '<div class="sof-hosts"><span>%s</span><span>%s</span><span>%s</span></div>'
        '</div>'
    ) % (T("949:1546"), hero_lockup(False), T("949:1553"), T("949:1560"),
         u("bestfulfill_logo"), T("949:1563"), T("949:1564"), T("949:1565"))
    # desktop stack (870:21) — the copy column is pinned left, the hosts strip
    # is flush to the right edge above the blurred navy shade.
    desktop = (
        '<div class="sof-hero-d">'
        '<div class="sof-hero-col">'
        '<p class="sof-date">%s</p>'
        '%s'
        '<div class="sof-tag"><span>%s</span></div>'
        + cta % (CTA_HREF, T("949:1121")) +
        '<div class="sof-pow"><b>%s</b>'
        '<img src="%s" alt="BestFulfill" loading="lazy" decoding="async"></div>'
        '</div>'
        '<div class="sof-hero-shadeblur" aria-hidden="true"></div>'
        '<div class="sof-hosts"><span>%s</span><span>%s</span><span>%s</span></div>'
        '</div>'
    ) % (T("949:1108"), hero_lockup(True), T("949:1116"), T("949:1122"),
         u("bestfulfill_logo"), T("949:1126"), T("949:1127"), T("949:1128"))
    # The two frames crop the same photograph differently (1920x1088 against
    # 390x844), so each breakpoint gets its own node render -- object-fit cannot
    # reach the other crop. display:contents keeps the <img> as the positioned
    # element, so <picture> adds no box of its own.
    return (
        '<picture class="sof-hero-pic">'
        '<source media="(max-width:767px)" srcset="%s">'
        '<img class="sof-hero-plate" src="%s" alt="" aria-hidden="true" '
        'fetchpriority="high" decoding="async"></picture>'
        '<div class="sof-hero-wash" aria-hidden="true"></div>'
        '<div class="sof-hero-shade" aria-hidden="true"></div>'
        % (u("hero_mobile"), u("hero_desktop"))) + hero_h1() + mobile + desktop


# -------------------------------------------------------------- 3 · stats
STATS = [("stat_300", "300+", "stat_operators", "OPERATORS"),
         ("stat_12", "12", "stat_speakers", "SPEAKERS"),
         ("stat_2", "2", "stat_days", "DAYS")]


def stats_html():
    out = []
    for i, (nk, nalt, lk, lalt) in enumerate(STATS):
        if i:
            out.append('<span class="sof-statdiv" aria-hidden="true"></span>')
        out.append(
            '<div class="sof-stat">'
            '<span class="sof-num"><img src="%s" alt="%s" loading="lazy" '
            'decoding="async"></span>'
            '<span class="sof-lab"><img src="%s" alt="%s" loading="lazy" '
            'decoding="async"></span></div>'
            % (u(nk), nalt, u(lk), lalt))
    return '<div class="sof-stats-row">%s</div>' % "".join(out)


# ----------------------------------------------------------- 4 · speakers
SPEAKERS = [
    ("name_gonzalo", "Gonzalo", "949:1285", False),
    ("name_ronak", "Ronak Shah", "949:1251", False),
    ("name_alex", "Alex Fedotoff", "949:1240", False),
    ("name_tba", "TBA", "870:154", True),
    ("name_tba", "TBA", "870:163", True),
    ("name_tba", "TBA", "870:172", True),
    ("name_tba", "TBA", "870:181", True),
    ("name_tba", "TBA", "870:190", True),
    ("name_tba", "TBA", "870:199", True),
    ("name_tba", "TBA", "870:208", True),
]


def speakers_html():
    """Ten plates, eight of them now real photographs (frame 904:203).

    Names were name-shaped ARTWORK before, because the design sets them in
    Scaling Lockup and that is not a webfont. The new frame names ten people
    instead of three, so ten more name images would be ten more uploads and
    ten more things to regenerate on a spelling fix. They are live text in the
    display face instead -- the same substitution the nav and the stats strip
    have always made for that font, and it makes the names searchable,
    selectable and checkable by design_diff rather than invisible inside a PNG.
    """
    cards = []
    seen = [n for n, _, _, _, _ in SPEAKERS_V2]
    assert len(set(seen)) == len(seen), (
        "two speaker rows share a name node: %s -- see the note above about "
        "TBA plates resolving onto each other"
        % sorted({n for n in seen if seen.count(n) > 1}))
    for idx, (name_id, role_id, photo_key, size_cls, tba) in enumerate(SPEAKERS_V2):
        bio = speaker_bio(photo_key)
        if photo_key is None:
            # 904:358 etc. — the Passion One "?" plate. Shown for a seat that is
            # still TBA, and for an announced speaker whose photo has not landed.
            photo = '<div class="sof-photo"><em aria-hidden="true">%s</em></div>' % T("949:1289")
        else:
            photo = ('<img class="sof-spk-photo" src="%s" alt="%s" '
                     'loading="lazy" decoding="async">'
                     % (u(photo_key), esc(_plain(speaker_name(name_id)))))
        role_txt = T(role_id)
        # No role yet: drop the line instead of printing an empty one, which
        # would hold open a gap the other cards do not have.
        role_html = ('<p class="sof-spk-role%s">%s</p>'
                     % (" sof-spk-role--tba" if tba else "", role_txt)) if role_txt else ""
        # No bio yet -> no trigger at all. The card is byte-for-byte what it
        # was before the modal existed.
        hit, info = "", ""
        if bio:
            who = esc(_plain(speaker_name(name_id)))
            hit = ('<label class="sof-spk-hit" for="sof-spk-%d" tabindex="0" '
                   'role="button" aria-label="Read %s\u2019s bio"></label>'
                   % (idx, who))
            info = ('<label class="sof-spk-i" for="sof-spk-%d" tabindex="0" '
                    'role="button" aria-label="Read %s\u2019s bio">'
                    '<span aria-hidden="true">i</span></label>' % (idx, who))
        cards.append(
            '<div class="sof-card%s">'
            '%s%s'
            '<div class="sof-card-foot">'
            '<p class="sof-spk-name%s">%s%s</p>'
            '%s</div></div>'
            % (" sof-card--bio" if bio else "", photo, hit,
               (" sof-spk-name--tba" if tba else "") + size_cls,
               speaker_name(name_id), info, role_html))
    return (
        '<h2>%s%s<span class="sof-vh">How the best are scaling right now</span></h2>'
        '<div class="sof-grid">%s</div>'
    ) % (art(u("t_speakers"), "How the best are scaling right now", "sof-t-d"),
         art(u("t_speakers_m"), "How the best are scaling right now", "sof-t-m"),
         "".join(cards))


# ------------------------------------------------------------ 5 · formats
FORMATS = [
    ("format_1", "949:1356", "949:1357", "949:1358",
     "Two operators on stage mid-interview"),
    ("format_2", "949:1362", "949:1363", "949:1364",
     "A speaker presenting a system on the main stage"),
    ("format_3", "949:1368", "949:1369", "949:1370",
     "An attendee asking a question from the audience"),
]


def formats_html():
    cards = []
    for key, kick, head, body, alt in FORMATS:
        cards.append(
            '<div class="sof-fcard">'
            '<div class="sof-fcard-img"><img src="%s" alt="%s" loading="lazy" '
            'decoding="async"><i aria-hidden="true"></i></div>'
            '<div class="sof-fcard-body">'
            '<p class="sof-fkick">%s</p>'
            '<p class="sof-fhead">%s</p>'
            '<p class="sof-fbody sof-rich">%s</p>'
            '</div></div>' % (u(key), esc(alt), T(kick), T(head), T(body)))
    return (
        '<div class="sof-eyebrow"><b>%s</b><i aria-hidden="true"></i></div>'
        '<h2 class="sof-ftitle">%s%s%s'
        '<span class="sof-vh">Three formats. Zero filler.</span></h2>'
        '<p class="sof-subline">%s</p>'
        '<div class="sof-fcards">%s</div>'
    ) % (T("949:1324"),
         art(u("t_formats"), "Three formats. Zero filler.", "sof-t-d"),
         art(u("t_formats_m1"), "Three formats.", "sof-t-m sof-ft1"),
         art(u("t_formats_m2"), "Zero filler.", "sof-t-m sof-ft2"),
         T("949:1352"), "".join(cards))


# --------------------------------------------------------- 6 · you decide
def decide_html():
    return (
        # The two frames crop the same photograph differently -- 870:262 is
        # 1920x1168 (1.64) and 870:687 is 390x800 (0.49) -- so each breakpoint
        # gets its own node render. object-fit cannot reach the other crop:
        # cover-fitting the 1.78 landscape file into the 0.49 portrait box kept
        # a narrow centre slice and lost the iguana driver, most of the car and
        # nearly all the skyline (pixel distance 0.248 against the mobile frame
        # against 0.000 for the mobile render).
        #
        # THE BOUNDARY MUST EQUAL THE LAYOUT'S GATE. It was 1199 when the
        # mobile design served up to 1199; the desktop design now starts at
        # 1024, so it is 1023. Left at 1199 the page drew the desktop
        # composition around the portrait crop and showed sky where the lizard
        # should be. Same display:contents <picture> as the hero plate above.
        '<picture class="sof-decide-pic">'
        # 767, not 1023. The boundary used to equal the LAYOUT's gate because
        # the plate sat behind the copy and the composition was drawn around
        # the crop. Below 1024 the plate is in the flow underneath the copy
        # now, so the crop is just a picture choice -- and the 506x900
        # portrait at full width is 1366 tall at 768 and 1820 at 1023, which
        # made the section 2051 and 2639 tall. The landscape render is 467
        # tall at 768. Phones keep the portrait; the tablet band takes the
        # landscape.
        '<source media="(max-width:1023px)" srcset="%s">'
        '<img class="sof-decide-bg" src="%s" alt="" aria-hidden="true" '
        'loading="lazy" decoding="async"></picture>'
        '<div class="sof-decide-wash" aria-hidden="true"></div>'
        '<div class="sof-in">'
        '<p class="sof-kicker">%s</p>'
        # Group 10 (918:476): three TEXT_PATH lines on a curve.
        # OPEN QUESTION 2 IS CLOSED. The artwork used to read "SCALLING" with
        # two Ls, straight off the vector, through four frames. The V4 frame
        # spells it correctly (918:477), so this is that group re-exported.
        # The sr-only heading text sits on the h2 OUTSIDE the artwork wrapper:
        # it used to be inside the element the stylesheet hid below 768, which
        # took the heading away from a screen reader on every phone and left
        # the page with five rendered h2s instead of six.
        '<h2 class="sof-decide-head">'
        '<span class="sof-vh">Are you scaling or failing?</span>'
        '<span class="sof-decide-art">'
        '<img src="%s" alt="Are you scaling or failing?" loading="lazy" '
        'decoding="async"></span></h2>'
        '<p class="sof-decide-body sof-decide-intro sof-only-d sof-rich">%s</p>'
        '<p class="sof-decide-body sof-decide-intro sof-only-m sof-rich">%s</p>'
        '<p class="sof-decide-body sof-decide-promise sof-rich">%s</p>'
        '</div>'
    ) % (u("car_scene_mobile"), u("car_scene"), T("949:1373"), u("art_youdecide_v4"),
         Tseg("949:1398"), Tseg("949:1882"), Tbr("949:1399"))


# ------------------------------------------------------------- 7 · topics
# Tab colour is measured per chip, NOT a left/right alternation: SNAPCHAT is
# yellow where the pattern would say red, NATIVE ADS is red where it would say
# yellow. Reproduced as measured.
CHIPS = [("905:2299", "y"), ("905:2304", "r"), ("905:2309", "y"), ("905:2314", "r"),
         ("905:2319", "y"), ("905:2324", "r"), ("905:2329", "y"), ("905:2334", "y"),
         ("905:2339", "r"), ("905:2344", "r"), ("905:2349", "y"), ("905:2354", "r")]


def topics_html():
    chips = "".join(
        '<div class="sof-chip"><div class="sof-chip-panel">'
        '<span class="sof-chip-tab sof-chip-tab--%s" aria-hidden="true"></span>'
        '<span class="sof-chip-label">%s</span></div></div>' % (tab, T(tid))
        for tid, tab in CHIPS)
    return (
        '<h2>%s%s<span class="sof-vh">Let’s talk topics</span></h2>'
        '<p class="sof-subtitle">%s</p>'
        '<div class="sof-chips">%s</div>'
    ) % (art(u("t_topics"), "Let’s talk topics", "sof-t-d"),
         art(u("t_topics_m"), "Let’s talk topics", "sof-t-m"),
         T("905:2294"), chips)


# ------------------------------------------------------------ 8 · tickets
# The four Early Bird bullets. The VIP list is gone with the VIP card.
EB_BULLETS = ["949:1461", "949:1463", "949:1465", "949:1467"]


def ticket_card():
    """The one ticket: a single cream card.

    `.sof-ttop` is a two-column grid holding the pills, the name, the price
    and the Scalizard mark; the bullets and the button sit under it and run
    the card's full measure. The pills drop to their own full-width row on
    mobile and sit beside the mark on desktop, which is a grid-area swap
    rather than two layouts. No navy panel, no perforation and no date line --
    the badge reads on the card's own cream, which is the point of the design.

    One card now, so no `cards` wrapper and no per-card href: the only button
    on it is the Early Bird one.
    """
    lis = "".join("<li>%s</li>" % T(b) for b in EB_BULLETS)
    return (
        '<div class="sof-tcard">'
        # Gold banner across the card's top edge (982:1426 / 982:935). The
        # card already clips to its own radius, so the strip takes the
        # corners without needing its own. The tick is inline SVG rather
        # than an upload: fewer bytes than the request would cost, and it
        # resizes between breakpoints without a second export.
        '<p class="sof-tbanner"><span class="sof-tcheck" aria-hidden="true">'
        '<svg viewBox="0 0 14 10" fill="none" stroke="#fff" stroke-width="3"'
        ' stroke-linecap="round" stroke-linejoin="round">'
        '<path d="M1.6 5.2 5.4 9 12.4 1.4"/></svg></span>'
        '<b>LIMITED SEATS</b></p>'
        # .sof-ttop is a GRID and these four are placed by area, which is what
        # lets one markup give the pills a full-width row on mobile and a seat
        # beside the mark on desktop. The list and the button are card
        # children so they run the card's full measure.
        '<div class="sof-ttop">'
        '<div class="sof-badges">'
        '<span class="sof-badge">%s</span>'
        '</div>'
        '<p class="sof-tname">%s</p>'
        '<div class="sof-tpricerow"><p class="sof-tprice">%s</p></div>'
        '<div class="sof-tmark">'
        '<img class="sof-sticker" src="%s" alt="Scalizard recommends"'
        ' loading="lazy" decoding="async">'
        '</div></div>'
        '<ul class="sof-tlist">%s</ul>'
        '<a class="sof-tbtn" href="%s"><i aria-hidden="true"></i>'
        '<span>%s</span></a>'
        '<p class="sof-tsplit">or <a href="%s">split into 2 payments of $1,498.50</a></p>'
        '</div>'
    ) % (T("949:1457"), T("949:1458"), T("949:1459"),
         u("vip_sticker"), lis, EB_HREF, T("949:1471"), SPLIT_HREF)


def speaker_modal_html():
    """The radios and the dialog, for every speaker that has a bio.

    Returns "" when none do, so the page carries no modal markup at all when
    the placeholder is off and no real bio has landed.

    TWO PLACEMENT RULES, both of which this got wrong first time.

    1. It goes through `section(after=...)`, which puts it OUTSIDE .sof-scale.
       A position:fixed box inside a zoomed ancestor is scaled by it and
       trapped in its box.

    2. It hangs off the FOOTER, the last section, not off the speakers
       section it belongs to. Each Lightfunnels Section establishes its own
       stacking context, so z-index:9999 only wins inside its own section --
       mounted on the speakers section the scrim covered the viewport
       correctly but every later section painted straight over it, and the
       page below the fold was not dimmed. The legal dialog is on the footer
       for the same reason.
    """
    rows = [(i, n, r, k) for i, (n, r, k, _s, _t) in enumerate(SPEAKERS_V2)
            if speaker_bio(k)]
    if not rows:
        return ""

    # `none` is the closed state and is checked by default, so the dialog is
    # shut on load without needing a rule for it.
    radios = ('<input type="radio" name="sof-spk" id="sof-spk-none" '
              'class="sof-spk-r" checked aria-hidden="true" tabindex="-1">')
    radios += "".join(
        '<input type="radio" name="sof-spk" id="sof-spk-%d" class="sof-spk-r" '
        'aria-hidden="true" tabindex="-1">' % i for i, _n, _r, _k in rows)

    docs = []
    for i, name_id, role_id, key in rows:
        role = T(role_id)
        para = speaker_bio(key)
        placeholder = para is BIO_PLACEHOLDER
        body = "".join('<p%s>%s</p>'
                       % (' class="sof-spk-soon"' if placeholder else "", esc(p))
                       for p in para)
        # Their own profiles, opening in a new tab. noopener/noreferrer because
        # a third-party page opened with target=_blank can otherwise reach back
        # through window.opener.
        urls = SPEAKER_LINKS.get(key) or []
        linkrow = ('<div class="sof-spk-links">%s</div>' % "".join(
            '<a class="sof-spk-link" href="%s" target="_blank" '
            'rel="noopener noreferrer">%s</a>' % (esc(href), esc(lbl))
            for lbl, href in urls)) if urls else ""
        docs.append(
            '<div class="sof-spk-doc sof-spk-doc--%d">'
            '<img class="sof-spk-figure" src="%s" alt="" '
            'loading="lazy" decoding="async">'
            '<div class="sof-spk-copy">'
            '<p class="sof-spk-modal-name">%s</p>'
            '%s'
            '<div class="sof-spk-bio">%s</div>'
            '%s</div></div>'
            % (i, u(key), speaker_name(name_id),
               ('<p class="sof-spk-modal-role">%s</p>' % role) if role else "",
               body, linkrow))

    return (
        '%s'
        '<div class="sof-spk-modal" role="dialog" aria-modal="true" '
        'aria-label="Speaker bio">'
        '<label class="sof-spk-scrim" for="sof-spk-none" aria-hidden="true">'
        '</label>'
        '<div class="sof-spk-box">'
        '<label class="sof-spk-x" for="sof-spk-none" tabindex="0" '
        'role="button" aria-label="Close"><span aria-hidden="true">'
        '\u00d7</span></label>'
        '%s</div></div>'
    ) % (radios, "".join(docs))


def _tt_words():
    """The heading as words, for the alt text and the screen-reader heading.

    Read from the two nodes rather than typed: the apostrophe in DON'T is a
    curly U+2019 and typing it straight is exactly the kind of silent copy
    drift the node-id discipline exists to prevent.
    """
    return "%s %s" % (T("949:1505"), T("949:1506"))


def tickets_html():
    return (
        # The eyebrow leads, as both frames draw it: rule, text, rule.
        '<p class="sof-teyebrow"><i aria-hidden="true"></i><b>%s</b>'
        '<i aria-hidden="true"></i></p>'
        '<h2 class="sof-ttitle">%s%s'
        '<span class="sof-vh">%s</span></h2>'
        '<p class="sof-tdate">%s</p>'
        '%s'
    ) % (T("949:1509"),
         art(u("t_tickets_v5"), _tt_words(), "sof-t-d"),
         art(u("t_tickets_v5_m"), _tt_words(), "sof-t-m"),
         _tt_words(),
         T("949:1453"), ticket_card())


# ------------------------------------------------------------ 9 · sponsor
def sponsor_html():
    """OUR PARTNERS, POWERED BY, and the four tiers Figma actually draws:
    Diamond (the big BestFulfill plate), Platinum (Outcraft, solo), Gold
    (Suits/Whop/"Sponsor S" sharing a row) and Silver (Tazapay, solo). An
    earlier version of this flattened every partner after BestFulfill into
    one row regardless of tier; that matched neither the frame nor Joshua's
    screenshot of the live mistake, and is fixed here.

    The BestFulfill mark is the SAME symbol the marquee uses; only its colour
    differs, red here and navy there, which is why the symbol carries
    currentColor rather than a baked fill."""
    gold = "".join(
        '<div class="sof-splate sof-splate--%s">'
        '<svg role="img" aria-label="%s"><use href="#sof-logo-%s"/></svg></div>'
        % (k, label, k)
        for k, label in (("suits", "Suits Finance"),
                         ("whop", "Whop"), ("s", "Slash")))
    return (
        '<p class="sof-partner">%s</p>'
        '<div class="sof-sponsor-rule" aria-hidden="true"></div>'
        '<h2 class="sof-powered">%s</h2>'
        '<div class="sof-plate">'
        '<svg class="sof-plate-logo" role="img" aria-label="BestFulfill">'
        '<use href="#sof-logo-bf"/></svg></div>'
        '<div class="sof-tier">'
        '<div class="sof-tplate sof-tplate--oc">'
        '<svg role="img" aria-label="Outcraft"><use href="#sof-logo-oc"/></svg>'
        '</div></div>'
        '<div class="sof-sponsors">%s</div>'
        '<div class="sof-tier">'
        '<div class="sof-tplate sof-tplate--taza">'
        '<svg role="img" aria-label="Tazapay"><use href="#sof-logo-taza"/></svg>'
        '</div></div>'
    ) % (T("949:1513"), T("949:1515"), gold)


# --------------------------------------- 2b | sponsor logo marquee
# 1027:382 desktop / 1027:1043 mobile, new on 2026-10-31. The six-phrase
# ticker it replaces is gone from the frame entirely.
LOGO_DEFS = '<svg width="0" height="0" aria-hidden="true" focusable="false" style="position:absolute"><symbol id="sof-logo-bf" viewBox="0 0 560 87">\n<g clip-path="url(#sof-bf-clip0_1027_878)">\n<path d="M0.0761839 42.7354C0.0761839 29.2267 0.0761839 15.7179 0.0761839 2.23453C0.0761839 2.10757 0.0761839 1.95522 0.0761839 1.82825C0.101576 0.228532 0.304717 0 1.85365 0C4.6976 0 7.54155 0 10.3855 0C11.8329 0 13.2548 0 14.7022 0C17.0637 0 17.343 0.279316 17.343 2.6662C17.343 20.6186 17.343 38.5711 17.343 56.5489C17.343 59.7991 17.343 63.0494 17.343 66.325C17.343 67.7978 17.4192 67.8739 18.9174 67.8739C34.5083 67.8739 50.0992 67.8739 65.6902 67.8739C67.9501 67.8739 67.9501 67.8739 67.9501 65.5886C67.9501 49.9977 67.9501 34.4067 67.9755 18.8158C67.9755 17.9778 67.7216 17.6731 66.8582 17.6731C56.1934 17.6985 45.554 17.6985 34.8892 17.6985C33.0355 17.6985 32.7816 17.47 32.7816 15.6671C32.7816 11.0711 32.7816 6.47507 32.7816 1.87904C32.7816 0.203139 32.9848 0.0253924 34.7114 0.0253924C50.861 0.0253924 66.9852 0.0253924 83.1348 0.0253924C83.4141 0.0253924 83.6934 0.0253924 83.9473 0.0507848C85.2677 0.152355 85.5471 0.457064 85.5471 1.77747C85.5471 28.8204 85.5471 55.8633 85.5471 82.9062C85.5471 85.4455 85.3947 85.5978 82.8809 85.5978C55.7617 85.5978 28.668 85.5978 1.54894 85.5978C0.279319 85.5978 0.0253977 85.3693 0.0253977 83.9981C5.42497e-06 76.8375 0 69.6768 0 62.5161C0 55.9395 0 49.3629 0 42.7862C0.0507848 42.7354 0.0507914 42.7354 0.0761839 42.7354Z" fill="currentColor"/>\n<path d="M32.8071 42.6589C32.8071 40.2212 32.8071 37.8089 32.8071 35.3713C32.8071 33.2637 33.1626 32.9336 35.2194 32.9336C39.8662 32.9336 44.5384 32.9336 49.1852 32.9336C52.4101 32.9336 52.6894 33.2383 52.6894 36.4631C52.6894 40.9576 52.6894 45.4267 52.6894 49.9211C52.6894 50.302 52.6894 50.6829 52.6386 51.0384C52.5116 51.9271 52.08 52.435 51.0896 52.4604C46.4682 52.4858 41.8468 52.5619 37.2254 52.6127C36.362 52.6127 35.5241 52.6127 34.6608 52.6127C33.3911 52.5873 32.9087 52.181 32.8325 50.9114C32.7563 49.7942 32.8071 48.6515 32.8071 47.5342C32.8071 45.8837 32.8071 44.2586 32.8071 42.6589Z" fill="currentColor"/>\n</g>\n<g clip-path="url(#sof-bf-clip1_1027_878)">\n<path d="M158.727 45.6395L158.77 40.9923V29.609V29.4811V24.834H154.165H120.953V29.4811H154.165V40.9923H120.868V45.6395H154.165V57.6197H120.953V62.2668H158.727V57.6197V45.6395Z" fill="currentColor"/>\n<path d="M205.412 57.6621H169.855V62.3092H205.412V57.6621Z" fill="currentColor"/>\n<path d="M204.517 24.9619H169.855V29.609H204.517V24.9619Z" fill="currentColor"/>\n<path d="M201.234 41.0352H169.855V45.6823H201.234V41.0352Z" fill="currentColor"/>\n<path d="M293.025 23.9814H260.111V28.6286H293.025V23.9814Z" fill="currentColor"/>\n<path d="M274.255 38.1104V61.3886H278.86V38.1104H274.255Z" fill="currentColor"/>\n<path d="M337.492 23.9814H302.916V28.6286H337.492V23.9814Z" fill="currentColor"/>\n<path d="M334.21 40.1396H302.916V61.3715H307.52V44.7441H334.21V40.1396Z" fill="currentColor"/>\n<path d="M467.101 23.9814H432.524V28.6286H467.101V23.9814Z" fill="currentColor"/>\n<path d="M463.861 40.1396H432.524V61.3715H437.129V44.7441H463.861V40.1396Z" fill="currentColor"/>\n<path d="M481.553 23.9814H476.991V61.4143H481.553V23.9814Z" fill="currentColor"/>\n<path d="M219.779 23.9814H215.217V28.6286V40.1398V44.7017V44.7443H228.05V40.1398H219.779V28.6286H248.77V23.9814H219.779Z" fill="currentColor"/>\n<path d="M237.387 40.1396V44.7441H244.166V56.7243H215.217V61.3715H244.166H248.77V56.7243V44.7441V40.1396H244.166H237.387Z" fill="currentColor"/>\n<path d="M398.843 56.7245V23.9814H394.281V56.7245V61.3716H398.843H422.675V56.7245H398.843Z" fill="currentColor"/>\n<path d="M496.049 56.7245V23.9814H491.444V56.7245V61.3716H496.049H519.839V56.7245H496.049Z" fill="currentColor"/>\n<path d="M534.291 56.7245V23.9814H529.729V56.7245V61.3716H534.291H558.124V56.7245H534.291Z" fill="currentColor"/>\n<path d="M351.945 56.7245V23.9814H347.34V56.7245V61.3716H351.945H361.281V56.7245H351.945Z" fill="currentColor"/>\n<path d="M379.827 56.7245V23.9814H384.432V56.7245V61.3716H379.827H370.49V56.7245H379.827Z" fill="currentColor"/>\n</g>\n<defs>\n<clipPath id="sof-bf-clip0_1027_878">\n<rect width="86.3342" height="86.3342" fill="white"/>\n</clipPath>\n<clipPath id="sof-bf-clip1_1027_878">\n<rect width="439.132" height="38.3708" fill="white" transform="translate(120.868 23.9814)"/>\n</clipPath>\n</defs>\n</symbol><symbol id="sof-logo-suits" viewBox="0 0 175 48">\n<g clip-path="url(#sof-suits-clip0_1027_904)">\n<path d="M76.4708 31.3468C76.4708 37.1912 71.5664 40.9654 63.7113 40.9654C55.0981 40.9654 49.8813 36.5012 49.6938 29.8389H54.7232C55.2259 33.7351 57.9919 36.3762 63.6489 36.3762C68.1756 36.3762 71.0041 34.6155 71.0041 31.2219C71.0041 28.6461 69.3058 27.3256 65.472 26.6327L60.6954 25.8148C54.0331 24.6846 50.6367 21.8561 50.6367 17.0141C50.6367 11.607 54.9731 7.52051 62.6436 7.52051C70.314 7.52051 75.0281 11.4793 75.4683 18.0194H70.2515C69.8738 14.4355 67.2981 12.0472 62.5214 12.0472C58.1197 12.0472 56.0466 14.0578 56.0466 16.7614C56.0466 19.1497 57.617 20.5327 62.0188 21.2881L66.9232 22.1684C73.0828 23.3015 76.4793 26.3175 76.4793 31.3468H76.4708Z" fill="currentColor"/>\n<path d="M81.708 28.5804V8.46289H87.1151V27.3223C87.1151 33.357 89.3784 36.1855 93.9052 36.1855C99.3122 36.1855 102.706 32.099 102.768 23.8634V8.46289H108.175V40.0193H103.208V34.6775C101.26 38.889 97.739 40.965 93.0248 40.965C86.0473 40.965 81.7109 36.3758 81.7109 28.5804H81.708Z" fill="currentColor"/>\n<path d="M115.982 8.46289H121.389V40.0193H115.982V8.46289Z" fill="currentColor"/>\n<path d="M132.061 31.0309V13.2421H126.342V8.46546H129.798C131.431 8.46546 132.311 7.58511 132.311 5.95219V2.74316H137.341V8.46546H143.753V13.2421H137.403V33.3567C137.403 34.7397 137.968 35.2424 139.351 35.2424H144.696V40.019H141.552C135.14 40.019 132.059 36.6254 132.059 31.0309H132.061Z" fill="currentColor"/>\n<path d="M175.001 31.3468C175.001 37.1912 170.096 40.9654 162.241 40.9654C153.628 40.9654 148.411 36.5012 148.224 29.8389H153.253C153.756 33.7351 156.522 36.3762 162.179 36.3762C166.705 36.3762 169.534 34.6155 169.534 31.2219C169.534 28.6461 167.836 27.3256 164.002 26.6327L159.225 25.8148C152.563 24.6846 149.166 21.8561 149.166 17.0141C149.166 11.607 153.503 7.52051 161.173 7.52051C168.844 7.52051 173.558 11.4793 173.998 18.0194H168.781C168.404 14.4355 165.828 12.0472 161.051 12.0472C156.649 12.0472 154.576 14.0578 154.576 16.7614C154.576 19.1497 156.147 20.5327 160.549 21.2881L165.453 22.1684C171.613 23.3015 175.009 26.3175 175.009 31.3468H175.001Z" fill="currentColor"/>\n<path d="M34.2543 30.4834C34.2543 40.0934 26.4617 47.886 16.8517 47.886C8.74105 47.886 1.92258 42.3369 0 34.834L7.16494 27.6691C9.49361 30.8696 12.9071 33.238 16.8517 34.2519H16.8602L30.9089 20.2031C33.0076 23.0856 34.2543 26.6411 34.2543 30.4805V30.4834Z" fill="currentColor"/>\n<path d="M38.0632 13.0519L30.9096 20.2055C28.561 17.0164 25.1561 14.6451 21.2115 13.6313H21.203L7.16563 27.6686C5.0471 24.7862 3.81177 21.2392 3.81177 17.3998C3.80893 7.79255 11.6015 0 21.2115 0C29.3221 0 36.1406 5.54906 38.0632 13.0519Z" fill="currentColor"/>\n</g>\n<defs>\n<clipPath id="sof-suits-clip0_1027_904">\n<rect width="175" height="47.8855" fill="white"/>\n</clipPath>\n</defs>\n</symbol><symbol id="sof-logo-oc" viewBox="0 0 189 35">\n<g clip-path="url(#sof-oc-clip0_1027_913)">\n<path d="M72.6555 16.9254C72.6555 25.7309 66.5355 31.6976 57.5037 31.6976C48.4723 31.6976 42.3523 25.7338 42.3523 16.9254C42.3523 8.11713 48.4723 2.15332 57.5069 2.15332C66.5415 2.15332 72.6583 8.12006 72.6583 16.9254H72.6555ZM47.1817 16.9254C47.1817 23.6632 51.4686 27.5976 57.5037 27.5976C63.5392 27.5976 67.8686 23.6602 67.8686 16.9254C67.8686 10.1907 63.5813 6.21188 57.5037 6.21188C51.4262 6.21188 47.1817 10.1878 47.1817 16.9254Z" fill="currentColor"/>\n<path d="M91.0123 10.7988H95.3841V31.0887H91.0123V28.6134C89.4733 30.4802 87.1826 31.6972 84.0196 31.6972C78.3175 31.6972 74.7791 27.6799 74.7791 22.2834V10.7988H79.1509V22.3631C79.1509 25.6921 80.8991 27.8425 84.3954 27.8425C88.2248 27.8425 91.0151 25.2874 91.0151 20.9453V10.7988H91.0123Z" fill="currentColor"/>\n<path d="M106.66 27.9222V31.7767C101.582 32.0604 98.2947 29.8302 98.2947 24.5134V2.68164H102.667V10.7987H106.663V14.6535H102.667V24.6758C102.667 27.6798 104.496 27.9222 106.663 27.9222H106.66Z" fill="currentColor"/>\n<path d="M125.432 23.2139H129.761C129.137 28.3684 124.726 31.6942 118.939 31.6942C112.362 31.6942 107.908 27.3522 107.908 20.9394C107.908 14.5267 112.362 10.1846 118.939 10.1846C124.683 10.1846 129.095 13.4722 129.761 18.5853H125.389C124.641 15.7023 122.184 14.0393 118.939 14.0393C114.901 14.0393 112.071 16.5973 112.071 20.9394C112.071 25.2815 114.901 27.8367 118.939 27.8367C122.226 27.8367 124.684 26.1737 125.432 23.211V23.2139Z" fill="currentColor"/>\n<path d="M132.258 31.0892V10.7993H136.63V12.2999C138.378 10.3917 140.917 9.66209 144.165 10.4744L143.417 14.1254C138.672 13.3544 136.633 16.0335 136.633 20.9428V31.0892H132.261H132.258Z" fill="currentColor"/>\n<path d="M161.227 28.8144C159.647 30.5602 157.274 31.6942 154.069 31.6942C147.782 31.6942 143.328 27.3522 143.328 20.9394C143.328 14.5267 147.782 10.1846 154.069 10.1846C157.274 10.1846 159.647 11.3218 161.227 13.0645V10.7931H165.6V31.083H161.227V28.8114V28.8144ZM154.36 27.8426C158.438 27.8426 161.227 25.2875 161.227 20.9454C161.227 16.6033 158.441 14.0452 154.36 14.0452C150.279 14.0452 147.491 16.6033 147.491 20.9454C147.491 25.2875 150.321 27.8426 154.36 27.8426Z" fill="currentColor"/>\n<path d="M175.502 6.04942C174.298 6.04942 172.883 6.53683 172.883 8.84967V11.325H176.878V15.1797H172.883V31.0861H168.51V8.89103C168.51 5.19873 170.759 2.15332 174.837 2.15332C175.669 2.15332 177.418 2.27443 178.957 3.00698L177.333 6.33302C176.666 6.12917 175.999 6.04942 175.502 6.04942Z" fill="currentColor"/>\n<path d="M188.783 27.9222V31.7767C183.704 32.0604 180.418 29.8302 180.418 24.5134V2.68164H184.789V10.7987H188.786V14.6535H184.789V24.6758C184.789 27.6798 186.62 27.9222 188.786 27.9222H188.783Z" fill="currentColor"/>\n<path d="M34.4747 16.0364V18.5058V19.2885C27.7701 19.9472 19.7263 17.5517 16.5966 11.2127C15.7271 12.7339 14.9546 13.8121 14.0033 14.7307C13.0125 15.6878 11.8643 16.4351 10.2374 17.2976C11.8552 18.1572 13.0035 18.9045 13.9911 19.8557C14.9879 20.8186 15.7878 21.9587 16.7179 23.607C17.6753 21.8465 18.6145 20.4168 20.5262 18.9399C21.6229 19.6016 23.2044 20.3933 25.2556 21.0136L24.5768 21.3945C22.6559 22.4727 21.3351 24.1003 20.4595 25.979C19.3536 28.3509 18.9476 31.1244 18.9234 33.7325L18.9143 34.5951H18.0327H15.4272H14.5637L14.5395 33.7445C14.4062 28.9475 13.3609 25.4738 11.1765 23.1787C9.00426 20.8895 5.63525 19.708 0.848365 19.4717L0 19.4303V18.6061V18.6003V16.0038V15.995V15.1708L0.848365 15.1295C5.79887 14.8873 9.16483 13.6437 11.2977 11.3308C13.4427 9.00322 14.4092 5.53248 14.5395 0.856561L14.5637 0.00585938H15.4272H18.0327H18.9143L18.9234 0.868379C19.0113 10.6278 24.701 16.19 34.4747 15.0615V16.0393V16.0364Z" fill="currentColor"/>\n</g>\n<defs>\n<clipPath id="sof-oc-clip0_1027_913">\n<rect width="189" height="34.5923" fill="white"/>\n</clipPath>\n</defs>\n</symbol><symbol id="sof-logo-taza" viewBox="0 0 190 44">\n<g clip-path="url(#sof-taza-clip0_1033_675)">\n<path d="M16.9365 13.2761H10.5513V25.5405C10.5513 26.5917 10.7849 27.3704 11.2521 27.7987C11.7193 28.2659 12.4591 28.4995 13.3935 28.5774C14.3279 28.6163 15.4959 28.6163 16.8976 28.5384V33.4831C12.6537 33.9893 9.61685 33.6389 7.78693 32.3929C5.95702 31.147 5.02259 28.8499 5.02259 25.5016V13.2372H0.311523V7.9032H5.02259V2.37451L10.5513 0.739258V7.9032H16.8976V13.2761H16.9365Z" fill="currentColor"/>\n<path d="M40.3748 7.943H45.9035V33.484H40.3748V29.7852C38.2724 32.6664 35.3133 34.1459 31.4199 34.1459C27.9158 34.1459 24.8789 32.8221 22.3871 30.2524C19.8953 27.6438 18.6494 24.4512 18.6494 20.7135C18.6494 16.9369 19.8953 13.7442 22.3871 11.1356C24.8789 8.52702 27.8769 7.24219 31.4199 7.24219C35.3133 7.24219 38.3113 8.68276 40.3748 11.525V7.943ZM26.4752 26.5926C27.9937 28.15 29.9404 28.9287 32.2765 28.9287C34.6125 28.9287 36.5203 28.15 38.0777 26.5926C39.5961 25.0352 40.3748 23.0885 40.3748 20.7524C40.3748 18.4164 39.5961 16.4696 38.0777 14.9123C36.5592 13.3549 34.6125 12.5762 32.2765 12.5762C29.9404 12.5762 28.0326 13.3549 26.4752 14.9123C24.9568 16.4696 24.1781 18.4164 24.1781 20.7524C24.1781 23.0885 24.9179 25.0352 26.4752 26.5926Z" fill="currentColor"/>\n<path d="M93.1312 7.943H98.6599V33.484H93.1312V29.7852C91.0287 32.6664 88.0697 34.1459 84.1763 34.1459C80.6722 34.1459 77.6353 32.8221 75.1435 30.2524C72.6517 27.6438 71.4058 24.4512 71.4058 20.7135C71.4058 16.9369 72.6517 13.7442 75.1435 11.1356C77.6353 8.52702 80.6332 7.24219 84.1763 7.24219C88.0697 7.24219 91.0677 8.68276 93.1312 11.525V7.943ZM79.2705 26.5926C80.789 28.15 82.7357 28.9287 85.0717 28.9287C87.4078 28.9287 89.3156 28.15 90.873 26.5926C92.3914 25.0352 93.1701 23.0885 93.1701 20.7524C93.1701 18.4164 92.3914 16.4696 90.873 14.9123C89.3545 13.3549 87.4078 12.5762 85.0717 12.5762C82.7357 12.5762 80.8279 13.3549 79.2705 14.9123C77.7521 16.4696 76.9734 18.4164 76.9734 20.7524C76.9734 23.0885 77.7131 25.0352 79.2705 26.5926Z" fill="currentColor"/>\n<path d="M118.594 7.28027C122.099 7.28027 125.135 8.60404 127.627 11.1737C130.119 13.7823 131.365 16.9749 131.365 20.7127C131.365 24.4893 130.119 27.6819 127.627 30.2905C125.135 32.8991 122.137 34.184 118.594 34.184C114.701 34.184 111.703 32.7434 109.64 29.9012V43.7618H104.111V7.98109H109.64V11.6799C111.703 8.75978 114.701 7.28027 118.594 7.28027ZM111.937 26.5918C113.455 28.1491 115.402 28.9278 117.738 28.9278C120.074 28.9278 121.982 28.1491 123.539 26.5918C125.058 25.0344 125.836 23.0877 125.836 20.7516C125.836 18.4155 125.058 16.4688 123.539 14.9114C122.021 13.354 120.074 12.5754 117.738 12.5754C115.402 12.5754 113.494 13.354 111.937 14.9114C110.418 16.4688 109.64 18.4155 109.64 20.7516C109.601 23.0877 110.379 25.0344 111.937 26.5918Z" fill="currentColor"/>\n<path d="M155.66 7.943H161.189V33.484H155.66V29.7852C153.558 32.6664 150.599 34.1459 146.705 34.1459C143.201 34.1459 140.164 32.8221 137.672 30.2524C135.18 27.6438 133.935 24.4512 133.935 20.7135C133.935 16.9369 135.18 13.7442 137.672 11.1356C140.164 8.52702 143.162 7.24219 146.705 7.24219C150.599 7.24219 153.596 8.68276 155.66 11.525V7.943ZM141.76 26.5926C143.279 28.15 145.226 28.9287 147.562 28.9287C149.898 28.9287 151.805 28.15 153.363 26.5926C154.881 25.0352 155.66 23.0885 155.66 20.7524C155.66 18.4164 154.881 16.4696 153.363 14.9123C151.844 13.3549 149.898 12.5762 147.562 12.5762C145.226 12.5762 143.318 13.3549 141.76 14.9123C140.242 16.4696 139.463 18.4164 139.463 20.7524C139.463 23.0885 140.242 25.0352 141.76 26.5926Z" fill="currentColor"/>\n<path d="M183.887 7.94238H189.766L179.916 34.3399C177.463 40.9588 173.297 44.0735 167.418 43.7621V38.5838C169.17 38.7006 170.571 38.3112 171.623 37.4936C172.674 36.676 173.569 35.3522 174.231 33.6002L174.504 33.094L163.641 7.98132H169.676L177.307 26.553L183.887 7.94238Z" fill="currentColor"/>\n<path d="M66.0715 7.94238L62.3728 13.1596L59.9199 16.5858C58.674 18.2989 59.9199 20.6739 62.0224 20.6739C62.8789 20.6739 63.6576 20.2846 64.1248 19.5838L69.8482 11.6022L72.4957 7.94238H66.0715Z" fill="currentColor"/>\n<path d="M50.8872 7.94238V13.1596H62.3729L66.0716 7.94238H50.8872Z" fill="currentColor"/>\n<path d="M57.8955 28.305L58.5963 27.2927L60.3873 24.8009C61.6332 23.0878 60.3873 20.6738 58.2459 20.6738C57.3894 20.6738 56.6107 21.0632 56.1435 21.764L50.3422 29.8234L47.6558 33.5222H54.2746L57.8955 28.305Z" fill="currentColor"/>\n<path d="M70.3545 28.3057H57.9344L54.3135 33.5229H70.3545V28.3057Z" fill="currentColor"/>\n</g>\n<defs>\n<clipPath id="sof-taza-clip0_1033_675">\n<rect width="190" height="43.9959" fill="white"/>\n</clipPath>\n</defs>\n</symbol><symbol id="sof-logo-s" viewBox="0 0 185.320343 64"><image width="185.320343" height="64" href="data:image/png;base64,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"/></symbol><symbol id="sof-logo-whop" viewBox="0 0 160.53 35.2"><g fill="currentColor"><g transform="translate(0,-0.0002)"><path d="M 8.52681856647827 0 C 5.001946324082972 0 2.5720518411312105 1.5559801690209518 0.7332123118528703 3.3155434576518443 C 0.7332123118528703 3.3155434576518443 -0.009293641885952863 4.023431570356628 0.00008816359773144247 4.044998805555587 L 7.722690354200971 11.814081192016602 L 15.443855285644531 4.044998805555587 C 13.981713587400503 2.0198044223657416 11.224801281920492 0 8.52681856647827 0 Z"/></g><g transform="translate(9.5477,-0.0002)"><path d="M 18.04796941444083 0 C 14.523129059464534 0 12.093173479311789 1.5559802326201533 10.25430232842727 3.3155435931715127 C 10.25430232842727 3.3155435931715127 9.576188166506522 4.0045478660930485 9.545407899734426 4.045004189442738 L 0 13.649163700569368 L 7.710589355345764 21.406108856201172 L 24.96506118774414 4.045004189442738 C 23.502761700784166 2.0198045049233166 20.747320059466805 0 18.04796941444083 0 Z"/></g><g transform="translate(19.0954,-0.0002)"><path d="M 27.621530195880354 0 C 24.09658406044985 0 21.666785296851213 1.5559802112673125 19.827914038946638 3.3155435476720436 C 19.827914038946638 3.3155435476720436 19.121543974330297 4.00994097725285 19.09481512389815 4.0449989153812025 L 0 23.25734398732633 L 2.0211321826648194 25.290629789790586 C 5.148039317461519 28.43637330909815 10.266455727572225 28.43637330909815 13.393362862368926 25.290629789790586 L 34.51431194991126 4.0449989153812025 L 34.53851318359375 4.0449989153812025 C 33.07637147271514 2.0198044772053785 30.320775623405957 0 27.621530195880354 0 Z"/></g><g transform="translate(61.8762,4.0439)"><path d="M 5.881400484878955 23.58901596069336 L 0 0 L 5.247377006209757 0 L 9.190411629123712 16.326975836294437 L 9.257228354700587 16.326975836294437 L 14.938692489441838 0 L 19.44997436429878 0 L 25.131432076207616 16.326975836294437 L 25.1982552246169 16.326975836294437 L 29.17495833503196 0 L 34.3886604309082 0 L 28.506213024346174 23.58901596069336 L 23.159917976166845 23.58901596069336 L 17.210640998363115 7.820309539247498 L 17.144871194469317 7.820309539247498 L 11.161925729164484 23.58901596069336 L 5.881400484878955 23.58901596069336 Z"/></g><g transform="translate(97.8723,4.0439)"><path d="M 0 0 L 4.945362638228855 0 L 4.945362638228855 7.820309347566578 L 5.012712459681318 7.820309347566578 C 5.449423972664757 7.011340731599649 6.313900745653753 6.368163891570198 7.3262295669500945 5.932662520514136 C 8.264370056617585 5.528151893970385 9.625538064121088 5.271965484367311 10.827810113392005 5.265230655894984 C 12.151098563096104 5.258495827422657 13.98054996827539 5.600972339581772 15.27226889167095 6.273771133185898 C 16.586086473446812 6.9911355538778315 17.578949044293083 7.955162740131231 18.246644079131116 9.164590555155058 C 18.959588771689948 10.420004647560013 19.3158016204834 11.83163577850949 19.3158016204834 13.401166429083414 L 19.3158016204834 23.587753295898438 L 14.370438982254543 23.587753295898438 L 14.370438982254543 14.072492135987165 C 14.370438982254543 12.683749571984425 13.957404087129532 11.60775630565361 13.133439982367474 10.844668692826659 C 12.308949707125318 10.082791282167491 11.183494533678314 9.701272815835894 9.757078978080553 9.701272815835894 C 8.33118959296289 9.701272815835894 7.1946912622663275 10.104467689989626 6.281806353502965 10.91206829278381 C 5.3904939326398065 11.718300882405247 4.945362638228855 12.772775551918892 4.945362638228855 14.072492135987165 L 4.945362638228855 23.587753295898438 L 0 23.587753295898438 L 0 0 Z"/></g><g transform="translate(118.9108,9.3132)"><path d="M 0 9.413973727883137 C 0 8.002343223701779 0.2667613204798306 6.713308033506755 0.8013383095838494 5.548340591653814 C 1.3359152986878682 4.383425837098908 2.0651760769749865 3.391038399769819 2.990162648707803 2.5725989299350793 C 3.914623049936063 1.7541594601003396 4.979036475764983 1.1217691261942047 6.18130858092285 0.6727981295474311 C 7.38463302708983 0.2251425089298808 8.653723065990874 0 9.99174405026459 0 C 11.32923886403375 0 12.670955285364354 0.23056232583277336 13.884802840552169 0.6889515533411112 C 15.099176566244541 1.148761431117984 16.157799707961047 1.787885703496757 17.060161449781763 2.604957160182618 C 17.961997021097922 3.4233966300173577 18.67494947426829 4.409049526733259 19.19900330417309 5.563283311517034 C 19.72200479306878 6.7174118220614965 19.984554290771484 8.00092327593055 19.984554290771484 9.412711641292498 C 19.984554290771484 10.824394732415135 19.716214508956366 12.141737754098298 19.183215981187633 13.29586626464276 C 18.64811282157906 14.449994775187221 17.924642929544927 15.43701417970063 17.0107056373375 16.254085636386492 C 16.096242274982284 17.07252510622123 15.0333944146447 17.704865211569906 13.819546859456885 18.153888845336336 C 12.605173133764513 18.60164969001482 11.329239867601373 18.826738357543945 9.992797394841325 18.826738357543945 C 8.656354922081277 18.826738357543945 7.347279838747696 18.59612269209421 6.132906113055324 18.137680827466216 C 4.918532387362953 17.677976173750277 3.859896901764687 17.03353685692413 2.9580613304485284 16.204205919018015 C 2.0556995886278138 15.375032842292487 1.3374948137691591 14.38396123259803 0.8023916541605843 13.228412071785034 C 0.2678146650565655 12.074283561240572 0.0010533445767348859 10.802874831335524 0.0010533445767348859 9.412711641292498 L 0 9.413973727883137 Z M 15.038664750371817 9.413973727883137 C 15.038664750371817 7.890376693972329 14.576691964852897 6.668847581079 13.65170539312008 5.74928051282329 C 12.726718821387264 4.83108140753808 11.507607654375406 4.37127142940445 9.992797394841325 4.37127142940445 C 9.257227889407934 4.37127142940445 8.577431654603393 4.495339754797891 7.954460027869191 4.740740053127553 C 7.329909939799702 4.987508364606093 6.794807281974939 5.328563405907144 6.35020339183639 5.766853382604407 C 5.9040210403625535 6.203617484972202 5.559390298765383 6.736247882357593 5.314200463620919 7.3632708859453535 C 5.069010628476455 7.991504041501405 4.946942884976402 8.673826629538913 4.946942884976402 9.413973727883137 C 4.946942884976402 10.154331274349225 5.069010628476455 10.83244374584672 5.314200463620919 11.448680505424038 C 5.559390298765383 12.06486467806008 5.910337494979521 12.59749502526709 6.365990714821843 13.045098008764985 C 6.823222395999452 13.494121642531415 7.356746592488929 13.840598482781331 7.9702473508546445 14.087314182229406 C 8.58269581838963 14.334135105738413 9.257227889407934 14.4567298175842 9.992797394841325 14.4567298175842 C 10.728893070779273 14.4567298175842 11.40658467374397 14.334135105738413 12.031134761813458 14.087314182229406 C 12.654632559052216 13.840598482781331 13.189209548156235 13.49943653644365 13.635918070134627 13.061304420926975 C 14.080521960273176 12.62438245737859 14.426217336582836 12.091857334232513 14.6714071717273 11.464886917586028 C 14.91712317737632 10.837916500939544 15.038664750371817 10.154331274349225 15.038664750371817 9.413973727883137 Z"/></g><g transform="translate(140.6827,9.3028)"><path d="M 0 0 L 4.745946437868984 0 L 4.745946437868984 2.5618126916044424 L 4.81329625794035 2.5618126916044424 C 5.122151248272618 1.8876458686846138 6.428071880548434 0.763140619469623 7.452502300809442 0.46112567431968476 C 8.476932721070451 0.15905809204791216 9.512942805569692 0.006735143032512537 10.561050395165761 0.006735143032512537 C 11.897492778396504 0.006735143032512537 13.122396254955556 0.2534505014437843 14.23785215927166 0.7469345077071172 C 15.350677211241225 1.2404185139704502 16.31459586986162 1.9132702618768977 17.128036799232945 2.7640684989585482 C 17.942530019364504 3.616182112123867 18.574969913002118 4.61262129409405 19.032727734018735 5.756068882196077 C 19.490485555035352 6.8993586091109815 19.717260360717773 8.120940760935403 19.717260360717773 9.420815237312574 C 19.717260360717773 10.720531852502624 19.488907093805807 12.009566594268584 19.032727734018735 13.15301418237061 C 18.574969913002118 14.296303909285514 17.94095155813496 15.287375610180018 17.128036799232945 16.128702978888438 C 16.31459586986162 16.96871497151319 15.34646433500032 17.630728289446335 14.22101149283764 18.1121106751691 C 13.09555865067496 18.593545647835317 11.875395726177453 18.83484314607623 10.562630411925017 18.83484314607623 C 10.138546698090039 18.83484314607623 9.665530284712148 18.795696751724844 9.14200266038342 18.717562219363938 C 8.616896574825148 18.639269838360505 8.106523914726399 18.520723695128808 7.604042607386195 18.364296781764473 C 7.1026136409846075 18.207869868400138 6.6227545527652065 18.011034154154355 6.16762753391675 17.776472702156816 C 5.710395883369442 17.54049062492113 5.325252522552366 17.266784415641887 5.014819045901365 16.95250996367507 L 4.947469225829998 16.95250996367507 L 4.947469225829998 25.896099090576172 L 0.0026333612654263166 25.896099090576172 L 0.0026333612654263166 0 L 0 0 Z M 14.770844479393945 9.420815237312574 C 14.770844479393945 7.897218140338216 14.313610771533147 6.681002867448901 13.400725881489697 5.773537381671749 C 12.48678865050763 4.8660718958945965 11.271889437838311 4.411733048340017 9.757605450251837 4.411733048340017 C 9.22302849695954 4.411733048340017 8.673197567716723 4.502074406489885 8.10494645706441 4.680021196735375 C 7.536695346412095 4.859336000186367 7.018953941359284 5.116838732068114 6.551199082139335 5.453948462088945 C 6.082391932159148 5.789742790936918 5.698826530787841 6.194253452255888 5.397863921870864 6.664796956399919 C 5.098479774183432 7.135340460543951 4.945889209070742 7.673336855699809 4.945889209070742 8.278787396327022 L 4.945889209070742 10.53174532764592 C 4.945889209070742 11.31656330884596 5.174244031512421 12.000148212482042 5.632001852529037 12.58260561386812 C 6.086602751086565 13.165115652376032 6.661690816245321 13.614139505441624 7.352010665787832 13.926835470983175 C 8.065481514196097 14.285622913983092 8.877349552137808 14.464832819528276 9.791286783119874 14.464832819528276 C 11.28347211277921 14.464832819528276 12.48678865050763 13.99976121767111 13.400725881489697 13.069355179596277 C 14.313610771533147 12.138949141521444 14.770844479393945 10.92289172981925 14.770844479393945 9.422077323955452 L 14.770844479393945 9.420815237312574 Z"/></g></g></symbol></svg>'


def marquee_html():
    """Two identical sequences. The second is aria-hidden: it exists only so
    the loop has something to scroll into, and a screen reader meeting each
    sponsor twice would be reading a rendering trick aloud."""
    seq = "".join(
        '<svg class="sof-marq-logo sof-marq-logo--%s" role="img"'
        ' aria-label="%s"><use href="#sof-logo-%s"/></svg>' % (k, label, k)
        for k, label in (("bf", "BestFulfill"), ("suits", "Suits Finance"),
                         ("oc", "Outcraft"), ("taza", "Tazapay"),
                         ("s", "Slash"), ("whop", "Whop")))
    hidden = seq.replace(' role="img"', ' aria-hidden="true"')
    for label in ("BestFulfill", "Suits Finance", "Outcraft",
                  "Tazapay", "Slash", "Whop"):
        hidden = hidden.replace(' aria-label="%s"' % label, "")
    return (
        '%s'
        '<div class="sof-marq-win">'
        '<div class="sof-marq-track">'
        '<div class="sof-marq-seq">%s</div>'
        '<div class="sof-marq-seq" aria-hidden="true">%s</div>'
        '</div>'
        '</div>'
    ) % (LOGO_DEFS, seq, hidden)


# ------------------------------------------- 9c | who it's for, and the FAQ
# (name node, role node, photo key or None)
# Gonzalo's name sits in TWO nodes in the frame, 909:2921 "Gonzalo " and
# 909:2919 the full name, because the card splits it over two lines and the
# second line's node still holds the whole string. 909:2917 is a third copy and
# is visible:false. The full name is used once here and allowed to wrap, which
# is what the card does anyway.
# NAME/ROLE OVERRIDES: none left, and that is the point.
#
# Between 2026-10-09 and 2026-10-10 this file carried four: three roles Joshua
# corrected, and Dara Denney's name typed into a plate that still read "TBA".
# The designer has since put all four in Figma, so copy comes from node ids
# again and nothing here is retyped.
#
# The remap onto frame 904:108 checked each of the three roles against the
# value we had been overriding it to, NOT against the old text -- the old text
# was gone by design, so matching on it could only ever fail. Passing that
# check is what proves Figma caught up rather than merely changed.
#
# Dara still fills the FIRST of the two TBA plates rather than becoming an
# eleventh card: the grid is five across and ten deep, and a TBA plate is a
# reserved seat. She has a photograph and an affiliation now, so nothing about
# her card is special any more, which is why her row looks like the other eight.
#
# ⚠️ THE TRAP, IF A PLATE IS EVER RESEATED AGAIN. The remap resolves node ids
# by their TEXT, and a plate reading "TBA" / "Announced soon" is
# indistinguishable from every other plate reading the same. Dara's row and the
# last TBA row both resolved onto the single remaining TBA plate, and the page
# went out carrying two identical cards before this was caught. The assert in
# speakers_html is there so that is a build failure next time, not a deploy.


def speaker_name(node_id):
    """The speaker's name, with the frame's own line break kept.

    Gonzalo's plate is a single node containing a hard newline --
    "GONZALO
FERNANDEZ" -- because the card breaks his name over two lines.
    T() would hand that to HTML, where whitespace collapses and the two lines
    become one, which is a reflow the designer did not ask for. Tbr keeps it.
    """
    return Tbr(node_id)


# V2 reorders the grid, drops the last TBA plate and adds Jay Cruiz, so all ten
# seats are now named people.
#
# ROLE_OVERRIDES IS GONE, 2026-10-15, on Joshua's call: follow the frame.
#
# It existed because three affiliations he corrected on 2026-10-10 kept
# arriving wrong -- the frame was repeatedly branched from a copy that
# predated the correction, so "Super Tan Brothers", "Founder of Obvi" and
# "Brand Owner - $600K+ Days" came back four pastes running and had to be
# re-pointed at the new node ids each time.
#
# The dict is deleted rather than emptied. An empty override table is an
# invitation to refill it, and the point of this change is that the frame is
# the source of truth for a speaker's affiliation again. If one is wrong, it
# is wrong in Figma and that is where it gets fixed.


# Topi's wording, given 2026-10-14, not yet in Figma. Keyed by node id and
# applied over the frame's text, so design_diff will correctly report each as
# RETYPED until the designer applies it at source. Both frames carry the same
# copy, so each edit is two ids.
#
# This is the LAST override table on the page. The speakers' one was deleted on
# 2026-10-15 because the frame became the source of truth for affiliations;
# these three are here only until the copy changes land in Figma, and they
# should go the same way.
#
#   "GET ANSWER"  -> "GET ANSWERS"      plural, it is a list of questions
#   "open up"     -> "break down"       what the session actually does
#   "funnels and" -> "funnels, and"     the serial comma Topi asked for
COPY_EDITS = {
    # Eline, 2026-10-21: Day 3 stays but is invite only, not a VIP tier you
    # buy. Desktop and mobile carry the chip separately.
    "949:1436": "DAY 3 \u00b7 INVITE ONLY",
    "949:1935": "DAY 3 \u00b7 INVITE ONLY",
    # Topi, 2026-10-23: the card said $400M+ and the bio said $350M+ -- the
    # same claim, two numbers. Joshua's call: $500M+ everywhere. The matching
    # bio figure is fixed in scratchpad/sync_v2.py so a re-sync keeps it.
    "949:1268": "$500M+ a year on Amazon",   # Phil Li
    "949:1274": "$500M+ a year on Amazon",   # Shawn He
    # Joshua, 2026-10-24: "Jay Cruiz not Cruz". The Figma card says CRUZ and
    # the planner sheet says Cruiz; the sheet is right. This overrides the
    # card and the modal heading, which read the same node. The bio spells it
    # from the sheet, so removing the old fix in sync_v2.py covers that side.
    "949:1281": "JAY CRUIZ",
    # ...and his new tagline, same request. Middot to match the other cards.
    "949:1280": "AEO That Works · 9 Figure Traffic",
    # Joshua, 2026-10-24: drop the VIP day from the intro. Day 3 is invite
    # only, so the event is two days you can buy; the ticker already says so.
    "949:1412": ("Two days in the room. Every block is built to send you "
                 "home with something you can ship on Monday."),
    "949:1911": ("Two days in the room. Every block is built to send you "
                 "home with something you can ship on Monday."),
    # ...and the Day 3 slot stops promising VIPs. "Invited operators" rather
    # than Joshua's "selected individuals", which he asked to be phrased
    # better -- it matches the DAY 3 . INVITE ONLY chip directly above it.
    "I949:1439;255:526": "Small rooms with the speakers and invited operators.",
    "I949:1938;255:526": "Small rooms with the speakers and invited operators.",
    # V2 ticket card, 2026-10-25. Badge 1 loses its suffix (the card
    # already says EARLY BIRD in 88px underneath it) and badge 2 becomes
    # the deadline the countdown bar counts to. Keep this date and
    # COUNTDOWN_ENDS in step or the page contradicts itself.
    # GENERAL ADMISSION, 2026-10-31. Early Bird ended at 23:59:59 US Pacific
    # on 30 October and the live page was rewritten in place by
    # funnels/sof/scaling-or-failing/edits/bake_general_admission.py. These
    # overrides exist so a REBUILD produces the same page instead of quietly
    # restoring Early Bird pricing. The "ENDS OCT 30" pill (949:1473) and the
    # struck-through compare price (949:1475) are gone from ticket_html
    # entirely, so their keys are no longer read.
    # The eyebrow is "OUR PARTNERS" in the new frame (1027:871).
    "949:1513": "OUR PARTNERS",
    "949:1457": "FINAL PRICE",
    "949:1458": "FULL ACCESS PASS",
    "949:1459": "$2997",
    "949:1471": "SECURE YOUR SEAT  →",
    # ⚠️ THE HERO BUTTON IS TWO NODES, ONE PER BREAKPOINT, AND ONLY THE
    # MOBILE ONE WAS OVERRIDDEN AT FIRST. The live page was right anyway,
    # because the 2026-10-31 bake matched on the button TEXT and caught all
    # three buttons; the builder did not, so a rebuild quietly put "GET
    # EARLY BIRD TICKET" back on desktop. Caught only because the rebuild
    # went to a throwaway step first. 949:1558 is mobile, 949:1121 desktop.
    "949:1121": "SECURE YOUR SEAT  →",
    "949:1558": "SECURE YOUR SEAT  →",
    # Eline, 2026-10-31, on the red bar at the top. Read off her
    # screenshot, so the middle separator is the one character I am not
    # certain of; the page uses · everywhere else ("DAY 3 · INVITE
    # ONLY", "BANGKOK · DEC 7-8, 2026") so it follows the house style.
    "949:1090": "2 DAYS BEFORE AFFILIATE WORLD BANGKOK · LIMITED SPOTS",
    "949:1369": "GET ANSWERS TO YOUR EXACT QUESTIONS.",
    "949:1826": "GET ANSWERS TO YOUR EXACT QUESTIONS.",
}
_FORMAT2 = ("A select few speakers take the stage solo to break down one "
            "system that\u2019s working right now. The exact creatives, "
            "funnels, and margins behind it. Shown for the first time, in "
            "this room only.")
COPY_EDITS["949:1364"] = _FORMAT2
COPY_EDITS["949:1821"] = _FORMAT2

for _nid, _txt in COPY_EDITS.items():
    assert _nid in _TEXT, "COPY_EDITS points at a node the frames do not have: %s" % _nid
    assert _TEXT[_nid] != _txt, (
        "COPY_EDITS still overrides %s but the frame now matches it -- delete "
        "the entry rather than carrying a no-op override" % _nid)
    _TEXT[_nid] = _txt


SPEAKERS_V2 = [
    # (name node, role node, photo key, size class, is-TBA)
    #
    # Grid order, read off the frame scan of 921:1304 rather than matched on
    # text: the 2026-10-15 paste rewrote every name and most roles, so there
    # was nothing to match on. Matching speakers on text is what once put two
    # identical Dara Denney cards live.
    #
    # The size-class column is empty for every row now. V4 sized four names
    # down per card so a long one would hold a line in a 336px card; V4.5
    # uppercases them all at a single 28px and the problem goes away.
    ("949:1235", "949:1234", "spk_steve", "", False),
    ("949:1241", "949:1240", "spk_alex", "", False),
    ("949:1247", "949:1246", "spk_joshua", "", False),
    ("949:1252", "949:1251", "spk_ronak", "", False),
    ("949:1257", "949:1256", "spk_dara", "", False),
    ("949:1263", "949:1262", "spk_jem", "", False),
    ("949:1269", "949:1268", "spk_phil", "", False),
    ("949:1275", "949:1274", "spk_shawn", "", False),
    ("949:1281", "949:1280", "spk_jay", "", False),
    ("949:1286", "949:1285", "spk_gonzalo", "", False),
    # Barry Hott and Dee Deng took the first two open seats on 2026-10-21.
    # Their photos are NODE RENDERS, not image fills: both rectangles use
    # scaleMode CROP, so the raw fill is not what the card shows.
    ("949:1292", "949:1291", "spk_barry", "", False),
    ("949:1298", "949:1297", "spk_dee", "", False),
    # The three "Announcing soon" seats were REMOVED on 2026-10-22 (ClickUp
    # z941abzgdq). There are twelve speakers and the other three were never
    # going to be filled, so the grid is twelve cards in 4 x 3 rather than
    # fifteen in 5 x 3. The is-TBA column and its rendering stay: they cost
    # nothing and the frame still draws the placeholders.
]

# Speaker bios for the modal, keyed by the photo key in SPEAKERS_V2.
# Each value is a list of paragraphs -- a short highlight reel, not a CV.
#
# EMPTY ON PURPOSE. Eline is researching these. A speaker with no entry here
# renders exactly as before: no info button, no photo trigger, no modal. Add
# an entry and that speaker turns on; nothing else needs touching.
#
#   SPEAKER_BIOS = {
#       "spk_steve": [
#           "First paragraph.",
#           "Second paragraph.",
#       ],
#   }
#
# Gonzalo (spk_gonzalo) is the one nobody can source from a search -- his has
# to come from him or from his intake form.
# Pulled from the event planner, Speakers tab: "Short Bio (for website/intro)",
# "Linkedin" and "Other Links (IG / Website)".
# docs.google.com/spreadsheets/d/1S-qa8tfOxb9BeOdVIc0C8ADd226eSzV2XfbiiB47iVw
# (gid 180332380). Last synced 2026-10-23. READ ONLY -- never written back.
#
# Regenerated wholesale by scratchpad/sync_v2.py, never edited by hand, so a
# later pass cannot half-apply it.
#
# Eline pasted each speaker's LinkedIn, Instagram and company URL onto their
# own lines at the end of the BIO cell. Those lines are harvested into
# SPEAKER_LINKS and removed from the prose; a URL inside a SENTENCE is left
# alone, because cutting it would gut the sentence.
#
# Mechanical fixes on the way through: the stray scheme in Jay's
# "http://Ampifire.com", and Phil's and Shawn's $350M+ -> $500M+ (Topi flagged
# it against their $500M+ cards). The "Jay Cruiz" -> "Jay Cruz" rename was
# REMOVED on 2026-10-24 -- the sheet was right, the Figma card was wrong, and
# the card is overridden in COPY_EDITS instead.
SPEAKER_BIOS = {
    "spk_steve": [
        "$100M+ in ecom sales. Steve Tan and his brother Evan turned "
        "that into Super Tan Brothers Group, a stack of ecommerce, "
        "software, education, logistics and marketing companies with "
        "400+ people across six countries. He built eCommerce Elites "
        "Mastermind into a 100,000+ member community along the way. Now "
        "he is all-in on AI, and he is showing operators what actually "
        "works.",
    ],
    "spk_alex": [
        "Alex Fedotoff has built and sold two ecommerce businesses, "
        "both in 7 to 8 figure acquisitions. Then he did it again at "
        "scale: an eight-figure ecom portfolio and an education company "
        "for the next wave of founders, run out of Miami. He has worked "
        "with 1,000+ DTC founders and says his Facebook ads strategy "
        "has added over $100M in revenue. There is a reason they call "
        "him the Godfather of Ecom.",
    ],
    "spk_joshua": [
        "Joshua Chin runs Chronos, the Singapore agency behind email, "
        "SMS and push for 500+ DTC brands. His team has driven $400M+ "
        "in attributed revenue, across beauty, wellness, apparel and "
        "home goods. If your owned channels are leaving money on the "
        "table, this is the guy who finds it.",
    ],
    "spk_ronak": [
        "Ronak Shah is the founder of Obvi and the man they call \u201cThe "
        "DTC Plumber.\u201d He advises and invests in 25+ DTC brands out of "
        "New York, and he knows where the leaks are. His new project is "
        "AI infrastructure, built under RONSHAH.CO.",
    ],
    "spk_dara": [
        "Performance Creative Expert and Ad Agency Owner.",
        "Dara Denney is a performance creative expert and ad agency "
        "owner who went from humanitarian work to education to the top "
        "of paid creative. Her YouTube channel gives away her creative "
        "strategy for free, which tells you how deep the playbook goes. "
        "Her team runs creative testing and AI-assisted production for "
        "brands that want to win on the ad, not just the media buy. New "
        "York built her, and the DTC world watches what she posts.",
    ],
    "spk_jem": [
        "Google Ads for High-Growth DTC Brands",
        "Jem Bourouh runs Adcubator, the Dubai Google Ads agency DTC "
        "brands call when the account needs a rebuild. His team manages "
        "nine figures a year in ad spend for brands like BR\u0112Z, Hey "
        "Shape, Calming Co and Eskiin, across Search, Shopping, PMAX "
        "and YouTube. The agency also runs its own ecommerce brands, so "
        "the advice comes from people who pay their own ad bills. He "
        "has keynoted at OMR, and he is the King of Google Ads for a "
        "reason.",
    ],
    "spk_phil": [
        "180+ brands launched to Amazon. $500M+ in Amazon sales",
        "Phil Li has launched 180+ brands on Amazon and generated "
        "$500M+ in Amazon sales. He runs Black Compass Digital out of "
        "Toronto, where his team adds millions in revenue for ecommerce "
        "brands like Goda, Luxe Cosmetics, Cupids and KittySpout. Phil "
        "knows how to turn Amazon into a growth channel, not a side listing. "
        "Come hear how he does it.",
    ],
    "spk_shawn": [
        "Shawn He is the co-founder of Black Compass Digital in "
        "Toronto, and his team has driven $500M+ in incremental revenue "
        "for DTC brands on Amazon and in retail. He takes 7, 8 and 9 "
        "figure brands into Amazon, Walmart, Target and Costco, and his "
        "team pulled in $60M in a single Black Friday and Cyber Monday "
        "weekend. Before Black Compass, he built brands and exited "
        "them.",
    ],
    "spk_jay": [
        "Jay Cruiz is a world-renowned expert in AI-powered organic "
        "traffic for ecommerce and a keynote speaker. As co-creator of "
        "AmpCast AI by Ampifire.com, he helps brands dominate ChatGPT, "
        "Google, YouTube, and social search with AI-generated content "
        "published across 300+ high-authority sites. His clients see "
        "5-50x ROCS and massive organic growth, including scaling one "
        "brand to 60,000+ monthly organic clicks.",
    ],
    "spk_gonzalo": [
        "Gonzalo Martin built a DTC craft kit brand that hit $600K+ "
        "days just eight months after launch. Every order comes with "
        "guided lessons, and he has turned buyers into a community that "
        "keeps coming back. He built a brand that scales, and you can "
        "hear exactly how in Bangkok.",
    ],
    "spk_barry": [
        "Barry Hott is the founder of Hott Growth and has managed over "
        "$600M in paid media since 2008. He is famous for ugly ads that "
        "convert, and he builds creative testing systems from first "
        "principles, not from trends. He helped launch Lone River Ranch "
        "Water, which Diageo acquired in 2021. These days he is also "
        "building URL Love It, a website change monitor.",
    ],
    "spk_dee": [
        "Dee Deng is the CEO of Right Hook Digital, based in Brisbane, "
        "Australia. Growth marketer, coach and investor, he helps 7 to "
        "8 figure brands uncap their growth. He has seen what the next "
        "level looks like, and he knows how to get you there.",
    ],
}

# Label is read off the host. Known networks get their name; anything
# else gets its bare domain rather than a vague "Website", because Alex
# has two non-social links and one of each would be indistinguishable.
SPEAKER_LINKS = {
    "spk_steve": [
        ("LinkedIn", "https://www.linkedin.com/in/heystevetan/"),
        ("Instagram", "https://www.instagram.com/heystevetan/?hl=en"),
        ("supertanbros.com", "https://www.supertanbros.com/"),
    ],
    "spk_alex": [
        ("LinkedIn", "https://www.linkedin.com/in/alex-fedotoff"),
        ("alexfedotoff.com", "https://www.alexfedotoff.com/"),
        ("Instagram", "https://www.instagram.com/alexfedotofff/?hl=en"),
        ("gethookd.ai", "https://www.gethookd.ai/"),
    ],
    "spk_joshua": [
        ("LinkedIn", "https://www.linkedin.com/in/joshua-chin-jl/"),
        ("Instagram", "https://www.instagram.com/joshchinn/?hl=en"),
        ("chronos.agency", "https://chronos.agency/about-us/"),
    ],
    "spk_ronak": [
        ("LinkedIn", "https://www.linkedin.com/in/ronak06/?isSelfProfile=false"),
        ("ronshah.co", "https://www.ronshah.co/"),
    ],
    "spk_dara": [
        ("LinkedIn", "https://www.linkedin.com/in/daradenney/"),
        ("YouTube", "https://www.youtube.com/watch?v=-E9sjb2msjo"),
    ],
    "spk_jem": [
        ("LinkedIn", "https://www.linkedin.com/in/jem-bourouh/?isSelfProfile=false"),
        ("Instagram", "https://www.instagram.com/jembourouh/?hl=en"),
        ("X", "https://x.com/JemBourouhDE"),
        ("adcubator.com", "https://adcubator.com/"),
    ],
    "spk_phil": [
        ("LinkedIn", "https://www.linkedin.com/in/philipli1/"),
        ("Instagram", "https://www.instagram.com/philipjhli/"),
        ("blackcompass.digital", "https://www.blackcompass.digital/"),
    ],
    "spk_shawn": [
        ("LinkedIn", "https://www.linkedin.com/in/heshawn/"),
        ("blackcompass.digital", "https://www.blackcompass.digital/"),
    ],
    "spk_jay": [
        ("LinkedIn", "https://www.linkedin.com/in/jay-cruiz-745270108/"),
        ("Instagram", "https://www.instagram.com/jaycruiz_/"),
        ("ampifire.com", "https://ampifire.com/"),
    ],
    "spk_barry": [
        ("LinkedIn", "https://www.linkedin.com/in/binghott/"),
        ("buildingadswithbarry.com", "https://www.buildingadswithbarry.com/"),
        ("Instagram", "https://www.instagram.com/binghott/?hl=en"),
        ("hottgrowth.com", "https://www.hottgrowth.com/"),
    ],
    "spk_dee": [
        ("LinkedIn", "https://www.linkedin.com/in/deedeng/?isSelfProfile=false"),
        ("Instagram", "https://www.instagram.com/yo.uncledee/"),
        ("righthookdigital.com", "https://righthookdigital.com/"),
    ],
}

# Shown for any speaker with no entry above. ON while the remaining bios are
# still being researched, so every card has a working trigger. A real bio
# overrides it for that speaker, one at a time, so this never has to be
# switched off in one go -- it just stops being reachable as the copy lands.
# Set False to hide the trigger entirely for anyone without a real bio.
BIO_PLACEHOLDER_ON = True
BIO_PLACEHOLDER = ["Full bio coming soon."]


def speaker_bio(photo_key):
    """The bio for a speaker, or the placeholder, or None if neither."""
    real = SPEAKER_BIOS.get(photo_key)
    if real:
        return real
    if BIO_PLACEHOLDER_ON and photo_key is not None:
        return BIO_PLACEHOLDER
    return None


WHO_IN = ["905:2374", "905:2379", "905:2384"]
WHO_OUT = ["905:2391", "905:2396", "905:2401"]

# (question node, answer node). The last answer is "[Refund policy to confirm]"
# IN THE DESIGN -- that placeholder is the designer's, not ours, and it is the
# same open question the ticket terms carry.
FAQ_ITEMS = [
    ("I905:2466;255:536", "I905:2466;255:540"),
    ("I905:2467;255:529", "I905:2467;255:533"),
    ("I905:2468;255:529", "I905:2468;255:533"),
    ("I905:2469;255:529", "I905:2469;255:533"),
    ("I905:2470;255:529", "I905:2470;255:533"),
    ("I905:2471;255:529", "I905:2471;255:533"),
]


def who_html():
    def rows(ids, mark):
        return "".join(
            '<p class="sof-wrow"><i aria-hidden="true">%s</i><span>%s</span></p>'
            % (mark, T(i)) for i in ids)
    return (
        '<p class="sof-meyebrow"><i></i><span>%s</span><i></i></p>'
        '<h2 class="sof-art">'
        '<img src="%s" alt="" loading="lazy" decoding="async">'
        '<span class="sof-vh">Is this your mission?</span></h2>'
        '<div class="sof-wgrid">'
        '<div class="sof-wcard"><p class="sof-whead">%s</p>%s</div>'
        '<div class="sof-wcard sof-wcard--skip"><p class="sof-whead">%s</p>%s</div>'
        '</div>'
        '<a class="sof-wcta" href="%s">%s</a>'
    ) % (T("905:2362"), u("art_mission_title_who"),
         T("905:2369"), rows(WHO_IN, "\u2713"),
         T("905:2386"), rows(WHO_OUT, "\u2715"),
         CTA_HREF, T("I905:2402;255:431"))


def faq_html():
    items = "".join(
        '<details class="sof-faqitem">'
        '<summary class="sof-faqq">%s</summary>'
        '<p class="sof-faqa">%s</p></details>' % (T(q), T(a))
        for q, a in FAQ_ITEMS)
    return (
        '<p class="sof-meyebrow"><i></i><span>%s</span><i></i></p>'
        '<h2 class="sof-art">'
        '<img src="%s" alt="" loading="lazy" decoding="async">'
        '<span class="sof-vh">Questions? Answered.</span></h2>'
        '<div class="sof-faqlist">%s</div>'
        '<p class="sof-faqtail">%s</p>'
    ) % (T("905:2460"), u("art_faq_title"), items, T("905:2472"))


# --------------------------------------------------- 6b | mission map agenda
# Rows are component instances in Figma, so each one's three texts carry a
# compound id: "I<instance>;<component part>". 255:523 is the time, 255:525 the
# title, 255:526 the description -- the same three parts for all seventeen
# rows, which is why only the instance id changes below.
_SLOT_T, _SLOT_H, _SLOT_D = "255:523", "255:525", "255:526"

DAYS = [
    # (chip node, heading node, vip?, [row instance ids])
    # V3 cuts the agenda right down: 7/6/4 rows became 3/4/2.
    ("949:1417", "949:1418", False, ["949:1420", "949:1421", "949:1422"]),
    ("949:1426", "949:1427", False,
     ["949:1429", "949:1430", "949:1431", "949:1432"]),
    ("949:1436", "949:1437", True, ["949:1439", "949:1440"]),
]


# Day 2's after party is the one sponsored row. Keyed on the row instance
# rather than its position, so reordering the agenda moves the logo with it.
AFTER_PARTY = "949:1432"


def _slot(inst):
    logo = ""
    if inst == AFTER_PARTY:
        logo = ('<span class="sof-bfplate">'
                '<img class="sof-slot-bf" src="%s" alt="BestFulfill" '
                'loading="lazy" decoding="async"></span>'
                % u("bestfulfill_logo"))
    # The logo is a SIBLING of the text block, not inside it, so the row can
    # put it alongside rather than underneath.
    return ('<div class="sof-slot%s">'
            # No time cell: 255:523 is visible:false on all nine rows.
            '<div class="sof-slot-b">'
            '<p class="sof-slot-h">%s</p>'
            '<p class="sof-slot-d">%s</p>'
            '</div>%s</div>') % (" sof-slot--bf" if logo else "",
                                 T("I%s;%s" % (inst, _SLOT_H)),
                                 T("I%s;%s" % (inst, _SLOT_D)), logo)


def mission_html():
    cards = []
    for chip, head, vip, rows in DAYS:
        # No call to action on Day 3 any more. It is invite only, so there is
        # nothing to buy; the UPGRADE TO VIP button and its Stripe link are
        # gone. The `vip` flag in DAYS still drives the gold treatment.
        cards.append(
            '<div class="sof-day%s">'
            '<span class="sof-daychip%s">%s</span>'
            '<h3 class="sof-day-h">%s</h3>'
            '<div class="sof-slots">%s</div>'
            '</div>' % (
                " sof-day--gold" if vip else "",
                " sof-daychip--gold" if vip else "",
                T(chip), T(head), "".join(_slot(r) for r in rows)))
    return (
        '<p class="sof-meyebrow"><i></i><span>%s</span><i></i></p>'
        '<h2 class="sof-art">'
        '<img src="%s" alt="%s" loading="lazy" decoding="async">'
        '<span class="sof-vh">The Mission Map</span></h2>'
        '<p class="sof-mission-intro">%s</p>'
        '<div class="sof-days">%s</div>'
        '<p class="sof-mission-note">%s</p>'
    ) % (T("949:1407"), u("art_mission_title"), "",
         T("949:1412"), "".join(cards), T("949:1442"))


# ------------------------------------------------- 9b | legal popup content
# Written 2026-10-09 on Topi's say-so that we generate these rather than wait
# for a lawyer. Two things follow from that, both deliberate:
#
#  1. NOTHING HERE IS INVENTED. Every factual claim is either from the design
#     (dates, city, the ticket tiers) or measured from the live page. The cookie
#     and third-party list in the privacy policy came from loading the page and
#     reading what it actually set: four Lightfunnels cookies, one of them
#     `lfbid` at about a year, plus Google Fonts, unpkg and Sentry. The first
#     draft of this said "we set no cookies and run no tracking", which the
#     page itself disproved. A privacy policy that is wrong about its own site
#     is worse than no policy.
#  2. The handful of facts only the organiser knows are TBC() placeholders, not
#     guesses. A made-up legal entity or jurisdiction would make the document
#     look finished while being unenforceable, which is the failure mode worth
#     avoiding here.
#
# This is a sensible baseline for a paid two-day event. It is not a substitute
# for a lawyer reading it before tickets go on sale.
LEGAL_UPDATED = "Last updated 10 October 2026"
# The two documents are dated separately now. Connecting the contact form
# changed what the privacy policy describes; the terms did not change, so
# moving one date must not move the other.
PRIVACY_UPDATED = "Last updated 14 October 2026"
LEGAL_SUB = ("Scaling or Failing &middot; Bangkok, Thailand "
             "&middot; 7 and 8 December 2026")


def TBC(label):
    """A fact only the organiser can supply. Gold and dashed on the page so it
    cannot be shipped by accident, and one class so the rendered page can be
    checked for leftovers."""
    return '<span class="sof-legal-tbc">[%s]</span>' % label


# Supplied by the attendee terms, 2026-10-10. Filling these here also
# fills them in the Privacy tab, which reads the same constants.
ENTITY = "99Commerce Limited"
# Reproduced exactly as the document writes it, including "COmm" --
# an address is not something to correct on a guess.
ADDRESS = ("Office Unit B on 9/F Thomson COmm Bldg 8 Thomson Rd "
           "Wan Chai Hong Kong")
# Supplied 2026-10-14, so this one is no longer a TBC. The other three still
# are: a legal entity, a registered address and a jurisdiction are not things
# that can be inferred, and a privacy policy naming the wrong data controller
# is worse than one that admits it does not know yet.
#
# Written as a mailto link rather than plain text: in a privacy policy the
# address is how someone exercises a data right, so it has to be actionable,
# not just legible.
EMAIL = ('<a class="sof-legal-mail" href="mailto:%s">%s</a>'
         % (CONTACT_EMAIL, CONTACT_EMAIL))
LAW = "Hong Kong"

# The document still carries five square-bracketed items. A bracket in a
# legal document means nobody has decided yet, so each one renders as a
# TBC -- gold and dashed, and countable from the live page -- rather than
# being quietly resolved here.
FORCE_MAJEURE = TBC("what is deducted from a force-majeure refund")
# Confirmed by Joshua, 2026-10-15.
COMPLAINT_DAYS = "30"
# Confirmed by Joshua, 2026-10-15, as 30. The source document says 14 --
# see the note in v6_terms_fill.py. Put it back to 14 if only the
# complaint window was meant to move.
CHANGE_DAYS = "30"

# The two "[privacy policy URL]" placeholders. On this site the privacy
# policy is the other tab of the same dialog, so they switch to it.
PRIVACY_TAB = ('<label class="sof-legal-open" for="sof-legal-privacy">'
               'privacy policy</label>')

TERMS_DOC = """
<h3>Attendee terms and conditions</h3>
<p class="sof-legal-meta">{sub} &middot; {upd}</p>

<h4>Key points at a glance</h4>
<ul>
<li>99Commerce Limited, a Hong Kong company, hosts this event. You buy tickets
and manage your registration through the Whova app.</li>
<li>Tickets are non-refundable. You can transfer your ticket to someone else
until December 1, 2026 at no cost.</li>
<li>If we cancel the event, you get your money back. If we postpone it, your
ticket moves to the new date, or you can ask for a refund.</li>
<li>This is a mastermind. People share real numbers and real mistakes. Keep what
others share in the room confidential.</li>
<li>You may not record sessions, including with AI note-taking or transcription
tools, unless we give you written permission.</li>
<li>We photograph and film the event. Tell us if you would rather not appear in
our promotional material.</li>
<li>You are responsible for your own travel, visa, insurance and health
arrangements.</li>
<li>The event gives you ideas and contacts. It does not guarantee business
results.</li>
<li>We handle your data as set out in our {priv}. We never sell or hand over
attendee lists to sponsors.</li>
</ul>

<h4>1. Who we are and what these terms cover</h4>
<p>"We", "us" and "our" means {entity}, a company incorporated in Hong Kong
registered at {address}. "You" means the person who buys a ticket or attends the
event.</p>
<p>These terms apply to the Scaling or Failing BKK Mastermind in Bangkok,
Thailand, on December 7 and 8, 2026, including any official side events, dinners
and online content we provide with it (together, "the event").</p>
<p>By buying a ticket, registering, or entering the event, you agree to these
terms. If you buy a ticket for someone else, you must make sure they know about
these terms and agree to them.</p>
<p>You must be at least 18 years old to attend.</p>

<h4>2. Registration</h4>
<p>We run registration, ticketing and the event app through Whova, a third-party
platform. To register, you will need to create a Whova account and follow
Whova's own terms of use and privacy policy.</p>
<p>Please give us accurate, complete and current information, including your full
name as it appears on your ID. We may ask for ID at check-in. If your details
change, update them in Whova or email us.</p>
<p>Each ticket admits one named person. You may not share a ticket or a
badge.</p>
<p>Ticket transfers and name changes, you can email {email}.</p>
<p>We may decline or cancel a registration at our discretion, for example if the
event is over capacity or if a person's attendance would conflict with section 7.
If we do this before the event for reasons that are not your fault, we will
refund what you paid.</p>

<h4>3. Ticket prices and payment</h4>
<p>Ticket prices are shown on our website. Prices are in USD and are inclusive of
VAT and other applicable taxes.</p>
<p>You must pay in full at the time of booking unless we agree a different
arrangement in writing (for example, an invoice for a group booking). Card fees
or currency conversion charges from your own bank are your responsibility.</p>
<p>Your ticket is confirmed once payment clears and you receive a confirmation
from us. Prices can change over time (for example, early-bird pricing ends). A
later price change does not entitle you to a refund or a partial refund.</p>

<h4>4. Refunds, cancellations and substitutions</h4>
<p>All ticket sales are final and non-refundable, except as described below.</p>
<p><strong>Event cancellation by 99Commerce:</strong> If we cancel the event
entirely, you will receive a full refund of the ticket price within 30 days.</p>
<p><strong>Event postponement by 99Commerce:</strong> If the event is postponed,
your ticket stays valid for the new date. If you cannot attend the new date, you
may request a refund within 14 days of the postponement announcement.</p>
<p><strong>Attendee cancellation:</strong> We do not offer refunds if you cancel,
for any reason. This includes travel disruptions, visa issues, and personal
emergencies. We strongly recommend buying travel insurance.</p>
<p><strong>Ticket transfers:</strong> If you cannot attend, you can transfer your
ticket to someone else until December 1, 2026. Email {email} with the new
attendee's name and email. Each ticket is valid for one named attendee only.</p>
<p>Refunds are paid to the original payment method. Nothing in this section
limits any refund right the law gives you that cannot be waived by contract.</p>

<h4>6. Events outside our control (force majeure)</h4>
<p>We are not in breach of these terms if events outside our reasonable control
stop us from running the event or part of it, or force us to change it. Examples
include natural disasters, extreme weather, flooding, fire, epidemics or public
health orders, government action or travel restrictions, civil unrest, terrorism,
strikes, power or venue failures, and the venue becoming unavailable.</p>
<p>If one of these events happens, we will first try to postpone or relocate the
event, or move part of it online. If we have to cancel the event entirely,
section 5 applies and you receive a partial refund of the ticket price
{forcemajeure}.</p>

<h4>7. Code of conduct</h4>
<p>We want an event where people speak openly about what is working and what is
failing in their business. That only works if everyone feels safe and
respected.</p>
<p>At the event, at side events you agree to:</p>
<ul>
<li>treat other attendees, speakers, sponsors, staff and venue workers with
respect;</li>
<li>not harass, intimidate, threaten or discriminate against anyone, in person or
online;</li>
<li>not make unwelcome physical contact or sexual comments;</li>
<li>respect the confidentiality rules in section 9;</li>
<li>follow the instructions of our staff, venue staff and security;</li>
<li>not be intoxicated to a degree that disrupts others;</li>
<li>follow Thai law. Note that e-cigarettes and vapes are illegal in Thailand,
and that drug offences carry severe penalties;</li>
<li>not host or promote any unofficial event that presents itself as part of, or
connected to, the Scaling or Failing BKK Mastermind without our written
approval.</li>
</ul>
<p>If you experience or see behaviour that breaks these rules, tell a member of
our team at the event or email {email}. We will handle reports discreetly.</p>

<h4>8. Removal from the event</h4>
<p>We may refuse entry to, or remove, anyone who breaks these terms, Thai law, or
venue rules, or whose behaviour we reasonably believe puts others at risk or
disrupts the event. We may also deactivate their Whova access.</p>
<p>If we remove you for one of these reasons, you will not receive a refund, and
we may refuse you entry to future events.</p>

<h4>9. Mastermind confidentiality</h4>
<p>This event runs as a mastermind. Attendees and speakers will share revenue
figures, margins, supplier details, failed launches, team problems and other
sensitive business information. They do this because they trust the room.</p>
<p>By attending, you agree:</p>
<ul>
<li>not to share, publish or post information that another attendee or speaker
shares in a session, roundtable or private conversation if it identifies them or
their business, unless they give you permission;</li>
<li>not to use another attendee's confidential business information to compete
with them, copy their business, or approach their suppliers, staff or customers
in a way that relies on that information;</li>
<li>that you may use general lessons and ideas you learn, as long as you do not
identify who shared them.</li>
</ul>
<p>This does not cover information that is already public, information you
already knew, or disclosures the law requires.</p>
<p>Please use judgement about what you share. We ask everyone to respect
confidentiality, but we cannot control what other attendees do and we are not
liable if someone breaks this section. Do not share anything that would seriously
harm you or your business if it became public.</p>

<h4>10. No recording of sessions</h4>
<p>You may not record, livestream, photograph or transcribe any session,
including slides and screens, without our prior written permission. This includes
audio and video recording on phones, and AI note-taking or transcription
tools.</p>
<p>Taking your own written or typed notes for personal use is fine.</p>
<p>If you record without permission, we may ask you to delete the recording,
remove you under section 8, or both.</p>

<h4>11. Photos, video and media release</h4>
<p>We and our contractors will take photographs, video and audio at the event.
This may include footage in which you appear, including in the audience or in
public areas.</p>
<p>By attending, you allow us to use that footage, including your image, name and
voice, to report on and promote the Scaling or Failing BKK Mastermind and future
99Commerce events, on our website, social media, in advertising and in other
media, without payment to you.</p>
<p>If you would prefer not to appear in promotional material:</p>
<ul>
<li>tell us when you register or email {email} before the event;</li>
<li>tell our photographer at the event.</li>
</ul>
<p>We will make reasonable efforts to respect your preference. We cannot
guarantee you will not appear in wide shots of the room, but we will not feature
you prominently and we will remove footage of you from our own channels on
request where reasonably possible.</p>
<p>We do not photograph or film confidential mastermind sessions unless we tell
participants in advance.</p>

<h4>12. Speaker content and intellectual property</h4>
<p>Speakers and 99Commerce own the content they present, including slides,
frameworks, templates, workbooks and recordings. Where we give you materials, you
may use them for your own business. You may not copy, sell, publish, share
publicly, or use them to train or teach others commercially without the owner's
written permission.</p>
<p>The Scaling or Failing BKK Mastermind name, logos and branding belong to
{entity}. You may not use them in a way that suggests an endorsement or
partnership without our written permission.</p>
<p>Speakers' views are their own and do not necessarily reflect ours.</p>

<h4>13. Networking and solicitation</h4>
<p>Networking is a big part of this event. We want people to meet, swap ideas and
do business. We also want everyone to have a good experience.</p>
<p>You agree not to:</p>
<ul>
<li>send mass or repeated unsolicited sales messages to attendees, in person,
through Whova or afterwards;</li>
<li>add attendees to mailing lists or marketing campaigns unless they have
agreed;</li>
<li>collect attendee contact details through scraping, bots or other automated
tools;</li>
<li>sell products, run paid pitches or promote a business in sessions or public
areas unless you are an approved sponsor;</li>
<li>hand out promotional material or merchandise at the venue unless you are an
approved sponsor.</li>
</ul>
<p>One-to-one conversations where both people are interested are welcome. If
someone tells you they are not interested, respect that.</p>

<h4>14. Health, safety, travel and visas</h4>
<p>You are responsible for:</p>
<ul>
<li>your passport, visa and entry permission for Thailand. Check the current
rules with the Thai embassy or consulate in your country. From September 15,
2026, many nationalities receive a 30-day visa-free stay for tourism. If you are
unsure whether attending a business event fits your entry category, get advice
before you travel;</li>
<li>your flights, accommodation and local transport;</li>
<li>travel and medical insurance. We strongly recommend insurance that covers
cancellation, medical treatment and personal belongings;</li>
<li>your own health, including any vaccinations, medication and dietary needs.
Tell us in Whova about dietary or accessibility needs and we will do our best to
accommodate them;</li>
<li>following venue safety rules and the instructions of staff in an
emergency.</li>
</ul>
<p>Thai law may differ from the law in your country. Alcohol sales and
consumption are restricted in some places and at some times. Vaping and
e-cigarettes are illegal. You are responsible for following local law.</p>
<p>We may change health or safety measures at the event if public health guidance
or venue rules require it.</p>

<h4>15. Your belongings and the venue</h4>
<p>You are responsible for your own belongings. We are not responsible for loss,
theft or damage to personal property at the event, including items left in a
cloakroom or meeting room, unless it was caused by our negligence.</p>
<p>You are responsible for any damage you cause to the venue or its
equipment.</p>

<h4>16. No guarantee of results</h4>
<p>The event gives you information, perspectives and contacts. It is not legal,
tax, financial or investment advice. What works for one business may not work for
yours.</p>
<p>We do not guarantee any particular business outcome, revenue, profit or growth
from attending. You make your own decisions and are responsible for the results.
Take professional advice before acting on anything you hear.</p>
<p>We do not vet or endorse attendees, sponsors or the products and services they
offer. Do your own checks before doing business with anyone you meet.</p>

<h4>17. Our liability</h4>
<p>To the maximum extent permitted by law, {entity} shall not be liable for any
indirect, incidental, special, or consequential damages arising from your
attendance at or inability to attend Scaling or Failing, use of this Site, or any
event-related circumstances.</p>
<p>Our total liability to you for any claim related to Scsaling or Failing shall
not exceed the amount you paid for your ticket.</p>

<h4>18. Your data and privacy</h4>
<p>Our full {priv} is the other tab of this dialog. Here is a short summary.</p>
<p><strong>What we collect:</strong> your name, email, phone number, company and
job title, billing details, ticket type, dietary and accessibility needs you
choose to share, and information about your use of Whova. We also capture photos
and video at the event (see section 11).</p>
<p><strong>Why we use it:</strong> to process your ticket, run check-in and the
event, send you event updates, keep the event safe, handle questions and refunds,
meet legal and accounting duties, and improve future events. We will only send
you marketing about future events if you have agreed, and you can opt out at any
time.</p>
<p><strong>Whova:</strong> Whova runs our registration and app. When Whova
processes your data for our event, we are responsible for that data and Whova
acts on our instructions. Whova also has its own privacy policy at
<a class="sof-legal-mail" href="https://whova.com/privacy/" target="_blank"
rel="noopener">whova.com/privacy</a>, which applies to your Whova account. By
default, your name and profile appear in the in-app attendee list so other
attendees can find you. You can switch to "invisible" in the Whova settings at
any time. Whova does not show your email or phone number to other attendees
unless you choose to exchange them.</p>
<p><strong>Sponsors:</strong> we do not sell your data or give sponsors an
attendee list. A sponsor only receives your details if you choose to share them,
for example by letting them scan your badge or QR code, exchanging contact
details in Whova, or claiming one of their offers. Once you share your details
with a sponsor, their own privacy policy applies to how they use them.</p>
<p><strong>Who else we share data with:</strong> service providers that help us
run the event (such as Whova and its payment provider, the venue, our
photographers and our email tools), professional advisers, and authorities where
the law requires it.</p>
<p><strong>International transfers:</strong> we are based in Hong Kong, the event
is in Thailand, and Whova stores data in the United States. Your data may be
processed in these and other countries. We take reasonable steps to protect it
when it moves.</p>
<p><strong>Retention:</strong> we keep your data only as long as we need it for
these purposes and to meet legal and accounting requirements.</p>
<p><strong>Your rights:</strong> depending on where you live (including under
Hong Kong's Personal Data (Privacy) Ordinance and Thailand's Personal Data
Protection Act), you may have the right to access, correct or delete your data,
object to or restrict some uses, withdraw consent, or complain to a data
protection authority. To use these rights, email {email}.</p>

<h4>19. Governing law and disputes</h4>
<p>{law} law governs these terms.</p>
<p>If you have a complaint, please email {email} first. We will try to resolve it
within {complaintdays} days.</p>
<p>If we cannot resolve it, the courts of Hong Kong have non-exclusive
jurisdiction. This means you or we can bring a claim in Hong Kong, and nothing
here stops you using the courts or consumer protection bodies where you live if
the law gives you that right.</p>
<p>If you are a consumer, nothing in these terms removes any protection that the
law of your country of residence gives you and that cannot be changed by
contract.</p>

<h4>20. Changes to these terms</h4>
<p>We may update these terms, for example to reflect a change in law, venue or
event format. We will post the updated version on our website and in Whova with a
new "last updated" date, and email registered attendees about any significant
change.</p>
<p>If a change significantly affects you before the event and you do not accept
it, you may ask for a refund of your ticket price within {changedays} days of our
notice.</p>

<h4>21. General</h4>
<ul>
<li>These terms, together with our privacy policy and any specific terms shown at
checkout, make up the whole agreement between you and us about the event.</li>
<li>If a court finds part of these terms invalid, the rest still applies.</li>
<li>If we do not enforce a right straight away, we can still enforce it
later.</li>
<li>You may not transfer your rights under these terms except through a ticket
transfer under section 2.</li>
<li>If there is a translated version of these terms, the English version applies
if the two differ.</li>
</ul>

<h4>22. Contact us</h4>
<p>{entity}<br>{address}<br>Email: {email}</p>
""".format(sub=LEGAL_SUB, upd=LEGAL_UPDATED, entity=ENTITY, address=ADDRESS,
           email=EMAIL, law=LAW, priv=PRIVACY_TAB,
           forcemajeure=FORCE_MAJEURE, complaintdays=COMPLAINT_DAYS,
           changedays=CHANGE_DAYS)
PRIVACY_DOC = """
<h3>Privacy Policy</h3>
<p class="sof-legal-meta">{sub} &middot; {upd}</p>

<h4>1. Who we are</h4>
<p>{entity}, trading as Scaling or Failing, of {address}, decides how the
personal data described here is used. You can reach us at {email}.</p>

<h4>2. What we collect</h4>
<ul>
<li><strong>When you book.</strong> Your name, email, phone, company, job title
and billing details, plus anything you choose to add such as dietary or
accessibility needs.</li>
<li><strong>When you contact us.</strong> Whatever you put in your message.</li>
<li><strong>At the event.</strong> Your name and company on your badge, and
photography and film of the room.</li>
<li><strong>When you visit this page.</strong> See the next section.</li>
</ul>

<h4>3. What this page does</h4>
<p>The event page asks you for nothing. The contact page has a form. What you
type into it is emailed to us so that we can reply, and is not stored anywhere
else. Both pages set cookies and contact a few other services:</p>
<ul>
<li>Our website platform, Lightfunnels, sets a session cookie, two cart cookies,
and an identifier called lfbid that lasts about a year and lets the platform
recognise a returning browser.</li>
<li>Google Fonts serves the typefaces, so Google receives your IP address.</li>
<li>unpkg serves the smooth scrolling library, so unpkg receives your IP
address.</li>
<li>Sentry receives a report if the page hits an error.</li>
</ul>
<p>We run no advertising pixels, no analytics and no remarketing tags on this
page.</p>

<h4>4. Why we use it</h4>
<ul>
<li>To sell you a ticket and get you into the event, which we need in order to
perform our contract with you.</li>
<li>To keep this website working and secure, which is our legitimate
interest.</li>
<li>To tell you about this event and future ones, with your consent where
consent is required. You can opt out at any time.</li>
<li>To meet our accounting and tax obligations, which is a legal duty.</li>
</ul>

<h4>5. Who we share it with</h4>
<ul>
<li>Our registration and ticketing platform, which processes your booking.</li>
<li>Stripe, our payment provider, which handles the checkout and your card
details. We never see your full card number.</li>
<li>The venue and our catering and production suppliers, for names, access and
dietary needs.</li>
<li>Partners and sponsors, <strong>only where you have agreed</strong>, for
example by letting a sponsor scan your badge.</li>
<li>Our email and automation providers, which carry your contact form message
to us.</li>
<li>Professional advisers and authorities, where we are required to.</li>
</ul>
<p>We do not sell your personal data.</p>

<h4>6. Where it goes</h4>
<p>The event is in Thailand and some of our suppliers are in the United States,
so your data will be transferred outside the UK and the EEA. Where it is, we
rely on appropriate safeguards such as standard contractual clauses.</p>

<h4>7. How long we keep it</h4>
<p>Booking and payment records for seven years, to satisfy accounting rules.
Marketing contact details until you opt out. Event photography and film are kept
as part of our archive.</p>

<h4>8. Your rights</h4>
<p>You can ask us for a copy of your data, to correct it, to delete it, to
restrict or object to how we use it, or to receive it in a portable form, and
you can withdraw consent at any time. Email {email}. You can also complain to
your local data protection regulator.</p>

<h4>9. Marketing</h4>
<p>Every marketing email has an unsubscribe link. Unsubscribing does not stop
the messages we need to send you about a ticket you have already bought.</p>

<h4>10. Children</h4>
<p>This event is for business professionals and is not intended for anyone under
18.</p>

<h4>11. Changes to this policy</h4>
<p>If we change this policy we will update the date at the top of it.</p>
""".format(sub=LEGAL_SUB, upd=PRIVACY_UPDATED, entity=ENTITY, address=ADDRESS,
           email=EMAIL)


def legal_html():
    """The three radios, then the dialog.

    DOM order is load-bearing: every rule that opens the dialog or switches its
    tab is a sibling combinator from a checked radio, so the radios must come
    before the dialog markup.
    """
    return (
        '<input type="radio" name="sof-legal" id="sof-legal-off"'
        ' class="sof-legal-r" checked>'
        '<input type="radio" name="sof-legal" id="sof-legal-terms"'
        ' class="sof-legal-r">'
        '<input type="radio" name="sof-legal" id="sof-legal-privacy"'
        ' class="sof-legal-r">'
        '<div class="sof-legal" role="dialog" aria-modal="true"'
        ' aria-label="Terms and Privacy">'
        '<label class="sof-legal-scrim" for="sof-legal-off"'
        ' aria-label="Close"></label>'
        '<div class="sof-legal-box">'
        '<div class="sof-legal-head">'
        '<div class="sof-legal-tabs">'
        '<label class="sof-legal-tab sof-legal-tab--t" for="sof-legal-terms">'
        'TERMS</label>'
        '<label class="sof-legal-tab sof-legal-tab--p" for="sof-legal-privacy">'
        'PRIVACY</label>'
        '</div>'
        '<label class="sof-legal-x" for="sof-legal-off" aria-label="Close">'
        '&times;</label>'
        '</div>'
        '<div class="sof-legal-body" data-lenis-prevent tabindex="0">'
        '<div class="sof-legal-doc sof-legal-doc--t">' + TERMS_DOC + '</div>'
        '<div class="sof-legal-doc sof-legal-doc--p">' + PRIVACY_DOC + '</div>'
        '</div></div></div>'
    )


# --------------------------------------------------------- 11 | contact page
# (label node, placeholder node, input name, type)
CONTACT_FIELDS = [
    ("909:3288", "909:3290", "name", "text"),
    ("909:3292", "909:3294", "email", "email"),
    ("909:3296", "909:3298", "topic", "select"),
    ("909:3301", "909:3303", "message", "textarea"),
]
# The topic options are one string in the frame, "Tickets / Sponsorship /
# Speaking / Other", because Figma has no select control to draw.
TOPIC_OPTIONS = ["Tickets", "Sponsorship", "Speaking", "Other"]


# Off-screen, not display:none. A bot that skips hidden fields will still fill
# an off-screen one, which is the whole point of a honeypot. Inline style rather
# than a class so the stylesheet does not have to carry a rule whose only job is
# to hide something. n8n drops any submission that arrives with this filled in.
HONEYPOT = (
    '<div aria-hidden="true" style="position:absolute;left:-9999px;top:auto;'
    'width:1px;height:1px;overflow:hidden"><label for="sof-website">Website</label>'
    '<input id="sof-website" name="website" type="text" tabindex="-1" '
    'autocomplete="off"></div>'
)


def contact_html():
    rows = []
    for label_id, ph_id, name, kind in CONTACT_FIELDS:
        label, ph = T(label_id), T(ph_id)
        if kind == "select":
            opts = "".join('<option value="%s">%s</option>' % (esc(o), esc(o))
                           for o in TOPIC_OPTIONS)
            # The frame's grey line is a PLACEHOLDER, not a choice. disabled
            # stops it being picked again once the visitor has chosen, hidden
            # keeps it out of the open list, and the empty value keeps the
            # select :invalid so the grey styling holds until a real pick.
            field = ('<div class="sof-select">'
                     '<select id="sof-%s" name="%s" required>'
                     '<option value="" disabled selected hidden>%s</option>'
                     '%s</select></div>'
                     % (name, name, ph, opts))
        elif kind == "textarea":
            field = ('<textarea id="sof-%s" name="%s" rows="5" '
                     'placeholder="%s" required></textarea>' % (name, name, ph))
        else:
            field = ('<input id="sof-%s" name="%s" type="%s" placeholder="%s" '
                     'required>' % (name, name, kind, ph))
        rows.append('<div class="sof-field"><label for="sof-%s">%s</label>%s</div>'
                    % (name, label, field))
    return (
        '<h1 class="sof-art">'
        '<img src="%s" alt="" loading="eager" decoding="async">'
        '<span class="sof-vh">Get in touch</span></h1>'
        '<p class="sof-contact-sub">%s</p>'
        # No action and no method ON PURPOSE. The submit handler in the funnel's
        # header_scripts intercepts the submit and POSTs to n8n with fetch; an
        # action would make a non-JS submit navigate away to a raw JSON
        # response. See CONTACT-FORM-IMPLEMENTATION.md.
        '<form class="sof-form">%s%s'
        '<button class="sof-send" type="submit">%s</button>'
        '<p class="sof-form-note">Or email <a href="mailto:%s">%s</a></p>'
        '</form>'
    ) % (u("t_contact"), T("909:3284"), "".join(rows), HONEYPOT,
         T("I909:3304;255:431"), CONTACT_EMAIL, CONTACT_EMAIL)


# ------------------------------------------------------------- 10 | footer
def _plain(escaped):
    """Undo T()'s escaping so a name can be re-escaped into an attribute.

    T() returns HTML-escaped text for element content. Dropping that straight
    into alt="" would double-escape an ampersand, and "Super Tan Brothers &amp;
    Co" would be read out as the literal "&amp;".
    """
    return (escaped.replace("&quot;", '"').replace("&#x27;", "'")
            .replace("&lt;", "<").replace("&gt;", ">").replace("&amp;", "&"))


def legal_copy():
    """The footer copy line with its two legal words turned into the dialog's
    triggers.

    The design draws "Privacy" and "Terms" as plain text inside the copyright
    sentence, with no destination -- they were the page's last open question.
    Wrapping each word in a <label> keeps the CHARACTERS exactly as drawn, so
    the copy design_diff compares is byte for byte unchanged and only markup is
    added around two words.

    The count assertion is the point: a blind .replace() on a word this short
    would silently also hit a second occurrence if the copy were ever reworded,
    and a half-linked sentence is the kind of defect no check here would catch.
    """
    copy = T("949:1527")
    for word, target in (("Privacy", "sof-legal-privacy"),
                         ("Terms", "sof-legal-terms")):
        n = copy.count(word)
        assert n == 1, ("footer copy 870:431 contains %d occurrences of %r, "
                        "expected exactly 1 -- check the role of the string "
                        "before replacing it" % (n, word))
        copy = copy.replace(word, '<label class="sof-legal-open" for="%s">%s'
                                  '</label>' % (target, word))
    return copy


def footer_html():
    links = "".join(
        '<a href="%s"%s>%s</a>'
        % (nav_href(href), ' class="sof-gold"' if gold else "", label)
        for label, href, gold in NAV)
    return (
        '<div class="sof-footer-in">'
        '<div><p class="sof-fbrand">%s</p><p class="sof-fdate">%s</p></div>'
        '<nav class="sof-fnav" aria-label="Footer">%s</nav>'
        '<p class="sof-fcopy sof-rich">%s</p>'
        '</div>'
    ) % (T("949:1520"), T("949:1521"), links, legal_copy())


# ==========================================================================
# Assemble the LF body. One Section per design section, each a full-bleed
# wrapper around a single HtmlElement.
# ==========================================================================
def html_block(content):
    return {"t": "HtmlElement", "id": nid(), "p": {"content": content},
            "styles": [{"prop": "width", "value": "100%"}]}


def section(html, anchor=None, extra_class="", bleed=False, wrap=True,
            scale=True, after=""):
    """One design section. `bleed` drops the page gutter for a full-width band;
    `wrap` adds the centred max-width:1680 content column; `scale` puts the
    section inside the .sof-scale container that carries the 1024-1919 zoom.

    scale=False is for anything that must stay in real viewport pixels -- the
    position:fixed legal dialog, which a zoomed ancestor would both shrink
    and trap inside that section."""
    cls = "sof sof-sec " + extra_class + (" sof-sec--bleed" if bleed else "")
    inner = '<div class="sof-in">%s</div>' % html if wrap else html
    # .sof-cap is what stops at 1400. The SECTION stays full width so its
    # background bleeds; this wrapper is pinned to the design's 1920 and the
    # zoom lands it on 1400. See the .sof-cap rules.
    inner = '<div class="sof-cap">%s</div>' % inner
    wrap_html = '<div class="%s"%s>%s</div>' % (
        cls.strip(), (' id="%s"' % anchor) if anchor else "", inner)
    if scale:
        wrap_html = '<div class="sof-scale">%s</div>' % wrap_html
    if after:
        # Appended OUTSIDE .sof-scale, so it is not zoomed, but inside the same
        # html block, so it does not cost an LF Section -- an empty Section
        # still draws its divider, which is where the 103px white band under
        # the footer came from.
        wrap_html += after
    return {"t": "Section", "id": nid(),
            "styles": [{"prop": "padding",
                        "value": {"top": "0px", "bottom": "0px",
                                  "left": "0px", "right": "0px"}}],
            "p": {"layout": "", "dividerPosition": ["top"], "horizontalFlip": False,
                  "embedded_video": {"src": "", "video_size": "stretch",
                                     "video_position": "center"},
                  "children": [html_block(wrap_html)]}}


# Both pages share this file so they share one stylesheet, one header and one
# footer; two builders would mean two copies of that drifting apart. PAGE is
# set at the top, next to FUNNEL and STEP_SLUG.
if PAGE == "contact":
    STEP_SLUG = os.environ.get("SOF_SLUG", "contact")
    _children = [
        # scale=False: outside the zoom, so 36px is 36px at every width.
        section(promo_html(), extra_class="sof-promobar", bleed=True,
                wrap=False, scale=False),
        # scale=False for the same reason as the bar above it: the ask was a
        # constant size, and inside .sof-scale these would be design px.
        section(countdown_html(), extra_class="sof-cdbar", bleed=True,
                wrap=False, scale=False),
        # scale=False, like the bar above it: inside the zoom the nav grew
        # from 58px to 108px across the desktop range. Outside it, the heights
        # below are real pixels and hold at every width.
        section(header_html(), extra_class="sof-head", bleed=True, wrap=False,
                scale=False),
        section(contact_html(), extra_class="sof-contact"),
        section(footer_html(), anchor="contact", extra_class="sof-footer",
                # The dialog rides along after the scaled wrapper.
                after=legal_html() + speaker_modal_html()),
    ]
else:
    _children = [
        # V3 order, frame 909:2659. Ticker is back ABOVE Stats, and You
        # Decide sits after Formats rather than before Speakers.
        # scale=False: outside the zoom, so 36px is 36px at every width.
        section(promo_html(), extra_class="sof-promobar", bleed=True,
                wrap=False, scale=False),
        # scale=False for the same reason as the bar above it: the ask was a
        # constant size, and inside .sof-scale these would be design px.
        section(countdown_html(), extra_class="sof-cdbar", bleed=True,
                wrap=False, scale=False),
        # scale=False, like the bar above it: inside the zoom the nav grew
        # from 58px to 108px across the desktop range. Outside it, the heights
        # below are real pixels and hold at every width.
        section(header_html(), extra_class="sof-head", bleed=True, wrap=False,
                scale=False),
        section(hero_html(), extra_class="sof-hero", bleed=True, wrap=False),
        section(stats_html(), extra_class="sof-stats", bleed=True, wrap=False),
        section(marquee_html(), extra_class="sof-marqbar", bleed=True, wrap=False),
        section(speakers_html(), anchor="speakers", extra_class="sof-speakers"),
        section(formats_html(), extra_class="sof-formats"),
        section(decide_html(), anchor="about", extra_class="sof-decide", wrap=False),
        section(mission_html(), anchor="topics", extra_class="sof-mission"),
        section(tickets_html(), anchor="tickets", extra_class="sof-tickets"),
        section(sponsor_html(), extra_class="sof-sponsor"),
        section(footer_html(), anchor="contact", extra_class="sof-footer",
                # The dialog rides along after the scaled wrapper.
                after=legal_html() + speaker_modal_html()),
    ]

body = {
    "id": nid(), "t": "Root", "version": 11,
    "styles": [{"prop": "pageWidth", "value": "1680px"},
               {"prop": "backgroundColor",
                "value": {"r": 252, "g": 236, "b": 199, "a": 1}}],
    "p": {"children": _children}}


# ---------------------------------------------------------------- sanity
def _scan(nd, path="root"):
    bad = []
    if isinstance(nd, dict):
        if "t" in nd and "id" not in nd:
            bad.append(path + " missing id")
        for k, v in nd.items():
            if v is None:
                bad.append(path + "." + k + " None")
            bad += _scan(v, path + "." + str(k))
    elif isinstance(nd, list):
        for i, x in enumerate(nd):
            bad += _scan(x, path + "[%d]" % i)
    return bad


_iss = _scan(body)
print("sections:", len(body["p"]["children"]))
print("sanity issues:", len(_iss))
for _x in _iss[:10]:
    print("  !", _x)
_all = json.dumps(body)
assert 'href="#"' not in _all, "href=\"#\" is banned by the standing requirements"
assert _all.count("<h1") == 1, "exactly one h1 on the page"
if PAGE == "event":
    assert _all.count("<h2") == 6, "section headings are h2"   # V3 dropped Topics, Who it's for and the FAQ


# ==========================================================================
# SEO + head/foot custom HTML
# ==========================================================================
TITLE = "Scaling or Failing — Bangkok, December 7–8 2026"
SEO = {
    "title": "Scaling or Failing 2026 — Bangkok, Dec 7–8",
    "description": ("Two days in Bangkok with the operators actually running the "
                    "brands. Live interviews, unreleased playbooks and open-mic "
                    "Q&A. Early Bird $1,997."),
    "keywords": ("Scaling or Failing, ecommerce event Bangkok, ecommerce conference "
                 "2026, DTC mastermind, paid media conference, TikTok Shops, native "
                 "ads, Facebook ads event, BestFulfill, Bangkok December 2026"),
    "social_image_uid": IMG["og_sof"]["src_uid"],
}
assert 140 <= len(SEO["description"]) <= 160, len(SEO["description"])

# ==========================================================================
# META PIXEL — requested by Topi via Joshua, 2026-10-22 (ClickUp z941abzgdq
# item 4). Base code goes in the <head> of EVERY page, so it lives in PERF,
# which is the step's custom_html.header; both steps are built from this file,
# so one definition covers the event page and the contact page.
#
# The loader below is Meta's own snippet, pasted verbatim rather than retyped.
# ==========================================================================
META_PIXEL_ID = "4614760112140269"

# What a ticket is worth, for the event payloads. The page prices in USD even
# though Stripe's checkout defaults to the buyer's local currency, so USD is
# what the pixel should report -- a value in a currency Meta was not told
# about is worse than no value.
TICKET_SKU = "sof-early-bird"
TICKET_VALUE = "1997"
TICKET_CURRENCY = "USD"

META_PIXEL = """<!-- Meta Pixel Code -->
<script>
!function(f,b,e,v,n,t,s)
{if(f.fbq)return;n=f.fbq=function(){n.callMethod?
n.callMethod.apply(n,arguments):n.queue.push(arguments)};
if(!f._fbq)f._fbq=n;n.push=n;n.loaded=!0;n.version='2.0';
n.queue=[];t=b.createElement(e);t.async=!0;
t.src=v;s=b.getElementsByTagName(e)[0];
s.parentNode.insertBefore(t,s)}(window, document,'script',
'https://connect.facebook.net/en_US/fbevents.js');
fbq('init', '%s');
fbq('track', 'PageView');
</script>
<noscript><img height="1" width="1" style="display:none"
src="https://www.facebook.com/tr?id=%s&ev=PageView&noscript=1"/></noscript>
<!-- End Meta Pixel Code -->
""" % (META_PIXEL_ID, META_PIXEL_ID)

# ViewContent on the EVENT page only. The contact page sells nothing, and
# reporting a product view there would inflate the only number this pixel
# exists to measure.
META_VIEW = ("<script>fbq('track','ViewContent',{content_ids:['%s'],"
             "content_type:'product',value:%s,currency:'%s'});</script>"
             % (TICKET_SKU, TICKET_VALUE, TICKET_CURRENCY)) if PAGE == "event" else ""

PERF = (
    META_PIXEL + META_VIEW +
    _PRELOAD + _HERO_PRELOAD +
    "<style>" + _GF_FACES + _INTER_FACE + _INTER_FALLBACK + "</style>\n"
    '<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>\n'
    "<style>" + CSS + "</style>\n"
    # settings.seo emits og:* only — without these X renders no card at all.
    '<meta name="twitter:card" content="summary_large_image">\n'
    '<meta name="twitter:title" content="%s">\n'
    '<meta name="twitter:description" content="%s">\n'
    '<meta name="twitter:image" content="%s">\n'
    % (esc(SEO["title"]), esc(SEO["description"]), u("og_sof")))

# The LF storefront theme emits maximum-scale=1, which blocks pinch-zoom and is
# an accessibility failure. There is no per-step viewport knob, so rewrite it.
PERF_FOOTER = (
    # COUNTDOWN. Corrects the build-time digits against the visitor's own
    # clock, then ticks. Recomputed from Date.now() every tick rather than
    # decremented, so a throttled background tab is right when it returns.
    # At zero the bar is REMOVED -- Joshua asked for it to disappear, and an
    # empty gold band would read as broken.
    '<script>(function(){var b=document.querySelector(".sof-cd");'
    'if(!b)return;var end=Date.parse(b.getAttribute("data-cd-ends"));'
    'if(!end)return;var f={};'
    '["d","h","m","s"].forEach(function(k){'
    'f[k]=b.querySelector(\'[data-cd="\'+k+\'"]\');});'
    'function p(n){return n<10?"0"+n:""+n;}'
    'function tick(){var left=Math.floor((end-Date.now())/1000);'
    'if(left<=0){clearInterval(t);'
    'if(b.parentNode)b.parentNode.removeChild(b);return;}'
    'if(f.d)f.d.textContent=p(Math.floor(left/86400));'
    'if(f.h)f.h.textContent=p(Math.floor(left/3600)%24);'
    'if(f.m)f.m.textContent=p(Math.floor(left/60)%60);'
    'if(f.s)f.s.textContent=p(left%60);}'
    'var t=setInterval(tick,1000);tick();})();</script>'
    # Meta: AddToCart and InitiateCheckout when someone leaves for checkout.
    # Matched on the href rather than the class, so any future checkout link
    # is covered too; the nav's GET TICKET only scrolls, so it is correctly
    # excluded. The link navigates away immediately -- fbevents sends these
    # over sendBeacon, which survives the unload, so navigation is not
    # delayed to wait for them.
    #
    # ⚠️ 2026-11-04: the match was `buy.stripe.com` only, and the live
    # ticket button has pointed at whop.com since the Whop switch earlier
    # the same day -- so this tracking had silently stopped firing for
    # every real click since then. Caught while fixing the EB_HREF
    # regression above, not reported separately. Matched on EITHER host
    # now, so a future processor swap only needs a new clause here, not a
    # silent tracking gap until someone happens to check.
    #
    # Both events describe the SAME click, on Joshua's instruction
    # (2026-10-23). There is no cart on this site, so Meta will show a 100%
    # AddToCart -> InitiateCheckout step with no drop-off. That is what "no
    # cart" looks like once both events exist, not a bug to chase later.
    # They share one payload object so the two cannot drift apart.
    '<script>(function(){document.addEventListener("click",function(e){'
    'if(!e.target.closest)return;'
    'if(!e.target.closest(\'a[href*="buy.stripe.com"],a[href*="whop.com"]\'))return;'
    'if(!window.fbq)return;'
    'var p={content_ids:["' + TICKET_SKU + '"],content_type:"product",'
    'value:' + TICKET_VALUE + ',currency:"' + TICKET_CURRENCY + '"};'
    'fbq("track","AddToCart",p);fbq("track","InitiateCheckout",p);'
    '});})();</script>\n'
    '<script>(function(){var v=document.querySelector("meta[name=viewport]");'
    'if(v&&/maximum-scale/.test(v.content))'
    'v.setAttribute("content","width=device-width, initial-scale=1");})();</script>\n'
    '<script>(function(){var c=document.getElementById("sof-menu");if(!c)return;'
    # Opening the dialog moves the page on its own at mobile widths: measured
    # -271px at 390 from merely setting the radio in JS -- no click, no focus
    # change -- animated because html carries scroll-behavior:smooth. 1920 does
    # not do it. Rather than chase which box the browser decides to reveal, the
    # position is captured before the state changes and written back over the
    # next ~20 frames. Two was not enough: html carries scroll-behavior:smooth
    # so the browser's own animation is still running and simply re-applies
    # itself, which is why the pin also forces scroll-behavior:auto for the
    # duration and puts it back afterwards.
    'function hold(){var y=window.pageYOffset,h=document.documentElement,'
    'p=h.style.scrollBehavior,n=0;h.style.scrollBehavior="auto";'
    '(function tick(){if(window.pageYOffset!==y)window.scrollTo(0,y);'
    'if(++n<20){requestAnimationFrame(tick);}else{h.style.scrollBehavior=p;}'
    '})();}'
    'document.addEventListener("click",function(e){var a=e.target.closest'
    '(".sof-menu a");if(a)c.checked=false;});})();</script>\n'
    # Keyboard for the speaker bio modal. A <label> is not focusable and
    # :checked cannot hear Escape, so without this the feature is mouse-only,
    # which on a list of speakers is an exclusion rather than a nicety.
    # Enter/Space opens a focused trigger, Escape closes, and focus returns to
    # whichever trigger opened it so a keyboard user is not dropped at the top
    # of the document. Inert when no bios are set: nothing matches.
    # Holding the scroll position is the fiddly part. Opening the dialog sets
    # html{overflow:hidden} to stop the page moving behind it, and the browser
    # does not reliably keep scrollY across that -- measured, it jumped ~100px
    # at 1920 and ~950px at 390, so closing the dialog left you somewhere else
    # on the page entirely. The position is captured on the way in and written
    # back on the next frame, and again on the way out.
    '<script>(function(){'
    'var OPEN=".sof-spk-hit,.sof-spk-i",SHUT=".sof-spk-x,.sof-spk-scrim",o=null;'
    'function set(t){var r=document.getElementById(t.getAttribute("for"));'
    'if(!r)return false;r.checked=true;return true;}'
    # Opening the dialog moves the page on its own at mobile widths: measured
    # -297px at 390 from merely setting the radio, with no click and no focus
    # change. It is animated, because html carries scroll-behavior:smooth --
    # which is also why restoring the position once is not enough, the
    # browser's own animation simply carries on. So the pin forces
    # scroll-behavior:auto, rewrites the position for about twenty frames, and
    # puts the behaviour back. 1920 never needed it; 390 does.
    'function hold(){var y=window.pageYOffset,h=document.documentElement,'
    'p=h.style.scrollBehavior,n=0;h.style.scrollBehavior="auto";'
    '(function tick(){if(window.pageYOffset!==y)window.scrollTo(0,y);'
    'if(++n<20){requestAnimationFrame(tick);}else{h.style.scrollBehavior=p;}'
    '})();}'
    # The triggers carry tabindex=0 for keyboard users, and a mouse click would
    # otherwise FOCUS the label -- and the browser scrolls a newly focused
    # element into view, which moves the page under someone clicking a card
    # that is only half on screen. preventDefault on mousedown stops the focus
    # without stopping the click. Tabbing never fires mousedown, so keyboard
    # focus is untouched.
    'document.addEventListener("mousedown",function(e){'
    'if(e.target.closest&&e.target.closest(OPEN+","+SHUT))e.preventDefault();});'
    'document.addEventListener("click",function(e){'
    'if(!e.target.closest)return;'
    'var t=e.target.closest(OPEN+","+SHUT);if(!t)return;'
    'e.preventDefault();hold();if(!set(t))return;'
    'if(t.matches(OPEN)){o=t;}else if(o){o.focus({preventScroll:true});o=null;}});'
    'document.addEventListener("keydown",function(e){'
    'var t=e.target.closest?e.target.closest(OPEN+","+SHUT):null;'
    'if(t&&(e.key==="Enter"||e.key===" ")){e.preventDefault();t.click();return;}'
    'if(e.key!=="Escape")return;'
    'var n=document.getElementById("sof-spk-none");if(!n||n.checked)return;'
    'hold();n.checked=true;if(o){o.focus({preventScroll:true});o=null;}});})();</script>\n')

CUSTOM_HTML = {"header": PERF, "footer": PERF_FOOTER}


# ==========================================================================
# WRITE — create the step if it is new, otherwise update its body in place and
# leave every sibling step untouched.
# ==========================================================================
if __name__ == "__main__":
    guard(FUNNEL, STEP_SLUG)

    existing = sgql(
        'query($q: String!){ funnels(first:1,query:$q){ edges { node { '
        'id published starting_step_id steps { id uid slug title type settings '
        'visual { x y } } } } } }',
        {"q": "id:%s" % FUNNEL})["funnels"]["edges"][0]["node"]
    steps = existing["steps"]
    mine = next((s for s in steps if s["slug"] == STEP_SLUG), None)
    # updateFunnel validates every step in the list against InputStep, and
    # `settings` is a required field there -- a sibling echoed back without it
    # fails the whole mutation. Echo each sibling's own stored settings/visual
    # so nothing of theirs is changed by being listed.
    others = [{"id": s["id"], "slug": s["slug"], "title": s["title"],
               "type": s["type"], "settings": s["settings"], "visual": s["visual"]}
              for s in steps if s["slug"] != STEP_SLUG]

    node = {"slug": STEP_SLUG, "title": TITLE, "type": "article_page",
            "settings": {"custom_html": CUSTOM_HTML, "seo": SEO},
            "body": body}

    # Recovery hatch for a DETACHED step. createStep makes the step and claims
    # the slug immediately, but it only becomes visible to `funnels.steps` once
    # updateFunnel attaches it. So if that second call fails, the slug is taken
    # by a step that nothing can see: the guard reports the slug as new, and
    # createStep refuses it with errors_duplicated_step_slug. Re-running with
    # the id createStep printed skips straight to the attach.
    orphan = os.environ.get("SOF_STEP_ID")

    if mine:
        print("redeploying existing step ->", mine["id"])
        node["id"] = mine["id"]
        node["visual"] = mine["visual"]
        new_steps = others + [node]
        update = {"steps": new_steps}
    else:
        if orphan:
            sid = orphan
            print("attaching detached step ->", sid)
        else:
            created = sgql(
                'mutation($fid: ID!, $node: InputStep!){ createStep(funnel_id:$fid,'
                'node:$node){ step { id uid } } }',
                {"fid": FUNNEL, "node": dict(node, visual={"x": 120, "y": 90})})
            sid = created["createStep"]["step"]["id"]
            print("created detached step ->", created["createStep"]["step"])
        node["id"] = sid
        node["visual"] = {"x": 120, "y": 90}
        update = {"steps": others + [node]}
        # Only claim the entry slot if the funnel does not already have one.
        # Repointing a published funnel's entry changes what /<funnel-slug>/
        # serves, which is a live-traffic change and not this script's call.
        if not existing.get("starting_step_id"):
            update["starting_step_id"] = sid
        else:
            print("funnel already has starting_step_id ->",
                  existing["starting_step_id"], "- left untouched")

    r = sgql(
        'mutation($id: ID!, $node: InputFunnel!){ updateFunnel(id:$id,node:$node){ '
        'id starting_step_id published steps { id uid slug title } } }',
        {"id": FUNNEL, "node": update})
    print("WROTE", json.dumps(r["updateFunnel"], indent=2))
