---
id: ADP-install-pinned-external-security-skills
area: ADP
title: Install exactly the reviewed bundled security skills
persona: Workflow adopter
journey: J-enable-external-security-skills
expected: Guided installation publishes five reviewed security skill trees and the original security-pentest tree with matching Claude links; reviewed source, path, CLI version, commit, and tree hash match skills-lock.json without a networked second step.
entry_points: npx workflow-toolkit install; skills-lock.json; .agents/skills/; .claude/skills/
qa_status: untested
bug_ids: BUG-20260822-security-installer-rejects-active-npx
fix_status: fixed
retest_status: pass
fix_commits: 1fa087d; 7795295
evidence: docs/qa/evidence/2026-08-22-external-security-skills/session.md
last_report: docs/qa/reports/2026-08-22-external-security-skills.md
overlaps:
---

Owns packaged provenance and installed-result promises for the five reviewed security skills and
the original `security-pentest` skill.
Historical evidence covers the retired standalone installer only; the bundled core path requires a
fresh exact-package walk.
