# Review Rounds

**Read when:** reviewing code, or acting on review findings.

**Why this exists:** Remediating every nitpick in one iteration is unbounded: each fix changes the
diff and the next review finds new nits. Monotonic findings, in-run defect batches, a stall bound,
and filed Trivials make review end.

## The review stages, and what each is for

| Stage | Asks | Cap |
| --- | --- | --- |
| **Technical Verifier** (feature closing step) | Does one fresh independent pass prove every check over the complete feature range? | One full-feature pass after the last code-changing slice |
| **wtk-deep-review** (resolved implementation groups) | Is the code correct, safe and maintainable? | Discovery once; one remediation check per batch until no Critical/Major is open or `stall_attempts` halts |
| **QA session** (feature closing step when the public surface changes) | Does the finished feature work for a real user? | Plan as needed; one impact-scoped Execute cycle |
The selected `verification` or `qa` stage executes exactly one phase per packet: `technical`, `wtk-qa-plan`, or `wtk-qa-execute`.
The orchestrator dispatches one technical packet over the complete feature range after
the last code-changing slice and QA packets once, at feature close, when the feature changes public,
UI, API, CLI, or adoption behaviour; no slice runs QA. Deep-review is a separate orchestrator stage, not a Verifier phase.
The QA session reads `../../wtk-qa/references/qa-scenarios.md` for scenario fields and statuses.

Intent vocabulary is routing input, not a keyword bypass. `wtk` selects discovery, integrated Lean,
modular planning/implementation, diagnosis, or an explicitly named capability from the request and
repository state. State facts and validation before dispatch; escalation requires newly discovered
named evidence, not file count or UI presence. An `issue` is neutral until repository evidence
identifies its applicable route.

## Why resolved groups, not a rigid interval

A discovery review reads the whole change, so its cost explodes with the diff. The remediation check
reads only `reviewed_head..HEAD`, so remediation cost tracks the fix, not the feature.

Use the project-owned `wtk-lean/scripts/workflow_route.py` snapshot when a feature route is needed.
Follow [agent selection](agent-selection.md) before delegation or a changed stage choice.
Deep Review is on demand by default, and one pull request and one actor per stage remain unchanged.

**Stages do not loop back into each other.** A wtk-deep-review finding never sends work back to
Technical Verifier. A clean remediation check or the stall bound ends the loop; neither revokes the
approval for local remediation already in progress. The post-fix gate and escalation rule below
decide whether the feature's selected review route is done.

Before final QA, complete the final pending implementation wtk-deep-review group; cadence `skip` resolves no groups, so nothing waits for wtk-deep-review. For QA code remediation, review only `reviewed_head..HEAD`, then re-walk affected scenario rows.

## The feature closing step

A feature's closing step is the **QA session** when its public, UI, API, CLI, or adoption surface
requires a user walk, after the final implementation review group. It needs the whole feature and
cannot run on part of one. The `wtk-qa-plan` and `wtk-qa-execute` skills own it.

It writes no product code and does not replace the feature's technical Verifier or wtk-deep-review.
It walks every scenario the feature flagged. `../../wtk-qa-execute/references/qa-execution.md` owns conditional Plan dispatch and
same non-author session reuse; packet phases remain distinct.

## Hard rules

1. **A review contains only findings not raised before.** Before writing a finding, read the prior
   ledger. A pending, accepted, or already-resolved issue is never re-raised. This is what makes the
   loop monotonic and therefore finite.

   `wtk` points here for remediation identity and counting; this rule prevents a renamed
   finding from resetting its history while allowing a distinct finding to proceed.
