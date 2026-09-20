# Workflow Toolkit

The npm package is `workflow-toolkit`; the executable is `wtk`.

An operating system for agents. It ships the workflow-owned [`wtk`](.agents/skills/wtk/SKILL.md)
router and its Lean skills (`wtk-lean`, `wtk-discover`, `wtk-plan`, `wtk-implement`)
with a capped delivery loop, countable tests and security surfaces, and a knowledge bundle. It is
not a product template and not a stack starter.

The design problem is the usual one: **ship, without lying about quality**. Unbounded review feels
responsible and never finishes. A green suite with no spec contract ships bugs. This pack picks a
middle: small vertical slices, cheap gates while building, a hard cap on review rounds, and a
human-owned merge.

## Quick start

From the repository you want to install into, run the guided Node.js installer:

```bash
npx workflow-toolkit install
```

The command targets the current directory, requires Node.js 18 or newer, and walks through module
selection, state assessment, a complete preview, conflict decisions, final confirmation, and a
result summary. It never requires Python. Existing files that are replaced or removed are copied
byte-for-byte with their modes into `.my-workflow/backups/<UTC timestamp>/`; the adoption manifest
is published last. Cancelling at any prompt writes nothing.

Choose `core`, `quality`, or `extras`; selecting any non-core module also selects `core`.
Every module is shown as `not installed`, `up to date`, `outdated`, `modified`, or `conflict`. A
conflict must be explicitly backed up and replaced, excluded, or cancelled. Successful replacements
that affect consumer guidance include a `knowledge-transfer.md` checklist with a pending human
transfer; consumer knowledge is never merged automatically.

The terminal wizard supports 80×24 and 120×40 layouts and `NO_COLOR=1`. The package's complete
current workflow is documented in [docs/toolkit/](docs/toolkit/).

Start here: **[docs/toolkit/](docs/toolkit/)** — an index of every stage, guideline, and choice.

## Purpose

| Delivery | Reliability |
| --- | --- |
| Auto-sized planning (one line needs no spec) | Tests assert spec outcomes, not the implementation |
| Proportional scoped gate; full gate only when selected | Never weaken a test to go green |
| Nitpicks become filed issues, not extra rounds | Critical and Major still hold the ship |
| `ponytail` at `full` — shortest code that works | Security surfaces declared and given `SEC-` ids |
| `wtk-ship` scopes remote delivery | Its invocation authorizes the feature-branch push, one pull request, and merge after readiness is rechecked; readiness is evidence, not authorization for deploy/release, production mutations, force-push, direct `main` push, or unrelated remote actions |

The loop, the caps, and the guidelines are the mechanism. The tour explains **why** each exists.
`AGENTS.md` is what agents run.

## Current workflow

Use plain intent in the request:

- “Visual polish / UI-only correction; I am doing manual QA” keeps adjustments to colors, spacing,
  typography, alignment, borders, and layout on the narrow inspect → implement → targeted check →
  commit path when behavior stays unchanged.
- “Feature” starts the smallest spec and slice route that fits the behavior. “Cross-feature” sets a
  broader mapping floor. A neutral Linear `issue` is classified from its concrete outcome, not its
  label.
- Documentation maintenance, agent-instruction changes, and mixed executable changes automatically
  use proportional checks from `.agents/skills/wtk/references/validation.md`. Named risk or changed public behavior selects stronger
  evidence. Confirmed wtk-deep-review defects are fixed inside their run; cosmetics become follow-up work.

The feature path is Plan → Checks → Build → Verify. Builders use whole observable slices and
coherent commits, then one fresh independent Technical Verifier proves the complete feature range.
Deep Review is optional and defaults to `skip`; QA runs when the changed surface requires a user-visible
walk; the full gate remains selected by changed behavior and concrete risk.

For UI work, Designer starts with constraints, reads selected references, and inspects existing
components read-only. A design tool or isolated prototype supports exploration when useful. Three
alternatives apply when a new screen or meaningful redesign leaves an actual design choice open;
existing patterns handle bounded compositions. One exploration and one refinement is the default.
Human visual acceptance is recorded only after the human confirms it.

The shared workflow stays in `AGENTS.md`. Keep the product index short and point to existing
documents, for example:

