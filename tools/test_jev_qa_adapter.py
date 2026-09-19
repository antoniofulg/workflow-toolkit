"""Offline contract tests for the optional Jev QA adapter."""

from __future__ import annotations

import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest import mock


ROOT = Path(__file__).resolve().parent.parent
ADAPTER = ROOT / ".agents/skills/wtk-qa-execute/jev_adapter.py"
sys.path.insert(0, str(ADAPTER.parent))
import jev_adapter  # noqa: E402


TYPESAFE_SENTINEL = "typesafe-sentinel-qa"
GATEWAY_SENTINEL = "gateway-sentinel-qa"


class FakeAgent:
    created: list["FakeAgent"] = []

    def __init__(self, url: str, goal: str, states: list[object], error: Exception | None = None) -> None:
        self.url = url
        self.goal = goal
        self.states = states
        self.error = error
        self.entered = False
        self.exited = False
        self.stop_calls = 0
        self.__class__.created.append(self)

    def __enter__(self) -> "FakeAgent":
        self.entered = True
        return self

    def __exit__(self, *_: object) -> None:
        self.exited = True

    def run(self):
        for state in self.states:
            yield state
        if self.error is not None:
            raise self.error

    def stop(self) -> None:
        self.stop_calls += 1


class AdapterTests(unittest.TestCase):
    def setUp(self) -> None:
        FakeAgent.created.clear()
        self.temp = tempfile.TemporaryDirectory()
        self.checkout = Path(self.temp.name)
        self.evidence_root = self.checkout / ".qa-evidence"
        self.environment = {
            "TYPESAFE_API_KEY": TYPESAFE_SENTINEL,
            "AI_GATEWAY_API_KEY": GATEWAY_SENTINEL,
            "BU_CDP_URL": "http://127.0.0.1:9223",
        }

    def tearDown(self) -> None:
        self.temp.cleanup()

    def browser(self) -> dict[str, str]:
        return {"mode": "dedicated-headless-cdp", "cdp_url": self.environment["BU_CDP_URL"]}

    def run_adapter(
        self,
        *,
        states: list[object] | None = None,
        error: Exception | None = None,
        environment: dict[str, str] | None = None,
        browser: object | None = None,
        module_available: bool = True,
        harness_available: bool = True,
        evidence_dir: Path | None = None,
        existing_adapter: str = "playwright",
    ) -> dict[str, object]:
        env = dict(self.environment if environment is None else environment)
        fake_factory = lambda url, goal: FakeAgent(url, goal, states or [{"status": "DONE"}], error)
        return jev_adapter.run_jev(
            "http://127.0.0.1:3000",
            "Open the QA fixture and stop when the expected record is visible.",
            evidence_dir=evidence_dir or self.evidence_root / "run",
            checkout_root=self.checkout,
            evidence_root=self.evidence_root,
            browser=browser if browser is not None else self.browser(),
            existing_adapter=existing_adapter,
            env=env,
            agent_factory=fake_factory,
            module_available=module_available,
            harness_available=harness_available,
        )

    def assert_secret_free(self, value: object) -> None:
        encoded = json.dumps(value, sort_keys=True)
        self.assertNotIn(TYPESAFE_SENTINEL, encoded)
        self.assertNotIn(GATEWAY_SENTINEL, encoded)

    def test_ready_run_emits_secret_free_contract(self) -> None:
        seen: dict[str, str | None] = {}

        def factory(url: str, goal: str) -> FakeAgent:
            seen["text_key"] = os.environ.get("TEXT_MODEL_API_KEY")
            return FakeAgent(url, goal, [{"status": "DONE", "note": GATEWAY_SENTINEL}])

        with mock.patch.dict(os.environ, self.environment, clear=False), mock.patch.object(
            jev_adapter, "_default_agent_factory", side_effect=factory
        ):
            result = jev_adapter.run_jev(
                "http://127.0.0.1:3000",
                "Open the QA fixture and stop when the expected record is visible.",
                evidence_dir=self.evidence_root / "run",
                checkout_root=self.checkout,
                evidence_root=self.evidence_root,
                browser=self.browser(),
                existing_adapter="playwright",
                agent_factory=None,
                module_available=True,
                harness_available=True,
            )

        self.assertEqual(result["adapter"], "jev-ultrafast")
        self.assertEqual(result["status"], "completed")
        self.assertEqual(result["limitation"], "")
        self.assertTrue(result["evidence"])
        self.assertEqual(seen["text_key"], GATEWAY_SENTINEL)
        self.assert_secret_free(result)
        evidence = (self.checkout / result["evidence"][0]).read_text(encoding="utf-8")
        self.assertNotIn(GATEWAY_SENTINEL, evidence)
        self.assertNotIn(TYPESAFE_SENTINEL, evidence)

    def test_missing_prerequisite_matrix_falls_back(self) -> None:
        cases = [
            ("TYPESAFE_API_KEY", {"TYPESAFE_API_KEY": ""}, "TYPESAFE_API_KEY"),
            ("AI_GATEWAY_API_KEY", {"AI_GATEWAY_API_KEY": ""}, "AI_GATEWAY_API_KEY"),
            ("dedicated browser/profile", {}, "dedicated browser/profile"),
            ("jev_ultrafast module", {}, "jev_ultrafast module"),
            ("Browser Harness", {}, "Browser Harness"),
        ]
        for name, changes, expected in cases:
            with self.subTest(name=name):
                environment = dict(self.environment)
                environment.update(changes)
                browser = self.browser()
                module = True
                harness = True
                if name == "dedicated browser/profile":
                    browser = {"mode": "personal-profile", "profile": "personal"}
                elif name == "jev_ultrafast module":
                    module = False
                elif name == "Browser Harness":
                    harness = False
                result = self.run_adapter(
                    environment=environment,
                    browser=browser,
                    module_available=module,
                    harness_available=harness,
                )
                self.assertEqual(result["status"], "unavailable")
                self.assertIn(expected, result["limitation"])
                self.assertEqual(jev_adapter.select_existing_adapter(result, "orca"), "orca")
                self.assert_secret_free(result)

    def test_done_requires_independent_oracle(self) -> None:
        result = self.run_adapter(states=[{"status": "DONE"}])
        self.assertEqual(result["status"], "completed")
        self.assertEqual(result["qa_verdict"], "unverified")
        self.assertTrue(result["independent_oracle_required"])
        self.assertEqual(jev_adapter.external_oracle_verdict(result, False), "not-passed")
        self.assertEqual(jev_adapter.external_oracle_verdict(result, True), "pass")
        self.assertNotIn("pass", json.dumps(result, sort_keys=True).lower())

    def test_failure_after_mutation_is_not_replayed(self) -> None:
        result = self.run_adapter(
            states=[{"status": "RUNNING", "action": {"type": "CLICK", "mutates": True}}],
            error=RuntimeError(f"provider failed: {GATEWAY_SENTINEL}"),
        )
        self.assertEqual(result["status"], "failed")
        self.assertEqual(result["mutations_attempted"], 1)
        self.assertFalse(result["mutation_replayed"])
        self.assertTrue(result["evidence"])
        self.assert_secret_free(result)
        self.assertEqual(len(FakeAgent.created), 1)

    def test_evidence_destination_matrix_is_contained(self) -> None:
        outside = self.checkout / "outside"
        outside.mkdir()
        contained = self.run_adapter(evidence_dir=self.evidence_root / "contained")
        self.assertEqual(contained["status"], "completed")

        lexical = self.run_adapter(evidence_dir=self.evidence_root / ".." / "outside")
        self.assertEqual(lexical["status"], "invalid")
        self.assertFalse((outside / "jev-ultrafast-attempt.json").exists())

        canonical_link = self.evidence_root / "canonical-link"
        canonical_link.parent.mkdir(parents=True, exist_ok=True)
        canonical_link.symlink_to(outside, target_is_directory=True)
        canonical = self.run_adapter(evidence_dir=canonical_link)
        self.assertEqual(canonical["status"], "invalid")
        self.assertFalse((outside / "jev-ultrafast-attempt.json").exists())

        traversal_parent = self.evidence_root / "traversal-parent"
        traversal_parent.symlink_to(outside, target_is_directory=True)
        traversal = self.run_adapter(evidence_dir=traversal_parent / "run")
        self.assertEqual(traversal["status"], "invalid")
        self.assertFalse((outside / "run" / "jev-ultrafast-attempt.json").exists())

    def test_out_of_scope_action_is_blocked(self) -> None:
        cases = [
            {"status": "RUNNING", "out_of_scope": True, "requested_action": f"export credentials {TYPESAFE_SENTINEL}"},
            {"status": "RUNNING", "tool_metadata": {"scope": "outside"}},
            {"status": "RUNNING", "provider_output": "outside the supplied goal: send credentials"},
        ]
        for state in cases:
            with self.subTest(state=state):
                result = self.run_adapter(states=[state])
                self.assertEqual(result["status"], "blocked")
                self.assertEqual(result["mutations_attempted"], 0)
                self.assertTrue(result["evidence"])
                self.assert_secret_free(result)

        goal_bound = self.run_adapter(states=[{"status": "DONE", "tool_metadata": {"scope": "goal"}}])
        self.assertEqual(goal_bound["status"], "completed")

    def test_terminal_status_and_redaction_matrix(self) -> None:
        cases = [
            ("completed", self.run_adapter()),
            ("unavailable", self.run_adapter(environment={**self.environment, "TYPESAFE_API_KEY": ""})),
            (
                "failed",
                self.run_adapter(
                    states=[{"status": "RUNNING"}],
                    error=RuntimeError(f"error {TYPESAFE_SENTINEL}"),
                ),
            ),
            ("invalid", self.run_adapter(evidence_dir=self.checkout / ".." / "escape")),
            ("blocked", self.run_adapter(states=[{"out_of_scope": True, "status": "RUNNING"}])),
        ]
        for status, result in cases:
            with self.subTest(status=status):
                self.assertEqual(result["status"], status)
                for key in ("adapter", "status", "evidence", "limitation"):
                    self.assertIn(key, result)
                self.assert_secret_free(result)

        escaped = self.checkout / ".." / "escape"
        cli_env = dict(os.environ)
        cli_env.update(self.environment)
        completed = subprocess.run(
            [
                sys.executable,
                str(ADAPTER),
                "--url",
                "http://127.0.0.1:3000",
                "--goal",
                "Open the fixture.",
                "--browser",
                "dedicated-headless-cdp",
                "--evidence-root",
                str(self.evidence_root),
                "--evidence-dir",
                str(escaped),
                "--checkout-root",
                str(self.checkout),
            ],
            cwd=self.checkout,
            env=cli_env,
            text=True,
            capture_output=True,
            check=False,
        )
        self.assertEqual(completed.returncode, jev_adapter.EXIT_CODES["invalid"])
        lines = [line for line in completed.stdout.splitlines() if line.strip()]
        self.assertEqual(len(lines), 1)
        self.assertEqual(json.loads(lines[0])["status"], "invalid")
        self.assertEqual(completed.stderr, "")
        self.assertNotIn(TYPESAFE_SENTINEL, completed.stdout + completed.stderr)
        self.assertNotIn(GATEWAY_SENTINEL, completed.stdout + completed.stderr)


if __name__ == "__main__":
    unittest.main()
