# BUG-20260923-adaptive-guidelines-recommendation-has-no-source

- **Status:** fixed
- **Severity:** minor
- **Scenarios:** `ADP-separate-external-security-skills`; `DOC-read-explicit-workflow-provenance`
- **Expected:** Every item presented as a recommended companion has a verified canonical source and a use case, matching the pack guide's claim.
- **Observed:** `README.md` places Adaptive Guidelines in the recommended-companion table but gives its source as `Canonical source not selected yet`; `docs/toolkit/pack.md` states that the README names the source and use case for every listed companion.
- **Adapter:** Manual documentation readback from a fresh process
- **Exact path:** `README.md#recommended-companion-skills-and-tools` and `docs/toolkit/pack.md#optional-companion-choices` at `a9566e32b39eb8e17d8dd306e4bcf630020ea207`
- **Evidence:** `docs/qa/evidence/2026-09-23-skills-only-workflow/documentation-readback.json`; `docs/qa/reports/2026-09-23-skills-only-workflow.md`

## Impact

Readers cannot identify or install the recommended Adaptive Guidelines skill, and the pack guide
overstates the completeness of the companion source list.

## Resolution

Adaptive Guidelines was moved out of the recommended-companion table into a clearly labeled
candidate note until its canonical upstream source is verified. The pack guide now lists only
companions with a source URL and use case.

Regression check: the distribution proof parses the four recommended rows, requires a source URL
and use case, and asserts that Adaptive Guidelines is absent from the table.
