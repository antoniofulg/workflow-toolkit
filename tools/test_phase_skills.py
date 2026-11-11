"""Contract tests for the Workflow Toolkit skill collection and role packets."""

from __future__ import annotations

import argparse
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKILLS = ROOT / ".agents/skills"
PUBLIC = (
    "wtk", "wtk-deep-review", "wtk-discover", "wtk-implement", "wtk-knowledge-check",
    "wtk-lean", "wtk-plan", "wtk-qa", "wtk-qa-execute", "wtk-qa-plan",
    "wtk-reuse-review", "wtk-ship", "wtk-test-audit", "wtk-test-review",
)


def frontmatter(path: Path) -> dict[str, str]:
    lines = path.read_text(encoding="utf-8").splitlines()
    assert lines and lines[0] == "---", f"{path} has no frontmatter"
    end = lines.index("---", 1)
    return {key.strip(): value.strip() for key, _, value in (line.partition(":") for line in lines[1:end])}


def blocks(relative: str) -> list[str]:
    """Logical lines of a skill file: a list item or paragraph joined with its continuation lines."""
    out: list[str] = []
    start_new = True
    for line in (SKILLS / relative).read_text(encoding="utf-8").splitlines():
        if not line.strip():
            start_new = True
        elif start_new or line.startswith(("- ", "|", "#", "```")):
            out.append(line.strip())
            start_new = line.startswith(("|", "#", "```"))
        else:
            out[-1] += " " + line.strip()
    return out


def owns(relative: str, *fragments: str) -> bool:
    """True when one logical line of the file carries every fragment: the rule sits where it is owned."""
    return any(all(fragment in block for fragment in fragments) for block in blocks(relative))

UIUX = "wtk/references/ui-ux.md"


def test_public_skill_contracts() -> None:
    for name in PUBLIC:
        path = SKILLS / name / "SKILL.md"
        assert path.is_file(), f"missing public skill {name}"
        fields = frontmatter(path)
        assert fields.get("name") == name
        assert fields.get("description", "").strip(), f"{name}: missing description"
        assert len(fields["description"]) <= 1024
    for old in ("workflow-spec-driven", "wspecify", "wdesign", "wtasks", "wimplement", "wverify", "wqa", "wreview"):
        assert not (SKILLS / old).exists(), f"obsolete skill remains: {old}"


def test_router_is_thin_and_on_demand() -> None:
    router = (SKILLS / "wtk/SKILL.md").read_text(encoding="utf-8")
    assert len(router.splitlines()) <= 150
    assert "wtk-lean" in router and "wtk-discover" in router
    assert "wtk-deep-review" in router and "wtk-qa" in router and "wtk-ship" in router
    assert "references/security.md" in router and "references/ui-ux.md" in router
    assert "Do not preload quality, UI, security" in router
    assert "A diagnosis with no unresolved product or architecture choice" in router
    assert "route to discovery merely because the cause is unknown" in router
    assert not re.search(r"workflow-spec-driven|/wspecify|/wtasks|/wimplement|/wverify", router)


def test_artifact_contracts_remain_distinct() -> None:
    discover = (SKILLS / "wtk-discover/SKILL.md").read_text(encoding="utf-8")
    plan = (SKILLS / "wtk-plan/SKILL.md").read_text(encoding="utf-8")
    implement = (SKILLS / "wtk-implement/SKILL.md").read_text(encoding="utf-8")
    lean = (SKILLS / "wtk-lean/SKILL.md").read_text(encoding="utf-8")
    assert ".design/<name>.md" in discover
    assert "organised by **vertical slice**" in discover
    assert ".tasks/<name>.md" in plan
    assert ".checks/<feature>.md" in implement
    assert ".specs/features/<feature>/plan.md" in lean or ".specs/features/<feature>/plan.md" in (SKILLS / "wtk/SKILL.md").read_text(encoding="utf-8")
    assert ".specs/features/<feature>/plan.md" not in plan
    assert ".specs/features/<feature>/plan.md" not in implement
    assert "whole slices" in lean and "fresh Verifier" in lean
    assert "A build agent never spawns another agent at all" in implement


