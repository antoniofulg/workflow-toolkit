# Adopt TLC spec-lean 2.2 verification and resume improvements

## Approval

- Decision: "Aprovado" - user approved the plan, the presence-only approval gate, and the update of the Approval row in knowledge/wiki/decisions/workflow-toolkit-contract.md
- Source: conversation turn answering the plan review question, 2026-11-11
- Date: 2026-11-11
- Reviewed revision: plan.md sha256 b2f24c83c604 on base e61c460a
- Scope: S1-S7 local edits and local commits on feat/tlc-lean-2-2-adoption; push, PR, merge and release follow wtk-ship only when invoked

## Problem

A Lean feature that runs long loses state the chat held. After a compaction the builder can start
coding with no approval on record, and nothing it runs reminds it that the Verifier or the screens
judge is still owed: the next step lives only in a reference it read hours earlier.

Verification is slow and partly mechanical. The fresh Verifier reruns and batches every proof
itself (`wtk-lean/references/verify.md` step 2), checks by hand that each named test ran, and under
`standard` and `ui` always injects up to five faults, even in code where a weak test costs little.
Upstream measured the same split: Lean verification fell from about 63 min to 9-25 min once a
script ran the proofs and the Verifier only judged (TLC release post, 2026-10). A filter that
selects nothing still exits 0 on several runners, so a typo can pass a check.

Screens are judged by the same Verifier that reads the code and the diff, so a difference can be
explained away instead of reported, and nothing bounds how many fix rounds a screen gets.

Fault injection by default also pushes in the wrong direction for projects that already carry too
many tests: every survivor becomes another test.

When this ships, a resumed agent refuses to build without the recorded approval and is told what
the feature still owes after every commit; a script runs every proof once at `HEAD` and the
Verifier spends its time judging each check's test; screens are judged item by item by a judge
that never sees the code; faults run only where a weak test costs most.

## Flow

Reuses the existing Lean validators, the `## Approval` receipt, the verify core and the UI
acceptance procedure; it adds one script and one judge, and no second schema.

1. plan approved -> `## Approval` receipt (exists) in `plan.md` or beside `## Intent`
2. `validate_checks.py` (exists) - refuses a feature with no receipt; with `--execute` runs the `Build:` line once (door 2)
3. builder commits -> `check_commit.py` (exists) - validates, then prints what each open feature still owes
4. `check_proofs.py` (new, door 1) - runs every `Run` group and lone proof once at a clean `HEAD`, writes `proofs.md`
5. Verifier (exists) - reads `proofs.md`, judges each check's test in `## Checks` with `Holds` (door 3), injects faults only for `Risk:` checks (door 4)
6. screens judge (new sub-agent, door 5) - when a criterion cites a binding capture, writes `screens.md`
7. out: `validate_verification.py` (exists) - exit 0 only when `proofs.md` is green at `HEAD`, every check `Holds: yes`, and `screens.md` matches at `HEAD` under `ui`

## Impact

| Front | What changes |
| --- | --- |
| domain | existing term: `standard` profile meant "standard plus one fault per assertion surface", now means faults only for checks named on the `Risk:` line - `validate_verification.py`, `verify-core.md` and `test-contract.md` branch on it |
| domain | existing term: Approval meant "written convention no validator judges" (2026-11-06 generalization decision), now its presence and a non-empty `Decision` gate the build; authenticity stays the Verifier's judgment |
| domain | new term: `Run` group - one project test command run once, whose output each `run` proof greps for its pass line, lives in `checks.md` |
| domain | new term: screens judge - a fresh sub-agent that sees captures and pictures only, lives in `wtk/references/ui-ux.md` |
| stored data | nothing to migrate: feature directories are transient; an in-flight feature without the new lines fails its gate and gets them added |
| shared verify core | `verify-core.md` fault injection and `test-contract.md#mutation` change for the modular route too; pruning and `wtk-test-review` keep mutation mandatory |
| provenance | `.skill-meta.json` re-pins to TLC `e74dc8a`; `NOTICE.md` and the Lean NOTICE list the new adaptations |

## Relations

`None - no stored-data shape change`

## Surface

