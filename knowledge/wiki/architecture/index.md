# Architecture

How the system is shaped. Architecture invariants live in the consuming project's architecture
docs. `AD-NNN` with three digits is a project decision and lives in `.specs/STATE.md`. They are
different namespaces.

* [Workflow runtime ownership](workflow-runtime-ownership.md) - Keep installer inputs in the package and reusable runtime with its owning skill, preserving product-owned content.
* [Security skill integration](security-skill-integration.md) - Security guidance depends on installed skills, reproducible distribution and phase routing agreeing.
* [Construction constraints](construction-constraints.md) - Preserve explicit reuse, construction order, and approval requirements across planning, delegation, verification, and resume.
