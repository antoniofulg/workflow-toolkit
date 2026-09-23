# Guidelines

Runtime execution contracts live in the installed skill `references/` directories and load by
condition. This source-only page catalogs the ownership map; it is not part of a consuming
project's skill installation.

## Instruction cost

| File | Why it exists |
| --- | --- |
| [context-budget.md](../../.agents/skills/wtk/references/context-budget.md) | Instruction files load into prompts. A previous arrangement dumped more than a thousand mandatory lines before any task. Growing a file with restated prose is a defect. Dispatch by condition. |

## How work is cut and kept

| File | Why it exists |
| --- | --- |
| [code-reuse.md](../../.agents/skills/wtk/references/code-reuse.md) | Find the owning implementation before adding code; verify reuse and consistency across frontend, backend, and tooling. |
| [git.md](../../.agents/skills/wtk/references/git.md) | `type/slug` names the behaviour, never `main`, delete after merge. Isolated checkouts must not share a runtime. |
| [artifacts.md](../../.agents/skills/wtk/references/artifacts.md) | Planning artifacts are finished when the code exists. Durable store is code, `AD-NNN`, `docs/qa/`, product/architecture/design. The inverted arrangement gated drift on documents nobody read. |
| [memory.md](../../.agents/skills/wtk-lean/references/memory.md) | Small slices are cheap to review and expensive to ramp. Shared memory is how reasoning survives the task boundary without becoming a second spec. |
| [validation.md](../../.agents/skills/wtk/references/validation.md) | Proportional scoped gates; full gate only when selected. It also owns the credential-free declarative agent-tool configuration path. Never skip a test to go green. Cached evidence only for the exact tree. |

## Proof

| File | Why it exists |
| --- | --- |
| [test-contract.md](../../.agents/skills/wtk/references/test-contract.md) | “All branches covered” cannot be audited. `UT-001` assigned to one task can. Cases come from the spec; tests assert the contracted outcome. Coverage-only tests are forbidden. |
| [evidence.md](../../.agents/skills/wtk/references/evidence.md) | Completion without a fresh command is a false report. Scope binds. Secrets in a diff are an absolute stop. |
| [review-rounds.md](../../.agents/skills/wtk/references/review-rounds.md) | See [reviews.md](reviews.md). Caps, monotonic findings, filed issues. |
| [security.md](../../.agents/skills/wtk/references/security.md) | Security that lives only in a review at the end is theatre. Eleven surfaces, declared at Specify, become `SEC-` cases. Review looks for what the table missed. |

## Surfaces people meet

| File | Why it exists |
| --- | --- |
| [ui-ux.md](../../.agents/skills/wtk/references/ui-ux.md) | Internals designed first get redesigned when the screen moves. `uiux.md` enumerates states so a design agent can execute, and so QA knows the feature is UI-bearing. |
| [dx.md](../../.agents/skills/wtk-plan/references/dx.md) | Same idea one layer down: routes, config, CLI, exports — written as if already shipped, failures enumerated, then internals serve that contract. |
| [frontend.md](../../.agents/skills/wtk/references/frontend.md) | Feature folders own capability; shared UI owns reuse. Routes compose, they do not draw layout. Keeps front-end organization portable (no framework names). |
| [modeling.md](../../.agents/skills/wtk/references/modeling.md) | The domain must outlive the web, API, and persistence frameworks. One aggregate, one module; invariants in the transition, not only in SQL. |
| [qa-scenarios.md](../../.agents/skills/wtk-qa/references/qa-scenarios.md) | Feature verification dies with the feature. A scenario holds a verdict that survives, and goes stale when a diff invalidates it. Content-addressed ids so parallel branches do not collide. |
| [qa-execution.md](../../.agents/skills/wtk-qa-execute/references/qa-execution.md) | A green automated suite can still fail its user. Persona, independent confirmation, dated report. Auto-fix only when the change is contained, unambiguous, and regression-tested. |

## Durable understanding

| File | Why it exists |
| --- | --- |
| [knowledge-wiki.md](../../.agents/skills/wtk-knowledge-check/references/knowledge-wiki.md) | Source documents cannot see each other. The wiki holds the graph and the contradictions. Source always wins. Harvest is explicit and per finished feature, never part of `make check`. |

## How to add a guideline

Do not. Extend an existing file, or justify why both must exist, in [context-budget.md](../../.agents/skills/wtk/references/context-budget.md). A rule earns lines by preventing a defect that occurred, or by resolving an ambiguity an agent actually hit.
