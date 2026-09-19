# CH-use-optional-jev-qa-adapter-2026-09-19

- **Date:** 2026-09-19
- **Scope:** `abacbb01..680076a0` on `feat/optional-jev-qa-adapter`; execute only against the frozen final reviewed snapshot
- **Time-box:** 30 minutes maximum; stop when the listed public observables and residue check are complete
- **Persona:** Workflow operator
- **Journey:** [`J-use-optional-jev-qa-adapter`](../journeys/J-use-optional-jev-qa-adapter.md)
- **Tour:** Exact-package installation, installed-policy readback, fail-closed preflight, and residue tour
- **Public entry point:** local `workflow-toolkit-1.0.5.tgz` → packed `wtk install` with `quality` selected → installed `.agents/skills/wtk-qa-execute/jev_adapter.py`
- **Adapter candidate:** CLI/manual through the local packed package and independent filesystem readback, as declared in [`docs/qa/README.md`](../README.md)
- **Scenario:** `QAS-use-optional-jev-qa-adapter`
- **Adjacent canary:** narrow archive membership, installer, and residue observations from `ADP-install-versioned-workflow-package`; do not reset its unchanged promise

## Mission

Walk the adapter exactly as a source-pack operator can: install the reviewed quality module from a
local archive, read its helper and instructions outside the source tree, and exercise only
fail-closed preflight paths. Prove that missing authority never becomes an implicit installation,
browser launch, provider call, or passing QA verdict.

## Expected observable

The exact local package contains and installs the optional helper plus its instructions without
adding Jev Ultrafast, Browser Harness, Playwright, or provider dependencies. Independent readback
shows dedicated headless-CDP default, explicit-headed dedicated-CDP policy, personal/default-browser
rejection, Playwright-first fallback, and external-oracle ownership. With provider keys absent, the
installed helper emits one secret-free structured `unavailable` result for missing prerequisites
and one for consequential-policy rejection; an escaping evidence destination emits `invalid` and
writes nothing outside the disposable evidence root. No live browser or provider is contacted.

## Criterion disposition

| AC | Disposition |
| --- | --- |
| 1 | `QAS-use-optional-jev-qa-adapter`: prove packaged helper/result contract and installed headless-default/explicit-headed dedicated-CDP policy. Live ready execution is unreachable here and remains Technical Verification evidence only. |
| 2 | `QAS-use-optional-jev-qa-adapter`: invoke installed missing-key and consequential-policy preflights; read the complete prerequisite list and Playwright → Orca → Maestri → manual order. No real keys, modules, browser, or fallback adapter are used. |
| 3 | `QAS-use-optional-jev-qa-adapter`: independently reload installed instructions and confirm `DONE` cannot grant `pass`. A live `DONE` is outside this source repository and is not simulated as QA. |
| 4 | Internal runtime-failure invariant after `Agent.run()` begins. No source-pack public surface can reach it without installing or stubbing the external runtime, so QA retains the Round 3 Technical Verification proof and does not claim a user walk. |
| 5 | `QAS-use-optional-jev-qa-adapter`: read the installed process-environment policy and absence of a stored duplicate key requirement; execute with all provider-key variables absent. Runtime aliasing remains Technical Verification evidence. |
| 6 | `QAS-use-optional-jev-qa-adapter`: invoke the installed CLI with an escaping evidence destination and prove structured `invalid` plus unchanged outside sentinel. |
| 7 | `QAS-use-optional-jev-qa-adapter`: the QA Execute report must name the installed helper as the attempted path, record that no browser adapter ran, cite evidence/absence and limitation, and record independent readback. |
| 8 | `QAS-use-optional-jev-qa-adapter`: invoke consequential-policy rejection before prerequisite discovery and read back the dedicated-browser/personal-browser restrictions plus Playwright-first fallback. Live fallback remains consumer-owned and uncalled. |

## Planned probes

