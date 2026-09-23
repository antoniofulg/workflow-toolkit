---
id: REL-report-current-workflow-release
area: REL
title: Report the current skills-only release consistently
persona: Repository reader
journey: J-review-workflow-release
expected: The changelog, package manifest, Bun lockfile, README, and source skill inventory describe the current skills-only distribution and its explicit migration helper without checkout residue.
entry_points: CHANGELOG.md; README.md; package.json; bun.lock; npx skills add antoniofulg/workflow-toolkit --skill wtk --agent '*' --copy --yes
qa_status: untested
bug_ids:
fix_status:
retest_status:
fix_commits:
evidence:
last_report:
overlaps:
---

Version-neutral owner for public release consistency. For release `1.4.1`, compare the changelog
heading and package manifest before walking the current skills-only installation and migration route.

Compare the newest changelog heading with the package manifest, Bun lockfile, README, and full
wtk skill inventory. Confirm the package has no npm installer executable, the README Skills CLI route
is actionable, optional companions are described separately, and the migration helper is available
for existing adopters. Registry publication and remote consistency remain outside this local scenario.
