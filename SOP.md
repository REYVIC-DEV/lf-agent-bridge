# Team SOP — Building Pages from Figma with Claude

A step-by-step guide for turning a **Figma design** into a real page using Claude
Code. You don't need to write code — you mostly *talk* to Claude in plain English
and it does the building for you.

**There are two places a page can go**, and they work differently. Pick one before
you start:

| | **Lightfunnels** | **The website** |
|---|---|---|
| Where it lives | a funnel page on Lightfunnels | a page on `hlthtrack.com` |
| Going live | you publish, and it's live immediately — **no staging** | Claude pushes to `staging` for review first |
| Use it for | funnels, offers, quick tests | blog articles, advertorials, campaign pages |
| Follow | Section 4 | **Section 4B** |

> **TL;DR (Lightfunnels):** open your Figma file → "build this Figma design as a
> Lightfunnels page" → review the preview → ask for tweaks → publish.
>
> **TL;DR (the website):** open **both** the desktop and mobile Figma frames → tell
> Claude where the page should live → it builds and checks it → you review → it asks
> before pushing to `staging`.

---

## 1. What this tool does

Normally you'd rebuild a landing page by hand — dragging blocks in the Lightfunnels
editor, or writing code for the website — matching fonts, colours and spacing to a
design by eye. This tool lets **Claude** do that for you:

- It **reads the design straight from Figma** (exact colours, fonts, sizes, images).
- It **builds the page**, either in Lightfunnels or in the website's code.
- It handles **desktop and mobile** layouts.
- It then **checks its own work against the design**, element by element, and tells you
  what doesn't match — see Section 4C.
- You **review** and ask for changes in plain language.
- When it looks right, you **publish** (Lightfunnels) or Claude **asks** before pushing
  to `staging` (the website).

Think of it as an assistant that builds the page, guided by the design and your
feedback — and then marks its own homework so you're not the one hunting for what's off.

---

## 2. What you need (once)

1. **Claude Code** installed on your computer (the app you type instructions into).
2. **The project folder** (`lf-agent-bridge`) on your computer.
3. **The Figma desktop app** with the **Figwright plugin** installed — this is how
   Claude reads your design (see Section 3A). With Figwright you **don't need any
   Figma key**; it just reads whatever file you have open.
4. **Your own Lightfunnels sign-in.** You do this yourself with one command —
   `python3 lf.py login` (Section 3B). It saves your session and refreshes itself
   automatically, so you rarely repeat it. **You never copy or paste any token by
   hand.**
5. **For website pages only** — the storefront code on your computer at `~/hlth-site`,
   on the `staging` branch. Whoever sets this up clones it once (the steps are in
   `webforge/README.md`). You don't run anything in it yourself; Claude starts and stops
   the local site for you.

> One-time technical bits (installing the repo, and an optional permanent
> Lightfunnels app key for read-only listing) are handled once by whoever sets this
> up. As a day-to-day user, your only sign-in is `python3 lf.py login`.

> 🔒 **Never share, screenshot, or commit any keys** (the hidden `.env` file or your
> login session). They're like passwords — they stay on the computer.

---

## 3. One-time setup (do this once)

### A. Connect Figma (so Claude can read designs)

1. Open the **Figma desktop app** (not the browser version).
2. Open the design file you want to build from.
3. Run the **Figwright** plugin: **Menu → Plugins → Development → Figwright**.
4. Leave it running — it should say **"Connected."**

That's it. As long as Figwright is connected and your file is open, Claude can
read whatever design you have open.

### B. Sign in to Lightfunnels (so Claude can save pages)

In Claude Code, type:

```
run: python3 lf.py login
```

A browser window opens. **Sign in to Lightfunnels normally** (2-factor is fine).
This saves your session so Claude can create and edit pages — no tokens to copy.
It **refreshes itself automatically**, so you usually never touch this again; only
rerun `python3 lf.py login` if Claude ever says your session fully expired.

### C. Quick test

Ask Claude:

> "List my Lightfunnels funnels."

If it shows a list, you're ready. 🎉

---

## 4. Build a **Lightfunnels** page from a Figma design

*(For the website instead, skip to Section 4B.)*

### Step 1 — Open the design in Figma
Open the Figma file and make sure the **Figwright plugin says Connected**.

### Step 2 — Give Claude the design
Copy the Figma link for the exact frame you want (right-click the frame in Figma →
**Copy link to selection**), then tell Claude what you want. For example:

> "Build this Figma design as a **new** Lightfunnels page for testing:
> `<paste Figma link>`. Match it exactly, including the footer."

