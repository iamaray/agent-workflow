# Agent Workflow Template

A reusable, document-driven feature workflow for [Codex](https://openai.com/codex/) and [Claude Code](https://docs.anthropic.com/en/docs/claude-code). It gives both coding agents the same disciplined loop—from product intent through implementation—while using each tool's native skills, commands, project instructions, and read-only subagents.

The workflow is designed to be copied into an existing repository and then tuned to that codebase. Each feature gets an isolated workspace containing a PRD and TDD, with validation and content hashes enforcing clean handoffs between stages.

## The loop

```text
finetune-loop (once per project, or after major changes)
        |
        v
PRD interview --> four-lens PRD critique --> technical design --> implementation
   draft             approval gate          approval gate       tests + commit
```

The stages are deliberately separate:

1. **Finetune** inspects the repository and adds durable, project-specific context to the otherwise generic skills and specialist agents.
2. **PRD** interviews the user and turns a feature brief into testable product requirements without prematurely designing the solution.
3. **PRD critique** runs four parallel, read-only critics against the document and current codebase, revises the PRD, and approves it only when blockers are resolved.
4. **TDD** inspects the repository, maps every approved requirement to a technical design and verification plan, and records the repository revision used as its baseline.
5. **Implement** follows the approved TDD, adds tests and documentation, runs the required checks, updates the implementation record, and creates one scoped commit. It never pushes or deploys.

PRDs and TDDs carry a self-excluding SHA-256 `content_revision`. The validation scripts check document structure, required sections, unresolved template placeholders, approval status, blockers, and the immutable handoff between the PRD and TDD.

## Repository contents

| Path | Purpose |
| --- | --- |
| `.agents/skills/` | Codex skills for finetuning, PRD creation and critique, TDD creation, and implementation |
| `.codex/` | Codex project configuration and read-only specialist agent definitions |
| `.claude/skills/` | Claude Code versions of the workflow skills |
| `.claude/agents/` | Claude Code specialist agents for critique, design research, and implementation review |
| `AGENTS.md` / `CLAUDE.md` | Project guidance templates populated for the target repository |
| `*-init.sh` | Install the appropriate agent configuration into another repository |
| `*-new-feature.sh` | Create an isolated feature directory with fresh PRD and TDD templates |
| `scripts/` | Stamp and validate workflow artifacts |

## Install in an existing project

Prerequisites are Bash, Python 3, Git, and the Codex or Claude Code CLI. Clone or download this repository somewhere permanent, then set `WORKFLOW_ROOT` to its absolute path:

```bash
export WORKFLOW_ROOT=/absolute/path/to/agents_workflow
cd /absolute/path/to/your/project
```

The init scripts back up an existing agent directory and instruction file with a timestamp before replacing them. They do not merge configurations. Review any backup and reapply project-specific settings that should survive.

The feature skills also require the scaffold and validation helpers. The commands below install those alongside the agent configuration. If your project already has files with the same names, inspect and merge them instead of overwriting them.

### Codex

Run from the root of the project you want to initialize:

```bash
"$WORKFLOW_ROOT/codex-init.sh"

cp "$WORKFLOW_ROOT/codex-new-feature.sh" ./codex-new-feature
chmod +x ./codex-new-feature

mkdir -p scripts
cp "$WORKFLOW_ROOT/scripts/stamp_revision.py" scripts/stamp_revision.py
cp "$WORKFLOW_ROOT/scripts/validate_artifact.py" scripts/validate_artifact.py
```

Review `AGENTS.md` and replace its bracketed repository-map and command placeholders. Then launch Codex with the project root on `PATH` so the `$prd` skill can invoke `codex-new-feature`:

```bash
PATH="$PWD:$PATH" codex
```

In Codex, run:

```text
$finetune-loop
```

The complete Codex feature sequence is:

```text
$prd <feature brief>
$prd-critique <feature name, slug, or PRD path>
$tdd <feature name, slug, or PRD path>
$implement <feature name, slug, or TDD path>
```

Codex stores feature artifacts under `.codex/features/<feature-slug>/`.

### Claude Code

Run from the root of the project you want to initialize:

```bash
"$WORKFLOW_ROOT/claude-init.sh"

cp "$WORKFLOW_ROOT/claude-new-feature.sh" ./claude-new-feature.sh
chmod +x ./claude-new-feature.sh

mkdir -p scripts
cp "$WORKFLOW_ROOT/scripts/stamp_revision.py" scripts/stamp_revision.py
cp "$WORKFLOW_ROOT/scripts/validate_artifact.py" scripts/validate_artifact.py
```

Review `CLAUDE.md`, then launch Claude Code from the project root:

```bash
claude
```

In Claude Code, run:

```text
/finetune-loop
```

The complete Claude feature sequence is:

```text
/prd <feature brief>
/prd-critique <feature name, slug, or PRD path>
/clear
/tdd <feature name, slug, or PRD path>
/clear
/implement <feature name, slug, or TDD path>
```

Claude stores feature artifacts under `.claude/features/<feature-slug>/`.

## Working with features

Normally, start a feature by invoking the PRD skill; it derives a slug and calls the appropriate scaffold helper itself. The helpers can also be run directly:

```bash
# From an initialized Codex project (with the project root on PATH)
codex-new-feature "Audit log export"

# From an initialized Claude project
./claude-new-feature.sh "Audit log export"
```

Both commands normalize the name to a lowercase, hyphenated slug and refuse to overwrite an existing feature workspace.

Use a fresh agent session between major handoffs so the next stage reasons from the approved artifact rather than stale conversational context. Keep the PRD and TDD together in the same feature directory, and commit or copy approved artifacts before moving the work to another worktree.

## Artifact utilities

The skills call these automatically, but they are also useful when editing an artifact by hand:

```bash
# Recompute the content hash after editing
python3 scripts/stamp_revision.py .codex/features/<slug>/PRD.md

# Validate an artifact at a lifecycle gate
python3 scripts/validate_artifact.py .codex/features/<slug>/PRD.md --phase review
python3 scripts/validate_artifact.py .codex/features/<slug>/PRD.md --phase approved
python3 scripts/validate_artifact.py .codex/features/<slug>/TDD.md --phase approved
python3 scripts/validate_artifact.py .codex/features/<slug>/TDD.md --phase implemented
```

For Claude, replace `.codex/features/` with `.claude/features/` in those paths.

## Safety and scope

The workflow preserves unrelated changes and treats the approved PRD as product authority and the approved TDD as technical authority. Specialist agents are read-only. Implementation stages are constrained to the selected feature, stage only intended files, and stop when approval evidence, traceability, baseline compatibility, or required verification is missing. Neither workflow pushes, deploys, publishes, or modifies external systems unless explicitly requested.
