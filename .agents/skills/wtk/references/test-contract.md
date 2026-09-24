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

The native profile owns mutation depth: `standard` and `ui` inject faults; `light` does not. Do not
infer a local mutation threshold from this guideline.

## Rules

1. **Derive, do not invent.** Every case maps to a spec acceptance criterion. Use components, error
   paths, boundaries, and journeys to find coverage gaps; if one reveals behavior absent from the
   spec, clarify the acceptance criterion before adding a case. Never create a case solely because a
   component or boundary exists. Security cases also follow `security.md` when its
   condition fires.
2. **Every claim names an exact input, condition, concrete value, and expected result.** "Test the
   happy path" is not a claim. "`POST` the create route with an unknown region returns 422 and no
   row" is. Name one or more exact tests or commands whose exit codes settle it; repeat `Proof:` when
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
authorization wiring, or browser interaction. Keep real end-to-end journeys; leave input/error
matrices to their lower-layer owner instead of replaying them through the browser.

Permanent e2e specs carry `@feature:<slug>` and `@journey:<slug>` tags, unique data with `finally`
cleanup, and residue-zero assertions. The `@feature:<slug>` tag is the selector the consuming
project's browser scoped gate uses to run only that feature's scenarios.

## Never add a test just to raise coverage

Before adding a test, search existing unit, integration, and end-to-end suites. Name the invariant,
its canonical suite and layer, and the concrete regression that existing proofs cannot catch.
Record that justification in the existing check, task notes, or PR. Extend the owner; reuse its
proof when no new failure is distinguished. Reviewers reject additions without this justification.

When consolidating cases, map every unique assertion to its retained proof before removing the
duplicate. Similar test names or shared setup alone do not establish equivalent coverage.

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

## Test execution cost

- Test harness orchestration with small isolated fixtures. Target injected failures to their fixture;
  leave full application builds and catalogs to their canonical gates unless the test proves a
  distinct product integration. Keep scratch outputs and caches separate from the checkout's.
- Combine assertions sharing the same scenario when their failure conditions remain distinguishable.
  Reuse immutable fixture preparation; keep mutable state and cleanup isolated per case.
- When changing CI lanes or selectors, verify that their union covers the required cases without
  duplicate execution in the same runtime. A full suite already includes its smoke subset. Distinct
  runtime matrices and bounded reliability probes need an explicit purpose for repetition.
- Measure affected-suite time before and after adding expensive setup or recurring execution; record
  timings and why a cheaper proof is insufficient beside the coverage justification.

## Visual acceptance evidence

When a visual acceptance criterion names an approved reference, attach paired-capture evidence to the
owning check or slice and point to its feature `uiux.md` row when present. Follow the method in
`ui-ux.md#verifying-the-built-screen` and record its output fields. A manual paired
comparison is evidence, not an automated test, and never replaces behavioral cases. Add automated
screenshot regression only when an actual visual invariant has an owning canonical suite.
