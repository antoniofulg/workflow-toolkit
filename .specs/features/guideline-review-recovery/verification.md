# Guideline review and evidence-safe recovery verification

**Verdict**: FAIL
**Profile**: standard
**Diff range**: 86ae3f9f8f6402c31146362840bbbe1843389d5e..fb85f321c634866c96d32baed51009bedf7ce357
**Round**: 1 - full
**Verifier**: independent sub-agent FeatureVerifier, author != verifier; coordinator Main did not write product code; no child agents launched

All C1-C12 and AC1-AC16 were inspected. Ten checks are proven; C4 and C10 have concrete counterexamples. Fourteen acceptance criteria are satisfied; AC6 and AC14 fail the stricter structural contracts. No product files, plan, checks, workflow snapshot or knowledge were changed by this Verifier. The coordinator owns disposition, remediation, the final strict report gate and cleanup.

## Ranked findings

1. **P2 — Reject approval examples introduced by a subsection heading.** `.agents/skills/wtk-lean/scripts/native_evidence.py:53-60` recognizes only level-one/two headings and plain `Example:` markers. With the complete fixture receipt beneath `## Approval` followed by `### Example`, it parses the illustrative bullets as an observed receipt. Both actual CLIs with `--strict` returned 0 with zero errors/warnings, although the only receipt is explicitly an example and AC6 requires exit 1. Recognize subsection example/template markers, or exclude their field content, rather than accepting it as the operative receipt. C4 / AC6; confidence 0.99.
2. **P2 — Reject incomplete visual tables instead of silently skipping them.** `.agents/skills/wtk-lean/scripts/validate_verification.py:227-229` discards a visual table when any required header is absent. If a report has one complete current-schema table and a second old-schema table for another viewport, `evidence_rows` remains nonzero and completion accepts the second table without validating its absent provenance or nonexistent captures. An actual strict completion CLI returned 0 with zero errors/warnings for a current table plus a legacy desktop row naming three missing PNGs. Emit an error for an unsupported/incomplete evidence-table schema in Visual fidelity instead of treating that row as absent; one valid table must not excuse other supplied rows. C10 / AC14; confidence 0.99.

These are structural failures, not attempts to make a Markdown gate authenticate a person or detect sophisticated image resizing. Both have explicit, locally visible distinguishing inputs.

## Binding sources

| Source | Opened | Contradiction | Uncovered |
| --- | --- | --- | --- |
| Original user request: ask whether existing guideline rules should be kept or changed, then implement the proposed selective TLC updates | yes — parent transcript Main user message and raw approval receipt below | none | - |
| Approved feature plan, snapshot 2389; current `plan.md:58-102` | yes — all 16 criteria, scope/exclusions, original snapshot marker recovered | none | AC6 example subsection; AC14 mixed-schema visual rows, findings 1-2 |
| `AGENTS.md:23-43,59-64,68-109` and `CLAUDE.md:1` | yes — standard profile, clean cutover, canonical proof owners, independence, local authority and conditional sources | none | - |
| Shared owners: `project-requirements.md:6-100`, `construction-constraints.md:17-70`, `context-handoff.md:6-72`, `ui-ux.md:122-168` | yes — requirement discovery, native authority, six dispatch states, capture authenticity and evidence reuse | none | gate enforcement gaps are findings 1-2 |
| Proof owners: `validation.md:48-100`, `test-contract.md:19-99`, `evidence.md:8-44`, Lean `references/verify.md:130-239` | yes — causal reuse, boundary assertions, no prose-string substitution and independent fault injection | none | - |
| Setup `SKILL.md:23-85` and `references/interview.md:6-73`; Lean and modular planning/build/verification entrypoints | yes — real consuming paths and templates, not just added text | none | - |
| Decision-store discovery: `knowledge/wiki/index.md:11-37`, workflow contract, construction constraints, design reference fidelity and artifact ownership concepts | yes — followed to owning README, skill references and artifact lifecycle; existing conceptual catalog is not a superseding policy source | none | - |
| Three upstream commit links in `plan.md:160-162` | not fetched — provenance for selective adoption, not a separately binding application/design contract; approved local criteria define adoption | none | - |

Applicability was independently derived from the request, full 31-file diff and root routing. This is a skills-only repository (`AGENTS.md:5-9`); there is no application product documentation or actual changed screen. Relevant concerns are instruction ownership, source adoption, local authority, Markdown/path parsing, distribution/import composition, proof levels and recovery. The project decision convention routes through the existing knowledge index and canonical sources; no new decision registry is justified. Read-only inspection creates no knowledge write. Database/tenant controls, network providers, Cloudflare, application architecture, deployment, PR/merge work and application QA are outside the actual change. Optional security specialists are not in the available skill set; the native security baseline was applied. Native LSP is unavailable, as the recovered parent host status states; source/import tracing was used.

## Approval authority and execution selection

