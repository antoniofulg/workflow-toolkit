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
BASELINE_PATH = ROOT / "tools/fixtures/native-agent-baseline.json"
BASELINE = json.loads(BASELINE_PATH.read_text(encoding="utf-8"))


def load_route():
    spec = importlib.util.spec_from_file_location("workflow_route", ROUTE_PATH)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


workflow_route = load_route()


def _git(root: Path, *args: str) -> None:
    subprocess.run(["git", *args], cwd=root, check=True, capture_output=True, text=True)


def _native_bytes(relative: str, metadata: dict[str, str]) -> bytes:
    model = metadata["model"]
    effort = metadata["effort"]
    if relative.startswith(".cursor/"):
        return f"---\nmodel: {model}[effort={effort}]\n---\n".encode()
    if relative.startswith(".codex/"):
        return f'model = "{model}"\nmodel_reasoning_effort = "{effort}"\n'.encode()
    return f"---\nmodel: {model}\neffort: {effort}\n---\n".encode()


def _fixture_root() -> Path:
    root = Path(tempfile.mkdtemp(prefix="wtk-native-route-"))
    _git(root, "init", "-q")
    _git(root, "config", "user.email", "test@example.com")
    _git(root, "config", "user.name", "WTK Test")
    for relative, metadata in BASELINE.items():
        path = root / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(_native_bytes(relative, metadata))
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
    assert len(BASELINE) == 18
    assert sum(relative.startswith(".cursor/") for relative in BASELINE) == 6
    for relative, metadata in BASELINE.items():
        path = ROOT / relative
        if path.is_file():
            assert hashlib.sha256(path.read_bytes()).hexdigest() == metadata["sha256"], relative
            assert _native_bytes(relative, metadata).splitlines()[1] in path.read_bytes(), relative

    scratch = _fixture_root()
    try:
        for relative, metadata in BASELINE.items():
            path = scratch / relative
            assert path.read_bytes() == _native_bytes(relative, metadata), relative
    finally:
        shutil.rmtree(scratch)


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


def test_route_derives_verification_profile_and_refreshes() -> None:
    root = _fixture_root()
    try:
        checks = root / ".specs/features/profiled/checks.md"
        checks.parent.mkdir(parents=True, exist_ok=True)
        checks.write_text("Profile: ui\n\n### S1 - fixture\n", encoding="utf-8")
        first = workflow_route.resolve(root=root, feature="profiled", native_provider="codex")
        assert first["verification_profile"] == "ui"
        checks.write_text("Profile: light\n\n### S1 - fixture\n", encoding="utf-8")
        resumed = workflow_route.resolve(root=root, feature="profiled", native_provider="claude")
        assert resumed["verification_profile"] == "ui"
        refreshed = workflow_route.resolve(
            root=root, feature="profiled", native_provider="claude", refresh=True
        )
        assert refreshed["verification_profile"] == "light"
    finally:
        shutil.rmtree(root)


def test_route_fails_closed_for_missing_agent_and_invalid_snapshot() -> None:
    root = _fixture_root()
    try:
        missing = root / ".codex/agents/verifier.toml"
        missing.unlink()
        try:
            workflow_route.resolve(root=root, feature="missing-agent", native_provider="codex")
        except workflow_route.RouteError as error:
            assert "missing native agent file" in str(error)
        else:
            raise AssertionError("missing native agent unexpectedly used a fallback")
        snapshot_path = root / ".specs/features/invalid/workflow.json"
        snapshot_path.parent.mkdir(parents=True, exist_ok=True)
        snapshot_path.write_text("{}\n", encoding="utf-8")
        try:
            workflow_route.resolve(root=root, feature="invalid", native_provider="claude")
        except workflow_route.RouteError as error:
            assert "incomplete schema" in str(error)
        else:
            raise AssertionError("invalid snapshot was accepted")
        workflow_route.resolve(root=root, feature="stale", native_provider="claude")
        stale_path = root / ".specs/features/stale/workflow.json"
        stale = json.loads(stale_path.read_text(encoding="utf-8"))
        stale["version"] = 99
        stale_path.write_text(json.dumps(stale), encoding="utf-8")
        try:
            workflow_route.resolve(root=root, feature="stale", native_provider="claude")
        except workflow_route.RouteError as error:
            assert "snapshot version is stale" in str(error)
        else:
            raise AssertionError("stale snapshot was accepted")
    finally:
        shutil.rmtree(root)


def test_route_enforces_slice_assertion_before_snapshot_write() -> None:
    root = _fixture_root()
    try:
        checks = root / ".specs/features/sliced/checks.md"
        checks.parent.mkdir(parents=True, exist_ok=True)
        checks.write_text(
            "Profile: standard\n\n### S1 - first\n\n### S2 - second\n",
            encoding="utf-8",
        )
        try:
            workflow_route.resolve(
                root=root, feature="sliced", native_provider="cursor", slice_count=1
            )
        except workflow_route.RouteError as error:
            assert "does not match derived slice count 2" in str(error)
        else:
            raise AssertionError("incorrect slice assertion was accepted")
        assert not (root / ".specs/features/sliced/workflow.json").exists()
        resolved = workflow_route.resolve(
            root=root, feature="sliced", native_provider="cursor", slice_count=2
        )
        assert resolved["feature"] == "sliced"
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
