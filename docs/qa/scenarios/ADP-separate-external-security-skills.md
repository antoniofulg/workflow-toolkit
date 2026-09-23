---
id: ADP-separate-external-security-skills
area: ADP
title: Choose optional companion skills explicitly
persona: Workflow adopter
journey: J-adopt-workflow
expected: WTK leaves security-lifecycle, Ponytail, Adaptive Guidelines, Graphify, and Graft outside its installation while the README gives each recommended companion its canonical source and accurate use case.
entry_points: README.md#recommended-companion-skills-and-tools; https://github.com/antoniofulg/adaptive-guidelines; npx skills add antoniofulg/security-lifecycle --agent '*' --copy --yes; npx skills add dietrichgebert/ponytail --agent '*' --copy --yes
qa_status: pass
bug_ids: BUG-20260923-adaptive-guidelines-recommendation-has-no-source
fix_status: fixed
retest_status: pass
fix_commits: d363b1c
evidence: docs/qa/evidence/2026-09-23-skills-only-workflow/skills-install.json; docs/qa/evidence/2026-09-23-adaptive-guidelines-recommendation/readback.json
last_report: docs/qa/reports/2026-09-23-adaptive-guidelines-recommendation.md
overlaps: ADP-install-pinned-external-security-skills; ADP-preserve-security-install-target
---

Use the README optional-companion table as the source of truth. Confirm the WTK skill installation
contains no companion tree or alias, then independently install only the companion selected for the
walk through its upstream Skills CLI route. Do not claim optional tooling ran during a WTK route
unless the project explicitly installed and invoked it.

Historical QA on 2026-09-23 confirmed the WTK install contains no companion tree and that Ponytail, Security
lifecycle, Graft, and Graphify each have a source and use case. Adaptive Guidelines is presented as
a recommendation without a verified source, so the scenario fails.

Historical remediation retest at `d363b1c` found four recommended companions with source links and use cases.
Adaptive Guidelines is now a clearly labeled candidate and no longer an install recommendation.
The prior WTK install evidence still proves that no companion tree was bundled.

Fresh QA at `68e787c` found Adaptive Guidelines restored as a recommended companion with its
canonical public GitHub source and the accurate use case of turning recurring agent corrections
into reviewable project guidelines. The README and pack guide agree, while the prior install
evidence continues to prove that WTK bundles no companion tree.
