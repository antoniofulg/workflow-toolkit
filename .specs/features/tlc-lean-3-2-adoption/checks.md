# Adopt the additive parts of TLC spec-lean 3.2 - checks

Profile: standard
Plan: `.specs/features/tlc-lean-3-2-adoption/plan.md`
Build: `python3 .agents/skills/wtk-lean/scripts/selftest.py`
Risk: C1, C7, C10 - a gate that reads the wrong file, a trailer pattern that matches too little or too much, and an untracked list that silently drops entries would each pass a weak test
Run selftest: `python3 .agents/skills/wtk-lean/scripts/selftest.py -v`

## Intent

24 checks in 5 slices · 2 one-way doors · 0 open

## Checks

Instruction-only claims (C5, C6, C23, C16-C21) are proven by a named contract test in
`tools/test_phase_skills.py` that the rule's key terms sit on one logical line of the file that owns
it, and are judged by the Verifier against the plan. The
[test contract](../../../.agents/skills/wtk/references/test-contract.md) forbids prose assertions by
default and allows them when the artifact is the product contract and no stronger gate owns it: in
this pack the instruction text is the product, and these rules have no script behind them. Each test
uses `owns()` with the rule's terms, never a whole sentence, so wording stays free; a matching string
alone does not prove agent behaviour, which is why the Verifier's `Holds` judgment reads the rule.

### S1 - The request survives in a file

**C1** - `validate_checks.py` exits 1 with an `ERROR` line naming `request.md` when the feature directory has none (LEAN-01, AC 1)
Proof: `python3 tools/test_tlc_validators.py -k test_checks_rejects_missing_request_record`

**C2** - A `request.md` with no non-blank line is rejected like a missing one (LEAN-01, AC 1)
Proof: `python3 tools/test_tlc_validators.py -k test_checks_rejects_blank_request_record`

**C3** - The scaffolded fixture feature, which now carries `request.md`, passes `validate_checks.py` with no request error (LEAN-01, AC 2)
Proof: `python3 tools/test_tlc_validators.py -k test_checks_accepts_request_record`

**C4** - `selftest.py` empties the fixture `request.md` as a mutant and the gate kills it (LEAN-01, AC 1)
Proof: run selftest | killed validate_checks: empty the request record

**C5** - The Lean plan reference instructs saving the request verbatim to `.specs/features/<feature>/request.md`, captures listed by path, before the first question, and the skill's artifact tree lists `request.md` (LEAN-01, AC 3)
Proof: `python3 tools/test_phase_skills.py -k test_lean_request_record_is_written_at_plan`

**C6** - The Lean verify reference names `request.md` as what the Verifier receives, what the dispatch brief hands over and what concerns derive from, no longer says "the original request", and instructs reading it sentence by sentence against what was built (LEAN-01, AC 4)
Proof: `python3 tools/test_phase_skills.py -k test_lean_verifier_reads_request_record`

**C23** - The Lean checks reference names `request.md` as the request handed to the fresh criteria reviewer (LEAN-01, AC 5)
Proof: `python3 tools/test_phase_skills.py -k test_lean_criteria_reviewer_gets_request_record`

### S2 - The commit check names trailers and untracked files

**C7** - A line after the header starting with `Co-Authored-By:` or `Made-with:` exits 1 with an `ERROR` line naming the trailer, table-driven over both names, each in the documented case, in lower case, with leading whitespace, and with a space before the colon (LEAN-02, AC 6)
Proof: `python3 tools/test_tlc_validators.py -k test_commit_rejects_agent_trailer`

**C8** - A body line that only mentions `Co-Authored-By` after other words is accepted (LEAN-02, AC 6)
Proof: `python3 tools/test_tlc_validators.py -k test_commit_accepts_trailer_words_mid_line`

**C9** - With `--allow-trailers`, a valid message carrying a trailer exits 0 (LEAN-02, AC 7)
Proof: `python3 tools/test_tlc_validators.py -k test_commit_allows_trailer_with_flag`

**C10** - After a passing message, one `UNTRACKED` line names each untracked entry for 1 and for 8 entries, names 8 and `1 more` for 9, and names an untracked directory holding 3 files as one entry; exit 0 (LEAN-02, AC 8)
Proof: `python3 tools/test_tlc_validators.py -k test_commit_lists_untracked_entries`

**C11** - Outside a git work tree a valid message exits 0 with no `UNTRACKED` line (LEAN-02, AC 9)
Proof: `python3 tools/test_tlc_validators.py -k test_commit_skips_untracked_outside_git`

**C12** - Untracked entries under `.specs/` and git-ignored paths produce no `UNTRACKED` line (LEAN-02, AC 9)
Proof: `python3 tools/test_tlc_validators.py -k test_commit_untracked_excludes_specs_and_ignored`

**C13** - A rejected message prints no `UNTRACKED` line (LEAN-02, AC 8)
Proof: `python3 tools/test_tlc_validators.py -k test_commit_invalid_message_prints_no_untracked_line`

**C14** - No message at all exits 2 (LEAN-02, AC 6)
Proof: `python3 tools/test_tlc_validators.py -k test_commit_without_message_exits_2`

