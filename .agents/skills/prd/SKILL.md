---
name: prd
description: Infer a new feature name from the user's brief, create its Codex feature workspace with codex-new-feature, interview the user, and write its PRD. Use only when explicitly invoked as $prd with a feature description; never design or implement the solution.
---

# Generate a PRD

Treat all text accompanying the invocation as the initial feature brief, not as a required slug.

## Create the feature workspace

1. Resolve the repository root from the current working directory, read applicable `AGENTS.md` files, and operate from that root.
2. Infer one short, distinguishing feature name from the brief. Use the user's product terminology; do not ask the user to supply a slug when a clear name can be inferred.
3. If the brief is missing or could reasonably describe multiple distinct features, ask one concise follow-up before creating anything.
4. Predict the normalized slug and check `.codex/features/<slug>`. Never overwrite or adopt a pre-existing directory during `$prd`; if it exists, ask whether the user wants a different feature name or intended to continue that existing feature with another skill.
5. Snapshot the existing immediate child directories of `.codex/features/`, then run `codex-new-feature "<inferred feature name>"` yourself from the repository root. If the shell cannot resolve the alias non-interactively, invoke the same command through the user's interactive login shell so the alias is loaded. Do not reproduce its `mkdir` or template-copying behavior manually. If the command is unavailable or fails, report the exact error and do not create a substitute workspace.
6. Compare the directory list and verify that the command created exactly the predicted directory with sibling `PRD.md` and `TDD.md`; bind the rest of this run to those files and never switch feature directories.
7. Read `assets/PRD_template.md` and `references/interview.md` from this skill. Inspect code only when needed to describe current user-visible behavior; leave feasibility analysis to `$prd-critique`.

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

Report the selected feature slug, PRD path, scope summary, unresolved OQ-IDs, validation result, and the exact next invocation: `$prd-critique <feature name or description>`.
