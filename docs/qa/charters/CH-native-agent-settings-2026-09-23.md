# CH-native-agent-settings-2026-09-23

- **Date:** 2026-09-23
- **Scope:** product snapshot `e6002ca18d4fe07f842acff8c03efeca16748a72`; QA planning artifacts may follow without changing the product snapshot
- **Time-box:** 60 minutes maximum; stop dependent paths on a defect and finish safe independent paths on the same frozen snapshot
- **Personas:** Workflow adopter; Workflow operator; Repository reader for the documentation and release canaries
- **Journeys:** [`J-adopt-workflow`](../journeys/J-adopt-workflow.md); [`J-configure-feature-workflow`](../journeys/J-configure-feature-workflow.md); [`J-use-optional-jev-qa-adapter`](../journeys/J-use-optional-jev-qa-adapter.md); [`J-review-workflow-release`](../journeys/J-review-workflow-release.md)
- **Tour:** Full 12-skill installation, project-native routing, fixed workflow defaults, legacy packet cleanup, and current setup guidance
- **Public entry points:** `README.md#install-the-skills`; `.agents/skills/wtk-lean/scripts/workflow_route.py`; `.agents/skills/wtk-ship/scripts/review_convergence.py`; installed `.agents/skills/wtk-qa-execute/`; `node scripts/migrate.js --root <project> [--apply]`
- **Adapter candidate:** Skills CLI/manual, public Python and Node CLIs, and independent filesystem readback through [`docs/qa/README.md`](../README.md)
- **Scenarios:** `ADP-install-versioned-workflow-package`; `ADP-adopt-workflow-safely`; `ADP-resolve-legacy-adoption-conflicts`; `CFG-route-project-native-agent-settings`; `CFG-keep-local-artifacts-out-of-git`; `CFG-resolve-deep-review-cadence`; `QAS-use-optional-jev-qa-adapter`; `REL-report-current-workflow-release`
- **Adjacent canary:** `DOC-read-explicit-workflow-provenance`; do not reset it unless the walk invalidates its current promise

## Mission

Act as a developer installing the current WTK set into a project that owns its native agent files.
Confirm the installed skills require no WTK TOML or config skill, route features without changing
native model and effort metadata, expose the fixed defaults, and still clean verified legacy provider
packets. Read the current setup guidance as a repository reader.

## Expected observable

The Skills CLI discovers and installs exactly 12 WTK skills. Installation changes only the Skills
CLI-owned skill, link, and lock scope while project sentinels remain unchanged. In a TOML-free
consumer, route creation, resume, and refresh leave all native agent files
byte-identical and persist provider/role identity without model or effort. Deep Review stays on
demand, the builder stays sequential, QA selects `auto` when the task gives no adapter, and the
remediation ledger reports `stall_attempts = 3` and halts on the third consecutive non-progress
attempt. Migration removes all 18 exact historical packets without current templates and preserves
edited or consumer-owned files. Current docs describe the same boundary.

## Criterion disposition

| AC | Disposition |
| --- | --- |
| 1 | `J-adopt-workflow` → `ADP-install-versioned-workflow-package` and `ADP-adopt-workflow-safely`: public Skills CLI discovery/install must return exactly 12 WTK skills and no `wtk-config`. |
| 2 | `J-adopt-workflow` plus `J-configure-feature-workflow` → installation scenarios and `CFG-route-project-native-agent-settings`: install and route with no `.wtk.toml` or example created or required. |
| 3 | `J-configure-feature-workflow` → `CFG-route-project-native-agent-settings`, with `ADP-adopt-workflow-safely` as the install canary: compare all 18 native files before and after install, create, resume, and refresh. |
| 4 | `J-adopt-workflow` → `CFG-keep-local-artifacts-out-of-git` and `ADP-adopt-workflow-safely`: inspect the clean source/package inventory and verify native metadata preservation. |
| 5 | `J-configure-feature-workflow` → `CFG-route-project-native-agent-settings`: independently read `workflow.json` and require provider/role identity with no model, effort, or WTK config fields. |
| 6 | `J-configure-feature-workflow` → `CFG-resolve-deep-review-cadence`: walk the public convergence CLI through an initial minimum plus three unchanged failure sets; require threshold `3`, open after the first two stalls, and halted after the third. |
| 7 | `J-configure-feature-workflow` → `CFG-resolve-deep-review-cadence`: require no automatic Deep Review groups and confirm direct `wtk-deep-review` remains installed and addressable. |
| 8 | `J-use-optional-jev-qa-adapter` → `QAS-use-optional-jev-qa-adapter`, with the install scenario as canary: absent task-scoped choice selects `auto`; only safe pre-action fallback may continue. Live browser/provider legs remain `untested` under this profile. |
| 9 | `J-adopt-workflow` → `ADP-resolve-legacy-adoption-conflicts` and `ADP-adopt-workflow-safely`: preview/apply all 18 exact packet fixtures without current templates and preserve the full edited matrix. Public rollback injection remains unavailable, so the broader migration scenario cannot become `pass` from this cycle alone. |
| 10 | `J-review-workflow-release` plus the three operational journeys → `REL-report-current-workflow-release`, the affected behavior scenarios, and `DOC-read-explicit-workflow-provenance` as canary: README, AGENTS, installed skills, and QA instructions must name project-native ownership and fixed defaults without TOML setup. |
| 11 | `J-adopt-workflow` and `J-review-workflow-release` → installation and release scenarios: source/package/installed inventories contain no WTK TOML example, provider template, config skill, or packet-generation entry point. |
| 12 | `J-adopt-workflow` → `ADP-install-versioned-workflow-package`, with `REL-report-current-workflow-release` as documentation canary: every local reference resolves inside the isolated 12-skill installation and no source-only path is required. |

