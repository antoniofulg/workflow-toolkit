"""Regression tests for the pinned TLC Lean validators and commit contract."""

from __future__ import annotations

import base64
import contextlib
import io
import json
import tempfile
import unittest
import subprocess
from pathlib import Path
import sys

SCRIPTS = Path(__file__).resolve().parents[1] / ".agents/skills/wtk-lean/scripts"
sys.path.insert(0, str(SCRIPTS))

import check_commit  # noqa: E402
import validate_checks  # noqa: E402
import validate_plan  # noqa: E402
import validate_verification  # noqa: E402
import workflow_route  # noqa: E402

FIXTURES = SCRIPTS / "fixtures"
PNG = base64.b64decode("iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mP8/x8AAwMCAO+aGv0AAAAASUVORK5CYII=")


def scaffold(root: Path, *, ui: bool = False) -> Path:
    feature = root / ".specs/features/fixture"
    feature.mkdir(parents=True)
    for name in ("plan.md", "checks.md", "verification.md"):
        body = (FIXTURES / name).read_text(encoding="utf-8")
        if ui:
            body = body.replace("Profile: standard", "Profile: ui").replace("**Profile**: standard", "**Profile**: ui")
            if name == "verification.md":
                body += "\n" + (FIXTURES / "visual.md").read_text(encoding="utf-8")
        (feature / name).write_text(body, encoding="utf-8")
    if ui:
        for name in ("reference.png", "full.png", "viewport.png"):
            (feature / name).write_bytes(PNG)
    return feature


def run_gate(root: Path, gate: str) -> subprocess.CompletedProcess:
    return subprocess.run(
        [sys.executable, str(SCRIPTS / f"{gate}.py"), "fixture", "--root", str(root), "--strict"],
        capture_output=True, text=True,
    )


