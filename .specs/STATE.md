# Project state

## Handoff

- **Feature**: `default-jev-qa`; locally complete and closed on `feat/default-jev-qa`.
- **Phase / Task**: Build, independent standard-profile verification, closing QA, durable promotion, and transient feature cleanup are complete.
- **Completed**: Both config readers default `[qa].browser_adapter` to `auto`, validate the six stable values, and preserve an existing local config. `auto` selects Jev first, then Playwright MCP, one host-declared IDE-native adapter, and manual. Only a typed Jev-construction timeout permits Playwright fallback; every result retains oracle-owned verdict and secret-free evidence. AD-038, maintained instructions/tests, and durable QA records own the lasting contract.
- **Evidence**: Independent verification proves C1-C7, 16/16 coverage sets, 4/4 test-policy rows, 5/5 killed faults, and 0 confirmed security findings; `validate_verification.py` exits 0. Fresh suites pass 64 Python config, 9 Bun config, 38 QA-skill, 9 Jev-adapter, and 78 installer packet/terminal tests. Closing QA passes every authorized offline package/config/preflight/readback leg with no defect; `QAS-use-optional-jev-qa-adapter` truthfully remains `untested` for the unavailable live browser route.
- **Constraints**: Stable config names only; no `jev-ultrafast` alias; `auto` walks Jev -> Playwright MCP -> one host-declared IDE-native adapter -> manual; direct values force one adapter; Jev stays limited to dedicated non-consequential fixtures; auto-fallback only for unavailable or proven pre-action timeout; independent oracle owns pass; install no browser/provider dependency; expose no secrets or raw exceptions.
- **Next step**: Human-scheduled consumer live Jev/Playwright QA or authorized delivery. No remote delivery is authorized in this cycle.
- **Blockers**: None. Live Jev, safe-timeout continuation, unsafe no-replay, downstream adapters, and browser-oracle evidence remain a consumer-project QA limitation.
- **Branch / state**: `feat/default-jev-qa`; implementation commits are `7ef7175b101c2eb745edf6089038d2be8d66cfd9` and `f39fef06b7183a87889c346b90835af0699fa59c`; feature artifacts are removed after promotion per AD-037. No push, deployment, provider call, publication, or production mutation is authorized.

## Decisions

### AD-001

- **Decision**: Agent always-on is a thin `AGENTS.md` (contract + pointers). `CLAUDE.md` is
  `@AGENTS.md`. Project decisions are looked up via `.specs/AD-INDEX.md`, not by reading
  `.specs/STATE.md`. Planner, implementer and verifier are three windows with different
  packets; models live only on the agent files. The delivery loop is unchanged.
- **Reason**: A `CLAUDE.md` symlink made Cursor inject the contract twice. Design/resume paid
  for the whole decision log. Packets cut that without adding a TLC phase or a front/back split.
- **Trade-off**: Role prose is copied per provider so spawn does not follow a pointer; the
  three copies can drift. Accepted over a renderer until a packet change actually diverges.
  Adopt copies agent folders only when the destination has none, so model pins survive re-adopt.
- **Scope**: `AGENTS.md`, `CLAUDE.md`, `.cursor/agents/`, `.claude/agents/`, `.codex/agents/`,
  `.specs/AD-INDEX.md`, `tools/ad-index.py`, `scripts/adopt.py`.
- **Date**: 2026-08-19
- **Status**: active

### AD-002

- **Decision**: QA planning and QA execution are separate provider-neutral skills dispatched in fresh
  sessions by the existing Verifier. The consuming project selects its adapter through
  `docs/qa/README.md`; the workflow does not mandate or install a QA framework.
- **Reason**: Independent review must be stable across Cursor, Claude and Codex while the consuming
  product remains free to use browser, API, CLI, mobile or manual tooling.
- **Trade-off**: Each consuming project maintains a small operational profile, and a missing runner
  can leave documented manual or blocked legs instead of automatic framework installation.
- **Scope**: `.agents/skills/qa-plan/`, `.agents/skills/qa-execute/`, provider `verifier` packets,
  `docs/qa/README.md`, QA guidelines and workflow docs.
- **Date**: 2026-08-20
- **Status**: superseded by AD-038

### AD-003

- **Decision**: `.specs/features/` is ignored local state. Durable project decisions remain tracked in
  `.specs/STATE.md` and indexed by `.specs/AD-INDEX.md`; task commits no longer include `tasks.md`.
- **Reason**: Feature specs, designs, tasks, memory and validation reports are execution scaffolding,
  not the public workflow contract.
- **Trade-off**: A fresh clone cannot resume an in-progress local feature from Git; the active
  checkout owns its planning state until durable knowledge is promoted.
- **Scope**: `.gitignore`, `AGENTS.md`, TLC workflow guidance, artifact lifecycle and commit evidence.
- **Date**: 2026-08-20
- **Status**: superseded by AD-007

### AD-004

- **Decision**: Workflow routing is consumer-configurable in `.my-workflow.toml`. The public
  hierarchy is `Feature -> Vertical Slice -> Task`; deep-review accepts `slice`, `feature`, or
  balanced `grouped.N`, defaults to `grouped.3`, and freezes its effective route in the feature
  snapshot before dispatch. Technical Verifier remains per code-changing slice; QA closes the
  feature after the final review group.
