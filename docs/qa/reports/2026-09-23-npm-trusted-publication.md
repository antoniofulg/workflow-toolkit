# Trusted npm Publication QA Retest

- **Date:** 2026-09-23
- **Frozen tree:** `cfa8e4ae4c09ab1dab7096dd8b530d6fe05784d8`
- **Result:** PASS — release `v1.4.5` published the tested archive through npm trusted publishing with signed SLSA provenance
- **Adapter:** CLI/manual through read-only GitHub and npm public interfaces, with independent local manifest readback
- **Execution path:** GitHub Actions run `35814659824`; GitHub release `v1.4.5`; npm package, dist-tags, and attestations endpoints
- **Environment:** Darwin 27.0.0 arm64; Node v22.23.1; npm 10.9.8; GitHub-hosted Ubuntu runner recorded by Actions
- **Recorded gate:** GitHub Actions run `35814659824` — completed success; `test` and dependent `publish` jobs passed
- **Raw evidence:** `docs/qa/evidence/2026-09-23-npm-trusted-publication/readback.md`

## Matrix

| Charter | Scenario | Verdict | Independent confirmation | Evidence |
| --- | --- | --- | --- | --- |
| `CH-review-npm-trusted-publication-2026-09-22` | `REL-report-current-workflow-release` | pass | Release/tag/run SHA, local dry-run archive identity, registry bytes, `latest`, publish log, and signed attestation endpoint agree on `1.4.5` | `readback.md` |

## Results

GitHub release `v1.4.5` is public, stable, and bound to frozen revision
`cfa8e4ae4c09ab1dab7096dd8b530d6fe05784d8`. Release-triggered Actions run
`35814659824` used the same SHA and completed successfully. Its read-only `test` job passed release
identity, frozen install, the full test gate, clean-checkout, packaging, and artifact upload. The
dependent `publish` job passed download, archive verification, and npm publication.

The public publish log records `npm publish` with `--provenance --access public --tag latest`, a
signed provenance statement sourced from GitHub Actions, transparency-log index `2914610457`, and
the terminal `+ workflow-toolkit@1.4.5` result.

The public registry reports `workflow-toolkit@1.4.5`, `latest=1.4.5`, the expected description,
homepage, repository, integrity, shasum, and attestation URL. A local `npm pack --dry-run` produced
the same integrity and shasum without creating an archive. The attestation endpoint independently
returned the npm publish attestation and SLSA provenance/v1 as signed Sigstore bundles with
transparency-log entries.

## Historical attempts

Runs for `1.4.2`, `1.4.3`, and `1.4.4` remain recorded as failures. In each, the test job failed,
package/upload did not complete, and the dependent publish job was skipped. Changelog entries and
the intervening commits record the missing Linux `expect` prerequisite, portable PTY control-signal
correction, and readline-close cancellation fix. Run `35814659824` confirms those earlier attempts
were superseded by the passing `1.4.5` test and publish path; their historical outcomes were not
rewritten.

## Gate selection

The production-parity gate is the successful public release workflow itself: its test job ran the
full project gate before packaging, and its dependent job published only the verified artifact. This
bounded retest independently read the public end state and used a local dry-run to compare archive
identity. No local full gate was repeated. The durable scenario/report edits receive the focused
release-history contract and whitespace checks before commit.

## Findings

No product defect was observed and no bug record was created. The previous `blocked-verify` reason is
resolved by the successful `1.4.5` release, registry package, and signed provenance evidence.

## Cleanup

The local package command used `--dry-run` and created no archive. Final checkout status is expected
to differ from the opening clean snapshot only by this report and the scenario status update. The
primary checkout's unrelated `skills-lock.json` work was outside this checkout and untouched.

## Limitations

This retest did not induce npm rejection or mutate a GitHub release. The prior local contract proof
continues to cover terminal failure and unchanged-release behavior; the live success path now proves
OIDC publication and provenance. No tag, release, workflow rerun, npm publication, push, pull request,
merge, deploy, credential read, or other remote mutation occurred during QA.
