# Implementation protocol

## Authority

- The approved PRD controls product behavior and scope.
- The approved TDD controls technical approach, contracts, sequence, and verification.
- Repository instructions and code control local conventions and describe the current state.
- Stop when these conflict on P0/P1 behavior, public compatibility, data/security boundaries, irreversible work, or verification.

## Safe adaptation

Continue without escalation only for behavior-preserving local adaptations that follow an established repository pattern. Record material deviations in the TDD. Do not use a local adaptation to introduce a dependency, broaden scope, weaken a requirement, or skip a test.

## Worktree discipline

- Preserve all pre-existing changes and untracked files.
- Do not reset, checkout over, stash, delete, or reformat unrelated work.
- Keep delegated agents read-only; centralize edits in the main agent.
- Stage explicit paths and inspect the staged diff before committing.
- Never push or deploy as an implied part of implementation.

## Verification

Run the TDD's canonical CMD-IDs and capture concise outcomes in its completion record. A test is complete only when its expected evidence is observed. A waiver must name an authorized decider and follow-up. Reproduce a claimed pre-existing failure both before and after the change when possible.

