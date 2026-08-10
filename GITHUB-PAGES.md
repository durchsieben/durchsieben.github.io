# GitHub Pages Operations

This repository-only runbook owns GitHub Pages setup, custom-domain cutover, verification, maintenance, and rollback for Management÷7. It is operational documentation, not public site content: do not place it under `src/content/`, copy it to `public/`, add it to Astro collections, or link it from site navigation, the sitemap, or `robots.txt`.

## Current State

Recheck every value before making a provider change.

| Surface | Observed 2026-08-10 | Required state |
| --- | --- | --- |
| Repository | Public `durchsieben/durchsieben.github.io`; local `origin` is `git@github.com:durchsieben/durchsieben.github.io.git`. | Retain the organization repository and SSH remote. |
| Pages publishing | GitHub Actions, `build_type: workflow`; preview at `https://durchsieben.github.io/`; HTTPS enforcement enabled. | Retain workflow publishing. |
| Preview evidence | Run `31379076437` built and deployed successfully. Homepage, a dated article, and the three published pages returned HTTP 200. | Re-run the full workflow after deployment changes. |
| Apex DNS | `durchsieben.de` resolves to WordPress A records `192.0.78.24` and `192.0.78.25`; authoritative nameservers are WordPress.com. | Replace only at the approved cutover with all four GitHub Pages A records. |
| `www` DNS | `www.durchsieben.de` CNAME points to the apex. | Point directly to `durchsieben.github.io`. |
| Custom domain | Not configured in repository Pages settings. | Verify the domain for the `durchsieben` organization, then configure `durchsieben.de`. |
| WordPress | Still live. | Keep it live until custom-domain verification passes. |

## Control Surfaces

- `.github/workflows/deploy-pages.yml` installs pinned pnpm through Corepack, runs `pnpm check`, `pnpm build`, and `pnpm verify`, then uploads `dist/` and deploys it through GitHub Pages OIDC.
- `astro.config.mjs` declares static output and canonical site URL `https://durchsieben.de`. Do not add a repository `base` path.
- `package.json` pins pnpm to an exact version because Corepack rejects version ranges in `devEngines.packageManager`.
- `scripts/verify_static_site.py` checks imported counts, every legacy route, and local links in the generated site.
- `public/CNAME` contains exactly `durchsieben.de` followed by one newline. With Actions publishing GitHub Pages settings remain authoritative; the file records repository intent only.
- `docs/changes/active/CHG-001-wordpress-to-astro.md` is the gated migration record. It controls whether DNS or WordPress changes are permitted.
- GitHub repository **Settings → Pages** controls the custom domain and HTTPS enforcement.

No deployment secret is required. The workflow uses GitHub-provided `pages: write` and `id-token: write` permissions. Do not commit DNS credentials, tokens, or copied settings exports.

## Prerequisites

- Organization-owner access to `durchsieben`.
- Admin access to `durchsieben/durchsieben.github.io`.
- Access to the DNS zone served by the WordPress.com nameservers.
- Node 24, Corepack, pnpm, Git, and `gh` for local validation and deployment review.
- A clean working tree and a successful `pnpm check && pnpm build && pnpm verify` result.
- Explicit authorization in `CHG-001` before custom-domain or DNS changes.

## First-Time Pages Setup

This is completed for the preview deployment and is retained here for recovery or audit.

1. Keep the repository public and named `durchsieben.github.io` under the `durchsieben` organization.
2. In repository **Settings → Pages**, set the source to **GitHub Actions**.
3. Push `.github/workflows/deploy-pages.yml` to `main`.
4. Confirm a real workflow run completes both `build` and `deploy`; inspect individual step conclusions, not only the overall green status.
5. Confirm the Pages API reports `build_type: workflow` and HTTPS enforcement:

   ```bash
   gh api repos/durchsieben/durchsieben.github.io/pages \
     --jq '{build_type,https_enforced,status,html_url,cname}'
   ```

