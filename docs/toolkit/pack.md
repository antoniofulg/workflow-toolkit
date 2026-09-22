# Skills, knowledge, adopt

## Skills

The workflow ships twenty local capabilities:

| Skill | Role |
| --- | --- |
| `wtk` | Router. Sizing, phase chain, `.specs` layout, resume. |
| `wtk-discover` | Discovery for unresolved product or architecture choices. |
| `wtk-plan` | Modular planning: slices, observable criteria, and source-grounded decisions. |
| `wtk-implement` | Modular execution: proof-backed checks, gate, and atomic commit. |
| `wtk-lean` | Integrated Lean plan, checks, build, and independent feature verification. |
| `wtk-config` | Resolves provider routes, profiles, and feature snapshots. |
| `wtk-knowledge-check` | Validates the consuming knowledge bundle when present. |
| `wtk-deep-review` | Review phase: deep review of branch diffs, working trees, or PRs. |
| `wtk-qa` | QA phase: run user-visible QA plans or walks over tagged journeys. |
| `wtk-qa-plan` | Maps changed user-visible promises to durable QA journeys and charters. |
| `wtk-qa-execute` | Walks those journeys through the consuming project's existing adapter. |
| `ponytail` (`full`) | Shortest code that works. Stdlib before a dependency. |
| `prompt-review` | Audits instruction bundles for scope, overlap, loading, and authorization clarity. |
| `wtk-ship` | Unattended run: classify work; credential-free configuration stays local, while eligible work may deliver one feature branch through one pull request. |
| `security-audit-coordinator` | Coordinates explicit whole-codebase audits with coverage and independent verification. |
| `security-spec` | Defines security requirements and negative tests during Specify. |
| `security-threat-model` | Models repository-grounded threats and trust boundaries. |
| `security-implementation` | Implements secure defaults and requested hardening. |
| `security-pentest` | Tests authorized running web apps and APIs for reproducible vulnerabilities. |
| `security-review` | Reviews bounded diffs or code slices for confirmed vulnerabilities. |

Canonical copies: `.agents/skills/`. Claude: symlinks in `.claude/skills/`. Cursor / Codex /
OpenCode consume `.agents`. Do not add `.cursor/skills`.

Five security skills are bundled reviewed capabilities. Their `skills-lock.json` entries pin
the upstream source, canonical path, commit, CLI version (`1.5.23`), and full-tree hash. Adoption
installs the packaged trees through core without resolving `latest` or contacting the network.
The sixth, `security-pentest`, is original Apache-2.0 work with its own provenance notice.

Planner / implementer / explorer / verifier / designer are five windows. Canonical packet bodies live in
`.agents/skills/wtk-config/assets/agents/{cursor,claude,codex}/`; sync generates ignored runtime files in
`.cursor/agents/`, `.claude/agents/`, and `.codex/agents/`. Spawn models live on those generated
files. `CLAUDE.md` is `@AGENTS.md`. Explorer is read-only and handles product-tree searches and
flow traces for the parent agent.

`wtk-ship` readiness still needs: full gate 0 on the final tree, no Critical, Major, or Minor left,
`main` not moved underneath, and flagged scenarios terminal (`untested` blocks; `blocked-verify` does not).
Invoking `wtk-ship` authorizes the feature-branch push, one pull request, and merge after readiness
is rechecked. Readiness is evidence, not authorization for deploy/release, production mutations,
force-push, direct push to `main`, or unrelated remote actions; those require explicit instruction.

## Knowledge bundle

Empty on purpose. Machinery only: operating schema, `raw/` README, stub indexes, checker.

| Piece | Job |
| --- | --- |
| `knowledge/AGENTS.md` | OKF v0.2 schema (frontmatter, ingest, harvest, lint) |
| `knowledge/wiki/` | Concepts, when the consuming project earns them |
| `knowledge/raw/` | Immutable originals. Privacy surface — committed, so strip personal data |
| `bun run knowledge` | Conformance, drift, gaps. Run when writing to the bundle, not as the product gate |

## Guided installation

The package `workflow-toolkit@1.0.0` exposes the single canonical command:

```bash
npx workflow-toolkit install
```

The wizard targets the current directory, requires Node.js 18 or newer and an interactive
terminal, and never requires Python. It selects `core`, `quality`, or `extras` (with
`core` automatically included for every non-core selection), previews every action, and requires
an explicit conflict choice before publication. Replaced or removed files are verified in
`.my-workflow/backups/<UTC timestamp>/`; the adoption manifest publishes last. Cancellation writes
nothing. A successful knowledge-bearing replacement creates a pending `knowledge-transfer.md`
checklist; consumer content is never semantically merged.

The installer catalog includes the operating loop, Bun-native knowledge tooling, assisted slice
execution, review/QA skills, optional Ponytail utilities, and prompt-review. Existing consumer prose and knowledge
remain owned by the consuming project. An interrupted publication leaves a transaction journal;
the next run offers restoration before a new plan.

Fresh consumers receive generic managed knowledge instructions and neutral consumer-owned wiki
indexes/log files. Source concepts and dated raw observations are never copied. Reviewed security
skills are managed core files and follow the same preview, conflict, backup, and rollback contract.

The consuming project owns product docs, architecture, design, stack, and `make check`.

## What was left out, and why

Stack skills, product wiki pages, a starter app, ports, and retired orchestration would make this
a clone of one product. The reliability rules are process; they travel. The domain does not.
