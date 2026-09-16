Run the adopted agent operating system as the delivery workflow. Load the guideline named by the
current task before acting, keep product ownership in the consuming project, and use the local
wtk-configuration as the authority for delegated model and effort choices.

## Product context

Read `docs/product/AGENT-CONTEXT.md` before product-specific work. Use its critical constraints and
role/task routes; task-specific routes override role defaults. Load only cited paths or headings and
surface missing required context as a named gap.

| Role/task | Select |
| --- | --- |
| Visual polish / adjustment | Design/accessibility only; stronger evidence if semantics change |
| Customer copy | Voice reference |
| Boundary change | Boundary architecture reference |
| Planner, other feature | Overview + affected capabilities/journeys |
| Plan or Specify: runtime, config, public behaviour, authentication, authorization | `docs/toolkit/guidelines/SECURITY.md` — before coding; use sections 2 and 3 at their named phases |
| Design or Build: screen or interaction | `docs/toolkit/guidelines/UI-UX.md` — before Design or Build; use the feature `uiux.md` when present |
| Implementer | Approved slice + relevant architecture/design |
| Explicit reuse, construction order, or approval requirement | `.agents/skills/wtk/references/construction-constraints.md` |
| Phase checkpoint, resume, compaction, context pressure, or session transfer | `.agents/skills/wtk/references/context-handoff.md` |

Activate Ponytail at full at the start of workflow work and keep it active through Specify, Design,
Tasks, Execute, fixes, and reviews. It stays active until the human explicitly says `stop ponytail`
or `normal mode`.
