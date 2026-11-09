---
name: wtk-test-audit
description: Audit a whole test suite for cost and flakiness from CI data and classify every expensive test by the cheapest layer that proves it. Use when CI is slow or flaky, or when asked to audit the e2e or browser suite, find which tests can be cheaper, or reduce test cost; not reviewing one scope with mutation, deleting tests or fixing the product.
license: CC-BY-4.0
metadata:
  author: Antonio Fulgêncio
  version: '6.1.0'
---

# Test audit

Audit the whole suite when CI is slow or flaky - "audit our browser suite", "which tests can be
cheaper", "reduce test cost". Rank tests from CI data, then classify every expensive one by the
cheapest layer that proves it under the
[test contract](../wtk/references/test-contract.md#choosing-the-layer). **Propose only.** The audit
names candidates; every removal or move runs through
[pruning](../wtk/references/test-contract.md#pruning), owner approval and a fresh Verifier.
[`wtk-test-review`](../wtk-test-review/SKILL.md) stays the one-scope review with mutation; the audit
feeds it and never replaces it.

## Settings

Read the project's `tiers`, `test-audit` and `test-review scopes`
[settings](../wtk/references/project-settings.md):

- the [test tiers](../wtk/references/validation.md#test-tiers) and their commands;
- the test runner's final summary format: how it reports failed, flaky or passed on retry, and
  did not run;
- the CI log source for recent pull-request and deploy runs, every attempt included;
- where component, integration and e2e tests live;
- the lane or shard layout and worker count.

Without settings, use the stack-neutral defaults: the hosting provider's run logs, the runner's own
summary, test roots found by tracing the code, and one lane. Name every default you took in the
report. Install nothing.

## Audit

1. **Rank from data.** Follow [cost ranking](references/cost-ranking.md): parse the runner's
   summaries from every attempt of recent runs, aggregate by file and title, and produce a flake
   ranking and a cost ranking. Record both on the tracking issue before classifying.
2. **Diagnose the top flakes before proposing fixes.** A timeout reported at a `finally` or
   teardown call is where the clock ran out; find the slow step in the trace or step timings.
   Check library behaviour in the vendor docs before trusting a theory. A real product race is a
   bug: file it, never weaken the test.
3. **Classify every expensive test.** Split files by cost across two or three read-only auditors
   with a call budget each. Each test gets exactly one class:
   - **REMOVE**, naming the covering test;
   - **ARTIFACT-ONLY**: its only effect is output no assertion or gate reads;
   - **TO-COMPONENT**: every assertion is a UI state the component layer proves;
   - **TO-INTEGRATION**: it re-asserts rows, refusals or permissions an integration test owns;
   - **TRIM**, naming the assertions or the repeated viewport or theme that move;
   - **KEEP**, with the browser-only reason from the layer table.

   Estimate the seconds saved per test, list what was not checked, and label every estimate as
   read from titles. Title-based estimates run about twice the real saving: many UI-state tests
   also check rows, real layout or real network behaviour, and those assertions stay in the
   browser. Only an implementer reading each assertion finds the real number.
4. **Plan batches by confidence**, in this order: confirmed duplicates; moves to component tests;
   moves to integration tests; files owned by in-flight branches, after those merge. About four
   spec files per batch, so one implementer finishes within its turn budget, committing after
   each file.
5. **Hand over for execution.** Each batch runs through `wtk-test-review` or the pruning
   procedure. For every assertion the implementer reads the covering test's assertion, not its
   title; adds the missing assertion to the cheaper test and runs it first; then removes it from
   e2e, mapping each removed assertion to the `file:line` of its kept proof in the commit. An
   assertion with no lower proof stays. Nobody edits the checkout during a local browser run; a
   run against a changed tree is not evidence.
6. **Re-check timing after removals.** A removed screenshot or network-idle navigation may have
   been the only wait before a count, text or attribute read. Wait for the loading state to end,
   such as `aria-busy` gone, or poll the assertion; never sleep.
7. **Guard against regression.** Propose a ratchet test that counts known-bad patterns per file
   against a baseline that may only go down: network-idle waits, fixed sleeps, serial groups, and
   screenshots nothing asserts on.
8. **Measure.** Report the real saving from CI runs, not the estimate: full-run browser
   worker-minutes, the longest shard and the first-attempt green rate, before and after. The exit
   criterion is three full runs in a row green on the first attempt.

## Result

Report, for the suite:

- revision, runs sampled, settings or defaults used, and the parser's check against a real log
  excerpt;
- the flake ranking and the cost ranking;
- the classification table: `file:line` | test | median s | class | reason or target | seconds
  saved, then totals per class;
- what stays in e2e, and why;
- the batches in order, each with its files and estimated saving;
- limits: files, lanes or runs not read, and why.

End with the next step, not an action: the owner picks the first batch, and execution follows the
pruning procedure in its own `test(...)` commits with a fresh Verifier.
