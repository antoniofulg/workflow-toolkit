# Project harness setup checks

Profile: standard
Plan: `.specs/features/project-harness-setup/plan.md`

## Intent

6 checks in 3 slices · 2 one-way doors · 0 open.

## Checks

### S1 - Harness discovery and project guidance

**C1** - Setup discovers existing policy and actual skill metadata, proposes a small baseline, interviews unresolved responsibilities across relevant areas, and distinguishes source conflicts and policy/expertise/proof gaps (SETUP-01, AC 1, AC 2, AC 3).
Proof: manual contract comparison against binding design AC-01 through AC-05, plus new-project scenario P1 and existing-project scenario P2 below.

**C2** - Authorized setup reuses project guideline owners or proposes `docs/guidelines/`, keeps root routing small, selects conditional guidance by role/phase/concern while preserving cross-cutting obligations, handles changed-input reruns, and leaves assessment-only project sentinels untouched (SETUP-01, AC 4, AC 5, AC 6, AC 7).
Proof: manual contract comparison against binding design AC-06 through AC-12 and Key decision 8, plus P1/P2 below.

### S2 - Requirement inheritance and independent checking

**C3** - Both planning paths read applicable driver guidance and land adopted requirements, use one fresh feature criteria reviewer with independent applicability discovery, block dependent work for blocking gaps, and retain proportional maintenance and handoff behavior (SETUP-02, AC 8, AC 9, AC 10, AC 14).
Proof: manual phase-integration inspection and omission scenario P3 below, against design AC-13 through AC-16 and AC-18.

**C4** - Loading criteria discriminate real pending/ready composition and both Verify paths independently catch omitted sources and violated outcomes, retain unproven obligations and return fixes to the builder (SETUP-02, AC 11, AC 12, AC 13).
Proof: manual phase-integration inspection and loading/security scenario P4 below, against design AC-17 and AC-19 through AC-24.

### S3 - Portable distribution

**C5** - The complete skill catalog, package manifest, tracked Claude alias, discovery output and installed references consistently include `wtk-setup` as the thirteenth skill without optional companions (SETUP-03, AC 15).
Proof: `node --test --test-name-pattern='full WTK set|approved execution selection|Skills CLI discovers|WTK routes resolve' tests/skills/distribution.test.js`

**C6** - Installation preserves existing harness files and the distribution contains no executable installer, mandatory native role files, policy registry or application runtime dependency (SETUP-03, AC 16).
Proof: `node --test --test-name-pattern='skill installation|distribution has|skills-only documentation' tests/skills/distribution.test.js`
Proof: manual diff inspection for no executable helper or dependency change.

## Scenario proofs

These are bounded forward exercises performed by the non-author checker using the delivered instructions, with scratch project artifacts isolated from both consuming applications. They support the exercised behavior only, not a general reliability claim. Pre-supplied scenario answers stand in for a user interview; record questions that would be asked and preserve the distinction between proposed and adopted requirements.

