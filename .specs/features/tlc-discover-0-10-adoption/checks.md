# Adopt TLC discover 0.10 design documents and their validator - checks

Profile: standard
Plan: `.specs/features/tlc-discover-0-10-adoption/plan.md`
Build: `python3 tools/test_phase_skills.py`
Risk: C4, C5, C7 - an order check that never fires, a blocked slice read as clear, and a budget that counts code blocks would each pass a weak test

## Intent

25 checks in 4 slices · 3 one-way doors · 0 open

## Checks

Instruction-only claims (C15, C17-C21) are proven by a named contract test in
`tools/test_phase_skills.py` that the rule's key terms sit on one logical line of the file that owns
it, and are judged by the Verifier against the plan. The
[test contract](../../../.agents/skills/wtk/references/test-contract.md) forbids prose assertions by
default and allows them when the artifact is the product contract and no stronger gate owns it: in
this pack the instruction text is the product, and these rules have no script behind them. Each test
uses `owns()` with the rule's terms, never a whole sentence; a matching string alone does not prove
agent behaviour, which is why the Verifier's `Holds` judgment reads the rule.

### S1 - A script checks the design document

**C1** - `validate_design.py` exits 0 with no `ERROR` line on the fixture design (DISC-01, AC 1)
Proof: `python3 tools/test_discover_design.py -k test_fixture_design_passes`

**C2** - On the fixture, which is not declined and has known headings, removing each of the seven required sections in turn exits 1 with an `ERROR` line naming that section (DISC-01, AC 2)
Proof: `python3 tools/test_discover_design.py -k test_missing_required_section_is_rejected`

**C3** - A slice index whose names or order differ from the slice sections exits 1 (DISC-01, AC 3)
Proof: `python3 tools/test_discover_design.py -k test_slice_index_must_match_sections`

**C4** - A slice that depends on a slice later in the `Order` line exits 1 saying the order does not hold, and the same dependency in the right order passes (DISC-01, AC 4)
Proof: `python3 tools/test_discover_design.py -k test_order_must_respect_dependencies`

**C5** - An Open row whose third cell names a slice with status `clear` exits 1; the same row with the slice marked `blocked by` it passes; and a third cell that names the clear slice only in a go-live segment passes (DISC-01, AC 5)
Proof: `python3 tools/test_discover_design.py -k test_blocked_slice_cannot_be_clear`

**C6** - A decision in the index table with no section, and a decision section with no index row, each exit 1 (DISC-01, AC 6)
Proof: `python3 tools/test_discover_design.py -k test_decision_index_and_sections_agree`

**C7** - More than 2,000 words between the `Summary` and `Slices` headings, and more than 4,000 words in the whole document, each print a `WARN` line with the count and the budget and exit 0; the same words inside a fenced code block raise neither warning, and words in a table row count (DISC-01, AC 7)
Proof: `python3 tools/test_discover_design.py -k test_word_budget_warns_and_ignores_code_blocks`

**C8** - A document with nine slices raises the total budget by 250 words (DISC-01, AC 7)
Proof: `python3 tools/test_discover_design.py -k test_word_budget_grows_per_slice_beyond_eight`

**C9** - The fixture with its headings and its labels replaced by the Portuguese set exits 0, and with the headings replaced and the labels left in English exits 1 (DISC-01, AC 8)
Proof: `python3 tools/test_discover_design.py -k test_portuguese_headings_and_labels_are_recognised`

**C10** - No path, and two paths, each print the usage text and exit 2 (DISC-01, AC 9)
Proof: `python3 tools/test_discover_design.py -k test_wrong_usage_exits_2`

**C11** - Each of the sixteen structural defects, applied alone to the fixture, exits 1 with an `ERROR` line (DISC-01, AC 10)
Proof: `python3 tools/test_discover_design.py -k test_each_structural_defect_is_rejected`

**C12** - A code cited and never defined on the page prints a `WARN` line naming it and exits 0 (DISC-01, AC 11)
Proof: `python3 tools/test_discover_design.py -k test_undefined_cited_code_warns`

**C13** - The SHA-256 of `.agents/skills/wtk-discover/scripts/validate_design.py` is `d81f94e75eaa38aace818a4611e6cf42698c6a2e30869cb0ea2088028882cdbe` (DISC-01, AC 12)
Proof: `python3 tools/test_discover_design.py -k test_validator_is_upstream_byte_for_byte`

### S2 - The template and the validator agree

**C14** - The format reference's template carries, in order, every heading the validator requires, and names the `Status` and `Ready to plan?` header rows, the Open table, the `Order` line and the slice parts `Behaviour`, `Contract` and `Data` (DISC-02, AC 13)
Proof: `python3 tools/test_discover_design.py -k test_template_carries_the_validated_section_set`

**C15** - The format reference states that a contract line may be a command, an exported symbol or an event topic, and that a data part may describe a store that is not a SQL table (DISC-02, AC 14)
Proof: `python3 tools/test_phase_skills.py -k test_discover_format_stays_interface_neutral`

### S3 - The skill writes for a team and checks before handover

**C16** - The skill states the word budget, and the three numbers it gives equal the validator's `READ_BUDGET`, `TOTAL_BUDGET` and `PER_SLICE` constants (DISC-03, AC 15)
Proof: `python3 tools/test_discover_design.py -k test_skill_budget_matches_validator_constants`