6. Verify the preview before custom-domain work:

   ```bash
   curl -fsSI https://durchsieben.github.io/
   curl -fsSI https://durchsieben.github.io/2020/08/03/d-h-fuehrung/
   curl -fsSI https://durchsieben.github.io/artikeluebersicht/
   curl -fsSI https://durchsieben.github.io/about/
   curl -fsSI https://durchsieben.github.io/impressum/
   ```

## Organization Domain Verification

Verify `durchsieben.de` for the `durchsieben` organization before associating it with the repository. This prevents another GitHub account from claiming the domain or its immediate subdomains.

1. Open GitHub: **Organizations → durchsieben → Settings → Pages → Add a domain**.
2. Enter `durchsieben.de`.
3. Copy the exact TXT record name and value GitHub presents. Do not guess or reuse a value from another organization.
4. Create that TXT record in the WordPress.com-managed DNS zone without changing the existing website records.
5. Wait for the record to resolve, then verify it:

   ```bash
   dig _github-pages-challenge-durchsieben.durchsieben.de \
     +nostats +nocomments +nocmd TXT
   ```

6. Return to the organization Pages settings and select **Verify**.
7. Keep the TXT record permanently unless the organization deliberately relinquishes the domain.

## Custom-Domain Cutover

Configure GitHub before DNS. Reversing that order permits a domain-takeover window.

1. Confirm the organization domain is verified and the preview is healthy.
2. In `durchsieben/durchsieben.github.io`: **Settings → Pages → Custom domain**, enter `durchsieben.de`, then save.
3. Confirm GitHub Pages reports the configured domain:

   ```bash
   gh api repos/durchsieben/durchsieben.github.io/pages \
     --jq '{cname,https_enforced,status,html_url}'
   ```

4. Preserve `public/CNAME` in the repository and confirm the published artifact includes it:

   ```bash
   pnpm build
   test "$(tr -d '\r\n' < dist/CNAME)" = 'durchsieben.de'
   ```

5. Only after steps 1–4 pass, edit DNS. Preserve mail and verification records; replace only the apex and `www` website records described below.
6. Leave WordPress hosting running until HTTP and route checks at the custom domain pass.

## DNS Setup

GitHub documents the authoritative target values. Recheck its documentation immediately before changing the zone:

