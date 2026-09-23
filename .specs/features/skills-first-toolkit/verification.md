# Skills-only Workflow Toolkit verification

**Verdict**: PASS
**Profile**: standard
**Diff range**: cd195aa4..ac6afbb095192526dda34a8f18cf688367d32c97
**Round**: 7 - scoped
**Verifier**: independent sub-agent (author `/root/skills_only_build` != verifier `/root/skills_only_verify`)

## Binding sources

| Source | Opened | Contradiction | Uncovered |
| --- | --- | --- | --- |
| Approved `plan.md` and `checks.md` | yes - updated by the user's explicit full-set decision | none | - |
| Retired installer at `cd195aa4` | yes - exact 18 packet assets plus instruction-block behavior | none after remediation | - |
| Current QA scenario and report contract at committed `ac6afbb` | yes - all active source-install scenarios, charter, final report, fixed bug records, and disposable readbacks | none | - |

## Checks

| Check | Claim | Proof run | Evidence | Result |
| --- | --- | --- | --- | --- |
| C1 | Complete installed 13-skill set carries required runtime content | Fresh named proof exit 0; isolated fault exit 1; QA install evidence causally equivalent | `tests/skills/distribution.test.js:16-52` copies only all 13 skill directories, proves source `docs/toolkit/guidelines/` absent, and resolves Markdown, local script/reference, and absolute WTK skill paths inside that isolated set. QA's public install at `a9566e3` found all 13 and zero unresolved references; `.agents/skills`, `package.json`, and `skills-lock.json` are unchanged since that snapshot. | PASS |
| C2 | Skill installation leaves host harness files unchanged | Fresh distribution suite exit 0 | `tests/skills/distribution.test.js:71-96` snapshots all harness sentinels; QA public installation also preserved them byte-for-byte | PASS |
| C3 | Skill-installer-only distribution, no npm installer or new manifest | Fresh distribution suite 6/6; prior frozen-HEAD Skills CLI list retained by causal equivalence | `tests/skills/distribution.test.js:53-69` proves source locks containing WTK self entries suppress discovery and clean sources expose 13. `:98-111` retains no-installer and exact route assertions. | PASS |
| C4 | Preview is complete and read-only | Fresh named suite exit 0; exact 18-packet legacy fixture exit 0 | `tests/skills/migration.test.js:52-70` proves read-only preview for owned files/blocks/links. Independent `cd195aa4` fixture produced 18 packet actions and no target writes before apply. | PASS |
| C5 | Apply backs up/removes verified ownership, preserves project bytes, removes adoption state, reports review prose | Fresh named suite exit 0; exact 18-packet fixture exit 0 | `tests/skills/migration.test.js:73-105` covers real legacy packet retirement and preservation; `:108-129` covers two blocks in one file. Independent fixture removed all 18 packets and the manifest with zero packets remaining. | PASS |
| C6 | Modified owned content prevents all writes and names conflict | Fresh named suite exit 0 | `tests/skills/migration.test.js:132-140` asserts refusal plus whole-tree equality | PASS |
| C7 | Publication failure restores files, links, modes, instructions, and adoption state | Fresh named suite exit 0 | `tests/skills/migration.test.js:143-154` asserts injected failure plus whole-tree equality | PASS |
| C8 | WTK resolves moved references without optional companions and makes no false tool claim | Fresh distribution suite exit 0 | `tests/skills/distribution.test.js:113-124` proves companions absent, old guideline paths absent, and native fallback text present | PASS |
| C9 | README distinguishes installation/instructions/companions and retained phase contracts remain reachable | Fresh distribution suite 6/6; fresh QA contract suite 38/38; direct sweep of every active source-install scenario | README recommendations and prior QA fixes remain correct. All four active scenarios containing the WTK Skills CLI route select exactly the approved 13-skill set; `QAS-use-optional-jev-qa-adapter.md:19-22` invokes the QA route only after full-set installation. | PASS |

