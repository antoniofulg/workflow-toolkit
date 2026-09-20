---
id: QAS-use-optional-jev-qa-adapter
area: QAS
title: Use the default Jev browser QA route safely
persona: Workflow operator
journey: J-use-optional-jev-qa-adapter
expected: When browser_adapter is absent, WTK selects auto and uses Jev first for eligible fixtures, allows Playwright MCP only for unavailable or proven pre-action timeout, and records pass only after matching independent readback after reload.
entry_points: consumer .wtk.toml; wtk install; .agents/skills/wtk-qa-execute/SKILL.md; .agents/skills/wtk-qa-execute/jev_adapter.py
qa_status: untested
bug_ids:
fix_status:
retest_status:
fix_commits:
evidence:
last_report:
overlaps: ADP-install-versioned-workflow-package; ADP-layered-workflow-adoption
---

This promise covers the default browser route and the packaged safety boundary. An absent setting
resolves to `auto`, which starts with Jev for eligible non-consequential fixtures. Automatic
continuation requires Jev unavailability or a typed pre-action timeout plus independently known
fixture state; any possible action requires inspection or reset. A matching independent readback
after reload remains the only source of a QA pass.

The 2026-09-19 report remains evidence for the earlier package-only promise. This checkout has no
consumer fixture app, browser, Jev runtime, Browser Harness, or live Playwright MCP, so this updated
promise stays `untested` until a consumer-level walk verifies the automatic route and verdict.
