# Project-owned agent settings verification

**Verdict**: PASS
**Profile**: standard
**Diff range**: 868baa1..35a5fdf
**Round**: 2 - scoped
**Verifier**: independent sub-agent (author != verifier)

## Binding sources

No external binding source was declared. The approved `plan.md`, `checks.md`, complete feature diff,
current WTK instruction surfaces, and retained executable contracts were compared. No contradiction
was found. Round 2 inspected remediation commit `35a5fdf` without author context.

## Checks

| Check | Claim | Proof run | Evidence | Result |
| --- | --- | --- | --- | --- |
| C1 | exactly 12 installable WTK skills, no config payload | carried from `07d658df`; remediation changes no skill, package, distribution, or product file | `tests/skills/distribution.test.js:17` asserts the exact 12-skill list; lines 125-126 assert Skills CLI exit 0 and `Found 12 skills` | PASS |
| C2 | TOML-free routing preserves Claude, Codex, and Cursor native files | fresh clean-worktree native-routing run: 8 passed | `tools/test_native_agent_routing.py:99` asserts byte equality over all 18 baseline-created files; line 100 asserts no `.wtk.toml` | PASS |
| C3 | source checkout has no WTK TOML and preserves all existing native metadata | fresh clean-worktree proof passed; optional source-file probe covers all 18; prior Cursor mutant killed | `tools/test_native_agent_routing.py:108` asserts 18 baseline entries; line 109 asserts six Cursor entries; lines 110-120 validate present source files and all scratch members | PASS |
| C4 | snapshot stores route identity with no model, effort, or config version | fresh clean-worktree native-routing run passed | `tools/test_native_agent_routing.py:134` asserts verifier route keys; lines 136-138 reject model, effort, and config version; line 142 asserts persisted equality | PASS |
| C5 | fixed stall threshold is 3 and halts on the third consecutive stall | carried from `07d658df`; remediation changes no convergence code or test | `tools/test_review_convergence.py:195`-`tools/test_review_convergence.py:201` assert counts, threshold `3`, open stalls, and halt | PASS |
| C6 | Deep Review is on demand and the builder is sequential; direct skill remains available | fresh clean-worktree native-routing run passed; direct-skill evidence carried from `07d658df` | `tools/test_native_agent_routing.py:155` asserts skip/zero groups; line 156 asserts disabled parallelization; `tools/test_wtk_deep_review_contract.py:15` asserts direct skill name | PASS |
| C7 | absent task choice uses safe `auto` QA fallback | carried from `07d658df`; remediation changes no QA adapter, skill, or proof | `tools/test_jev_qa_adapter.py:196`-`tools/test_jev_qa_adapter.py:207` assert fallback order; lines 244-251 allow safe pre-action fallback; lines 278-285 forbid unsafe replay | PASS |
| C8 | migration recognizes, removes, and protects all 18 historical packets | fresh clean-worktree migration matrix: 2 passed; prior hash mutant killed | `tests/skills/migration.test.js:99` creates all 18 tracked fixtures; lines 104-114 assert preview/apply removal of every path; lines 125-133 reject edits for every provider/role | PASS |
| C9 | current docs, inventory, references, QA routes, and AD index agree | carried from `07d658df`; remediation changes only tests, tracked fixtures, and checks checkpoint | `tests/skills/distribution.test.js:38` asserts package/catalog equality; lines 47-61 assert ownership/default guidance; lines 82-94 assert AD/helper/config removal | PASS |

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
| Installed skill routes (12) | source skill directories and Skills CLI output | C1/C9 over all 12 | - |

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

## Reuse review

Scope: `868baa1..35a5fdf`. No confirmed reuse violation. Relocated helpers remain single-owned and
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

Round-2 mutations ran in a detached clean HEAD worktree. The scratch checkout was removed and the
real tree returned to its opening porcelain state, containing only this verifier-owned report.

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

No full-gate repeat was selected: the prior full run remains input-equivalent outside the freshly
executed changed tests, and the remediation added no shared runtime or dependency uncertainty.

## QA disposition

QA remains required because the feature changes the public skill catalog, adoption command,
migration behavior, agent-facing configuration, and docs-as-interface. Existing affected scenarios
include `ADP-adopt-workflow-safely`, `ADP-install-versioned-workflow-package`,
`CFG-keep-local-artifacts-out-of-git`, `CFG-resolve-deep-review-cadence`,
`QAS-use-optional-jev-qa-adapter`, and `REL-report-current-workflow-release`.

## Ranked gaps

None. Round-1 C3, C8, and retained-route proof gaps are closed by `35a5fdf`.

## Execution metrics

Round 1 technical verification: actor `/root/native_settings_verify`; OpenAI GPT-5; 2026-09-23
20:30:29-20:48:12 UTC (17m43s); tokens and cost unavailable; Jev adviser 607 input / 74 output.

Round 2 scoped recheck: same actor/model; start timestamp unavailable, stop 2026-09-23 20:59:10 UTC;
base-model tokens and cost unavailable. Validation overhead: clean routing proof 1.28s, clean
migration proof 0.07s, two focused mutant reruns under 0.1s each, no full gate. Verification cycles:
2 completed passes, 1 implementation return, 1 completed loop, 0 pending; first-pass acceptance no,
final technical acceptance yes. QA and Deep Review were not run in this stage. Optimization: reused
the input-equivalent full gate and reran only remediation-invalidated proof surfaces.
