---
name: tdd
description: Generate an implementation-ready technical design and complete test design from an approved PRD after inspecting the current repository. Use when the user invokes /tdd with a path to PRD.md; may delegate zero to three bounded read-only investigations and edits only the sibling TDD.md.
argument-hint: <path-to-PRD.md>
disable-model-invocation: true
user-invocable: true
---

# Generate a TDD

Read `references/design-protocol.md` and `assets/TDD_template.md` before writing.

## Validate inputs

1. Resolve the PRD and sibling TDD paths under `.claude/features/`.
2. Require `status: approved`, a valid immutable `content_revision`, and no open `BLOCKER` in the PRD.
3. Run `python3 scripts/validate_artifact.py <PRD-path> --phase approved`.
4. Read applicable `CLAUDE.md`, the full PRD, repository status, manifests, architecture, relevant code, tests, schemas, migrations, CI, and operational configuration.
5. Capture the exact repository revision. Treat meaningful drift during design as a reason to re-check affected sections.

## Investigate

Choose zero to three independent questions whose parallel investigation materially improves correctness or speed. Typical questions cover current architecture/contracts, data/concurrency/security, and test/rollout/operations. Spawn no more than three `design-researcher` subagents, keep them read-only, give each a bounded question, and wait for all results. Investigate directly when delegation would duplicate context or add latency.

## Design

1. Map every in-scope PRD obligation to a technical response and verification.
2. Resolve exact change surfaces, contracts, invariants, data/time/concurrency semantics, failure behavior, security, compatibility, observability, rollout, and rollback.
3. Write a dependency-ordered, file-aware implementation sequence.
4. Design the full test strategy, including exact locations, fixtures, commands, edge cases, migration/rollback checks, and pass evidence.
5. Ask the user only when a missing decision changes product behavior, architecture, a public contract, security/data boundaries, irreversible work, or required verification.

Replace the sibling `TDD.md` with a completed template. Delete authoring prompts and inapplicable optional sections. Do not edit application code.

Set `status: approved` only when the readiness gate passes and the user has resolved consequential choices; otherwise set `in_review`. Set `related_prd_revision` to the PRD's immutable revision and `repository_revision` to the inspected baseline. Run `python3 scripts/stamp_revision.py <TDD-path>` and validate with `python3 scripts/validate_artifact.py <TDD-path> --phase approved` when approved, otherwise `--phase review`.

## Return

Report the TDD path, selected design, delegated investigations, blockers, validation status, and exact next invocation: `/implement <path-to-TDD.md>`. Recommend `/clear` in the same worktree; recommend a new worktree only after both approved documents are committed or copied there.
