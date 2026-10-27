# Context recovery and handoff

**Read when:** checkpointing a WTK phase boundary, resuming, recovering after compaction, facing
context pressure, or transferring ownership to a fresh session.

## Checkpoint before context is lost

Record user answers, approval/delegation, scope changes and settled clarifications in the existing
owning contract/decision fields or Handoff **in the receiving turn**, before dependent action.
Phase/batch-end checkpoints supplement these live writes; they do not postpone them. Update the
handoff before an action would depend mainly on conversational memory. Reliable host telemetry
may trigger an early checkpoint; never estimate a context percentage or require a fresh session.

Use the active route's artifacts:

| Route | Contract and current state |
| --- | --- |
| Lean | `.specs/features/<feature>/plan.md` when present and `checks.md`, including its existing `Handoff` |
| Modular | `.tasks/<name>.md` and `.checks/<feature>.md`, including its existing `Handoff` |
| Before a checklist exists, or project-level resume | Existing `.specs/STATE.md` `Handoff`, pointing to the active source/plan/design |

Preserve the artifact's native fields. In its existing handoff, record phase, criterion/check status
and evidence references, binding architecture/construction constraints, pending approvals and their
scope, blocked work and release conditions, checkout/branch/HEAD and uncommitted work, authorization
limits, and one next action. Include runtime identifiers only when active; delegated state follows below.
Reference canonical criteria and approval records instead of copying the spec. A project-level
handoff points to feature state; update only its section, preserving decisions and unrelated work.

## Record dispatch and reconcile ownership

The coordinator records each assignment in the existing Handoff **before send**: phase/stage,
scope/check set, checked revision, accepted execution selection and status `pending dispatch`.
This is intent, not proof of a live worker. Immediately after successful send, record the actual
returned host identifier and observed status. Record a failed send as `send failed`, with the
error and whether the host proves no assignment was created; never invent a host identifier.

Before waiting, sending, consuming or replacing work on recovery, query available host
status/reports and reconcile them with this record:

| Evidence | Next authorized action |
| --- | --- |
| Pending intent; host confirms no assignment/send occurred | Send the recorded assignment once, then record its real identifier |
| Successful send with actual host identity, confirmed live | Retain ownership and wait using that identity |
| Send failed; host confirms no worker exists | Record failure, then retry within accepted settings |
| Returned report | Record returned status/report and checked revision before consuming it |
| Definitively terminated/cannot return | Record terminal evidence and release ownership before replacement |
| Missing/unavailable host status or uncertain send/ownership | Record `ownership unverifiable`; block duplicate dispatch and resolve via host reports/operator evidence |

An unproven pending intent cannot justify waiting as though a worker exists; equally it cannot
justify redispatch while a send may have succeeded. Preserve accepted choices on retries/resume.
The coordinator dispatches the final independent Verifier; builders report and stop. This is
artifact bookkeeping, not a new scheduler or dispatch service.

## Recover before continuing

After compaction or on resume, the current agent:

1. Reloads applicable instructions and the active contract/checks, cited decisions and handoff.
2. Reconciles branch, HEAD, working diff and check status with recorded evidence. Git establishes
   code state, not human approval. Mark stale or unsupported claims instead of inventing history.
3. Preserves the active feature's frozen route using the project-owned
   `../../wtk-lean/scripts/workflow_route.py` resume path and revalidates the accepted choices through
   [agent selection](agent-selection.md); unchanged rows need no repeated confirmation.
   Reconcile pending/live/returned dispatches against host status/reports as above before choosing
   any wait, send, consume or replace action.
4. States the recovered objective, binding constraints, unresolved approvals, blocked work and next
   authorized action, with artifact references. Continue when that action's prerequisites are proven;
   this statement is not a request to repeat existing approval.

If objectives or constraints cannot be reconstructed, stop dependent work, identify the missing source
and resolve the gap. A fresh session cannot repair a missing contract. Successful recovery allows
the current session to continue; compaction and phase boundaries do not mandate replacement.

## Transfer only when needed

Use an actual transfer when recovery is insufficient for continued execution, a concrete context
limit prevents continuing, or the user/host requires a fresh session. Preserve the role's existing
handoff boundaries: builders finish whole slices with green batch proofs for a normal transfer.
If that boundary cannot be reached, checkpoint the incomplete state and report a blocker without
claiming a completed batch or dispatching dependent work.

The coordinator uses the host's supported handoff mechanism and the accepted stage settings in
the current checkout;
this protocol does not authorize builders to spawn agents or select a different provider. Freeze
outgoing edits and dispatch before transfer, retaining ownership only to finish the handoff.
The successor runs the recovery steps, explicitly accepts ownership and starts its turn before
the outgoing planner retires. Record that acknowledgement in the existing handoff.

If transfer fails or no supported mechanism exists, preserve the checkpoint and report the exact
resume action. Keep work paused until ownership is resolved; never leave two planners dispatching
the same work or claim a successor started without evidence.
