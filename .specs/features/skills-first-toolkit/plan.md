# Skills-only Workflow Toolkit — Proposed plan

## Problem

Workflow Toolkit currently installs more than workflow skills: it manages blocks in a consuming project's `AGENTS.md` and `CLAUDE.md`, publishes standalone guidelines and knowledge scaffolding, generates provider packets, and bundles companion skills. Editing a managed instruction block causes a conflict on the next update. The npm installer also makes toolkit updates a separate process from the skill installers a project already uses.

The requested outcome is one self-contained set of `wtk` and `wtk-*` skills distributed through users' skill installers. Each project owns its agent instructions and chooses complementary tools. No measured adoption or context-cost data was supplied; the changed distribution contract and a safe exit for existing adopters are the observable goals.

## Flow

Reuse the existing `wtk` router, phase skills, and their owned scripts; use the consumer's skill installer for installation and updates.

1. An existing adopter first runs an explicit one-time migration helper from the source checkout. It previews old manifest-owned files and instruction blocks, backs up exact bytes, removes only verified toolkit-owned content, and flags any unowned legacy prose for project review.
2. A user installs the complete 13-skill WTK set through a supported skill installer; the installer places those directories in its own scope. Migration runs before a project-local skill update so it cannot delete newly installed skills.
3. `wtk` (exists) routes an invoked task to its phase skill and skill-local references without consulting installed `docs/toolkit/guidelines/` or requiring companion skills.
4. `README.md` (exists) explains skill installation, an optional project-owned instruction snippet, and individually chosen companion skills and code-intelligence tools.

## Impact

| Front | What changes |
| --- | --- |
| Distribution | Users' skill installers become the only WTK installation and update path. The supported installation unit is the complete 13-skill WTK set. Retire the published `workflow-toolkit` npm installer, `wtk install`, module selection, adoption manifests for new installs, and installer-created Claude aliases. |
| Instructions | WTK no longer creates or updates project `AGENTS.md` or `CLAUDE.md`. The source repository retains its own maintainer instructions; the README offers optional text a project can adopt and own. |
| Skill references | Operational guidelines move to the narrowest owning `wtk-*` skill reference; shared rules have one canonical home and links are updated together. Human-facing explanations stay in the source README or toolkit docs. |
| Optional capabilities | Stop bundling or mandating Ponytail, security-lifecycle, adaptive-guidelines, prompt-review, Graphify, and Graft. Document them as choices with a specific use case and verified source. CodeGraph remains a candidate until its identity and value are established. |
| Configuration | `wtk-config` stays an invocable skill, but base WTK no longer writes `.wtk.toml`, provider packets, or checkout ignore rules. Host-specific role setup is a separate explicit action. |
| Existing adopters | Provide a one-time, explicit cleanup path before project-local skill installation. Do not migrate unrelated consumer files or silently discard modified owned content. A prior fresh install may have seeded untracked workflow prose in `AGENTS.md`; flag it for manual review. |
| Decisions | Supersede the affected parts of AD-001, AD-010, AD-033, and AD-036 when the new contract is approved; update `.specs/AD-INDEX.md` in that decision commit. |

### Keep, change, remove

| Keep as behavior | Change | Remove |
| --- | --- | --- |
| `wtk` routing and distinct `wtk-*` phase skills | Place conditional guidelines in skill `references/` | Managed host instruction blocks and adoption templates |
| Lean `plan.md` → `checks.md` → build → independent verification | Make provider setup an explicit `wtk-config` action | Automatic local config and 18 provider packets |
| Acceptance, evidence, QA, review, security-boundary, and delivery contracts | Use native inspection when optional graph tools are absent | Mandatory Ponytail activation and bundled non-WTK skills |
| Public WTK skill names and skill-local scripts | Document supported skill installers and installation scopes | npm installer CLI, its `core`/`quality`/`extras` catalog, and normal-install adoption manifest |
| Source-repository human docs and maintainer instructions | Rewrite README around an opt-in harness | Installed `docs/toolkit/`, product/knowledge starter files, ignore-file edits, and installer output suggesting tool setup |

