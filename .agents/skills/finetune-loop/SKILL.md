---
name: finetune-loop
description: Inspect a newly initialized or materially changed repository and add concise, durable project-specific context to the prd, prd-critique, tdd, and implement skills plus the Codex agents in .codex/agents. Use only when explicitly invoked as $finetune-loop to attune the otherwise project-agnostic feature workflow; update existing generated context idempotently without changing the workflow's generic rules.
---

# Finetune the feature loop

Adapt the installed feature workflow to the current repository. Treat repository evidence as authoritative, keep the generic workflow intact, and write only facts that will remain useful across multiple features.

## Inspect the project

1. Resolve the repository root. Require these skill files:
   - `.agents/skills/prd/SKILL.md`
   - `.agents/skills/prd-critique/SKILL.md`
   - `.agents/skills/tdd/SKILL.md`
   - `.agents/skills/implement/SKILL.md`
2. Require at least one `*.toml` agent definition in `.codex/agents/`. Update every agent definition there, including project-added agents.
3. Read the root `AGENTS.md`, then every other applicable `AGENTS.md`. Read the root `README.md` when it exists; also read directly linked architecture or contributor documentation that materially constrains the workflow.
4. Inventory the project before forming conclusions. Inspect tracked source, tests, manifests, lockfiles, build and task configuration, schemas and migrations, CI, deployment and operational configuration, and representative implementation paths. For a small repository, read all text code. For a large repository, use the full inventory to identify components and inspect enough code from every first-party component to establish its boundaries, patterns, and commands.
5. Read current Git status and preserve unrelated changes. Do not inspect ignored secrets, credential files, dependency trees, build outputs, vendored code, binaries, or generated files except when repository instructions explicitly require them.
6. Establish facts from files, not filenames or assumptions. Verify commands from repository configuration; never invent a command. Mark uncertainty by omission rather than adding speculative guidance.

If required workflow targets are missing or malformed, stop and report the exact paths instead of partially tuning the loop.

## Distill durable context

Keep only project facts that change how a role should reason or act. Prefer exact paths, named symbols, verified commands, and explicit invariants. Avoid feature-specific details, prose copied from documentation, exhaustive file lists, transient Git state, obvious language facts, and generic advice already present in the workflow.

Tailor the context by target:

- `prd`: product vocabulary, user-visible behavior, established product boundaries, compatibility promises, and relevant policy constraints. Do not preload solution design.
- `prd-critique`: repository reality, cross-component risk surfaces, compatibility and data constraints, and high-value evidence locations.
- `tdd`: architecture and dependency boundaries, contracts, state and data conventions, test structure, CI and operational constraints, and verified design-time commands.
- `implement`: edit boundaries, local implementation patterns, generated or vendored exclusions, required documentation, and exact setup, focused-test, full-test, lint, type-check, or build commands that actually exist.
- each Codex agent: only the subset needed for that agent's stated responsibility. Preserve its name, sandbox mode, generic instructions, and response contract.

When `AGENTS.md` still contains placeholders or conflicts with executable repository configuration, record the verified repository fact in the role that needs it and report the stale instruction; do not silently rewrite `AGENTS.md`.

## Update idempotently

In each workflow `SKILL.md`, append a final section using exactly these boundary comments:

```markdown
<!-- finetune-loop:start -->
## Project-specific context

[concise role-specific bullets]
<!-- finetune-loop:end -->
```

In each `.codex/agents/*.toml`, place the equivalent role-specific block inside `developer_instructions` immediately before its closing triple quote, using exactly these plain-text boundaries:

```text
[finetune-loop:start]
Project-specific context:
- ...
[finetune-loop:end]
```

Replace an existing bounded block in place. Never add a second block. Do not change content outside the boundaries unless needed to repair malformed boundaries, and report any such repair. If there is no useful target-specific fact, use `- No additional project-specific constraints identified.` so successful tuning is explicit.

Keep each block compact: normally three to eight bullets, combining tightly related facts. Do not add secrets, absolute machine-specific paths, mutable revision hashes, or claims unsupported by inspected files.

## Verify and report

1. Re-read every edited target and confirm there is exactly one well-formed block, valid Markdown or TOML structure, no placeholders introduced, and no changes outside the intended blocks.
2. Review the diff for accuracy, role relevance, duplication, accidental secrets, and unrelated edits.
3. Run repository-provided format or validation checks that cover the edited files when they exist. Do not run application test suites merely because context files changed.
4. Do not edit application code, feature documents, Git history, or external systems. Do not commit unless explicitly requested.

Report inspected sources, updated targets, the most consequential context added, validation performed, unresolved uncertainties, and any stale or conflicting repository documentation found.
