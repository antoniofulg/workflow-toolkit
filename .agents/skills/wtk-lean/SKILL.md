---
name: wtk-lean
description: 'Run spec-driven feature work through a reviewed plan, proof-backed checks, build, and independent verification. Use for `.specs/features/` work; not modular task lists or standalone design.'
license: CC-BY-4.0
metadata:
  author: Tech Leads Club - github.com/tech-leads-club
  version: '6.2.0'
---

# Tech Lead's Club - Spec, Lean

Run a decided feature through four moves: `PLAN → CHECKS → BUILD → VERIFY`. A human reviews the
feature shape before checks freeze its obligations; builders choose reversible implementation detail;
one fresh Verifier proves the complete feature. There is no task breakdown or component catalogue.

Before environment setup or handoff, apply [runtime lifecycle](../wtk/references/runtime-lifecycle.md)
to the checkout's application/test services.

For explicit reuse, construction-order or approval requirements, apply
[construction constraints](../wtk/references/construction-constraints.md) at Plan, Checks, Build
and Verify. At phase boundaries or context recovery, use
[context handoff](../wtk/references/context-handoff.md).

When implementing a selected image or design, freeze [the UI contract](../wtk/references/ui-ux.md)
before coding and carry its source and evidence requirements through build and independent verification.
Use the `ui` profile for binding interface sources.

At Plan, Checks, Build and Verify, apply
[project requirements](../wtk/references/project-requirements.md), including for checks-only
features. The phase references carry its entry points; profiles never waive inherited requirements.

## Core contract