Every AC has a public CLI, installed-tree, filesystem, or documentation observable. No criterion is
classified as internal-only. Automated Technical Verification remains separate forward evidence.

## Planned probes

1. Confirm the product snapshot is `e6002ca18d4fe07f842acff8c03efeca16748a72`. Record opening porcelain and exact checkout-owned source-copy, consumer, route, migration, and evidence paths. QA planning artifacts are allowed; any product-file drift pauses the walk.
2. Copy only the 12 WTK skill directories to an isolated local source. Use the existing Skills CLI to list and install the exact README selection into a disposable Git consumer. Independently require exactly 12 installed skills, resolved local references, no `wtk-config`, and no WTK TOML/config/provider-template payload.
3. Before installation, seed consumer-owned AGENTS, CLAUDE, ignore, product-context, knowledge, unrelated-config, and unrelated-file sentinels plus all 18 native Claude, Codex, and Cursor role files with byte-distinct model/effort metadata. After installation, compare sentinel bytes and modes, inventory Skills CLI-owned skill/link/lock additions, and require no WTK-owned host configuration or instruction edit.
4. In TOML-free disposable Git fixtures, create valid Lean checks and run `workflow_route.py` with Claude, Codex, and Cursor as the native provider. Resume and refresh each route. Independently compare all 18 native files, confirm neither WTK TOML path appeared, and require snapshots to store only the documented identity/default fields.
5. Inspect route output for `deep_review: {cadence: skip, groups: []}` and disabled parallelization, then confirm installed `wtk-deep-review` remains directly invocable. Read installed QA instructions with no task-scoped choice and exercise only the existing scrubbed, non-consequential helper preflight and safe fallback probes from `J-use-optional-jev-qa-adapter`; do not launch a browser or provider.
6. In a disposable feature root, invoke `review_convergence.py` once to establish the failing-set minimum, then three more times with the same fingerprint and normalized failing set. Independently read every JSON result and persisted ledger; require `stall_attempts: 3`, two open consecutive-stall results, then a halted third stall with its halt reason and attempted fixes.
7. Seed all 18 exact historical packet fixtures plus a separate full edited matrix. Run public migration preview and apply against the exact matrix, compare bytes/modes/state independently, and require every edited packet to remain. Do not use the private failure hook as a public rollback pass.
8. Read README, AGENTS, package metadata, changelog, Bun lockfile, installed skill instructions, QA profile, and current journeys/scenarios. Require one 12-skill contract, project-native model/effort ownership, no TOML setup step, fixed defaults, current helper paths, resolved installed references, and historical records clearly labeled historical.
9. Remove only recorded disposable roots. Require closing source status to equal the opening snapshot plus this cycle's durable QA report and allowed scenario status/report/evidence fields.

## Boundaries and limitations

No network, registry, browser, provider, optional companion installation, product edit, active feature
deletion, publication, push, pull request, merge, deploy, release, or production mutation. Do not use
the source checkout's native agent files as mutable fixtures. Jev consultation is unavailable because
the QA profile forbids network access. Missing live browser/provider tooling leaves its scenario
`untested`; it is not `blocked-verify`. A confirmed product defect returns to an Implementer.

## Planning risk

The current `CHANGELOG.md` release section still describes the retired package installer and bundled
security skills. `REL-report-current-workflow-release` must independently confirm whether that stale
release text contradicts the current 12-skill source boundary and report a defect if it does.

## QA Execute handoff

Dispatch one fresh non-author Verifier with `phase: wtk-qa-execute` against frozen product snapshot
`e6002ca18d4fe07f842acff8c03efeca16748a72` and this charter. Read `docs/qa/README.md`; use its existing
Skills CLI/manual, public Python/Node CLI, and independent filesystem-readback adapter. Store raw
evidence under `docs/qa/evidence/2026-09-23-native-agent-settings/`, write the durable report to
`docs/qa/reports/2026-09-23-native-agent-settings.md`, and update only the eight listed scenarios plus
the adjacent provenance canary if fresh observation invalidates it.

Walk safe independent paths after a defect, but stop every dependent path. Report the selected
interface/runner, exact paths, snapshot, evidence, limitations, independent readback, cleanup, and
residue. Batch product defects for an Implementer; resume only affected scenarios and causal canaries
on the new frozen snapshot. Do not fix product code or perform remote actions.
