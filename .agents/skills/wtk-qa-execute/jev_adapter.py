#!/usr/bin/env python3
"""Optional, dependency-free process boundary for a consuming project's Jev adapter.

The consuming project owns Jev Ultrafast and Browser Harness installation.  This helper only
preflights them, aliases the Vercel text-helper key in process memory, runs one bounded attempt,
and emits a secret-free result.  It never assigns a QA pass verdict.
"""

from __future__ import annotations

import argparse
import contextlib
import importlib.util
import io
import json
import os
from pathlib import Path
import shutil
import sys
import tempfile
from typing import Any, Callable, Iterator, Mapping
from urllib.parse import urlparse


ADAPTER = "jev-ultrafast"
TEXT_HELPER_URL = "https://ai-gateway.vercel.sh/v1"
TEXT_HELPER_MODEL = "inception/mercury-2.5"
MAX_URL_CHARS = 2048
MAX_GOAL_CHARS = 4000
MAX_STEPS = 32
MAX_TRACE_CHARS = 12000
EVIDENCE_NAME = "jev-ultrafast-attempt.json"
EXIT_CODES = {"completed": 0, "unavailable": 2, "failed": 1, "invalid": 2, "blocked": 3}
REDACT_ENV_NAMES = ("TYPESAFE_API_KEY", "AI_GATEWAY_API_KEY", "TEXT_MODEL_API_KEY")
HEADLESS_MODES = {"headless-cdp", "dedicated-headless-cdp"}
HEADED_MODES = {"headed-qa-profile", "dedicated-headed-qa"}
HOST_NATIVE_MODES = {"orca", "maestri"}


class AdapterInputError(ValueError):
    """An input failed closed before a browser or provider was touched."""


def _string(value: Any) -> str:
    return value if isinstance(value, str) else str(value)


def _secret_values(env: Mapping[str, str]) -> tuple[str, ...]:
    return tuple(value for name in REDACT_ENV_NAMES if (value := env.get(name)) and len(value) >= 4)


def redact(value: Any, env: Mapping[str, str] | None = None) -> Any:
    """Redact configured credential values recursively before any result/evidence sink."""
    secrets = _secret_values(env or os.environ)
    if isinstance(value, str):
        result = value
        for secret in secrets:
            result = result.replace(secret, "[REDACTED]")
        return result
    if isinstance(value, Mapping):
        return {str(key): redact(item, env) for key, item in value.items()}
    if isinstance(value, (list, tuple)):
        return [redact(item, env) for item in value]
    return value


def _bounded_json(value: Any, env: Mapping[str, str]) -> str:
    encoded = json.dumps(redact(value, env), ensure_ascii=False, sort_keys=True, default=str)
    return encoded[:MAX_TRACE_CHARS]


def _result(
    status: str,
    *,
    evidence: list[str] | None = None,
    limitation: str = "",
    env: Mapping[str, str] | None = None,
    **extra: Any,
) -> dict[str, Any]:
    result = {
        "adapter": ADAPTER,
        "status": status,
        "evidence": evidence or [],
        "limitation": limitation,
        **extra,
    }
    return redact(result, env)


def _valid_url(url: str) -> bool:
    parsed = urlparse(url)
    return len(url) <= MAX_URL_CHARS and parsed.scheme in {"http", "https"} and bool(parsed.netloc)


def _callable_or_bool(value: bool | Callable[[], bool] | None, default: Callable[[], bool]) -> bool:
    if value is None:
        return default()
    return bool(value() if callable(value) else value)


def _module_available() -> bool:
    try:
        return importlib.util.find_spec("jev_ultrafast") is not None
    except (ImportError, ValueError):
        return False


def _harness_available() -> bool:
    return shutil.which("browser-harness") is not None


def _default_agent_factory(url: str, goal: str) -> Any:
    from jev_ultrafast import Agent

    return Agent(url, goal)


