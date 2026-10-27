"""Contract checks for safe transient feature cleanup."""

from pathlib import Path
import shutil
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]


def make_feature(root: Path, name: str = "fixture") -> Path:
    validator = root / ".agents" / "skills" / "wtk-lean" / "scripts" / "validate_verification.py"
    validator.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(ROOT / ".agents/skills/wtk-lean/scripts/validate_verification.py", validator)
    shutil.copy2(ROOT / ".agents/skills/wtk-lean/scripts/native_evidence.py", validator.parent / "native_evidence.py")
    target = root / ".specs" / "features" / name
    target.mkdir(parents=True)
    fixtures = ROOT / ".agents" / "skills" / "wtk-lean" / "scripts" / "fixtures"
    for filename in ("plan.md", "checks.md", "verification.md"):
        shutil.copy2(fixtures / filename, target / filename)
    return target


def tree_state(root: Path) -> dict[Path, tuple[str, bytes | str | None]]:
    if root.is_symlink():
        return {Path("."): ("symlink", str(root.readlink()))}
    if root.is_file():
        return {Path("."): ("file", root.read_bytes())}
    state: dict[Path, tuple[str, bytes | str | None]] = {}
    for path in sorted(root.rglob("*")):
        relative = path.relative_to(root)
        if path.is_symlink():
            state[relative] = ("symlink", str(path.readlink()))
        elif path.is_file():
            state[relative] = ("file", path.read_bytes())
        elif path.is_dir():
            state[relative] = ("directory", None)
    return state


def load_module():
    import importlib.util

    path = ROOT / ".agents/skills/wtk-ship/scripts/close_feature.py"
    spec = importlib.util.spec_from_file_location("close_feature", path)
    module = importlib.util.module_from_spec(spec)
    assert spec and spec.loader
    spec.loader.exec_module(module)
    return module


class WtkLifecycleTests(unittest.TestCase):
    def test_cleanup_waits_for_required_promotions(self) -> None:
        module = load_module()
        root = Path(tempfile.mkdtemp())
        outside = Path(tempfile.mkdtemp())
        try:
            target = make_feature(root)
            (target / "target-sentinel").write_bytes(b"target sentinel")
            (outside / "outside-sentinel").write_bytes(b"outside sentinel")
            before_target = tree_state(target)
            before_outside = tree_state(outside)
            with self.assertRaisesRegex(ValueError, "promotion receipt is required"):
                module.close_feature(root, "fixture")
            self.assertEqual(tree_state(target), before_target)
            self.assertEqual(tree_state(outside), before_outside)
        finally:
            shutil.rmtree(root)
            shutil.rmtree(outside)

    def test_verified_feature_is_deleted(self) -> None:
        module = load_module()
        root = Path(tempfile.mkdtemp())
        try:
            target = make_feature(root)
            module.close_feature(root, "fixture", promoted=True)
            self.assertFalse(target.exists())
            self.assertTrue(not (root / ".specs" / "features").exists() or (root / ".specs" / "features").is_dir())
        finally:
            shutil.rmtree(root)

    def test_cleanup_refuses_unsafe_states(self) -> None:
        module = load_module()
        cases = (
            (
                "missing verification",
                lambda target, outside: (target / "verification.md").unlink(),
                "verification.md is required",
                "fixture",
            ),
            (
                "failed verification",
                lambda target, outside: (target / "verification.md").write_text(
                    (target / "verification.md").read_text(encoding="utf-8").replace(
                        "**Verdict**: PASS", "**Verdict**: FAIL", 1
                    ),
                    encoding="utf-8",
                ),
                "verdict is FAIL",
                "fixture",
            ),
            (
                "profile mismatch",
                lambda target, outside: (target / "verification.md").write_text(
                    (target / "verification.md").read_text(encoding="utf-8").replace(
                        "**Profile**: standard", "**Profile**: light", 1
                    ),
                    encoding="utf-8",
                ),
                "checks.md was approved under",
                "fixture",
            ),
            (
                "pending checks",
                lambda target, outside: (target / "checks.md").unlink(),
                "checks.md is required",
                "fixture",
            ),
            (
                "symlink target",
                lambda target, outside: (
                    shutil.rmtree(target),
                    target.symlink_to(outside, target_is_directory=True),
                ),
                "must not be a symlink",
                "fixture",
            ),
            (
                "path escape",
                lambda target, outside: None,
                "feature must be a lowercase slug",
                "../outside",
            ),
        )
        for name, mutate, message, feature in cases:
            with self.subTest(name=name):
                root = Path(tempfile.mkdtemp())
                outside = Path(tempfile.mkdtemp())
                try:
                    target = make_feature(root)
                    (target / "target-sentinel").write_bytes(b"target sentinel")
                    (outside / "outside-sentinel").write_bytes(b"outside sentinel")
                    mutate(target, outside)
                    before_target = tree_state(target)
                    before_outside = tree_state(outside)
                    with self.assertRaisesRegex(ValueError, message):
                        module.close_feature(root, feature, promoted=True)
                    self.assertEqual(tree_state(target), before_target)
                    self.assertEqual(tree_state(outside), before_outside)
                finally:
                    shutil.rmtree(root)
                    shutil.rmtree(outside)

    def test_cleanup_validates_the_intended_feature_directory(self) -> None:
        module = load_module()
        root = Path(tempfile.mkdtemp())
        try:
            target = make_feature(root)
            (target / "target-sentinel").write_bytes(b"target sentinel")
            (target / "verification.md").write_text(
                "# Verification\n\nVerdict: FAIL\nProfile: standard\nRound: initial\n\nEvidence: checks.md:1\n",
                encoding="utf-8",
            )
            decoy = root / "fixture"
            decoy.mkdir()
            fixtures = ROOT / ".agents" / "skills" / "wtk-lean" / "scripts" / "fixtures"
            for filename in ("checks.md", "verification.md"):
                shutil.copy2(fixtures / filename, decoy / filename)
            (decoy / "decoy-sentinel").write_bytes(b"decoy sentinel")
            before_target = tree_state(target)
            before_decoy = tree_state(decoy)
            with self.assertRaisesRegex(ValueError, "verdict is FAIL"):
                module.close_feature(root, "fixture", promoted=True)
            self.assertEqual(tree_state(target), before_target)
            self.assertEqual(tree_state(decoy), before_decoy)
        finally:
            shutil.rmtree(root)

    def test_unrequested_legacy_feature_is_untouched(self) -> None:
        module = load_module()
        root = Path(tempfile.mkdtemp())
        try:
            legacy = make_feature(root, "legacy-pending")
            before = {path.relative_to(legacy): path.read_bytes() for path in legacy.rglob("*") if path.is_file()}
            make_feature(root, "fixture")
            module.close_feature(root, "fixture", promoted=True)
            after = {path.relative_to(legacy): path.read_bytes() for path in legacy.rglob("*") if path.is_file()}
            self.assertEqual(after, before)
        finally:
            shutil.rmtree(root)


if __name__ == "__main__":
    unittest.main()
