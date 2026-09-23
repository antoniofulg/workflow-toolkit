# BUG-20260923-full-set-scenarios-use-partial-install-command

- **Status:** open
- **Severity:** minor
- **Scenarios:** `ADP-adopt-workflow-safely`; `ADP-install-versioned-workflow-package`; `ADP-layered-workflow-adoption`
- **Expected:** A scenario whose expected result says “full WTK skill set” uses the same 13-skill command published by the README.
- **Observed:** `ADP-adopt-workflow-safely` selects 3 skills, while `ADP-install-versioned-workflow-package` and retired `ADP-layered-workflow-adoption` select 6; all three expected fields describe the full WTK set.
- **Adapter:** Manual QA-contract readback
- **Exact path:** The `expected` and `entry_points` fields of the three named scenario files at `a9566e32b39eb8e17d8dd306e4bcf630020ea207`
- **Evidence:** `docs/qa/evidence/2026-09-23-skills-only-workflow/scenario-contract-readback.json`; `docs/qa/reports/2026-09-23-skills-only-workflow.md`

## Impact

A later QA session can follow the scenario literally, install only part of WTK, and incorrectly
claim the documented full-set promise passed.

## Remediation recommendation

Make current full-set scenarios use the exact 13-skill README command. For the retired layered
scenario, either remove the obsolete command from `entry_points` or state that it is historical and
must not be executed.

Regression check: compare every current scenario that says “full WTK skill set” with the README's
normalized `--skill` selection and require exact membership.

