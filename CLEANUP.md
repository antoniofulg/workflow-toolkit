# Clean up an older Workflow Toolkit installation

Use this guide in a project that previously ran `npx workflow-toolkit install`. The current
Workflow Toolkit is the 12 `wtk*` Agent Skills installed with a skill installer. It does not
update project instructions or run a migration command. Use the [current install command](README.md#install-the-skills)
after cleaning up the old install.

## 1. Establish ownership

Read the project's `.my-workflow/adoption.json` and record its `files` and `blocks` before
changing anything. A `files` entry with `ownership: "managed"` is removable only when the
current file's SHA-256 equals `installed_sha256`. An entry with `ownership: "consumer"` belongs
to the project. A missing manifest does not prove that a file is toolkit-owned; inspect and
report uncertain paths instead of deleting them.

Record `git status --short` and a before-state list of the proposed paths. Preserve a copy of
each file or instruction block that will change. If a managed file is missing, modified, or
replaced by another tool, leave it in place and report the conflict.

## 2. Remove verified old installer output

| Old output | Cleanup boundary |
| --- | --- |
| `docs/toolkit/` and old `.agents/skills/wtk*` copies, including `wtk-config` | Remove only manifest-managed files whose hashes match. The current 12 skills replace these copies. |
| Bundled Ponytail, security, and prompt-review skills | Remove only verified old managed copies that the project chooses to retire. These are independent optional skills now. |
| `.wtk.toml.example` | Remove when manifest-managed and unchanged. Review any local `.wtk.toml` separately; transfer wanted settings to project-native agent files before removing it. |
| `AGENTS.md` and `CLAUDE.md` | Remove only hash-matching managed blocks between `<!-- my-workflow:core:start -->` and `<!-- my-workflow:core:end -->`, or their `quality` equivalents. Preserve all surrounding prose and useful project rules. |
| `.claude/skills/<name>` | Remove only an old installer alias recorded for a managed skill when it is still a symlink to `../../.agents/skills/<name>`. Preserve other aliases or current skill-installer output. |
| `.claude/agents/`, `.codex/agents/`, `.cursor/agents/` | Inspect the six old generated role packets (`planner`, `implementer`, `verifier`, `explorer`, `deep-reviewer`, `designer`). Preserve current project-native definitions and any model or effort choices. Remove a packet only when its retired generated origin is proven and its useful settings are retained. |
| `.gitignore` and `.ignore` | Remove only exact old toolkit lines that no longer serve the project, such as `.wtk.toml` or retired cache paths. Keep rules still needed by the project or optional tools. |
| `.my-workflow/adoption.json` | Remove after the old managed files and blocks have been reconciled. Keep any migration backups until the result has been checked. |

The old installer could also copy `knowledge/AGENTS.md` and `knowledge/raw/README.md`. Apply the
same managed-file hash rule to those files. Preserve the project's `knowledge/wiki/` concepts,
raw sources, and edits.

Old ignore candidates include `.wtk.toml`, `.claude/agents/`, `.codex/agents/`,
`.cursor/agents/`, `.wtk-deep-review/*`, `graft/`, `graphify-out/`, and
`.repository-intelligence/`. The old search ignore file may also contain `!graft/`,
`graft/.cache/`, and `graft/.graph/`. Check each line against current project use before removal.

## 3. Preserve project data

Do not copy this source repository's deletion of `docs/` or `.specs/` into the consuming
project. Preserve its `docs/product/`, `docs/design/`, `docs/qa/`, `.specs/STATE.md`, active
feature records, tests, and other project-authored files. Current WTK skills still use a
project's own QA records and feature artifacts. Keep custom instructions outside verified
managed blocks. Review old workflow prose there and update it to point at the installed `wtk`
skill only when it is still wanted.

## 4. Install and check

Install the [complete WTK skill set](README.md#install-the-skills) through the project's skill
installer. Confirm that all 12 `wtk*` skills resolve their references, `wtk-config` is absent,
and project-owned instructions and agent settings are intact. Search active instructions for
`docs/toolkit/`, `wtk-config`, `.wtk.toml`, and the retired package install command; update
project-owned prose that still routes through them. Review the diff, run
`git diff --check` and the project's relevant checks, and list every file retained because
ownership or content differed from the old manifest. Do not treat an unresolved conflict as
completed cleanup.

## Agent handoff

> Update this project from the retired Workflow Toolkit package installer to the current
> skills-only WTK release. Read this cleanup guide and the current README install command. Inventory
> `.my-workflow/adoption.json` and the working tree. Remove only verified installer-owned
> files, exact managed instruction blocks, and proven old aliases or generated packets.
> Preserve project documentation, QA records, `.specs/`, knowledge, tests, custom instructions,
> and native agent settings. Install all 12 WTK skills, run the relevant project checks, and
> report the changed paths, retained conflicts, and check results.
