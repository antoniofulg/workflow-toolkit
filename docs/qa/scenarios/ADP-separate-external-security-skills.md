---
id: ADP-separate-external-security-skills
area: ADP
title: Choose optional companion skills explicitly
persona: Workflow adopter
journey: J-adopt-workflow
expected: WTK leaves security-lifecycle, Ponytail, adaptive-guidelines, Graphify, and Graft outside its installation while the README gives each selected companion its source and use case.
entry_points: README.md#recommended-companion-skills-and-tools; npx skills add antoniofulg/security-lifecycle --agent '*' --copy --yes; npx skills add dietrichgebert/ponytail --agent '*' --copy --yes
qa_status: fail
bug_ids: BUG-20260923-adaptive-guidelines-recommendation-has-no-source
fix_status: pending
retest_status:
fix_commits:
evidence: docs/qa/evidence/2026-09-23-skills-only-workflow/skills-install.json; docs/qa/evidence/2026-09-23-skills-only-workflow/documentation-readback.json
last_report: docs/qa/reports/2026-09-23-skills-only-workflow.md
overlaps: ADP-install-pinned-external-security-skills; ADP-preserve-security-install-target
---

Use the README optional-companion table as the source of truth. Confirm the WTK skill installation
contains no companion tree or alias, then independently install only the companion selected for the
walk through its upstream Skills CLI route. Do not claim optional tooling ran during a WTK route
unless the project explicitly installed and invoked it.

QA on 2026-09-23 confirmed the WTK install contains no companion tree and that Ponytail, Security
lifecycle, Graft, and Graphify each have a source and use case. Adaptive Guidelines is presented as
a recommendation without a verified source, so the scenario fails.
