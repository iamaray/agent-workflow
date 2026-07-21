---
name: tdd
description: Infer the intended existing Codex feature and generate an implementation-ready technical design and complete test design from its approved PRD after inspecting the repository. Use only when explicitly invoked as $tdd with a feature name, description, path, or sufficient conversational context; may delegate zero to three bounded read-only investigations and edits only that feature's TDD.md.
---

# Generate a TDD

Read `references/design-protocol.md` and `assets/TDD_template.md` before writing.

## Validate inputs

1. Resolve the repository root and enumerate immediate child directories of `.codex/features/` that contain sibling `PRD.md` and `TDD.md` files.
2. Infer the intended feature from, in order of strength, an explicit in-tree artifact path or exact slug, the invocation text, the current conversation, and the PRD titles and summaries. Never select by modification time or directory ordering alone.
3. Proceed only when exactly one feature is a clear semantic match. If none or multiple remain plausible, ask one concise follow-up that lists the candidate slugs; do not read, edit, or combine their artifacts beyond the minimum needed to disambiguate.
4. Bind the PRD and TDD paths to that one feature directory for the entire run, state the selected slug before design, reject any artifact path outside it, and never use another feature's PRD or TDD as design authority or evidence.
5. Require `status: approved`, a valid immutable `content_revision`, and no open `BLOCKER` in the PRD.
6. Run `python3 scripts/validate_artifact.py <PRD-path> --phase approved`.
7. Read applicable `AGENTS.md`, the full PRD, repository status, manifests, architecture, relevant code, tests, schemas, migrations, CI, and operational configuration.
8. Capture the exact repository revision. Treat meaningful drift during design as a reason to re-check affected sections.

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

Report the selected feature slug, TDD path, selected design, delegated investigations, blockers, validation status, and exact next invocation: `$implement <feature name or description>`. Recommend a fresh session in the same worktree; recommend a new worktree only after both approved documents are committed or copied there.
