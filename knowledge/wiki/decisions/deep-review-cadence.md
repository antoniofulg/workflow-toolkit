---
type: Decision
title: Deep review cadence
description: Deep Review runs on demand through `wtk-deep-review` and does not block the default delivery path.
tags: [deep-review, cadence, cost, delivery-speed]
status: stable
generated: { by: codex/gpt-6, at: 2026-09-23T22:36:59Z }
sources:
  - id: delivery-cost
    resource: ../../raw/2026-09-10-deep-review-delivery-cost.md
    title: Maintainer observation and same-day benchmark (morning)
    last_modified: 2026-09-10
  - id: skip-review
    resource: ../../raw/2026-09-10-feature-close-qa-and-skip-review.md
    title: Maintainer decision on delivery speed and PR #98 (evening)
    last_modified: 2026-09-10
  - id: review-rounds
    resource: ../../../.agents/skills/wtk/references/review-rounds.md
    title: Review Rounds — stages, remediation check, severity
    last_modified: 2026-09-23
  - id: state-ad-031
    resource: ../../../.specs/STATE.md
    title: STATE.md — AD-031
  - id: state-ad-034
    resource: ../../../.specs/STATE.md
    title: STATE.md — AD-034
    last_modified: 2026-09-23
  - id: state-ad-036
    resource: ../../../.specs/STATE.md
    title: STATE.md — AD-036
    last_modified: 2026-09-23
  - id: state-ad-042
    resource: ../../../.specs/STATE.md
    title: STATE.md — AD-042
    last_modified: 2026-09-23
---

# Deep review cadence

## Two decisions on one day

| When | Question | Decision |
| --- | --- | --- |
| 2026-09-10 morning | Should deep review run once every N features to cut its cost? | No. Keep it per feature; cut cost per review (one discovery round, remediation checks, no polish lane).[^delivery-cost][^state-ad-031] |
| 2026-09-10 evening | Should deep review gate the merge at all while the product is pre-launch? | No. `cadence = "skip"` resolves no groups; merge does not wait. The human runs the then-current `wreview` later over several features, with autonomous remediation.[^skip-review] |

The two are not the same question. The morning kept the **per-review** cost levers; the evening
removed deep review from the **merge path**. Both hold: when deep review runs, it runs as AD-031
shaped it; whether it runs before merge is a cadence choice the product phase owns.

## Current Workflow Toolkit effect

AD-036 replaces the old capability name with `wtk-deep-review` and removes the task-granular,
parallel slice pipeline. AD-042 removes WTK configuration and keeps Deep Review on demand, so no
review group blocks feature delivery unless the operator invokes the skill.[^state-ad-034][^state-ad-036][^state-ad-042]

Resolved review groups organize review scope; they do not make the sequential builder parallel.
The name `wreview` below belongs to the 2026-09-10 record, while `wtk-deep-review` is the current
entrypoint.[^state-ad-036]

## The lever table

| Lever | Owner | Status |
| --- | --- | --- |
| One discovery review, then one-job remediation checks until clean | `review-rounds.md` rule 2; AD-031 | decided[^review-rounds][^state-ad-031] |
| No automatic groups; invoke `wtk-deep-review` when needed | WTK route; AD-034 and AD-042 | current default[^state-ad-034][^state-ad-042] |
| Skip deep review for `Small` features by tier | `.agents/skills/wtk/references/validation.md` classifier | open; `skip` makes it moot for the current phase |

## What the morning arguments still say

Batching raises cost per finding, returns findings out of context, and lets defects tests miss ship
for a cycle.[^delivery-cost] The evening decision accepts all three for a pre-launch product with few
users, where a bug in `main` has no measurable cost and constancy of delivery does.[^skip-review]
The trade-off is the maintainer's, stated, and reversible by explicitly invoking Deep Review when
the phase changes.

## Related

[QA at feature close](/decisions/qa-at-feature-close.md) was decided in the same session and removed
per-slice QA. Workflow Toolkit later replaced per-slice Technical Verification with one independent
full-feature Verifier, reducing the mandatory proof topology again without making qualifying QA
optional.[^skip-review][^state-ad-036]

[^delivery-cost]: Maintainer statement and the three-build benchmark table in the morning observation.
[^skip-review]: Session count, the maintainer's risk statement, and the two merged commits in the evening observation.
[^review-rounds]: Stage table and rule 2 (remediation check); the `skip` clause before final QA.
[^state-ad-031]: One discovery round plus remediation checks; polish lane removed; round cap deleted.
[^state-ad-034]: Deep Review defaults to on demand.
[^state-ad-036]: Workflow Toolkit names the current capability `wtk-deep-review` and uses sequential whole-slice builders.
[^state-ad-042]: Project-owned agent settings; Deep Review remains on demand without WTK TOML.
