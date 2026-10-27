# Project requirements

**Read when:** deriving feature criteria or checks, building or verifying a feature, or applying
adopted project guidance during bounded maintenance. Applies to Lean and modular paths under every profile.

## Discover applicability

Start from the user's request, the proposed change (actual diff during verification), and the
project's authoritative instruction routing. Derive affected concerns independently of the
planner's source list: data shown in a screen can bring authorization and privacy into frontend
work. Select guidance by **role, phase and affected concern** together; a role filter must not hide
an applicable cross-cutting requirement. Exclude unrelated procedures with a concrete reason.

Read the applicable owning project guidelines and the relevant instructions of selected required
driver skills **before deriving criteria or checks**. Resolve skills through the host's actual
available metadata and installed source, not a presumed name or an invocation claim. Follow source
pointers far enough to recover the applicable rule. Naming a skill is not reading or applying it.
Use project-owned locations; no particular guideline directory or native role file is required.

Resolve the project's [decision store](artifacts.md#decision-store) and read applicable accepted
decisions alongside the source PRD, RFC or design. Use
[artifact handoffs](artifacts.md#product-and-decision-artifacts) to carry settled intent without
repeating discovery. Preserve decision links and status in the native Sources and criteria fields.

Keep adopted project rules distinct from observed patterns and proposed additions. A specialist's
recommendation cannot silently replace an adopted decision. Resolve precedence using the project's
authority and explicit supersession; otherwise cite conflicting claims and the owning unresolved
decision. Inspect representative implementation and enforcement as evidence, not as policy adoption.
Setup or policy revision is not required merely because a task reads existing guidance.

User-owned scope, product behavior and departures from binding sources require an answer or
explicit delegation before dependent implementation. Resolve routine facts and reversible detail
from repository evidence. Record unanswered product choices as unresolved with dependent work
blocked; an assumption/default or silence cannot authorize them. Record answers and delegation
in the receiving turn under the native decision fields, using the approval and recovery procedures.

Separate missing policy, missing expertise/required driver, and unavailable proof capability.
An absent optional specialist alone does not block work when existing guidance suffices. An
unavailable required driver needs a named affected responsibility and an authorized alternative or
gap disposition; never silently substitute a skill, invent a command, or install anything.

## Land requirements in the native contract

For each applicable adopted requirement, record its source/section and one landing in the existing
plan/task/checks fields; do not create a parallel registry or report schema:

- A concrete feature criterion and proof-backed check.
- Unchanged existing behavior, with its source and valid evidence at the claimed boundary.
- Non-applicability, with the reason tied to this change.
- An unresolved gap classified as `open`, `blocks` or `blocks go-live`, naming dependent work and
  the release condition. A recorded gap does not authorize blocked work or activation.

Compose concerns rather than choosing a single driver for the whole feature. Use the existing
[construction constraints](construction-constraints.md), [security procedure](security.md) when
its trigger fires, and [test contract](test-contract.md) for proofs; do not duplicate their rules.
Keep sources and dispositions reachable in existing Sources, criteria, Coverage, Swept, Unresolved
or Handoff fields as appropriate. A checks-only feature retains these landings without a full plan.
Bounded maintenance keeps its direct proportional route in [validation](validation.md), without a
mandatory feature reviewer or delegation.

## Review criteria before dependent feature build

The coordinator obtains **one fresh non-author criteria reviewer** for the complete feature
contract. Use an existing Plan/Checks review when it fulfills this responsibility; add a specialist
only for a concrete coverage gap. The `planning` stage in [agent selection](agent-selection.md)
owns its approved execution settings; reuse session approvals within their scope.

Give the reviewer the original request, proposed delta, authoritative project routing and native
contract. The reviewer repeats **Discover applicability**, reads applicable sources/required driver
guidance, and challenges the planner's selections, exclusions and gap dispositions. A missing
source or adopted outcome is a finding even if every listed criterion has a proof. Return the
source, missing outcome and owning contract location to the planner; the planner corrects that
contract, and the reviewer rechecks affected coverage before dependent build. `blocks` gaps keep
dependent build blocked; `blocks go-live` gaps prevent activation. Reuse valid unchanged evidence
through [validation](validation.md); do not add another human approval for routine corrections.

## Build and recover

Before dependent edits, read the inherited applicable guidance and review disposition. Preserve
the obligations; do not narrow a criterion to fit the implementation. A newly affected concern,
changed source or missing prerequisite reopens its affected coverage and criteria review. Carry
sources, driver responsibilities, landings and unresolved blockers through the existing handoff
using [context recovery](context-handoff.md). Reconcile changed inputs and retain valid evidence.

## Verify independently

The fresh full-feature Verifier repeats **Discover applicability** from the original request,
actual change and authoritative routing, rather than treating planner-selected sources as complete.
Challenge exclusions, then reconcile adopted rules with criteria, checks, proofs and implementation
under every profile. An omitted source or requirement is a finding despite green listed proofs.
Resolve the decision store independently, follow applicable accepted records and supersession links,
and check that implementation honors them. A draft proposal cannot substitute for an accepted decision.
Record findings and limits in the existing verification report; no second report is required.

Match evidence to the claimed boundary: trace shared ownership through actual consumers, inspect
rendered states for browser behavior/motion, and require behavioral authorization/security evidence
where claimed. Skill metadata or source inspection alone cannot prove a browser or security outcome.
An unavailable runtime or source leaves the affected obligation unproven, not waived. Return failures
to the builder through [review rounds](review-rounds.md); independently recheck fixes using
[validation](validation.md) to retain valid unchanged proofs.

### Challenge with independent examples

Before the verdict, choose a small risk-based set of inputs or states the plan and checks do not
name. Target boundaries, empty/repeated input or partial failure where listed proofs could stay
green despite violating an approved claim. Derive expected outcomes from that claim and adopted
rules, not the implementation; an unsettled product answer is a decision gap, not a new default.
Run the examples through the claimed boundary with disposable requests or tests. Record the owning
claim, exact input/state, expected and actual outcome, command and result in the existing report.
Reuse an executed case only when its evidence independently settles that exact example. Explain
when no distinct relevant example exists; unavailable execution leaves the affected claim unproven.
Examples do not count as mutations or change the declared profile. Keep the selection bounded
without a fixed quota, extra reviewer, new report or unapproved capability.

## When content-shaped loading is adopted

Read the affected view's real loaded composition before writing its loading criteria. Identify
known headings, controls and structure that remain visible; mask only unresolved values with shapes
derived from their loaded owners. Specify action feedback and refresh behavior, including retention
of valid same-context content and recovery after failure. A generic spinner or arbitrary skeleton
cannot stand in for this adopted requirement.

Name evidence comparing pending and ready geometry, bounds, wrapping and overflow at representative
widths, content lengths and response conditions. Exercise short and held responses where relevant
without artificial minimum loading time. Derive any tolerances from the project's approved design
and actual composition; no universal pixel threshold applies. During verification inspect these
states independently, including known content wrongly masked, mismatched unknown-value geometry,
and valid content discarded on refresh. Missing rendered evidence leaves the outcome unproven.
