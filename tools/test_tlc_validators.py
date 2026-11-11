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
    for name in ("plan.md", "checks.md", "verification.md", "proofs.md"):
        body = (FIXTURES / name).read_text(encoding="utf-8")
        if ui:
            body = body.replace("Profile: standard", "Profile: ui").replace("**Profile**: standard", "**Profile**: ui")
            if name == "verification.md":
                body += "\n" + (FIXTURES / "visual.md").read_text(encoding="utf-8")
        (feature / name).write_text(body, encoding="utf-8")
    if ui:
        (feature / "screens.md").write_text((FIXTURES / "screens.md").read_text(encoding="utf-8"), encoding="utf-8")
        for name in ("reference.png", "full.png", "viewport.png"):
            (feature / name).write_bytes(PNG)
    return feature


def run_gate(root: Path, gate: str, *extra: str) -> subprocess.CompletedProcess:
    return subprocess.run(
        [sys.executable, str(SCRIPTS / f"{gate}.py"), "fixture", "--root", str(root), "--strict", *extra],
        capture_output=True, text=True,
    )


def run_script(root: Path, script: str, *args: str) -> subprocess.CompletedProcess:
    return subprocess.run(
        [sys.executable, str(SCRIPTS / f"{script}.py"), *args, "--root", str(root)],
        capture_output=True, text=True,
    )


def commit_all(root: Path) -> str:
    """Make `root` a git repository with everything committed; return its short HEAD."""
    git = ["git", "-c", "user.name=t", "-c", "user.email=t@example.test", "-c", "commit.gpgsign=false"]
    subprocess.run(["git", "init", "-q"], cwd=root, check=True)
    subprocess.run(["git", "add", "-A"], cwd=root, check=True)
    subprocess.run([*git, "commit", "-q", "-m", "chore: fixture"], cwd=root, check=True)
    return subprocess.run(["git", "rev-parse", "--short", "HEAD"], cwd=root, capture_output=True, text=True, check=True).stdout.strip()


PROOF_CHECKS = """# Proof fixture checks

Profile: standard
Run g: printf 'x\\n' >> .specs/count-g.log; printf '\\033[32mPASS\\033[0m alpha\\n'; echo PASS beta; echo PASS; echo gamma
Plan: n/a

## Checks

**C1** - alpha passes (AC 1)
Proof: run g | PASS alpha

**C2** - beta passes (AC 2)
Proof: run g | PASS beta

**C3** - a lone command passes (AC 3)
Proof: `printf 'x\\n' >> .specs/count-lone.log`
"""


