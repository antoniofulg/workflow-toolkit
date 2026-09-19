# Optional Jev QA Adapter checks

Profile: standard
Plan: `.specs/features/optional-jev-qa-adapter/plan.md`

8 checks in 1 slice · 1 one-way door · 0 open, of which 0 block

## Checks

### S1 - Execute browser QA through optional Jev with safe fallback · 4 files · <40 KB · <12k

**C1** - With both provider keys, a non-consequential fixture charter, an explicit dedicated CDP endpoint, Jev Ultrafast, and Browser Harness present, one URL/goal run returns adapter `jev-ultrafast`, status `completed`, allowlisted evidence paths, and an empty limitation; headless is the default, an explicit headed request uses the same dedicated endpoint, and the child text helper receives the Gateway key without credential output (JQA-01, AC 1, 5; SEC-001, SEC-002)
Proof: `python3 tools/test_jev_qa_adapter.py -k test_ready_run_emits_secret_free_contract`

**C2** - Removing each prerequisite independently—TypeSafe key, Gateway key, non-consequential declaration, dedicated CDP endpoint, Jev Ultrafast module, or Browser Harness—returns status `unavailable`, names only the unmet prerequisite/policy, and selects fallback order Playwright MCP then declared Orca, Maestri, or manual adapter (JQA-02, AC 2; SEC-002, SEC-004, SEC-006)
Proof: `python3 tools/test_jev_qa_adapter.py -k test_missing_prerequisite_matrix_falls_back`

**C3** - A Jev `DONE` result never emits or records QA `pass`; the existing session protocol still requires independent readback after reload, and only the matching oracle control can produce a passing scenario (JQA-03, AC 3, 7; SEC-005)
Proof: `python3 tools/test_jev_qa_adapter.py -k test_done_requires_independent_oracle`
Proof: `bun test tools/shared/tests/qa-skills.test.ts -t "IT-023 keeps Jev as a driver and the oracle independent"`

**C4** - A provider or browser failure after `Agent.run()` begins returns status `failed`, preserves bounded allowlisted evidence, and the adapter calls `Agent.run()` exactly once without restart or retry (JQA-04, AC 4; SEC-007)
Proof: `python3 tools/test_jev_qa_adapter.py -k test_failure_calls_agent_run_once`

**C5** - A contained evidence destination may receive the bounded trace, while a lexical escape, canonical escape, or symlink traversal returns status `invalid` before creating or changing any destination file (JQA-05, AC 6; SEC-003)
Proof: `python3 tools/test_jev_qa_adapter.py -k test_evidence_destination_matrix_is_contained`

**C6** - A consequential charter, personal/default browser request, or missing dedicated endpoint returns `unavailable` before constructing `Agent` and selects Playwright MCP first; a non-consequential fixture with a dedicated endpoint constructs one agent (JQA-06, AC 8; SEC-002, SEC-006)
Proof: `python3 tools/test_jev_qa_adapter.py -k test_unsafe_jev_scope_falls_back_before_agent`

**C7** - The quality module packages the optional helper without a runtime dependency or installer action, and `wtk-qa-execute` documents Jev headless-default/explicit-headed dedicated CDP, Playwright MCP first fallback, then Orca/Maestri/manual, actual-adapter reporting, and external-oracle ownership (JQA-01, JQA-02, AC 1, 2, 7; Landing 1)
Proof: `bun test tools/shared/tests/qa-skills.test.ts -t "IT-024 packages the optional Jev QA adapter without owning installation"`
Proof: `bun test ./tests/installer/package.test.js -t "IT-026 package includes the optional Jev QA adapter helper"`

**C8** - Every terminal adapter outcome—`completed`, `unavailable`, `failed`, and `invalid`—crosses the subprocess boundary as exactly one parseable result carrying `adapter`, `status`, `evidence`, and `limitation`; allowlisted evidence excludes authorization, cookie, token, and credential fields, and sentinels are absent from stdout, stderr, evidence, exception text, and the report-facing result (JQA-01, JQA-02, JQA-04, JQA-05, JQA-06; AC 1, 2, 4, 6, 8; SEC-001, SEC-004, SEC-005)
Proof: `python3 tools/test_jev_qa_adapter.py -k test_terminal_status_and_redaction_matrix`

## Coverage

