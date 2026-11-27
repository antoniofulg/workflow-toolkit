# Adopt TLC discover 0.10 design documents and their validator

## Approval

- Decision: "Então vamos prosseguir com o resto das atualizações"
- Source: maintainer conversation turn of 2026-11-27, quoted in `request.md`
- Date: 2026-11-27
- Reviewed revision: the four-item Discover recommendation presented in that conversation (copied in `request.md`); the maintainer approved it without reviewing this file, which was written afterwards
- Scope: the upstream 0.10.0 discover update adapted to `wtk-discover`, local commits, push, one pull request and merge; no version release, no `knowledge/` writes

## Problem

A `wtk-discover` design document has no size limit and no mechanical check. A document can state
the same decision in several sections, leave a slice that depends on a later one, call a blocked
slice clear, or cite a decision code nothing defines, and nothing says so before `wtk-plan` reads
it. The skill's handover is a prose checklist the author applies to their own text. Upstream
`tlc-discover` 0.10.0 restructures the document so a team can align on it in one sitting and adds a
script for what a script can check; the source gives no measurement beyond "every draft this was
tried on had some" contradictions found by a fresh reader.

When this ships, a design document has a word budget, a fixed section set that a validator checks,
and a fresh-reader review before it is handed to planning.

## Flow

Reuses the three-way merge of upstream 0.9.2 to 0.10.0 onto the local skill, which is upstream 0.9.2
plus project additions, instead of rewriting the skill by hand.

1. the confirmed verdict -> `wtk-discover/SKILL.md` (exists) - writes `.design/<name>.md` under the two-questions rule and the word budget
2. `wtk-discover/references/document-format.md` (exists) - the fixed section set and order the document follows
3. `wtk-discover/scripts/validate_design.py` (door 1) - upstream's script, byte for byte; errors on sections, anchors, decision and slice agreement, order and blocked slices, warns on undefined cited codes, slice count and word budget
4. `wtk-discover/SKILL.md` (exists) - a fresh reader gets the document and the repository and returns quoted contradictions
5. out: `.design/<name>.md` handed to `wtk-plan` or the Lean Plan phase; `.skill-meta.json` (door 2) records the upstream revision

## Impact

