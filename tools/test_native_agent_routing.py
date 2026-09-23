"""Contract tests for project-owned native agent routing."""

from __future__ import annotations

import hashlib
import importlib.util
import json
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
ROUTE_PATH = ROOT / ".agents/skills/wtk-lean/scripts/workflow_route.py"
NATIVE_HASHES = {
    ".claude/agents/deep-reviewer.md": "982a0b1420967d3814043bfe53e332c386bdf4460375288973e789ef60d61683",
    ".claude/agents/designer.md": "814cce3730dd0da24a8f1880c1e7f14d644a478958f86418586bbc3162a093dc",
    ".claude/agents/explorer.md": "ddfa0534658a94e9577a4ae24100a656bd756cdf4b094f00a9b3eb47c255b1b1",
    ".claude/agents/implementer.md": "d376456d93913a682526f43d000a533487a0025d408f8e018c723e11422ad473",
    ".claude/agents/planner.md": "355e2d29320c05bd76ed433803027ff9d09c33e578022e99c37ade18bce518c8",
    ".claude/agents/verifier.md": "c70f3025b40faec2decfeb41da31f712cf38bcec1dd1516e76a50a75a6bc8813",
    ".codex/agents/deep-reviewer.toml": "5dd24a0ab2c533982911d445dcd31ea334a51961d11f7382e7adeb3b9ca5ef47",
    ".codex/agents/designer.toml": "65eab5a92ea72c70b8ffe66e0839d8e67450027e593343dd536154c71c5d5611",
    ".codex/agents/explorer.toml": "2df294eec16919bab1b4e54f7638e812b363a7e47ddcc8e81efca56689050a11",
    ".codex/agents/implementer.toml": "b9d2daa1727ff6a9354384056e98ecf14deada654bdbba6294538262029ecdfd",
    ".codex/agents/planner.toml": "49b41840fea8704b4c5783c72489e9138055b63c8ad8d6b93c67fa7c5f6f9b78",
    ".codex/agents/verifier.toml": "b09f249a723276ba270d4110baf8122ab485041893222af56f0fbc9c715a474c",
}


def load_route():
    spec = importlib.util.spec_from_file_location("workflow_route", ROUTE_PATH)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


workflow_route = load_route()


def _git(root: Path, *args: str) -> None:
    subprocess.run(["git", *args], cwd=root, check=True, capture_output=True, text=True)


def _fixture_root() -> Path:
    root = Path(tempfile.mkdtemp(prefix="wtk-native-route-"))
    _git(root, "init", "-q")
    _git(root, "config", "user.email", "test@example.com")
    _git(root, "config", "user.name", "WTK Test")
    for provider in workflow_route.PROVIDERS:
        extension = "toml" if provider == "codex" else "md"
        for role in workflow_route.ROLES:
            agent_name = workflow_route.AGENT_NAMES.get(role, role)
            path = root / f".{provider}" / "agents" / f"{agent_name}.{extension}"
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(
                f"project-owned {provider} {role}\nmodel = \"{provider}-{role}\"\neffort = \"medium\"\n",
                encoding="utf-8",
            )
    checks = root / ".specs/features/fixture/checks.md"
    checks.parent.mkdir(parents=True, exist_ok=True)
    checks.write_text("Profile: standard\n\n### S1 - fixture\n", encoding="utf-8")
    _git(root, "add", ".")
    _git(root, "commit", "-qm", "fixture")
    return root


def _all_values(value: object):
    if isinstance(value, dict):
        for key, item in value.items():
            yield key
            yield from _all_values(item)
    elif isinstance(value, list):
        for item in value:
            yield from _all_values(item)
    elif isinstance(value, str):
        yield value


def test_toml_free_route_preserves_native_agents() -> None:
    root = _fixture_root()
    try:
        before = {
            str(path.relative_to(root)): path.read_bytes()
            for path in (root / ".claude/agents").glob("*.md")
        }
        before.update(
            {
                str(path.relative_to(root)): path.read_bytes()
                for path in (root / ".codex/agents").glob("*.toml")
            }
        )
        before.update(
            {
                str(path.relative_to(root)): path.read_bytes()
                for path in (root / ".cursor/agents").glob("*.md")
            }
        )
        snapshot = workflow_route.resolve(root=root, feature="fixture", native_provider="codex")
        resumed = workflow_route.resolve(root=root, feature="fixture", native_provider="claude")
        assert resumed == snapshot
        assert snapshot["deep_review"] == {"cadence": "skip", "groups": []}
        assert snapshot["parallelization"] == {"mode": "disabled"}
        assert all(path.read_bytes() == bytes_before for path, bytes_before in ((root / relative, value) for relative, value in before.items()))
        assert not (root / ".wtk.toml").exists()
    finally:
        shutil.rmtree(root)


def test_source_checkout_has_no_wtk_toml() -> None:
    assert not (ROOT / ".wtk.toml").exists()
    assert not (ROOT / ".wtk.toml.example").exists()
    for relative, expected in NATIVE_HASHES.items():
        path = ROOT / relative
        assert path.is_file(), relative
        assert hashlib.sha256(path.read_bytes()).hexdigest() == expected, relative


def test_snapshot_freezes_identity_not_model() -> None:
    root = _fixture_root()
    try:
        snapshot = workflow_route.resolve(
            root=root,
            feature="fixture",
            native_provider="cursor",
            overrides=["verifier=codex"],
        )
        assert set(snapshot["roles"]["verifier"]) == {"provider", "agent_file"}
        assert snapshot["roles"]["verifier"]["provider"] == "codex"
        assert "model" not in set(_all_values(snapshot))
        assert "effort" not in set(_all_values(snapshot))
        assert "config_version" not in set(_all_values(snapshot))
        persisted = json.loads(
            (root / ".specs/features/fixture/workflow.json").read_text(encoding="utf-8")
        )
        assert persisted == snapshot
        assert not any(
            path.name.startswith(".workflow.json.")
            for path in (root / ".specs/features/fixture").iterdir()
        )
    finally:
        shutil.rmtree(root)


def test_review_is_on_demand() -> None:
    root = _fixture_root()
    try:
        route = workflow_route.resolve(root=root, feature="fixture", native_provider="claude")
        assert route["deep_review"] == {"cadence": "skip", "groups": []}
        assert route["parallelization"] == {"mode": "disabled"}
    finally:
        shutil.rmtree(root)


def test_route_rejects_unsafe_feature_slug() -> None:
    root = _fixture_root()
    try:
        for feature in ("../escape", "feature/sub", "Feature", "feature_name"):
            try:
                workflow_route.resolve(root=root, feature=feature, native_provider="claude")
            except workflow_route.RouteError:
                continue
            raise AssertionError(f"unsafe feature slug accepted: {feature}")
    finally:
        shutil.rmtree(root)


if __name__ == "__main__":
    pattern = None
    if "-k" in sys.argv:
        index = sys.argv.index("-k")
        pattern = sys.argv[index + 1] if index + 1 < len(sys.argv) else ""
    selected = [
        (name, function)
        for name, function in sorted(globals().items())
        if name.startswith("test_") and (pattern is None or pattern in name)
    ]
    for name, function in selected:
        function()
    print(f"{len(selected)} passed, 0 failed")
