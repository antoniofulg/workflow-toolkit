# BUG-20260923-full-set-scenarios-use-partial-install-command

- **Status:** fixed — fresh QA retest passed
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

## Resolution

The two current full-set scenarios now use the exact 13-skill README command. The retired layered
scenario keeps its ID for history, has no executable legacy command, and points to the replacement
full-set journeys.

Regression check: the scenario readback compares current full-set entry points with the README
selection and confirms the retired scenario has no legacy installer command.

Fresh QA retest at `d363b1c` found exact 13-skill selections in both current scenarios and no
executable command in the retired layered scenario. `scenario-contract-readback.json` records zero
missing current skills and the retired status.
