---
name: implement
description: Plan privately, implement, verify, document, and commit an approved TDD in the current repository. Use when the user invokes /implement with a feature name or a path to TDD.md; may use zero to two bounded read-only subagents, must preserve unrelated work, and never pushes or deploys.
argument-hint: <feature> (name or path to TDD.md)
disable-model-invocation: true
user-invocable: true
---

# Implement an approved TDD

Read `references/implementation-protocol.md` before editing.

## Gate the work

1. Identify the target feature from the user's description: accept a path to `TDD.md`, a feature slug, or a natural-language feature name (slugify it and match against the directories under `.claude/features/`). Resolve to exactly one `.claude/features/<slug>/` workspace, then use its `TDD.md` and sibling `PRD.md`. If the description names no feature, matches none, or matches more than one, list the available features under `.claude/features/` and ask which one before proceeding. Work only within the resolved feature folder; never read or modify another feature's documents.
2. Validate both approved artifacts and their immutable revisions with `python3 scripts/validate_artifact.py <path> --phase approved`.
3. Confirm the TDD's PRD revision matches the current PRD and its repository baseline is compatible with the current `HEAD`.
4. Read applicable `CLAUDE.md`, the full documents, current Git status, and every cited path.
5. Stop for overlapping unrelated changes, missing approval evidence, unresolved blockers, unsafe baseline drift, or an infeasible required verification.

## Plan and investigate

Build a dependency-ordered implementation plan in working context; do not create another plan artifact. Map every step to TDD STEP/TEST/CMD IDs.

Use zero to two `implementation-reviewer` subagents only when bounded read-only exploration, test analysis, or an independent final review adds value. The main agent owns all edits. Never delegate overlapping writes.

## Implement and verify

1. Implement the smallest coherent change that satisfies the TDD.
2. Follow the plan and verify after each meaningful increment.
3. Add tests, migrations, generated artifacts, telemetry, and documentation explicitly required by the TDD.
4. Run every applicable focused and full command. Distinguish regressions from reproducible pre-existing failures.
5. Review the final diff against the PRD, TDD, repository rules, and unrelated user changes.
6. Complete the TDD implementation record and completion gate, set `status: implemented`, then re-stamp and validate it with `--phase implemented`.

Do not silently deviate from product behavior, public contracts, data/security boundaries, dependencies, irreversible actions, or required verification. Follow the TDD stop/approval rules.

## Commit

Stage only intended implementation files and the feature documents. Inspect the staged diff, create one cohesive commit with a descriptive message, and report the commit hash. Do not amend an existing commit, push, deploy, publish, or clean unrelated changes.

If the completion gate does not pass, do not commit or claim completion; report the exact blocker and leave the work recoverable.
