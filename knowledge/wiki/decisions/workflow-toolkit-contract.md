---
type: Decision
title: Workflow Toolkit contract
description: Workflow Toolkit replaces the task pipeline with upstream-shaped Lean and modular routes, sequential whole-slice builds, one full-feature Verifier over a shared verify core, and transient feature artifacts.
tags: [workflow-toolkit, lean, verification, lifecycle]
status: stable
generated: { by: claude/sonnet-5.5, at: 2026-11-11T21:00:00Z }
sources:
  - id: maintainer-contract
    resource: ../../raw/2026-09-12-workflow-toolkit-contract.md
    title: Maintainer decisions for the Workflow Toolkit replacement
    last_modified: 2026-09-12
  - id: state-ad-035
    resource: git:8ef07ba74cb1eb3c80e0d1678911d86bad9bd7a7:.specs/STATE.md
    title: STATE.md — AD-035
    last_modified: 2026-09-23
  - id: state-ad-036
    resource: git:8ef07ba74cb1eb3c80e0d1678911d86bad9bd7a7:.specs/STATE.md
    title: STATE.md — AD-036
    last_modified: 2026-09-23
  - id: state-ad-037
    resource: git:8ef07ba74cb1eb3c80e0d1678911d86bad9bd7a7:.specs/STATE.md
    title: STATE.md — AD-037
    last_modified: 2026-09-23
  - id: state-ad-041
    resource: git:8ef07ba74cb1eb3c80e0d1678911d86bad9bd7a7:.specs/STATE.md
    title: STATE.md — AD-041
    last_modified: 2026-09-23
  - id: state-ad-042
    resource: git:8ef07ba74cb1eb3c80e0d1678911d86bad9bd7a7:.specs/STATE.md
    title: STATE.md — AD-042
    last_modified: 2026-09-23
  - id: toolkit-router
    resource: ../../../.agents/skills/wtk/SKILL.md
    title: Workflow Toolkit route contract
    last_modified: 2026-11-07
  - id: artifact-lifecycle
    resource: ../../../.agents/skills/wtk/references/artifacts.md
    title: Artifact Lifecycle
    last_modified: 2026-11-06
  - id: maintainer-settings
    resource: ../../raw/2026-11-04-fix-verification-and-execution-settings.md
    title: Maintainer decision removing model approval
    last_modified: 2026-11-04
  - id: role-models
    resource: ../../raw/2026-11-07-role-owned-models.md
    title: Maintainer decision moving model and effort to agent roles
    last_modified: 2026-11-07
  - id: upstream-pin
    resource: ../../../.agents/skills/wtk-lean/.skill-meta.json
    title: Lean skill upstream source metadata
    last_modified: 2026-11-11
  - id: lean-2-2
    resource: ../../raw/2026-11-11-tlc-lean-2-2-adoption.md
    title: Maintainer-approved TLC spec-lean 2.2 adoption
    last_modified: 2026-11-11
  - id: generalization
    resource: ../../raw/2026-11-06-skill-pack-generalization.md
    title: Maintainer-approved skill-pack generalization
    last_modified: 2026-11-06
  - id: verify-core
    resource: ../../../.agents/skills/wtk/references/verify-core.md
    title: Verify Core — obligations both verify routes share
    last_modified: 2026-11-11
  - id: dx
    resource: ../../../.agents/skills/wtk/references/dx.md
    title: Public surface contract
    last_modified: 2026-11-06
---

# Workflow Toolkit contract

## Replacement and current boundaries

AD-036 originally chose the public identity and execution topology. AD-035 constrains that replacement to
upstream artifact names and formats rather than a local translation. AD-037 then defines when those
artifacts stop being useful and may be removed.[^state-ad-035][^state-ad-036][^state-ad-037]

Together they remove the reason to preserve the former task pipeline: compatibility readers would
reintroduce local schema drift, and permanent feature archives would turn a temporary coordination
contract into a second product description. The append-only AD ledger preserves why the old paths
existed; current runtime and documentation do not preserve those paths.[^state-ad-036][^state-ad-037]

## Current boundary

