#!/usr/bin/env python3
"""Optional Jev QA boundary for a consuming project's non-consequential fixtures.

The consumer installs Jev Ultrafast and Browser Harness. This wrapper only validates the declared
fixture/CDP boundary, aliases the Vercel text-helper key in process memory, calls Agent.run once,
and writes an allowlisted trace. It never assigns a QA pass verdict.
"""

from __future__ import annotations

import argparse
import contextlib
import importlib.util
import io
import json
import os
from pathlib import Path
import re
import shutil
import tempfile
from typing import Any, Callable, Iterable, Iterator, Mapping
from urllib.parse import urlparse


ADAPTER = "jev-ultrafast"
TEXT_HELPER_URL = "https://ai-gateway.vercel.sh/v1"
TEXT_HELPER_MODEL = "inception/mercury-2.5"
MAX_URL_CHARS = 2048
MAX_GOAL_CHARS = 4000
MAX_STEPS = 32
MAX_TRACE_CHARS = 12000
EVIDENCE_NAME = "jev-ultrafast-attempt.json"
EXIT_CODES = {"completed": 0, "unavailable": 2, "failed": 1, "invalid": 2}
REDACT_ENV_NAMES = ("TYPESAFE_API_KEY", "AI_GATEWAY_API_KEY", "TEXT_MODEL_API_KEY")
FALLBACK_ORDER = ("playwright-mcp", "declared-orca", "declared-maestri", "manual")
SAFE_MODES = {"headless", "headed"}
SAFE_STATUSES = {"RUNNING", "DONE", "COMPLETED", "FAILED"}
SAFE_OPERATIONS = {"CLICK", "TYPE_TEXT", "SELECT", "UPLOAD", "SUBMIT", "NAVIGATE", "OBSERVE"}
SENSITIVE_KEY_RE = re.compile(
    r"(?:authorization|cookie|token|credential|secret|password|api[_-]?key|session|csrf|bearer)",
    re.IGNORECASE,
)


class AdapterInputError(ValueError):
    """An input failed closed before a browser or provider was touched."""


def _string(value: Any) -> str:
    return value if isinstance(value, str) else str(value)


def _sensitive_key(key: Any) -> bool:
    return bool(SENSITIVE_KEY_RE.search(_string(key)))


def _secret_values(env: Mapping[str, str]) -> tuple[str, ...]:
    return tuple(value for name in REDACT_ENV_NAMES if (value := env.get(name)) and len(value) >= 4)


def redact(value: Any, env: Mapping[str, str] | None = None) -> Any:
    """Drop credential-shaped fields and replace configured key values recursively."""
    secrets = _secret_values(env or os.environ)
    if isinstance(value, str):
        result = value
        for secret in secrets:
            result = result.replace(secret, "[REDACTED]")
        return result
    if isinstance(value, Mapping):
        return {
            str(key): redact(item, env)
            for key, item in value.items()
            if not _sensitive_key(key)
        }
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


def _valid_cdp(endpoint: str | None) -> bool:
    if not endpoint or len(endpoint) > MAX_URL_CHARS:
        return False
    parsed = urlparse(endpoint)
    return parsed.scheme in {"http", "https", "ws", "wss"} and bool(parsed.netloc)


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


def _normalize_browser(browser: Any, env: Mapping[str, str]) -> tuple[str, str | None]:
    """Return an explicit safe mode and endpoint; no profile/local-browser fallback exists."""
    if browser is None:
        mode, endpoint = "headless", None
    elif isinstance(browser, str):
        mode, endpoint = browser.strip().lower(), None
    elif isinstance(browser, Mapping):
        mode = _string(browser.get("mode", "headless")).strip().lower()
        if any(key in browser for key in ("profile", "browser_profile", "user_data_dir", "personal")):
            raise AdapterInputError("personal/default browser attachment is unsupported")
        endpoint = _string(browser.get("cdp_url", "")).strip() or None
    else:
        raise AdapterInputError("dedicated CDP endpoint is required")

    if mode not in SAFE_MODES:
        raise AdapterInputError("dedicated CDP endpoint is required")
    endpoint = endpoint or env.get("BU_CDP_URL") or env.get("BU_CDP_WS")
    if not _valid_cdp(endpoint):
        raise AdapterInputError("dedicated CDP endpoint is required")
    return mode, endpoint


def _path_contains(path: Path, root: Path) -> bool:
    try:
        path.relative_to(root)
        return True
    except ValueError:
        return False


