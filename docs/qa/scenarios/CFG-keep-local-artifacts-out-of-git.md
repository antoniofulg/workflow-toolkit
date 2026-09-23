---
id: CFG-keep-local-artifacts-out-of-git
area: CFG
title: Keep disposable workflow artifacts out of Git
persona: Workflow adopter
journey: J-adopt-workflow
expected: Git and package output include reviewable workflow sources but exclude local agent config, generated runtimes, Graphify/Graft state, and benchmark scratch records, while a clean clone can regenerate checkout-local state and durable feature state remains reviewable.
entry_points: .gitignore; .ignore; .claude/agents/; .codex/agents/; .cursor/agents/; package.json; npx skills add antoniofulg/workflow-toolkit; .specs/features/<feature>/workflow.json; .wtk-deep-review/learnings.md; graft/; graphify-out/; .repository-intelligence/
qa_status: pass
bug_ids: BUG-20260822-adoption-omits-graft-ignores; BUG-20260822-feature-specs-ignored; BUG-20260822-feature-state-gate-conflicts; BUG-20260923-source-retains-removed-wtk-config-link
fix_status: fixed
retest_status: pass
fix_commits: b509b10; a7397d2; 43e9910; a3fc718; 5b5474e; f9b1c4d
evidence: docs/qa/evidence/2026-09-23-native-agent-settings/install-readback.json; docs/qa/evidence/2026-09-23-native-agent-settings/release-retest-readback.json
last_report: docs/qa/reports/2026-09-23-native-agent-settings.md
overlaps:
---

Covers package and clean-clone ownership, consumer-native agent files, checkout-local Graphify/Graft
state and benchmark scratch records, versioned feature workflow state, atomic route snapshots, and
preservation of unrelated target ignore entries during adoption. The previous Graft cache and
search-ignore contract remains historical; the routed artifact set is reset for fresh QA.

Fresh QA at `e6002ca1` confirmed native agent, Graphify, Graft, review runtime, and repository
intelligence paths remain checkout-local while durable workflow state is reviewable. The source
inventory still tracks `.claude/skills/wtk-config`, a dangling alias to the removed config skill,
so current checkout residue fails this promise.

Fresh remediation QA at `f9b1c4d` found exactly 12 tracked Claude skill aliases matching the 12
published WTK skills, with every target resolving. The removed `wtk-config` alias and target were
absent. Earlier green install and local-runtime evidence remained input-equivalent.