| Concern | Current contract | Boundary it protects |
| --- | --- | --- |
| Public identity | The full `wtk` and `wtk-*` skill set installed as one set through a skill installer | Ponytail and security lifecycle stay optional external skills.[^state-ad-041][^state-ad-042] |
| Planning shapes | Integrated Lean owns `plan.md`, `checks.md`, and `verification.md`; direct modular discovery/planning retains `.design/`, `.tasks/`, and `.checks/` | Each upstream shape remains recognizable instead of passing through a local compatibility schema.[^toolkit-router][^state-ad-035] |
| Build and proof | `Feature -> Slice -> Check`; builders run sequentially, hand off only between whole observable slices, and make coherent commits before one fresh independent Verifier covers the complete feature | Builder decomposition stays flexible while slice integrity, author/verifier independence, and complete-feature proof stay fixed.[^state-ad-036] |
| Shared verification | Lean and modular verify procedures link one verify core for approval, evidence or zero, visual evidence, the swept re-read and scratch-worktree fault injection, which Lean scopes to `Risk:` checks and `unsure` rows; each keeps its route-specific steps | The two routes cannot drift on the obligations they share, and survivors outside risk do not grow the suite.[^verify-core][^generalization][^lean-2-2] |
| Approval | `## Approval` is gated on presence: `validate_checks.py` refuses a missing receipt or an empty `Decision`, and the Verifier still judges who approved which revision | A compaction loses the chat that held the approval, so the receipt must survive on disk; markdown still cannot authenticate authority, so judgment of it stays with the independent Verifier. This reverses the 2026-11-06 convention-only decision.[^generalization][^lean-2-2] |
| Public surfaces | Both planning routes load `wtk/references/dx.md` when a public surface changes; compatibility and language follow the project's declared policy | One contract serves Lean and modular planning.[^dx][^generalization] |
| Profiles and capabilities | Lean profiles are `light`, `standard`, and `ui`, with `standard` as default; security, UI, QA, review, and delivery load when their owning trigger applies | Conditional dispatch is not permission to skip a mandatory check. Deep Review runs on demand.[^state-ad-036][^state-ad-042] |
| Agent settings | The coordinator picks each stage's role from the user's routing table and states it without human approval; model and effort come from the role's agent file, a role the human names wins, and the feature snapshot records each role with its resolved settings | WTK does not write agent files, copy the routing table or choose a model.[^state-ad-042][^role-models] Feature approval stays separate.[^maintainer-settings] |
| Lifecycle | Keep an exact feature directory through independent verification, selected gates, and required promotion; then delete that directory | Foreign pending work, unrequested legacy-plan adaptation, decisions, tests, product docs, QA evidence, and knowledge are outside cleanup.[^artifact-lifecycle][^state-ad-037] |

The Lean source metadata remains part of the drift boundary, not merely attribution: local
adaptations can be compared with the recorded upstream source while preserving distinct integrated
and modular contracts.[^upstream-pin][^maintainer-contract]

## Supersession graph

- AD-036 supersedes the coordinator, parallel-slice, phase-skill, and old package decisions named in
  its ledger entry. Sequential execution therefore describes the current topology; old parallel
  records remain historical evidence, not alternate live modes.[^state-ad-036]
- AD-037 supersedes AD-007's permanent feature-state retention. Cleanup promotes durable facts to
  their owning stores first and never uses age or a broad directory sweep as authority.[^state-ad-037]
- AD-041 replaces the package installer with a complete skill-installer set, and AD-042 removes
  WTK-owned configuration and packet generation.[^state-ad-041][^state-ad-042]
- [Deep review cadence](/decisions/deep-review-cadence.md) remains a separate reversible cost choice:
  Deep Review stays on demand, and route snapshots no longer record the constant cadence field.
- [QA at feature close](/decisions/qa-at-feature-close.md) still prohibits per-slice QA. Workflow
  Toolkit changes technical proof to one full-feature independent Verifier; qualifying public
  changes still receive one feature-level QA cycle.
- [Fix verification](/decisions/fix-verification.md) adds a diff-scoped Verifier outside the
  full-feature pass and removes the human approval of execution settings.
- [Workflow runtime ownership](/architecture/workflow-runtime-ownership.md) survives the
  replacement: namespace and artifact changes do not transfer product-owned content to the pack or
  broaden installer deletion authority.

[^maintainer-contract]: Maintainer-approved original namespace, profile, conditional-capability, verifier, and cleanup boundaries.
[^state-ad-035]: Upstream Lean artifact names and formats are the local contract.
[^state-ad-036]: Workflow Toolkit replaces the task pipeline and fixes the public identity, execution topology, profiles, and retained integrations.
[^state-ad-037]: Feature planning and verification artifacts are transient after proof and promotion; unrelated pending work is preserved.
[^toolkit-router]: `wtk` routes integrated Lean and the distinct modular entries without compatibility aliases.
[^state-ad-041]: The consuming project owns its instructions and setup; WTK ships as skills.
[^state-ad-042]: Native agent metadata owns model and effort; WTK records route identity only.
[^artifact-lifecycle]: Durable facts move to their owning stores before exact-feature cleanup.
[^maintainer-settings]: The maintainer removed human approval of provider, model and effort on 2026-11-04.
[^role-models]: Model and effort belong to agent roles; WTK dispatches by role and records the result.
[^upstream-pin]: The Lean skill records its upstream source, revision, content hash, and license in `.skill-meta.json`.
[^generalization]: Decisions 5, 7 and 8: approval judged by the Verifier, `dx.md` location, shared verify core.
[^verify-core]: The shared obligations and the links from both verify procedures.
[^lean-2-2]: Decisions 1 and 6 of the 2026-11-11 adoption: the presence-gated approval and risk-scoped faults.
[^dx]: Public surface contract and its project-owned compatibility and language policy.
