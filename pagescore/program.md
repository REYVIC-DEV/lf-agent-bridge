LANDING PAGE QA RUNBOOK
Standard operating procedure for QA of advertorials, funnels, and landing pages.
Written from the techunboxed.co QA run of 21 Aug 2026.

Seven phases, run in order. One report per page, in the standard format at the end.


PHASE 0 - SCOPE THE PAGE

Record the exact URL you were given.

Load it once and note whether it redirects. Funnel roots often forward to a slug (example: techunboxed.co/ redirects to /smartwatch-review/xNlR_CA6j). All checks run against the final URL, but the redirect itself is a speed finding - each hop adds real load time for paid traffic.

List every page in scope. One report per page.


PHASE 1 - SPEED

Run Lighthouse twice: desktop and mobile. PageSpeed Insights (pagespeed.web.dev) gives both plus real-user Core Web Vitals data when available. Record the metrics, not just the headline score. Mobile matters more than desktop for paid social traffic - if you can only run one, run mobile.

Pass criteria:
- Performance score: 90 or higher = pass, 80-89 = flag, below 80 = fail
- LCP under 2.5 seconds
- CLS under 0.1
- TBT under 200 ms
- Total page weight under 2 MB
- Zero redirect hops on the URL ads point to


PHASE 2 - LINKS

Collect links from TWO sources, because they differ: the raw HTML (what curl sees) and the rendered DOM (what the browser builds after JavaScript runs). On Lightfunnels pages, most buy buttons and footer links only exist in the rendered DOM.

To pull rendered links, run this in the browser console on the live page:

[...document.querySelectorAll('a[href]')].map(a => a.getAttribute('href') + ' | ' + a.innerText.trim())

Then request every URL and record the HTTP status.

Pass criteria:
- 200 (or a redirect ending in 200) = pass
- 404 / 410 / 5xx = fail
- href="#" or javascript:void(0) on a real link (Terms, Privacy) = fail. This is also an ad-account compliance risk.
- 403 from bot-protected sites (Trustpilot, Amazon) is NOT a fail. Verify those by opening them once in a normal browser.
- Affiliate links: confirm the tag parameter is present (example: tag=techunboxed04-20)


PHASE 3 - HEADLINE, META AND SOCIAL SHARING

View source on the final URL and pull the title tag, meta description, and every og: tag. Then compare against what the rendered page shows - JavaScript can overwrite the title after load.

Pass criteria:
- ONE headline. Title tag, rendered browser-tab title, og:title, and the on-page headline all carry the same message.
- Meta description exists and is actually written. It must not be the title repeated. 140-160 characters, sells the click.
- og:image returns 200, is roughly 1200 x 630 (1.91:1 ratio), under 1 MB, and actually depicts the offer. Paste the URL into a share-preview tool or a private Slack message to see it render.
- Exactly one h1 tag containing the headline. A styled div does not count.


PHASE 4 - RESPONSIVENESS

Test four viewports, in this order: 1440 (desktop), 768 (tablet), 375 (common phone), 320 (smallest supported phone).

At each width:
1. Take a full-page screenshot.
2. Run the overflow test in the console:
   document.documentElement.scrollWidth > window.innerWidth
   Then confirm it is real: window.scrollTo(50, 0); window.scrollX
   If scrollX is greater than 0, the page actually pans sideways.
3. Visually inspect the known trouble spots: comparison tables, embedded video, the references/citations block, image grids, the sticky CTA bar.

Pass criteria:
- No horizontal scroll at any width, 320px included
- Tables either reflow or scroll inside their own container; numbers never wrap mid-digit (like "£22 9")
- Long URLs (citations, references) wrap. The usual fix is overflow-wrap: anywhere on that block.
- Tap targets and CTAs remain full-width and reachable

If overflow exists but no element obviously sticks out, walk the DOM comparing each element's scrollWidth to its clientWidth until you find the container that is too wide. On the techunboxed page it was unbroken DOI URLs in the References section.


PHASE 5 - CONGRUENCY

Read the page as a skeptical customer and check that every number and claim agrees with itself.

- Prices: list every price on the page. Each product's price must be identical everywhere it appears, and stated totals must add up (Whoop 229 + 229 = 458, correct).
- Headline claims: any number in the headline ("We spent £1,581...") must be reconstructable from the page. If you cannot make the math work, flag it.
- Link labels: the text on a card or button must match the page it opens. Example found: a Further Reading card titled "Oura vs Whoop" opened an article titled "Budget vs Premium Fitness Trackers".
- Ratings: quoted review scores (Trustpilot 4.5 etc.) should match the live source page.
- Brand and domain consistency: product names, brand spelling, and domains consistent throughout.


PHASE 6 - CONSOLE AND ERRORS

With DevTools open, load the page and scroll it end to end.

Pass criteria:
- Zero console errors
- Warnings are triaged, not ignored: repeated preload/crossorigin warnings are minor performance issues; failed tracking-pixel requests are revenue issues
- No broken image requests in the Network tab


PHASE 7 - THE REPORT

Every QA run produces one report in this exact shape, so results are comparable across pages and over time.

1. SUMMARY TABLE
One row per check, three columns: Check, Result, Notes. Status first. Every check from phases 1-6 appears, including the passes.

Example rows:
Speed (mobile) | FLAG | LCP 3.0s, page weight 3.9 MB
Links | FAIL | "Terms" is href="#"; 28 of 29 pass
Mobile 320px | FAIL | 15px sideways scroll, references block
Social image | PASS | 1400x781, loads, on-message

2. ISSUE DETAIL TABLES
One short table per problem area (example: "Congruency issues") with a numbered row per issue: what it is, where it is, evidence.

3. PRIORITY FIX LIST
A ranked table. Order by risk to money and compliance, not by how easy the fix is: legal/ad-compliance first, then conversion blockers, then speed, then cosmetics.

4. SCREENSHOTS
Attach viewport-sized screenshots of each defect (a cropped shot of the broken table beats a 25,000-pixel full-page image), plus one full-page desktop capture for reference.

5. LIMITATIONS
Say what was not tested and why - bot-blocked sites verified manually, tools that only ran desktop, pages out of scope. A QA report that hides its gaps is not a QA report.

STATUS LEGEND (used everywhere):
PASS = meets criteria.
FLAG = works, but below target or inconsistent; fix when practical.
FAIL = broken, blocking, or a compliance risk; fix before spending on traffic.


TOOLING NOTE
Tools used in the original run: Lighthouse (via DataForSEO), curl for link status, Playwright for viewport testing and screenshots. Any equivalent tools work - the phases and pass criteria are the standard, not the tooling.