## Coverage

| Set (size) | Recomputed from | Member -> proof | Unproven |
| --- | --- | --- | --- |
| Distribution doors (2) | updated plan Landing, AD-041, README, package | complete 13-skill set C1-C3; adopter exit C4-C7 | - |
| Project harness files (6) | C2 sentinel inventory | `AGENTS.md`, `CLAUDE.md`, config, packets, knowledge, ignores -> C2 | - |
| Old ownership classes (3) | exact old assets and migration actions | managed blocks C4-C7; recorded files C4-C7; links C4-C7 | - |
| Migration outcomes (4) | migration API and expanded fixtures | preview C4; success C5; conflict C6; rollback C7 | - |
| Optional companions (4) | removed skill tree and fallback instructions | Ponytail, security lifecycle, Graphify, Graft -> C8 | - |
| Preserved phase contracts (5) | installed skills, README, tests, durable QA records | Lean artifacts C9; verifier separation C9; scoped validation C9; QA/review C9; delivery C9 | - |
| Approved decision updates (4) | AD-041 plus generated index | AD-001, AD-010, AD-033, AD-036 -> AD-041 | - |

## Test policy rows

No `Test policy` section exists in `checks.md`. Remediation added isolated full-set reference closure, discriminating Skills CLI discovery and companion-table assertions, retained C5 discrimination, and QA independently compared scenario command membership. The checks validator emits one acknowledged warning for the absent optional section and zero errors.

## Swept existing

- Validation: the complete supported 13-skill set resolves every scanned runtime reference in isolation; subset installation is explicitly unsupported.
- Failure modes: modified ownership refusal and rollback remain green after shared migration edits.
- Idempotency: successful cleanup removes adoption state; a later invocation is a no-op.
- Authorization: migration remains explicit; preview remains read-only.
- Data lifecycle: old adoption state and temporary journal are removed after success; backups retain bytes and modes.
- Dependency failure: optional companion absence retains native fallback text.
- Observability: exact legacy packets, links, blocks, files, ignore entries, conflicts, and manual-review prose are now observable.

## Reuse review

Scope: remediation `e0806212..03a32e3` plus affected consumers. Historical packet identity is kept as a bounded hash table in the one-time migration owner; generation remains owned by `wtk-config`. No duplicate active installer or migration owner was introduced. The skill-install command reuses the existing Skills CLI. No actionable reuse violation found.

## Construction verification

The user explicitly chose the complete 13-skill installation unit. The plan, C1, Coverage row, README, and isolated proof now agree on that construction shape. No individual phase subset is promised.

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

Round 5 added one scoped C1 fault: changing `wtk-ship`'s raw cross-skill validation reference to a missing WTK path made the isolated full-set proof fail at `tests/skills/distribution.test.js:48`. The mutant was killed and its detached worktree removed.

## Gates

