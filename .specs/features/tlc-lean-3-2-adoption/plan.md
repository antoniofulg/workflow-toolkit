# Adopt the additive parts of TLC spec-lean 3.2

## Approval

- Decision: "Vamos aplicar as mudanças recomendadas, prosseguir para a publicação em merge e depois eu vou validar melhor essa mudança da linha"
- Source: maintainer conversation turn of 2026-11-27, quoted in `request.md`
- Date: 2026-11-27
- Reviewed revision: the eight-item recommendation list presented in that conversation (copied in `request.md`); the maintainer approved the list and chose to review the result after merge, so this file was written from the list and was not itself presented before the build
- Scope: the eight listed Lean changes, local commits, push, one pull request and merge; no version release, no `knowledge/` writes, no removal of checks, proofs or the Verifier report

## Problem

A Lean feature's request lives only in the chat. The Verifier is told to check "the original
request", but after a compaction or in a fresh session the coordinator hands it a paraphrase, so a
sentence of the request that no criterion carries cannot be found by anyone. The same gap lets a
plan built from captures drop what the request names and no capture draws. A builder can
also stack one layer for every slice before anything works end to end, a commit can carry an agent
trailer or leave tool output untracked without anything saying so, and a Verifier is not told to
leave the running app's data alone. Upstream `tlc-spec-lean` 3.2.0 answers each of these; the
source gives no measurement for them.

When this ships, a Lean feature cannot reach the build without its request on disk, the Verifier
reads that file sentence by sentence, and the commit check names trailers and untracked files.

## Flow

Reuses the presence-gate pattern of the `## Approval` receipt in `validate_checks.py` and the
post-pass `OWED` output of `check_commit.py` instead of adding a script.

1. the user's request -> `wtk-lean/references/plan.md` (exists) - the coordinator saves it verbatim as `request.md` (door 1) before asking anything, reads it against the captures, and treats answers as plan changes, not approval
2. `wtk-lean/scripts/validate_checks.py` (exists) - refuses a feature whose `request.md` is missing or empty
3. `wtk-lean/references/build.md` (exists) - first slice thin and end to end, never one layer for every slice
4. `wtk-lean/scripts/check_commit.py` (exists) - rejects an agent trailer (door 2), prints an `UNTRACKED` line after a passing message
5. `wtk-lean/references/verify.md` (exists) and `wtk/references/verify-core.md` (exists) - the Verifier reads `request.md` sentence by sentence and leaves the running app's data alone
6. out: `.skill-meta.json`, `NOTICE.md` and `CHANGELOG.md` name upstream 3.2.0

## Impact

