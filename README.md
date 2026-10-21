# Workflow Toolkit

Workflow Toolkit is a stack-agnostic set of Agent Skills for turning an idea into a reviewed,
verified change. The `wtk` router selects the smallest phase skill and loads its references on
demand. Projects keep ownership of their own instructions, approved execution choices,
tools, and QA records.

## Install the skills

Use the skill installer supported by your agent host. Install the complete WTK skill set as one
unit; phase skills are listed for discoverability and are not a supported subset installation:

| Skill | Use |
| --- | --- |
| `wtk` | Route a request to the smallest WTK procedure. |
| `wtk-setup` | Set up, assess or update project guidance and driver-skill responsibilities. |
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
npx skills@latest add antoniofulg/workflow-toolkit \
  --skill wtk wtk-deep-review wtk-discover wtk-implement \
  wtk-knowledge-check wtk-lean wtk-plan wtk-qa wtk-qa-execute \
  wtk-qa-plan wtk-reuse-review wtk-setup wtk-ship \
  --agent '*' --copy --yes
```

Use `npx skills@latest list` to inspect the project installation. The full WTK set carries the
shared phase dependencies. WTK does not provide a package installer executable.

The full 13-skill WTK set is self-contained: its scripts, assets, and conditional references live
below the distributed skill directories.

Projects that used the retired package installer can follow the [legacy cleanup guide](CLEANUP.md)
before installing the skills.

## Updating an existing installation

Run from the project root:

```bash
npx skills@latest update --project
```

Updates follow each skill's recorded source and `ref`; they do not select the newest WTK GitHub
release or read this repository's `package.json` version. A tag such as `v2.0.1` or a commit SHA
in `skills-lock.json` pins that installation: updating it keeps the same revision. A branch ref
follows that branch; an absent ref follows the source repository's default branch. Committing the
lockfile alone does not pin a revision; the `ref` value does. Older Skills CLI versions may also
fail to clone a commit SHA with a "Remote branch ... not found" error; use `skills@latest`, then
reinstall from the unpinned source to advance beyond that revision.

If WTK remains on 2.0.x, inspect the `wtk*` entries in the project's `skills-lock.json`. To leave
a pinned revision, rerun the [complete install command above](#install-the-skills) with the bare
`antoniofulg/workflow-toolkit` source, without a tag, commit or `/tree/<ref>` suffix. This replaces
the recorded WTK source/ref and refreshes all 13 skills. Review the installed files and lockfile
diff, then commit them in the consuming project. Future updates follow the default branch.

For a global installation, use `npx skills@latest update --global`; its tracking file is
`~/.agents/.skill-lock.json` (or `$XDG_STATE_HOME/skills/.skill-lock.json` when configured).
A missing `skillPath` or an installation made by the retired WTK
package installer also requires reinstalling through the current skill installer; use the
[cleanup guide](CLEANUP.md) for the retired installer. Updating skills does not rewrite project
instructions, native agent files or old feature workflow snapshots; follow the release's breaking
change notes separately.

See the [Skills CLI documentation](https://github.com/vercel-labs/skills#readme) for installation
sources and update scope. WTK's individual skill frontmatter versions are not the toolkit release
number; use source/ref and installed content to identify what was installed.

## Optional project instructions

Installing a skill does not edit `AGENTS.md`, `CLAUDE.md`, `.gitignore`, project configuration, or
generated agent files. If a project wants automatic routing, it can add and own a short instruction
such as:

```markdown
Use the installed `wtk` skill as the entrypoint for workflow requests. Read the project's own
product context before product-specific work, then load only the references selected by the active
WTK phase. The project owns its instructions, configuration, tests, and delivery permissions.
The project owns this text; installing or updating WTK skills does not change it.
```

Invoke `wtk-setup` to assess an existing harness or set up project guidance through a focused
policy and driver-skill interview. Assessment proposes a delta without editing project files;
authorized setup can apply settled guidance and local commits. Reuse existing guideline owners
and locations; `docs/guidelines/` is a proposal only when no convention exists, and you may choose
another location. Setup keeps root routing small and loads guidance by role, phase and concern.
It does not install tools or run as an installation side effect.

Both feature paths read applicable project guidance and required driver instructions before
deriving criteria. [Project requirements](.agents/skills/wtk/references/project-requirements.md)
owns inheritance, one fresh non-author criteria review before dependent feature build, and
independent source/applicability discovery during final verification under every profile.
Additional specialists require a concrete coverage gap; bounded maintenance keeps its direct route.

Before delegated work, WTK proposes task-specific provider/model/effort settings using the host's
current capabilities. You accept the needed stages or replace individual choices before dispatch.
[Agent selection](.agents/skills/wtk/references/agent-selection.md) owns confirmation, overrides,
inherited controls and unsupported-host handling. Skills supply responsibilities; native role files
are optional and remain untouched. Fresh checking sessions and handoffs use the current checkout.

Feature workflow state follows the [artifact lifecycle](.agents/skills/wtk/references/artifacts.md)
and remains project-owned. The Lean builder runs sequentially, Deep Review is on demand with no
automatic groups unless a feature requests it, and QA uses the `auto` adapter when the project has
no task-scoped choice. Remediation uses the fixed default `stall_attempts = 3`. When a route
snapshot is needed, `.specs/features/<feature>/workflow.json` stores approved stage/model/effort
choices, rationale, host limitations and exact approval evidence scoped to the feature and checkout.
Unchanged retries and resume reuse those choices; changed rows need targeted acceptance.

## Recommended companion skills and tools

These are independent choices. Install them through their own canonical skill or tool installer;
WTK does not bundle or configure them. When the four security phase skills below are installed,
WTK invokes them at the matching phase and uses its baseline security guidance when they are absent.
Report companion use from actual execution evidence.

| Companion | Source | Use it when |
| --- | --- | --- |
| Ponytail | [dietrichgebert/ponytail](https://github.com/dietrichgebert/ponytail) | You want a deliberately minimal-code implementation style. |
| Security lifecycle | [antoniofulg/security-lifecycle](https://github.com/antoniofulg/security-lifecycle) | The project needs dedicated threat modeling, secure implementation, review, or authorized pentesting skills. |
| Adaptive Guidelines | [antoniofulg/adaptive-guidelines](https://github.com/antoniofulg/adaptive-guidelines) | You want to turn recurring agent corrections into reviewable project guidelines. |
| Graft | [trailhq/Graft](https://github.com/trailhq/Graft) | You need checkout-local symbols, callers, or blast-radius pointers during exploration. |
| Graphify | [graphifyy on PyPI](https://pypi.org/project/graphifyy/) | You need an architecture map before tracing implementation details. |

To add the four security skills used by WTK's feature workflow, install them from the public
security-lifecycle repository:

```sh
npx skills add antoniofulg/security-lifecycle \
  --skill security-spec security-threat-model security-implementation security-review \
  --agent '*' --copy --yes
