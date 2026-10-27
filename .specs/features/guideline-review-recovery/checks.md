# Guideline review and evidence-safe recovery checks

Profile: standard
Plan: `.specs/features/guideline-review-recovery/plan.md`

## Intent

12 checks in 4 slices, 2 changed artifact contracts, 0 open product decisions. The approved plan and execution-choice reply are recorded in the plan's Approval section. No application UI changes or remote delivery are authorized.

## Checks

### S1 - Review existing guideline rules and preserve user decisions

**C1** - Setup asks keep/change/retire/defer for source-linked material rules in every relevant existing guideline area, rather than only interviewing gaps, and records the exact covered set without repeating its settled question in the same interview (SETUP-01, AC 1, 2).
Proof: Independent semantic scenario review of an existing project with two relevant guideline areas, an unchanged rule, one selected revision, one explicitly selected retirement and one deferred rule; require the assessment proposal to retire only the named selected rule while preserving neighboring unaffected rules and owners. Record the actual questions/dispositions and PASS/FAIL in verification.md. This is an instruction-product judgment, not a source-string test.

**C2** - Setup explicitly covers UI/UX and frontend outcomes and requires actual driver availability/selection, without adopting or installing Frontend Craft automatically (SETUP-01, AC 3).
Proof: Independent semantic scenario review with a binding design, interaction/accessibility requirements and an unavailable proposed companion; record adopted policy versus unresolved driver/proof responsibility in verification.md.

**C3** - Both planning paths ask unresolved user-owned product decisions or honor explicit delegation, while preserving routine factual and reversible implementation discretion; an unanswered product choice cannot be converted into approval through a default (PLAN-01, AC 4).
Proof: Independent semantic scenario review of unanswered product behavior, explicit "you decide", a binding-source departure and a repository-set reversible convention; inspect the contract and dependent-work disposition in verification.md.

### S2 - Require genuine approval evidence at dependent gates

**C4** - Missing, empty and example/template-only feature approval receipts fail the real pre-build and completion gates even when execution settings were approved; complete native receipts satisfy only the structural obligation (APPROVAL-01, AC 5, 6).
Proof: `python3 tools/test_tlc_validators.py -k approval`
Proof: `python3 .agents/skills/wtk-lean/scripts/selftest.py`
Proof: Throwaway-project smoke invoking both actual gate CLIs with no receipt, a fenced example and a complete observed-receipt fixture; record commands, exit codes and decisive diagnostics in verification.md.

**C5** - Checks-only work keeps its receipt with intent without requiring a synthetic plan; modular work preserves approval source, reviewed revision and scope in the native task/checklist entry procedure (APPROVAL-01, AC 7).
Proof: `python3 tools/test_tlc_validators.py -k approval`
Proof: Independent semantic review of modular approval and checks-only authorization, including a current user request that already authorizes the bounded work; record the absence of a newly imposed human stop in verification.md.

**C6** - Resume reuses genuine unchanged approval within scope and asks targeted acceptance for a new product decision, without treating reversible detail/additive noncontradictory discoveries as blanket reapproval triggers (APPROVAL-01, AC 8).
Proof: Independent semantic recovery scenario review of unchanged scope, new user-owned behavior and allowed reversible detail; record the next authorized action and authority source in verification.md.

### S3 - Recover live decisions and actual dispatch state

**C7** - Both feature paths write user decisions in the receiving turn, and coordinator dispatch records distinguish pending intent, successful host identity, send failure and returned work (RECOVERY-01, AC 9, 10, 12).
Proof: Independent scenario review of a mid-build user clarification and send/return transitions in existing Handoff; record the minimum required writes and order in verification.md. Do not add permanent tests asserting instruction wording.

**C8** - Recovery reconciles the Handoff with host status/reports before send/wait/consume/replace decisions; an unproven host assignment or unresolved ownership does not authorize a duplicate dispatch (RECOVERY-01, AC 11, 12).
Proof: Independent scenario review covering pre-send interruption, successful send with recorded identity, failed send, returned report and unavailable host status; record send/wait/consume/replace/block outcomes in verification.md.

### S4 - Reject missing visual provenance without automating fidelity judgment

**C9** - The UI contract records the contracted CSS viewport, source scale/DPR and environment, and requires a genuine render rather than a resized/cropped image from another viewport (VISUAL-01, AC 13).
Proof: Independent visual-evidence scenario review of a source-sized viewport render and a wider render resized to the same image dimensions; record what is proven and what remains unverified in verification.md.

**C10** - The real completion gate rejects absent required visual provenance and nonexistent local reference/full-page/viewport captures even with PASS cells, and accepts structurally complete evidence with real files (VISUAL-01, AC 14).
Proof: `python3 tools/test_tlc_validators.py -k visual`
Proof: `python3 .agents/skills/wtk-lean/scripts/selftest.py`
Proof: Throwaway-project completion CLI smoke with real local capture files, missing files and missing provenance; record exit codes and diagnostics in verification.md.

