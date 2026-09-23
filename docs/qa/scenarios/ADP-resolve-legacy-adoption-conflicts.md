---
id: ADP-resolve-legacy-adoption-conflicts
area: ADP
title: Resolve legacy WTK ownership safely
persona: Workflow adopter
journey: J-adopt-workflow
expected: The migration helper previews legacy ownership, refuses modified hashes without writes, removes only verified files, blocks, links, packets, and ignore entries, and restores the exact target on publication failure.
entry_points: README.md#optional-project-instructions; node scripts/migrate.js --root project; scripts/migrate.js
qa_status: untested
bug_ids:
fix_status:
retest_status:
fix_commits:
evidence: docs/qa/evidence/2026-09-23-skills-only-workflow/migration-results.json
last_report: docs/qa/reports/2026-09-23-skills-only-workflow.md
overlaps: ADP-adopt-workflow-safely
---

Walk pristine, edited, multi-block, generated-packet, and interrupted-publication fixtures through
the explicit migration helper. Preview remains read-only. Apply backs up bytes and modes, preserves
surrounding project prose and unrelated files, removes the old adoption manifest, and reports
unowned workflow prose for manual review. A failed publication restores files, links, modes,
instruction bytes, and adoption state exactly.

QA on 2026-09-23 passed public preview, apply, and conflict paths with independent byte, mode, link,
backup, manifest, journal, and residue readback. The shipped failure hook restored exact state, but
the public CLI exposes no safe fault-injection or rollback option. That forward evidence does not
grant a public-interface pass, so this scenario remains `untested`.
