---
name: wtk-test-review
description: Review the tests of one module, feature or page with scoped mutation and propose removals and missing tests. Use when asked to review, audit or slim a scope's tests; not deleting tests, writing features or whole-repository certification.
license: CC-BY-4.0
metadata:
  author: Antonio Fulgêncio
  version: '6.4.0'
---

# Test review

Review the tests of one scope - "review the tests of the billing page" - and report which tests
earn their place, which are redundant, and which behaviour has no proof. **Propose only.** Never
delete, skip or weaken a test here; a removal is a separate change under
[pruning](../wtk/references/test-contract.md#pruning), and the owner decides.

## Settings

Read the project's `tiers`, `mutation` and `test-review scopes`
[settings](../wtk/references/project-settings.md):

- the mutation command and how it scopes to files or line ranges;
- the [test tiers](../wtk/references/validation.md#test-tiers) and their commands;
- scope paths, such as where a page or module's code and tests live;
- any break threshold the project declares for changed files.

Without settings, use the stack-neutral defaults: the stack's own test commands, scope paths found
by tracing the code, manual faults under
[fault injection](../wtk/references/verify-core.md#fault-injection-standard-ui) in place of a
mutation tool, and no numeric threshold. Name every default you took in the report. Install nothing.

## Review

1. **Scope.** Resolve the named module, feature or page to its source files and its tests at every
   layer. If the scope cannot be resolved, ask for it; do not widen to the repository. A suite-wide
   [test audit](../wtk-test-audit/SKILL.md) may hand over the scope with title-based classes;
   this review confirms or overturns them from the assertions.
2. **Inventory.** List each test per layer (unit, component, integration, e2e) with the claim or
   invariant it proves, using the [test contract](../wtk/references/test-contract.md). A test with no claim is a finding. Record
   each e2e test's median duration and retry-pass count from recent CI where available, and review
   in order of cost × flakiness.
3. **Mutate.** Run the [mutation](../wtk/references/test-contract.md#mutation) step over the scope's
   decision code in a scratch worktree, never the real tree, reporting every killing test per
   mutant (no bail). Without a tool, run the manual faults and say how far they reach.
4. **Classify.** Sort tests into the pruning candidate classes and report each against its
   evidence:
   - **killing** - kills at least one mutant no other test kills;
   - **redundant** - kills no mutant, or only mutants another test also kills; propose at most one
     removal per equal-kill set, keeping its lowest-layer member, and none without a mutation tool;
   - **e2e replaceable by component** - every assertion is a UI state under the
     [lowest-layer rule](../wtk/references/test-contract.md#choosing-the-layer), each mapped to
     the component test that asserts it with the server stubbed, or marked as having none;
   - **e2e replaceable by lower layer** - under the same rule, with each e2e assertion mapped to
     the unit or integration test that asserts the same outcome through the same contract, or
     marked as having none; never a `@smoke` cohort member or the sole proof of a journey or of
     wiring;
   - **forbidden subject** - copy, snapshots, config or style, unless that artifact is the contract;
     in a mixed test, propose dropping only those assertions;
   - **unstable** - passes and fails on the same unchanged revision, handled under
     [unstable tests](../wtk/references/test-contract.md#unstable-tests);
   - **artifact-only** - its only effect is producing artifacts no assertion or gate reads; a
     removal candidate without a mutation run, since it kills nothing by construction;
   - **duplicate suite**.
5. **Gaps.** Report each surviving mutant on decision code and each claim with no proof as a
   missing test, naming the layer that should own it.

A member of the permanent security smoke suite is never proposed for removal; any other SEC proof
needs a named lower-layer replacement. A mapping that leaves an assertion with no kept proof keeps
the test.

## Result

Report, for the scope:

- scope, revision, settings or defaults used, and the mutation or fault command with its result;
- the classified test table: test, layer, claim, mutants killed, class, evidence;
- proposed removals, each with its assertion -> kept-proof mapping;
- proposed missing tests, each with the survivor or unproven claim it closes;
- limits: code, layers or mutants not reached, and why.

End with the next step, not an action: the owner chooses which proposals to apply, and an applied
removal follows the pruning procedure in its own `test(...)` commit with a fresh Verifier.
