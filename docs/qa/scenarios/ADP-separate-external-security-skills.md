---
id: ADP-separate-external-security-skills
area: ADP
title: Choose optional companion skills explicitly
persona: Workflow adopter
journey: J-adopt-workflow
expected: WTK leaves security-lifecycle, Ponytail, adaptive-guidelines, Graphify, and Graft outside its installation while the README gives each selected companion its source and use case.
entry_points: README.md#recommended-companion-skills-and-tools; npx skills add antoniofulg/security-lifecycle --agent '*' --copy --yes; npx skills add dietrichgebert/ponytail --agent '*' --copy --yes
qa_status: untested
bug_ids:
fix_status:
retest_status:
fix_commits:
evidence:
last_report:
overlaps: ADP-install-pinned-external-security-skills; ADP-preserve-security-install-target
---

Use the README optional-companion table as the source of truth. Confirm the WTK skill installation
contains no companion tree or alias, then independently install only the companion selected for the
walk through its upstream Skills CLI route. Do not claim optional tooling ran during a WTK route
unless the project explicitly installed and invoked it.
