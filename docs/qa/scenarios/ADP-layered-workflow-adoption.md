---
id: ADP-layered-workflow-adoption
area: ADP
title: Adopt workflow capabilities incrementally
persona: Workflow adopter
journey: J-adopt-workflow
expected: A project selects selected WTK skills, sees non-core selections include core, installs each exact current catalog including unchanged third-party Ponytail names plus optional prompt-review and current Claude aliases, and repeats with an explicit no-change result and no parallel module or retired alias.
entry_points: README.md#install-the-skills; npx skills add antoniofulg/workflow-toolkit --skill wtk wtk-config wtk-lean wtk-qa wtk-deep-review wtk-ship --agent '*' --copy --yes
qa_status: untested
bug_ids:
fix_status:
retest_status:
fix_commits:
evidence: docs/qa/evidence/2026-09-13-workflow-toolkit-adoption/adoption-summary.md; docs/qa/evidence/2026-09-13-workflow-toolkit-adoption/source-core-readopt.log; docs/qa/evidence/2026-09-13-workflow-toolkit-adoption/source-quality-readback.log; docs/qa/evidence/2026-09-13-workflow-toolkit-adoption/source-extras-readback.log
last_report: docs/qa/reports/2026-09-13-prompt-review-security-follow-up.md
overlaps: ADP-adopt-workflow-safely
---

This follow-up manual cycle was closed as over-scoped under `26950bf`. Current package/adoption
regression checks passed; unwalked charter legs are skipped, not reported as manual passes.

Fresh QA must select and install `core`, then select dependent modules in a new PTY session. Verify
that `core` is selected once and named as required, installed modules remain cumulative in the
manifest, omitted modules and their records remain unchanged, consumer `package.json` and `bun.lock`
survive, and the installed tree has canonical skill-owned runtime with no workflow-created root
`templates/` or `tools/`. Repeat the same selection and require the exact no-change summary.

The current cycle also covers selecting the full WTK skill set, conflict exclusion with dependency
cascade, staged provider-packet synchronization, and importing the installed assisted probe through
a call-counting fake `orca`. Exact hash, path-containment, manifest-schema, and publication-order
mechanics remain technical-verification evidence; QA observes their public no-write and
atomic-publication outcomes.

Release 0.9.1 adjacent QA passed fresh full and incremental consumers. Read-only plans stayed
unchanged; core and final four-layer states were clean; package/lock hashes survived; Bun knowledge
and zero-effect probe import passed; independent clones returned clean status.

QA Execute on 2026-08-30 passed all three layered-adoption charters at `714716c`. Read-only plans
kept the target byte-identical; incremental and full applies produced a clean four-layer manifest,
preserved consumer instructions, package metadata, local config, QA profile, custom skill pointer,
and missing-only files, and refused drift, collisions, unsafe symlinks, invalid blocks, and invalid
manifests without writes. Bun knowledge exited 0, probe import made zero Orca calls, reapply was
byte-stable, and the adopted target contained no repository test files or transaction residue. Live
Orca scenarios remain unchanged and outside this offline adoption verdict.

The legacy-adoption-resolution cycle changes the shared planning and publication path while
promising unchanged normal `plan`, `apply`, and `status` behaviour. The previous report remains as
history, but this promise is reset to `untested` for an adjacent disposable-target canary.

The 2026-08-31 adjacent canary passed at `827d629`: a fresh target's read-only plan stayed
byte-identical, normal parallel apply and status reached clean state, reversible managed drift
returned status exit 1 without writes, restoration returned exit 0, and all disposable state was
removed.

The `phase-skills` feature changes the fixed core layer's managed path list, so what `plan`, `apply`, and `status` report for `--layers core` has changed; reset to `untested` pending the 2026-09-03 cycle. Prior evidence remains historical.

The `lean-consumer-installation` cycle changes the `core`, `parallel`, and default `full` installed
footprints. Reset to `untested`; prior evidence remains historical. Fresh QA must confirm canonical
skill paths and absence of workflow-created root `templates/` and `tools/`.

The `interactive-installer` cycle removes the legacy command set. Current QA uses only the guided
`install` command; historical `plan`, `apply`, and `status` results above are not current entry
points or evidence for this cycle.

The 2026-09-13 cycle changes the catalog to `core`, `quality`, and `extras`, removes `parallel`, and
replaces old phase names with Workflow Toolkit names. Re-walk exact core and quality catalogs plus
all extras members; `ponytail-audit`, `ponytail-debt`, `ponytail-gain`, `ponytail-help`, and
`ponytail-review` retain their third-party names. Prior verdict is stale for this catalog.

The completed 2026-09-13 report and evidence cover the prior five-member extras catalog and remain
historical. The follow-up adds `prompt-review` as the sixth optional extra and refreshes Claude links
to current `wtk-*`, Ponytail, and `prompt-review` aliases while removing retired aliases. Reset to
`untested` pending source and packed CLI readback, byte-stable re-adoption, and a no-op/cancel canary.
