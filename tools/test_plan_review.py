"""Contract tests for the wtk-plan-review skill: findings validator and owned instruction rules."""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKILLS = ROOT / ".agents/skills"
VALIDATOR = SKILLS / "wtk-plan-review/scripts/validate_findings.py"

KEYS = ("schema_version", "review_kind", "round", "readiness", "reviewer", "generated_at")
HEADINGS = ("# Summary", "# Blockers", "# Nits", "# Evidence", "# Deferred Or Follow-Up")
BLOCKER = "## B-001 - Door has a live alternative\n\n- Section: Landing\n- Issue: the shape is not final.\n"
NIT = "## N-001 - Vague title\n\n- Section: Flow\n- Issue: unclear hop.\n"


def findings(
    *, readiness: str = "BLOCKED", round_: int = 1, blockers: str = BLOCKER, nits: str = "None.",
    drop_key: str | None = None, drop_heading: str | None = None, extra: str = "",
) -> str:
    values = {
        "schema_version": "1", "review_kind": "plan", "round": str(round_), "readiness": readiness,
        "reviewer": "claude-opus", "generated_at": "2026-11-12T10:00:00Z",
    }
    front = "\n".join(f"{key}: {values[key]}" for key in KEYS if key != drop_key)
    sections = {
        "# Summary": "Two sentences explaining the verdict.",
        "# Blockers": blockers,
        "# Nits": nits,
        "# Evidence": "plan.md read in full.",
        "# Deferred Or Follow-Up": "None.",
    }
    body = "\n\n".join(f"{heading}\n\n{text}" for heading, text in sections.items() if heading != drop_heading)
    return f"---\n{front}\n---\n\n{body}\n{extra}"


def validate(content: str | None, *args: str, round_: str = "1") -> subprocess.CompletedProcess[str]:
    with tempfile.TemporaryDirectory() as tmp:
        path = Path(tmp) / "review-findings.md"
        if content is not None:
            path.write_text(content, encoding="utf-8")
        return subprocess.run(
            [sys.executable, str(VALIDATOR), "--round", round_, *args, str(path)],
            capture_output=True, text=True,
        )


def output(result: subprocess.CompletedProcess[str]) -> str:
    return result.stdout + result.stderr


def test_validator_accepts_valid_findings() -> None:
    for readiness, blockers in (("READY", "None."), ("BLOCKED", BLOCKER), ("NEEDS_REWORK", BLOCKER)):
        for nits in ("None.", NIT):
            result = validate(findings(readiness=readiness, blockers=blockers, nits=nits))
            assert result.returncode == 0, f"{readiness}: {output(result)}"


def test_validator_rejects_missing_or_empty_file() -> None:
    missing = validate(None)
    assert missing.returncode == 1 and "review-findings.md" in output(missing)
    empty = validate("")
    assert empty.returncode == 1 and "review-findings.md" in output(empty)


def test_validator_names_each_missing_element() -> None:
    for key in KEYS:
        result = validate(findings(drop_key=key))
        assert result.returncode == 1 and key in output(result), f"{key}: {output(result)}"
    for heading in HEADINGS:
        result = validate(findings(drop_heading=heading))
        assert result.returncode == 1 and heading in output(result), f"{heading}: {output(result)}"


def test_validator_rejects_bad_readiness_and_round() -> None:
    bad = validate(findings(readiness="MAYBE"))
    assert bad.returncode == 1 and "readiness" in output(bad)
    wrong_round = validate(findings(round_=2), round_="1")
    assert wrong_round.returncode == 1 and "round is 2, expected 1" in output(wrong_round)


def test_validator_rejects_empty_item_section() -> None:
    for blockers, nits, section in (("Nothing to report.", "None.", "# Blockers"), ("None.", "Looks fine.", "# Nits")):
        result = validate(findings(readiness="NEEDS_REWORK", blockers=blockers, nits=nits))
        assert result.returncode == 1 and section in output(result), f"{section}: {output(result)}"
    wrong_prefix = validate(findings(readiness="BLOCKED", blockers="None.", nits=BLOCKER))
    assert wrong_prefix.returncode == 1 and "# Nits" in output(wrong_prefix)


def test_validator_rejects_ready_with_blocker() -> None:
    result = validate(findings(readiness="READY", blockers=BLOCKER))
    assert result.returncode == 1 and "READY" in output(result)


def test_validator_rejects_placeholder_words() -> None:
    for word in ("TBD", "TODO", "PLACEHOLDER"):
        result = validate(findings(readiness="READY", blockers="None.", extra=f"\nOpen: {word} later.\n"))
        assert result.returncode == 1 and word in output(result), f"{word}: {output(result)}"
    contained = validate(findings(readiness="READY", blockers="None.", extra="\nSee TBDX, TODOS, PLACEHOLDERS and MYTODO.\n"))
    assert contained.returncode == 0, output(contained)


def test_validator_argument_errors_exit_2() -> None:
    def run(*args: str) -> int:
        return subprocess.run([sys.executable, str(VALIDATOR), *args], capture_output=True, text=True).returncode

    assert run("--round", "1") == 2
    assert run("some-path.md") == 2
    assert run("--round", "0", "some-path.md") == 2
    assert run("--round", "x", "some-path.md") == 2
    assert run("--round", "-1", "some-path.md") == 2


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("-k", dest="pattern")
    pattern = parser.parse_args().pattern
    tests = [
        function for name, function in sorted(globals().items())
        if name.startswith("test_") and (pattern is None or pattern in name)
    ]
    if not tests:
        raise SystemExit(f"no tests matched: {pattern}")
    for function in tests:
        function()
    print(f"{len(tests)} passed, 0 failed")
