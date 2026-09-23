---
id: ADP-install-versioned-workflow-package
area: ADP
title: Install the full WTK skill set from its source
persona: Workflow adopter
journey: J-adopt-workflow
expected: The Skills CLI installs the full 12-skill WTK set from the canonical repository into a disposable project, and an independent readback finds no npm installer, WTK configuration payload, or host-file mutation.
entry_points: README.md#install-the-skills; package.json; npx skills add antoniofulg/workflow-toolkit --skill wtk wtk-deep-review wtk-discover wtk-implement wtk-knowledge-check wtk-lean wtk-plan wtk-qa wtk-qa-execute wtk-qa-plan wtk-reuse-review wtk-ship --agent '*' --copy --yes
qa_status: untested
bug_ids: BUG-20260923-skills-cli-omits-required-wtk-skills; BUG-20260923-full-set-scenarios-use-partial-install-command
fix_status: fixed
retest_status: pass
fix_commits: a9566e3; d363b1c
evidence: docs/qa/evidence/2026-09-23-skills-only-workflow/skills-discovery.json; docs/qa/evidence/2026-09-23-skills-only-workflow/skills-install.json; docs/qa/evidence/2026-09-23-skills-only-workflow/scenario-contract-readback.json
last_report: docs/qa/reports/2026-09-23-skills-only-workflow.md
overlaps: ADP-adopt-workflow-safely
---

Use the documented Skills CLI command from a disposable project. Read back the installed skill
directories and confirm their local references resolve. Confirm no bin executable, npm installer,
adoption manifest, generated provider packet, ignore-file edit, or project instruction appeared.

Historical QA on 2026-09-23 passed the previous README's full-skill command after `a9566e3`: every
installed local reference resolved, all host sentinels survived byte-for-byte, and no retired output or
companion appeared. That evidence remains historical after the native-settings boundary changed.

Fresh QA retest at `d363b1c` confirmed the previous entry point selected the same full set as its README.
Run the current 12-skill command before returning this scenario to `pass`.
