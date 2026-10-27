# Construction constraints

**Read when:** planning, dispatching, building or verifying work with an explicit reuse,
construction-order or approval requirement from the user or an approved contract.

## Plan and derive checks

Record each required construction method as an acceptance criterion in the active plan or task,
then map it to a check and named proof. Identify the shared responsibility and permitted extension
points, or the prerequisite, blocked work and release condition. A reversible implementation choice
becomes binding when explicitly required; a `Flow` description or chat summary alone is insufficient.

Distinguish visual consistency from implementation reuse. Require shared code only for the contracted
responsibility. Feature authority lives in the native plan/task, or checks-only intent, as below;
a separately required implementation approval remains a separate prerequisite.

## Native feature approval

At the existing review boundary, record the actual user decision in the receiving turn under
`## Approval` in the owning plan or modular task. When Lean's checks-only escape applies, put it
beside `## Intent` in `checks.md`; create no synthetic plan. Use these literal fields:

```markdown
## Approval

- Decision: <actual user words/decision, not a proposed approval>
- Source: <conversation turn/tool response or durable decision link>
- Date: <observed date, when available>
- Reviewed revision: <snapshot/hash or exact reviewed artifact revision>
- Scope: <authorized work and limits>
```

Replace placeholders only from observed evidence. `Decision`, `Reviewed revision` and `Scope`,
plus `Source` or `Date`, must be usable unfenced data; empty fields and template/example receipts
do not qualify. Cite the actual source whenever available. If the current request already
authorizes bounded checks-only or decided modular work, record that request: do not add a redundant
approval pause. Otherwise use the existing review boundary, not an extra mandatory stop.

Reuse genuine approval on unchanged resume within its scope. Ask targeted acceptance for a new
user-owned product decision outside that scope; reversible detail and additive noncontradictory
discoveries do not require blanket reapproval. Provider/model/effort acceptance in the execution
route does not approve feature shape. Local Markdown is procedural evidence, not authentication:
independent review still judges authenticity and scope. Local edits/commits do not authorize
push, deploy or production mutations. Silence, Git history and passing tests supply no approval.

## Dispatch and build

Before dispatch or the first dependent edit, the coordinator and builder check the native feature
receipt's source, reviewed revision and scope, prerequisite completion and any separately required
implementation approval. Lean's pre-build and completion validators enforce receipt structure;
modular Extract/Build and its independent completion review enforce the same native-task contract.
The assignment cites governing criteria/checks, shared owner and allowed extension points. File
ownership does not authorize recreating a shared implementation. Missing or unusable prerequisites
keep dependent work blocked: return the gap to the coordinator; repair only from real evidence,
and ask only if authority or the contract must change.

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
