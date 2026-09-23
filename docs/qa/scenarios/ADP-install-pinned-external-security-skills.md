---
id: ADP-install-pinned-external-security-skills
area: ADP
title: Install exactly the reviewed optional security skills
persona: Workflow adopter
journey: J-enable-external-security-skills
expected: Guided installation publishes optional security-lifecycle skill trees from their upstream source with matching Claude links; reviewed source, path, CLI version, commit, and tree hash match skills-lock.json without a networked second step.
entry_points: README.md#recommended-companion-skills-and-tools; npx skills add antoniofulg/security-lifecycle --agent '*' --copy --yes; skills-lock.json
qa_status: untested
bug_ids: BUG-20260822-security-installer-rejects-active-npx
fix_status: fixed
retest_status: pass
fix_commits: 1fa087d; 7795295
evidence: docs/qa/evidence/2026-08-22-external-security-skills/session.md
last_report: docs/qa/reports/2026-08-22-external-security-skills.md
overlaps:
---

Owns packaged provenance and installed-result promises for the optional security-lifecycle skills and
the optional security-lifecycle pentest skill.
Historical evidence covers the retired standalone installer only; the optional core path requires a
fresh exact-package walk.
