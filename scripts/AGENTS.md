# Import Scripts

## Purpose

Contains reproducible, standard-library migration tooling.

## Local Contracts

- `import_wordpress.py` consumes only the ignored backups recorded in `../backup/wordpress/`.
- It emits published content, a route manifest, and local media assets; it does not publish drafts.
- Curated asset substitutions belong in `CURATED_MEDIA_URLS`; the about-page portrait maps the legacy `2015/10/img_1359.jpg` attachment to `public/images/raphael-bossek-portrait.png` during import.
- HTML entities are decoded once on the way out, in both the body and the frontmatter `title`. Frontmatter is plain text, so a title left as `&amp;` is escaped again at render and displays as a literal `&amp;`.
- `verify_static_site.py` validates the imported counts, all generated legacy routes, local media inventory, and local links in `dist/`.
- Fail on an incomplete or inconsistent WXR/media pair rather than generating a partial site.

## Verification

- Run the importer from a clean output tree and verify 109 posts, 3 pages, 78 media files, and preserved source paths.
- No generated `title:` line contains an HTML entity: `grep -rIh '^title:' ../src/content/ | grep -c '&[a-zA-Z#0-9]*;'` reports 0.

## Child DOX Index

No child documentation scopes yet.
