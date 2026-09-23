"""Canonical contract tests for the bundled Deep Review gates.

Run: python3 tools/test_deep_review_contract.py
"""

from __future__ import annotations

import json
import hashlib
import os
import re
import subprocess
import sys
import tempfile
import unittest
import unittest.mock
from pathlib import Path

sys.dont_write_bytecode = True

SCRIPTS = Path(__file__).resolve().parents[1] / ".agents/skills/wtk-deep-review/scripts"
BUILD_MANIFEST = SCRIPTS / "build_manifest.py"
BUILD_JOBS = SCRIPTS / "build_jobs.py"
MERGE_FINDINGS = SCRIPTS / "merge_findings.py"
RUN_JOBS = SCRIPTS / "run_jobs.py"
RENDER_REVIEW = SCRIPTS / "render_review.py"
RENDER_HTML = SCRIPTS / "render_html.py"
BUILD_KNOWLEDGE = SCRIPTS / "build_knowledge.py"
PUBLISH_RECIPE = (
    Path(__file__).resolve().parents[1]
    / ".agents/skills/wtk-deep-review/references/publish-github.md"
)
sys.path.insert(0, str(SCRIPTS))

from _common import fingerprint, freeze_snapshot  # noqa: E402
from build_jobs import validate_cohorts  # noqa: E402
from merge_findings import coverage_ledger, group_duplicates, merge_group, reconcile  # noqa: E402


def git(root: Path, *args: str) -> str:
    result = subprocess.run(["git", *args], cwd=root, capture_output=True, text=True)
    if result.returncode:
        raise AssertionError(result.stderr or result.stdout)
    return result.stdout.strip()


def run_script(script: Path, root: Path, *args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(script), *args], cwd=root, capture_output=True, text=True
    )


def publish_walkthrough_recipe() -> str:
    document = PUBLISH_RECIPE.read_text(encoding="utf-8")
    section = document[document.index("## 1. Upsert the walkthrough comment") :]
    start = section.index("```bash") + len("```bash\n")
    end = section.index("```", start)
    return section[start:end]


def init_repo(raw: str) -> Path:
    root = Path(raw)
    git(root, "init", "-q")
    git(root, "config", "user.email", "test@example.com")
    git(root, "config", "user.name", "wtk-deep-review tests")
    (root / "source.txt").write_text("a\n", encoding="utf-8")
    git(root, "add", "source.txt")
    git(root, "commit", "-qm", "initial")
    return root


def valid_payload() -> dict:
    return {
        "defects": [],
        "advisories": [],
        "suppressions": [],
        "coverage": {"hunks": [], "rules": []},
    }


def write_job_round(root: Path, *, payload: dict | None = None, job: dict | None = None) -> Path:
    out = root / ".wtk-deep-review" / "out"
    out.mkdir(parents=True)
    head = git(root, "rev-parse", "HEAD")
    (out / "manifest.json").write_text(
        json.dumps(
            {
                "target": "test",
                "mode": "full",
                "round": 1,
                "concurrency": 3,
                "base": head,
                "effective_base": head,
                "head": head,
                "diff_command": "git diff HEAD..HEAD -- <file>",
                "worktree_snapshot": freeze_snapshot(root, out),
                "files": [],
            }
        ),
        encoding="utf-8",
    )
    prompt = out / "prompt.md"
    prompt.write_text("review\n", encoding="utf-8")
    output = out / "agents" / "job.json"
    output.parent.mkdir()
    if payload is not None:
        output.write_text(json.dumps(payload), encoding="utf-8")
    (out / "jobs.json").write_text(
        json.dumps(
            {
                "jobs": [
                    {
                        "label": "sweep-tests",
                        "kind": "sweep",
                        "lane": "sweep",
                        "prompt": str(prompt.relative_to(root)),
                        "output": str(output.relative_to(root)),
                        "required_hunks": [],
                        "rule_ids": [],
                        **(job or {}),
                    }
                ]
            }
        ),
        encoding="utf-8",
    )
    return out


def validate_status(root: Path, out: Path) -> tuple[subprocess.CompletedProcess[str], dict]:
    result = run_script(RUN_JOBS, root, "--out", str(out), "--validate-only")
    status = json.loads((out / "runs/jobs-status.json").read_text(encoding="utf-8"))
    return result, status["jobs"][0]


def render_fixture(root: Path, findings: list[dict]) -> Path:
    out = root / ".wtk-deep-review" / "render"
    out.mkdir(parents=True)
    head = git(root, "rev-parse", "HEAD")
    (out / "manifest.json").write_text(
        json.dumps(
            {
                "target": "test",
                "mode": "full",
                "round": 1,
                "concurrency": 3,
                "base": head,
                "head": head,
                "worktree_snapshot": freeze_snapshot(root, out),
                "files": [],
            }
        ),
        encoding="utf-8",
    )
    (out / "rules.json").write_text(json.dumps({"rules": []}), encoding="utf-8")
    (out / "context-pack.md").write_text("# Context\n", encoding="utf-8")
    (out / "findings.json").write_text(
        json.dumps(
            {
                "findings": findings,
                "advisories": [],
                "summary": {"merged_raw": 0},
                "review_stats": {"coverage": {"selected_hunk_lines": 0}},
                "reconciliation": {"resolved": [], "still_open_unreviewed": []},
            }
        ),
        encoding="utf-8",
    )
    return out


def finding(severity: str) -> dict:
    return {
        "fingerprint": f"fp-{severity}",
        "result_kind": "defect",
        "round_status": "new",
        "file": "source.txt",
        "line": 1,
        "end_line": None,
        "in_diff": False,
        "hunk": None,
        "category": "potential-issue",
        "severity": severity,
        "quick_win": False,
        "title": f"{severity} finding",
        "body": "The contract is violated.",
        "rule_ids": [],
        "evidence": ["Premise: contract fails → Path: source.txt:1 → Verdict: blocked."],
    }


def incremental_fixture(root: Path, *, sweeps: list[str], prior_status: str = "open") -> tuple[Path, dict]:
    """Round 1 with one open Major, a fix commit, then an incremental manifest and jobs."""
    base = git(root, "rev-parse", "HEAD")
    major = {
        **finding("major"),
        "also_applies": ["source.txt:7"],
        "evidence": ["Premise: guard missing → Path: the caller skips the guard → Verdict: blocked."],
    }
    out = render_fixture(root, [major])
    first = run_script(RENDER_REVIEW, root, "--out", str(out))
    assert first.returncode == 0, first.stdout + first.stderr
    state = json.loads((out / "state.json").read_text(encoding="utf-8"))
    state["ledger"]["fp-major"]["status"] = prior_status
    (out / "state.json").write_text(json.dumps(state), encoding="utf-8")

    (root / "source.txt").write_text("a\nguarded\n", encoding="utf-8")
    git(root, "add", "source.txt")
    git(root, "commit", "-qm", "fix: add the guard")
    manifest = run_script(BUILD_MANIFEST, root, "--out", str(out), "--base", base)
    assert manifest.returncode == 0, manifest.stdout + manifest.stderr
    assert json.loads((out / "manifest.json").read_text(encoding="utf-8"))["mode"] == "incremental"
    (out / "plan.json").write_text(json.dumps({
        "cohorts": [
            {"id": "A", "name": "first", "risk": "normal", "files": ["source.txt"]},
            {"id": "B", "name": "second", "risk": "low", "files": ["missing.txt"]},
        ],
        "sweeps": sweeps,
    }), encoding="utf-8")
    (out / "rules.json").write_text(json.dumps({"rules": [], "sources": []}), encoding="utf-8")
    (out / "knowledge.json").write_text(
        json.dumps({"selected_paths": ["source.txt"], "sources": []}), encoding="utf-8"
    )
    build = run_script(BUILD_JOBS, root, "--out", str(out))
    assert build.returncode == 0, build.stdout + build.stderr
    return out, {"stdout": build.stdout, "head": git(root, "rev-parse", "HEAD"), "major": major}


def full_fixture(root: Path, plan: dict, *, files: int = 3, lines: int = 1) -> tuple[Path, subprocess.CompletedProcess[str]]:
    """Full-mode round: <files> new <lines>-line files in one commit, then build_jobs.py on <plan>."""
    base = git(root, "rev-parse", "HEAD")
    names = [f"file{i}.txt" for i in range(files)]
    for name in names:
        (root / name).write_text("changed\n" * lines, encoding="utf-8")
    git(root, "add", *names)
    git(root, "commit", "-qm", "feat: three files")
    out = root / ".wtk-deep-review" / "full"
    manifest = run_script(BUILD_MANIFEST, root, "--out", str(out), "--base", base)
    assert manifest.returncode == 0, manifest.stdout + manifest.stderr
    (out / "plan.json").write_text(json.dumps({"sweeps": [], **plan}), encoding="utf-8")
    (out / "rules.json").write_text(json.dumps({"rules": [], "sources": []}), encoding="utf-8")
    (out / "knowledge.json").write_text(json.dumps({"selected_paths": names, "sources": []}), encoding="utf-8")
    (out / "context-pack.md").write_text("# Context\n", encoding="utf-8")
    return out, run_script(BUILD_JOBS, root, "--out", str(out))


