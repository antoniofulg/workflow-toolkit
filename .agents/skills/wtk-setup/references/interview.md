# Setup interview

**Read when:** reviewing existing guideline rules, proposing a baseline or interviewing policy
and driver responsibilities in a new or existing project.

## Area menu

Use the menu to discover what applies, not to require a skill or document per row. Security can
affect every area. Group the relevant material rules by area and cite each owning path/section.

| Area | Policy and evidence to discover | Driver responsibility to settle |
| --- | --- | --- |
| Product and domain | Goals, vocabulary, sensitive workflows, authoritative product sources | Read product/domain sources before deriving feature outcomes |
| Branching and collaboration | Branch/worktree conventions, review and merge authority | Preserve the project's collaboration and checkout rules |
| CI and delivery | Iteration/readiness gates, promotion and deploy authority | Derive executable gate and release obligations without extending authority |
| UI/UX and frontend | User journeys, interactions, necessary content, shared owners, states, motion, accessibility, responsive behavior and binding visual sources | Read adopted UI policies and actually available selected design/frontend guidance before screen criteria |
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

For each relevant existing area, show its source-linked material rule summary and ask: **keep this
named set, change selected rules, retire selected rules, or defer?** A grouped keep answer covers
only the displayed set; drill into selected changes/retirements. Ask in small area-grouped batches,
including apparently settled rules rather than only conflicts or gaps. Existing file presence,
implementation patterns and assigned drivers do not answer this question.

Record the user's disposition, exact covered rules/source and selected delta in the normal
assessment proposal or authorized owning documents in the receiving turn. Retire only explicitly
selected rules and their obsolete routes; preserve neighboring rules and unaffected owners.
Unanswered/deferred rules stay unchanged and visibly unresolved, with dependent work classified
through the shared gap dispositions. Reuse that record so a settled set is not asked again in the
same active interview; changed inputs reopen only the affected choice. Assessment remains read-only.

- For a blank project: which relevant baseline outcomes should be adopted, and which product or
  engineering constraints change them? Where should owning guidance live if no convention exists?
- For an existing harness: after the disposition question, which conflicting source is authoritative?
  Does observed recovery, data or UI behavior reflect intended policy or an implementation gap?
- For each unsettled area: which available driver should planning read, for what responsibility,
  and which build/verification procedures should it supply? Present a grounded recommendation and
  any expertise limits; allow one driver to own several areas.
- For missing capability: can existing guidance and tools satisfy the requirement, is an alternative
  authorized, or what dependent work must remain blocked? Optional skill absence and unavailable
  browser execution are different gaps.
- For UI/UX and frontend: which journeys/interactions and visual sources bind the work, and which
  actually available specialist should supply the needed expertise? A recommendation such as
  Frontend Craft is optional, not an adopted driver or permission to install it.
- For a changed-input rerun: does the renamed source, removed skill or changed runtime alter the
  adopted responsibility? Ask only about that change and preserve unaffected decisions.

Record adopted answers in their existing owners during authorized setup, proposals as proposals,
and unresolved gaps through the shared dispositions. Never infer consent to install missing tools
or to change a project's delivery authority.
