#!/usr/bin/env bash
set -euo pipefail

usage() {
  printf 'Usage: %s <feature-name>\n' "$(basename "$0")" >&2
  printf 'Run from the root of the project where the feature should be created.\n' >&2
}

if [[ $# -ne 1 ]]; then
  usage
  exit 2
fi

feature_name=$1
slug=$(printf '%s' "$feature_name" \
  | tr '[:upper:]' '[:lower:]' \
  | sed -E 's/[^a-z0-9]+/-/g; s/^-+//; s/-+$//; s/-+/-/g')

if [[ -z "$slug" ]]; then
  printf 'Error: feature name must contain at least one letter or digit.\n' >&2
  exit 2
fi

repository_root=$(pwd -P)
feature_root="$repository_root/.codex/features"
prd_template="$repository_root/.agents/skills/prd/assets/PRD_template.md"
tdd_template="$repository_root/.agents/skills/tdd/assets/TDD_template.md"

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
printf 'Next: start codex at %s and invoke $prd with the feature brief.\n' "$repository_root"
