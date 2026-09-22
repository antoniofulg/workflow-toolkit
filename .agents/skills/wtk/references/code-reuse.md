# Code reuse and ownership

**Read when:** planning, implementing, refactoring, or reviewing code in any layer.

## Find the owner before adding code

Search the repository for the responsibility being changed, including differently named
implementations and their consumers. Inspect the relevant behavior and project contracts; names,
matching syntax, and a shared import alone do not establish reuse.

Reuse the canonical implementation when its contract fits. Extend its existing composition or
variation mechanism when needed. Before adding a separate implementation, record the nearest
existing owner, the concrete requirement it cannot satisfy, and why extension would couple
different responsibilities or violate a boundary. Keep that decision in the existing plan's
`Flow`, task notes, or PR; no separate inventory or report is required. If no owner exists, place
the new responsibility at the narrowest appropriate boundary.

Apply this policy to application code, services, scripts, adapters, configuration logic, and
shared infrastructure. Search the relevant repository scope, including other packages, without
turning each edit into a whole-codebase audit.

## Preserve the right boundaries

Share code that owns the same contract and should change for the same reason. Preserve deliberate
differences between domains, runtime constraints, and independently deployed services. Similar
syntax alone is not a reason to extract a common abstraction. Keep validation and authorization
at every trust boundary that requires them; centralizing a rule does not remove enforcement.

For frontend work, follow [component organization](../../../../docs/toolkit/guidelines/FRONTEND.md#component-script)
and the consuming project's design system. Trace repeated UI patterns to their components,
tokens, styles, and supported variants. Page-local overrides must express a required difference;
an override that recreates the shared treatment defeats reuse. Check corresponding states and
viewports across affected pages; a shared import does not establish visual consistency.

For backend work, trace callers through domain rules, policies, transformations, services, and
data access. Keep each shared decision with its owning module; use adapters for transport or
persistence differences. Apply [modeling guidance](../../../../docs/toolkit/guidelines/MODELING.md)
when its boundary or domain-type trigger applies.

## Change and verify

When consolidating implementations, identify affected consumers and preserve their required
behavior, state, errors, accessibility, and boundary enforcement. Map unique test assertions to
retained proofs under [the test contract](test-contract.md); select affected validation through
[the existing gate policy](validation.md). Remove obsolete implementations once consumers move.

Review changed responsibilities against existing owners with
[wtk-reuse-review](../../wtk-reuse-review/SKILL.md) during the existing verification pass. Keep
unrelated legacy duplication outside the change as follow-up findings. Whole-codebase audits
require that scope to be requested explicitly. Explicit reuse, sequencing, and approval
requirements additionally follow [construction constraints](construction-constraints.md).
