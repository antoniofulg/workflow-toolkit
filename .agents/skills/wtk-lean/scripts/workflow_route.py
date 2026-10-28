#!/usr/bin/env python3
"""Freeze human-confirmed WTK stage selections in a checkout-owned feature route."""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import Any


STAGES = (
    "planning", "exploration", "design", "implementation", "verification", "qa",
    "deep_review", "remediation", "delivery",
)
SNAPSHOT_VERSION = 2
SELECTION_KEYS = {"version", "feature", "checkout", "stages", "approval"}
SNAPSHOT_KEYS = SELECTION_KEYS | {
    "git_head", "profile", "verification_profile", "deep_review", "parallelization",
}
SLUG_RE = re.compile(r"^[a-z0-9](?:[a-z0-9-]*[a-z0-9])?$")
PROFILE_RE = re.compile(
    r"^\**Profile\**\s*:\s*`?(light|standard|ui)`?\s*$",
    re.IGNORECASE | re.MULTILINE,
)


class RouteError(ValueError):
    """A user-correctable route input error."""


def _error(message: str) -> RouteError:
    return RouteError(f"wtk-lean: {message}")


def _snapshot_path(root: Path, feature: str) -> Path:
    if not isinstance(feature, str) or not SLUG_RE.fullmatch(feature):
        raise _error("feature must be a lowercase slug")
    current = root
    for component in (".specs", "features", feature, "workflow.json"):
        current /= component
        if current.is_symlink():
            raise _error(f"snapshot destination must not contain symlinks: {current}")
        if current.exists() and (
            not current.is_file() if component == "workflow.json" else not current.is_dir()
        ):
            raise _error(f"snapshot destination has an invalid path component: {current}")
    return current


def _git_head(root: Path) -> str:
    try:
        return subprocess.check_output(
            ["git", "rev-parse", "HEAD"], cwd=root, text=True, stderr=subprocess.PIPE
        ).strip()
    except (OSError, subprocess.CalledProcessError) as exc:
        raise _error(f"cannot resolve git head in {root}") from exc


def _derived_slice_count(root: Path, feature: str) -> int:
    checks = root / ".specs" / "features" / feature / "checks.md"
    if not checks.is_file():
        return 1
    count = sum(
        1 for line in checks.read_text(encoding="utf-8").splitlines()
        if re.match(r"^### S\d+\s+-", line)
    )
    return count or 1


def _verification_profile(root: Path, feature: str, requested: str | None) -> str:
    checks = root / ".specs" / "features" / feature / "checks.md"
    approved = None
    if checks.is_file():
        match = PROFILE_RE.search(checks.read_text(encoding="utf-8"))
        approved = match.group(1).lower() if match else None
    selected = requested if requested is not None else approved or "standard"
    if not isinstance(selected, str) or selected not in {"light", "standard", "ui"}:
        raise _error("verification profile must be 'light', 'standard', or 'ui'")
    if approved and selected != approved:
        raise _error(
            f"verification profile '{selected}' does not match checks.md profile '{approved}'"
        )
    return selected


def _nonempty(value: Any) -> bool:
    return isinstance(value, str) and bool(value.strip())