- **Reason**: Deep-review per slice repeatedly rereads shared context and wastes tokens. A single
  canonical resolver makes cadence and mixed-provider routing explicit without duplicating provider
  definitions or moving project gates and QA policy into workflow config.
- **Trade-off**: A project can choose less frequent deep-review and must inspect the frozen snapshot
  when resuming. Provider availability is an explicit orchestrator concern; the resolver never falls
  back silently.
- **Scope**: `.my-workflow.toml`, `.agents/skills/workflow-config/`, `AGENTS.md`, review guidance,
  workflow docs, and adoption.
- **Date**: 2026-08-21
- **Status**: superseded by AD-034

### AD-005

- **Decision**: Keep the optional, checkout-local Graft `0.10.1` integration as the deep-review
  context aid. Graft failure, absence, stale output, and dot-directory coverage always fall back to
  plain repository inspection; Graphify is not adopted.
- **Reason**: The completed local trials showed Graft improved repository-map and symbol context,
  while the project requires a non-blocking review path and has no evidence to justify replacing it
  with Graphify.
- **Trade-off**: The workflow carries a pinned optional tool and its installation surface, while
  hosts without it retain full review functionality through ordinary inspection.
- **Scope**: `.agents/skills/deep-review/`, `package.json`, lockfiles, deep-review tests and
  documentation.
- **Date**: 2026-08-22
- **Status**: superseded by AD-033

### AD-006

- **Decision**: Keep the workflow stack- and tool-agnostic while allowing optional capability
  integrations. Recommend Graft for deep-review context and OpenDesign for visual iteration; neither
  is mandatory. The repository remains authoritative for approved handoffs, with precedence
  `spec.md` → `uiux.md` → approved design artifact → tool or plugin output, then legacy mockup.
- **Reason**: Optional tools can improve context or iteration without imposing installation, provider,
  framework, or product-specific paths on consuming projects.
- **Trade-off**: Integrations may be absent or fail, so agents use honest repository fallbacks;
  external writers need explicit filesystem boundaries and non-destructive imports.
- **Scope**: `README.md`, `docs/guidelines/UI-UX.md`, `docs/guidelines/SECURITY.md`, optional
  integration skills, and feature snapshots.
- **Date**: 2026-08-23
- **Status**: superseded by AD-033

### AD-007

- **Decision**: `.specs/features/` is versioned, durable workflow state. Completed feature state is
  retained by default, archived explicitly when needed, and never auto-deleted.
- **Reason**: Worktrees, gates, handoffs, and audit need the same specs, tasks, snapshots, and
  validation state across branches and fresh checkouts.
- **Trade-off**: The repository retains small planning artifacts and maintainers must choose when to
  archive them.
- **Scope**: `.specs/features/`, `.gitignore`, `AGENTS.md`, artifact lifecycle guidance, and TLC
  workflow state handling.
- **Date**: 2026-08-24
- **Status**: superseded by AD-037

### AD-008

- **Decision**: Adopt upstream ai-memory `1.31.0` only as an opt-in, transient handoff transport
  between Claude Code, Codex, and Cursor. Lifecycle hooks and the sourceable Codex helper may create
  one pending baton, but MCP, briefing, routing skills, managed workstreams, LLMs, embeddings,
  consolidation, and auto-improvement remain disabled. Git, `.specs/`, tasks, architecture docs,
  and `knowledge/` remain the only project authority. Reviewer continuity is packet-defined: internal
  Verifier and Deep Reviewer subagents do not consume Implementer handoffs.
- **Reason**: Provider limits can end a session before work is finished; a bounded single-use baton
  resumes the next session without recurring startup context or a second task and decision ledger.
- **Trade-off**: The local runtime stores captured session material outside the checkout and still
  needs explicit path exclusions because free-form prompts and shell output are not a complete DLP
  boundary. Codex requires a manual `handoff` fallback when its process exits abnormally. Dropping
  subagent captures reduces storage noise but does not protect a top-level reviewer; role isolation
  remains an explicit packet rule.
- **Scope**: `scripts/ai-memory.zsh`, `scripts/test_ai_memory.py`, `docs/workflow/ai-memory.md`,
  `README.md`, `docs/guidelines/REVIEW-ROUNDS.md`, `docs/qa/`, the ai-memory feature contracts and
  threat model, and this decision record.
- **Date**: 2026-08-23
- **Status**: superseded by AD-019

### AD-009

- **Decision**: `.my-workflow.toml` is the single editable source for bundled Claude, Codex, and
  Cursor agent models and efforts. Provider packet metadata is generated through explicit sync, and
  delegated model settings freeze in each feature workflow snapshot.
- **Reason**: Provider-specific model pins duplicate one operator choice across three syntaxes and
  can silently diverge. The native runtimes still require those fields, so generated metadata keeps
  their contracts while centralizing ownership.
- **Trade-off**: Native packet files remain materialized tracked output, and an active feature needs
  explicit refresh after a deliberate model change. Provider runtimes still decide whether a model
  supports a selected effort.
- **Scope**: `.my-workflow.toml`, provider agent packets, workflow configuration and snapshots,
  adoption, tests, and public workflow documentation.
- **Date**: 2026-08-24
- **Status**: superseded by AD-010

### AD-010

