# Project settings

**Read when:** a WTK procedure needs a project-declared command, path or policy listed below, or
setup records them.

A project declares its WTK settings in one optional `## wtk-settings` section of its `AGENTS.md`.
It is Markdown that agents read, not a configuration file: no parser, no TOML. Every key is
optional; an absent key takes the default shown. The Lean `profile` stays under `## wtk-lean`.

```markdown
## wtk-settings

- tiers: T0 `<command>` · T1 `<command>` · T2 `<command>`, run in CI
- mutation: `<command scoped to changed files>`; break threshold 80% on changed files
- quarantine: owner @team-quality; cap 5 tests; expiry 14 days
- qa root: `docs/qa/`
- compatibility: semver on the public API; deprecation window one minor release
- language: English for versioned text
- commit validator: `<command>`
- execution metrics: on
- merge: stop at the pull request; two approving reviews
- test-review scopes: billing page = `src/billing/`, `tests/billing/`
- test-audit: logs `<CI run log source>`; summary `<runner summary format>`; component `<path>` · integration `<path>` · e2e `<path>`; lanes `<shard layout, workers>`
```

| Key | Used by | Default when absent |
| --- | --- | --- |
| `tiers` | [Test tiers](validation.md#test-tiers), `wtk-ship`, `wtk-test-review`, `wtk-test-audit` | The stack's own test commands; T2 is the full e2e suite wherever delivery runs it |
| `mutation` | [Mutation](test-contract.md#mutation), `wtk-test-review` | Manual faults; no numeric threshold |
| `quarantine` | [Test tiers](validation.md#test-tiers), the verification report | No quarantine; a flaky test is a failure |
| `qa root` | [QA scenarios](../../wtk-qa/references/qa-scenarios.md) | `docs/qa/` |
| `compatibility`, `language` | [DX](dx.md) | Ask before a breaking removal; English artifacts |
| `commit validator` | Lean [build](../../wtk-lean/references/build.md) | `check_commit.py` |
| `execution metrics` | [Execution metrics](execution-metrics.md) | Off |
| `merge` | `wtk-ship` | Ship authorizes push, one pull request and merge; branch protection and required checks still apply |
| `test-review scopes` | `wtk-test-review`, `wtk-test-audit` | Scope paths found by tracing the code |
| `test-audit` | `wtk-test-audit` | The hosting provider's run logs, the runner's own summary, test roots traced from the code, one lane |
