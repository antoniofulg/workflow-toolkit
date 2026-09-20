# Default Jev Auto QA — 2026-09-19

- **Snapshot:** `f39fef06b7183a87889c346b90835af0699fa59c`
- **Branch:** `feat/default-jev-qa`
- **Charter:** [`CH-use-default-jev-auto-qa-2026-09-19`](../charters/CH-use-default-jev-auto-qa-2026-09-19.md)
- **Journey:** [`J-use-optional-jev-qa-adapter`](../journeys/J-use-optional-jev-qa-adapter.md)
- **Persona:** Workflow operator
- **Adapter:** CLI/manual through an exact local package, installed public config/helper CLIs, and independent filesystem readback
- **Execution path:** frozen local checkout -> local archive -> extracted runner -> packed `wtk install` selecting `quality` -> installed config/helper preflight -> separate-process reload
- **Environment:** Darwin 27.0.0 arm64; Bun 1.4.2; Node v22.23.1; Python 3.14.7; Git 2.54.0; Expect 5.45
- **Technical gate:** independent Technical Verification PASS at `f39fef06`: C1-C7, 5/5 mutants killed, 0 confirmed security findings
- **Raw evidence:** `docs/qa/evidence/2026-09-19-default-jev-auto-qa/`
- **Live limitations:** no consumer fixture application, Jev runtime, Browser Harness, Playwright MCP, Orca, Maestri, provider call, browser, or real credential is authorized

## Scenario matrix

| Scenario | Entry point | Expected | Verdict | Evidence |
| --- | --- | --- | --- | --- |
| `QAS-use-optional-jev-qa-adapter` | exact local package; packed `wtk install`; consumer `.wtk.toml`; installed config/helper paths | Default `auto`, closed six-value enum, safe unavailable preflight, no unsafe replay, and oracle-owned pass | **untested** — offline legs passed; live route unavailable | `package-summary.json`; `config-reader-matrix.json`; `installed-readback.json`; `preflight-results.json` |

## Session log

| Probe | Expected | Observed | Result |
| --- | --- | --- | --- |
| Frozen snapshot | Product HEAD is `f39fef06`; only verifier-owned QA/spec artifacts differ | Detached package source and active product HEAD both stayed `f39fef06`; product files did not change | pass |
| Exact local archive | Version 1.1.0 contains both readers, config example, QA skill, and helper with no browser/provider dependency or credential file | 146 members; SHA-256 `74ea29bb601665417daa90469be6a43545ec3e5508b4573d2a443e4ca5984d55`; required members present; sole dependency `smol-toml@1.8.0`; no credential file matched | pass |
| Packed public install | `quality` includes `core`; consumer package/lock/config bytes survive; no dependency or external security skill is installed | Public PTY installed `core, quality` with 159 adds; all three consumer hashes stayed exact; consumer `node_modules` and four external security skills remained absent | pass |
| Python config reader | Absent table/key and six values pass; alias, unknown value, and unknown key reject with the enum and no marker echo | Eight accepted cells exited 0; three invalid cells exited 2; every config hash stayed fixed; all invalid diagnostics listed six values and omitted the inert marker | pass |
| Installer config reader | Same matrix through packed `wtk install`, with no fixture mutation | Eight accepted cells reached the up-to-date public flow and exited 0; three invalid cells exited 1 before apply; all case repositories remained clean; enum shown and marker omitted | pass |
| Installed routing policy | Independent reload shows default/six values, exact auto order, direct-only values, safe timeout, no replay, raw-error exclusion, and external oracle | Fresh line-oriented readback found every marker; packed and installed workflow config, QA skill, and helper hashes matched exactly | pass |
| Missing prerequisite | Scrubbed helper preflight returns one bounded unavailable result and does not act | Exit 2; one stdout JSON object; empty stderr; `unavailable`; `fallback_safe: true`; Playwright MCP; `not-started`; `not-passed`; no evidence root | pass |
| Consequential policy | Policy rejects before prerequisite/browser discovery | Exit 2; one stdout JSON object; empty stderr; fixed policy limitation; safe Playwright metadata; no evidence | pass |
| Invalid evidence destination | Outside-root request is invalid and leaves sentinel unchanged | Exit 2; one stdout JSON object; empty stderr; `invalid`; no fallback/evidence; sentinel hash stayed `585b9b70…d53273` | pass |
| Live Jev/fallback/oracle | Ready Jev-first, safe constructor timeout, unsafe no-replay, and matching browser oracle are observed | No consumer fixture, provider, Jev, Browser Harness, Playwright MCP, Orca, Maestri, or browser was authorized or available | untested |

## Criterion disposition results

