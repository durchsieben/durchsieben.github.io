# CAP-001 — Static site and legacy-route compatibility

## Outcome

Management÷7 is a static Astro site published at `https://durchsieben.de` through GitHub Pages.

## Current target behaviour

- The published WordPress content is represented as repository-owned Markdown/MDX plus locally stored media assets.
- The 109 WordPress posts and 3 published pages observed during migration planning are rendered by the static site. The 28 WordPress drafts are retained in the source backup but are not published unless explicitly selected later.
- Every legacy public pathname from the WordPress export resolves to its corresponding Astro page at the same pathname. This includes dated article paths and the three published pages.
- A generated route manifest is the authority for preserved paths; build verification fails when a published source path has no generated destination.
- `durchsieben.de` and `www.durchsieben.de` use HTTPS after the approved DNS cutover.

## Boundaries

- GitHub Pages is static hosting. It cannot return server-side HTTP redirects for arbitrary old paths; Astro static redirects are HTML/meta-refresh redirects. Exact-path rendering is therefore required for all exported legacy paths.
- WordPress comments, subscribers, dashboard settings, plugin configuration, and drafts are backup data, not part of the initial static-site runtime.

## Evidence required before this record becomes current

- WordPress WXR export and media export have recorded checksums.
- Import verification reports 109 published posts, 3 published pages, and no unmapped published path.
- `pnpm build` succeeds and the route-manifest verification passes.
- GitHub Pages deploy is reachable on its GitHub URL before DNS is changed; sampled legacy URLs resolve successfully after cutover.