def knowledge_round_one(root: Path) -> tuple[Path, str]:
    """AGENTS.md at the base, a round-1 full manifest with rules.json marking it applied."""
    (root / "AGENTS.md").write_text("# Agents\n\nUse the alpha skill.\n", encoding="utf-8")
    git(root, "add", "AGENTS.md")
    git(root, "commit", "-qm", "docs: agents")
    base = git(root, "rev-parse", "HEAD")
    (root / "source.txt").write_text("a\nb\n", encoding="utf-8")
    git(root, "add", "source.txt")
    git(root, "commit", "-qm", "feat: change")
    out = root / ".wtk-deep-review" / "out"
    result = run_script(BUILD_MANIFEST, root, "--out", str(out), "--base", base)
    assert result.returncode == 0, result.stdout + result.stderr
    (out / "rules.json").write_text(json.dumps({
        "sources": [{"source": "AGENTS.md", "kind": "instruction", "status": "applied", "reason": "root rules"}],
        "rules": [{"id": "R1", "source": "AGENTS.md", "guideline": "Use the alpha skill.", "scope": ["**/*"]}],
    }), encoding="utf-8")
    (out / "knowledge.json").write_text(json.dumps({"selected_paths": ["source.txt"], "sources": []}), encoding="utf-8")
    (out / "state.json").write_text(json.dumps({"rounds": [{"n": 1, "head": git(root, "rev-parse", "HEAD")}]}), encoding="utf-8")
    return out, base


def raw_defect(raw_id: str, title: str, line: int, end_line: int, suggestion: str) -> dict:
    item = {
        "raw_id": raw_id, "source_job": f"job-{raw_id}", "result_kind": "defect",
        "file": "booking.py", "category": "potential-issue", "severity": "major",
        "line": line, "end_line": end_line, "in_diff": True, "hunk": "new:100-108",
        "quick_win": False, "rule_ids": [], "title": title, "body": title,
        "evidence": [f"Premise: {title} → Path: booking.py:{line} → Verdict: blocked."],
        "suggestion": suggestion,
    }
    return {**item, "fingerprint": fingerprint(item)}


