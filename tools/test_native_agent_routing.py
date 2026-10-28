"""Contract tests for approved WTK stage selection and native-file preservation."""

from __future__ import annotations

import argparse
import copy
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


def _fixture_root(*, native: bool = False) -> Path:
    root = Path(tempfile.mkdtemp(prefix="wtk-stage-route-")).resolve()
    _git(root, "init", "-q")
    _git(root, "config", "user.email", "test@example.com")
    _git(root, "config", "user.name", "WTK Test")
    if native:
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


def _stage(**changes) -> dict:
    return {
        "provider": "codex", "model": "gpt-6.1-sol", "effort": "max",
        "rationale": "One coding worker owns the route and canonical tests.",
        "limitations": [], **changes,
    }


def _selection(root: Path, feature: str = "fixture", *, stages=None, reference="User reply 1: accept the proposed rows.") -> dict:
    stages = copy.deepcopy(stages if stages is not None else {"implementation": _stage()})
    return {
        "version": 2, "feature": feature, "checkout": str(root), "stages": stages,
        "approval": {"status": "confirmed", "reference": reference, "stages": copy.deepcopy(stages)},
    }


def _selection_file(root: Path, selection: dict) -> Path:
    path = root / "selection.json"
    path.write_text(json.dumps(selection), encoding="utf-8")
    return path


def _resolve(root: Path, feature: str = "fixture", *, selection=None, **kwargs) -> dict:
    selection = selection if selection is not None else _selection(root, feature)
    return workflow_route.resolve(
        root=root, feature=feature, selection_file=_selection_file(root, selection), **kwargs
    )


def _reject(root: Path, selection: dict | None, *, feature="fixture", error="", **kwargs) -> None:
    try:
        workflow_route.resolve(
            root=root, feature=feature,
            selection_file=_selection_file(root, selection) if selection is not None else None,
            **kwargs,
        )
    except workflow_route.RouteError as exc:
        assert error in str(exc), str(exc)
    else:
        raise AssertionError(f"invalid route input accepted: {selection}")


def _snapshot_path(root: Path, feature: str = "fixture") -> Path:
    return root / ".specs/features" / feature / "workflow.json"


def test_toml_free_route_preserves_native_agents() -> None:
    root = _fixture_root(native=True)
    try:
        before = {relative: (root / relative).read_bytes() for relative in BASELINE}
        snapshot = _resolve(root)
        resumed = workflow_route.resolve(root=root, feature="fixture")
        assert resumed == snapshot
        assert snapshot["deep_review"] == {"cadence": "skip", "groups": []}
        assert snapshot["parallelization"] == {"mode": "disabled"}
        assert all((root / relative).read_bytes() == value for relative, value in before.items())
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
    scratch = _fixture_root(native=True)
    try:
        for relative, metadata in BASELINE.items():
            assert (scratch / relative).read_bytes() == _native_bytes(relative, metadata), relative
    finally:
        shutil.rmtree(scratch)


def test_approved_stage_selection_without_native_files() -> None:
    root = _fixture_root()
    try:
        stages = {
            "implementation": _stage(provider="project-runtime", model="human-selected-model", effort="high", scope="C2 through C6"),
            "verification": _stage(
                model="inherited", effort="inherited", rationale="Fresh context checks every criterion.",
                limitations=["model: host does not expose the checking model", "effort: inherited host default"],
            ),
        }
        selection = _selection(root, stages=stages, reference="User reply 2: use this model and high effort; accept the checking limits.")
        path = _selection_file(root, selection)
        result = subprocess.run(
            [sys.executable, str(ROUTE_PATH), "--root", str(root), "--feature", "fixture", "--selection-file", str(path)],
            capture_output=True, text=True,
        )
        assert result.returncode == 0, result.stderr
        snapshot = json.loads(result.stdout)
        assert snapshot["version"] == 2
        assert snapshot["feature"] == "fixture" and snapshot["checkout"] == str(root)
        assert snapshot["stages"] == stages
        assert snapshot["approval"] == selection["approval"]
        assert snapshot["git_head"] == subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=root, text=True).strip()
        assert snapshot["profile"] is None and snapshot["verification_profile"] == "standard"
        assert "roles" not in snapshot and "overrides" not in snapshot and "config_version" not in snapshot
        assert json.loads(_snapshot_path(root).read_text(encoding="utf-8")) == snapshot
        assert not any(path.name.startswith(".workflow.json.") for path in _snapshot_path(root).parent.iterdir())
        assert all(not (root / f".{provider}/agents").exists() for provider in ("codex", "claude", "cursor"))
    finally:
        shutil.rmtree(root)


def test_review_is_on_demand() -> None:
    root = _fixture_root()
    try:
        route = _resolve(root)
        assert route["deep_review"] == {"cadence": "skip", "groups": []}
        assert route["parallelization"] == {"mode": "disabled"}
    finally:
        shutil.rmtree(root)


