# Workflow tour

Human-facing maintainer notes. Agents run their installed `wtk` skill and load a reference only
when its condition fires. This folder explains the stages and trade-offs; installed skill
references own runtime behavior.

These pages explain the rules; installed skill references remain the source of truth for behaviour.

Cross-provider session continuation is owned by the host. Repository files, Git state, feature
artifacts, and explicit handoff prompts remain the durable semantic context.

## Walk this in order

1. [Purpose — delivery and reliability](purpose.md)
2. [The loop — stages from spec to merge](loop.md)
3. [Reviews — three questions, hard caps](reviews.md)
4. [Decisions — two namespaces, halt vs decide](decisions.md)
5. [Guidelines — why each file exists](guidelines.md)
6. [Skills and optional extensions](pack.md)
7. [Repository intelligence](repository-intelligence.md)

## Map

| You want | Read |
| --- | --- |
| The thesis | [purpose.md](purpose.md) |
| Specify → slice → gate → PR | [loop.md](loop.md) |
| Verifier, QA, wtk-deep-review, filed issues | [reviews.md](reviews.md) |
| `AD-NNN` vs architecture invariants | [decisions.md](decisions.md) |
| One paragraph per guideline | [guidelines.md](guidelines.md) |
| What is vendored and what is not | [pack.md](pack.md) |
| Graphify/Graft routing, setup, freshness, and benchmark | [repository-intelligence.md](repository-intelligence.md) |
| Shared execution contracts | [`wtk/references/`](../../.agents/skills/wtk/references/) |
| Surface-specific rules | Installed skill `references/` directories |
| What agents load every turn | [`AGENTS.md`](../../AGENTS.md) |

## The loop at a glance

```
per slice    implement → scoped gate → atomic commit
feature      one fresh Technical Verifier over the complete feature range
resolved     optional wtk-deep-review groups, before QA

feature      selected QA session (no product code)
then         selected full/scoped gate → pull request
```

Public hierarchy: `Feature -> Slice -> Check`. Project-native agent files own model and effort;
`wtk-lean/scripts/workflow_route.py` records provider and role identity when a feature snapshot is
needed. Deep Review is on demand, QA defaults to `auto`, and remediation stops after three stalls.

Repeated review blockers use the immutable fingerprint and independent counter in the installed
`wtk/references/review-rounds.md`; this guide does not duplicate that protocol.

A filed issue skips the ceremony: `implement → scoped gate → one commit`.
Credential-free declarative agent-tool configuration uses the local light path in
[`validation.md`](../../.agents/skills/wtk/references/validation.md).
