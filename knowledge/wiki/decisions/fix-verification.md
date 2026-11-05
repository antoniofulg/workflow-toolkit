---
type: Decision
title: Fix verification
description: Every fix, correction or refactor of executable code gets a fresh diff-scoped Verifier, and choosing that agent's model needs no human approval.
tags: [verification, independence, remediation, execution-settings]
status: stable
generated: { by: claude/opus-5.5, at: 2026-11-05T01:46:47Z }
sources:
  - id: maintainer-decisions
    resource: ../../raw/2026-11-04-fix-verification-and-execution-settings.md
    title: Maintainer decisions on fix verification and execution settings
    last_modified: 2026-11-04
  - id: validation
    resource: ../../../.agents/skills/wtk/references/validation.md
    title: Gates — Fix verification
    last_modified: 2026-11-04
  - id: review-rounds
    resource: ../../../.agents/skills/wtk/references/review-rounds.md
    title: Review Rounds — filed issues and Minor batches
    last_modified: 2026-11-04
  - id: agent-selection
    resource: ../../../.agents/skills/wtk/references/agent-selection.md
    title: Agent selection — dispatch without asking
    last_modified: 2026-11-04
---

# Fix verification

## What it reversed

The filed-issue path skipped a Verifier because the defect had already been reviewed. That reasoning
conflated two subjects: the review examined the defect, and nobody had examined the fix.[^review-rounds]
Reported failures from a consuming project supplied the evidence, including a fix whose own test
passed 18 focused repeats and then failed in a wider lane.[^maintainer-decisions]

## Where the line sits

| Change | Independent check | Why |
| --- | --- | --- |
| Fix, correction or refactor of code or tests, or a mixed change | Fresh Verifier over the diff | The builder's own label cannot decide whether its change preserved behaviour[^validation][^maintainer-decisions] |
| Documentation or instruction-only correction | None | There is no behaviour to rerun[^maintainer-decisions] |
| Minor-only batch in a feature run | Fresh Verifier over the batch diff | Without it only the builder's scoped gate closes the batch[^review-rounds]; the batch can also land after the feature's Verifier pass (the agent's inference) |
| Critical or Major batch in a feature run | Remediation check | That incremental Deep Review already examines the fix[^review-rounds] |

## Trade-offs accepted

- **Refactors go beyond the observed failures.** The evidence covers behaviour-changing fixes only, and
  the agent recommended exempting pure refactors. The maintainer chose the wider rule, so this is a
  judgement rather than a response to a refactor defect. Reversing it needs no new evidence about
  fixes.[^maintainer-decisions]
- **Every code fix now costs an agent run.** The maintainer met the model question on a fix Verifier and
  removed it. The source records no stated reason, so linking the two decisions by cost is the agent's
  inference.[^maintainer-decisions]

## Execution settings

A rule that adds a Verifier to every fix would also add a model question to every fix. The maintainer
removed the human approval of provider, model and effort instead of adding a timeout or a standing
approval.[^maintainer-decisions][^agent-selection]

This does not touch feature approval: `## Approval` receipts still record the user's decision on
feature shape. [Workflow Toolkit contract](/decisions/workflow-toolkit-contract.md) records the
current settings boundary, and [Deep review cadence](/decisions/deep-review-cadence.md) stays separate
because a Verifier here checks one diff and does not make Deep Review a default stage.

[^maintainer-decisions]: The maintainer's rule, its reach, and the removal of model approval.
[^validation]: `## Fix verification` owns the Verifier's scope and exceptions.
[^review-rounds]: Owns the filed-issue flow, Minor-only batches and remediation checks.
[^agent-selection]: `## Dispatch without asking` owns selection, human overrides and unsupported settings.
