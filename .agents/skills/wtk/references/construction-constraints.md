# Construction constraints

**Read when:** planning, dispatching, building or verifying work with an explicit reuse,
construction-order or approval requirement from the user or an approved contract.

## Plan and derive checks

Record each required construction method as an acceptance criterion in the active plan or task,
then map it to a check and named proof. Identify the shared responsibility and permitted extension
points, or the prerequisite, blocked work and release condition. A reversible implementation choice
becomes binding when explicitly required; a `Flow` description or chat summary alone is insufficient.

Distinguish visual consistency from implementation reuse. Require shared code only for the contracted
responsibility, and human approval only where the user or governing contract requires it. Record the
approval's scope and reviewed revision with a reference to the actual human decision. Existing
approval remains valid within that scope; a plan approval, silence or passing tests cannot supply
a separately required implementation approval.

## Dispatch and build

Before dispatch or the first dependent edit, the coordinator and builder check the prerequisite's
completion and required approval evidence. The assignment cites the governing criteria/checks,
shared owner and allowed extension points. File ownership does not authorize recreating a shared
implementation. Missing or unusable prerequisites keep dependent work blocked: return the gap to
the coordinator and repair it within existing authority; ask only if the contract must change.

Implementation order and extraction remain the builder's choice within these constraints. At
phase boundaries, preserve their current state through [context recovery](context-handoff.md).

## Verify

Under every profile, reconcile explicit construction requirements with criteria and checks; an
omitted requirement is a finding even when all listed proofs pass. Trace consumers into the actual
shared implementation and inspect the contracted dependency direction. A shared import with duplicated
behavior, a passing behavior test or a screenshot alone does not prove implementation reuse.

For required sequencing, inspect recorded prerequisite completion and approval before dependent
dispatch or edits. Final code cannot prove historical order. Report missing evidence as unproven;
never infer or backdate approval. Use existing boundary checks and recorded inspection evidence,
with commands and locations, without introducing a new test framework or report schema.
