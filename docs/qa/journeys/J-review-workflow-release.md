# J-review-workflow-release

**Persona:** Repository reader
**Goal:** Confirm Workflow Toolkit identity, provenance, shipped capabilities, and authority limits.
**Entry point:** `README.md`
**Tags:** wtk-release

## Flow

1. Reconcile `workflow-toolkit`, the current release version, private source metadata, and the exact
   12-skill inventory across README, changelog, package manifest, lockfile, and local package output.
2. Confirm project-owned capabilities use `wtk` or `wtk-*`, while Ponytail, Security lifecycle,
   Adaptive Guidelines, Graft, and Graphify remain optional external companions.
3. Follow workflow and provenance links. Confirm project-native files own model and effort, no WTK
   TOML or generated provider packets are current setup requirements, and Lean and modular artifact
   contracts are described without legacy aliases.
4. Inspect `wtk-ship`: an authorized feature-branch push, one pull request, and merge remain scoped
   delivery actions, while deploy, release, production mutation, force-push, direct `main` push, and
   unrelated remote work remain separately authorized. Perform no remote action during QA.
5. Reconcile public release claims with current scenario statuses and leave retired installer,
   configuration, provider-packet, and parallel-execution reports explicitly historical.

## Promises

- [`DOC-read-explicit-workflow-provenance`](../scenarios/DOC-read-explicit-workflow-provenance.md)
- [`DOC-require-explicit-remote-action-approval`](../scenarios/DOC-require-explicit-remote-action-approval.md)
- [`REL-report-current-workflow-release`](../scenarios/REL-report-current-workflow-release.md)

This journey is the adjacent canary for `J-adopt-workflow`. Current release/provenance walks use
local source and package readback without publishing or performing remote delivery.
