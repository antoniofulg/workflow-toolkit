# Jev lifecycle checks

Profile: standard
Plan: `.specs/features/jev-lifecycle/plan.md`

8 checks in 2 slices · 2 one-way doors · 0 open, of which 0 block.

## Checks

### S1 - Advisory decisions across the lifecycle

**C1** - All six phases preview a Choice with 2–8 supplied options plus insufficient_evidence and an independent evidence Noul; previews and help make zero provider calls (JEV-01, AC 1, 2).
Proof: `node --test --test-name-pattern='JEV-001' tests/installer/jev-adviser.test.js`

**C2** - Valid send returns advice with the selected option, distribution, confidence, Noul, actual model, token usage and hash; changed normalized input changes the hash (JEV-01, SEC-004, AC 3, 10).
Proof: `node --test --test-name-pattern='JEV-002' tests/installer/jev-adviser.test.js`

**C3** - Malformed JSON, invalid schema or phase, unknown flags and input beyond 32 KiB return invalid/exit 2 before provider access; documented exact limits remain accepted (JEV-01, SEC-003, AC 4).
Proof: `node --test --test-name-pattern='JEV-003' tests/installer/jev-adviser.test.js`

**C4** - Missing key, HTTP/network error, invalid or over-64-KiB response and 20-second deadline return unavailable/exit 3 with no advice and no automatic retry (JEV-01, SEC-003, AC 5, 6).
Proof: `node --test --test-name-pattern='JEV-004' tests/installer/jev-adviser.test.js`

**C5** - The only credential recipient is the fixed HTTPS endpoint; redirects are refused, sentinel secrets and provider errors are absent from output, model-selected shell text causes no action or artifact mutation, and no implicit context is collected (JEV-01, SEC-001, SEC-002, AC 7, 8, 9).
Proof: `node --test --test-name-pattern='JEV-005' tests/installer/jev-adviser.test.js`

### S2 - Agents use the adviser at decision points

**C6** - Lifecycle entrypoints, including direct phase invocation, require Jev-first consultation for semantic decisions whenever available, resolve one shared adviser reference with examples for all six phases and policy for bounded non-sensitive input, batched questions, no authority expansion, unavailable advice and stale results; consultation is not limited to uncertain decisions (JEV-02, SEC-004, AC 11–13; explicit user steering during Build).
Proof: `node --test --test-name-pattern='JEV-006' tests/installer/jev-adviser.test.js`

**C7** - A temporary core-only consumer receives the helper and shared reference and can run a preview without keys, QA dependencies or the quality module (JEV-02, AC 14).
Proof: `node --test --test-name-pattern='JEV-007' tests/installer/jev-adviser.test.js`

**C8** - Published package inventory includes the adviser helper and shared reference (JEV-02, AC 14).
Proof: `node --test --test-name-pattern='JEV-008' tests/installer/package.test.js`

## Coverage

| Set (size) | Member -> proof | Unproven |
| --- | --- | --- |
| Phases (6) | plan C1 · build C1 · verify C1 · review C1 · qa C1 · ship C1 | - |
| Command statuses (4) | preview C1 · advice C2 · invalid C3 · unavailable C4 | - |
| Command exit codes (3) | 0 C1 C2 · 2 C3 · 3 C4 | - |
| Failure reasons (5) | missing_key C4 · timeout C4 · http_error C4 · invalid_response C4 · network_error C4 | - |
| Input schema (4) | phase C3 · decision C3 · evidence C3 · options C3 | - |
| Boundaries (8) | input bytes C3 · decision length C3 · evidence count C3 · evidence length C3 · option count C3 · option identifiers C3 · option descriptions C3 · response bytes C4 | - |
| Response validation (5) | selected option C4 · probabilities C4 · confidence C4 · Noul C4 · model and usage C4 | - |
| Doors (2) | advisory contract C1 C2 C5 · external inference C4 C5 | - |
| Distribution assemblies (2) | core consumer C7 · npm package C8 | - |
| Guidance phases (6) | plan C6 · build C6 · verify C6 · review C6 · qa C6 · ship C6 | - |
| Security requirements (4) | SEC-001 C5 · SEC-002 C5 · SEC-003 C3 C4 · SEC-004 C2 C6 | - |

