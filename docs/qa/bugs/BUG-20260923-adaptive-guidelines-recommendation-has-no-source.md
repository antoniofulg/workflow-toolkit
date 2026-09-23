# BUG-20260923-adaptive-guidelines-recommendation-has-no-source

- **Status:** open
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

## Remediation recommendation

Either identify and link the verified canonical Adaptive Guidelines source, or move it out of the
recommended table into a clearly labeled candidate/evaluation note. Keep the pack guide's claim
aligned with the resulting list.

Regression check: parse every recommended-companion row and require a source URL plus a non-empty
use case. A future candidate without a verified source must not appear as a recommendation.

