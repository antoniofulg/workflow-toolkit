# Setup interview

**Read when:** choosing relevant setup areas, proposing a baseline or interviewing unresolved policy
and driver responsibilities in a new or existing project.

## Area menu

Use the menu to discover what applies, not to require a skill or document per row. Security can
affect every area. Inspect existing answers first, then ask focused questions about remaining choices.

| Area | Policy and evidence to discover | Driver responsibility to settle |
| --- | --- | --- |
| Product and domain | Goals, vocabulary, sensitive workflows, authoritative product sources | Read product/domain sources before deriving feature outcomes |
| Branching and collaboration | Branch/worktree conventions, review and merge authority | Preserve the project's collaboration and checkout rules |
| CI and delivery | Iteration/readiness gates, promotion and deploy authority | Derive executable gate and release obligations without extending authority |
| Frontend | Necessary content, shared owners, async states, motion, accessibility, responsive behavior | Read UI policies and chosen design/frontend guidance before screen criteria |
| Backend and integrations | Public contracts, input validation, authority, transactions, retries, provider failures | Derive boundary outcomes and recovery requirements |
| Architecture | Ownership, module boundaries, dependency direction, representative flows | Carry architectural constraints into criteria and source-tracing proofs |
| Database and lifecycle | Integrity, tenancy, migration authority, retention, recovery | Derive data/isolation obligations and distinguish execution authority |
| Security and privacy | Assets, actors, trust boundaries, secrets, permissions, permitted disclosures | Apply WTK's existing security phases plus adopted project security guidance |
| Quality and evidence | Proof layers, fixtures, browser capability, evidence limits | Choose proofs reaching the claimed boundaries; preserve unproven outcomes |
| Runtime and operations | Checkout/resource ownership, cleanup, observability, performance, incident recovery | Carry runtime and operational requirements into work and handoff |
| Agent workflow | Source precedence, roles, phase/concern routing, tool authority | Bind actual available skills to explicit planning/build/checking responsibilities |

## Small baseline to propose

Adapt only relevant proposals; none becomes binding through inspection alone:

- Keep UI content necessary, reuse existing shared owners, derive pending masks from loaded
  composition, and make transitions purposeful and accessible. The conditional loading contract is
  in [project requirements](../../wtk/references/project-requirements.md#when-content-shaped-loading-is-adopted).
- Define public contracts, boundary validation, caller authority and recoverable failure/retry behavior.
- Define integrity, isolation and lifecycle requirements for affected persistence.
- Name proportionate evidence for each adopted outcome and keep diagnostics free of secrets.
- Set branching, delivery/deployment authority and checkout runtime ownership/cleanup expectations.

Do not prescribe a framework, architecture style, provider, compatibility rule, skill list or test
suite. Extend the existing [security procedure](../../wtk/references/security.md), not a second one.

## Focused questions

Use available evidence to make the question concrete. Ask the relevant unresolved subset, in small
batches; reuse prior explicit answers rather than running a fixed questionnaire.

- For a blank project: which relevant baseline outcomes should be adopted, and which product or
  engineering constraints change them? Where should owning guidance live if no convention exists?
- For an existing harness: which conflicting or stale source is authoritative? Does the observed
  recovery, data or UI behavior reflect intended policy, or an implementation gap? Existing driver
  choices do not settle these questions.
- For each unsettled area: which available driver should planning read, for what responsibility,
  and which build/verification procedures should it supply? Present a grounded recommendation and
  any expertise limits; allow one driver to own several areas.
- For missing capability: can existing guidance and tools satisfy the requirement, is an alternative
  authorized, or what dependent work must remain blocked? Optional skill absence and unavailable
  browser execution are different gaps.
- For a changed-input rerun: does the renamed source, removed skill or changed runtime alter the
  adopted responsibility? Ask only about that change and preserve unaffected decisions.

Record adopted answers in their existing owners during authorized setup, proposals as proposals,
and unresolved gaps through the shared dispositions. Never infer consent to install missing tools
or to change a project's delivery authority.
