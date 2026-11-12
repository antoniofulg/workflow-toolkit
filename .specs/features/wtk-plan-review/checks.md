# Add an on-demand peer review of the Lean plan - checks

Profile: standard
Plan: `.specs/features/wtk-plan-review/plan.md`
Build: `python3 .agents/skills/wtk-lean/scripts/selftest.py`
Risk: C6, C13 - the two paths that could turn a missing or contradictory review into a false `READY`

## Intent

26 checks in 4 slices · 3 one-way doors · 0 open

## Checks

Instruction-only claims are proven by a named contract test that the rule is present where it is
owned, and judged by the Verifier against the plan; a string match alone never settles behaviour.
Validator claims are proven at the script CLI in `tools/test_plan_review.py`.

### S1 - A findings file is either valid or rejected with its defect

**C1** - A file with every door-1 key and heading, `None.` or prefixed items in both sections, exits 0 for each readiness value `READY`, `BLOCKED`, `NEEDS_REWORK` (PREV-01, AC 1)
Proof: `python3 tools/test_plan_review.py -k test_validator_accepts_valid_findings`

**C2** - A missing or empty file exits 1 naming the path (PREV-01, AC 2)
Proof: `python3 tools/test_plan_review.py -k test_validator_rejects_missing_or_empty_file`

**C3** - Each of the six frontmatter keys and five headings, removed one at a time, exits 1 naming that element (PREV-01, AC 3)
Proof: `python3 tools/test_plan_review.py -k test_validator_names_each_missing_element`

**C4** - A readiness outside the three values, or a `round` other than `--round`, exits 1 (PREV-01, AC 3)
Proof: `python3 tools/test_plan_review.py -k test_validator_rejects_bad_readiness_and_round`

**C5** - `# Blockers` or `# Nits` holding neither `None.` nor an item of its prefix exits 1 naming the section (PREV-01, AC 4)
Proof: `python3 tools/test_plan_review.py -k test_validator_rejects_empty_item_section`

**C6** - `READY` with a `B-NNN` item exits 1 (PREV-01, AC 6)
Proof: `python3 tools/test_plan_review.py -k test_validator_rejects_ready_with_blocker`

**C7** - `TBD`, `TODO` or `PLACEHOLDER` as a word exits 1, and a word that merely contains them does not (PREV-01, AC 5)
Proof: `python3 tools/test_plan_review.py -k test_validator_rejects_placeholder_words`

**C8** - A missing path or `--round`, or a `--round` of `0` or a non-integer, exits 2 (PREV-01, AC 7)
Proof: `python3 tools/test_plan_review.py -k test_validator_argument_errors_exit_2`

### S2 - User-picked reviewers review the plan and the user selects findings

**C9** - With no reviewer named, the skill lists the dispatchable reviewers and asks for one or more before dispatch; with no resolvable `plan.md` it reports `no plan found` and dispatches nothing (PREV-02, AC 8)
Proof: `python3 tools/test_plan_review.py -k test_skill_asks_for_reviewers`

**C10** - Reviewers named in the request are dispatched without asking (PREV-02, AC 9)
Proof: `python3 tools/test_plan_review.py -k test_skill_dispatches_named_reviewers`

**C11** - An undispatchable reviewer is named and never substituted (PREV-02, AC 10)
Proof: `python3 tools/test_plan_review.py -k test_skill_never_substitutes_reviewer`

**C12** - Each reviewer is a fresh non-author session, and the prompt names `plan.md`, `checks.md` when present, `Sources` and the one writable findings path (PREV-02, AC 11)
Proof: `python3 tools/test_plan_review.py -k test_prompt_scopes_reviewer`

**C13** - Every findings file is validated, and a missing or invalid one is reported as an incomplete review, never `READY` (PREV-02, AC 13)
Proof: `python3 tools/test_plan_review.py -k test_skill_reports_incomplete_review`

**C14** - The prompt directs review of `Flow`, `Impact`, `Relations`, `Surface`, `Landing`, `Out of scope` and excludes what `validate_plan.py` rejects (PREV-02, AC 12)
Proof: `python3 tools/test_plan_review.py -k test_prompt_targets_plan_shape`

**C15** - Findings are merged into one list tagged by reviewer and id, and only selected items edit `plan.md` (PREV-02, AC 14)
Proof: `python3 tools/test_plan_review.py -k test_skill_merges_and_applies_selected_only`

**C16** - After applying the selection the skill writes `round<N>-disposition.md` with `Finding`, `Reviewer`, `Disposition`, `Changed`, disposition `applied` or `declined - <reason>` (PREV-02, AC 15)
Proof: `python3 tools/test_plan_review.py -k test_skill_writes_disposition`

**C17** - A further round runs only on request with the changed plan, prior findings and disposition, and the skill never writes `## Approval` (PREV-02, AC 16)
Proof: `python3 tools/test_plan_review.py -k test_skill_rounds_opt_in_and_no_approval`