- **Decision**: Track `.my-workflow.toml.example` and provider packet templates, while keeping
  `.my-workflow.toml` and generated `.claude`, `.codex`, and `.cursor` runtime agent trees local and
  ignored. Feature snapshots continue to freeze delegated model and effort settings.
- **Reason**: Provider access, quotas, profiles, models, and efforts vary by operator. Switching them
  must not create repository changes, while agent instructions still need a reviewable source.
- **Trade-off**: A fresh checkout must initialize local config and generate runtime packets before
  custom agents are available.
- **Scope**: Workflow configuration, provider templates/runtime packets, adoption, packaging, tests,
  documentation, and feature snapshots.
- **Date**: 2026-08-24
- **Status**: active

### AD-011

- **Decision**: Parallelization is an opt-in inter-slice orchestration layer above unchanged TLC;
  `disabled` is the default, `safe` consumes independent or verified cross-slice producers, and
  `full` consumes completed gated checkpoints with sync and revalidation. Uncertainty falls back to
  serial execution; waiting turns end and resume by dependency event; sync occurs at checkpoints,
  and affected evidence is revalidated after integration or remediation.
- **Reason**: Reduce wall time only when isolation and dependency evidence are proven, while keeping
  the reliable sequential task contract and every readiness stage.
- **Trade-off**: Capable orchestrators own worktree/runtime isolation and reconciliation, and full
  mode can pay rebase and repeated evidence costs; tasks inside a slice never run in parallel.
- **Scope**: `.my-workflow.toml`, frozen feature workflow snapshots, workflow-config planning,
  autonomous orchestration, and Verifier/deep-review/QA integration.
- **Date**: 2026-08-24
- **Status**: superseded by AD-015

### AD-012

- **Decision**: Parallel execution uses a provider-neutral deterministic coordinator whose adapters
  own external effects. Orca is the first worktree/worker/event adapter; checkpoint sync rebases only
  the private dependent lane, verified slices merge without rewriting their commits, and any missing
  adapter or consumer resource-provider capability falls back to serial execution.
- **Reason**: Restart safety, event correlation, Git evidence, and isolation policy must behave the
  same across agents and IDEs, while real port/runtime/database semantics remain owned by each
  consuming project.
- **Trade-off**: Non-Orca environments stay serial until they implement the conformance protocol,
  and resource-bearing concurrency requires a small project executable plus adoption QA.
- **Scope**: Autonomous parallel execution, workflow snapshots and task resource metadata, Orca/Git
  adapters, consumer resource providers, and future IDE adapters.
- **Date**: 2026-08-24
- **Status**: superseded by AD-036

### AD-013

- **Decision**: The provider-neutral coordinator derives and validates a deterministic sibling Git worktree destination, creates that checkout with fixed argv, and gives Orca only an existing worktree to attach a worker to.
- **Reason**: Orca's public worktree-create command does not accept a destination path, while SEC-004 requires destination validation before the first writer or worker process.
- **Trade-off**: The core owns this narrow Git worktree primitive; adapter-specific worker and event effects remain behind the provider-neutral protocol.
- **Scope**: Parallel slice executor worktree creation, adapter contracts, and future worktree/worker providers.
- **Date**: 2026-08-24
- **Status**: superseded by AD-036

### AD-014

- **Decision**: Technical Verifier remediation is bounded per blocker fingerprint, defined by the
  requirement, root cause, and concrete failure path. Distinct blockers start independent counts;
  the same fingerprint halts only after its third failed remediation, and reopening retains its
  identity and count.
- **Reason**: A slice-global round cap can stop an unattended run even while each cycle closes a
  different defect, wasting the delivery window without signalling non-convergence.
- **Trade-off**: A slice with many distinct blockers can run longer, while repeated or renamed
  versions of one blocker remain bounded and all other halt conditions still apply.
- **Scope**: Technical Verifier fix/reverify loops, autonomous halt decisions, TLC verifier guidance,
  review workflow documentation, and their contract tests.
- **Date**: 2026-08-28
- **Status**: superseded by AD-016

### AD-015

- **Decision**: Replace the vendored TLC phase-batch delegation with a workflow-owned,
  CC-BY-4.0-attributed spec-driven skill that dispatches vertical slices through hybrid assisted
  execution. Only concurrent writers receive worktrees; tasks within a slice remain sequential;
  fresh Verifier, Deep Review, and QA sessions remain independent. Adaptive concurrency starts at
  two workers and may scale one lane at a time to a default ceiling of four when a machine-only
  health proof and resource leases permit it. Context cleanup and slice-scoped packets are part of
  the foundation, not a later optimization. This decision supersedes AD-011's opt-in modes,
  unchanged-TLC premise, and default-disabled policy; AD-012 through AD-014 remain active.
- **Reason**: The current TLC skill teaches sequential phase batches, while the approved workflow
  uses safe vertical slices as the unit of concurrent delivery. A single, lean contract removes
  contradictory scheduling instructions and reduces repeated context.
- **Trade-off**: The workflow owns a maintained adaptation and additional scheduler/resource
  machinery. Independent proof still consumes tokens, and unavailable health evidence prevents
  scaling above the safe baseline.
- **Scope**: Agent instructions, spec-driven skill and references, role packets, workflow snapshot
  schema, planner/executor scheduling, resource provider and health probe, worktree lifecycle,
  adoption, verification, QA, and context-budget evidence.
