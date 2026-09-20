---
id: QAS-consult-jev-adviser
area: QAS
title: Consult Jev before choosing a semantic path
persona: Workflow operator
journey: J-consult-jev-adviser
expected: When TypeSafe is configured, the agent consults Jev before a semantic choice, checks its advice against evidence, and retains action authority.
entry_points: direct WTK phase-skill invocation; node .agents/skills/wtk/scripts/advise.mjs --phase <phase> --send
qa_status: untested
bug_ids:
fix_status:
retest_status:
fix_commits:
evidence:
last_report:
overlaps:
---

This promise covers Jev-first semantic consultation across direct WTK phase invocations. The command's preview, advice, validation, security and package boundaries have automated feature proofs. No independent host-agent walk has verified this behavior; the configured provider leg also requires a consumer session with authorized provider access, so the scenario remains untested.
