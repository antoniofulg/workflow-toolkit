# External Review Runtimes

**Read when:** executing accepted Deep Review jobs through a project-selected external command.

Use the runtime and invocation adopted in project guidelines or explicitly selected for this task.
Verify its advertised model/effort controls against the accepted `deep_review` row from
[agent selection](../../wtk/references/agent-selection.md). A command that cannot represent that
row blocks the affected dispatch; changing it needs targeted acceptance. No vendor or transport
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

## Failure handling

- Exit 2: a provider block stopped scheduling; active attempts finish and `run-blocker.json`
  records pending work. Resume the same accepted invocation after the block clears. Supply
  `--block-on` patterns when the provider's documented signals differ.
- Exit 1: inspect `runs/<label>.attempt-*.err` and invalid output artifacts before retrying.
  Repair the failure without dropping unfinished coverage.
- Missing runtime or unsupported model/control: name the gap and follow agent selection's targeted
  decision branch. Never substitute a provider, model, effort or transport silently.
