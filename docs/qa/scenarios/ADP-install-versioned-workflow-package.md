---
id: ADP-install-versioned-workflow-package
area: ADP
title: Install Workflow Toolkit from an exact local package
persona: Workflow adopter
journey: J-adopt-workflow
expected: An exact local workflow-toolkit package exposes only the wtk executable, completes a guided install without registry access, and reads back the reviewed package identity and managed tree from outside the source checkout.
entry_points: README.md#quick-start; package.json; bun pm pack --filename <pack-dir>/workflow-toolkit-1.0.0.tgz --ignore-scripts; node <runner>/package/bin/wtk.js install
qa_status: untested
bug_ids:
fix_status:
retest_status:
fix_commits:
evidence: docs/qa/evidence/2026-09-13-workflow-toolkit-adoption/adoption-summary.md; docs/qa/evidence/2026-09-13-workflow-toolkit-adoption/package-core-readback.log
last_report: docs/qa/reports/2026-09-13-workflow-toolkit-adoption.md
overlaps: ADP-adopt-workflow-safely; ADP-layered-workflow-adoption; ADP-resolve-legacy-adoption-conflicts
---

Walk the public package bin from a runner outside the source checkout. Pin the exact local tarball,
run `workflow-spec-driven install` in a PTY from the disposable target, select all four modules, and
review the complete plan before approval. Repeat the same selection after an independent reload and
require `Selected modules are up to date. No files will change.` with zero target writes. Use a prior
manifest fixture to exercise managed provider-template promotion and runtime regeneration.

Preserve consumer product context, local `.wtk.toml`, package metadata, an existing QA
profile, and non-empty wiki/raw knowledge byte-for-byte. Confirm a fresh target receives only generic
managed knowledge instructions and neutral consumer-owned indexes, while source concepts and dated raw
observations remain absent. Confirm edited provider templates and retired workflow files become
explicit conflicts before final confirmation. Cancel or exclude to prove zero writes; accept
replacement only after its backup action is visible. Pristine retired workflow files are removed
only when their ownership hashes match.

The package installs five reviewed security skills through core without a child network installer.
Existing modified destinations remain subject to the normal preview/conflict/backup contract.

The `lean-consumer-installation` cycle changes archive membership, installed paths, previous-layout
retirement, and repeat-apply output. Reset to `untested`; prior evidence remains historical. QA must
upgrade the real prior tarball identified by SHA `c85e68c...` to a fresh final-reviewed tarball
identified by a distinct SHA, even when both declare `0.10.0`.

The `interactive-installer` cycle replaces `plan`, `apply`, `resolve`, and `status` with the guided
`install` journey and changes the current package identity to `workflow-spec-driven@0.10.1`. Its QA
walk uses the final reviewed local tarball at `4487afb`; all earlier evidence remains historical.

The 2026-09-13 Workflow Toolkit Lean cycle replaces package identity and executable. Re-walk this
scenario from an exact local archive with no registry lookup. Prior reports and evidence remain
historical until the new `workflow-toolkit` / `wtk` result is observed.
