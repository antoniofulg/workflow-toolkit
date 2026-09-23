---
type: Concept
title: Construction constraints
description: Preserve explicit reuse, construction order, and approval requirements across planning, delegation, verification, and resume.
sources:
  - id: incident
    resource: ../../raw/2026-09-16-construction-constraints-incident.md
    title: Maintainer-supplied construction constraints retrospective
    last_modified: 2026-09-16
  - id: build
    resource: ../../../.agents/skills/wtk-lean/references/build.md
    title: Build — fixed checks, implementation discretion, and context recovery
  - id: test-contract
    resource: ../../../.agents/skills/wtk/references/test-contract.md
    title: Test Contract — derive claims and audit coverage before build
  - id: evidence
    resource: ../../../.agents/skills/wtk/references/evidence.md
    title: Verification Evidence — scope binds
  - id: frontend
    resource: ../../../.agents/skills/wtk/references/frontend.md
    title: Front-End Engineering — composition and ownership
  - id: memory
    resource: ../../../.agents/skills/wtk/references/context-handoff.md
    title: Context recovery and handoff — referenced constraints and lifecycle
---

# Construction constraints

A feature can behave correctly and look correct while violating the requested method of
construction. The reported incident connects three failures: an explicit reuse and sequencing
instruction did not become a blocking criterion, delegation encouraged an independent implementation,
and verification could not distinguish that implementation from the required shared one.
The retrospective says the instruction survived compaction; context loss is a risk, not an
established root cause of this incident. This is a reported failure, not an independent code audit.
[^incident]

## Where the contracts connect

Build grants discretion over order, decomposition and extraction, and treats `Flow` as a map rather
than an obligation. The test contract makes criteria the source of fixed checks. Together these
create a critical boundary: an explicitly required construction method belongs in criteria and
checks, even when the same choice would ordinarily be a reversible implementation detail. Leaving
it only in `Flow` or a conversation exposes it to legitimate-looking implementation discretion.
[^build][^test-contract][^incident]

The following prevention pattern is derived from that incident and the existing contracts. It is
not a new artifact schema or a claim that an automated gate already enforces these constraints.

| Explicit requirement | Durable home | Evidence that distinguishes compliance |
| --- | --- | --- |
| Reuse implementation A in consumer B | `plan.md` criterion naming the shared responsibility; corresponding `checks.md` obligation | Trace both consumers into the actual shared implementation; a common import that leaves duplicate behavior in each consumer is insufficient |
| Finish prerequisite A before dependent work B | Criterion defining the blocked work and release condition; current state in the existing Handoff | Recorded prerequisite completion before B's dispatch or first dependent edit |
| Obtain human approval of A before B | Criterion naming the approval scope; approval reference and reviewed revision in the existing artifact | Actual human approval of that scope and revision; tests, silence and approval of the plan do not substitute |
| Keep shared code independent of consumer policy | Architectural criterion with the allowed dependency direction | Inspect shared dependencies and consumer adapters, plus the owning boundary check when available |

These proofs cover different properties. Behavior tests do not establish source reuse; screenshots
do not establish module ownership; final code does not establish historical execution order.
Acceptance-derived checks and scope-bound evidence must cover each requested property separately.
[^test-contract][^evidence]

## Carry the constraint through execution

1. Before build approval, reconcile explicit human constraints against criteria and named proofs.
   Include required construction methods and forbidden alternatives, not just observable behavior.
2. Before dispatching dependent work, resolve its prerequisite and approval evidence. Give the
   implementer the relevant criterion/check references, shared owner and permitted extension points.
   File ownership must not authorize a parallel implementation of the shared responsibility.
3. If the prerequisite implementation is missing or unusable, keep dependent work blocked and
   return the gap to the coordinator. Repair the prerequisite within existing authority; request
   a decision only when the approved contract must change. Do not silently build a substitute.
4. At verification, inspect the actual composition and required sequence as well as behavior and
   appearance. Missing approval history is an unproven obligation, not permission to infer approval.
5. At handoff or resume, reload the relevant criteria, checks, diff and current prerequisite state
   before choosing the next work. Keep a compact pointer to blocked work, its release condition,
   approval evidence and governing constraint in the existing Handoff; avoid a second spec.

This pattern connects shared-component ownership to evidence and recovery: frontend composition
prevents duplication only when delegation preserves its owner, while recovery helps only when it
reloads the binding obligation rather than a summary of the intended appearance.
[^frontend][^evidence][^build][^memory][^incident]

## Boundaries

Apply a human approval gate only when required by the user or governing contract; do not add one
to every slice. Reuse the contracted responsibility, not every part of two similar features.
Use existing composition mechanisms before inventing adapters or slot frameworks. If the user
asked only for visual consistency, that alone does not require identical implementation.
The incident's component list and product sequence are examples, not universal architecture.
[^incident][^frontend]

[Design reference fidelity](/design/design-reference-fidelity.md) separates visual authority from
code ownership. This concept adds the connection to construction order and explicit approval:
appearance can be satisfied independently while the construction contract remains violated.

[^incident]: Supplied retrospective — reported instruction, planning failure and verification gap.
[^build]: Build — What is fixed and what is not; Running out of context.
[^test-contract]: Test Contract — Rules; Choosing the layer.
[^evidence]: Verification Evidence — Scope binds; Stop and hand it back.
[^frontend]: Front-End Engineering — Feature folders vs shared UI; Component script.
[^memory]: Context recovery and handoff — checkpoint and transfer.
