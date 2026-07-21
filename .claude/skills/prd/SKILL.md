---
name: prd
description: Interview the user and generate a product requirements document for a feature workspace created by new_feature.sh. Use when the user invokes /prd with a feature slug and optional brief; create or revise that feature's PRD.md without designing or implementing the solution.
argument-hint: <slug> [feature brief]
disable-model-invocation: true
user-invocable: true
---

# Generate a PRD

Treat the first argument as the feature slug and the remaining text as the initial brief.

## Resolve inputs

1. Resolve the repository root from the current working directory.
2. Open `.claude/features/<slug>/PRD.md`; require the sibling `TDD.md` to exist, but do not edit it.
3. Read `assets/PRD_template.md` and `references/interview.md` from this skill.
4. Read applicable `CLAUDE.md` files. Inspect code only when needed to describe current user-visible behavior; leave feasibility analysis to `/prd-critique`.

If the slug is missing, the feature directory is missing, or the feature brief is empty, ask for the missing input before writing.

## Interview

Ask one to three high-impact questions at a time. Resolve problem, users, scope, non-goals, behavior, permissions, lifecycle, errors, quality targets, success, rollout, and policy. Challenge proposed solutions that do not establish a user need. Record unknowns explicitly instead of guessing.

Continue until all product decisions needed for a reviewable PRD are answered or recorded as owned open questions. Do not ask technical-implementation questions unless the answer changes product behavior or a hard constraint.

## Write

1. Replace the initialized PRD with a completed instance of the template.
2. Keep stable IDs and one canonical location per fact.
3. Delete inapplicable optional sections and all authoring prompts.
4. Set `status: in_review`; do not mark the PRD approved before critique.
5. Do not edit source code, `TDD.md`, Git history, or external systems.
6. Run `python3 scripts/stamp_revision.py <PRD-path>` and `python3 scripts/validate_artifact.py <PRD-path> --phase review` from the repository root.

## Return

Report the PRD path, scope summary, unresolved OQ-IDs, validation result, and the exact next invocation: `/prd-critique <path-to-PRD.md>`.
