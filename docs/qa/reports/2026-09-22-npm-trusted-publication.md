# Trusted npm Publication QA Execute

- **Date:** 2026-09-22
- **Frozen tree:** `0a290ff30a35461c07e754f744e3115c757348d5`
- **Result:** BLOCKED-VERIFY — local contract and public readback matched; no release has exercised the new OIDC workflow
- **Adapter:** CLI/manual through local package commands and read-only GitHub/npm interfaces, with independent file and archive readback
- **Execution path:** `.github/workflows/publish.yml`; `README.md`; `package.json`; local package archive; public GitHub releases/Actions; public npm metadata
- **Environment:** Darwin 27.0.0 arm64; Node v22.23.1; Bun 1.4.2; npm 10.9.8; Git 2.54.0
- **Recorded gate:** fresh `bun test tools/shared/tests/publish-workflow.test.ts` — exit `0`; 7 passed, 0 failed, 71 assertions
- **Raw evidence:** `docs/qa/evidence/2026-09-22-npm-trusted-publication/`

## Matrix

| Charter | Scenario | Verdict | Independent confirmation | Evidence |
| --- | --- | --- | --- | --- |
| `CH-review-npm-trusted-publication-2026-09-22` | `REL-report-current-workflow-release` | blocked-verify | Local archive manifest and checksum plus public GitHub/npm reads confirmed current state; GitHub Actions reported zero runs for `publish.yml` | `readback.md` |

## Results

The canonical publication proof passed all seven named cases. It covered the stable release trigger,
prerelease skip, release identity rejection, frozen gate ordering, checksum-bound artifact handoff,
OIDC/public `latest` configuration, terminal publish failure, least privilege, runtime floors, and
maintainer setup text.

The exact local `npm pack --ignore-scripts` path produced a 243-file `workflow-toolkit@1.4.1`
archive. Independent archive readback confirmed the public package name, version, repository URL,
and `wtk` executable. The archive SHA-256 was
`fc82e892cd8d5c88424ad527d5dd9ade31d9b2371ce2d560727b4411af71c90b`.

Public readback found stable GitHub release `v1.4.1` at tag commit `539d3b13`, published at
`2026-09-23T00:18:03Z`, and npm `latest=1.4.1`, published at `2026-09-23T00:15:28.488Z`.
GitHub Actions reported zero runs for `.github/workflows/publish.yml`. The public `1.4.1` package is
therefore current release evidence, but it cannot prove this branch's later automatic publication
path. npm page metadata beyond the publication contract remains a separate follow-up.

## Gate selection

The focused canonical test owns the changed workflow contract and was rerun at the frozen snapshot.
The prior independent Technical Verifier PASS remains applicable because `0a290ff3` added only the
decision record after verified product revision `9e525287`. No full gate was repeated: local QA
changed only durable QA artifacts, and the focused proof plus exact package/readback path covers this
cycle's causal scope.

## Findings

No product defect was observed and no bug record was created. The missing live result is a declared
go-live dependency, not a failed implementation: `1.4.1` is already immutable, and no future
unpublished version exists for safe exercise of the OIDC exchange.

## Cleanup

The generated local archive and pack directory were removed after independent readback. Final source
status preserved the coordinator's pre-existing feature verification artifacts and differs from the
opening snapshot only by this cycle's planned journey, charter, report, and scenario changes.

## Limitations

Live npm OIDC exchange, provenance attestation, npm rejection behavior, and confirmation that a
failed publication leaves the GitHub release unchanged require a future unpublished version and a
human stable-release action. This cycle created no release, workflow dispatch/rerun, publication,
tag, push, pull request, merge, deploy, credential read, or other remote mutation. The scenario stays
`blocked-verify`; local tests and declarative inspection do not convert that leg to `pass`.
