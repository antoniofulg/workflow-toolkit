# J-adopt-workflow

**Persona:** Workflow adopter
**Goal:** Install or update Workflow Toolkit without losing consumer-owned repository state.
**Entry point:** `README.md` → **Quick start** → source `wtk install` or an exact local package
**Tags:** wtk-adoption

## Flow

1. Record the source checkout and disposable consumer state; inspect package identity and membership.
2. Launch the public CLI in a PTY from the consumer, select `core`, `quality`, or `extras`, and review
   the complete preview before confirmation. Any non-core selection includes `core`.
3. Read back the installed `wtk-*` skills, provider packets, docs, `.wtk.toml.example`, ignored
   `.wtk.toml`, and adoption manifest from a separate process. Confirm third-party Ponytail names
   remain unchanged, `prompt-review` is an optional extra with its current Claude alias, retired
   aliases remain absent, and the five reviewed security skills and aliases install through core.
4. Re-adopt the same target and require a no-change result while preserving consumer config, product
   context, QA records, knowledge, ignore rules, and unrelated files byte-for-byte.
5. In isolated copies, exercise cancellation, non-interactive refusal, consumer-modified conflicts,
   pristine managed retirement, and publication recovery. Confirm documented exits and no unintended
   writes.
6. Remove only recorded disposable roots and confirm source-checkout residue matches the opening
   snapshot apart from planned QA artifacts.

## Promises

- [`ADP-install-versioned-workflow-package`](../scenarios/ADP-install-versioned-workflow-package.md)
- [`ADP-layered-workflow-adoption`](../scenarios/ADP-layered-workflow-adoption.md)
- [`ADP-adopt-workflow-safely`](../scenarios/ADP-adopt-workflow-safely.md)
- [`ADP-resolve-legacy-adoption-conflicts`](../scenarios/ADP-resolve-legacy-adoption-conflicts.md)

## Adjacent canary

Inspect [`ADP-install-pinned-external-security-skills`](../scenarios/ADP-install-pinned-external-security-skills.md)
for packaged provenance, then walk [`J-review-workflow-release`](J-review-workflow-release.md) for
package identity and release metadata.

## Current cycle

Workflow Toolkit Lean replaced the prior package, executable, module catalog, phase skills, and
configuration names. Its completed 2026-09-13 report remains historical evidence. The follow-up
catalog cycle resets `ADP-layered-workflow-adoption` for optional `prompt-review` and current aliases,
and resets the security-skill installation promise for the bundled five-skill boundary. Safe
adoption is an adjacent canary; obsolete phase-skill and parallel-module promises remain `skipped`.
