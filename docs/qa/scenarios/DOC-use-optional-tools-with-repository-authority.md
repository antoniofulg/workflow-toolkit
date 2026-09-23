---
id: DOC-use-optional-tools-with-repository-authority
area: DOC
title: Use routed tools without surrendering repository authority
persona: Repository reader
journey: J-review-workflow-release
expected: The workflow uses optional Graphify and Graft when selected, reports exact setup without changing runtime dependencies, preserves source and approved-handoff authority with explicit native fallback, and keeps OpenDesign optional.
entry_points: README.md#recommended-companion-skills-and-tools; docs/toolkit/repository-intelligence.md; .agents/skills/wtk/references/ui-ux.md#optional-design-tooling; .agents/skills/wtk/references/security.md#external-filesystem-writers; .specs/AD-INDEX.md; .specs/STATE.md
qa_status: untested
bug_ids:
fix_status:
retest_status:
fix_commits:
evidence: docs/qa/evidence/2026-08-23-optional-design-tools/session.md
last_report: docs/qa/reports/2026-08-23-optional-design-tools.md
overlaps:
---

Covers the public part of active `AD-033`: Graphify and Graft are standard routed development tools,
the repository remains authoritative when either tool is absent or fails, setup is report-only and
exact-versioned, approved visual artifacts follow documented precedence, and OpenDesign remains a
separate optional capability. Filesystem-writing integrations preserve destination-only files without
automatic deletion.
