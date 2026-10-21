# Agent selection

**Read when:** proposing delegated WTK work, dispatching a stage, or resuming its approved selection.

## Recommend only the needed stages

First resolve the task and its proof obligations through `wtk`. Bounded maintenance may stay in the
current session. Before proposed delegation, assess complexity, risk, affected surfaces, required
verification profile and the host's actual provider/model/effort controls. Bounded discovery in the
current session may establish these inputs; it does not authorize the proposed agents.

Use currently advertised host capabilities. If availability or a model's properties need checking,
consult current official documentation through the project's documentation lookup policy. Record
the capability source and date in the existing handoff. Select a capable model and effort for each
task; do not keep a permanent model ranking, price registry or named-role preset as the authority.
When generic dispatch supports the requested settings, use it instead of an obsolete role preset.

Present one consolidated table before dispatch:

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
| `verification` | A fresh non-author session; the complete feature range and every check |
| `qa` | One `wtk-qa-plan` or `wtk-qa-execute` phase per packet |
| `deep_review` | `wtk-deep-review`, on demand, with its existing job bounds |
| `remediation` | Authorized fixes under the active workflow and review policy |
| `delivery` | `wtk-ship` within the user's delivery authority |

The current coordinator's model/effort may be fixed by its host session. State the actual settings
when exposed and that limitation in the proposal. Requested settings apply only to supported
subsequent dispatches. If a control is unavailable, propose explicit `inherited` configuration and
name the uncontrolled field; human acceptance of that limitation is required before dispatch.

## Wait for the human decision

Treat the proposal as pending until an actual user reply accepts it or specifies replacements.
Silence, timeout, a suggested table and plan approval alone are not acceptance of execution choices.
While pending, dispatch none of the proposed agents and persist no executable approved route.
Preserve human overrides exactly and check their current host support before marking them confirmed.

Confirm the initial table once. Reuse accepted choices for unchanged retries, resume and handoff.
For changed rows or stage scope, present only the change and obtain its targeted acceptance;
unchanged rows retain their earlier approval. Unsupported settings remain blocked: name the missing
control/model, offer supported alternatives or inherited settings, and wait for the affected choice.
Never silently substitute another provider, model, effort, runtime or role preset.

## Freeze a feature selection

For a feature needing a snapshot, write a local selection JSON only after observing acceptance:

```json
{
  "version": 2,
  "feature": "feature-slug",
  "checkout": "/absolute/path/to/current/checkout",
  "stages": {
    "implementation": {
      "provider": "codex",
      "model": "host-advertised-model",
      "effort": "host-supported-effort",
      "rationale": "This task needs one sequential coding worker.",
      "limitations": [],
      "scope": "The approved feature checks"
    }
  },
  "approval": {
    "status": "confirmed",
    "reference": "Exact user reply or its durable reference accepting these rows",
    "stages": {
      "implementation": {
        "provider": "codex",
        "model": "host-advertised-model",
        "effort": "host-supported-effort",
        "rationale": "This task needs one sequential coding worker.",
        "limitations": [],
        "scope": "The approved feature checks"
      }
    }
  }
}
```

Replace the example values with actual accepted choices; they are not model recommendations.
`checkout` is the resolved current checkout path. Include only selected stage keys from the table.
Each stage requires nonempty provider, model, effort and rationale plus a list of nonempty named
limitations; `scope` is an optional nonempty string. Providers use existing `claude`, `codex` or
`cursor` host mechanisms. For `model: inherited` or `effort: inherited`, include a limitation
starting with `model:` or `effort:` respectively, stating what is inherited and unknown.

`approval.stages` must exactly match the accepted rows, including scope and limitations. The
reference records the observed human decision; for a targeted change, cite both prior acceptance
and the new changed-row reply. A changed selection requires a fresh reference. This is a procedural
claim, not authentication: local JSON cannot prove human identity or host support. The coordinator
must have the actual reply and check the host before asserting approval or dispatching.

```sh
python3 .agents/skills/wtk-lean/scripts/workflow_route.py \
  --root . --feature feature-slug --selection-file /path/to/confirmed-selection.json
```

Exit 0 returns a version 2 `workflow.json` with the exact stages and approval, feature/checkout
scope, Git revision, approved verification profile, sequential builder and on-demand Deep Review.
Exit 2 rejects malformed, unconfirmed, stale, foreign or unsafe input without replacing prior state.
Resume with the same command or omit `--selection-file` to validate and reuse the frozen snapshot.
`--slices` and `--verification-profile` are assertions; `--refresh` recomputes snapshot metadata
from checks using a confirmed selection. Stale schemas require an explicitly replaced selection;
there is no migration or native-file routing mode. Existing native files stay untouched.

## Dispatch and report

Before each dispatch, revalidate feature/checkout scope and current support for its accepted row.
Pass the selected stage's skill, approved artifacts, bounded responsibility and current checkout to
the existing host mechanism, using its real model/effort controls. A named role is optional only
when it can honor the exact accepted settings; its preset cannot override the selection. If the
host cannot honor the row, stop that dispatch and follow the targeted decision branch above.

A fresh session supplies independent context in the current checkout. Keep that checkout for
handoffs and checking; a separate checkout needs a concrete approved exception. Controlled
fault-injection scratch follows the existing verification proof and is discarded after use.
Freeze author edits while independent checking evaluates the complete approved revision/range.

Return the existing [execution receipt](execution-metrics.md) with actual provider/model/effort
when exposed, identity, interval, source/scope, counters and missing coverage. Record inherited or
unknown settings explicitly. No receipt field, proof obligation or review cadence changes here.