def _normalize_browser(
    browser: Any, env: Mapping[str, str]
) -> tuple[str | None, str | None, str | None, str | None]:
    if isinstance(browser, str):
        mode, profile, cdp_url = browser, None, None
    elif isinstance(browser, Mapping):
        mode = _string(browser.get("mode", ""))
        profile = browser.get("profile")
        cdp_url = browser.get("cdp_url") or env.get("BU_CDP_URL") or env.get("BU_CDP_WS")
        if browser.get("dedicated") is False:
            return None, None, None, "dedicated browser/profile"
    else:
        return None, None, None, "dedicated browser/profile"

    mode = mode.strip().lower()
    profile = _string(profile).strip() if profile else env.get("QA_BROWSER_PROFILE", "").strip() or None
    if mode in HOST_NATIVE_MODES:
        return mode, profile, cdp_url, "host-native adapter preferred"
    if mode in {"personal", "personal-profile"} or (profile and "personal" in profile.lower()):
        return None, None, None, "dedicated browser/profile"
    if mode in HEADLESS_MODES and not cdp_url:
        return None, None, None, "dedicated browser/profile"
    if mode in HEADED_MODES and not profile:
        return None, None, None, "dedicated browser/profile"
    if mode not in HEADLESS_MODES | HEADED_MODES:
        return None, None, None, "dedicated browser/profile"
    return mode, profile, cdp_url, None


def _path_contains(path: Path, root: Path) -> bool:
    try:
        path.relative_to(root)
        return True
    except ValueError:
        return False


def _has_symlink_between(path: Path, ancestor: Path) -> bool:
    current = path
    while True:
        if current.exists() or current.is_symlink():
            try:
                if current.is_symlink():
                    return True
            except OSError:
                return True
        if current == ancestor:
            return False
        if current.parent == current or not _path_contains(current, ancestor):
            return True
        current = current.parent


def _evidence_destination(
    evidence_dir: str | Path,
    checkout_root: str | Path,
    evidence_root: str | Path | None,
) -> tuple[Path, Path]:
    checkout = Path(checkout_root).absolute()
    root = Path(evidence_root or checkout / ".qa-evidence")
    if not root.is_absolute():
        root = checkout / root
    destination = Path(evidence_dir)
    if not destination.is_absolute():
        destination = checkout / destination
    root = root.absolute()
    destination = destination.absolute()
    if any(part == ".." for part in destination.relative_to(checkout).parts) if _path_contains(destination, checkout) else True:
        raise AdapterInputError("evidence destination has a lexical escape")
    if not _path_contains(root, checkout) or not _path_contains(destination, root):
        raise AdapterInputError("evidence destination is outside the checkout-owned disposable root")
    if _has_symlink_between(root, checkout) or _has_symlink_between(destination, root):
        raise AdapterInputError("evidence destination traverses a symbolic link")
    try:
        resolved_checkout = checkout.resolve(strict=True)
        resolved_root = root.resolve(strict=False)
        resolved_destination = destination.resolve(strict=False)
    except OSError as exc:
        raise AdapterInputError("evidence destination cannot be resolved") from exc
    if not _path_contains(resolved_root, resolved_checkout) or not _path_contains(resolved_destination, resolved_root):
        raise AdapterInputError("evidence destination escapes its canonical root")
    return resolved_root, resolved_destination


@contextlib.contextmanager
def _temporary_environment(updates: Mapping[str, str]) -> Iterator[None]:
    previous: dict[str, str | None] = {key: os.environ.get(key) for key in updates}
    try:
        for key, value in updates.items():
            os.environ[key] = value
        yield
    finally:
        for key, value in previous.items():
            if value is None:
                os.environ.pop(key, None)
            else:
                os.environ[key] = value


def _write_evidence(destination: Path, trace: Any, env: Mapping[str, str]) -> str:
    destination.mkdir(parents=True, exist_ok=True)
    target = destination / EVIDENCE_NAME
    if target.is_symlink():
        raise AdapterInputError("evidence destination traverses a symbolic link")
    payload = _bounded_json(trace, env) + "\n"
    fd, temporary = tempfile.mkstemp(prefix=".jev-", dir=destination)
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as handle:
            handle.write(payload)
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temporary, target)
    finally:
        Path(temporary).unlink(missing_ok=True)
    return target.as_posix()


def _relative(path: Path, checkout: Path) -> str:
    try:
        return path.relative_to(checkout).as_posix()
    except ValueError:
        return path.as_posix()


