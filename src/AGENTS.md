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

## Verification

- Import reconciliation must report 109 posts, 3 pages, 78 media files, and 113 unique source paths.

## Child DOX Index

No child documentation scopes yet.
