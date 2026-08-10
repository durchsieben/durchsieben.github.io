# CHG-002 — Editorial redesign: search-first homepage, modern typography

## Request

Direct operator request: redesign the blog theme to a modern dark/light-supported design, promote articles on the homepage, sort by date (newest first), integrate a search at the top, and use a newspaper-style reading font that works on desktop and mobile (Medium-style).

## Affected capability

- [CAP-001 — Static site and legacy-route compatibility](../../product/capabilities/CAP-001-static-site-and-route-compatibility.md)

## Decisions and constraints

- The homepage is the archive. Search + topic filter live directly above the article feed; the old standalone `/artikeluebersicht/`-as-page fallback is removed because the homepage now shows the full set.
- Articles are server-rendered newest-first on the homepage; the search and topic filter are client-side, working against the embedded JSON payload so the site stays static.
- Typography uses Source Serif 4 for editorial reading and Inter for UI, matching the Medium/newspaper feel; colors use OKLCH light/dark tokens with system-aware defaults plus a toggle.
- All 109 posts, 3 pages, 78 media files, and 113 legacy routes are preserved. No source content or `sourcePath` is changed.

## Verification

- `pnpm check` (0 errors, 0 warnings).
- `pnpm build` (114 pages emitted, 109 article + 3 page + 1 homepage + 1 RSS).
- `pnpm verify` (`{"routes": 113, "posts": 109, "pages": 3, "media": 78, "localLinks": "PASS"}`).
- Visual check: home has hero + search pill + 9 topic pills + 109 article rows in newest-first order (top row `2022-08-11`).

## Follow-up

- Phase 4 (DNS cutover) of CHG-001 remains in progress and is unaffected by this change.