| AC | Planned public observation | Result |
| --- | --- | --- |
| 1 | Absent table/key accepted; installed default readback | offline pass; effective live selection remains part of untested scenario |
| 2 | Six public values through both readers | pass |
| 3 | Alias, unknown value, unknown key; enum and marker exclusion | pass |
| 4 | Installed exact auto route and one-native priority | policy readback pass; live chain untested |
| 5 | Installed direct-only contract and internal Jev mapping | policy/config pass; live direct adapters untested |
| 6 | Existing local config byte preservation plus absent default | pass |
| 7 | Ready eligible Jev-first route | untested — no live consumer runtime |
| 8 | Unavailable preflight and Playwright-first metadata | offline preflight pass; downstream live adapters untested |
| 9 | Typed constructor-timeout safe continuation | untested — no Jev/browser runtime or test double used |
| 10 | Post-action/ambiguous no-replay | untested — no product action or second driver used |
| 11 | Completion remains non-passing until independent reload | policy readback pass; successful live browser oracle untested |
| 12 | Config diagnostics, package membership, scrubbed preflight output | offline pass; full ready/failure redaction remains Technical Verification forward evidence |

## Independent readback

Separate processes reloaded the archive, installed files, config fixtures, preflight JSON, and final
hashes. Packed and installed SHA-256 values matched for `workflow_config.py`
(`1dc9203c…d0cbd`), `wtk-qa-execute/SKILL.md` (`9d08c679…0ef9d`), and `jev_adapter.py`
(`bbc77850…04d36`). Consumer `.wtk.toml`, `package.json`, and `bun.lock` retained their original
hashes. No browser adapter ran: the actual product path was packed CLI/manual installation, installed
config CLI validation, helper `preflight`, and independent filesystem readback.

The first exact-substring readback script reported false for several wrapped/backticked instruction
markers. A fresh line-oriented reload located the authoritative installed lines and matching hashes;
this was observer formatting, not product divergence.

## Findings

No product defect observed. No bug record created.

One initial runner attempt reached Node's `ERR_MODULE_NOT_FOUND` before the consumer was initialized
because a directly extracted archive has no installed dependency tree. The consumer stayed clean.
The single clean retry reused the checkout-local, lock-matching `smol-toml@1.8.0` dependency without
network or installation and completed the public flow. Two later no-op prompt harness attempts used
an imprecise Expect pattern and were stopped without writes; the existing repository pattern
`Modules.*comma-separated` completed the remaining matrix. These are harness/setup limitations, not
product findings.

## Cleanup and residue

The detached source worktree was removed. The exact disposable root
`/tmp/default-jev-auto-qa.EooUdm` was moved to Trash as
`/Users/antoniofulg/.Trash/default-jev-auto-qa.EooUdm`; cleanup is recoverable and the original path
is absent. Product HEAD remains `f39fef06`. Final source status differs from the opening snapshot only
by the planned charter, report, scenario update, existing verifier artifacts, and ignored raw evidence.
`workflow.json` is unchanged.

## Selected gate

- Reused: independent Technical Verification PASS at `f39fef06`; product code, configuration
  authority, tests, dependencies, and runtime inputs stayed unchanged during QA.
- Fresh QA structural close: all four raw evidence JSON files parse; scenario id/status/report/evidence
  fields and charter/report links resolve; no pending report row remains; durable files have no
  trailing whitespace.
- No full or automated product gate was repeated because QA changed only QA records and exercised the
  frozen package through its public interfaces.

## Limitations

The source pack cannot reach the scenario's complete expected observable: live ready Jev execution,
constructor-time timeout continuation, post-action/ambiguous no-replay, downstream Playwright/IDE
fallback, and matching independent browser readback were not walked. Missing tooling keeps the
scenario `untested`, not `blocked-verify`. Technical tests remain separately labeled evidence and do
not grant the QA verdict. No registry/network access, credential, provider call, browser launch,
framework/tool installation, external security-skill execution, product fix, push, or deployment
occurred.

## Verdict

**UNTESTED** — every charter-authorized offline CLI/package/config/preflight/readback leg passed with
no product defect, but the complete live default-`auto` browser promise is unreachable in this source
checkout. `QAS-use-optional-jev-qa-adapter` correctly remains `qa_status: untested`.

## Execution metrics

Execution metrics — measured interval: 2026-09-19T23:51:59-03:00 -> 2026-09-20T00:03:15-03:00; complete.

| Stage | Actor/session | Provider/model/effort | Elapsed | Tokens (input / cached input / output) | Rounds |
| --- | --- | --- | --- | --- | --- |
| QA Execute | `/root/verify_default_jev_qa` | codex / `gpt-5.6-sol` / high from frozen route; billing tier unavailable | 11m16s | unavailable - harness exposed no task-scoped usage counters | 1 |

Total elapsed: 11m16s | Cumulative actor time: 11m16s | Token total: unavailable

Token cost: unavailable - no provider-reported billable token breakdown or billing tier.

Validation overhead (included above): one local package build/readback; one successful public install
after one dependency-setup retry; two-reader matrices covering eight accepted and three rejected
configurations; three helper preflights; one structural close. Reused evidence: Technical
Verification at the identical frozen product snapshot. Waiting/blockers: none. Unmeasured scope:
model tokens/cost and all live browser/provider/MCP runtime.

Verification cycles: 1 QA Execute cycle | 0 implementation returns | 0 completed fix loops | 0
pending returns | first-pass complete-promise acceptance: not achieved because authorized runtime
scope is unavailable, not because of a product defect.

Optimization: use the repository's exact `Modules.*comma-separated` Expect pattern and link the
checkout-local dependency tree before invoking a directly extracted archive; this avoids three
observer-only setup retries without reducing product coverage.