### S3 - A risky plan comes with a peer review offer

**C18** - "Then confirm" offers `wtk-plan-review` in one line naming the triggers, for each of the four triggers (PREV-03, AC 17)
Proof: `python3 tools/test_plan_review.py -k test_lean_plan_offers_review_on_triggers`

**C19** - No offer without a trigger or for a checks-only feature (PREV-03, AC 18)
Proof: `python3 tools/test_plan_review.py -k test_lean_plan_no_offer_without_trigger`

**C20** - The offer adds no stop: one answer can decline it and approve the plan (PREV-03, AC 19)
Proof: `python3 tools/test_plan_review.py -k test_lean_plan_offer_adds_no_stop`

### S4 - The skill ships with the WTK set

**C21** - The full set counts 16 skills including `wtk-plan-review` in README table, install command, `package.json` and the distribution test (PREV-04, AC 20)
Proof: `node --test --test-name-pattern='full WTK set has sixteen skills' tests/skills/distribution.test.js`

**C22** - The phase-skill contract and the QA skill version count include `wtk-plan-review` (PREV-04, AC 20)
Proof: `python3 tools/test_phase_skills.py -k test_public_skill_contracts`
Proof: `bun test tools/shared/tests/qa-skills.test.ts -t 'IT-005'`

**C23** - The `wtk` router sends "peer review the plan" to `wtk-plan-review` (PREV-04, AC 21)
Proof: `python3 tools/test_plan_review.py -k test_router_routes_plan_review`

**C24** - `agent-selection.md` lists `plan_review` with human-picked reviewers, and `workflow_route.py` accepts a selection containing `plan_review` (PREV-04, AC 22)
Proof: `python3 tools/test_plan_review.py -k test_plan_review_stage_selectable`

**C25** - `.gitignore` ignores `.wtk-plan-review/*` (PREV-04, AC 23)
Proof: `python3 tools/test_plan_review.py -k test_review_output_ignored`

**C26** - The README provenance paragraph credits Pedro Nauck's `spec-peer-review` for `wtk-plan-review` (PREV-04, AC 24)
Proof: `python3 tools/test_plan_review.py -k test_readme_credits_upstream`

## Coverage

| Set (size) | Member -> proof | Unproven |
| --- | --- | --- |
| `validate_findings.py` exit codes (3) | 0 C1 · 1 C2 C3 C4 C5 C6 C7 · 2 C8 | - |
| readiness values (3) | `READY` C1 · `BLOCKED` C1 · `NEEDS_REWORK` C1 | - |
| frontmatter keys (6) | `schema_version` C3 · `review_kind` C3 · `round` C3 C4 · `readiness` C3 C4 · `reviewer` C3 · `generated_at` C3 | - |
| headings (5) | `# Summary` C3 · `# Blockers` C3 C5 · `# Nits` C3 C5 · `# Evidence` C3 · `# Deferred Or Follow-Up` C3 | - |
| placeholder words (3) | `TBD` C7 · `TODO` C7 · `PLACEHOLDER` C7 | - |
| skill outcomes (4) | `ready` C13 · `findings to select` C15 · `incomplete review` C13 · `no plan found` C9 | - |
| offer triggers (4) | live `Landing` alternative C18 · `Relations` changes existing data C18 · consumed `Surface` changes C18 · security surface C18 | - |
| disposition values (2) | `applied` C16 · `declined - <reason>` C16 | - |
| Surface interfaces (4) | `wtk-plan-review [feature] [--reviewers r1,r2] [--round N]` C9 C10 · `validate_findings.py --round N <path>` C1 C8 · `round<N>-<reviewer>.md` C1 C3 · stage key `plan_review` C24 | - |

- Claims naming an outcome or interface: C1-C8 cross the script CLI; C24 runs `workflow_route.py`
- No other check claims more than the single case its proof exercises

## Test policy

Omitted: the repo already answers the level - validator behaviour at the script CLI, instruction ownership by contract tests in `tools/test_*.py`, distribution in `tests/skills/`.

## Swept

- validation: C3, C4, C5, C8
- failure modes: C2, C11, C13
- idempotency: n/a - the validator only reads; each round writes new files by round number
- authorization: C12 - the reviewer may write one path; the skill never writes `## Approval` (C17)
- concurrency: n/a - reviewers write distinct files named by reviewer
- data lifecycle: C25 - review output stays checkout-local and ignored
- dependency failure: C11, C13 - an unavailable or failed reviewer is named, never hidden
- state transitions: C17 - round N to N+1 only on request
- observability: C16 - the disposition records what changed and why
- deploy compatibility: n/a - pack release; no backward compatibility per AGENTS.md
- performance budget: n/a - one review round per request, no hot path
