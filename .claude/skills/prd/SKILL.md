---
name: prd
description: Interview the user and generate a product requirements document. Use when the user invokes /prd with a feature brief; infer a feature slug from the brief, scaffold the workspace with claude-new-feature, then create or revise only that feature's PRD.md without designing or implementing the solution.
argument-hint: <feature brief>
disable-model-invocation: true
user-invocable: true
---

# Generate a PRD

Treat the entire argument as the feature brief.

## Resolve the feature

1. Resolve the repository root from the current working directory.
2. Infer a concise, valid feature slug (lowercase, hyphen-separated) that names the feature described in the brief. If the brief is empty or too vague to name a feature, ask the user for a one-line description before continuing. Report the chosen slug.
3. If `.claude/features/<slug>/` does not exist, scaffold it by running `./claude-new-feature.sh <slug>` from the repository root; this creates the feature's `PRD.md` and `TDD.md`. If the directory already exists, reuse it and revise its `PRD.md` in place rather than re-scaffolding.
4. Open only `.claude/features/<slug>/PRD.md`; require the sibling `TDD.md` to exist, but do not edit it. Read from and write to nothing under any other feature folder.
5. Read `assets/PRD_template.md` and `references/interview.md` from this skill.
6. Read applicable `CLAUDE.md` files. Inspect code only when needed to describe current user-visible behavior; leave feasibility analysis to `/prd-critique`.

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

Report the resolved feature slug, the PRD path, scope summary, unresolved OQ-IDs, validation result, and the exact next invocation: `/prd-critique <feature>` (the feature name or the path to its `PRD.md`).
