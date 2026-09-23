---
type: Concept
title: Security skill integration
description: WTK keeps baseline security guidance while each project chooses optional lifecycle skills for deeper work.
generated: { by: codex/gpt-6, at: 2026-09-23T22:39:27Z }
sources:
  - id: maintainer-observation
    resource: ../../raw/2026-09-13-security-skill-integration.md
    title: Maintainer observation and proposed security skill replacement
    last_modified: 2026-09-13
  - id: security-workflow
    resource: ../../../.agents/skills/wtk/references/security.md
    title: Security phases and installed guidance
  - id: skills-only-decision
    resource: ../../../.specs/STATE.md
    title: STATE.md — AD-041
    last_modified: 2026-09-23
  - id: security-distribution
    resource: ../../../README.md
    title: External security skills and consumer installation contract
---

# Security skill integration

The maintainer observed that the security layer referenced skills absent from
the local project. A written security phase therefore did not establish that its
guidance was available to the executing agent.[^maintainer-observation][^security-workflow]

Local availability and consumer delivery are separate boundaries. WTK distributes its baseline
security reference with the full WTK skill set; the consuming project chooses whether to install
specialized Security Lifecycle skills separately.[^skills-only-decision][^security-distribution]

The discussed direction replaces `security-best-practices` with
`security-implementation` and separates specification, threat modeling,
implementation and review. Comparative quality remains unvalidated; the
replacement direction is not evidence of equal security outcomes or completed
integration.[^maintainer-observation]

The security reference names the optional `security-spec`, `security-threat-model`,
`security-implementation`, and `security-review` skills at their matching phases. When they are
absent, WTK uses its baseline surface and proof rules and reports the unavailable specialized
guidance. This does not measure comparative quality or prove a consumer installed or ran a
companion skill.[^security-workflow][^skills-only-decision]

[Workflow runtime ownership](/architecture/workflow-runtime-ownership.md) explains why WTK's
baseline guidance and consumer-selected companions have different owners.

[^maintainer-observation]: Authorized conversation record, including the unresolved comparison question.
[^security-workflow]: Security guidance is loaded before coding and connected to requirements, threat modeling and review.
[^skills-only-decision]: AD-041 makes Security Lifecycle an optional companion rather than bundled WTK content.
[^security-distribution]: README links the optional upstream source and states that WTK does not install it.
