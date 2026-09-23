"""Contract checks for the on-demand Workflow Toolkit router."""

from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]
ROUTER = (ROOT / ".agents/skills/wtk/SKILL.md").read_text(encoding="utf-8")


class WtkForwardTests(unittest.TestCase):
    def test_defined_on_demand(self) -> None:
        self.assertIn("A decided feature without Lean artifacts", ROUTER)
        self.assertIn("read and invoke `wtk-lean`", ROUTER)
        self.assertIn("Do not preload quality, UI, security,", ROUTER)

    def test_discovery_boundary(self) -> None:
        self.assertIn("open product decision, or competing solution alternatives", ROUTER)
        self.assertIn("wtk-discover", ROUTER)
        self.assertIn("A diagnosis with no unresolved product or architecture choice", ROUTER)
        self.assertIn("route to discovery merely because the cause is unknown", ROUTER)

    def test_conditional_integrations(self) -> None:
        self.assertIn("load them only when the selected route or changed surface", ROUTER)
        self.assertIn("wtk-deep-review", ROUTER)
        self.assertIn("wtk-qa", ROUTER)
        self.assertIn("wtk-config", ROUTER)
        self.assertIn("wtk-ship", ROUTER)
        self.assertIn("authentication, or authorization", ROUTER)
        self.assertIn("references/security.md", ROUTER)
        self.assertIn("## 2. At\nSpecify — declare the surfaces", ROUTER)
        self.assertIn("## 3. At the test contract — abuse cases get IDs", ROUTER)
        self.assertIn("Before Design or Build", ROUTER)
        self.assertIn("references/ui-ux.md", ROUTER)
        adopted = (ROOT / "README.md").read_text(encoding="utf-8")
        self.assertIn("installed `wtk` skill", adopted)
        self.assertIn("references/security.md", ROUTER)
        self.assertIn("references/ui-ux.md", ROUTER)


if __name__ == "__main__":
    unittest.main()