| Interface | In | Out | Outcomes |
| --- | --- | --- | --- |
| `check_proofs.py <feature>` | `checks.md` `Run` and `Proof` lines, git `HEAD` | `.specs/features/<feature>/proofs.md` | exit `0` all pass, `1` a proof failed or `no test ran` or dirty tree, `2` feature unresolved |
| `validate_checks.py <feature> [--execute]` | `checks.md`, `plan.md` `## Approval`, `Build:` line | messages | exit `0`, `1` missing receipt or build red, `2` unresolved |
| `check_commit.py` | commit message | validation, then an owed-step line per open feature | exit `0`, `1`, `2` |
| `checks.md` lines | `Build:`, `Run <name>:`, `Proof: run <name>` with a pass line, `Risk:` | parsed by the validators | `accepted`, `error` |
| `verification.md` `## Checks` | columns `Check`, `Test`, `Holds` | read by the gate | `yes`, `no`, `unsure` |
| `screens.md` | `**Round**`, `**HEAD**`, verdict table, one inventory per picture | read by the gate | `matches`, `diverges` |

## Landing

| One-way door | Literal shape | Alternative rejected |
| --- | --- | --- |
| proof runner artifact | `check_proofs.py` writes `proofs.md`: `**HEAD**`, `**Shell**`, `\| Proof \| Result \| Line \|`, `## Output` with the last 15 lines of each run | the Verifier reruns proofs itself - the slowest mechanical step, and it re-derives "the test ran" by hand |
| proof grammar | `Run <name>: <cmd>` once per group; `Proof: run <name> \| <words>` passes when the words appear in order on one ANSI-stripped output line, else `no test ran`; a lone `Proof: <cmd>` is judged by its exit code | per-runner adapters - each is code that tracks someone else's CLI (upstream removed theirs) |
| build preflight | `Build: <cmd>` line in `checks.md`, run once by `validate_checks.py --execute` before the first change | trusting a green baseline - a red build then looks like the feature's fault |
| Verifier judgment table | `## Checks` gains `Test` and `Holds` (`yes` / `no` / `unsure`); `no` is a finding, `unsure` requires a fault on that check | a mutation score - samples a few rules and costs a suite run per mutant |
| risk-scoped faults | `Risk: <none \| C3, C7> - <reason>` required under `standard` and `ui`; faults run for listed checks and `unsure` rows, cap five | faults on every feature - slowest step, and survivors in low-risk code inflate the suite |
| survivor policy | outside a `Risk:` check a survivor is recorded `accepted - <reason>`, not turned into a test | kill every survivor - grows the suite against the project's test-reduction goal |
| screens judge | fresh sub-agent given the binding captures, the `<capture>.running.png` pictures and the plan's departures, never code, diff or handoff; inventory rows `same` / `differs` (controls, arrangement, copy, drawing, render), `differs - resized` when a shared label reads smaller; verdict pinned to `**HEAD**`; round 2 reopens `differs` rows and marks regressions; no round 3 | the Verifier judging screens beside the code - the code explains a difference away |
| approval gate | `validate_checks.py` fails without `## Approval` holding a non-empty `- Decision:` | prose-only receipt - the chat that held the approval does not survive compaction |

- Nothing else in this change is hard to reverse

## Criteria

### S1: The approval survives a compaction (P1)

A resumed builder cannot start building a feature whose approval was never recorded.

**Acceptance Criteria**

1. IF `plan.md` exists and has no `## Approval` section with a non-empty `- Decision:` line THEN `validate_checks.py` SHALL exit `1` naming the missing receipt
2. IF a checks-only feature has no `## Approval` section with a non-empty `- Decision:` line in `checks.md` THEN `validate_checks.py` SHALL exit `1` naming the missing receipt
3. WHEN the receipt is present with a non-empty `Decision` THEN `validate_checks.py` SHALL raise no approval error

**Independent test:** delete the receipt from the fixture plan and run `validate_checks.py`.

### S2: Every commit names what is still owed (P1)

After a passing commit message the agent reads its next obligation from the tool it just ran.

**Acceptance Criteria**

