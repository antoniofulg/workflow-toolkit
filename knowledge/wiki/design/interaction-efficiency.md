---
type: Design Guideline
title: Interaction efficiency
description: Connect common completion paths, native form semantics, acceptance criteria, and QA evidence.
sources:
  - id: interaction-efficiency-report
    resource: ../../raw/2026-09-09-interaction-efficiency.md
    title: Interaction efficiency — maintainer report and decision
    last_modified: 2026-09-09
  - id: ui-contract
    resource: ../../../.agents/skills/wtk/references/ui-ux.md
    title: UI/UX Surface Map
  - id: test-contract
    resource: ../../../.agents/skills/wtk/references/test-contract.md
    title: Test Contract
  - id: qa-scenarios
    resource: ../../../.agents/skills/wtk-qa/references/qa-scenarios.md
    title: QA Scenarios
---

# Interaction efficiency

A maintainer reported that a tag-creation flow with a color selector, name input, and Create button
did not submit when Enter was pressed in the name field. The report led to a UI contract rule for
tracing intent-to-completion paths and using native form submission for plain single-line fields.
[^interaction-efficiency-report][^ui-contract]

The UI contract owns the interaction expectation: it identifies completion, recovery, and repeated-entry
behavior. Acceptance criteria should name the observable path, and tests should derive exact
input-condition-result cases from those criteria.[^ui-contract][^test-contract] QA scenarios retain the
user-visible promise and its current verdict.[^qa-scenarios]

The [design reference fidelity](design-reference-fidelity.md) concept supplies the visual authority and
component ownership side of the UI contract; this concept supplies completion behavior, so both belong
in the surface contract.

[^interaction-efficiency-report]: Interaction efficiency — approved conversation record.
[^ui-contract]: UI/UX Surface Map — interaction and surface contract.
[^test-contract]: Test Contract — acceptance-derived test cases.
[^qa-scenarios]: QA Scenarios — user-visible promise tracking.