- **Date**: 2026-08-28
- **Status**: superseded by AD-036

### AD-016

- **Decision**: A halted blocker fingerprint may resume only after explicit human authorization
  creates a new audit generation under that same fingerprint. The prior generation, cumulative
  failure count, halt event, and authorization reference remain immutable; only the new
  generation-local failure count starts at zero, and only a fresh independent PASS may close it.
- **Reason**: A human must be able to authorize a redesigned remediation after a legitimate halt
  without erasing why the autonomous run stopped or bypassing convergence by rewording the finding.
- **Trade-off**: Convergence state gains generation history and an explicit resume operation; a
  halted path cannot continue through JSON edits, a replacement fingerprint, or an ordinary result
  record.
- **Scope**: Technical Verifier convergence state, autonomous halt/resume decisions, review
  guidance, and their contract tests. Supersedes AD-014.
- **Date**: 2026-08-28
- **Status**: active

### AD-017

- **Decision**: Heavy test commands use an explicit named kernel lock separate from lane-wide
  resource-provider leases. The default scope coordinates linked worktrees of one project; an
  explicit machine scope coordinates projects using the same resource name. Adoption installs the
  dormant wrapper with the `parallel` layer and never rewrites consumer-owned test commands.
- **Reason**: A lane lease serializes implementation and light tests along with the contested gate,
  while a command lock preserves concurrency until the exact browser, database, container, or media
  command begins.
- **Trade-off**: Consumers must classify and wrap their heavy commands. Incorrectly unwrapped gates
  remain concurrent, while overly broad resource names reduce useful parallelism.
- **Scope**: Parallel adoption inventory, heavy-gate execution, project test commands, and local
  process-isolation guidance.
- **Date**: 2026-08-30
- **Status**: active

### AD-018

- **Decision**: The gate fingerprint is `sha256` over the gate label, the exact command argv, and
  the Git tree object written from a temporary index seeded with the checkout index and refreshed
  with every non-ignored worktree file. Records live in checkout-local ignored `.gate-cache/`.
- **Reason**: One `git write-tree` names the exact content the gate could read, honours `.gitignore`,
  changes on any edit, and does not change on a commit alone — which is the invalidation rule
  `docs/guidelines/GATES.md` already states. Hand-rolled file walks restate Git badly.
- **Trade-off**: Interpreter, dependency-binary, and environment versions are outside the key, so a
  toolchain upgrade needs the cache directory deleted. A document-only edit also invalidates code
  gates; that is conservative in the safe direction.
- **Scope**: The gate cache tool. Whether a cached record may be cited as readiness evidence is a
  separate decision, deferred with the wiring; `.agents/skills/autonomous/SKILL.md` still refuses
  cached results and this delivery does not change it.
- **Date**: 2026-09-01
- **Status**: active

### AD-019

- **Decision**: Cross-provider session continuation is owned by the host. Repository files, Git
  state, feature artifacts, and explicit handoff prompts remain the durable semantic context.
- **Reason**: Host-native continuation now covers provider unavailability, instability, and token
  exhaustion; Praxis CRM proved the approach with Orca's `Continue in New Session`, selectable
  destination agents, focused handoffs, older transcript access, and unchanged original sessions.
- **Trade-off**: Host capabilities vary, so the repository provides no replacement runtime,
  wrapper, database, hook, protocol, or compatibility layer; operators use the host UI to continue.
- **Scope**: Cross-provider continuation guidance, reviewer packets, adoption, QA, and release
  contracts in this workflow pack.
- **Date**: 2026-08-25
- **Status**: active

### AD-020

- **Decision**: Vertical slice count is derived from validated task outcomes that remain worth
  merging if all later slices are cancelled. Technical phases, cohorts, directories, runners, and
  worker batches do not create slices without an independently mergeable outcome.
- **Reason**: A manual count froze technical organization as delivery structure and multiplied
  Verifier, gate, and review cost before Tasks proved the cut.
- **Trade-off**: Every planned primary task must declare slice membership and every slice needs an
  explicit closure row; old task documents require the new contract before refresh, while normal
  resume keeps its frozen snapshot.
- **Scope**: TLC task templates and validation, workflow configuration, parallel task planning,
  feature snapshots, adoption, tests, and workflow documentation.
- **Date**: 2026-08-27
- **Status**: active

### AD-021

- **Decision**: When automatic host orchestration is incompatible, explicit human authorization may
  enable coordinator-assisted inter-slice execution through the host's direct worktree and terminal
  primitives. The coordinator owns worker launch, dependency checkpoints, same-terminal follow-up,
  synchronization, integration, and cleanup; slice workers never spawn workers. This path never
  marks the automatic adapter compatible.
- **Reason**: Direct Orca worktree creation and prompt delivery work on `1.4.188`, so a supervising
  coordinator can overlap eligible slices without weakening TLC task order, verification, review,
  gates, QA, or fail-closed automatic execution.
- **Trade-off**: The coordinator must supervise and reconstruct parked workers from Orca and Git
  state. It lacks transactional `worker_done`, ack, and release receipts, so dirty, ambiguous,
  conflicting, or unrecoverable state returns to serial execution.
- **Scope**: Autonomous inter-slice coordination, Orca direct worktree/terminal handoffs, dependency
  checkpoints, follow-up, integration, and exact owned-resource cleanup.
