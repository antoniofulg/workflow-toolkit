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

    def test_approval_receipts_reach_both_cli_gates(self) -> None:
        source = (FIXTURES / "plan.md").read_text(encoding="utf-8")
        receipt, rest = source.split("## Problem", 1)
        invalid = {
            "absent": "# Dunning\n\n## Problem" + rest,
            "empty": source.replace("## Approval", "## Approval\n\n## Empty", 1),
            "fenced example": "# Dunning\n\n```markdown\n" + receipt + "```\n\n## Problem" + rest,
            "tilde fenced example": "# Dunning\n\n~~~markdown\n" + receipt + "~~~\n\n## Problem" + rest,
            "placeholder": source.replace("User approved the dunning plan in TLC-412 comment 7.", "<actual user decision>"),
            "bracket placeholder": source.replace("dunning-plan-3 on base a1b2c3d", "[reviewed revision]"),
            "example": source.replace("User approved the dunning plan in TLC-412 comment 7.", "Example: user approves"),
            "unfenced template": source.replace("## Approval", "## Approval\n\nTemplate: proposed receipt"),
            "plain placeholder": source.replace("dunning-plan-3 on base a1b2c3d", "reviewed revision"),
            "duplicate decision": source.replace("## Approval", "## Approval\n\n- Decision: user approved another scope"),
            "execution settings only": source.replace("## Approval", "## Execution selection approval"),
            "empty scope": source.replace("Both dunning slices and local implementation/commits; no remote delivery.", ""),
            "no source or date": "\n".join(line for line in source.splitlines() if not line.startswith(("- Source:", "- Date:"))),
        }
        for title, plan in invalid.items():
            with self.subTest(title=title), tempfile.TemporaryDirectory() as raw:
                root = Path(raw)
                feature = scaffold(root)
                (feature / "plan.md").write_text(plan, encoding="utf-8")
                for gate in ("validate_checks", "validate_verification"):
                    result = run_gate(root, gate)
                    self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
                    self.assertIn("approval", result.stdout.lower())
        with tempfile.TemporaryDirectory() as raw:
            root = Path(raw)
            scaffold(root)
            for gate in ("validate_checks", "validate_verification"):
                result = run_gate(root, gate)
                self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_approval_execution_route_does_not_authorize_feature_shape(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            root = Path(raw).resolve()
            feature = scaffold(root)
            plan = feature / "plan.md"
            plan.write_text(plan.read_text(encoding="utf-8").replace("## Approval", "## Awaiting feature review"), encoding="utf-8")
            stages = {"implementation": {
                "provider": "codex", "model": "gpt-6.1-sol", "effort": "max",
                "rationale": "One sequential builder for the fixture.", "limitations": [],
            }}
            snapshot = {
                "version": 2, "feature": "fixture", "checkout": str(root), "stages": stages,
                "approval": {"status": "confirmed", "reference": "Fixture user reply: accept these execution settings only.", "stages": stages},
                "git_head": "a1b2c3d", "profile": None, "verification_profile": "standard",
                "deep_review": {"cadence": "skip", "groups": []},
                "parallelization": {"mode": "disabled"},
            }
            self.assertEqual(workflow_route.validate_snapshot(root, "fixture", snapshot), snapshot)
            (feature / "workflow.json").write_text(json.dumps(snapshot), encoding="utf-8")
            for gate in ("validate_checks", "validate_verification"):
                result = run_gate(root, gate)
                self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
                self.assertIn("approval missing usable decision", result.stdout)

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

    def test_approval_plan_cannot_be_bypassed_by_checks_receipt(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            root = Path(raw)
            feature = scaffold(root)
            plan = feature / "plan.md"
            source = plan.read_text(encoding="utf-8")
            receipt = source[source.index("## Approval"):source.index("## Problem")]
            plan.write_text(source.replace("## Approval", "## Awaiting approval"), encoding="utf-8")
            checks = feature / "checks.md"
            checks.write_text(checks.read_text(encoding="utf-8") + receipt, encoding="utf-8")
            for gate in ("validate_checks", "validate_verification"):
                result = run_gate(root, gate)
                self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
                self.assertIn("plan.md: approval", result.stdout)

    def test_approval_is_not_required_before_presenting_plan(self) -> None:
        source = (FIXTURES / "plan.md").read_text(encoding="utf-8")
        with tempfile.TemporaryDirectory() as raw:
            path = Path(raw) / "plan.md"
            path.write_text("# Dunning\n\n## Problem" + source.split("## Problem", 1)[1], encoding="utf-8")
            errors, _warnings = validate_plan.check_file(str(path))
            self.assertEqual(errors, [])

    def test_visual_provenance_and_results_reach_completion_cli(self) -> None:
        fields = ("Source/revision", "Source scale", "Implementation revision", "Route/state",
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
                "no DPR": original.replace("DPR: 1;", ""),
                "zero DPR": original.replace("DPR: 1;", "DPR: 0;"),
                "empty browser": original.replace("browser: Chromium 130;", "browser: -;"),
                "empty OS": original.replace("OS: Linux;", "OS: n/a;"),
                "no scroll": original.replace("390x844; scroll: 0,0", "390x844"),
                "bad viewport": original.replace("390x844", "0x844"),
                "bad source scale": original.replace("| 1x |", "| 0x |"),
                "template revision": original.replace("| e4f5a6b |", "| <implementation revision> |"),
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

    def test_breaking_marker_requires_footer(self) -> None:
        self.assertEqual(self._exit_code("feat(wtk)!: rename public command"), 1)
        self.assertEqual(
            self._exit_code("feat(wtk)!: rename public command\n\nBREAKING CHANGE: old command removed"),
            0,
        )


if __name__ == "__main__":
    unittest.main()
