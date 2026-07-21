#!/usr/bin/env python3
"""Validate structural handoff invariants for workflow PRDs and TDDs."""

from __future__ import annotations

import argparse
import re
import subprocess
import sys
from pathlib import Path


FRONTMATTER_RE = re.compile(r"\A---\r?\n(?P<body>.*?)\r?\n---\r?\n", re.DOTALL)
SCALAR_RE = re.compile(r"^(?P<key>[a-z_]+):[ \t]*(?P<value>.*)$")
FENCE_RE = re.compile(r"(?ms)^(?P<fence>`{3,}|~{3,})[^\n]*\n.*?^(?P=fence)[ \t]*$")
LINK_RE = re.compile(r"!?\[[^\]\n]+\]\([^\)\n]+\)")
INLINE_CODE_RE = re.compile(r"`[^`\n]*`")
DIGEST_RE = re.compile(r"^sha256:[0-9a-f]{64}$")
GIT_REVISION_RE = re.compile(r"^(?:git:)?[0-9a-f]{40,64}$")

STATUS = {
    "prd": {"draft", "in_review", "approved", "superseded"},
    "tdd": {"draft", "in_review", "approved", "implemented", "superseded"},
}

REQUIRED = {
    "prd": {
        "keys": {"document_type", "schema_version", "revision", "content_revision", "title", "status"},
        "headings": {
            "Agent handoff summary",
            "Problem and context",
            "Product intent",
            "Functional requirements",
            "Acceptance criteria",
            "Non-functional requirements",
            "Traceability",
            "Implementation handoff gate",
        },
        "template": Path(".agents/skills/prd/assets/PRD_template.md"),
    },
    "tdd": {
        "keys": {
            "document_type",
            "schema_version",
            "revision",
            "content_revision",
            "title",
            "status",
            "related_prd_revision",
            "repository_revision",
        },
        "headings": {
            "Implementation handoff summary",
            "Authority, conflict, and agent execution rules",
            "Context and repository baseline",
            "Requirements and design goals",
            "Selected design",
            "Failure modes and recovery",
            "Security, privacy, and abuse resistance",
            "Implementation plan",
            "Test and verification plan",
            "Implementation readiness gate",
        },
        "template": Path(".agents/skills/tdd/assets/TDD_template.md"),
    },
}


def unquote(value: str) -> str:
    value = value.split(" #", 1)[0].strip()
    if len(value) >= 2 and value[0] == value[-1] and value[0] in {'"', "'"}:
        return value[1:-1]
    return value


def parse_frontmatter(text: str) -> tuple[dict[str, str], list[str]]:
    match = FRONTMATTER_RE.match(text)
    if not match:
        return {}, ["missing YAML frontmatter"]
    fields: dict[str, str] = {}
    errors: list[str] = []
    for line_number, line in enumerate(match.group("body").splitlines(), start=2):
        if not line or line[0].isspace() or line.startswith("-") or line.startswith("#"):
            continue
        scalar = SCALAR_RE.match(line)
        if not scalar:
            continue
        key = scalar.group("key")
        if key in fields:
            errors.append(f"duplicate frontmatter key {key!r} on line {line_number}")
            continue
        fields[key] = unquote(scalar.group("value"))
    return fields, errors


def semantic_text(text: str) -> str:
    text = FENCE_RE.sub("", text)
    text = LINK_RE.sub("", text)
    return INLINE_CODE_RE.sub("", text)


def headings(text: str) -> set[str]:
    result: set[str] = set()
    for line in semantic_text(text).splitlines():
        match = re.match(r"^#{2,3}\s+(?:\d+(?:\.\d+)*\.\s*)?(.+?)(?:\s+—.*)?$", line)
        if match:
            result.add(match.group(1).strip())
    return result


def template_placeholders(document_type: str) -> set[str]:
    root = Path(__file__).resolve().parent.parent
    template = root / REQUIRED[document_type]["template"]
    try:
        source = semantic_text(template.read_text(encoding="utf-8"))
    except OSError:
        return set()
    tokens = set(re.findall(r"\[[^\]\n]+\]", source))
    return {token for token in tokens if token.strip("[] ") and token not in {"[x]", "[X]"}}


def run_revision_check(path: Path) -> str | None:
    helper = Path(__file__).with_name("stamp_revision.py")
    result = subprocess.run(
        [sys.executable, str(helper), str(path), "--check"],
        capture_output=True,
        text=True,
        check=False,
    )
    return None if result.returncode == 0 else result.stderr.strip()