```

`security-audit-coordinator` and `security-pentest` are separate opt-in skills for whole-codebase
audits and authorized runtime testing; see the [security-lifecycle README](https://github.com/antoniofulg/security-lifecycle#usage)
for their install options.

When Graft or Graphify is absent or fails, WTK uses ordinary repository inspection and records that
the optional tool was unavailable. Optional companion use never changes the WTK phase contracts.

For product and decision documents, TLC's
[`tlc-prd`](https://github.com/tech-leads-club/agent-skills/tree/main/packages/skills-catalog/skills/%28development%29/tlc-prd),
[`create-rfc`](https://github.com/tech-leads-club/agent-skills/tree/main/packages/skills-catalog/skills/%28creation%29/create-rfc), and
[`create-adr`](https://github.com/tech-leads-club/agent-skills/tree/main/packages/skills-catalog/skills/%28creation%29/create-adr)
are optional authoring companions. WTK uses an available companion for the requested artifact;
otherwise it uses project templates and conventions. Project language, location and approval rules
take precedence. No additional WTK skill or companion installation is required.

## The workflow

The public hierarchy is `Feature -> Slice -> Check`:

1. `wtk-discover` shapes an idea or investigates a product signal when the problem or boundary is unclear.
2. `wtk-lean` records the reviewed plan and proof-backed checks.
3. One builder implements whole slices sequentially and commits each coherent slice.
4. One fresh Verifier checks the complete feature range independently.
5. QA, Deep Review, and delivery run only when their changed surface and project policy require them.

The feature artifacts are `.specs/features/<feature>/plan.md`, `checks.md`, and `verification.md`.
The project decides its validation command, provider route, QA adapter, and delivery authority.

Discover can use available PostHog analytics, Sentry issues, logs and support reports to establish
impact and compare remedies. It resolves connected tools and relevant analysis skills, reads only
the evidence needed for the question, and checks hypotheses against the repository. Missing tools
or tracking remain explicit gaps. A bounded bug uses focused diagnosis; an unresolved product or
architecture choice uses discovery. No provider connection or separate PRD is required. See
[discovery evidence](.agents/skills/wtk-discover/SKILL.md#evidence).

## Choose the artifact

Use documents for the questions the work still needs answered. A feature does not need a PRD, RFC,
ADR and separate technical design in sequence. An existing approved PRD feeds discovery only for
unresolved shape, or planning directly when the shape is settled; confirmed product questions and
build decisions are carried forward. An artifact-only request stops at that document.

| Artifact | Use it when | Owner and location | Retention |
| --- | --- | --- | --- |
| PRD | Product problem, success measures, boundary or journey needs agreement | Project product owner; existing product-document location, or `.prd/<slug>.md` with TLC's default | Keep useful product intent in maintained product docs; preserve business measures for outcome review |
| RFC | A consequential proposal needs alternatives compared and stakeholder agreement | Project decision owner and approvers; existing proposal location, or proposed `docs/rfcs/` for a new convention | Preserve the outcome and links under the project's documentation policy |
| ADR | A significant architectural choice needs lasting rationale | Project decision owners; existing ADR directory or log, or proposed `docs/adr/` for a new convention | Preserve history; supersede with linked records |
| Technical design | A separate system design review is needed | Project engineering owners; existing design-document location | Maintain current design facts when they outlive the feature |
| Lean plan, checks and verification | A decided feature needs reviewed shape and proof | Planner, builder and independent Verifier; `.specs/features/<feature>/` | Keep through verification and required promotion, then remove the exact feature directory |

WTK resolves the decision store from project instructions and existing records. Lean uses
`.specs/STATE.md` only when no other decision convention exists; with another decision store,
`STATE.md` keeps handoff only. Planning, checks, implementation and verification follow applicable
accepted decisions from that store. Feature cleanup preserves lasting decisions and useful source
documents. See [artifact ownership and lifecycle](.agents/skills/wtk/references/artifacts.md).

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
