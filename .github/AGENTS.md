# GitHub Automation

## Purpose

Owns deployment automation for the static Management÷7 archive.

## Local Contracts

- `workflows/deploy-pages.yml` validates the static site before publishing its `dist/` artifact through GitHub Pages.
- The workflow may deploy only to the GitHub Pages preview URL. Custom-domain and DNS actions remain controlled by `docs/changes/active/CHG-001-wordpress-to-astro.md`.
- Do not add credentials, secrets, or custom-domain values to workflow files.

## Verification

- Run `pnpm check`, `pnpm build`, and `pnpm verify` locally before a deployment workflow change.
- Verify the remote workflow run and Pages URL after pushing.

## Child DOX Index

- `workflows/` — GitHub Actions definitions.
