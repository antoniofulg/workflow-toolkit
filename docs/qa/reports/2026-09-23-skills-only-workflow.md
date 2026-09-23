# QA Execute — Skills-only Workflow Toolkit — 2026-09-23

- **Charter:** [`CH-skills-only-workflow-2026-09-23`](../charters/CH-skills-only-workflow-2026-09-23.md)
- **Snapshots:** initial `a0d09af820a61c5c7070e86b93634a96406cf608`; installation retest `a9566e32b39eb8e17d8dd306e4bcf630020ea207`
- **Personas:** Workflow adopter; Repository reader
- **Adapter:** Vercel Skills CLI 1.5.23/manual, public Node CLI, and independent filesystem readback through [`docs/qa/README.md`](../README.md)
- **Environment:** local source checkout; no network, registry, browser, server, provider, or optional companion installation
- **Technical gate:** coordinator-owned Technical Verification; this report does not substitute for it
- **Evidence root:** `docs/qa/evidence/2026-09-23-skills-only-workflow/` (disposable and ignored)
- **Opening porcelain:** user-owned `skills-lock.json`; verifier-owned `.specs/features/skills-first-toolkit/verification.md`; this charter/report/bugs and scenario status fields

## Scenario matrix

| Scenario | Verdict | Evidence / limitation |
| --- | --- | --- |
| `ADP-install-versioned-workflow-package` | fail | Full 13-skill install passed after remediation, but the scenario entry point selects only 6. `skills-discovery.json`; `skills-install.json`; `scenario-contract-readback.json`; `BUG-20260923-full-set-scenarios-use-partial-install-command`. |
| `ADP-adopt-workflow-safely` | fail | Install, sentinel preservation, preview, apply, and conflict passed; public rollback injection is unavailable and the scenario entry point selects only 3 skills. `skills-install.json`; `migration-results.json`; scenario-contract bug. |
| `ADP-resolve-legacy-adoption-conflicts` | untested — all reachable public legs passed | `migration-results.json`; rollback passed only through the shipped failure hook because the CLI exposes no safe fault injection. |
| `ADP-separate-external-security-skills` | fail | WTK installed zero companions, but Adaptive Guidelines lacks a verified source. `skills-install.json`; `documentation-readback.json`; `BUG-20260923-adaptive-guidelines-recommendation-has-no-source`. |
| `DOC-read-explicit-workflow-provenance` | fail | Core provenance and optional scope matched; Adaptive Guidelines source and pack-guide claim did not. Same documentation evidence and bug. |

## Skills CLI discovery and fix loop

On `a0d09af`, `npx --no-install skills add /Users/antoniofulg/Projects/my-workflow --list --full-depth`
exited 0 but reported `Found 10 skills`, omitting `wtk`, `wtk-lean`, and `wtk-deep-review`. This
blocked the full-set install before consumer mutation and created
[`BUG-20260923-skills-cli-omits-required-wtk-skills`](../bugs/BUG-20260923-skills-cli-omits-required-wtk-skills.md).

Remediation `a9566e3` removed those three self-referential entries from the committed
`skills-lock.json`. Against the same isolated skill tree, the pre-fix lock found 10, no lock found
13, and the fixed lock found 13. Fresh public discovery at the fixed snapshot also found all 13.

## Full-set install retest

The Skills CLI installed the README's 13-skill selection from an exact isolated copy of `a9566e3`
into a fresh Git project using `--agent '*' --copy --yes`. Independent `skills list --json` and
filesystem reload found every named `SKILL.md`, zero unresolved local Markdown references, and zero
Ponytail or security-lifecycle trees. Existing `AGENTS.md`, `CLAUDE.md`, `.wtk.toml`, provider
packet, ignore files, product context, knowledge index, and unrelated sentinel retained exact bytes
and modes. No `.my-workflow/adoption.json`, `bin/wtk.js`, or `docs/toolkit/` appeared. Both isolated
source and consumer roots were removed.

Evidence: [`skills-install.json`](../evidence/2026-09-23-skills-only-workflow/skills-install.json).

## Legacy migration

