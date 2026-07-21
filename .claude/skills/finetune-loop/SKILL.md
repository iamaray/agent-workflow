---
name: finetune-loop
description: Attune the project-agnostic prd, prd-critique, tdd, and implement skills and their subagents to the current project by reading CLAUDE.md, README.md, and existing code, then writing managed project-context blocks. Use when the user invokes /finetune-loop after dropping this workflow into a repository, or whenever project structure, stack, or commands change.
argument-hint: [project directory]
disable-model-invocation: true
user-invocable: true
---

# Attune the workflow to this project

Read `references/finetune-protocol.md` and `assets/context-block-template.md` before editing any target.

The `prd`, `prd-critique`, `tdd`, and `implement` skills and the `prd-critic`, `design-researcher`, and `implementation-reviewer` subagents are project-agnostic by design. This skill keeps their universal protocol intact and injects a regenerated, marker-delimited **Project context** block into each so their execution is tuned to this repository. It is idempotent: re-run it whenever the project changes.

## Resolve inputs

1. Treat the first argument as the project directory; default to the repository root of the current working directory.
2. Require `.claude/skills/{prd,prd-critique,tdd,implement}/SKILL.md` and `.claude/agents/{prd-critic,design-researcher,implementation-reviewer}.md` to exist. If a target is missing, report it and continue with the rest.
3. Read `CLAUDE.md` and every file it `@`-includes, `README.md` and any `README.*` / `docs/` overview if present, and the current Git status. `CLAUDE.md` is the Claude workflow's source of truth; ignore `AGENTS.md`, which belongs to the codex workflow.

If no `CLAUDE.md` and no `README.md` exist and the directory has no recognizable code, ask the user for the project's purpose and stack before writing.

## Build the project profile

Derive the profile from documentation first, then confirm against code. Follow the protocol's extraction checklist. Capture: product domain and users; tech stack and languages; architecture and key module boundaries with exact paths; locations of source, tests, schemas/contracts, migrations, generated/vendored code, config, and CI; test framework and file conventions; and the highest-risk failure surfaces for this kind of project.

Discover commands (setup, focused test, full test, lint/type-check/build) only from repository files — `package.json` scripts, `Makefile`, `pyproject.toml`/`tox.ini`, `justfile`, CI config, and the like. Verify each exists before recording it. **Never invent a command.** Record anything you cannot establish as an explicit `Unknown` in the profile.

Separate observed facts from inference. Do not fabricate paths, personas, or conventions.

## Update the canonical repository facts

`CLAUDE.md` is the single source of truth for the repository map and commands that `tdd` and `implement` depend on. Fill its bracketed placeholders with the verified profile values (real paths and exact commands). Leave a bracketed placeholder or an explicit `Unknown` where you could not verify a value; do not guess. Do not duplicate these commands into the per-skill blocks — reference `CLAUDE.md` instead so each fact has one canonical home.

## Write the managed blocks

For each target, insert or regenerate exactly one Project context block using the marker convention and per-target content defined in `assets/context-block-template.md`:

1. Locate the existing `<!-- FINETUNE-LOOP:BEGIN ... -->` / `<!-- FINETUNE-LOOP:END -->` pair. If present, replace everything between the markers. If absent, insert a fresh block at the target's anchor (immediately after the H1 in a SKILL.md; immediately after the frontmatter `---` in an agent file).
2. Fill only the sections relevant to that target's role. Keep each block tight — role-specific execution guidance and exact paths, not a copy of the profile or of `CLAUDE.md`.
3. Never edit anything outside the markers. The universal protocol text, frontmatter, and reference files stay untouched.

## Safety

- Edit only the seven target files and `CLAUDE.md`. Never write to `AGENTS.md` — it is the codex workflow's file, not Claude's. Do not touch feature documents, source code, other skills' protocol/reference files, or Git history.
- Preserve all unrelated and untracked changes. Do not run destructive Git commands.
- Do not push, deploy, or modify external systems.

## Return

Report: the project directory and profile summary; the values written to `CLAUDE.md` and any placeholders left unresolved; which of the seven blocks were created versus updated; every `Unknown` a user must resolve; and the reminder that `/finetune-loop` can be re-run whenever the project's structure, stack, or commands change.
