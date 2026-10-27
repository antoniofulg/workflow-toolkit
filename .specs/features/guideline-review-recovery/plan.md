# Guideline review and evidence-safe recovery

## Approval

- Decision: user selected "Approve plan" in the feature_plan question in this conversation.
- Date: 2026-10-27 UTC.
- Source: functions.ask response immediately following presentation of this plan.
- Reviewed revision: plan snapshot 2389 on feature base 86ae3f9f8f6402c31146362840bbbe1843389d5e.
- Scope: all four slices and the stated exclusions; local implementation and commits only.
- Execution selection: user selected "Accept inherited settings" for the fresh criteria reviewer, sequential builder and independent final Verifier; inherited child-model and effort limitations accepted.

## Problem

WTK setup currently interviews material uncertainties but can preserve existing guideline rules without explicitly asking whether the user still wants them. The user wants a guided keep-or-change interview about those rules, not only a gap interview.

Feature execution also depends on human approval and visual evidence that the current structural gates do not fully represent. Earlier disposable-project probes in this conversation observed `validate_checks.py --strict` accepting a plan with no approval receipt and `validate_verification.py --strict` accepting a UI report naming nonexistent capture files. The existing verifier remains responsible for semantic truth; these gaps expose inexpensive structural safeguards.

After this change, setup presents relevant existing rule sets for an explicit keep/change decision, and the Lean and modular procedures preserve authorization, live dispatch state and trustworthy visual evidence across context recovery. The selective upstream changes do not replace WTK's coordinator-owned independent verification or causal evidence reuse.

## Flow

Reuse the existing setup interview, shared requirement/construction/recovery/UI references, native feature artifacts and Lean validator suites; do not introduce a policy registry or parallel verification pipeline.

1. A setup request -> `wtk-setup` (exists) - discovers existing owners and presents source-linked rule groups for keep/change/retire/defer decisions.
2. A decided feature -> `wtk-lean` Plan or `wtk-plan` (exists) - resolves user-owned choices, records observed approval in the native contract, and derives obligations only within its scope.
3. A build entry -> `validate_checks.py` (exists) and the shared construction procedure (exists) - reject absent approval evidence and block dependent work without usable authority.
4. A user decision or coordinator dispatch -> shared context handoff (exists) - updates existing artifacts immediately, records dispatch intent before sending, and records actual host identity after sending.
5. A binding-source comparison -> shared UI procedure and `validate_verification.py` (exists) - require genuine viewport capture evidence and structural provenance; independent verification judges actual fidelity and input equivalence.

## Impact

| Front | What changes |
| --- | --- |
| domain | Existing setup decisions become explicit keep/change/retire/defer dispositions for relevant guideline rule groups; observed implementation remains distinct from adopted policy. |
| domain | Feature approval evidence remains separate from provider/model/effort approval in `workflow.json`; neither substitutes for the other. |
| stored data | Native Markdown feature contracts gain approval evidence; visual report rows gain explicit provenance fields. Existing incompatible evidence must be corrected from real sources, never fabricated or silently grandfathered. No application data changes. |
| consumers | Setup instructions, shared references, Lean and modular phase entrypoints/templates, validator fixtures and owning regression suites, README and changelog must remain consistent. |

## Relations

None - no application stored-data shape change. Existing feature contracts own approval receipts, existing Handoff owns live decisions and dispatch state, and existing verification reports own visual evidence.

## Surface

None - nothing consumed outside through a new route or changed command signature.

No new command or flag. Existing `validate_checks.py <feature> --root <project>` and `validate_verification.py <feature> --root <project>` keep exit codes 0 for accepted evidence, 1 for invalid evidence and 2 for an unresolved target. Their accepted artifact contract becomes stricter as recorded below.

## Landing

