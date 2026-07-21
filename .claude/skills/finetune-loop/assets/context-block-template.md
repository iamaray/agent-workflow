# Project context block template

Copy the marker frame verbatim into each target and fill only the sections listed for that target in `references/finetune-protocol.md`. Delete any section you have no verified content for; write `Unknown — <what to check>` where a needed fact could not be established. Do not restate commands that live in `CLAUDE.md`.

## Marker frame

```
<!-- FINETUNE-LOOP:BEGIN — regenerate with /finetune-loop; do not edit inside these markers -->
## Project context

<sections>
<!-- FINETUNE-LOOP:END -->
```

## Example — tdd/SKILL.md

```
<!-- FINETUNE-LOOP:BEGIN — regenerate with /finetune-loop; do not edit inside these markers -->
## Project context

- Stack: <languages, frameworks, build system, package manager>.
- Architecture: <key modules and responsibilities with exact paths>. Architecture doc: <path or None>.
- Contracts & data: schemas at `<path>`; migrations at `<path>`; config at `<path>`; CI at `<path>`.
- Tests: <framework>; files under `<path>` named `<convention>`. Commands are canonical in CLAUDE.md.
- Conventions to honor: <project-specific design rules>.
<!-- FINETUNE-LOOP:END -->
```

## Example — implement/SKILL.md

```
<!-- FINETUNE-LOOP:BEGIN — regenerate with /finetune-loop; do not edit inside these markers -->
## Project context

- Run the verification commands recorded in CLAUDE.md (setup, focused test, full test, lint/type-check/build).
- Project quirks: <codegen/generate step, lockfile discipline, required formatter, etc.>.
- Do not hand-edit generated or vendored paths: `<paths>`.
- Code conventions enforced by: <linter/formatter and config path>. Commit convention: <convention or None>.
<!-- FINETUNE-LOOP:END -->
```

## Example — agents/prd-critic.md

```
<!-- FINETUNE-LOOP:BEGIN — regenerate with /finetune-loop; do not edit inside these markers -->
## Project context

- Domain: <one line>.
- Stay alert to these risk surfaces for this project: <surface> (evidence in `<path>`); <surface> (evidence in `<path>`).
<!-- FINETUNE-LOOP:END -->
```

Follow the same frame and the per-target section lists for `prd/SKILL.md`, `prd-critique/SKILL.md`, `agents/design-researcher.md`, and `agents/implementation-reviewer.md`.
