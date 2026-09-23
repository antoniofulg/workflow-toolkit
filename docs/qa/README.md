# QA operational profile

This repository distributes Workflow Toolkit skills, not a running application. Its public surfaces
are the installed agent-facing skill directories, optional migration helper, documentation, and
source metadata. No browser, HTTP API, mobile app, authentication flow, server, or production health
endpoint exists here.

## Public interfaces and area codes

| Area | Interface | Entry point | Authority |
| --- | --- | --- | --- |
| `SKL` | Skill installer and self-contained WTK skill directories | `.agents/skills/wtk*/SKILL.md` | [`package.json`](../../package.json); [README installation](../../README.md#install-the-skills) |
| `CFG` | Project-native agent routing, fixed workflow defaults, and Lean feature state | native agent files; `.agents/skills/wtk-lean/scripts/workflow_route.py`; `.specs/features/<feature>/workflow.json` | [`wtk-lean`](../../.agents/skills/wtk-lean/SKILL.md); [workflow route](../../.agents/skills/wtk-lean/scripts/workflow_route.py) |
| `QAS` | Agent-facing workflow, validation, review, QA, and closeout procedures | `.agents/skills/wtk*/`; Lean validators; close helper | [skills contract](../../README.md#the-workflow); [`wtk-lean`](../../.agents/skills/wtk-lean/SKILL.md); [`wtk-ship`](../../.agents/skills/wtk-ship/SKILL.md) |
| `DOC` | Workflow documentation and authorization boundaries | `README.md`; `docs/toolkit/` | [`README.md`](../../README.md); [workflow index](../toolkit/README.md) |
| `REL` | Source identity and skill membership | `package.json`; `bun.lock` | [`package.json`](../../package.json) |

Command facts remain in their executable manifests or CI authorities.

## Runner and adapter

- Adapter: skill-installer/manual through isolated temporary consumers plus an independent filesystem
  readback. The distribution tests copy only selected `.agents/skills/wtk*` directories; they are the
  existing pattern, not a separate QA framework.
- Migration path: from this checkout, run `node scripts/migrate.js --root <consumer>` in preview mode,
  then repeat with `--apply` only after the named actions are reviewed.
- Configuration path: keep model and effort metadata in the consuming project's native agent files.
  When a Lean feature needs a route snapshot, invoke
  `python3 .agents/skills/wtk-lean/scripts/workflow_route.py` and independently read back its
  provider and role identity. Deep Review is on demand, QA defaults to `auto`, and remediation
  halts after three consecutive stalls.
- Lean validation and closeout path: invoke the installed validators under
  `.agents/skills/wtk-lean/scripts/` and
  `python3 .agents/skills/wtk-ship/scripts/close_feature.py <feature> --promoted` only against
  disposable feature fixtures. Inspect agent routing and on-demand guidance as shipped; assigned
  technical-forward evidence may support discrimination that cannot be made deterministic through
  this repository's CLI.
- Optional companion paths: install Ponytail, security-lifecycle, adaptive-guidelines, Graphify, or
  Graft through their own installers when the consuming project chooses them. WTK tests the native
  fallback when those companions are absent.
- Gate authority: [`package.json`](../../package.json) declares Bun, Node, and Python suites.
  Automated suites prove technical contracts; they are not substitutes for the public-interface
  QA walk.

## Build, start, and health

- Build/start: none. The package ships source files and CLIs without a server build.
- Health signals: the installer exits with its documented result and an independent readback sees
  the expected managed tree; the route helper exits `0` and its JSON agrees with the reloaded
  snapshot; validators accept valid fixtures and reject the planned discriminator; closeout deletes
  only the named eligible feature.
- Isolation: every mutable probe uses a directory owned by this checkout. Never reuse another
  checkout's runtime or target.

## Authentication and test data

- Authentication/session setup: none.
- Fixtures or seed: disposable empty, adopted, conflicting, interrupted, and untouched skill consumers
  following `tests/skills/*.test.js`.
- Prompt-review fixture: one bounded read-only tree containing visible and hidden instruction files;
  record its path before the walk and verify its bytes and file set are unchanged afterward.
- Routing fixtures: byte-distinct native Claude, Codex, and Cursor agent files plus disposable
  `checks.md` fixtures for `light`, `standard`, and `ui`. Preserve every consumer-selected model
  and effort value during route creation and resume.
- Lifecycle fixtures: one disposable passing Lean feature and one unrelated pending feature with
  recorded foreign bytes. Close only the passing named feature; never use this repository's active
  feature directory as the target.
- Cleanup: remove only the disposable runner, package, consumer, and feature roots created for the
  QA run. Record their exact paths first.
- Residue check: final source `git status --short` equals the opening snapshot apart from planned
  durable QA report/status updates, and every recorded disposable path is absent.

## Evidence and limitations

- Raw evidence: `docs/qa/evidence/` (disposable and ignored).
- Durable reports and statuses: `docs/qa/reports/`, `docs/qa/scenarios/`, and immutable charters.
- The `workflow-toolkit` source package is private. Do not fetch a registry package, publish, push,
  open or merge a pull request, deploy, or mutate production during QA.
- Network access is not authorized during QA. Confirm selected WTK skills copy without editing project
  instructions or configuration; optional companion installation is outside this repository's QA.
- This workflow does not install a framework or invent commands. Use the source CLI or local packed
  package, existing PTY pattern, public Python CLIs, and filesystem readback.
- Agent-selection discrimination is partly instruction-visible and partly nondeterministic. Report
  instruction/path inspection and the assigned Technical Verification forward evidence separately;
  do not convert technical tests into a claimed user walk.

`wtk-qa-plan` uses this profile to select bounded charters. A non-author `wtk-qa-execute` Verifier records
the selected interface, exact path, evidence, limitations, and observed status. Product defects go
to an Implementer; QA does not fix them.

## Historical parallel-execution records

Parallel slice execution was removed by Workflow Toolkit Lean. Its durable reports, bugs, and
charters remain historical evidence only and are not current adapter instructions. The terminal
summary is [`2026-08-25-parallel-slice-executor-final`](reports/2026-08-25-parallel-slice-executor-final.md);
the last live safe retest is
[`2026-08-25-parallel-slice-executor-v060-safe-retest`](reports/2026-08-25-parallel-slice-executor-v060-safe-retest.md).
Retired scenario files retain earlier blocked, failed, and cleanup evidence; retirement does not
turn those outcomes into passes.
