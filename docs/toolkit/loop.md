# The loop

`wtk` routes discovery, integrated Lean, and distinct modular entries. Auto-size still holds:
a one-line change gets no feature artifacts; a multi-component feature gets full planning.

Ponytail is an optional companion skill. When a project installs it, its own instructions govern
minimal-code choices; WTK remains usable without it.

Public hierarchy: `Feature -> Slice -> Check`. Resolve cadence with `wtk-config` before dispatch.

## Stages

Walk these in order. The imperative detail lives in `AGENTS.md` and the guideline named in the
last column.

| # | Stage | What it is for | Skip when | Rule |
| --- | --- | --- | --- | --- |
| 1 | **Plan / Checks** | Freeze `plan.md`, `checks.md`, and proof selectors | Auto-sized skip (tiny, obvious change) | `wtk-lean` |
| 2 | **Slice** | One observable behaviour plus the checks that prove it | — | `AGENTS.md` |
| 3 | **Build** | The smallest code that makes the slice true | — | `wtk-lean` and the project's own coding rules |
| 4 | **Scoped gate** | Prove *this* diff, not the whole product | Escalate if the selector cannot scope it | [validation.md](../../.agents/skills/wtk/references/validation.md) |
| 5 | **Atomic commit** | One Conventional Commit after the applicable Lean check state is current | — | `AGENTS.md` |
| 6 | **Technical Verifier** | One fresh independent pass proves every check over the complete feature range; mutants must die at the approved profile | Filed-issue path; no product code in final QA session | installed `wtk/references/review-rounds.md` |
| 7 | **Deep-review** | Correct, safe, maintainable — resolved groups, blocking findings only | Cadence `skip` (no groups; human runs `wtk-deep-review` later), or proportional classifier selects scoped validation | installed `wtk/references/review-rounds.md` |
| 8 | **QA session** | The finished feature, as a person meets it: Plan as needed, then impact-scoped Execute | Feature has no public, UI, API, CLI, or adoption change | installed `wtk-qa-execute/references/qa-execution.md` |
| 9 | **Full gate** | The product gate, once, when the proportional classifier selects it | Scoped gate is sufficient | [validation.md](../../.agents/skills/wtk/references/validation.md) |
| 10 | **Remote delivery** | `wtk-ship` authorizes the feature-branch push, one pull request, and merge after readiness is rechecked | Readiness is evidence, not authorization for deploy/release, production mutations, force-push, direct `main` push, and unrelated remote actions; those need explicit instruction | [evidence.md](../../.agents/skills/wtk/references/evidence.md) |

The feature-closing step is the QA session when the proportional classifier selects a public walk;
no slice runs QA. Implementation slices remain vertical and independently committed; the Technical Verifier reads the
complete feature after implementation; wtk-deep-review follows resolved
groups when selected, then QA and the full/scoped gate follow the route rather than file count or feature wording.

The selected route records its gate and limitation in the handoff.

## Why slices, not “the whole feature”

Review cost explodes with diff size. Every round re-reads the whole change; every fix moves what
the next round reads. Three rounds over one behaviour is a signal about that behaviour. Twenty
over a finished feature is the size talking.

One pull request still. The slice is how much each reading has to hold.

A slice that is not observable or not complete is not a slice. Tests are never a separate task.
e2e is only for a journey nothing else already walks; a second slice in the same journey proves
itself at integration.

## Work classes

| Work | Path |
| --- | --- |
| **Feature** — a capability the product lacks | The full table above |
| **Direct correction** — one exact, unambiguous invariant | The narrowest applicable check in [validation.md](../../.agents/skills/wtk/references/validation.md) |
| **Filed issue** — already reviewed, then parked | `implement → scoped gate → one commit` |
| **Credential-free declarative agent-tool configuration** | The local light path in [validation.md](../../.agents/skills/wtk/references/validation.md) |

A defect nobody filed is a feature at auto-sized depth. A “one-line fix” that opens a schema or a
design question stopped being a filed issue; say so and take the feature path.

## Seven rules that hold at every size

Copied as orientation; `AGENTS.md` is canonical:

1. The gate decides done, not self-assessment.
2. One atomic commit per task.
3. The Verifier is a different actor than the author.
4. A round contains only findings not already raised.
5. Only Critical and Major trigger a remediation check.
6. Stages never loop into each other; review caps and post-fix escalation follow `REVIEW-ROUNDS.md`.
7. Every count or measurement cites the command that produced it.

## Isolated checkouts

If the project isolates checkouts, each owns its runtime. Never `reuseExistingServer: true` across
siblings — a gate in one checkout must not silently test another’s application.