Public preview with `--json` listed verified files, the `AGENTS.md:core` block, one Claude link, a
legacy provider packet, exact ignore changes, and remaining unowned workflow prose. A full recursive
snapshot before and after preview was identical.

Public apply removed only those verified paths, preserved surrounding project prose and an unrelated
0600 file, retained instruction and unrelated modes, removed the old adoption manifest and journal,
created a byte-and-mode backup, and reported the unowned prose. An independently created modified
managed-file fixture returned exit 1 with its exact path and no byte, mode, link, or manifest change.

The shipped `applyMigration({ failAfter: "AGENTS.md" })` hook restored the exact recursive snapshot
and removed failed backup/journal residue. This is forward evidence, not a public CLI walk: `--help`
exposes only `--root`, `--apply`, and `--json`. The rollback leg therefore cannot grant `pass` to
`ADP-resolve-legacy-adoption-conflicts`.

Evidence: [`migration-results.json`](../evidence/2026-09-23-skills-only-workflow/migration-results.json).

## Optional instructions and companions

Independent README readback found the full-set Skills CLI command, explicit absence of a package
installer, self-contained skill claim, optional project-owned instruction snippet, and the statement
that skill installation does not edit host instructions/configuration. Install evidence matched.

Ponytail, Security lifecycle, Graft, and Graphify each had a source and use case. Adaptive Guidelines
was in the recommended table with `Canonical source not selected yet`. The pack guide simultaneously
claimed the README names the sources and uses of all five. This created
[`BUG-20260923-adaptive-guidelines-recommendation-has-no-source`](../bugs/BUG-20260923-adaptive-guidelines-recommendation-has-no-source.md).

Evidence: [`documentation-readback.json`](../evidence/2026-09-23-skills-only-workflow/documentation-readback.json).

## QA-contract consistency

The two current scenarios that promise the full WTK set select only 3 and 6 skills in their
`entry_points`; the retired layered scenario also carries a 6-skill command. The README installs 13.
This created
[`BUG-20260923-full-set-scenarios-use-partial-install-command`](../bugs/BUG-20260923-full-set-scenarios-use-partial-install-command.md).

Evidence: [`scenario-contract-readback.json`](../evidence/2026-09-23-skills-only-workflow/scenario-contract-readback.json).

## Findings

1. Fixed major: Skills CLI omitted the primary router, Lean workflow, and Deep Review because the
   committed lock self-suppressed those local skills. `a9566e3` passed fresh non-author retest.
2. Open minor: Adaptive Guidelines is recommended without a verified source; the pack guide claims
   every listed source is named.
3. Open minor: full-set QA scenarios publish partial skill selections and could support a false pass.

## Limitations

- Network and registry access are outside the QA profile. The public Skills CLI used an exact local
  source copy of the fixed revision; remote GitHub resolution was not attempted.
- Optional companions were not installed. Their absence and README guidance were observed.
- The public migration CLI has no safe failure-injection path. Rollback remains `untested` at the
  user-interface layer despite exact forward evidence from the shipped hook.
- Agent behavior and lifecycle discrimination remain Technical Verification evidence.

## Cleanup and residue

Every recorded disposable source, consumer, preview, apply, conflict, rollback, and discriminator
root was removed. Closing source porcelain contains the pre-existing user-owned `skills-lock.json`,
the coordinator's verification report, and planned QA artifacts only. No product file was edited by
this QA session.

## Commands and results

| Command / observation | Exit | Reported wall time |
| --- | ---: | ---: |
| Pre-fix local Skills CLI discovery | 0, incorrect 10-skill inventory | 0.478 s tool wall |
| Pre-fix lock / no lock / fixed lock isolated discriminators | 0 / 0 / 0 | 0.423 / 0.238 / 0.231 s |
| Fixed full-set Skills CLI install | 0 | 3.587 s |
| Independent `skills list --json` | 0 | 0.659 s |
| Migration preview / apply / conflict | 0 / 0 / 1 expected | 0.038 / 0.045 / 0.038 s |
| Rollback forward evidence | expected throw and exact restore | 0.009 s |
| Documentation / scenario contract readback | 0 / 0 | 0.026 / <0.001 s |
