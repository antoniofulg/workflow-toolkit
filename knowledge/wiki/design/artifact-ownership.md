---
type: Research Note
title: Artifact ownership
description: Separate durable decisions from transient feature proof, and route PRD, RFC, and ADR work without duplicating discovery.
status: draft
sources:
  - id: assessment
    resource: ../../raw/2026-10-21-artifact-ownership-assessment.md
    title: Artifact ownership assessment and recording approval
    last_modified: 2026-10-21
  - id: upstream-origin
    resource: ../../../.agents/skills/wtk-lean/.skill-meta.json
    title: Lean upstream source metadata
  - id: memory
    resource: ../../../.agents/skills/wtk-lean/references/memory.md
    title: Lean memory — existing decision-store ownership
    last_modified: 2026-09-23
  - id: plan
    resource: ../../../.agents/skills/wtk-lean/references/plan.md
    title: Lean planning — active decisions and unresolved choices
    last_modified: 2026-10-20
  - id: lifecycle
    resource: ../../../.agents/skills/wtk/references/artifacts.md
    title: Artifact lifecycle — promotion before feature cleanup
    last_modified: 2026-09-13
  - id: discovery
    resource: ../../../.agents/skills/wtk-discover/SKILL.md
    title: WTK discovery — product framing and technical shape
    last_modified: 2026-09-23
  - id: tlc-prd
    resource: https://github.com/tech-leads-club/agent-skills/blob/main/packages/skills-catalog/skills/%28development%29/tlc-prd/SKILL.md
    title: TLC PRD
  - id: tlc-adr
    resource: https://github.com/tech-leads-club/agent-skills/blob/main/packages/skills-catalog/skills/%28creation%29/create-adr/SKILL.md
    title: TLC ADR creator
  - id: tlc-rfc
    resource: https://github.com/tech-leads-club/agent-skills/blob/main/packages/skills-catalog/skills/%28creation%29/create-rfc/SKILL.md
    title: TLC RFC creator
  - id: adr-templates
    resource: https://adr.github.io/adr-templates/
    title: ADR templates — Nygard, MADR, and Y-statements
  - id: aws-adr
    resource: https://docs.aws.amazon.com/prescriptive-guidance/latest/architectural-decision-records/best-practices.html
    title: AWS ADR best practices
---

# Artifact ownership

This assessment connects upstream artifact creation to WTK's project ownership and cleanup rules.
Recording was approved in conversation. The integration below remains a recommendation; this note
does not change installed skill behavior or establish a new decision store.[^assessment]

## Inherited shape and local lifecycle

WTK's Lean source metadata identifies TLC as its upstream. The
[Workflow Toolkit contract](/decisions/workflow-toolkit-contract.md) connects AD-035's preservation
of upstream artifact names, AD-036's adapted execution model, and AD-037's transient-feature policy.
Together they distinguish the inherited artifact shape from WTK's decision to remove completed
feature directories after verification and durable promotion.[^upstream-origin][^lifecycle]

In consuming projects, `.specs/features/<feature>/` holds the plan, proof obligations, and verification
state. `.specs/STATE.md` is the default shared decision log and handoff location. Neither implies
that an architectural decision must originate inside a feature directory. A choice constraining
future features is recorded when made, and an existing project ADR store takes precedence over
starting another log.[^memory][^lifecycle]

## The ownership inconsistency

The memory guide explicitly accepts an existing ADR store. Planning still directs agents to read
and supersede decisions in `.specs/STATE.md`, while lifecycle promotion explicitly targets that
same file. Following those instructions literally could split decisions between two stores.
The proposed correction is to make reading, recording, supersession, and promotion follow the
same project-owned decision store.[^memory][^plan][^lifecycle][^assessment]

This relates to [Workflow runtime ownership](/architecture/workflow-runtime-ownership.md): WTK
can define how a phase consumes project decisions without taking ownership of project documentation.

## Conditional artifact routing

The recommended integration assigns each artifact a distinct question. It does not require every
feature to create every document.[^assessment]

| Artifact | Trigger | Relationship to WTK |
| --- | --- | --- |
| PRD | Business problem, intended outcome, boundary, or user journey needs agreement | Feed product decisions into discovery or Lean planning; do not repeat a settled interview |
| RFC | A consequential proposal needs alternatives compared and stakeholder agreement | Resolve the disputed direction before treating it as an accepted constraint |
| ADR | A significant architectural choice is made or being finalized | Preserve context, rationale, consequences, status, and supersession beyond feature cleanup |
| Technical design document | A separate system design review is justified | Keep optional because discovery and Lean planning already cover technical shape |

TLC's PRD deliberately stops before technical design. Its RFC creator drives proposal review;
its ADR creator records a decision and its consequences. WTK discovery spans product framing and
technical shape, so PRD support needs a handoff boundary rather than another mandatory product
interview.[^tlc-prd][^tlc-rfc][^tlc-adr][^discovery]

For example, a billing initiative could use a PRD to establish customer needs, an RFC to compare
providers, and an ADR to preserve the chosen provider's rationale. Its individual features would
then use Lean planning and checks. An understood feature or bounded correction would skip artifacts
whose questions are already settled.[^assessment]

## Proposed integration boundary

1. Reuse the project's decision convention. For a new convention, propose `docs/adr/` and
   `docs/rfcs/`; keep durable records outside transient feature directories.
2. Initially document TLC's artifact creators as optional companions. Add conditional routing
   and shared ownership guidance before creating more WTK authoring skills.
3. Carry links to accepted decisions through planning, checks, verification, and promotion.
   Keep one authoritative rationale rather than copying it into multiple durable stores.
4. Consume an existing PRD as product input; use discovery for unresolved shape questions.
5. Add a README table covering each artifact's purpose, trigger, owner, location, and retention.
   Preserve the project's English artifact policy when invoking companions that follow the
   conversation language.[^assessment]

Short Nygard-style records and fuller MADR records are established template choices, not evidence
that one document sequence suits every team. AWS guidance supports accessible centralized records
and preserved supersession history. These sources support durable ownership and traceability;
they do not establish a universal folder name or require a PRD/RFC/ADR chain for every change.
[^adr-templates][^aws-adr]

[^assessment]: Conversation excerpts — assessment and approval to record it.
[^upstream-origin]: WTK Lean source metadata.
[^memory]: Lean memory — decision timing and existing-store precedence.
[^plan]: Lean planning — explicit reads and supersession in STATE.md.
[^lifecycle]: Artifact lifecycle — decision promotion and feature cleanup.
[^discovery]: WTK discovery — product questions, technical shape, and RFC/spike boundaries.
[^tlc-prd]: TLC PRD — product scope and the boundary before technical design.
[^tlc-adr]: TLC ADR creator — decision rationale, consequences, and supersession.
[^tlc-rfc]: TLC RFC creator — proposal comparison and stakeholder agreement.
[^adr-templates]: ADR GitHub organization — supported template families.
[^aws-adr]: AWS Prescriptive Guidance — ownership, central access, and preserved history.
