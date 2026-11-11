#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""A simple thank-you page, to redirect to after payment on Whop.

JOSHUA, 2026-11-04: shared a chat screenshot settling the copy -- "yes
thank you page", "or C u in Bangkok", "tapos sa baba for questions email
hello@scalingorfailing.com" -- then "create me a simple thank you page we
will redirect there after payment on whop".

Read as: a confirmation line (thank you / you're in), "See You In Bangkok"
as the main line underneath, and the support email at the bottom ("tapos
sa baba" = "then at the bottom"). Combined rather than picked between,
since the two phrases read as headline + subheading, not two options for
the same line.

Built as a plain standalone HtmlElement, same pattern as buy-link and the
other recent additions -- NOT run through build_sof_event.py. That
builder rewrites an entire page body from a 200KB+ script meant for the
main ticket page's own layout (nav, hero, speaker grid, FAQ); a one-screen
static confirmation page has none of that and pulling it into the shared
builder risks exactly the kind of cross-page mistake this project has hit
before (SOF_PAGE vs SOF_SLUG). A few inline styles, matching the site's
own navy/gold palette by eye, is the right amount of engineering for a
page whose entire job is to be read once and closed.

Lives on the MAIN funnel (fun_RoOL_WXDCAxK4hEk0v5xX), not the sof-checkout
test funnel, because this needs a real, permanent, live URL for Whop's own
dashboard to redirect to -- not a test artifact.

    https://www.scalingorfailing.com/event/thank-you

⚠️ Setting Whop to actually redirect here is a WHOP DASHBOARD setting,
not something this script or this repo can do -- there is no Whop API
key configured anywhere in this project (checked before writing this).
Once the page is live, the one remaining step is pasting this URL into
whatever field Whop's checkout/product settings expose for a
post-payment redirect.

    py funnels/sof/scaling-or-failing/edits/add_thank_you_step.py
    py funnels/sof/scaling-or-failing/edits/add_thank_you_step.py --apply
"""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", "..", "..", ".."))
sys.path.insert(0, ROOT)
os.chdir(ROOT)
import lf_api

FUNNEL = "fun_RoOL_WXDCAxK4hEk0v5xX"
SLUG = "thank-you"
LOGO_PATH = ("https://assets.lightfunnels.com/account-90380/images_library/"
             "52e02c2e-5a33-48e2-af68-7f7010d89b00._5dGZ_Nl-HGsVJlNnoUXb.webp")
# Same "Scalizard recommends" mascot used on the ticket card
# (`vip_sticker` in pagescore/.cache/sof_img_map.json) -- Eline asked for it
# here too, in place of the generic checkmark that was removed earlier.
SCALIZARD_PATH = ("https://assets.lightfunnels.com/account-90380/images_library/"
                  "3e14af5e-fdf8-442b-9317-1d0b608d4125.webp")
APPLY = "--apply" in sys.argv

HTML = """
<div style="background:#0B1A32;padding:24px;text-align:center">
  <img src="%(logo)s" alt="Scaling or Failing"
       style="height:44px;width:auto;max-width:220px;object-fit:contain">
</div>
<div style="max-width:560px;margin:0 auto;padding:100px 32px;text-align:center;
            font-family:Inter,sans-serif">
  <img src="%(scalizard)s" alt="Scalizard"
       style="width:100px;max-width:100px;height:auto;aspect-ratio:1/1;
              margin:0 auto 20px;display:block">
  <p style="font-size:14px;font-weight:700;letter-spacing:.08em;
            text-transform:uppercase;color:#A3051B;margin:0 0 12px">
    You're In</p>
  <h1 style="font-size:36px;font-weight:700;margin:0 0 16px;color:#041C32;
             line-height:1.2">
    Cu in Bangkok!</h1>
  <p style="font-size:17px;color:#57637A;margin:0 0 8px;line-height:1.5">
    December 7&ndash;8, 2026. Watch your inbox for your event invite,
    and please allow a little time to receive it.</p>
  <p style="font-size:15px;color:#57637A;margin:40px 0 0;line-height:1.6">
    Questions? Email
    <a href="mailto:hello@scalingorfailing.com"
       style="color:#041C32;font-weight:700;text-decoration:underline">
      hello@scalingorfailing.com</a>
  </p>
  <a href="https://www.scalingorfailing.com/"
     style="display:inline-block;margin-top:40px;padding:14px 32px;
            background:#041C32;color:#fff;border-radius:9999px;
            font-weight:700;font-size:15px;text-decoration:none">
    Back to the event page</a>
</div>
""" % {"logo": LOGO_PATH, "scalizard": SCALIZARD_PATH}


def main():
    ACCT = open(".lf_account").read().strip()
    HH = lf_api.session_headers(ACCT)
    n = lf_api.gql(
        None,
        """query($id:ID!){node(id:$id){... on Funnel{
             steps{uid slug title type product_id settings visual{x y}}}}}""",
        {"id": FUNNEL}, extra_headers=HH)["node"]
    existing = next((s for s in n["steps"] if s["slug"] == SLUG), None)

    body = {
        "id": "root-thank-you", "t": "Root", "version": 11,
        "styles": [{"prop": "pageWidth", "value": "1140px"},
                   {"prop": "backgroundColor", "value": {"r": 255, "g": 255, "b": 255, "a": 1}}],
        "p": {"children": [{
            "t": "Section", "id": "thank-you-section",
            "styles": [{"prop": "margin", "value": "0px"}, {"prop": "padding", "value": "0px"}],
            "p": {"layout": "", "children": [{
                "t": "HtmlElement", "id": "thank-you-html",
                "styles": [{"prop": "width", "value": "100%"}],
                "p": {"content": HTML},
            }]},
        }]},
    }

    settings = {"seo": {
        "title": "You're In: Scaling or Failing",
        "description": "You're registered for Scaling or Failing, Bangkok, December 7-8 2026.",
    }}

    print("page body: %d bytes" % len(json.dumps(body)))

    if not APPLY:
        print("dry run. pass --apply to write.")
        return

    others = [{"id": s["uid"], "slug": s["slug"], "title": s["title"], "type": s["type"],
               "settings": s["settings"], "visual": s["visual"], "product_id": s.get("product_id")}
              for s in n["steps"] if s["slug"] != SLUG]

    if existing:
        mine = {"id": existing["uid"], "slug": SLUG, "title": "Thank You: Scaling or Failing",
                "type": "article_page", "settings": settings,
                "visual": existing["visual"], "body": body}
        print("replacing existing thank-you step")
    else:
        created = lf_api.gql(
            None,
            'mutation($fid:ID!,$node:InputStep!){createStep(funnel_id:$fid,'
            'node:$node){step{id uid slug}}}',
            {"fid": FUNNEL, "node": {
                "slug": SLUG, "title": "Thank You: Scaling or Failing",
                "type": "article_page", "settings": settings,
                "visual": {"x": 1800, "y": 420}, "body": body}},
            extra_headers=HH)
        sid = created["createStep"]["step"]["id"]
        print("created detached step ->", created["createStep"]["step"])
        mine = {"id": sid, "slug": SLUG, "title": "Thank You: Scaling or Failing",
                "type": "article_page", "settings": settings, "visual": {"x": 1800, "y": 420}}

    r = lf_api.gql(
        None,
        "mutation($id:ID!,$node:InputFunnel!){updateFunnel(id:$id,node:$node){"
        "id steps{uid slug type}}}",
        {"id": FUNNEL, "node": {"steps": others + [mine]}}, extra_headers=HH)
    print(json.dumps(r, indent=1))
    print("\nlive at: https://www.scalingorfailing.com/event/%s" % SLUG)


main()
