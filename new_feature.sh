#!/usr/bin/env bash
set -euo pipefail

usage() {
  printf 'Usage: %s <feature-name> <codex|claude>\n' "$(basename "$0")" >&2
}

if [[ $# -ne 2 ]]; then
  usage
  exit 2
fi

feature_name=$1
model_name=$(printf '%s' "$2" | tr '[:upper:]' '[:lower:]')
slug=$(printf '%s' "$feature_name" \
  | tr '[:upper:]' '[:lower:]' \
  | sed -E 's/[^a-z0-9]+/-/g; s/^-+//; s/-+$//; s/-+/-/g')

if [[ -z "$slug" ]]; then
  printf 'Error: feature name must contain at least one letter or digit.\n' >&2
  exit 2
fi

script_dir=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)

case "$model_name" in
  codex)
    feature_root="$script_dir/.codex/features"
    prd_template="$script_dir/.agents/skills/prd/assets/PRD_template.md"
    tdd_template="$script_dir/.agents/skills/tdd/assets/TDD_template.md"
    invocation='$prd'
    ;;
  claude)
    feature_root="$script_dir/.claude/features"
    prd_template="$script_dir/.claude/skills/prd/assets/PRD_template.md"
    tdd_template="$script_dir/.claude/skills/tdd/assets/TDD_template.md"
    invocation='/prd'
    ;;
  *)
    printf 'Error: model must be "codex" or "claude".\n' >&2
    usage
    exit 2
    ;;
esac

for template in "$prd_template" "$tdd_template"; do
  if [[ ! -f "$template" ]]; then
    printf 'Error: missing template: %s\n' "$template" >&2
    exit 1
  fi
done

target="$feature_root/$slug"
mkdir -p -- "$feature_root"
if ! mkdir -- "$target"; then
  printf 'Error: feature workspace already exists or cannot be reserved: %s\n' "$target" >&2
  exit 1
fi

created_target=1
cleanup() {
  if [[ "${created_target:-0}" = 1 && -d "$target" ]]; then
    rm -f -- "$target/PRD.md" "$target/TDD.md"
    rmdir -- "$target" 2>/dev/null || true
  fi
}
trap cleanup EXIT INT TERM

cp -- "$prd_template" "$target/PRD.md"
cp -- "$tdd_template" "$target/TDD.md"
created_target=0
trap - EXIT INT TERM

printf 'Created %s\n' "$target"
printf 'Next: start %s at %s and invoke %s %s <feature brief>\n' "$model_name" "$script_dir" "$invocation" "$slug"
