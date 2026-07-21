#!/usr/bin/env python3
"""Stamp or verify a self-excluding SHA-256 revision in YAML frontmatter."""

from __future__ import annotations

import argparse
import hashlib
import re
import sys
from pathlib import Path


FRONTMATTER_RE = re.compile(r"\A---\r?\n(?P<body>.*?)\r?\n---\r?\n", re.DOTALL)
REVISION_RE = re.compile(r'(?m)^content_revision:[ \t]*(?P<value>.*)$')
NORMALIZED_LINE = 'content_revision: ""'


def frontmatter_parts(text: str) -> tuple[re.Match[str], re.Match[str]]:
    frontmatter = FRONTMATTER_RE.match(text)
    if not frontmatter:
        raise ValueError("missing YAML frontmatter")
    matches = list(REVISION_RE.finditer(frontmatter.group("body")))
    if len(matches) != 1:
        raise ValueError("frontmatter must contain exactly one content_revision field")
    return frontmatter, matches[0]


def normalized_digest(text: str) -> str:
    frontmatter, revision = frontmatter_parts(text)
    body = frontmatter.group("body")
    normalized_body = body[: revision.start()] + NORMALIZED_LINE + body[revision.end() :]
    normalized = text[: frontmatter.start("body")] + normalized_body + text[frontmatter.end("body") :]
    return "sha256:" + hashlib.sha256(normalized.encode("utf-8")).hexdigest()


def current_revision(text: str) -> str:
    _, revision = frontmatter_parts(text)
    value = revision.group("value").strip()
    if len(value) >= 2 and value[0] == value[-1] and value[0] in {'"', "'"}:
        value = value[1:-1]
    return value


def stamped_text(text: str, digest: str) -> str:
    frontmatter, revision = frontmatter_parts(text)
    body = frontmatter.group("body")
    replacement = f'content_revision: "{digest}"'
    updated_body = body[: revision.start()] + replacement + body[revision.end() :]
    return text[: frontmatter.start("body")] + updated_body + text[frontmatter.end("body") :]


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("path", type=Path)
    parser.add_argument("--check", action="store_true", help="verify without modifying")
    args = parser.parse_args()

    try:
        text = args.path.read_text(encoding="utf-8")
        expected = normalized_digest(text)
        current = current_revision(text)
    except (OSError, UnicodeError, ValueError) as exc:
        print(f"revision error: {exc}", file=sys.stderr)
        return 1

    if args.check:
        if current != expected:
            print(f"revision mismatch: expected {expected}, found {current}", file=sys.stderr)
            return 1
        print(expected)
        return 0

    try:
        args.path.write_text(stamped_text(text, expected), encoding="utf-8")
    except OSError as exc:
        print(f"revision error: {exc}", file=sys.stderr)
        return 1
    print(expected)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