def _state_scope_violation(state: Any) -> bool:
    if not isinstance(state, Mapping):
        return False
    for key in ("out_of_scope", "outside_scope", "blocked", "unsafe"):
        if state.get(key) is True:
            return True
    for key in ("scope", "scope_status", "action_scope"):
        if _string(state.get(key, "")).strip().lower() in {"outside", "out-of-scope", "blocked", "unsafe"}:
            return True
    allowed = state.get("allowed_actions")
    requested = state.get("requested_action")
    if isinstance(allowed, (list, tuple, set)) and requested is not None and requested not in allowed:
        return True
    for key in ("page_content", "provider_output", "model_output", "tool_metadata"):
        nested = state.get(key)
        if isinstance(nested, Mapping) and _state_scope_violation(nested):
            return True
        if isinstance(nested, str) and any(
            marker in nested.lower()
            for marker in ("outside qa scope", "outside the supplied goal", "out-of-scope action")
        ):
            return True
    return False


def _is_mutation(state: Any) -> bool:
    if not isinstance(state, Mapping):
        return False
    if state.get("mutates") is True or state.get("mutation") is True:
        return True
    action = state.get("action")
    if isinstance(action, Mapping) and action.get("mutates") is True:
        return True
    return _string(state.get("operation", "")).upper() in {"CLICK", "TYPE_TEXT", "SELECT", "UPLOAD", "SUBMIT"} and bool(state.get("mutation"))


def select_existing_adapter(result: Mapping[str, Any], existing_adapter: str) -> str:
    """Select the consumer adapter only for Jev preflight unavailability."""
    return existing_adapter if result.get("status") == "unavailable" else _string(result.get("adapter", ADAPTER))


def external_oracle_verdict(result: Mapping[str, Any], independent_readback_matches: bool) -> str:
    """Apply a consuming-project oracle result; Jev itself never calls this function."""
    if result.get("status") == "completed" and independent_readback_matches:
        return "pass"
    return "not-passed"


