# Project-owned agent settings verification

**Verdict**: PASS
**Profile**: standard
**Diff range**: 868baa1..457ad3cf
**Round**: 3 - scoped follow-up
**Verifier**: independent sub-agent (author != verifier)

## Binding sources

No external binding source was declared. The approved `plan.md`, `checks.md`, complete feature diff,
current WTK instruction surfaces, and retained executable contracts were compared. No contradiction
was found. Round 2 inspected remediation commit `35a5fdf`; round 3 inspected QA remediation
`f9b1c4d` and the intervening durable QA records without author context.

## Checks

| Check | Claim | Proof run | Evidence | Result |
| --- | --- | --- | --- | --- |
| C1 | exactly 12 installable WTK skills, no config payload | fresh clean-worktree distribution batch: 2 passed | `tests/skills/distribution.test.js:17` asserts the exact 12-skill list; lines 42-52 assert exactly 12 tracked, resolving Claude aliases; lines 143-144 assert Skills CLI exit 0 and `Found 12 skills` | PASS |
| C2 | TOML-free routing preserves Claude, Codex, and Cursor native files | fresh clean-worktree native-routing run: 8 passed | `tools/test_native_agent_routing.py:99` asserts byte equality over all 18 baseline-created files; line 100 asserts no `.wtk.toml` | PASS |
| C3 | source checkout has no WTK TOML and preserves all existing native metadata | fresh clean-worktree proof passed; optional source-file probe covers all 18; prior Cursor mutant killed | `tools/test_native_agent_routing.py:108` asserts 18 baseline entries; line 109 asserts six Cursor entries; lines 110-120 validate present source files and all scratch members | PASS |
| C4 | snapshot stores route identity with no model, effort, or config version | fresh clean-worktree native-routing run passed | `tools/test_native_agent_routing.py:134` asserts verifier route keys; lines 136-138 reject model, effort, and config version; line 142 asserts persisted equality | PASS |
| C5 | fixed stall threshold is 3 and halts on the third consecutive stall | carried from `07d658df`; remediation changes no convergence code or test | `tools/test_review_convergence.py:195`-`tools/test_review_convergence.py:201` assert counts, threshold `3`, open stalls, and halt | PASS |
| C6 | Deep Review is on demand and the builder is sequential; direct skill remains available | route evidence carried from `35a5fdf`; direct skill alias resolved fresh at `f9b1c4d` | `tools/test_native_agent_routing.py:155` asserts skip/zero groups; line 156 asserts disabled parallelization; `tests/skills/distribution.test.js:49`-`tests/skills/distribution.test.js:52` resolve every direct skill alias | PASS |
| C7 | absent task choice uses safe `auto` QA fallback | carried from `07d658df`; remediation changes no QA adapter, skill, or proof | `tools/test_jev_qa_adapter.py:196`-`tools/test_jev_qa_adapter.py:207` assert fallback order; lines 244-251 allow safe pre-action fallback; lines 278-285 forbid unsafe replay | PASS |
| C8 | migration recognizes, removes, and protects all 18 historical packets | fresh clean-worktree migration matrix: 2 passed; prior hash mutant killed | `tests/skills/migration.test.js:99` creates all 18 tracked fixtures; lines 104-114 assert preview/apply removal of every path; lines 125-133 reject edits for every provider/role | PASS |
| C9 | current docs, inventory, references, QA routes, and AD index agree | fresh clean-worktree distribution batch: 2 passed; current QA contract file: 38 passed | `tests/skills/distribution.test.js:38` asserts package/catalog equality; lines 42-52 assert tracked alias equality and resolution; lines 62-76 assert ownership/default guidance; lines 86-90 inspect current scenario interfaces; `tools/shared/tests/qa-skills.test.ts:1053`-`tools/shared/tests/qa-skills.test.ts:1063` assert current Unreleased guidance while retaining release 1.4.1 | PASS |

## Coverage

