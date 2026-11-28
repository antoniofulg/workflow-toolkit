---
type: Decision
title: Upstream adoption
description: WTK takes from each upstream only what fits its proof contract — Lean keeps the checks and proofs upstream 3.x removed, Discover copies the upstream validator unchanged, and Deep Review ports single pieces of a diverged fork.
tags: [upstream, lean, discover, deep-review, drift]
status: stable
generated: { by: claude/fable-5.2, at: 2026-11-28T03:30:00Z }
sources:
  - id: adoptions
    resource: ../../raw/2026-11-27-upstream-adoptions-lean-discover-deep-review.md
    title: Maintainer-approved Lean 3.2, Discover 0.10 and Deep Review adoptions
    last_modified: 2026-11-27
  - id: lean-2-2
    resource: ../../raw/2026-11-11-tlc-lean-2-2-adoption.md
    title: Maintainer-approved TLC spec-lean 2.2 adoption
    last_modified: 2026-11-11
  - id: state-ad-035
    resource: git:8ef07ba74cb1eb3c80e0d1678911d86bad9bd7a7:.specs/STATE.md
    title: STATE.md — AD-035
    last_modified: 2026-09-23
  - id: lean-pin
    resource: ../../../.agents/skills/wtk-lean/.skill-meta.json
    title: Lean skill upstream source metadata
    last_modified: 2026-11-28
  - id: lean-notice
    resource: ../../../.agents/skills/wtk-lean/NOTICE.md
    title: Lean attribution and what was adapted from each upstream release
    last_modified: 2026-11-28
  - id: discover-pin
    resource: ../../../.agents/skills/wtk-discover/.skill-meta.json
    title: Discover skill upstream source metadata
    last_modified: 2026-11-28
  - id: validator-test
    resource: ../../../tools/test_discover_design.py
    title: Discover validator tests, including the upstream hash pin
    last_modified: 2026-11-28
  - id: orchestration
    resource: ../../../.agents/skills/wtk-deep-review/references/orchestration.md
    title: Deep Review orchestration — the per-job gate in each prompt
    last_modified: 2026-11-28
---

# Upstream adoption

## One rule, three modes

AD-035 adopted the upstream Lean artifact names and formats so that later upstream changes stay easy
to compare and take.[^state-ad-035] That reason held while upstream grew the proof machinery: the 2.2
adoption took its proof runner and gates whole.[^lean-2-2] It stopped holding on 2026-11-27, when the
maintainer kept what upstream 3.x removed.[^adoptions] Each upstream now has its own mode:

| Local skill | Upstream | Mode | What detects drift |
| --- | --- | --- | --- |
| `wtk-lean` | `tlc-spec-lean` 3.2.0 | Additions only; upstream's removals are refused | The pin and the notice, which names what came from each release.[^lean-pin][^lean-notice] No test compares the local text with upstream |
| `wtk-discover` | `tlc-discover` 0.10.0 | The validator is an unmodified copy; the skill text and document format follow it | A test fails when the validator's SHA-256 differs from the pinned upstream one.[^validator-test][^discover-pin] |
| `wtk-deep-review` | `deep-review` in `pedronauck/skills` | Single pieces, chosen by cost against a diverged fork | Nothing: no pin is recorded, so each comparison is a manual diff.[^adoptions] |

## Why Lean diverges

Upstream 3.x moves trust from scripts to one fresh reviewer with one fix pass, on the claim that
current models do not need step-by-step build instruction. WTK keeps `checks.md`, `proofs.md`, the
validators and the structured Verifier report for three reasons the maintainer accepted:[^adoptions]

1. No WTK usage data shows that the proofs do not pay for themselves, and upstream published no
   measurement for 3.x.
2. WTK builders are often delegated, cheaper models. A remembered rule drops most there, so a script
   gate is worth most there.
3. Upstream keeps `check_commit.py` for the same stated reason: a model holds a rule at high effort
   and drops it at lower effort.

The cost is on the AD-035 side. Every later Lean release must now be read for what it adds, and its
build and review text no longer maps onto the local phases one to one. The maintainer has not
validated this choice beyond the approval; a measured comparison would be the evidence that reopens
it.[^adoptions]

## Why Discover copies and Deep Review picks

The two modes follow from one fact each. The Discover validator accepts only upstream's section set,
so keeping it unmodified forced the whole format to follow; the adoption therefore went beyond the
four approved items, and a design in the old section set is refused.[^adoptions] The local Deep
Review already had a per-job filter and status file, so carrying the gate in each prompt was cheap,
while the rest of the upstream rework was about 500 lines against a diverged fork with no published
measurement.[^adoptions][^orchestration] The saving of the adopted piece is itself unmeasured.

## Tension recorded here

- **Approval scope.** Both adoption plans were written after the maintainer approved the
  recommendation lists and were not presented before the build. The
  [Workflow Toolkit contract](/decisions/workflow-toolkit-contract.md) gates the approval receipt on
  presence only, and each Verifier judged that the receipt covered the list, not the plan.[^adoptions]
- **Coordinator choices.** The `request.md` presence gate and the default trailer rejection were not
  on the approved list; upstream has neither as a validator rule.[^adoptions]

[Deep review cadence](/decisions/deep-review-cadence.md) is unaffected: the adopted piece changes
what a reviewer does inside a run, not when a run happens.

[^adoptions]: Upstream state compared, decisions 1 to 6 and the open approval point.
[^lean-2-2]: The 2.2 adoption that took upstream's proof runner and gates.
[^state-ad-035]: Upstream Lean artifact names and formats are the local contract, to minimize drift.
[^lean-pin]: Source, commit and content hash of the Lean upstream.
[^lean-notice]: What was adapted from 2.2.0 and from 3.2.0, and what WTK keeps.
[^discover-pin]: Source, commit and content hash of the Discover upstream.
[^validator-test]: `test_validator_is_upstream_byte_for_byte`.
[^orchestration]: Each materialized prompt carries the gate scoped to its job; the stage gate stays the coordinator's.
