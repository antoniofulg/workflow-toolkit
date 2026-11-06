# Skill-pack generalization — maintainer-approved changes

Date: 2026-11-06. Source: the maintainer's approved change list for branch
`fix/agent-invocable-skills`, recorded with the maintainer's yes to update the knowledge records.

Goal stated by the maintainer: the pack carries general architecture, pattern and workflow guidance
and stops encoding one project's, host's or stack's rules. Project policy becomes a default that
each project can override.

Decisions relevant to recorded concepts:

1. Route snapshots drop the always-constant `deep_review` cadence and `parallelization` fields.
   Behaviour is unchanged: Deep Review stays on demand and the Lean builder stays sequential.
2. A violation of a project-declared architecture invariant or module boundary is a Major defect,
   not an advisory, so a Deep Review that finds one returns `FIX_BEFORE_SHIP`. An optional
   `boundaries` sweep lens reviews dependency direction, boundary leaks, cohesion and
   representable invalid states.
3. Severity and volume live only in the Deep Review taxonomy; there is no numeric finding cap.
4. The reviewer is a fresh agent without the author's transcript; a different model is preferred,
   not sufficient.
5. The `## Approval` section stays a written convention. The anti-forgery value blocklist and the
   validator gate are dropped; the Verifier confirms the approval names who approved which revision.
6. `review_convergence.py` and `remediation.py` are deleted. The stall rule stays in prose:
   halt after N attempts without measurable progress.
7. The public surface contract moves to `wtk/references/dx.md`, loaded by both the Lean and the
   modular planning routes when a public surface changes.
8. The verify obligations both routes share (approval, evidence or zero, visual evidence, the swept
   re-read, fault injection in a scratch worktree) move to one shared section under
   `wtk/references/` that both verify procedures link to. Route-specific steps stay in each.
