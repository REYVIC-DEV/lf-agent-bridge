#!/usr/bin/env python3
"""Step 12 footer: drop the social icons, wire the policy links to the popup.

Three changes:

1. REMOVE the social-icon row (block 67fee7c4). Verified it contained nothing but
   four <a aria-label>+<svg> pairs, all href="#" — no visible text — so the whole
   block goes. Frees 1,885 chars and four dead links.

2. ADD trigger ids to the four footer policy links, which were all href="#" with
   no id:  Terms->terms, Privacy->priv, Editorial standards->edit,
   Affiliate policy->aff. These are the ids the popup script already listens for.

3. ADD the policy popup. Its markup + script come from step 3's block 067bf652 —
   the only place this modal exists, so reusing it is a deliberate exception to
   "no sections from other steps"; there is nothing to author from scratch here.

   **Improved on step 3's version:** step 3 ships the popup's <style> inside the
   body, which is exactly the in-body-stylesheet pattern that cost 2,703ms of
   style recalc there. Here the 1,019-char <style> is split out into
   settings.custom_html.header (renders in <head>) and only the markup + script
   go in the body — so step 12 keeps its 0 in-body <style> tags.

   The script is a delegated document click listener with preventDefault, so it
   works regardless of where the block sits and href="#" will not jump the page.
"""
import json, re, sys, uuid
sys.path.insert(0, ".")
import lf_api

FUNNEL = "fun_vGqQYxn4H2i_traYYkh4w"
STEP = "step_0hL9bV7NUmyESdgkwY4Ih"
SOCIAL = "67fee7c4"
POLICY = "5eeedf5b"
IDS = {"Terms": "terms", "Privacy": "priv",
       "Editorial standards": "edit", "Affiliate policy": "aff"}

popup = open("popup-src.html", encoding="utf-8").read()
m = re.search(r"<style>.*?</style>", popup, re.S)
assert m, "no <style> in the popup source"
popup_css = m.group(0)
popup_rest = (popup[:m.start()] + popup[m.end():]).strip()
assert ".tu-overlay" in popup_css and "tu-overlay" in popup_rest
assert "<style" not in popup_rest, "style left in the body part"

tok = open(".session_token").read().strip()
acct = open(".lf_account").read().strip()
h = lf_api.session_headers(acct)
node = lf_api.get_funnel_steps(tok, FUNNEL, extra_headers=h)
s = {x["uid"]: x for x in node["steps"]}[STEP]
was_str = isinstance(s["body"], str)
body = json.loads(s["body"]) if was_str else s["body"]

log = {"social_removed": 0, "ids_added": 0}

def walk(x):
    if isinstance(x, dict):
        for v in x.values():
            walk(v)
    elif isinstance(x, list):
        for i in range(len(x) - 1, -1, -1):
            v = x[i]
            if isinstance(v, dict):
                pid = str(v.get("id", ""))[:8]
                if pid == SOCIAL:
                    c = (v.get("p") or {}).get("content") or ""
                    assert re.sub(r"<[^>]+>", "", c).strip() == "", \
                        "social block has visible text — not removing"
                    del x[i]
                    log["social_removed"] += 1
                    continue
                if pid == POLICY:
                    p = v.get("p") or {}
                    c = p.get("content") or ""
                    assert 'id="' not in c, "policy links already have ids"
                    for label, tid in IDS.items():
                        old = f'<a href="#" style="color:#bdbdbd;text-decoration:none">{label}</a>'
                        assert old in c, f"link markup for {label!r} not found"
                        c = c.replace(old, old.replace('<a href="#"', f'<a href="#" id="{tid}"'), 1)
                        log["ids_added"] += 1
                    p["content"] = c
            walk(v)

walk(body)
assert log["social_removed"] == 1, log
assert log["ids_added"] == 4, log

# Append the popup into the last Section's container, the same depth step 3 uses
# (/p/children[2]/p/children[0]). The tree nests through p.children, not children.
sections = ((body.get("p") or {}).get("children") or [])
assert sections and sections[-1].get("t") == "Section",     f"unexpected root children: {[c.get('t') for c in sections]}"
container = ((sections[-1].get("p") or {}).get("children") or [])
assert container, "last Section has no container"
container[-1].setdefault("p", {}).setdefault("children", []).append({
    "t": "HtmlElement", "id": str(uuid.uuid4()),
    "p": {"content": popup_rest},
    "styles": [{"prop": "maxWidth", "value": "100%"}],
})
print(f"social row removed, {log['ids_added']} trigger ids added, popup appended "
      f"({len(popup_rest)} chars body / {len(popup_css)} chars CSS to <head>)")

# popup CSS -> custom_html.header
st = s["settings"]
st = json.loads(st) if isinstance(st, str) else dict(st or {})
ch = dict(st.get("custom_html") or {})
hdr = ch.get("header") or ""
assert ".tu-overlay" not in hdr, "popup CSS already in the step header"
ch["header"] = hdr.rstrip() + "\n\n<!-- policy popup CSS (markup+script live in the body block) -->\n" + popup_css + "\n"
st["custom_html"] = ch

lf_api.gql(tok, "mutation($id:ID!,$node:InputFunnel!){updateFunnel(id:$id,node:$node){id}}",
           {"id": FUNNEL, "node": {"steps": [{
               "id": STEP, "slug": s["slug"], "title": s["title"], "type": s["type"],
               "settings": st, "visual": s["visual"],
               "body": json.dumps(body) if was_str else body}]}}, extra_headers=h)
print("write ok")
