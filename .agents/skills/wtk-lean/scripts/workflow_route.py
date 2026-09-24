#!/usr/bin/env python3
"""Record a project-owned WTK feature route without reading WTK configuration."""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import Any


PROVIDERS = ("claude", "codex", "cursor")
ROLES = ("implementer", "verifier", "explorer", "deep_reviewer", "designer")
AGENT_NAMES = {"deep_reviewer": "deep-reviewer"}
SNAPSHOT_VERSION = 1
SNAPSHOT_KEYS = {
    "version", "feature", "git_head", "profile", "verification_profile", "overrides",
    "deep_review", "parallelization", "roles",
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
    if not SLUG_RE.fullmatch(feature):
        raise _error("feature must be a lowercase slug")
    return root / ".specs" / "features" / feature / "workflow.json"


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
    selected = requested or approved or "standard"
    if selected not in {"light", "standard", "ui"}:
        raise _error("verification profile must be 'light', 'standard', or 'ui'")
    if approved and selected != approved:
        raise _error(
            f"verification profile '{selected}' does not match checks.md profile '{approved}'"
        )
    return selected


def _runtime_relative(provider: str, role: str) -> Path:
    extension = "toml" if provider == "codex" else "md"
    return Path(f".{provider}") / "agents" / f"{AGENT_NAMES.get(role, role)}.{extension}"


def _agent_file(root: Path, provider: str, role: str) -> str:
    relative = _runtime_relative(provider, role)
    current = root / relative
    if current.is_symlink() or not current.is_file():
        raise _error(
            f"missing native agent file for provider {provider!r}, role {role!r}; "
            f"expected {relative.as_posix()}"
        )
    return relative.as_posix()


def _parse_overrides(values: list[str]) -> dict[str, str]:
    parsed: dict[str, str] = {}
    for value in values:
        role, separator, provider = value.partition("=")
        if not separator or role not in ROLES or provider not in PROVIDERS:
            raise _error("override must use a supported role=provider pair")
        if role in parsed:
            raise _error(f"duplicate override for role {role!r}")
        parsed[role] = provider
    return parsed


def _validate_snapshot(root: Path, feature: str, snapshot: Any) -> dict[str, Any]:
    if not isinstance(snapshot, dict) or set(snapshot) != SNAPSHOT_KEYS:
        raise _error("existing snapshot has an incomplete schema")
    if snapshot.get("version") != SNAPSHOT_VERSION:
        raise _error("existing snapshot version is stale; rerun resolution with --refresh")
    if snapshot.get("feature") != feature:
        raise _error("existing snapshot feature does not match the requested feature")
    if not isinstance(snapshot.get("git_head"), str) or not snapshot["git_head"]:
        raise _error("existing snapshot git_head must be a non-empty string")
    if snapshot.get("profile") is not None and not isinstance(snapshot["profile"], str):
        raise _error("existing snapshot profile must be a string or null")
    if snapshot.get("verification_profile") not in {"light", "standard", "ui"}:
        raise _error("existing snapshot verification_profile is invalid")
    overrides = snapshot.get("overrides")
    if not isinstance(overrides, dict):
        raise _error("existing snapshot overrides must be an object")
    _parse_overrides([f"{role}={provider}" for role, provider in overrides.items()])
    if snapshot.get("deep_review") != {"cadence": "skip", "groups": []}:
        raise _error("existing snapshot deep_review must remain on demand")
    if snapshot.get("parallelization") != {"mode": "disabled"}:
        raise _error("existing snapshot parallelization must remain sequential")
    roles = snapshot.get("roles")
    if not isinstance(roles, dict) or set(roles) != set(ROLES):
        raise _error("existing snapshot roles must contain every delegated workflow role")
    for role in ROLES:
        route = roles[role]
        if not isinstance(route, dict) or set(route) != {"provider", "agent_file"}:
            raise _error(f"existing snapshot role {role!r} must contain provider and agent_file only")
        provider = route["provider"]
        if provider not in PROVIDERS:
            raise _error(f"existing snapshot role {role!r} has an invalid provider")
        expected = _runtime_relative(provider, role).as_posix()
        if route["agent_file"] != expected:
            raise _error(f"existing snapshot role {role!r} has an invalid agent_file")
        _agent_file(root, provider, role)
    return snapshot


def validate_snapshot(root: Path, feature: str, snapshot: Any) -> dict[str, Any]:
    """Validate a route snapshot for runtime readers."""
    return _validate_snapshot(root.resolve(), feature, snapshot)


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
    *, root: Path, feature: str, native_provider: str, slice_count: int | None = None,
    profile: str | None = None, verification_profile: str | None = None,
    overrides: list[str] | None = None, refresh: bool = False,
) -> dict[str, Any]:
    """Resolve and persist a project-owned feature route."""
    root = root.resolve()
    if not root.is_dir():
        raise _error(f"root is not a directory: {root}")
    if native_provider not in PROVIDERS:
        raise _error(f"invalid native provider {native_provider!r}")
    snapshot_path = _snapshot_path(root, feature)
    if snapshot_path.exists() and not refresh:
        try:
            snapshot = json.loads(snapshot_path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as exc:
            raise _error(f"existing snapshot is invalid: {snapshot_path}") from exc
        return _validate_snapshot(root, feature, snapshot)

    derived_count = _derived_slice_count(root, feature)
    if slice_count is not None:
        if slice_count < 1:
            raise _error("slice count must be at least 1")
        if slice_count != derived_count:
            raise _error(
                f"slice count assertion {slice_count} does not match derived slice count {derived_count}"
            )
    verification_profile = _verification_profile(root, feature, verification_profile)
    parsed_overrides = _parse_overrides(overrides or [])
    providers = {role: parsed_overrides.get(role, native_provider) for role in ROLES}
    roles = {
        role: {"provider": provider, "agent_file": _agent_file(root, provider, role)}
        for role, provider in providers.items()
    }
    snapshot = {
        "version": SNAPSHOT_VERSION,
        "feature": feature,
        "git_head": _git_head(root),
        "profile": profile,
        "verification_profile": verification_profile,
        "overrides": parsed_overrides,
        "deep_review": {"cadence": "skip", "groups": []},
        "parallelization": {"mode": "disabled"},
        "roles": roles,
    }
    _write_snapshot(snapshot_path, snapshot)
    return snapshot


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path.cwd())
    parser.add_argument("--feature", required=True)
    parser.add_argument("--slices", dest="slice_count", type=int)
    parser.add_argument("--native-provider", required=True)
    parser.add_argument("--profile")
    parser.add_argument("--verification-profile")
    parser.add_argument("--override", dest="overrides", action="append", default=[])
    parser.add_argument("--refresh", action="store_true")
    return parser


def main(argv: list[str] | None = None) -> int:
    try:
        snapshot = resolve(**vars(_parser().parse_args(argv)))
    except RouteError as exc:
        print(str(exc), file=sys.stderr)
        return 2
    print(json.dumps(snapshot, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
