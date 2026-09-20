# J-enable-external-security-skills

**Persona:** Workflow adopter
**Goal:** Install the reviewed security lifecycle through Workflow Toolkit's core module.
**Entry point:** exact local package → `wtk install` → core

## Flow

1. Pack the exact Workflow Toolkit snapshot and confirm the archive contains all five complete skill
   trees, `skills-lock.json`, and no standalone security installer.
2. Review the five source, path, CLI-version, commit, and tree-hash authorities in `skills-lock.json`.
3. Install each module selection into a checkout-local disposable target and inspect the preview.
4. Independently read the five installed trees, Claude links, adoption-manifest hashes, and consumer
   sentinels; confirm no networked child installer ran.
5. Re-run the same installation and require a no-change result.
6. Exercise cancellation, modified-destination conflict, and publication rollback through the normal
   guided installer and confirm consumer-owned state is preserved.

## Promises

- [`ADP-install-pinned-external-security-skills`](../scenarios/ADP-install-pinned-external-security-skills.md)
- [`ADP-preserve-security-install-target`](../scenarios/ADP-preserve-security-install-target.md)

## Adjacent canary

Walk [`ADP-adopt-workflow-safely`](../scenarios/ADP-adopt-workflow-safely.md) to confirm bundled
security files do not regress consumer-owned state preservation.
