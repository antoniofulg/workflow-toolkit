# BUG-20260923-skills-cli-omits-required-wtk-skills

- **Status:** fixed — fresh QA retest passed
- **Severity:** major
- **Scenarios:** `ADP-install-versioned-workflow-package`; `ADP-adopt-workflow-safely`
- **Expected:** The Vercel Skills CLI discovers all 13 skills named by the README full-set command, including `wtk`, `wtk-lean`, and `wtk-deep-review`.
- **Observed:** Skills CLI 1.5.23 reported `Found 10 skills` for the exact local source and omitted `wtk`, `wtk-lean`, and `wtk-deep-review`; therefore the documented full-set command cannot install its requested selection.
- **Adapter:** Vercel Skills CLI/manual with local-source resolution and no network
- **Exact path:** From `/Users/antoniofulg/Projects/my-workflow` at `a0d09af820a61c5c7070e86b93634a96406cf608`, run `npx --no-install skills add /Users/antoniofulg/Projects/my-workflow --list --full-depth`.
- **Evidence:** `docs/qa/evidence/2026-09-23-skills-only-workflow/skills-cli-list.txt`; `docs/qa/evidence/2026-09-23-skills-only-workflow/skills-discovery.json`; `docs/qa/evidence/2026-09-23-skills-only-workflow/skills-install.json`; `docs/qa/reports/2026-09-23-skills-only-workflow.md`

## Impact

The primary `wtk` router, Lean feature workflow, and Deep Review procedure cannot be selected from
the documented source. The full WTK installation journey stops before project mutation.

## Remediation recommendation

Make the three omitted `SKILL.md` frontmatters discoverable by the documented Skills CLI while
preserving their contracts. Add one integration regression that runs Skills CLI discovery against
the repository and requires the README's complete 13-skill set before installation.

After remediation, a non-author Verifier should rerun discovery, install all 13 skills into a fresh
isolated project, compare host sentinels byte-for-byte, and independently reload the installed
inventory and local references.

## Resolution

Fixed by `a9566e3`, which removed the three self-referential WTK entries from the committed
`skills-lock.json`. A cause discriminator against the same isolated 13-skill tree found 10 skills
with the pre-fix lock, 13 without a lock, and 13 with the fixed lock. The public Skills CLI then
installed all 13 skills into a fresh Git project in 3.587 seconds; independent `skills list` and
filesystem readback found all 13, zero unresolved local references, unchanged host sentinels, no
companion skills, no adoption manifest, no npm executable, and no installed toolkit docs. See
`skills-discovery.json` and `skills-install.json`.
