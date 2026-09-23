---
id: QAS-use-optional-jev-qa-adapter
area: QAS
title: Use the default Jev browser QA route safely
persona: Workflow operator
journey: J-use-optional-jev-qa-adapter
expected: When a project has no task-scoped browser adapter choice, WTK selects `auto` and uses Jev first for eligible fixtures, allows Playwright MCP only for unavailable or proven pre-action timeout, and records pass only after matching independent readback after reload.
entry_points: native project agent files; npx skills add antoniofulg/workflow-toolkit --skill wtk wtk-deep-review wtk-discover wtk-implement wtk-knowledge-check wtk-lean wtk-plan wtk-qa wtk-qa-execute wtk-qa-plan wtk-reuse-review wtk-ship --agent '*' --copy --yes; .agents/skills/wtk-qa-execute/SKILL.md; .agents/skills/wtk-qa-execute/jev_adapter.py
qa_status: untested
bug_ids:
fix_status:
retest_status:
fix_commits:
evidence: docs/qa/evidence/2026-09-23-native-agent-settings/install-readback.json; docs/qa/evidence/2026-09-23-native-agent-settings/qa-adapter-readback.json
last_report: docs/qa/reports/2026-09-23-native-agent-settings.md
overlaps: ADP-install-versioned-workflow-package
---

This promise is consumer-owned. Install the full WTK skill set through the Skills CLI, then invoke
the WTK QA route against the project's declared adapter. Retain the safe-timeout, no-replay,
independent-readback, and reload rules. The source repository has no consumer fixture, browser, Jev
runtime, or live Playwright MCP, so this scenario remains untested until a consumer QA walk exists.

Fresh source-pack QA at `e6002ca1` passed installed helper preflight and scrubbed boundary probes:
missing prerequisites and constructor timeout selected safe Playwright fallback, while a timeout
after a recorded action selected no fallback. Every helper result remained `not-passed`. No live
browser, provider, reload, or consumer oracle was available, so the scenario remains `untested`.
