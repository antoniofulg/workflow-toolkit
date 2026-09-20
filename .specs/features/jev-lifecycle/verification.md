# Jev lifecycle verification

**Verdict**: PASS
**Profile**: standard
**Diff range**: `012f1295fe25ad8c152c631a8f4918a260310ec8..2f9c575b97c5b98d9b8cc3b3ff8d66a9115239fd`
**Round**: 1 - full
**Verifier**: `/root/verify_jev` (independent technical verifier; author was `/root/build_jev`)

## Contract inspection

The complete assigned range was compared with `plan.md`, `checks.md`, `dx.md`, and
`threat-model.md`. The implementation keeps the approved local CLI, fixed provider boundary,
advisory-only authority, core-package placement, and direct phase routing. No visual acceptance
criterion exists.

The user-amended default is present in the shared instruction at
`.agents/skills/wtk/references/jev-adviser.md:5`: every semantic path decision consults Jev when
the key is available, even when the agent has a preferred answer. Lines 18, 26, 38, 45, and 47
respectively require normal phase invocation, quiet use of the existing trusted caller credential,
fallback without repeated attempts, retained host authority, and stale-advice discard. Lines 54–59
provide one concrete example for each supported phase. All 14 direct entrypoints resolve this one
shared reference; the automated proof checks those resolved paths rather than incidental prose.

## Checks

| Check | Claim | Proof run | Evidence | Result |
| --- | --- | --- | --- | --- |
| C1 | Six-phase preview creates Choice plus independent Noul and makes no provider call | Batched `node --test` run, JEV-001, exit 0 | `tests/installer/jev-adviser.test.js:75` loops every phase; `:85` asserts supplied options plus `insufficient_evidence`; `:86` and `:87` assert Choice/Noul; `:88` asserts no capture | PASS |
| C2 | Send mode returns typed advice, model, usage, hash, and hash changes with normalized input | Batched run, JEV-002, exit 0 | `tests/installer/jev-adviser.test.js:101` asserts exact output keys; `:103`–`:109` assert status/model/Choice/Noul/usage; `:113` and `:116` discriminate changed and normalized input | PASS |
| C3 | Malformed, unknown, or over-bound input exits 2 before provider access while exact limits pass | Batched run, JEV-003, exit 0 | `tests/installer/jev-adviser.test.js:126`–`:132` assert documented maxima and exact 32-KiB acceptance; `:154`–`:159` assert every invalid input exits 2 with no capture; `:160`–`:164` assert phase/flag rejection | PASS |
| C4 | Missing key and bounded provider failures exit 3, return no advice, and make at most one request | Batched run, JEV-004, exit 0 | `tests/installer/jev-adviser.test.js:169`–`:177` assert missing-key and exact 64-KiB boundaries; `:187`–`:198` assert all five reasons, one request, redirect refusal, and 20-second deadline; `:207`–`:213` assert every response-validation class | PASS |
| C5 | Fixed recipient, header-only credential, no redirect, leak, execution, implicit context, or artifact mutation | Batched run, JEV-005, exit 0 | `tests/installer/jev-adviser.test.js:229`–`:241` assert advice-only output, zero extra files, fixed URL/method/manual redirect, exact headers, bounded state, and no key; `:249`–`:276` reject reflected credentials before output or provider access | PASS |
| C6 | Direct lifecycle entrypoints share Jev-first semantic guidance for all phases | Batched run, JEV-006, exit 0, plus semantic inspection | `tests/installer/jev-adviser.test.js:282`–`:305` enumerate and resolve all 14 entrypoints; `:306` asserts all six examples; `.agents/skills/wtk/references/jev-adviser.md:5`, `:12`, `:18`, `:26`, `:38`, `:45`, and `:47` settle the amended always-consult, bounded-input, credential, fallback, authority, and stale-result policy | PASS |
| C7 | Core-only consumer stages the helper/reference and executes preview without QA or quality | Batched run, JEV-007, exit 0 | `tests/installer/jev-adviser.test.js:312`–`:317` assert core-only staging and absence of QA/quality; `:324`–`:332` execute the staged helper and assert preview/exit 0 | PASS |
| C8 | Published package contains helper and shared reference | Batched run, JEV-008, exit 0 | `tests/installer/package.test.js:14` asserts both paths in `npm pack --dry-run --json` inventory | PASS |

## Coverage

