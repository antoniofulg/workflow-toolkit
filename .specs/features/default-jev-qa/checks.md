# Default Jev browser QA checks

Profile: standard
Plan: `.specs/features/default-jev-qa/plan.md`

7 checks in 2 slices · 2 one-way doors · 0 open, of which 0 block

## Checks

### S1 - Select the configured browser QA adapter · 8 files · 178 KB · ~45k

**C1** - With `[qa].browser_adapter` absent, the Python config reader resolves `auto`; each of `auto`, `jev`, `playwright-mcp`, `orca`, `maestri`, and `manual` resolves unchanged; `jev-ultrafast`, another unknown value, and an unknown `[qa]` key are rejected with the six valid values and no credential access or output (JDF-01, AC 1-3; SEC-001, SEC-002)
Proof: `python3 -m unittest tools.test_workflow_config.WtkWorkflowConfigContractTests -k test_qa_browser_adapter_contract`

**C2** - The installer-side config reader applies the same absent default, six-value enum, unknown-key rejection, and no `jev-ultrafast` alias as the Python reader (JDF-01, AC 1-3; SEC-001, SEC-002)
Proof: `bun test tools/shared/tests/workflow-config.test.ts -t "accepts the QA browser adapter contract"`

**C3** - Agent synchronization and adoption preserve an existing local `.wtk.toml` with no `[qa]` table byte-for-byte while the effective browser adapter is `auto`; the tracked example documents `[qa] browser_adapter = "auto"` and all six valid values (JDF-02, AC 6)
Proof: `python3 -m unittest tools.test_workflow_config.WtkWorkflowConfigContractTests -k test_qa_default_preserves_existing_local_config`
Proof: `bun test tools/shared/tests/workflow-config.test.ts -t "documents and preserves the default QA browser adapter"`

**C4** - `wtk-qa-execute` resolves `auto` as Jev -> LLM + Playwright MCP -> exactly one host-declared `orca` or `maestri` adapter -> manual, while each non-auto value selects only that logical adapter and `jev` maps internally to Jev Ultrafast (JDF-02, JDF-03, AC 4, 5, 7, 8; SEC-002, SEC-004)
Proof: `bun test tools/shared/tests/qa-skills.test.ts -t "IT-027 routes the configured QA browser adapter"`

### S2 - Continue the automatic chain safely after Jev cannot complete · 3 files · 47 KB · ~12k

**C5** - A typed Jev timeout with no recorded product action returns `failed`, fixed `pre-action-timeout` classification, `fallback_safe: true`, and Playwright MCP as the next automatic adapter without exposing raw exception text or credential sentinels (JDF-03, AC 9, 12; SEC-003, SEC-004)
Proof: `python3 tools/test_jev_qa_adapter.py -k test_pre_action_timeout_allows_playwright_fallback`

**C6** - A timeout after a product action and a timeout with ambiguous action state both return `failed`, `fallback_safe: false`, and no selected automatic fallback; the wrapper calls `Agent.run()` once and the instructions require independent inspection or fixture reset before another driver acts (JDF-04, AC 10; SEC-005)
Proof: `python3 tools/test_jev_qa_adapter.py -k test_unsafe_timeout_forbids_automatic_fallback`
Proof: `bun test tools/shared/tests/qa-skills.test.ts -t "IT-028 forbids unsafe Jev replay"`

**C7** - Across completed, unavailable, safe-timeout, unsafe-timeout, generic-failed, and invalid results, only completed plus matching independent readback may pass; stdout, stderr, evidence, result fields, and report-facing instructions exclude credentials, cookies, authorization values, reusable tokens, and raw exception text (JDF-04, AC 11, 12; SEC-003, SEC-006)
Proof: `python3 tools/test_jev_qa_adapter.py -k test_fallback_terminal_and_redaction_matrix`
Proof: `bun test tools/shared/tests/qa-skills.test.ts -t "IT-023 keeps Jev as a driver and the oracle independent"`

## Coverage

