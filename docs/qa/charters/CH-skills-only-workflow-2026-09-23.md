# CH-skills-only-workflow-2026-09-23

- **Date:** 2026-09-23
- **Scope:** initial snapshot `a0d09af820a61c5c7070e86b93634a96406cf608`; installation retest snapshot `a9566e32b39eb8e17d8dd306e4bcf630020ea207`
- **Time-box:** 45 minutes maximum; stop dependent installation paths on a defect and finish safe independent migration and documentation paths
- **Persona:** Workflow adopter; Repository reader for the documentation canary
- **Journey:** [`J-adopt-workflow`](../journeys/J-adopt-workflow.md), with [`J-review-workflow-release`](../journeys/J-review-workflow-release.md) as the documentation canary
- **Tour:** Full WTK Skills CLI install, legacy cleanup, and optional harness guidance
- **Public entry points:** `README.md#install-the-skills`; `node scripts/migrate.js --root <project> [--apply]`; `README.md#optional-project-instructions`; `README.md#recommended-companion-skills-and-tools`
- **Adapter candidate:** Skills CLI/manual, public Node CLI, and independent filesystem readback through [`docs/qa/README.md`](../README.md)
- **Scenarios:** `ADP-adopt-workflow-safely`; `ADP-install-versioned-workflow-package`; `ADP-resolve-legacy-adoption-conflicts`; `ADP-separate-external-security-skills`; `DOC-read-explicit-workflow-provenance`

## Mission

Act as a developer moving from the retired managed installer to project-owned WTK skills. Install
the documented full skill set into an isolated project, independently confirm host files are
unchanged, exercise the one-time migration helper across preview, apply, conflict, and rollback
outcomes, and read the optional instruction and companion guidance as a repository reader.

## Expected observable

The Skills CLI discovers and installs every skill named by the README. Only its skill scope changes.
Migration preview is read-only, apply removes only verified ownership with backups, conflicts write
nothing, and a publication failure restores exact state. The README clearly separates WTK, optional
project-owned instruction text, and independently installed companion tools with sources and uses.

## Criterion disposition

| AC | Disposition |
| --- | --- |
| 1-3 | `ADP-install-versioned-workflow-package` and `ADP-adopt-workflow-safely`: use the public Skills CLI against the exact local source, then independent inventory and sentinel readback. Remote GitHub resolution is unavailable under the no-network profile. |
| 4-8 | `ADP-resolve-legacy-adoption-conflicts` and `ADP-adopt-workflow-safely`: public preview/apply/conflict paths; publication rollback is observed through the shipped migration API because the public CLI intentionally exposes no fault-injection option. |
| 9-10 | Installed-tree reference and absent-companion outcomes belong to the installation scenarios. Agent route discrimination remains Technical Verification forward evidence. |
| 11 | `ADP-separate-external-security-skills` and `DOC-read-explicit-workflow-provenance`: manual README and installed-tree readback. Do not install optional companions because network access is outside the profile. |
| 12 | Lifecycle schemas and role separation remain Technical Verification evidence; QA reads only the public documentation consequences. |

## Planned probes

1. Record revision, opening porcelain, Skills CLI version, and exact disposable/evidence paths.
2. Ask the Skills CLI to list the exact local source with full-depth discovery. Require all 13 README skills before attempting installation. If any named skill is absent, stop the dependent install path and file one defect.
3. If discovery passes, create an isolated Git project with instruction, config, packet, ignore, product-context, knowledge, and unrelated sentinels. Run the README full-set command against the exact local source; independently list installed skills and compare sentinel bytes.
4. Build pristine and modified legacy fixtures. Run public preview, public apply, and public conflict commands; independently reload outputs, bytes, modes, links, adoption state, backup state, and unrelated sentinels.
5. Exercise publication rollback through the shipped `applyMigration` failure hook used by the canonical fixture. Keep this separately labeled technical-forward evidence because the public CLI has no safe failure-injection flag.
6. Read the optional project-instruction block and companion table. Confirm sources/use cases, unresolved Adaptive Guidelines source disclosure, and no claim that companions were installed or ran.
7. Remove disposable roots and compare closing porcelain with the opening snapshot plus planned QA artifacts and the pre-existing user/verifier files.

## Boundaries

No registry or GitHub fetch, optional companion installation, provider/browser call, product edit,
remote action, publication, or release. Jev advice is unavailable because this QA profile forbids
network access. A confirmed defect returns to an Implementer; independent safe paths may finish on
the same frozen snapshot.
