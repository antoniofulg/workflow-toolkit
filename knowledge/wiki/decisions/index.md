# Decisions

The historical `.specs/STATE.md` ledger remains available at the cited Git revision. These pages
hold what its append-only ledger structurally cannot: which requirements a decision constrains,
which invariant it follows from, which alternative it killed.

* [Workflow Toolkit contract](workflow-toolkit-contract.md) - Workflow Toolkit replaces the task pipeline with upstream-shaped Lean and modular routes, sequential whole-slice builds, one full-feature Verifier over a shared verify core, and transient feature artifacts.
* [Fix verification](fix-verification.md) - Refactors, fix batches and risk-area changes get a fresh diff-scoped Verifier while a small covered local fix relies on hosted CI, and the Verifier's role, not a per-task choice, sets its model.
* [Deep review cadence](deep-review-cadence.md) - Deep Review runs on demand through `wtk-deep-review` and does not block the default delivery path; when it runs, a violated project-declared invariant blocks.
* [QA at feature close](qa-at-feature-close.md) - Qualifying public changes receive one QA cycle over the integrated feature; no slice runs QA, and one independent Verifier proves the complete feature first.
