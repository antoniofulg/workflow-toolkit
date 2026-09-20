# CH-use-default-jev-auto-qa-2026-09-19

- **Date:** 2026-09-19
- **Scope:** frozen product snapshot `f39fef06b7183a87889c346b90835af0699fa59c` on `feat/default-jev-qa`
- **Time-box:** 45 minutes maximum; stop when every offline observable has evidence or a named limitation
- **Persona:** Workflow operator
- **Journey:** [`J-use-optional-jev-qa-adapter`](../journeys/J-use-optional-jev-qa-adapter.md)
- **Tour:** Exact-package installation, default/enum configuration, installed routing-policy readback, fail-closed preflight, independent reload, and residue tour
- **Public entry point:** local `workflow-toolkit-1.1.0.tgz` -> packed `wtk install` with `quality` selected -> consumer `.wtk.toml` and installed `.agents/skills/wtk-config/` plus `.agents/skills/wtk-qa-execute/`
- **Adapter candidate:** CLI/manual through the local packed package, public Python config CLI, installed helper preflight, and independent filesystem readback, as declared in [`docs/qa/README.md`](../README.md)
- **Scenario:** `QAS-use-optional-jev-qa-adapter`
- **Adjacent canary:** narrow archive membership, installer, config-preservation, and residue observations from `ADP-install-versioned-workflow-package`; do not reset its unchanged promise

## Mission

Walk the changed browser-QA promise through every public surface available in this source pack.
Install the exact reviewed package into disposable consumers, observe both configuration readers
through their existing public CLI/package paths, independently reload the installed selection and
safety instructions, and exercise only helper preflight paths that cannot contact a provider or
browser. Distinguish offline observations from the live Jev/fallback/oracle legs that this checkout
cannot walk.

## Expected observable

The exact local package documents and accepts only `auto`, `jev`, `playwright-mcp`, `orca`,
`maestri`, and `manual`; absence resolves to `auto`; `jev-ultrafast`, another unknown value, and an
unknown `[qa]` key fail with the six valid values without echoing the supplied marker. Adoption
preserves a consumer `.wtk.toml` with no `[qa]` table byte-for-byte while a fresh config read resolves
`auto`. Independent installed-file readback shows `auto` ordering Jev, Playwright MCP, exactly one
host-declared Orca or Maestri adapter, then manual; direct values select one adapter; unsafe or
uncertain action state forbids replay; and only independent readback after reload may grant `pass`.
With provider keys absent, installed helper preflight returns one secret-free structured
`unavailable` result with Playwright MCP as the eligible first fallback and performs no browser or
provider action.

Offline success does not close the whole scenario. `QAS-use-optional-jev-qa-adapter` remains
`untested` unless a later authorized consumer-level walk observes the live Jev-first route,
constructor-time safe timeout continuation, unsafe no-replay path, and matching independent browser
oracle.

## Criterion disposition

