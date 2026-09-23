---
id: DOC-read-explicit-workflow-provenance
area: DOC
title: Read current skill provenance and optional scope
persona: Repository reader
journey: J-review-workflow-release
expected: README, pack guide, notices, and installed WTK skills identify project-owned provenance and optional companion sources while keeping the product-neutral workflow scope consistent.
entry_points: README.md; docs/toolkit/pack.md; NOTICE.md; .agents/skills/wtk-qa-plan/SKILL.md; .agents/skills/wtk-qa-execute/SKILL.md
qa_status: pass
bug_ids: BUG-20260923-adaptive-guidelines-recommendation-has-no-source
fix_status: fixed
retest_status: pass
fix_commits: d363b1c
evidence: docs/qa/evidence/2026-09-23-skills-only-workflow/skills-install.json; docs/qa/evidence/2026-09-23-adaptive-guidelines-recommendation/readback.json
last_report: docs/qa/reports/2026-09-23-adaptive-guidelines-recommendation.md
overlaps:
---

Read the current README, pack guide, notices, and full WTK skill inventory. Confirm the Skills CLI
route, project-owned instruction boundary, optional companion table, Lean attribution, QA provenance,
and absence of toolkit-installed security or Ponytail trees. Earlier package and installer reports remain
historical.

Historical QA on 2026-09-23 confirmed current WTK provenance, project-owned instructions, optional companion
scope, Lean attribution, QA provenance, and absence of bundled companion trees. Adaptive Guidelines
lacks a verified source while the pack guide claims all listed sources are named, so the scenario fails.

Historical remediation retest at `d363b1c` found matching README and pack-guide companion scope: all four
recommendations have sources and uses, and Adaptive Guidelines is disclosed only as a pending
candidate. Existing install evidence still proves no optional companion was bundled.

Fresh QA at `68e787c` found matching README and pack-guide scope for five optional companions.
Adaptive Guidelines now names its canonical public GitHub source and accurately describes converting
recurring agent corrections into reviewable project guidelines. Existing install evidence still
proves no optional companion was bundled.