def test_route_requires_confirmed_selection() -> None:
    root = _fixture_root()
    try:
        unapproved = []
        for change in ("pending", "absent", "mismatched", "empty-reference"):
            candidate = _selection(root)
            if change == "pending":
                candidate["approval"]["status"] = "pending"
            elif change == "absent":
                del candidate["approval"]
            elif change == "mismatched":
                candidate["approval"]["stages"]["implementation"]["model"] = "another-model"
            else:
                candidate["approval"]["reference"] = " "
            unapproved.append(candidate)
        _reject(root, None, error="confirmed selection")
        for candidate in unapproved:
            _reject(root, candidate)
            assert not _snapshot_path(root).exists()
        _resolve(root)
        before = _snapshot_path(root).read_bytes()
        for candidate in unapproved:
            _reject(root, candidate, refresh=True)
            assert _snapshot_path(root).read_bytes() == before
    finally:
        shutil.rmtree(root)


def test_selection_resume_and_changes() -> None:
    root = _fixture_root()
    try:
        selection = _selection(root, stages={"implementation": _stage(), "verification": _stage(model="checking-model", effort="high")})
        snapshot = _resolve(root, selection=selection)
        before = _snapshot_path(root).read_bytes()
        assert workflow_route.resolve(root=root, feature="fixture") == snapshot
        assert _resolve(root, selection=selection) == snapshot
        assert _snapshot_path(root).read_bytes() == before
        changed = copy.deepcopy(selection)
        changed["stages"]["implementation"]["model"] = "human-override"
        _reject(root, changed, error="approval")
        changed["approval"]["stages"] = copy.deepcopy(changed["stages"])
        _reject(root, changed, error="fresh approval reference")
        assert _snapshot_path(root).read_bytes() == before
        changed["approval"]["reference"] = "User reply 1 accepted unchanged rows; reply 3 accepts only the implementation override."
        updated = _resolve(root, selection=changed)
        assert updated["stages"] == changed["stages"]
        assert updated["stages"]["verification"] == snapshot["stages"]["verification"]
        assert updated["approval"] == changed["approval"]
        assert workflow_route.resolve(root=root, feature="fixture") == updated
    finally:
        shutil.rmtree(root)


def test_selection_cli_failures_preserve_snapshot() -> None:
    root = _fixture_root()
    foreign = _fixture_root()
    try:
        _resolve(root)
        before = _snapshot_path(root).read_bytes()
        cases = ["{", "[]"]
        duplicate = json.dumps(_selection(root)).replace('"status": "confirmed"', '"status": "pending", "status": "confirmed"')
        cases.append(duplicate)
        for key, value in (("version", 1), ("feature", "other"), ("checkout", str(foreign))):
            candidate = _selection(root)
            candidate[key] = value
            cases.append(json.dumps(candidate))
        path = root / "selection.json"
        for source in cases:
            path.write_text(source, encoding="utf-8")
            result = subprocess.run(
                [sys.executable, str(ROUTE_PATH), "--root", str(root), "--feature", "fixture", "--selection-file", str(path), "--refresh"],
                capture_output=True, text=True,
            )
            assert result.returncode == 2, result.stderr
            assert result.stderr.startswith("wtk-lean:") and not result.stdout
            assert _snapshot_path(root).read_bytes() == before
        path.unlink()
        result = subprocess.run(
            [sys.executable, str(ROUTE_PATH), "--root", str(root), "--feature", "fixture", "--selection-file", str(path)],
            capture_output=True, text=True,
        )
        assert result.returncode == 2 and _snapshot_path(root).read_bytes() == before
        stale = json.loads(before)
        stale["version"] = 1
        _snapshot_path(root).write_text(json.dumps(stale), encoding="utf-8")
        stale_bytes = _snapshot_path(root).read_bytes()
        _reject(root, None, error="version is stale")
        assert _snapshot_path(root).read_bytes() == stale_bytes
    finally:
        shutil.rmtree(root)
        shutil.rmtree(foreign)


def test_selection_validation_matrix() -> None:
    root = _fixture_root()
    try:
        for stage in ("planning", "exploration", "design", "implementation", "verification", "qa", "deep_review", "remediation", "delivery"):
            selected = {stage: _stage()}
            assert _resolve(root, selection=_selection(root, stages=selected, reference=f"User accepts {stage}."))["stages"] == selected
        before = _snapshot_path(root).read_bytes()
        invalid_rows = [
            {"provider": " "}, {"provider": ["codex"]}, {"provider": ""},
            {"model": ""}, {"model": 3}, {"effort": " "}, {"effort": None},
            {"rationale": ""}, {"limitations": "none"}, {"limitations": [""]},
            {"limitations": [False]}, {"model": "inherited"}, {"effort": "inherited"},
            {"model": "inherited", "limitations": ["effort: inherited"]},
            {"model": "inherited", "limitations": ["model:"]},
            {"effort": "inherited", "limitations": ["effort: "]},
            {"scope": 42}, {"scope": ""}, {"agent_file": ".codex/agents/implementer.toml"},
        ]
        for changes in invalid_rows:
            _reject(root, _selection(root, stages={"implementation": _stage(**changes)}))
            assert _snapshot_path(root).read_bytes() == before
        for stages in ({}, [], {"implementer": _stage()}, {"implementation": []}, {"implementation": {"provider": "codex"}}):
            _reject(root, _selection(root, stages=stages))
            assert _snapshot_path(root).read_bytes() == before
        candidate = _selection(root)
        candidate["version"] = 2.0
        _reject(root, candidate, error="version")
        assert _snapshot_path(root).read_bytes() == before
    finally:
        shutil.rmtree(root)


