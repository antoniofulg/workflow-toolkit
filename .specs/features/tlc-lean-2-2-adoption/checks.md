# Adopt TLC spec-lean 2.2 verification and resume improvements - checks

Profile: standard
Plan: `.specs/features/tlc-lean-2-2-adoption/plan.md`
Build: `python3 .agents/skills/wtk-lean/scripts/selftest.py`
Risk: C9, C10, C14 - the gates that would turn a missing or stale proof into a false green

## Intent

34 checks in 7 slices · 8 one-way doors · 0 open

## Checks

Instruction-only claims are proven by a named contract test that the rule is present where it is
owned, and judged by the Verifier against the plan; a string match alone never settles behaviour.

### S1 - The approval survives a compaction

**C1** - `validate_checks.py` exits 1 naming the receipt when `plan.md` has no `## Approval` with a non-empty `- Decision:` (LEAN-01, AC 1)
Proof: `python3 tools/test_tlc_validators.py -k test_checks_rejects_plan_without_approval`

**C2** - `validate_checks.py` exits 1 for a checks-only feature whose `checks.md` has no non-empty `- Decision:` (LEAN-01, AC 2)
Proof: `python3 tools/test_tlc_validators.py -k test_checks_only_rejects_missing_approval`

**C3** - A receipt with a non-empty `Decision` raises no approval error (LEAN-01, AC 3)
Proof: `python3 tools/test_tlc_validators.py -k test_checks_accepts_recorded_approval`

**C4** - An `## Approval` with an empty `- Decision:` is rejected like a missing one (LEAN-01, AC 1)
Proof: `python3 tools/test_tlc_validators.py -k test_checks_rejects_empty_decision`

### S2 - Every commit names what is still owed

**C5** - After a valid message, `check_commit.py` prints one line naming each feature with `checks.md` and no `verification.md`, with `check_proofs.py` and the Verifier (LEAN-02, AC 4)
Proof: `python3 tools/test_tlc_validators.py -k test_commit_names_owed_steps_for_open_feature`

**C6** - The owed line adds the screens judge when that feature's plan cites a capture (LEAN-02, AC 4)
Proof: `python3 tools/test_tlc_validators.py -k test_commit_names_screens_judge_when_capture_cited`

**C7** - With no open feature, no owed line is printed (LEAN-02, AC 5)
Proof: `python3 tools/test_tlc_validators.py -k test_commit_prints_nothing_owed_without_open_feature`

**C8** - An invalid message exits 1 and prints no owed line (LEAN-02, AC 6)
Proof: `python3 tools/test_tlc_validators.py -k test_commit_invalid_message_prints_no_owed_line`

### S3 - A script runs every proof once

**C9** - Each `Run` group runs exactly once and each lone proof once, and `proofs.md` records the `HEAD` short sha (LEAN-03, AC 7)
Proof: `python3 tools/test_tlc_validators.py -k test_proofs_run_each_group_once_and_record_head`

**C10** - A `run` proof whose words appear in order on one ANSI-stripped output line reads `pass`; words out of order or split across lines read `no test ran` and exit 1 (LEAN-03, AC 8, AC 9)
Proof: `python3 tools/test_tlc_validators.py -k test_proofs_match_pass_line_in_order`
Proof: `python3 tools/test_tlc_validators.py -k test_proofs_unmatched_line_is_no_test_ran`

**C11** - A lone proof exiting non-zero reads `fail` and the script exits 1, still writing every row (LEAN-03, AC 10)
Proof: `python3 tools/test_tlc_validators.py -k test_proofs_failing_lone_proof_fails_and_writes_all_rows`

**C12** - A dirty working tree exits 1 before any proof runs (LEAN-03, AC 11)
Proof: `python3 tools/test_tlc_validators.py -k test_proofs_refuse_dirty_tree`

