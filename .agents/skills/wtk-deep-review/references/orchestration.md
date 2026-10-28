# Orchestration

The pipeline stage map, cohort planning rules, sweep triggers, and the execution engines. Prompt wording is single-sourced in `assets/PROMPT.md` (rendered by `build_jobs.py`); output shape in `assets/findings.schema.json` — this file explains how the stages compose and how jobs get executed.

## Pipeline — stages, gates, artifacts

Every stage materializes jobs with lane ownership (`{label, kind, lane, prompt, output, required_hunks, rule_ids}`), executes them on any engine, and passes a script gate. Valid outputs are preserved, so re-running touches only missing or invalid work.

| Stage | Produce | Execute | Gate (exit 0) |
| --- | --- | --- | --- |
| Knowledge | `build_knowledge.py` → knowledge.json + rules.template.json | — | source discovery |
| Plan | `build_jobs.py` → prompts + jobs.json | — | source accounting + ownership |
| Review | — | jobs.json (defect cohorts plus opt-in sweeps) | `run_jobs.py --validate-only` |
| Merge | `merge_findings.py` → findings.json + review-stats.json | — | complete defect-lane coverage |
| Report | `render_review.py` → review.md + state.json; `render_html.py` → review.html | — | `render_review.py` |

Both job kinds (`cohort`, `sweep`) return the same schema: defects, advisories, objective suppressions, hunk coverage, and explicit rule accounting. `hunk` is the assigned canonical range (`<side>:<start>-<end>`), null outside the diff. Defects use the causal certificate; advisories use the improvement certificate.

## Cohort rules (Step 2)

1. Group selected files by package/directory and domain: a source file, its tests, and its types travel together; a file pulled apart from its test loses its reviewer the cheapest evidence.
2. For a small selection (≤40 files and ≤1,500 changed lines), prefer one defect cohort when the configured `--max-cohort-files` and existing line limits permit. Use extra cohorts only when an actual engine limit requires them or a named independent high-risk boundary justifies them; record the count and concrete reason in `walkthrough.md` before dispatch.
3. Otherwise target ~400 changed lines per cohort, so at most `min(concurrency, ceil(changed_lines / 400))` cohorts (fewer is allowed), each ≤ `--max-cohort-files` files (default `100`) **and** ≤ ~6,000 changed lines. Pass the same value to `build_jobs.py`; a single oversized file becomes its own cohort. Keep every exception within the current validator caps.
4. **Oversized-file split** — when one file alone exceeds ~6,000 changed lines, divide the search across sibling reviewers: same file, disjoint slices of its manifest hunks (`hunk_scope`), one cohort per slice. Every slice reviewer reads the whole file for context but judges only its slice; build_jobs.py proves the merged slices cover every hunk line exactly once.
5. Tag each cohort `risk: high|normal|low` — high when it touches storage/migrations, security/auth, public contracts, or concurrency; low for docs/config-only. Risk feeds reviewer emphasis, not selection.
6. Every selected file in exactly one cohort (or, when sliced, every hunk line in exactly one slice) — build_jobs.py rejects any other shape. `plan.json`:

```json
{ "cohorts": [
    { "id": "c01", "name": "store: task queue", "risk": "high",
      "files": ["internal/store/queue.go", "internal/store/queue_test.go"] },
    { "id": "c02a", "name": "loop/action.go — hunks 1-14", "risk": "high",
      "files": ["internal/loop/action.go"],
      "hunk_scope": { "internal/loop/action.go": [{"start": 12, "lines": 40, "side": "new"}] } }
  ],
  "sweeps": ["contracts", {"key": "layering", "lens": "custom lens text"}] }
```

Sweeps are bare keys from the table below (built-in lens text) or `{key, lens}` objects for a custom lens.

When `manifest.mode` is `incremental` (a remediation check), `build_jobs.py` ignores `cohorts` and `sweeps` (printing `sweeps skipped in incremental mode` when any were planned) and emits one defect-lane job `cohort-rc` over every selected path, carrying `prior_fingerprints` and `prior_anchors` for every `open` ledger entry in `state.json`; the gate demands one `prior_findings` row per fingerprint and rejects a defect at a prior anchor. Write `plan.json` as usual.

