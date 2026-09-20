---
id: ADP-preserve-security-install-target
area: ADP
title: Preserve the target when security installation succeeds or fails
persona: Workflow adopter
journey: J-enable-external-security-skills
expected: Guided installation preserves consumer-owned files byte-for-byte, treats modified security skill destinations as conflicts, and restores all security paths and adoption state after publication failure.
entry_points: npx workflow-toolkit install; skills-lock.json; .agents/skills/; .claude/skills/; .my-workflow/adoption.json
qa_status: untested
bug_ids:
fix_status:
retest_status:
fix_commits:
evidence: docs/qa/evidence/2026-08-22-external-security-skills/session.md
last_report: docs/qa/reports/2026-08-22-external-security-skills.md
overlaps:
---

Owns the user-observable preservation, conflict, and rollback outcomes for bundled security paths.
Prior standalone-installer evidence remains historical.
