# Project Harness Setup

> Plan from this document. Each slice carries the decisions and observable outcomes it owns.
> Status: confirmed by Antonio, 2026-10-20 — proceed with one fresh criteria reviewer; guideline location follows the consuming project's convention.

## Situation

- Project: WTK is distributed and in active use in consuming projects.
- Decision: Antonio committed to shaping a general WTK setup/review capability with a small proposed baseline, an interview about driver skills, on-demand guidelines, and stronger planning and verification.
- In flight: Plaaay supplies phase/surface skill routing and requirement-to-proof examples; Arquimedium supplies role/task routing, architectural gates and security requirements.
- Outside this change: the consuming applications are read-only research inputs; their conflicting or stale instructions are evidence, not authorized remediation.
- At stake: an incorrect project rule can affect every later feature, while excessive context can hide the rules agents need.

## Problem

Feature planners can omit project expectations that are already documented or covered by installed skills. Builders and verifiers then satisfy an incomplete feature contract. Antonio reports repeated unnecessary frontend text, incomplete loading states, omitted transitions and inconsistent use of existing styles; security and other engineering concerns can fail through the same omission.

The current substitute is repeated user correction and manually assembled project instructions. Two read-only repository explorations found both useful routing and conflicting guidance. The frequency and cost of missed requirements have not been measured; source inspection does not establish current runtime correctness.

## Success

- Worked if: setup produces a small, usable project contract; a later planner accounts for its applicable requirements; independent checking detects both omissions and implementations that violate them.
- Going wrong: all guidelines load for every task, observed conventions become binding without a decision, missing skills become unexplained blockers, or verification checks only the criteria the planner remembered.
- Review: Antonio reviews this design after the two approved explorers check its criteria against their source findings. Implementation planning follows that review.

## Boundary

In: new-project setup, existing-harness assessment and authorized updates, skill discovery and selection, conditional context routing, project requirement inheritance, criteria review and independent implementation verification.

Out: application refactors, whole-codebase security certification, automatic skill installation, a new WTK CLI executable, runtime provisioning and deployment. These are separate operations with their own scope and authority.

Unchanged: the public `Feature -> Slice -> Check` hierarchy, the project's ownership of tools and delivery authority, and the separation between builder and fresh Verifier.

## Prior art

- Plaaay already separates root instructions, skill routing and project contracts; its frontend example carries component reuse into criteria, browser obligations and independent source inspection. Take the relationship, not its stack or brand choices.
- Arquimedium already loads sources by role/task and mechanically checks some architectural boundaries. Its separate feature-planning and visual-work routes can leave frontend requirements disconnected. Combine role, phase and affected concern when selecting guidance.
- Both projects contain stale or duplicated instructions. Resolve authority and source ownership before promoting more rules.
- WTK security already supports optional specialists, a baseline when they are absent, explicit requirements and proofs. Extend that inheritance principle without duplicating the security procedure.

## Shape

`wtk-setup` is a proposed skill that discovers the project harness, interviews the user and proposes or updates project-owned guidance. Its output connects applicable requirements and selected driver skills to WTK planning, checks and verification. The binding decision is adoption of a project policy or skill responsibility; inspection alone does not adopt either. A machine-readable policy registry becomes worthwhile only if bounded evaluation shows that ordinary conditional guidance cannot support reliable applicability and tracing; it is outside the first version.

## Key decisions

