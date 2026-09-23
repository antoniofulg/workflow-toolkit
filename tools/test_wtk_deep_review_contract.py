"""Contract checks for the namespaced Deep Review boundary."""

from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]


class WtkDeepReviewContractTests(unittest.TestCase):
    def test_namespaced_review_boundary(self) -> None:
        skill = (ROOT / ".agents/skills/wtk-deep-review/SKILL.md").read_text(encoding="utf-8")
        config = (ROOT / ".agents/skills/wtk-config/SKILL.md").read_text(encoding="utf-8")
        reviews = (ROOT / ".agents/skills/wtk/references/review-rounds.md").read_text(encoding="utf-8")
        self.assertIn("name: wtk-deep-review", skill)
        self.assertIn("deep-reviewer", skill)
        self.assertIn("cadence defaults to `skip`", config)
        self.assertIn("technical Verifier", reviews)
        self.assertIn("distinct", reviews)
        self.assertIn("wtk-deep-review", reviews)


if __name__ == "__main__":
    unittest.main()