| Set (size) | Member -> proof | Unproven |
| --- | --- | --- |
| adapter selection outcomes (4) | Jev ready C1 · Playwright MCP first fallback C2/C6/C7 · Orca/Maestri fallback C2/C7 · manual fallback C2/C7 | - |
| required prerequisites/policies (6) | `TYPESAFE_API_KEY` C2 · `AI_GATEWAY_API_KEY` C2 · non-consequential charter C2/C6 · dedicated CDP endpoint C2/C6 · `jev_ultrafast` module C2 · Browser Harness executable C2 | - |
| terminal statuses (4) | `completed` C1/C8 · `unavailable` C2/C6/C8 · `failed` C4/C8 · `invalid` C5/C8 | - |
| evidence destinations (4) | contained C5 · lexical escape C5 · canonical escape C5 · symlink traversal C5 | - |
| secret-bearing sinks (5) | stdout C1/C8 · stderr C8 · allowlisted evidence C1/C4/C8 · exception text C8 · report-facing result C8 | - |
| sensitive field classes (4) | authorization C8 · cookie C8 · token C8 · credential C8 | - |
| browser isolation modes (3) | dedicated headless CDP default C1/C7 · explicit dedicated headed CDP C1/C7 · ordinary personal/default browser rejected C2/C6 | - |
| Jev scope outcomes (2) | consequential journey falls back before Agent C6 · non-consequential fixture constructs Agent C6 | - |
| post-start failure outcomes (2) | failure evidence retained C4 · `Agent.run()` called once C4 | - |
| oracle outcomes (2) | `DONE` plus mismatch remains non-pass C3 · `DONE` plus matching independent readback may pass C3 | - |
| packaged integration door (1) | optional helper reuses consumer-installed adapter and owns no installation C7 | - |
| SEC requirements (7) | SEC-001 C1/C8 · SEC-002 C2/C7 · SEC-003 C5 · SEC-004 C2/C8 · SEC-005 C3/C8 · SEC-006 C6 · SEC-007 C4 | - |

- Claims naming adapter statuses or result fields: C1-C8; each Python proof crosses the helper's process/result boundary, while C3 and C7 also assert the owning skill contract.
- No other check claims more than the cases enumerated beside its proof.

## Test policy

| Code | Required proofs | Coverage expectation |
| --- | --- | --- |
| Python adapter decision code, reached across a process boundary | one subprocess/public-result proof and focused tests at its own layer | every prerequisite/policy, terminal status, evidence-path class, browser mode, fallback, scope outcome, redacted field class, and post-start failure outcome independently asserted |
| QA instruction/packaging integration | existing contract tests at the package and skill boundary | Jev remains optional, no installer/runtime dependency is added, and independent-oracle plus existing-adapter rules stay explicit |
| Upstream Jev Ultrafast and Browser Harness instrumentation | none of its own in this repository | mocked at the adapter boundary; a consuming web project owns any later live journey evidence |

Evidence:

- planned `jev_adapter.py`: dispatches over 6 prerequisites/policies, 4 terminal statuses, 4 evidence-path classes, 3 browser modes, 4 adapter outcomes, 4 sensitive-field classes, 2 scope outcomes, and 2 post-start failure outcomes -> decides.
- `.agents/skills/wtk-qa-execute/SKILL.md`: instruction boundary consumed by Verifier agents; canonical conformance lives in `tools/shared/tests/qa-skills.test.ts`.
- closest analogue: `.agents/skills/wtk-config/scripts/repository_intelligence.py` plus `tools/test_repository_intelligence.py`, where an optional external integration is isolated behind bounded Python results, explicit degraded fallback, path/state checks, and offline collaborators.

Cost: 8 focused proofs across one Python adapter test module and the existing QA/package contract suites. Without these rows, missing prerequisites, provider failure, and unsafe evidence paths would be proven only by a happy path that happened to traverse them.

## Swept

- validation: C2, C5, C6
- failure modes: C2, C4, C8
- idempotency: C4 - the wrapper calls `Agent.run()` once and never restarts it after failure; upstream internal behavior remains outside this claim
- authorization: C2, C6 - consequential work and personal/default browsers are rejected before agent construction; existing consuming-project identity policy remains authoritative
- concurrency: existing - `.agents/skills/wtk/references/validation.md` permits at most one queued browser execution per checkout
- data lifecycle: C5, C7 - raw evidence stays in the existing checkout-owned disposable root and durable QA schemas do not change
- dependency failure: C2, C4
- state transitions: C1-C6, C8 - every adapter terminal status is enumerated
- observability: C1, C4, C7, C8 - actual adapter, execution path, evidence, fallback/limitation, and oracle result remain reportable without secrets

## Handoff

Default: one builder owns the complete S1 slice; no planned transfer.

## Build state

Round 2 remediation is complete in the local build. The revised focused Python proofs, QA skill
contract proof, exact IT-026 helper-package proof, full installer suite, both Lean validators, and
diff check are green. The adapter now requires exact dedicated browser declarations, proves the
Playwright-first selector with Orca/Maestri/manual outcomes, rejects arbitrary trace fields, and
emits valid JSON for malformed CLI input and oversized evidence. A fresh non-author Verifier remains
responsible for the complete feature range and independent oracle evidence.