1. **WTK owns the discovery and inheritance procedure; projects own adopted rules.** The shared baseline supplies questions and small proposals. Brand, architecture style, deployment provider, branch syntax, data policy and compatibility choices come from project decisions.
2. **Setup includes a focused interview about driver skills for every relevant area.** Frontend, backend, security, architecture, database and quality are candidates, not an exhaustive required skill list. Inspect actual available skill metadata and existing bindings first; ask the user to choose or confirm unsettled driver responsibilities, including which skills planning must read. Reuse explicit decisions already made in the session.
3. **A discovered pattern is evidence, not authority.** Distinguish adopted rules, observed conventions, proposed baseline additions, contradictions and unavailable evidence. Preserve approved project decisions; surface unresolved conflicts instead of silently choosing a winner.
4. **Guidance loads by role, phase and affected surface or concern.** Root instructions carry minimal authority and routing. Conditional guidance has one owning source and a clear trigger; specialist skills supply relevant procedures. A role filter cannot hide an applicable requirement from the planner or Verifier.
5. **Every applicable adopted requirement needs an explicit landing in the feature contract.** Resolve it to a concrete criterion/check, unchanged behavior with source and valid evidence, a justified non-applicability decision, or a named unresolved gap. Classify gaps using existing `open`, `blocks` and `blocks go-live` dispositions, with the dependent work and release condition; a recorded gap does not authorize blocked work. Both Lean and modular planning must support this; smaller task paths retain the obligation without requiring a full plan.
6. **Feature criteria receive one fresh non-author review before dependent build.** Antonio approved this default; add specialists only for a concrete coverage gap and use an existing Plan/Checks review when it fulfills this responsibility. The reviewer independently derives applicable concerns and sources from the request, proposed change and authoritative project routing, then challenges the planner's selection and exclusions. After build, a fresh Verifier repeats this reasoning against the actual change and checks criteria, proofs and implementation; fixes return to the builder. Bounded maintenance retains WTK's existing direct, proportional route.
7. **Skill presence, policy quality and proof capability are separate.** An absent optional skill does not itself invalidate work. Missing policy, missing expertise and unavailable execution tools receive distinct dispositions; use existing guidance when sufficient, ask about material gaps, and never claim a browser or security outcome from metadata alone.
8. **Guideline location follows the consuming project.** Reuse its existing owning documents and directory convention. When none exists, propose `docs/guidelines/` as a default and create only applicable documents during authorized setup; users may choose another location. Keep routing in root instructions rather than copying guidelines there.

## Work

