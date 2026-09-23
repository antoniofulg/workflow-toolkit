# Skills-only Workflow Toolkit checks

Profile: standard
Plan: `.specs/features/skills-first-toolkit/plan.md`

9 checks in 3 slices · 2 one-way doors · 0 open blockers

## Checks

### S1 - Install WTK through skill installers

**C1** - Each published `wtk` and `wtk-*` skill has its referenced scripts, assets, and guideline content inside the distributed skill set (WTK-01, AC 1)
Proof: `node --test --test-name-pattern='published WTK skills resolve every local reference' tests/skills/distribution.test.js`

**C2** - Installing a published WTK skill into a project leaves `AGENTS.md`, `CLAUDE.md`, local config, provider packets, knowledge files, and ignore files byte-for-byte unchanged (WTK-01, AC 2)
Proof: `node --test --test-name-pattern='skill installation leaves project harness files untouched' tests/skills/distribution.test.js`

**C3** - Published WTK instructions use skill installers and the source package exposes no `wtk install` executable or new adoption manifest (WTK-01, AC 3)
Proof: `node --test --test-name-pattern='distribution has no npm install command or adoption manifest' tests/skills/distribution.test.js`

### S2 - Exit the old managed installation

**C4** - One-time cleanup preview lists old manifest-owned files, links, and managed instruction blocks without writing (WTK-02, AC 4)
Proof: `node --test --test-name-pattern='migration preview is complete and read only' tests/skills/migration.test.js`

**C5** - Cleanup backs up and removes only hash-verified old ownership, preserves surrounding project prose and unrelated files, removes old adoption state, and reports remaining unowned workflow prose (WTK-02, AC 5, 8)
Proof: `node --test --test-name-pattern='migration removes only verified ownership and reports manual review' tests/skills/migration.test.js`

**C6** - An edited managed block or file prevents all migration writes and identifies the conflict (WTK-02, AC 6)
Proof: `node --test --test-name-pattern='migration refuses modified owned content without writes' tests/skills/migration.test.js`

**C7** - A publication failure restores old files, links, modes, instruction bytes, and adoption state (WTK-02, AC 7)
Proof: `node --test --test-name-pattern='migration rollback restores exact prior state' tests/skills/migration.test.js`

### S3 - Run WTK alone and guide optional extensions

**C8** - A plan/build/review route resolves moved guidelines from skill references with Ponytail, security-lifecycle, Graphify, and Graft absent, and never claims they ran (WTK-03, AC 9, 10)
Proof: `node --test --test-name-pattern='WTK routes resolve references without optional companions' tests/skills/distribution.test.js`

**C9** - The README identifies skill installation, optional project-owned instruction text, and individually sourced companion recommendations, while existing phase schemas and verifier/delivery boundaries remain reachable (WTK-03, AC 11, 12)
Proof: `node --test --test-name-pattern='skills-only documentation and phase contracts remain reachable' tests/skills/distribution.test.js`

## Coverage

| Set (size) | Member -> proof | Unproven |
| --- | --- | --- |
| Distribution doors (2) | skill-installer-only C1, C2, C3 · one-time adopter exit C4, C5, C6, C7 | - |
| Project harness files (6) | `AGENTS.md` C2, C5 · `CLAUDE.md` C2, C5 · `.wtk.toml` C2 · provider packets C2 · knowledge files C2 · ignore files C2 | - |
| Old ownership classes (3) | managed instruction blocks C4-C7 · recorded files C4-C7 · recorded links C4-C7 | - |
| Migration outcomes (4) | preview C4 · success C5 · conflict C6 · rollback C7 | - |
| Optional companion classes (4) | Ponytail C8 · security-lifecycle C8 · Graphify C8 · Graft C8 | - |
| Preserved phase contracts (5) | Lean artifacts C9 · verifier separation C9 · scoped validation C9 · QA/review C9 · delivery authority C9 | - |

- C2 and C4-C7 cross their respective file-system boundaries using isolated target fixtures.
- C8 proves reference resolution and absence handling; C9 includes focused inspection of the phase contracts, not a copy snapshot.

## Swept

- validation: C1, C3 - distributed skill references and package entrypoints are checked
- failure modes: C6, C7 - conflict refusal and interrupted publication are checked
- idempotency: C5 - repeated cleanup must not recreate ownership; no second migration write after success
- authorization: C4, C5 - preview precedes explicit apply; no install-triggered cleanup
- concurrency: n/a - migration is an explicit single-checkout operation requiring a clean target
- data lifecycle: C5 - old manifest and temporary migration state are removed after success
- dependency failure: C8 - absent optional companion tools retain a native path
- state transitions: C4-C7 - old adoption moves through preview, apply, conflict, and rollback outcomes
- observability: C4, C6 - preview and conflict output identify affected paths

## Handoff

The `wc -c` scope estimate is below the declared 150k-token budget: package, installer, and installer tests = 228,703 bytes; guidelines, WTK skill entrypoints, and shared references = 241,814 bytes; README, toolkit human docs, and role templates = 115,509 bytes. The disjoint total is 586,026 bytes / 4 = about 146,507 tokens. This is a conservative read-size estimate, not projected changed lines. One builder owns S1-S3 sequentially; one fresh Verifier checks the complete feature after the last build commit.