4. WHEN `check_commit.py` passes a message and a feature under `.specs/features/` has `checks.md` and no `verification.md` THEN it SHALL print one line naming that feature and `check_proofs.py`, the Verifier and, when a criterion cites a capture, the screens judge
5. WHEN no feature is open THEN `check_commit.py` SHALL print no owed-step line
6. IF the message fails validation THEN `check_commit.py` SHALL exit `1` and print no owed-step line

**Independent test:** a fixture root with one open feature and a valid message.

### S3: A script runs every proof once (P1)

The Verifier receives a mechanical proof record instead of rerunning proofs.

**Acceptance Criteria**

7. WHEN `check_proofs.py <feature>` runs on a clean tree THEN it SHALL run each `Run` group exactly once and each lone proof once, one at a time with no timeout, and write `proofs.md` with the `HEAD` short sha
8. WHEN every word after `|` of a `run` proof appears in order on one ANSI-stripped line of its group's output THEN that proof's row SHALL read `pass`
9. IF no output line of its group matches a `run` proof THEN that row SHALL read `no test ran` and the script SHALL exit `1`
10. IF a lone proof exits non-zero THEN its row SHALL read `fail` and the script SHALL exit `1`
11. IF the working tree is dirty THEN `check_proofs.py` SHALL exit `1` without running any proof
12. IF a `run <name>` proof names no `Run <name>:` line THEN `validate_checks.py` SHALL exit `1`
13. IF `proofs.md` is missing, not all `pass`, or records a `HEAD` other than the current one THEN `validate_verification.py` SHALL exit `1`

**Independent test:** fixture checks with one green group, one renamed test and one failing lone proof.

### S4: A red build stops before the first change (P2)

**Acceptance Criteria**

14. WHEN `validate_checks.py <feature> --execute` runs and `checks.md` has a `Build:` line THEN it SHALL run that command once before reporting
15. IF that command exits non-zero THEN `validate_checks.py` SHALL exit `1` stating the build was red before any change
16. IF `checks.md` has no `Build:` line THEN `validate_checks.py` SHALL exit `1` naming the missing line

**Independent test:** a fixture whose `Build:` is `false`.

### S5: Screens are judged item by item by a judge that never sees the code (P1)

**Acceptance Criteria**

17. The UI acceptance procedure SHALL dispatch the screens judge as a fresh sub-agent whose inputs are the binding captures, the `<capture>.running.png` pictures and the plan's listed departures, and SHALL exclude source, diff and handoff
18. The screens judge SHALL write `screens.md` with `**Round**`, `**HEAD**`, a verdict table and one inventory per picture whose rows read `same` or `differs` with the category and what the picture draws instead
19. WHEN a label the capture also draws reads smaller in the picture THEN the judge SHALL mark that row `differs - resized`
20. IF the profile is `ui` and `screens.md` is missing, any verdict reads `diverges`, or its `**HEAD**` differs from the current `HEAD` THEN `validate_verification.py` SHALL exit `1`
21. IF `screens.md` records `**Round**` above `2` THEN `validate_verification.py` SHALL exit `1`
22. WHEN round 2 runs THEN the judge SHALL reopen only `differs` rows and mark a `same` row the new picture breaks `differs - regression`

**Independent test:** fixture `screens.md` at round 3, then with a stale `HEAD`.

### S6: The Verifier judges every test; faults only where risk is (P1)

**Acceptance Criteria**

23. The Verifier SHALL write one `## Checks` row per check with `Test` and `Holds` of `yes`, `no` or `unsure`
24. IF any check has no row, or a `Holds` other than `yes` without a closing commit, THEN `validate_verification.py` SHALL exit `1`
25. IF the profile is `standard` or `ui` and `checks.md` has no `Risk:` line THEN `validate_checks.py` SHALL exit `1`
26. WHEN `Risk:` lists checks or a row reads `unsure` THEN the Verifier SHALL inject at least one fault per listed check, up to five, and record each in `Faults injected`
27. WHEN `Risk: none` and no row reads `unsure` THEN `validate_verification.py` SHALL accept a report with no `Faults injected` rows
28. IF a survivor sits outside a `Risk:` check THEN the disposition `accepted - <reason>` SHALL be valid and require no new test
29. The pruning procedure and `wtk-test-review` SHALL keep a mutation or manual-fault run mandatory

