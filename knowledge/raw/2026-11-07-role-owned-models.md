# Role-owned models — maintainer decision

Recorded on 2026-11-07 from a maintainer-approved handoff.

## Change

On 2026-11-07 model and effort became fixed per agent role, per harness, in the user's agent files.
Role names are the same on every harness; a routing table in the user's agent instructions maps work
to roles without naming models. WTK still told the dispatching agent to pick model and effort per
task and gave role presets no authority, so any WTK run could override that table.

## Maintainer's rule

1. Dispatch by role: the role comes from the routing table, and model and effort from the role's
   agent file. WTK never chooses, overrides or upgrades them per task.
2. A risk-area Verifier is `verifier-risk`; any other is `verifier`. This replaces the
   2026-11-07 model hint (strongest model for risk, mid-tier otherwise).
3. Deep Review reviewers are `verifier` for ordinary cohorts and `verifier-risk` for risk cohorts.
4. The selection snapshot records each stage's role plus the model and effort it resolved to.
5. A host without the selected role stops that dispatch; no model is substituted.
6. WTK points to the routing table and never copies it or model names.
