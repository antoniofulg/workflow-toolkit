---
name: wtk-ship
description: Ship a proven feature through verification, local gates, lifecycle closeout, and authorized branch delivery. Use when asked to ship a proven feature; not unverified work, deploys or releases.
argument-hint: "[the work, in your own words]"
metadata:
  version: '6.0.0'
---

# Workflow Toolkit Ship

Deliver the requested branch using the scope rules in `.agents/skills/wtk/references/validation.md`.

Before delivery closeout or worktree removal, apply
[runtime lifecycle](../wtk/references/runtime-lifecycle.md) and include cleanup/retention evidence
in the normal handoff.

## Previously verified work

Identify the recorded verified base and the subsequent diff. If that diff is bounded maintenance,
use the existing receipt plus its scoped evidence and proceed to delivery; a fix in that diff also
needs its own [fix verification](../wtk/references/validation.md#fix-verification). A merge request does not
trigger a new full-branch Verifier or QA cycle, and needs no extra local full gate; T2 still gates
merge. Closed artifacts may remain in Git; do not
recreate them merely to satisfy this entrypoint. Apply active feature closeout only to unverified
feature work or a substantive change whose named risk requires that scope.

## Active feature closeout

An active Lean feature has `.specs/features/<feature>/plan.md`, `checks.md`, and independent
`verification.md`. The following steps apply to that feature scope.

Resolve or resume the selection through `.agents/skills/wtk-lean/scripts/workflow_route.py`
when a feature snapshot is required. Delegation follows
[agent selection](../wtk/references/agent-selection.md) in the current checkout.

1. Confirm the feature's verification report passes the profile recorded in `checks.md` by running
   `.agents/skills/wtk-lean/scripts/validate_verification.py <feature>`.
2. Apply incremental impact selection from `.agents/skills/wtk/references/validation.md`, including merges from main.
   Run invalidated proofs and reuse valid evidence; a full gate needs that reference's trigger or an
   explicit human request. Run selected `wtk-deep-review`, security, UI and QA procedures only for
   their affected scope.
3. Promote durable decisions, lessons, product promises, architecture rules, and QA evidence to
   their owning stores. Promotion is semantic work; do not invent an automatic knowledge merger.
4. After promotion is complete, delete the entire transient feature directory with
   `python3 .agents/skills/wtk-ship/scripts/close_feature.py <feature> --promoted`. The helper refuses
   cleanup without a passing verification receipt and explicit promotion confirmation.

**Modular closeout.** Modular work carries `.tasks/<name>.md`, `.checks/<feature>.md` and the
Verifier's `.checks/<feature>.verified.md`. Confirm that report's verdict passes with every check
proven, then apply steps 2 and 3 to its scope. Keep or delete those working files under the
project's tracking convention; `close_feature.py` applies only to Lean feature directories.

## Delivery authority

Invoke this skill only when a human asks in this session to ship the work; finishing work never
invokes it. By default, that invocation (or a plain human "ship it" on proven-ready work) authorizes
the feature branch push, one pull request, and merge after readiness is rechecked immediately before
the merge. Do not pause between those scoped delivery steps. Stop at the pull request when told so up
front. The project's declared merge authority, required reviews, branch protection and required
checks win over this default; see [project settings](../wtk/references/project-settings.md). Deploy,
release, production mutations, force-push, direct push to `main`, and unrelated remote actions remain
separately authorized.

**Merge-readiness recheck.** Immediately before the merge, confirm on the merge head:
[T2](../wtk/references/validation.md#test-tiers) (full e2e) green wherever the project runs it (CI
or local), plus the project's required checks. Report the quarantined tests named in the
verification report alongside the result.

If required readiness evidence is missing, name the affected scope and required check. A builder
never certifies its own work; feature verification uses a fresh agent over the complete feature
range, and a fix gets fix verification over its diff. Confirmed Critical, Major,
and realistically triggered Minor Deep Review findings are fixed in the feature run before delivery.
