"""Conditional Graphify context preparation for Deep Review."""

from __future__ import annotations

import hashlib
import sys
from pathlib import Path
from typing import Any

RI_SCRIPTS = Path(__file__).resolve().parent
if str(RI_SCRIPTS) not in sys.path:
    sys.path.insert(0, str(RI_SCRIPTS))

import repository_intelligence as ri  # noqa: E402


def question_hash(question: str) -> str:
    return hashlib.sha256(question.encode("utf-8")).hexdigest()


def _fallback(path: Path, digest: str, reason: str) -> dict[str, str]:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        "\n".join([
            "# Graphify context",
            "",
            "status: degraded",
            f"question_hash: {digest}",
            f"reason: {reason}",
            "",
            "Graphify context is unavailable; use targeted repository inspection.",
        ]) + "\n",
        encoding="utf-8",
    )
    return {"status": "degraded", "path": str(path), "question_hash": digest, "reason": reason}


def _result_error(error: Exception) -> str:
    if isinstance(error, ri.IntelligenceError):
        return ri._redact(error.reason)
    return "Graphify query failed"


def prepare_graphify_context(repo: Path, out: Path, question: str) -> dict[str, str]:
    """Run one bounded Graphify question and persist only its content-safe hash."""
    path = out / "graphify-context.md"
    digest = question_hash(question)
    try:
        result: Any = ri._run_context(repo, "graphify", "query", [question])
    except Exception as error:  # adapter converts expected tool failures to IntelligenceError
        return _fallback(path, digest, _result_error(error))
    if isinstance(result, dict) and result.get("status") == "degraded":
        return _fallback(path, digest, ri._redact(str(result.get("reason") or "Graphify query failed")))
    context = str(result.get("context", "")).strip() if isinstance(result, dict) else ""
    if not context:
        return _fallback(path, digest, "Graphify returned insufficient context")
    status = str(result.get("status", "ready")) if isinstance(result, dict) else "ready"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        "\n".join([
            "# Graphify context",
            "",
            f"status: {status}",
            f"question_hash: {digest}",
            "",
            "Use this bounded architecture context as orientation; verify every claim against the checkout.",
            "",
            "## Architecture context",
            "```text",
            context[:12000],
            "```",
        ]) + "\n",
        encoding="utf-8",
    )
    return {"status": status, "path": str(path), "question_hash": digest}