**C11** - Non-UI profiles do not acquire screenshot requirements, and unchanged unaffected rendering evidence is reused only with independent input-equivalence evidence while changed source/render inputs invalidate affected captures (VISUAL-01, AC 14, 15).
Proof: `python3 tools/test_tlc_validators.py -k visual`
Proof: Independent scenario review of an unrelated documentation-only change, a shared style change and a source revision change; record affected versus reusable viewport/state evidence in verification.md.

**C12** - Structural gate acceptance never replaces independent approval-scope/authenticity or visual-fidelity judgment; both verification paths retain image inspection, complete contracted coverage and interaction reproduction where needed (VISUAL-01, AC 16; APPROVAL-01, AC 5).
Proof: Independent full-feature verification against the original request and applicable guideline/driver instructions; record scope/authenticity limits, actual inspected pairs and any gaps in verification.md.

## Coverage

| Set (size) | Member -> proof | Unproven |
| --- | --- | --- |
| setup rule dispositions (4) | keep C1; change C1; retire C1; defer C1 | - |
| approval receipt cases (4) | absent C4; empty C4; template/example C4; complete C4 | - |
| native contract paths (3) | Lean plan C4; checks-only C5; modular task C5 | - |
| recovery evidence states (5) | pending intent C8; recorded live identity C8; failed send C8; returned report C8; unavailable ownership/status C8 | - |
| visual capture roles (3) | reference C10; full-page C10; actual viewport C10 | - |
| evidence change classes (3) | unrelated inputs C11; changed rendering inputs C11; changed binding source C11 | - |
| verification profile families (2) | UI C10; non-UI C11 | - |

## Test policy

The existing test contract owns case derivation and proof layers. Extend `tools/test_tlc_validators.py` for artifact/gate outcomes and the Lean `selftest.py` mutant controls; do not add a second suite or freeze guideline wording. Instruction behavior is judged through concrete independent scenarios and reported as judgment, not as an automated passing test. The real CLI smoke distinguishes consumer-visible exit/diagnostic behavior from parser-only assertions.

## Swept

- validation: C4, C5, C10
- failure modes: C4, C8, C10
- idempotency: C1, C6, C8
- authorization: C3, C4, C5, C6, C12
- concurrency: C7, C8
- data lifecycle: C7, C8, C11
- dependency failure: C2, C8, C10
- state transitions: C1, C6, C7, C8
- observability: C4, C7, C8, C10, C12

## Handoff

- Phase: Build complete; scoped executable gates and actual CLI smoke passed; fresh full-feature verification pending.
- Feature base: `86ae3f9f8f6402c31146362840bbbe1843389d5e`.
- Approval: plan snapshot 2389 and inherited reviewer/builder/Verifier settings explicitly accepted through the current conversation's functions.ask answers. Source and scope are in plan.md Approval.
- Size: `wc -c` over 20 known owning instructions/validators/tests/docs returned 297949 bytes; /4 = 74487.25 estimated tokens. Allowing 75000 additional tokens for the related entrypoints, fixtures and implementation remains below the declared 200000-token budget. One builder owns S1-S4 sequentially, with no slice split.
- Runtime: no application server needed; standard-library Python fixture/CLI probes and existing Node distribution checks own the changed surface.
- Code intelligence: `xd://lsp` status returned "No language servers configured for this project"; ordinary code inspection is the available path.
- Settled mid-build: none.
- Dispatch: planning/criteria review and targeted recheck returned PASS from `CriteriaReview` / `CriteriaReview-2`; only initial finding was C1 retirement proof coverage and is closed.
- Dispatch: implementation S1-S4 returned from host agent `WorkflowBuilder`; complete batch received, no builder self-verdict.
- Evidence: `python3 tools/test_tlc_validators.py && python3 .agents/skills/wtk-lean/scripts/selftest.py && python3 tools/test_wtk_lifecycle.py` exited 0 on Python 3.15.1: 16 owning tests, 57/57 selftest mutants killed with clean baselines/controls/tooling, 5 lifecycle tests. Unclosed-file ResourceWarnings were emitted by completion-validator reads; assertions passed.
- Evidence: `node --test --test-name-pattern='full WTK set|approved execution selection' tests/skills/distribution.test.js && python3 tools/test_phase_skills.py` exited 0 on Node v22.23.1 / Python 3.15.1: 2 distribution checks and 7 phase checks.
- Evidence: coordinator Eval `run_guideline_recovery_cli_smoke()` ran 15 actual CLI invocations with disposable fixture artifacts: both gates reject absent/fenced/placeholder approval; complete and checks-only receipts pass; non-UI needs no captures; UI accepts complete provenance plus local PNGs and rejects missing implementation revision, viewport file or DPR. All expected exits observed; temporary project removed. Generated images prove structure/files only, not visual fidelity.
- Dispatch: verification pending for every C1-C12 over complete feature base..HEAD after the local implementation commit; no host identity assigned yet. Coordinator owns dispatch and completion gate.
- Next action: commit coherent feature batch, dispatch the accepted fresh final Verifier immediately, then disposition its report before feature cleanup.
- Metrics baseline: collection began after initial scoping; CODEX_THREAD_ID, CODEX_HOME, explicit session path and usage-counter environment keys were absent. Current-session token telemetry cannot be resolved by the supplied Codex reader without identity. No unrelated session logs were inspected.
