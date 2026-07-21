# PRD interview guide

Use questions to resolve decisions, not to make the user narrate the template. Ask only what cannot be established from the prompt or observable current behavior.

## Question order

1. Outcome: user, problem, evidence, and why now.
2. Boundary: smallest useful release, non-goals, compatibility, and migration expectations.
3. Behavior: happy path, failure paths, permissions, lifecycle, repeated actions, races visible to users, and exact limits.
4. Quality: performance, reliability, accessibility, security, privacy, compliance, and cost targets that affect release.
5. Evidence: acceptance criteria, success metrics, guardrails, telemetry, rollout, and rollback conditions.

## Rules

- Ask one to three questions per turn, ordered by downstream impact.
- Offer concrete options when that reduces ambiguity, but do not bias the answer with a straw man.
- Distinguish product behavior from a suggested implementation.
- Use `Unknown — OQ-<n>` with an owner and safe default only for non-blocking uncertainty.
- Mark a question `BLOCKER` when different answers would change P0/P1 behavior, scope, policy, data handling, or a public contract.
- Write acceptance criteria as deterministic Given/When/Then outcomes with observable evidence.
- Do not fabricate baselines, targets, personas, research, or dependencies.

