---
id: QAS-enforce-spec-anchored-qa-contracts
area: QAS
title: Enforce spec-anchored QA contracts
persona: Workflow adopter
journey: J-adopt-workflow
expected: Each QA case maps to a feature acceptance criterion, a charter is reused when its mission still fits, and filed-issue QA runs only when the fix changes a public promise.
entry_points: .agents/skills/wtk-qa-execute/references/qa-execution.md; .agents/skills/wtk/references/test-contract.md; .agents/skills/wtk/references/review-rounds.md; .agents/skills/wtk-qa-plan/SKILL.md
qa_status: untested
bug_ids:
fix_status:
retest_status:
fix_commits:
evidence: docs/qa/evidence/2026-08-22-spec-anchored-qa-contracts/session.md
last_report: docs/qa/reports/2026-08-22-spec-anchored-qa-contracts.md
overlaps:
---

Covers the public planning contract for immutable per-cycle charters, acceptance-criterion-derived
test cases, and conditional QA in the filed-issue shortcut. The current pass independently re-read
all contract authorities after reload and ran the focused structural test.
