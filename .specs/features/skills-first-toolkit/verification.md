# Skills-only Workflow Toolkit verification

**Verdict**: FAIL
**Profile**: standard
**Diff range**: cd195aa4..61116cd7da616bc2a041d580a787ddfa8a6b905d
**Round**: 4 - scoped
**Verifier**: independent sub-agent (author `/root/skills_only_build` != verifier `/root/skills_only_verify`)

## Binding sources

| Source | Opened | Contradiction | Uncovered |
| --- | --- | --- | --- |
| Approved `plan.md` and `checks.md` | yes - unchanged approved artifacts | Plan and C1 describe selected self-contained skills; AD-041 and remediation README require the full 13-skill set while README lines 9-10 still tell users to add only the phase skills they use | User decision on individual closure versus full-set-only distribution remains open |
| Retired installer at `cd195aa4` | yes - exact 18 packet assets plus instruction-block behavior | none after remediation | - |
| Current QA scenario and report contract at committed `61116cd` | yes - current scenarios, charter, report, fixed bug records, and disposable readbacks | none | Public rollback fault injection is unavailable by design; QA keeps the two migration scenarios `untested`, while C7 retains exact technical proof |

## Checks

| Check | Claim | Proof run | Evidence | Result |
| --- | --- | --- | --- | --- |
| C1 | Published skills carry required runtime content | Fresh named suite exit 0; round-one isolated probe carried because skill files were unchanged | `tests/skills/distribution.test.js:16-35` proves references resolve only when all skill directories coexist. README now documents the full set, but `README.md:9-10` still offers partial selection and approved C1 still requires selected-skill closure. User decision pending. | FAIL |
| C2 | Skill installation leaves host harness files unchanged | Fresh named suite exit 0 | `tests/skills/distribution.test.js:43-64` snapshots all harness sentinels; remediation did not add an installer mutation path | PASS |
| C3 | Skill-installer-only distribution, no npm installer or new manifest | Fresh distribution suite 6/6; frozen-HEAD Skills CLI list exit 0 | `tests/skills/distribution.test.js:41-57` proves source locks containing WTK self entries suppress discovery and clean sources expose 13. Direct `add <HEAD-worktree> --list --full-depth` reported `Found 13 skills` and enumerated every approved name. `:86-99` retains the no-installer and exact route assertions. | PASS |
| C4 | Preview is complete and read-only | Fresh named suite exit 0; exact 18-packet legacy fixture exit 0 | `tests/skills/migration.test.js:52-70` proves read-only preview for owned files/blocks/links. Independent `cd195aa4` fixture produced 18 packet actions and no target writes before apply. | PASS |
| C5 | Apply backs up/removes verified ownership, preserves project bytes, removes adoption state, reports review prose | Fresh named suite exit 0; exact 18-packet fixture exit 0 | `tests/skills/migration.test.js:73-105` covers real legacy packet retirement and preservation; `:108-129` covers two blocks in one file. Independent fixture removed all 18 packets and the manifest with zero packets remaining. | PASS |
| C6 | Modified owned content prevents all writes and names conflict | Fresh named suite exit 0 | `tests/skills/migration.test.js:132-140` asserts refusal plus whole-tree equality | PASS |
| C7 | Publication failure restores files, links, modes, instructions, and adoption state | Fresh named suite exit 0 | `tests/skills/migration.test.js:143-154` asserts injected failure plus whole-tree equality | PASS |
| C8 | WTK resolves moved references without optional companions and makes no false tool claim | Fresh named suite exit 0 | `tests/skills/distribution.test.js:84-92` proves companions absent, old guideline paths absent, and native fallback text present | PASS |
| C9 | README distinguishes installation/instructions/companions and retained phase contracts remain reachable | Fresh distribution suite 6/6; QA contract suite 38/38; direct README/scenario/readback inspection | `README.md:84-92` has four recommended rows, each with source link and use case; Adaptive Guidelines is a non-recommended candidate. Both current full-set scenarios contain README's exact 13-skill membership, the retired layered scenario has no executable command, and QA report lines 16-20 records the resulting dispositions. | PASS |

## Coverage

