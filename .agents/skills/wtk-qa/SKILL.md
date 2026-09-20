---
name: wtk-qa
description: "Run one tagged QA planning or execution phase through `/wtk-qa [plan] <flow>`. Use for verifier-owned journey work."
argument-hint: "[plan] <flow>"
context: fork
agent: verifier
background: false
---

# QA

Run this phase for: $ARGUMENTS. If empty, stop and ask for the flow.

For semantic QA decisions, follow the [Jev-first guidance](../wtk/references/jev-adviser.md) before choosing a path.

Run exactly one QA phase: wtk-qa-plan when the first argument is plan, else wtk-qa-execute, over journeys tagged with the flow; read .agents/skills/wtk-qa-plan/SKILL.md or wtk-qa-execute/SKILL.md in full; if no journey carries the tag, report and stop.