class WorkflowValidatorTests(unittest.TestCase):
    def test_plan_fixture_passes(self) -> None:
        errors, _warnings = validate_plan.check_file(str(FIXTURES / "plan.md"))
        self.assertEqual(errors, [])

    def test_plan_missing_shape_section_is_rejected(self) -> None:
        source = (FIXTURES / "plan.md").read_text(encoding="utf-8")
        with tempfile.TemporaryDirectory() as raw:
            path = Path(raw) / "plan.md"
            path.write_text(source.replace("## Impact", "## Missing", 1), encoding="utf-8")
            errors, _warnings = validate_plan.check_file(str(path))
        self.assertTrue(any("missing required section: ## Impact" in error for error in errors))

    def test_checks_fixture_passes(self) -> None:
        errors, _warnings, _summary = validate_checks.check_file(str(FIXTURES / "checks.md"))
        self.assertEqual(errors, [])

    def test_checks_missing_proof_is_rejected(self) -> None:
        source = (FIXTURES / "checks.md").read_text(encoding="utf-8")
        with tempfile.TemporaryDirectory() as raw:
            path = Path(raw) / "checks.md"
            path.write_text(source.replace("Proof:", "No proof:", 1), encoding="utf-8")
            errors, _warnings, _summary = validate_checks.check_file(str(path))
        self.assertTrue(any("has no `Proof:` line" in error for error in errors))

    def test_verification_fixture_passes(self) -> None:
        errors, _warnings = validate_verification._check_feature(str(FIXTURES), "fixture")
        self.assertEqual(errors, [])

    def test_surface_accepts_non_http_interfaces_and_outcomes(self) -> None:
        source = (FIXTURES / "plan.md").read_text(encoding="utf-8")
        http_row = "| `POST /webhooks/provider` | the provider envelope as sent | `{}` · `{error}` | `200`, `409`, `422` |"
        self.assertIn(http_row, source)
        rows = {
            "billing suspend <account>": "| `billing suspend <account>` | account id | summary line | exit `0`, exit `2`, `AccountNotFound` |",
            "billing.subscription_suspended": "| `billing.subscription_suspended` | charge result | event payload | `emitted`, `skipped` |",
        }
        for interface, row in rows.items():
            with self.subTest(interface=interface), tempfile.TemporaryDirectory() as raw:
                root = Path(raw)
                feature = scaffold(root)
                (feature / "plan.md").write_text(source.replace(http_row, row), encoding="utf-8")
                errors, _warnings = validate_plan.check_file(str(feature / "plan.md"))
                self.assertEqual(errors, [])
                _errors, warnings, _profile = validate_checks.check_file(str(feature / "checks.md"))
                self.assertTrue(any(f"`{interface}`" in warning for warning in warnings), warnings)
                checks = feature / "checks.md"
                checks.write_text(checks.read_text(encoding="utf-8") + f"\nCovers `{interface}`.\n", encoding="utf-8")
                _errors, warnings, _profile = validate_checks.check_file(str(checks))
                self.assertFalse(any(f"`{interface}`" in warning for warning in warnings), warnings)
                empty = source.replace(http_row, row.rsplit("|", 2)[0] + "|  |")
                (feature / "plan.md").write_text(empty, encoding="utf-8")
                errors, _warnings = validate_plan.check_file(str(feature / "plan.md"))
                self.assertTrue(any("Outcomes names no outcome" in error for error in errors), errors)

    def test_surface_rejects_placeholder_outcomes(self) -> None:
        source = (FIXTURES / "plan.md").read_text(encoding="utf-8")
        outcomes = "| `200`, `409`, `422` |"
        for placeholder in ("-", "n/a", "none", "TBD", "`-` · n/a"):
            with self.subTest(placeholder=placeholder), tempfile.TemporaryDirectory() as raw:
                feature = scaffold(Path(raw))
                (feature / "plan.md").write_text(source.replace(outcomes, f"| {placeholder} |"), encoding="utf-8")
                errors, _warnings = validate_plan.check_file(str(feature / "plan.md"))
                self.assertTrue(any("Outcomes names no outcome" in error for error in errors), errors)

    def test_fault_disposition_accepts_only_killed_or_reasoned_survivors(self) -> None:
        source = (FIXTURES / "verification.md").read_text(encoding="utf-8")
        row = "| `app/webhooks/ingest.rb:31` | killed |"
        self.assertIn(row, source)
        cases = {
            "killed": True,
            "equivalent - same result on every input": True,
            "arid - logging only": True,
            "survived": False,
            "no": False,
            "equivalent": False,
            "arid - n/a": False,
        }
        for value, accepted in cases.items():
            with self.subTest(disposition=value), tempfile.TemporaryDirectory() as raw:
                feature = scaffold(Path(raw))
                (feature / "verification.md").write_text(
                    source.replace(row, f"| `app/webhooks/ingest.rb:31` | {value} |"), encoding="utf-8"
                )
                errors, _warnings = validate_verification._check_feature(str(feature), "fixture")
                self.assertEqual(errors == [], accepted, errors)

    def test_checks_rejects_plan_without_approval(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            root = Path(raw)
            feature = scaffold(root)
            plan = feature / "plan.md"
            source = plan.read_text(encoding="utf-8")
            plan.write_text(source[:source.index("## Approval")] + source[source.index("## Problem"):], encoding="utf-8")
            result = run_gate(root, "validate_checks")
            self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
            self.assertIn("plan.md: no `## Approval` receipt with a non-empty `- Decision:` line", result.stdout)

    def test_checks_only_rejects_missing_approval(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            root = Path(raw)
            feature = scaffold(root)
            (feature / "plan.md").unlink()
            result = run_gate(root, "validate_checks")
            self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
            self.assertIn("checks.md: no `## Approval` receipt with a non-empty `- Decision:` line", result.stdout)

    def test_checks_accepts_recorded_approval(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            root = Path(raw)
            feature = scaffold(root)
            result = run_gate(root, "validate_checks")
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            self.assertNotIn("Approval", result.stdout)

    def test_checks_rejects_empty_decision(self) -> None:
        for decision in ("- Decision:", "- Decision:   ", "- Decision: <actual user words>", "- Decision: -"):
            with self.subTest(decision=decision), tempfile.TemporaryDirectory() as raw:
                root = Path(raw)
                feature = scaffold(root)
                plan = feature / "plan.md"
                source = plan.read_text(encoding="utf-8")
                line = next(ln for ln in source.splitlines() if ln.startswith("- Decision:"))
                plan.write_text(source.replace(line, decision), encoding="utf-8")
                result = run_gate(root, "validate_checks")
                self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
                self.assertIn("non-empty `- Decision:` line", result.stdout)

    def test_approval_checks_only_uses_intent_without_synthetic_plan(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            root = Path(raw)
            feature = scaffold(root)
            plan = (feature / "plan.md").read_text(encoding="utf-8")
            receipt = plan[plan.index("## Approval"):plan.index("## Problem")]
            (feature / "plan.md").unlink()
            checks = feature / "checks.md"
            original = checks.read_text(encoding="utf-8")
            checks.write_text(original + "\n" + receipt, encoding="utf-8")
            for gate in ("validate_checks", "validate_verification"):
                result = run_gate(root, gate)
                self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            self.assertFalse((feature / "plan.md").exists())
            checks.write_text((original + "\n" + receipt).replace("## Intent", "## Missing"), encoding="utf-8")
            for gate in ("validate_checks", "validate_verification"):
                result = run_gate(root, gate)
                self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
                self.assertIn("## Intent", result.stdout)

    def test_approval_is_not_required_before_presenting_plan(self) -> None:
        source = (FIXTURES / "plan.md").read_text(encoding="utf-8")
        with tempfile.TemporaryDirectory() as raw:
            path = Path(raw) / "plan.md"
            path.write_text("# Dunning\n\n## Problem" + source.split("## Problem", 1)[1], encoding="utf-8")
            errors, _warnings = validate_plan.check_file(str(path))
            self.assertEqual(errors, [])

    def test_visual_provenance_and_results_reach_completion_cli(self) -> None:
        fields = ("Source/revision", "Source scale", "Implementation revision", "Screen/state",
                  "Viewport/scroll", "Environment", "Reference capture", "Full-page capture",
                  "Viewport capture", "Comparison", "Result")
        with tempfile.TemporaryDirectory() as raw:
            root = Path(raw)
            feature = scaffold(root, ui=True)
            report = feature / "verification.md"
            original = report.read_text(encoding="utf-8")
            accepted = run_gate(root, "validate_verification")
            self.assertEqual(accepted.returncode, 0, accepted.stdout + accepted.stderr)
            for index, field in enumerate(fields):
                with self.subTest(missing=field):
                    lines = original.splitlines()
                    cells = lines[-1].split("|")
                    cells[index + 1] = " - "
                    lines[-1] = "|".join(cells)
                    report.write_text("\n".join(lines), encoding="utf-8")
                    result = run_gate(root, "validate_verification")
                    self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
                    self.assertIn("visual fidelity", result.stdout)
            for title, body in {
                "missing table": original.split("## Visual fidelity", 1)[0],
                "fenced table": original.replace("## Visual fidelity", "```markdown\n## Visual fidelity") + "\n```\n",
                "invalid second row": original + original.splitlines()[-1].replace("| viewport.png |", "| missing.png |") + "\n",
                "old schema": original.replace("Source/revision", "Source").replace("Viewport/scroll", "Viewport"),
                "no scale": original.replace("scale: 1;", ""),
                "zero scale": original.replace("scale: 1;", "scale: 0;"),
                "empty runtime": original.replace("runtime: Chromium 130 on Linux;", "runtime: -;"),
                "no runtime": original.replace("runtime: Chromium 130 on Linux;", ""),
                "no scroll": original.replace("390x844; scroll: 0,0", "390x844"),
                "bad viewport": original.replace("390x844", "0x844"),
                "bad source scale": original.replace("| 1x |", "| 0x |"),
                "template revision": original.replace("| e4f5a6b |", "| <implementation revision> |"),
                "ellipsis revision": original.replace("| e4f5a6b |", "| ... |"),
                "unicode ellipsis revision": original.replace("| e4f5a6b |", "| … |"),
                "material drift": original.replace("| PASS |", "| FAIL |"),
                "uninspected": original.replace("| PASS |", "| unverified |"),
                "contradiction": original.replace("| none | - |", "| dark theme replaces light source | - |"),
            }.items():
                with self.subTest(title=title):
                    report.write_text(body, encoding="utf-8")
                    result = run_gate(root, "validate_verification")
                    self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
            report.write_text(original, encoding="utf-8")
            for name in ("reference.png", "full.png", "viewport.png"):
                with self.subTest(missing_file=name):
                    capture = feature / name
                    capture.unlink()
                    result = run_gate(root, "validate_verification")
                    self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
                    self.assertIn("not an existing local file", result.stdout)
                    capture.write_bytes(PNG)

    def test_visual_mixed_table_schemas_cannot_hide_invalid_evidence(self) -> None:
        fragment = (FIXTURES / "visual.md").read_text(encoding="utf-8")
        valid = fragment.split("## Visual fidelity\n\n", 1)[1]
        legacy = (
            "| Source | Screen/state | Viewport | Captures | Comparison | Result |\n"
            "| --- | --- | --- | --- | --- | --- |\n"
            "| mockup revision 1 | /listings open | 390x844 | missing.png | inspected | PASS |\n"
        )
        invalid_tables = {
            "legacy": legacy,
            "missing column": valid.replace("| Source scale |", "| Scale |"),
            "duplicate column": valid.replace("| Source scale |", "| Implementation revision |"),
            "empty legacy": "\n".join(legacy.splitlines()[:2]) + "\n",
        }
        for title, invalid in invalid_tables.items():
            for first, second in ((valid, invalid), (invalid, valid)):
                with self.subTest(schema=title,invalid_first=first == invalid), tempfile.TemporaryDirectory() as raw:
                    root = Path(raw)
                    feature = scaffold(root, ui=True)
                    report = feature / "verification.md"
                    prefix = report.read_text(encoding="utf-8").split("## Visual fidelity", 1)[0]
                    report.write_text(prefix + "## Visual fidelity\n\n" + first + "\n" + second, encoding="utf-8")
                    result = run_gate(root, "validate_verification")
                    self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
                    self.assertIn("unsupported or incomplete provenance columns", result.stdout)
        with tempfile.TemporaryDirectory() as raw:
            root = Path(raw)
            feature = scaffold(root, ui=True)
            report = feature / "verification.md"
            report.write_text(
                report.read_text(encoding="utf-8") + "\n" + valid.replace("/listings populated", "/listings filters open"),
                encoding="utf-8",
            )
            result = run_gate(root, "validate_verification")
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_visual_paths_are_literal_local_data(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            root = Path(raw)
            feature = scaffold(root, ui=True)
            report = feature / "verification.md"
            original = report.read_text(encoding="utf-8")
            local = feature / "captures with spaces"
            local.mkdir()
            (local / "reference.png").write_bytes(PNG)
            for path in ("`captures with spaces/reference.png`", str(local / "reference.png")):
                report.write_text(original.replace("| reference.png |", f"| {path} |"), encoding="utf-8")
                result = run_gate(root, "validate_verification")
                self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            for path in ("https://example.test/reference.png", "captures with spaces", "$(touch injected).png"):
                report.write_text(original.replace("| reference.png |", f"| {path} |"), encoding="utf-8")
                result = run_gate(root, "validate_verification")
                self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
                self.assertIn("not an existing local file", result.stdout)
            self.assertFalse((root / "injected").exists())
            self.assertFalse((feature / "injected").exists())

    def test_visual_non_ui_profiles_do_not_require_captures(self) -> None:
        for profile in ("light", "standard"):
            with self.subTest(profile=profile), tempfile.TemporaryDirectory() as raw:
                root = Path(raw)
                feature = scaffold(root)
                for name in ("checks.md", "verification.md"):
                    path = feature / name
                    path.write_text(path.read_text(encoding="utf-8").replace("standard", profile), encoding="utf-8")
                result = run_gate(root, "validate_verification")
                self.assertEqual(result.returncode, 0, result.stdout + result.stderr)


class CommitContractTests(unittest.TestCase):
    """The Lean build contract requires Conventional Commits."""

    def _exit_code(self, message: str) -> int:
        with contextlib.redirect_stdout(io.StringIO()):
            return check_commit.main(["--message", message])

    def test_conventional_message_is_accepted(self) -> None:
        self.assertEqual(self._exit_code("feat(wtk): add lean router"), 0)

    def test_invalid_type_is_rejected(self) -> None:
        self.assertEqual(self._exit_code("release(wtk): publish package"), 1)
        self.assertEqual(self._exit_code("chore(wtk): tidy files"), 1)

    def test_breaking_marker_needs_no_footer(self) -> None:
        self.assertEqual(self._exit_code("feat(wtk)!: rename public command"), 0)
        self.assertEqual(
            self._exit_code("feat(wtk)!: rename public command\n\nBREAKING CHANGE: old command removed"),
            0,
        )


if __name__ == "__main__":
    unittest.main()
