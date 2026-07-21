---
document_type: prd
schema_version: "1.0"
revision: 1
content_revision: "[Commit SHA or SHA-256 digest of this approved file]"
title: "[Feature or project name]"
status: draft # draft | in_review | approved | superseded
owner: "[Product owner]"
authors: ["[Name]"]
reviewers: ["[Name or team]"]
created: YYYY-MM-DD
last_updated: YYYY-MM-DD
target_release: "[Date, milestone, or TBD]"
related_tdd: "[Link or path, or TBD]"
source_material:
  - "[Research, issue, design, analytics, or customer-feedback link]"
---

# PRD: [Feature or project name]

> This document is the authority for **why the feature exists, what behavior is required, and how success is judged**. It must not prescribe implementation unless a technical choice is itself a product or regulatory constraint.

## Authoring rules

Delete this section when the PRD is approved.

- Complete every **Required** field; delete optional sections that do not apply.
- Replace every bracketed prompt. Do not leave ambiguous placeholders such as “etc.” or “as needed.”
- Use stable IDs. Never reuse or renumber an ID after review begins.
- Increment `revision` for every approved normative change and set `content_revision` to an immutable commit SHA or file digest. A timestamp is not an immutable revision.
- Use **MUST**, **SHOULD**, and **MAY** to describe behavior when an item is included. The **Priority** field alone controls release inclusion: P0 blocks launch; P1 may be deferred only by a recorded PD-ID naming the authorized decider; P2 does not block launch.
- State observable outcomes, not classes, tables, frameworks, or algorithms.
- Quantify limits and quality targets. If a value is unknown, record it as an open question with an owner.
- Use `None` when an applicable category has no entries. Use `Unknown — OQ-[ID]` when the answer is not known; never fabricate a baseline, target, dependency, risk, or constraint to fill the template.
- Keep each fact in one canonical location: business rules define invariant behavior; requirements reference rules; acceptance criteria verify behavior; journeys illustrate sequencing without redefining rules; §13 owns cross-ID traceability.
- Mark unresolved implementation-blocking questions as `BLOCKER`; all blockers must be resolved before implementation handoff.

## 0. Agent handoff summary — Required

Complete this derived index after the detailed sections. It is the minimum context an implementation or design agent should read first; use IDs rather than restating normative content.

| Field | Answer |
|---|---|
| Objective | [G-IDs plus a one-sentence outcome] |
| Primary users | [ACT-IDs] |
| User-visible change | [UC/FR-IDs] |
| In-scope deliverables | [FR/NFR-IDs] |
| Explicit exclusions | [NG-IDs] |
| Release condition | [AC/MET/GR-IDs] |
| Critical constraints | [BR/NFR/DEP/data-policy IDs] |
| Blockers | [None, or OQ-IDs marked BLOCKER] |

## 1. Problem and context — Required

### 1.1 Problem statement

**[User or actor]** cannot reliably **[complete a task or achieve an outcome]** because **[root cause or unmet need]**, resulting in **[measurable user or business impact]**.

### 1.2 Current behavior

[Describe the current workflow, product behavior, and workarounds. Include only context necessary to understand the requirements.]

### 1.3 Evidence

| Evidence | Source | What it demonstrates |
|---|---|---|
| [Metric, research finding, request, or incident] | [Link or citation] | [Relevance to the problem] |

### 1.4 Why now?

[Explain the trigger, urgency, and consequence of not acting.]

## 2. Product intent — Required

### 2.1 Goals

| ID | Outcome | Success signal |
|---|---|---|
| G-01 | [User or business outcome] | [How we will know it occurred] |

### 2.2 Non-goals

| ID | Out of scope | Reason or future disposition |
|---|---|---|
| NG-01 | [Capability, user, platform, or scenario not included] | [Why it is excluded or where it belongs] |

### 2.3 Product principles

[Optional: list only principles that resolve likely tradeoffs, in priority order.]

1. [Example: Prevent irreversible user harm before optimizing speed.]
2. [Example: Preserve existing workflows unless a requirement says otherwise.]

## 3. Users and use cases — Required

### 3.1 Actors