| Scenario | Given and attempt | Required observation |
| --- | --- | --- |
| P1 | A blank project, relevant frontend/backend/security concerns, available arbitrary specialist names, and a user-selected `engineering/rules/` guideline location | Propose the small baseline; ask unsettled policy/driver questions; map chosen skills to planning responsibilities; preserve the selected location; create only relevant documents when setup is authorized |
| P1R | P1 with a selected required driver unavailable and no approved replacement | Identify the affected planning responsibility, ask about the missing capability or alternative, and block dependent claims rather than silently substituting another skill |
| P2 | Existing guideline owners, an approved driver, an unsettled recovery policy, a renamed guideline and removed optional skill; request assessment, then describe an authorized rerun | Assessment changes no sentinels; ask about unsettled recovery without repeating settled choices; separate capability gaps; propose repaired/retired stale routes and preserve unaffected policy |
| P2U | P2 after responsibilities and policy are settled, rerun with unchanged inputs | Preserve adopted owners and decisions without duplicate rules, empty documents or repeated settled questions |
| P2C | P2 with conflicting instructions about delivery authority and no clear supersession | Cite both claims, identify the owning decision and record the unsettled authority gap; do not broaden delivery authority |
| P3 | A planner labels a tenant-data UI feature as frontend-only and omits the security guideline and an adopted criterion | Independently rediscover security and challenge the exclusion before build; surface the missing rule, classify the blocking authorization gap, and point to the native contract correction |
| P3F | A frontend-only feature with no backend, persistence or deployment change | Load the applicable UI and cross-cutting requirements while excluding unrelated backend/database procedures with a reason |
| P3B | A backend-only feature with no changed screen | Load its backend, architecture and security requirements while excluding unrelated appearance/motion guidance with a reason |
| P3S | A checks-only short-path feature, compared with a bounded correction under the existing maintenance route | Preserve applicable rule landings and fresh criteria review for the feature without manufacturing a full plan; preserve rule inheritance and proportional direct validation for maintenance without mandatory feature delegation |
| P4 | All listed proofs are green, but loading masks a known heading and unknown-value masks have wrong wrapping/geometry; authorization evidence is absent | Derive the original applicable policies independently; report the concrete loading mismatch and unproven security obligation; demand boundary-appropriate evidence and return fixes to the builder |

## Coverage

| Set (size) | Member -> proof | Unproven |
| --- | --- | --- |
| Plan criteria (16) | 1 C1 · 2 C1 · 3 C1 · 4 C2 · 5 C2 · 6 C2 · 7 C2 · 8 C3 · 9 C3 · 10 C3 · 11 C4 · 12 C4 · 13 C4 · 14 C3 · 15 C5 · 16 C6 | - |
| New skill integration (4) | router C5 · package manifest C5 · tracked Claude alias C5 · public install/discovery C5 | - |
| Planning/verification paths (4) | Lean planning C3 · modular planning C3 · Lean verification C4 · modular verification C4 | - |
| Conversational dispositions (3) | proposed C1 · unresolved C1 · applied C2 | - |
| Forward scenarios (10) | P1 C1/C2 · P1R C1 · P2 C1/C2 · P2U C2 · P2C C1 · P3 C3 · P3F C2/C3 · P3B C2/C3 · P3S C3 · P4 C4 | - |

No check asserts production application behavior. C1 through C4 require semantic source inspection and the named bounded exercises; package tests alone cannot settle them.

## Test policy

Existing test contract covers instruction products through routing, metadata, resolvable references and safety boundaries, with semantic inspection for instruction behavior. Extend the canonical distribution catalog expectations for 13 skills; preserve all existing assertions and installation sentinels. No new prose-matching suite, runtime dependency or executable helper is required.

## Swept

- validation: C1, C5
- failure modes: C1, C4
- idempotency: C2
- authorization: C1, C2, C6
- concurrency: n/a - no concurrent runtime or writer introduced; one sequential builder
- data lifecycle: C2 for stale guidance and C6 for installation preservation; no application data
- dependency failure: C1, C2
- state transitions: C1, C2, C3, C4
- observability: C1, C4 for honest outcomes/evidence gaps; no runtime telemetry introduced

## Handoff

