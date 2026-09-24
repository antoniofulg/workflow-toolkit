"""Best-effort Graft context preparation for wtk-deep-review prompts."""

from __future__ import annotations

import json
import hashlib
import sys
import os
from pathlib import Path
from typing import Any

RI_SCRIPTS = Path(__file__).resolve().parent
if str(RI_SCRIPTS) not in sys.path:
    sys.path.insert(0, str(RI_SCRIPTS))

import repository_intelligence as ri  # noqa: E402

FALLBACK_LINE = "Graft context is unavailable; use plain repository inspection."
PARTIAL_LINE = "Graft context is partial; use targeted repository inspection for uncovered paths."


def _fallback(path: Path, reason: str, dot_paths: list[str], digest: str) -> dict[str, str]:
    lines = [
        "# Graft context",
        "",
        "status: fallback",
        f"question_hash: {digest}",
        f"reason: {reason}",
        "",
        FALLBACK_LINE,
    ]
    if dot_paths:
        lines.extend([
            "",
            "Graft does not index dot-directories; inspect these paths plainly:",
            *[f"- `{item}`" for item in dot_paths],
        ])
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return {"status": "fallback", "path": str(path), "question_hash": digest, "reason": reason}


def _result_error(error: Exception) -> str:
    if isinstance(error, ri.IntelligenceError):
        return ri._redact(error.reason)
    return "Graft context failed"


def _context(result: Any) -> str:
    return str(result.get("context", "")).strip() if isinstance(result, dict) else ""


def _reason(result: Any, default: str) -> str:
    if not isinstance(result, dict):
        return default
    return ri._redact(str(result.get("reason") or default))


def prepare_graft_context(repo: Path, out: Path, selected_paths: list[str]) -> dict[str, str]:
    """Build and query Graft through the shared adapter without blocking review."""
    context_path = out / "graft-context.md"
    dot_paths = [path for path in selected_paths if path.startswith(".") or path.startswith("graft/")]
    visible_paths = [path for path in selected_paths if path not in dot_paths]
    query = " ".join(visible_paths[:20]) or "repository structure"
    digest = hashlib.sha256(query.encode("utf-8")).hexdigest()
    try:
        mapped = ri._run_context(repo, "graft", "map", [])
    except Exception as error:  # adapter converts expected tool failures to IntelligenceError
        return _fallback(context_path, _result_error(error), dot_paths, digest)
    if isinstance(mapped, dict) and mapped.get("status") == "degraded":
        return _fallback(context_path, _reason(mapped, "Graft map failed"), dot_paths, digest)

    try:
        asked = ri._run_context(repo, "graft", "ask", ["--json", "--limit", "8", query])
    except Exception as error:
        asked = None
        ask_reason = _result_error(error)
    else:
        ask_reason = _reason(asked, "Graft symbol lookup failed")

    symbols: list[str] = []
    asked_context = _context(asked)
    if asked_context:
        try:
            hits = json.loads(asked_context).get("hits", [])
            symbols = [
                str(hit.get("title", "")).split(" · ", 1)[0]
                for hit in hits
                if hit.get("kind") == "symbol"
            ][:3]
        except (TypeError, ValueError, json.JSONDecodeError):
            symbols = []

    partial = mapped.get("status") == "partial" if isinstance(mapped, dict) else False
    partial = partial or (asked.get("status") == "partial" if isinstance(asked, dict) else False)
    lines = [
        "# Graft context",
        "",
        "status: partial" if partial else ("status: ready" if asked_context and not dot_paths else "status: ready-with-fallback"),
        f"question_hash: {digest}",
        "",
        "Use this map as review orientation; verify every claim against the checkout.",
        "",
        "## Repository map",
        "```text",
        _context(mapped)[:12000],
        "```",
    ]
    if asked_context:
        lines.extend(["", "## Relevant symbols", "```text", asked_context[:12000], "```"])
    else:
        lines.extend(["", ask_reason, "Use plain repository inspection for relevant symbols and callers."])

    blast_failed = False
    blast_partial = False
    for symbol in symbols:
        try:
            callers = ri._run_context(repo, "graft", "callers", ["--json", "--depth", "1", symbol])
        except Exception:
            blast_failed = True
            continue
        callers_context = _context(callers)
        blast_partial = blast_partial or (isinstance(callers, dict) and callers.get("status") == "partial")
        if callers_context:
            lines.extend(["", f"### `{symbol}`", "```text", callers_context[:6000], "```"])
        else:
            blast_failed = True
    if blast_failed:
        lines.extend(["", "Graft blast-radius lookup failed; use plain repository inspection for callers."])
    partial = partial or blast_partial
    if partial:
        lines[2] = "status: partial"
        lines.extend(["", PARTIAL_LINE])
    if dot_paths:
        lines.extend([
            "",
            "Graft does not index dot-directories; use plain repository inspection for:",
            *[f"- `{item}`" for item in dot_paths],
        ])
    if not _context(mapped):
        return _fallback(context_path, "Graft returned insufficient context", dot_paths, digest)
    context_path.parent.mkdir(parents=True, exist_ok=True)
    context_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    status = "partial" if partial else ("ready" if asked_context and not dot_paths and not blast_failed else "ready-with-fallback")
    return {"status": status, "path": str(context_path), "question_hash": digest}


def graft_binary(repo: Path) -> str | None:
    """Compatibility inspection helper for callers that need local tool discovery."""
    local = repo / "node_modules" / ".bin" / "graft"
    package = repo / "node_modules" / "@nanonets" / "graft" / "package.json"
    if not local.is_file() or not package.is_file() or not os.access(local, os.X_OK):
        return None
    try:
        manifest = json.loads(package.read_text(encoding="utf-8"))
        local.resolve(strict=True).relative_to(repo.resolve() / "node_modules")
        package.parent.resolve(strict=True).relative_to(repo.resolve() / "node_modules")
    except (OSError, ValueError, json.JSONDecodeError):
        return None
    return str(local) if manifest.get("version") == ri.GRAFT_VERSION else None
