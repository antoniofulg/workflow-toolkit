---
id: ADP-adopt-workflow-safely
area: ADP
title: Install WTK skills without replacing project state
persona: Workflow adopter
journey: J-adopt-workflow
expected: The full WTK skill set installs through the Skills CLI while project instructions, configuration, generated files, ignores, product context, and knowledge remain byte-for-byte unchanged; an existing adoption can preview and apply the migration helper safely.
entry_points: README.md#install-the-skills; npx skills add antoniofulg/workflow-toolkit --skill wtk wtk-config wtk-lean --agent '*' --copy --yes; node scripts/migrate.js --root project
qa_status: untested
bug_ids:
fix_status:
retest_status:
fix_commits:
evidence:
last_report:
overlaps: ADP-resolve-legacy-adoption-conflicts
---

Walk a disposable project with existing AGENTS.md, CLAUDE.md, local configuration, provider files,
ignore files, product context, and knowledge files. Run the documented full-set Skills CLI command
and independently compare sentinel files before and after installation. Confirm the installer creates
only its own skill scope.

For a legacy project, run node scripts/migrate.js --root project in preview mode, inspect every
managed file, block, link, packet, and ignore action, then apply it. Confirm hash conflicts refuse
all writes, pristine ownership is backed up with bytes and modes, surrounding prose survives, and
remaining workflow prose is reported for review. Historical installer reports remain historical.
