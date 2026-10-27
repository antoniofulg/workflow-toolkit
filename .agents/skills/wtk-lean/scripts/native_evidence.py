"""Structural native approval evidence shared by the pre-build and completion gates."""

import os
import re


EMPTY_VALUES = {
    "", "-", "—", "–", "none", "n/a", "na", "nothing", "pending", "unresolved",
    "user decision", "actual user decision", "reviewed revision", "revision",
    "scope", "authorized scope", "source", "date",
}


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
        and not re.search(r"<[^>]*>|^\[[^\]]*\]$|\b(?:TODO|TBD)\b|^placeholder\b", value, re.I)
        and not re.match(r"(?:template|example|sample)\b", value, re.I)
    )


def approval_errors(checks_path):
    """The sibling plan owns approval when present; otherwise checks own bounded intent."""
    plan_path = os.path.join(os.path.dirname(os.path.abspath(checks_path)), "plan.md")
    path = plan_path if os.path.isfile(plan_path) else checks_path
    label = os.path.basename(path)
    if not os.path.isfile(path):
        return [f"{label}: missing native approval contract - recover the actual user decision"]
    with open(path, encoding="utf-8") as source:
        lines = unfenced_lines(source.read())
    fields, active = {}, False
    intent = []
    in_intent = False
    for line in lines:
        heading = re.match(r"^#{1,2}\s+(.+?)\s*$", line)
        if heading:
            active = heading[1].lower() == "approval"
            in_intent = heading[1].lower() == "intent"
        elif active:
            if re.match(r"^\s*(?:example|template|sample)\s*:", line, re.I):
                return [f"{label}: approval is a template/example - recover the actual user decision"]
            match = re.match(r"^\s*[-*]\s+(Decision|Date|Source|Reviewed revision|Scope):\s*(.*?)\s*$", line, re.I)
            if match:
                key = match[1].lower()
                if key in fields:
                    return [f"{label}: approval has duplicate {match[1]} fields - retain one observed receipt"]
                fields[key] = match[2]
        elif in_intent:
            intent.append(line)
    errors = []
    for key in ("decision", "reviewed revision", "scope"):
        if not usable_value(fields.get(key, "")):
            errors.append(f"{label}: approval missing usable {key} - record the actual user decision/source, reviewed revision and scope in ## Approval")
    if not any(usable_value(fields.get(key, "")) for key in ("source", "date")):
        errors.append(f"{label}: approval missing usable Source or Date - cite the observed user decision, not execution settings or an example")
    if path == checks_path and not usable_value(" ".join(intent)):
        errors.append("checks.md: checks-only approval requires usable ## Intent beside its receipt; do not create a synthetic plan")
    return errors
