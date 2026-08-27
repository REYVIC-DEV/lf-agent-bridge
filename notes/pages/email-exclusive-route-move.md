---
categories:
  - "[[Web-Tech]]"
subjects:
  - "[[Lightfunnels]]"
focus_area: email-exclusive-route-move
status: live
created: 2026-08-26
---

# email-exclusive-route-move

| | |
|---|---|
| URL | http://localhost:3000/blog/template/email-exclusive |
| Builder | `-` |
| Funnel | `-` |

Part of [[LF Page Pipeline]].

## Open questions

<!-- questions -->
- [ ] Soft 404 on /pages/* (pre-existing, not from this move): a missing Shopify handle returns HTTP 200 with the branded not-found body, in a production build. Every /pages/<anything> is a soft 404. Worth a look — it is in app/[locale]/pages/[handle], which serves the whole Shopify pages surface, so I have not touched it. — [[2026-08-26-email-exclusive-route-move]]
- [ ] Offer price — the 1440w frame says £79 / Save 50%, the 390w frame says £67.15 / Save 57%. Still the only fidelity failure, and now explicitly a template-content question rather than a live-offer one. — [[2026-08-26-email-exclusive-route-move]]

## Session history

<!-- history -->
- 2026-08-26 — [[2026-08-26-email-exclusive-route-move]] — email-exclusive moved to /blog/template, and the routing rule written down (in-progress)
