"""Structural helpers shared by the pre-build and completion gates."""

import os
import re


RUN_RE = re.compile(r"^\**\s*Run\s+([\w-]+)\s*\**\s*:\s*(.+)$", re.IGNORECASE)
RUN_PROOF_RE = re.compile(r"^run\s+([\w-]+)\s*\|\s*(.*)$", re.IGNORECASE)
EMPTY_VALUES = {"", "-", "—", "–", "none", "n/a", "na", "nothing", "pending", "unresolved"}


def unfenced_lines(text):
    """Preserve line positions while excluding backtick and tilde fenced examples."""
    lines, fence = [], None
    for line in text.splitlines():
        match = re.match(r"^\s*(`{3,}|~{3,})", line)
        if fence:
            if match and match[1][0] == fence[0] and len(match[1]) >= len(fence):
                fence = None
            lines.append("")
        elif match:
            fence = match[1]
            lines.append("")
        else:
            lines.append(line)
    return lines


def usable_value(value):
    value = value.strip().strip("`*").strip()
    return (
        value.lower() not in EMPTY_VALUES
        and not re.fullmatch(r"[\s.…?_\-–—]+", value)
        and not re.search(r"<[^>]*>|^\[[^\]]*\]$|\b(?:TODO|TBD)\b|^placeholder\b", value, re.I)
        and not re.match(r"(?:template|example|sample)\b", value, re.I)
    )


def intent_errors(checks_path):
    """Checks-only work (no sibling plan) keeps its bounded intent in checks.md."""
    plan_path = os.path.join(os.path.dirname(os.path.abspath(checks_path)), "plan.md")
    if os.path.isfile(plan_path) or not os.path.isfile(checks_path):
        return []
    with open(checks_path, encoding="utf-8") as source:
        lines = unfenced_lines(source.read())
    intent, in_intent = [], False
    for line in lines:
        heading = re.match(r"^(#{1,6})\s+(.+?)\s*#*\s*$", line)
        if heading and len(heading[1]) <= 2:
            in_intent = heading[2].lower() == "intent"
        elif in_intent:
            intent.append(line)
    if usable_value(" ".join(intent)):
        return []
    return ["checks.md: checks-only work requires usable ## Intent; do not create a synthetic plan"]


APPROVAL_DECISION_RE = re.compile(r"^\s*[-*]\s*\**Decision\**\s*:\s*(.*)$", re.IGNORECASE)


def approval_errors(checks_path):
    """The native approval receipt is gated on presence: `## Approval` with a usable `- Decision:`.

    It lives in plan.md, or beside `## Intent` in checks.md when there is no plan. The chat that
    held the approval does not survive a compaction, so a resumed builder finds it here or stops.
    Whether the decision names who approved which revision stays the Verifier's judgment.
    """
    folder = os.path.dirname(os.path.abspath(checks_path))
    plan_path = os.path.join(folder, "plan.md")
    owner = plan_path if os.path.isfile(plan_path) else checks_path
    if not os.path.isfile(owner):
        return []
    with open(owner, encoding="utf-8") as source:
        lines = unfenced_lines(source.read())
    in_approval, decision = False, ""
    for line in lines:
        heading = re.match(r"^(#{1,6})\s+(.+?)\s*#*\s*$", line)
        if heading and len(heading[1]) <= 2:
            in_approval = heading[2].lower() == "approval"
        elif in_approval:
            match = APPROVAL_DECISION_RE.match(line)
            if match:
                decision = match[1]
    if usable_value(decision):
        return []
    return [
        f"{os.path.basename(owner)}: no `## Approval` receipt with a non-empty `- Decision:` line - "
        "record the user's actual decision before checks or code; never write the approval yourself"
    ]


def unquote(text):
    return text.strip().strip("`").strip()


def read_runs(lines):
    """{name: command} for every `Run <name>: <command>` line outside fenced blocks."""
    runs = {}
    for line in lines:
        match = RUN_RE.match(line.strip())
        if match:
            runs[match[1]] = unquote(match[2])
    return runs
