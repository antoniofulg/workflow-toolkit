# QA operational profile

This repository distributes Workflow Toolkit, not a running application. Its public surfaces are
the guided adoption CLI, installed agent-facing files, local workflow configuration, documentation,
and package metadata. No browser, HTTP API, mobile app, authentication flow, server, or production
health endpoint exists here.

## Public interfaces and area codes

| Area | Interface | Entry point | Authority |
| --- | --- | --- | --- |
| `ADP` | Guided installer and generated consumer filesystem | `workflow-toolkit` package; `wtk install` executable | [`package.json`](../../package.json); [README quick start](../../README.md#quick-start); [`bin/wtk.js`](../../bin/wtk.js) |
| `CFG` | Workflow configuration, resolution, generated packets, and Lean feature state | `.wtk.toml.example`; checkout-local `.wtk.toml`; `workflow_config.py` | [`wtk-config`](../../.agents/skills/wtk-config/SKILL.md); [tracked example](../../.wtk.toml.example) |
| `QAS` | Agent-facing workflow, instruction audit, validation, review, QA, and closeout procedures | `.agents/skills/wtk*/`; `.agents/skills/prompt-review/SKILL.md`; provider packets; Lean validators; close helper | [skills contract](../../README.md#current-workflow); [`prompt-review`](../../.agents/skills/prompt-review/SKILL.md); [`wtk-lean`](../../.agents/skills/wtk-lean/SKILL.md); [`wtk-ship`](../../.agents/skills/wtk-ship/SKILL.md) |
| `DOC` | Workflow documentation and authorization boundaries | `README.md`; `docs/toolkit/` | [`README.md`](../../README.md); [workflow index](../toolkit/README.md) |
| `REL` | Package identity and membership | `package.json`; `bun.lock`; local package archive | [`package.json`](../../package.json) |

Command facts remain in their executable manifests or CI authorities.

## Runner and adapter

- Adapter: CLI/manual through public commands plus an independent filesystem readback. The Node
  installer tests use isolated temporary consumers and `/usr/bin/expect` for PTY input; they are the
  existing pattern, not a separate QA framework.
- Source CLI path for this checkout: from a checkout-owned disposable Git consumer, run
  `node /Users/antoniofulg/Projects/my-workflow/bin/wtk.js install`. This invokes the public
  executable directly without a registry lookup.
- Offline package path: create a local archive with
  `bun pm pack --filename <checkout-owned-pack-dir>/workflow-toolkit-1.1.0.tgz --ignore-scripts`,
  extract it into a separate checkout-owned runner, then run
  `node <runner>/package/bin/wtk.js install` from the disposable consumer. Record archive identity
  and package membership before execution.
- Configuration path: invoke
  `python3 .agents/skills/wtk-config/scripts/workflow_config.py` against a disposable consumer and
  reload its generated files through a separate process. The command contract lives in
  [`wtk-config`](../../.agents/skills/wtk-config/SKILL.md).
- Lean validation and closeout path: invoke the installed validators under
  `.agents/skills/wtk-lean/scripts/` and
  `python3 .agents/skills/wtk-ship/scripts/close_feature.py <feature> --promoted` only against
  disposable feature fixtures. Inspect agent routing and on-demand guidance as shipped; assigned
  technical-forward evidence may support discrimination that cannot be made deterministic through
  this repository's CLI.
- Prompt-review path: use the installed `.agents/skills/prompt-review/SKILL.md` through a bounded,
  read-only instruction-bundle audit. Inventory hidden instruction files, reload cited source lines
  independently, and record the observed findings or exact no-issue result plus coverage and
  exclusions. The skill has no standalone executable; keep this manual agent-facing observation
  separate from deterministic contract-test evidence.
- Gate authority: [`package.json`](../../package.json) declares Bun, Node, and Python suites.
  Automated suites prove technical contracts; they are not substitutes for the public-interface
  QA walk.

## Build, start, and health

- Build/start: none. The package ships source files and CLIs without a server build.
- Health signals: the installer exits with its documented result and an independent readback sees
  the expected managed tree; the resolver exits `0` and its JSON agrees with the reloaded snapshot;
  validators accept valid fixtures and reject the planned discriminator; closeout deletes only the
  named eligible feature.
- Isolation: every mutable probe uses a directory owned by this checkout. Never reuse another
  checkout's runtime or target.

## Authentication and test data

- Authentication/session setup: none.
- Fixtures or seed: disposable empty, adopted, re-adopted, conflicting, cancelled, and
  non-interactive Git consumers following `tests/installer/*.test.js`; use the existing PTY pattern
  in [`tests/installer/package.test.js`](../../tests/installer/package.test.js).
- Prompt-review fixture: one bounded read-only tree containing visible and hidden instruction files;
  record its path before the walk and verify its bytes and file set are unchanged afterward.
- Config fixtures: a copy of `.wtk.toml.example`, a byte-distinct consumer `.wtk.toml`, and
  disposable `checks.md` fixtures for `light`, `standard`, and `ui`. Preserve both source files and
  every consumer-selected value during re-adoption.
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
- The `workflow-toolkit` package is not published. Do not fetch a registry package, publish, push,
  open or merge a pull request, deploy, or mutate production during QA.
- Network access and external-skill installation are not authorized. Inspect the separately printed
  security command and confirm `security-spec`, `security-threat-model`, `security-implementation`,
  and `security-review` remain absent; do not execute
  `scripts/install_security_skills.py`.
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
