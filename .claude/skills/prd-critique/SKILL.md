---
name: prd-critique
description: Audit and revise an in-review PRD against the current codebase with exactly four parallel read-only critics chosen from the PRD's likely failure surfaces. Use when the user invokes /prd-critique with a feature name or a path to PRD.md; approve only when evidence, traceability, and product decisions are implementation-ready.
argument-hint: <feature> (name or path to PRD.md)
disable-model-invocation: true
user-invocable: true
---

# Critique a PRD

Read `references/critique-protocol.md` before selecting critics.

## Establish the baseline

1. Resolve the repository root, then identify the target feature from the user's description: accept a path to `PRD.md`, a feature slug, or a natural-language feature name (slugify it and match against the directories under `.claude/features/`). Resolve to exactly one `.claude/features/<slug>/` workspace and use its `PRD.md`. If the description names no feature, matches none, or matches more than one, list the available features under `.claude/features/` and ask which one before proceeding. Require the sibling `TDD.md` to exist. Work only within the resolved feature folder; never read or modify another feature's documents.
2. Run `python3 scripts/validate_artifact.py <PRD-path> --phase review`.
3. Read the entire PRD, applicable `CLAUDE.md`, repository structure, and current Git status.
4. Assess the PRD's failure surface. Choose exactly four distinct lenses; repository reality and implementation feasibility must be covered by at least one.

## Delegate exactly four critiques

Spawn exactly four `prd-critic` subagents in parallel. Give each the repository root, PRD path, one bounded lens, relevant PRD IDs, and the response schema from the protocol. Keep every critic read-only. Wait for all four; a failed or incomplete critic must be retried or replaced before synthesis.

Do not tell critics the desired conclusion. Require repository evidence and explicit SIGN_OFF, REJECT, or NOT_APPLICABLE verdicts.

## Adjudicate and revise

1. Re-check cited evidence in the main thread.
2. Deduplicate findings and resolve cross-lens conflicts.
3. Ask the user only for product decisions that cannot be established from the PRD or codebase.
4. Revise `PRD.md` directly. Do not create a separate critique artifact.
5. Record material changes and decisions in the PRD decision log.
6. Set `status: approved` only if all applicable P0/P1 content is signed off, the handoff gate passes, and no `BLOCKER` remains; otherwise use `in_review`.
7. Re-stamp and validate with `python3 scripts/stamp_revision.py <PRD-path>` and `python3 scripts/validate_artifact.py <PRD-path> --phase approved` when approved, otherwise `--phase review`.

Do not edit `TDD.md`, source code, Git history, or external systems.

## Return

Summarize the four lenses and verdict counts, material revisions, unresolved blockers, final status, and validation result. If approved, instruct the user to run `/clear` before invoking `/tdd <feature>` (the feature name or the path to its `PRD.md`). Recommend a new worktree only after the approved PRD has been committed or otherwise copied into that worktree.
