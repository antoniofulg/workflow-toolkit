---
id: ADP-install-versioned-workflow-package
area: ADP
title: Install the full WTK skill set from its source
persona: Workflow adopter
journey: J-adopt-workflow
expected: The Skills CLI installs the full WTK skill set from the canonical repository into a disposable project, and an independent readback finds no npm installer or host-file mutation.
entry_points: README.md#install-the-skills; package.json; npx skills add antoniofulg/workflow-toolkit --skill wtk wtk-config wtk-lean wtk-qa wtk-deep-review wtk-ship --agent '*' --copy --yes
qa_status: untested
bug_ids:
fix_status:
retest_status:
fix_commits:
evidence:
last_report:
overlaps: ADP-adopt-workflow-safely
---

Use the documented Skills CLI command from a disposable project. Read back the installed skill
directories and confirm their local references resolve. Confirm no bin executable, npm installer,
adoption manifest, generated provider packet, ignore-file edit, or project instruction appeared.
