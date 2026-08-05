# Team SOP — Building Lightfunnels Pages from Figma with Claude

A step-by-step guide for turning a **Figma design** into a live **Lightfunnels
page** using Claude Code. You don't need to write code — you mostly *talk* to
Claude in plain English and it does the building for you.

> **TL;DR:** Open your Figma file → tell Claude "build this Figma design as a
> Lightfunnels page" → review the preview link → ask for tweaks → publish.

---

## 1. What this tool does

Normally you'd rebuild a landing page by hand inside the Lightfunnels editor —
dragging blocks, matching fonts, colors, and spacing to a design. This tool lets
**Claude** do that for you:

- It **reads the design straight from Figma** (exact colors, fonts, sizes, images).
- It **builds the page inside Lightfunnels** for you, matching the design.
- It handles **desktop and mobile** layouts.
- You **review a preview link** and ask for changes in plain language.
- When it looks right, you **publish**.

Think of it as an assistant that edits Lightfunnels for you, guided by the Figma
design and your feedback.

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

## 4. Build a page from a Figma design (the main workflow)

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

🚫 **Don't**
- Don't share, screenshot, or commit the access keys (`.env`, session token). They're
  private, like passwords.
- Don't publish until you've reviewed the preview.
- Don't edit a live, published page directly for big experiments — ask Claude to test
  on a **duplicate** first.

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

---

## 8. A few words that help you talk to Claude

- **Funnel** = a Lightfunnels project that contains one or more pages.
- **Step / page** = a single page inside a funnel.
- **Preview link** = a private link to see the page before it's live.
- **Publish** = make the page live to the public.
- **Session** = your Lightfunnels login that lets Claude actually save pages.
- **Figwright** = the Figma plugin that lets Claude read your open design.

---

## 9. Golden rules (for consistent results)

1. **Always work from the real Figma design** — Claude matches the exact node, so
   keep the correct frame open in Figma.
2. **Review before you publish** — always open the preview on desktop *and* mobile.
3. **Ask for exact changes** — the more specific your feedback, the closer the match.
4. **Keep keys private** — never share the `.env` or login token.

---

*Questions or something not working? Grab whoever set this up, or open an issue in
this GitHub repo.*
