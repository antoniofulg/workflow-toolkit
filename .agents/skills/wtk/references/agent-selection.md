# Agent selection

**Read when:** selecting agents for delegated WTK work, dispatching a stage, or resuming its selection.

## Select only the needed stages

First resolve the task and its proof obligations through `wtk`. Bounded maintenance may stay in the
current session. Before delegating, assess complexity, risk, affected surfaces, required
verification profile and the host's actual provider/model/effort controls. Bounded discovery in the
current session may establish these inputs.

Use currently advertised host capabilities. If availability or a model's properties need checking,
consult current official documentation through the project's documentation lookup policy. Record
the capability source and date in the existing handoff. Select a capable model and effort for each
task; do not keep a permanent model ranking, price registry or named-role preset as the authority.
When generic dispatch supports the requested settings, use it instead of an obsolete role preset.

State one consolidated table at dispatch:

| Stage | Provider | Model | Effort | Task rationale | Host limitations |
| --- | --- | --- | --- | --- | --- |
| Each needed stage | Advertised provider | Exact available model or `inherited` | Supported effort or `inherited` | One sentence tied to this task | Named limits, or none |

Explain the tradeoff using the task: bounded tracing can use less effort; cross-surface changes,
security boundaries and independent verification may need more. Selection never reduces the
approved profile, checks, QA scope or independence. Omit inapplicable stages, or mark them not run;
do not create an agent or load every skill merely to fill the table.

| Stage key | Responsibility supplied by the selected skill |
| --- | --- |
| `planning` | `wtk-discover`, `wtk-plan` or the Plan/Checks phase of `wtk-lean`, including fresh non-author feature criteria review under [project requirements](project-requirements.md#review-criteria-before-dependent-feature-build) |
| `exploration` | A bounded read-only trace supporting the selected phase |
| `design` | The relevant design/UI guidance when a design is needed |
| `implementation` | `wtk-lean` Build or `wtk-implement`; one sequential builder |
| `verification` | A fresh non-author session; the complete feature range and every check, or a fix's diff under [fix verification](validation.md#fix-verification) |
| `qa` | One `wtk-qa-plan` or `wtk-qa-execute` phase per packet |
| `deep_review` | `wtk-deep-review`, on demand, with its existing job bounds |
| `remediation` | Authorized fixes under the active workflow and review policy |
| `delivery` | `wtk-ship` within the user's delivery authority |

The current coordinator's model/effort may be fixed by its host session. State the actual settings
when exposed and that limitation in the selection table. Requested settings apply only to supported
subsequent dispatches. If a control is unavailable, use explicit `inherited` configuration and name
the uncontrolled field.

## Dispatch without asking

Do not ask the human to approve provider, model or effort. State the selection and dispatch. A
choice the human names wins: preserve it exactly and check its current host support.

Reuse a selection for unchanged retries, resume and handoff. If a selected setting is unsupported,
choose a supported one and state the change; if the human named it, stop that dispatch, name the
missing control or model, and ask for a supported choice. Never silently substitute another
provider, model, effort, runtime or role preset.

## Freeze a feature selection

For a feature needing a snapshot, write a local selection JSON:

```json
{
  "version": 3,
  "feature": "feature-slug",
  "checkout": "/absolute/path/to/current/checkout",
  "stages": {
    "implementation": {
      "provider": "host-provider",
      "model": "host-advertised-model",
      "effort": "host-supported-effort",
      "rationale": "This task needs one sequential coding worker.",
      "limitations": [],
      "scope": "The approved feature checks"
    }
  }
}
```

Replace the example values with the actual choices; they are not model recommendations.
`checkout` is the resolved current checkout path. Include only selected stage keys from the table.
Each stage requires nonempty provider, model, effort and rationale plus a list of nonempty named
limitations; `scope` is an optional nonempty string. The provider names the actual project-selected
host mechanism; the snapshot does not impose a vendor list. For `model: inherited` or
`effort: inherited`, include a limitation starting with `model:` or `effort:` respectively,
stating what is inherited and unknown.

```sh
python3 .agents/skills/wtk-lean/scripts/workflow_route.py \
  --root . --feature feature-slug --selection-file /path/to/selection.json
```

Exit 0 returns a version 3 `workflow.json` with the exact stages, feature/checkout scope, Git
revision, approved verification profile, sequential builder and on-demand Deep Review.
Exit 2 rejects malformed, stale, foreign or unsafe input without replacing prior state.
Resume with the same command or omit `--selection-file` to validate and reuse the frozen snapshot.
`--slices` and `--verification-profile` are assertions; `--refresh` recomputes snapshot metadata
from checks using a selection file. Stale schemas require an explicitly replaced selection;
there is no migration or native-file routing mode. Existing native files stay untouched.

## Dispatch and report

Before each dispatch, revalidate feature/checkout scope and current support for its selected row.
Pass the selected stage's skill, approved artifacts, bounded responsibility and current checkout to
the existing host mechanism, using its real model/effort controls. A named role is optional only
when it can honor the exact selected settings; its preset cannot override the selection. If the
host cannot honor the row, apply the unsupported-setting rule above.

A fresh session supplies independent context in the current checkout. Keep that checkout for
handoffs and checking; a separate checkout needs a concrete approved exception. Controlled
fault-injection scratch follows the existing verification proof and is discarded after use.
Freeze author edits while independent checking evaluates the complete approved revision/range.

Return the existing [execution receipt](execution-metrics.md) with actual provider/model/effort
when exposed, identity, interval, source/scope, counters and missing coverage. Record inherited or
unknown settings explicitly. No receipt field, proof obligation or review cadence changes here.
