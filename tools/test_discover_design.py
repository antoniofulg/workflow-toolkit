"""Regression tests for the pinned design validator and the discover design template."""

from __future__ import annotations

import hashlib
import re
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DISCOVER = ROOT / ".agents/skills/wtk-discover"
SCRIPT = DISCOVER / "scripts/validate_design.py"
FIXTURE = (DISCOVER / "scripts/fixtures/design.md").read_text(encoding="utf-8")
UPSTREAM_SHA256 = "d81f94e75eaa38aace818a4611e6cf42698c6a2e30869cb0ea2088028882cdbe"

SECTIONS = {
    "Summary": "summary",
    "Context and problem": "context and problem",
    "How we will know it worked": "how we will know it worked",
    "Scope": "scope",
    "How it works": "how it works",
    "Key decisions": "key decisions",
    "Slices": "slices",
}


def run(text: str) -> subprocess.CompletedProcess:
    """Run the validator on `text` written to a temp file."""
    with tempfile.TemporaryDirectory() as tmp:
        path = Path(tmp) / "design.md"
        path.write_text(text, encoding="utf-8")
        return subprocess.run([sys.executable, str(SCRIPT), str(path)], capture_output=True, text=True)


def rep(text: str, old: str, new: str) -> str:
    """Replace the one occurrence of `old`; a mutation that does not apply fails the test."""
    assert text.count(old) == 1, f"mutation anchor must occur once: {old!r}"
    return text.replace(old, new)


def errors(result: subprocess.CompletedProcess) -> list[str]:
    return [line for line in result.stdout.splitlines() if line.startswith("ERROR")]


def warnings(result: subprocess.CompletedProcess) -> list[str]:
    return [line for line in result.stdout.splitlines() if line.startswith("WARN")]


