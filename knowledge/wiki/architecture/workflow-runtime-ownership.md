---
type: Requirement
title: Workflow runtime ownership
description: Keep WTK runtime inside its owning skills and preserve project-owned instructions, agent settings, and product context.
generated: { by: codex/gpt-6, at: 2026-09-23T22:39:27Z }
sources:
  - id: consumer-footprint
    resource: ../../raw/2026-09-08-consumer-workflow-footprint.md
    title: Approved consumer workflow footprint correction
    last_modified: 2026-09-08
  - id: product-boundary
    resource: ../../../README.md
    title: Source-pack and consumer ownership boundary
  - id: adoption-provenance
    resource: ../../../scripts/migrate.js
    title: One-time hash-verified legacy adoption cleanup
    last_modified: 2026-09-23
  - id: state-ad-041
    resource: git:8ef07ba74cb1eb3c80e0d1678911d86bad9bd7a7:.specs/STATE.md
    title: STATE.md — AD-041
    last_modified: 2026-09-23
---

# Workflow runtime ownership

The skill installer places the complete WTK skill set; scripts and references needed by later
workflow operations belong with their owning skills. WTK does not copy a separate agent operating
system into the consuming project.[^consumer-footprint][^state-ad-041]

This policy applies to reusable workflow internals. Product context, local configuration, authored
knowledge and approved design references have separate owners. The source pack must preserve that
boundary.[^product-boundary]

A directory name alone never grants deletion authority. The one-time legacy cleanup uses recorded
hashes and leaves modified or unrelated product files safe. New skill installs have no WTK adoption
manifest.[^consumer-footprint][^adoption-provenance][^state-ad-041]

The [Workflow Toolkit contract](/decisions/workflow-toolkit-contract.md) changes the public
namespace, planning artifacts, and execution topology without changing this ownership boundary.
Feature-artifact cleanup remains exact-feature and promotion-based.

[Design reference fidelity](/design/design-reference-fidelity.md) depends on retaining the product's
chosen source and comparison evidence. An approved HTML reference is therefore not equivalent to a
generic installer scaffold merely because both may be called a template.

[^consumer-footprint]: Approved observation and correction in the maintainer conversation.
[^product-boundary]: The README gives consuming projects ownership of their instructions and product context.
[^adoption-provenance]: The legacy migration helper validates recorded hashes before removing old owned files.
[^state-ad-041]: The toolkit installs only skills and leaves project instructions and configuration with their owners.
