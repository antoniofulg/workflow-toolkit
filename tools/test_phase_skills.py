"""Contract tests for the Workflow Toolkit skill collection and role packets."""

from __future__ import annotations

import re
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKILLS = ROOT / ".agents/skills"
PUBLIC = (
    "wtk", "wtk-deep-review", "wtk-discover", "wtk-implement", "wtk-knowledge-check",
    "wtk-lean", "wtk-plan", "wtk-qa", "wtk-qa-execute", "wtk-qa-plan",
    "wtk-reuse-review", "wtk-ship",
)


def frontmatter(path: Path) -> dict[str, str]:
    lines = path.read_text(encoding="utf-8").splitlines()
    assert lines and lines[0] == "---", f"{path} has no frontmatter"
    end = lines.index("---", 1)
    return {key.strip(): value.strip() for key, _, value in (line.partition(":") for line in lines[1:end])}


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
    assert ".tasks/<name>.md" in plan
    assert ".checks/<feature>.md" in implement
    assert ".specs/features/<feature>/plan.md" in lean or ".specs/features/<feature>/plan.md" in (SKILLS / "wtk/SKILL.md").read_text(encoding="utf-8")
    assert ".specs/features/<feature>/plan.md" not in plan
    assert ".specs/features/<feature>/plan.md" not in implement
    assert "whole slices" in lean and "fresh Verifier" in lean


def test_native_route_owns_snapshots_without_config() -> None:
    route = SKILLS / "wtk-lean/scripts/workflow_route.py"
    assert route.is_file()
    text = route.read_text(encoding="utf-8")
    assert "native_provider" in text and "workflow.json" in text
    assert ".wtk.toml" not in text
    assert "model" not in text and "effort" not in text


def test_router_references_resolve() -> None:
    router = SKILLS / "wtk"
    text = (router / "SKILL.md").read_text(encoding="utf-8")
    links = re.findall(r"\[[^\]]+\]\((references/[^)#]+)(?:#[^)]*)?\)", text)
    assert links, "router must expose its shared references"
    for target in links:
        assert (router / target).is_file(), f"missing router reference: {target}"
    for token in re.findall(r"(?:\.agents/skills/)?[\w./-]+/scripts/[\w-]+\.py", text):
        assert (ROOT / token.lstrip("./")).is_file(), f"{router}: missing {token}"


def test_repository_intelligence_order_is_bounded() -> None:
    text = (ROOT / "docs/toolkit/repository-intelligence.md").read_text(encoding="utf-8")
    assert text.index("query Graphify first") < text.index("query Graft before broad native search")
    assert text.index("one degraded reason") < text.index("Generated graphs")
    assert "Existing file, symbol, API, caller, and callee pointers" in text


def test_ui_and_delivery_boundaries_stay_local() -> None:
    uiux = (ROOT / ".agents/skills/wtk/references/ui-ux.md").read_text(encoding="utf-8")
    ship = (SKILLS / "wtk-ship/SKILL.md").read_text(encoding="utf-8")
    assert "uiux.md" in uiux and "written in Specify" in uiux
    assert "close_feature.py" in ship
    assert "feature branch push, one pull request, and merge" in ship
    assert re.search(r"deploy", ship, re.IGNORECASE)
    assert "force-push" in ship and "direct push to `main`" in ship


def test_direct_script_execution_reports_success() -> None:
    result = subprocess.run(["python3", str(ROOT / "tools/test_wtk_forward.py")], cwd=ROOT, text=True, capture_output=True)
    assert result.returncode == 0, result.stderr


if __name__ == "__main__":
    tests = [function for name, function in sorted(globals().items()) if name.startswith("test_")]
    for function in tests:
        function()
    print(f"{len(tests)} passed, 0 failed")