def padding(count: int) -> str:
    """`count` words in short sentences, so no long-sentence warning joins the budget ones."""
    return " ".join(["Alpha beta gamma delta epsilon."] * (count // 5)) + "\n"


def add_slices(text: str, names: list[str]) -> str:
    """Append rfc slices, each with an index row, an Order entry and a section."""
    text = rep(text, "| [Receipt](#receipt) | a receipt is sent after confirmation | blocked by the sender address |\n",
               "| [Receipt](#receipt) | a receipt is sent after confirmation | blocked by the sender address |\n"
               + "".join(f"| [{n}](#{n.lower()}) | {n} is delivered | rfc |\n" for n in names))
    text = rep(text, "Invoice → Payment → Receipt.", "Invoice → Payment → Receipt → " + " → ".join(names) + ".")
    sections = "".join(
        f"\n---\n\n### {n}\n\n> **Delivers:** {n} is delivered.\n> **Status:** rfc · **Depends on:** nothing\n\n"
        f"**Behaviour**\n\n| Situation | What happens |\n|---|---|\n| {n} happens | {n} is stored |\n"
        for n in names)
    return rep(text, "\n## References\n", sections + "\n## References\n")


def reported(result: subprocess.CompletedProcess, label: str) -> int:
    match = re.search(rf"words: (\d+) {label}", result.stdout)
    assert match, result.stdout
    return int(match.group(1))


class ValidatorTest(unittest.TestCase):
    def assert_error(self, result: subprocess.CompletedProcess, fragment: str) -> None:
        self.assertEqual(result.returncode, 1, result.stdout)
        self.assertTrue(any(fragment.lower() in line.lower() for line in errors(result)),
                        f"no ERROR line with {fragment!r}:\n{result.stdout}")

    def assert_clean(self, result: subprocess.CompletedProcess) -> None:
        self.assertEqual(result.returncode, 0, result.stdout)
        self.assertEqual(errors(result), [], result.stdout)

    def test_fixture_design_passes(self) -> None:
        self.assert_clean(run(FIXTURE))

    def test_missing_required_section_is_rejected(self) -> None:
        for heading, name in SECTIONS.items():
            with self.subTest(section=heading):
                self.assert_error(run(rep(FIXTURE, f"\n## {heading}\n", "\n")), f"required section missing: {name}")

    def test_slice_index_must_match_sections(self) -> None:
        invoice = "| [Invoice](#invoice) | an invoice carries its number and a paid marker | clear |\n"
        payment = "| [Payment](#payment) | a customer pays an invoice online | clear — go-live waits on the provider contract |\n"
        for label, text in (
            ("rows in another order", rep(FIXTURE, invoice + payment, payment + invoice)),
            ("index row for a slice with no section", rep(FIXTURE, invoice, invoice + "| [Refund](#refund) | money back | rfc |\n")),
            ("section with no index row", rep(FIXTURE, invoice, "")),
        ):
            with self.subTest(case=label):
                self.assert_error(run(text), "slice index and slice sections differ")

    def test_order_must_respect_dependencies(self) -> None:
        # Payment depends on Invoice and Receipt depends on Payment
        self.assert_clean(run(FIXTURE))
        self.assert_error(run(rep(FIXTURE, "Invoice → Payment → Receipt.", "Payment → Invoice → Receipt.")),
                          "order does not hold: 'Payment' depends on 'Invoice'")
        self.assert_error(run(rep(FIXTURE, "Invoice → Payment → Receipt.", "Invoice → Receipt → Payment.")),
                          "order does not hold: 'Receipt' depends on 'Payment'")
        # the same order is fine once the dependency is gone, so the error comes from the dependency
        freed = rep(FIXTURE, "**Depends on:** Payment", "**Depends on:** nothing")
        self.assert_clean(run(rep(freed, "Invoice → Payment → Receipt.", "Invoice → Receipt → Payment.")))

    def test_blocked_slice_cannot_be_clear(self) -> None:
        # a row that blocks the spec of a clear slice
        blocks_invoice = rep(FIXTURE, "| rfc - not decided | the spec of Receipt |", "| rfc - not decided | the spec of Invoice |")
        self.assert_error(run(blocks_invoice), "Open says something blocks 'Invoice', but the slice status is 'clear'")
        # the slice the row names is marked blocked by it: the fixture itself
        self.assert_clean(run(FIXTURE))
        # a clear slice named only in a go-live segment is not reported, alone or in a mixed cell
        golive = rep(FIXTURE, "| go-live of Payment |", "| go-live of Invoice and Payment |")
        self.assert_clean(run(golive))
        mixed = rep(FIXTURE, "| the spec of Receipt |", "| the spec of Receipt; go-live of Invoice |")
        self.assert_clean(run(mixed))
        # in a mixed cell the segment that blocks the spec still counts
        mixed_blocking = rep(FIXTURE, "| go-live of Payment |", "| the spec of Payment; go-live of Invoice |")
        self.assert_error(run(mixed_blocking), "Open says something blocks 'Payment'")

    def test_decision_index_and_sections_agree(self) -> None:
        no_section = rep(FIXTURE, "### D2 — Confirmed payment\n", "")
        self.assert_error(run(no_section), "decision D2 is in the index table and has no section")
        no_row = rep(FIXTURE, "| D2 | Confirmed payment | Payment, Receipt |\n", "")
        self.assert_error(run(no_row), "decision D2 has a section and is missing from the index table")

    def test_word_budget_warns_and_ignores_code_blocks(self) -> None:
        base = run(FIXTURE)
        reading, total = reported(base, "from Summary to Slices"), reported(base, "in all")
        summary_end = "\n## Context and problem\n"
        # 2,100 words between Summary and Slices
        over = run(rep(FIXTURE, summary_end, "\n" + padding(2100) + summary_end))
        self.assertEqual(over.returncode, 0, over.stdout)
        self.assertTrue(any(f"the part read together is {reading + 2100} words, over the 2000 budget" in w
                            for w in warnings(over)), over.stdout)
        # 4,100 words after Slices: only the whole-document budget is crossed
        whole = run(rep(FIXTURE, "\n## References\n", "\n## References\n\n" + padding(4100)))
        self.assertEqual(whole.returncode, 0, whole.stdout)
        self.assertTrue(any(f"whole document is {total + 4100} words, over the 4000 budget" in w
                            for w in warnings(whole)), whole.stdout)
        self.assertFalse(any("part read together" in w for w in warnings(whole)), whole.stdout)
        # the same words inside a fenced block raise neither warning
        fenced = run(rep(FIXTURE, summary_end, "\n```text\n" + padding(2100) + "```\n" + summary_end))
        self.assertEqual((fenced.returncode, warnings(fenced)), (0, []), fenced.stdout)
        fenced_whole = run(rep(FIXTURE, "\n## References\n", "\n## References\n\n```text\n" + padding(4100) + "```\n"))
        self.assertEqual((fenced_whole.returncode, warnings(fenced_whole)), (0, []), fenced_whole.stdout)
        # words in a table row count
        row = "| " + " ".join(["alpha"] * 2100) + " | table |\n"
        table = run(rep(FIXTURE, summary_end, "\n| A | B |\n|---|---|\n" + row + summary_end))
        self.assertTrue(any("the part read together is" in w and "over the 2000 budget" in w
                            for w in warnings(table)), table.stdout)
        # words in a heading count
        heading = run(rep(FIXTURE, summary_end, "\n### " + " ".join(["alpha"] * 2100) + "\n" + summary_end))
        self.assertTrue(any("the part read together is" in w for w in warnings(heading)), heading.stdout)

    def test_word_budget_grows_per_slice_beyond_eight(self) -> None:
        eight = add_slices(FIXTURE, ["Alpha", "Bravo", "Charlie", "Delta", "Echo"])
        nine = add_slices(FIXTURE, ["Alpha", "Bravo", "Charlie", "Delta", "Echo", "Foxtrot"])
        total_eight = reported(run(eight), "in all")
        total_nine = reported(run(nine), "in all")
        self.assertIn("budget about 4000 for 8 slices", run(eight).stdout)
        self.assertIn("budget about 4250 for 9 slices", run(nine).stdout)
        # 4,100 words: over the 8-slice budget, inside the 9-slice budget
        pad = "\n## References\n\n" + padding(4100 - total_eight)
        at_eight = run(rep(eight, "\n## References\n", pad))
        self.assertTrue(any("over the 4000 budget" in w for w in warnings(at_eight)), at_eight.stdout)
        pad = "\n## References\n\n" + padding(4100 - total_nine)
        at_nine = run(rep(nine, "\n## References\n", pad))
        self.assertEqual((at_nine.returncode, warnings(at_nine)), (0, []), at_nine.stdout)
        # 4,300 words: over the 9-slice budget of 4,250
        pad = "\n## References\n\n" + padding(4300 - total_nine)
        over = run(rep(nine, "\n## References\n", pad))
        self.assertTrue(any("over the 4250 budget" in w for w in warnings(over)), over.stdout)

    def test_portuguese_headings_and_labels_are_recognised(self) -> None:
        headings = {
            "Summary": "Resumo", "Context and problem": "Contexto e problema",
            "How we will know it worked": "Como saberemos que funcionou", "Scope": "Escopo",
            "How it works": "Como funciona", "Key decisions": "Decisões-chave",
            "Open": "Em aberto", "Slices": "Fatias", "References": "Referências",
        }
        labels = {
            "Delivers": "Entrega", "Depends on": "Depende de", "Applies": "Aplica", "Behaviour": "Comportamento",
            "Order": "Ordem", "Ready to plan?": "Pronto para planejar?", "Rule": "Regra",
        }
        only_headings = FIXTURE
        for english, portuguese in headings.items():
            only_headings = rep(only_headings, f"\n## {english}\n", f"\n## {portuguese}\n")
        self.assertNotEqual(only_headings, FIXTURE)
        self.assert_clean(run(only_headings))
        everything = only_headings
        for english, portuguese in labels.items():
            everything = re.sub(rf"\*\*{re.escape(english)}", f"**{portuguese}", everything)
        everything = re.sub(r"\bclear\b", "clara", everything)
        self.assertIn("**Entrega", everything)
        self.assertIn("2 slices clara", everything)
        self.assert_clean(run(everything))

    def test_wrong_usage_exits_2(self) -> None:
        for label, args in (("no path", []), ("two paths", ["a.md", "b.md"])):
            with self.subTest(case=label):
                result = subprocess.run([sys.executable, str(SCRIPT), *args], capture_output=True, text=True)
                self.assertEqual(result.returncode, 2, result.stdout + result.stderr)
                self.assertIn("Usage: python3 validate_design.py <path-to-design.md>", result.stdout)

    def test_each_structural_defect_is_rejected(self) -> None:
        invoice_head = "> **Status:** clear · **Applies:** D1 (Invoice numbering) · **Depends on:** nothing"
        defects = {
            "anchor that does not resolve": (
                lambda t: rep(t, "| gains `paid_at` | [Invoice](#invoice) |", "| gains `paid_at` | [Invoice](#invoicex) |"),
                "anchor does not resolve: #invoicex"),
            "slice header with no Delivers": (
                lambda t: rep(t, "> **Delivers:** an invoice carries its number and a paid marker.\n", ""),
                "slice 'Invoice' has no Delivers line"),
            "slice header with no Status": (
                lambda t: rep(t, invoice_head, "> **Applies:** D1 (Invoice numbering) · **Depends on:** nothing"),
                "slice 'Invoice' has no Status"),
            "slice header with no Depends on": (
                lambda t: rep(t, invoice_head, "> **Status:** clear · **Applies:** D1 (Invoice numbering)"),
                "slice 'Invoice' does not say what it depends on"),
            "index status differs from the header": (
                lambda t: rep(t, "paid marker | clear |", "paid marker | rfc |"),
                "status in the index (rfc) differs from its header (clear)"),
            "Applies code without its name": (
                lambda t: rep(t, invoice_head, "> **Status:** clear · **Applies:** D1 · **Depends on:** nothing"),
                "cites D1 without its name beside it"),
            "Applies code that is not a key decision": (
                lambda t: rep(t, "**Applies:** D2 (Confirmed payment) · **Depends on:** Payment",
                              "**Applies:** D9 (Other) · **Depends on:** Payment"),
                "applies D9, which is not a key decision"),
            "decision index lists a slice that does not apply it": (
                lambda t: rep(t, "| D1 | Invoice numbering | Invoice, Payment |", "| D1 | Invoice numbering | Invoice, Payment, Receipt |"),
                "decision index says D1 affects 'Receipt', but the slice does not apply it"),
            "slice applies a decision whose index row omits it": (
                lambda t: rep(t, "| D2 | Confirmed payment | Payment, Receipt |", "| D2 | Confirmed payment | Payment |"),
                "slice 'Receipt' applies D2, but the decision index does not list the slice"),
            "no Order line": (
                lambda t: rep(t, "**Order:** Invoice → Payment → Receipt. Nothing runs in parallel.\n", ""),
                "no Order line under the slice index"),
            "Order line that leaves out a slice": (
                lambda t: rep(t, "Invoice → Payment → Receipt.", "Invoice → Payment."),
                "Order line leaves out slices: Receipt"),
            "Order line that names what is not a slice": (
                lambda t: rep(t, "Invoice → Payment → Receipt.", "Invoice → Payment → Receipt → Refund."),
                "Order line names what is not a slice: refund"),
            "Order line that names a slice twice": (
                lambda t: rep(t, "Invoice → Payment → Receipt.", "Invoice → Payment → Payment → Receipt."),
                "Order line names a slice more than once: payment"),
            "clear count that differs from the headers": (
                lambda t: rep(t, "2 slices clear", "3 slices clear"),
                "header says 3 clear slices; the slice headers show 2"),
            "success target with no measurement": (
                lambda t: rep(t, "| under half a day per month | the monthly close checklist |", "| under half a day per month | |"),
                "a success target has no measurement beside it"),
        }
        for label, (mutate, fragment) in defects.items():
            with self.subTest(defect=label):
                self.assert_error(run(mutate(FIXTURE)), fragment)
        for filler in ("n/a", "tbd", "todo"):
            with self.subTest(defect=f"a line that is only {filler}"):
                text = rep(FIXTURE, "\n**Unchanged**", f"\n{filler}\n\n**Unchanged**")
                self.assert_error(run(text), f"empty section filler ({filler})")
        self.assertEqual(len(defects) + 1, 16)

    def test_undefined_cited_code_warns(self) -> None:
        cited = run(rep(FIXTURE, "\n**Unchanged**", "\nThe roadmap item ZZ-77 asked for this.\n\n**Unchanged**"))
        self.assertEqual(cited.returncode, 0, cited.stdout)
        self.assertTrue(any("ZZ-77 is cited and never defined" in w for w in warnings(cited)), cited.stdout)
        defined = run(rep(FIXTURE, "\n**Unchanged**", "\nThe roadmap item ZZ-77: the payment request.\n\n**Unchanged**"))
        self.assertEqual((defined.returncode, warnings(defined)), (0, []), defined.stdout)

    def test_validator_is_upstream_byte_for_byte(self) -> None:
        self.assertEqual(hashlib.sha256(SCRIPT.read_bytes()).hexdigest(), UPSTREAM_SHA256)


if __name__ == "__main__":
    unittest.main()