def test_route_rejects_unsafe_feature_slug() -> None:
    root = _fixture_root()
    try:
        _resolve(root)
        before = _snapshot_path(root).read_bytes()
        for feature in ("../escape", "feature/sub", "Feature", "feature_name", "", "."):
            _reject(root, _selection(root, feature), feature=feature, error="lowercase slug")
            assert _snapshot_path(root).read_bytes() == before
        assert not (root / ".specs/escape").exists()
    finally:
        shutil.rmtree(root)


def test_snapshot_destination_ownership() -> None:
    foreign = Path(tempfile.mkdtemp(prefix="wtk-foreign-destination-")).resolve()
    try:
        for component in (".specs", ".specs/features", ".specs/features/fixture", ".specs/features/fixture/workflow.json"):
            root = _fixture_root()
            try:
                target = foreign / "workflow.json" if component.endswith(".json") else foreign
                sentinel = foreign / "workflow.json"
                sentinel.write_text("foreign state\n", encoding="utf-8")
                path = root / component
                if path.is_dir():
                    shutil.rmtree(path)
                path.symlink_to(target, target_is_directory=target.is_dir())
                _reject(root, _selection(root), error="snapshot destination")
                assert sentinel.read_text(encoding="utf-8") == "foreign state\n"
            finally:
                shutil.rmtree(root)
        root = _fixture_root()
        try:
            local = root / "local"
            local.mkdir()
            path = root / ".specs/features/fixture"
            shutil.rmtree(path)
            path.symlink_to(local, target_is_directory=True)
            _reject(root, _selection(root), error="snapshot destination")
            assert not (local / "workflow.json").exists()
        finally:
            shutil.rmtree(root)
    finally:
        shutil.rmtree(foreign)


def test_route_derives_verification_profile_and_refreshes() -> None:
    root = _fixture_root()
    try:
        checks = root / ".specs/features/profiled/checks.md"
        checks.parent.mkdir(parents=True, exist_ok=True)
        checks.write_text("Profile: ui\n\n### S1 - fixture\n", encoding="utf-8")
        first = _resolve(root, "profiled")
        assert first["verification_profile"] == "ui"
        checks.write_text("Profile: light\n\n### S1 - fixture\n", encoding="utf-8")
        assert workflow_route.resolve(root=root, feature="profiled") == first
        refreshed = _resolve(root, "profiled", refresh=True)
        assert refreshed["verification_profile"] == "light"
        assert refreshed["stages"] == first["stages"] and refreshed["approval"] == first["approval"]
        before = _snapshot_path(root, "profiled").read_bytes()
        _reject(root, _selection(root, "profiled"), feature="profiled", verification_profile="standard", error="does not match")
        assert _snapshot_path(root, "profiled").read_bytes() == before
        for invalid in ("", "unknown"):
            _reject(root, _selection(root, "profiled"), feature="profiled", verification_profile=invalid, refresh=True, error="verification profile must be")
            assert _snapshot_path(root, "profiled").read_bytes() == before
    finally:
        shutil.rmtree(root)


def test_route_fails_closed_for_invalid_snapshot() -> None:
    root = _fixture_root()
    try:
        _snapshot_path(root).write_text("{}\n", encoding="utf-8")
        _reject(root, None, error="incomplete schema")
        assert _snapshot_path(root).read_bytes() == b"{}\n"
    finally:
        shutil.rmtree(root)


def test_route_enforces_slice_assertion_before_snapshot_write() -> None:
    root = _fixture_root()
    try:
        checks = root / ".specs/features/sliced/checks.md"
        checks.parent.mkdir(parents=True, exist_ok=True)
        checks.write_text("Profile: standard\n\n### S1 - first\n\n### S2 - second\n", encoding="utf-8")
        _reject(root, _selection(root, "sliced"), feature="sliced", slice_count=1, error="does not match derived slice count 2")
        assert not _snapshot_path(root, "sliced").exists()
        resolved = _resolve(root, "sliced", slice_count=2)
        assert resolved["feature"] == "sliced"
        before = _snapshot_path(root, "sliced").read_bytes()
        for count in (0, 1):
            _reject(root, None, feature="sliced", slice_count=count)
            assert _snapshot_path(root, "sliced").read_bytes() == before
    finally:
        shutil.rmtree(root)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("-k", dest="pattern")
    pattern = parser.parse_args().pattern
    selected = [
        (name, function) for name, function in sorted(globals().items())
        if name.startswith("test_") and (pattern is None or pattern in name)
    ]
    if not selected:
        raise SystemExit(f"no tests matched: {pattern}")
    for name, function in selected:
        function()
    print(f"{len(selected)} passed, 0 failed")