| Set (size) | Recomputed from | Member -> proof | Unproven |
| --- | --- | --- | --- |
| Phases (6) | `dx.md:9`; `.agents/skills/wtk/scripts/advise.mjs:9` | plan C1 C6; build C1 C6; verify C1 C6; review C1 C6; qa C1 C6; ship C1 C6 | - |
| CLI flags/modes (3) | `dx.md:7`–`:11`; `advise.mjs:17`–`:23` | `--phase` C1 C3; `--send` C2 C4 C5; `--help` C1 | - |
| Command statuses (4) | `dx.md:37`–`:42`; `advise.mjs:14`, `:15`, `:145`, `:182` | preview C1; advice C2; invalid C3; unavailable C4 | - |
| Exit codes (3) | `dx.md:37`–`:42`; `advise.mjs:145`, `:160`, `:167`, `:188`, `:196` | 0 C1 C2; 2 C3 C5; 3 C4 C5 | - |
| Unavailable reasons (5) | `dx.md:42`; `advise.mjs:136`–`:148`, `:187` | missing_key C4; timeout C4; http_error C4; invalid_response C4 C5; network_error C4 | - |
| Input schema (4) | `dx.md:7`, `:13`–`:30`; `advise.mjs:42`–`:50` | phase C1 C3; decision C3; evidence C3; options C1 C3 | - |
| Input/response boundaries (8) | `dx.md:13`, `:26`–`:30`, `:48`; `advise.mjs:6`–`:8`, `:31`, `:44`–`:49`, `:90` | input bytes C3; decision length C3; evidence count C3; evidence length C3; option count C3; option identifiers C3; option descriptions C3; response bytes C4 | - |
| Response validation (5) | `dx.md:44`–`:48`; `advise.mjs:101`–`:121` | selected option C4; probability keys/range/sum C4; confidence C4; Noul C4; model and usage C2 C4 | - |
| Transport controls (5) | `dx.md:48`, `:55`–`:58`; `advise.mjs:124`–`:149` | one fixed endpoint C5; authorization-only key C5; redirects refused C4 C5; 20-second deadline C4; one request/no retry C4 | - |
| Direct entrypoint links (14) | `tests/installer/jev-adviser.test.js:282`–`:297` and each listed file | router, discover, modular plan, Lean, Lean plan/checks/build/verify, implement, deep review, QA router/plan/execute, ship -> C6 | - |
| Guidance examples (6) | `.agents/skills/wtk/references/jev-adviser.md:50`–`:59` | plan C6; build C6; verify C6; review C6; qa C6; ship C6 | - |
| One-way doors (2) | `plan.md:53`–`:57` | advisory CLI contract C1 C2 C3 C5; external inference C4 C5 | - |
| Distribution assemblies (2) | `scripts/installer/engine.js:22`–`:24`; `package.json:15`–`:45` | core consumer C7; npm package C8 | - |
| Security requirements (4) | `threat-model.md:51`–`:56` | SEC-001 C5 C6; SEC-002 C5; SEC-003 C3 C4; SEC-004 C2 C6 | - |

No additional enumeration in the approved Surface, Landing, Relations, criteria, or claim prose was
left without a proof. Relations is explicitly empty. Output fields, provider-failure reasons, and
security surfaces resolve through the rows above.

## Test policy

| Row | Files it classifies | Required proof | Expectation met |
| --- | --- | --- | --- |
| Adviser validation and result decisions | `.agents/skills/wtk/scripts/advise.mjs`, `tests/installer/jev-fetch-mock.mjs` | CLI boundary plus controlled transport; every documented input bound, response class, and status | yes — JEV-001 through JEV-005 exercise the public process boundary and fake provider; exact maxima and each named failure class are asserted |
| Instruction routing | 14 entrypoints plus `.agents/skills/wtk/references/jev-adviser.md` | Resolvable routing plus independent semantic inspection across all phases | yes — JEV-006 resolves each link; direct inspection confirms the always-when-available default and authority/disclosure/fallback/staleness rules |
| Package distribution | `scripts/installer/engine.js`, `package.json` | Core consumer execution plus package inventory | yes — JEV-007 executes staged core content; JEV-008 inspects packed inventory |

JEV-006 does not claim that a future host agent obeys prose. That nondeterministic public behavior
remains for the separately authorized QA session; it is not substituted with static-string or live
connectivity evidence here.

