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
AUTH_SENTINEL = "authorization-sentinel-qa"
COOKIE_SENTINEL = "cookie-sentinel-qa"
TOKEN_SENTINEL = "token-sentinel-qa"
CREDENTIAL_SENTINEL = "credential-sentinel-qa"


class FakeAgent:
    created: list["FakeAgent"] = []

    def __init__(self, url: str, goal: str, states: list[object], error: Exception | None = None) -> None:
        self.url = url
        self.goal = goal
        self.states = states
        self.error = error
        self.run_calls = 0
        self.__class__.created.append(self)

    def __enter__(self) -> "FakeAgent":
        return self

    def __exit__(self, *_: object) -> None:
        return None

    def run(self):
        self.run_calls += 1
        for state in self.states:
            yield state
        if self.error is not None:
            raise self.error


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

    def browser(self, mode: str = "headless") -> dict[str, object]:
        return {"mode": mode, "cdp_url": self.environment["BU_CDP_URL"], "dedicated": True}

    def run_adapter(
        self,
        *,
        states: list[object] | None = None,
        error: Exception | None = None,
        environment: dict[str, str] | None = None,
        browser: object | None = None,
        journey_scope: str | None = "non-consequential",
        module_available: bool = True,
        harness_available: bool = True,
        evidence_dir: Path | None = None,
        existing_adapter: str = "playwright-mcp",
        factory: object | None = None,
    ) -> dict[str, object]:
        env = dict(self.environment if environment is None else environment)
        fake_factory = factory or (lambda url, goal: FakeAgent(url, goal, states or [{"status": "DONE"}], error))
        return jev_adapter.run_jev(
            "http://127.0.0.1:3000",
            "Open the QA fixture and stop when the expected record is visible.",
            evidence_dir=evidence_dir or self.evidence_root / "run",
            checkout_root=self.checkout,
            evidence_root=self.evidence_root,
            browser=browser if browser is not None else self.browser(),
            journey_scope=journey_scope,
            existing_adapter=existing_adapter,
            env=env,
            agent_factory=fake_factory,
            module_available=module_available,
            harness_available=harness_available,
        )

    def assert_secret_free(self, value: object) -> None:
        encoded = json.dumps(value, sort_keys=True).lower()
        for sentinel in (
            TYPESAFE_SENTINEL,
            GATEWAY_SENTINEL,
            AUTH_SENTINEL,
            COOKIE_SENTINEL,
            TOKEN_SENTINEL,
            CREDENTIAL_SENTINEL,
        ):
            self.assertNotIn(sentinel, encoded)

    def test_ready_run_emits_secret_free_contract(self) -> None:
        seen: list[dict[str, str | None]] = []

        def factory(url: str, goal: str) -> FakeAgent:
            seen.append({
                "text_key": os.environ.get("TEXT_MODEL_API_KEY"),
                "cdp_url": os.environ.get("BU_CDP_URL"),
                "cdp_ws": os.environ.get("BU_CDP_WS"),
            })
            return FakeAgent(url, goal, [{"status": "DONE", "authorization": AUTH_SENTINEL}])

        with mock.patch.dict(os.environ, self.environment, clear=False), mock.patch.object(
            jev_adapter, "_default_agent_factory", side_effect=factory
        ):
            result = jev_adapter.run_jev(
                "http://127.0.0.1:3000",
                "Open the QA fixture and stop when the expected record is visible.",
                evidence_dir=self.evidence_root / "headless",
                checkout_root=self.checkout,
                evidence_root=self.evidence_root,
                journey_scope="non-consequential",
                browser=None,
                agent_factory=None,
                module_available=True,
                harness_available=True,
                env=self.environment,
            )
            headed = jev_adapter.run_jev(
                "http://127.0.0.1:3000",
                "Open the QA fixture and stop when the expected record is visible.",
                evidence_dir=self.evidence_root / "headed",
                checkout_root=self.checkout,
                evidence_root=self.evidence_root,
                journey_scope="non-consequential",
                browser=self.browser("headed"),
                agent_factory=factory,
                module_available=True,
                harness_available=True,
                env=self.environment,
            )

        for attempt in (result, headed):
            self.assertEqual(attempt["adapter"], "jev-ultrafast")
            self.assertEqual(attempt["status"], "completed")
            self.assertEqual(attempt["limitation"], "")
            self.assertTrue(attempt["evidence"])
            evidence_path = self.checkout / attempt["evidence"][0]
            self.assertTrue(evidence_path.is_file())
            self.assertTrue(str(evidence_path).startswith(str(self.evidence_root)))
            self.assert_secret_free(attempt)
            self.assert_secret_free(json.loads(evidence_path.read_text(encoding="utf-8")))
        self.assertEqual(seen[0]["text_key"], GATEWAY_SENTINEL)
        self.assertEqual(seen[0]["cdp_url"], self.environment["BU_CDP_URL"])
        self.assertEqual(seen[1]["cdp_url"], self.environment["BU_CDP_URL"])
        self.assertEqual(seen[1]["cdp_ws"], "")

    def test_missing_prerequisite_matrix_falls_back(self) -> None:
        cases = [
            ("TYPESAFE_API_KEY", {"TYPESAFE_API_KEY": ""}, "missing prerequisite: TYPESAFE_API_KEY", "non-consequential"),
            ("AI_GATEWAY_API_KEY", {"AI_GATEWAY_API_KEY": ""}, "missing prerequisite: AI_GATEWAY_API_KEY", "non-consequential"),
            ("non-consequential policy", {}, "policy: non-consequential fixture declaration required", None),
            ("dedicated CDP endpoint", {"BU_CDP_URL": ""}, "missing prerequisite: dedicated CDP endpoint is required", "non-consequential"),
            ("jev_ultrafast module", {}, "missing prerequisite: jev_ultrafast module", "non-consequential"),
            ("Browser Harness", {}, "missing prerequisite: Browser Harness", "non-consequential"),
        ]
        for name, changes, expected, scope in cases:
            with self.subTest(name=name):
                environment = dict(self.environment)
                environment.update(changes)
                module = name != "jev_ultrafast module"
                harness = name != "Browser Harness"
                result = self.run_adapter(
                    environment=environment,
                    journey_scope=scope,
                    browser="headless" if name == "dedicated CDP endpoint" else self.browser(),
                    module_available=module,
                    harness_available=harness,
                    existing_adapter="declared-orca",
                )
                self.assertEqual(result["status"], "unavailable")
                self.assertEqual(result["limitation"], expected)
                self.assertEqual(result["fallback_order"], list(jev_adapter.FALLBACK_ORDER))
                self.assertEqual(result["fallback_adapter"], "orca")
                self.assertEqual(result["declared_fallback"], "orca")
                self.assertEqual(jev_adapter.select_fallback_adapter(["declared-orca", "playwright-mcp"]), "playwright-mcp")
                self.assertEqual(jev_adapter.select_fallback_adapter(["declared-orca"]), "orca")
                self.assertEqual(jev_adapter.select_fallback_adapter(["declared-maestri"]), "maestri")
                self.assertEqual(jev_adapter.select_fallback_adapter(["declared-maestri", "declared-orca"]), "orca")
                self.assertEqual(jev_adapter.select_fallback_adapter(["manual"]), "manual")
                self.assertEqual(
                    jev_adapter.select_existing_adapter({"status": "unavailable"}, ["declared-orca", "playwright-mcp"]),
                    "playwright-mcp",
                )
                self.assert_secret_free(result)

    def test_done_requires_independent_oracle(self) -> None:
        result = self.run_adapter(states=[{"status": "DONE"}])
        self.assertEqual(result["status"], "completed")
        self.assertEqual(result["qa_verdict"], "unverified")
        self.assertTrue(result["independent_oracle_required"])
        self.assertEqual(jev_adapter.external_oracle_verdict(result, False), "not-passed")
        self.assertEqual(jev_adapter.external_oracle_verdict(result, True), "pass")
        self.assertNotIn('"pass"', json.dumps(result, sort_keys=True).lower())

    def test_failure_calls_agent_run_once(self) -> None:
        result = self.run_adapter(
            states=[
                {
                    "status": "RUNNING",
                    "history": [{"authorization": AUTH_SENTINEL, "cookie": COOKIE_SENTINEL}],
                    "token": TOKEN_SENTINEL,
                    "credential": CREDENTIAL_SENTINEL,
                }
            ],
            error=RuntimeError(f"provider failed: {GATEWAY_SENTINEL}"),
        )
        self.assertEqual(result["status"], "failed")
        self.assertTrue(result["evidence"])
        self.assert_secret_free(result)
        evidence = json.loads((self.checkout / result["evidence"][0]).read_text(encoding="utf-8"))
        self.assert_secret_free(evidence)
        self.assertEqual(len(FakeAgent.created), 1)
        self.assertEqual(FakeAgent.created[0].run_calls, 1)

    def test_pre_action_timeout_allows_playwright_fallback(self) -> None:
        def timed_out_factory(url: str, goal: str) -> FakeAgent:
            raise TimeoutError(f"Page.navigate timed out: {TOKEN_SENTINEL}")

        result = self.run_adapter(factory=timed_out_factory)
        self.assertEqual(result["status"], "failed")
        self.assertEqual(result["failure_class"], "pre-action-timeout")
        self.assertTrue(result["fallback_safe"])
        self.assertEqual(result["fallback_adapter"], "playwright-mcp")
        self.assertEqual(result["fallback_order"], list(jev_adapter.FALLBACK_ORDER))
        self.assertFalse(result["agent_run_started"])
        self.assertEqual(result["action_state"], "not-started")
        self.assertEqual(FakeAgent.created, [])
        self.assert_secret_free(result)
        evidence = json.loads((self.checkout / result["evidence"][0]).read_text(encoding="utf-8"))
        self.assert_secret_free(evidence)
        self.assertNotIn(TOKEN_SENTINEL, json.dumps(evidence))

    def test_unsafe_timeout_forbids_automatic_fallback(self) -> None:
        cases = (
            (
                "post-action-timeout",
                [
                    {
                        "status": "RUNNING",
                        "history": [{"kind": "click", "authorization": AUTH_SENTINEL}],
                    }
                ],
                "post-action-timeout",
                "started",
            ),
            ("ambiguous-timeout", [{"status": "RUNNING"}], "ambiguous-timeout", "unknown"),
        )
        for name, states, failure_class, action_state in cases:
            with self.subTest(name=name):
                result = self.run_adapter(
                    states=states,
                    error=TimeoutError(f"{name}: {TOKEN_SENTINEL}"),
                )
                self.assertEqual(result["status"], "failed")
                self.assertEqual(result["failure_class"], failure_class)
                self.assertFalse(result["fallback_safe"])
                self.assertIsNone(result["fallback_adapter"])
                self.assertIsNone(result["fallback_order"])
                self.assertEqual(result["action_state"], action_state)
                self.assertTrue(result["agent_run_started"])
                self.assertEqual(FakeAgent.created[-1].run_calls, 1)
                self.assert_secret_free(result)
                evidence = json.loads((self.checkout / result["evidence"][0]).read_text(encoding="utf-8"))
                self.assert_secret_free(evidence)
                self.assertNotIn(TOKEN_SENTINEL, json.dumps(evidence))

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

    def test_unsafe_jev_scope_falls_back_before_agent(self) -> None:
        def unexpected_factory(url: str, goal: str) -> FakeAgent:
            raise AssertionError("Agent must not be constructed for unsafe preflight")

        consequential = self.run_adapter(
            journey_scope="consequential",
            factory=unexpected_factory,
        )
        self.assertEqual(consequential["status"], "unavailable")
        self.assertEqual(consequential["limitation"], "policy: non-consequential fixture declaration required")
        self.assertEqual(consequential["fallback_adapter"], "playwright-mcp")

        missing_endpoint = self.run_adapter(
            environment={**self.environment, "BU_CDP_URL": ""},
            browser="headless",
            factory=unexpected_factory,
        )
        self.assertEqual(missing_endpoint["status"], "unavailable")
        self.assertEqual(missing_endpoint["limitation"], "missing prerequisite: dedicated CDP endpoint is required")

        for declaration in (
            {"mode": "headless", "cdp_url": self.environment["BU_CDP_URL"], "dedicated": False},
            {"mode": "headless", "cdp_url": self.environment["BU_CDP_URL"]},
            {"mode": "headless", "cdp_url": self.environment["BU_CDP_URL"], "dedicated": True, "profile": "personal"},
        ):
            with self.subTest(declaration=declaration):
                unsafe = self.run_adapter(browser=declaration, factory=unexpected_factory)
                self.assertEqual(unsafe["status"], "unavailable")
                self.assertEqual(unsafe["fallback_adapter"], "playwright-mcp")

        safe = self.run_adapter(states=[{"status": "DONE"}])
        self.assertEqual(safe["status"], "completed")
        self.assertEqual(len(FakeAgent.created), 1)

    def _write_child_shims(self, root: Path) -> tuple[Path, Path]:
        module = root / "jev_ultrafast.py"
        module.write_text(
            """import os
import sys

class Agent:
    def __init__(self, url, goal):
        self.url = url
        self.goal = goal
        if os.environ.get('FAKE_JEV_OUTCOME') == 'pre-action-timeout':
            raise TimeoutError(
                'Page.navigate timed out: ' + os.environ.get('FAKE_EXCEPTION', 'timeout')
            )

    def __enter__(self):
        return self

    def __exit__(self, *args):
        return None

    def run(self):
        print(os.environ.get('FAKE_STDOUT', ''), end='')
        print(os.environ.get('FAKE_STDERR', ''), file=sys.stderr, end='')
        yield {
            'status': 'RUNNING',
            'benign_upstream_field': 'must-not-enter-evidence',
            'nested_benign': {'page_text': 'untrusted page text must-not-enter-evidence'},
            'authorization': os.environ.get('AUTH_SENTINEL', ''),
            'cookie': os.environ.get('COOKIE_SENTINEL', ''),
            'token': os.environ.get('TOKEN_SENTINEL', ''),
            'credential': os.environ.get('CREDENTIAL_SENTINEL', ''),
        }
        outcome = os.environ.get('FAKE_JEV_OUTCOME')
        if outcome == 'post-action-timeout':
            history = [{'kind': 'click', 'authorization': os.environ.get('AUTH_SENTINEL', '')}]
            yield {'status': 'RUNNING', 'history': history}
            raise TimeoutError(os.environ.get('FAKE_EXCEPTION', 'timeout'))
        if outcome == 'ambiguous-timeout':
            raise TimeoutError(os.environ.get('FAKE_EXCEPTION', 'timeout'))
        if outcome == 'failed':
            raise RuntimeError(os.environ.get('FAKE_EXCEPTION', 'provider failure'))
        yield {'status': 'DONE', 'elapsed_ms': 1}
""",
            encoding="utf-8",
        )
        bin_dir = root / "bin"
        bin_dir.mkdir()
        harness = bin_dir / "browser-harness"
        harness.write_text("#!/bin/sh\nexit 0\n", encoding="utf-8")
        harness.chmod(0o700)
        return module, bin_dir

    def _run_cli(
        self,
        root: Path,
        *,
        outcome: str,
        missing_key: str | None = None,
        invalid: bool = False,
        malformed: bool = False,
    ) -> subprocess.CompletedProcess[str]:
        shim_root = root / "shims"
        shim_root.mkdir()
        _, harness_dir = self._write_child_shims(shim_root)
        evidence_root = root / ".qa-evidence"
        evidence_dir = root / ".." / "outside" if invalid else evidence_root / outcome
        env = dict(os.environ)
        env.update(
            {
                "TYPESAFE_API_KEY": TYPESAFE_SENTINEL,
                "AI_GATEWAY_API_KEY": GATEWAY_SENTINEL,
                "BU_CDP_URL": "http://127.0.0.1:9223",
                "FAKE_JEV_OUTCOME": outcome,
                "FAKE_STDOUT": AUTH_SENTINEL,
                "FAKE_STDERR": COOKIE_SENTINEL,
                "FAKE_EXCEPTION": TOKEN_SENTINEL,
                "AUTH_SENTINEL": AUTH_SENTINEL,
                "COOKIE_SENTINEL": COOKIE_SENTINEL,
                "TOKEN_SENTINEL": TOKEN_SENTINEL,
                "CREDENTIAL_SENTINEL": CREDENTIAL_SENTINEL,
                "PYTHONPATH": str(shim_root),
                "PATH": str(harness_dir) + os.pathsep + env.get("PATH", ""),
            }
        )
        if missing_key:
            env.pop(missing_key, None)
        args = [
            sys.executable,
            str(ADAPTER),
            "--url",
            "http://127.0.0.1:3000",
            "--goal",
            "Open the fixture.",
            "--journey-scope",
            "non-consequential",
            "--browser",
            "headless",
            "--checkout-root",
            str(root),
            "--evidence-root",
            str(evidence_root),
            "--evidence-dir",
            str(evidence_dir),
        ]
        if malformed:
            args.append("--unknown-option")
        return subprocess.run(args, cwd=root, env=env, text=True, capture_output=True, check=False)

    def test_fallback_terminal_and_redaction_matrix(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            cases = [
                ("completed", None, False, 0, False, "completed", None, False, "unknown", None),
                (
                    "unavailable", "TYPESAFE_API_KEY", False, 2, False,
                    "unavailable", "unavailable", True, "not-started", "playwright-mcp",
                ),
                ("failed", None, False, 1, False, "failed", "unclassified-failure", False, "unknown", None),
                (
                    "pre-action-timeout", None, False, 1, False,
                    "failed", "pre-action-timeout", True, "not-started", "playwright-mcp",
                ),
                (
                    "post-action-timeout", None, False, 1, False,
                    "failed", "post-action-timeout", False, "started", None,
                ),
                (
                    "ambiguous-timeout", None, False, 1, False,
                    "failed", "ambiguous-timeout", False, "unknown", None,
                ),
                ("ignored", None, True, 2, False, "invalid", None, False, "not-started", None),
                ("malformed", None, False, 2, True, "invalid", None, False, "not-started", None),
            ]
            for (
                outcome,
                missing_key,
                invalid,
                exit_code,
                malformed,
                expected_status,
                failure_class,
                fallback_safe,
                action_state,
                fallback_adapter,
            ) in cases:
                with self.subTest(outcome=outcome):
                    case_root = root / outcome
                    case_root.mkdir()
                    completed = self._run_cli(
                        case_root,
                        outcome=outcome,
                        missing_key=missing_key,
                        invalid=invalid,
                        malformed=malformed,
                    )
                    self.assertEqual(completed.returncode, exit_code)
                    lines = [line for line in completed.stdout.splitlines() if line.strip()]
                    self.assertEqual(len(lines), 1)
                    self.assertEqual(completed.stderr, "")
                    result = json.loads(lines[0])
                    self.assertEqual(result["status"], expected_status)
                    self.assertEqual(result["failure_class"], failure_class)
                    self.assertEqual(result["fallback_safe"], fallback_safe)
                    self.assertEqual(result["fallback_adapter"], fallback_adapter)
                    self.assertEqual(result["action_state"], action_state)
                    expected_order = list(jev_adapter.FALLBACK_ORDER) if fallback_safe else None
                    self.assertEqual(result["fallback_order"], expected_order)
                    for key in (
                        "adapter",
                        "status",
                        "evidence",
                        "limitation",
                        "failure_class",
                        "fallback_safe",
                        "fallback_adapter",
                        "fallback_order",
                        "action_state",
                    ):
                        self.assertIn(key, result)
                    self.assert_secret_free(completed.stdout + completed.stderr)
                    self.assert_secret_free(result)
                    self.assertNotIn("must-not-enter-evidence", completed.stdout + completed.stderr)
                    self.assertNotIn(TOKEN_SENTINEL, completed.stdout + completed.stderr)
                    self.assertEqual(jev_adapter.external_oracle_verdict(result, False), "not-passed")
                    self.assertEqual(
                        jev_adapter.external_oracle_verdict(result, True),
                        "pass" if expected_status == "completed" else "not-passed",
                    )
                    for path in result["evidence"]:
                        evidence = (case_root / path).read_text(encoding="utf-8")
                        self.assert_secret_free(evidence)
                        self.assertNotIn("must-not-enter-evidence", evidence)
                        self.assertNotIn(TOKEN_SENTINEL, evidence)

            with mock.patch.object(jev_adapter, "MAX_TRACE_CHARS", 10):
                oversized = self.run_adapter(evidence_dir=self.evidence_root / "oversized")
            self.assertEqual(oversized["status"], "completed")
            json.loads((self.checkout / oversized["evidence"][0]).read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main()