**C24** - When `--root` is a subdirectory of a git repository, the `UNTRACKED` line names entries relative to `--root`, excludes that root's `.specs/`, and leaves out untracked entries outside `--root` (LEAN-02, AC 8, AC 9)
Proof: `python3 tools/test_tlc_validators.py -k test_commit_untracked_is_scoped_to_root`

**C15** - The hook file the Lean build reference shows for a repository that asks for trailers passes `--allow-trailers`, and running `check_commit.py` with the flags that hook shows accepts a message carrying a trailer (LEAN-02, AC 7)
Proof: `python3 tools/test_phase_skills.py -k test_lean_hook_can_allow_trailers`

### S3 - The plan is written from the whole request

**C16** - The Lean plan reference states that answers are not the approval: the plan holding them is presented again and an answer is never recorded as the receipt's `Decision` (LEAN-03, AC 10)
Proof: `python3 tools/test_phase_skills.py -k test_lean_answers_are_not_the_approval`

**C17** - The Lean plan reference states that a capture shows part of the request, not the whole of it: each sentence is read against the captures, what no capture draws gets a criterion or a question, and a screen criterion says what the user sees (LEAN-03, AC 11)
Proof: `python3 tools/test_phase_skills.py -k test_lean_capture_is_not_the_whole_request`

**C18** - The Lean plan reference instructs asking whether the running app should hold the captures' sample data at handover (LEAN-03, AC 12)
Proof: `python3 tools/test_phase_skills.py -k test_lean_asks_about_sample_data`

### S4 - The build and the verification stay honest

**C19** - The Lean build reference requires the first slice thin and end to end before any other, forbids one layer for every slice first, and requires a slice that is a layer to be cut again by outcome (LEAN-04, AC 13)
Proof: `python3 tools/test_phase_skills.py -k test_lean_first_slice_is_end_to_end`

**C20** - The shared verify core forbids changing the data the running app holds or anything outside the repository, and requires a stubbed response or a throwaway copy named in the report (LEAN-04, AC 14)
Proof: `python3 tools/test_phase_skills.py -k test_verifier_leaves_app_data_alone`

### S5 - The source pin names upstream 3.2.0

**C21** - `.skill-meta.json` carries `sourceCommit` `586a794efa688358e456b942b1849b76672115ae` and `contentHash` `788382a643dcb946c6062764e7a5af73995aaf2724357b1c478fa494b1723262`, and `NOTICE.md` names 3.2.0, the four adapted items and the kept proof machinery (LEAN-05, AC 15, AC 16)
Proof: `python3 tools/test_phase_skills.py -k test_lean_provenance_pins_upstream`

**C22** - `CHANGELOG.md` names the request gate, `--allow-trailers`, the `UNTRACKED` line and the `586a794` re-pin (LEAN-05, AC 17)
Proof: `sh -c 'grep -q "request.md" CHANGELOG.md && grep -q -- "--allow-trailers" CHANGELOG.md && grep -q "UNTRACKED" CHANGELOG.md && grep -q "586a794" CHANGELOG.md'`

## Coverage

| Set (size) | Member -> proof | Unproven |
| --- | --- | --- |
| `check_commit.py --allow-trailers` outcomes (3) | exit `0` C9 · exit `1` C7 · exit `2` C14 | - |
| `request.md` states (3) | missing C1 · blank C2 · present C3 | - |
| trailer forms (8) | `Co-Authored-By` × documented case C7 · lower case C7 · leading whitespace C7 · space before the colon C7 · `Made-with` × documented case C7 · lower case C7 · leading whitespace C7 · space before the colon C7, table-driven over all 8 | - |
| untracked list sizes (4) | 1 entry C10 · 8 entries C10 · 9 entries C10 · one directory of 3 files C10 | - |
| untracked exclusions (4) | not a git work tree C11 · under `.specs/` C12 · git-ignored C12 · outside a `--root` that is a subdirectory C24 | - |
| readers handed `request.md` (2) | the criteria reviewer C23 · the Verifier C6 | - |
| one-way doors (2) | the request artifact C1, C5 · the trailer rejection default C7, C9 | - |
| assemblies that copy the fixture file list (2) | `selftest.py` `scaffold()` C4 · `tools/test_tlc_validators.py` `scaffold()` C3 | - |

- Claims naming an outcome, interface or response shape: C1, C7, C9, C10, C14, C24 - each has a proof that runs the script
- Every existing `validate_checks` and `validate_verification` test passes through one of the two `scaffold()` helpers, so a helper that omits `request.md` turns those suites red
- No other check claims more than the single case its proof exercises

## Swept

- validation: C2, C8
- failure modes: C11
- idempotency: n/a - both scripts are read-only checks with no state to repeat
- authorization: n/a - local scripts run by whoever holds the checkout
- concurrency: n/a - one invocation reads the tree once and writes nothing
- data lifecycle: existing - close removes the whole feature directory, `request.md` included
- dependency failure: C11
- state transitions: n/a - no stored state changes
- observability: C10, C13
- deploy compatibility: n/a - skills ship as files; under the project's no-compatibility rule an in-flight feature adds `request.md`, named in the changelog (C22)
- performance budget: n/a - one `git status` call per commit check
