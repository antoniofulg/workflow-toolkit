# Agent operating system

This file is the delivery workflow. It is not a product description.

## What this project is

Read `docs/product/AGENT-CONTEXT.md` before product-specific work. It holds identity, critical
constraints, and role/task routes; load only its cited references. Surface missing required context
as a named gap; do not recurse through product/history directories.

## This chat's role

**Planner for feature work**, unless spawned as implementer, explorer, verifier, or designer.

For features, Specify + Design + Tasks here. After approval, dispatch **implementer** and stay. Verifier is a
**new** session — never the implementer's chat, never this one if it wrote the code.

For bounded maintenance under `.agents/skills/wtk/references/validation.md`, the active agent edits and validates directly; delegation
is optional when it adds useful independent work, not a required handoff.
Spawn the named agent without model overrides; use `explorer` for feature exploration and traces.
Local `.wtk.toml` owns provider settings; `wtk-config` owns packet generation and frozen feature routes.
Provider definitions are real files, not symlinks.

## Critical rules

- Write all project artifacts in English: code, identifiers, comments, filenames, documentation,
  specs, commit messages, and PR titles/descriptions. Conversation may follow the user's language;
  non-English messages do not change the artifact language.
- **Do not preserve backward compatibility.** Remove obsolete paths instead of adding compatibility
  layers, fallbacks, or migrations. A rename updates code, schema, API, tests and docs in one change.
- **Never weaken, skip or delete a test to make a gate pass.**
- Derive tests from acceptance criteria or an identified invariant, not implementation details or a
  coverage target. Extend the canonical suite at the owning layer.
- **Remote delivery follows `wtk-ship`.** Invoking it, or a human go-ahead on proven-ready work,
  authorizes push, one pull request, and merge after readiness is rechecked; never ask between those
  steps; stop at the pull request only when told so up front. Readiness is not authorization for
  deploy/release, production mutations, force-push, direct push to `main`, or unrelated remote actions.
- Before editing agent instructions or guidelines, read `docs/toolkit/guidelines/CONTEXT-BUDGET.md`.
  Keep shared rules in one place and load conditional guidance only for the relevant task.
- Offer to record durable observations or decisions missing from the documents: name the destination
  and ask. Writing `knowledge/` requires a yes and follows `docs/toolkit/guidelines/KNOWLEDGE-WIKI.md`.

## How work happens

Use `wtk` as the entrypoint; it selects feature work or bounded maintenance from the request and
existing artifacts. Ponytail is an optional companion skill; WTK remains usable without it.

Continue authorized work through implementation, applicable validation and local commit. Resolve
routine choices and fix failures caused by the change without asking again; ask only for missing
decisions or new authority. Planning-only requests still end at the reviewable plan.

After a coherent edit batch, use the existing formatter on changed files, when configured, then the
applicable validation. Keep successful formatter output silent. `.agents/skills/wtk/references/validation.md`
owns check selection and evidence reuse; do not install a formatter solely for an edit.
When selecting or repeating gates, apply incremental validation by impact from that reference.

**Public hierarchy is `Feature -> Slice -> Check`.** A slice is observable end-to-end behaviour;
a check is a proof-backed obligation. `plan.md` freezes decisions and `checks.md` freezes obligations.
One builder handles whole slices sequentially; the coordinator owns handoff, verification, integration
and cleanup. After Build, one fresh Verifier covers the complete feature range. `wtk-lean` owns the
phase procedures; `wtk-config` owns review cadence. Every counted claim cites its producing command.

Delivery is human-scheduled. Git and the artifacts named below own durable state.

## wtk-lean

profile: standard
budget: 200k

## Load (the heading, not the whole file)

| When | Open |
| --- | --- |
| Planning, implementing, refactoring, or reviewing code | `.agents/skills/wtk/references/code-reuse.md` |
| Writing or reviewing tests; planning specs or tasks | `.agents/skills/wtk/references/test-contract.md` |
| Starting a task in a multi-task feature | `docs/toolkit/guidelines/WORKFLOW-MEMORY.md` |
| Specify touches a security surface | `docs/toolkit/guidelines/SECURITY.md` — `## 2. At Specify — declare the surfaces` |
| Writing tests for an abuse case | `docs/toolkit/guidelines/SECURITY.md` — `## 3. At the test contract — abuse cases get IDs` |
| Review residual | `docs/toolkit/guidelines/SECURITY.md` — `## 5. At review — the residual only` |
| Adds or changes a screen | `docs/toolkit/guidelines/UI-UX.md` |
| Front-end code or a mockup | `docs/toolkit/guidelines/FRONTEND.md` — only the heading in dispute |
| Module boundary, port, or domain type | `docs/toolkit/guidelines/MODELING.md` |
| Public surface — route, CLI verb, config key | `docs/toolkit/guidelines/DX.md` |
| Diff changes user-visible behaviour | `docs/toolkit/guidelines/QA-SCENARIOS.md` |
| QA pass at the end of a feature | `docs/toolkit/guidelines/QA-EXECUTION.md` |
| Reviewing, or acting on findings | `docs/toolkit/guidelines/REVIEW-ROUNDS.md` |
| Resolving feature workflow | `.agents/skills/wtk-config/SKILL.md` |
| About to claim done, or to commit | `.agents/skills/wtk/references/evidence.md` |
| Choosing which gate to run | `.agents/skills/wtk/references/validation.md` |
| Branch or worktree | `.agents/skills/wtk/references/git.md` |
| Keep or discard an artifact | `.agents/skills/wtk/references/artifacts.md` |
| A rule stated in more than one document | `knowledge/wiki/index.md`, then the concept |
| Recording or verifying the bundle | `docs/toolkit/guidelines/KNOWLEDGE-WIKI.md` |
| Editing this file or a guideline | `docs/toolkit/guidelines/CONTEXT-BUDGET.md` |
| Why a past choice (`AD-NNN`) | `.specs/AD-INDEX.md`; body `rg -A 20 '^### AD-NNN' .specs/STATE.md` |
| Explicit reuse, construction order, or approval requirement | `.agents/skills/wtk/references/construction-constraints.md` |
| Phase checkpoint, resume, compaction, context pressure, or session transfer | `.agents/skills/wtk/references/context-handoff.md` |

Docs and formatting do not trigger `SECURITY.md`.

`AD-NNN` (three digits, `.specs/STATE.md`) are project decisions. Architecture invariants live in the
consuming project's architecture docs. Cite the file with the label. Do not invent invariant ids in
this pack.

Recording an `AD-NNN` also runs `python3 .agents/skills/wtk-config/scripts/ad-index.py` in that commit. Lean validators
live in `.agents/skills/wtk-lean/scripts/`; the consuming project owns `make check`.

## Where the truth lives

| You need | Read |
| --- | --- |
| What to build and why | `docs/product/` |
| How the system is shaped | `docs/architecture/` |
| How it looks and behaves | `docs/design/` |
| Why a past choice was made | `.specs/AD-INDEX.md` |
| Versioned feature requirements and proof state | `.specs/features/<feature>/plan.md`, `checks.md`, `verification.md` |
| What the product currently promises users | `docs/qa/scenarios/` |

## Isolated checkouts

If the consuming project isolates checkouts (worktrees, sibling clones), **each checkout owns its
runtime**. Never set `reuseExistingServer: true` across siblings — that lets a gate in one checkout
silently test another's application.

## Commit style

Conventional Commits: `<type>(<scope>): <description>`, types `feat|fix|refactor|perf|docs|test|build|ci`.
One commit per task. One commit per review-remediation batch. If a pre-commit hook fails, fix the
issue and make a new commit — never `--amend`.