def open_blocker_exists(text: str) -> bool:
    for line in semantic_text(text).splitlines():
        if line.startswith("|"):
            cells = [cell.strip() for cell in line.strip().strip("|").split("|")]
            if "BLOCKER" in cells and cells[-1].lower() == "open":
                return True
        elif re.search(r"^\s*[-*]\s*BLOCKER\b.*\b(open|unresolved|pending)\b", line, re.IGNORECASE):
            return True
    return False


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("path", type=Path)
    parser.add_argument("--phase", choices=("draft", "review", "approved", "implemented"), default="review")
    args = parser.parse_args()

    errors: list[str] = []
    try:
        text = args.path.read_text(encoding="utf-8")
    except (OSError, UnicodeError) as exc:
        print(f"validation error: {exc}", file=sys.stderr)
        return 1

    fields, frontmatter_errors = parse_frontmatter(text)
    errors.extend(frontmatter_errors)
    document_type = fields.get("document_type", "")
    if document_type not in REQUIRED:
        errors.append(f"unsupported document_type: {document_type or '<missing>'}")
    else:
        missing_keys = sorted(REQUIRED[document_type]["keys"] - fields.keys())
        if missing_keys:
            errors.append("missing frontmatter keys: " + ", ".join(missing_keys))
        empty_keys = sorted(key for key in REQUIRED[document_type]["keys"] if key in fields and not fields[key])
        if empty_keys:
            errors.append("empty required frontmatter values: " + ", ".join(empty_keys))
        missing_headings = sorted(REQUIRED[document_type]["headings"] - headings(text))
        if missing_headings:
            errors.append("missing required headings: " + ", ".join(missing_headings))

    if document_type in STATUS and fields.get("status") not in STATUS[document_type]:
        errors.append(f"invalid {document_type} status: {fields.get('status') or '<missing>'}")
    if fields.get("revision") and not re.fullmatch(r"[1-9][0-9]*", fields["revision"]):
        errors.append("revision must be a positive integer")

    expected_status = {"draft": "draft", "approved": "approved", "implemented": "implemented"}.get(args.phase)
    if expected_status and fields.get("status") != expected_status:
        errors.append(f"phase {args.phase} requires status: {expected_status}")
    if args.phase == "review" and fields.get("status") not in {"in_review", "approved"}:
        errors.append("review phase requires status: in_review or approved")
    if args.phase == "implemented" and document_type != "tdd":
        errors.append("implemented phase is valid only for a TDD")

    cleaned = semantic_text(text)
    if args.phase != "draft" and document_type in REQUIRED:
        revision_error = run_revision_check(args.path)
        if revision_error:
            errors.append(revision_error)
        unresolved = sorted(token for token in template_placeholders(document_type) if token in cleaned)
        if unresolved:
            errors.append("unresolved template placeholders: " + ", ".join(unresolved[:8]))
        if "YYYY-MM-DD" in cleaned or "STEP-XX" in cleaned or "[TODO" in cleaned:
            errors.append("unresolved template sentinel found")

    if args.phase in {"approved", "implemented"}:
        if open_blocker_exists(text):
            errors.append("open BLOCKER remains")
        if "- [ ]" in cleaned:
            errors.append("unchecked readiness/completion item remains")

    if document_type == "tdd" and args.phase in {"approved", "implemented"}:
        if not DIGEST_RE.fullmatch(fields.get("related_prd_revision", "")):
            errors.append("related_prd_revision must be sha256 plus 64 lowercase hex characters")
        repository_revision = fields.get("repository_revision", "")
        if not (GIT_REVISION_RE.fullmatch(repository_revision) or repository_revision.startswith("non-git:")):
            errors.append("repository_revision must be a Git SHA or an explicit non-git immutable revision")

    if args.phase != "draft" and fields.get("content_revision") and not DIGEST_RE.fullmatch(fields["content_revision"]):
        errors.append("content_revision must be sha256 plus 64 lowercase hex characters")
    if args.phase == "implemented" and "Implementation completion gate" not in headings(text):
        errors.append("implemented TDD is missing the completion gate")

    if errors:
        for error in dict.fromkeys(errors):
            print(f"validation error: {error}", file=sys.stderr)
        return 1

    print(f"valid {document_type} ({args.phase}): {args.path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

