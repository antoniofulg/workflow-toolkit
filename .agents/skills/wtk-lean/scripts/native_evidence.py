"""Structural helpers shared by the pre-build and completion gates."""

import os
import re


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
