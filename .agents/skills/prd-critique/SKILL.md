---
name: prd-critique
description: Infer the intended existing Codex feature, then audit and revise its in-review PRD against the current codebase with exactly four parallel read-only critics. Use only when explicitly invoked as $prd-critique with a feature name, description, path, or sufficient conversational context; approve only when evidence, traceability, and product decisions are implementation-ready.
---

# Critique a PRD

Read `references/critique-protocol.md` before selecting critics.

## Establish the baseline

1. Resolve the repository root and enumerate immediate child directories of `.codex/features/` that contain sibling `PRD.md` and `TDD.md` files.
2. Infer the intended feature from, in order of strength, an explicit in-tree artifact path or exact slug, the invocation text, the current conversation, and the PRD titles and summaries. Never select by modification time or directory ordering alone.
3. Proceed only when exactly one feature is a clear semantic match. If none or multiple remain plausible, ask one concise follow-up that lists the candidate slugs; do not read, edit, or combine their artifacts beyond the minimum needed to disambiguate.
4. Bind `feature_dir`, `PRD.md`, and `TDD.md` to that one directory for the entire run. State the selected slug before critique, reject any artifact path outside it, and never use another feature's PRD or TDD as authority or critique evidence.
5. Run `python3 scripts/validate_artifact.py <PRD-path> --phase review`.
6. Read the entire PRD, applicable `AGENTS.md`, repository structure, and current Git status.
7. Assess the PRD's failure surface. Choose exactly four distinct lenses; repository reality and implementation feasibility must be covered by at least one.

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

Report the selected feature slug, four lenses and verdict counts, material revisions, unresolved blockers, final status, and validation result. If approved, instruct the user to start a fresh session in the same worktree before invoking `$tdd <feature name or description>`. Recommend a new worktree only after the approved PRD has been committed or otherwise copied into that worktree.