| Set (size) | Recomputed from | Member -> proof | Unproven |
| --- | --- | --- | --- |
| Distribution doors (2) | plan Landing, AD-041, README, package | skill-installer-only C1-C3; adopter exit C4-C7 | selected-skill versus full-set distribution decision |
| Project harness files (6) | C2 sentinel inventory | `AGENTS.md`, `CLAUDE.md`, config, packets, knowledge, ignores -> C2 | - |
| Old ownership classes (3) | exact old assets and migration actions | managed blocks C4-C7; recorded files C4-C7; links C4-C7 | - |
| Migration outcomes (4) | migration API and expanded fixtures | preview C4; success C5; conflict C6; rollback C7 | - |
| Optional companions (4) | removed skill tree and fallback instructions | Ponytail, security lifecycle, Graphify, Graft -> C8 | - |
| Preserved phase contracts (5) | installed skills, README, tests, durable QA records | Lean artifacts C9; verifier separation C9; scoped validation C9; QA/review C9; delivery C9 | - |
| Approved decision updates (4) | AD-041 plus generated index | AD-001, AD-010, AD-033, AD-036 -> AD-041 | - |

## Test policy rows

No `Test policy` section exists in `checks.md`. Remediation added discriminating Skills CLI discovery and companion-table assertions, retained C5 discrimination, and QA independently compared scenario command membership. C1 remains intentionally unresolved pending the distribution-shape decision.

## Swept existing

- Validation: full-set reference resolution is green; individual selected-skill closure remains open.
- Failure modes: modified ownership refusal and rollback remain green after shared migration edits.
- Idempotency: successful cleanup removes adoption state; a later invocation is a no-op.
- Authorization: migration remains explicit; preview remains read-only.
- Data lifecycle: old adoption state and temporary journal are removed after success; backups retain bytes and modes.
- Dependency failure: optional companion absence retains native fallback text.
- Observability: exact legacy packets, links, blocks, files, ignore entries, conflicts, and manual-review prose are now observable.

## Reuse review

Scope: remediation `e0806212..03a32e3` plus affected consumers. Historical packet identity is kept as a bounded hash table in the one-time migration owner; generation remains owned by `wtk-config`. No duplicate active installer or migration owner was introduced. The skill-install command reuses the existing Skills CLI. No actionable reuse violation found.

## Construction verification

AD-041 records full-set installation, and the README now supplies a concrete full-set Skills CLI command. This closes the missing route but changes the approved selected-skill construction shape. C1 cannot pass until the user confirms full-set-only distribution or implementation supplies dependency-closed individual selection. The approved checks were not altered.

## Faults injected

Five remediation-specific mutations ran in detached scratch worktree `/tmp/wtk-reverify-mutants.1eoumC`; it was removed after the run.

| Mutation | Location | Covering proof | Killed |
| --- | --- | --- | --- |
| Replace legacy Claude planner hash with zeros | `scripts/migrate.js:38` | C5 legacy-packet proof exit 1 | yes |
| Remove instruction blocks in ascending offset order | `scripts/migrate.js:451` | C5 two-block proof exit 1 | yes |
| Point README install command at a wrong owner | `README.md:33` | C3 named proof exit 1 | yes |
| Point bundled config fallback at a missing asset | `.agents/skills/wtk-config/scripts/workflow_config.py:596` | workflow-config suite exit 1 | yes |
| Revert AD-001 index status while ledger retains AD-041 | `.specs/AD-INDEX.md:10` | AD index check exit 1 | yes |

No mutant survived. Real checkout porcelain changed during this pass because the separately dispatched QA session began editing its owned scenario files; all technical tests and mutations were anchored to committed `03a32e3` or detached worktrees, and this verifier did not alter those QA files or `skills-lock.json`.

Round 3 added one scoped C3 fault: restoring a `wtk` self entry to frozen HEAD's `skills-lock.json` changed direct `--list --full-depth` discovery from 13 to 12 and removed `wtk` from output. The mutant was killed and its detached worktree removed.

Round 4 added one scoped C9 fault: restoring Adaptive Guidelines as a fifth source-less recommendation made the named C9 proof fail `5 !== 4`. The mutant was killed and its detached worktree removed.

## Gates