- **Date**: 2026-08-26
- **Status**: superseded by AD-015

### AD-022

- **Decision**: The assisted coordinator writes each complete slice packet to a coordinator-owned
  file outside every slice worktree and sends only a short fixed-shape pointer to that file through
  the host's one mandated `terminal send`. The inline-packet transport is removed, not retained as a
  fallback or length-threshold alternative. `exec_payload` and the pre-packet recording obligations
  are unchanged.
- **Reason**: `BUG-20260827-orca-terminal-send-truncates-claude-worker-packet` proves
  `orca terminal send --text` reports a complete write while the receiving TUI gets a mangled
  fragment. Loss is timing-dependent, `--text` is the only expressible transport, and the one-send
  and no-replacement-worker rules make the loss unrecoverable. A pointer keeps the mandated payload
  at a size the observed loss did not reach.
- **Trade-off**: This does not make the host transport reliable; it only shrinks the mandated
  payload. The coordinator owns packet-file lifecycle outside every worktree, and the worker must
  read a file before acting. A truncated pointer cannot produce a valid marker, so truncation still
  fails closed rather than half-executing.
- **Scope**: Assisted Orca packet delivery, the `parallelization.md` contract, AST-04, IT-005, and
  the assisted QA charter and scenario.
- **Date**: 2026-08-27
- **Status**: active

### AD-030

- **Decision**: The canonical consumer installer is the unscoped `workflow-spec-driven` npm package
  and homonymous Node.js 18 executable. Its guided installer ports the adoption and install-time
  packet-generation path from Python, while workflow tools unrelated to installation remain with
  their current owners and runtimes.
- **Reason**: Repository maintainers need one discoverable `npx workflow-spec-driven install`
  journey with module selection, recoverable upgrades, and no Python prerequisite during
  installation.
- **Trade-off**: The JavaScript port must prove parity with a mature Python adopter and temporarily
  duplicates install-time packet rendering from the Python workflow resolver. The already-published
  scoped package remains immutable registry history rather than a compatibility channel.
- **Scope**: npm package identity, installer CLI, adoption planner and transaction, install-time
  provider packet generation, installation tests, adoption documentation, and QA scenarios.
- **Date**: 2026-09-08
- **Status**: superseded by AD-036

### AD-031

- **Decision**: Deep-review runs one discovery review per implementation group. Remediation is proven
  by a single incremental job (the remediation check) that reviews `reviewed_head..HEAD` and returns
  an explicit `prior_findings` disposition for every open prior fingerprint; a prior finding resolves
  only through a `resolved` row, never by absence. The round cap is deleted; the loop is bounded by
  `[remediation].stall_attempts`.
- **Reason**: The second full round re-read the whole change to answer one question — did the fix
  land — and reviewers silently "resolved" findings that merely stopped being re-reported. One job
  with explicit dispositions answers that question at fix cost, not feature cost.
- **Trade-off**: A reviewer can still mark `resolved` on weak evidence; the prompt requires
  re-running the certificate Path and `evidence` is mandatory, but it is not machine-checked.
- **Scope**: `build_jobs.py` incremental mode, `merge_findings.py` reconciliation, `render_review.py`
  Repair plan and ledger fields, `REVIEW-ROUNDS.md` remediation rule and severity vocabulary.
- **Date**: 2026-09-09
- **Status**: active

### AD-032

- **Decision**: `one-round-deep-review` is delivered with `bun run test:all` red only on
  `tests/installer` `IT-011` (frozen canonical packet bytes) and `IT-012` (frozen Python parity
  fixtures). Both fail identically on `origin/main` at `28e4a6ae` with `node_modules` present; the
  branch changes no installer code or fixture.
- **Reason**: The readiness rule wants the full gate at 0 on the final tree; a red caused entirely by
  frozen fixtures that `main` already breaks is not evidence about this delivery, and hiding it in
  silence is worse than naming it. Regenerating those fixtures is a `main` correction with its own
  contract to understand.
- **Trade-off**: A reader of the merge sees a red gate; this entry and the pull request name the two
  ids so nobody mistakes them for regressions of this feature.
- **Scope**: `tests/installer/*.test.js` #39, #97; follow-up correction on `main`.
- **Date**: 2026-09-10
- **Status**: active

### AD-023

- **Decision**: `assisted` is the default inter-slice execution mode whenever the frozen task DAG
  exposes independent safe slices. The main agent owns direct worktree and terminal creation,
  pointer-only packet delivery, dependency parking, producer verification, exact commit sync,
  affected-gate rerun, same-handle continuation, deterministic integration, and cleanup. `disabled`
  is the explicit sequential override; `safe` and `full` retain their automatic-adapter semantics.
  Fewer than two ready slices or any isolation, resource, ownership, or reconciliation uncertainty
  falls back to sequential execution. AD-022 remains active until upstream transport is proven.
- **Reason**: Retest 12 proved useful overlap and exact cleanup under supervised coordination, while
  the upstream Orca transport and lifecycle gaps still prevent trustworthy automatic orchestration.
- **Trade-off**: Default development can consume more local CPU and memory, and the main coordinator
  must supervise fail-closed mechanics until upstream support replaces the workaround. Operators who
  need lower machine use must select `disabled` explicitly.
- **Scope**: Workflow mode resolution, feature snapshots, assisted planning and dispatch, adopted
  agent instructions and probe tooling, pointer delivery, checkpoint continuation, integration, and
  exact owned-resource cleanup.
