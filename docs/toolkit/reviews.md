# Reviews

Review is how reliability gets a **second reader** without getting an infinite loop.

An unbounded loop was measured at 30 rounds on one feature. The rule that caused it sounded
responsible: remediate every confirmed finding **and every nitpick** in the same iteration. Each
nit changes the diff; the next round finds new nits. The loop is unbounded by construction.

[REVIEW-ROUNDS.md](guidelines/REVIEW-ROUNDS.md) is the protocol. The installed `wtk/references/review-rounds.md`
is the runtime copy. This page is the choice.

The public hierarchy is `Feature -> Slice -> Check`. Before dispatch, read
`.agents/skills/wtk-config/SKILL.md`; it resolves the feature's review groups.

## One Verifier role, several phases

The provider `verifier` executes one phase per packet. Deep-review is a separate stage, not a Verifier phase.
Remediation identity, independent counters, and halt behavior follow `REVIEW-ROUNDS.md`; the fingerprint is requirement + root cause + failure path.

| Reviewer | Question only it can answer | Cap |
| --- | --- | --- |
| **Technical Verifier** (feature close) | Does one fresh independent pass prove every check over the complete feature range? | One full-feature pass after the last code-changing slice |
| **Deep-review** (resolved groups; none under cadence `skip`) | Is the code correct, safe, maintainable? | Discovery once; remediation checks until no Critical/Major is open or `stall_attempts` halts |
| **QA session** (feature closing step when the public surface changes) | Does the finished feature feel right, through the declared adapter? | One `wtk-qa-plan` and one `wtk-qa-execute` session; no slice runs QA |

A documentation-only slice follows the proportional classifier in [validation.md](../../.agents/skills/wtk/references/validation.md):
accuracy and affected-link checks close pure maintenance, while mixed changes run canonical tests for
changed executable behavior. Deep-review and QA require named concrete risk or changed public promise;
file count and the word "feature" do not escalate them.

Technical Verifier reads the integrated final tree over the complete feature range. Deep-review reads the integrated
commit range, and the closing QA packets read the integrated final tree under `QA-EXECUTION.md`. The coordinator records
distinct author and proof identities; the last implementer supplies a handoff and never certifies
the integrated result.

They do not send work back to each other. A wtk-deep-review finding never restarts the Verifier. A
Critical/Major finding is fixed under the approved loop and its scoped gate, then proven by a one-job
remediation check (incremental wtk-deep-review); batch and check repeat until none is open or
`stall_attempts` halts. Remediation follows the stall bound: each attempt runs the scoped gate, a smaller failing
test set resets the counter, and an equal-size or larger set increments it. An unavailable gate
halts immediately; a reached nonzero threshold halts with the normalized signature, attempt count,
and fixes tried. If a wtk-deep-review fix changes user-visible behaviour, re-walk **the affected scenario
rows only**.

## What blocks, what files

| Severity | Remediation check? | Feature delivery |
| --- | --- | --- |
| `Critical` | Yes | Fix now |
| `Major` | Yes | Fix now |
| `Minor` | No | Fix in one current-run batch, scoped gate, one commit |
| `Trivial` | No | File an issue |

Every wtk-deep-review defect is fixed inside the feature run. Minor fixes start no new proof round.
Filed Trivial issues are real backlog, not a disposal bin; they do **not** re-enter Verifier + QA +
wtk-deep-review because that ceremony already happened.

A user-visible fix still flags and walks its scenario. A fix that grows into a design or schema
change is a feature.

## Why the Verifier is not the author

A model that implemented the change will defend it. The Verifier re-derives coverage from `plan.md` and
`checks.md` and injects behavioural mutants. Enumerated cases in `checks.md` prove coverage *exists*; mutants
prove it is *real*.

A green gate is not a met requirement. Reviewers compare the deliverable to `plan.md`, `checks.md`,
`verification.md`, and `uiux.md` / `dx.md` field by field. Paraphrase is not parity.

## Evidence

[evidence.md](../../.agents/skills/wtk/references/evidence.md): no completion claim without a
fresh command. Scope binds — unit tests do not justify “feature complete”. A passing review over a
red gate is void.

Escalate when the scoped gate is unavailable or the configured stall threshold is reached. An
open Critical alone does not halt while remediation is making measurable progress. A halt report is
a result.