**Independent test:** a `standard` fixture with `Risk: none` and no faults passes; one `unsure` row with no fault fails.

### S7: Provenance follows the adaptation (P2)

**Acceptance Criteria**

30. The Lean source metadata `.agents/skills/wtk-lean/.skill-meta.json` SHALL record `sourceCommit` `e74dc8a` with that commit's content hash
31. The Lean notice `.agents/skills/wtk-lean/NOTICE.md` SHALL list the proof runner, build preflight, compaction gates and screens judge as adapted material

**Independent test:** read both files.

## Traceability

| ID | Slice | Criteria | Status |
| --- | --- | --- | --- |
| LEAN-01 | S1 | 1, 2, 3 | Pending |
| LEAN-02 | S2 | 4, 5, 6 | Pending |
| LEAN-03 | S3 | 7, 8, 9, 10, 11, 12, 13 | Pending |
| LEAN-04 | S4 | 14, 15, 16 | Pending |
| LEAN-05 | S5 | 17, 18, 19, 20, 21, 22 | Pending |
| LEAN-06 | S6 | 23, 24, 25, 26, 27, 28, 29 | Pending |
| LEAN-07 | S7 | 30, 31 | Pending |

## Out of scope

| Excluded | Why |
| --- | --- |
| Removing the `light` / `standard` / `ui` profiles | upstream dropped them; ours are a recorded contract and still select UI obligations |
| A proof runner for the modular `wtk-implement` route | it has no scripts today; porting is its own change |
| Per-runner adapters or a built-in mutation tool | upstream paused both as fragile; projects declare their own mutation command |
| Changes to `tlc-spec-driven`-only material (`spec.md`, `tasks.md`) | WTK adapts the Lean skill |

## Assumptions

| Assumption | Chosen default | Rationale | Confirmed? |
| --- | --- | --- | --- |
| Approval gate reverses the 2026-11-06 decision | gate checks presence and a non-empty `Decision` only; the Verifier still judges who approved which revision; the decision record is updated | the gate is for resume, not authentication, which was the reason the old blocklist was dropped | y |
| Approval line shape | keep our `## Approval` receipt, not upstream's `**Approved**:` line | one receipt across Lean and modular routes | y |
| Where the screens protocol lives | `wtk/references/ui-ux.md` `## Verifying the built screen`, linked from Lean verify and `wtk-implement/references/screens.md` | one shared rule, per the context budget | y |
| Release | toolkit minor release after merge, through `wtk-ship` | matches 6.1.0 / 6.2.0 | y |

**Open questions:** none - all resolved or logged above.

## Observable

| Surface | Decision | Landing |
| --- | --- | --- |
| command `check_proofs.py` | output format and verbosity | AC 7 |
| command `check_proofs.py` | flags and defaults | AC 7 - one positional feature, `--root` as the other scripts |
| command `check_proofs.py` | exit codes | AC 9, 10, 11 |
| command `check_proofs.py` | what it prints when it fails halfway | AC 9, 10 - every row is still written, `## Output` keeps each run's tail |
| command `validate_checks.py --execute` | flag and default | AC 14 - off by default |
| command `validate_checks.py` | exit codes | AC 1, 12, 15, 16, 25 |
| command `check_commit.py` | output | AC 4, 5, 6 |
| document `screens.md` | structure | AC 18 |
| document `screens.md` | what the reader does next | AC 22 - the builder fixes only the rows named |
| document `verification.md` `## Checks` | structure | AC 23 |
| document `proofs.md` | what the reader does next | AC 13 - the Verifier reads it instead of rerunning |
| screen | n/a - this pack ships no screens |

## Sources

- TLC agent-skills `e74dc8a`, `tlc-spec-lean` 2.2.0 and PR #259 - the runner-agnostic proofs, the paused mutations, the screens judge and the resume gates
- TLC release post "tlc-spec-driven 4 e tlc-spec-lean 2" - the 63 -> 9-25 min verification evidence
