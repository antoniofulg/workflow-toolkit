"""Contract tests for repository_intelligence.py (UT/IT/SEC repository-intelligence cases)."""

from __future__ import annotations

import json
import os
from contextlib import contextmanager
from io import StringIO
from pathlib import Path
import shutil
import signal
import stat
import subprocess
import tempfile
import unittest
from unittest import mock


ROOT = Path(__file__).resolve().parent.parent
SCRIPT = ROOT / ".agents/skills/wtk-deep-review/scripts/repository_intelligence.py"
import sys
sys.path.insert(0, str(SCRIPT.parent))
import repository_intelligence as ri


SPEC_METRIC_FIELDS = (
    "input_tokens", "output_tokens", "total_tokens", "repository_intelligence_calls",
    "native_search_calls", "direct_files_read", "wall_clock_ms", "rework_count",
    "review_findings",
)


class RepositoryFixture(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        subprocess.run(["git", "init", "-q"], cwd=self.root, check=True)
        (self.root / "src").mkdir()
        (self.root / "src/app.py").write_text("def call(): pass\n", encoding="utf-8")
        subprocess.run(["git", "add", "."], cwd=self.root, check=True)
        subprocess.run(["git", "-c", "user.email=test@example.com", "-c", "user.name=test", "commit", "-qm", "fixture"], cwd=self.root, check=True)

    def tearDown(self) -> None:
        self.temp.cleanup()

    def fake_tool(self, name: str, version: str, output: str = "src/app.py:1 symbol call\n", code: int = 0) -> Path:
        path = self.root / "bin" / name
        path.parent.mkdir(exist_ok=True)
        body = "#!/usr/bin/env python3\nimport sys\n"
        body += f"if '--version' in sys.argv: print('{version}'); raise SystemExit(0)\n"
        body += f"print({output!r})\nraise SystemExit({code})\n"
        path.write_text(body, encoding="utf-8")
        path.chmod(path.stat().st_mode | stat.S_IXUSR)
        return path

    def env_path(self, *paths: Path) -> dict[str, str]:
        return {"PATH": os.pathsep.join(str(path.parent) for path in paths) + os.pathsep + os.environ.get("PATH", "")}


class RoutingTests(unittest.TestCase):
    def test_ut001_unknown_code_uses_graft(self) -> None:
        result = ri.route({"phase": "execute"})
        self.assertEqual(result["first"], "graft")
        self.assertNotIn("graphify", result["tools"])

    def test_ut002_architectural_design_uses_graphify(self) -> None:
        result = ri.route({"phase": "design", "triggers": ["domain boundary"]})
        self.assertEqual(result["tools"], ["graphify"])

    def test_ut003_sufficient_pointers_skip_tools(self) -> None:
        self.assertEqual(ri.route({"sufficient_context": True})["tools"], [])

    def test_ut004_local_work_does_not_use_graphify(self) -> None:
        self.assertNotIn("graphify", ri.route({"phase": "execute", "file_count": 20})["tools"])

    def test_ut010_all_architecture_triggers_are_classified(self) -> None:
        for trigger in ("module boundary", "boundary", "responsibility transfer", "shared abstraction", "central flow", "residual architectural uncertainty"):
            self.assertEqual(ri.route({"phase": "design", "triggers": [trigger]})["first"], "graphify")

    def test_ut010_file_count_is_not_trigger(self) -> None:
        self.assertNotEqual(ri.route({"phase": "design", "file_count": 100})["first"], "graphify")

    def test_ut011_indexer_metrics_are_excluded(self) -> None:
        result = ri.agent_metrics({"tool_calls": 2, "direct_files_read": 3, "indexer_reads": 99, "indexer_calls": 8})
        self.assertEqual(result, {"tool_calls": 2, "direct_files_read": 3})


class AdapterTests(RepositoryFixture):
    def test_r1_graphify_requires_setup_before_query(self) -> None:
        graphify = self.fake_tool("graphify", ri.GRAPHIFY_VERSION)
        with mock.patch.dict(os.environ, self.env_path(graphify), clear=False):
            with self.assertRaisesRegex(ri.IntelligenceError, "setup required"):
                ri._run_context(self.root, "graphify", "path", ["domain"])

    def test_r1_graphify_setup_discloses_preflight_before_extraction(self) -> None:
        graphify = self.fake_tool("graphify", ri.GRAPHIFY_VERSION)
        output = StringIO()
        events: list[str] = []

        def run(command, root, **kwargs):
            events.append(command[1])
            if command[1] == "--version":
                return subprocess.CompletedProcess(command, 0, ri.GRAPHIFY_VERSION + "\n", "")
            return subprocess.CompletedProcess(command, 0, "src/app.py:1\n", "")

        def announce(value="", **kwargs):
            if '"preflight"' in str(value):
                events.append("disclosure")
            output.write(str(value) + "\n")

        with mock.patch.dict(os.environ, self.env_path(graphify), clear=False), mock.patch.object(ri, "_run", side_effect=run), mock.patch("builtins.print", side_effect=announce):
            result = ri.graphify_setup(self.root, "claude-cli", "code-only")
        self.assertLess(events.index("disclosure"), events.index("extract"))
        self.assertIn('"preflight"', output.getvalue().splitlines()[0])
        self.assertEqual(result["backend"], "claude-cli")

    def test_r1_graphify_wrong_version_is_rejected(self) -> None:
        graphify = self.fake_tool("graphify", "0.0.1")
        with mock.patch.dict(os.environ, self.env_path(graphify), clear=False):
            with self.assertRaisesRegex(ri.IntelligenceError, "version mismatch"):
                ri._require_tool(self.root, "graphify", ri.GRAPHIFY_VERSION)

    def test_ut005_wrong_version_is_degraded_with_expected_and_actual(self) -> None:
        graft = self.fake_tool("graft", "9.9.9")
        with mock.patch.dict(os.environ, self.env_path(graft), clear=False):
            result = subprocess.run([sys.executable, str(SCRIPT), "graft", "--root", str(self.root), "map"], text=True, capture_output=True)
        self.assertEqual(result.returncode, 3)
        payload = json.loads(result.stdout)
        self.assertEqual(payload["expected_version"], ri.GRAFT_VERSION)
        self.assertEqual(payload["actual_version"], "9.9.9")

    def test_r2_degraded_output_names_targeted_fallback_once(self) -> None:
        graft = self.fake_tool("graft", "9.9.9")
        with mock.patch.dict(os.environ, self.env_path(graft), clear=False):
            result = subprocess.run([sys.executable, str(SCRIPT), "graft", "--root", str(self.root), "map"], text=True, capture_output=True)
        self.assertEqual(result.returncode, ri.DEGRADED_EXIT)
        payload = json.loads(result.stdout)
        self.assertEqual(payload["fallback"], ri.DEGRADED_FALLBACK)
        self.assertEqual(result.stdout.count("version mismatch"), 1)

    def test_ut006_foreign_state_rejected(self) -> None:
        graft = self.fake_tool("graft", ri.GRAFT_VERSION)
        (self.root / ri.STATE_DIR).mkdir(mode=0o700)
        (self.root / ri.STATE_DIR / "graft.json").write_text(json.dumps({"checkout": "/other/checkout"}), encoding="utf-8")
        with mock.patch.dict(os.environ, self.env_path(graft), clear=False):
            result = subprocess.run([sys.executable, str(SCRIPT), "graft", "--root", str(self.root), "map"], text=True, capture_output=True)
        self.assertEqual(result.returncode, ri.DEGRADED_EXIT)
        self.assertTrue(json.loads(result.stdout)["rejected"])

    def test_ut007_bounded_output_keeps_pointer_and_drops_bulk(self) -> None:
        output, status = ri._bounded_output("src/app.py:1 symbol\n" + ("explanation " * 5000))
        self.assertEqual(status, "partial")
        self.assertIn("src/app.py:1", output)
        self.assertLessEqual(len(output), ri.MAX_CONTEXT_CHARS)

    def test_ut008_redaction_removes_credential_name_and_value(self) -> None:
        with mock.patch.dict(os.environ, {"GRAPHIFY_API_TOKEN": "sentinel-token"}, clear=False):
            result = ri._redact("GRAPHIFY_API_TOKEN=sentinel-token backend=claude-cli")
        self.assertNotIn("sentinel-token", result)
        self.assertNotIn("GRAPHIFY_API_TOKEN", result)
        self.assertIn("claude-cli", result)

    def test_ut010_exact_text_uses_native_search(self) -> None:
        self.assertEqual(ri.route({"exact_text": True})["first"], "native")

    def test_it001_graft_query_returns_exact_pointer(self) -> None:
        graft = self.fake_tool("graft", ri.GRAFT_VERSION)
        with mock.patch.dict(os.environ, self.env_path(graft), clear=False):
            result = ri._run_context(self.root, "graft", "map", [])
        self.assertEqual(result["status"], "ready")
        self.assertIn("src/app.py:1", result["context"])
        self.assertEqual(result["command"][1], "map")

    def test_it002_missing_graft_has_exact_remediation(self) -> None:
        with mock.patch.object(ri, "_tool_path", return_value=None):
            with self.assertRaises(ri.IntelligenceError) as raised:
                ri._run_context(self.root, "graft", "map", [])
        self.assertIn("npm install --save-dev --save-exact @nanonets/graft@0.10.1", raised.exception.reason)

    def test_it002_failed_graft_refresh_is_degraded(self) -> None:
        graft = self.fake_tool("graft", ri.GRAFT_VERSION, code=1)
        with mock.patch.dict(os.environ, self.env_path(graft), clear=False):
            with self.assertRaisesRegex(ri.IntelligenceError, "refresh failed"):
                ri._run_context(self.root, "graft", "map", [])

    def test_r1_graft_insufficient_result_is_degraded(self) -> None:
        graft = self.fake_tool("graft", ri.GRAFT_VERSION, output="")
        with mock.patch.dict(os.environ, self.env_path(graft), clear=False):
            with self.assertRaisesRegex(ri.IntelligenceError, "insufficient context"):
                ri._run_context(self.root, "graft", "map", [])

    def test_r1_dot_directory_result_is_partial_with_targeted_fallback(self) -> None:
        graft = self.fake_tool("graft", ri.GRAFT_VERSION)
        with mock.patch.dict(os.environ, self.env_path(graft), clear=False):
            result = ri._run_context(self.root, "graft", "map", [".agents"])
        self.assertEqual(result["status"], "partial")
        self.assertEqual(result["fallback"], "targeted-native-inspection")
        self.assertEqual(result["dot_paths"], [".agents"])

    def test_r1_stale_after_refresh_is_rejected(self) -> None:
        path = self.root / "bin" / "graft"
        path.parent.mkdir(exist_ok=True)
        path.write_text("#!/usr/bin/env python3\nimport sys\nif '--version' in sys.argv: print('0.10.1'); raise SystemExit(0)\nif sys.argv[1] == 'check': raise SystemExit(1)\nprint('src/app.py:1')\n", encoding="utf-8")
        path.chmod(path.stat().st_mode | stat.S_IXUSR)
        with mock.patch.dict(os.environ, self.env_path(path), clear=False):
            with self.assertRaisesRegex(ri.IntelligenceError, "stale after refresh"):
                ri._run_context(self.root, "graft", "map", [])

    def test_it003_graphify_query_is_bounded_and_fresh(self) -> None:
        graphify = self.fake_tool("graphify", ri.GRAPHIFY_VERSION, output="domain -> src/app.py:1\n")
        with mock.patch.dict(os.environ, self.env_path(graphify), clear=False):
            ri.graphify_setup(self.root, "claude-cli", "code-only", announce=False)
            result = ri._run_context(self.root, "graphify", "path", ["domain"])
        self.assertEqual(result["status"], "partial")
        self.assertIn("domain -> src/app.py:1", result["context"])

    def test_it004_graphify_not_called_by_local_route(self) -> None:
        self.assertEqual(ri.route({"phase": "execute"})["first"], "graft")

    def test_it008_state_is_checkout_local(self) -> None:
        graft = self.fake_tool("graft", ri.GRAFT_VERSION)
        with mock.patch.dict(os.environ, self.env_path(graft), clear=False):
            ri._run_context(self.root, "graft", "map", [])
        state = ri.read_state(self.root, "graft")
        self.assertEqual(state["checkout"], str(self.root))
        self.assertEqual(state["tree"], ri.tree_fingerprint(self.root))
        self.assertEqual(state["tool_version"], ri.GRAFT_VERSION)
        self.assertEqual(state["source_scope"], ["."])
        self.assertIn("src/app.py", state["indexed_source_manifest"])
        self.assertFalse(any(path.startswith(f"{ri.STATE_DIR}/") for path in state["indexed_source_manifest"]))

    def test_r1_source_mutation_refreshes_fingerprint_and_manifest(self) -> None:
        graft = self.fake_tool("graft", ri.GRAFT_VERSION)
        with mock.patch.dict(os.environ, self.env_path(graft), clear=False):
            first = ri._run_context(self.root, "graft", "map", [])
            (self.root / "notes.md").write_text("indexed\n", encoding="utf-8")
            second = ri._run_context(self.root, "graft", "map", [])
        self.assertNotEqual(first["tree"], second["tree"])
        self.assertIn("notes.md", ri.read_state(self.root, "graft")["indexed_source_manifest"])

    def test_r11_real_graft_command_handles_tracked_directory_symlink(self) -> None:
        target = self.root / ".agents/skills/wtk-ship"
        target.mkdir(parents=True)
        (target / "SKILL.md").write_text("skill\n", encoding="utf-8")
        link = self.root / ".claude/skills/wtk-ship"
        link.parent.mkdir(parents=True)
        link.symlink_to(Path("../../.agents/skills/wtk-ship"), target_is_directory=True)
        subprocess.run(["git", "add", "."], cwd=self.root, check=True)
        graft = self.fake_tool("graft", ri.GRAFT_VERSION)

        with mock.patch.dict(os.environ, self.env_path(graft), clear=False):
            result = subprocess.run(
                [sys.executable, str(SCRIPT), "graft", "--root", str(self.root), "map"],
                text=True,
                capture_output=True,
            )

        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(json.loads(result.stdout)["status"], "ready")
        state = ri.read_state(self.root, "graft")
        self.assertIn(".claude/skills/wtk-ship", state["indexed_source_manifest"])

        before = state["source_fingerprint"]
        other_target = self.root / ".agents/skills/other"
        other_target.mkdir()
        link.unlink()
        link.symlink_to(Path("../../.agents/skills/other"), target_is_directory=True)
        subprocess.run(["git", "add", "."], cwd=self.root, check=True)
        self.assertNotEqual(before, ri._source_fingerprint(self.root))

    def test_r1_interrupted_publication_preserves_last_state(self) -> None:
        graft = self.fake_tool("graft", ri.GRAFT_VERSION)
        with mock.patch.dict(os.environ, self.env_path(graft), clear=False):
            ri._run_context(self.root, "graft", "map", [])
            original_run = ri._run

            def interrupt_build(command, root, **kwargs):
                if command[1] == "build":
                    raise OSError("interrupted")
                return original_run(command, root, **kwargs)

            with mock.patch.object(ri, "_run", side_effect=interrupt_build):
                with self.assertRaises(ri.IntelligenceError):
                    ri._run_context(self.root, "graft", "map", [])
        state = ri.read_state(self.root, "graft")
        self.assertEqual(state["status"], "unavailable")
        self.assertEqual(state["tree"], ri.tree_fingerprint(self.root))

    def test_r2_query_runs_under_shared_read_lock_after_refresh(self) -> None:
        events: list[str] = []

        @contextmanager
        def mutation(_root: Path):
            events.append("mutation-enter")
            yield
            events.append("mutation-exit")

        @contextmanager
        def read(_root: Path):
            events.append("read-enter")
            yield
            events.append("read-exit")

        def run(command, _root, **_kwargs):
            events.append(command[1])
            return subprocess.CompletedProcess(command, 0, "src/app.py:1\n", "")

        with mock.patch.object(ri, "_require_tool", return_value="graft"), mock.patch.object(ri, "_run", side_effect=run), mock.patch.object(ri, "mutation_lock", mutation), mock.patch.object(ri, "read_lock", read):
            result = ri._run_context(self.root, "graft", "map", [])
        self.assertEqual(result["status"], "ready")
        self.assertLess(events.index("mutation-exit"), events.index("read-enter"))
        self.assertLess(events.index("read-enter"), events.index("map"))
        self.assertLess(events.index("map"), events.index("read-exit"))

    def test_r1_code_only_graphify_context_remains_partial(self) -> None:
        graphify = self.fake_tool("graphify", ri.GRAPHIFY_VERSION, output="domain -> src/app.py:1\n")
        with mock.patch.dict(os.environ, self.env_path(graphify), clear=False):
            ri.graphify_setup(self.root, "claude-cli", "code-only", announce=False)
            result = ri._run_context(self.root, "graphify", "path", ["domain"])
        self.assertEqual(result["status"], "partial")

    def test_it014_remote_scope_outside_checkout_is_refused(self) -> None:
        with self.assertRaisesRegex(ri.IntelligenceError, "outside checkout"):
            ri._validate_scope(self.root, "openai", str(self.root.parent))

    def test_sec001_path_tool_version_is_validated(self) -> None:
        graft = self.fake_tool("graft", "0.0.1")
        with mock.patch.dict(os.environ, self.env_path(graft), clear=False):
            with self.assertRaisesRegex(ri.IntelligenceError, "version mismatch"):
                ri._require_tool(self.root, "graft", ri.GRAFT_VERSION)

    def test_sec003_arguments_are_not_shell_evaluated(self) -> None:
        marker = self.root / "executed"
        graft = self.fake_tool("graft", ri.GRAFT_VERSION, output="src/app.py:1\n")
        with mock.patch.dict(os.environ, self.env_path(graft), clear=False):
            result = ri._run_context(self.root, "graft", "grep", [f"x; touch {marker}"])
        self.assertIn("src/app.py:1", result["context"])
        self.assertFalse(marker.exists())

    def test_sec004_setup_does_not_persist_credentials(self) -> None:
        graphify = self.fake_tool("graphify", ri.GRAPHIFY_VERSION)
        with mock.patch.dict(os.environ, {**self.env_path(graphify), "GRAPHIFY_API_TOKEN": "sentinel"}, clear=False):
            result = ri.graphify_setup(self.root, "claude-cli", "code-only")
        text = json.dumps(result) + (self.root / ri.STATE_DIR / "graphify.json").read_text(encoding="utf-8")
        self.assertNotIn("sentinel", text)
        self.assertIn("claude-cli", text)

    def test_sec005_remote_source_scope_requires_disclosed_checkout(self) -> None:
        with self.assertRaisesRegex(ri.IntelligenceError, "source scope"):
            ri._validate_scope(self.root, "azure", str(self.root / "src"))

    def test_sec006_state_foreign_path_is_rejected(self) -> None:
        self.assertTrue(ri._foreign_state(self.root, {"checkout": "/foreign"}))

    def test_r2_foreign_fingerprint_is_rejected(self) -> None:
        self.assertTrue(ri._foreign_state(self.root, {"checkout": str(self.root), "tree": "foreign-tree"}))

    def test_r3_public_foreign_fingerprint_is_rejected(self) -> None:
        graft = self.fake_tool("graft", ri.GRAFT_VERSION)
        (self.root / ri.STATE_DIR).mkdir(mode=0o700)
        (self.root / ri.STATE_DIR / "graft.json").write_text(
            json.dumps({
                "checkout": str(self.root), "tree": "f" * 40,
                "source_fingerprint": ri._source_fingerprint(self.root), "status": "ready",
            }),
            encoding="utf-8",
        )
        with mock.patch.dict(os.environ, self.env_path(graft), clear=False):
            result = ri._run_context(self.root, "graft", "map", [])
        self.assertEqual(result["status"], "degraded")
        self.assertTrue(result["rejected"])

    def test_r3_source_mutation_after_query_is_rejected(self) -> None:
        graft = self.fake_tool("graft", ri.GRAFT_VERSION)
        original_fingerprint = ri.tree_fingerprint
        calls = 0

        def fingerprint(root: Path) -> str:
            nonlocal calls
            calls += 1
            value = original_fingerprint(root)
            if calls == 3:
                (root / "src/app.py").write_text("def changed(): pass\n", encoding="utf-8")
            return value

        with mock.patch.dict(os.environ, self.env_path(graft), clear=False), mock.patch.object(ri, "tree_fingerprint", side_effect=fingerprint):
            with self.assertRaisesRegex(ri.IntelligenceError, "stale before publication"):
                ri._run_context(self.root, "graft", "map", [])

    def test_r3_abrupt_exit_leaves_unavailable_state(self) -> None:
        graft = self.root / "bin" / "graft"
        graft.parent.mkdir(exist_ok=True)
        graft.write_text(
            "#!/usr/bin/env python3\nimport os, signal, sys\n"
            "if '--version' in sys.argv: print('0.10.1'); raise SystemExit(0)\n"
            "if sys.argv[1] == 'build': os.kill(os.getppid(), signal.SIGKILL)\n"
            "print('src/app.py:1')\n",
            encoding="utf-8",
        )
        graft.chmod(graft.stat().st_mode | stat.S_IXUSR)
        ri._state_dir(self.root)
        ready = ri._base_state(self.root.resolve(), "graft", ri.GRAFT_VERSION)
        ri._write_json(ri._state_path(self.root.resolve(), "graft"), ready)
        with mock.patch.dict(os.environ, self.env_path(graft), clear=False):
            result = subprocess.run(
                [sys.executable, str(SCRIPT), "graft", "--root", str(self.root.resolve()), "map"],
                text=True, capture_output=True, env={**os.environ, **self.env_path(graft)},
            )
        self.assertEqual(result.returncode, -signal.SIGKILL)
        self.assertEqual(ri.read_state(self.root, "graft")["status"], "unavailable")

    def test_r12_graphify_commands_require_real_paths_and_force_flag(self) -> None:
        graphify = self.root / "bin" / "graphify"
        graphify.parent.mkdir(exist_ok=True)
        calls = self.root / ri.STATE_DIR / "graphify-calls"
        graphify.write_text(
            "#!/usr/bin/env python3\nimport json, pathlib, sys\n"
            f"log = pathlib.Path({str(calls)!r})\n"
            "log.parent.mkdir(parents=True, exist_ok=True)\n"
            "with log.open('a') as stream: stream.write(json.dumps(sys.argv[1:]) + '\\n')\n"
            "if '--version' in sys.argv: print('0.9.14'); raise SystemExit(0)\n"
            "if sys.argv[1] in {'extract', 'update'} and (len(sys.argv) < 3 or pathlib.Path(sys.argv[2]).resolve() != pathlib.Path.cwd().resolve()): raise SystemExit(2)\n"
            "if sys.argv[1] == 'extract' and ('--out' not in sys.argv or pathlib.Path(sys.argv[sys.argv.index('--out') + 1]).resolve() != pathlib.Path.cwd().resolve() or '--full-rebuild' in sys.argv): raise SystemExit(2)\n"
            "if sys.argv[1] == 'update' and not pathlib.Path('src/app.py').exists() and '--force' not in sys.argv: raise SystemExit(1)\n"
            "print('domain -> src/app.py:1')\n",
            encoding="utf-8",
        )
        graphify.chmod(graphify.stat().st_mode | stat.S_IXUSR)
        with mock.patch.dict(os.environ, self.env_path(graphify), clear=False):
            ri.graphify_setup(self.root, "claude-cli", "deep", announce=False)
            (self.root / "src/app.py").unlink()
            result = ri._run_context(self.root, "graphify", "path", ["domain"])
        self.assertIn("domain -> src/app.py:1", result["context"])
        commands = [json.loads(line) for line in calls.read_text(encoding="utf-8").splitlines()]
        extract = next(command for command in commands if command[0] == "extract")
        updates = [command for command in commands if command[0] == "update"]
        self.assertEqual(extract[1], str(self.root.resolve()))
        self.assertIn("--mode", extract)
        self.assertEqual(extract[extract.index("--out") + 1], str(self.root))
        self.assertGreaterEqual(len(updates), 2)
        self.assertEqual(updates[0], ["update", str(self.root.resolve())])
        self.assertIn("--force", updates[-1])
        self.assertEqual(updates[-1][1], str(self.root.resolve()))
        self.assertNotIn("--full-rebuild", " ".join(command for command in extract))
        self.assertNotIn("src/app.py", ri.read_state(self.root, "graphify")["indexed_source_manifest"])

    def test_r14_code_only_setup_uses_mode_without_backend(self) -> None:
        graphify = self.root / "bin" / "graphify"
        graphify.parent.mkdir(exist_ok=True)
        calls = self.root / ri.STATE_DIR / "graphify-calls"
        checkout = str(self.root.resolve())
        graphify.write_text(
            "#!/usr/bin/env python3\nimport json, pathlib, sys\n"
            f"log = pathlib.Path({str(calls)!r})\n"
            "log.parent.mkdir(parents=True, exist_ok=True)\n"
            "with log.open('a') as stream: stream.write(json.dumps(sys.argv[1:]) + '\\n')\n"
            "if '--version' in sys.argv: print('0.9.14'); raise SystemExit(0)\n"
            f"if sys.argv[1:] == ['extract', {checkout!r}, '--code-only', '--out', {checkout!r}]: pass\n"
            "elif sys.argv[1] == 'extract' and '--backend' in sys.argv and 'code-only' not in sys.argv: pass\n"
            "else: raise SystemExit(2)\n"
            "print('domain -> src/app.py:1')\n",
            encoding="utf-8",
        )
        graphify.chmod(graphify.stat().st_mode | stat.S_IXUSR)
        environment = {**os.environ, **self.env_path(graphify)}
        setup = subprocess.run(
            [sys.executable, str(SCRIPT), "graphify-setup", "--root", checkout, "--backend", "code-only", "--mode", "code-only"],
            text=True, capture_output=True, env=environment,
        )
        self.assertEqual(setup.returncode, 0, setup.stderr)
        setup_payload = json.loads(setup.stdout.splitlines()[-1])
        self.assertEqual(setup_payload["status"], "partial")
        self.assertEqual(setup_payload["backend"], "code-only")

        status = subprocess.run(
            [sys.executable, str(SCRIPT), "status", "--root", checkout, "--json"],
            text=True, capture_output=True, env=environment,
        )
        self.assertEqual(status.returncode, 0, status.stderr)
        status_payload = json.loads(status.stdout)
        self.assertEqual(status_payload["tools"]["graphify"]["status"], "partial")
        self.assertEqual(status_payload["tools"]["graphify"]["backend"], "code-only")

        with mock.patch.dict(os.environ, environment, clear=False):
            ri.graphify_setup(self.root.resolve(), "claude-cli", "deep", announce=False)
        commands = [json.loads(line) for line in calls.read_text(encoding="utf-8").splitlines()]
        self.assertIn(["extract", checkout, "--code-only", "--out", checkout], commands)
        self.assertIn(["extract", checkout, "--mode", "deep", "--backend", "claude-cli", "--out", checkout], commands)

    def test_r3_query_timeout_is_degraded(self) -> None:
        graft = self.fake_tool("graft", ri.GRAFT_VERSION)
        original_run = ri._run

        def run(command, root, **kwargs):
            if command[1] == "map":
                raise ri.IntelligenceError("graft timed out")
            return original_run(command, root, **kwargs)

        with mock.patch.dict(os.environ, self.env_path(graft), clear=False), mock.patch.object(ri, "_run", side_effect=run):
            with self.assertRaisesRegex(ri.IntelligenceError, "timed out"):
                ri._run_context(self.root, "graft", "map", [])
        self.assertEqual(ri.read_state(self.root, "graft")["status"], "unavailable")

    def test_r4_public_query_timeout_converts_subprocess_exception(self) -> None:
        graft = self.fake_tool("graft", ri.GRAFT_VERSION)
        original_run = subprocess.run

        def run(command, *args, **kwargs):
            if Path(command[0]).name == "graft" and len(command) > 1 and command[1] == "map":
                raise subprocess.TimeoutExpired(command, kwargs.get("timeout", 0))
            return original_run(command, *args, **kwargs)

        stdout = StringIO()
        stderr = StringIO()
        with mock.patch.dict(os.environ, self.env_path(graft), clear=False), mock.patch.object(subprocess, "run", side_effect=run), mock.patch("sys.stdout", stdout), mock.patch("sys.stderr", stderr):
            exit_code = ri.main(["graft", "--root", str(self.root), "map"])

        self.assertEqual(exit_code, 3)
        payload = json.loads(stdout.getvalue())
        self.assertEqual(payload["status"], "degraded")
        self.assertEqual(payload["reason"], "graft timed out")
        self.assertEqual(payload["fallback"], ri.DEGRADED_FALLBACK)
        self.assertEqual(stderr.getvalue().strip(), "graft timed out")
        self.assertEqual(ri.read_state(self.root, "graft")["status"], "unavailable")

    def test_r3_query_failure_is_degraded(self) -> None:
        graft = self.fake_tool("graft", ri.GRAFT_VERSION)
        original_run = ri._run

        def run(command, root, **kwargs):
            if command[1] == "map":
                return subprocess.CompletedProcess(command, 1, "", "failed")
            return original_run(command, root, **kwargs)

        with mock.patch.dict(os.environ, self.env_path(graft), clear=False), mock.patch.object(ri, "_run", side_effect=run):
            with self.assertRaisesRegex(ri.IntelligenceError, "query failed"):
                ri._run_context(self.root, "graft", "map", [])
        self.assertEqual(ri.read_state(self.root, "graft")["status"], "unavailable")

    def test_r3_graphify_budget_keeps_bounded_architecture_pointers(self) -> None:
        context, status = ri._bounded_output("domain -> src/app.py:1\n" + ("architecture detail " * 5000))
        self.assertEqual(status, "partial")
        self.assertIn("domain -> src/app.py:1", context)
        self.assertLessEqual(len(context), ri.MAX_CONTEXT_CHARS)

    def test_r2_all_indexed_file_classes_refresh_state(self) -> None:
        graft = self.fake_tool("graft", ri.GRAFT_VERSION)
        with mock.patch.dict(os.environ, self.env_path(graft), clear=False):
            previous = ri._run_context(self.root, "graft", "map", [])
            (self.root / "src/app.py").write_text("def changed(): pass\n", encoding="utf-8")
            (self.root / "contract.md").write_text("contract\n", encoding="utf-8")
            (self.root / "config.json").write_text("{}\n", encoding="utf-8")
            (self.root / "docs.md").write_text("docs\n", encoding="utf-8")
            refreshed = ri._run_context(self.root, "graft", "map", [])
            self.assertNotEqual(previous["tree"], refreshed["tree"])
            manifest = ri.read_state(self.root, "graft")["indexed_source_manifest"]
            self.assertTrue({"contract.md", "config.json", "docs.md"}.issubset(manifest))
            (self.root / "src/app.py").unlink()
            deleted = ri._run_context(self.root, "graft", "map", [])
        self.assertNotEqual(refreshed["tree"], deleted["tree"])
        self.assertNotIn("src/app.py", ri.read_state(self.root, "graft")["indexed_source_manifest"])

    def test_r2_interrupted_tool_publication_marks_state_unavailable(self) -> None:
        path = self.root / "bin" / "graft"
        path.parent.mkdir(exist_ok=True)
        path.write_text(
            "#!/usr/bin/env python3\nimport pathlib, sys\n"
            "if '--version' in sys.argv: print('0.10.1'); raise SystemExit(0)\n"
            "if sys.argv[1] == 'build': pathlib.Path('graft').mkdir(exist_ok=True); pathlib.Path('graft/partial').write_text('partial'); raise SystemExit(1)\n"
            "print('src/app.py:1')\n",
            encoding="utf-8",
        )
        path.chmod(path.stat().st_mode | stat.S_IXUSR)
        with mock.patch.dict(os.environ, self.env_path(path), clear=False):
            with self.assertRaisesRegex(ri.IntelligenceError, "refresh failed"):
                ri._run_context(self.root, "graft", "map", [])
        state = ri.read_state(self.root, "graft")
        self.assertEqual(state["status"], "unavailable")
        self.assertNotEqual(state.get("status"), "ready")

    def test_r2_generated_state_is_ignored_and_not_staged(self) -> None:
        probe = ROOT / ri.STATE_DIR / "probe"
        probe.parent.mkdir(mode=0o700, exist_ok=True)
        probe.write_text("local\n", encoding="utf-8")
        try:
            ignored = subprocess.run(["git", "check-ignore", "--quiet", str(probe.relative_to(ROOT))], cwd=ROOT)
            self.assertEqual(ignored.returncode, 0)
            staged = subprocess.run(["git", "add", "--dry-run", "--", str(probe.relative_to(ROOT))], cwd=ROOT, text=True, capture_output=True)
            self.assertNotEqual(staged.returncode, 0)
            self.assertEqual(staged.stdout, "")
        finally:
            probe.unlink(missing_ok=True)
            try:
                probe.parent.rmdir()
            except OSError:
                pass

    def test_r2_mutation_waits_for_read_lock_in_another_process(self) -> None:
        marker = self.root / "mutation-complete"
        code = (
            "import sys\nfrom pathlib import Path\n"
            "sys.path.insert(0, sys.argv[2])\nimport repository_intelligence as ri\n"
            "root=Path(sys.argv[1])\n"
            "with ri.mutation_lock(root):\n"
            "    Path(root / 'mutation-complete').write_text('done')\n"
        )
        with ri.read_lock(self.root):
            child = subprocess.Popen([sys.executable, "-c", code, str(self.root), str(SCRIPT.parent)])
            self.assertIsNone(child.poll())
        self.assertEqual(child.wait(timeout=2), 0)
        self.assertEqual(marker.read_text(encoding="utf-8"), "done")


class BenchmarkTests(unittest.TestCase):
    def record(self, task: str, configuration: str, *, tree: str = "tree", category: str = "local") -> dict:
        metrics = {field: 1 for field in SPEC_METRIC_FIELDS}
        metrics["total_tokens"] = metrics["input_tokens"] + metrics["output_tokens"]
        return {
            "schema": 1, "task_id": task, "category": category, "configuration": configuration,
            "tree": tree, "prompt_hash": "prompt", "acceptance_contract_hash": "contract",
            "provider": "provider", "model": "model", "effort": "high",
            "metrics": metrics, "gate": "PASS",
            "verifier": "PASS", "outcome": "success",
        }

    def test_ut009_mismatch_names_every_control(self) -> None:
        records = [self.record(str(i), configuration) for i in range(10) for configuration in ("graft", "routed")]
        records[1]["tree"] = "other"
        records[1]["model"] = "other-model"
        with tempfile.NamedTemporaryFile(mode="w", suffix=".jsonl") as handle:
            handle.write("\n".join(json.dumps(record) for record in records)); handle.flush()
            with self.assertRaisesRegex(ValueError, "model.*tree|tree.*model"):
                ri.benchmark_report(handle.name)

    def test_r2_each_control_mismatch_is_named(self) -> None:
        for field in ri.CONTROL_FIELDS:
            records = [self.record(str(i), configuration) for i in range(10) for configuration in ("graft", "routed")]
            records[1][field] = "mismatch"
            with tempfile.NamedTemporaryFile(mode="w", suffix=".jsonl") as handle:
                handle.write("\n".join(json.dumps(record) for record in records)); handle.flush()
                with self.assertRaisesRegex(ValueError, field):
                    ri.benchmark_report(handle.name)

    def test_ut012_controlled_runs_group_by_configuration(self) -> None:
        records = [self.record(str(i), configuration, category="local" if i < 5 else "bug") for i in range(10) for configuration in ("graft", "routed")]
        with tempfile.NamedTemporaryFile(mode="w", suffix=".jsonl") as handle:
            handle.write("\n".join(json.dumps(record) for record in records)); handle.flush()
            result = ri.benchmark_report(handle.name)
        self.assertEqual(result["tasks"], 10)
        self.assertEqual(result["runs"], 20)
        self.assertEqual(result["categories"]["local"]["configurations"]["graft"]["tasks"], 5)
        self.assertEqual(result["categories"]["bug"]["configurations"]["routed"]["tasks"], 5)
        self.assertEqual(result["comparison"], "graft-to-routed")
        self.assertEqual(set(result["categories"]["local"]["configurations"]["graft"]["metrics"]), set(SPEC_METRIC_FIELDS))

    def test_r3_distinct_task_bounds_reject_duplicate_pairs(self) -> None:
        records = [self.record(str(i), configuration) for i in range(5) for configuration in ("graft", "routed")]
        with tempfile.NamedTemporaryFile(mode="w", suffix=".jsonl") as handle:
            handle.write("\n".join(json.dumps(record) for record in records)); handle.flush()
            with self.assertRaisesRegex(ValueError, "distinct task"):
                ri.benchmark_report(handle.name)

    def test_r3_required_metrics_are_literal_contract_fields(self) -> None:
        records = [self.record(str(i), configuration) for i in range(10) for configuration in ("graft", "routed")]
        del records[0]["metrics"]["native_search_calls"]
        with tempfile.NamedTemporaryFile(mode="w", suffix=".jsonl") as handle:
            handle.write("\n".join(json.dumps(record) for record in records)); handle.flush()
            with self.assertRaisesRegex(ValueError, "native_search_calls"):
                ri.benchmark_report(handle.name)

    def test_r2_baseline_to_graft_comparison_is_explicit(self) -> None:
        records = [self.record(str(i), configuration) for i in range(10) for configuration in ("baseline", "graft")]
        with tempfile.NamedTemporaryFile(mode="w", suffix=".jsonl") as handle:
            handle.write("\n".join(json.dumps(record) for record in records)); handle.flush()
            result = ri.benchmark_report(handle.name)
        self.assertEqual(result["comparison"], "baseline-to-graft")

    def test_r2_short_and_long_benchmark_boundaries_are_rejected(self) -> None:
        for count in (8, 21):
            records = [self.record(str(i), configuration) for i in range(count) for configuration in ("graft", "routed")]
            with tempfile.NamedTemporaryFile(mode="w", suffix=".jsonl") as handle:
                handle.write("\n".join(json.dumps(record) for record in records)); handle.flush()
                with self.assertRaisesRegex(ValueError, "10-20"):
                    ri.benchmark_report(handle.name)

    def test_it019_success_requires_independent_evidence(self) -> None:
        record = self.record("1", "graft"); record["gate"] = "FAIL"
        records = [record, self.record("1", "routed")] + [self.record(str(i), configuration) for i in range(2, 6) for configuration in ("graft", "routed")]
        with tempfile.NamedTemporaryFile(mode="w", suffix=".jsonl") as handle:
            handle.write("\n".join(json.dumps(item) for item in records)); handle.flush()
            with self.assertRaisesRegex(ValueError, "gate/Verifier"):
                ri.benchmark_report(handle.name)

    def test_it019_malformed_and_short_benchmarks_rejected(self) -> None:
        with tempfile.NamedTemporaryFile(mode="w", suffix=".jsonl") as handle:
            handle.write("not-json\n"); handle.flush()
            with self.assertRaisesRegex(ValueError, "malformed"):
                ri.benchmark_report(handle.name)

    def test_it019_unavailable_metrics_are_explicit(self) -> None:
        records = [self.record(str(i), configuration) for i in range(10) for configuration in ("graft", "routed")]
        records[0]["metrics"]["input_tokens"] = "unavailable"
        with tempfile.NamedTemporaryFile(mode="w", suffix=".jsonl") as handle:
            handle.write("\n".join(json.dumps(record) for record in records)); handle.flush()
            result = ri.benchmark_report(handle.name)
        self.assertEqual(result["tasks"], 10)

    def test_r2_missing_full_evidence_fields_is_rejected(self) -> None:
        record = self.record("1", "graft")
        del record["metrics"]["total_tokens"]
        records = [record, self.record("1", "routed")] + [self.record(str(i), configuration) for i in range(2, 11) for configuration in ("graft", "routed")]
        with tempfile.NamedTemporaryFile(mode="w", suffix=".jsonl") as handle:
            handle.write("\n".join(json.dumps(item) for item in records)); handle.flush()
            with self.assertRaisesRegex(ValueError, "total_tokens"):
                ri.benchmark_report(handle.name)

    def test_r2_removal_recommendation_requires_explicit_surface_decision(self) -> None:
        records = [self.record(str(i), configuration) for i in range(10) for configuration in ("graft", "routed")]
        records[0]["retention_recommendation"] = "remove"
        with tempfile.NamedTemporaryFile(mode="w", suffix=".jsonl") as handle:
            handle.write("\n".join(json.dumps(record) for record in records)); handle.flush()
            with self.assertRaisesRegex(ValueError, "explicit project decision"):
                ri.benchmark_report(handle.name)
        records[0]["project_decision"] = {"id": "AD-999", "approved": True, "surfaces": sorted(ri.REMOVAL_SURFACES)}
        with tempfile.NamedTemporaryFile(mode="w", suffix=".jsonl") as handle:
            handle.write("\n".join(json.dumps(record) for record in records)); handle.flush()
            result = ri.benchmark_report(handle.name)
        self.assertTrue(result["removal_decision_required"])

    def test_r2_record_benchmark_writes_complete_terminal_record(self) -> None:
        record = self.record("1", "graft")
        with tempfile.NamedTemporaryFile(mode="w", suffix=".jsonl") as handle:
            ri.record_benchmark(handle.name, record)
            stored = json.loads(Path(handle.name).read_text(encoding="utf-8"))
        self.assertEqual(stored["metrics"]["total_tokens"], 2)

    def test_r1_disjoint_task_ids_cannot_bypass_control_matching(self) -> None:
        records = [self.record(str(i), "graft") for i in range(10)] + [self.record("0", "routed")]
        records[0]["tree"] = "other-tree"
        records[0]["provider"] = "other-provider"
        with tempfile.NamedTemporaryFile(mode="w", suffix=".jsonl") as handle:
            handle.write("\n".join(json.dumps(record) for record in records)); handle.flush()
            with self.assertRaisesRegex(ValueError, "matched task/category/configuration"):
                ri.benchmark_report(handle.name)


if __name__ == "__main__":
    unittest.main()
