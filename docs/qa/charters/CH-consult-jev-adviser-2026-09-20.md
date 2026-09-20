# CH-consult-jev-adviser-2026-09-20

- **Date:** 2026-09-20
- **Scope:** frozen product snapshot `2f9c575b97c5b98d9b8cc3b3ff8d66a9115239fd` on `feat/jev-lifecycle`
- **Time-box:** 15 minutes maximum; stop when the four offline legs and residue check are complete
- **Persona:** Workflow operator
- **Journey:** [`J-consult-jev-adviser`](../journeys/J-consult-jev-adviser.md)
- **Tour:** Six-phase preview, missing-key fallback, stale-hash discrimination, direct-policy routing, and residue tour
- **Public entry points:** `node .agents/skills/wtk/scripts/advise.mjs --phase <phase> [--send]`; direct WTK phase skill files
- **Adapter candidate:** CLI/manual through the public Node command plus independent filesystem readback, as declared in [`docs/qa/README.md`](../README.md)
- **Scenario:** `QAS-consult-jev-adviser`
- **Adjacent canary:** none; package membership and installer staging remain closed Technical Verification claims

## Mission

Walk every safe public behavior this source-pack checkout can observe without a key or network:
preview each supported phase, observe the missing-key send result, prove that changed normalized
input changes the advice fingerprint, and independently reload each direct phase route plus the
shared Jev-first policy. Keep live provider advice and actual host-agent compliance explicitly
untested.

## Expected observable

Each of `plan`, `build`, `verify`, `review`, `qa`, and `ship` exits 0 in preview mode with one JSON
object containing `status: preview`, a 64-hex-character `input_hash`, phase-matching state, a Choice
whose candidates include the two supplied options plus `insufficient_evidence`, and an independent
Noul. `--send` in an environment with `TYPESAFE_API_KEY` absent exits 3 with exactly
`{"status":"unavailable","reason":"missing_key"}` and no credential, provider call, artifact
mutation, or stderr leak. Changing phase, evidence, or options changes the hash; unchanged normalized
input retains it.

Independent readback resolves every direct lifecycle entrypoint to the one shared reference. That
reference requires Jev before every semantic choice whenever a key is available, even with a
preferred answer; limits disclosure; loads only the trusted existing caller credential when allowed;
retains host authority; continues on unavailable/insufficient evidence; and discards stale advice.

Offline success does not close the configured-host promise. `QAS-consult-jev-adviser` remains
`untested` until an authorized consumer walk observes a real host consulting Jev, checking returned
advice against current evidence, and taking no automatic action or gate verdict. The repository's
no-network QA policy forbids that leg here.

## Criterion disposition

| AC | Surface | Disposition |
| --- | --- | --- |
| 1 | Public preview request | Walk all six phases and read the Choice plus independent Noul from stdout. |
| 2 | Public preview/no-send behavior | Same walk: require exit 0 and preview output with no `--send`; inspect no residue. Network absence is constrained by the no-network environment and the command mode. |
| 3 | Successful provider advice | User-visible but unreachable under no-network/no-key policy. Carry Technical Verification plus the assigned synthetic connectivity smoke separately; do not claim a QA pass. |
| 4 | Public invalid-input behavior | Deterministic technical-only matrix already proven by JEV-003. The bounded QA tour does not repeat malformed/oversize cases. |
| 5 | Public unavailable behavior | Walk the missing-key `--send` case only. Timeout, HTTP, network, malformed, and oversize provider cases remain Technical Verification evidence because provider contact and doubles are outside this QA walk. |
| 6 | Request-count/retry invariant | Technical-only transport claim, proven with the controlled boundary in JEV-004; no live request is authorized. |
| 7 | Advisory-only authority and zero mutation | Inspect the installed/shared policy and compare source porcelain before/after all offline probes. Actual host compliance remains untested. |
| 8 | Credential recipient, redirect, and error secrecy | Technical-only security boundary, proven by JEV-005. QA reads no key and contacts no provider. |
| 9 | No implicit context collection | Technical-only helper boundary plus source residue observation. QA supplies synthetic stdin and performs no secret/context discovery. |
| 10 | Input fingerprint | Walk changed phase, evidence, and options plus one normalized-repeat control; require the expected hash differences/stability. |
| 11 | Jev-first direct invocation | Independently resolve direct routes and inspect the all-semantic-decisions rule and six phase examples. Real host invocation with configured Jev remains untested. |
| 12 | Disclosure, batching, advisory authority, staleness | Inspect the shared reference and the preview's two-question request; changed-input hash is the observable stale-result discriminator. Host adherence remains untested. |
| 13 | Unavailable/insufficient-evidence continuation | Walk missing-key command output and inspect the continue-with-existing-reasoning/no-gate policy. Actual host continuation remains untested. |
| 14 | Core/package distribution | Technical-only installation and package claims, proven by JEV-007/JEV-008. No duplicate adoption/package walk is planned. |

