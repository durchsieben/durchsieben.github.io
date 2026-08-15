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

### Phase 3 — PageSpeed follow-ups [done]

Direct operator request: apply remaining recommendations from https://pagespeed.web.dev/analysis/https-durchsieben-de/zig4iileyb where applicable. Production already reports P 100 / A 96 / BP 100 / SEO 100.

1. Raise light-mode accent/muted contrast so brand `sup`, nav, eyebrow, and feed-more pass WCAG AA; make the sticky header opaque so translucent glass no longer undercuts contrast.
2. Inline the global stylesheet (`build.inlineStylesheets: 'always'`) to remove the render-blocking `/_astro/BaseLayout.*.css` request (~110 ms PSI estimate).
3. Drop the Source Serif 4 weight-700 face; map bold chrome (brand, labels) to 600 so first paint pulls two serif files instead of three.
4. Ship `favicon.svg` + `favicon.ico` so browsers stop logging a console 404 on `/favicon.ico` (Best Practices).

Not applicable on this host:

- Long cache lifetimes for hashed `/_astro/*` assets — GitHub Pages fixes `Cache-Control: max-age=600`; no `_headers` or custom asset headers without a CDN in front.
- Extra `preconnect` origins — first-party only; PSI reports no candidates.
- DOM-size reduction — 328 nodes / depth 9 is well under Lighthouse thresholds; feed page size stays at 20.
- Stopping idle `/search-index.json` prefetch — intentional warm cache after first paint; score is already 100 and first interaction must stay snappy.

Gate: `pnpm check` 0 errors / 0 warnings; `pnpm build` 114 pages; `pnpm verify` `{"routes": 113, "posts": 109, "drafts": 28, "pages": 3, "media": 78, "localLinks": "PASS"}`. `dist/index.html` inlines CSS (no BaseLayout stylesheet link), has no `source-serif-4-latin-700` reference, serves `/favicon.ico`, and light `--accent` is `oklch(0.45 0.135 145)`. Local mobile Lighthouse (`http://127.0.0.1:4321/`): P 100 / A 100 / BP 100 / SEO 100; FCP/LCP 1.5s; TBT 0; CLS 0; 75 KiB; 0 contrast failures; 0 render-blocking resources.

### Phase 4 — PageSpeed 8u4nr2vhig [done]

Direct operator request: apply remaining findings from https://pagespeed.web.dev/analysis/https-durchsieben-de/8u4nr2vhig?form_factor=mobile. Production already reports P 100 / A 100 / BP 100; SEO 91 from a robots.txt fetch timeout; Agentic Browsing 2/3 from an llms.txt fetch timeout.

1. Stop idle `/search-index.json` prefetch. Fetch only on first search, topic filter, or `Weitere Beiträge`. Removes the 20 KiB JSON from the first-load critical path.
2. Publish `public/llms.txt` (H1 + summary + key links) so the agentic-browsing audit has a real file instead of a 404/timeout.
3. Keep `public/robots.txt` as the static Allow-all + sitemap file. Verify it in `pnpm verify`. The PSI mobile timeout is a gather-phase fetch flake (desktop pass; live file is 73 bytes / 200 / ~80 ms); no content change.

Not applicable on this host:

- Long cache lifetimes for hashed `/_astro/*.woff2` — GitHub Pages still fixes `Cache-Control: max-age=600`. Clearing that unscored audit needs a CDN in front, not `_headers`.
- Dropping the two first-paint Source Serif files — would clear the cache diagnostic and shorten the font chain, but it changes the editorial face. Out of scope unless requested.

Gate: `pnpm check` 0 errors / 0 warnings; `pnpm build` 114 pages; `pnpm verify` `{"routes": 113, "posts": 109, "drafts": 28, "pages": 3, "media": 78, "localLinks": "PASS", "crawlerFiles": "PASS"}`. Homepage script has no `requestIdleCallback` / idle `loadIndex()`. `dist/llms.txt` has an H1 and `https://durchsieben.de`. `dist/robots.txt` is `User-agent: *` / `Allow: /` / sitemap on the apex.

## Verification

- `pnpm check` — 0 errors, 0 warnings, 0 hints
- `pnpm build` — 114 pages
- `pnpm verify` — `{"routes": 113, "posts": 109, "drafts": 28, "pages": 3, "media": 78, "localLinks": "PASS", "crawlerFiles": "PASS"}`
- Homepage HTML inlines critical CSS; no weight-700 serif asset in `dist/`; `dist/favicon.ico` and `dist/favicon.svg` present
- Homepage script does not idle-prefetch `/search-index.json`; `dist/robots.txt` and `dist/llms.txt` verify
- Local mobile Lighthouse: P 100 / A 100 / BP 100 / SEO 100
