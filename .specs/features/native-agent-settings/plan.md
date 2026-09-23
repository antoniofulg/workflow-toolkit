# Project-owned agent settings — Proposed plan

## Problem

Workflow Toolkit still requires a checkout-local `.wtk.toml` even though its skills-only installation leaves project configuration to the consumer. That file contains a complete model and effort matrix for Claude, Codex, and Cursor, plus review, QA, routing, and remediation settings. The `wtk-config` skill renders 18 provider packets and snapshots model/effort values, so a project must maintain WTK-specific configuration alongside its native agent files. The source checkout also tracks two identical examples. The user has explicitly chosen to remove `.wtk.toml` and `wtk-config`, let each project set model and effort natively, and use three stall attempts by default.

No measured configuration failure rate was supplied. Success is observable through file ownership, TOML-free phase execution, unchanged project-native agent files, and the fixed remediation default.

## Flow

Reuse the existing WTK phase skills, Lean artifacts, independent verifier boundary, and project-native agent definitions.

1. A project installs the complete WTK skill set minus `wtk-config` through its skill installer; the project creates and edits its native agent definitions, including model and effort.
2. `wtk-lean` (exists) records a minimal feature route snapshot from the active host/provider and role identities when a snapshot is needed. It does not read `.wtk.toml`, generate agent files, or persist model/effort.
3. The host dispatches roles using the project's native definitions. WTK checks role availability and author/verifier separation, without rewriting those definitions.
4. Deep Review remains explicitly invoked unless requested by the feature; the Lean builder remains sequential. QA uses its existing auto adapter route unless the project supplies an explicit task-scoped choice. Remediation uses a default stall threshold of `3`.
5. The old-adoption cleanup helper continues to recognize hash-verified historical generated packets after WTK's provider templates are removed.

## Impact

| Front | What changes |
| --- | --- |
| Installed skills | Remove `wtk-config`; the complete supported WTK set changes from 13 to 12. Relocate its still-used decision-index and repository-intelligence helpers to the owning WTK skills. |
| Host configuration | Remove local `.wtk.toml`, root `.wtk.toml.example`, bundled example, provider template assets, packet rendering/synchronization, and WTK model/effort validation. Native project agent files become the sole model/effort source. |
| Feature state | Keep a small `workflow.json` route snapshot when the feature uses one, containing provider/role identity and other required handoff state, but no `model` or `effort` fields or WTK config version. Do not read old config snapshots through compatibility paths. |
| Defaults | Deep Review `skip` unless invoked; sequential Lean builder; QA adapter `auto` absent a task-scoped project choice; remediation `stall_attempts = 3`. Remove TOML profiles and other TOML-only overrides. |
| Existing adopters | `scripts/migrate.js` keeps its verified cleanup behavior without consulting removed provider templates. Consumer-owned old `.wtk.toml` files are not deleted by migration. |
| Documentation and decisions | Update AGENTS, README, skill references, current QA scenarios, tests, package inventory, and active decision index. Supersede AD-010 and AD-038 plus the affected configuration terms of AD-036/AD-041. Historical reports remain historical. |

## Relations

The project-native agent files remain consumer-owned. The feature-local `workflow.json` remains transient WTK state, but its new shape stores only route identity needed for handoff and verification, never model or effort. No application data schema changes.

## Surface

None - no application HTTP route changes. The public WTK skill catalog loses `wtk-config`; WTK no longer exposes `.wtk.toml`, its examples, `--sync-agents`, or the provider model/effort matrix as supported configuration. Current feature routes use the active host's native agent definitions and default behavior named in Flow.

## Landing

| One-way door | Literal shape | Alternative rejected |
| --- | --- | --- |
| Ownership boundary | No WTK TOML file or generated provider packets; each consuming project owns its native model/effort declarations. | Retaining a reduced WTK TOML would preserve a second configuration surface and the original source-of-truth conflict. |
| Public skill set | Complete supported installation is the 12 remaining `wtk`/`wtk-*` skills; retained `wtk-config` helpers move to their owning skills. | Keeping an empty configuration skill would add a routing step without an editable WTK configuration contract. |
| Remediation default | Three consecutive non-progress attempts is the default and is reported as `3`; no TOML override. | Reading a hidden or fallback config would make the threshold depend on a file the product says it no longer owns. |

## Criteria

### S1: A project owns its agent models and effort (P1)

Installing WTK gives the host skills, while the project controls native role metadata.

**Acceptance Criteria**

