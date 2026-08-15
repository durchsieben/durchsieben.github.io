# Imported Site Content

## Purpose

Owns deterministic WordPress-derived content and the legacy-route manifest used by the Astro site.

## Local Contracts

- `content/posts/` contains released WordPress posts; `content/drafts/` contains restored WordPress draft posts keyed by WordPress ID.
- `content/pages/` contains the 3 published WordPress pages only.
- `data/legacy-routes.json` is the importer's generated mapping for retained released content, including `/`; drafts deliberately have no route.
- `content.config.ts`, `layouts/`, `pages/`, and `styles/` implement the static Astro archive; preserve every `sourcePath` during route generation.
- The catch-all route renders each imported post and page body; presentation must not replace or omit source content.
- Explicit route aliases may retain stale WordPress-internal paths without changing imported content or the 113-path manifest.
- Rewrite only the imported content and route data through `../scripts/import_wordpress.py`; remove retained articles through `../scripts/remove_wordpress_articles.py`; do not hand-edit imported source URLs or route paths.
- `lib/posts.ts` is the single helper for post summaries, sort order (newest first), plain-text extraction, reading time, and topic generation. Pages and components use it instead of re-implementing sort or text extraction.
- `components/` holds Astro UI components (`SearchAndFeed.astro`). Pages compose them; do not duplicate feed/search markup in individual pages.
- The homepage hero pairs the archive introduction with the transparent Raphael Bossek portrait on desktop (`public/images/portrait/` AVIF/WebP derivatives; original PNG stays at `public/images/raphael-bossek-portrait.png` for the importer). The portrait is omitted on viewports ≤760px and must not be downloaded there. The homepage HTML renders the newest 20 posts; remaining rows and title/excerpt search load from `/search-index.json`. A separate `/artikeluebersicht/` archive page is no longer maintained and the old inline article list in the catch-all route is removed.
- The `/about/` page uses the same portrait, rewritten at render time to the AVIF/WebP derivatives, in a two-column author introduction that preserves a broad reading column on desktop and stacks on mobile.
- Typography self-hosts a Latin Source Serif 4 subset at weights 400/600 only (`font-display: optional`). Bold chrome maps to 600. UI chrome uses the system sans stack. Do not add Google Fonts.
- Global CSS is always inlined at build time (`build.inlineStylesheets: 'always'`) so first paint does not wait on a separate stylesheet request. GitHub Pages cache lifetimes stay at the platform default (`max-age=600`); do not invent `_headers` for Pages.

## Verification

- A fresh import reconciles 109 released posts, 28 drafts, 3 pages, 78 media files, and 113 unique public source paths.
- `pnpm check` reports 0 errors and 0 warnings; `pnpm build` emits 114 public pages; `pnpm verify` validates retained-content counts, generated released routes, and local links.
