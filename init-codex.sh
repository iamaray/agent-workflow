#!/usr/bin/env bash
set -euo pipefail

usage() {
  printf 'Usage: %s\n' "$(basename "$0")" >&2
  printf 'Run from inside the project directory you want to initialize.\n' >&2
  printf 'Copies .agents/, .codex/, and AGENTS.md from this workflow into the current directory.\n' >&2
}

if [[ $# -gt 0 ]]; then
  usage
  exit 2
fi

script_dir=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
target_dir=$(pwd -P)

if [[ "$target_dir" == "$script_dir" ]]; then
  printf 'Error: run this from a different project directory, not %s.\n' "$script_dir" >&2
  exit 1
fi

for source_path in "$script_dir/.agents" "$script_dir/.codex" "$script_dir/AGENTS.md"; do
  if [[ ! -e "$source_path" ]]; then
    printf 'Error: missing source: %s\n' "$source_path" >&2
    exit 1
  fi
done

timestamp=$(date +%Y%m%d%H%M%S)

backup_if_exists() {
  local path=$1
  if [[ -e "$path" || -L "$path" ]]; then
    local backup="${path}.bak-${timestamp}"
    local suffix=1

    while [[ -e "$backup" || -L "$backup" ]]; do
      backup="${path}.bak-${timestamp}-${suffix}"
      suffix=$((suffix + 1))
    done

    mv -- "$path" "$backup"
    printf 'Backed up existing %s -> %s\n' "$path" "$backup"
  fi
}

backup_if_exists "$target_dir/.agents"
backup_if_exists "$target_dir/.codex"
backup_if_exists "$target_dir/AGENTS.md"

cp -R -- "$script_dir/.agents" "$target_dir/.agents"
cp -R -- "$script_dir/.codex" "$target_dir/.codex"
cp -- "$script_dir/AGENTS.md" "$target_dir/AGENTS.md"

printf 'Copied .agents, .codex, and AGENTS.md into %s\n' "$target_dir"
