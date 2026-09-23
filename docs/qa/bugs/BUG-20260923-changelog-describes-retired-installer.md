# BUG-20260923-changelog-describes-retired-installer

- **Status:** open
- **Severity:** major
- **Scenario:** `REL-report-current-workflow-release`
- **Expected:** Current changelog guidance distinguishes the unreleased skills-only source state from historical release instructions and names the 12-skill install boundary, optional security lifecycle, and explicit migration helper.
- **Observed:** `Unreleased` is empty, so the newest visible setup guidance remains the historical `1.4.1` block, which says security skills are installed in core and instructs readers to run `npx workflow-toolkit@1.4.1 install`; the current source package has no installer executable and security lifecycle is now optional.
- **Snapshot:** `e6002ca18d4fe07f842acff8c03efeca16748a72`
- **Adapter:** Manual public-document/package/installed-tree readback without registry access
- **Exact path:** Compare `CHANGELOG.md` current `1.4.1` block with `package.json` version and files, `bun.lock`, `README.md#install-the-skills`, and the isolated 12-skill installation.
- **Evidence:** `docs/qa/evidence/2026-09-23-native-agent-settings/release-readback.json`; `docs/qa/evidence/2026-09-23-native-agent-settings/install-readback.json`

## Impact

A reader looking for the current migration path reaches the historical `1.4.1` instructions because
the changelog has no current unreleased guidance. That route asks npx to run an executable that no
longer exists and expects a bundled security skill that the current source intentionally excludes.

## Remediation recommendation

Preserve the historical `1.4.1` record. Record the skills-only and native-settings changes in
`Unreleased`, or publish a new release block and matching package version that names the 12-skill
Skills CLI command, optional companion boundary, and one-time `scripts/migrate.js` cleanup path.
Extend the release consistency contract so the newest applicable guidance cannot name the retired
package installer or bundled security skills. Then rerun `REL-report-current-workflow-release` and
the adjacent provenance canary.
