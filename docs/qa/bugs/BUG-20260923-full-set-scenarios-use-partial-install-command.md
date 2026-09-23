# BUG-20260923-full-set-scenarios-use-partial-install-command

- **Status:** fixed — fresh QA retest passed
- **Severity:** minor
- **Scenarios:** `ADP-adopt-workflow-safely`; `ADP-install-versioned-workflow-package`; `ADP-layered-workflow-adoption`; `REL-report-current-workflow-release`; `QAS-use-optional-jev-qa-adapter`
- **Expected:** A scenario whose expected result says “full WTK skill set” uses the same 13-skill command published by the README.
- **Observed:** `ADP-adopt-workflow-safely` selects 3 skills, while `ADP-install-versioned-workflow-package` and retired `ADP-layered-workflow-adoption` select 6; all three expected fields describe the full WTK set.
- **Adapter:** Manual QA-contract readback
- **Exact path:** The `expected` and `entry_points` fields of the three named scenario files at `a9566e32b39eb8e17d8dd306e4bcf630020ea207`
- **Evidence:** `docs/qa/evidence/2026-09-23-skills-only-workflow/scenario-contract-readback.json`; `docs/qa/evidence/2026-09-23-skills-only-workflow/full-set-contract-readback.json`; `docs/qa/reports/2026-09-23-skills-only-workflow.md`

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

## Later contract recheck

When `b3e430b` made the complete 13-skill set the only supported installation, scoped QA found two
additional active subset promises: the release scenario selected only `wtk`, and the Jev scenario
selected only `wtk-qa-execute` and told users to install that selected skill. Remediation `da1e239`
changed both entry points to the exact README selection and changed the Jev prose to install the
full set before invoking its route.

Fresh readback at `da1e239` found the exact 13 skills in the README and every active install command,
with no active partial promise. `.agents/skills/`, `package.json`, and `skills-lock.json` had no
changes from the successful `a9566e3` live install, so that evidence remains reusable. See
`full-set-contract-readback.json`.