1. WHEN a supported skill installer lists this repository THEN it SHALL find exactly the 12 published WTK skills and no `wtk-config` skill.
2. WHEN WTK runs in a project with no `.wtk.toml` or WTK example THEN its supported planning, build, verification, QA, review, and ship routes SHALL not create or require either file.
3. WHEN a project has native Claude, Codex, or Cursor agent definitions THEN WTK SHALL leave their model and effort metadata byte-for-byte unchanged during its supported routes.
4. WHEN this source checkout is cleaned THEN its ignored root `.wtk.toml` SHALL be absent and its existing native agent definitions SHALL retain their model/effort metadata.
5. WHEN a feature route is recorded THEN its `workflow.json` SHALL contain provider/role identity needed for handoff and no WTK `model` or `effort` fields.

**Independent test:** Install the 12-skill set in an isolated project with byte-distinct native role files and no WTK TOML; walk route creation/resume and compare the full host-file inventory.

### S2: Fixed defaults replace the removed configuration (P1)

The workflow remains usable without recreating a hidden configuration channel.

**Acceptance Criteria**

6. WHEN remediation starts without an explicit internal threshold THEN WTK SHALL use and report `stall_attempts = 3` and halt after the third consecutive non-progress attempt.
7. WHEN a feature has no explicit review request THEN WTK SHALL schedule zero automatic Deep Review groups while leaving direct `wtk-deep-review` invocation usable.
8. WHEN QA has no task-scoped adapter choice THEN it SHALL use the existing `auto` adapter route and preserve its safe fallback rules.
9. WHEN an old adoption contains hash-verified generated provider packets THEN migration preview and apply SHALL still list and remove those packets without removed template assets, while preserving modified or consumer-owned files.

**Independent test:** Exercise the remediation sequence at attempts 1–3, the no-review and explicit-review routes, default QA adapter, and migration against exact old packet fixtures.

### S3: Current guidance and proofs match the skills-only boundary (P2)

The repository and consuming projects can understand the new setup without stale instructions.

**Acceptance Criteria**

10. WHEN a reader opens current README, AGENTS, skill, and QA instructions THEN they SHALL identify project-native agent files as the model/effort source and state the defaults without a `.wtk.toml` setup step.
11. WHEN the source package and supported skill tree are inspected THEN neither SHALL contain WTK TOML examples, provider packet templates, or packet-generation entrypoints.
12. WHEN a new project installs the documented full WTK set THEN its source references SHALL resolve after helper relocation, and no source-only file shall be required at runtime.

**Independent test:** Resolve links from an isolated 12-skill installation, inspect package inventory and current QA scenario commands, and run the canonical affected suites.

## Traceability

| ID | Slice | Criteria | Status |
| --- | --- | --- | --- |
| WTKCFG-01 | S1 | 1, 2, 3, 4, 5 | Pending |
| WTKCFG-02 | S2 | 6, 7, 8, 9 | Pending |
| WTKCFG-03 | S3 | 10, 11, 12 | Pending |

## Out of scope

| Excluded | Why |
| --- | --- |
| Automatically editing a consumer's native agent files | The user assigned model/effort ownership to each project. |
| Migrating consumer-authored `.wtk.toml` values into native agent metadata | WTK cannot infer each host's desired model and effort; current files remain consumer-owned for manual reference. |
| Changing Lean plan/check/verification schemas or author/verifier separation | Configuration removal does not alter the feature quality contract. |
| Deleting historical QA reports or past decision bodies | They record what earlier releases did. |

## Assumptions

| Assumption | Chosen default | Rationale | Confirmed? |
| --- | --- | --- | --- |
| TOML removal | Remove `.wtk.toml` entirely, including examples. | User explicitly selected this. | y |
| Skill removal | Remove `wtk-config` and relocate needed helpers. | User explicitly selected this. | y |
| Native metadata | WTK neither writes nor freezes model/effort; projects set them in host-native agent definitions. | User explicitly selected project ownership. | y |
| Other former TOML choices | Deep Review on demand, sequential builder, QA auto unless task-scoped choice, remediation default 3. | These are existing defaults and avoid a replacement configuration file. | n |

**Open questions:** none block this proposed plan; the unconfirmed default row is reviewable.

## Observable

| Surface | Decision | Landing |
| --- | --- | --- |
| Skill installer | 12 skills, no config skill or examples | AC 1, 11, 12 |
| Native agent files | No WTK writes to model/effort; source local TOML removed | AC 2, 3, 4 |
| Feature route snapshot | Provider/role identity, no model/effort | AC 5 |
| Remediation | Three-attempt default and halt | AC 6 |
| Review and QA | On-demand review and auto QA fallback | AC 7, 8 |
| Legacy migration | Old packet cleanup without templates | AC 9 |
| Current docs | No TOML setup instruction | AC 10 |

## Sources

- User's explicit instructions in this conversation: remove provider model/effort setup, make projects own it, default stall attempts to 3, remove `.wtk.toml` and `wtk-config`.
- `.agents/skills/wtk-config/scripts/workflow_config.py` and `packets.js`: current configuration and packet ownership.
- `.specs/AD-INDEX.md`: active decisions affected by this removal.
