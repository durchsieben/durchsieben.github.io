# Import Scripts

## Purpose

Contains reproducible, standard-library migration tooling.

## Local Contracts

- `import_wordpress.py` consumes only the ignored backups recorded in `../backup/wordpress/`.
- It emits published content, a route manifest, and local media assets; it does not publish drafts.
- `verify_static_site.py` validates the imported counts, all generated legacy routes, local media inventory, and local links in `dist/`.
- Fail on an incomplete or inconsistent WXR/media pair rather than generating a partial site.

## Verification

- Run the importer from a clean output tree and verify 109 posts, 3 pages, 78 media files, and preserved source paths.

## Child DOX Index

No child documentation scopes yet.
