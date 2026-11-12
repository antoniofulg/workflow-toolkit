# Add an on-demand peer review of the Lean plan

## Approval

- Decision: "Sim, pode prosseguir" - user approved the plan as presented, including the four assumptions marked unconfirmed
- Source: conversation turn answering the plan review question, 2026-11-12
- Date: 2026-11-12
- Reviewed revision: plan.md sha256 719c0271d432 on base 6917b021
- Scope: S1-S4 local edits and local commits on feat/wtk-plan-review; push, PR, merge and release follow wtk-ship only when invoked

## Problem

The only review a Lean plan gets before approval is the planner's own closure gate and the human
reading it. An architecture mistake written into `Landing`, `Relations` or `Surface` - a one-way
door with a better alternative, a change to data that already exists, a consumed interface that
silently changes - is found after Build, by `wtk-deep-review` or the Verifier, when fixing it means
reworking code instead of editing a paragraph. `wtk-deep-review` reviews diffs, not plans, and the
mandatory criteria reviewer in `wtk/references/project-requirements.md` checks requirement coverage,
not architecture.

The source gives no measured cost; the evidence is the user's request to adopt Pedro Nauck's
`spec-peer-review` skill as an on-demand step.

When this ships, presenting a risky plan comes with a one-line offer of a peer review. If the user
accepts, they pick the reviewers from what the harness offers, each reviewer writes one validated
findings file, and the user selects which findings the planner applies before approving.

## Flow

Reuses the Lean plan presentation, the host's agent dispatch and the routing table in
`agent-selection.md`; it adds one skill, one prompt and one validator, and no new approval step.

1. planner presents `plan.md` -> `wtk-lean/references/plan.md` "Then confirm" (exists) - when a trigger holds, appends one offer line naming the trigger
2. user accepts, or invokes `wtk-plan-review` directly (new skill) - lists the reviewers the harness can dispatch and asks the user to pick one or more (door 2)
3. coordinator dispatches each picked reviewer as a fresh non-author session through the host mechanism, with `references/reviewer-prompt.md` (new) filled in
4. each reviewer writes only `.wtk-plan-review/<feature>/round<N>-<reviewer>.md` (door 1)
5. `validate_findings.py` (new) - checks each findings file; a missing or malformed file makes that review incomplete
6. coordinator merges the findings into one list tagged by reviewer; user selects; planner edits `plan.md` and writes `round<N>-disposition.md` (door 3)
7. out: the revised plan goes back to the existing human approval; a next round runs only when the user asks

## Impact

| Front | What changes |
| --- | --- |
| domain | new term: plan peer review - an opt-in, user-staffed architecture review of an unapproved `plan.md`, lives in `wtk-plan-review` |
| domain | new term: plan review trigger - one of four plan conditions that makes the planner offer a peer review, lives in `wtk-lean/references/plan.md` |
| domain | existing term: agent selection meant "dispatch without asking the human", now has one stage, `plan_review`, whose reviewers the human picks - `agent-selection.md` and `workflow_route.py` `STAGES` branch on stage keys |
| stored data | nothing to migrate: `.wtk-plan-review/` is new, checkout-local and gitignored |
| distribution | the full WTK set grows from 15 to 16 skills - README, `package.json`, distribution and phase-skill tests count them |

## Relations

`None - no stored-data shape change`

## Surface

| Interface | In | Out | Outcomes |
| --- | --- | --- | --- |
| skill `wtk-plan-review [feature] [--reviewers r1,r2] [--round N]` | feature slug or `plan.md` path, optional reviewer names, round | findings files, merged list, disposition | `ready`, `findings to select`, `incomplete review`, `no plan found` |
| `validate_findings.py --round N <path>` | one findings file | message per defect | exit `0` valid, `1` missing or malformed, `2` bad arguments |
| findings file `round<N>-<reviewer>.md` | reviewer output | read by the validator and the coordinator | readiness `READY`, `BLOCKED`, `NEEDS_REWORK` |
| stage key `plan_review` | selection JSON | frozen route | `accepted` |

## Landing

