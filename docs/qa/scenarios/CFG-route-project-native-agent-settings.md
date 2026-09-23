---
id: CFG-route-project-native-agent-settings
area: CFG
title: Route features through project-native agent settings
persona: Workflow adopter
journey: J-configure-feature-workflow
expected: Without a WTK TOML file, route creation, resume, and refresh preserve every native Claude, Codex, and Cursor agent file byte-for-byte while workflow.json stores provider and role identity without model, effort, or WTK configuration fields.
entry_points: .claude/agents/; .codex/agents/; .cursor/agents/; python3 .agents/skills/wtk-lean/scripts/workflow_route.py --root . --feature <slug> --native-provider <provider>; .specs/features/<slug>/workflow.json
qa_status: untested
bug_ids:
fix_status:
retest_status:
fix_commits:
evidence:
last_report:
overlaps: ADP-adopt-workflow-safely; CFG-resolve-deep-review-cadence
---

Use a checkout-owned disposable Git consumer with no `.wtk.toml` or `.wtk.toml.example`. Give all
18 native provider/role files byte-distinct model and effort metadata. Create, resume, and refresh
routes through the public `workflow_route.py` CLI for Claude, Codex, and Cursor, then independently
compare the complete native-file inventory and read back each `workflow.json`.

The snapshot may retain provider, agent-file, feature, Git, profile, override, on-demand review, and
sequential-builder identity. It must not copy model, effort, WTK configuration version, or generated
packet content into project-owned feature state.
