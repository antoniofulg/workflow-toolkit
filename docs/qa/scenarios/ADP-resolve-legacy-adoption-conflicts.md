---
id: ADP-resolve-legacy-adoption-conflicts
area: ADP
title: Resolve reviewed legacy adoption conflicts safely
persona: Workflow adopter
journey: J-adopt-workflow
expected: A maintainer sees pristine owned legacy workflow paths retired without aliases, while modified or unknown destinations remain explicit conflicts and every cancelled or refused target stays byte-for-byte unchanged.
entry_points: README.md#optional-project-instructions; node scripts/migrate.js --root <project>; scripts/migrate.js
qa_status: untested
bug_ids:
fix_status:
retest_status:
fix_commits:
evidence: docs/qa/evidence/2026-09-13-workflow-toolkit-adoption/adoption-summary.md; docs/qa/evidence/2026-09-13-workflow-toolkit-adoption/legacy-pristine.log; docs/qa/evidence/2026-09-13-workflow-toolkit-adoption/legacy-modified.log; docs/qa/evidence/2026-09-13-workflow-toolkit-adoption/legacy-unknown.log
last_report: docs/qa/reports/2026-09-13-workflow-toolkit-adoption.md
overlaps: ADP-layered-workflow-adoption; ADP-adopt-workflow-safely
---

Covers projects copied from an older workflow release before adoption manifests existed. The guided
installer must classify existing unowned workflow paths as conflicts and withhold final confirmation
until every decision is complete. `Back up and replace` preserves exact original bytes and modes;
`Exclude module` recalculates the plan and names any dependency cascade; `Cancel installation`
leaves target, adoption, journal, and backup state unchanged.

Disposable copies must exercise malformed adoption state, unsafe or symlinked paths, dirty/non-Git
targets, edited managed blocks, and unowned collisions through the public guided command. Each case
must name the blocking condition before publication and leave target and outside sentinels unchanged.
Exact injected-failure rollback and direct-argv implementation mechanics stay with technical
verification; QA observes their public atomicity and no-unexpected-effect boundary.

QA Execute on 2026-08-31 passed at `827d629`. A clean committed legacy target reviewed two exact
conflicts, rejected incomplete and unsafe ownership transfers without writes, resolved both through
the public CLI, preserved consumer instruction bytes, reached clean managed status, and remained
byte-stable under normal re-apply. Git-boundary, symlink, and literal-metacharacter probes left no
external or helper effect; every disposable target was removed.

That result is historical. The `interactive-installer` cycle removes the standalone `resolve`
command; current QA proves the same safety promise through the source `retired package installer` path.

Workflow Toolkit Lean replaces the legacy contract completely. The 2026-09-13 walk must prove
hash-owned pristine old paths are removed, modified or unowned old paths block publication, no
legacy alias is installed, and cancellation preserves the full target. Prior legacy reports remain
historical.