| One-way door | Literal shape | Alternative rejected |
| --- | --- | --- |
| Native approval evidence | The owning plan/task, or checks-only intent contract, records the actual user decision/date or durable source, reviewed revision and authorization scope. Lean build and completion gates require the applicable record; independent review judges authenticity and scope. The contract must distinguish a real receipt from a template/example. | Reusing execution-selection approval or trusting commit history cannot establish approval of feature shape. A standalone authorization registry creates a second source of truth. |
| Visual evidence contract | Existing visual-fidelity report rows explicitly identify source/revision, implementation revision, route/state, CSS viewport/scroll, environment including DPR, local reference/full-page/viewport capture paths, comparison and independent result. Gates require usable structural provenance and existing local files; judgment remains independent. | Accepting a nonempty free-text capture cell permits nonexistent images. A new screenshot framework or separate mandatory screen reviewer is unnecessary. |

Nothing else in this change is hard to reverse. The implementation should reuse the current parser composition and the narrowest shared helper only when multiple gates own the same evidence contract.

## Criteria

### S1: Explicit guideline review and user-owned decisions (P1)

**Acceptance Criteria**

1. WHEN setup assesses or updates an existing project THEN it SHALL present source-linked summaries of the material rules in each relevant existing guideline area and ask whether to keep them, change selected rules, retire selected rules, or defer the decision; existing file presence or a driver assignment SHALL NOT supply that answer.
2. WHEN the user answers for an area or an explicitly grouped rule set THEN setup SHALL record the covered disposition in its normal proposal or authorized owning documents, preserve unaffected owners, and avoid repeating that settled question in the same active setup interview; unanswered rules SHALL remain unchanged and visibly unresolved rather than implicitly approved or retired.
3. WHEN setup covers UI work THEN its area menu SHALL explicitly name UI/UX and frontend, including journeys/interactions, states, accessibility, responsive behavior and binding visual sources, while allowing the project to select an actually available specialist rather than hardwiring Frontend Craft.
4. WHEN a product scope, product behavior or binding-source departure remains genuinely unsettled THEN Lean and modular planning SHALL ask the user or record explicit delegation before dependent implementation; routine facts and reversible implementation choices SHALL remain agent-owned, and silence SHALL NOT become approval through an assumption row.

**Independent test:** Walk the setup procedure against a disposable existing-project scenario with settled rules, a rule selected for revision, an unavailable proposed driver and a deferred decision; inspect its proposed delta and questions without modifying the source project. Review planning scenarios with explicit delegation and unanswered product behavior.

### S2: Approval evidence reaches build and completion (P1)

**Acceptance Criteria**

5. WHEN a real feature approval arrives THEN the agent SHALL record its actual source/words, reviewed revision and scope in the owning native contract in that turn, without claiming that local Markdown authenticates the user or grants remote delivery authority.
6. IF an applicable Lean approval receipt is absent, empty or merely a template/example THEN the pre-build and completion gates SHALL exit 1 with an actionable diagnostic; a structurally complete receipt SHALL satisfy that structural obligation without waiving independent scope/authenticity review.
7. WHEN the existing checks-only escape applies THEN the approval evidence SHALL live with its intent in `checks.md`, without requiring a synthetic plan or an additional approval when the current request already authorizes that bounded work; modular tasks SHALL preserve the same source/scope semantics in their own contract and dependent-build procedure.
8. WHEN a previously approved feature resumes unchanged THEN it SHALL reuse its genuine approval within scope; a changed product decision outside that scope SHALL require targeted acceptance, while allowed reversible detail and additive noncontradictory build discoveries SHALL NOT trigger blanket reapproval.

**Independent test:** Run the real gate CLIs over temporary project fixtures with missing, placeholder/fenced, complete and checks-only receipts. Exercise valid execution-selection approval without feature approval as a negative control, and inspect the modular handoff semantics.

### S3: Recovery does not lose decisions or duplicate dispatch (P1)

**Acceptance Criteria**

