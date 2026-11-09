# Test Contract

**Read when:** writing, planning, or reviewing tests, or deriving feature checks.

**Why this exists:** "All branches covered" cannot be audited. Named cases with claims and proofs can.
A test that mirrors the implementation, or exists only to raise coverage, proves nothing.

## The artifact

Every integrated Lean feature has `.specs/features/<feature>/checks.md`. The native
[Lean checks reference](../../wtk-lean/references/checks.md) is the only schema and
authoring source for that artifact: read it for `Profile`, check and proof syntax, `Coverage`,
`Test policy`, `Swept`, and `Handoff`. This guideline supplies local test-case policy below; it does
not define a second checks schema.

The native profile owns mutation depth: `standard` and `ui` inject faults; `light` does not.
[Mutation](#mutation) sets their scope and survivor policy.

## Rules

1. **Derive, do not invent.** Every case maps to a spec acceptance criterion. Use components, error
   paths, boundaries, and journeys to find coverage gaps; if one reveals behavior absent from the
   spec, clarify the acceptance criterion before adding a case. Never create a case solely because a
   component or boundary exists. Security cases also follow `security.md` when its
   condition fires.
2. **Every claim names an exact input, condition, concrete value, and expected result.** "Test the
   happy path" is not a claim. "Creating an order with an unknown region is rejected as
   invalid and stores nothing" is, whether the interface is a `POST` route, a CLI verb exiting
   non-zero, or an event that lands on the dead-letter topic. Name one or more exact tests or commands whose exit codes settle it; repeat `Proof:` when
   a proof cannot settle the whole claim.
3. **Coverage is explicit.** Every enumerated set gets a `Coverage` row with each member as its own
   token beside the check or proof that asserts it. Shared or table-driven proofs may be reused when
   each named claim or member is independently asserted; reuse never replaces the explicit join.
4. **Audit before the build is approved.** Every claim and coverage member maps to at least one check
   with named proof(s); no claim or member is left orphaned.
5. **Tests ship with the slice that closes the behaviour.** Never a test-only slice.
6. **A case is not done because a test exists.** It is done when the test asserts the contracted
   expected result. A test that exists without asserting the contracted behaviour is a hollow case and
   fails review.

## Choosing the layer

**Each failure has a canonical owner at the cheapest discriminating layer.**

| Layer | Use for | Cost |
| --- | --- | --- |
| Unit | Domain rules, validation, pure transformation, every error path | Cheapest |
| Integration | Anything crossing a boundary: repository, HTTP handler, queue | Moderate |
| End-to-end | A complete user journey through the real stack | Most expensive — deliberately scarce |

Another layer earns a test only for a distinct failure, such as persistence, serialization,
authorization wiring, or browser interaction. Keep real end-to-end journeys. A browser test asserts
what the user perceives: visible state, focus, navigation and the message shown. Assert data effects
(rows written, refused or unchanged) and input/error matrices at their lower-layer owner; never
replay them through the browser.

**Lowest layer that proves it.** Do not write an end-to-end test for a behaviour a unit or
integration test can prove. End-to-end is reserved for what lower layers cannot reach: real browser
or runtime wiring across processes, a user journey crossing several services, and the `@smoke`
cohort. Plan and Checks state that reason whenever they choose end-to-end as a proof layer.

Before replacing or removing an existing end-to-end test on this ground, prove the coverage: map
every assertion in it to a unit or integration test asserting the same outcome through the same
contract, and confirm with a scoped [mutation](#mutation) run, or manual faults, that the lower
tests kill the mutants the end-to-end test killed. An assertion with no lower-layer proof keeps the
end-to-end test, or gets its lower test first. Never remove the only proof of cross-component wiring.

Use the real collaborator when it is fast and deterministic in the test, such as an in-process
value, a local database or a filesystem in a temporary directory. Fake one only when it is slow,
nondeterministic, costs money or has external side effects, and fake it at a port the code owns, not
inside a library. A fake proves nothing about the real collaborator. Between separately deployed
services, a consumer-driven contract test pins what the consumer reads, and the provider's suite
replays it.

Permanent e2e tests carry a feature and a journey marker in the runner's own mechanism (a tag,
category, trait or label, such as `@feature:<slug>` and `@journey:<slug>`), unique data with
guaranteed cleanup, and residue-zero assertions. The feature marker is the selector the consuming
project's scoped e2e gate uses to run only that feature's scenarios. [Test tiers](validation.md#test-tiers)
own which cohort runs when.

## Never add a test just to raise coverage

Before adding a test, search existing unit, integration, and end-to-end suites. Name the invariant,
its canonical suite and layer, and the concrete regression that existing proofs cannot catch.
Record that justification in the existing check, task notes, or PR. Extend the owner; reuse its
proof when no new failure is distinguished. Reviewers reject additions without this justification.

When consolidating cases, follow [pruning](#pruning). Similar test names or shared setup alone do
not establish equivalent coverage.

Forbidden by default — allowed only when that artifact is the product contract and no stronger gate
already owns it:

- Tests asserting prose, copy or documentation content
- Snapshot tests standing in for behavioural assertions
- Tests over generated files, config shape, or CSS
- A second suite duplicating an existing one because the existing one was hard to find

For instruction products, assert routing, metadata, resolvable references and safety boundaries;
do not freeze line wrapping, incidental wording or historical release prose. Compare release
identities to the authoritative manifest. Review semantic instruction changes directly: a matching
string alone does not prove agent behavior.

## Mutation

[Fault injection](verify-core.md#fault-injection-standard-ui) owns the isolated procedure.

- **Declared tool.** When the project declares a mutation command, run it scoped to the changed
  decision code only: the files or line ranges of the diff against the base, in incremental mode
  when the tool supports it. Examples only: StrykerJS or Stryker.NET (`--since`), PIT for Java
  (`scmMutationCoverage`, `targetClasses`), Mull or dextool for C++, mutmut for Python,
  cargo-mutants for Rust.
- **No declared tool.** Inject manual faults as that procedure states.
- **Survivors.** There is no global score target, and this pack sets no number. Every survivor on
  a changed decision line is a finding: kill it with a test, or record it as equivalent or arid with
  a one-line reason. A project may declare its own break threshold, scoped to changed files.

## Pruning

Removing a redundant test is its own reviewed change, never part of a fix or a red gate.

1. Scope one module, feature or page.
2. List its tests per layer and map each to the claim or invariant it proves.
3. Find candidates:
   - (a) a higher-layer test whose assertions the lower-layer owner all covers, proven under the
     [lowest-layer rule](#choosing-the-layer); never a `@smoke` cohort member or the sole proof of
     a journey or of wiring;
   - (b) a test that kills no mutant, or only mutants another test also kills, found by a
     [mutation](#mutation) tool run over the scope that reports every killing test (no bail).
     Propose at most one removal per equal-kill set, keeping its lowest-layer member. Without a
     mutation tool, class (b) is not proposed;
   - (c) a test over a forbidden subject: copy, snapshots, config or CSS, or whose only effect is
     producing artifacts no assertion or gate reads;
   - (d) a duplicate suite.
4. For each candidate, map every unique assertion to the proof that is kept.
5. Delete in its own `test(...)` commit, never inside a fix.
6. Re-run mutation over the scope, or without a tool the manual faults the removed test used to
   kill. The kill set must not shrink; a new survivor reverts that deletion.
7. A fresh Verifier checks the mapping.
8. Never prune a member of the permanent security smoke suite; any other SEC proof needs a named
   lower-layer replacement.

## Test execution cost

- Test harness orchestration with small isolated fixtures. Target injected failures to their fixture;
  leave full application builds and catalogs to their canonical gates unless the test proves a
  distinct product integration. Keep scratch outputs and caches separate from the checkout's.
- Combine assertions sharing the same scenario when their failure conditions remain distinguishable.
  Reuse immutable fixture preparation; keep mutable state and cleanup isolated per case. Each test
  owns its browser context and data and scopes fixture queries to its own tenant, so a retry is safe.
- A single test over about 60 s, or a serial group, needs a stated reason; otherwise split it so it shards.
- When changing CI lanes or selectors, verify that their union covers the required cases without
  duplicate execution in the same runtime. A full suite already includes its smoke subset. Distinct
  runtime matrices and bounded reliability probes need an explicit purpose for repetition. One
  viewport proves a behaviour; a second needs a layout-specific claim with different assertions.
- Measure affected-suite time before and after adding expensive setup or recurring execution; record
  timings and why a cheaper proof is insufficient beside the coverage justification.

## Visual acceptance evidence

**Paired captures prove what a screen looks like; e2e proves what it does.** Arrangement, order,
count and copy are proven by the paired visual captures the Verifier compares, and a mismatch blocks
completion. Give each screen exactly one structural e2e assertion as a guard. Otherwise e2e asserts
behaviour, and copy only when copy is the contract.

When a visual acceptance criterion names an approved reference, attach paired-capture evidence to the
owning check or slice and point to its feature `uiux.md` row when present. Follow the method in
`ui-ux.md#verifying-the-built-screen`, which owns how captures are produced, and record its output
fields. A manual paired comparison is evidence, not an automated test, and never replaces behavioral
cases. A gate test never writes a screenshot or artifact it does not assert on. Add automated
screenshot regression only when an actual visual invariant has an owning canonical suite.
