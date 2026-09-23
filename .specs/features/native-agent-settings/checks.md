# Project-owned agent settings checks

Profile: standard
Plan: `.specs/features/native-agent-settings/plan.md`

9 checks in 3 slices · 3 one-way doors · 0 open blockers

## Checks

### S1 - Project-owned native agent settings

**C1** - Skills CLI discovers exactly 12 WTK skills and neither source nor isolated installation includes `wtk-config` or WTK TOML examples (WTKCFG-01, AC 1; WTKCFG-03, AC 11, 12)
Proof: `node --test --test-name-pattern='full WTK set has twelve skills and no WTK config payload' tests/skills/distribution.test.js`

**C2** - A project with no WTK TOML can route a Lean feature and retain byte-identical native Claude, Codex, and Cursor model/effort metadata (WTKCFG-01, AC 2, 3)
Proof: `python3 tools/test_native_agent_routing.py -k toml_free_route_preserves_native_agents`

**C3** - The source checkout has no local `.wtk.toml` after cleanup, while its native agent files retain their pre-change metadata bytes (WTKCFG-01, AC 4)
Proof: `python3 tools/test_native_agent_routing.py -k source_checkout_has_no_wtk_toml`

**C4** - A new feature `workflow.json` stores provider/role identity for resume but no `model`, `effort`, or WTK config version (WTKCFG-01, AC 5)
Proof: `python3 tools/test_native_agent_routing.py -k snapshot_freezes_identity_not_model`

### S2 - Fixed defaults and legacy cleanup

**C5** - Remediation reports threshold `3`, continues after attempts 1 and 2 without progress, and halts after attempt 3 (WTKCFG-02, AC 6)
Proof: `python3 -c 'from tools import test_review_convergence as t; t.test_same_fingerprint_counts_failed_verifier_and_halts_after_three_stalls()'`

**C6** - No feature request schedules Deep Review automatically; an explicit direct Deep Review remains callable (WTKCFG-02, AC 7)
Proof: `python3 tools/test_native_agent_routing.py -k review_is_on_demand`

**C7** - QA with no task-scoped adapter selection uses the existing `auto` order and safe fallback (WTKCFG-02, AC 8)
Proof: `python3 -m unittest tools.test_jev_qa_adapter.AdapterTests.test_missing_prerequisite_matrix_falls_back tools.test_jev_qa_adapter.AdapterTests.test_pre_action_timeout_allows_playwright_fallback tools.test_jev_qa_adapter.AdapterTests.test_unsafe_timeout_forbids_automatic_fallback`

**C8** - Migration still previews/removes all 18 exact historical generated packets without current WTK templates and refuses edited or consumer-owned packets (WTKCFG-02, AC 9)
Proof: `node --test --test-name-pattern='migration retires historical packets without templates' tests/skills/migration.test.js`

### S3 - Current documentation and helper ownership

**C9** - Current README, AGENTS, skill references, QA routes, package inventory, and decision index agree on 12 skills, project-native model/effort, TOML-free defaults, and relocated helper paths (WTKCFG-03, AC 10, 11, 12)
Proof: `node --test --test-name-pattern='native agent ownership and current WTK catalog are consistent' tests/skills/distribution.test.js`

## Coverage

| Set (size) | Member -> proof | Unproven |
| --- | --- | --- |
| One-way doors (3) | native metadata ownership C2, C3 · twelve-skill catalog C1, C9 · fixed remediation default C5 | - |
| Native providers (3) | Claude C2 · Codex C2 · Cursor C2 | - |
| Removed WTK config outputs (4) | `.wtk.toml` C2, C3 · root example C1 · bundled example C1 · generated provider packets C2, C8 | - |
| Feature route snapshot (4) | provider C4 · role identity C4 · no model C4 · no effort C4 | - |
| Fixed defaults (4) | stall attempts 3 C5 · Deep Review skip C6 · sequential builder C6 · QA auto C7 | - |
| Historical packet providers (3) | Claude C8 · Codex C8 · Cursor C8, table-driven over six roles each | - |
| Installed skill routes (12) | C1, C9; table-driven list of all 12 in distribution proof | - |

- C2, C3, C4, C5, C7, and C8 assert behavior at file-system or route boundaries, not matching prose.
- C9 inspects current instruction surfaces semantically; it does not freeze incidental wording.

## Swept

- validation: C1, C2, C4 - catalog, route input, and snapshot shape
- failure modes: C2, C8 - no missing-TOML failure; modified legacy packets are refused
- idempotency: C4 - resume reuses the same route identity; no model regeneration
- authorization: C2, C3 - project-native agent metadata remains project-owned
- concurrency: C6 - one sequential Lean builder; no config-controlled parallel execution
- data lifecycle: C3, C8 - old local config removed and old generated packets retired safely
- dependency failure: C7 - QA adapter safe fallback; graph tools remain optional through existing rules
- state transitions: C5 - remediation progress/non-progress transitions halt at the third stall
- observability: C5, C9 - reported threshold and current setup instructions name the defaults

## Handoff

The project's declared budget is 200k tokens. Pre-edit `wc -c / 4` arithmetic measured S1 at
507,883 bytes / 4 ≈ 126,971 tokens; S2 at 45,897 / 4 ≈ 11,474; and S3 at 376,854 / 4 ≈ 94,214.
The cumulative estimate is 930,634 bytes / 4 ≈ 232,659 tokens, above 200k. The proposed
whole-slice cut is after S2: S1+S2 = 553,780 bytes / 4 = 138,445 tokens; S3 ≈ 94,214.
Mechanism: sequential whole-slice handoff after S2, chosen by the user. The first builder owns
S1+S2 (≈138,445 tokens); a fresh builder takes S3 (≈94,214 tokens) only after S1+S2 proofs are
green and committed. The coordinator owns the handoff and final independent verification.
