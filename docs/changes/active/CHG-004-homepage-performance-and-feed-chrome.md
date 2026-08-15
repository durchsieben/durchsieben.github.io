# CHG-004 — Homepage performance and feed chrome

## Request

Direct operator request: improve Lighthouse metrics for https://lighthouse-metrics.com/lighthouse/checks/fc3a2739-4784-4243-a375-e05bb5703406; remove the double line in the page title and the table borders on blog entries. Mid-turn: hide the homepage portrait on mobile.

## Affected capability

- [CAP-001 — Static site and legacy-route compatibility](../../product/capabilities/CAP-001-static-site-and-route-compatibility.md)

## Decisions and constraints

- The circled two-bar `.brand-mark` next to “Management÷7” is removed. Wordmark stays.
- The article feed is no longer a bordered table (no outer box, no 1px grid, no column rule). Rows use a single hairline separator.
- The homepage portrait is desktop-only. Mobile must not download it; CSS `display: none` alone is not enough.
- Homepage search filters title + excerpt. The initial HTML no longer embeds the full archive or a search JSON blob.
- The original `public/images/raphael-bossek-portrait.png` stays the about-page/importer asset. Rendered pages use AVIF/WebP derivatives.
- No imported Markdown, routes, or source content change.

## Phases

### Phase 1 — Presentation and payload [done]

1. Remove brand mark and feed table chrome.
2. Hide and skip-download the homepage portrait below 761px; serve sized AVIF/WebP above that.
3. Filter the feed in-DOM; drop the inline search JSON.

Gate: `pnpm check` 0 errors / 0 warnings; `pnpm build` 114 pages; `pnpm verify` `{"routes": 113, "posts": 109, "drafts": 28, "pages": 3, "media": 78, "localLinks": "PASS"}`. `dist/index.html` is 165 KB / 27 KB gzip (was 846 KB / 265 KB) and contains no `search-payload`. Portrait `<source>` elements are gated by `min-width: 761px`. Local mobile Lighthouse against `pnpm preview`: performance 81 (was 63), FCP 0.9s (was 4.6s), LCP 1.7s (was 12.5s), total bytes 199 KiB (was 2.17 MB).

### Phase 2 — First-paint cut [done]

Direct operator request: implement the remaining performance suggestions (paginate first paint, self-host serif, drop Inter/Google Fonts, data-URI pixel, about-page portrait).

1. Server-render the newest 20 rows. Remaining posts load via `Weitere Beiträge` or after idle from `/search-index.json`. Search/topic filter fetches that index on first use. No-JS users see 20 posts.
2. Self-host a Latin Source Serif 4 subset (`font-display: optional`). Drop Inter and the Google Fonts chain; UI uses the system sans stack.
3. Homepage fallback image is a data URI (no `empty.gif` request). About-page render rewrites the importer PNG to the same AVIF/WebP sources without editing Markdown.

Gate: `pnpm check` 0 errors / 0 warnings; `pnpm build` 114 pages; `pnpm verify` `{"routes": 113, "posts": 109, "drafts": 28, "pages": 3, "media": 78, "localLinks": "PASS"}`. `dist/index.html` is 33 KB / 7 KB gzip, contains 20 article rows, and has no `fonts.googleapis.com`. Local mobile Lighthouse: performance 100, FCP 1.4s, LCP 1.4s, TBT 20ms, 94 KiB.

## Verification

- `pnpm check` — 0 errors, 0 warnings, 0 hints
- `pnpm build` — 114 pages
- `pnpm verify` — `{"routes": 113, "posts": 109, "drafts": 28, "pages": 3, "media": 78, "localLinks": "PASS"}`
- Local mobile Lighthouse (`http://127.0.0.1:4321/`): P 100 / A 96 / BP 100 / SEO 100
