---
id: QAS-use-optional-jev-qa-adapter
area: QAS
title: Use the default Jev browser QA route safely
persona: Workflow operator
journey: J-use-optional-jev-qa-adapter
expected: When browser_adapter is absent, WTK selects auto and uses Jev first for eligible fixtures, allows Playwright MCP only for unavailable or proven pre-action timeout, and records pass only after matching independent readback after reload.
entry_points: consumer .wtk.toml; npx skills add antoniofulg/workflow-toolkit --skill wtk wtk-config wtk-deep-review wtk-discover wtk-implement wtk-knowledge-check wtk-lean wtk-plan wtk-qa wtk-qa-execute wtk-qa-plan wtk-reuse-review wtk-ship --agent '*' --copy --yes; .agents/skills/wtk-qa-execute/SKILL.md; .agents/skills/wtk-qa-execute/jev_adapter.py
qa_status: untested
bug_ids:
fix_status:
retest_status:
fix_commits:
evidence:
last_report:
overlaps: ADP-install-versioned-workflow-package
---

This promise is consumer-owned. Install the full WTK skill set through the Skills CLI, then invoke
the WTK QA route against the project's declared adapter. Retain the safe-timeout, no-replay,
independent-readback, and reload rules. The source repository has no consumer fixture, browser, Jev
runtime, or live Playwright MCP, so this scenario remains untested until a consumer QA walk exists.
