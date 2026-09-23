# Workflow Toolkit

Workflow Toolkit is a stack-agnostic set of Agent Skills for turning an idea into a reviewed,
verified change. The `wtk` router selects the smallest phase skill and loads its references on
demand. Projects keep ownership of their own instructions, native agent model and effort settings,
tools, and QA records.

## Install the skills

Use the skill installer supported by your agent host. Install the complete WTK skill set as one
unit; phase skills are listed for discoverability and are not a supported subset installation:

| Skill | Use |
| --- | --- |
| `wtk` | Route a request to the smallest WTK procedure. |
| `wtk-discover` | Shape an undecided idea or stop it. |
| `wtk-lean` | Run a decided feature through Plan, Checks, Build, and Verify. |
| `wtk-plan` | Write a modular task contract from a decided source. |
| `wtk-implement` | Implement an approved modular task. |
| `wtk-reuse-review` | Check implementation ownership and reuse. |
| `wtk-knowledge-check` | Check a project's optional `knowledge/` bundle. |
| `wtk-qa`, `wtk-qa-plan`, `wtk-qa-execute` | Plan and execute user-visible QA. |
| `wtk-deep-review` | Run an independent implementation review. |
| `wtk-ship` | Close and deliver proven work when the project authorizes it. |

The canonical source paths are the `.agents/skills/<name>/` directories in this repository. Use
the [Vercel Skills CLI](https://github.com/vercel-labs/skills#readme), whose current command is
`skills add <owner>/<repository>`, to install the full WTK set into the project:

```bash
npx skills add antoniofulg/workflow-toolkit \
  --skill wtk wtk-deep-review wtk-discover wtk-implement \
  wtk-knowledge-check wtk-lean wtk-plan wtk-qa wtk-qa-execute \
  wtk-qa-plan wtk-reuse-review wtk-ship \
  --agent '*' --copy --yes
```

Use `npx skills list` to inspect the project installation and `npx skills update` to update it.
The full WTK set carries the shared phase dependencies. WTK does not provide a package installer
executable.

The full 12-skill WTK set is self-contained: its scripts, assets, and conditional references live
below the distributed skill directories.

## Optional project instructions

Installing a skill does not edit `AGENTS.md`, `CLAUDE.md`, `.gitignore`, project configuration, or
generated agent files. If a project wants automatic routing, it can add and own a short instruction
such as:

```markdown
Use the installed `wtk` skill as the entrypoint for workflow requests. Read the project's own
product context before product-specific work, then load only the references selected by the active
WTK phase. The project owns its instructions, configuration, tests, and delivery permissions.
The project owns this text; WTK never stages or commits files for it.
```

Projects also own native model and effort metadata in their Claude, Codex, or Cursor agent files.
WTK leaves those files unchanged. A feature route snapshot records only the active provider and
role identities through `wtk-lean/scripts/workflow_route.py`.

Projects that already adopted the retired installer can preview and apply the one-time cleanup
from this source checkout before installing skills:

```bash
node scripts/migrate.js --root /path/to/project
node scripts/migrate.js --root /path/to/project --apply
```

Preview lists every verified file, managed instruction block, link, and ignore entry it would
remove. Apply backs up exact bytes and modes, refuses modified ownership, preserves surrounding
project prose, and reports legacy workflow prose for manual review. It does not create a successor
adoption manifest.

Feature workflow state follows the [artifact lifecycle](.agents/skills/wtk/references/artifacts.md)
and remains project-owned. The Lean builder runs sequentially, Deep Review is on demand with no
automatic groups unless a feature requests it, and QA uses the `auto` adapter when the project has
no task-scoped choice. Remediation uses the fixed default `stall_attempts = 3`. When a route
snapshot is needed, `.specs/features/<feature>/workflow.json` stores provider and role identity;
model and effort remain in the project's native agent files.

## Recommended companion skills and tools

These are independent choices. Install them through their own canonical skill or tool installer;
WTK does not bundle, activate, configure, or claim that any of them ran.

| Companion | Source | Use it when |
| --- | --- | --- |
| Ponytail | [dietrichgebert/ponytail](https://github.com/dietrichgebert/ponytail) | You want a deliberately minimal-code implementation style. |
| Security lifecycle | [antoniofulg/security-lifecycle](https://github.com/antoniofulg/security-lifecycle) | The project needs dedicated threat modeling, secure implementation, review, or authorized pentesting skills. |
| Adaptive Guidelines | [antoniofulg/adaptive-guidelines](https://github.com/antoniofulg/adaptive-guidelines) | You want to turn recurring agent corrections into reviewable project guidelines. |
| Graft | [trailhq/Graft](https://github.com/trailhq/Graft) | You need checkout-local symbols, callers, or blast-radius pointers during exploration. |
| Graphify | [graphifyy on PyPI](https://pypi.org/project/graphifyy/) | You need an architecture map before tracing implementation details. |

When Graft or Graphify is absent or fails, WTK uses ordinary repository inspection and records that
the optional tool was unavailable. Optional companion use never changes the WTK phase contracts.

## The workflow

The public hierarchy is `Feature -> Slice -> Check`:

1. `wtk-discover` shapes an idea when the problem or boundary is unclear.
2. `wtk-lean` records the reviewed plan and proof-backed checks.
3. One builder implements whole slices sequentially and commits each coherent slice.
4. One fresh Verifier checks the complete feature range independently.
5. QA, Deep Review, and delivery run only when their changed surface and project policy require them.

The feature artifacts are `.specs/features/<feature>/plan.md`, `checks.md`, and `verification.md`.
The project decides its validation command, provider route, QA adapter, and delivery authority.

## Development

This repository is the source pack and maintainer checkout. Run the focused skill proofs with:

```bash
bun run test
```

The source checkout keeps skill tests and local development helpers. Selecting a WTK skill installs
only that skill's files.

## Provenance and license

Project-owned WTK skills are MIT or CC BY 4.0 as declared in their frontmatter. `wtk-lean` retains
its Tech Leads Club attribution in [its notice](.agents/skills/wtk-lean/NOTICE.md). The project-owned
adaptations are maintained by Antonio Fulgêncio; `wtk-deep-review` and the QA skills were inspired by
[Pedro Nauck's skills](https://github.com/pedronauck/skills/tree/main/skills/mine) and the integrated
Lean route by [Tech Leads Club](https://github.com/tech-leads-club/agent-skills/tree/main/skills).
Optional companion projects retain their own licenses and provenance.
