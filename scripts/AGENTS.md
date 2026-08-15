# Import Scripts

## Purpose

Contains reproducible, standard-library migration tooling.

## Local Contracts

- `import_wordpress.py` consumes only the ignored backups recorded in `../backup/wordpress/`.
- It restores released posts/pages and drafts from the WXR export, reconciles released content against the recorded public API JSON, emits routes only for released content, and never publishes drafts.
- `remove_wordpress_articles.py WORDPRESS_ID...` removes retained released or draft articles by WordPress ID. It updates the route manifest for released articles but leaves the ignored WXR backup intact for re-import.
- Curated asset substitutions belong in `CURATED_MEDIA_URLS`; the about-page portrait maps the legacy `2015/10/img_1359.jpg` attachment to `public/images/raphael-bossek-portrait.png` during import.
- HTML entities are decoded once on the way out, in both the body and the frontmatter `title`. Frontmatter is plain text, so a title left as `&amp;` is escaped again at render and displays as a literal `&amp;`.
- `verify_static_site.py` validates the imported counts, all generated legacy routes, local media inventory, local links in `dist/`, and the published `robots.txt` / `llms.txt` crawler files.
- Fail on an incomplete or inconsistent WXR/media pair rather than generating a partial site.

## Verification

- Run the importer from a clean output tree and verify 109 released posts, 28 drafts, 3 pages, 78 media files, and 113 preserved public source paths.
- No generated `title:` line contains an HTML entity: `grep -rIh '^title:' ../src/content/ | grep -c '&[a-zA-Z#0-9]*;'` reports 0.

## Child DOX Index

No child documentation scopes yet.
