---
type: Decision
title: Workflow Toolkit contract
description: Workflow Toolkit replaces the task pipeline with upstream-shaped Lean and modular routes, sequential whole-slice builds, one full-feature Verifier, and transient feature artifacts.
tags: [workflow-toolkit, lean, verification, lifecycle]
status: stable
generated: { by: codex/gpt-6, at: 2026-09-23T22:39:27Z }
sources:
  - id: maintainer-contract
    resource: ../../raw/2026-09-12-workflow-toolkit-contract.md
    title: Maintainer decisions for the Workflow Toolkit replacement
    last_modified: 2026-09-12
  - id: state-ad-035
    resource: ../../../.specs/STATE.md
    title: STATE.md — AD-035
    last_modified: 2026-09-23
  - id: state-ad-036
    resource: ../../../.specs/STATE.md
    title: STATE.md — AD-036
    last_modified: 2026-09-23
  - id: state-ad-037
    resource: ../../../.specs/STATE.md
    title: STATE.md — AD-037
    last_modified: 2026-09-23
  - id: state-ad-041
    resource: ../../../.specs/STATE.md
    title: STATE.md — AD-041
    last_modified: 2026-09-23
  - id: state-ad-042
    resource: ../../../.specs/STATE.md
    title: STATE.md — AD-042
    last_modified: 2026-09-23
  - id: toolkit-router
    resource: ../../../.agents/skills/wtk/SKILL.md
    title: Workflow Toolkit route contract
    last_modified: 2026-09-23
  - id: artifact-lifecycle
    resource: ../../../.agents/skills/wtk/references/artifacts.md
    title: Artifact Lifecycle
    last_modified: 2026-09-13
  - id: upstream-pin
    resource: ../../../.agents/skills/wtk-lean/.skill-meta.json
    title: Lean skill upstream source metadata
    last_modified: 2026-09-23
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
| Public identity | Twelve `wtk` and `wtk-*` skills installed as one set through a skill installer | Ponytail and security lifecycle stay optional external skills.[^state-ad-041][^state-ad-042] |
| Planning shapes | Integrated Lean owns `plan.md`, `checks.md`, and `verification.md`; direct modular discovery/planning retains `.design/`, `.tasks/`, and `.checks/` | Each upstream shape remains recognizable instead of passing through a local compatibility schema.[^toolkit-router][^state-ad-035] |
| Build and proof | `Feature -> Slice -> Check`; builders run sequentially, hand off only between whole observable slices, and make coherent commits before one fresh independent Verifier covers the complete feature | Builder decomposition stays flexible while slice integrity, author/verifier independence, and complete-feature proof stay fixed.[^state-ad-036] |
| Profiles and capabilities | Lean profiles are `light`, `standard`, and `ui`, with `standard` as default; security, UI, QA, review, and delivery load when their owning trigger applies | Conditional dispatch is not permission to skip a mandatory check. Deep Review runs on demand.[^state-ad-036][^state-ad-042] |
| Agent settings | Each project owns native provider, model, and effort metadata; WTK's feature snapshot records provider and role identity only | WTK does not write project agent files or require a TOML configuration.[^state-ad-042] |
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
  Workflow Toolkit renames the capability but preserves `skip` as the default.
- [QA at feature close](/decisions/qa-at-feature-close.md) still prohibits per-slice QA. Workflow
  Toolkit changes technical proof to one full-feature independent Verifier; qualifying public
  changes still receive one feature-level QA cycle.
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
[^upstream-pin]: The Lean skill records its upstream source, revision, content hash, and license in `.skill-meta.json`.
