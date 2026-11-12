"""Contract tests for the wtk-plan-review skill: findings validator and owned instruction rules."""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
import tempfile
from pathlib import Path

from test_phase_skills import ROOT, SKILLS, owns

SKILL = "wtk-plan-review/SKILL.md"
PROMPT = "wtk-plan-review/references/reviewer-prompt.md"
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


def test_skill_asks_for_reviewers() -> None:
    assert owns(SKILL, "list the reviewers the host can dispatch", "pick one or more", "before any dispatch")
    assert owns(SKILL, "no resolvable `plan.md`", "`no plan found`", "dispatch nothing")


def test_skill_dispatches_named_reviewers() -> None:
    assert owns(SKILL, "Reviewers named in the request", "dispatched without asking")


def test_skill_never_substitutes_reviewer() -> None:
    assert owns(SKILL, "cannot dispatch", "is named", "never substitute another reviewer")


def test_prompt_scopes_reviewer() -> None:
    assert owns(SKILL, "Dispatch each reviewer as a fresh session that did not author the plan")
    assert owns(SKILL, "writes only `.wtk-plan-review/<feature>/round<N>-<reviewer>.md`")
    prompt = (SKILLS / PROMPT).read_text(encoding="utf-8")
    for fragment in ("{plan_path}", "{checks_path}", "`## Sources`", "exactly one file, `{findings_path}`"):
        assert fragment in prompt, fragment
    assert owns(PROMPT, "Checks, when present")


def test_prompt_template_passes_validator() -> None:
    prompt = (SKILLS / PROMPT).read_text(encoding="utf-8")
    template = re.search(r"```\n(---\n.*?)```", prompt, re.DOTALL).group(1)
    filled = template.replace("{round}", "1").replace("{reviewer}", "claude-opus")
    filled = filled.replace("READY|BLOCKED|NEEDS_REWORK", "READY").replace("<ISO-8601 timestamp>", "2026-11-12T10:00:00Z")
    result = validate(filled)
    assert result.returncode == 0, output(result)


def test_skill_reports_incomplete_review() -> None:
    assert owns(SKILL, "validate_findings.py --round <N> <file>", "on each file")
    assert owns(SKILL, "missing or invalid file is an incomplete review", "never `ready`")
    assert owns(SKILL, "`incomplete review` when any file failed", "`ready` only when every file is valid")


def test_prompt_targets_plan_shape() -> None:
    assert owns(PROMPT, "`Flow`", "`Impact`", "`Relations`", "`Surface`", "`Landing`", "`Out of scope`")
    assert owns(PROMPT, "DO NOT report what `validate_plan.py` already rejects")


def test_skill_merges_and_applies_selected_only() -> None:
    assert owns(SKILL, "one merged list", "tagged `<reviewer> B-001`")
    assert owns(SKILL, "Edit `plan.md` only for the selected items")


def test_skill_writes_disposition() -> None:
    assert owns(SKILL, "round<N>-disposition.md", "| Finding | Reviewer | Disposition | Changed |")
    assert owns(SKILL, "one row per finding", "`applied`", "`declined - <reason>`")


def test_skill_rounds_opt_in_and_no_approval() -> None:
    assert owns(SKILL, "Run another round only when the user asks", "the changed plan", "the prior findings", "the disposition")
    assert owns(SKILL, "never writes the plan's `## Approval` receipt")


LEAN_PLAN = "wtk-lean/references/plan.md"


def test_lean_plan_offers_review_on_triggers() -> None:
    assert owns(
        LEAN_PLAN, "offering", "wtk-plan-review", "one line", "naming the triggers that hold",
        "`Landing` door with a live alternative", "`Relations` changes data that already exists",
        "`Surface` changes an interface already consumed", "security surface declared at Specify",
    )


def test_lean_plan_no_offer_without_trigger() -> None:
    assert owns(LEAN_PLAN, "With no trigger, or for a checks-only feature, offer nothing")


def test_lean_plan_offer_adds_no_stop() -> None:
    assert owns(LEAN_PLAN, "The offer adds no stop", "one answer may decline the review and approve the plan")


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
