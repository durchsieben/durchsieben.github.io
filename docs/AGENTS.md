# Documentation

## Purpose

Owns durable migration records and user-facing operating contracts for Management÷7.

## Local Contracts

- `product/capabilities/` states verified, current site behaviour.
- `changes/active/` contains exactly the active implementation record; `changes/archive/` contains completed receipts.
- Never put credentials, WordPress exports, downloaded media, or personally identifying comment data in `docs/`.
- Keep records concise and link to executable checks instead of duplicating implementation detail.

## Child DOX Index

- `product/AGENTS.md` — capability contracts.
- `changes/AGENTS.md` — implementation-progress records.