| Set (size) | Member -> proof | Unproven |
| --- | --- | --- |
| public `browser_adapter` values (6) | `auto` C1/C2/C4 · `jev` C1/C2/C4 · `playwright-mcp` C1/C2/C4 · `orca` C1/C2/C4 · `maestri` C1/C2/C4 · `manual` C1/C2/C4 | - |
| config readers (2) | Python C1 · installer/Node C2 | - |
| config presence (2) | absent -> `auto` C1/C2/C3 · explicit value preserved C1/C2 | - |
| invalid QA config (3) | `jev-ultrafast` C1/C2 · unknown value C1/C2 · unknown key C1/C2 | - |
| automatic chain stages (4) | Jev C4 · Playwright MCP C4/C5 · one declared IDE-native adapter C4 · manual C4 | - |
| IDE-native alternatives (2) | host declares Orca C4 · host declares Maestri C4 | - |
| timeout action state (3) | proven pre-action C5 · post-action C6 · ambiguous C6 | - |
| adapter result classes (6) | completed C7 · unavailable C4/C7 · safe-timeout C5/C7 · unsafe-timeout C6/C7 · generic-failed C7 · invalid C7 | - |
| fallback eligibility (2) | safe C5 · forbidden C6 | - |
| secret-bearing sinks (5) | stdout C5/C7 · stderr C5/C7 · evidence C5/C7 · result C5/C7 · report-facing instructions C7 | - |
| sensitive field classes (5) | provider credential C5/C7 · cookie C7 · authorization C7 · reusable token C7 · raw exception text C5/C7 | - |
| oracle outcomes (2) | completed + mismatch is not pass C7 · completed + matching reload may pass C7 | - |
| public configuration door (1) | `[qa] browser_adapter = "auto"` with six values C1-C4 | - |
| replay boundary door (1) | automatic fallback only unavailable/proven pre-action timeout C4-C6 | - |
| SEC requirements (6) | SEC-001 C1/C2 · SEC-002 C1-C4 · SEC-003 C5/C7 · SEC-004 C4/C5 · SEC-005 C6 · SEC-006 C7 | - |

- Claims naming config values or rejection behavior: C1-C3 cross the owning config-reader boundaries.
- Claims naming adapter routing or verdict behavior: C4, C6, C7 assert the agent-facing instruction boundary; C5-C7 assert the executable adapter result boundary.
- No other check claims more than the cases enumerated beside its proof.

## Test policy

| Code | Required proofs | Coverage expectation |
| --- | --- | --- |
| Config parser/default decision, duplicated across Python and installer readers | one focused proof at each public reader | absent table, every accepted value, implementation alias, unknown value, and unknown key asserted independently in both readers |
| Agent-facing adapter routing policy | instruction contract proof plus executable helper proof for result metadata | every configured value and automatic stage named; safe and unsafe continuation differentiated |
| Adapter failure classification reached through a process/result boundary | focused executable proof at its own layer | pre-action, post-action, ambiguous, generic failure, unavailable, completed, and invalid outcomes independently asserted |
| Pass-through documentation and fixed metadata | existing semantic contract suite | public names, default, fallback order, no-replay, and oracle authority asserted without freezing incidental prose |

Evidence:

- `.agents/skills/wtk-config/scripts/workflow_config.py`: validates top-level/table keys and decides defaults -> decision code.
- `scripts/installer/packets.js`: independently validates installer-read configuration -> decision code at a separate public reader.
- `.agents/skills/wtk-qa-execute/jev_adapter.py`: decides preflight, terminal status, failure classification, evidence and fallback eligibility across multiple branches -> decision code.
- `.agents/skills/wtk-qa-execute/SKILL.md`: agent-consumed routing contract; canonical semantic assertions live in `tools/shared/tests/qa-skills.test.ts`.
- Closest repository analogue: existing remediation and parallelization config matrices prove each accepted/rejected value in `tools/test_workflow_config.py` and `tools/shared/tests/workflow-config.test.ts`.

Cost: seven focused proofs across the existing Python adapter/config and Bun instruction/installer suites. Without both config-reader proofs, one accepted consumer config can fail only during installation; without executable timeout cases, prose can authorize replay without a discriminating result.

## Swept

- validation: C1, C2
- failure modes: C4-C7
- idempotency: C6 - possible or uncertain product action forbids automatic replay; a reset creates a new known fixture attempt
- authorization: existing - declared charter, non-consequential scope, dedicated browser, and Verifier delegation remain required before Jev construction
- concurrency: n/a - one Verifier walks one fixture journey; this change adds no concurrent adapter execution
- data lifecycle: C3, C7 - local config remains consumer-owned; evidence remains checkout-owned and secret-free
- dependency failure: C4, C5 - unavailable Jev proceeds through the automatic chain; explicit values do not silently substitute another adapter
- state transitions: C4-C7 - configured selection -> attempt -> safe fallback, stop/reset, or oracle verdict is fully enumerated
- observability: C5-C7 - result records actual adapter, bounded failure class, fallback eligibility, evidence, and limitation without raw errors or secrets

## Handoff

- S1 reads approximately 178 KB / 4 = 45k tokens across config readers, examples, docs, and their canonical tests; S2 adds approximately 47 KB / 4 = 12k across the adapter, skill, and focused tests; cumulative ~57k is under the 150k budget - one builder owns both slices sequentially.
- **Boundary:** C1-C4 closed at `7ef7175b101c2eb745edf6089038d2be8d66cfd9`.
- **Settled mid-build:** No additional S1 decisions.
- **Abandoned:** No S1 implementation attempts.
- **Boundary:** C5-C7 proved green in the S2 commit; its hash is returned in the implementer handoff.
- **Settled mid-build:** Only a typed timeout during Jev construction proves pre-action; no timeout text is parsed.
- **Abandoned:** Automatic fallback after `Agent.run()` begins, because action state can be uncertain.
