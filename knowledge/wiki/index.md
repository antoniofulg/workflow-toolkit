---
okf_version: "0.2"
---

# Knowledge Bundle

The project's durable understanding, as an Open Knowledge Format v0.2 bundle. Read
[the operating schema](../AGENTS.md) before creating or updating anything here. Untouched originals
live in `../raw/`, outside the bundle.

Nothing here restates its sources. `README.md`, the WTK skills, and cited Git history stay canonical;
these concepts carry the graph between them and the places where they disagree. When sources conflict,
the owning source wins.

Add a concept when a source earns one.

# Groups

* [Domain](domain/) - Ubiquitous language. One concept per term.
* [Product](product/) - What the product must do.
* [Architecture](architecture/) - How the system is shaped, and the invariants that hold.
* [Design](design/) - Visual and experience guidelines.
* [Decisions](decisions/) - Why a past choice was made.
* [Research](research/) - External material, market, competitors, interviews.
* [Open questions](open-questions/) - Contradictions between sources that no document resolves and no concept owns.

# Concepts

* [Workflow Toolkit contract](decisions/workflow-toolkit-contract.md) - Workflow Toolkit replaces the task pipeline with upstream-shaped Lean and modular routes, sequential whole-slice builds, one full-feature Verifier, and transient feature artifacts.
* [Deep review cadence](decisions/deep-review-cadence.md) - Deep Review runs on demand through `wtk-deep-review` and does not block the default delivery path.
* [QA at feature close](decisions/qa-at-feature-close.md) - Qualifying public changes receive one QA cycle over the integrated feature; no slice runs QA, and one independent Verifier proves the complete feature first.
* [Workflow runtime ownership](architecture/workflow-runtime-ownership.md) - Keep WTK runtime inside its owning skills and preserve project-owned instructions, agent settings, and product context.
* [Security skill integration](architecture/security-skill-integration.md) - WTK keeps baseline security guidance while each project chooses optional lifecycle skills for deeper work.
* [Design reference fidelity](design/design-reference-fidelity.md) - How HTML exports connect visual authority, component reuse, and proportional verification.
* [Interaction efficiency](design/interaction-efficiency.md) - Connect common completion paths, native form semantics, acceptance criteria, and QA evidence.
* [Construction constraints](architecture/construction-constraints.md) - Preserve explicit reuse, construction order, and approval requirements across planning, delegation, verification, and resume.