- **Date**: 2026-08-27
- **Status**: superseded by AD-015

### AD-024

- **Decision**: Merge the workflow-side assisted-parallelization remediation with the affected live
  QA scenario truthfully left `untested`; defer live Orca QA until the upstream `orca terminal send
  --text` transport support is corrected. The pointer-only workaround and all technical fake-Orca
  evidence remain required, and no live run is claimed by this waiver.
- **Reason**: The human authorized commit and merge without publishing while explicitly choosing to
  wait for the Orca team to fix the host transport. Holding the workflow-side fail-closed and
  pointer-only delivery improvements would delay usable intermediate parallelization without making
  live QA possible in this repository.
- **Trade-off**: Autonomous readiness accepts technical/fake-host evidence for this merge, while
  the changed user journey remains visibly untested and must be walked after upstream support lands.
- **Scope**: This feature merge only: assisted default dispatch, adopted probe, pointer delivery,
  direct capability/resource proof, same-handle reconciliation, and cleanup.
- **Date**: 2026-08-28
- **Status**: active

### AD-025

- **Decision**: One `Review-Signal` trailer per delivered pull request, carried on its merge commit,
  aggregating the feature through `slices=<n> verified=<m>` counts. Not one trailer per slice.
- **Reason**: No per-slice commit can carry the verdict. The per-slice lifecycle commits each task
  before the fresh Verifier runs (`references/sub-agents.md:50-57`), and integration may be a
  fast-forward with no commit of its own, so a slice has no commit that exists after its verdict is
  known. A merge commit always exists and is the unit principle 9 names. `slices`/`verified` sum
  across deliveries to the same slice-level fraction a per-slice trailer would give.
- **Trade-off**: A pull request squashed or merged outside the documented command loses its signal.
  The reader counts a missing signal as unproven rather than as reviewed, which is the honest
  reading, but it makes the metric sensitive to how a human merges.
- **Scope**: The trailer grammar, `check_commit.py` validation, and `tools/review-metrics.py`.
- **Date**: 2026-09-03
- **Status**: active

### AD-026

- **Decision**: `check_commit.py` validates the `Review-Signal` trailer only when present; it never
  requires one. A malformed trailer is exit 1, an absent trailer is exit 0.
- **Reason**: Every task commit inside a feature runs through the same validator, and only the
  delivery commit carries a verdict. Requiring the trailer would reject every ordinary commit; not
  validating it at all would let a mistyped signal poison the metric silently.
- **Trade-off**: Nothing forces a delivery to carry the trailer, so the emitting step stays an
  instruction rather than a gate. `review-metrics.py` reporting unsigned deliveries is what catches
  omission, after the fact.
- **Scope**: `check_commit.py` only.
- **Date**: 2026-09-03
- **Status**: active

### AD-027

- **Decision**: Round 2's Finding 1 is resolved as documentation, not code. `review-metrics.py` keeps
  counting every first-parent commit as a delivery, including commits that reached `main` before the
  pull-request process existed. The operator narrows the range; the tool adds no heuristic for
  whether a commit "went through a pull request".
- **Reason**: Those commits did reach `main` and were not reviewed, so reporting them as unsigned is
  the true reading, and the bias runs pessimistic - it understates review coverage rather than
  flattering it, which is the opposite of the failure this feature exists to prevent. Any rule that
  guessed which historical commits count would be exactly the cleverness the reviewer would flag
  next, and it would decide from the tool what is properly the operator's question.
- **Trade-off**: Run over this repository's whole history today, 6 of 60 first-parent commits predate
  the process and dilute the fraction by roughly a tenth. That noise decays as history grows, and a
  reader who wants the post-adoption number passes a range. A reader who does not pass one, and does
  not read the help text, will read a number lower than the truth.
- **Scope**: `tools/review-metrics.py` delivery enumeration only. Findings 2 and 3 of the same round
  are accepted as defects and remediated in code.
- **Date**: 2026-09-03
- **Status**: active

### AD-028

- **Decision**: Each workflow phase (Specify, Design, Tasks, Implement, Verify) is its own skill
  (`wspecify`, `wdesign`, `wtasks`, `wimplement`, `wverify`) whose `SKILL.md` carries the phase
  procedure under 200 lines, with templates under `references/`. `workflow-spec-driven` remains
  the router (sizing, phase-to-skill map, `.specs` layout, resume) and keeps `scripts/`. Claude agent
  templates preload their phase skill through frontmatter `skills:`; implementer, explorer, and
  deep-reviewer carry `disallowedTools: Skill`.
- **Reason**: Preload injects only `SKILL.md`, so a phase skill that merely pointed at a reference
  would scope nothing. A role that preloads one phase and cannot invoke others reads exactly its
  own procedure, which is what makes a cheap qualifier, a forked `/w<phase>` entry point, and
  per-role model choice possible.
- **Trade-off**: Six skills instead of one directory; the router name stays because about ninety
  references and the adopted gate path cite it. Cursor and Codex keep prose load lines until their
  preload support is verified.
- **Scope**: `.agents/skills/w*`, `workflow-spec-driven/SKILL.md`, `templates/agents/claude/*`,
  `scripts/adopt.py` core catalog.
- **Date**: 2026-09-03
- **Status**: superseded by AD-036

