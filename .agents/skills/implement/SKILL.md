---
name: implement
description: Infer the intended existing Codex feature, then plan, implement, verify, document, and commit its approved TDD in the current repository. Use only when explicitly invoked as $implement with a feature name, description, path, or sufficient conversational context; may use zero to two bounded read-only subagents, must preserve unrelated work, and never pushes or deploys.
---

# Implement an approved TDD

Read `references/implementation-protocol.md` before editing.

## Gate the work

1. Resolve the repository root and enumerate immediate child directories of `.codex/features/` that contain sibling `PRD.md` and `TDD.md` files.
2. Infer the intended feature from, in order of strength, an explicit in-tree artifact path or exact slug, the invocation text, the current conversation, and the PRD and TDD titles and summaries. Never select by modification time or directory ordering alone.
3. Proceed only when exactly one feature is a clear semantic match. If none or multiple remain plausible, ask one concise follow-up that lists the candidate slugs; do not read, edit, or combine their artifacts beyond the minimum needed to disambiguate.
4. Bind the TDD and PRD paths to that one feature directory for the entire run, state the selected slug before implementation, reject any artifact path outside it, and never use another feature's PRD or TDD as implementation authority or evidence.
5. Validate both approved artifacts and their immutable revisions with `python3 scripts/validate_artifact.py <path> --phase approved`.
6. Confirm the TDD's PRD revision matches the current PRD and its repository baseline is compatible with the current `HEAD`.
7. Read applicable `AGENTS.md`, the full documents, current Git status, and every cited path.
8. Stop for overlapping unrelated changes, missing approval evidence, unresolved blockers, unsafe baseline drift, or an infeasible required verification.

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

Every modified implementation path must trace to an in-scope ID in the bound PRD and TDD. Never edit or stage another directory under `.codex/features/`. Stop for user direction if a required path appears owned exclusively by another feature or lacks traceability to the selected feature.

Do not silently deviate from product behavior, public contracts, data/security boundaries, dependencies, irreversible actions, or required verification. Follow the TDD stop/approval rules.

## Commit

Stage only intended implementation files and the bound feature's `PRD.md` and `TDD.md`. Inspect the staged diff, create one cohesive commit with a descriptive message, and report the commit hash. Do not amend an existing commit, push, deploy, publish, or clean unrelated changes.

If the completion gate does not pass, do not commit or claim completion; report the exact blocker and leave the work recoverable.
