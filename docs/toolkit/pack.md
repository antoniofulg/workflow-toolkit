# Skills and optional extensions

Proven work reaches delivery only with no Critical, Major, or Minor left in the selected
review scope.

Workflow Toolkit is distributed as portable `wtk` and `wtk-*` skill directories. A project uses
its own skill installer to select and update those directories. The source repository does not own
consumer `AGENTS.md`, `CLAUDE.md`, ignore files, provider packets, configuration, product context,
knowledge scaffolding, or adoption manifests.

The installed directories are:

- `wtk` — routing and shared references;
- `wtk-discover`, `wtk-plan`, `wtk-implement`, and `wtk-lean` — discovery, planning, execution, and
  integrated Lean work;
- `wtk-reuse-review`, `wtk-knowledge-check`, and `wtk-ship` — bounded review, knowledge checks, and
  authorized delivery;
- `wtk-qa`, `wtk-qa-plan`, `wtk-qa-execute`, and `wtk-deep-review` — optional quality phases.

Each skill carries its scripts and conditional references below its own directory. The old
`docs/toolkit/guidelines/` copies are source-pack maintainer notes; consuming agents use the skill
references instead.

## Optional companion choices

Ponytail, security-lifecycle, Adaptive Guidelines, Graphify, and Graft are separate choices. The
README names their sources and use cases. WTK records when an optional tool is unavailable and
falls back to native repository inspection; it never claims a companion ran merely because the
project uses WTK.

## Existing adopters

Projects that have `.my-workflow/adoption.json` can run `node scripts/migrate.js --root <project>`
from a source checkout. Preview is read-only. Apply removes only hash-verified managed files and
instruction blocks, exact old links and installer ignore entries, after creating a byte-and-mode
backup. Modified ownership blocks the operation with zero target writes. Remaining workflow prose
outside verified blocks is reported for the project owner to review.