### Guideline destination

| Current guideline | Planned owner |
| --- | --- |
| `SECURITY.md` | Small WTK security-boundary reference needed for baseline planning and validation; deeper audit and hardening procedures stay in optional security-lifecycle skills. |
| `UI-UX.md`, `FRONTEND.md`, `MODELING.md` | Shared `wtk/references/` files, loaded by the relevant plan, build, design, or verification route. |
| `DX.md` | `wtk-plan/references/` public-surface planning guidance. |
| `QA-SCENARIOS.md` | `wtk-qa/references/` shared by QA planning and execution. |
| `QA-EXECUTION.md` | `wtk-qa-execute/references/`; merge any duplicate procedure into its owning skill. |
| `REVIEW-ROUNDS.md` | Shared `wtk/references/` rule used by review and remediation routes. |
| `WORKFLOW-MEMORY.md` | Merge non-duplicate rules into `wtk-lean/references/memory.md`. |
| `KNOWLEDGE-WIKI.md` | `wtk-knowledge-check/references/`, loaded only for a project that uses the knowledge bundle. |
| `CONTEXT-BUDGET.md` | Source-repository maintainer guidance, excluded from consumer skill payloads. |

Update skill, script, test, role-template, and human-doc links before deleting old guideline copies. Keep human-facing explanations in the README or source-repository docs, outside installed runtime rules.

## Relations

New installations have no WTK adoption manifest. The current `.my-workflow/adoption.json` schema is input only to an explicit one-time cleanup helper for existing adopters. That helper does not create a successor ownership record. No product data model changes.

## Surface

None - nothing consumed outside remains as a WTK CLI or application HTTP route. The published npm command `npx workflow-toolkit install` is removed. WTK's public entrypoints are its `SKILL.md` files and documented skill-installer source paths. The one-time cleanup helper is explicit and separate from installing skills; its preview and apply modes must name every file it would alter.

## Landing

| One-way door | Literal shape | Alternative rejected |
| --- | --- | --- |
| Distribution boundary | Publish the complete 13-skill `wtk`/`wtk-*` set as one supported installation unit; skill installers own placement and updates. No WTK npm install command or normal-install manifest. | Individually installable phase subsets would require a maintained dependency graph and extra distribution proofs. |
| Existing-adopter exit | Explicit one-time cleanup uses old recorded hashes to remove only exact toolkit blocks and pristine obsolete files, with preview and backup; remaining unowned prose is reported for manual review. | Dropping the installer without cleanup guidance would leave stale mandatory instructions in adopted projects. |

## Criteria

### S1: A new project gets WTK through a skill installer (P1)

The project installs the complete WTK set without taking on a managed harness.

**Acceptance Criteria**

1. WHEN a supported skill installer installs the complete 13-skill WTK set THEN every runtime reference SHALL resolve within the installed set, including required scripts and assets, with no dependency on the source checkout's `docs/toolkit/guidelines/`.
2. WHEN a project installs or updates WTK skills THEN WTK-provided installation material SHALL neither create nor edit `AGENTS.md`, `CLAUDE.md`, local provider config, generated agent packets, product/knowledge scaffolding, or ignore files.
3. WHEN WTK is distributed THEN its published install instructions SHALL use skill installers, and the source package SHALL define no `wtk install` executable or promise an adoption manifest.

**Independent test:** Install all 13 published WTK skill directories into an isolated project through the documented skill-installer route; inventory files, resolve every runtime reference, and compare existing project instructions byte-for-byte.

### S2: Existing adopters can leave the old managed install safely (P1)

A project with the current manifest can remove the old toolkit ownership before continuing with its skill installer.

**Acceptance Criteria**

