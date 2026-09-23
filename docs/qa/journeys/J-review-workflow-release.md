# J-review-workflow-release

**Persona:** Repository reader
**Goal:** Confirm Workflow Toolkit identity, provenance, shipped capabilities, and authority limits.
**Entry point:** `README.md`
**Tags:** wtk-release

## Flow

1. Reconcile `workflow-toolkit`, the current manifest version, executable `wtk`, and package
   membership across README, changelog, package manifest, lockfile, and a local archive.
2. Confirm project-owned capabilities use `wtk-*`, while third-party Ponytail skills and
   `prompt-review` keep their current names and `security-spec`, `security-threat-model`,
   `security-implementation`, and `security-review` remain separate pinned dependencies.
3. Follow workflow and provenance links; confirm Lean artifacts and modular artifact contracts are
   described without legacy aliases.
4. Inspect `wtk-ship`: an authorized feature-branch push, one pull request, and merge remain scoped
   delivery actions, while deploy, release, production mutation, force-push, direct `main` push, and
   unrelated remote work remain separately authorized. Perform no remote action during QA.
5. Reconcile public release claims with current scenario statuses and leave historical parallel
   reports explicitly historical.
6. For a stable GitHub release, follow the public `release.published` run through the read-only gate,
   checksum-bound archive, npm trusted-publisher identity, provenance, and public package readback.
   Record a future release action that QA cannot safely perform as `blocked-verify`.

## Promises

- [`DOC-read-explicit-workflow-provenance`](../scenarios/DOC-read-explicit-workflow-provenance.md)
- [`DOC-require-explicit-remote-action-approval`](../scenarios/DOC-require-explicit-remote-action-approval.md)
- [`REL-report-current-workflow-release`](../scenarios/REL-report-current-workflow-release.md)

This journey is the adjacent canary for `J-adopt-workflow`. The 2026-09-13 charter re-walks the
remote-authority promise and uses release/provenance rows as canaries without publishing.
