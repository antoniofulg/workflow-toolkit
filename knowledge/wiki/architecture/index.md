# Architecture

How the system is shaped. Architecture invariants live in the consuming project's architecture
docs. `AD-NNN` with three digits is a project decision and lives in `.specs/STATE.md`. They are
different namespaces.

* [Workflow runtime ownership](workflow-runtime-ownership.md) - Keep WTK runtime inside its owning skills and preserve project-owned instructions, agent settings, and product context.
* [Security skill integration](security-skill-integration.md) - WTK keeps baseline security guidance while each project chooses optional lifecycle skills for deeper work.
* [Construction constraints](construction-constraints.md) - Preserve explicit reuse, construction order, and approval requirements across planning, delegation, verification, and resume.