1. Record `680076a0`, opening porcelain, and explicit checkout-owned pack, runner, consumer,
   evidence, and outside-sentinel paths. Stop if the product snapshot differs. Durable QA-plan files
   may be present; no other product change is allowed during the walk.
2. Build the local archive through the profile-declared `bun pm pack --filename <pack-dir>/workflow-toolkit-1.0.5.tgz --ignore-scripts` path. Record its SHA-256 and membership. From a separate extracted runner, confirm the archive contains both `wtk-qa-execute/SKILL.md` and `jev_adapter.py`, and its manifest declares no Jev Ultrafast, Browser Harness, Playwright, or provider dependency.
3. In a disposable Git consumer, snapshot `package.json`, `bun.lock`, and the managed tree. Run the
   packed `node <runner>/package/bin/wtk.js install` public entry in a PTY, select `quality`, review
   the complete preview, and approve. Require `core` plus `quality`, then independently reload the
   installed helper and instructions. Consumer package/lock bytes must remain unchanged.
4. Through a fresh process, inspect the installed instructions for optional selection,
   non-consequential scope, `TYPESAFE_API_KEY` plus `AI_GATEWAY_API_KEY`, no required stored
   `TEXT_MODEL_API_KEY`, dedicated headless default, explicit headed dedicated CDP, rejection of
   personal/default discovery, Playwright-first ordered fallback, actual-adapter reporting, and
   independent readback/reload ownership of `pass`.
5. Start a scrubbed child environment with `TYPESAFE_API_KEY`, `AI_GATEWAY_API_KEY`, and
   `TEXT_MODEL_API_KEY` absent. Invoke the installed helper with a local HTTP fixture URL, bounded
   goal, `--journey-scope non-consequential`, default headless mode, checkout root, and contained
   evidence paths. Require exit `2`, one parseable stdout JSON object, empty stderr, `adapter`,
   `status`, `evidence`, and `limitation`, status `unavailable`, missing-TypeSafe limitation,
   Playwright-first fallback metadata, empty evidence, and no created evidence file.
6. Repeat from a clean contained evidence directory with `--journey-scope consequential`. Require
   policy limitation before key/module/browser discovery, the same structured unavailable shape,
   and no created evidence file or browser/provider process. This is the only policy-execution leg.
7. Point `--evidence-dir` outside the declared evidence root while preserving an outside sentinel.
   Require exit `2`, one structured `invalid` result, empty stderr, and identical outside bytes.
8. Reload installed files from another process and compare their hashes with archive members.
   Record the exact helper path, actual attempted adapter path, no-browser-used result, JSON
   evidence or its absence, limitations, fallback order, and oracle readback in the durable report.
9. Remove only recorded disposable roots. Require source porcelain to match the opening snapshot
   except the planned report and this scenario's status/evidence/report fields.

## Boundaries and limitations

Do not launch Jev, Browser Harness, Playwright, Orca, Maestri, Chrome, or another browser. Do not
read, set, print, or reuse real provider keys; parse `.env` files; install a dependency or framework;
contact a registry; run `scripts/install_security_skills.py`; publish; push; open or merge a pull
request; or change product code. Do not use test doubles as a user walk. The source pack has no
browser app, so ready, post-start failure, live fallback, and successful independent browser-oracle
paths remain unwalked limitations backed only by separately labeled Technical Verification.

## QA Execute handoff

Dispatch `phase: wtk-qa-execute` against frozen snapshot `680076a0`. Read `docs/qa/README.md`, use
its local-package CLI/manual adapter, and walk only this charter through the installed package copy.
Store disposable evidence under
`docs/qa/evidence/2026-09-19-optional-jev-qa-adapter/`, write the durable report to
`docs/qa/reports/2026-09-19-optional-jev-qa-adapter.md`, and update only
`QAS-use-optional-jev-qa-adapter` from observed results. Record interface/runner, exact installed
path, archive identity, evidence or absence, limitation, independent readback, and residue. Stop and
return any product defect to a new Implementer; do not fix code, install tooling, or expand into a
live browser/provider walk.
