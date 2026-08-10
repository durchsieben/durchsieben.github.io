# CHG-003 — Restore and manage WordPress draft articles

## Request

Direct operator request: "add support for draft and released articles so all are restored from the XML and JSON and both can be removed from the project"

## Affected capability

- [CAP-001 — Static site and legacy-route compatibility](../../product/capabilities/CAP-001-static-site-and-route-compatibility.md)

## Phase 1 — Restore retained article source [done]

- Import all 109 released posts and 28 drafts from the WXR export. Reconcile released post/page IDs with the recorded public API JSON snapshots before writing content.
- Store drafts separately from released posts so they remain repository source but produce no routes, feed entries, or RSS entries.
- Add an ID-based removal command that updates the retained content and route manifest for either state while keeping the ignored WXR backup intact for re-import.

## Verification

- A clean import reports 109 released posts, 28 drafts, 3 pages, and 78 media files.
- `python3 scripts/remove_wordpress_articles.py 22 992 --dry-run` identifies one released post and one draft without modifying the project.
- A temporary project copy verifies real removal of both states updates counts and removes the released route.
- `pnpm check && pnpm build && pnpm verify` passed: Astro emitted 114 public pages and `pnpm verify` reported 113 routes, 109 released posts, 28 drafts, 3 pages, 78 media files, and passing local links.