## Planned probes

1. Confirm HEAD is exactly `2f9c575b97c5b98d9b8cc3b3ff8d66a9115239fd`. Record opening
   porcelain and one checkout-owned disposable evidence root. Stop if product code moved; the
   technical verification report, this charter, the planning report, and later QA report/status
   updates are allowed checkout changes.
2. In a child environment with `TYPESAFE_API_KEY` removed, invoke the public helper once for each
   supported phase with the same synthetic decision, evidence, and two candidates. Store stdout,
   stderr, and exit status under `docs/qa/evidence/2026-09-20-jev-lifecycle/`. Parse through a
   separate process; require the preview observable above for all six results.
3. With the same scrubbed environment and synthetic stdin, invoke `--phase build --send`. Require
   exit 3, exact missing-key unavailable JSON, empty stderr, and no provider/network activity or
   created product artifact. Stop if any key is requested or provider reach is attempted.
4. Produce local previews for identical normalized input, changed phase, changed evidence, changed
   options, and reordered option keys. Compare hashes in a separate process: identical/reordered
   normalized inputs remain equal; each semantic change differs.
5. Reload the 14 entrypoint files enumerated by the technical JEV-006 proof through an independent
   filesystem read. Resolve each Markdown link to the same
   `.agents/skills/wtk/references/jev-adviser.md`. Inspect that shared reference for the always-when-
   available default, preferred-answer independence, minimal non-sensitive input, one batched
   Choice/Noul request, quiet trusted caller credential policy, advisory authority, unavailable
   continuation, and stale-result discard. Record instruction/path inspection separately from CLI
   observations.
6. Compare closing porcelain with the opening snapshot, allowing only the planned durable QA
   report/status updates. Remove only the recorded evidence/disposable roots after the report has
   captured the necessary paths. Do not change `qa_status` from `untested` merely because every
   offline leg succeeds.

## Boundaries and limitations

Do not read, load, print, copy, synthesize, or pass provider keys. Do not source
`~/.config/workflow-toolkit/qa.env`; contact TypeSafe or any other network endpoint; install a
framework or dependency; use a fake provider as a user walk; run the package installer; publish,
push, open or merge a pull request; deploy; or change product code. Do not convert the coordinator's
synthetic connectivity smoke or deterministic Technical Verification tests into host-agent QA.

If an unexpected key, provider reach, network attempt, product-tree drift, or uncontrolled state is
observed, stop that path. Safe independent legs may finish. Missing live provider/host capability
keeps the scenario `untested`; it is not `blocked-verify` under the scenario vocabulary.

## QA Execute handoff

Dispatch `phase: wtk-qa-execute` against frozen snapshot
`2f9c575b97c5b98d9b8cc3b3ff8d66a9115239fd`. Read `docs/qa/README.md`; use its CLI/manual adapter
through the source public helper and independent filesystem readback. Store disposable evidence
under `docs/qa/evidence/2026-09-20-jev-lifecycle/`, write the execution report to
`docs/qa/reports/2026-09-20-jev-lifecycle.md`, and update only
`QAS-consult-jev-adviser` fields justified by observed results. Report the selected interface,
runner, exact command/path, evidence, residue, and the live host/provider limitation. Stop and batch
any product defect for a new Implementer; do not fix product code or expand into network execution.
