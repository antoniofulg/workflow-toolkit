---
id: ADP-adopt-workflow-safely
area: ADP
title: Install WTK skills without replacing project state
persona: Workflow adopter
journey: J-adopt-workflow
expected: The full 12-skill WTK set installs through the Skills CLI while project instructions, native agent model and effort metadata, configuration, generated files, ignores, product context, and knowledge remain byte-for-byte unchanged; an existing adoption can preview and apply the migration helper safely.
entry_points: README.md#install-the-skills; npx skills add antoniofulg/workflow-toolkit --skill wtk wtk-deep-review wtk-discover wtk-implement wtk-knowledge-check wtk-lean wtk-plan wtk-qa wtk-qa-execute wtk-qa-plan wtk-reuse-review wtk-ship --agent '*' --copy --yes; node scripts/migrate.js --root project
qa_status: untested
bug_ids: BUG-20260923-skills-cli-omits-required-wtk-skills; BUG-20260923-full-set-scenarios-use-partial-install-command
fix_status: fixed
retest_status: pass
fix_commits: a9566e3; d363b1c
evidence: docs/qa/evidence/2026-09-23-native-agent-settings/install-readback.json; docs/qa/evidence/2026-09-23-native-agent-settings/migration-readback.json
last_report: docs/qa/reports/2026-09-23-native-agent-settings.md
overlaps: ADP-resolve-legacy-adoption-conflicts
---

Walk a disposable project with existing AGENTS.md, CLAUDE.md, native agent model and effort metadata,
local configuration, provider files,
ignore files, product context, and knowledge files. Run the documented full-set Skills CLI command
and independently compare sentinel files before and after installation. Confirm the installer creates
only its own skill scope.

For a legacy project, run node scripts/migrate.js --root project in preview mode, inspect every
managed file, block, link, packet, and ignore action, then apply it. Confirm hash conflicts refuse
all writes, pristine ownership is backed up with bytes and modes, surrounding prose survives, and
remaining workflow prose is reported for review. Historical installer reports remain historical.

Historical QA on 2026-09-23 passed the previous 13-skill install, host-sentinel preservation, preview,
apply, and conflict legs after `a9566e3`. That report remains historical; the current contract installs
12 skills and leaves native model and effort metadata with the consuming project. Public rollback fault
injection remains unavailable, so this scenario remains `untested` pending a consumer walk.

Fresh QA retest at `d363b1c` confirmed the previous 13-skill entry point matched its then-current README.
Both linked bugs passed retest. The prior evidence does not certify the current 12-skill native-settings
contract.

Fresh QA at `e6002ca1` passed the 12-skill install, all 18 native-file and host-sentinel byte
comparisons, exact 18-packet migration, edited-packet preservation, and managed-conflict refusal.
The public CLI still exposes no safe rollback fault injection, so the scenario remains `untested`
despite every reachable public leg passing.
