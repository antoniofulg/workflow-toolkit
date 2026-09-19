# CH-review-release-1-1-0-2026-09-19

- **Date:** 2026-09-19
- **Scope:** local release candidate `ea132ad32c1e1ff9d074ca9535d24102137e05fd`
- **Time-box:** 20 minutes maximum; stop after local package readback and cleanup
- **Persona:** Repository reader
- **Journey:** [`J-review-workflow-release`](../journeys/J-review-workflow-release.md)
- **Tour:** Release identity, archive membership, credential exclusion, packaged CLI adoption, and residue
- **Public entry point:** `CHANGELOG.md`, `README.md`, `package.json`, `bun.lock`, and the local package archive
- **Adapter:** CLI/manual through the packed public `wtk` executable plus independent filesystem readback
- **Scenario:** `REL-report-current-workflow-release`

## Mission

Read and install the finished source pack as a repository maintainer. Confirm release `1.1.0`
identity, shipped Jev adapter membership, credential exclusion, and usable packaged CLI without any
registry, publication, or remote action.

## Expected observable

The newest changelog release, README, package manifest, Bun lockfile, installer constant, and local
archive agree on `workflow-toolkit@1.1.0` with sole executable `wtk`. The archive contains
`.agents/skills/wtk-qa-execute/jev_adapter.py`, contains no `qa.env` or credential file, installs into
a disposable Git consumer, and the installed files survive an independent reload.

## Planned probes

1. Compare version identity and public commands across the changelog, README, manifest, lockfile,
   installer constant, and extracted archive manifest.
2. Create the exact local archive declared by the QA profile and inspect its complete member list.
3. Require the Jev adapter and its owning QA skill; reject `.env`, `qa.env`, credentials, and
   checkout-only residue.
4. Run the packed public CLI in a disposable Git consumer and independently reload the installed
   manifest, adapter, skill instructions, and workflow version.
5. Reconcile the release claims with the packaged contracts and the existing optional-Jev feature
   QA report without repeating that feature-level browser walk.
6. Remove the disposable package, extraction, and consumer roots; compare final source status with
   the opening snapshot apart from this cycle's durable QA artifacts.

## Boundaries

No registry lookup, network fetch, publication, tag, push, pull request, merge, deploy, production
mutation, external skill installation, provider call, secret read, or browser run. Registry/tag
consistency remains unavailable until an authorized publication cycle.

## QA Execute handoff

Use `wtk-qa-execute` with the declared CLI/manual adapter. Store raw evidence under
`docs/qa/evidence/2026-09-19-release-1-1-0/`, write
`docs/qa/reports/2026-09-19-release-1-1-0.md`, and update only
`REL-report-current-workflow-release` from observed results.
