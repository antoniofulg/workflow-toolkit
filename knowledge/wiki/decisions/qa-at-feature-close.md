---
type: Decision
title: QA at feature close
description: Qualifying public changes receive one QA cycle over the integrated feature; no slice runs QA, and one independent Verifier proves the complete feature first.
tags: [qa, cadence, delivery-speed, verifier]
status: stable
generated: { by: codex/gpt-5, at: 2026-09-13T02:16:58Z }
sources:
  - id: skip-review
    resource: ../../raw/2026-09-10-feature-close-qa-and-skip-review.md
    title: Maintainer decision on delivery speed and PR #98
    last_modified: 2026-09-10
  - id: review-rounds
    resource: ../../../.agents/skills/wtk/references/review-rounds.md
    title: Review Rounds — stage table
    last_modified: 2026-09-23
  - id: qa-execution
    resource: ../../../.agents/skills/wtk-qa-execute/references/qa-execution.md
    title: QA Execution — when QA runs
    last_modified: 2026-09-23
  - id: state-ad-002
    resource: ../../../.specs/STATE.md
    title: STATE.md — AD-002
  - id: state-ad-036
    resource: ../../../.specs/STATE.md
    title: STATE.md — AD-036
    last_modified: 2026-09-23
---

# QA at feature close

## What the maintainer asked for, and what the pack did

| | Requested | Shipped until 2026-09-10 |
| --- | --- | --- |
| When | Once, when the feature is complete | After every public slice, and again at feature close |
| What | Every flow, as a real user | Per-slice `qa-plan` + `qa-execute`, then the closing session |
| Sessions, 3 slices | 2 | 8 |

Per-slice QA came from the initial extraction (`eddecdbe`) and was doubled by AD-002, which chose
fresh Verifier sessions for QA without deciding whether QA should run per slice.[^skip-review][^state-ad-002]
The maintainer named it a misinterpretation; PR #98 removed it.[^skip-review]

## What the 2026-09-10 correction still controls

- A qualifying public change receives one `wtk-qa-plan` and one `wtk-qa-execute` cycle over the
  integrated tree. No slice runs QA.[^review-rounds][^qa-execution]
- AD-002 still holds for that session: QA skills stay provider-neutral and run in fresh Verifier
  sessions.[^state-ad-002]
- QA is conditional, not universally optional: its owning surface trigger decides whether it runs.
  UI, API, CLI, adoption, and other changed public promises qualify; an internal or narrower
  correction can close at its proportional technical proof.[^qa-execution]

## What Workflow Toolkit supersedes

The 2026-09-10 decision kept a Technical Verifier per code-changing slice. AD-036 later replaces
that task-era topology with one fresh independent Verifier over the complete feature. This changes
technical proof cadence, not the prohibition on per-slice QA and not the feature-level QA trigger
for qualifying public changes.[^skip-review][^state-ad-036]

## What is given up

A UI defect in an early slice may now survive until full-feature verification or the feature QA
cycle. That later detection is the deliberate cost of sequential whole-slice building with one
independent full-feature Verifier.[^state-ad-036]

## Related

[Deep review cadence](/decisions/deep-review-cadence.md): the same session moved deep review off the
merge path with `cadence = "skip"`. The two decisions together are what makes delivery constant.

[^skip-review]: Origin trace, session count and the maintainer's statements in the raw observation.
[^review-rounds]: Stage table after PR #98: Technical Verifier, deep-review, QA session.
[^qa-execution]: QA dispatched once, at feature close.
[^state-ad-002]: QA planning and execution as separate provider-neutral skills in fresh Verifier sessions.
[^state-ad-036]: Workflow Toolkit replaces per-slice Technical Verification with one fresh independent Verifier over the complete feature.