def _unique_object(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    value: dict[str, Any] = {}
    for key, item in pairs:
        if key in value:
            raise ValueError("duplicate JSON object key")
        value[key] = item
    return value


def _read_json(path: Path, label: str) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"), object_pairs_hook=_unique_object)
    except (OSError, ValueError) as exc:
        raise _error(f"{label} is unreadable or invalid JSON: {path}") from exc


def _validate_selection(root: Path, feature: str, selection: Any) -> dict[str, Any]:
    if not isinstance(selection, dict) or set(selection) != SELECTION_KEYS:
        raise _error("selection has an incomplete schema")
    if type(selection["version"]) is not int or selection["version"] != SNAPSHOT_VERSION:
        raise _error("selection version is stale; supply a newly confirmed version 2 selection")
    if selection["feature"] != feature:
        raise _error("selection feature does not match the requested feature")
    if selection["checkout"] != str(root):
        raise _error("selection checkout does not match the current checkout")
    stages = selection["stages"]
    if not isinstance(stages, dict) or not stages or not set(stages) <= set(STAGES):
        raise _error("selection stages must be a nonempty object of supported stage keys")
    for stage, row in stages.items():
        required = {"provider", "model", "effort", "rationale", "limitations"}
        if not isinstance(row, dict) or not required <= set(row) <= required | {"scope"}:
            raise _error(f"selection stage {stage!r} has an incomplete schema")
        for field in ("provider", "model", "effort", "rationale"):
            if not _nonempty(row[field]):
                raise _error(f"selection stage {stage!r} requires a nonempty {field}")
        if "scope" in row and not _nonempty(row["scope"]):
            raise _error(f"selection stage {stage!r} scope must be a nonempty string")
        limits = row["limitations"]
        if not isinstance(limits, list) or not all(_nonempty(limit) for limit in limits):
            raise _error(f"selection stage {stage!r} limitations must be a list of nonempty strings")
        for field in ("model", "effort"):
            if row[field] == "inherited" and not any(
                limit.startswith(f"{field}:") and _nonempty(limit[len(field) + 1:])
                for limit in limits
            ):
                raise _error(f"selection stage {stage!r} inherited {field} requires a named limitation")
    approval = selection["approval"]
    if not isinstance(approval, dict) or set(approval) != {"status", "reference", "stages"}:
        raise _error("selection approval must contain status, reference and exact stages")
    if approval["status"] != "confirmed" or not _nonempty(approval["reference"]):
        raise _error("selection requires confirmed approval with a human decision reference")
    if approval["stages"] != stages:
        raise _error("selection approval does not match the exact selected stages")
    return selection


def _validate_snapshot(root: Path, feature: str, snapshot: Any) -> dict[str, Any]:
    if not isinstance(snapshot, dict) or set(snapshot) != SNAPSHOT_KEYS:
        raise _error("existing snapshot has an incomplete schema")
    if type(snapshot.get("version")) is not int or snapshot["version"] != SNAPSHOT_VERSION:
        raise _error("existing snapshot version is stale; explicitly replace the obsolete snapshot")
    _validate_selection(root, feature, {key: snapshot[key] for key in SELECTION_KEYS})
    if not _nonempty(snapshot["git_head"]):
        raise _error("existing snapshot git_head must be a non-empty string")
    if snapshot.get("profile") is not None and not isinstance(snapshot["profile"], str):
        raise _error("existing snapshot profile must be a string or null")
    if not isinstance(snapshot["verification_profile"], str) or snapshot["verification_profile"] not in {"light", "standard", "ui"}:
        raise _error("existing snapshot verification_profile is invalid")
    if snapshot.get("deep_review") != {"cadence": "skip", "groups": []}:
        raise _error("existing snapshot deep_review must remain on demand")
    if snapshot.get("parallelization") != {"mode": "disabled"}:
        raise _error("existing snapshot parallelization must remain sequential")
    return snapshot


def validate_snapshot(root: Path, feature: str, snapshot: Any) -> dict[str, Any]:
    """Validate a route snapshot for runtime readers."""
    root = root.resolve()
    _snapshot_path(root, feature)
    return _validate_snapshot(root, feature, snapshot)


def _write_snapshot(path: Path, snapshot: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary: str | None = None
    try:
        with tempfile.NamedTemporaryFile(
            mode="w", encoding="utf-8", dir=path.parent, prefix=f".{path.name}.", delete=False
        ) as stream:
            temporary = stream.name
            json.dump(snapshot, stream, indent=2, sort_keys=True)
            stream.write("\n")
            stream.flush()
        Path(temporary).replace(path)
        temporary = None
    finally:
        if temporary:
            Path(temporary).unlink(missing_ok=True)


def resolve(
    *, root: Path, feature: str, selection_file: Path | None = None, slice_count: int | None = None,
    profile: str | None = None, verification_profile: str | None = None,
    refresh: bool = False,
) -> dict[str, Any]:
    """Validate approval and freeze exact choices, or reuse an unchanged approved route."""
    root = root.resolve()
    if not root.is_dir():
        raise _error(f"root is not a directory: {root}")
    snapshot_path = _snapshot_path(root, feature)
    derived_count = _derived_slice_count(root, feature)
    if slice_count is not None:
        if not isinstance(slice_count, int) or isinstance(slice_count, bool) or slice_count < 1:
            raise _error("slice count must be at least 1")
        if slice_count != derived_count:
            raise _error(
                f"slice count assertion {slice_count} does not match derived slice count {derived_count}"
            )
    if profile is not None and not _nonempty(profile):
        raise _error("profile must be a nonempty string or null")
    if verification_profile is not None:
        _verification_profile(root, feature, verification_profile)
    existing = None
    if snapshot_path.exists():
        existing = _validate_snapshot(root, feature, _read_json(snapshot_path, "existing snapshot"))
        if not refresh and verification_profile is not None and verification_profile != existing["verification_profile"]:
            raise _error("verification profile does not match the frozen snapshot; use --refresh")
    if selection_file is None:
        if existing is None or refresh:
            raise _error("a confirmed selection file is required before creating or refreshing a route")
        return existing
    selection = _validate_selection(root, feature, _read_json(selection_file, "selection file"))
    if existing is not None:
        changed = selection["stages"] != existing["stages"]
        if changed and selection["approval"]["reference"] == existing["approval"]["reference"]:
            raise _error("changed selections require a fresh approval reference")
        if not refresh and selection == {key: existing[key] for key in SELECTION_KEYS}:
            return existing
    selected_profile = (
        existing["verification_profile"] if existing is not None and not refresh
        else _verification_profile(root, feature, verification_profile)
    )
    snapshot = {
        **selection,
        "git_head": _git_head(root),
        "profile": profile if profile is not None else existing["profile"] if existing else None,
        "verification_profile": selected_profile,
        "deep_review": {"cadence": "skip", "groups": []},
        "parallelization": {"mode": "disabled"},
    }
    _write_snapshot(snapshot_path, snapshot)
    return snapshot


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path.cwd())
    parser.add_argument("--feature", required=True)
    parser.add_argument("--slices", dest="slice_count", type=int)
    parser.add_argument("--selection-file", type=Path)
    parser.add_argument("--profile")
    parser.add_argument("--verification-profile")
    parser.add_argument("--refresh", action="store_true")
    return parser


def main(argv: list[str] | None = None) -> int:
    try:
        snapshot = resolve(**vars(_parser().parse_args(argv)))
    except (RouteError, OSError) as exc:
        print(str(exc), file=sys.stderr)
        return 2
    print(json.dumps(snapshot, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