4. WHEN the one-time cleanup previews a current adoption THEN it SHALL list each exact managed instruction block, old toolkit-owned file, and link proposed for removal without changing the target.
5. WHEN cleanup applies to pristine recorded blocks and files THEN it SHALL back up their bytes and modes, remove only verified toolkit-owned content, preserve surrounding project prose, and leave unrelated project files unchanged.
6. IF an instruction block or old toolkit-owned file differs from its recorded hash THEN cleanup SHALL report the path and make no target changes until the project resolves that conflict.
7. IF cleanup fails after publication begins THEN it SHALL restore the previous files, links, instruction bytes, and old adoption state from its backup.
8. WHEN cleanup succeeds THEN it SHALL remove the old adoption manifest and temporary migration state rather than create a new WTK ownership manifest; it SHALL report any remaining unowned workflow prose in `AGENTS.md` for project review.

**Independent test:** Use pristine, edited, and interrupted old-install fixtures; compare all bytes, modes, links, and manifest state before and after preview, success, refusal, and rollback.

### S3: WTK remains usable alone and documents optional extensions (P2)

An agent can invoke the same workflow with only WTK installed; a human can choose extra harness tools from documented guidance.

**Acceptance Criteria**

9. WHEN a WTK route invokes a conditional rule THEN the installed skill SHALL resolve it from a skill-local reference.
10. WHEN Ponytail, security-lifecycle, Graphify, or Graft is absent THEN the relevant WTK route SHALL remain usable through its documented native path and SHALL not claim that optional tooling ran.
11. WHEN a reader opens the README THEN it SHALL distinguish WTK skills, optional project-owned instruction text, and individually recommended companion skills/tools with their verified source and use case.
12. WHEN a WTK phase runs after the reference move THEN its Lean artifacts, independent verifier boundary, scoped validation, QA/review rules, baseline security checks, and authorized delivery behavior SHALL retain their current contracts.

**Independent test:** Resolve every distributed skill reference, exercise representative plan/build/review routes without companion tools, and inspect the README and released skill inventory.

## Traceability

| ID | Slice | Criteria | Status |
| --- | --- | --- | --- |
| WTK-01 | S1 | 1, 2, 3 | Pending |
| WTK-02 | S2 | 4, 5, 6, 7, 8 | Pending |
| WTK-03 | S3 | 9, 10, 11, 12 | Pending |

## Out of scope

| Excluded | Why |
| --- | --- |
| Installing or benchmarking a CodeGraph project | Its exact upstream identity and suitability are not established. |
| Installing recommended third-party skills or graph tools in a consumer project | Each project chooses its harness. |
| Changing Lean artifact schemas or the feature/verification lifecycle | This is a distribution and reference-ownership change. |
| Migrating another product repository | Each consuming project must review its own instruction and tool choices. |

## Assumptions

| Assumption | Chosen default | Rationale | Confirmed? |
| --- | --- | --- | --- |
| Distribution path | Use skill installers only; remove `npx workflow-toolkit install`. | User selected this path explicitly. | y |
| Installation unit | Require the complete 13-skill WTK set; do not promise individually installable phase subsets. | User chose the full-set option after verification exposed cross-skill references. | y |
| Existing-adopter cleanup | Ship an explicit, one-time helper in the source repository; run it before project-local skill installation and never as part of skill installation. | Old managed instructions need a safe exit without giving new installs ownership of host files. | n |
| Optional recommendations | Identify the exact CodeGraph and adaptive-guidelines projects before adding install commands. | Similar names may refer to different upstreams. | n |

**Open questions:** none block this proposed plan; the defaults above are review decisions.

## Observable

| Surface | Decision | Landing |
| --- | --- | --- |
| Skill installation | Self-contained full 13-skill set and untouched host instructions | AC 1, 2 |
| Distribution docs | Skill-installer routes and removed npm command | AC 3, 11 |
| One-time cleanup | Preview and conflict refusal | AC 4, 6 |
| One-time cleanup | Verified deletion, backup, and rollback | AC 5, 7, 8 |
| Skill invocation | Missing optional companion | AC 10 |

## Sources

- User's explicit selections in this conversation: use skill installers only and install all 13 WTK skills together.
- `scripts/installer/engine.js` and `package.json`: current managed-file and npm distribution boundaries.
- `.specs/AD-INDEX.md`: active decisions this change must reconcile.
