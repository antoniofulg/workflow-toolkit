# External Review Runtimes

**Read when:** executing accepted Deep Review jobs through a project-selected external command.

Use the runtime and invocation adopted in project guidelines or explicitly selected for this task.
It runs the selected `deep_review` role from
[agent selection](../../wtk/references/agent-selection.md); a command that cannot run that role
blocks the affected dispatch. No vendor or transport
is required by this skill.

Before starting supporting application/test services, apply
[runtime lifecycle](../../wtk/references/runtime-lifecycle.md). Reviewer isolation does not require
another compatible same-checkout service stack; carry owned-resource evidence across retries.

## Command contract

Execute materialized jobs with the bundled runner from the repository root:

```bash
python3 <skill-dir>/scripts/run_jobs.py --out <out> \
  --command "<project-selected invocation containing {prompt}>"
```

Resolve the invocation from the project's actual runtime instructions; the example is a command
template, not an executable default. `{prompt}` is required; `{output}` and `{label}` are optional.
Each reviewer must write the schema-conforming artifact to the single output path named in its
prompt. Logs are operational evidence, not review output.

The runner consumes the manifest's bounded concurrency, keeps retries in their owning slot,
preserves valid outputs on resume and enforces source freeze. Optional metrics use the existing
execution receipt and available billing evidence; runtime identity alone proves neither cost nor spend.

**Host adapter (optional).** `--metrics-db` feeds `token_metrics.read_telemetry`, which reads one
host's thread-state SQLite database (Codex's `threads` table). It is host-specific: on any other
host, omit `--metrics` or supply an equivalent adapter. Review execution never depends on it.

## Failure handling

- Exit 2: a provider block stopped scheduling; active attempts finish and `run-blocker.json`
  records pending work. Resume the same accepted invocation after the block clears. The default
  pattern, `usageLimitExceeded`, is one host's signal; supply `--block-on` patterns for the
  provider's documented signals.
- Exit 1: inspect `runs/<label>.attempt-*.err` and invalid output artifacts before retrying.
  Repair the failure without dropping unfinished coverage.
- Missing runtime or role: name the gap and stop that dispatch. Never substitute a provider, role,
  model, effort or transport.