```markdown
## Critical constraints
- [Only the project constraints every task must see.]

## Role/task routes
| Role or task | Read only |
| --- | --- |
| Visual polish | docs/design/SYSTEM.md#tokens-and-accessibility |
| Customer-facing copy | docs/brand/VOICE.md |
| Feature planning | docs/product/OVERVIEW.md and affected journey references |
| Implementation | Assigned spec/task and the relevant architecture sections |
```

These paths are examples: replace them with real files and headings in your project. A visual-polish
task does not load the voice guide or all product journeys merely because those documents exist.
Project-specific operational rules, such as Linear routing and environment setup, can live in
separate references selected by the matching task.

## Credits and provenance

This workflow is maintained by Antonio Fulgêncio. The process builds on work from the following
authors and communities:

- Tech Leads Club: the adapted [`wtk`](.agents/skills/wtk/SKILL.md),
  based on [`tlc-spec-driven`](https://github.com/tech-leads-club/agent-skills/tree/main/skills/tlc-spec-driven),
  and the security gate with its [security skills](https://github.com/tech-leads-club/agent-skills/tree/main/skills).
  The integrated Lean source is pinned to commit `0ab82f644cd9caf94c65347a50ad934800b0cbc4` under
  CC BY 4.0; see [`NOTICE.md`](NOTICE.md) and [`skills-lock.json`](skills-lock.json).
- Pedro Nauck: [`wtk-deep-review`](https://github.com/pedronauck/skills/tree/main/skills/mine/wtk-deep-review),
  whose review workflow is adapted here.
- The project-owned `wtk-qa-plan` and `wtk-qa-execute` skills are Antonio's adaptations, inspired by Pedro's
  [`qa-report`](https://github.com/pedronauck/skills/tree/main/skills/mine/qa-report) and
  [`qa-execution`](https://github.com/pedronauck/skills/tree/main/skills/mine/qa-execution).

The QA skills use their own wording and structure for this workflow; the links above identify the
inspiration and do not claim upstream authorship.

The workflow bundles five reviewed security lifecycle skills:

- `security-audit-coordinator` for explicit whole-codebase security audits;
- `security-spec` for security requirements and negative tests during Specify;
- `security-threat-model` for repository-grounded threats and trust boundaries;
- `security-implementation` for secure-by-default implementation and hardening;
- `security-review` for high-confidence residual vulnerability reviews.

Their GitHub source, canonical path, reviewed commit, CLI version (`1.5.23`), and full-tree hash are
authoritative in [`skills-lock.json`](skills-lock.json). The package includes those exact reviewed
trees. `wtk install` publishes them through the normal offline core preview, conflict, backup,
rollback, alias, and adoption-manifest flow; it never resolves `latest` or fetches security skills.

## Guided installation details

Copy the loop, not the product. New projects receive a neutral, consumer-owned
`docs/product/AGENT-CONTEXT.md` index; fill its identity and routes with existing project references
instead of copying this source pack's profile. Existing projects preserve their filled product
paragraph and product-owned documentation. Knowledge transfer is always a human review step.

The three fixed modules are `core` (Lean operating loop and shared tooling), `quality` (review and QA),
and `extras` (optional Ponytail utilities and prompt-review). Selecting `quality` or `extras` automatically
includes `core`. The guided command is:

`core` contains the Lean operating loop and Bun tooling; `quality` adds review and QA skills; and
`extras` adds optional Ponytail utilities and prompt-review. `full` resolves all three catalog modules.
Invoke `$prompt-review` for instruction audits or requested simplification.

```bash
npx workflow-toolkit install
```

The target must be the current directory and the command must run in an interactive terminal.
The command never invokes Python. It previews add, update, adopt, preserve, replace, remove, and
no-change actions before asking for final confirmation.

Cancellation exits 0 with no target, adoption, journal, or backup changes. Invalid state, unsafe
paths, backup failures, and publication failures exit 1; non-interactive use exits 2 with the exact
TTY guidance.

Add capabilities later with another apply; installed layers are cumulative and omitted layers are
never removed. `--skip-agents` preserves both instruction files byte-for-byte and skips local-config
initialization and packet synchronization. Without it, adoption appends managed `core` and `quality`
blocks while preserving consumer prose. A differing
managed file or unowned destination is reported as a conflict and causes zero writes.

### Recovery and conflict handling

For an existing project copied from an older workflow release, the wizard inspects current files and
the adoption manifest. It reports every conflict before writing. Choose `Back up and replace`,
`Exclude module`, or `Cancel installation`; excluding `core` also excludes dependent modules.

If the process stops after publication begins, the next run detects the transaction journal and
offers restoration from its verified backup before allowing a new installation.

### Test resources

The Lean route uses one sequential builder. Consuming projects may serialize heavy commands that
share a browser, database, container runtime, or other declared resource.

Prerequisites: Node.js 18 or newer and an interactive terminal. Python is not an installer
prerequisite; unrelated Python workflow tools remain available after installation.

The preview is the review: inspect the complete action list and backup destination before confirming.

Feature workflow state follows the [artifact lifecycle](.agents/skills/wtk/references/artifacts.md) and
remains visible to Git. Adoption removes only the exact legacy `.specs/features/` ignore line,
including duplicates, preserves consumer-owned lines and comments, and never stages or commits files
from the transient feature tree.

The tracked `.wtk.toml.example` documents the complete v3 matrix and `mixed` profile. Each
checkout owns an ignored `.wtk.toml`, initialized from that example by adoption without
`--skip-agents` or by explicit sync;
it is the single editable source for all Claude, Codex, and Cursor model and effort choices. The
tracked `.agents/skills/wtk-config/assets/agents/` trees hold canonical instruction bodies, while sync generates the
ignored native runtime packets. Re-adoption preserves an existing local config byte-for-byte and
regenerates runtime packets from the templates and that config when `--skip-agents` is not used.
With `--skip-agents`, sync is an explicit later operator step.

The optional `[qa].browser_adapter` key defaults to `auto`. Valid values are `auto`, `jev`,
`playwright-mcp`, `orca`, `maestri`, and `manual`. `auto` tries Jev for eligible
non-consequential fixtures, then LLM + Playwright MCP, exactly one IDE-native adapter, then manual.
The QA execution skill defines safe timeout continuation and the independent-verdict requirement.

```bash
python3 .agents/skills/wtk-config/scripts/workflow_config.py \
  --root /path/to/target-project --sync-agents
```

Edit the `[models.<provider>.<role>]` tables in the local `.wtk.toml`, then run the explicit
sync command. If the local file is missing, sync validates and copies
`.wtk.toml.example` first. It reports changed and unchanged runtime packet paths and is
idempotent. Native `model`, `effort`, and `model_reasoning_effort` fields are generated output; do
not edit runtime packets manually. Runtime edits are disposable; edit tracked templates when
changing instruction bodies.

The `cadence` controls the wtk-deep-review groups:

The default is `skip`: Deep Review runs only when the operator requests it or explicitly selects a
scheduled cadence.

- `slice`: one group per slice (`1, 2, 3, 4` → `[1] [2] [3] [4]`).
- `feature`: one group for the whole feature (`1, 2, 3, 4` → `[1, 2, 3, 4]`).
- `grouped.N`: consecutive, balanced groups with at most `N` slices (`grouped.3` with four
  slices → `[1, 2] [3, 4]`).
- `skip`: no groups (`[]`); final QA, readiness, and merge do not wait for wtk-deep-review, and the
  human runs `wtk-deep-review` later.

Post-cap remediation is bounded by `[remediation] stall_attempts`. It defaults to `3`; `0` means
unbounded. The threshold is read from the current local config on every attempt and is not stored
in the feature snapshot:

```toml
[remediation]
stall_attempts = 3
```

After each remediation attempt, the scoped gate produces a normalized, sorted failing-test
signature. A strictly smaller failing-test set resets the stall counter; an equal-size or larger
set increments it, including when membership changes. A reached nonzero threshold halts with the
signature, attempt count, and fixes tried. An unavailable gate halts immediately. The review cap
never opens a third wtk-deep-review round.

The resolver uses the native provider for every role unless a named profile or role override is
selected. Precedence is `CLI override > profile > native provider`:

When a feature has `tasks.md`, the resolver validates its vertical-slice closure table and derives
the slice count from merge-alone outcomes. A feature without `tasks.md` uses one slice. `--slices`
is an optional assertion against that derived count during initial resolution or refresh; it is not
the source of truth.

```bash
# Native route: all roles use Codex.
python3 .agents/skills/wtk-config/scripts/workflow_config.py \
  --root /path/to/target-project --feature register-user-native \
  --native-provider codex

# Named profile: use the [profiles.mixed] routes from .wtk.toml.
python3 .agents/skills/wtk-config/scripts/workflow_config.py \
  --root /path/to/target-project --feature register-user-profile \
  --native-provider codex --profile mixed

# Role overrides win over both the selected profile and the native provider.
python3 .agents/skills/wtk-config/scripts/workflow_config.py \
  --root /path/to/target-project --feature register-user-override \
  --native-provider codex --profile mixed \
  --override deep_reviewer=cursor --override verifier=claude
```

The first resolution freezes the effective route and cadence in
`.specs/features/<feature>/workflow.json`, including model and effort for every delegated role.
Planner is synchronized but remains the top-level session, not a delegated snapshot role. On
resume, the snapshot is authoritative and packet metadata must still match its frozen model and
effort. If it differs, synchronize packets and explicitly refresh; ordinary resume will fail:

```bash
python3 .agents/skills/wtk-config/scripts/workflow_config.py \
  --root /path/to/target-project --feature register-user-refresh \
  --native-provider codex --refresh
```

The complete contract is in the
[wtk-config skill](.agents/skills/wtk-config/SKILL.md).

## Update an adopted project

Start from a clean tree and a dedicated update branch. Read the changelog since the version the
project adopted, then run the guided installer and inspect the complete diff before committing:

```bash
cd /path/to/target-project
git status --short
git switch -c build/update-wtk
npx workflow-toolkit install
git diff
```

Run `npx workflow-toolkit install` for every installation or update. It updates pristine
workflow-owned files, promotes provider templates using recorded source hashes, refreshes managed
instruction blocks and runtime packets, and stops with all conflicts before writing.

Adoption preserves product context, local config, package metadata, existing knowledge, and unknown
consumer files. A fresh target receives managed generic knowledge instructions plus neutral,
consumer-owned wiki indexes and log. Source concepts and dated raw observations never cross the
repository boundary. Retired workflow files are removed only when their managed hashes prove they
are pristine; edited or unproven paths conflict with zero writes.

Each release lists its upgrade steps under `### Migration` in the changelog; follow them in order
after installation. The package identity for this release is `workflow-toolkit@1.2.0` with the `wtk` executable.

## Managed paths

Review the managed paths and the installer's per-file actions. Installation updates only workflow-owned files,
preserves unknown consumer files, creates `.wtk.toml.example` and skill-owned runtime, and records ownership in `.my-workflow/adoption.json`. It never removes an
installed layer or consumer file. Product documentation, `.specs/`, `package.json`, `bun.lock`, an
existing local `.wtk.toml`, and an existing `docs/qa/README.md` remain consumer-owned.

The local config is the source for generated provider packets. Installation preserves an existing
`.wtk.toml` and installs tracked templates when missing. The guided command synchronizes and
regenerates the ignored `.claude/agents/`,
`.codex/agents/`, and `.cursor/agents/` packets from the templates and config. Edit the config or
tracked templates, not generated runtime packets.

## Troubleshooting

**`conflict` during installation.** Review every listed path. Restore an owned file to its recorded
hash or resolve an unowned collision, then run the guided command again. Installation is all-preflight:
no selected file or manifest is written while any conflict remains.

**`refusing adoption: Makefile:N uses machine-global workflow skill path`** Point the target's gate at
the vendored `.agents/skills/wtk-config/scripts/...` path.

**Claude skill symlinks point nowhere.** Re-run `npx workflow-toolkit install`; it recreates the `.claude/skills/`
links into `.agents/skills/`.

**A runtime packet has the wrong model or effort.** Edit the local `.wtk.toml`, then run
`npx workflow-toolkit install`. Runtime packets are generated output.

## Repository intelligence

The workflow stays stack- and tool-agnostic while using provider-neutral repository-intelligence defaults.
Graphify and Graft are the standard, checkout-local development tools for repository intelligence.
They never enter application runtime dependencies, and specs plus current checkout source remain
authoritative.

Use the smallest route that answers the question:

- Existing file, symbol, API, caller, and callee pointers: skip retrieval.
- Architectural trigger (boundary, responsibility transfer, shared abstraction, central flow, or
  unresolved architectural risk): query Graphify first, then use Graft for implementation pointers.
- Unknown code location or call relationship: query Graft before broad native search.
- Exact-text question: use exact native search.

Tool output stays bounded. Missing, wrong-version, stale, failed, partial, or insufficient output
produces one explicit degraded reason for the phase, then targeted native inspection. Degraded
inspection is a fallback, not normal routing.

Adoption reports these exact development-tool remediation commands without executing them or changing
application dependencies:

```bash
npm install --save-dev --save-exact @nanonets/graft@0.10.1
uv tool install graphifyy==0.9.14
python3 .agents/skills/wtk-config/scripts/repository_intelligence.py \
  graphify-setup --root . --backend <backend> --mode deep
```

Graphify semantic extraction requires an explicit backend and discloses its source scope before
extraction. Each query refreshes or rejects state using the active checkout and working-tree
fingerprint. Generated graphs, caches, backend metadata, and benchmark scratch records remain ignored
under `graft/`, `graphify-out/`, and `.repository-intelligence/`.

The directional retention pilot records one controlled terminal task per JSONL record, including task
category, configuration (`baseline`, `graft`, or `routed`), snapshot and prompt controls, provider,
model, effort, token metrics, repository-intelligence/native-search calls, files read, wall-clock time,
gate, Verifier, findings, rework, and outcome. Compare the same controls within each category after
10–20 terminal tasks. A promoted report is directional, not statistically conclusive; removing or
changing routing requires a later explicit project decision.

## Optional integrations

**OpenDesign** remains an optional visual capability. The repository stores only the approved handoff;
absence or failure falls back to normal repository artifacts. It is separate from standard Graphify
and Graft routing. No integration is mandatory or installed by adoption for visual iteration.

The installer merges workflow-owned ignore entries, copies missing example/templates, generates
local runtime packets, and records per-file ownership in `.my-workflow/adoption.json`. It preserves
consumer prose through managed blocks, never removes an installed layer, and leaves package
metadata, local config, and unknown files untouched. Always review the plan and resulting diff
before accepting managed-path updates.
Adoption installs the five reviewed security skills with core. No separate network step is required.

## Skills

Canonical copies live in `.agents/skills/`. Claude Code gets symlinks in `.claude/skills/`. Cursor,
Codex and OpenCode consume `.agents`. Do not add `.cursor/skills` or other agent trees. The
project-owned `wtk-qa-plan` and `wtk-qa-execute` skills use the consuming project's profile in
`docs/qa/README.md`; they do not select a framework or replace the project's gate.

`npx workflow-toolkit install` installs and updates the workflow-owned `wtk` router, its Lean skills
(`wtk-lean`, `wtk-discover`, `wtk-plan`, `wtk-implement`), Ponytail, Deep Review, QA, wtk-config,
wtk-ship, and the five reviewed security lifecycle skills. Keep canonical copies in
`.agents/skills/` and Claude Code symlinks in `.claude/skills/`.

`wtk-ship` is vendored here. `CLAUDE.md` is the one line `@AGENTS.md` (not a symlink). Canonical
packet templates live under `.agents/skills/wtk-config/assets/agents/{cursor,claude,codex}/`; generated implementer,
explorer and verifier runtimes live under the ignored `.cursor/agents/`, `.claude/agents/` and
`.codex/agents/` directories.

## Knowledge checker

These are optional source-pack maintainer checks, not adoption or consumer task gates.

```bash
bun install --frozen-lockfile
bun run test:all
bun run knowledge
```

The consuming project's full gate should not include this checker. Run it when writing to the
bundle.

## Out of scope

Product domains, product-owned documentation, architecture, infrastructure, and framework choices
belong to the consuming project. This pack is stack-agnostic on purpose and does not prescribe a
browser, API, CLI, mobile, or manual QA runner.

## Deliberately not included

- Any product, domain, architecture, or design *concepts* from a source project's wiki
- Dated `knowledge/raw/` observations
- Library and stack skills
- A product skeleton, Makefile, port scheme, or worktree-slot arithmetic
- Retired orchestration history
