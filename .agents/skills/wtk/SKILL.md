---
name: wtk
description: Route Workflow Toolkit work to the smallest applicable procedure, including bounded instruction or documentation corrections. Use for feature work, fixes, or workflow questions.
license: CC-BY-4.0
metadata:
  author: Antonio Fulgêncio
  version: '6.4.0'
---

# Workflow Toolkit

Use this entrypoint to select the smallest applicable Workflow Toolkit procedure. Keep the
router loaded and load only the selected skill and its directly relevant references.

## Route

Load shared references only for the current operation:

| Operation | Reference |
| --- | --- |
| Propose, dispatch or resume delegated work | [Agent selection](references/agent-selection.md) |
| Plan, implement, refactor, or review code | [Code reuse and ownership](references/code-reuse.md) |
| Security surface or abuse case | [Security boundary](references/security.md) |
| Screen, interaction, or visual reference | [UI/UX surface map](references/ui-ux.md) and [front-end organization](references/frontend.md) |
| Domain boundary or dependency direction | [Modeling](references/modeling.md) |
| Add or change a public surface — route, CLI verb, config key, export | [Public surface contract](references/dx.md) |
| Choose checks or reuse evidence | [Validation](references/validation.md) |
| Start, reuse or close an application/test environment | [Runtime lifecycle](references/runtime-lifecycle.md) |
| Report completion or commit evidence | [Evidence](references/evidence.md) |
| Write, review or derive tests, choose their layer, or handle an unstable test | [Test contract](references/test-contract.md) |
| Review code or act on findings | [Review rounds](references/review-rounds.md) |
| Create a branch or isolate a checkout | [Git](references/git.md) |
| PRD/RFC/ADR work, decision-store ownership, or artifact retention | [Artifacts](references/artifacts.md) |
| Preserve explicit reuse, construction order or approval requirements | [Construction constraints](references/construction-constraints.md) |
| Phase checkpoint, resume, compaction, context pressure or session transfer | [Context recovery](references/context-handoff.md) |
| Edit agent instructions or skill references | [Context budget](references/context-budget.md) |
| Implementation through delivery, when the project's `AGENTS.md` opts into execution metrics ([settings](references/project-settings.md)) | [Execution metrics](references/execution-metrics.md) |
| Derive criteria/checks, build, verify, or apply adopted project guidance | [Project requirements](references/project-requirements.md) |
| Read or record a project-declared WTK command, path or policy | [Project settings](references/project-settings.md) |

- An explicit PRD, RFC or ADR authoring request: follow
  [product and decision artifacts](references/artifacts.md#product-and-decision-artifacts).
  Honor the requested document boundary; an artifact-only request does not start a feature build.
- A request to set up, assess or update a project's guidance and driver-skill responsibilities:
  read and invoke `wtk-setup`. Assessment remains read-only; installation itself never runs setup.
- An authorized bounded documentation, instruction-only skill, or direct correction: the active
  agent applies the maintenance route in `.agents/skills/wtk/references/validation.md`, including declarative
  registration in an existing skill catalog. Complete its scoped checks and local commit; a change
  to executable code then follows that reference's fix verification. Escalate for a substantive behavior or authority change, not merely a new
  skill name, registry entry, CLI label, or pending merge.
- An unshaped idea, an analytics/error signal requiring a product or architecture decision, or
  competing solution alternatives: read and invoke `wtk-discover`. It may conclude build,
  build smaller/differently, not now, or do not build.
- An existing integrated Lean feature directory with `plan.md`, `checks.md`, or
  `verification.md`: resume the matching `wtk-lean` phase; do not route it to the modular entries.
- A decided feature without Lean artifacts: read and invoke `wtk-lean`, which runs Plan → Checks →
  Build → Verify using `.specs/features/<feature>/plan.md`, `checks.md`, and `verification.md`.
- A decided design or ticket that needs the modular upstream contract: read and invoke `wtk-plan`,
  which produces the upstream `.tasks/<name>.md` contract.
- An approved modular `.tasks/<name>.md` or `.checks/<feature>.md`: read and invoke
  `wtk-implement`.
- A request to review, audit or slim the tests of a module, feature or page: read and invoke
  `wtk-test-review`. It proposes removals and missing tests; it never deletes a test.
- Slow or flaky CI, or a request to audit the suite's cost, find which tests can be cheaper or
  reduce test cost: read and invoke `wtk-test-audit`. It ranks and classifies the whole suite from
  CI data and proposes only; one scope with mutation stays `wtk-test-review`.
- A diagnosis with no unresolved product or architecture choice: continue diagnosis directly; do not
  route to discovery merely because the cause is unknown.
- A user explicitly names a capability (`wtk-deep-review`, `wtk-qa`, `wtk-ship`, or
  another `wtk-*` skill): invoke that capability directly and do not reopen planning.
- A capability requested in plain words routes the same way: "review in depth" → `wtk-deep-review`,
  "peer review the plan" → `wtk-plan-review`, "check reuse" → `wtk-reuse-review`, "walk QA" →
  `wtk-qa`, "ship it" → `wtk-ship`, "check knowledge" → `wtk-knowledge-check`, "review the tests of
  X" → `wtk-test-review`, "reduce test cost" → `wtk-test-audit`.

When `wtk-discover` resolves an idea that entered through this router, continue into the integrated
Lean route after the discovery decision. Direct invocation of `wtk-discover` retains its upstream
modular handoff to `wtk-plan`.

Ask only the smallest question needed to distinguish routes. Do not preload quality, UI, security,
QA, review, or delivery procedures; load them only when the selected route or changed surface
requires them. For Plan or Specify work touching runtime, configuration, dependency, public behaviour,
authentication, or authorization, read `references/security.md` before coding, using `## 2. At
Specify — declare the surfaces` and `## 3. At the test contract — abuse cases get IDs` at their
named phases; use `## 5. At review — the residual only` during review. Do not run a broad security
audit without a matching trigger or explicit request. Before Design or Build work that adds or changes
a screen or interaction, read `references/ui-ux.md` and any feature `uiux.md`; a feature with no
changed screen skips it. `wtk-lean` defaults its approved verification profile to `standard`; use `ui`
when binding interface sources are part of the feature.

The Lean artifacts and the modular entries deliberately retain their upstream names and schemas.
Completed feature artifacts are transient: after independent verification and selected local gates,
promote durable facts and delete the feature directory according to the lifecycle procedure.