| Slice | Delivers | Status |
| --- | --- | --- |
| [Harness discovery](#harness-discovery) | An evidence-backed baseline and interview covering relevant areas and driver responsibilities | clear |
| [Project guidance](#project-guidance) | A small, consistent project harness with conditional guidance | clear |
| [Feature criteria](#feature-criteria) | Applicable project requirements in the feature contract, checked before build | clear |
| [Implementation verification](#implementation-verification) | Independent source-to-outcome checking with actionable failures | clear |

Order: Harness discovery -> Project guidance -> Feature criteria -> Implementation verification.

Already handled by existing WTK procedures: deriving named proofs, selecting proportional validation, preserving explicit construction constraints, security surfaces and abuse cases, and handing implementation defects back to a builder. Extend their existing contracts rather than creating parallel proof or security systems.

### Harness discovery

**Delivers** a bounded project assessment and the user decisions needed for its requirements. **Status: clear.**

The initial area set is a discovery menu, not a requirement to create a document or install a skill for every row:

| Area | Discover |
| --- | --- |
| Product and domain | User goals, vocabulary, sensitive workflows and authoritative product sources |
| Branching and collaboration | Branch conventions, worktree use, review and merge authority |
| CI and delivery | Iteration and readiness gates, environment promotion and deployment authority |
| Frontend | Content necessity, shared owners, async states, motion, accessibility and responsive behavior |
| Backend and integrations | Public contracts, validation, error handling, transactions, retries and provider failures |
| Architecture | Ownership, module boundaries, dependency direction and representative flows |
| Database and data lifecycle | Integrity, tenancy, migration authority, retention and recovery |
| Security and privacy | Assets, actors, trust boundaries, secrets, permissions and permitted data disclosure |
| Quality and evidence | Proof layers, fixtures, browser capability and evidence limits |
| Runtime and operations | Checkout/resource ownership, cleanup, observability, performance and incident recovery |
| Agent workflow | Roles, driver skills, source precedence, conditional context and tool authority |

Security applies across the relevant areas, including frontend exposure, persistence and deployment.

Starter proposals, selected for relevance and adapted through the interview, are:

- Necessary UI content, existing shared owners, content-shaped pending states and purposeful accessible transitions.
- Explicit public contracts, boundary validation, caller authority and recoverable failure/retry behavior.
- Defined data integrity, isolation and lifecycle requirements for affected persistence.
- Named, proportionate proof for each adopted outcome, with secret-free diagnostics.
- Explicit branching, delivery/deployment authority and runtime ownership/cleanup expectations.

These are proposals for adoption, not a fixed architecture, skill list or universal test suite.

| ID | State | What should happen | User sees |
| --- | --- | --- | --- |
| AC-01 | A new project has little guidance | Propose a small baseline for the relevant areas and ask about unresolved expectations and driver skills | A bounded proposal and concrete questions; assumptions remain marked |
| AC-02 | An existing harness is present | Inspect routing, sources and representative implementation/enforcement examples; interview about unsettled expectations and driver responsibilities, reusing explicit prior answers | Adopted rules, conventions, proposals and gaps distinguished; existing skill bindings do not suppress policy questions |
| AC-03 | An applicable area needs a driver decision | Present relevant available skills, their planning responsibilities and a recommendation; ask the user to choose or confirm | Frontend, backend, security and other relevant drivers resolved independently; one skill may cover several areas |
| AC-04 | A skill or proof capability is absent | Apply Key decision 7 and identify the affected requirement and available alternative | A specific disposition; no automatic installation or invented proof command |
| AC-05 | Evidence contradicts an instruction or another source | Name the conflicting claims and the owning decision; resolve only what existing authority settles | An actionable conflict or explicit unresolved decision |
| AC-06 | The request is an assessment | Inspect and propose without changing the consuming harness | Findings and a reviewable proposed delta |

### Project guidance

**Delivers** adopted guidance reachable by the agents that need it. **Status: clear.**

| ID | State | What should happen | User sees |
| --- | --- | --- | --- |
| AC-07 | Setup/update is authorized and decisions are settled | Extend the existing owning documents and routing, applying Key decisions 1–4 | A scoped diff that distinguishes binding project requirements from skill procedures |
| AC-08 | A conditional requirement is adopted | Give it a clear trigger, one authoritative source, observable outcome and suitable evidence approach | A usable rule rather than a generic instruction to improve quality |
| AC-09 | A role begins a task | Select guidance using its phase and affected concerns, including cross-cutting requirements | A frontend planner receives applicable UI/security guidance; a backend-only task avoids unrelated appearance guidance |
| AC-10 | Setup is repeated | Reuse equivalent decisions and owners; for changed policies, skills, sources or runtime assumptions, repair or retire stale bindings within authority and ask about materially changed responsibilities | No duplicate rules or empty topic documents; obsolete routes are exposed and unaffected decisions remain intact |
| AC-11 | Existing guidance references a missing source or skill | Expose the broken dependency and its impact before dependent claims | A repaired route within authority or a named limitation; no silent successful-load claim |
| AC-12 | A specialist recommendation conflicts with a project decision | Apply the project's source precedence and Key decision 3 | No implicit replacement of the project's adopted policy |

Native role files and host-specific configuration are optional; conditional project guidance must remain usable without them. Merely naming skills or listing documents does not prove that their applicable requirements were applied.

### Feature criteria

**Delivers** a reviewable feature contract whose requirements survive planning and handoff. **Status: clear.**

| ID | State | What should happen | User sees |
| --- | --- | --- | --- |
| AC-13 | Planning starts through either supported path | Select applicable project rules and required driver skills; read their relevant instructions before deriving feature criteria | Source-backed landings under Key decision 5; a missing required driver receives a gap disposition rather than silent substitution |
| AC-14 | A feature contains several concerns | Compose their requirements and identify conflicts or genuine non-applicability | UI, backend, security or data requirements travel together without a full unrelated guideline load |
| AC-15 | A feature contract is ready for criteria review | One fresh non-author reviewer applies Key decision 6, including independent concern/source discovery and challenges to non-applicability decisions | Missing sources or requirements produce findings before dependent build, citing the source and missing outcome |
| AC-16 | Criteria review causes a correction | The planner updates the owning contract and the reviewer rechecks affected coverage and gap dispositions | Reviewed coverage; blocking gaps prevent dependent build or go-live, while valid unchanged evidence is reused |
| AC-17 | The project requires content-shaped loading | Derive the affected view's masks from its real loaded composition, specifying unresolved values, retained known structure, action feedback and refresh behavior; require pending/ready geometry, wrapping and overflow checks at representative widths and short/held responses where relevant | Neither a generic spinner nor incorrectly shaped masks satisfy the criterion; no universal pixel tolerance or artificial minimum loading time |
| AC-18 | A feature contract is handed to a builder or resumed | Carry its applicable requirements, selected sources and review disposition through the existing handoff | The builder inherits the same obligations; a newly applicable concern reopens affected coverage |

### Implementation verification

**Delivers** independent checks that the actual change satisfies its project requirements. **Status: clear.**

| ID | State | What should happen | User sees |
| --- | --- | --- | --- |
| AC-19 | Every listed feature proof passes | The fresh Verifier independently derives applicable concerns/sources from the request, actual change and authoritative routing; challenge exclusions and reconcile the original rules with criteria and proofs | A missing source or requirement is a finding even when recorded tests are green |
| AC-20 | An implementation claims loading, motion, reuse or security compliance | Match each claim to evidence that reaches its boundary | Source tracing for shared ownership, rendered evidence for browser behavior, and behavioral evidence for security outcomes |
| AC-21 | Loading masks known content, uses mismatched geometry or discards valid same-context content on refresh | Compare pending/ready bounds, wrapping, overflow and retained content with the adopted criterion in its affected states | A concrete failure tied to the loaded component and relevant viewport/response conditions |
| AC-22 | Evidence or a required runtime is unavailable | Retain the requirement and mark the affected outcome unproven | No source-only visual pass, no waived requirement and no invented successful execution |
| AC-23 | Verification finds a violation | Return a finding to the builder, then independently recheck the affected fix | Author/checker separation and the existing remediation limits are preserved |
| AC-24 | Requirements, source inputs or affected concerns change after review | Reconcile the causal delta and reselect affected criteria and proofs | Current coverage with valid unchanged evidence retained |

Initial evaluation should include a blank project; an existing harness with unsettled policy; unchanged and changed-input setup reruns; frontend-only and backend-only plans; mixed security/data work; a missing optional specialist and missing required driver; conflicting instructions; a short-path task; a blocking gap; a deliberately omitted guideline and criterion; incorrectly shaped skeletons; and a green test suite whose implementation still violates an adopted rule. These are behavior probes for the future skill, not tests executed during this discovery.

## Sources

- Antonio's instructions in this conversation, 2026-10-20: WTK owns setup; propose a small baseline and ask questions; discover driver skills beyond frontend/backend, including security; use on-demand role guidance. Antonio approved one fresh criteria reviewer per feature by default, with additional specialists only for a concrete gap; model/effort choices still follow the existing agent-selection contract.
- [WTK public contract](../README.md), [context budget](../.agents/skills/wtk/references/context-budget.md), [construction constraints](../.agents/skills/wtk/references/construction-constraints.md) and [security](../.agents/skills/wtk/references/security.md): existing ownership and phase contracts.
- [Plaaay routing](https://github.com/antoniofulg/my-court/blob/3f0e5f9edc426ef4106249e2f46a6b7118846ba4/.agents/SKILL-ROUTING.md), [product context](https://github.com/antoniofulg/my-court/blob/3f0e5f9edc426ef4106249e2f46a6b7118846ba4/docs/product/AGENT-CONTEXT.md), [style contract](https://github.com/antoniofulg/my-court/blob/3f0e5f9edc426ef4106249e2f46a6b7118846ba4/docs/product/STYLE-CONTRACT.md) and [verification example](https://github.com/antoniofulg/my-court/blob/3f0e5f9edc426ef4106249e2f46a6b7118846ba4/docs/qa/reports/customer-phone-whatsapp/verification.md): source-inspected routing and recorded inheritance.
- [Arquimedium product context](https://github.com/arquimedium/crm/blob/c0d0b8269a5ff6feec7600a5a043895dc98277fa/docs/product/AGENT-CONTEXT.md), [frontend guidance](https://github.com/arquimedium/crm/blob/c0d0b8269a5ff6feec7600a5a043895dc98277fa/docs/design/FRONTEND.md) and [architecture](https://github.com/arquimedium/crm/blob/c0d0b8269a5ff6feec7600a5a043895dc98277fa/docs/architecture/ARCHITECTURE.md): source-inspected role routing, proof distinctions and architectural authority.
- [Adaptive Guidelines](https://github.com/antoniofulg/adaptive-guidelines): existing companion for capturing and promoting recurring lessons; this capability concerns initial setup, assessment and feature inheritance rather than a second lesson store.
