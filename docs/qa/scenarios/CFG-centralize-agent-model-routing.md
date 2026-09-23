---
id: CFG-centralize-agent-model-routing
area: CFG
title: Synchronize every provider agent from central model settings
persona: Workflow adopter
journey: J-configure-feature-workflow
expected: Explicit sync and resolution use only .wtk.toml.example and the byte-preserved local .wtk.toml, render current native packets, default verification to standard, accept light, standard, and ui when pinned by checks, and reject obsolete config names without aliases.
entry_points: .wtk.toml.example; .wtk.toml; .agents/skills/wtk-config/assets/agents/; .agents/skills/wtk-config/scripts/workflow_config.py; .claude/agents/; .codex/agents/; .cursor/agents/
qa_status: skipped
bug_ids:
fix_status:
retest_status:
fix_commits:
evidence: docs/qa/evidence/2026-09-13-workflow-toolkit-lean/lean-summary.md
last_report: docs/qa/reports/2026-09-13-workflow-toolkit-lean.md
overlaps: ADP-adopt-workflow-safely; CFG-preload-agent-skills-in-packets
---

Retired — WTK no longer owns central TOML model/effort routing or generated provider packets.
Current native model and effort ownership is covered by `ADP-adopt-workflow-safely` and the
native route contract in `CFG-resolve-deep-review-cadence`. The prior report remains historical.

Covers E2E-001 and E2E-002: local model/effort editing, template-driven native packet generation,
idempotent reporting, invalid-source and symlink containment, frozen delegated settings, explicit
drift rejection, fresh adoption, and runtime regeneration.

The `phase-skills` feature makes Claude templates carry `skills:` and `disallowedTools:` and gives `--sync-agents` a new fail-closed preflight, so the rendering promise now covers lines this scenario never walked; walked on 2026-09-03 and confirmed `pass`: a perturbed `.wtk.toml` changed only the `model` and `effort` lines of the affected packets, while `skills:` and `disallowedTools:` were carried through byte for byte. Prior evidence remains historical.

The `specify-impact-designer` feature adds `designer` as a sixth matrix role (eighteen native model and effort fields), three `[models.<provider>.designer]` example tables, three designer templates, and a fail-closed missing-table refusal. `AGENTS.md` names designer among the roles and stays at or below 134 lines; `docs/toolkit/pack.md` names five windows. Reset to `untested`. Prior evidence remains historical.

The `lean-consumer-installation` cycle moves the provider template source under
`workflow-config/assets/agents`. Reset to `untested`; prior evidence remains historical. Walk
`CH-sync-skill-owned-agent-packets-2026-09-08` against the final reviewed installed package.

The 2026-09-13 replacement renames both configuration sources and their owning skill. In a
disposable consumer, preserve every selected local value through sync and re-adoption, exercise
native-provider resolution with approved `ui`, explicit `standard`, and the default `standard`, and
confirm `.my-workflow.toml` names are rejected rather than read. Prior reports remain historical.