9. WHEN a user answers during planning or build THEN the agent SHALL update the existing owning decision/contract or Handoff in that turn rather than waiting for a batch-end checkpoint.
10. WHEN a coordinator prepares a delegated assignment THEN it SHALL record assignment scope, phase/stage and checked revision as pending dispatch in the existing Handoff before sending it, then record the returned host identifier/status immediately after a successful send; a failed send SHALL remain distinguishable from a running assignment.
11. WHEN recovery finds pending or running work THEN it SHALL reconcile the record with available host status/reports before waiting or redispatching; an intent with no proven host assignment SHALL NOT be treated as a live agent, and unresolved ownership SHALL block duplicate dispatch rather than invent a successful send.
12. WHEN a running assignment returns or definitively cannot return THEN the coordinator SHALL update its existing record before proceeding or replacing it, preserving accepted execution choices and the coordinator/builder/Verifier separation.

**Independent test:** Walk recovery scenarios for pre-send interruption, successful send with recorded host identity, failed send, returned report and unavailable host status. Observe whether the next authorized action is send, wait, consume, replace or remain blocked; do not create a new scheduler or persistent dispatch service.

### S4: Authentic and current visual evidence (P1)

**Acceptance Criteria**

13. WHEN a binding visual source is compared with the implementation THEN the capture SHALL be taken at the contracted CSS viewport with recorded DPR/source scale and environment; resizing or cropping a different viewport's image SHALL NOT serve as evidence of that contracted render.
14. IF a visual-fidelity row lacks required provenance or a named local reference/full-page/viewport capture does not exist THEN the completion gate SHALL exit 1 even when behavior proofs and the report's result cells say PASS; non-UI profiles SHALL NOT require UI evidence.
15. WHEN implementation or source inputs affecting a contracted screen change THEN the independent Verifier SHALL invalidate and refresh affected evidence; unrelated changes SHALL preserve evidence only with an explicit input-equivalence reason, not solely an old PASS or a matching filename.
16. WHEN visual evidence is structurally accepted THEN the independent Verifier SHALL still open the images, judge every contracted pair and reproduce states where screenshots cannot establish behavior; no structural gate SHALL claim to prove fidelity, approval authenticity or complete matrix coverage.

**Independent test:** Run the real completion gate against disposable UI projects with genuine local image files, missing files and missing provenance; compare acceptance with non-UI controls. Independently inspect a synthetic wrong-viewport/resized-image scenario and changed versus unchanged rendering inputs. No production application screen is changed by this feature.

## Traceability

| ID | Slice | Criteria | Status |
| --- | --- | --- | --- |
| SETUP-01 | S1 | 1, 2, 3 | Pending |
| PLAN-01 | S1 | 4 | Pending |
| APPROVAL-01 | S2 | 5, 6, 7, 8 | Pending |
| RECOVERY-01 | S3 | 9, 10, 11, 12 | Pending |
| VISUAL-01 | S4 | 13, 14, 15, 16 | Pending |

## Out of scope

| Excluded | Why |
| --- | --- |
| Automatic companion installation or binding Frontend Craft for every project | Driver selection remains project-owned and availability must be verified. |
| A policy registry, dispatch service, screenshot framework or new mandatory screens agent | Existing artifacts and coordinator responsibilities own these contracts. |
| Wholesale upstream replacement, fixed mutation quotas or one-fix-pass verification limits | The approved recommendation preserves WTK's independent verification and impact-based evidence reuse. |
| Application UI changes, deployments, pushes, pull requests or merge | The request authorizes local toolkit changes, not remote delivery or consuming-project modifications. |
| Knowledge bundle edits | No durable knowledge write has been authorized. |

## Assumptions

| Assumption | Chosen default | Rationale | Confirmed? |
| --- | --- | --- | --- |
| Interview question granularity | Present each relevant area's material rules together; allow a single explicit keep decision to cover that named set and drill into selected changes. | Explicitly accepted with "Approve plan". | y |
| Scope of TLC adoption | Implement all four recommended improvements, preserving the exclusions stated in the earlier assessment. | Explicitly accepted with "Approve plan". | y |