2. **Nitpicks never trigger a review.** Fix every confirmed wtk-deep-review defect in the active feature run, except a Minor with no realistic trigger, which is filed as an issue. Critical and Major findings trigger one remediation batch, then one remediation check: a one-job incremental wtk-deep-review over `reviewed_head..HEAD` that dispositions every open prior finding and reviews the fix. Repeat batch + check until no Critical/Major is open or the default three-attempt stall bound halts. Minor findings join that batch, or close together in one Minor-only batch with one scoped gate and one commit; a Minor-only batch starts no full-feature Technical Verifier, QA phase, or remediation check, and gets [fix verification](validation.md#fix-verification) over its diff. Trivials and advisories go to the pull request follow-up list. **In an active, already-approved review loop, fix blocking findings without new human approval and run the scoped gate after each correction; escalate only if the post-fix gate fails or the stall threshold is reached for the same fingerprint.** Local fixes only; remote actions retain separate approval requirements.
3. **Deduplicate by root cause, not by occurrence.** One missing null check repeated in six files is
   one finding that lists six files — not six findings.
4. **Verify before flagging.** Check adjacent comments, accepted [project decisions](artifacts.md#decision-store),
   or a test validating the behaviour. Unconventional is not the same as wrong.
5. **Never report what a linter already catches.** Run the consuming project's linter first and drop
   every overlapping candidate.
6. **The reviewer is not the author.** The reviewer is a fresh agent without the author's
   transcript; a different model is preferred, not sufficient.
   Verifier and Deep Reviewer receive fresh role packets. They do not inherit the Implementer's
   transcript or operator handoff. Their conclusions must come from the spec, diff, tests, and
   assigned evidence.
7. **Documentation and instruction changes follow the proportional classifier in `.agents/skills/wtk/references/validation.md`.** Pure maintenance and bounded instruction changes do not start wtk-deep-review or QA by default; mixed changes run canonical checks for changed executable behavior. Named concrete risk or changed public promise can select stronger review; file count and the word "feature" do not escalate them.
8. **A passing verdict requires valid evidence for its scope.** Apply `.agents/skills/wtk/references/validation.md` to the finding's causal path and retain unaffected results.
   A failed full run stays failed even when focused correction proofs pass.
9. **A new control for an unobserved failure is Major (YAGNI) unless the spec named it.** A
   killed-process shim, a test-of-the-test, or a prefix allowlist the spec did not name is overbuild.
   Filed-issue review uses the same rule; YAGNI is blocking without a companion skill.

## Fingerprinted remediation accounting
`fingerprint = requirement + root cause + failure path` is each finding's identity. Rewording or reopening a finding preserves its fingerprint and its attempt count; a distinct finding starts at zero.
## The Review-Signal trailer

The delivery commit for a pull request carries one `Review-Signal:` line recording its review
outcome, so the record survives the pruning of `.specs/features/`. The line is optional, and no
bundled validator checks it.

## Finding shape
Every finding states, in this order:

- **Premise** — the fact in the code that starts the argument, with `file:line`
- **Path** — the concrete sequence from that fact to a wrong outcome
- **Verdict** — severity from the [review taxonomy](../../wtk-deep-review/references/taxonomy.md#severity), never inflated
A finding without a failure path is an advisory, not a defect. Advisories state
**Premise → Improvement → Fix** and never block.

The Verifier and wtk-deep-review share that one severity vocabulary. An unfixed `Critical` or
`Major` means the verdict is `FIX_BEFORE_SHIP`, and only those severities trigger a remediation
check. A realistic trigger is an input or state the feature's normal use can reach.

Filed issues are real work, not a disposal bin. They enter the backlog like any other item.

## Fixing a filed issue

**A filed issue does not re-enter the loop above, but its fix is still verified.** The review
examined the defect, not the fix. A Minor with a realistic trigger never enters this path; it closes inside its originating feature run.

Fix one, or a batch of them, as a small change:

```
implement → scoped gate → one commit for the batch → fresh Verifier → delivery
```

[Fix verification](validation.md#fix-verification) owns the Verifier and its exceptions. No spec, no
tasks file, no wtk-deep-review round. `wtk` already sizes this way:
a change of a few files with an obvious outcome skips planning entirely.

Three things still apply, because they are about the change and not about the review:

- **If the fix changes user-visible behaviour**, flag its scenario per `../../wtk-qa/references/qa-scenarios.md` and walk it.
  A `Trivial` finding on a screen is still a change a user can see.
- **If the fix touches a security surface**, `security.md` fires as it would for any diff.
- **If the fix turns out to be large** — it needs a schema change, it spreads across a boundary, the
  "one-line fix" opens a design question — it stopped being a filed issue and became a feature. Take
  it through the full loop and say why.

Batch aggressively. One commit per remediation batch is already the commit rule, and a batch of six
`Trivial` findings in one area is one review's worth of attention, not six.

## Escalation

While a remediation check leaves a Critical/Major open, finish approved remediation and run its scoped gate after every attempt; the fix needs no new approval. Halt after three attempts (`stall_attempts`) on the same fingerprint without measurable progress, such as a shrinking failing-test set, and report the attempt count and fixes tried. If the gate is unavailable, halt immediately. wtk-ship uses the same halt contract.

## Requirement and contract parity

A green gate proves the code compiles, lints and passes its tests. It does not prove the code matches
the feature contract. Every reviewer additionally compares the deliverable against the canonical
artifacts — `plan.md` acceptance criteria, `checks.md` cases, the independent `verification.md` report,
and the `uiux.md` / `dx.md` surface contracts when they exist — field by field, not by paraphrase.

The failure this prevents is specific: a change can pass many review rounds while contradicting the
plan and checks, because every round measured engineering quality against an implementation paraphrase and nothing ever compared it to the source.