def _lexically_contained(path: Path, root: Path) -> bool:
    if not _path_contains(path, root):
        return False
    return ".." not in path.relative_to(root).parts


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
    destination = Path(evidence_dir)
    if not root.is_absolute():
        root = checkout / root
    if not destination.is_absolute():
        destination = checkout / destination
    root, destination = root.absolute(), destination.absolute()
    if not _lexically_contained(root, checkout) or not _lexically_contained(destination, root):
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
    fd, temporary = tempfile.mkstemp(prefix=".jev-", dir=destination)
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as handle:
            handle.write(_bounded_json(trace, env) + "\n")
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temporary, target)
    finally:
        Path(temporary).unlink(missing_ok=True)
    return target.as_posix()


def _safe_trace_state(state: Any, index: int) -> dict[str, Any]:
    """Keep evidence to a small public shape; never serialize upstream snapshots."""
    record: dict[str, Any] = {"index": index}
    if not isinstance(state, Mapping):
        return record
    status = _string(state.get("status", "")).upper()
    if status in SAFE_STATUSES:
        record["status"] = status
    elapsed = state.get("elapsed_ms")
    if isinstance(elapsed, (int, float)) and 0 <= elapsed <= 86_400_000:
        record["elapsed_ms"] = elapsed
    operation = _string(state.get("operation", "")).upper()
    if operation in SAFE_OPERATIONS:
        record["operation"] = operation
    return record


def select_fallback_adapter(available: Iterable[str]) -> str:
    """Select the first available consumer-owned fallback in the frozen order."""
    values = {str(item).strip().lower() for item in available}
    return next((candidate for candidate in FALLBACK_ORDER if candidate in values), "manual")


def select_existing_adapter(result: Mapping[str, Any], existing_adapter: str) -> str:
    """Keep compatibility with callers that provide one declared fallback adapter."""
    if result.get("status") != "unavailable":
        return _string(result.get("adapter", ADAPTER))
    return existing_adapter if existing_adapter in FALLBACK_ORDER else "playwright-mcp"


def _declared_fallback(value: str) -> str:
    name = _string(value).strip().lower()
    return name if name in FALLBACK_ORDER else "manual"


def external_oracle_verdict(result: Mapping[str, Any], independent_readback_matches: bool) -> str:
    """Apply a consuming-project oracle result; Jev itself never calls this function."""
    if result.get("status") == "completed" and independent_readback_matches:
        return "pass"
    return "not-passed"


def _unavailable(limitation: str, env: Mapping[str, str], existing_adapter: str) -> dict[str, Any]:
    return _result(
        "unavailable",
        limitation=limitation,
        env=env,
        fallback_order=list(FALLBACK_ORDER),
        fallback_adapter="playwright-mcp",
        declared_fallback=_declared_fallback(existing_adapter),
        execution_path="preflight",
    )