**C13** - A `run <name>` proof with no `Run <name>:` line fails `validate_checks.py` (LEAN-03, AC 12)
Proof: `python3 tools/test_tlc_validators.py -k test_checks_rejects_run_proof_without_group`

**C14** - `validate_verification.py` exits 1 when `proofs.md` is missing, has a non-`pass` row, or records another `HEAD` (LEAN-03, AC 13)
Proof: `python3 tools/test_tlc_validators.py -k test_verification_requires_green_proofs_at_head`
Proof: `python3 tools/test_tlc_validators.py -k test_verification_rejects_proofs_missing_a_check`

**C15** - An unresolved feature exits `check_proofs.py` with 2 (LEAN-03, AC 7)
Proof: `python3 tools/test_tlc_validators.py -k test_proofs_unresolved_feature_exits_2`

**C34** - A `Run` group that exits non-zero fails its proofs even when their pass lines printed (LEAN-03, AC 10)
Proof: `python3 tools/test_tlc_validators.py -k test_proofs_run_group_nonzero_exit_fails`

### S4 - A red build stops before the first change

**C16** - `--execute` runs the `Build:` line once and passes on exit 0 (LEAN-04, AC 14)
Proof: `python3 tools/test_tlc_validators.py -k test_checks_execute_runs_build_once`

**C17** - A red `Build:` exits 1 stating the build was red before any change (LEAN-04, AC 15)
Proof: `python3 tools/test_tlc_validators.py -k test_checks_execute_red_build_stops`

**C18** - A missing `Build:` line exits 1 naming it (LEAN-04, AC 16)
Proof: `python3 tools/test_tlc_validators.py -k test_checks_rejects_missing_build_line`

### S5 - Screens judged item by item by a judge that never sees the code

**C19** - The UI procedure dispatches a fresh screens judge given captures, pictures and listed departures, and excludes source, diff and handoff (LEAN-05, AC 17)
Proof: `python3 tools/test_phase_skills.py -k test_screens_judge_inputs_exclude_code`

**C20** - The procedure defines the `screens.md` schema with `**Round**`, `**HEAD**`, the verdict table and per-picture inventories using the five categories (LEAN-05, AC 18)
Proof: `python3 tools/test_phase_skills.py -k test_screens_report_schema_is_defined`

**C21** - A smaller shared label is a `differs - resized` row (LEAN-05, AC 19)
Proof: `python3 tools/test_phase_skills.py -k test_screens_resized_tell_is_defined`

**C22** - Under `ui`, a missing `screens.md`, a `diverges` verdict or a stale `**HEAD**` exits 1 (LEAN-05, AC 20)
Proof: `python3 tools/test_tlc_validators.py -k test_verification_ui_requires_matching_screens_at_head`

**C23** - `**Round**` above 2 exits 1 (LEAN-05, AC 21)
Proof: `python3 tools/test_tlc_validators.py -k test_verification_rejects_third_screens_round`

**C24** - Round 2 reopens only `differs` rows and marks a broken `same` row `differs - regression` (LEAN-05, AC 22)
Proof: `python3 tools/test_phase_skills.py -k test_screens_second_round_is_bounded`

**C25** - Non-`ui` profiles carry no screens obligation (LEAN-05, AC 20)
Proof: `python3 tools/test_tlc_validators.py -k test_visual_non_ui_profiles_do_not_require_captures`

### S6 - The Verifier judges every test; faults only where risk is

**C26** - The Lean verify procedure requires one `## Checks` row per check with `Test` and `Holds` (LEAN-06, AC 23)
Proof: `python3 tools/test_phase_skills.py -k test_verifier_judges_each_check_test`

**C27** - A check with no row, or `Holds` `no` / `unsure` without a closing commit, exits 1 (LEAN-06, AC 24)
Proof: `python3 tools/test_tlc_validators.py -k test_verification_requires_holds_yes_per_check`

