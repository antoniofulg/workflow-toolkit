"""Contract checks for modular entry points and Lean build boundaries."""

from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]


def read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


class WtkContractTests(unittest.TestCase):
    def test_modular_entries_keep_upstream_artifacts(self) -> None:
        discover = read(".agents/skills/wtk-discover/SKILL.md")
        plan = read(".agents/skills/wtk-plan/SKILL.md")
        implement = read(".agents/skills/wtk-implement/SKILL.md")
        self.assertIn(".design/<name>.md", discover)
        self.assertIn("organised by **vertical slice**", discover)
        self.assertIn(".tasks/<name>.md", plan)
        self.assertIn(".checks/<feature>.md", implement)
        self.assertNotIn(".specs/features/<feature>/plan.md", plan)
        self.assertNotIn(".specs/features/<feature>/plan.md", implement)

    def test_build_and_verify_boundaries(self) -> None:
        lean = read(".agents/skills/wtk-lean/SKILL.md")
        implement = read(".agents/skills/wtk-implement/SKILL.md")
        self.assertIn("whole slices", lean)
        self.assertIn("fresh Verifier over `<feature base>..HEAD` with every check", lean)
        self.assertIn("same turn after the feature's last commit", lean)
        self.assertIn("When it exceeds the budget", lean)
        self.assertIn("A build agent never spawns another agent at all", implement)
        self.assertIn("coherent pieces", implement)

    def test_generated_packets_preserve_integrated_lean_roles(self) -> None:
        for provider, extension in (("claude", "md"), ("codex", "toml"), ("cursor", "md")):
            implementer = read(f".agents/skills/wtk-config/assets/agents/{provider}/implementer.{extension}")
            verifier = read(f".agents/skills/wtk-config/assets/agents/{provider}/verifier.{extension}")
            self.assertIn("wtk-lean", implementer)
            self.assertIn("checks.md", implementer)
            self.assertTrue("Select `wtk-lean`" in implementer or "Select wtk-lean" in implementer)
            self.assertIn("wtk-implement", implementer)
            self.assertIn("plan.md", verifier)
            self.assertIn("checks.md", verifier)
            self.assertIn("verification.md", verifier)


if __name__ == "__main__":
    unittest.main()