| Front | What changes |
| --- | --- |
| domain | new term: `request.md` - the user's request verbatim plus the paths of the captures it came with, lives in `.specs/features/<feature>/` |
| existing behaviour | `validate_checks.py <feature>` passed without a request file, now exits 1 - every caller is affected: `build.md` (before the first change), `selftest.py`, the `scaffold()` helper of `tools/test_tlc_validators.py`, and any in-flight feature of a consuming project, which adds the file (no migration path, per the project's no-compatibility rule) |
| existing behaviour | `check_commit.py` accepted any body, now exits 1 on `Co-Authored-By:` or `Made-with:` - a consuming project that installed it as a `commit-msg` symlink and whose harness appends a trailer needs a hook file that passes `--allow-trailers` |
| existing behaviour | `build.md` listed slice order as the builder's choice ("Yours: order, decomposition"); the first slice and one-slice-at-a-time become fixed, decomposition inside a slice stays the builder's |
| existing behaviour | `wtk/references/verify-core.md` is shared with `wtk-implement`, so the app-data rule reaches the modular Verifier too |
| fixtures | `wtk-lean/scripts/fixtures/` gains `request.md`, and both helpers that copy a fixed file list copy it too: `scaffold()` in `selftest.py` and `scaffold()` in `tools/test_tlc_validators.py`; every existing `validate_checks` test passes through them |
| text that restates the changed behaviour | kept true in the same commits: the docstrings of `check_commit.py` and `validate_checks.py`, the scripts table and validator paragraph of `wtk-lean/SKILL.md`, the commit section of `build.md`, the approval paragraph of `README.md`, and the receipt paragraph of `wtk/references/construction-constraints.md` where it lists what `validate_checks.py` refuses |
| existing wording | `wtk-lean/references/verify.md` says "the original request" in the Verifier's inputs, its dispatch brief and its discovery rule; all three name `request.md`. `wtk-implement/references/verify.md` and `wtk/references/project-requirements.md` keep "the original request": the modular route has no request file |
| stored data | nothing to migrate - feature directories are transient and close removes the whole directory, `request.md` included |

## Relations

`None - no stored-data shape change`

## Surface

| Interface | In | Out | Outcomes |
| --- | --- | --- | --- |
| `check_commit.py --allow-trailers` | a commit message, the optional flag, `--root` | `check_commit: OK` with `OWED` and `UNTRACKED` lines · `ERROR` lines | exit `0`, exit `1`, exit `2` |

## Landing

| One-way door | Literal shape | Alternative rejected |
| --- | --- | --- |
| the request artifact | `.specs/features/<feature>/request.md`: the request verbatim, then a `Captures:` line listing each capture by path or `none`; written once at Plan and not rewritten. The gate enforces presence only; the `Captures:` line and the no-rewrite rule are instructions the Verifier judges | a `## Request` section in `plan.md` - a checks-only feature has no plan, and the plan is rewritten during review while the request must stay as given |
| trailer rejection default | `ERROR` and exit 1 on a body line matching `Co-Authored-By:` or `Made-with:`, case-insensitive, unless `--allow-trailers`; leading whitespace and spaces before the colon still match | accept by default with an opt-in `--reject-trailers` - a rule that is off until someone remembers the flag is the remembered rule the script exists to replace |

- Nothing else in this change is hard to reverse

## Criteria

### S1: The request survives in a file (P1)

A Lean feature without its request on disk cannot start building, and every later reader gets that file.

**Acceptance Criteria**

1. IF a feature directory has no `request.md`, or one with no non-blank line, THEN `validate_checks.py` SHALL exit 1 and name `request.md` in an `ERROR` line
2. WHEN a feature directory holds a `request.md` with at least one non-blank line THEN `validate_checks.py` SHALL raise no request error
3. The Lean plan reference SHALL instruct saving the user's request verbatim to `.specs/features/<feature>/request.md`, with the captures it came with listed by path, before the first question is asked, and the Lean skill's artifact tree SHALL list `request.md`
4. The Lean verify reference SHALL name `request.md`, in place of "the original request", as what the Verifier receives, what its dispatch brief hands over and what it derives concerns from, and SHALL instruct reading it sentence by sentence against what was built, not only against the plan
5. The Lean checks reference SHALL name `request.md` as the request handed to the fresh criteria reviewer

**Independent test:** run `validate_checks.py` on the fixture feature with `request.md` emptied and confirm exit 1 naming the file.

### S2: The commit check names trailers and untracked files (P1)

A commit message with an agent trailer is rejected, and a passing message lists what no commit carries.

**Acceptance Criteria**

6. IF a line after the header, ignoring leading whitespace, starts with `Co-Authored-By` or `Made-with` in any letter case followed by optional spaces and a colon THEN `check_commit.py` SHALL exit 1 with an `ERROR` line naming the trailer
7. WHERE `--allow-trailers` is passed `check_commit.py` SHALL exit 0 for an otherwise valid message carrying such a trailer
8. WHEN a message passes and `git status --porcelain --untracked-files=normal` at `--root` reports untracked entries outside `.specs/` THEN `check_commit.py` SHALL print one `UNTRACKED` line naming up to 8 of those entries, an untracked directory counting as one entry, and the count of the rest, and exit 0
9. IF `--root` is not a git work tree, or every untracked entry is under `.specs/` or git-ignored, THEN `check_commit.py` SHALL print no `UNTRACKED` line and exit 0 for a valid message

**Independent test:** run `check_commit.py --message` with a `Co-Authored-By:` body, then in a temporary repository holding one untracked file.

### S3: The plan is written from the whole request (P2)

The plan phase reads the request against its captures and keeps answers apart from approval.

**Acceptance Criteria**

10. The Lean plan reference SHALL state that answers to the agent's questions are not the approval: the plan that holds them is presented again, and an answer is never recorded as the receipt's `Decision`
11. The Lean plan reference SHALL state that a capture shows part of the request and not the whole of it: each sentence of the request is read against the captures, what the request names and no capture draws gets a criterion or a question, and a screen criterion says what the user sees
12. The Lean plan reference SHALL instruct asking the user whether the running app should hold the captures' sample data at handover

**Independent test:** read the plan reference and find each of the three rules once, in the section that owns it.

### S4: The build and the verification stay honest (P2)

The first slice works end to end before anything is stacked on it, and the Verifier changes nothing the app holds.

**Acceptance Criteria**

13. The Lean build reference SHALL require the first slice to be built thin and end to end before any other, SHALL forbid building one layer for every slice first, and SHALL require a slice that turns out to be a layer to be cut again by outcome before it is built
14. The shared verify core SHALL forbid the Verifier from changing the data the running app holds or anything outside the repository, and SHALL require it to reach a state the data lacks through a stubbed response or a throwaway copy and to name which in the report

**Independent test:** read `build.md` and `verify-core.md` and find each rule once.

### S5: The source pin names upstream 3.2.0 (P2)

The provenance records match the upstream revision the adaptation was read from.

**Acceptance Criteria**

15. The Lean source metadata `.agents/skills/wtk-lean/.skill-meta.json` SHALL carry `sourceCommit` `586a794efa688358e456b942b1849b76672115ae` and `contentHash` `788382a643dcb946c6062764e7a5af73995aaf2724357b1c478fa494b1723262`
16. The Lean `NOTICE.md` SHALL name upstream 3.2.0 at commit `586a794`, list the adapted material (the request record, the commit trailer and untracked check, the capture rule, the tracer-bullet slice order), and state that Workflow Toolkit keeps the checks, proofs and Verifier report upstream 3.x removed
17. The changelog `CHANGELOG.md` SHALL list under `[Unreleased]` the request gate, the trailer rejection with `--allow-trailers`, the `UNTRACKED` line, and the re-pin

**Independent test:** run the provenance contract test.

## Traceability

| ID | Slice | Criteria | Status |
| --- | --- | --- | --- |
| LEAN-01 | S1 | 1, 2, 3, 4, 5 | Pending |
| LEAN-02 | S2 | 6, 7, 8, 9 | Pending |
| LEAN-03 | S3 | 10, 11, 12 | Pending |
| LEAN-04 | S4 | 13, 14 | Pending |
| LEAN-05 | S5 | 15, 16, 17 | Pending |

## Out of scope

| Excluded | Why |
| --- | --- |
| Removing `checks.md`, the proof runner, the Verifier report and lessons, as upstream 3.x did | the maintainer keeps the proof machinery and will judge that change separately |
| Upstream's `**Review:**` and `**Fix pass:**` lines and its single fix pass | they replace the Verifier report and review rounds this pack keeps |
| Upstream's plan-less path that keeps answers in `request.md` | this pack's short path keeps `## Intent` and the receipt in `checks.md` |
| The Windows UTF-8 output fix in the scripts | not in the approved list; a separate fix if a consumer needs it |
| The modular route's inputs (`wtk-plan`, `wtk-implement`) | they keep their upstream modular contract; only the shared verify core changes |

## Assumptions

| Assumption | Chosen default | Rationale | Confirmed? |
| --- | --- | --- | --- |
| Whether the request record is enforced or only instructed | a presence gate in `validate_checks.py` | the approved reason for adopting it is that a remembered rule is dropped by a cheaper builder; the receipt already uses the same gate | n |
| How a project that wants trailers keeps a `commit-msg` hook | `build.md` shows a hook file that calls the script with `--allow-trailers` beside the symlink form | a symlink cannot pass a flag | n |
| Where the capture rule lives and how it is worded | the Lean plan reference, beside the surface walk, worded as "shows part of the request" | it shapes criteria at Plan; `ui-ux.md` already uses "viewport" for a width x height pair and keeps owning fidelity evidence | n |
| Recording this adoption in `knowledge/` | not written here | writing `knowledge/` needs the maintainer's yes; offered after delivery | n |

**Open questions:** none - all resolved or logged above.

## Observable

| Surface | Decision | Landing |
| --- | --- | --- |
| command `check_commit.py` | output format and verbosity | AC 6, AC 8 |
| command `check_commit.py` | every flag and its default | AC 7 |
| command `check_commit.py` | exit codes | AC 6, AC 7, AC 8 |
| command `check_commit.py` | what it prints when it fails halfway | AC 9 |
| command `validate_checks.py` | output format, exit codes | AC 1, AC 2 |
| command `validate_checks.py` | every flag and its default | existing - no flag is added or changed |
| document `request.md` | structure, tone, depth, what the reader does next | AC 3, AC 4, AC 5 |
| document Lean references | structure, tone, depth | existing - each rule lands in the reference that already owns its phase |

## Sources

- `request.md` - the maintainer's request and the approved recommendation list
- upstream `tlc-spec-lean` 3.2.0 at `586a794efa688358e456b942b1849b76672115ae` (tech-leads-club/agent-skills PR #274) - the source of each adapted rule