**C28** - Under `standard` or `ui` a missing `Risk:` line fails `validate_checks.py` (LEAN-06, AC 25)
Proof: `python3 tools/test_tlc_validators.py -k test_checks_rejects_missing_risk_line`

**C29** - A listed `Risk:` check or an `unsure` row with no `Faults injected` row exits 1 (LEAN-06, AC 26)
Proof: `python3 tools/test_tlc_validators.py -k test_verification_requires_faults_for_risk_and_unsure`

**C30** - `Risk: none` with no `unsure` row passes with no fault rows (LEAN-06, AC 27)
Proof: `python3 tools/test_tlc_validators.py -k test_verification_accepts_no_faults_without_risk`

**C31** - `killed`, `equivalent - <reason>` and `arid - <reason>` stay valid, and `accepted - <reason>` is valid only outside `Risk:` checks (LEAN-06, AC 28)
Proof: `python3 tools/test_tlc_validators.py -k test_fault_disposition_accepted_only_outside_risk`

**C32** - Pruning and `wtk-test-review` still require a mutation or manual-fault run (LEAN-06, AC 29)
Proof: `python3 tools/test_phase_skills.py -k test_pruning_keeps_mandatory_mutation`

### S7 - Provenance follows the adaptation

**C33** - `.skill-meta.json` records `sourceCommit` `e74dc8a…` with that tree's content hash, and the Lean NOTICE names the four adaptations (LEAN-07, AC 30, AC 31)
Proof: `python3 tools/test_phase_skills.py -k test_lean_provenance_pins_upstream`

## Coverage

| Set (size) | Member -> proof | Unproven |
| --- | --- | --- |
| `check_proofs.py` exit codes (3) | 0 C9 · 1 C10 C11 C12 · 2 C15 | - |
| proof row results (3) | `pass` C10 · `no test ran` C10 · `fail` C11 C34 | - |
| `validate_checks.py` new rejections (6) | missing receipt C1 C2 · empty decision C4 · run without group C13 · red build C17 · missing build C18 · missing risk C28 | - |
| `check_commit.py` outcomes (3) | owed line C5 C6 · nothing owed C7 · invalid C8 | - |
| `Holds` values (3) | `yes` C27 C30 · `no` C27 · `unsure` C27 C29 | - |
| screens verdicts (2) | `matches` C22 · `diverges` C22 | - |
| inventory categories (5) | controls C20 · arrangement C20 · copy C20 · drawing C20 · render C20 | - |
| `differs` qualifiers (2) | `resized` C21 · `regression` C24 | - |
| fault dispositions (4) | `killed` C31 · `equivalent` C31 · `arid` C31 · `accepted` C31 | - |
| `proofs.md` gate failures (3) | missing C14 · non-pass C14 · other `HEAD` C14 | - |
| Surface interfaces (6) | `check_proofs.py <feature>` C9 · `validate_checks.py <feature> [--execute]` C16 · `check_commit.py` C5 · `checks.md` lines C13 C18 C28 · `## Checks` C27 · `screens.md` C22 | - |

## Test policy

Omitted: the repo's test contract already answers the level - validator behaviour at the script CLI in `tools/test_tlc_validators.py`, instruction ownership in `tools/test_phase_skills.py`.

## Swept

- validation: C4, C13, C18, C28
- failure modes: C11, C17
- idempotency: n/a - every gate is a read or a fresh run; rerunning writes the same report
- authorization: n/a - local scripts with the invoking user's permissions
- concurrency: n/a - proofs run one at a time by design (C9); no shared state between gates
- data lifecycle: existing - feature directories stay transient under the lifecycle procedure
- dependency failure: C12, C17
- state transitions: C23, C24
- observability: C11 - `## Output` keeps each run's tail
- deploy compatibility: n/a - pack release; no backward compatibility per AGENTS.md
- performance budget: C9 - each group runs once

## Out of scope

- Removing the profiles - recorded contract, see plan
- A proof runner for `wtk-implement` - its own change