class DeepReviewContractTests(unittest.TestCase):
    def test_distinct_fingerprints_on_overlapping_lines_never_merge(self) -> None:
        # UT-001 (P1 AC1)
        first = raw_defect("RD0001", "Reject bookings owned by another account", 100, 105, "check_owner()")
        second = raw_defect("RD0002", "Reject negative booking amounts", 103, 108, "check_amount()")
        groups = group_duplicates([first, second])
        self.assertEqual(len(groups), 2)
        merged = {m["raw_id"]: m for m in (merge_group(g) for g in groups)}
        for raw in (first, second):
            self.assertEqual(merged[raw["raw_id"]]["evidence"][0], raw["evidence"][0])
            self.assertEqual(merged[raw["raw_id"]]["suggestion"], raw["suggestion"])
            self.assertEqual(merged[raw["raw_id"]]["also_applies"], [])

    def test_identical_fingerprints_merge_and_keep_anchors(self) -> None:
        # UT-002 (P1 AC2)
        first = raw_defect("RD0001", "Reject negative booking amounts", 10, 10, "check_amount()")
        second = raw_defect("RD0002", "Reject negative booking amounts", 40, 40, "check_amount()")
        groups = group_duplicates([first, second])
        self.assertEqual(len(groups), 1)
        self.assertIn("booking.py:40", merge_group(groups[0])["also_applies"])

    def test_prior_open_major_without_disposition_blocks_ship(self) -> None:
        # IT-001 (P1 AC5)
        with tempfile.TemporaryDirectory() as raw:
            root = init_repo(raw)
            out = render_fixture(root, [])
            head = git(root, "rev-parse", "HEAD")
            manifest = json.loads((out / "manifest.json").read_text(encoding="utf-8"))
            (out / "manifest.json").write_text(json.dumps({**manifest, "round": 2}), encoding="utf-8")
            (out / "state.json").write_text(json.dumps({
                "target": "test", "rounds": [{"n": 1, "head": head}],
                "ledger": {"fp-major": {
                    "file": "source.txt", "title": "Original defect still exists.",
                    "severity": "major", "status": "open", "round": 1,
                    "result_kind": "defect", "comment_id": None, "resolved_in": None,
                }},
            }), encoding="utf-8")
            ledger = json.loads((out / "findings.json").read_text(encoding="utf-8"))
            ledger["reconciliation"] = {"resolved": [], "still_open_unreviewed": ["fp-major"]}
            (out / "findings.json").write_text(json.dumps(ledger), encoding="utf-8")

            result = run_script(RENDER_REVIEW, root, "--out", str(out))
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            review = (out / "review.md").read_text(encoding="utf-8")
            verdict_line = next(line for line in review.splitlines() if line.startswith("**Verdict:"))
            self.assertTrue(verdict_line.startswith("**Verdict: FIX_BEFORE_SHIP**"), verdict_line)
            duplicates = review.split("## Duplicates", 1)[1].split("## Advisories", 1)[0]
            self.assertIn("Original defect still exists.", duplicates)
            state = json.loads((out / "state.json").read_text(encoding="utf-8"))
            self.assertEqual(state["ledger"]["fp-major"]["status"], "open")
            self.assertEqual(state["rounds"][-1]["verdict"], "FIX_BEFORE_SHIP")

    def test_same_round_snapshot_drift_archives_reviewer_outputs(self) -> None:
        # IT-002 (P1 AC6)
        with tempfile.TemporaryDirectory() as raw:
            root = init_repo(raw)
            out = write_job_round(root, payload=valid_payload())
            old = json.loads((out / "manifest.json").read_text(encoding="utf-8"))["worktree_snapshot"]
            original = (out / "agents/job.json").read_bytes()
            (root / "source.txt").write_text("changed after reviewer finished\n", encoding="utf-8")
            restarted = run_script(BUILD_MANIFEST, root, "--out", str(out), "--base", "HEAD", "--worktree")
            self.assertEqual(restarted.returncode, 0, restarted.stdout + restarted.stderr)
            self.assertIn("stale outputs archived: 1", restarted.stdout)
            self.assertEqual(list((out / "agents").iterdir()), [])
            self.assertEqual((out / "rounds" / f"round-1-stale-{old[:12]}" / "job.json").read_bytes(), original)
            result, row = validate_status(root, out)
            self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
            self.assertEqual(row["status"], "pending")

    def test_same_round_unchanged_snapshot_keeps_reviewer_outputs(self) -> None:
        # IT-003 (P1 AC7)
        with tempfile.TemporaryDirectory() as raw:
            root = init_repo(raw)
            out = write_job_round(root, payload=valid_payload())
            restarted = run_script(BUILD_MANIFEST, root, "--out", str(out), "--base", "HEAD", "--worktree")
            self.assertEqual(restarted.returncode, 0, restarted.stdout + restarted.stderr)
            self.assertNotIn("stale outputs archived", restarted.stdout)
            self.assertTrue((out / "agents/job.json").is_file())
            self.assertFalse((out / "rounds").exists())
            result, row = validate_status(root, out)
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            self.assertEqual(row["status"], "valid")

    def test_undispositioned_prior_open_finding_stays_open(self) -> None:
        # UT-003 (P1 AC3)
        prior = {"rounds": [{"n": 1}], "ledger": {"fp-major": {"status": "open", "file": "source.txt"}}}
        result = reconcile([], set(), prior, [])
        self.assertEqual(result["still_open_unreviewed"], ["fp-major"])
        self.assertEqual(result["resolved"], [])

    def test_resolved_disposition_resolves_prior_finding(self) -> None:
        # UT-004 (P1 AC4)
        prior = {"rounds": [{"n": 1}], "ledger": {"fp-major": {"status": "open", "file": "source.txt"}}}
        rows = [{"fingerprint": "fp-major", "status": "resolved", "evidence": "source.txt:1 → gone"}]
        result = reconcile([], set(), prior, rows)
        self.assertEqual(result["resolved"], ["fp-major"])
        self.assertEqual(result["still_open_unreviewed"], [])

    def test_missing_prior_disposition_invalidates_output(self) -> None:
        # IT-008 (P2 AC5)
        with tempfile.TemporaryDirectory() as raw:
            root = init_repo(raw)
            out = write_job_round(root, payload=valid_payload(), job={"prior_fingerprints": ["fp-major"]})
            result, row = validate_status(root, out)
            self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
            self.assertEqual(row["status"], "invalid")
            self.assertIn("fp-major", row["reason"])

        with tempfile.TemporaryDirectory() as raw:
            root = init_repo(raw)
            payload = {**valid_payload(), "prior_findings": [
                {"fingerprint": "fp-major", "status": "open", "evidence": "source.txt:1 → still there"}
            ]}
            out = write_job_round(root, payload=payload, job={"prior_fingerprints": ["fp-major"]})
            result, row = validate_status(root, out)
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            self.assertEqual(row["status"], "valid")

    def test_full_mode_rejects_prior_dispositions(self) -> None:
        # IT-009 (P2 AC6)
        with tempfile.TemporaryDirectory() as raw:
            root = init_repo(raw)
            payload = {**valid_payload(), "prior_findings": [
                {"fingerprint": "fp-major", "status": "resolved", "evidence": "source.txt:1 → gone"}
            ]}
            out = write_job_round(root, payload=payload)
            result, row = validate_status(root, out)
            self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
            self.assertEqual(row["status"], "invalid")

        with tempfile.TemporaryDirectory() as raw:
            root = init_repo(raw)
            out = write_job_round(root, payload=valid_payload())
            result, row = validate_status(root, out)
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            self.assertEqual(row["status"], "valid")

    def test_walkthrough_publish_is_one_idempotent_upsert(self) -> None:
        recipe = publish_walkthrough_recipe()
        self.assertIn("--jq '[.[] | select(.body | contains(\"<!-- wtk-deep-review:walkthrough -->\"))][0].id // empty'", recipe)
        self.assertIn('if [ -n "$CID" ]; then', recipe)
        self.assertNotIn("/comments/null", recipe)

        with tempfile.TemporaryDirectory() as raw:
            root = Path(raw)
            out = root / "out dir"
            out.mkdir()
            walkthrough = out / "walkthrough.md"
            walkthrough.write_text("walkthrough\n", encoding="utf-8")
            log = root / "gh.log"
            fake_gh = root / "gh"
            fake_gh.write_text(
                "#!/bin/sh\n"
                "printf 'CALL\\n' >> \"$GH_LOG\"\n"
                "for arg do printf '<%s>\\n' \"$arg\" >> \"$GH_LOG\"; done\n"
                "if [ \"$GH_MODE\" = existing ] && [ \"$2\" = \"repos/$R/issues/$N/comments\" ]; then\n"
                "  printf '42\\n'\n"
                "fi\n",
                encoding="utf-8",
            )
            fake_gh.chmod(0o700)

            def run_publish(mode: str) -> list[list[str]]:
                env = os.environ.copy()
                env.update(
                    {
                        "GH_LOG": str(log),
                        "GH_MODE": mode,
                        "PATH": f"{root}:{env['PATH']}",
                        "R": "owner/repo",
                        "N": "17",
                        "OUT": str(out),
                    }
                )
                log.write_text("", encoding="utf-8")
                result = subprocess.run(
                    ["sh", "-eu", "-c", recipe],
                    cwd=root,
                    env=env,
                    capture_output=True,
                    text=True,
                )
                self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
                calls: list[list[str]] = []
                current: list[str] = []
                for line in log.read_text(encoding="utf-8").splitlines():
                    if line == "CALL":
                        if current:
                            calls.append(current)
                        current = []
                    else:
                        current.append(line[1:-1])
                if current:
                    calls.append(current)
                return calls

            list_call = ["api", "repos/owner/repo/issues/17/comments", "--paginate", "--jq", "[.[] | select(.body | contains(\"<!-- wtk-deep-review:walkthrough -->\"))][0].id // empty"]
            body_arg = f"body=@{walkthrough}"
            self.assertEqual(
                run_publish("empty"),
                [list_call, ["api", "repos/owner/repo/issues/17/comments", "-F", body_arg]],
            )
            self.assertEqual(
                run_publish("existing"),
                [list_call, ["api", "repos/owner/repo/issues/comments/42", "-X", "PATCH", "-F", body_arg]],
            )

    def test_html_renderer_emits_real_findings_advisories_suppressions_and_coverage(self) -> None:
        # IT-024 (P1 AC8)
        with tempfile.TemporaryDirectory() as raw:
            root = init_repo(raw)
            out = render_fixture(root, [finding("major")])
            ledger = json.loads((out / "findings.json").read_text(encoding="utf-8"))
            ledger["advisories"] = [{
                **finding("minor"),
                "fingerprint": "fp-advisory",
                "result_kind": "advisory",
                "category": "refactor",
                "title": "Keep the review summary focused",
                "evidence": ["Premise: the summary mixes concerns → Improvement: clarify ownership → Fix: keep the lane summary focused."],
            }]
            ledger["suppressions"] = [{
                "source_job": "cohort-a", "file": "source.txt", "line": 1,
                "hunk": "new:1-1", "candidate": "format-only change",
                "reason": "formatting", "rule_ids": [], "note": "formatter-owned",
            }]
            ledger["coverage"] = {
                "hunks": [{"file": "source.txt", "hunk": "new:1-1", "checks": ["defect"], "outcome": "reported"}],
                "rules": [],
                "summary": {"selected_hunk_lines": 1, "lanes": {"defect": {"complete": True}}},
            }
            ledger["review_stats"] = {"candidates": 3, "reported": 2, "suppressed": 1, "coverage": ledger["coverage"]["summary"]}
            (out / "findings.json").write_text(json.dumps(ledger), encoding="utf-8")

            rendered = run_script(RENDER_REVIEW, root, "--out", str(out), "--no-freeze-check")
            self.assertEqual(rendered.returncode, 0, rendered.stdout + rendered.stderr)
            html = run_script(RENDER_HTML, root, "--out", str(out))
            self.assertEqual(html.returncode, 0, html.stdout + html.stderr)
            report = (out / "review.html").read_text(encoding="utf-8")
            self.assertNotIn("__DEEP_REVIEW_DATA__", report)
            data_match = re.search(r'<script id="dr-data" type="application/json">(.*?)</script>', report, re.S)
            self.assertIsNotNone(data_match)
            data = json.loads(data_match.group(1))
            self.assertEqual([row["title"] for row in data["findings"]], ["major finding", "Keep the review summary focused"])
            self.assertEqual(data["suppressions"][0]["reason"], "formatting")
            self.assertTrue(data["coverage"]["summary"]["lanes"]["defect"]["complete"])
            self.assertEqual(len(data["findings"][0]["repair_plan"]), 5)
            self.assertIn("Repair plan", report)

    def test_incremental_manifest_uses_effective_base_for_hunks_and_command(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            root = Path(raw)
            init_repo(raw)
            base = git(root, "rev-parse", "HEAD")
            (root / "source.txt").write_text("a\nb\n", encoding="utf-8")
            git(root, "add", "source.txt")
            git(root, "commit", "-qm", "first change")
            first = git(root, "rev-parse", "HEAD")
            out = root / ".wtk-deep-review" / "out"
            first_run = run_script(BUILD_MANIFEST, root, "--out", str(out), "--base", base, "--head", first)
            self.assertEqual(first_run.returncode, 0, first_run.stdout + first_run.stderr)
            (root / "source.txt").write_text("a\nb\nc\n", encoding="utf-8")
            git(root, "add", "source.txt")
            git(root, "commit", "-qm", "second change")
            second = git(root, "rev-parse", "HEAD")
            (out / "state.json").write_text(
                json.dumps({"rounds": [{"n": 1, "head": first}]}), encoding="utf-8"
            )

            second_run = run_script(BUILD_MANIFEST, root, "--out", str(out), "--base", base)
            self.assertEqual(second_run.returncode, 0, second_run.stdout + second_run.stderr)
            manifest = json.loads((out / "manifest.json").read_text(encoding="utf-8"))
            row = next(item for item in manifest["files"] if item["path"] == "source.txt")
            self.assertEqual(manifest["mode"], "incremental")
            self.assertEqual(manifest["effective_base"], first)
            self.assertEqual(row["hunks"], [{"start": 3, "lines": 1, "side": "new"}])
            self.assertEqual(manifest["diff_command"], f"git diff {first[:12]}..{second[:12]} -- <file>")

    def test_manifest_concurrency_uses_cli_config_default_and_rejects_invalid_values(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            root = Path(raw)
            init_repo(raw)
            out = root / ".wtk-deep-review" / "default"
            result = run_script(BUILD_MANIFEST, root, "--out", str(out), "--base", "HEAD", "--head", "HEAD")
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            self.assertEqual(json.loads((out / "manifest.json").read_text())["concurrency"], 3)

        with tempfile.TemporaryDirectory() as raw:
            root = Path(raw)
            init_repo(raw)
            (root / ".wtk-deep-review.yaml").write_text("concurrency: 5\n", encoding="utf-8")
            out = root / ".wtk-deep-review" / "config"
            result = run_script(BUILD_MANIFEST, root, "--out", str(out), "--base", "HEAD", "--head", "HEAD")
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            self.assertEqual(json.loads((out / "manifest.json").read_text())["concurrency"], 5)
            override = root / ".wtk-deep-review" / "override"
            result = run_script(BUILD_MANIFEST, root, "--out", str(override), "--base", "HEAD", "--head", "HEAD", "--concurrency", "2")
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            self.assertEqual(json.loads((override / "manifest.json").read_text())["concurrency"], 2)
            (root / ".wtk-deep-review.yaml").write_text("concurrency: 1\n", encoding="utf-8")
            one = root / ".wtk-deep-review" / "one"
            result = run_script(BUILD_MANIFEST, root, "--out", str(one), "--base", "HEAD", "--head", "HEAD")
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            self.assertEqual(json.loads((one / "manifest.json").read_text())["concurrency"], 1)
            six = root / ".wtk-deep-review" / "six"
            result = run_script(BUILD_MANIFEST, root, "--out", str(six), "--base", "HEAD", "--head", "HEAD", "--concurrency", "6")
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            self.assertEqual(json.loads((six / "manifest.json").read_text())["concurrency"], 6)

        for raw_value in ("true", "false", "0", "7", '"3"', "1.5"):
            with self.subTest(raw_value=raw_value), tempfile.TemporaryDirectory() as raw:
                root = Path(raw)
                init_repo(raw)
                (root / ".wtk-deep-review.yaml").write_text(f"concurrency: {raw_value}\n", encoding="utf-8")
                result = run_script(BUILD_MANIFEST, root, "--out", str(root / ".wtk-deep-review/out"), "--base", "HEAD", "--head", "HEAD")
                self.assertNotEqual(result.returncode, 0)

    def test_runner_rejects_removed_workers_option(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            root = Path(raw)
            init_repo(raw)
            out = write_job_round(root, payload=valid_payload())
            result = run_script(RUN_JOBS, root, "--out", str(out), "--workers", "2", "--validate-only")
            self.assertNotEqual(result.returncode, 0)

    def test_manifest_handles_untracked_regular_files_and_symlinks(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            root = Path(raw)
            init_repo(raw)
            (root / "regular.txt").write_text("one\ntwo\n", encoding="utf-8")
            os.symlink("regular.txt", root / "link.txt")
            result = run_script(
                BUILD_MANIFEST,
                root,
                "--out",
                str(root / ".wtk-deep-review" / "out"),
                "--base",
                "HEAD",
                "--worktree",
            )
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            manifest = json.loads(
                (root / ".wtk-deep-review/out/manifest.json").read_text(encoding="utf-8")
            )
            regular = next(item for item in manifest["files"] if item["path"] == "regular.txt")
            link = next(item for item in manifest["files"] if item["path"] == "link.txt")
            self.assertEqual((regular["adds"], regular["dels"]), (2, 0))
            self.assertEqual(regular["hunks"], [{"start": 1, "lines": 2, "side": "new"}])
            self.assertEqual((link["kind"], link["target"]), ("symlink", "regular.txt"))
            self.assertEqual(link["hunks"], [{"start": 1, "lines": 1, "side": "new"}])

    def test_critical_and_major_findings_cannot_render_ship(self) -> None:
        for severity in ("critical", "major"):
            with self.subTest(severity=severity), tempfile.TemporaryDirectory() as raw:
                root = Path(raw)
                init_repo(raw)
                out = render_fixture(root, [finding(severity)])
                result = run_script(RENDER_REVIEW, root, "--out", str(out), "--no-freeze-check")
                self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
                review = (out / "review.md").read_text(encoding="utf-8")
                self.assertIn("**Verdict: FIX_BEFORE_SHIP**", review)
                self.assertNotIn("**Verdict: SHIP**", review)

    def repaired_findings(self) -> list[dict]:
        return [
            {
                **finding(severity),
                "also_applies": [f"source.txt:{7 + index}", "other.py:3"],
                "evidence": [f"Premise: guard missing → Path: {severity} caller skips the guard → Verdict: blocked."],
                "suggestion": "add_guard()" if severity == "major" else "",
            }
            for index, severity in enumerate(("critical", "major", "minor"))
        ]

    def test_repair_plan_rendered_for_every_defect_severity(self) -> None:
        # IT-004 (P2 AC1)
        with tempfile.TemporaryDirectory() as raw:
            root = init_repo(raw)
            findings = self.repaired_findings()
            out = render_fixture(root, findings)
            result = run_script(RENDER_REVIEW, root, "--out", str(out))
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            review = (out / "review.md").read_text(encoding="utf-8")
            self.assertNotIn("Prompt for AI Agents", review)

            def repair_plan(item: dict) -> str:
                before = review.split(f"<!-- wtk-deep-review:fp:{item['fingerprint']} -->", 1)[0]
                finding_block = before.rsplit(f"**{item['title']}.**", 1)[1]
                self.assertIn("<summary>🛠️ Repair plan</summary>", finding_block)
                plan = finding_block.rsplit("<summary>🛠️ Repair plan</summary>", 1)[1]
                return plan.split("</details>", 1)[0]

            for item in findings:
                plan = repair_plan(item)
                root_cause = next(line for line in plan.splitlines() if line.startswith("1. Root cause:"))
                self.assertIn("guard missing", root_cause)
                self.assertIn(f"{item['severity']} caller skips the guard", root_cause)
                self.assertNotIn("Verdict", root_cause)
                for anchor in item["also_applies"]:
                    self.assertIn(anchor, plan)
                self.assertIn(f"{item['file']}:{item['line']}", plan)
                self.assertIn("grep", plan)
                self.assertIn("fails on the Premise", plan)
            self.assertIn("Suggested change: add_guard()", repair_plan(findings[1]))

    def test_ledger_open_entries_carry_certificate(self) -> None:
        # IT-005 (P2 AC2)
        with tempfile.TemporaryDirectory() as raw:
            root = init_repo(raw)
            findings = self.repaired_findings()
            out = render_fixture(root, findings)
            result = run_script(RENDER_REVIEW, root, "--out", str(out))
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            ledger = json.loads((out / "state.json").read_text(encoding="utf-8"))["ledger"]
            for item in findings:
                entry = ledger[item["fingerprint"]]
                self.assertEqual(entry["status"], "open")
                self.assertEqual(entry["certificate"], item["evidence"][0])
                self.assertEqual(entry["also_applies"], item["also_applies"])
                self.assertEqual(entry["line"], item["line"])

    def test_incremental_mode_emits_one_defect_job_without_polish_or_sweeps(self) -> None:
        # IT-006 (P2 AC3; edge: retained sweep is skipped)
        with tempfile.TemporaryDirectory() as raw:
            root = init_repo(raw)
            out, info = incremental_fixture(root, sweeps=["consistency"])
            jobs = json.loads((out / "jobs.json").read_text(encoding="utf-8"))["jobs"]
            self.assertEqual(len(jobs), 1, jobs)
            self.assertEqual(jobs[0]["lane"], "defect")
            self.assertEqual({row["file"] for row in jobs[0]["required_hunks"]}, {"source.txt"})
            self.assertEqual(jobs[0]["prior_fingerprints"], ["fp-major"])
            self.assertIn("sweeps skipped in incremental mode", info["stdout"])
            self.assertEqual(sorted(p.name for p in (out / "prompts").iterdir()), ["cohort-rc.md"])

    def test_remediation_prompt_lists_prior_findings(self) -> None:
        # IT-007 (P2 AC4)
        with tempfile.TemporaryDirectory() as raw:
            root = init_repo(raw)
            out, info = incremental_fixture(root, sweeps=[])
            job = json.loads((out / "jobs.json").read_text(encoding="utf-8"))["jobs"][0]
            prompt = (root / job["prompt"]).read_text(encoding="utf-8")
            self.assertIn("fp-major", prompt)
            self.assertIn("major", prompt)
            self.assertIn("source.txt:1", prompt)
            self.assertIn(info["major"]["evidence"][0], prompt)
            self.assertIn("source.txt:7", prompt)
            self.assertIn("prior_findings", prompt)
            self.assertIn("resolved", prompt)
            self.assertIn("evidence", prompt)
            self.assertNotIn("No prior findings to disposition", prompt)

    def test_resolved_disposition_without_new_defects_ships(self) -> None:
        # IT-010 (P2 independent test)
        with tempfile.TemporaryDirectory() as raw:
            root = init_repo(raw)
            out, info = incremental_fixture(root, sweeps=[])
            job = json.loads((out / "jobs.json").read_text(encoding="utf-8"))["jobs"][0]
            payload = {
                **valid_payload(),
                "coverage": {
                    "hunks": [{**row, "checks": ["defect"], "outcome": "clear"} for row in job["required_hunks"]],
                    "rules": [],
                },
                "prior_findings": [
                    {"fingerprint": "fp-major", "status": "resolved", "evidence": "source.txt:2 → guard present"}
                ],
            }
            (root / job["output"]).write_text(json.dumps(payload), encoding="utf-8")
            result, row = validate_status(root, out)
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            self.assertEqual(row["status"], "valid")
            merged = run_script(MERGE_FINDINGS, root, "--out", str(out))
            self.assertEqual(merged.returncode, 0, merged.stdout + merged.stderr)
            rendered = run_script(RENDER_REVIEW, root, "--out", str(out))
            self.assertEqual(rendered.returncode, 0, rendered.stdout + rendered.stderr)
            review = (out / "review.md").read_text(encoding="utf-8")
            self.assertIn("**Verdict: SHIP**", review)
            details = review.split("## Review details", 1)[1].split("## Findings", 1)[0]  # script-derived, never a walkthrough
            self.assertIn("(incremental, round 2)", details)
            self.assertIn("**Files**: 1 selected", details)
            self.assertIn("**Jobs**: 1 (1 cohort)", details)
            self.assertNotIn("## Walkthrough", review)
            state = json.loads((out / "state.json").read_text(encoding="utf-8"))
            self.assertEqual(state["ledger"]["fp-major"]["status"], "resolved")
            self.assertEqual(state["ledger"]["fp-major"]["resolved_in"], info["head"])
            self.assertEqual(state["rounds"][-1]["verdict"], "SHIP")

    def test_incremental_round_with_empty_selection_keeps_prior_findings_open(self) -> None:
        # IT-022 (edge: fix touched only ignored paths)
        with tempfile.TemporaryDirectory() as raw:
            root = init_repo(raw)
            base = git(root, "rev-parse", "HEAD")
            out = render_fixture(root, [finding("major")])
            first = run_script(RENDER_REVIEW, root, "--out", str(out))
            self.assertEqual(first.returncode, 0, first.stdout + first.stderr)
            before = json.loads((out / "state.json").read_text(encoding="utf-8"))["ledger"]
            self.assertEqual(before["fp-major"]["status"], "open")

            (root / "foo.lock").write_text("lockfile\n", encoding="utf-8")
            git(root, "add", "foo.lock")
            git(root, "commit", "-qm", "chore: bump lockfile")
            result = run_script(BUILD_MANIFEST, root, "--out", str(out), "--base", base)
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            self.assertIn("nothing selected", result.stdout)
            manifest = json.loads((out / "manifest.json").read_text(encoding="utf-8"))
            self.assertEqual(manifest["mode"], "incremental")
            self.assertEqual([f for f in manifest["files"] if f["disposition"] == "selected"], [])
            after = json.loads((out / "state.json").read_text(encoding="utf-8"))["ledger"]
            self.assertEqual(after, before)
            self.assertEqual(after["fp-major"]["status"], "open")

    def test_open_disposition_and_new_defect_in_same_file_both_appear(self) -> None:
        # IT-023 (edge: prior stays visible next to a distinct new defect in the same file; C8 rejects the same anchor)
        with tempfile.TemporaryDirectory() as raw:
            root = init_repo(raw)
            out, info = incremental_fixture(root, sweeps=[])
            job = json.loads((out / "jobs.json").read_text(encoding="utf-8"))["jobs"][0]
            new_defect = {
                "file": "source.txt", "line": 2, "end_line": None, "in_diff": True, "hunk": "new:2-2",
                "category": "potential-issue", "severity": "major", "quick_win": False, "rule_ids": [],
                "title": "Guard rejects the wrong account",
                "body": "The new guard compares the wrong identifier.",
                "evidence": ["Premise: guard compares ids → Path: caller passes the owner id → Verdict: blocked."],
            }
            payload = {
                **valid_payload(),
                "defects": [new_defect],
                "coverage": {
                    "hunks": [{**row, "checks": ["defect"], "outcome": "reported"} for row in job["required_hunks"]],
                    "rules": [],
                },
                "prior_findings": [
                    {"fingerprint": "fp-major", "status": "open", "evidence": "source.txt:1 → guard still skipped"}
                ],
            }
            (root / job["output"]).write_text(json.dumps(payload), encoding="utf-8")
            merged = run_script(MERGE_FINDINGS, root, "--out", str(out))
            self.assertEqual(merged.returncode, 0, merged.stdout + merged.stderr)
            ledger = json.loads((out / "findings.json").read_text(encoding="utf-8"))
            new = [f for f in ledger["findings"] if f["title"] == new_defect["title"]]
            self.assertEqual(len(new), 1)
            self.assertEqual(new[0]["round_status"], "new")
            self.assertNotEqual(new[0]["fingerprint"], "fp-major")
            self.assertIn("fp-major", ledger["reconciliation"]["still_open_unreviewed"])
            self.assertNotIn("fp-major", ledger["reconciliation"]["resolved"])

            rendered = run_script(RENDER_REVIEW, root, "--out", str(out))
            self.assertEqual(rendered.returncode, 0, rendered.stdout + rendered.stderr)
            review = (out / "review.md").read_text(encoding="utf-8")
            self.assertIn("**Verdict: FIX_BEFORE_SHIP**", review)
            self.assertIn(f"<!-- wtk-deep-review:fp:{new[0]['fingerprint']} -->", review)
            duplicates = review.split("## Duplicates", 1)[1].split("## Advisories", 1)[0]
            self.assertIn(info["major"]["title"], duplicates)
            state = json.loads((out / "state.json").read_text(encoding="utf-8"))["ledger"]
            self.assertEqual(state["fp-major"]["status"], "open")
            self.assertEqual(state[new[0]["fingerprint"]]["status"], "open")

    def test_defect_at_prior_anchor_is_rejected_as_re_report(self) -> None:
        # C8: a prior finding is dispositioned, never re-listed in defects
        with tempfile.TemporaryDirectory() as raw:
            root = init_repo(raw)
            out, _ = incremental_fixture(root, sweeps=[])
            job = json.loads((out / "jobs.json").read_text(encoding="utf-8"))["jobs"][0]
            self.assertEqual(job["prior_anchors"], [{"fingerprint": "fp-major", "file": "source.txt", "line": 1}])
            self.assertIn("Never list it, or a rewording of it, in `defects`", (root / job["prompt"]).read_text(encoding="utf-8"))

            def defect(line: int) -> dict:
                return {
                    "file": "source.txt", "line": line, "end_line": None, "in_diff": line == 2,
                    "hunk": "new:2-2" if line == 2 else None, "category": "potential-issue", "severity": "major",
                    "quick_win": False, "rule_ids": [], "title": f"Guard still skipped at {line}", "body": "Reworded prior.",
                    "evidence": ["Premise: guard missing → Path: the caller skips the guard → Verdict: blocked."],
                }

            def status_for(defects: list[dict]) -> dict:
                (root / job["output"]).write_text(json.dumps({
                    **valid_payload(), "defects": defects,
                    "coverage": {"hunks": [{**row, "checks": ["defect"], "outcome": "reported"} for row in job["required_hunks"]], "rules": []},
                    "prior_findings": [{"fingerprint": "fp-major", "status": "open", "evidence": "source.txt:1 → still skipped"}],
                }), encoding="utf-8")
                return validate_status(root, out)[1]

            row = status_for([defect(1)])
            self.assertEqual(row["status"], "invalid")
            self.assertIn("$.defects[0]: re-reports prior finding fp-major", row["reason"])
            self.assertEqual(status_for([])["status"], "valid")
            self.assertEqual(status_for([defect(2)])["status"], "valid")

    def test_incremental_mode_with_no_open_prior_findings_still_emits_one_job(self) -> None:
        # IT-019 (edge: empty prior set)
        with tempfile.TemporaryDirectory() as raw:
            root = init_repo(raw)
            out, _ = incremental_fixture(root, sweeps=[], prior_status="resolved")
            jobs = json.loads((out / "jobs.json").read_text(encoding="utf-8"))["jobs"]
            self.assertEqual(len(jobs), 1, jobs)
            self.assertEqual(jobs[0]["prior_fingerprints"], [])
            prompt = (root / jobs[0]["prompt"]).read_text(encoding="utf-8")
            self.assertIn("No prior findings to disposition", prompt)
            self.assertNotIn("fp-major", prompt)

    def test_review_rounds_guideline_states_remediation_check_rule(self) -> None:
        # IT-020 (P2 AC7–8)
        guideline = (Path(__file__).resolve().parents[1] / ".agents/skills/wtk/references/review-rounds.md").read_text(encoding="utf-8")
        self.assertIn("remediation check", guideline)
        self.assertIn("stall_attempts", guideline)
        for banned in ("round 3", "Blocker", "Cosmetic", "≤2 rounds"):
            self.assertNotIn(banned, guideline)

    def test_coverage_gate_requires_the_defect_lane_only(self) -> None:
        # IT-015 (P3 AC1): complete defect-lane coverage merges; a missing defect row is rejected
        files = [{"path": "source.txt", "disposition": "selected", "status": "M", "adds": 1, "dels": 0,
                  "hunks": [{"start": 1, "lines": 1, "side": "new"}]}]
        with self.assertRaisesRegex(RuntimeError, "defect coverage incomplete"):
            coverage_ledger({"files": files}, {"hunk_coverage": [], "rule_coverage": []})

        with tempfile.TemporaryDirectory() as raw:
            root = init_repo(raw)
            hunks = [{"file": "source.txt", "hunk": "new:1-1"}]
            payload = {**valid_payload(), "coverage": {
                "hunks": [{**row, "checks": ["defect"], "outcome": "clear"} for row in hunks], "rules": [],
            }}
            out = write_job_round(root, payload=payload, job={
                "label": "cohort-a", "kind": "cohort", "lane": "defect", "required_hunks": hunks,
            })
            manifest = json.loads((out / "manifest.json").read_text(encoding="utf-8"))
            (out / "manifest.json").write_text(json.dumps({**manifest, "files": files}), encoding="utf-8")
            merged = run_script(MERGE_FINDINGS, root, "--out", str(out))
            self.assertEqual(merged.returncode, 0, merged.stdout + merged.stderr)
            lanes = json.loads((out / "review-stats.json").read_text(encoding="utf-8"))["coverage"]["lanes"]
            self.assertTrue(lanes["defect"]["complete"])
            self.assertNotIn("polish", lanes)

    def test_small_selection_split_into_two_cohorts_is_rejected(self) -> None:
        # UT-006 (P3 AC6): ~400 changed lines per cohort, capped by reviewer concurrency
        selected = {
            f"file{i}.txt": {"adds": 10, "dels": 3 + i, "hunks": [{"start": 1, "lines": 10, "side": "new"}]}
            for i in range(3)
        }
        cohorts = [
            {"id": "A", "name": "first", "risk": "normal", "files": ["file0.txt", "file1.txt"]},
            {"id": "B", "name": "second", "risk": "normal", "files": ["file2.txt"]},
        ]
        errors = validate_cohorts(cohorts, selected, 100, 3)
        self.assertEqual(len(errors), 1, errors)
        self.assertIn("should use at most 1 cohorts", errors[0])
        self.assertEqual(validate_cohorts([{**cohorts[0], "files": list(selected)}], selected, 100, 3), [])

    def test_cohort_count_is_capped_by_concurrency_and_line_target(self) -> None:
        # UT-006 companion: 939 lines at concurrency 3 -> at most 3 cohorts
        adds = (235, 235, 235, 234)
        selected = {
            f"file{i}.txt": {"adds": n, "dels": 0, "hunks": [{"start": 1, "lines": n, "side": "new"}]}
            for i, n in enumerate(adds)
        }
        one_each = [{"id": f"C{i}", "name": f"c{i}", "risk": "normal", "files": [f"file{i}.txt"]} for i in range(4)]
        three = [{**one_each[0], "files": ["file0.txt", "file1.txt"]}, one_each[2], one_each[3]]
        self.assertEqual(validate_cohorts(three, selected, 100, 3), [])
        errors = validate_cohorts(one_each, selected, 100, 3)
        self.assertEqual(len(errors), 1, errors)
        self.assertIn("plan has 4 cohorts; 939 changed lines at concurrency 3 should use at most 3 cohorts", errors[0])

    def test_defect_job_output_with_an_advisory_validates(self) -> None:
        # IT-011 (P3 AC2)
        with tempfile.TemporaryDirectory() as raw:
            root = init_repo(raw)
            advisory = {
                "file": "source.txt", "line": 1, "end_line": None, "in_diff": False, "hunk": None,
                "category": "refactor", "severity": "minor", "quick_win": True, "rule_ids": [],
                "title": "Name the magic constant", "body": "The literal repeats three times.",
                "evidence": ["Premise: literal at source.txt:1 → Improvement: one named constant → Fix: extract it."],
            }
            out = write_job_round(root, payload={**valid_payload(), "advisories": [advisory]}, job={
                "label": "cohort-a", "kind": "cohort", "lane": "defect",
            })
            result, row = validate_status(root, out)
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            self.assertEqual(row["status"], "valid")

    def test_full_mode_emits_no_polish_jobs(self) -> None:
        # IT-021 (P3 AC1)
        with tempfile.TemporaryDirectory() as raw:
            root = init_repo(raw)
            out, build = full_fixture(root, {"cohorts": [
                {"id": "A", "name": "all", "risk": "normal", "files": ["file0.txt", "file1.txt", "file2.txt"]},
            ]})
            self.assertEqual(build.returncode, 0, build.stdout + build.stderr)
            jobs = json.loads((out / "jobs.json").read_text(encoding="utf-8"))["jobs"]
            self.assertEqual([job["lane"] for job in jobs], ["defect"])
            self.assertNotIn("polish", build.stdout)

    def test_removed_sweeps_are_rejected_by_name(self) -> None:
        # IT-012 (P3 AC3)
        for sweep, owner in (("tests", "test adequacy"), ("spec-parity", "spec parity")):
            with self.subTest(sweep=sweep), tempfile.TemporaryDirectory() as raw:
                root = init_repo(raw)
                _, build = full_fixture(root, {"sweeps": [sweep], "cohorts": [
                    {"id": "A", "name": "all", "risk": "normal", "files": ["file0.txt", "file1.txt", "file2.txt"]},
                ]})
                self.assertEqual(build.returncode, 1, build.stdout + build.stderr)
                self.assertIn(f"sweep '{sweep}' was removed: the Technical Verifier owns {owner}", build.stderr)

    def test_spec_contract_without_spec_parity_job_ships_with_no_conformance_section(self) -> None:
        # IT-013 (P3 AC4)
        with tempfile.TemporaryDirectory() as raw:
            root = init_repo(raw)
            out = render_fixture(root, [])
            (out / "context-pack.md").write_text(
                "# Context\n\n## Spec contract\n\n- `docs/spec.md` → the contract\n", encoding="utf-8"
            )
            (out / "jobs.json").write_text(json.dumps({"jobs": []}), encoding="utf-8")
            result = run_script(RENDER_REVIEW, root, "--out", str(out))
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            review = (out / "review.md").read_text(encoding="utf-8")
            self.assertIn("**Verdict: SHIP**", review)
            self.assertNotIn("## Spec conformance", review)
            self.assertNotIn("spec-parity", review)

    def one_cohort_per_file(self, files: int = 3) -> list[dict]:
        return [{"id": f"C{i}", "name": f"file {i}", "risk": "normal", "files": [f"file{i}.txt"]} for i in range(files)]

    def test_sweeps_require_three_or_more_cohorts(self) -> None:
        # Sweeps duplicate cohort findings on small diffs; three 300-line files make room for 3 cohorts at concurrency 3.
        with tempfile.TemporaryDirectory() as raw:
            root = init_repo(raw)
            cohorts = self.one_cohort_per_file()
            two = [{**cohorts[0], "files": ["file0.txt", "file1.txt"]}, cohorts[2]]
            _, build = full_fixture(root, {"sweeps": ["consistency"], "cohorts": two}, lines=300)
            self.assertEqual(build.returncode, 1, build.stdout + build.stderr)
            self.assertIn("sweeps need at least 3 cohorts (2 planned)", build.stderr)
            self.assertIn("remove sweeps from plan.json", build.stderr)
        with tempfile.TemporaryDirectory() as raw:
            root = init_repo(raw)
            out, build = full_fixture(root, {"sweeps": ["consistency"], "cohorts": self.one_cohort_per_file()}, lines=300)
            self.assertEqual(build.returncode, 0, build.stdout + build.stderr)
            jobs = json.loads((out / "jobs.json").read_text(encoding="utf-8"))["jobs"]
            self.assertEqual([job["kind"] for job in jobs], ["cohort", "cohort", "cohort", "sweep"])
            cohort_prompt = (out / "prompts/cohort-c0.md").read_text(encoding="utf-8")
            self.assertIn("concrete, actionable maintainability or project-rule improvements", cohort_prompt)

    def test_sweep_may_not_re_report_a_single_cohort_result(self) -> None:
        # C9: a sweep result inside cohort-owned hunks needs also_applies across two other files
        with tempfile.TemporaryDirectory() as raw:
            root = init_repo(raw)
            out, build = full_fixture(root, {"sweeps": ["consistency"], "cohorts": self.one_cohort_per_file()}, lines=300)
            self.assertEqual(build.returncode, 0, build.stdout + build.stderr)
            sweep = next(job for job in json.loads((out / "jobs.json").read_text(encoding="utf-8"))["jobs"] if job["kind"] == "sweep")
            self.assertEqual(sorted(row["file"] for row in sweep["cohort_hunks"]), ["file0.txt", "file1.txt", "file2.txt"])
            self.assertIn("rejected unless its `also_applies` names anchors in at least two other files",
                          (root / sweep["prompt"]).read_text(encoding="utf-8"))
            base = {
                "file": "file0.txt", "line": 1, "end_line": None, "category": "potential-issue", "severity": "major",
                "quick_win": False, "rule_ids": [], "title": "Rename missed a sibling", "body": "The sibling keeps the old name.",
                "evidence": ["Premise: file0.txt:1 renamed → Path: sibling still calls the old name → Verdict: blocked."],
            }
            inside = {**base, "in_diff": True, "hunk": "new:1-300"}

            def status_for(defect: dict) -> dict:
                (root / sweep["output"]).write_text(json.dumps({**valid_payload(), "defects": [defect]}), encoding="utf-8")
                result = run_script(RUN_JOBS, root, "--out", str(out), "--validate-only", "--only", sweep["label"])
                return json.loads((out / "runs/jobs-status.json").read_text(encoding="utf-8"))["jobs"][0]

            row = status_for(inside)
            self.assertEqual(row["status"], "invalid")
            self.assertIn("$.defects[0]: single-cohort result belongs to the cohort lane", row["reason"])
            self.assertEqual(status_for({**inside, "also_applies": ["file1.txt:1", "file2.txt:1"]})["status"], "valid")
            self.assertEqual(status_for({**base, "in_diff": False, "hunk": None})["status"], "valid")

    def test_prompt_and_schema_carry_no_reporting_only_obligations(self) -> None:
        # IT-014 (P3 AC5)
        with tempfile.TemporaryDirectory() as raw:
            root = init_repo(raw)
            out, build = full_fixture(root, {"sweeps": ["consistency"], "cohorts": self.one_cohort_per_file()}, lines=300)
            self.assertEqual(build.returncode, 0, build.stdout + build.stderr)
            prompts = sorted((out / "prompts").iterdir())
            self.assertEqual(len(prompts), 4)
            for prompt in prompts:
                text = prompt.read_text(encoding="utf-8")
                for banned in ("RULE COVERAGE", "PRODUCT CONTEXT", "RECORD every investigated"):
                    self.assertNotIn(banned, text, prompt.name)
                self.assertIn("HUNK COVERAGE", text)

            jobs = json.loads((out / "jobs.json").read_text(encoding="utf-8"))["jobs"]
            unruled = {
                "file": "file0.txt", "line": 1, "end_line": None, "in_diff": False, "hunk": None,
                "category": "potential-issue", "severity": "minor", "quick_win": False,
                "title": "Placeholder line ships", "body": "The file only says changed.",
                "rule_ids": [],
                "evidence": ["Premise: file0.txt:1 is a placeholder → Path: shipped as-is → Verdict: blocked."],
            }
            bare = {"defects": [unruled], "advisories": [], "suppressions": []}
            full = {
                "defects": [], "advisories": [],
                "suppressions": [{"file": "file0.txt", "line": 1, "hunk": "new:1-1", "candidate": "trailing newline",
                                  "reason": "formatting", "rule_ids": [], "note": "formatter-owned"}],
            }
            for variant, extra in (("bare", bare), ("full", full)):
                with self.subTest(variant=variant):
                    for job in jobs:
                        hunks = [{**row, "checks": ["read callers", "traced input"], "outcome": "clear"} for row in job["required_hunks"]]
                        coverage = {
                            "hunks": hunks,
                            "rules": [
                                {"rule_id": rule_id, "status": "not-applicable", "note": "no match"}
                                for rule_id in job["rule_ids"]
                            ],
                        }
                        (root / job["output"]).write_text(json.dumps({**extra, "coverage": coverage}), encoding="utf-8")
                    result = run_script(RUN_JOBS, root, "--out", str(out), "--validate-only")
                    self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
                    status = json.loads((out / "runs/jobs-status.json").read_text(encoding="utf-8"))
                    self.assertEqual({row["status"] for row in status["jobs"]}, {"valid"})
                    merged = run_script(MERGE_FINDINGS, root, "--out", str(out))
                    self.assertEqual(merged.returncode, 0, merged.stdout + merged.stderr)
                    if variant == "bare":
                        merged_rows = json.loads((out / "findings.json").read_text(encoding="utf-8"))["findings"]
                        self.assertEqual([row["rule_ids"] for row in merged_rows if row["title"] == unruled["title"]], [[]])

    def test_skill_candidacy_requires_explicit_dispatch(self) -> None:
        # UT-005 (P3 AC7; a skill whose own files are in the diff is a knowledge source)
        with tempfile.TemporaryDirectory() as raw:
            root = init_repo(raw)
            skills = (("alpha", "Alpha helper."), ("beta", "Review source.txt source files."), ("gamma", "Gamma helper."))
            for name, description in skills:
                skill = root / ".agents" / "skills" / name / "SKILL.md"
                skill.parent.mkdir(parents=True)
                skill.write_text(f"---\nname: {name}\ndescription: {description}\n---\n# {name}\n", encoding="utf-8")
            (root / "AGENTS.md").write_text("# Agents\n\nUse the alpha skill.\n", encoding="utf-8")
            git(root, "add", ".agents", "AGENTS.md")
            git(root, "commit", "-qm", "chore: skills")
            base = git(root, "rev-parse", "HEAD")
            script = root / ".agents" / "skills" / "gamma" / "scripts" / "x.py"
            script.parent.mkdir()
            script.write_text("print('x')\n", encoding="utf-8")
            (root / "source.txt").write_text("a\nb\n", encoding="utf-8")
            git(root, "add", ".agents", "source.txt")
            git(root, "commit", "-qm", "feat: change")
            out = root / ".wtk-deep-review" / "out"
            manifest = run_script(BUILD_MANIFEST, root, "--out", str(out), "--base", base)
            self.assertEqual(manifest.returncode, 0, manifest.stdout + manifest.stderr)
            result = run_script(BUILD_KNOWLEDGE, root, "--out", str(out))
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            sources = {s["path"]: s for s in json.loads((out / "knowledge.json").read_text(encoding="utf-8"))["sources"]}
            self.assertTrue(sources[".agents/skills/alpha/SKILL.md"]["candidate"])
            beta = sources[".agents/skills/beta/SKILL.md"]
            self.assertFalse(beta["candidate"])
            self.assertEqual(beta["candidate_reason"], "no explicit dispatch")
            gamma = sources[".agents/skills/gamma/SKILL.md"]
            self.assertTrue(gamma["candidate"])
            self.assertIn("skill directory contains", gamma["candidate_reason"])
            self.assertEqual(gamma["applies_to"], [".agents/skills/gamma/scripts/x.py"])

    def test_rules_reused_when_no_applied_source_changed(self) -> None:
        # IT-016 (P3 AC8)
        with tempfile.TemporaryDirectory() as raw:
            root = init_repo(raw)
            out, base = knowledge_round_one(root)
            prior_rules = (out / "rules.json").read_bytes()
            prior_knowledge = (out / "knowledge.json").read_bytes()
            (root / "source.txt").write_text("a\nb\nc\n", encoding="utf-8")
            git(root, "add", "source.txt")
            git(root, "commit", "-qm", "fix: guard")
            manifest = run_script(BUILD_MANIFEST, root, "--out", str(out), "--base", base)
            self.assertEqual(manifest.returncode, 0, manifest.stdout + manifest.stderr)
            self.assertEqual(json.loads((out / "manifest.json").read_text(encoding="utf-8"))["mode"], "incremental")
            result = run_script(BUILD_KNOWLEDGE, root, "--out", str(out))
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            self.assertIn("rules reused from round 1", result.stdout)
            self.assertEqual((out / "rules.json").read_bytes(), prior_rules)
            self.assertEqual((out / "knowledge.json").read_bytes(), prior_knowledge)
            self.assertFalse((out / "rules.template.json").exists())

    def test_rules_rebuilt_when_an_applied_source_changed(self) -> None:
        # IT-017 (P3 AC8 boundary)
        with tempfile.TemporaryDirectory() as raw:
            root = init_repo(raw)
            out, base = knowledge_round_one(root)
            (root / "AGENTS.md").write_text("# Agents\n\nUse the beta skill.\n", encoding="utf-8")
            git(root, "add", "AGENTS.md")
            git(root, "commit", "-qm", "docs: switch skill")
            manifest = run_script(BUILD_MANIFEST, root, "--out", str(out), "--base", base)
            self.assertEqual(manifest.returncode, 0, manifest.stdout + manifest.stderr)
            result = run_script(BUILD_KNOWLEDGE, root, "--out", str(out))
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            self.assertNotIn("rules reused", result.stdout)
            self.assertTrue((out / "rules.template.json").is_file())
            self.assertFalse((out / "rules.json").exists())

    def test_graft_runs_by_default_and_ignores_legacy_config(self) -> None:
        # IT-005 / IT-007: Graft is attempted for every selected review.
        plan = {"cohorts": [{"id": "A", "name": "all", "risk": "normal", "files": ["file0.txt", "file1.txt", "file2.txt"]}]}
        for opt_in in (False, True):
            with self.subTest(opt_in=opt_in), tempfile.TemporaryDirectory() as raw:
                root = init_repo(raw)
                sentinel = root / "graft-invoked"
                shim = "#!/bin/sh\n" f"touch '{sentinel}'\n" "exit 1\n"
                shim_dir = root / "shim"
                shim_dir.mkdir()
                for path in (shim_dir / "graft", root / "node_modules" / ".bin" / "graft"):
                    path.parent.mkdir(parents=True, exist_ok=True)
                    path.write_text(shim, encoding="utf-8")
                    path.chmod(0o700)
                package = root / "node_modules" / "@nanonets" / "graft" / "package.json"
                package.parent.mkdir(parents=True)
                package.write_text(json.dumps({"version": "0.10.1"}), encoding="utf-8")
                (root / ".gitignore").write_text("node_modules/\nshim/\ngraft-invoked\n", encoding="utf-8")
                if opt_in:
                    (root / ".wtk-deep-review.yaml").write_text("graft: true\n", encoding="utf-8")
                git(root, "add", "-A")
                git(root, "commit", "-qm", "chore: shim")
                env = {**os.environ, "PATH": f"{shim_dir}:{os.environ['PATH']}"}
                with unittest.mock.patch.dict(os.environ, env):
                    out, build = full_fixture(root, plan)
                self.assertEqual(build.returncode, 0, build.stdout + build.stderr)
                context = (out / "graft-context.md").read_text(encoding="utf-8")
                self.assertTrue(sentinel.exists())
                self.assertIn("status: fallback", context)
                self.assertIn("plain repository inspection", context)
                jobs = json.loads((out / "jobs.json").read_text(encoding="utf-8"))
                expected_hash = hashlib.sha256("file0.txt file1.txt file2.txt".encode("utf-8")).hexdigest()
                self.assertEqual(jobs["repository_intelligence"]["graft"]["question_hash"], expected_hash)

    def test_degraded_context_keeps_frozen_review_validation(self) -> None:
        # IT-017 / RIR-03.5: both degraded artifacts still flow through job validation and freeze checks.
        plan = {"cohorts": [{"id": "A", "name": "all", "risk": "normal", "files": ["file0.txt", "file1.txt", "file2.txt"]}]}
        with tempfile.TemporaryDirectory() as raw:
            root = init_repo(raw)
            node_bin = root / "node_modules" / ".bin" / "graft"
            node_bin.parent.mkdir(parents=True)
            node_bin.write_text("#!/bin/sh\nexit 1\n", encoding="utf-8")
            node_bin.chmod(0o700)
            package = root / "node_modules" / "@nanonets" / "graft" / "package.json"
            package.parent.mkdir(parents=True)
            package.write_text(json.dumps({"version": "0.10.1"}), encoding="utf-8")
            (root / ".gitignore").write_text("node_modules/\n", encoding="utf-8")
            git(root, "add", ".gitignore")
            git(root, "commit", "-qm", "chore: local graft shim")
            out, build = full_fixture(root, plan)
            self.assertEqual(build.returncode, 0, build.stdout + build.stderr)
            build = run_script(BUILD_JOBS, root, "--out", str(out), "--graphify-question", "shared boundary")
            self.assertEqual(build.returncode, 0, build.stdout + build.stderr)
            metadata = json.loads((out / "jobs.json").read_text(encoding="utf-8"))["repository_intelligence"]
            self.assertEqual(metadata["graft"]["status"], "fallback")
            self.assertEqual(metadata["graphify"]["status"], "degraded")
            self.assertIn("dual_use_reason", metadata)

            jobs = json.loads((out / "jobs.json").read_text(encoding="utf-8"))["jobs"]
            for job in jobs:
                (root / job["output"]).write_text(json.dumps({
                    **valid_payload(),
                    "coverage": {"hunks": [{**hunk, "checks": ["defect"], "outcome": "clear"} for hunk in job["required_hunks"]], "rules": []},
                }), encoding="utf-8")
            result = run_script(RUN_JOBS, root, "--out", str(out), "--validate-only")
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            (root / "file0.txt").write_text("drifted\n", encoding="utf-8")
            drifted = run_script(RUN_JOBS, root, "--out", str(out), "--validate-only")
            self.assertEqual(drifted.returncode, 3, drifted.stdout + drifted.stderr)

    def test_build_jobs_help_removes_graft_opt_in(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            root = init_repo(raw)
            result = run_script(BUILD_JOBS, root, "--help")
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            self.assertIn("always prepares Graft context", result.stdout)
            self.assertNotIn("graft: true", result.stdout)

    def test_validate_only_rejects_source_drift_before_accepting_valid_output(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            root = Path(raw)
            init_repo(raw)
            out = write_job_round(root, payload=valid_payload())
            (root / "source.txt").write_text("drifted\n", encoding="utf-8")
            result = run_script(RUN_JOBS, root, "--out", str(out), "--validate-only")
            self.assertEqual(result.returncode, 3, result.stdout + result.stderr)
            self.assertIn("source drifted", result.stderr)

    def test_render_requires_manifest_concurrency(self) -> None:
        # Review details read manifest keys build_manifest.py always emits; a missing key is an error, not a default
        with tempfile.TemporaryDirectory() as raw:
            root = init_repo(raw)
            out = render_fixture(root, [])
            manifest = json.loads((out / "manifest.json").read_text(encoding="utf-8"))
            del manifest["concurrency"]
            (out / "manifest.json").write_text(json.dumps(manifest), encoding="utf-8")
            result = run_script(RENDER_REVIEW, root, "--out", str(out), "--no-freeze-check")
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("concurrency", result.stderr)

    def test_render_rejects_source_drift(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            root = Path(raw)
            init_repo(raw)
            out = render_fixture(root, [])
            (root / "source.txt").write_text("drifted\n", encoding="utf-8")
            result = run_script(RENDER_REVIEW, root, "--out", str(out))
            self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
            self.assertIn("source drifted", result.stderr)

    def test_invalid_and_blocked_jobs_never_validate(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            root = Path(raw)
            init_repo(raw)
            out = write_job_round(root, payload={})
            invalid = run_script(RUN_JOBS, root, "--out", str(out), "--validate-only")
            self.assertEqual(invalid.returncode, 1, invalid.stdout + invalid.stderr)
            status = json.loads((out / "runs/jobs-status.json").read_text(encoding="utf-8"))
            self.assertEqual(status["jobs"][0]["status"], "invalid")

        with tempfile.TemporaryDirectory() as raw:
            root = Path(raw)
            init_repo(raw)
            out = write_job_round(root)
            blocker = out / "blocker.py"
            blocker.write_text("print('usageLimitExceeded')\n", encoding="utf-8")
            blocked = run_script(
                RUN_JOBS,
                root,
                "--out",
                str(out),
                "--command",
                f"{sys.executable} {blocker} {{prompt}} {{output}} {{label}}",
            )
            self.assertEqual(blocked.returncode, 2, blocked.stdout + blocked.stderr)
            self.assertEqual(
                json.loads((out / "run-blocker.json").read_text(encoding="utf-8"))["status"],
                "blocked",
            )
            validation = run_script(RUN_JOBS, root, "--out", str(out), "--validate-only")
            self.assertEqual(validation.returncode, 1, validation.stdout + validation.stderr)

    def test_provider_block_detected_from_error_events_not_tool_output(self) -> None:
        # Block patterns count in structured error events and raw non-JSON/stderr lines, never in tool output.
        def run_stub(body: str) -> tuple[subprocess.CompletedProcess[str], bool]:
            with tempfile.TemporaryDirectory() as raw:
                root = init_repo(raw)
                out = write_job_round(root)
                stub = out / "stub.py"
                stub.write_text("import json, sys\n" + body, encoding="utf-8")
                result = run_script(
                    RUN_JOBS, root, "--out", str(out), "--command",
                    f"{sys.executable} {stub} {{prompt}} {{output}} {{label}}",
                )
                return result, (out / "run-blocker.json").exists()

        tool_output = (
            f"open(sys.argv[2], 'w').write(json.dumps({valid_payload()!r}))\n"
            "print(json.dumps({'type': 'item.completed', 'item': {'type': 'command_execution',"
            " 'aggregated_output': 'grep hit: usageLimitExceeded'}}))\n"
        )
        result, blocker = run_stub(tool_output)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("PASS sweep-tests", result.stdout)
        self.assertFalse(blocker)

        # Same tool output, no artifact: a plain failure, never a provider block (no valid output to mask detection)
        result, blocker = run_stub(tool_output.split("\n", 1)[1])
        self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
        self.assertIn("FAIL sweep-tests", result.stdout)
        self.assertNotIn("BLOCKED", result.stdout)
        self.assertFalse(blocker)

        result, blocker = run_stub("print(json.dumps({'type': 'error', 'message': 'usageLimitExceeded'}))\n")
        self.assertEqual(result.returncode, 2, result.stdout + result.stderr)
        self.assertIn("BLOCKED sweep-tests", result.stdout)
        self.assertTrue(blocker)

        result, _ = run_stub("print('usageLimitExceeded', file=sys.stderr)\n")
        self.assertEqual(result.returncode, 2, result.stdout + result.stderr)
        self.assertIn("BLOCKED sweep-tests", result.stdout)

    def test_invalid_artifact_is_repaired_not_re_reviewed(self) -> None:
        # C6: an invalid artifact is kept and the next attempt runs a repair prompt naming the errors.
        invalid = {"defects": [], "advisories": [],
                   "coverage": {"hunks": [{"file": "source.txt", "hunk": "new:1-1", "checks": ["defect"]}]}}
        with tempfile.TemporaryDirectory() as raw:
            root = init_repo(raw)
            out = write_job_round(root)
            log, stub = out / "prompts.log", out / "stub.py"
            stub.write_text(
                "import json, sys\n"
                f"open({str(log)!r}, 'a').write(sys.argv[1] + '\\n')\n"
                f"payload = {valid_payload()!r} if 'repair-' in sys.argv[1] else {invalid!r}\n"
                "open(sys.argv[2], 'w').write(json.dumps(payload))\n",
                encoding="utf-8",
            )
            result = run_script(
                RUN_JOBS, root, "--out", str(out), "--command",
                f"{sys.executable} {stub} {{prompt}} {{output}} {{label}}",
            )
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            self.assertIn("REPAIR sweep-tests attempt=2", result.stdout)
            self.assertIn("PASS sweep-tests attempt=2", result.stdout)
            prompts = log.read_text(encoding="utf-8").splitlines()
            self.assertEqual(len(prompts), 2)
            self.assertIn("repair-2", prompts[1])
            kept = out / "agents" / "job.json.attempt-1-invalid.json"
            self.assertEqual(json.loads(kept.read_text(encoding="utf-8")), invalid)
            repair = (root / prompts[1]).read_text(encoding="utf-8")
            self.assertIn("missing required key 'outcome'", repair)
            self.assertIn(str(kept.relative_to(root)), repair)
            self.assertIn("Do not re-review", repair)


if __name__ == "__main__":
    unittest.main()