`build_jobs.py` remains authority for the numeric target and per-cohort caps: it rejects a plan with more cohorts than the current target and prints `cohort target: E for L changed lines at concurrency C`. Merge over-split cohorts; do not change or invent a cap in the plan.

## Sweep triggers

Defect cohorts are the only default review lane. Sweeps remain **opt-in and rare** — default to none. Each sweep is one extra agent that sees the manifest, not one cohort; include it only when its trigger clearly fires and the plan has three or more cohorts (`build_jobs.py` rejects sweeps on smaller plans), and prefer at most one or two per round:

| Key | Trigger | Looks for |
| --- | --- | --- |
| `contracts` | exported/wire/API symbol changed contract | breaking changes, drift between spec/impl/clients, missing codegen co-ship |
| `security` | new endpoint/input path/authz surface/secret handling | injection, missing authn/authz, secret leakage, cross-tenant access |
| `migrations` | schema/migration files in diff | destructive ops, missing migration for model change, ordering/identity hazards |
| `consistency` | renames or repeated patterns in diff | incomplete renames, sibling paths not mirroring a fix, duplicated logic |
| `config` | config keys/flags/env vars changed | unwired or undocumented keys, dead flags, default mismatches |

## Engines

The jobs contract makes engines interchangeable. Use the project-selected mechanism, record its actual name in context-pack.md, and always close the loop with `run_jobs.py --validate-only`. Validation rejects missing coverage rows, in-diff anchors outside job ownership, and unassigned rule ids.

**Skill-directed dispatch.** Follow [agent selection](../../wtk/references/agent-selection.md)
before proposed reviewer work. Use the accepted `deep_review` row and materialized prompts with
the host's supported model/effort controls in the current checkout. The skill supplies review
responsibilities; a named native role is optional only when it honors those exact settings.
Prefer a supported generic dispatch over a stale named-role preset. Missing controls or a provider
block stop the affected dispatch; changing settings requires targeted acceptance.
Keep manifest concurrency and worker-slot retries; after a provider block, active attempts finish
and pending slots are not refilled.

Metrics are optional provider-neutral hooks. An adapter may call `start_metrics`,
`checkpoint_metrics`, and `finalize_metrics` around the bounded dispatch; the main thread records
serialized cumulative snapshots only and never assigns overlapping deltas to jobs or changes exits.
Record the actual engine in context-pack.md, then run the validate-only gate. Provider-specific
telemetry setup belongs in the runtime adapter guidance, not in this orchestration contract.

Collect repository maps, symbol/caller traces or architecture evidence only when the review needs
them, using project-selected inspection tools or ordinary repository inspection. Put relevant
evidence in context-pack.md and verify it against the frozen checkout. Prompt materialization
does not invoke third-party inspection tools or require tool-specific artifacts.

**Host dispatch.** Pass each pending job its materialized prompt and single output path through
the project's available dispatch capability. Repository files remain read-only. Apply the pinned
concurrency and refill rules below. If the host inherits model/effort instead of exposing controls,
obtain acceptance of those named limitations first. Generic prompt dispatch is sufficient; pass
no unsupported role argument. After dispatch, run the validate-only gate and resume only pending
or invalid jobs with unchanged accepted choices. Inspect a failing output after two re-dispatches
without progress.

**External commands.** Use `run_jobs.py --command` with the project-selected runtime and accepted
row, following [external runtime guidance](subagent-runtimes.md). The runner owns bounded execution,
retries, output validation, provider-block detection and the freeze check.

The orchestrator never reviews inline, regardless of PR size: reviewers spend their own context on their cohort; the orchestrator plans, dispatches, gates, and reports.

### Bounded dispatch

The manifest builder resolves reviewer concurrency once, with precedence `--concurrency N` over
`.wtk-deep-review.yaml` over the default `3`, validates `1` through `6`, and pins the result in
`manifest.json`. Every execution engine consumes that pinned value. It launches up to
`min(concurrency, pending jobs)`, refills a worker slot after completion, and never schedules a
new job after the first provider block. Active attempts finish; pending and blocked jobs remain in
the blocker ledger. Results are stored by label and emitted in jobs-file order, regardless of
completion order. The removed legacy `--workers` option is rejected.
