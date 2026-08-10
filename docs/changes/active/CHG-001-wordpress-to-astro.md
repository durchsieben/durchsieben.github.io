# CHG-001 — WordPress archive to Astro/GitHub Pages

## Request

Direct operator request: "I wan to backup my wordpress page at https://durchsieben.de I've logedin at https://raphaelbossek.wordpress.com/wp-admin/ and recreate afterward in https://astro.build for GitHub Pages. The links for the articles should be preserved, redirected is ok. For frontend I prefer Shadcn with Shadcnblocks including the Pro blocks like described at https://www.shadcnblocks.com/dashboard/api using SHADCNBLOCKS_API_KEY as api key. Use the application-records skill for planning before execution"

## Affected capability

- [CAP-001 — Static site and legacy-route compatibility](../../product/capabilities/CAP-001-static-site-and-route-compatibility.md)

## Follow-up request

Direct operator request: "create wireframes for the homepage, one exemplary blog post, and the 3 published pages using the https://www.shadcnblocks.com/template/apex for Astro"

## Discovery evidence

- The WordPress dashboard shows 109 published posts, 28 drafts, and 3 published pages.
- `https://durchsieben.de/sitemap.xml` exposes dated article paths plus `/artikeluebersicht/`, `/about/`, and `/impressum/`.
- The public WordPress.com API reports 109 published posts. It is useful for reconciliation but is not the primary backup.
- The working directory has only `AGENTS.md`; it is not a Git repository and does not yet contain an Astro project.
- A public API/sitemap snapshot was saved under ignored `backup/wordpress/`; its recorded reconciliation is 109 published posts and 3 published pages.
- The original WXR export and media archive are stored under ignored `backup/wordpress/`. The WXR independently parses to 109 published posts, 28 drafts, 3 published pages, and 78 attachments; the media archive contains 78 files. Checksums, inventories, and a 113-path sitemap route seed are recorded beside the archives.
- `node` v25.6.1, `pnpm` v11.17.0, and authenticated `gh` are available. Presence of `SHADCNBLOCKS_API_KEY` has not yet been verified and its value must never be read or committed.

## Approved execution sequence

### Phase 1 — Source discovery, IA wireframes, and backup [done]

1. Create a canonical wireframe source for the homepage, one representative article, `/artikeluebersicht/`, `/about/`, and `/impressum/`. Use Apex for its Astro-compatible editorial layout cues, not as a verbatim page/template copy.
2. Download a WordPress WXR export for all content through **Tools → Export content**.
3. Download the media export through **Tools → Export media files**.
4. Store original download files outside Git history under `backup/wordpress/`, checksum them, and record counts and source paths in an inventory manifest.
5. Fetch a read-only public API/sitemap snapshot and compare published post/page counts and paths against the WXR inventory.

Gate: the wireframe `.pen` source and review exports show all five requested screens; WXR and media archives exist with checksums; inventory shows 109 published posts and 3 published pages; every sitemap URL is either a generated legacy route or a documented deliberate exclusion.

### Phase 2 — Create the repository and import pipeline [done]

1. Initialize this directory as the GitHub Pages repository; use the explicit Raphael Bossek identity only for project commits so the surrounding agent environment is not mutated.
2. Add a reproducible importer that converts the WXR archive to content entries and builds a source-to-destination route manifest.
3. Download and rewrite WordPress-hosted media references to local `public/` assets; retain source URLs and checksums in the manifest.
4. Preserve original dated article pathnames exactly. Do not substitute client-side redirects where a static page can be emitted.

Gate: importer runs from a clean checkout using only the recorded backup; content count and route manifest reconciliation pass.

### Phase 3 — Build the Astro frontend [done]

1. Create an Astro static site with content collections, an article index, article pages, the existing legal/about pages, RSS, sitemap, and accessible typography.
2. Use native Astro, semantic HTML, and custom CSS primitives; do not introduce React, Tailwind, shadcn, or Shadcnblocks solely for component styling.
3. Implement the approved wireframe structure while preserving the editorial information architecture rather than copying a generic landing page.
4. Canonicalize imported links to the former site host when their target has a preserved route; record and resolve stale internal aliases discovered by the link check.
5. Add route-manifest, content-count, link, and production-build checks.

Gate: `pnpm build` plus focused route/content/link checks pass locally; no secret is tracked or emitted.

### Phase 4 — Deploy and controlled cutover [in-progress]

1. Add the official Astro GitHub Pages workflow and deploy to the GitHub Pages URL first.
2. Configure `public/CNAME` for `durchsieben.de`, set the GitHub Pages custom domain, and change DNS only after the preview verification gate passes.
3. Enable HTTPS, verify the apex and `www` domains, and sample legacy article links plus the three pages after propagation.
4. Keep the WordPress site online until the custom-domain and legacy-route verification succeeds; only then decide whether to retire its paid hosting.

Gate: GitHub Pages deployment succeeds; HTTPS is active; sampled old paths return rendered content at the custom domain; no DNS or WordPress destructive action occurred before that proof.

## Decisions and constraints

- Publish the existing public surface (109 posts, 3 pages); retain drafts in the backup but do not publish them initially.
- GitHub Pages requires static output. Exact generated legacy paths are the compatibility mechanism; Astro's static redirect output is not an HTTP 301/308 service.
- `durchsieben.de` is an apex domain. Cutover requires GitHub Pages custom-domain configuration plus appropriate DNS records, which is a user-visible external change and is deferred to Phase 4.
- The public deployment target is `durchsieben/durchsieben.github.io` over SSH. The initial `forgegod/durchsieben.de` repository remains an historical migration checkpoint; GitHub Pages and DNS remain deferred to Phase 4.
- The operator removed the shadcn and Shadcnblocks requirement during Phase 3. The site remains dependency-light and static; interactive UI work requires a separate explicit request.

## Verification ledger

| Phase | Status | Evidence |
| --- | --- | --- |
| 1 | done | Five-screen canonical wireframe source/export set passed fresh layout and visual checks. Public API, WXR, and media archive inventories reconcile to 109 published posts, 3 published pages, and 78 attachments; source checksums and the 113-path sitemap route seed passed verification. |
| 2 | done | Initial public `forgegod/durchsieben.de` migration checkpoint initialized on `main`; the importer generated 109 posts, 3 pages, 78 local media files, and 113 unique legacy paths. A literal fresh Git clone re-imported from the recorded backup and produced no tracked differences. |
| 3 | done | Native Astro frontend implements the five approved page structures without React, Tailwind, shadcn, or Shadcnblocks. `pnpm check`, `pnpm build`, and `pnpm verify` passed: 113 generated routes, 109 posts, 3 pages, 78 media assets, and no broken local links. The importer canonicalizes stale former-host links to preserved paths before output. |
| 4 | in-progress | Deployment target moved to `durchsieben/durchsieben.github.io` over SSH. GitHub Pages is enabled, but the initial workflow run failed before install because `setup-node` attempted pnpm cache discovery before Corepack enabled pnpm; the workflow now uses the dependency-free setup order and awaits a rerun. No custom domain or DNS change has occurred. |