| Set (size) | Recomputed from | Member -> proof | Unproven |
| --- | --- | --- | --- |
| One-way doors (3) | plan Landing plus source tree | native metadata C2/C3 · 12-skill catalog C1/C9 · remediation default C5 | - |
| Native providers (3) | route providers and tracked baseline | Claude C2/C3 · Codex C2/C3 · Cursor C2/C3 | - |
| Removed WTK config outputs (4) | diff/package inventory | TOML C2/C3 · root example C1/C9 · bundled example C1/C9 · generated packets C8 | - |
| Feature route snapshot (9 keys) | `workflow_route.SNAPSHOT_KEYS` at `.agents/skills/wtk-lean/scripts/workflow_route.py:20` | identity/model boundary C4 · verification profile derive/freeze/refresh `tools/test_native_agent_routing.py:174` · fail-closed resume line 193 · defaults C6 | - |
| Route boundary failures (5) | retained route branches and removed-test audit | profile derive/freeze/refresh line 174 · missing agent line 193 · invalid snapshot line 204 · stale snapshot line 213 · slice assertion/no write line 228 | - |
| Fixed defaults (4) | plan Flow and current owners | stall attempts C5 · review skip C6 · sequential builder C6 · QA auto C7 | - |
| Historical packet matrix (18) | tracked fixtures plus migration provider/role set | preview/apply C8 over 3 providers × 6 roles; edited-packet refusal C8 over the same matrix | - |
| Installed skill routes (12) | source directories, tracked Claude aliases, and Skills CLI output | C1/C9 over all 12 directories and all 12 resolving aliases | - |

## Test policy rows

`checks.md` declares no `Test policy` rows. Round-2 direct review confirms the restored cases assert
observable route results and failure behavior: profile values across resume/refresh, exact failure
classes for missing agents and invalid/stale snapshots, and slice mismatch with no snapshot write.
Tracked migration fixtures are independent packet bytes consumed through the public migration helper;
they are not generated from `LEGACY_PACKET_HASHES` or from migration normalization code.

## Swept existing

- Validation, failure modes, idempotency, authorization, concurrency, data lifecycle, dependency
  fallback, state transitions, and observability all have located evidence.
- Source preservation is reproducible in a clean worktree through the tracked 18-entry baseline and
  still checks ignored host files when they exist.
- Migration preview/apply and edited-packet refusal cover every historical provider/role member.
- Source aliases contain exactly the 12 supported WTK skills, all resolve to their canonical skill
  directories, and no `wtk-config` alias remains. Current Unreleased guidance names the skill-only
  route while the historical 1.4.1 block remains unchanged.

## Reuse review

Scope: `868baa1..f9b1c4d`. No confirmed reuse violation. Relocated helpers remain single-owned and
all consumers point to their new owners. Remediation adds test fixtures and boundary cases without
duplicating runtime implementation. No UI or rendered surface was in scope. Historical skipped QA
records remain historical evidence.

## Faults injected

| Mutation | Location | Killed |
| --- | --- | --- |
| restored a `wtk-config` skill directory | `.agents/skills/wtk-config/SKILL.md` | yes - carried from `07d658df`; relevant inputs unchanged |
| added a persisted `model` field to a role route | `.agents/skills/wtk-lean/scripts/workflow_route.py:201` | yes - carried from `07d658df`; route implementation unchanged |
| changed default stall threshold `3` to `2` | `.agents/skills/wtk-ship/remediation.py:16` | yes - carried from `07d658df`; convergence inputs unchanged |
| changed Cursor planner model and effort | `.cursor/agents/planner.md:5` | yes - reinjected at `35a5fdf`; C3 failed on the Cursor checksum |
| corrupted `cursor/designer` legacy packet hash | `scripts/migrate.js:54` | yes - reinjected at `35a5fdf`; C8 omitted the packet from preview and failed |
| restored the dangling tracked `wtk-config` Claude alias | `.claude/skills/wtk-config` | yes - reinjected at `f9b1c4d`; C9 alias-set equality failed |

Round-2 and round-3 mutations ran in detached clean HEAD worktrees. Scratch checkouts were removed
and the real tree returned to its opening porcelain state.

## Gate

Reused full gate: `bun run test:all` at `07d658df` exited 0 in 59.4 seconds with 80 Bun tests, 20
Node tests, and every then-tracked Python suite passing. Remediation commit `35a5fdf` changes only
tests, tracked fixtures, and the checks checkpoint; no product/runtime, package, instruction, QA, or
documentation input changed. Fresh proofs cover every changed executable test input:

- Clean HEAD worktree `python3 tools/test_native_agent_routing.py`: exit 0, 8 passed.
- Clean HEAD worktree migration matrix selector: exit 0, 2 passed.
- Fixture inventory: 18 tracked packet fixtures; baseline 18 entries split 6/6/6.
- `validate_checks.py native-agent-settings`: exit 0, 0 errors, 3 pre-existing warnings.
- `git diff --check 868baa1..HEAD`: exit 0.

