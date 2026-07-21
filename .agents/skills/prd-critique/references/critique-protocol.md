# PRD critique protocol

## Select four lenses

Choose the four highest-risk, non-overlapping surfaces for the actual PRD. Candidate surfaces include:

- codebase reality and feasibility
- scope, requirements, and traceability coherence
- authorization, security, privacy, and abuse
- state lifecycle, concurrency, failure, and recovery
- data ownership, migration, retention, and compatibility
- APIs, integrations, clients, and backward compatibility
- UX states, accessibility, localization, and user error recovery
- testability, observability, success metrics, and rollout
- capacity, performance, cost, and operations

Do not select four generic personas. Name a concrete risk hypothesis for each lens.

## Critic task schema

Provide each critic:

- PRD path and immutable revision
- repository root and baseline revision
- assigned lens and risk hypothesis
- relevant requirement IDs
- instruction to remain read-only and cite exact paths/lines

Require this response:

1. `LENS`
2. `INSPECTED`: paths, symbols, tests, and configuration
3. `VERDICTS`: PRD ID | SIGN_OFF / REJECT / NOT_APPLICABLE | evidence | reason
4. `MISSING`: required behavior or constraint absent from the PRD
5. `EDITS`: minimal proposed PRD changes
6. `QUESTIONS`: product decisions only; no implementation questions disguised as product questions

## Main-agent sign-off

- Verify evidence rather than voting by majority.
- A REJECT on P0/P1 behavior, security, data safety, public compatibility, or testability blocks approval until resolved or explicitly waived in the PRD decision log.
- Preserve product authority: codebase constraints may expose tradeoffs but do not silently redefine desired behavior.
- Do not store critic transcripts beside the feature documents; fold durable conclusions into the PRD.