### AD-029

- **Decision**: `designer` is a delegated matrix role that owns mockups and `uiux-review.md`;
  Claude runs it on `inherit`.
- **Reason**: Isolates mockup and UX review responsibilities from planner, implementer, and
  verifier. Keeps product code out of the designer's scope. Running Claude on `inherit` lets the
  session model drive design output without forcing a separate expensive tier by default.
- **Trade-off**: Introduces a sixth role to the configuration matrix and adoption sync across
  Claude, Codex, and Cursor.
- **Scope**: `templates/agents/*`, `.my-workflow.toml.example`, `scripts/adopt.py`, `workflow_config.py`.
- **Date**: 2026-09-03
- **Status**: active

### AD-033

- **Decision**: Graphify Labs `graphifyy` `0.9.14` and Nanonets Graft `0.10.1` are the workflow's
  standard repository-intelligence tools. Graphify identifies architectural territory during Design
  and architecturally uncertain review; Graft is the first code-discovery tool during exploration,
  implementation, and every selected Deep Review. Existing sufficient context skips retrieval;
  missing, failed, stale, partial, or insufficient tool output is an explicit degraded path to
  targeted native inspection, not normal routing. Generated state is checkout-local and ignored;
  specs and the current checkout remain authoritative. Vendor installers never own managed agent
  instructions, neither tool enters application runtime dependencies, and retention or removal after
  the 10–20 task pilot requires a later explicit decision. This supersedes AD-005 and AD-006; their
  repository-authority and honest-fallback constraints remain here, while OpenDesign remains an
  optional visual capability.
- **Reason**: Standard routed retrieval should reduce broad repository search, token use, irrelevant
  reads, and missed architectural or call-graph impact while assigning one tool to each information
  level.
- **Trade-off**: The workflow now owns exact development-tool versions, graph freshness, role routing,
  degraded behavior, and benchmark evidence. Graphify semantic extraction may consume an external
  model and transmit the disclosed source scope; each checkout must explicitly select its backend.
- **Scope**: Repository-intelligence routing, phase skills and role packets, Deep Review, adoption,
  local graph hygiene, QA scenarios, benchmark evidence, package metadata, and workflow docs.
- **Date**: 2026-09-10
- **Status**: active

### AD-034

- **Decision**: Deep Review defaults to on demand. Absent cadence and the tracked example resolve to
  `skip` with no review groups; an operator explicitly selects `slice`, `feature`, or `grouped.N` to
  schedule Deep Review. Technical Verifier behavior and remediation limits remain unchanged. This
  supersedes AD-004's `grouped.3` default while preserving its configurable routing and frozen feature
  snapshot contract.
- **Reason**: Technical verification already owns normal feature correctness. Deep Review is an
  additional inspection requested for the changes that warrant its cost.
- **Trade-off**: Features receive no Deep Review unless the operator requests or schedules it; the
  frozen route makes that absence explicit and leaves `wreview` available on demand.
- **Scope**: Workflow configuration defaults, tracked/local config, public documentation, QA scenario,
  tests, and future feature snapshots.
- **Date**: 2026-09-11
- **Status**: active

### AD-035

- **Decision**: Adopt the upstream TLC Lean artifact names and formats (`plan.md`, `checks.md`, and
  `verification.md`). Adapt local consumers to that contract instead of retaining local artifact
  names or rewriting upstream templates to match them.
- **Reason**: The user prioritizes minimizing drift from the evolving upstream skill so updates
  remain easier to compare and incorporate.
- **Trade-off**: Local validation, reporting, and integrations must accommodate upstream contracts;
  preserving the current local nomenclature is not a requirement.
- **Scope**: Artifact names, formats, templates, and their consumers in the TLC Lean adoption.
- **Date**: 2026-09-12
- **Status**: active

### AD-036

- **Decision**: Replace the task-granular workflow with Workflow Toolkit: package `workflow-toolkit`
  version `1.0.0`, CLI and on-demand entry `wtk`, and project-owned capabilities named `wtk-*`,
  including `wtk-deep-review`. Base Lean, discovery, modular planning, and modular implementation on
  TLC commit `0ab82f644cd9caf94c65347a50ad934800b0cbc4`, keeping their distinct upstream contracts.
  Use sequential builders, whole observable slices, coherent commits, and a fresh independent
  Verifier over the complete feature. Support native `light`, `standard`, and `ui` profiles with
  `standard` as the toolkit default. Retain local security, UI, QA, review, configuration, and
  authorized delivery integrations on demand; Deep Review remains optional under AD-034. No old
  skill aliases, task pipeline, or compatibility readers remain. This supersedes AD-012, AD-013,
  AD-015, AD-028, and AD-030 while retaining installer safety and author/verifier independence.
- **Reason**: A thin integration around the upstream contracts reduces maintenance drift and
  instruction overhead while retaining the toolkit's own capabilities. A major version keeps
  existing `0.x` installations older than the replacement without a version exception.
- **Trade-off**: Slice parallelism and granular task checkpoints are removed initially; pending
  older plans require explicit adaptation, and independent findings may arrive later in the build.
- **Scope**: Public identity, skills, installer catalog, provider packets, configuration, workflow
  execution, verification, and documentation. Native agent role identities remain distinct from
  namespaced skill names.
- **Date**: 2026-09-12
- **Status**: active