**Open questions:** none - scope and inherited execution settings explicitly accepted; fresh non-author criteria review still precedes Build.

## Observable

| Surface | Decision | Landing |
| --- | --- | --- |
| Setup interview | Questions about existing rules, retained decisions, deferred areas and required drivers | AC 1, 2, 3 |
| Planning guidance | Genuine product decisions versus routine reversible detail | AC 4, 5, 7, 8 |
| CLI gates | Invalid approval evidence returns 1 without changing project authority | AC 6 |
| Recovery guidance | Dispatch intent, actual host status, ownership and restart action | AC 9, 10, 11, 12 |
| Visual report | Genuine viewport, provenance, local capture availability and evidence validity | AC 13, 14, 15, 16 |
| CLI gates | Existing parser/target-resolution exit codes | existing - current validate_checks.py and validate_verification.py entrypoints |
| Browser screen | New or changed application screen states | n/a - this toolkit feature changes workflow instructions and evidence validation, not an application screen |

## Security Surfaces

| ID | Surface | Control | Requirements |
| --- | --- | --- | --- |
| S1 | Stricter public validator behavior and workflow instructions | Explicit local authorization boundaries and native-artifact validation | APPROVAL-01, VISUAL-01 |
| S6 | Markdown receipt and capture-path parsing | Parse evidence as data, never execute it; resolve named local files predictably and report unavailable provenance | APPROVAL-01, VISUAL-01 |

S1 and S6 alone do not require a separate threat model. No network ingress, credentials, production data or external mutation is introduced. Local receipts remain procedural evidence rather than authentication.

## Sources

- Current user request - explicitly requests keep-or-change guideline interviews and the selective TLC improvements from this conversation.
- `AGENTS.md` - planner-owned feature contract, approved execution selections, sequential builder, independent Verifier and local delivery constraints.
- `.agents/skills/wtk-setup/SKILL.md` and `references/interview.md` - existing setup ownership and interview baseline.
- `.agents/skills/wtk/references/project-requirements.md`, `construction-constraints.md`, `context-handoff.md`, `ui-ux.md`, `validation.md` and `test-contract.md` - existing shared owners and evidence boundaries.
- https://github.com/tech-leads-club/agent-skills/commit/ef2672d67 - selective specification, product-decision and proof changes.
- https://github.com/tech-leads-club/agent-skills/commit/65ca25bf3 - approval/dispatch persistence through compaction.
- https://github.com/tech-leads-club/agent-skills/commit/eec04107f - Lean approval and screenshot provenance/recovery changes.

## Accepted execution selection

Accepted through the execution_settings answer "Accept inherited settings" in this conversation. The frozen route and dispatch status are recorded in the feature checks Handoff.

| Stage | Provider | Model | Effort | Responsibility | Host limitations |
| --- | --- | --- | --- | --- | --- |
| planning | codex | inherited | inherited | One fresh non-author criteria review of the complete contract before Build. | model: child default is not exposed in advance; effort: dispatch API exposes no effort override. |
| implementation | codex | inherited | inherited | One sequential builder handles all four slices, tests, fixtures and public documentation. | model: child default is not exposed in advance; effort: dispatch API exposes no effort override. |
| verification | codex | inherited | inherited | One fresh non-author Verifier covers the complete feature range under standard profile. | model: child default is not exposed in advance; effort: dispatch API exposes no effort override. |

Capability source: current host tool schema exposes fresh agent dispatch and optional model selection, but no advertised model availability list or effort override. Coordinator model is exposed as `openai-codex/gpt-6.1-sol`; that does not establish a child's default. All work stays in this checkout. The coordinator owns integration, verification dispatch and local commits. No QA or Deep Review stage is proposed because no application screen changes and no separate review need has been established.