def proof_feature(root: Path, checks: str = PROOF_CHECKS) -> Path:
    feature = root / ".specs/features/fixture"
    feature.mkdir(parents=True)
    (feature / "checks.md").write_text(checks, encoding="utf-8")
    return feature


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

    def test_proofs_run_each_group_once_and_record_head(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            root = Path(raw)
            feature = proof_feature(root)
            head = commit_all(root)
            result = run_script(root, "check_proofs", "fixture")
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            self.assertEqual((root / ".specs/count-g.log").read_text().count("x"), 1)
            self.assertEqual((root / ".specs/count-lone.log").read_text().count("x"), 1)
            report = (feature / "proofs.md").read_text(encoding="utf-8")
            self.assertIn(f"**HEAD**: {head}", report)
            self.assertEqual(report.count("| pass |"), 3, report)

    def test_proofs_match_pass_line_in_order(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            root = Path(raw)
            feature = proof_feature(root)
            commit_all(root)
            result = run_script(root, "check_proofs", "fixture")
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            report = (feature / "proofs.md").read_text(encoding="utf-8")
            self.assertIn("| C1: run g / PASS alpha | pass | PASS alpha |", report)  # the ANSI codes are gone

    def test_proofs_unmatched_line_is_no_test_ran(self) -> None:
        for words in ("beta PASS", "PASS gamma", "PASS alphx"):  # out of order, split across lines, renamed
            with self.subTest(words=words), tempfile.TemporaryDirectory() as raw:
                root = Path(raw)
                feature = proof_feature(root, PROOF_CHECKS.replace("run g | PASS beta", f"run g | {words}"))
                commit_all(root)
                result = run_script(root, "check_proofs", "fixture")
                self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
                report = (feature / "proofs.md").read_text(encoding="utf-8")
                self.assertIn(f"| C2: run g / {words} | no test ran |", report)
                self.assertIn("| C1: run g / PASS alpha | pass |", report)

    def test_proofs_failing_lone_proof_fails_and_writes_all_rows(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            root = Path(raw)
            checks = PROOF_CHECKS + "\n**C4** - a failing command (AC 4)\nProof: `false`\n\n**C5** - a later command (AC 5)\nProof: `true`\n"
            feature = proof_feature(root, checks)
            commit_all(root)
            result = run_script(root, "check_proofs", "fixture")
            self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
            report = (feature / "proofs.md").read_text(encoding="utf-8")
            self.assertIn("| C4: false | fail | exit 1 |", report)
            self.assertIn("| C5: true | pass | exit 0 |", report)
            self.assertIn("`false` - exit 1", report)  # the output section keeps each run's tail

    def test_proofs_refuse_dirty_tree(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            root = Path(raw)
            feature = proof_feature(root)
            commit_all(root)
            (root / "stray.txt").write_text("uncommitted", encoding="utf-8")
            result = run_script(root, "check_proofs", "fixture")
            self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
            self.assertIn("dirty", result.stderr)
            self.assertFalse((root / ".specs/count-g.log").exists())
            self.assertFalse((feature / "proofs.md").exists())

    def test_proofs_unresolved_feature_exits_2(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            result = run_script(Path(raw), "check_proofs", "missing")
            self.assertEqual(result.returncode, 2, result.stdout + result.stderr)

    def test_checks_rejects_run_proof_without_group(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            root = Path(raw)
            feature = scaffold(root)
            checks = feature / "checks.md"
            source = checks.read_text(encoding="utf-8")
            checks.write_text(source.replace("Proof: run billing | test_failed_charge_suspends = .", "Proof: run ghost | test_failed_charge_suspends = ."), encoding="utf-8")
            result = run_gate(root, "validate_checks")
            self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
            self.assertIn("no `Run ghost: <command>` line defines it", result.stdout)
            checks.write_text(source.replace("Proof: run billing | test_failed_charge_suspends = .", "Proof: run billing"), encoding="utf-8")
            result = run_gate(root, "validate_checks")
            self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
            self.assertIn("names no pass line after `|`", result.stdout)

    def _with_build(self, root: Path, build: str) -> None:
        checks = scaffold(root) / "checks.md"
        source = checks.read_text(encoding="utf-8")
        line = next(ln for ln in source.splitlines() if ln.startswith("Build:"))
        checks.write_text(source.replace(line, build), encoding="utf-8")

    def test_checks_execute_runs_build_once(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            root = Path(raw)
            self._with_build(root, "Build: `printf 'x\\n' >> build.log`")
            result = run_gate(root, "validate_checks", "--execute")
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            self.assertEqual((root / "build.log").read_text().count("x"), 1)
            skipped = run_gate(root, "validate_checks")  # off by default
            self.assertEqual(skipped.returncode, 0, skipped.stdout + skipped.stderr)
            self.assertEqual((root / "build.log").read_text().count("x"), 1)

    def test_checks_execute_red_build_stops(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            root = Path(raw)
            self._with_build(root, "Build: `echo compile error; false`")
            result = run_gate(root, "validate_checks", "--execute")
            self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
            self.assertIn("the build was red before any change", result.stdout)
            self.assertIn("compile error", result.stdout)

    def test_checks_rejects_missing_build_line(self) -> None:
        for build in ("", "Build: none"):
            with self.subTest(build=build), tempfile.TemporaryDirectory() as raw:
                root = Path(raw)
                self._with_build(root, build)
                result = run_gate(root, "validate_checks")
                self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
                self.assertIn("Build", result.stdout)
        with tempfile.TemporaryDirectory() as raw:
            root = Path(raw)
            self._with_build(root, "Build: none - the repo has no build step")
            result = run_gate(root, "validate_checks", "--execute")
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_verification_requires_green_proofs_at_head(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            root = Path(raw)
            feature = scaffold(root)
            proofs = feature / "proofs.md"
            head = commit_all(root)
            original = proofs.read_text(encoding="utf-8").replace("**HEAD**: e4f5a6b", f"**HEAD**: {head}")
            proofs.write_text(original, encoding="utf-8")
            accepted = run_gate(root, "validate_verification")
            self.assertEqual(accepted.returncode, 0, accepted.stdout + accepted.stderr)
            proofs.unlink()
            missing = run_gate(root, "validate_verification")
            self.assertEqual(missing.returncode, 1, missing.stdout + missing.stderr)
            self.assertIn("no proofs.md", missing.stdout)
            for title, (body, fragment) in {
                "non-pass row": (original.replace("| pass | exit 0 |", "| no test ran | |", 1), "proofs.md - C4"),
                "failing row": (original.replace("| pass | exit 0 |", "| fail | exit 1 |", 1), "proofs.md - C4"),
                "other HEAD": (original.replace(f"**HEAD**: {head}", "**HEAD**: deadbee"), "was written at deadbee"),
            }.items():
                with self.subTest(title=title):
                    proofs.write_text(body, encoding="utf-8")
                    result = run_gate(root, "validate_verification")
                    self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
                    self.assertIn(fragment, result.stdout)

    def _stamp_head(self, feature: Path, head: str) -> None:
        for name in ("proofs.md", "screens.md"):
            path = feature / name
            if path.exists():
                path.write_text(path.read_text(encoding="utf-8").replace("e4f5a6b", head), encoding="utf-8")

    def test_verification_ui_requires_matching_screens_at_head(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            root = Path(raw)
            feature = scaffold(root, ui=True)
            head = commit_all(root)
            self._stamp_head(feature, head)
            screens = feature / "screens.md"
            original = screens.read_text(encoding="utf-8")
            accepted = run_gate(root, "validate_verification")
            self.assertEqual(accepted.returncode, 0, accepted.stdout + accepted.stderr)
            screens.unlink()
            missing = run_gate(root, "validate_verification")
            self.assertEqual(missing.returncode, 1, missing.stdout + missing.stderr)
            self.assertIn("no screens.md", missing.stdout)
            for title, (body, fragment) in {
                "diverges": (original.replace("| matches |", "| diverges |"), "not matches"),
                "stale HEAD": (original.replace(f"**HEAD**: {head}", "**HEAD**: deadbee"), "screens.md judged deadbee"),
                "no HEAD": (original.replace(f"**HEAD**: {head}\n", ""), "names no `**HEAD**`"),
                "no verdict table": (original.split("| Screen |")[0], "no verdict table"),
            }.items():
                with self.subTest(title=title):
                    screens.write_text(body, encoding="utf-8")
                    result = run_gate(root, "validate_verification")
                    self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
                    self.assertIn(fragment, result.stdout)

    def test_verification_rejects_third_screens_round(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            root = Path(raw)
            feature = scaffold(root, ui=True)
            screens = feature / "screens.md"
            original = screens.read_text(encoding="utf-8")
            for round_number, accepted in ((1, True), (2, True), (3, False)):
                with self.subTest(round=round_number):
                    screens.write_text(original.replace("**Round**: 1", f"**Round**: {round_number}"), encoding="utf-8")
                    result = run_gate(root, "validate_verification")
                    self.assertEqual(result.returncode, 0 if accepted else 1, result.stdout + result.stderr)
                    if not accepted:
                        self.assertIn("there is no round 3", result.stdout)

    def _edit(self, feature: Path, name: str, old: str, new: str) -> None:
        path = feature / name
        source = path.read_text(encoding="utf-8")
        self.assertIn(old, source)
        path.write_text(source.replace(old, new), encoding="utf-8")

    def test_checks_rejects_missing_risk_line(self) -> None:
        for profile, accepted in (("standard", False), ("ui", False), ("light", True)):
            with self.subTest(profile=profile), tempfile.TemporaryDirectory() as raw:
                root = Path(raw)
                feature = scaffold(root)
                checks = (feature / "checks.md").read_text(encoding="utf-8")
                risk = next(ln for ln in checks.splitlines() if ln.startswith("Risk:"))
                self._edit(feature, "checks.md", risk + "\n", "")
                self._edit(feature, "checks.md", "Profile: standard", f"Profile: {profile}")
                result = run_gate(root, "validate_checks")
                self.assertEqual(result.returncode, 0 if accepted else 1, result.stdout + result.stderr)
                if not accepted:
                    self.assertIn("no `Risk:` line", result.stdout)

    def test_verification_requires_holds_yes_per_check(self) -> None:
        row5 = next(ln for ln in (FIXTURES / "verification.md").read_text(encoding="utf-8").splitlines() if ln.startswith("| C5 |"))
        c4 = "`suspended_denies_paid_groups` | yes |"
        cases = {
            "no row for a check": (row5 + "\n", "", "has no row for C5"),
            "no without a closing commit": (c4, "`suspended_denies_paid_groups` | no - asserts the status only |", "no closing commit"),
            "unsure without a closing commit": (c4, "`suspended_denies_paid_groups` | unsure - looser than the claim |", "no closing commit"),
            "a Holds outside the three values": (c4, "`suspended_denies_paid_groups` | maybe |", "expected yes, no or unsure"),
            "no test named": ("| C4 | `test/billing/access_test.rb` `suspended_denies_paid_groups` |", "| C4 | - |", "row C4 names no test"),
        }
        for title, (old, new, fragment) in cases.items():
            with self.subTest(title=title), tempfile.TemporaryDirectory() as raw:
                root = Path(raw)
                feature = scaffold(root)
                self._edit(feature, "verification.md", old, new)
                result = run_gate(root, "validate_verification")
                self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
                self.assertIn(fragment, result.stdout)
        with tempfile.TemporaryDirectory() as raw:  # a non-yes row stands once its closing commit is written
            root = Path(raw)
            feature = scaffold(root)
            self._edit(feature, "verification.md", c4, "`suspended_denies_paid_groups` | no - asserted the status only; closed by a1b2c3d4 |")
            result = run_gate(root, "validate_verification")
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_verification_requires_faults_for_risk_and_unsure(self) -> None:
        c9 = "`missing_subscription_id_is_422` | yes |"
        unsure = "`missing_subscription_id_is_422` | unsure - asserts the status only; closed by a1b2c3d4 |"
        c7_row = "| C7 | removed the `409` on a concurrent delivery | `app/webhooks/ingest.rb:44` | killed |"
        with tempfile.TemporaryDirectory() as raw:  # a listed Risk check with no fault row
            root = Path(raw)
            feature = scaffold(root)
            self._edit(feature, "verification.md", c7_row + "\n", "")
            result = run_gate(root, "validate_verification")
            self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
            self.assertIn("no fault row names C7", result.stdout)
        with tempfile.TemporaryDirectory() as raw:  # no fault rows at all
            root = Path(raw)
            feature = scaffold(root)
            report = (feature / "verification.md").read_text(encoding="utf-8")
            (feature / "verification.md").write_text(report[:report.index("## Faults injected")] + report[report.index("## Gate"):], encoding="utf-8")
            result = run_gate(root, "validate_verification")
            self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
            self.assertIn("no fault row names C7, C8", result.stdout)
        with tempfile.TemporaryDirectory() as raw:  # an unsure row owes a fault even under Risk: none
            root = Path(raw)
            feature = scaffold(root)
            self._edit(feature, "checks.md", "Risk: C7, C8 - the concurrency and idempotency guards would pass silently with a weak test", "Risk: none - covered by the type system")
            self._edit(feature, "verification.md", c9, unsure)
            result = run_gate(root, "validate_verification")
            self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
            self.assertIn("no fault row names C9", result.stdout)
            self._edit(feature, "verification.md", "| C11 | bound", "| C9 | bound")
            result = run_gate(root, "validate_verification")
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_verification_accepts_no_faults_without_risk(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            root = Path(raw)
            feature = scaffold(root)
            self._edit(feature, "checks.md", "Risk: C7, C8 - the concurrency and idempotency guards would pass silently with a weak test", "Risk: none - covered by the type system")
            report = (feature / "verification.md").read_text(encoding="utf-8")
            (feature / "verification.md").write_text(report[:report.index("## Faults injected")] + report[report.index("## Gate"):], encoding="utf-8")
            result = run_gate(root, "validate_verification")
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_fault_disposition_accepted_only_outside_risk(self) -> None:
        source = (FIXTURES / "verification.md").read_text(encoding="utf-8")
        inside = "| C8 | removed the delivery-id guard | `app/webhooks/ingest.rb:31` | killed |"
        outside = "| C11 | log level `info` -> `debug` on the retry trace | `app/models/billing/dunning.rb:40` | arid - logging only, no decision reads it |"
        self.assertIn(inside, source)
        self.assertIn(outside, source)
        cases = [
            (inside, "| C8 | removed the delivery-id guard | `app/webhooks/ingest.rb:31` | killed |", True),
            (inside, "| C8 | removed the delivery-id guard | `app/webhooks/ingest.rb:31` | equivalent - same result on every input |", True),
            (inside, "| C8 | removed the delivery-id guard | `app/webhooks/ingest.rb:31` | arid - never read |", True),
            (inside, "| C8 | removed the delivery-id guard | `app/webhooks/ingest.rb:31` | accepted - rare path |", False),
            (outside, outside.replace("arid - logging only, no decision reads it", "accepted - logging only"), True),
            (outside, outside.replace("arid - logging only, no decision reads it", "accepted"), False),
            (outside, outside.replace("| C11 |", "| - |").replace("arid - logging only, no decision reads it", "accepted - logging only"), False),
        ]
        for old, new, accepted in cases:
            with self.subTest(row=new), tempfile.TemporaryDirectory() as raw:
                root = Path(raw)
                feature = scaffold(root)
                self._edit(feature, "verification.md", old, new)
                result = run_gate(root, "validate_verification")
                self.assertEqual(result.returncode == 0, accepted, result.stdout + result.stderr)

    def test_proofs_run_group_nonzero_exit_fails(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            root = Path(raw)
            checks = PROOF_CHECKS.replace("echo gamma", "echo gamma; exit 3")
            feature = proof_feature(root, checks)
            commit_all(root)
            result = run_script(root, "check_proofs", "fixture")
            self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
            report = (feature / "proofs.md").read_text(encoding="utf-8")
            self.assertIn("| C1: run g / PASS alpha | pass |", report)  # its pass line printed
            self.assertIn("| Run g: ", report)
            self.assertRegex(report, r"\| Run g: [^\n]*\| fail \| exit 3 \|")

    def test_verification_rejects_proofs_missing_a_check(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            root = Path(raw)
            feature = scaffold(root)
            proofs = feature / "proofs.md"
            original = proofs.read_text(encoding="utf-8")
            row = next(ln for ln in original.splitlines() if ln.startswith("| C7:"))
            proofs.write_text(original.replace(row + "\n", "", 1), encoding="utf-8")
            result = run_gate(root, "validate_verification")
            self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
            self.assertIn("proofs.md has 0 row(s) for C7 but checks.md names 1 proof(s)", result.stdout)

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

    def _commit(self, root: Path, message: str) -> subprocess.CompletedProcess:
        return subprocess.run(
            [sys.executable, str(SCRIPTS / "check_commit.py"), "--message", message, "--root", str(root)],
            capture_output=True, text=True,
        )

    def _open_feature(self, root: Path) -> Path:
        feature = scaffold(root)
        (feature / "verification.md").unlink()
        return feature

    def test_commit_names_owed_steps_for_open_feature(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            root = Path(raw)
            self._open_feature(root)
            result = self._commit(root, "feat(wtk): add lean router")
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            owed = [line for line in result.stdout.splitlines() if "OWED" in line]
            self.assertEqual(len(owed), 1, result.stdout)
            self.assertIn("fixture", owed[0])
            self.assertIn("check_proofs.py", owed[0])
            self.assertIn("Verifier", owed[0])
            self.assertNotIn("screens judge", owed[0])

    def test_commit_names_screens_judge_when_capture_cited(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            root = Path(raw)
            feature = self._open_feature(root)
            plan = feature / "plan.md"
            source = plan.read_text(encoding="utf-8")
            criterion = next(ln for ln in source.splitlines() if ln.lstrip().startswith("1. WHEN"))
            plan.write_text(source.replace(criterion, criterion + " as drawn in `captures/billing.png`"), encoding="utf-8")
            result = self._commit(root, "feat(wtk): add lean router")
            owed = [line for line in result.stdout.splitlines() if "OWED" in line]
            self.assertEqual(len(owed), 1, result.stdout)
            self.assertIn("screens judge", owed[0])

    def test_commit_prints_nothing_owed_without_open_feature(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            root = Path(raw)
            result = self._commit(root, "feat(wtk): add lean router")
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            self.assertNotIn("OWED", result.stdout)
            scaffold(root)  # a feature with its verification.md owes nothing
            result = self._commit(root, "feat(wtk): add lean router")
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            self.assertNotIn("OWED", result.stdout)

    def test_commit_invalid_message_prints_no_owed_line(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            root = Path(raw)
            self._open_feature(root)
            result = self._commit(root, "Updated stuff.")
            self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
            self.assertNotIn("OWED", result.stdout)


if __name__ == "__main__":
    unittest.main()
