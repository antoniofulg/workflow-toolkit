# Verification Evidence

**Read when:** reporting completion or preparing a commit.

Match each claim to evidence covering its scope. `.agents/skills/wtk/references/validation.md` selects the checks and defines when
passing evidence can be reused; this document defines what the result supports.

## Scope binds

| Claim | Required evidence |
| --- | --- |
| Test passes | That test ran and passed |
| Slice complete | Named proofs and scoped gate passed |
| Feature complete / ready for a pull request | Fresh independent full-feature Verifier, selected gates and applicable QA |
| Bounded documentation or instruction update | Proportional checks from `.agents/skills/wtk/references/validation.md` |
| Previously verified feature with bounded follow-ups | Recorded feature receipt plus scoped evidence for the subsequent changes; no new feature certification |
| Visual reference matched | Paired evidence at the states/viewports required by `references/ui-ux.md` |
| Bug fixed | Original symptom observed failing, then passing |
| Regression test discriminates | Red before the fix and green after |

For spec-driven work, compare the deliverable with the approved criteria, checks and binding surface
contracts, including concrete names, values and behavior. Passing tests do not permit rewriting a
requirement to match the implementation. Use `verification.md` when the feature requires it.

## Report shape

For bounded edits, report the change and the validation command, exit code, decisive output and any
limitation. No separate report file or full feature template is needed.

For implementation/delivery summaries, append [execution metrics](execution-metrics.md) from the
collected stage receipts. Late or unavailable measurements remain explicit gaps, not estimates of usage.

For slice/feature handoffs or failed gates, record:

```text
Claim:     <scope>
Evidence:  <command, exit code, decisive output; fresh or valid cached record>
Contract:  <approved artifacts compared and result, or n/a>
QA:        <applicable scenario verdicts, or no changed user-visible behavior>
Verdict:   PASS | FAIL — <limitations or blockers>
```

Numbers must come from the cited command. A slice report states which full-feature verification or
gate remains deferred. On failure, report the failure and remaining work without claiming completion.

## Before a commit

Use passing evidence at the scope selected by `.agents/skills/wtk/references/validation.md`, account for applicable QA flags, and check
that the staged diff matches the requested change. Report that evidence, then commit. Before a pull
request, recheck delivery readiness through `wtk-ship`; its invocation supplies only its defined authority.

## When verification fails

Read the failures and group them by cause. Where timing or isolation is plausible, rerun unchanged
before modifying code. Resolve failures caused by the authorized change, preserving assertions and
the approved contract. Reselect tests from the fix's causal delta under `validation.md`; retain
unaffected green evidence. Record a failed full run separately from passing targeted retests.
An isolated pass is diagnostic evidence, not proof of a harness flake or a green full gate.

Follow `references/review-rounds.md` for review remediation and its stall bound. Report pre-existing or unrelated
failures separately; do not silently expand the task to repair them or claim the full gate passed.

## Stop and hand it back

Request direction when a required decision remains unresolved, the approved contract must change,
the selected gate is unavailable, the remediation stall bound is reached, or completion needs new
authority. Existing authorization remains valid for routine local fixes and applicable checks.

If credentials or secrets appear in a diff, log, fixture or artifact, stop that exposure path and
report without reproducing the values. Do not proceed by weakening tests, hiding failures or using
unauthorized remote/production actions. Name the blocker and the condition needed to resume.
