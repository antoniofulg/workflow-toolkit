---
type: Decision
title: Fix verification
description: Refactors, fix batches and risk-area changes get a fresh diff-scoped Verifier while a small covered local fix relies on hosted CI, and choosing that agent's model needs no human approval.
tags: [verification, independence, remediation, execution-settings]
status: stable
generated: { by: claude/opus-5.5, at: 2026-11-05T01:46:47Z }
sources:
  - id: proportional-evidence
    resource: ../../raw/2026-11-07-proportional-fix-verification.md
    title: Consuming-project evidence for proportional fix verification
    last_modified: 2026-11-07
  - id: maintainer-decisions
    resource: ../../raw/2026-11-04-fix-verification-and-execution-settings.md
    title: Maintainer decisions on fix verification and execution settings
    last_modified: 2026-11-04
  - id: validation
    resource: ../../../.agents/skills/wtk/references/validation.md
    title: Gates — Fix verification
    last_modified: 2026-11-07
  - id: review-rounds
    resource: ../../../.agents/skills/wtk/references/review-rounds.md
    title: Review Rounds — filed issues and Minor batches
    last_modified: 2026-11-06
  - id: agent-selection
    resource: ../../../.agents/skills/wtk/references/agent-selection.md
    title: Agent selection — dispatch without asking
    last_modified: 2026-11-06
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
| Refactor, batch of fixes, or any change touching security, auth, production/deploy/release, CI/CD, data or migrations | Fresh Verifier over the diff | Verifiers on these changes caught real defects the builder's checks missed[^proportional-evidence][^validation] |
| Small local fix outside those areas, covered by a focused test or hosted CI | Author's focused checks plus hosted CI | Verifiers on such fixes found nothing that CI did not already cover[^proportional-evidence][^validation] |
| Documentation or instruction-only correction | None | There is no behaviour to rerun[^maintainer-decisions] |
| Remediation of a Verifier's findings | One fresh Verifier over the whole remediation range | One Verifier per commit repeated the cost without new findings[^proportional-evidence][^validation] |
| Minor-only batch in a feature run | Fresh Verifier over the batch diff | Without it only the builder's scoped gate closes the batch[^review-rounds] |
| Critical or Major batch in a feature run | Remediation check | That incremental Deep Review already examines the fix[^review-rounds] |

## Trade-offs accepted

- **The 2026-11-04 rule gave every code fix a Verifier.** It answered a fix that passed 18 focused
  repeats and then failed in a wider lane.[^maintainer-decisions] The small-fix exception relies on
  hosted CI for that wider lane; a fix CI does not cover still gets a Verifier.
- **Refactors keep a Verifier regardless of size.** The maintainer chose that wider rule without a
  refactor defect, and the 2026-11-07 proposal kept it.[^maintainer-decisions][^proportional-evidence]
- **Size is the author's call.** A builder classifies its own fix as small; the rule sends an
  unclear class to a Verifier.[^validation]

## Execution settings

A rule that adds a Verifier to many fixes would also add a model question to each. The maintainer
removed the human approval of provider, model and effort instead of adding a timeout or a standing
approval.[^maintainer-decisions][^agent-selection]

This does not touch feature approval: `## Approval` receipts still record the user's decision on
feature shape. [Workflow Toolkit contract](/decisions/workflow-toolkit-contract.md) records the
current settings boundary, and [Deep review cadence](/decisions/deep-review-cadence.md) stays separate
because a Verifier here checks one diff and does not make Deep Review a default stage.

[^proportional-evidence]: Reported Verifier cost and yield, and the proportional rule the maintainer approved.
[^maintainer-decisions]: The original every-fix rule, its reach, and the removal of model approval.
[^validation]: `## Fix verification` owns the Verifier's scope and exceptions.
[^review-rounds]: Owns the filed-issue flow, Minor-only batches and remediation checks.
[^agent-selection]: `## Dispatch without asking` owns selection, human overrides and unsupported settings.