**C17** - The skill states the two questions a fact must pass to be in the document (DISC-03, AC 16)
Proof: `python3 tools/test_phase_skills.py -k test_discover_two_questions_rule`

**C18** - The skill instructs running `validate_design.py` before handover and fixing every error, and the script path it names exists (DISC-03, AC 17)
Proof: `python3 tools/test_phase_skills.py -k test_discover_handover_runs_the_validator`

**C19** - The skill instructs the fresh-reader review with only the document and the repository and quoted conflicting lines, requires saying so when no fresh reader is available, and states the stopping rule (DISC-03, AC 18)
Proof: `python3 tools/test_phase_skills.py -k test_discover_fresh_reader_review`

**C20** - The skill lists the judgment questions after the validator and the fresh reader, including stopping after the Summary and the two-questions pass over every row (DISC-03, AC 19)
Proof: `python3 tools/test_phase_skills.py -k test_discover_judgment_questions`

**C21** - The skill keeps its project additions: the artifact handoff link, the `Evidence` heading and signal table, the decision-store link, the `wtk-plan` handoff, the product-signal example, command, event and exported symbol in the identifier ceiling, and the two phrases the artifact-contract test asserts (DISC-03, AC 20)
Proof: `python3 tools/test_phase_skills.py -k test_discover_keeps_project_additions`

**C22** - The skill's frontmatter name is `wtk-discover` and its version equals the `package.json` version (DISC-03, AC 21)
Proof: `python3 tools/test_phase_skills.py -k test_discover_frontmatter_stays_the_packs`

### S4 - The source pin names upstream 0.10.0

**C23** - `.agents/skills/wtk-discover/.skill-meta.json` carries `sourceCommit` `d4ab26545b16ed7cfec01bd7fdee0f5305b89d86`, `contentHash` `e76c2dc3b32297bb54aaf511266f96273fecd94dbdc9f18d2fcc93be5c250748` and `license` `CC-BY-4.0` (DISC-04, AC 22)
Proof: `python3 tools/test_phase_skills.py -k test_discover_provenance_pins_upstream`

**C24** - `NOTICE.md` names `wtk-discover` as an adaptation of `tlc-discover` and links its source metadata, and the link resolves (DISC-04, AC 23)
Proof: `python3 tools/test_phase_skills.py -k test_notice_names_the_discover_adaptation`

**C25** - The `[Unreleased]` section of `CHANGELOG.md` names `validate_design.py`, the word budget, the fresh-reader review and the new section set (DISC-04, AC 24)
Proof: `python3 -c "import re,sys;u=re.split(r'^## \[',open('CHANGELOG.md',encoding='utf-8').read(),flags=re.M)[1].lower();sys.exit(0 if u.startswith('unreleased') and all(k in u for k in ('validate_design.py','word budget','fresh reader','how it works')) else 1)"`

## Coverage

| Set (size) | Member -> proof | Unproven |
| --- | --- | --- |
| `validate_design.py <path>` outcomes (3) | exit `0` C1 · exit `1` C2 · exit `2` C10 | - |
| required sections (7) | `Summary` C2 · `Context and problem` C2 · `How we will know it worked` C2 · `Scope` C2 · `How it works` C2 · `Key decisions` C2 · `Slices` C2, table-driven over all 7 | - |
| structural defects of AC 10 (16) | unresolved anchor C11 · no `Delivers` C11 · no `Status` C11 · no `Depends on` C11 · index status differs C11 · `Applies` code without its name C11 · `Applies` code that is not a key decision C11 · index lists a slice that does not apply C11 · slice applies an unlisted decision C11 · no `Order` line C11 · `Order` leaves out a slice C11 · `Order` names a non-slice C11 · `Order` repeats a slice C11 · wrong clear count C11 · success target without a measurement C11 · filler line C11, table-driven over all 16 | - |
| word budgets (3) | reading 2,000 C7 · total 4,000 C7 · 250 per slice beyond eight C8 | - |
| decision disagreement (2) | index row without a section C6 · section without an index row C6 | - |
| wrong usage (2) | no path C10 · two paths C10 | - |
| heading languages (2) | English C1 · Portuguese C9 | - |
| one-way doors (3) | the design validator C1, C10, C13 · the discover source pin C23 · the document's section set C14 | - |
| project additions kept (8) | artifact handoff C21 · `Evidence` section C21 · decision store C21 · `wtk-plan` handoff C21 · product-signal example C21 · identifier ceiling C21 · `.design/<name>.md` C21 · vertical-slice phrase C21, table-driven over all 8 | - |

- Claims naming an outcome, interface or response shape: C1, C2, C7, C10, C11, C12 - each has a proof that runs the script
- No other check claims more than the single case its proof exercises

## Swept

- validation: C2, C3, C6, C11
- failure modes: C10; a missing or unreadable path is upstream's traceback and exit 1, named in the plan's Out of scope
- idempotency: n/a - the validator reads one file and writes nothing
- authorization: n/a - a local script run by whoever holds the checkout
- concurrency: n/a - one invocation reads one file once
- data lifecycle: n/a - the validator stores nothing; `.design/` documents follow the project's own tracking
- dependency failure: n/a - standard library only, no network or tool dependency
- state transitions: C5
- observability: C7, C12
- deploy compatibility: n/a - skills ship as files; under the project's no-compatibility rule an in-flight design is rewritten to the new section set, named in the changelog (C25)
- performance budget: n/a - one pass over a document of a few thousand words
