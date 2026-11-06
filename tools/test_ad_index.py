"""Self-check for the bundled AD index. Run: python3 tools/test_ad_index.py"""

from __future__ import annotations

import importlib.util
import subprocess
import tempfile
import unittest
from pathlib import Path

MODULE_PATH = Path(__file__).resolve().parent.parent / ".agents/skills/wtk-lean/scripts/ad-index.py"


def load():
    spec = importlib.util.spec_from_file_location("ad_index", MODULE_PATH)
    assert spec and spec.loader
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


ad_index = load()

SAMPLE = """# Project state

## Decisions

| ID | Decision | Rationale | Status | Date |
| --- | --- | --- | --- | --- |
| AD-002 | Second decision uses a \\| pipe. | escaped cells stay intact | active | 2026-03-02 |
| AD-001 | First decision is short. The rest is dropped. | only the first sentence is indexed | superseded by AD-002 | 2026-02-14 |

## Handoff

| ID | Decision | Status |
| --- | --- | --- |
| note | not a decision row | active |
"""


class AdIndexTests(unittest.TestCase):
    def test_parse_and_render(self) -> None:
        rows = ad_index.parse(SAMPLE)
        self.assertEqual(
            [(ident, status, decision) for _n, ident, decision, status in rows],
            [
                ("AD-001", "superseded by AD-002", "First decision is short."),
                ("AD-002", "active", "Second decision uses a | pipe."),
            ],
        )
        text = ad_index.render(rows)
        self.assertIn("| `AD-001` | superseded by AD-002 | First decision is short. |", text)
        self.assertIn("| `AD-002` | active | Second decision uses a \\| pipe. |", text)
        self.assertNotIn("The rest is dropped", text)

    def test_check_stale_then_fresh(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            root = Path(raw)
            specs = root / ".specs"
            specs.mkdir()
            (specs / "STATE.md").write_text(SAMPLE, encoding="utf-8")
            dest = root / ".agents/skills/wtk-lean/scripts/ad-index.py"
            dest.parent.mkdir(parents=True, exist_ok=True)
            dest.write_text(MODULE_PATH.read_text(encoding="utf-8"), encoding="utf-8")
            cmd = ["python3", str(dest), "--check"]
            stale = subprocess.run(cmd, cwd=root, capture_output=True, text=True)
            self.assertEqual(stale.returncode, 1, stale.stderr)
            write = subprocess.run(["python3", str(dest)], cwd=root, capture_output=True, text=True)
            self.assertEqual(write.returncode, 0, write.stderr)
            ok = subprocess.run(cmd, cwd=root, capture_output=True, text=True)
            self.assertEqual(ok.returncode, 0, ok.stderr)
            self.assertIn("AD-001", (specs / "AD-INDEX.md").read_text(encoding="utf-8"))

    def test_root_flag_targets_another_project(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            root = Path(raw)
            (root / ".specs").mkdir()
            (root / ".specs/STATE.md").write_text(SAMPLE, encoding="utf-8")
            cmd = ["python3", str(MODULE_PATH), "--root", str(root)]
            write = subprocess.run(cmd, capture_output=True, text=True)
            self.assertEqual(write.returncode, 0, write.stderr)
            self.assertIn("| `AD-002` | active |", (root / ".specs/AD-INDEX.md").read_text(encoding="utf-8"))
            ok = subprocess.run([*cmd, "--check"], capture_output=True, text=True)
            self.assertEqual(ok.returncode, 0, ok.stderr)


if __name__ == "__main__":
    unittest.main()
