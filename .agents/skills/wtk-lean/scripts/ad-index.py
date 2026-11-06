#!/usr/bin/env python3
"""Regenerate `.specs/AD-INDEX.md` from `.specs/STATE.md`.

One line per AD-NNN. Agents load the index, not the log.

  python3 .agents/skills/wtk-lean/scripts/ad-index.py          write the index
  python3 .agents/skills/wtk-lean/scripts/ad-index.py --check  exit 1 if the index is stale
  --root PATH                                                project root (default: the installing project)
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]

AD_ID = re.compile(r"^AD-\d+$")
CELL_SPLIT = re.compile(r"(?<!\\)\|")


def first_sentence(text: str, limit: int = 140) -> str:
    collapsed = re.sub(r"\s+", " ", text.replace("**", "")).strip()
    cut = collapsed.find(". ")
    sentence = collapsed[: cut + 1] if cut != -1 else collapsed
    if len(sentence) > limit:
        return sentence[: limit - 1].rstrip() + "…"
    return sentence


def cells(line: str) -> list[str]:
    parts = CELL_SPLIT.split(line.strip())[1:-1]
    return [part.strip().replace("\\|", "|") for part in parts]


def parse(state: str) -> list[tuple[int, str, str, str]]:
    """Read every `| AD-NNN | ... |` row of a table whose header names ID, Decision and Status."""
    rows: list[tuple[int, str, str, str]] = []
    columns: dict[str, int] | None = None
    for line in state.splitlines():
        if not line.lstrip().startswith("|"):
            columns = None
            continue
        row = cells(line)
        names = [cell.lower() for cell in row]
        if {"id", "decision", "status"} <= set(names):
            columns = {name: names.index(name) for name in ("id", "decision", "status")}
            continue
        if columns is None or len(row) <= max(columns.values()):
            continue
        ident = row[columns["id"]].strip("`")
        if not AD_ID.match(ident):
            continue
        status = row[columns["status"]] or "active"
        rows.append((int(ident.split("-")[1]), ident, first_sentence(row[columns["decision"]]), status))
    rows.sort(key=lambda row: row[0])
    return rows


def render(rows: list[tuple[int, str, str, str]]) -> str:
    lines = [
        "# Project decision index",
        "",
        "One line per `AD-NNN`. The append-only log lives in `.specs/STATE.md`.",
        "",
        "Row: `rg '^\\| AD-NNN ' .specs/STATE.md`. Resume: `rg -A 20 '^## Handoff' .specs/STATE.md`.",
        "When recording an `AD-NNN`, run the bundled wtk-lean ad-index.py in the same commit.",
        "",
        "| ID | Status | Decision |",
        "| --- | --- | --- |",
    ]
    for _number, ident, decision, status in rows:
        escaped = decision.replace("|", "\\|")
        lines.append(f"| `{ident}` | {status} | {escaped} |")
    lines.append("")
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description="Regenerate .specs/AD-INDEX.md from .specs/STATE.md.")
    parser.add_argument("--root", type=Path, default=ROOT, help="project root (default: the installing project)")
    parser.add_argument("--check", action="store_true", help="exit 1 if the index is stale")
    args = parser.parse_args()
    root = args.root.resolve()
    state = root / ".specs" / "STATE.md"
    index = root / ".specs" / "AD-INDEX.md"
    if not state.is_file():
        print(f"missing {state}", file=sys.stderr)
        return 1
    text = render(parse(state.read_text()))
    if args.check:
        current = index.read_text() if index.is_file() else ""
        if current != text:
            print("stale .specs/AD-INDEX.md; run the bundled wtk-lean ad-index.py", file=sys.stderr)
            return 1
        print("AD-INDEX.md up to date")
        return 0
    index.write_text(text, encoding="utf-8")
    print(f"wrote {index.relative_to(root)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