| One-way door | Literal shape | Alternative rejected |
| --- | --- | --- |
| findings file schema | frontmatter `schema_version: 1`, `review_kind: plan`, `round`, `readiness: READY\|BLOCKED\|NEEDS_REWORK`, `reviewer`, `generated_at` (ISO-8601); headings `# Summary`, `# Blockers` (`## B-NNN - <title>` or `None.`), `# Nits` (`## N-NNN - <title>` or `None.`), `# Evidence`, `# Deferred Or Follow-Up` | upstream's separate `reviewer_runtime`/`reviewer_model` keys - the user names the reviewer, and one `reviewer` field holds what they picked plus the resolved model when the host exposes it |
| reviewer staffing | the skill lists dispatchable reviewers from the routing table and the host's other agent harnesses, the user picks one or more; a reviewer named in the request skips the question; a picked reviewer the host cannot dispatch stops that dispatch and is named | a fixed reviewer role or provider - the user wants to choose per plan |
| disposition record | `.wtk-plan-review/<feature>/round<N>-disposition.md`: `\| Finding \| Reviewer \| Disposition \| Changed \|`, disposition `applied` or `declined - <reason>` | recording dispositions inside `plan.md` - the plan is the reviewed shape, not its review log |

- Nothing else in this change is hard to reverse

## Criteria

### S1: A findings file is either valid or rejected with its defect (P1)

**Acceptance Criteria**

1. WHEN `validate_findings.py --round N <path>` reads a file with the door-1 frontmatter and headings, and each of `# Blockers` and `# Nits` holds `None.` or at least one item of its prefix THEN it SHALL exit `0`
2. IF the file is missing or empty THEN it SHALL exit `1` naming the path
3. IF a frontmatter key or heading of door 1 is missing, `readiness` is outside `READY`, `BLOCKED`, `NEEDS_REWORK`, or `round` differs from `--round` THEN it SHALL exit `1` naming the missing or wrong element
4. IF `# Blockers` or `# Nits` holds neither `None.` nor an item of its prefix THEN it SHALL exit `1` naming the section
5. IF the file contains `TBD`, `TODO` or `PLACEHOLDER` as a word THEN it SHALL exit `1`
6. IF `readiness` is `READY` and `# Blockers` holds an item THEN it SHALL exit `1`
7. IF an argument is missing or `--round` is not a positive integer THEN it SHALL exit `2`

**Independent test:** run the validator on a valid fixture and on one fixture per defect.

### S2: User-picked reviewers review the plan and the user selects findings (P1)

**Acceptance Criteria**

8. WHEN `wtk-plan-review` runs without reviewers named THEN it SHALL list the reviewers the harness can dispatch and ask the user to pick one or more before any dispatch
9. WHEN the request names reviewers THEN the skill SHALL dispatch those without asking
10. IF a picked reviewer cannot be dispatched by the host THEN the skill SHALL name it and SHALL NOT substitute another reviewer
11. The skill SHALL dispatch each reviewer as a fresh session that did not author the plan, with the reviewer prompt naming `plan.md`, `checks.md` when present, the plan's `Sources`, and the single findings path the reviewer may write
12. The reviewer prompt SHALL direct review of `Flow`, `Impact`, `Relations`, `Surface`, `Landing` and `Out of scope` for judgment defects and SHALL exclude what `validate_plan.py` already rejects
13. WHEN every reviewer has returned THEN the skill SHALL run `validate_findings.py` on each file and report a missing or invalid file as an incomplete review, never as `READY`
14. WHEN findings exist THEN the skill SHALL present one merged list, each item tagged with its reviewer and id, and SHALL edit `plan.md` only for the items the user selects
15. WHEN the user's selection has been applied THEN the skill SHALL write `round<N>-disposition.md` with one row per finding
16. The skill SHALL run a further round only when the user asks, sending the changed plan, prior findings and disposition, and SHALL NOT write the plan's `## Approval` receipt

**Independent test:** invoke the skill on a fixture feature naming one reviewer; read its findings file, validator output and disposition.

### S3: A risky plan comes with a peer review offer (P1)

