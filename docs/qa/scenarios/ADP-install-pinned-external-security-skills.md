---
id: ADP-install-pinned-external-security-skills
area: ADP
title: Install optional security lifecycle skills separately
persona: Workflow adopter
journey: J-enable-external-security-skills
expected: A project can install selected security-lifecycle skills through the Skills CLI without WTK installing or claiming companion ownership.
entry_points: README.md#recommended-companion-skills-and-tools; npx skills add antoniofulg/security-lifecycle --agent '*' --copy --yes; .agents/skills/security-lifecycle/
qa_status: skipped
bug_ids:
fix_status:
retest_status:
fix_commits:
evidence:
last_report:
overlaps: ADP-separate-external-security-skills
---

Retired: the old promise tested packaged security trees and package lock provenance. WTK no longer
bundles those skills. The replacement journey is ADP-separate-external-security-skills, which
covers the explicit optional installation path.