1. Every check is one observable claim with a concrete value and a proof whose exit code settles it.
2. Tests come from the approved checks, never from the implementation. Never weaken or skip a
   test, or delete one, to make a red gate pass; redundant-test removal follows
   [pruning](../wtk/references/test-contract.md#pruning). A wrong or impossible check stops for user
   renegotiation.
3. Approved `checks.md` and `Test policy` rows are fixed. New `Landing`, `Relations`, and `Surface`
   rows may be added when building discovers a door, entity, or interface; approved rows are never
   rewritten. Keep `Flow` and `Impact` current when the path changes.
4. The coordinator dispatches one fresh Verifier over `<feature base>..HEAD` with every check in
   the same turn after the feature's last commit. The builder reports and stops; verification is
   never optional, delayed for another prompt, or self-authored.
5. The declared profile is a floor. Its report names the profile and `validate_verification.py` must
   exit 0. An approved spec authorizes local edits and commits only; push, deploy, and production
   data changes require explicit authorization.

## Profile

`AGENTS.md` or the feature snapshot declares the profile. The resolver defaults to `standard`;
`light`, `standard`, and `ui` remain valid upstream levels. The profile is a floor, not a preference,
and `checks.md` plus the verification report must name the same value.

```markdown
## wtk-lean

profile: standard
```

| Profile | Proof obligations |
| --- | --- |
| `light` | proofs at `HEAD`, named tests exist and ran, one located assertion per check, level/sampling gaps, and `Swept existing` re-read |
| `standard` | light plus recomputed `Coverage`, `Test policy` verdicts, and one fault per assertion surface |
| `ui` | standard plus binding-source comparison, per-screen enumeration proven by paired captures, and one structural guard per screen |

An empty input costs a recorded line, not a skipped step. `validate_verification.py` rejects a
profile mismatch and missing sections required by `standard` or `ui`. If the declared floor is too
thin, ask the user to raise it rather than silently changing the profile.

## Artifacts

```
.specs/
├── STATE.md                    # Handoff + default decision log when no project store exists
├── LESSONS.md                  # rendered by scripts/lessons.py - never hand-edit
├── lessons.json                # machine-owned
└── features/<feature>/
    ├── plan.md                 # problem, flow, impact, remaining shape, criteria, then audit tables
    ├── checks.md               # claims + proofs, the coverage join, test policy, swept
    └── verification.md         # the Verifier's report
```

Create each file when its phase produces content. For a change under roughly three files with no
one-way door, write only `checks.md` with `## Intent` and the native
[approval receipt](../wtk/references/construction-constraints.md#native-feature-approval). The
current request can authorize that bounded intent; create no synthetic plan or redundant approval stop.

The plan is the human review boundary. Write the problem, walk the surfaces, write criteria, then
record the shape that implements them. File order serves the reviewer: `Problem`, `Flow`, `Impact`,
`Relations`, `Surface`, `Landing`, `Criteria`, `Traceability`, `Out of scope`, `Assumptions`,
`Observable`, and `Sources`. `Flow` is the path, `Relations` the entities and one-way constraints,
`Surface` the interface/signature/outcomes, `Landing` the literal irreversible choices and rejected
alternatives, and `Impact` what existing terms or data change. Placement and reversible
implementation detail stay in the diff.

`checks.md` derives proof-backed checks from the plan and joins every enumerated interface, entity,
outcome, and door to a check. `plan.md`, `checks.md`, and `verification.md` therefore stay
distinct: the first freezes reviewed shape, the second freezes obligations, and the third is the
independent evidence. An unresolved architecture choice needs its own ADR/RFC/spike before it can
be recorded as a `Landing` decision.

## Phase references

- **Plan:** human review of EARS criteria, boundary, surfaces, eleven implicit dimensions, and the
  five shape sections. Ask only genuine decisions; use `n/a - <reason>` where a dimension does not
  apply. Full procedure and closure gate: [plan.md](references/plan.md).
- **Checks:** derive proof-backed claims, join every enumerated set member, and record swept
  landings: [checks.md](references/checks.md).
- **Build:** tests come from checks and implementation decomposition is yours. Keep new `Landing`, `Relations`, and `Surface` rows
  additive before closing code, then use the scope guardrail and handoff procedure:
  [build.md](references/build.md).
- **Verify:** dispatch per core contract 4; procedure and report schema:
  [verify.md](references/verify.md).
- **Memory:** decisions, handoff, and lessons live in [memory.md](references/memory.md).

## Scripts

Resolve `<skill-dir>` as the directory containing this `SKILL.md` and invoke
`python3 <skill-dir>/scripts/<name>.py`. Project data under `.specs/` stays relative to the
project root; pass `--root` when cwd differs. A non-zero exit stops the phase.

| When | Command |
| --- | --- |
| Before presenting the plan | `validate_plan.py <feature>` |
| Before starting to build | `validate_checks.py <feature>` |
| Before each commit | the project's commit validator, else `check_commit.py --message "<msg>"` |
| Before declaring done | `validate_verification.py <feature>` |
| At distillation | `lessons.py add ...` |
| After editing a validator or template | `selftest.py` |

The validators own structural detail: `validate_plan.py` checks reviewable shape before presentation;
`validate_checks.py` catches missing proofs, coverage, swept rows and profile.
`validate_verification.py` also requires, under `ui`, visual provenance and existing local captures.
Approval and image fidelity are judgments the independent Verifier owns. Run `selftest.py` after validator/template changes.
If execution is unavailable, inspect the same obligations and report the degraded path.

## Execution selection

Before delegated work, follow [agent selection](../wtk/references/agent-selection.md) for the
task-specific settings, overrides and host limits. Skills supply stage
responsibilities; native role files are optional and remain untouched. When a feature needs a
persisted route, freeze its selection:

```bash
python3 .agents/skills/wtk-lean/scripts/workflow_route.py \
  --root . --feature <feature-slug> --selection-file <selection.json>
```

The version 4 route records each stage's role and resolved model/effort, scoped to the
feature and current checkout. It derives the approved verification profile, keeps Deep Review on
demand and the Lean builder sequential.
Unchanged retries and resume reuse the selection through the same helper.

## Sub-agents and handoff

One builder owns all whole slices sequentially; do not estimate size, ask or offer a transfer. Ask
the user only when that builder actually hits a context limit: hand off to a fresh builder at the
next whole-slice boundary, or continue with accepted compaction. The coordinator uses the host's
supported handoff mechanism with the stage selection in the current checkout.

Handoffs occur only between slices and only after every proof in the batch is green. The outgoing
builder records closed checks, user decisions, and abandoned approaches. The next builder reads the
artifact and landed diff, not a narrative. Never split a slice or create a task DAG. The coordinator
owns checkpoint synchronization and the Verifier dispatch in core contract 4.

## Knowledge chain

Use existing code and conventions, project docs, current library docs through the project's selected
lookup tools, then web search; mark anything still uncertain. Never invent an API, flag, command, or behaviour.

## Output

Produce the artifact, lead with the verdict, and keep schema headings and identifiers unchanged.
For a concrete feature path, `.specs/features/lockfile-v2/plan.md` is reviewed before its checks;
the route then validates checks, builds, and dispatches the fresh full-range Verifier.
