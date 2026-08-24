# funnels/ — local funnel workspaces

Lightfunnels is the live system of record; this folder is the **local working
copy** — what a funnel is made of, what we changed, and why. A *workspace*
groups related funnels (one brand, store, or campaign) so variants sit next to
their master instead of being scattered across the LF dashboard.

```
funnels/
├─ _template/                    skeletons to copy (see below)
│  ├─ workspace.json             → a new workspace root
│  └─ funnel/                    → a new funnel folder
└─ <workspace>/                  a brand / store / campaign
   ├─ workspace.json             store domain, LF account id, master funnel id
   └─ <funnel-slug>/             one funnel
      ├─ funnel.json             LF id, name, slug, published, what it came from
      ├─ NOTES.md                what this variant tests / why it exists
      ├─ steps/<step-slug>.json  captured page bodies (`capture --out`)
      ├─ texts/<label>.json      copy snapshots (`texts` output)
      └─ edits/<label>.json      reusable edit sets (`edit --file`)
```

Workspace and funnel folder names are **slugs** (lowercase, hyphens) and should
match the LF slug where one exists — that's what makes the mapping obvious.

## Start a workspace, then a funnel

```bash
# new workspace
mkdir -p funnels/<workspace>
cp funnels/_template/workspace.json funnels/<workspace>/

# new funnel inside it
cp -r funnels/_template/funnel funnels/<workspace>/<funnel-slug>
```

PowerShell: `Copy-Item -Recurse funnels/_template/funnel funnels/<ws>/<slug>`.

Then fill in `funnel.json` (the LF `id` is the one thing everything else keys
off), add the slug to the workspace's `funnels` list, and record the intent in
`NOTES.md`.

## Pull the live state down

Run from the **project root**:

```bash
# structure: ids, slugs, step uids
python3 lf.py funnel <funnel_id> \
  > funnels/<ws>/<funnel>/funnel.live.json

# copy, per step — read this before writing any `edit`
python3 lf.py texts <funnel_id> \
  > funnels/<ws>/<funnel>/texts/current.json

# a page body, for cloning or diffing layout
python3 lf.py capture <funnel_id> <step_uid> <step-slug> \
  --out funnels/<ws>/<funnel>/steps/
```

`funnel.live.json` is a raw dump, refreshed whenever you need it.
`funnel.json` is hand-maintained — the durable facts plus our intent.

## Push changes back

Edit sets live in `edits/` so a change is reviewable before it touches the live
page, and repeatable across variants:

```json
{ "Customer Reviews": "Verified Buyer Reviews", "Get My Plan": "Start Tonight" }
```

```bash
python3 lf.py edit <funnel_id> --session \
  --file funnels/<ws>/<funnel>/edits/<label>.json
```

Order of operations that avoids surprises: `texts` → write the edit set →
`edit --session` on a **duplicate** first → verify → then the real funnel.

## Conventions worth keeping

- **Everything here is committed**, including captured bodies — the diff of a
  page body across variants is the point. No tokens or secrets in this folder;
  those stay in `.env` (gitignored).
- **A funnel folder is never authoritative over LF.** If they disagree, re-pull.
  Note the pull date in `NOTES.md` when it matters.
- **Duplicates inherit `published`.** New variant → `publish --off` immediately,
  and say so in `NOTES.md`.
- `templates/` is the old shared capture dir (gitignored).
  Prefer `capture --out` into a workspace; keep templates/ for scratch.