The raw parent session is `/Users/antoniofulg/.omp/profiles/account2/agent/sessions/-Projects-my-workflow/2026-10-27T00-06-59-551Z_01a17aae-82df-745e-9f2f-cbf14cf1032a.jsonl` (abbreviated P below). Directly opened P entries `41b58031` / `4e9eac54`, lines 223/225, not a builder paraphrase. Ask call `call_274cce06fcd64737a853be5a58943807|fc_072af195cfc495f2016adfeeb10bd08191ac9233f8a232dfe4` was issued at 2026-10-27T00:22:15.040Z. Its feature option expressly covers keep/change/retire/defer, all four recommended safeguards and preservation of independent verification and impact-based evidence reuse. The execution question names a fresh criteria reviewer, one sequential builder and fresh final Verifier, unknown child defaults/no effort override, this checkout and no remote delivery.

Actual host tool answer at 2026-10-27T00:22:23.591Z: **feature_plan: Approve plan; execution_settings: Accept inherited settings**. The reviewed snapshot marker `plan.md#2389` is independently present in P entry `ba379c7e`, line 207; the receipt edit against that snapshot appears at P lines 246-248 in the receiving assistant turn before dependent build. Current `plan.md:3-10` faithfully records source, decision, reviewed revision and local scope. `workflow.json:2-39,52-88` separately preserves the accepted inherited settings and standard profile. The actual dispatch is in P lines 388-390 after the implementation commit; the subsequent Handoff records FeatureVerifier. This establishes observed local feature and stage authority, not remote delivery, application compliance or general authentication by Markdown.

## Checks

Paths in this table are repository-relative; abbreviated shared owners are expanded in the scenario sections below. R1-R3 are the original observed executable receipts under Gate. S1-S8 are the concrete independent semantic exercises below; they are instruction-product judgments, not automated agent behavior or source-string tests.

| Check | Claim | Proof run | Evidence | Result |
| --- | --- | --- | --- | --- |
| C1 | Source-linked keep/change/retire/defer, exact settled set, neighboring preservation | S1 existing-project interview, independent | `.agents/skills/wtk-setup/references/interview.md:42-53`; actual questions and disposition proposal in S1, with unchanged unanswered neighbor and no repeat | PASS |
| C2 | UI/UX/frontend outcomes and actually available driver choice | S2 unavailable-driver exercise | `.agents/skills/wtk-setup/references/interview.md:16,59-69`; `.agents/skills/wtk-setup/SKILL.md:31-35,52-62`; S2 separates adopted UI policy, specialist gap and proof availability | PASS |
| C3 | User-owned intent cannot become an assumed default; delegation and reversible detail differ | S3, both native planning paths | `.agents/skills/wtk-lean/references/plan.md:101-117`; `.agents/skills/wtk-plan/SKILL.md:89-112`; shared `project-requirements.md:31-40`; explicit blocked versus delegated results below | PASS |
| C4 | Both gates reject absent/empty/example-only authority independently of stage approval | R1 + R3 reused; new strict Example-subheading CLI probe | `tools/test_tlc_validators.py:83-112` asserts `self.assertEqual(result.returncode, 1, result.stdout + result.stderr)` for 13 invalid variants and 0 for complete; `:114-136` proves a validated execution route is insufficient; actual unhandled example at `native_evidence.py:53-60` returns 0 in both gates | FAIL |
| C5 | Checks-only owns intent/receipt; modular task owns approval, no redundant pause | R1 reused; S4 | `tools/test_tlc_validators.py:138-156` asserts exits 0, no synthetic plan, then exit 1 without Intent; `:158-179` asserts plan precedence and no approval prerequisite to plan presentation; modular `SKILL.md:67-70`, checklist `:116-120` link real source rather than copy | PASS |
| C6 | In-scope authority reused; changed product intent gets targeted acceptance | S4 recovery cases | `.agents/skills/wtk/references/construction-constraints.md:39-55`; Lean build `:36-61`; modular implement `:100-104`; next actions in S4 | PASS |
| C7 | Receiving-turn writes; pending/send/return state ordering | S5 decision and dispatch transitions | `.agents/skills/wtk/references/context-handoff.md:8-35,45-51`; Lean build `:14-17,167-169`; modular implement `:87-90`; S5 records concrete minimum writes and order | PASS |
| C8 | Reconcile before send/wait/consume/replace; uncertain ownership blocks duplicates | S6 six-state recovery exercise | `.agents/skills/wtk/references/context-handoff.md:37-51,58-68`; all six dispatch branches and authorized actions enumerated independently below | PASS |
| C9 | Contracted CSS render, scale/DPR/environment, not a resized wider image | S7 genuine-versus-resized evidence judgment | `.agents/skills/wtk/references/ui-ux.md:31-38,126-141,153-161`; modular screens `:31-35`; S7 explicitly rejects the wider resized capture | PASS |
| C10 | UI completion rejects missing provenance/files despite PASS cells | R1 + R3 reused; new mixed-schema CLI probe | `tools/test_tlc_validators.py:181-231` asserts exit 1 for every blank required cell, malformed provenance and each missing capture; `:233-252` covers paths. One valid table masks an invalid second schema at `validate_verification.py:227-229`, so the broader claim fails | FAIL |
| C11 | No non-UI screenshots; causal reuse versus invalidation | R1 reused; S8 | `tools/test_tlc_validators.py:254-263` asserts exit 0 for both light/standard without captures; shared UI `:142-147` and validation `:50-66` retain causal reuse; S8 has explicit pair-level actions | PASS |
| C12 | Structure never substitutes for authenticity, full visual coverage or interaction judgment | Full source/consumer review, actual approval inspection, S7/S8 | Lean verify `:15-49,60-65,106-128`; modular verify `:11-50,83-114`; shared UI `:136-161`; approval raw source inspected above. Actual application image pairs inspected: 0, because the feature changes no screen and defines no product visual match | PASS |

