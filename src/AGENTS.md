# Imported Site Content

## Purpose

Owns deterministic WordPress-derived content and the legacy-route manifest used by the Astro site.

## Local Contracts

- `content/posts/` contains the 109 published WordPress posts only.
- `content/pages/` contains the 3 published WordPress pages only.
- `data/legacy-routes.json` is the importer's generated mapping for all 113 legacy sitemap paths, including `/`.
- `content.config.ts`, `layouts/`, `pages/`, and `styles/` implement the static Astro archive; preserve every `sourcePath` during route generation.
- The catch-all route renders each imported post and page body; presentation must not replace or omit source content.
- Explicit route aliases may retain stale WordPress-internal paths without changing imported content or the 113-path manifest.
- Rewrite only the imported content and route data through `../scripts/import_wordpress.py`; do not hand-edit imported source URLs or route paths.
- `lib/posts.ts` is the single helper for post summaries, sort order (newest first), plain-text extraction, reading time, and topic generation. Pages and components use it instead of re-implementing sort or text extraction.
- `components/` holds Astro UI components (`SearchAndFeed.astro`). Pages compose them; do not duplicate feed/search markup in individual pages.
- The homepage hero pairs the archive introduction with the transparent Raphael Bossek portrait at `public/images/raphael-bossek-portrait.png` before rendering the entire archive (newest first) with its client-side search and topic filter; a separate `/artikeluebersicht/` archive page is no longer maintained and the old inline article list in the catch-all route is removed.
- The `/about/` page uses the same portrait, supplied by the importer, in a two-column author introduction that preserves a broad reading column on desktop and stacks on mobile.

## Verification

- Import reconciliation must report 109 posts, 3 pages, 78 media files, and 113 unique source paths.
- `pnpm check` reports 0 errors and 0 warnings; `pnpm build` emits 114 pages; `pnpm verify` reports 113 routes and no broken local links.