def run_jev(
    url: str,
    goal: str,
    *,
    evidence_dir: str | Path,
    checkout_root: str | Path,
    evidence_root: str | Path | None = None,
    browser: Any = None,
    journey_scope: str | None = None,
    existing_adapter: str = "playwright-mcp",
    env: Mapping[str, str] | None = None,
    agent_factory: Callable[[str, str], Any] | None = None,
    module_available: bool | Callable[[], bool] | None = None,
    harness_available: bool | Callable[[], bool] | None = None,
) -> dict[str, Any]:
    """Run one optional Jev attempt and return one bounded, secret-free result."""
    effective_env = dict(os.environ if env is None else env)
    try:
        _, destination = _evidence_destination(evidence_dir, checkout_root, evidence_root)
    except AdapterInputError as exc:
        return _result("invalid", limitation=str(exc), env=effective_env, execution_path="preflight")
    if not isinstance(url, str) or not _valid_url(url):
        return _result("invalid", limitation="URL must use an http or https scheme", env=effective_env, execution_path="preflight")
    if not isinstance(goal, str) or not goal.strip() or len(goal) > MAX_GOAL_CHARS:
        return _result("invalid", limitation="goal must be a non-empty bounded string", env=effective_env, execution_path="preflight")
    if journey_scope != "non-consequential":
        return _unavailable("policy: non-consequential fixture declaration required", effective_env, existing_adapter)
    if not effective_env.get("TYPESAFE_API_KEY"):
        return _unavailable("missing prerequisite: TYPESAFE_API_KEY", effective_env, existing_adapter)
    if not effective_env.get("AI_GATEWAY_API_KEY"):
        return _unavailable("missing prerequisite: AI_GATEWAY_API_KEY", effective_env, existing_adapter)
    try:
        mode, cdp_endpoint = _normalize_browser(browser, effective_env)
    except AdapterInputError as exc:
        return _unavailable(f"missing prerequisite: {exc}", effective_env, existing_adapter)
    if not _callable_or_bool(module_available, _module_available):
        return _unavailable("missing prerequisite: jev_ultrafast module", effective_env, existing_adapter)
    if not _callable_or_bool(harness_available, _harness_available):
        return _unavailable("missing prerequisite: Browser Harness", effective_env, existing_adapter)

    factory = agent_factory or _default_agent_factory
    states: list[dict[str, Any]] = []
    captured_stdout, captured_stderr = io.StringIO(), io.StringIO()
    terminal = "failed"
    limitation = "provider or browser execution failed"
    run_started = False
    updates = {
        "TEXT_MODEL_API_KEY": effective_env["AI_GATEWAY_API_KEY"],
        "TEXT_MODEL_BASE_URL": effective_env.get("TEXT_MODEL_BASE_URL", TEXT_HELPER_URL),
        "TEXT_MODEL": effective_env.get("TEXT_MODEL", TEXT_HELPER_MODEL),
        "TEXT_MODEL_REASONING": effective_env.get("TEXT_MODEL_REASONING", "none"),
        "BU_CDP_URL": cdp_endpoint if cdp_endpoint.startswith(("http://", "https://")) else "",
        "BU_CDP_WS": cdp_endpoint if cdp_endpoint.startswith(("ws://", "wss://")) else "",
    }
    try:
        with _temporary_environment(updates), contextlib.redirect_stdout(captured_stdout), contextlib.redirect_stderr(captured_stderr):
            agent = factory(url, goal)
            with agent as active:
                run_started = True
                for index, state in enumerate(active.run(), start=1):
                    states.append(_safe_trace_state(state, index))
                    status = _string(state.get("status", "")).upper() if isinstance(state, Mapping) else ""
                    if status in {"DONE", "COMPLETED"}:
                        terminal = "completed"
                        limitation = ""
                        break
                    if index >= MAX_STEPS:
                        limitation = f"bounded run stopped after {MAX_STEPS} states"
                        break
    except Exception:
        terminal = "failed"
        limitation = "provider or browser execution failed"

    trace = {
        "schema": 1,
        "adapter": ADAPTER,
        "status": terminal,
        "browser_mode": mode,
        "run_started": run_started,
        "steps": states,
    }
    try:
        evidence_path = _write_evidence(destination, trace, effective_env)
    except AdapterInputError as exc:
        return _result("invalid", limitation=str(exc), env=effective_env, execution_path="evidence-write")
    except OSError:
        return _result("failed", limitation="evidence write failed", env=effective_env, execution_path="evidence-write")
    checkout = Path(checkout_root).resolve()
    result = _result(
        terminal,
        evidence=[Path(evidence_path).relative_to(checkout).as_posix()],
        limitation=limitation,
        env=effective_env,
        execution_path=f"jev_ultrafast.Agent via Browser Harness/{mode} CDP",
        qa_verdict="unverified" if terminal == "completed" else "not-passed",
        independent_oracle_required=True,
        agent_run_started=run_started,
        fallback_order=list(FALLBACK_ORDER) if terminal != "completed" else None,
    )
    return result


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Run one optional Jev Ultrafast QA journey.")
    parser.add_argument("--url", required=True)
    parser.add_argument("--goal", required=True)
    parser.add_argument("--journey-scope", choices=["non-consequential", "consequential"])
    parser.add_argument("--browser", choices=sorted(SAFE_MODES), default="headless")
    parser.add_argument("--checkout-root", default=os.getcwd())
    parser.add_argument("--evidence-root")
    parser.add_argument("--evidence-dir", required=True)
    parser.add_argument("--existing-adapter", default="playwright-mcp")
    return parser


def main(argv: list[str] | None = None) -> int:
    try:
        args = _parser().parse_args(argv)
        result = run_jev(
            args.url,
            args.goal,
            evidence_dir=args.evidence_dir,
            checkout_root=args.checkout_root,
            evidence_root=args.evidence_root,
            browser=args.browser,
            journey_scope=args.journey_scope,
            existing_adapter=args.existing_adapter,
        )
    except Exception:
        result = _result("invalid", limitation="invalid adapter input", env=os.environ, execution_path="input")
    print(json.dumps(result, ensure_ascii=False, sort_keys=True))
    return EXIT_CODES.get(result["status"], 1)


if __name__ == "__main__":
    raise SystemExit(main())
