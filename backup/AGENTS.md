# Backup Artifacts

## Purpose

Owns non-versioned source exports required to reproduce the Management÷7 migration.

## Local Contracts

- `wordpress/` contains original WordPress downloads, public API snapshots, checksum manifests, and inventories.
- Files here are intentionally excluded from Git history; record their presence and reconciliation outcome in the active CHG instead.
- Never store browser cookies, passwords, access tokens, or copied credentials here.

## Verification

- Each original download has a SHA-256 entry.
- The public snapshot reconciles post/page totals against WordPress dashboard counts.

## Child DOX Index

No child documentation scopes yet.