| AC | Surface | Disposition |
| --- | --- | --- |
| 1 | public config default | `QAS-use-optional-jev-qa-adapter`: omit `[qa]`, then omit only `browser_adapter`; observe `auto` through installed Python config CLI and packed installer path. |
| 2 | public config enum | Same scenario: exercise all six exact values through both installed readers and independently reload the effective value. This proves validation/preservation, not live adapter execution. |
| 3 | public config errors | Same scenario: submit `jev-ultrafast`, another unknown value, and an unknown `[qa]` key carrying an inert marker; require rejection, all six valid values, and no marker in stdout/stderr. No credential is read or synthesized. |
| 4 | agent-facing `auto` route | Same scenario: independently read installed instructions and helper metadata for Jev -> Playwright MCP -> exactly one host-declared Orca/Maestri -> manual, with Orca chosen if both exist. Live host-adapter execution is unavailable and remains an explicit limitation. |
| 5 | agent-facing direct route | Same scenario: read installed direct-selection contract for `jev`, `playwright-mcp`, `orca`, `maestri`, and `manual`; confirm `jev` maps internally and `jev-ultrafast` is rejected publicly. Do not substitute or launch an adapter. |
| 6 | adoption and sync | Same scenario: start with a byte-distinct consumer `.wtk.toml` lacking `[qa]`; run packed adoption/sync, compare bytes, and independently resolve `auto`. |
| 7 | ready Jev-first execution | Same scenario, limitation disposition: installed policy must name Jev first only for declared non-consequential dedicated fixtures. No installed Jev/browser/provider runtime exists, so ready execution is not simulated and cannot support `pass`. Retain Technical Verification as separately labeled forward evidence. |
| 8 | unavailable Jev fallback | Same scenario: with provider-key variables absent, invoke installed helper preflight and require `unavailable`, `fallback_safe: true`, Playwright MCP first, no evidence file, and no browser/provider action. Read the remaining one-IDE-native/manual order from installed policy. |
| 9 | safe constructor timeout | Same scenario, limitation disposition: independently read the installed typed constructor-timeout contract and technical receipt. Do not install/stub Jev or manufacture a timeout as QA; live safe continuation remains untested. |
| 10 | unsafe no-replay | Same scenario, limitation disposition: independently read the installed post-action/ambiguous stop-and-inspect/reset contract and technical receipt. Do not run a second driver or simulate a product action; live no-replay remains untested. |
| 11 | oracle-owned verdict | Same scenario: reload installed instructions in a separate process and confirm driver completion is never `pass` without matching independent readback after reload. No live completed driver result exists, so browser-oracle success remains untested. |
| 12 | credential/error exclusion | Same scenario: inspect archive membership for credential files, run config rejection with an inert marker, scrub provider-key variables before helper preflight, and require one bounded JSON stdout result plus empty stderr/evidence where specified. Full ready/failure redaction remains Technical Verification evidence because no real secret/provider/browser is used. |

## Planned probes

1. Confirm product HEAD is exactly `f39fef06b7183a87889c346b90835af0699fa59c`. Record opening porcelain and explicit checkout-owned package, runner, consumer, evidence, and outside-sentinel paths. Stop if product files differ from the frozen snapshot; verifier-owned `verification.md`, `workflow.json`, this charter, and later QA report/status fields are the only allowed checkout changes.
2. Create the exact local archive through `bun pm pack --filename <pack-dir>/workflow-toolkit-1.1.0.tgz --ignore-scripts`. Record archive SHA-256 and complete membership from a separately extracted runner. Require `.wtk.toml.example`, both config readers, `wtk-qa-execute/SKILL.md`, and `jev_adapter.py`; require no Jev Ultrafast, Browser Harness, Playwright, provider, `.env`, `qa.env`, or credential dependency/file.
3. Prepare a disposable Git consumer with a byte-distinct `.wtk.toml` copied from the v3 example after removing `[qa]`. Snapshot its config, package, lock, and managed-tree bytes. Run packed `node <runner>/package/bin/wtk.js install` in a PTY, select `quality`, inspect the preview, and approve. Require `core` plus `quality`, no package/lock dependency change, and byte-identical local `.wtk.toml`.
4. Through fresh processes, reload installed `.wtk.toml.example`, `wtk-config/SKILL.md`, `workflow_config.py`, `wtk-qa-execute/SKILL.md`, and `jev_adapter.py`. Record exact installed paths and hashes. Require the six public values, default `auto`, no public `jev-ultrafast`, exact automatic order, direct-only selection, typed constructor-timeout eligibility, unsafe stop/reset rule, raw-error exclusion, and independent oracle/reload ownership.
5. Exercise the installed Python configuration CLI against checkout-owned disposable consumers for absent `[qa]`, absent `browser_adapter`, and every accepted value. Independently reload generated/current output and local config; require `auto` for absence, exact preservation for explicit values, and no local-config byte mutation from sync.
6. Exercise the packed installer reader through disposable consumers for the same absent and accepted configurations. Require normal preview/installation or no-op flow without config mutation. Use separate consumers or restore the recorded fixture between cases; never reuse uncertain state.
7. Exercise both public readers with `jev-ultrafast`, an unrelated unknown value, and an unknown `[qa]` key whose value is an inert marker. Require rejection before QA execution, the six valid values in diagnostics, and no marker in stdout/stderr. Do not place or imitate a credential in any field.
8. Start a scrubbed child environment with `TYPESAFE_API_KEY`, `AI_GATEWAY_API_KEY`, and `TEXT_MODEL_API_KEY` absent. Invoke the installed helper with a local HTTP fixture URL, bounded goal, `--journey-scope non-consequential`, dedicated headless declaration, and contained evidence paths. Require exit `2`, exactly one JSON stdout object, empty stderr, `status: unavailable`, `failure_class: unavailable`, `fallback_safe: true`, `fallback_adapter: playwright-mcp`, `action_state: not-started`, `qa_verdict: not-passed`, empty evidence, and no browser/provider process.
9. Repeat only the existing fail-closed public preflights needed to confirm policy order: consequential journey rejection before prerequisite discovery and an evidence destination outside the declared checkout-owned root with an unchanged outside sentinel. Do not enter ready execution.
10. Reload installed files and the consumer config from separate processes after all probes. Compare hashes with archive/fixture bytes and record actual attempted path, no-browser-used result, evidence or absence, each limitation, and why AC 7, 9, 10, and the live portion of AC 11-12 remain untested rather than passed.
11. Remove only the recorded disposable roots. Require source porcelain to match the opening snapshot except the durable QA report and allowed scenario evidence/report/status updates. Preserve this charter, the existing journey, unrelated scenario state, `verification.md`, and `workflow.json`.

