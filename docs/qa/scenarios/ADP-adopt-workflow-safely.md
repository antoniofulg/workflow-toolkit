---
id: ADP-adopt-workflow-safely
area: ADP
title: Install WTK skills without replacing project state
persona: Workflow adopter
journey: J-adopt-workflow
expected: The full WTK skill set installs through the Skills CLI while project instructions, configuration, generated files, ignores, product context, and knowledge remain byte-for-byte unchanged; an existing adoption can preview and apply the migration helper safely.
entry_points: README.md#install-the-skills; npx skills add antoniofulg/workflow-toolkit --skill wtk wtk-config wtk-lean --agent '*' --copy --yes; node scripts/migrate.js --root project
qa_status: fail
bug_ids: BUG-20260923-skills-cli-omits-required-wtk-skills; BUG-20260923-full-set-scenarios-use-partial-install-command
fix_status: pending
retest_status:
fix_commits: a9566e3
evidence: docs/qa/evidence/2026-09-23-skills-only-workflow/skills-discovery.json; docs/qa/evidence/2026-09-23-skills-only-workflow/skills-install.json; docs/qa/evidence/2026-09-23-skills-only-workflow/migration-results.json; docs/qa/evidence/2026-09-23-skills-only-workflow/scenario-contract-readback.json
last_report: docs/qa/reports/2026-09-23-skills-only-workflow.md
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

QA on 2026-09-23 passed the full 13-skill install, host-sentinel preservation, preview, apply, and
conflict legs after `a9566e3`. Public rollback fault injection remains unavailable, and the scenario's
own entry point selects only 3 of the 13 skills its expected field promises. The scenario therefore
remains failed pending `BUG-20260923-full-set-scenarios-use-partial-install-command`.