| ID | Actor | Need | Permissions or constraints |
|---|---|---|---|
| ACT-01 | [User, admin, service, or external system] | [Goal] | [Relevant limitations] |

### 3.2 Use cases

| ID | Actor | Trigger | Expected outcome | Priority |
|---|---|---|---|---|
| UC-01 | ACT-01 | [What starts the use case] | [Observable end state] | P0 / P1 / P2 |

Priority meanings:

- **P0:** Required for initial release; absence blocks launch.
- **P1:** Important and expected; may be deferred only through an explicit decision.
- **P2:** Optional enhancement; implementation must not compromise P0/P1 behavior.

### 3.3 Detailed journey

Create one block for every P0 use case. For a P0 use case that needs no sequence beyond its requirement, state that explicitly. Add P1/P2 journeys only when sequencing clarifies behavior.

#### [UC-ID] — [Use-case name]

- **Preconditions:** [State, entitlement, authentication, or prior action]
- **Trigger:** [User or system action]
- **Happy path:**
  1. [Actor action]
  2. [Product response]
  3. [Observable result]
- **Alternative paths:** [Valid variations]
- **Failure paths:** [Invalid input, denied permission, unavailable dependency, interruption, or conflict]
- **Postconditions:** [State guaranteed after success or failure]

## 4. Functional requirements — Required

### 4.1 Requirement index

| ID | Requirement | Priority | Related use case |
|---|---|---|---|
| FR-01 | [Concise observable behavior] | P0 / P1 / P2 | UC-01 |

### 4.2 Detailed requirements

#### FR-01 — [Requirement name]

- **Statement:** The product MUST [observable behavior].
- **Rationale:** [Why this behavior is needed.]
- **Actors:** [ACT-IDs]
- **Preconditions:** [Required starting state, or None]
- **Inputs:** [User/system inputs and validation boundaries]
- **Behavior:** [Rules, ordering, permissions, and state changes visible at the product level]
- **Outputs:** [Visible result, notification, artifact, or state]
- **Error behavior:** [What the actor sees and what state is preserved]
- **Edge cases:** [Boundary cases that materially affect expected behavior]
- **Related rules:** [BR/data-policy IDs, or None]
- **Out of scope:** [Similar behavior this requirement does not imply]

Duplicate the subsection above for each requirement. Keep one independently testable behavior per requirement.

## 5. Acceptance criteria — Required

Every P0/P1 requirement must have at least one happy-path criterion and one relevant failure or boundary criterion. Criteria must be deterministic and externally observable.

### AC-01 — [Scenario name]

- **Given:** [Initial state and actor]
- **When:** [Single action or event]
- **Then:** [Observable result]
- **And:** [Additional result, if needed]
- **Evidence:** [Test result, UI observation, API response, emitted event, or metric]

### AC-02 — [Failure or boundary scenario]

- **Given:** [Failure, invalid, empty, concurrent, or limit condition]
- **When:** [Action or event]
- **Then:** [Expected outcome and preserved state]
- **Evidence:** [How a reviewer can verify it]

## 6. Experience and interface requirements — If applicable

### 6.1 Required states

| ID | Surface | Default | Loading/in progress | Empty | Success | Error | Permission denied | Parent requirement | Priority |
|---|---|---|---|---|---|---|---|---|---|
| IX-01 | [UI, API, CLI, notification, or report] | [Behavior] | [Behavior] | [Behavior] | [Behavior] | [Behavior] | [Behavior] | FR-01 | P0 / P1 / P2 |

### 6.2 Content and interaction rules

| ID | Content or interaction rule | Parent requirement | Priority |
|---|---|---|---|
| IX-02 | [User-facing terminology, confirmation, reversibility, feedback timing, accessibility, responsive behavior, or localization rule] | FR/NFR-ID | P0 / P1 / P2 |

Link designs rather than duplicating them. If a design contains normative behavior, assign that behavior an IX-ID here rather than relying on the external file alone.

### 6.3 Design references

- Canonical design: [Link or path]
- Prototype: [Link or path]
- Copy/content: [Link or path]

## 7. Product rules and data policy — Required when data is involved

### 7.1 Canonical terminology