**Acceptance Criteria**

17. WHEN the planner presents a plan in which a `Landing` door still has a live alternative, `Relations` changes data that already exists, `Surface` changes an interface already consumed, or a security surface was declared at Specify THEN the presentation SHALL end with one line offering `wtk-plan-review` and naming the triggers that hold
18. WHEN no trigger holds, or the feature is checks-only THEN the presentation SHALL carry no offer
19. The offer SHALL NOT add a stop beyond the existing plan approval: one answer may both decline the review and approve the plan

**Independent test:** read `wtk-lean/references/plan.md` "Then confirm".

### S4: The skill ships with the WTK set (P2)

**Acceptance Criteria**

20. The full WTK set SHALL list `wtk-plan-review` in the README skills table and install command, `package.json` files, and the distribution and phase-skill tests, and count 16 skills
21. The `wtk` router SHALL route "peer review the plan" to `wtk-plan-review`
22. The agent selection reference `agent-selection.md` SHALL list a `plan_review` stage whose reviewers the human picks, and `workflow_route.py` SHALL accept `plan_review` as a stage key
23. The repository `.gitignore` SHALL ignore `.wtk-plan-review/*`
24. The README provenance paragraph SHALL credit Pedro Nauck's `spec-peer-review` as the inspiration for `wtk-plan-review`

**Independent test:** `bun run test:all`.

## Traceability

| ID | Slice | Criteria | Status |
| --- | --- | --- | --- |
| PREV-01 | S1 | 1, 2, 3, 4, 5, 6, 7 | Pending |
| PREV-02 | S2 | 8, 9, 10, 11, 12, 13, 14, 15, 16 | Pending |
| PREV-03 | S3 | 17, 18, 19 | Pending |
| PREV-04 | S4 | 20, 21, 22, 23, 24 | Pending |

## Out of scope

| Excluded | Why |
| --- | --- |
| Reviewing modular `wtk-plan` task contracts or external RFCs | the user asked for the Lean plan; the skill can widen later |
| An automatic or looping review gate | upstream and the user keep it opt-in; approval stays human |
| A plan-size trigger (slice count) | dropped by the user: size is not risk |
| Implementation review | owned by `wtk-deep-review` |

## Assumptions

| Assumption | Chosen default | Rationale | Confirmed? |
| --- | --- | --- | --- |
| Skill name | `wtk-plan-review` | it reviews `plan.md`; "spec" is not a WTK artifact name | y |
| Output location | `.wtk-plan-review/<feature>/`, gitignored | mirrors `.wtk-deep-review/`; review logs are not feature artifacts | y |
| Upstream text | rewritten, not copied; credited as inspiration | matches how `wtk-deep-review` credits the same author | y |
| Version metadata | `6.2.0` like the rest of the set; release bump through `wtk-ship` | the set ships one version | y |

**Open questions:** none - all resolved or logged above.

## Observable

| Surface | Decision | Landing |
| --- | --- | --- |
| command `validate_findings.py` | flags and defaults | AC 1, 7 - `--round` required, one positional path |
| command `validate_findings.py` | exit codes | AC 1, 2, 7 |
| command `validate_findings.py` | output on failure | AC 2, 3, 4 - names the defect |
| skill `wtk-plan-review` | what it asks and when | AC 8, 9 |
| skill `wtk-plan-review` | failure of one reviewer | AC 10, 13 |
| document findings file | structure | Landing door 1, AC 1 |
| document findings file | what the reader does next | AC 14 - selects findings |
| document disposition | structure | Landing door 3, AC 15 |
| plan presentation | the offer line | AC 17, 18, 19 |
| screen | n/a - this pack ships no screens |

## Sources

- Pedro Nauck, `skills/mine/spec-peer-review` (SKILL.md, `references/peer-review-prompt.md`, `references/quality-markers.md`, `scripts/validate-findings.sh`) - the opt-in single-round review, scoped-write reviewer and findings schema
- Conversation 2026-11-11 - separate skill, user-picked reviewers dispatched through the harness, four triggers, no slice-count trigger
