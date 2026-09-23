# J-adopt-workflow

**Persona:** Workflow adopter
**Goal:** Install or update the full Workflow Toolkit skill set without losing consumer-owned repository state.
**Entry point:** README.md → **Install the skills** → Skills CLI full-set command
**Tags:** wtk-adoption

## Flow

1. Record the source checkout and disposable consumer state; inspect the README and selected skill source.
2. Run the documented full-set Skills CLI command and review the installed skill directories.
3. Independently compare AGENTS.md, CLAUDE.md, project configuration, generated provider files,
   ignore files, product context, knowledge, and unrelated files before and after installation.
4. For a legacy adopter, preview node scripts/migrate.js, review each file, block, link, packet, and
   ignore action, then apply only after the preview is understood.
5. Exercise pristine, edited, multi-block, generated-packet, and interrupted-publication migration
   fixtures. Confirm conflicts refuse writes, backups preserve bytes and modes, and rollback restores
   the exact prior state.
6. Remove only disposable roots and confirm source-checkout residue matches the opening snapshot,
   apart from the planned QA artifacts.

## Promises

- [`ADP-install-versioned-workflow-package`](../scenarios/ADP-install-versioned-workflow-package.md)
- [`ADP-layered-workflow-adoption`](../scenarios/ADP-layered-workflow-adoption.md)
- [`ADP-adopt-workflow-safely`](../scenarios/ADP-adopt-workflow-safely.md)
- [`ADP-resolve-legacy-adoption-conflicts`](../scenarios/ADP-resolve-legacy-adoption-conflicts.md)

## Adjacent canary

Inspect [`ADP-separate-external-security-skills`](../scenarios/ADP-separate-external-security-skills.md)
for optional companion provenance, then walk [`J-review-workflow-release`](J-review-workflow-release.md)
for source identity and release metadata.

## Current cycle

The current release installs 12 WTK skills as one set, leaves project-native agent settings untouched,
and provides no WTK TOML or generated provider packets. The full-set Skills CLI route and one-time
migration helper are current untested promises. Historical installer, module, packet, configuration,
and companion reports remain historical evidence and do not establish the current verdict.
