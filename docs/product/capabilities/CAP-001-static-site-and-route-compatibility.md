# CAP-001 — Static site and legacy-route compatibility

## Outcome

Management÷7 is a static Astro site published at `https://durchsieben.de` through GitHub Pages.

## Current target behaviour

- Released and draft WordPress articles are represented as repository-owned Markdown plus locally stored media assets. The WXR export is the full-content source; recorded public API JSON snapshots reconcile released post/page IDs before import.
- The 109 released WordPress posts and 3 published pages are rendered by the static site. The 28 restored draft posts remain source content only: they have no generated route, archive entry, or RSS item.
- The homepage lists the newest 20 posts in the initial HTML. Remaining archive rows and title/excerpt search load from `/search-index.json` on demand. Without JavaScript the listing stops at those 20 posts; every released article still has its own preserved route.
- `scripts/remove_wordpress_articles.py` removes a retained released or draft article by WordPress ID. Released removals also remove its route-manifest entry; the ignored WXR backup remains available for a clean re-import.
- Every legacy public pathname from the WordPress export resolves to its corresponding Astro page at the same pathname. This includes dated article paths and the three published pages.
- A generated route manifest is the authority for preserved paths; build verification fails when a published source path has no generated destination.
- `durchsieben.de` and `www.durchsieben.de` use HTTPS after the approved DNS cutover.

## Boundaries

- GitHub Pages is static hosting. It cannot return server-side HTTP redirects for arbitrary old paths; Astro static redirects are HTML/meta-refresh redirects. Exact-path rendering is therefore required for all exported legacy paths.
- WordPress comments, subscribers, dashboard settings, and plugin configuration are backup data, not part of the static-site runtime. Draft content is retained project source but is not public runtime content.

## Evidence required before this record becomes current

- WordPress WXR export and media export have recorded checksums.
- A fresh import reports 109 released posts, 28 drafts, 3 published pages, and no unmapped released path.
- `pnpm build` succeeds and the route-manifest verification passes.
- GitHub Pages deploy is reachable on its GitHub URL before DNS is changed; sampled legacy URLs resolve successfully after cutover.
