# Repository guidance

Keep this file short and replace bracketed values when installing the workflow in a real repository.

## Repository map

- Source: `[path]`
- Tests: `[path]`
- Generated or vendored code: `[paths; do not edit manually]`
- Architecture documentation: `[path or None]`

## Commands

- Setup: `[exact command]`
- Focused test: `[exact command]`
- Full test: `[exact command]`
- Lint/type-check/build: `[exact commands]`

If a command is unknown, discover it from repository files and verify it before recording it in a TDD. Never invent a command.

## Working rules

- Read applicable repository instructions before editing.
- Keep changes within the approved PRD and TDD. Treat the PRD as product authority and the TDD as technical authority.
- Follow existing patterns unless the TDD explicitly changes them.
- Preserve unrelated user changes. Do not use destructive Git commands to clean the worktree.
- Add or update tests for changed behavior. Report every required check that could not run.
- Do not push, deploy, publish, or modify external systems unless the user explicitly requests it.

## Done

Work is complete only when the in-scope requirements are implemented, required verification passes, documentation is current, and the intended changes are committed without unrelated files.
