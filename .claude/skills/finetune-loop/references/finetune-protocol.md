# Finetune-loop protocol

## Principles

- **Non-destructive.** Change only the marker-delimited Project context blocks and `CLAUDE.md`'s canonical fields. Never rewrite the universal protocol in any skill or agent.
- **One canonical location per fact.** Repository map and commands live in `CLAUDE.md`. Per-target blocks hold only role-specific execution guidance and reference `CLAUDE.md` for commands.
- **Evidence over invention.** Record only paths, commands, and conventions you verified. Mark everything else as `Unknown` with a short note on what to check. Never invent a command or a path.
- **Idempotent.** Re-running regenerates each block in place and produces no drift when the project is unchanged.

## Extraction checklist

Read documentation first, then confirm against code. Capture:

1. **Product** — domain, purpose, primary users/personas, domain glossary, and the user-visible surfaces that already exist (with paths). Source: `README`, `CLAUDE.md`, `docs/`.
2. **Stack** — languages, frameworks, runtime/build system, package manager, notable dependencies. Source: manifests and lockfiles.
3. **Architecture** — top-level module boundaries and their responsibilities, with exact directory paths. Note the architecture doc path if one exists, else `None`.
4. **Layout** — exact paths for: source, tests, schemas/contracts/API definitions, migrations, generated or vendored code (do-not-edit), runtime/config, and CI/pipeline definitions.
5. **Tests** — framework(s), test-file naming and location conventions, and how tests are grouped (unit/integration/e2e).
6. **Commands** — setup, focused test, full test, lint, type-check, build. Discover from `package.json` scripts, `Makefile`, `pyproject.toml`/`tox.ini`/`noxfile`, `justfile`, `Taskfile`, or CI config. Verify each target/script exists before recording. Do not execute heavy setup; existence in a manifest is sufficient evidence. Never invent.
7. **Risk surfaces** — the two or three failure surfaces most consequential for this class of project (e.g. data correctness and reproducibility for a data/ML repo; authz, input validation, and backward compatibility for a service; state and migration safety for anything with a datastore). Name where the evidence for each lives.
8. **Conventions** — formatter/linter rules, commit or branching conventions, and any hard local rules stated in repository instructions.

Label each captured item as observed or inferred. Anything unverifiable becomes `Unknown — <what to check>`.

## Marker convention

Every managed block is delimited exactly by:

```
<!-- FINETUNE-LOOP:BEGIN — regenerate with /finetune-loop; do not edit inside these markers -->
## Project context

<role-specific content>
<!-- FINETUNE-LOOP:END -->
```

- In a `SKILL.md`, anchor the block immediately after the H1 title line.
- In an agent `.md` (no H1), anchor it immediately after the closing frontmatter `---`.
- On re-run, replace only the text between the markers. If the markers are absent, insert one fresh block at the anchor. Exactly one block per file.

## Per-target content

Keep each block to the sections below that apply. Prefer exact paths and short imperative guidance. Reference `CLAUDE.md` for commands rather than restating them.

- **prd/SKILL.md** — product domain and purpose; primary users; existing user-visible surfaces and where they live (so the PRD can describe current behavior); domain glossary; product-level constraints (supported platforms, compliance, cost) that shape scope.
- **prd-critique/SKILL.md** — the highest-risk failure surfaces to prioritize when selecting the four lenses for this project, each with where its evidence lives; the security/data boundaries and their paths; the testability/observability entry points a critic should cite.
- **tdd/SKILL.md** — stack and build system; architecture and key module boundaries with paths; where contracts, schemas, migrations, config, and CI live; test framework and file conventions; project-specific design conventions to honor. Point to `CLAUDE.md` for exact commands.
- **implement/SKILL.md** — the exact verification commands to run (via `CLAUDE.md`) plus project quirks (codegen or generate step, lockfile discipline, required formatter); code conventions and where they are enforced; generated/vendored paths that must not be hand-edited; commit conventions if any.
- **agents/design-researcher.md** — the research map for this repo: where source, tests, schemas, config, and CI live; language(s); and where reusable patterns are found.
- **agents/prd-critic.md** — this project's domain and its concrete risk surfaces to stay alert to, with where corroborating evidence typically lives.
- **agents/implementation-reviewer.md** — test locations and how to run them (via `CLAUDE.md`); generated/vendored files to ignore in review; the local conventions to check the diff against.

## Stop conditions

Stop and ask the user only when the project's purpose or stack cannot be established from documentation or code, or when a required command genuinely cannot be discovered and its absence would block `tdd`/`implement`. Record non-blocking gaps as `Unknown` rather than guessing.