## Acceptance criteria reconciliation

| Acceptance criterion | Independent evidence / resulting action | Result |
| --- | --- | --- |
| AC1 | C1/S1 asks both relevant existing areas with named rule sets and sources rather than accepting file presence | PASS |
| AC2 | C1/S1 exact keep/change/retire/defer disposition; neighboring and unanswered rules preserved; no repeated settled question | PASS |
| AC3 | C2/S2 expressly includes journeys/interactions, states, accessibility, responsive constraints and binding sources; asks for an available specialist, no installation | PASS |
| AC4 | C3/S3 unanswered product behavior/departure blocks only dependent work; explicit delegation is recorded; implementation convention remains agent-owned | PASS |
| AC5 | Actual source/reviewed snapshot/local scope independently authenticated above; C7/S5 receiving-turn write; no remote authority inferred | PASS |
| AC6 | Ordinary invalid variants are rejected, but a complete receipt under `### Example` is accepted by both actual gates; finding 1 | FAIL |
| AC7 | C5/S4 checks-only intent with current-request authority needs neither synthetic plan nor new stop; modular task owns decision and checklist links it | PASS |
| AC8 | C6/S4 unchanged approval and additive reversible discoveries continue; new behavior asks targeted acceptance | PASS |
| AC9 | C7/S5 decision and affected dependency status recorded before continuing in both native paths | PASS |
| AC10 | C7/S5 pending intent precedes send; host identity/status or failure follows actual result | PASS |
| AC11 | C8/S6 host reconciliation precedes all decisions; unverifiable ownership blocks both fictitious waiting and duplicate dispatch | PASS |
| AC12 | C8/S6 records returned/terminal evidence and releases ownership before replacement, preserving choices and roles | PASS |
| AC13 | C9/S7 accepts only a genuine contracted CSS render as render evidence; resized wider image is rejected regardless of final pixel dimensions | PASS |
| AC14 | Non-UI exemption holds and ordinary invalid UI cases fail, but mixed legacy/current visual tables silently bypass required provenance/file validation; finding 2 | FAIL |
| AC15 | C11/S8 distinguishes unrelated documentation, shared styles and changed binding source with explicit affected pairs | PASS |
| AC16 | C12 independently preserves image opening, matrix completeness and real-viewport reproduction; fixture PNGs prove only structure/files | PASS |

## Independent semantic exercises

These synthetic inputs and simulated answers are verifier fixtures, not actual project policy or additional user decisions. No consuming-project files were created or edited for them.

### S1 — Two relevant existing guideline areas, all four dispositions

Fixture owners: `project/docs/guidelines/quality.md#proofs` contains Q1 canonical owning-suite proofs, Q2 run all tests after every edit, Q3 mandatory weekly coverage badge and Q4 nightly load gate; `project/docs/guidelines/ui.md#forms` contains U1 keyboard-reachable error recovery and U2 retained values after failed submission. These fixture paths are scenario labels, not repository citations.