## Swept existing

| Dimension | Re-read result |
| --- | --- |
| Validation and failure modes | `advise.mjs:26`–`:50` and `:124`–`:149` enforce the approved local and provider outcomes; C3/C4 cover them |
| Idempotency and concurrency | One process holds only local request state and performs at most one fetch; no shared mutable adviser state or retry/cache path exists (`advise.mjs:53`–`:74`, `:124`–`:149`) |
| Authorization | Output is projected data only (`advise.mjs:113`–`:121`); shared guidance retains all action, permission, approval, and gate authority (`jev-adviser.md:43`–`:48`) |
| Data lifecycle | Helper reads stdin and `TYPESAFE_API_KEY`, writes stdout, and contains no persistence or discovery path (`advise.mjs:26`–`:40`, `:152`–`:199`) |
| Dependency failure | Missing key, timeout, HTTP, malformed/oversize response, and network failure map to bounded unavailable results (`advise.mjs:124`–`:149`, `:185`–`:196`) |
| State transitions | Preview, advice, invalid, and unavailable are terminal process outputs, not workflow mutations (`advise.mjs:14`–`:15`, `:145`, `:159`, `:166`, `:182`, `:187`, `:195`) |
| Observability | Advice exposes hash/model/typed answers/usage while provider errors and raw bodies stay private (`advise.mjs:101`–`:121`, `:134`–`:149`) |

## Construction constraints

- Shared behavior is not duplicated: all 14 consumers resolve the single
  `.agents/skills/wtk/references/jev-adviser.md` policy, proven by JEV-006.
- Core distribution reaches the actual shared helper/reference through
  `scripts/installer/engine.js:22`–`:24` and staging at `:230`–`:236`, proven by JEV-007.
- Real-tree porcelain before and after fault injection was identical:
  ` M skills-lock.json`, `?? .agents/skills/typesafe-ai/`, and
  `?? .claude/skills/typesafe-ai`. These user-owned changes were not read, changed, staged, or
  copied into the scratch worktree.
- The trusted central credential file was not opened or printed. Offline proofs used the controlled
  mock transport; no provider call was made by this verification.

## Faults injected

All mutations ran in a detached temporary worktree at the assigned HEAD. The scratch tree was clean
after reversals, was removed, and the real-tree porcelain matched its baseline.

| Mutation | Location | Narrow proof | Killed |
| --- | --- | --- | --- |
| Choice question type `choice` -> `choice_fault` | `.agents/skills/wtk/scripts/advise.mjs:58` | JEV-001, exit 1, 0.088 s; assertion at `tests/installer/jev-adviser.test.js:86` | yes |
| Input byte limit `32 KiB` -> `32 KiB + 1` | `.agents/skills/wtk/scripts/advise.mjs:6` | JEV-003, exit 1, 0.583 s; oversize assertion at `tests/installer/jev-adviser.test.js:156` | yes |
| Fixed endpoint -> `https://example.invalid/systemone` | `.agents/skills/wtk/scripts/advise.mjs:4` | JEV-005, exit 1, 0.090 s; endpoint assertion at `tests/installer/jev-adviser.test.js:234` | yes |
| Ship entrypoint link -> missing shared reference | `.agents/skills/wtk-ship/SKILL.md:12` | JEV-006, exit 1, 0.050 s; entrypoint assertion at `tests/installer/jev-adviser.test.js:303` | yes |
| Installer catalog omits adviser helper/reference | `scripts/installer/engine.js:110` | JEV-007, exit 1, 0.078 s; staging assertion at `tests/installer/jev-adviser.test.js:314` | yes |

The five-fault profile cap was reached across distinct assertion surfaces. No mutant survived.

## Assigned evidence

The coordinator's one authorized synthetic live smoke exited 0 in 0.813 s and returned model
`jev-1.13.0`, 506 input tokens, 75 output tokens, and valid typed advice. It establishes provider
connectivity only. It does not prove host-agent compliance, token savings, decision quality, or any
gate verdict, and it was not repeated under the checkout's offline verification policy.

## Gate

`node --test --test-name-pattern='JEV-00[1-8]' tests/installer/jev-adviser.test.js tests/installer/package.test.js`
— exit 0 in 2.757 s; 8 passed, 0 failed, 0 skipped. Each JEV-001 through JEV-008 appeared
individually and passed.

