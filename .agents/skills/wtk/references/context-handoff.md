# Context recovery and handoff

**Read when:** checkpointing a WTK phase boundary, resuming, recovering after compaction, facing
context pressure, or transferring ownership to a fresh session.

## Checkpoint before context is lost

Update the existing handoff at phase boundaries and before the next action would depend mainly on
conversational memory. If reliable host telemetry exists, 80% context use may trigger an early
checkpoint; never estimate a percentage or make it a universal stop threshold. A checkpoint does
not require a fresh session or new approval.

Use the active route's artifacts:

| Route | Contract and current state |
| --- | --- |
| Lean | `.specs/features/<feature>/plan.md` when present and `checks.md`, including its existing `Handoff` |
| Modular | `.tasks/<name>.md` and `.checks/<feature>.md`, including its existing `Handoff` |
| Before a checklist exists, or project-level resume | Existing `.specs/STATE.md` `Handoff`, pointing to the active source/plan/design |

Preserve the artifact's native fields. In its existing handoff, record phase, criterion/check status
and evidence references, binding architecture/construction constraints, pending approvals and their
scope, blocked work and release conditions, checkout/branch/HEAD and uncommitted work, authorization
limits, and one next action. Include runtime and delegated-agent identifiers/status only when active.
Reference canonical criteria and approval records instead of copying the spec. A project-level
handoff points to feature state; update only its section, preserving decisions and unrelated work.

## Recover before continuing

After compaction or on resume, the current agent:

1. Reloads applicable instructions and the active contract/checks, cited decisions and handoff.
2. Reconciles branch, HEAD, working diff and check status with recorded evidence. Git establishes
   code state, not human approval. Mark stale or unsupported claims instead of inventing history.
3. Preserves the active feature's frozen route using [configuration resume](../../wtk-config/SKILL.md#resume);
   a changed `.wtk.toml` does not silently replace it.
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

The coordinator uses the host's supported handoff mechanism and the configured role/provider;
this protocol does not authorize builders to spawn agents or select a different provider. Freeze
outgoing edits and dispatch before transfer, retaining ownership only to finish the handoff.
The successor runs the recovery steps, explicitly accepts ownership and starts its turn before
the outgoing planner retires. Record that acknowledgement in the existing handoff.

If transfer fails or no supported mechanism exists, preserve the checkpoint and report the exact
resume action. Keep work paused until ownership is resolved; never leave two planners dispatching
the same work or claim a successor started without evidence.