Question 1: “Quality — Q1 canonical proofs, Q2 full suite after every edit, Q3 weekly coverage badge, Q4 nightly load gate (source: quality.md#proofs). Keep this named set, change selected rules, retire selected rules, or defer?” Simulated answer: keep Q1; change Q2 to impact-selected owning proofs after coherent batches; retire only Q3; defer Q4.

Question 2: “UI/UX and frontend — U1 keyboard-reachable errors and U2 retained values on failed submission (source: ui.md#forms). Keep this named set, change selected rules, retire selected rules, or defer?” Simulated answer: keep U1/U2 as the displayed set.

Resulting assessment proposal, recorded in that receiving turn: keep Q1 without changing its owner; edit only Q2 to the accepted impact-selected wording; remove only Q3 and a route used exclusively by Q3; keep quality.md and every shared route still serving Q1/Q2/Q4; leave Q4 text unchanged, visibly deferred with work that depends on a new load-gate decision blocked; keep U1/U2 and ui.md ownership. An undisplayed neighboring rule remains unchanged and not implicitly approved. Within this active interview ask no second disposition question for Q1-Q4 or U1-U2; a later source change reopens only the changed choice. In assessment mode these remain proposed edits, not writes. This follows interview `:42-53` and setup `:64-85`, and satisfies C1 without treating an existing driver as policy consent.

### S2 — UI/UX policy with an unavailable proposed driver

Input: binding design D7, journey “submit, recover an error, retry without lost input”; keyboard accessibility, loading/error/success states and 390x844/1440x900 responsive constraints. Proposed Frontend Craft is unavailable. Available fixture specialist A can review accessibility but cannot run a browser.

Generated question: “D7 and the listed interaction/state/accessibility/responsive requirements remain binding. Frontend Craft is unavailable. A can own accessibility review; existing project UI guidance can own the visual criteria. Select/confirm A for that responsibility, authorize a different actually available specialist, or leave the specialist responsibility unresolved?” Separate proof question only if required: “The required actual-viewport interaction proof is not executable here; authorize a capable available route or keep that affected proof unresolved?”

Result: retain adopted D7/product policies; do not install or bind the unavailable companion. An unanswered required driver responsibility is `blocks`, naming affected criteria; unavailable browser proof is a separate unproven outcome, not a waiver. Absence of an optional companion alone does not block unrelated work when existing guidance suffices. No actual skill availability or driver decision for the real user is fabricated. Sources: setup `SKILL.md:31-35,52-62`; interview `:16,59-69`; project requirements `:37-40`.

### S3 — Product intent, delegation, binding departure and routine detail

For both Lean and modular paths, input question “Should cancellation retain access until period end or end access immediately?” is a user-owned behavior choice. Proposed question: “Retain access through the paid period (recommended) or revoke immediately?” With no answer, Lean records proposed retain/default and `Confirmed? n`, with cancellation implementation blocked; modular records `Kind: blocks` and the same dependent work, not `blocks go-live` or a permissive `open` default. Independent settled work can continue.

With an explicit fixture reply “you decide,” record that exact delegation/source in the receiving turn; choose retain-through-period with rationale `user delegated` (`Confirmed? y` in Lean; native modular Sources/decision fields), derive its criterion, then implement within the delegated scope without repeating the question. For an approved two-column binding design versus a proposed one-column redesign, ask targeted acceptance and keep the departure blocked; the agent cannot relabel the source as inspiration. For an existing repository convention governing a helper name/location, inspect the convention and choose it directly; no extra human decision. Sources: shared project requirements `:31-35`; Lean plan `:101-117`; modular plan `:89-112`, document format `:30-35,143-153`. These are semantic distinctions, not string-test results.

### S4 — Native approval ownership, bounded work and resume

Checks-only input request: “Fix this validator diagnostic locally and add its focused test.” When the existing bounded escape applies, put the literal request/source, current reviewed intent revision and local scope in `checks.md` next to Intent. Continue within that authority; do not invent a plan or ask an additional approval. A drafting plan may pass its presentation gate before approval (`tools/test_tlc_validators.py:173-179`). A real sibling plan, when present, remains the owner; adding a checks receipt cannot override its missing approval (`:158-171`). For modular input, record the authorizing decided request in `.tasks/<name>.md#approval`, link that source from checklist Sources and inspect its authority before dependent Build; no duplicate approval registry/receipt.

Resume inputs and resulting actions: unchanged reviewed scope plus genuine receipt -> continue with the same receipt; choose a helper location or append a newly discovered noncontradictory extension point -> record the detail/additive row and continue; change paid access behavior to immediate revocation outside approval -> ask only for that behavior change, leave dependent edits blocked; separately prescribed implementation approval absent -> remain blocked even if feature shape was approved. Existing feature or stage approval does not authorize push/deploy. Sources: construction constraints `:19-55`; Lean checks `:24-26,250-265`; Lean build `:36-61`; modular implement `:67-70,100-104`; checklist `:116-120`.

### S5 — Receiving-turn decisions and dispatch write order

Mid-build fixture reply: “Keep the existing seven-day retention; do not add export.” Before dependent action, both Lean and modular paths record the actual answer/source, settled retention and exclusion in the existing owning decision fields, with a Handoff pointer/status for the affected check. They do not rewrite frozen checks silently and do not postpone the write until the batch completes. A conflict with a frozen criterion returns for targeted contract resolution rather than unilateral edits.

Coordinator preparing verification writes phase/stage, full check set, checked revision, accepted selection and `pending dispatch` in the existing Handoff before calling the host. Successful result W17/running -> immediately replace intent-only state with actual W17/observed status; failed send -> record `send failed`, error and whether no assignment is proven. On report receipt, write returned status, report location and checked revision before consuming it. Terminal work gets terminal evidence/ownership release before replacement. No new scheduler is proposed. Both entrypoints route to shared context-handoff `:8-51`; Lean build `:14-17,167-169` and modular implement `:87-90` retain the receiving-turn obligation.

### S6 — Recovery dispatch state matrix

| Observed input after reloading Handoff and available host reports | Proposed next authorized action | Owner/limit |
| --- | --- | --- |
| Pre-send interruption; pending intent; host positively confirms no send/assignment | Send recorded scope once; immediately record returned real identity/status | coordinator, same accepted selection |
| Actual W17 recorded; host confirms W17 live | Retain W17 ownership and wait by W17 identity | no replacement/second Verifier |
| Send failed; host positively confirms no worker exists | Record failure, retry once within accepted choices, then record actual result | no fabricated successful send |
| Host report has returned at checked revision R | Record returned status/report/revision, then consume it | stale/changed relevant inputs reselect proof, not blind reuse |
| Host definitively terminated and cannot return | Record terminal evidence and release ownership, then replace within accepted selection | replacement follows proof of lost owner |
| Host unavailable, pending without proof, or send outcome/ownership uncertain | Record ownership unverifiable; block duplicate dispatch and resolve through host/operator evidence | do not pretend a worker is running, and do not assume no worker exists |

Authority: `context-handoff.md:31-51,58-68`. The authoritative table has six states, not merely the five grouped states in frozen Coverage; definitive termination is independently covered here under C8/AC12. Final verification is still coordinator-dispatched, independent of the builder.

### S7 — Genuine CSS viewport versus a resized wider capture

Input A: a real render at CSS 390x844, scroll 0,0, DPR 2, source scale 1x, known browser/OS, fixtures, loaded fonts/assets and theme, with reference/full-page/actual-viewport captures. Proposed action: structurally accept complete provenance/files, then open source and captures and compare every contracted state/property; reproduce focus/sticky reachability at the actual CSS viewport. A DPR-2 raster may be 780x1688; CSS viewport is not inferred from PNG dimensions.

Input B: a 1440x900 CSS render later resized/cropped into a 390x844 PNG, with the same final filename/dimensions as A. Proposed action: reject it as evidence of the 390x844 render and require a genuine recapture. Responsive column changes, wrapping and sticky/focus reachability are not established by scaling pixels. Even a structurally accepted row cannot prove authenticity/fidelity. This is an independent provenance judgment applying shared UI `:126-141,153-161` and modular screens `:31-35`, not an image-detector claim.

No actual application source/capture pair exists in this feature, and none was visually inspected or claimed matched. Parent smoke generated uniform 390x844 PNGs; canonical tests use tiny local PNGs. Those prove only existing files and schema, not a genuine browser render, visual match, complete matrix or interaction. No product visual match is claimed.

### S8 — Pair-level evidence reuse and invalidation

Fixture contracted pairs: checkout/idle at 390x844 and 1440x900; checkout/error at 390x844; catalog/populated at 1440x900. Original revision/captures/environment are known.

- Unrelated README-only change, with no imports/content generator/assets/config/runtime/fixtures influencing those screens: retain all four pairs only after recording that dependency/input equivalence and original evidence revision. A new HEAD alone is not invalidation.
- Shared checkout typography/layout style changes: invalidate and recapture all three checkout pairs; catalog may be retained only if import tracing proves it does not consume the changed style. If it consumes that shared global style, invalidate catalog too. A matching capture filename does not help.
- Binding checkout source revision changes: invalidate affected checkout comparisons and reopen their source/property/matrix coverage; do not rewrite old comparison text to the new revision. Unchanged independent catalog source/render inputs may retain their evidence with the explicit reason.
- Fixture/theme/font/browser/DPR or implementation changes that influence a pair likewise invalidate that pair; selected interactive states must be reproduced where captures are insufficient.

Authority: shared UI `:142-147`, validation `:50-74`, Lean and modular verification `## Account for every proof`. This preserves coordinator-owned independent review and causal input-equivalence reuse rather than importing blanket every-HEAD invalidation.

## Coverage

Recomputed from the original request/approved criteria and the authoritative shared owners, then reconciled with actual parser/CLI/test dispatch. Not copied from checks Coverage. Plan Relations has no application entities; Surface adds no command/flag/signature and explicitly retains CLI exits; Landing has exactly two evidence contracts, both covered below. The pending/live/terminal states and exact UI fields were separately enumerated rather than inferred from successful fixtures.

| Set (size) | Recomputed from | Member -> proof | Unproven |
| --- | --- | --- | --- |
| Setup dispositions (4) | user-approved AC1-2; setup interview `:42-53` | keep C1/S1; change C1/S1; retire C1/S1; defer C1/S1 | - |
| Approval cases (4) | AC6, construction constraints `:33-37` | absent C4/R1-R3; empty C4/R1; template/example C4/R1 plus independent probe; complete C4/R1-R3 | subsection-marked example accepted, finding 1 |
| Native contract paths (3) | construction constraints `:19-21,48-51` | Lean plan C4; checks-only intent C5/S4; modular task linked by checklist C5/S4 | - |
| Recovery states (6) | context-handoff authoritative table `:40-47` | pending/no assignment C8/S6; proven live C8/S6; failed/no worker C8/S6; returned C8/S6; terminal/cannot return C8/S6; unavailable/uncertain C8/S6 | - |
| Capture roles (3) | AC14 and shared UI `:130-132,156-159` | reference C10/R1; full-page C10/R1; actual viewport C10/R1; each file removal has an exit assertion | mixed-schema row bypasses all roles, finding 2 |
| Evidence input classes (3) | AC15, shared UI `:142-147` and validation `:61-74` | unrelated inputs C11/S8; rendering inputs C11/S8; binding source C11/S8 | - |
| Profiles (3; 2 families) | project standard floor; validator `PROFILES`; effective UI branch | light C11 `test_visual_non_ui_profiles_do_not_require_captures`; standard same; ui C10 `test_visual_provenance_and_results_reach_completion_cli` | - |
| Visual columns (11) | shared UI literal table `:149-161` | source/revision; source scale; implementation revision; route/state; viewport/scroll; environment; reference capture; full-page capture; viewport capture; comparison; result — independently blanked in C10 test `:182-201` | incomplete second-table schema ignored, finding 2 |
| Required approval field groups (4) | construction constraints `:33-37` | Decision C4; Reviewed revision C4; Scope C4; Source-or-Date C4; fixture outcomes asserted at `tools/test_tlc_validators.py:83-112` | field values inside explicitly marked Example are incorrectly treated as operative, finding 1 |
| Planning decision classes (4) | AC4, shared project requirements `:31-35` | unanswered product C3/S3; explicit delegation C3/S3; binding departure C3/S3; routine reversible convention C3/S3 | - |
| CLI exits (3) | approved plan Surface `:47`; validators actual main/_resolve | accepted 0 C4/C5/C10/C11 tests; invalid 1 C4/C10 tests; unresolved target 2 selftest tooling `:322-337` and pre-build main `:400-406` | - |
| Helper distribution/consuming assemblies (3) | imports plus actual copying/distribution assembly | direct gates import shared helper (`validate_checks.py:58,244`; completion `:50,146`); isolated lifecycle copies helper (`tools/test_wtk_lifecycle.py:12-20`, R1); full skill distribution recursively copies scripts (`tests/skills/distribution.test.js:24,35-39`, manifest `package.json:18-34`, R2) | - |

Twelve sets recomputed. The four setup-policy outcomes are explicitly exercised on the approved two-area scenario; the eleven-row area menu is discovery guidance, not eleven necessarily applicable areas. The scope does not claim a statistical guarantee that every future agent will obey instructions. No application screens/entities/events or startup server assemblies are added. No new enum/message is emitted without a consumer; native helper errors flow into both validators and their CLI exit dispatch. The visual-table silent-discard branch itself is finding 2.

## Test policy rows

The frozen Test policy is one prose contract; its independent obligations are expanded here without changing it. Tests remain in canonical owners; instruction judgments are concrete scenarios rather than permanent text assertions.

| Row | Files it classifies | Required proof | Expectation met |
| --- | --- | --- | --- |
| Artifact/gate outcomes at owning boundary | native_evidence.py, validate_checks.py, validate_verification.py; tools/test_tlc_validators.py | Existing owner extended, actual CLI exit/diagnostic assertions for both gates and all relevant cases | no — ordinary cases pass R1/R3, but Example heading and mixed schemas have uncovered outcomes, findings 1-2 |
| Existing Lean mutant controls | selftest.py; fixtures/plan.md and visual.md | Clean baselines/negative controls/tooling, relevant invalid-artifact mutants killed | yes — R1 reports 57 killed/0 survived, including new approval/visual controls; inspected `selftest.py:38-49,214-232,377-458` |
| Instruction-product semantics | setup, shared guidance, Lean/modular phase instructions/templates | Independent concrete inputs, questions and resulting dispositions; no prose-string test as semantic proof | yes — S1-S8 above; 10 non-failing checks have located sources and judgment limits |
| Real consumer-visible smoke | actual CLI gates plus disposable complete projects | Exit and decisive diagnostic at the consumer boundary, not parser-only assertions | yes — independently recovered R3 has 15 expected exits; additional final probes expose 3 wrong exits rather than hiding them |
| Import/distribution cutover | lifecycle fixture copier; package and skill distribution | Helper shipped/copied to isolated consumers; old visual contract not intentionally supported | no — helper composition and R1/R2 pass, but silently ignored old-schema rows violate complete cutover, finding 2 |

Unique visual assertions retained from the replaced old test include missing captures/table, complete evidence, blank provenance, material drift/unverified result, binding-source contradiction and multiple supplied states. The new owner exercises these through actual CLIs (`tools/test_tlc_validators.py:181-231`); it does not merely weaken the old parser test. No compatibility alias/old-column fallback was added. The remaining mixed-schema silent skip is specifically reported, not passed as a compatibility promise.

## Swept existing

The frozen Swept contains no `existing` or `n/a` rows requiring inherited-behavior assertions: all nine dimensions map to C checks. Independently reconciled: validation C4/C5/C10; failure modes C4/C8/C10; idempotency C1/C6/C8; authorization C3-C6/C12; concurrency C7/C8; lifecycle C7/C8/C11; dependency failure C2/C8/C10; transitions C1/C6-C8; observability C4/C7/C8/C10/C12. Existing coordinator ownership, no builder dispatch and impact-based reuse were reread in both verification entrypoints and shared validation, not inferred from the patch summary. CLI target-resolution behavior remains at its original boundary.

## Reuse, security and visual limits

The closest prior approval responsibility was the shared construction procedure, not another executable receipt validator. The new 76-line `native_evidence.py` is the narrow shared owner used by both gates; the completion parser reuses its fence/value helpers. Existing Markdown parser/table/CLI composition and test suite remain owners; no registry, dispatch service, screenshot framework or second proof pipeline was introduced. Traced error lists through pre-build `check_file -> main` and completion `_check_feature -> main`; both return 1 on collected errors, not dropped messages. Lifecycle `make_feature` and skill-distribution assembly include the new helper. No confirmed duplicate implementation or direction violation in this feature; no repository-wide reuse audit claimed.

Security scope is local native artifacts and capture paths (plan S1/S6). `tools/test_tlc_validators.py:233-252` rejects URLs/directories and treats a shell-looking filename as data; no execution path or network call is introduced. Absolute/relative literal paths and spaces are intentional, with resolution beside the report. Threat model is not triggered by S1/S6 alone (`security.md:101-104`). No Critical/High security finding was identified (0/0) in this inspected scope; approval parsing is procedural, not an authentication boundary. No broader certification is claimed.

Visual fidelity: no actual application source/capture matrix is contracted by this feature, so actual inspected product pairs = 0 and no application visual match is claimed. Scenario S7 is an authenticity judgment; generated PNGs in R1/R3 prove only schema/files. Both independent verification paths still require opening images, complete contracted pairs and real-viewport interaction reproduction. Missing/changed product evidence would block those obligations; structural PASS is insufficient.

## Evidence reuse and proof selection

R1/R2/R3 were executed after the builder returned and before commit fb85f32. Independently recovered original outputs and smoke code from P, not merely Handoff. P lines 350/358/361 contain the results; lines 376-384 show only checks Handoff edits followed by the feature commit, and no intervening product edits. A read-only diff from fb85f32 to the current tree over skills/tools/tests/package/lock/docs shows no product/test/config delta; only checks Handoff changed to record actual dispatch. This Handoff is not a fixture input to these suites.

Inspected causal inputs: both gates import the new helper, owning tests construct their fixture projects from scripts/fixtures and validated workflow_route, selftest uses the shipped validators/tooling/fixtures, lifecycle copies completion+helper+native artifacts and invokes the real close helper, distribution recursively copies full skill trees and checks package/aliases, phase tests consume changed guidance and native route references. No package/lock/runtime configuration changed in the feature; current Python 3.15.1 and Node v22.23.1 match recorded runs. No application service/database/browser or external mutable fixture is involved. The independent final batch hashes all 31 feature files before/after and confirms unchanged inputs. Commit/actor changes alone therefore do not invalidate R1/R2/R3. Known tests passing does not settle the two newly found omitted scenarios.

Selector evidence: static AST enumeration finds exactly 16 unittest test methods, equal to R1 executed total with no skips. Five named methods match `-k approval`: test_approval_receipts_reach_both_cli_gates, test_approval_execution_route_does_not_authorize_feature_shape, test_approval_checks_only_uses_intent_without_synthetic_plan, test_approval_plan_cannot_be_bypassed_by_checks_receipt, test_approval_is_not_required_before_presenting_plan. Three match `-k visual`: test_visual_provenance_and_results_reach_completion_cli, test_visual_paths_are_literal_local_data, test_visual_non_ui_profiles_do_not_require_captures. The parent full invocation executed all eight as part of those 16, rather than relying on a selector that might hit nothing. Original assertions, setup, imports and controls were read before reuse. No unchanged full suite was rerun solely for a fresh actor.

Selected fresh work was one isolated final batch: three distinct source-code regressions against canonical tests, plus the two uncertain structural edge cases through three actual CLI invocations. No builds/lint/formatters or mid-flight tests were run. The report completion gate is intentionally left to the coordinator per assignment.

## Faults injected

Independent standard-profile fault injection used a disposable copy of the required validators, fixtures and canonical test module outside the repository, not mutation of the actual tree or stash. Parent 57 artifact mutants are reused executable evidence but are not represented as this independent source-fault exercise.

| Mutation | Location | Killed |
| --- | --- | --- |
| Skip required Decision/Reviewed revision/Scope value validation (`if not usable_value(...)` -> false) | isolated native_evidence.py:70 | yes — actual `WorkflowValidatorTests.test_approval_receipts_reach_both_cli_gates -v` exited 1; five named invalid-value subtests failed `assertEqual(returncode, 1)` at `tools/test_tlc_validators.py:105` with observed 0 |
| Treat DPR as constant 1 instead of reading evidence | isolated validate_verification.py:251 | yes — `WorkflowValidatorTests.test_visual_provenance_and_results_reach_completion_cli -v` exited 1; no-DPR and zero-DPR subtests failed the exit-1 assertion at `tools/test_tlc_validators.py:222` |
| Remove local file existence requirement | isolated validate_verification.py:257 | yes — `WorkflowValidatorTests.test_visual_paths_are_literal_local_data -v` exited 1 at `tools/test_tlc_validators.py:249` when a directory incorrectly passed as a capture |

Each test name appeared in verbose executed output; each failure was an expected AssertionError, not an import/harness error. Three independent mutations, three killed, zero survivors. Original source was restored within scratch before the unmutated probes. Scratch `/var/folders/lc/_v1mn5h560d2tsmz474y7d1c0000gn/T/wtk-independent-faults-4dcf46fz` was removed by TemporaryDirectory and its absence asserted. SHA-256 baselines for all 31 feature files matched afterward. The disposable batch driver was removed after report creation; no repository source mutation was required.

## Gate

**R1 — reused, independently inspected original output:** `python3 tools/test_tlc_validators.py && python3 .agents/skills/wtk-lean/scripts/selftest.py && python3 tools/test_wtk_lifecycle.py` exited 0; 16 owning tests in 2.393s; selftest 57 killed, 0 survived, clean baselines/controls/tooling; 5 lifecycle tests in 0.205s. Parent recorded command duration 5.452s (P line 358 / entry 1fe65518). Two ResourceWarnings came from unclosed completion-validator reads; tests passed. No warning suppression or unrelated fix was introduced.

**R2 — reused, independently inspected original output:** `node --test --test-name-pattern='full WTK set|approved execution selection' tests/skills/distribution.test.js && python3 tools/test_phase_skills.py` exited 0; the two individually named distribution tests passed (TAP duration 147.522458ms), then 7 phase tests passed. Parent recorded combined command duration 606ms (P line 350 / entry b0e36fd9).

**R3 — reused, independently inspected actual smoke code/result:** coordinator Eval `run_guideline_recovery_cli_smoke()` invokes `python3 <actual-skill-scripts>/<validate_checks|validate_verification>.py billing --root <temporary-project> --strict`. P entry c9b46e5d, line 361, contains exact argv construction and output; duration 526ms. Missing approval, fenced example and placeholder each exit 1 in both gates with approval diagnostics; complete receipt exits 0 in both; checks-only intent/receipt without plan exits 0 in both; non-UI without captures exits 0; UI with generated local PNGs and complete schema exits 0; missing implementation revision, viewport file and DPR each exit 1 with the specific visual diagnostic. Fifteen expected exits; temporary project removed. These do not cover the two findings.

**Fresh final batch:** `python3 /tmp/wtk-feature-verifier-batch.py` ran at 2026-10-27T00:44:21.668248Z–00:44:24.084278Z; measured internal duration 2.416s, tool wall time 2.55s. Driver exit 0 means the isolated experiment completed, not feature acceptance. Three canonical tests ran against three independent faulty implementations and each exited 1 as required to kill its mutant. Then unmodified copied validators produced three wrong exit-0 results: Example subsection in pre-build; Example subsection in completion; mixed current/legacy visual tables with missing captures in completion. Expected contract exit is 1 for each. Full decisive output is in the FeatureVerifier tool transcript for this command; fixture construction and exact child commands are preserved there. No repeated full suite.

**Feature completion gate:** not run by this Verifier; coordinator owns `python3 .agents/skills/wtk-lean/scripts/validate_verification.py guideline-review-recovery --strict`. The truthful FAIL report must block completion until the ranked findings are dispositioned and affected behavior is independently rechecked. No claim that a final report gate passed.

## Execution metrics

Stage: technical verification, attempt/round 1, full feature. Accepted provider/model/effort: codex/inherited/inherited, child defaults unknown in advance and no effort override, as explicitly accepted in the real ask receipt. Actual exposed checking model: openai-codex/gpt-6.1-sol; actual effort and billing tier are unavailable. No agents launched, no implementation/remediation/QA/delivery work performed by this actor.

Actor/session: FeatureVerifier / `01a17acd-9a34-7581-8937-35d4ef0f2bd5`; harness 18.13.0. Session start 2026-10-27T00:40:57.140Z. Metrics snapshot 2026-10-27T00:45:05.895537Z, last usage event 00:45:05.811Z: 248.756 seconds observed actor interval, excluding subsequent report/finalization. Baseline counters were not captured at entry; the late snapshot is self-only session cumulative, not a fabricated stage delta. Source: allowlisted actual assistant `message.usage` records in the assigned `FeatureVerifier.jsonl`, deduplicated by provider responseId (20 finalized requests), not context occupancy or parent-inclusive counters. Raw ordinary input 176520; cached reads 2102528; cache writes 0; output 10961; total 2290009. Normalized input including cache = 2279048. Final report/final response usage is not in this snapshot; totals are partial and no parent/child totals are added. Reset comparison unavailable without a captured baseline.

Source checks: CODEX_THREAD_ID and explicit SESSION_FILE are absent. CODEX_HOME is set in this worker environment, but without a session identity the Codex token_count reader cannot select a session safely; no fallback/unrelated Codex logs were read. The already assigned OMP worker transcript exposes finalized per-request usage for this exact actor, so those actual counters are used rather than declaring all tokens unavailable. No telemetry discovery outside this assigned actor and the explicitly authorized approval/gate parent receipt was performed.

| Stage | Observed elapsed interval | Tokens | Rounds |
| --- | --- | --- | --- |
| Technical verification | 248.756s through snapshot, partial closing interval | 2290009 self-only session cumulative; input including cache 2279048 / cache-read subset 2102528 / output 10961 | 1 full pass |

Validation overhead included above: one selected final batch, 2.416s internal / 2.55s tool wall, with three narrow mutant-proof invocations and three CLI edge probes; no full gate newly executed. R1-R3 are reused evidence, not new runs. One verification pass; two new P2 findings; no fix batch/completed loop performed by this actor. Coordinator disposition/return remains pending. Estimated token cost: unavailable — verified official applicable model rates and billing tier are not established; no invoice inferred from harness estimates. Actually billed: unavailable — no task-scoped billing evidence. Overall task lead time and other actor totals are coordinator-owned, not reconstructed here. Optimization evidence: unchanged parent suites were reused after causal inspection; no numerical savings or model-quality comparison is claimed.
