# Artifact Lifecycle

**Read when:** routing PRD/RFC/ADR work, resolving a project's decision store, or deciding whether
an artifact is kept or discarded.

**Why this exists:** Planning artifacts kept forever become a second, drifting description of the
code. The inverted arrangement gated drift on documents nobody read, while nothing remembered what
the product currently promises users. Keep what is still true after the feature ships; discard the
rest.

Every artifact costs something forever: review attention, drift risk, and context budget. The question
is never "is this useful" — it is "is this useful *after the feature ships*".

## The split

| Durable — committed, maintained | Disposable — scratch, dies at feature close |
| --- | --- |
| The code and its tests | `memory/` workflow memory |
| `.specs/features/<feature>/` workflow state until verified close | `uiux.md`, `dx.md`, review rounds |
| Project-owned ADRs or decision log | |
| `docs/qa/` — scenarios, journeys, bugs, charters, reports | |
| `docs/` — product, architecture, engineering, design | |
| Durable lessons | |

The principle behind the line: **feature workflow state travels with the work.** Plan, checks, and
verification state keep worktrees, gates, and reviewers aligned.

A verification artifact's job is never finished, because it answers a question about the *present*
state of the product — which is why `docs/qa/` is on the other side of the line.

## Why this exists

Product promises still belong in `docs/qa/scenarios/`; feature workflow state belongs under
`.specs/features/`.

## Decision store

Resolve the decision store from project instructions, then the existing ADR directory or decision
log. Reuse its location, identifiers, template and status convention. If multiple stores disagree
on authority, resolve that conflict before recording a decision. Do not create a second log.
Without an existing convention, use `.specs/STATE.md` `## Decisions`; its default format
lives in [Lean memory](../../wtk-lean/references/memory.md). When establishing a new documentation
convention is requested, propose `docs/adr/` for ADRs and `docs/rfcs/` for proposals instead of
moving existing records automatically.

Record a lasting decision when it is made, outside the transient feature directory. Include its
context, chosen direction, rationale, consequences, date and status; link alternatives or a related
RFC when relevant. Read applicable accepted/active decisions before deriving criteria or checks.
A proposed ADR or an undecided RFC is not an adopted constraint. To change an accepted decision,
obtain the required project approval, create a superseding record and link both directions while
preserving the old rationale and identifier.

Keep each rationale in its decision record. A feature's `Landing` or `Decided` row carries the
literal shape and a link; its Sources entry identifies what the record settles. Read, write, verify and
promote decisions through this same store. With another decision store, `STATE.md` keeps handoff only;
the `ad-index.py` helper applies only to a project's `AD-NNN` ledger in `STATE.md`.

## Product and decision artifacts

Choose an artifact for an unresolved question or an explicit document request, not as a mandatory
chain before every feature:

| Need | Artifact | Handoff |
| --- | --- | --- |
| Product problem, outcome, scope or journey needs agreement | PRD | Confirmed product intent feeds discovery for unresolved technical shape, or planning when shape is settled |
| A consequential proposal needs alternatives and stakeholder agreement | RFC | Record the outcome before treating its direction as accepted; preserve lasting architectural choices in the decision store |
| A significant architectural choice is made or being finalized | ADR | Record its actual status; accepted decisions constrain affected feature work |
| A separate system design review is needed | Technical design document | Reuse it as input; ordinary discovery and Lean plans already carry technical shape |

For an artifact-only request, produce that document and stop before design or implementation unless
also authorized. Follow project templates, conventions and selected authoring guidance. If no
template exists, use the artifact's purpose and the project's documentation conventions. Project
language, location and authority rules govern the document.
For an RFC, name the decision owner and approvers, criteria, viable alternatives, recommendation,
and actual outcome/status; unresolved proposals remain visibly undecided.

Consume an existing PRD's confirmed intent, success measures, boundary and journey states without
repeating settled questions. Its existence alone does not establish approval. Trace confirmed
journey states to feature criteria; keep business outcome measures in observability rather than
claiming a code test proves them. Use discovery only for remaining decisions, and retain its stop
verdicts. If only an experiment can settle the question, use a bounded spike instead of an RFC.

## Rules

1. **`.specs/features/` is transient Lean workflow state.** `plan.md`, `checks.md`, `verification.md`,
   and snapshots travel with the feature through worktrees and gates, then the complete feature
   directory is deleted after verification and required promotion. Adoption removes only the exact
   legacy managed `.specs/features/` ignore line; it never stages or commits feature files.
2. **Promote before cleanup.** Anything that must outlive the feature moves to its real home:
   - A project decision → the resolved [decision store](#decision-store)
   - A PRD, RFC or technical design still needed beyond the feature → its project-owned documentation location
   - A durable lesson → the lessons layer
   - A product promise → `docs/qa/scenarios/`
   - An architecture invariant → the consuming project's architecture docs
   - A shared workflow rule → its owning skill reference; a project-specific rule → the project's instructions
3. **Nothing gates a disposable artifact for drift after cleanup.** A document nobody reads after the merge cannot
   be stale in a way that matters.
4. **One home per fact.** A fact recorded in two durable places will disagree with itself. If it
   belongs in `docs/`, it is referenced from a guideline — never copied into one.

## Cleanup cadence follows read frequency, not size

The three stores need three different policies, and the sizes mislead:

| Store | Loaded when | Policy |
| --- | --- | --- |
| `.specs/archive/features/` | never | **No recurring job.** The rule above stops the directory regrowing |
| `.specs/lessons.json` | every Specify and Design | **Nothing to do.** It prunes itself — a candidate that has not recurred within `window_days` drops on every `add` or `list` |
| Project decision store | applicable decisions at planning/checks and resume | Follow its maintenance convention; for the default `STATE.md` ledger, split by status when superseded entries pass ~15, or annually |

The largest store is the one that needs no maintenance, because nothing reads it. The smallest is the
one that does, because everything does.

**Never delete a decision.** Preserve superseded records under the project's archival convention.
For the default ledger, moving a superseded entry to `DECISIONS-ARCHIVE.md` keeps its id and full
text. Ids are never reused.

**Never hand-edit the lessons store.** It is machine-owned; `LESSONS.md` is rendered from it.

## Archived planning trees

If a consuming project archives old feature directories under `.specs/archive/features/`, treat them
as history, not context: never loaded as implementation context, never maintained. Keep them only
while something still cites them as a `resource`.

## Scheduling follow-ons

Work identified but not done becomes ordinary features with ordinary specs. It is not carried as an
ambient intention in an instruction file. A model that counts is a model that miscounts — scripts
that audit `checks.md` ids, validate QA frontmatter, or cache gate fingerprints belong as features of
the consuming project, not as extra guidelines here.