- Phase: Build implemented; ready for the coordinator's fresh full-feature Verifier. The builder has not written a verification report.
- Contract: binding `.design/project-harness-setup.md`; folder policy follows existing project convention, with `docs/guidelines/` proposed only when absent.
- Approval: Antonio approved the design and asked to proceed; one fresh criteria reviewer is the default. Antonio confirmed: "Use inherited settings for all three stages" for criteria review, implementation and verification.
- Scope: one instruction-only skill, conditional shared references and phase integration, manifest/alias/README registration, and canonical distribution expectation updates. No application/runtime changes or remote delivery authorized.
- Size: `python3` file-size sum over the 11 likely touched existing inputs produced 136426 bytes / 4 = 34106 estimated context tokens, plus new instruction content. This is a planning context estimate, not measured consumption; below the 200k project budget, so one sequential builder.
- Checkout: `/Users/antoniofulg/Projects/my-workflow`, branch `docs/project-harness-discovery`, feature base `013864d`.
- Validation baseline: owning distribution suite passed all seven tests before implementation; no template or validator changes planned.
- Criteria review: the coordinator reports that the fresh reviewer accepted the targeted corrections for explicit role/phase/concern selection and the missing forward-probe variants before builder dispatch.
- Shared owner: `wtk/references/project-requirements.md` owns discovery, native landings, fresh criteria review, recovery, independent verification and conditional content-shaped loading. Setup owns the interview; existing security, construction, validation and review procedures remain linked owners. Lean Plan/Checks/Build and modular Plan/Extract/Build plus both Verify paths point to the shared procedure under every profile.
- Changes: added instruction-only `wtk-setup` and its interview reference; registered router, README catalog/install/update counts, package files and tracked Claude alias. Updated only existing distribution expectations from twelve to thirteen skills (and locked discovery from nine to ten), preserving every assertion and sentinel. No executable helper, runtime dependency, native role file, registry or root `AGENTS.md` change.
- Author inspection: `rtk cat .agents/skills/wtk-setup/SKILL.md .agents/skills/wtk-setup/references/interview.md .agents/skills/wtk/references/project-requirements.md` plus `rtk git diff --cached` were compared with the binding design and criteria. C1/C2 are covered in Discover/Interview/Propose and the area menu; C3/C4 in the shared owner and native phase entry points. This is source inspection, not an independent behavioral proof or a production application claim.
- C5/C6 automated evidence: `rtk proxy node --test tests/skills/distribution.test.js` exited 0, seven tests passed, zero failed/skipped, latest reported duration 424.917166 ms. It covers both named selector sets in one canonical invocation; paths/manifest/alias flow into isolated skill discovery, portable references and harness-preservation sentinels. The earlier run passed in 1045.091666 ms; the final run followed the setup authority-wording clarification because the suite reads skill content.
- Metadata: the existing `writing-skills/scripts/validate-metadata.py` helper passed for the exact `wtk-setup` name/description read from its frontmatter. No configured formatter was found in package scripts or repository formatter/config files; none was installed.
- Structure: `rtk proxy python3 .agents/skills/wtk-lean/scripts/validate_plan.py project-harness-setup` exited 0 (zero errors, one warning about standard-profile binding sources); `rtk proxy python3 .agents/skills/wtk-lean/scripts/validate_checks.py project-harness-setup` exited 0 (zero errors, five warnings for the approved manual proofs). These warnings do not prove semantic coverage; C1-C4 explicitly require the fresh checker to inspect the binding design at this profile.
- Commit preparation: `rtk git diff --cached --summary` and `rtk git diff --cached -- package.json tests/skills/distribution.test.js .claude/skills/wtk-setup` confirm the declared file-only registration, unchanged dependencies and preserved assertions; `rtk git diff --cached --check` exited 0; `rtk proxy python3 .agents/skills/wtk-lean/scripts/check_commit.py --message 'feat(wtk): add project harness setup and requirement inheritance'` exited 0 (`check_commit: OK`).
- Closed builder obligations: complete approved instruction implementation and canonical C5/C6 package evidence. Pending: fresh non-author semantic inspection and all P1/P1R/P2/P2U/P2C/P3/P3F/P3B/P3S/P4 probes for C1-C4, independent reconciliation of all six checks, and the coordinator's verification artifact/gate. No skipped or weakened criterion.
- Settled mid-build: no new product decisions; clarified that setup must not infer/expand delivery authority and may record explicitly authorized policy decisions. Abandoned: no alternate implementation or helper was needed.
- Next action: coordinator dispatches the accepted fresh Verifier over `013864d..HEAD`, original request, authoritative routing, binding design, plan and all checks. Retain valid unchanged evidence and return any findings to the builder under the existing remediation policy. Remote delivery remains unauthorized.
