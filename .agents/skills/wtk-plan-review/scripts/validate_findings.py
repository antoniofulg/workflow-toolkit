#!/usr/bin/env python3
"""
validate_findings.py - deterministic gate for one plan peer-review findings file.

A review that is missing, malformed or self-contradictory must read as an incomplete review,
never as READY. Standard library only; reads the file and never writes.

Usage:
  python3 <skill-dir>/scripts/validate_findings.py --round N <findings-file>

Exit 0 valid; 1 the file is missing or has defects (each printed, naming its element);
2 bad arguments.
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

READINESS = ("READY", "BLOCKED", "NEEDS_REWORK")
KEYS = ("schema_version", "review_kind", "round", "readiness", "reviewer", "generated_at")
HEADINGS = ("# Summary", "# Blockers", "# Nits", "# Evidence", "# Deferred Or Follow-Up")
ITEM_SECTIONS = (("# Blockers", "B"), ("# Nits", "N"))
TIMESTAMP = re.compile(r"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(?:\.\d+)?(?:Z|[+-]\d{2}:?\d{2})")
PLACEHOLDER = re.compile(r"(?<![A-Za-z0-9_])(TBD|TODO|PLACEHOLDER)(?![A-Za-z0-9_])")


def positive_int(text: str) -> int:
    if not re.fullmatch(r"[0-9]+", text) or int(text) < 1:
        raise argparse.ArgumentTypeError(f"must be a positive integer: {text!r}")
    return int(text)


def split_frontmatter(lines: list[str]) -> tuple[dict[str, str], list[str]] | None:
    if not lines or lines[0].rstrip() != "---":
        return None
    for end in range(1, len(lines)):
        if lines[end].rstrip() == "---":
            pairs = (line.partition(":") for line in lines[1:end])
            return {key.strip(): value.strip() for key, _, value in pairs}, lines[end + 1:]
    return None


def section(body: list[str], heading: str) -> list[str] | None:
    """Lines under a level-1 heading, up to the next one; None when the heading is absent."""
    for start, line in enumerate(body):
        if line.rstrip() == heading:
            rest = body[start + 1:]
            return rest[:next((i for i, text in enumerate(rest) if text.startswith("# ")), len(rest))]
    return None


def defects(text: str, round_number: int) -> list[str]:
    parsed = split_frontmatter(text.splitlines())
    if parsed is None:
        return ["missing or unclosed frontmatter"]
    front, body = parsed
    found: list[str] = [f"missing frontmatter key: {key}" for key in KEYS if not front.get(key)]
    if front.get("schema_version") and front["schema_version"] != "1":
        found.append(f"schema_version must be 1, got {front['schema_version']}")
    if front.get("review_kind") and front["review_kind"] != "plan":
        found.append(f"review_kind must be plan, got {front['review_kind']}")
    if front.get("round") and front["round"] != str(round_number):
        found.append(f"round is {front['round']}, expected {round_number}")
    if front.get("readiness") and front["readiness"] not in READINESS:
        found.append(f"readiness must be one of {', '.join(READINESS)}, got {front['readiness']}")
    if front.get("generated_at") and not TIMESTAMP.fullmatch(front["generated_at"]):
        found.append(f"generated_at is not an ISO-8601 timestamp: {front['generated_at']}")
    for heading in HEADINGS:
        if section(body, heading) is None:
            found.append(f"missing heading: {heading}")
    blockers = False
    for heading, prefix in ITEM_SECTIONS:
        lines = section(body, heading)
        if lines is None:
            continue
        items = [line for line in lines if re.match(rf"## {prefix}-\d{{3}} - \S", line)]
        if heading == "# Blockers":
            blockers = bool(items)
        if not items and not any(line.strip() == "None." for line in lines):
            found.append(f"section {heading} must hold None. or at least one {prefix}-NNN item")
    readiness = front.get("readiness")
    if readiness == "READY" and blockers:
        found.append("readiness is READY but # Blockers holds an item")
    if readiness in ("BLOCKED", "NEEDS_REWORK") and not blockers:
        found.append(f"readiness is {readiness} but # Blockers holds no item")
    found.extend(f"placeholder word: {word}" for word in sorted(set(PLACEHOLDER.findall(text))))
    return found


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--round", dest="round_number", type=positive_int, required=True)
    parser.add_argument("path", type=Path)
    args = parser.parse_args(argv)
    try:
        text = args.path.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError):
        text = ""
    if not text.strip():
        print(f"findings file missing or empty: {args.path}", file=sys.stderr)
        return 1
    problems = defects(text, args.round_number)
    for problem in problems:
        print(f"{args.path}: {problem}", file=sys.stderr)
    if problems:
        return 1
    print(f"findings valid: {args.path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