- [Managing a custom domain for GitHub Pages](https://docs.github.com/en/pages/configuring-a-custom-domain-for-your-github-pages-site/managing-a-custom-domain-for-your-github-pages-site)
- [Verifying a custom domain for GitHub Pages](https://docs.github.com/en/pages/configuring-a-custom-domain-for-your-github-pages-site/verifying-your-custom-domain-for-github-pages)
- [Securing a GitHub Pages site with HTTPS](https://docs.github.com/en/pages/getting-started-with-github-pages/securing-your-github-pages-site-with-https)

At the WordPress.com DNS provider, replace the existing website records with these values:

| Name | Type | Value | Notes |
| --- | --- | --- | --- |
| `@` / `durchsieben.de` | A | `185.199.108.153` | GitHub Pages IPv4 record 1. |
| `@` / `durchsieben.de` | A | `185.199.109.153` | GitHub Pages IPv4 record 2. |
| `@` / `durchsieben.de` | A | `185.199.110.153` | GitHub Pages IPv4 record 3. |
| `@` / `durchsieben.de` | A | `185.199.111.153` | GitHub Pages IPv4 record 4. |
| `www` | CNAME | `durchsieben.github.io` | Point directly to the organization Pages hostname, not to the apex and not to a repository path. |

Optional IPv6 requires all four records alongside the A records: `2606:50c0:8000::153`, `2606:50c0:8001::153`, `2606:50c0:8002::153`, and `2606:50c0:8003::153`. Do not add partial IPv6 coverage.

Do not create wildcard DNS records. Do not remove MX, TXT, mail, domain-verification, or unrelated subdomain records. DNS propagation can take up to 24 hours.

## Local Validation And Deployment

```bash
corepack enable
pnpm install --frozen-lockfile
pnpm check
pnpm build
pnpm verify
```

Push only after the checks pass. The workflow file must already exist on the pushed branch before manual dispatch is available.

```bash
gh workflow run "Deploy GitHub Pages" --repo durchsieben/durchsieben.github.io
sleep 5
gh run list --workflow "Deploy GitHub Pages" \
  --repo durchsieben/durchsieben.github.io --limit 3
gh run view RUN_ID --repo durchsieben/durchsieben.github.io \
  --json status,conclusion,jobs
```

A manual dispatch must execute both jobs. A `skipped` build or deploy job is a failure of this runbook, even if the workflow headline is green.

## Post-Cutover Verification

Wait for DNS propagation, then run:

```bash
dig durchsieben.de +noall +answer -t A
dig durchsieben.de +noall +answer -t AAAA
dig www.durchsieben.de +noall +answer -t CNAME
curl -fsSI http://durchsieben.de/
curl -fsSI https://durchsieben.de/
curl -fsSI https://www.durchsieben.de/
```

Confirm all of the following:

- Apex A records are all four GitHub Pages IPv4 addresses.
- `www` is a direct CNAME to `durchsieben.github.io` and redirects to the configured apex.
- HTTP redirects to HTTPS once GitHub makes HTTPS enforcement available.
- `https://durchsieben.de/` returns 200 with the Management÷7 title.
- The dated article, `/artikeluebersicht/`, `/about/`, and `/impressum/` all return rendered content.
- `https://durchsieben.de/robots.txt`, `/sitemap-index.xml`, and `/rss.xml` resolve.
- GitHub repository Pages settings report `cname: durchsieben.de` and `https_enforced: true`.
- Canonical URLs, sitemap entries, and `robots.txt` use `https://durchsieben.de`.
- The WordPress site remains available until every check passes.

## Routine Maintenance

- Before changing Astro, pnpm, Node, GitHub Actions, GitHub Pages, or DNS, recheck the linked official GitHub documentation.
- Dependency changes update `package.json` and `pnpm-lock.yaml` together and run the full local verification sequence.
- Content and presentation changes run the same verification sequence and a real deployment review.
- Do not add deployment secrets: this is a static GitHub Pages workflow.
- Keep `public/CNAME` synchronized with the intended custom domain, but treat Pages settings and DNS as authoritative for Actions publishing.

## Troubleshooting And Rollback

- **Build fails:** reproduce with the local validation commands, fix the source or lockfile, push, and inspect failed workflow logs with `gh run view RUN_ID --log-failed`.
- **Deploy job skipped or failed:** inspect the event trigger, `needs: build`, Pages source, and each job step conclusion. Re-run only after resolving the cause.
- **Domain cannot be added:** verify it at organization scope first; it may still be attached to another GitHub Pages site.
- **Certificate pending:** verify all DNS values, remove conflicting apex or `www` website records, wait for propagation, and keep HTTPS enforcement disabled until GitHub offers it.
- **Wrong site after DNS change:** use `dig` before relying on a browser; browser caches are not DNS evidence.
- **Rollback content:** revert to the last good `main` commit, push, and verify a fresh Pages deployment. DNS remains unchanged.
- **Rollback provider:** remove the custom domain from GitHub Pages settings before repointing DNS away from GitHub. Restore the previous WordPress A records only when deliberately returning traffic to WordPress. Never leave GitHub Pages disabled while DNS still points at it.

## Sources

- [GitHub: custom-domain management](https://docs.github.com/en/pages/configuring-a-custom-domain-for-your-github-pages-site/managing-a-custom-domain-for-your-github-pages-site)
- [GitHub: domain verification](https://docs.github.com/en/pages/configuring-a-custom-domain-for-your-github-pages-site/verifying-your-custom-domain-for-github-pages)
