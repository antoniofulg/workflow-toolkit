---
id: ADP-preserve-security-install-target
area: ADP
title: Preserve project state when adding optional security skills
persona: Workflow adopter
journey: J-enable-external-security-skills
expected: Installing a selected security-lifecycle skill through the Skills CLI changes only the selected skill scope and leaves existing project files unchanged.
entry_points: README.md#recommended-companion-skills-and-tools; npx skills add antoniofulg/security-lifecycle --agent '*' --copy --yes
qa_status: skipped
bug_ids:
fix_status:
retest_status:
fix_commits:
evidence:
last_report:
overlaps: ADP-separate-external-security-skills
---

Retired: the previous scenario exercised rollback inside the removed WTK npm installer. Companion
skill installation now belongs to the Skills CLI and its own upstream contract.