Claims about CLI exits cross the command boundary; transport cases exercise a controlled provider
boundary without permitting a configurable external destination in the public command.
C6 automation proves links and contract routing; the independent Verifier additionally reads
semantic guidance. No string test claims to prove future agent compliance.

## Test policy

| Code | Required proofs | Coverage expectation |
| --- | --- | --- |
| Adviser validation and result decisions | CLI boundary plus controlled transport assertions | Every documented input bound, response validation class and status |
| Instruction routing | Link/metadata contract plus independent semantic inspection | Each phase route and shared authority/disclosure/uncertainty rule |
| Package distribution | Core consumer execution and package inventory | Both distribution assemblies |

Evidence: existing `tools/test_jev_qa_adapter.py` separates boundary validation, provider outcomes
and secret-safe outputs; `tests/installer/package.test.js` owns npm inventory. The new executable
has four public status outcomes; exact implementation branch counts are inspected at verification.
Cost: one Node test file plus one package test, no new framework. These rows apply to this feature
only; no repository-wide test-policy change is proposed.

## Swept

- validation: C3, C4
- failure modes: C4
- idempotency: C4, C5; read-only inference may be repeated explicitly, without automatic retries
- authorization: C5, C6; advice never substitutes for existing host/action authority
- concurrency: C2, C5; independent processes share no mutable adviser state
- data lifecycle: C5; no persistence or automatic context discovery
- dependency failure: C4
- state transitions: C1, C2, C3, C4; preview/advice/invalid/unavailable are result states, not workflow transitions
- observability: C2, C5; usage/model/hash plus bounded secret-free diagnostics

## Handoff

- User approved the plan on 2026-09-20, then explicitly requested implementation. Local edits,
  tests and commits authorized; no push, PR, merge or deployment requested.
- Measured existing phase-entrypoint, package-test, plan and checks files: 172894 bytes / 4 =
  43224 tokens. Budget up to 32000 bytes / 4 = 8000 tokens for the helper, controlled-fetch test
  support, shared guidance and QA journey/scenario; feature artifacts remain under 12000 tokens.
  Total below 64000 tokens, under 150000: one sequential builder.
- Branch: `feat/jev-lifecycle`. Preserve user-owned skills-lock.json, TypeSafe skill and Claude link.
- Credentials already exist in `~/.config/workflow-toolkit/qa.env`; caller may load them for one
  synthetic smoke test. Never print credentials or change the central file.
- Token-saving priority: consult before costly context expansion; do not duplicate completed
  reasoning or claim measured savings. Independent questions share one request.
- User steering during Build: Jev must be the default and always used when available. AC 11/C6
  now require semantic-decision consultation even when the agent already has a preferred answer;
  this is an explicit user amendment, not a builder relaxation. Existing trusted central credential
  is loaded by the caller; no new store or per-call approval. Deterministic work is not an AI judgment.
- S1 boundary: C1-C5 closed at `ab13ba3`; each exact `JEV-001` through `JEV-005` proof passed
  1/1, and the combined targeted run passed 5/5. `validate_checks.py jev-lifecycle` exited 0.
- Coordinator live smoke (synthetic input only): `node .agents/skills/wtk/scripts/advise.mjs --phase build --send`
  exited 0 in 0.813s; model `jev-1.13.0`, choice `inspect_concurrency`,
  Choice confidence 1, evidence-sufficiency Noul 0.95, usage 506 input / 75 output tokens. No
  repository content was sent. This is not evidence of token savings; no repeat is needed.
- S2 checkpoint: C6 and C7 passed their named `JEV-006` and `JEV-007` proofs, 1/1 each; C8 passed
  `JEV-008` in `tests/installer/package.test.js`, 1/1. Phase guidance routes through the shared
  reference; the independent Verifier still owns semantic conformance review. The added QA scenario
  remains `untested` until an independent host-agent walk.
- Slice-order deviation: `JEV-007` was added to the shared adviser test file in S1 before the S2
  reference existed, so that proof was pending in the isolated S1 tree. It passes in this completed
  S2 tree; committed history is preserved.
- Next: coordinator dispatches the fresh full-feature Verifier.
