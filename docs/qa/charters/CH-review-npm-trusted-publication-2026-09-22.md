# CH-review-npm-trusted-publication-2026-09-22

- **Date:** 2026-09-22
- **Scope:** automatic npm publication feature at frozen revision `9e5252877da10d4d8cd1acee4154394b0bda3f82`
- **Time-box:** 20 minutes maximum; stop before any release, publication, or remote mutation
- **Persona:** Repository reader
- **Journey:** [`J-review-workflow-release`](../journeys/J-review-workflow-release.md)
- **Tour:** Stable-release trigger, release identity, tested archive handoff, OIDC authority, and public readback
- **Public entry point:** `.github/workflows/publish.yml`, `README.md`, local package archive, public GitHub releases and Actions, and public npm package metadata
- **Adapter:** CLI/manual through local package commands and read-only GitHub/npm interfaces, with independent file and archive readback
- **Scenario:** `REL-report-current-workflow-release`

## Mission

Read the finished publication contract as a repository maintainer. Confirm the release-triggered
workflow exposes the intended stable-release, tested-archive, and trusted-publisher path without a
stored npm write token. Observe current public GitHub/npm state without creating a release or
publishing a package.

## Expected observable

The workflow accepts only a stable `vX.Y.Z` release bound to its immutable event commit and `main`,
runs the frozen full gate in a read-only job, passes the tested archive by checksum, and grants OIDC
only to the dependent publish job. Maintainer instructions name the exact npm trusted-publisher
identity. A future unpublished stable release publishes that archive to public npm `latest` with
provenance, while a rejected publication leaves the GitHub release unchanged.

## Criterion disposition

| AC | Disposition |
| --- | --- |
| 1-2 | `REL-report-current-workflow-release` — inspect the stable `release.published` trigger and prerelease guard; a live skip remains unavailable unless an applicable public run exists |
| 3 | `REL-report-current-workflow-release` — exercise local release-identity validation with accepted and rejected fixtures, then independently read the workflow ordering |
| 4-6 | `REL-report-current-workflow-release` — run the exact local package proof, inspect the read-only gate and checksum-bound handoff, and confirm the publish command requests public `latest`, provenance, and OIDC without a static token |
| 7 | `REL-report-current-workflow-release` — inspect current public GitHub/npm state; do not induce an npm rejection or mutate a GitHub release |
| 8-10 | `REL-report-current-workflow-release` — compare workflow permissions/runtime floors and manifest repository identity with the documented trusted-publisher setup |
| Go-live | `REL-report-current-workflow-release` — a future unpublished version plus a human stable-release action is required for live OIDC exchange and provenance; record `blocked-verify` until that evidence exists |

## Planned probes

1. Record frozen revision, tool versions, opening source status, public repository remote, and the
   prior technical gate receipt.
2. Run the canonical publication workflow test and exact local package command. Inspect the archive
   manifest and checksum through a separate process; confirm name, version, repository, and no
   checkout residue.
3. Run the public release validator against one valid disposable Git fixture and selected rejected
   identities. Confirm rejection occurs before package installation or publication.
4. Read `.github/workflows/publish.yml`, `README.md`, and `package.json` independently. Confirm trigger,
   job ordering, permissions, runtime floors, checksum/manifest verification, public `latest`,
   provenance, exact trusted-publisher identity, and absence of a static npm token.
5. Query current public GitHub release/Actions metadata and npm package metadata read only. Reconcile
   what exists with the local version without creating a release, rerunning a workflow, or publishing.
6. Remove only checkout-owned disposable package and fixture roots. Compare final source status with
   the opening snapshot apart from planned durable QA artifacts.

## Boundaries

No release creation, workflow dispatch or rerun, npm publication, tag, push, pull request, merge,
deploy, production mutation, credential read, or product edit. Existing public metadata may be read.
The live npm OIDC exchange, provenance attestation, npm rejection behavior, and unchanged-release
result require a future unpublished version and human release action; local or declarative evidence
does not earn a QA pass for those legs.

## QA Execute handoff

Use `wtk-qa-execute` with the declared CLI/manual adapter. Store raw evidence under
`docs/qa/evidence/2026-09-22-npm-trusted-publication/`, write
`docs/qa/reports/2026-09-22-npm-trusted-publication.md`, and update only
`REL-report-current-workflow-release`. Expected terminal status is `blocked-verify` unless an already
completed matching public release supplies the full live OIDC and provenance evidence.