Be clear about:
- **New page vs. edit an existing one** ("create a new funnel" vs. "edit funnel X").
- **Any links/buttons** and where they should go (e.g. "the Buy button links to
  `https://…`").
- **Anything specific** you care about (footer, disclaimers, star ratings, etc.).

### Step 3 — Let Claude work
Claude will read the design in detail (this can take a few minutes for long pages —
that's normal; it's measuring every element so it matches). It then builds the page.

### Step 4 — Review the preview
Claude gives you a **preview link**. Open it in your browser.
- To check **mobile**, open it on your phone or make your browser window narrow.

### Step 5 — Ask for tweaks
Tell Claude what's off, in plain words. Examples:

> "The Trustpilot stars should be green for the top product."
> "On mobile the cost table text is too small — match the Figma."
> "The footer is missing the disclaimer."

Claude fixes it and gives you an updated preview. Repeat until it looks right.

### Step 6 — Publish (when approved)
When you're happy, tell Claude:

> "Publish it."

⚠️ **Claude will always confirm before publishing or deleting.** Publishing makes
the page live. If you're not ready, say "not yet."

---

## 4B. Build a page into the website (instead of Lightfunnels)

Same idea, three real differences: Claude needs **both** Figma frames, it will **ask you
where the page goes**, and nothing reaches the internet until you say so.

### Step 1 — Have both frames ready

The desktop frame and the mobile frame are **two designs, not one that reflows**. Copy
the link for each (right-click the frame → **Copy link to selection**).

If you only give one, only that one gets checked — and a phone layout nobody looked at is
where the traffic is.

### Step 2 — Say where the page should go

**Claude will ask, and it should.** It cannot tell from the design, because it isn't a
design question — it's a question about what the page is *for*. Two answers matter:

| You want | Answer |
|---|---|
| A **reusable layout** future articles get copied from | *"a blog template"* → `/blog/template/<name>` |
| A **live page** taking real traffic (email, ads, search) | *"a live page"* → `/pages/<name>`, and say so |

⚠️ **This matters more than it sounds.** A `/blog/template/` page is deliberately
invisible: not in Google, not linked anywhere, and it **shows a 404 on the real
website**. That's the guard working. But it also means **you cannot send email or ad
traffic to it** — tell Claude it's a live page and it will build it somewhere reachable.

Getting it wrong isn't fatal — Claude can move it — but a page that went public when it
shouldn't have has already been seen.

### Step 3 — Give Claude the job

> "Build these Figma frames into the website as a **blog template** called
> `founder-story`: desktop `<link>`, mobile `<link>`. Match them exactly."

Mention anything you care about: where buttons link, whether prices come from the real
store, whether the page should be findable in Google.

### Step 4 — Let it build and check itself

Claude builds the page, starts the site on your own computer, and runs the checks in
Section 4C. It'll tell you what doesn't match.

Some findings are **questions, not bugs** — if the two frames disagree with each other
(one says £79, the other £67.15) Claude will not pick for you. It stops and asks, because
guessing at a price is worse than waiting.

### Step 5 — Review it yourself

Claude gives you a local link (like `http://localhost:3000/blog/template/founder-story`).
Open it. Resize the window narrow to check mobile.

**Do this even when every check passed.** The checks don't read hover effects, animation,
or whether the offer is the one anyone agreed to. They also can't tell you the page is
*wrong for the campaign* — only that it matches the drawing.

### Step 6 — Ask for tweaks

Same as Lightfunnels — plain words, be specific:

> "The quote is too heavy — check the Figma, I think it's the lighter font."
> "The last photo is cropped tighter than the design."

### Step 7 — Push to staging (Claude will ask)

When you say the page looks right, Claude asks:

> The page is passing. Push these changes to `staging`?

Nothing is pushed until you answer. **Saying "the page looks good" is not the same as
saying "push it"** — Claude treats those as two separate answers on purpose.

Once it's on `staging`, whoever normally reviews and releases the website takes it from
there. Claude never pushes to `main`.

---

## 4C. What Claude checks, and what it can't

Claude checks its own work against the design so you're not the one hunting for what's
off. Worth knowing where the line is.

**It checks:**

- **Every word**, exactly — missing copy, and copy that was retyped instead of copied
- **Type** — size, weight, colour, and the actual **typeface**
- **Boxes** — widths, backgrounds, corner roundness, borders
- **Spacing** — gaps between elements and between sections
- **Photos** — whether they loaded, their shape, and **whether they show the right part
  of the picture**
- Plus the usual: page speed, broken links, social preview, four screen widths, browser
  errors, and accessibility

**It cannot check:**

- Letter spacing, text alignment, shadows
- Hover and click states, animation
- **Whether the page is right** — only whether it matches the drawing

That last one is the important one. Everything can pass and the page can still be
wrong for what you're trying to do. That's your call, which is why Section 4B Step 5
exists.

**One thing it deliberately ignores:** some numbers are meant to be live rather than
copied from the design. The Trustpilot score and review count are read from the real
Trustpilot feed every hour, so the design's frozen "4.5 / 272 reviews" is *supposed* to
be out of date. Claude records that as a deliberate exception with the reason, so it
stops being reported as a fault. If you see something listed as an "accepted deviation",
that's what it means — someone decided it, on purpose.

## 5. Other common tasks

**Edit wording on an existing page**
> "On funnel `<name/id>`, change 'Customer Reviews' to 'Verified Buyer Reviews'."

Claude reads the real page text first, then makes the exact change.

**Duplicate an existing page as a starting point**
> "Duplicate the `<name>` funnel and call it `<new name>`."

**Make a page mobile-friendly / match the mobile design**
> "Here's the mobile Figma frame: `<link>`. Make the mobile view match it."

**Change where a button links**
> "Point the 'Visit Site' buttons to `https://…`."

---

## 6. Do's and Don'ts

✅ **Do**
- Keep the Figma file **open** with **Figwright connected** while Claude works.
- Give Claude the **exact Figma link** for the frame you want.
- **Review the preview** on both desktop and mobile before publishing.
- Be specific with feedback ("the second heading should be 22px and centered").

✅ **Do — for website pages**
- Give Claude **both** Figma frames, desktop and mobile.
- **Tell it where the page goes** — a template, or a live page. It will ask; have the
  answer ready.
- **Open the page yourself** before saying it's right, even when every check passed.

🚫 **Don't**
- Don't share, screenshot, or commit the access keys (`.env`, session token). They're
  private, like passwords.
- Don't publish until you've reviewed the preview.
- Don't edit a live, published page directly for big experiments — ask Claude to test
  on a **duplicate** first.
- Don't send email or ad traffic to a `/blog/template/…` link — it shows a **404** on the
  real website. Ask Claude to move it to a live page first.
- Don't treat "all checks passed" as "ready to ship". The checks compare the page to the
  drawing; they can't tell you the drawing was right.

---

## 7. Troubleshooting

| Problem | What to do |
|---|---|
| Claude says it **can't read the Figma design** | Make sure the **Figma desktop app** is open, the right file is open, and the **Figwright plugin says Connected**. Then ask Claude to try again. |
| The preview page is **blank or 404** | A brand-new page may need publishing before it shows. Tell Claude — it can publish or refresh the preview. |
| The preview **looks out of date** | Previews are cached. Ask Claude to "refresh the preview" (it changes the link so you see the latest). |
| Claude says the **Lightfunnels session expired** | Run `python3 lf.py login` again and sign in. |
| A change **didn't save** | Ask Claude to confirm it saved in "session mode" — real edits need your login session, which the setup handles automatically. |
| Something looks **slightly off vs. Figma** | Point Claude at the specific element or Figma frame link and say what's wrong. It re-measures the design and fixes it. |
| **Website page shows a 404** on the real site | Expected if it's at `/blog/template/…` — those are hidden on purpose. If it needs to be public, tell Claude to make it a live page. |
| Claude says the page **doesn't match the design** but you can't see it | Ask it to show you `todo.md` — the merged list of what's off, per screen width. |
| A finding **keeps coming back** and it's intentional | Say so. Claude records it as an "accepted deviation" with the reason, and stops reporting it. |
| The two Figma frames **disagree** (different price, different numbers) | Only you can settle it. One page serves both screen sizes, so one of the two has to win. |

---

## 8. A few words that help you talk to Claude

- **Funnel** = a Lightfunnels project that contains one or more pages.
- **Step / page** = a single page inside a funnel.
- **Preview link** = a private link to see the page before it's live.
- **Publish** = make the page live to the public.
- **Session** = your Lightfunnels login that lets Claude actually save pages.
- **Figwright** = the Figma plugin that lets Claude read your open design.
- **Breakpoint** = a screen width the design was drawn at (390 for phones, 1440 for
  desktop). Each one gets checked separately.
- **Template** (website) = a reusable layout future pages get copied from. Deliberately
  hidden and **404s on the real site**.
- **Live page** (website) = a page real visitors can reach and Google can find.
- **Staging** = the review copy of the website. Website changes go there first, never
  straight to the real site.
- **Accepted deviation** = a place the page differs from the design *on purpose*, with
  the reason written down.

---

## 9. Golden rules (for consistent results)

1. **Always work from the real Figma design** — Claude matches the exact node, so
   keep the correct frame open in Figma.
2. **Both frames, every time** — desktop and mobile are two designs, not one that
   reflows. One frame means one checked layout.
3. **Say where the page goes before it's built** — template or live page. Claude will
   ask rather than guess, because guessing wrong either hides a page meant for traffic or
   publishes one that wasn't.
4. **Review before you publish or push** — open it on desktop *and* mobile yourself. A
   green check means it matches the drawing, not that it's right.
5. **Ask for exact changes** — the more specific your feedback, the closer the match.
6. **Keep keys private** — never share the `.env` or login token.

---

*Questions or something not working? Grab whoever set this up, or open an issue in
this GitHub repo.*