| Front | What changes |
| --- | --- |
| domain | existing term: a design document's section set meant Problem, Key decisions, a Work index and slices with state tables; it now means a status header, Summary, Context and problem, How we will know it worked, Scope, How it works, Key decisions with `D<n>` codes, one Open table, and Slices with Behaviour, Contract and Data parts - `wtk-plan` and the Lean Plan phase read the document as prose and name none of the old sections |
| domain | new term: `D<n>` decision code - a Key decision cited from a slice by code and name |
| existing behaviour | a design written under the old template fails the new validator; an in-flight design is rewritten to the new section set (no migration path, per the project's no-compatibility rule) |
| existing wording | upstream 0.10 calls the step after discovery "the spec"; the merged skill uses that word for the planning step and keeps `wtk-plan` as the skill's name |
| file size | `SKILL.md` grows from 384 to about 460 lines and `document-format.md` from 185 to about 290; both exceed the context-budget targets because the template and the handover procedure are that size |
| existing tests | `tools/test_phase_skills.py` asserts `.design/<name>.md` and "organised by **vertical slice**" in the discover skill; the merged skill keeps both phrases |
| stored data | nothing to migrate |

## Relations

`None - no stored-data shape change`

## Surface

| Interface | In | Out | Outcomes |
| --- | --- | --- | --- |
| `validate_design.py <path>` | the path of one design document | `ERROR` and `WARN` lines · the usage text | exit `0`, exit `1`, exit `2` |

## Landing

| One-way door | Literal shape | Alternative rejected |
| --- | --- | --- |
| the design validator | `.agents/skills/wtk-discover/scripts/validate_design.py`, byte-identical to upstream's file at the pinned commit (SHA-256 `d81f94e75eaa38aace818a4611e6cf42698c6a2e30869cb0ea2088028882cdbe`), standard library only, one positional path, exit 0 with warnings, 1 with any error, 2 on wrong usage | a locally adapted copy - every upstream fix to the validator would need a manual merge, and the project additions add no document section the script would have to learn |
| the discover source pin | `.agents/skills/wtk-discover/.skill-meta.json` with `source`, `sourceCommit` `d4ab26545b16ed7cfec01bd7fdee0f5305b89d86`, `contentHash` `e76c2dc3b32297bb54aaf511266f96273fecd94dbdc9f18d2fcc93be5c250748`, `license` `CC-BY-4.0`, the same four keys as the Lean pin | no pin - the next upstream comparison would again have to infer the base from text similarity |
| the document's section set | the English headings of the upstream 0.10.0 template, in its order, with the Portuguese set the validator also recognises | keeping the local 0.9.2 section set and writing a validator for it - a second validator to maintain against every upstream fix |

- Nothing else in this change is hard to reverse

## Criteria

### S1: A script checks the design document (P1)

A design that breaks a structural rule is refused by a command, and a sound one passes.

**Acceptance Criteria**

1. WHEN `validate_design.py` runs on the fixture design that follows the template THEN it SHALL exit 0 and print no `ERROR` line
2. IF a document whose `Status` is not declined and that has at least one known heading lacks a required section (`Summary`, `Context and problem`, `How we will know it worked`, `Scope`, `How it works`, `Key decisions` or `Slices`) THEN `validate_design.py` SHALL exit 1 with an `ERROR` line naming that section
3. IF the slice index and the slice sections differ in names or order THEN `validate_design.py` SHALL exit 1
4. IF a slice depends on a slice that comes later in the `Order` line THEN `validate_design.py` SHALL exit 1 with an `ERROR` line saying the order does not hold
5. IF the third cell of an Open row names a slice whose status is `clear`, outside a segment that blocks go-live only, THEN `validate_design.py` SHALL exit 1, and SHALL not report a slice that cell names only in a go-live segment
6. IF a key decision is in the index table without a section, or has a section and no index row, THEN `validate_design.py` SHALL exit 1
7. WHEN the words from the `Summary` heading up to the `Slices` heading exceed 2,000, or the words of the whole document exceed 4,000 plus 250 for each slice beyond eight, fenced code blocks excluded and tables and headings counted, THEN `validate_design.py` SHALL print a `WARN` line with the count and the budget and SHALL not fail on that alone
8. WHEN the fixture's headings and its labels (`Entrega`, `Depende de`, `Aplica`, `Ordem`, `Pronto para planejar?`, `Comportamento`) are replaced by the Portuguese set THEN `validate_design.py` SHALL exit 0
9. IF it is called with no path or with more than one THEN `validate_design.py` SHALL print its usage and exit 2
10. IF the document has any one of these defects THEN `validate_design.py` SHALL exit 1 with an `ERROR` line: an anchor that does not resolve; a slice header with no `Delivers`; one with no `Status`; one with no `Depends on`; an index status that differs from the slice header; an `Applies` code without its name beside it; an `Applies` code that is not a key decision; a decision index that lists a slice which does not apply the decision; a slice that applies a decision whose index row does not list it; no `Order` line; an `Order` line that leaves out a slice; one that names what is not a slice; one that names a slice twice; a `Ready to plan?` clear count that differs from the slice headers; a success target with no measurement; a line that is only `n/a`, `tbd` or `todo`
11. WHEN a code is cited and never defined on the page THEN `validate_design.py` SHALL print a `WARN` line naming the code and SHALL not fail on that alone
12. The design validator `validate_design.py` SHALL be byte-identical to upstream's file at the pinned commit: SHA-256 `d81f94e75eaa38aace818a4611e6cf42698c6a2e30869cb0ea2088028882cdbe`

**Independent test:** run the validator on the fixture, then on the fixture with its `Summary` heading removed.

### S2: The template and the validator agree (P1)

The format reference carries the section set the validator requires, and keeps the pack's interface neutrality.

**Acceptance Criteria**

13. The discover format reference SHALL carry, in order, every heading the validator requires, and its template SHALL name the status header rows `Status` and `Ready to plan?`, one Open table, the slice index with its `Order` line, and the slice parts `Behaviour`, `Contract` and `Data`
14. The discover format reference SHALL state that a contract line may be a command, an exported symbol or an event topic and that a data part may describe a store that is not a SQL table

**Independent test:** read the template and tick each required heading in order.

### S3: The skill writes for a team and checks before handover (P2)

The skill states the size budget and the two-questions rule, and its handover runs the validator and a fresh reader.

**Acceptance Criteria**

15. The discover skill SHALL state the word budget with the same three numbers the validator uses: 2,000, 4,000 and 250
16. The discover skill SHALL state that a fact earns its place only when two people on the team could disagree about it or be surprised by it, or when changing it after release would require telling somebody outside the team or migrating data
17. The discover skill SHALL instruct running `validate_design.py` before handover and fixing every error
18. The discover skill SHALL instruct handing only the document and the repository to a fresh reader who quotes the two lines that conflict, SHALL require saying so in the handover when no fresh reader is available, and SHALL state the stopping rule: stop when a run raises no question about something hard to reverse that Open does not already list
19. The discover skill SHALL list, after the validator and the fresh reader, the questions only judgment answers, including whether a person can stop after the Summary and whether every behaviour row, data field and contract line passes one of the two questions
20. The discover skill SHALL keep its project additions: the artifact handoff, the `Evidence` section and its signal table, the decision-store paragraph, the `wtk-plan` handoff, the product-signal example, an identifier ceiling that includes command, event and exported symbol, and the phrases `.design/<name>.md` and "organised by **vertical slice**" an existing contract test asserts
21. The discover skill's frontmatter SHALL keep `name: wtk-discover` and the pack version, not upstream's `0.10.0`

**Independent test:** read the skill's handover section and follow it against the fixture design.

### S4: The source pin names upstream 0.10.0 (P2)

The provenance records say which upstream revision the skill was adapted from.

**Acceptance Criteria**

22. The discover source metadata `.agents/skills/wtk-discover/.skill-meta.json` SHALL carry `sourceCommit` `d4ab26545b16ed7cfec01bd7fdee0f5305b89d86`, `contentHash` `e76c2dc3b32297bb54aaf511266f96273fecd94dbdc9f18d2fcc93be5c250748` and `license` `CC-BY-4.0`
23. The pack notice `NOTICE.md` SHALL name `wtk-discover` as an adaptation of Tech Leads Club's `tlc-discover` and point to its source metadata
24. The changelog `CHANGELOG.md` SHALL list under `[Unreleased]` the new document section set, `validate_design.py`, the word budget and the fresh-reader review

**Independent test:** run the provenance contract test.

## Traceability

| ID | Slice | Criteria | Status |
| --- | --- | --- | --- |
| DISC-01 | S1 | 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12 | Pending |
| DISC-02 | S2 | 13, 14 | Pending |
| DISC-03 | S3 | 15, 16, 17, 18, 19, 20, 21 | Pending |
| DISC-04 | S4 | 22, 23, 24 | Pending |

## Out of scope

| Excluded | Why |
| --- | --- |
| Changing what `wtk-plan` or the Lean Plan phase reads from a design | they read the document as prose and name no section; a mismatch found later is its own change |
| A validator for designs in a language other than English or Portuguese | upstream skips heading checks for other languages and so does this |
| Upstream's dry-run spec of the first slice as a mandatory step | upstream offers it only for an expensive door; it stays optional here |
| A message for a path that does not exist or cannot be read | upstream's script raises `FileNotFoundError` there: a Python traceback and exit 1; the port is byte-identical, so this stays as upstream has it |
| A criterion for each of upstream's other warnings (more than eight decisions, more than ten slices, a long sentence, a decision with no Rule line, a slice with no Behaviour part, a placeholder left in) | they never fail a run; AC 12 pins the file that produces them |
| Rewriting existing `.design/` documents of consuming projects | this pack holds none; each project rewrites its own in-flight design |

## Assumptions

| Assumption | Chosen default | Rationale | Confirmed? |
| --- | --- | --- | --- |
| The approved list named four additions (word budget, two-questions rule, validator, fresh-reader review); upstream 0.10.0 changes more | the whole skill and format are merged, not only those four: the fixed section set and order, the status header rows, `D<n>` decision codes with an index table, the slice index and `Order` line, slice parts `Behaviour`, `Contract` and `Data` in place of the state table, one Open table, the judgment questions at handover, and upstream's new common-failure entries | the validator checks that structure and cannot be adopted against the old template | n |
| Whether the validator is adapted or copied | copied byte for byte | the project additions live in the skill text, not in the document's sections, so the script needs no change | n |
| Whether discover gets a source pin like Lean's | a `.skill-meta.json` with the same four keys | this adoption had to infer the base revision from text similarity | n |
| Word for the step after discovery | upstream's "spec" inside the skill, `wtk-plan` as the skill name | rewording every merged paragraph would diverge from upstream for no behaviour | n |
| Where the validator's tests live | a new `tools/test_discover_design.py` with a fixture design under the skill's `scripts/fixtures/` | `test:python` already runs every `tools/test_*.py`; the Lean validators use the same layout | n |
| Recording this adoption in `knowledge/` | not written here | writing `knowledge/` needs the maintainer's yes; offered after delivery | n |

**Open questions:** none - all resolved or logged above.

## Observable

| Surface | Decision | Landing |
| --- | --- | --- |
| command `validate_design.py` | output format and verbosity | AC 2, AC 7, AC 11 |
| command `validate_design.py` | every flag and its default | existing - it takes one positional path and no flag |
| command `validate_design.py` | exit codes | AC 1, AC 2, AC 9, AC 10 |
| command `validate_design.py` | what it prints when it fails halfway | AC 9 |
| document `.design/<name>.md` | structure | AC 13 |
| document `.design/<name>.md` | tone, depth | AC 15, AC 16 |
| document `.design/<name>.md` | what the reader is meant to do next | AC 17, AC 18, AC 19 |

## Sources

- `request.md` - the maintainer's request and the approved recommendation
- upstream `tlc-discover` 0.10.0 at `d4ab26545b16ed7cfec01bd7fdee0f5305b89d86` (tech-leads-club/agent-skills) - the document format, the skill rules and the validator