def run_jev(
    url: str,
    goal: str,
    *,
    evidence_dir: str | Path,
    checkout_root: str | Path,
    evidence_root: str | Path | None = None,
    browser: Any = None,
    existing_adapter: str = "existing",
    env: Mapping[str, str] | None = None,
    agent_factory: Callable[[str, str], Any] | None = None,
    module_available: bool | Callable[[], bool] | None = None,
    harness_available: bool | Callable[[], bool] | None = None,
) -> dict[str, Any]:
    """Execute one optional Jev attempt and return one bounded, secret-free result."""
    effective_env = dict(os.environ if env is None else env)
    try:
        root, destination = _evidence_destination(evidence_dir, checkout_root, evidence_root)
    except AdapterInputError as exc:
        return _result("invalid", limitation=str(exc), env=effective_env, execution_path="preflight")
    if not isinstance(url, str) or not _valid_url(url):
        return _result("invalid", limitation="URL must use an http or https scheme", env=effective_env, execution_path="preflight")
    if not isinstance(goal, str) or not goal.strip() or len(goal) > MAX_GOAL_CHARS:
        return _result("invalid", limitation="goal must be a non-empty bounded string", env=effective_env, execution_path="preflight")

    mode, profile, cdp_url, browser_missing = _normalize_browser(browser, effective_env)
    missing: list[str] = []
    if not effective_env.get("TYPESAFE_API_KEY"):
        missing.append("TYPESAFE_API_KEY")
    if not effective_env.get("AI_GATEWAY_API_KEY"):
        missing.append("AI_GATEWAY_API_KEY")
    if browser_missing:
        missing.append(browser_missing)
    elif mode in HOST_NATIVE_MODES:
        return _result(
            "unavailable",
            limitation="host-native adapter preferred; Jev protocol bridge is not provided",
            env=effective_env,
            fallback_adapter=existing_adapter,
            execution_path=f"consumer-declared {mode} adapter",
        )
    if not _callable_or_bool(module_available, _module_available):
        missing.append("jev_ultrafast module")
    if not _callable_or_bool(harness_available, _harness_available):
        missing.append("Browser Harness")
    if missing:
        return _result(
            "unavailable",
            limitation="missing prerequisites: " + ", ".join(dict.fromkeys(missing)),
            env=effective_env,
            fallback_adapter=existing_adapter,
            execution_path="preflight",
        )

    factory = agent_factory or _default_agent_factory
    states: list[Any] = []
    mutations = 0
    captured_stdout, captured_stderr = io.StringIO(), io.StringIO()
    error_text = ""
    terminal = "failed"
    limitation = "Jev Ultrafast ended without DONE"
    updates = {
        "TEXT_MODEL_API_KEY": effective_env["AI_GATEWAY_API_KEY"],
        "TEXT_MODEL_BASE_URL": effective_env.get("TEXT_MODEL_BASE_URL", TEXT_HELPER_URL),
        "TEXT_MODEL": effective_env.get("TEXT_MODEL", TEXT_HELPER_MODEL),
        "TEXT_MODEL_REASONING": effective_env.get("TEXT_MODEL_REASONING", "none"),
    }
    if mode in HEADLESS_MODES:
        updates["BU_CDP_URL"] = effective_env.get("BU_CDP_URL", "") or (cdp_url or "")
        updates["BU_CDP_WS"] = effective_env.get("BU_CDP_WS", "")
    try:
        with _temporary_environment(updates), contextlib.redirect_stdout(captured_stdout), contextlib.redirect_stderr(captured_stderr):
            agent = factory(url, goal)
            with agent as active:
                for index, state in enumerate(active.run(), start=1):
                    states.append(state)
                    if _state_scope_violation(state):
                        terminal = "blocked"
                        limitation = "requested action is outside the supplied goal or QA browser scope"
                        if hasattr(active, "stop"):
                            active.stop()
                        break
                    if _is_mutation(state):
                        mutations += 1
                    status = _string(state.get("status", "")) if isinstance(state, Mapping) else ""
                    if status.upper() in {"DONE", "COMPLETED"}:
                        terminal = "completed"
                        limitation = ""
                        break
                    if index >= MAX_STEPS:
                        limitation = f"bounded run stopped after {MAX_STEPS} states"
                        break
    except Exception as exc:  # provider/browser errors stay inside the result boundary
        error_text = _string(exc)
        terminal = "failed"
        limitation = "provider or browser execution failed"

    trace = {
        "adapter": ADAPTER,
        "execution_path": "jev_ultrafast.Agent via Browser Harness/CDP",
        "browser_mode": mode,
        "browser_profile": profile,
        "states": states,
        "captured_stdout": captured_stdout.getvalue(),
        "captured_stderr": captured_stderr.getvalue(),
        "error": error_text,
    }
    try:
        evidence_path = _write_evidence(destination, trace, effective_env)
    except AdapterInputError as exc:
        return _result("invalid", limitation=str(exc), env=effective_env, execution_path="evidence-write")
    except OSError:
        return _result("failed", evidence=[_relative(destination, Path(checkout_root).absolute())], limitation="evidence write failed", env=effective_env, execution_path="evidence-write")
    result = _result(
        terminal,
        evidence=[_relative(Path(evidence_path), Path(checkout_root).absolute())],
        limitation=limitation,
        env=effective_env,
        execution_path="jev_ultrafast.Agent via Browser Harness/CDP",
        qa_verdict="unverified" if terminal == "completed" else "not-passed",
        independent_oracle_required=True,
        mutations_attempted=mutations,
        mutation_replayed=False,
        fallback_adapter=existing_adapter if terminal == "unavailable" else None,
    )
    return result


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Run one optional Jev Ultrafast QA journey.")
    parser.add_argument("--url", required=True)
    parser.add_argument("--goal", required=True)
    parser.add_argument("--browser", required=True, choices=sorted(HEADLESS_MODES | HEADED_MODES | HOST_NATIVE_MODES | {"personal-profile"}))
    parser.add_argument("--browser-profile")
    parser.add_argument("--checkout-root", default=os.getcwd())
    parser.add_argument("--evidence-root")
    parser.add_argument("--evidence-dir", required=True)
    parser.add_argument("--existing-adapter", default="existing")
    return parser


def main(argv: list[str] | None = None) -> int:
    try:
        args = _parser().parse_args(argv)
        browser: dict[str, str | None] = {"mode": args.browser, "profile": args.browser_profile}
        result = run_jev(
            args.url,
            args.goal,
            evidence_dir=args.evidence_dir,
            checkout_root=args.checkout_root,
            evidence_root=args.evidence_root,
            browser=browser,
            existing_adapter=args.existing_adapter,
        )
    except Exception as exc:
        result = _result("invalid", limitation="invalid adapter input", env=os.environ, execution_path="input")
        _ = exc
    print(json.dumps(result, ensure_ascii=False, sort_keys=True))
    return EXIT_CODES.get(result["status"], 1)


if __name__ == "__main__":
    raise SystemExit(main())
