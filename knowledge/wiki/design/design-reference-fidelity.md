---
type: Concept
title: Design reference fidelity
description: How HTML exports connect visual authority, component reuse, and proportional verification.
sources:
  - id: design-html-export
    resource: ../../raw/2026-09-07-design-html-export.md
    title: Design tool HTML exports — maintainer observation
    last_modified: 2026-09-07
  - id: ui-contract
    resource: ../../../.agents/skills/wtk/references/ui-ux.md
    title: UI/UX Surface Map
    last_modified: 2026-09-23
  - id: frontend-ownership
    resource: ../../../.agents/skills/wtk/references/frontend.md
    title: Front-End Engineering
  - id: scoped-validation
    resource: ../../../.agents/skills/wtk/references/validation.md
    title: Gates
---

# Design reference fidelity

The maintainer's design tools export HTML. This observation supports an executable-reference path;
it does not establish that every export includes CSS, fonts, assets, responsive rules, or the
design tool's original semantic tokens.[^design-html-export]

The connection between these sources is a division of authority: the approved reference defines
the visual result, the consuming project defines component ownership, and the gate classifier
defines the scope of verification. A faithful port can adapt markup to existing components while
retaining the contracted appearance; identical DOM structure is not the product promise.
[^ui-contract][^frontend-ownership]

A small correction and a full feature can therefore share the same visual reference without
sharing the same delivery process. Skipping feature artifacts does not remove the need to compare
the changed visual result; adding a comparison does not itself justify a full QA cycle.
[^ui-contract][^scoped-validation]

[^design-html-export]: Design tool HTML exports — approved conversation record.
[^ui-contract]: UI/UX Surface Map — operative visual-reference contract.
[^frontend-ownership]: Front-End Engineering — consuming-project component and shell ownership.
[^scoped-validation]: Gates — proportional validation and direct corrections.
