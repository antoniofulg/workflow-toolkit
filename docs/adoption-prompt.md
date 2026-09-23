# Skills-only setup prompt

Paste this once into an agent when adding WTK to an existing project. Replace the target path and
select only the skills the project wants.

```text
Set up the selected Workflow Toolkit skills in /path/to/target-project using the project's skill
installer. Use the project's skill installer and first check `git status --short`; do not stash, reset,
clean, or hide unrelated changes.
Read the source README and the selected SKILL.md files before writing.

Install only the selected `.agents/skills/wtk*` directories. The preview is read-only. Verify every selected skill's local
references and scripts resolve. Compare `AGENTS.md`, `CLAUDE.md`, `.gitignore`, `.ignore`, local
configuration, generated provider files, product context, and knowledge files byte-for-byte before
and after the install. Skill installation must not create or edit any of them; never overwrite existing content.
The QA procedure is `.agents/skills/wtk-qa-execute/references/qa-execution.md` when a project selects a
QA walk.

If the project has `.my-workflow/adoption.json`, run `node scripts/migrate.js --root
/path/to/target-project` from the Workflow Toolkit source checkout. Review the complete preview,
then use `--apply` only after each action is understood. Modified ownership must remain unresolved;
the helper backs up exact bytes and modes and reports unowned workflow prose for manual review.

Keep project-specific rules in the project's own `AGENTS.md` or equivalent. Optional companion
skills are installed separately; treat each optional companion as its own choice. Optionally add the
README's short WTK routing snippet. Treat Ponytail, security-lifecycle, adaptive-guidelines,
Graphify, and Graft as separate choices installed through their own sources; WTK does not claim
they ran when they are absent.
```