- `node --test tests/skills/distribution.test.js tests/skills/migration.test.js` - exit 0; 10 passed, 0 failed.
- `python3 tools/test_workflow_config.py` - exit 0; 64 passed, 0 failed.
- `bun test tools/shared/tests/qa-skills.test.ts` - exit 0; 38 passed, 0 failed.
- `python3 .agents/skills/wtk-config/scripts/ad-index.py --check` - exit 0; index up to date.
- `npx --no-install skills add --help` - exit 0; documented add/update flags and multi-skill form supported.
- Exact `cd195aa4` legacy-packet hash audit - exit 0; 18/18 normalized hashes match `LEGACY_PACKET_HASHES`.
- Exact 18-packet preview/apply fixture - exit 0; preview actions 18, apply true, remaining packets 0, old manifest absent.
- `git diff --check e0806212..03a32e3` - exit 0; no whitespace errors.
- `python3 .agents/skills/wtk-lean/scripts/validate_verification.py skills-first-toolkit` at `ac6afbb` - exit 0; 0 errors, 0 warnings.
- `node --test tests/skills/distribution.test.js` at `a9566e3` - exit 0; 6 passed, 0 failed, including clean/self-locked Skills CLI discovery.
- `node node_modules/skills/dist/cli.mjs add <frozen-HEAD-worktree> --list --full-depth` - exit 0; `Found 13 skills`, all approved names enumerated.
- `bun test tools/shared/tests/qa-skills.test.ts` at `a9566e3` - exit 0; 38 passed, 0 failed.
- `git diff --check a9566e3^..a9566e3` - exit 0; no whitespace errors.
- `node --test tests/skills/distribution.test.js` at `61116cd` - exit 0; 6 passed, 0 failed.
- `bun test tools/shared/tests/qa-skills.test.ts` at `61116cd` - exit 0; 38 passed, 0 failed.
- Independent README/scenario membership check - exit 0; README 13, both current scenarios 13/13 with no missing or extra names, retired scenario has no install command, four linked recommendation rows, Adaptive Guidelines candidate only.
- `git diff --check a9566e3..61116cd` - exit 0; no whitespace errors.
- `node --test --test-name-pattern='published WTK skills resolve every local reference' tests/skills/distribution.test.js` at `b3e430b` - exit 0; 1 passed, 0 failed.
- `node --test tests/skills/distribution.test.js` at `b3e430b` - exit 0; 6 passed, 0 failed.
- `git diff --quiet a9566e3..b3e430b -- .agents/skills package.json skills-lock.json` - exit 0; QA public-install inputs are equivalent.
- WTK runtime source-doc scan - exit 0; no `docs/toolkit/guidelines/` reference in the 13 installed skill trees.
- README installation semantic check - exit 0; full-set unit true, subset unsupported true, old ambiguous wording absent, 13 unique skill names.
- `validate_plan.py skills-first-toolkit` - exit 0; 0 errors, 0 warnings. `validate_checks.py skills-first-toolkit` - exit 0; 0 errors, 1 absent-Test-policy warning.
- `git diff --check 61116cd..b3e430b` - exit 0; no whitespace errors.
- `bun test tools/shared/tests/qa-skills.test.ts` at `da1e239` - exit 0; 38 passed, 0 failed.
- Active source-install scenario sweep at `da1e239` - exit 0; 4 scenarios, each exact 13/13 membership, zero missing or extra skills.
- `git diff --check b3e430b..da1e239` - exit 0; no whitespace errors.
- Final QA closeout inspection at `ac6afbb` - exact 13-skill contract recheck recorded for all active install scenarios; local-source installation reuse is justified by unchanged `.agents/skills`, `package.json`, and `skills-lock.json`; limitations remain explicit.
- `git diff --check da1e239..ac6afbb` - exit 0; no whitespace errors.
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

None.

## Verification stage receipt

- Stage: Technical verification, round 7 scoped
- Revision: `ac6afbb095192526dda34a8f18cf688367d32c97`
- Start: unavailable
- End: 2026-09-23 13:52:36 UTC
- Duration: unavailable
- Model: GPT-5 verifier role
- Effort: unavailable
- Input tokens: unavailable
- Output tokens: unavailable
- Estimated token cost: unavailable
- Validation overhead: prior scoped gates retained; round 5 added 4 scoped checks, 2 artifact validators and 1 isolated discrimination run; round 6 added 1 scoped gate and 1 active-scenario sweep; round 7 added QA closeout/readback inspection
- Reused evidence: C2-C8 and unaffected full-gate portions carried by causal input comparison; QA public installation reused after exact input-equivalence check; C1 fresh at `b3e430b`; C9 fresh at `da1e239`; `ac6afbb` changes only QA report/bug closeout prose
- Waiting/blockers: none
- Unmeasured scope: host token telemetry and exact actor timing; public rollback injection, network GitHub resolution, and optional companion installation remain explicit QA limitations
