---
id: REL-report-current-workflow-release
area: REL
title: Report the current skills-only release consistently
persona: Repository reader
journey: J-review-workflow-release
expected: The changelog, package manifest, Bun lockfile, README, and source skill inventory describe the current skills-only distribution and its explicit migration helper without checkout residue.
entry_points: CHANGELOG.md; README.md; package.json; bun.lock; npx skills add antoniofulg/workflow-toolkit --skill wtk wtk-deep-review wtk-discover wtk-implement wtk-knowledge-check wtk-lean wtk-plan wtk-qa wtk-qa-execute wtk-qa-plan wtk-reuse-review wtk-ship --agent '*' --copy --yes
qa_status: pass
bug_ids: BUG-20260923-changelog-describes-retired-installer; BUG-20260923-source-retains-removed-wtk-config-link
fix_status: fixed
retest_status: pass
fix_commits: f9b1c4d
evidence: docs/qa/evidence/2026-09-23-native-agent-settings/release-retest-readback.json; docs/qa/evidence/2026-09-23-native-agent-settings/install-readback.json
last_report: docs/qa/reports/2026-09-23-native-agent-settings.md
overlaps:
---

Version-neutral owner for public release consistency. For release `1.4.1`, compare the changelog
heading and package manifest before walking the current skills-only installation and migration route.

Compare the newest changelog heading with the package manifest, Bun lockfile, README, and full
wtk skill inventory. Confirm the package has no npm installer executable, the README Skills CLI route
is actionable, optional companions are described separately, and the migration helper is available
for existing adopters. Registry publication and remote consistency remain outside this local scenario.

Fresh QA at `e6002ca1` found matching 12-skill package, Bun lockfile, README, installed inventory,
and provenance guidance. The tracked source still contains a dangling `wtk-config` Claude alias.
The `Unreleased` changelog section is empty, so the newest visible setup guidance remains the
historical `1.4.1` npm-installer and bundled-security instructions. Those two defects fail the
current release-consistency promise without rewriting the historical release entry.

Fresh remediation QA at `f9b1c4d` found current `Unreleased` guidance for the exact 12-skill Skills
CLI command, project-native model and effort settings, optional security lifecycle, and public
migration preview/apply. The historical `1.4.1` block remained byte-identical. Package, lockfile,
README, source inventory, and all 12 resolving Claude aliases now agree.