def test_project_owned_route_is_frozen_and_native_files_are_preserved() -> None:
    route = SKILLS / "wtk-lean/scripts/workflow_route.py"
    assert route.is_file()
    text = route.read_text(encoding="utf-8")
    assert "workflow.json" in text
    assert ".wtk.toml" not in text
    guidance = SKILLS / "wtk/references/agent-selection.md"
    assert guidance.is_file()
    for relative in (
        "wtk/SKILL.md", "wtk-lean/SKILL.md", "wtk-lean/references/build.md",
        "wtk-lean/references/verify.md", "wtk-implement/SKILL.md",
        "wtk-implement/references/verify.md", "wtk-deep-review/SKILL.md",
        "wtk-deep-review/references/orchestration.md", "wtk-deep-review/references/subagent-runtimes.md",
        "wtk/references/context-handoff.md", "wtk/references/git.md",
        "wtk/references/review-rounds.md", "wtk-qa/SKILL.md", "wtk-qa-plan/SKILL.md",
        "wtk-qa-execute/SKILL.md", "wtk-qa-execute/references/qa-execution.md", "wtk-ship/SKILL.md",
    ):
        path = SKILLS / relative
        source = path.read_text(encoding="utf-8")
        links = re.findall(r"\[[^\]]+\]\(([^)#]*agent-selection\.md)(?:#[^)]*)?\)", source)
        assert links and all((path.parent / target).resolve() == guidance.resolve() for target in links), relative
        assert "--native-provider" not in source and "agent_file" not in source, relative
    qa = frontmatter(SKILLS / "wtk-qa/SKILL.md")
    assert "agent" not in qa and qa.get("context") != "fork"


def test_router_references_resolve() -> None:
    router = SKILLS / "wtk"
    text = (router / "SKILL.md").read_text(encoding="utf-8")
    links = re.findall(r"\[[^\]]+\]\((references/[^)#]+)(?:#[^)]*)?\)", text)
    assert links, "router must expose its shared references"
    for target in links:
        assert (router / target).is_file(), f"missing router reference: {target}"
    for token in re.findall(r"(?:\.agents/skills/)?[\w./-]+/scripts/[\w-]+\.py", text):
        assert (ROOT / token.lstrip("./")).is_file(), f"{router}: missing {token}"


def test_screens_judge_inputs_exclude_code() -> None:
    assert owns(UIUX, "**Dispatch:**", "fresh screens judge", "same turn as the Verifier")
    assert owns(UIUX, "**Inputs:**", "binding captures", "<capture>.running.png", "listed departures",
                "never source, diff or handoff")
    for relative in ("wtk-lean/references/verify.md", "wtk-implement/references/screens.md"):
        path = SKILLS / relative
        links = re.findall(r"\]\(([^)#]*ui-ux\.md)#screens-judge-ui\)", path.read_text(encoding="utf-8"))
        assert links and all((path.parent / target).resolve() == (SKILLS / UIUX).resolve() for target in links), relative


def test_screens_report_schema_is_defined() -> None:
    assert owns(UIUX, "**Round**: 1")
    assert owns(UIUX, "**HEAD**: <short sha")
    assert owns(UIUX, "| Screen | Compared with | Verdict | Finding |")
    assert owns(UIUX, "| Element | Result | Picture draws |")
    assert owns(UIUX, "`differs` categories", "`controls`", "`arrangement`", "`copy`", "`drawing`", "`render`")
    assert owns(UIUX, "**Verdict:**", "`diverges`", "`matches`")


def test_screens_resized_tell_is_defined() -> None:
    assert owns(UIUX, "**Resized:**", "reads smaller in the picture", "`differs - resized`")


def test_screens_second_round_is_bounded() -> None:
    assert owns(UIUX, "**Round 2:**", "reopens only the `differs` rows", "`differs - regression`",
                "There is no round 3")


def test_ui_and_delivery_boundaries_stay_local() -> None:
    uiux = (ROOT / ".agents/skills/wtk/references/ui-ux.md").read_text(encoding="utf-8")
    ship = (SKILLS / "wtk-ship/SKILL.md").read_text(encoding="utf-8")
    assert "uiux.md" in uiux and "written in Specify" in uiux
    assert "close_feature.py" in ship
    assert "feature branch push, one pull request, and merge" in ship
    assert re.search(r"deploy", ship, re.IGNORECASE)
    assert "force-push" in ship and "direct push to `main`" in ship


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
