# Technical design protocol

## Repository-first facts

Verify and cite exact paths, symbols, versions, commands, schemas, and conventions. Label proposals, observations, assumptions, and unresolved questions distinctly. Never write a speculative path as an observed fact.

Record a clean commit as the repository baseline. Uncommitted feature documents are allowed, but unrelated source-code changes must be committed, excluded with reproducible evidence, or treated as a blocker; a new worktree cannot see uncommitted documents from the prior worktree.

## Minimum complete design

- Trace all in-scope PRD requirements and linked policies.
- Inventory every create/modify/delete surface and important intentionally unchanged integration point.
- Specify contracts with exact validation, errors, authorization, compatibility, timeout, retry, ordering, and idempotency semantics.
- Specify state, time boundaries, concurrency winners, consistency, failure recovery, data retention, migration, and cache/replica behavior where applicable.
- Specify security and privacy enforcement points, sensitive-value handling, audit behavior, and abuse controls.
- Quantify capacity/performance/cost assumptions when material.
- Define deployment order, feature exposure, rollback, forward repair, irreversible points, and approvals.
- Map every acceptance criterion to deterministic verification.

## Delegation decision

Use zero agents for a narrow, well-localized change. Use one for a single uncertain subsystem. Use two or three only for genuinely independent surfaces. Keep delegated work read-only and reconcile all returned facts in the main thread.

## Stop conditions

Stop rather than invent when the design requires an unresolved P0/P1 product choice, public contract, data/security boundary, new dependency, destructive migration, or unverifiable release gate. Record non-blocking defaults explicitly.
