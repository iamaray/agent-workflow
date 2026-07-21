#!/usr/bin/env bash
set -euo pipefail

usage() {
  printf 'Usage: %s\n' "$(basename "$0")" >&2
  printf 'Run from inside the project directory you want to initialize.\n' >&2
  printf 'Copies .claude/ and CLAUDE.md from this workflow into the current directory.\n' >&2
}

if [[ $# -gt 0 ]]; then
  usage
  exit 2
fi

script_dir=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
target_dir=$(pwd)

source_claude="$script_dir/.claude"
source_claude_md="$script_dir/CLAUDE.md"

if [[ "$target_dir" == "$script_dir" ]]; then
  printf 'Error: run this from a different project directory, not %s.\n' "$script_dir" >&2
  exit 1
fi

if [[ ! -d "$source_claude" ]]; then
  printf 'Error: missing source directory: %s\n' "$source_claude" >&2
  exit 1
fi

if [[ ! -f "$source_claude_md" ]]; then
  printf 'Error: missing source file: %s\n' "$source_claude_md" >&2
  exit 1
fi

timestamp=$(date +%Y%m%d%H%M%S)

backup_if_exists() {
  local path=$1
  if [[ -e "$path" ]]; then
    local backup="${path}.bak-${timestamp}"
    mv -- "$path" "$backup"
    printf 'Backed up existing %s -> %s\n' "$path" "$backup"
  fi
}

backup_if_exists "$target_dir/.claude"
backup_if_exists "$target_dir/CLAUDE.md"

cp -R -- "$source_claude" "$target_dir/.claude"
cp -- "$source_claude_md" "$target_dir/CLAUDE.md"

printf 'Copied .claude and CLAUDE.md into %s\n' "$target_dir"