| Term | Exact definition | Not to be confused with |
|---|---|---|
| [Term] | [Unambiguous definition] | [Related term] |

### 7.2 Business rules

| ID | Rule | Applies to | Exceptions |
|---|---|---|---|
| BR-01 | [Validation, eligibility, limit, ownership, or lifecycle rule] | [FR/UC IDs] | [None or explicit exceptions] |

### 7.3 Authorization and eligibility matrix — Required when access differs by actor or state

| ID | Actor/role | Action | Scope | Eligibility/preconditions | Allowed result | Denial result | Parent requirement | Priority |
|---|---|---|---|---|---|---|---|---|
| AUTH-01 | [ACT-ID/role] | [Action] | [Tenant/resource scope] | [Identity, entitlement, state] | [Observable outcome] | [Error/outcome without information leakage] | FR-01 | P0 / P1 / P2 |

### 7.4 Lifecycle and concurrency model — Required for stateful features

| ID | Entity/current state | Trigger | Actor | Preconditions | Next state | Observable result | Failure result | Simultaneous-event precedence | Parent requirement | Priority |
|---|---|---|---|---|---|---|---|---|---|---|
| LIFE-01 | [Entity/state] | [Action/event/time boundary] | [ACT-ID/system] | [Rules] | [State] | [Outcome] | [Outcome] | [Which event wins and why] | FR-01 | P0 / P1 / P2 |

Include terminal states, exact time-boundary behavior, repeated actions, and meaningful races. Use `None` for features with no persisted or concurrent lifecycle.

### 7.5 Data handling requirements

| ID | Data category | Purpose | Visibility | Retention/deletion expectation | Sensitivity | Parent requirement | Priority |
|---|---|---|---|---|---|---|---|
| DATA-POL-01 | [Data] | [Why it is needed] | [Who may see it] | [Product-level expectation] | Public / Internal / Confidential / Restricted | FR-01 / NFR-04 | P0 / P1 / P2 |

## 8. Non-functional requirements — Required

Only include measurable requirements. The TDD will specify how they are achieved.

| ID | Area | Requirement | Measurement | Priority |
|---|---|---|---|---|
| NFR-01 | Performance | [Example: the operation MUST complete within 500 ms at p95 under defined load] | [Where/how measured] | P0 / P1 / P2 |
| NFR-02 | Availability | [Target and measurement boundary] | [SLI/SLO method] | P0 / P1 / P2 |
| NFR-03 | Security | [Access or protection outcome] | [Review/test] | P0 / P1 / P2 |
| NFR-04 | Privacy | [Collection, consent, retention, deletion, or residency outcome] | [Review/test] | P0 / P1 / P2 |
| NFR-05 | Accessibility | [Conformance target and surfaces] | [Audit/test] | P0 / P1 / P2 |
| NFR-06 | Compatibility | [Supported clients, versions, or integrations] | [Matrix/test] | P0 / P1 / P2 |
| NFR-07 | Reliability | [Correctness, durability, or recovery expectation] | [Metric/test] | P0 / P1 / P2 |
| NFR-08 | Cost | [Budget or unit-cost ceiling] | [Cost report] | P0 / P1 / P2 |

## 9. Measurement and telemetry — Required

### 9.1 Success metrics

| ID | Metric | Baseline | Target | Window | Segment | Owner |
|---|---|---:|---:|---|---|---|
| MET-01 | [Outcome metric] | [Value] | [Value] | [Period] | [Population] | [Name/team] |

### 9.2 Guardrails

| ID | Metric | Must remain | Response if breached | Parent requirement | Priority |
|---|---|---|---|---|---|
| GR-01 | [Metric that must not regress] | [Threshold] | [Pause, roll back, investigate, etc.] | FR/NFR-ID | P0 / P1 / P2 |

### 9.3 Required events or audit records

| ID | Event/audit record | Trigger | Required properties | Supports | Parent requirement | Priority |
|---|---|---|---|---|---|---|
| EVT-01 | [Stable name] | [Exact occurrence] | [Fields, excluding implementation-specific encoding] | MET-01 / compliance / support | FR/NFR-ID | P0 / P1 / P2 |

