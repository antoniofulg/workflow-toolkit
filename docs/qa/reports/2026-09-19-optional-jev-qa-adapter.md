# Optional Jev QA Adapter QA — 2026-09-19

- **Snapshot:** `680076a0b999b88ad6fb6ec091202d4a6fc079d5`
- **Branch:** `feat/optional-jev-qa-adapter`
- **Charter:** [`CH-use-optional-jev-qa-adapter-2026-09-19`](../charters/CH-use-optional-jev-qa-adapter-2026-09-19.md)
- **Journey:** [`J-use-optional-jev-qa-adapter`](../journeys/J-use-optional-jev-qa-adapter.md)
- **Persona:** Workflow operator
- **Adapter:** CLI/manual through an exact local package plus independent filesystem readback
- **Execution path:** local package → extracted runner → packed `wtk install` selecting `quality` → installed `jev_adapter.py`
- **Environment:** Darwin 27.0.0 arm64; Bun 1.4.2; Node v22.23.1; Python 3.14.7; Git 2.54.0; Expect 5.45
- **Technical gate:** Round 3 Technical Verification PASS at `680076a0`: 8/8 checks, 5/5 faults killed, 0 open confirmed security findings
- **Raw evidence:** `docs/qa/evidence/2026-09-19-optional-jev-qa-adapter/`
- **Live limitations:** no browser application, Jev runtime, Browser Harness, Playwright MCP, provider call, or real key is in scope

## Scenario matrix

| Scenario | Entry point | Expected | Verdict | Evidence |
| --- | --- | --- | --- | --- |
| `QAS-use-optional-jev-qa-adapter` | exact local package and installed `wtk-qa-execute` helper | Packaged dependency-free helper exposes readable safety policy and fails closed with structured fallback metadata | **pass** | `package-summary.json`; `installer-transcript.txt`; `installed-readback.json`; `preflight-results.json`; `selected-gates.txt` |

## Session log

| Probe | Expected | Observed | Result |
| --- | --- | --- | --- |
| Frozen snapshot | Product HEAD is `680076a0`; only verifier-owned artifacts differ | HEAD stayed `680076a0`; opening status contained only the assigned verification/workflow and new QA records | pass |
| Exact local archive | `workflow-toolkit@1.0.5` contains the skill and helper with no browser/provider dependency | SHA-256 `6bb9506a8e61604031e99dc242c61c6b149e64cbe19037c78deed466355d8708`; 146 files; both required members present; only runtime dependency is `smol-toml` | pass |
| Public guided install | Packed `wtk install` accepts `quality`, includes `core`, and installs the reviewed helper | PTY selection `2` previewed and installed `core, quality`; 160 additions; helper and skill present | pass |
| No dependency installation | Consumer package/lock stay unchanged; no runtime dependency tree appears | `package.json` and `bun.lock` hashes stayed `2d7ff49...` and `efc38019...`; `node_modules` absent; external security skills absent | pass |
| Installed policy readback | Optional non-consequential scope, dedicated headless/default and explicit-headed CDP, personal/default rejection, Playwright-first fallback, and external oracle are readable | Every policy marker was present in the independently loaded installed `SKILL.md` | pass |
| Missing prerequisite | No-key invocation returns one structured `unavailable` result without evidence or provider/browser work | Exit `2`; one JSON stdout line; empty stderr; `missing prerequisite: TYPESAFE_API_KEY`; `evidence: []`; Playwright-first order | pass |
| Consequential policy | Consequential scope rejects before prerequisite discovery | Exit `2`; one JSON stdout line; empty stderr; policy limitation; `execution_path: preflight`; no evidence | pass |
| Invalid evidence destination | Escaping destination returns `invalid` without changing the outside sentinel | Exit `2`; one JSON stdout line; empty stderr; outside-root limitation; sentinel hash stayed `85edfde7...` | pass |
| Post-probe reload | Installed bytes still equal packed bytes and keep the oracle/fallback policy | Fresh process matched skill hash `9cbf1827...` and helper hash `84748996...`; no evidence root or dependency tree appeared | pass |

One observer setup command initially used source-relative hash paths while its working directory was
the disposable consumer. It stopped before consumer initialization. The corrected absolute-path
readback passed; no product or consumer state was changed by the failed setup command.

## Independent readback

The package, install, and post-probe reads used separate processes. Packed and installed hashes
matched exactly:

- `.agents/skills/wtk-qa-execute/SKILL.md` — `9cbf1827e23a929c0ba72004e523a92a1d0bcbb590afd125e001a2ef6193b490`
- `.agents/skills/wtk-qa-execute/jev_adapter.py` — `84748996d1f7efd8223be104dae1bf42af413abc0b7bb7902a767dab31cebce3`

Actual public adapter was the packed CLI/manual installer plus filesystem readback. The installed
Jev wrapper was invoked only through its `preflight` execution path. No browser adapter ran; the
reported fallback was `playwright-mcp`, but fallback execution was intentionally not attempted.

## Findings

No product defect observed. No bug record created.

## Cleanup and residue

The exact recorded runtime root containing package, runner, consumer, and outside sentinel was moved
to Trash after the walk; the move is recoverable and every original disposable path is absent.
Source HEAD remains `680076a0`. Final porcelain differs from the opening snapshot only by this
durable report; scenario, journey, charter, verification, and workflow artifacts remain the same
assigned untracked records.

## Final selected gate

- `bun test tools/shared/tests/qa-skills.test.ts -t 'IT-024 packages the optional Jev QA adapter without owning installation'` — exit `0`; 1 pass, 35 filtered, 0 fail.
- `bun test ./tests/installer/package.test.js -t 'IT-026 package includes the optional Jev QA adapter helper'` — exit `0`; 1 pass, 7 filtered, 0 fail.
- Reused: Round 3 Technical Verification PASS at `680076a0`; product inputs stayed unchanged. No full gate was selected because the QA walk changed only durable QA records.

## Limitations

This source pack has no browser application, installed Jev Ultrafast, Browser Harness, Playwright
MCP, provider session, or independent browser outcome to walk. Ready execution, post-start failure,
live fallback, and successful browser-oracle paths remain unwalked and retain their separately
labeled Technical Verification evidence. No real key was read, passed, printed, or stored.

## Verdict

**PASS** — the packaged public surface and every chartered offline preflight/readback observable
matched. `QAS-use-optional-jev-qa-adapter` is `pass`; all in-scope rows are closed.