Post-QA remediation evidence at `f9b1c4d`:

- Clean HEAD worktree C1/C9 distribution batch: exit 0, 2 passed.
- `bun test tools/shared/tests/qa-skills.test.ts`: exit 0, 38 passed, 544 expectations.
- Alias inventory: 12 tracked aliases, 12 resolved, stale config alias absent.
- Reintroduced stale-alias mutant: killed by C9 alias-set equality.

No full-gate repeat was selected. Diffs after `35a5fdf` do not touch route, migration, remediation,
QA adapter runtime, package manifest, or their C2-C8 proofs. Changed distribution, QA-scenario, and
CHANGELOG inputs ran through their owning tests above; remaining full-gate inputs are equivalent.

## QA disposition

QA is complete. The durable report at
`docs/qa/reports/2026-09-23-native-agent-settings.md` records the initial walk, remediation snapshot
`f9b1c4d`, and passing scoped retest committed at `457ad3cf`. Both findings are fixed:

- `BUG-20260923-source-retains-removed-wtk-config-link`: fixed; alias inventory retest passed.
- `BUG-20260923-changelog-describes-retired-installer`: fixed; current-guidance and historical-1.4.1
  preservation retest passed.

`CFG-keep-local-artifacts-out-of-git` and `REL-report-current-workflow-release` now record `pass`,
`fix_status: fixed`, and `retest_status: pass`. Final QA acceptance is yes after one completed fix
loop; first-pass QA acceptance remains no.

Limitations remain explicit: public rollback injection is unavailable, so the two adoption/migration
scenarios remain `untested` with every reachable public leg passing. No live browser, Jev runtime,
provider, Playwright MCP, or reload oracle was available; the optional QA-adapter journey remains
`untested` with its reachable safe-fallback legs passing. Network/registry access was outside the QA
profile, and Skills CLI used a frozen local source copy.

## Ranked gaps

None. Round-1 technical gaps are closed by `35a5fdf`; post-QA technical surfaces are green at
`f9b1c4d`; QA retest closes both reported defects at `457ad3cf` with the limitations above.

## Execution metrics

Round 1 technical verification: actor `/root/native_settings_verify`; OpenAI GPT-5; 2026-09-23
20:30:29-20:48:12 UTC (17m43s); tokens and cost unavailable; Jev adviser 607 input / 74 output.

Round 2 scoped recheck: same actor/model; start timestamp unavailable, stop 2026-09-23 20:59:10 UTC;
base-model tokens and cost unavailable. Validation overhead: clean routing proof 1.28s, clean
migration proof 0.07s, two focused mutant reruns under 0.1s each, no full gate. Verification cycles:
2 completed passes, 1 implementation return, 1 completed loop, 0 pending; first-pass acceptance no,
final technical acceptance yes. QA and Deep Review were not run in this stage. Optimization: reused
the input-equivalent full gate and reran only remediation-invalidated proof surfaces.

Round 3 scoped follow-up: same actor/model; start timestamp unavailable, stop 2026-09-23 21:50:34
UTC; base-model tokens and cost unavailable. Validation overhead: distribution batch 0.66s, QA
contract file 1.09s, one alias mutant 0.20s, no full gate. Technical verification cycles remain 2
completed passes and 1 completed implementation loop; this post-QA follow-up adds no technical
return. QA subsequently completed its one remediation return. Optimization: reused C2-C8 and full
gate evidence after path-level input equivalence, rerunning only changed distribution/docs contracts.

QA execution receipt from the durable report: actor `/root/native_settings_qa_execute`, OpenAI GPT-5;
initial measured interval 2026-09-23 21:19:47-21:42:30 UTC (22m43s partial) plus remediation retest
2026-09-23 21:52:44-21:59:50 UTC (7m06s), combined non-overlapping actor time 29m49s partial.
Tokens, billing tier, and cost unavailable. One initial QA round and one scoped retest completed one
two-finding return/fix/recheck loop with zero pending returns; final QA acceptance yes, first-pass no.
Validation overhead: targeted QA gates 0.8s and 1.0s; no QA full gate. Input-equivalent install,
migration, and default evidence was reused. Public rollback and live-provider/browser scope remain
unmeasured as described above.