## 10. Dependencies and constraints — Required

| ID | Dependency or constraint | Owner/source | Needed by | Failure impact | Fallback | Parent requirement | Priority |
|---|---|---|---|---|---|---|---|
| DEP-01 | [Team, API, vendor, policy approval, date, or platform] | [Owner/link] | [Milestone] | [Impact] | [Fallback or None] | FR/NFR-ID | P0 / P1 / P2 |

## 11. Release and operations — Required

### 11.1 Release strategy

[Describe product-level rollout stages, eligibility, feature exposure, migration expectations, communication, and support readiness. Do not prescribe deployment mechanics unless they are constraints.]

### 11.2 Release gates

- [ ] All P0 acceptance criteria pass.
- [ ] P1 deferrals have explicit decision records.
- [ ] Success and guardrail telemetry is validated.
- [ ] Required security, privacy, legal, accessibility, and compliance reviews are complete.
- [ ] User/support documentation and ownership are ready.
- [ ] Rollback or disablement criteria are agreed.
- [ ] No open `BLOCKER` questions remain.

### 11.3 Pause or rollback conditions

| Condition | Threshold | Decision owner | Required response |
|---|---|---|---|
| [Guardrail, incident, or correctness failure] | [Measurable trigger] | [Name/team] | [Pause, restrict, or roll back] |

## 12. Assumptions, risks, and open questions — Required

### 12.1 Assumptions

| ID | Assumption | Confidence | Validation | Owner | If false |
|---|---|---|---|---|---|
| ASM-01 | [Belief used by this PRD] | Low / Medium / High | [Method and date] | [Name] | [Requirement/scope impact] |

### 12.2 Risks

| ID | Risk | Likelihood | Impact | Mitigation | Owner |
|---|---|---|---|---|---|
| RISK-01 | [Product, adoption, policy, delivery, or dependency risk] | Low / Medium / High | Low / Medium / High | [Action] | [Name] |

### 12.3 Open questions

| ID | Severity | Question | Options/default | Owner | Due | Resolution |
|---|---|---|---|---|---|---|
| OQ-01 | BLOCKER / Non-blocking | [Specific question] | [Options or safe default] | [Name] | YYYY-MM-DD | Open / [Answer] |

Non-blocking questions must specify the default an implementation agent may use if no answer arrives.

## 13. Traceability — Required

Every P0/P1 item must be traceable from goal to verification. This table is the canonical home for cross-ID relationships. Generate or validate it after editing other sections; do not maintain duplicate acceptance-criterion links elsewhere.

| Goal | Use case | Requirement | Linked rules/policies/events/guardrails | Acceptance criteria | Metric |
|---|---|---|---|---|---|
| G-01 | UC-01 | FR-01, NFR-01 | BR-01, AUTH-01, LIFE-01, DATA-POL-01, IX-01, IX-02, DEP-01, EVT-01, GR-01 | AC-01, AC-02 | MET-01 |

## 14. Implementation handoff gate — Required

The PRD is ready for technical design or implementation only when all applicable boxes are checked.

- [ ] The agent handoff summary is complete and consistent with the detailed sections.
- [ ] Scope, non-goals, actors, and terminology are unambiguous.
- [ ] Every P0/P1 functional requirement is independently testable.
- [ ] Happy paths, errors, permissions, empty states, and material edge cases are specified.
- [ ] NFRs contain numeric targets or explicit review criteria.
- [ ] Acceptance criteria map to requirements and expected evidence.
- [ ] Dependencies, policy constraints, and rollout gates are known.
- [ ] All product decisions required for design are resolved.
- [ ] No open `BLOCKER` questions remain.
- [ ] Reviewers have approved the document and `status` is `approved`.

## 15. Decision log

| ID | Date | Decision | Rationale | Affected IDs | Decider |
|---|---|---|---|---|---|
| PD-01 | YYYY-MM-DD | [Decision] | [Why] | [FR/NFR/UC IDs] | [Name] |

## Appendix

[Optional: glossary, research detail, calculations, mockups, examples, and other supporting material. Keep normative requirements in the numbered sections above.]
