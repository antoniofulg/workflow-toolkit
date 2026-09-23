---
id: CFG-resolve-deep-review-cadence
area: CFG
title: Resolve review cadence and remediation controls before QA
persona: Workflow adopter
journey: J-configure-feature-workflow
expected: Without a task-scoped review request, WTK keeps Deep Review on demand with no automatic groups, uses a sequential Lean builder, selects the `auto` QA adapter, and reports the fixed remediation default `stall_attempts = 3`.
entry_points: README.md#the-workflow; AGENTS.md; .agents/skills/wtk-lean/SKILL.md; .agents/skills/wtk-deep-review/SKILL.md; .agents/skills/wtk-qa-execute/SKILL.md; docs/toolkit/guidelines/REVIEW-ROUNDS.md
qa_status: pass
bug_ids:
fix_status:
retest_status:
fix_commits:
evidence: docs/qa/evidence/2026-09-23-native-agent-settings/defaults-readback.json; docs/qa/evidence/2026-09-23-native-agent-settings/route-readback.json
last_report: docs/qa/reports/2026-09-23-native-agent-settings.md
overlaps:
---

Covers the current default route: Deep Review is on demand, the Lean builder remains sequential, QA
uses `auto` without a task-scoped adapter choice, and remediation halts after three consecutive
non-progress attempts. Explicit direct `wtk-deep-review` invocation remains available.

The 2026-08-24 and 2026-08-25 evidence remains historical. Changing the cadence default to `skip`
resets the current verdict until the CLI/manual path is walked again.

Workflow Toolkit Lean keeps Technical Verification, Deep Review, and QA separate. A current walk must
confirm the native route pointers, fixed defaults, and that on-demand Deep Review does not skip
Technical Verification or feature-closing QA.

The prior report predates removal of WTK configuration. Its pass does not establish the current
fixed-default route, so this scenario is reset to `untested` for the native-agent-settings cycle.

Fresh QA at `e6002ca1` observed zero automatic Deep Review groups, a sequential Lean builder, the
installed direct `wtk-deep-review` route, and QA adapter `auto`. Four public convergence calls
established the baseline and three unchanged stalls: counts `0,1,2,3`, then
`stall_threshold_reached` with `stall_attempts: 3`.