### AD-037

- **Decision**: Feature planning and verification artifacts are transient. Keep them available
  through execution, independent verification, and selected local gates; promote required durable
  decisions, lessons, documentation, product promises, and QA evidence before deleting the exact
  completed feature directory. Do not archive it as a second product description. Unrelated pending
  features remain untouched, and adapting an older pending plan requires an explicit request.
  This supersedes AD-007's permanent-retention policy.
- **Reason**: The user considers specs temporary work aids; maintained documentation and executable
  tests carry the product contract after completion.
- **Trade-off**: Later investigation uses durable records and Git history rather than retaining the
  feature's planning tree. Cleanup depends on completed verification and promotion, not file age.
- **Scope**: Feature artifact lifecycle, closeout, handoff, and cleanup. Shared project decisions,
  durable lessons, and QA records are not feature cleanup targets; knowledge writes still require
  their own authorization.
- **Date**: 2026-09-12
- **Status**: active

### AD-038

- **Decision**: `.wtk.toml` owns the consuming project's browser QA adapter selection through
  `[qa].browser_adapter`. The stable values are `auto`, `jev`, `playwright-mcp`, `orca`, `maestri`,
  and `manual`; absence defaults to `auto`. Automatic selection walks Jev, Playwright MCP, the one
  IDE-native adapter declared by the host (`orca` or `maestri`), then manual. Direct values select
  only that adapter. `docs/qa/README.md` continues to own fixtures, identities,
  setup, cleanup, and limitations. Jev remains restricted to dedicated non-consequential fixtures,
  and automatic continuation through LLM + Playwright MCP is allowed only when Jev is unavailable
  or a timeout is proven to precede any product action. This supersedes AD-002's prose-only adapter
  selection location while retaining its provider-neutral skills and consumer-owned runtimes.
- **Reason**: WTK 1.1.0 required an explicit Jev declaration without defining a machine-readable
  declaration surface, and its navigation timeout path recorded fallback metadata without executing
  the reliable Playwright route.
- **Trade-off**: Workflow configuration gains QA policy and two validators must remain aligned;
  projects without Jev prerequisites immediately use the fixed Playwright-first fallback instead of
  treating Jev absence as terminal.
- **Scope**: `.wtk.toml`, `wtk-config`, installer config validation, `wtk-qa-execute`, Jev adapter,
  adoption, QA contracts, and workflow documentation.
- **Date**: 2026-09-19
- **Status**: active

### AD-039

- **Decision**: Jev is the default adviser for semantic decisions throughout the development
  lifecycle whenever available, including directly invoked phase procedures. Consult it before
  selecting context or an investigation path, not only when the agent is uncertain. The shared
  adviser reference in the core `wtk` skill owns operational guidance; deterministic checks and
  existing agent, verification and authorization responsibilities retain their authority.
- **Reason**: The user requested lifecycle-wide decision assistance and explicitly required Jev
  to be used by default when available. Earlier context selection can avoid unnecessary reasoning
  and reads; an extra opinion after that work cannot establish a token saving.
- **Trade-off**: Each consultation incurs inference overhead. Record provider usage without
  claiming net savings until measured against comparable agent-only work; unavailable inference
  leaves the existing reasoning path usable. The caller reuses its environment credential source.
- **Scope**: Lifecycle adviser, core distribution and phase routing. Browser QA remains governed
  separately by AD-038; this decision grants no model-selected action execution or gate authority.
- **Date**: 2026-09-20
- **Status**: superseded by AD-040

### AD-040

- **Decision**: The shared Jev adviser reference assigns ordinary tool selection to confirmed
  gateway-managed sessions and higher-level decisions to the explicit adviser. Other sessions
  retain standalone consultation. This supersedes AD-039's universal explicit-consultation scope;
  existing workflow, action and approval authority remains unchanged.
- **Reason**: The user is adopting `jev-gateway` across projects and requested a hotfix to avoid
  asking both integrations to decide the same ordinary tool choice.
- **Trade-off**: This is instruction-level ownership, not a proxy bypass or measured token saving.
  Installation alone does not prove current-session routing. Combined live behavior needs its own
  observation; the gateway can still inspect an adviser invocation as an ordinary tool request.
- **Scope**: Shared adviser policy and its consumer-facing promise. No gateway installation,
  executable helper changes, new configuration, or browser QA adapter changes.
- **Date**: 2026-09-20
- **Status**: active

### AD-041

- **Decision**: Publishing a stable GitHub release is the only automatic npm publication trigger.
  The release event's immutable commit and version must match the tagged package, the complete test
  gate must pass without npm publishing authority, and only a dependent job may use the npm trusted
  publisher to publish the tested archive. A merge or tag push alone does not publish a package.
- **Reason**: The maintainer chose GitHub release publication as the deliberate release action;
  local npm authentication blocked the previous manual launch, and package/test code must not be
  able to request publishing identity before validation passes.
- **Trade-off**: A failed npm publish can leave a public GitHub release without a matching npm
  version; the GitHub run reports failure for manual correction. The first future release is the
  live OIDC and provenance proof.
- **Scope**: `.github/workflows/publish.yml`, package repository metadata, release documentation,
  and npm trusted-publisher configuration for `antoniofulg/workflow-toolkit`.
- **Date**: 2026-09-22
- **Status**: active
