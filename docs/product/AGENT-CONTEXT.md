# Agent context

This repository is the my-workflow source pack for a stack-agnostic agent operating system. Product identity
belongs in consuming projects; this index routes source-pack work without loading product history.

## Critical constraints

- Keep shared workflow instructions product-neutral and preserve consumer-owned product context.
- Use the smallest role- and task-specific reference set; surface missing required context as a gap.
- Keep task classification, safety, QA, review, role separation, and permission boundaries intact.

## Role/task routes

| Role or task | Read only |
| --- | --- |
| Visual polish or visual adjustment | `.agents/skills/wtk/references/ui-ux.md`; `.agents/skills/wtk/references/frontend.md` |
| Customer-facing copy | [unset — source pack has no customer voice reference; consuming projects fill this route] |
| Boundary change | `.agents/skills/wtk/references/modeling.md`; `.agents/skills/wtk-plan/references/dx.md` |
| Planner, other feature | `README.md#purpose`; `docs/toolkit/README.md`; affected capability/journey docs |
| Implementer | Approved slice; `AGENTS.md#critical-rules`; relevant architecture/design docs |
| Reviewer or verifier | `.agents/skills/wtk/references/review-rounds.md`; `.agents/skills/wtk/references/evidence.md`; assigned spec/tests |
| Unknown scope or dependency | `.agents/skills/wtk/references/context-budget.md`; add affected reference with an explicit reason |
