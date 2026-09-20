---
id: QAS-consult-jev-adviser
area: QAS
title: Assign Jev decisions to the gateway or explicit adviser
persona: Workflow operator
journey: J-consult-jev-adviser
expected: In confirmed gateway sessions the gateway owns every overlapping decision and the explicit adviser handles only uncovered decisions, while standalone consultation and action authority remain intact.
entry_points: direct WTK phase-skill invocation; node .agents/skills/wtk/scripts/advise.mjs --phase <phase> --send
qa_status: untested
bug_ids:
fix_status:
retest_status:
fix_commits:
evidence: docs/qa/evidence/2026-09-20-jev-lifecycle/01-cli-observations.json; docs/qa/evidence/2026-09-20-jev-lifecycle/02-route-policy-readback.json
last_report: docs/qa/reports/2026-09-20-jev-lifecycle.md
overlaps:
---

This promise follows the shared consultation-ownership policy across direct WTK phase invocations.
The command's preview, advice, validation, security and package boundaries have automated feature
proofs. Gateway coexistence has instruction review only; no live combined host-agent walk or
duplicate-call benchmark has verified the new policy, so the scenario remains untested.

The 2026-09-20 offline QA cycle passed six-phase preview, missing-key fallback, changed-input hash,
normalized-input stability, direct-route resolution, and shared-policy readback through the public
CLI/manual adapter. It did not use a key or network and therefore does not establish configured
provider advice or actual host-agent compliance; the full promise remains `untested`.
