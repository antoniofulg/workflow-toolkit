# Automatic npm publishing checks

Profile: standard
Plan: `.specs/features/npm-trusted-publishing/plan.md`

7 checks in 1 slice · 3 one-way doors · 1 go-live dependency

## Checks

### S1 - Publish a stable GitHub release to npm

**C1** - Only a stable `release.published` event with tag `vX.Y.Z` reaches the publish job; a prerelease is skipped without publishing (PUB-01, AC 1-2, SEC-001).
Proof: `bun test tools/shared/tests/publish-workflow.test.ts -t 'PUB-001 release trigger'`

**C2** - Malformed tags, commits outside `main`, package names other than `workflow-toolkit`, and package versions different from the tag fail before dependency installation or publishing (PUB-01, AC 3, SEC-001).
Proof: `bun test tools/shared/tests/publish-workflow.test.ts -t 'PUB-002 release identity'`

**C3** - A valid release installs the frozen Bun lockfile and runs `bun run test:all` before `npm publish`; a failed gate prevents publication (PUB-01, AC 4-5, SEC-003).
Proof: `bun test tools/shared/tests/publish-workflow.test.ts -t 'PUB-003 gate ordering'`

**C4** - The publish step targets public npm `latest` with OIDC, publishes the package from the release checkout, and requests no static npm write token (PUB-01, AC 6, SEC-002, SEC-003).
Proof: `bun test tools/shared/tests/publish-workflow.test.ts -t 'PUB-004 trusted publisher'`

**C5** - A rejected npm publish, including a duplicate version or missing trust, leaves the workflow failed and does not alter the GitHub release (PUB-01, AC 7).
Proof: `bun test tools/shared/tests/publish-workflow.test.ts -t 'PUB-005 publish failure'`

**C6** - The publishing job grants only `contents: read` and `id-token: write`, uses a GitHub-hosted runner with Node `22.14.0+` and npm CLI `11.5.1+`, and the manifest repository URL is `https://github.com/antoniofulg/workflow-toolkit` (PUB-01, AC 8-10, SEC-002, SEC-003).
Proof: `bun test tools/shared/tests/publish-workflow.test.ts -t 'PUB-006 publish identity'`

**C7** - Maintainer instructions name the one-time `workflow-toolkit` trusted-publisher setup for `antoniofulg/workflow-toolkit` and `publish.yml`, including direct publish permission and the release trigger (PUB-01, Impact: Operations).
Proof: `bun test tools/shared/tests/publish-workflow.test.ts -t 'PUB-007 maintainer setup'`

## Coverage

| Set (size) | Member -> proof | Unproven |
| --- | --- | --- |
| Release class (2) | stable `vX.Y.Z` C1 · prerelease C1 | - |
| Rejected release identity (4) | malformed tag C2 · non-main commit C2 · wrong package name C2 · wrong package version C2 | - |
| Publish gates (2) | frozen dependency install C3 · `bun run test:all` C3 | - |
| npm rejection (3) | duplicate version C5 · missing trusted publisher C5 · registry failure C5 | - |
| Workflow authority (4) | exact repository C6 · `publish.yml` trusted identity C4 · `contents: read` C6 · `id-token: write` C6 | - |
| One-way doors (3) | `release.published` C1 · OIDC trusted publisher C4 · tagged commit from `main` C2 | - |
| Security abuse cases (4) | ABUSE-001 C2 · ABUSE-002 C2 · ABUSE-003 C4/C6 · ABUSE-004 C3/C6 | - |

- Workflow configuration is the product contract; C1-C7 assert release decisions and trust boundaries rather than incidental YAML formatting.
- Live npm OIDC publication cannot be proved by a local dry run. The first future release remains go-live evidence after the external trust setting is configured.

## Test policy

| Code | Required proofs | Coverage expectation |
| --- | --- | --- |
| Release guard and workflow step ordering | Parse the workflow and exercise guard decisions with controlled tag, manifest, and Git refs. | One asserted result for each accepted and rejected member in Coverage; publish is never reached for a rejection. |
| Declarative OIDC/publish configuration | Parse the workflow and inspect only the published identity and permission fields. | Exact repository, workflow filename, permissions, registry and package metadata; no npm token. |

Evidence: there is no existing `.github/workflows/` publication owner, while `tools/shared/tests/qa-skills.test.ts` already owns release metadata and Bun authority checks. A dedicated `publish-workflow.test.ts` keeps the high-risk event and guard cases together. Cost: one new Bun test file with seven named cases; no new test dependency or browser runner.

## Swept

- validation: C1, C2 - release class, tag, commit and manifest identity.
- failure modes: C3, C5 - gate and registry failures stop publication.
- idempotency: C5 - an already published npm version fails without retry or overwrite.
- authorization: C4, C6 - GitHub OIDC trust scoped to the package, repository and workflow.
- concurrency: C5 - duplicate or out-of-order version attempts fail through npm's immutable version/latest rules.
- data lifecycle: n/a - no application data is stored or migrated; npm package versions remain immutable.
- dependency failure: C3, C5 - frozen install and registry/trust failure remain visible.
- state transitions: C1, C5 - release published starts one attempt; npm success or failure does not mutate the release.
- observability: C5 - the GitHub job is terminal success or failure with no hidden retry.

## Handoff

- One builder owns S1. Initial owned context is the plan (~8 KB), package manifest (~3 KB), existing release tests (~50 KB), and new workflow/test/docs estimated under 20 KB: under 81 KB total, about 21k tokens at `bytes / 4`, below the 150k budget.
- Go-live dependency: npm package owner must configure trusted publishing for `antoniofulg/workflow-toolkit`, workflow filename `publish.yml`, and direct `npm publish` permission after that workflow lands on `main`. Do not submit the current npm form until the workflow exists there.
- Verification limit: local tests can prove event guards, package identity, and publish configuration; only the first future unpublished release can prove npm's live OIDC exchange and provenance.
- **Boundary:** C1-C7 closed by the implementation commit; independent verification remains pending.
- **Settled mid-build:** Release identity validation runs before npm CLI and dependency installation.
- **Abandoned:** none.