- `node --test tests/skills/distribution.test.js tests/skills/migration.test.js` - exit 0; 10 passed, 0 failed.
- `python3 tools/test_workflow_config.py` - exit 0; 64 passed, 0 failed.
- `bun test tools/shared/tests/qa-skills.test.ts` - exit 0; 38 passed, 0 failed.
- `python3 .agents/skills/wtk-config/scripts/ad-index.py --check` - exit 0; index up to date.
- `npx --no-install skills add --help` - exit 0; documented add/update flags and multi-skill form supported.
- Exact `cd195aa4` legacy-packet hash audit - exit 0; 18/18 normalized hashes match `LEGACY_PACKET_HASHES`.
- Exact 18-packet preview/apply fixture - exit 0; preview actions 18, apply true, remaining packets 0, old manifest absent.
- `git diff --check e0806212..03a32e3` - exit 0; no whitespace errors.
- `python3 .agents/skills/wtk-lean/scripts/validate_verification.py skills-first-toolkit` - exit 1 as required for this internally consistent FAIL report; validator routes the remaining gaps back for decision/remediation.
- `node --test tests/skills/distribution.test.js` at `a9566e3` - exit 0; 6 passed, 0 failed, including clean/self-locked Skills CLI discovery.
- `node node_modules/skills/dist/cli.mjs add <frozen-HEAD-worktree> --list --full-depth` - exit 0; `Found 13 skills`, all approved names enumerated.
- `bun test tools/shared/tests/qa-skills.test.ts` at `a9566e3` - exit 0; 38 passed, 0 failed.
- `git diff --check a9566e3^..a9566e3` - exit 0; no whitespace errors.
- `node --test tests/skills/distribution.test.js` at `61116cd` - exit 0; 6 passed, 0 failed.
- `bun test tools/shared/tests/qa-skills.test.ts` at `61116cd` - exit 0; 38 passed, 0 failed.
- Independent README/scenario membership check - exit 0; README 13, both current scenarios 13/13 with no missing or extra names, retired scenario has no install command, four linked recommendation rows, Adaptive Guidelines candidate only.
- `git diff --check a9566e3..61116cd` - exit 0; no whitespace errors.
- Full gate not repeated. Round-one `bun run test:all` had 89/89 Bun and 16/16 Node tests green and stopped only at the now-corrected workflow-config expectation. Remediation changed migration/distribution tests, QA scenario consumers, the workflow-config expectation, and AD files; each causal path received the fresh scoped suites above. Dependencies, lockfile, other Python modules, and other Bun suites are unchanged from that run.

## QA disposition

The independent QA report at `docs/qa/reports/2026-09-23-skills-only-workflow.md` records:

- full 13-skill installation and host-state preservation: pass;
- optional companion/provenance documentation: pass;
- public migration preview, apply, and conflict: passed reachable legs;
- public publication-failure rollback: honestly `untested`, because the CLI exposes no safe injection flag;
- exact rollback through the shipped failure hook: passed as technical-forward evidence and agrees with C7.

Other explicit limits are local-source installation without network/registry resolution, no optional companion installation, and no agent-behavior claim from QA. These limits do not weaken C9 or contradict C7.

## Ranked gaps

1. **Decision required - C1:** approved selected-skill self-containment conflicts with remediation's full-set-only shape. README itself currently says both “add only the phase skills the project uses” and “install the full WTK set.” Keep FAIL until the user chooses the public contract.

## Verification stage receipt

- Stage: Technical verification, round 4 scoped
- Revision: `61116cd7da616bc2a041d580a787ddfa8a6b905d`
- Start: unavailable
- End: 2026-09-23 06:11:59 UTC
- Duration: unavailable
- Model: GPT-5 verifier role
- Effort: unavailable
- Input tokens: unavailable
- Output tokens: unavailable
- Estimated token cost: unavailable
- Validation overhead: prior scoped gates retained; round 4 added 2 scoped gates, 1 semantic membership/readback check, and 1 isolated discrimination run
- Reused evidence: C2-C8 and unaffected full-gate portions carried by causal input comparison; C9 rerun fresh at `61116cd`; C1 isolated-copy result carried because skill contents are unchanged
- Waiting/blockers: C1 user decision
- Unmeasured scope: host token telemetry and exact actor timing; public rollback injection, network GitHub resolution, and optional companion installation remain explicit QA limitations
