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

    def test_native_route_has_no_model_or_effort_ownership(self) -> None:
        route = read(".agents/skills/wtk-lean/scripts/workflow_route.py")
        self.assertIn("native_provider", route)
        self.assertIn("workflow.json", route)
        self.assertNotIn(".wtk.toml", route)
        self.assertNotIn('"model"', route)
        self.assertNotIn('"effort"', route)


if __name__ == "__main__":
    unittest.main()