## Boundaries and limitations

Do not launch or install Jev, Browser Harness, Playwright, Orca, Maestri, Chrome, another browser,
provider SDK, test double, framework, or external skill. Do not read, set, print, copy, reuse, or
synthesize provider credentials; parse `.env` files; contact a registry or other network endpoint;
run `scripts/install_security_skills.py`; publish; push; open or merge a pull request; deploy; mutate
production; or change product code. The public interface is limited to the exact local package,
packed `wtk install`, installed config/helper CLIs that stop at preflight, and manual independent
filesystem readback.

Missing live tooling is not `blocked-verify`; keep the scenario `untested`. Automated Technical
Verification may be cited as forward evidence but never converted into a QA observation. Stop unsafe
or dependent paths on any unexpected browser/provider reach, credential request, product-tree drift,
or state whose ownership cannot be proven.

## QA Execute handoff

Dispatch `phase: wtk-qa-execute` for flow `wtk-qa` against frozen product snapshot
`f39fef06b7183a87889c346b90835af0699fa59c`. Read `docs/qa/README.md`; use its existing local-package
CLI/manual adapter and only the probes above. Store disposable evidence under
`docs/qa/evidence/2026-09-19-default-jev-auto-qa/`, write the durable report to
`docs/qa/reports/2026-09-19-default-jev-auto-qa.md`, and update only
`QAS-use-optional-jev-qa-adapter` from observed results. Keep its stable id and journey. The scenario
cannot become `pass` from offline results alone; absent an authorized live consumer fixture, retain
`qa_status: untested`, add the new report/evidence paths only if they accurately back that current
status, and name the unwalked runtime legs.

Record the selected interface/runner, exact package and installed paths, archive identity, each
criterion disposition, evidence or absence, limitations, independent reload, cleanup, and final
residue. Reuse the Technical Verification PASS only as separately labeled forward evidence after
confirming product inputs remain `f39fef06`. Stop and batch any product defect for a new Implementer;
do not fix code, install tooling, expand into live provider/browser work, or execute another journey.
