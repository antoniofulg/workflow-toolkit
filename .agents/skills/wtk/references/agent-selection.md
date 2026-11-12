# Agent selection

**Read when:** selecting agents for delegated WTK work, dispatching a stage, or resuming its selection.

## Select only the needed stages

First resolve the task and its proof obligations through `wtk`. Bounded maintenance may stay in the
current session. Before delegating, assess complexity, risk, affected surfaces, required
verification profile and the host's available agent roles. Bounded discovery in the current
session may establish these inputs.

Dispatch by role. Pick each stage's role from the routing table in the user's or project's agent
instructions (for example `implementer`, `implementer-risk`, `verifier`, `verifier-risk`); risk areas
are those of [fix verification](validation.md#fix-verification). Model and effort come from that
role's host agent file. Never choose, override or upgrade them per task. WTK keeps no copy of the
routing table or model names.

State one consolidated table at dispatch:

| Stage | Role | Provider | Model | Effort | Task rationale | Host limitations |
| --- | --- | --- | --- | --- | --- | --- |
| Each needed stage | Role from the routing table | Host | Resolved from the role's agent file or `inherited` | Resolved from the role's agent file or `inherited` | One sentence tied to this task | Named limits, or none |

Selection never reduces the approved profile, checks, QA scope or independence. Omit inapplicable stages, or mark them not run;
do not create an agent or load every skill merely to fill the table.

| Stage key | Responsibility supplied by the selected skill |
| --- | --- |
| `planning` | `wtk-discover`, `wtk-plan` or the Plan/Checks phase of `wtk-lean`, including fresh non-author feature criteria review under [project requirements](project-requirements.md#review-criteria-before-dependent-feature-build) |
| `plan_review` | `wtk-plan-review`, on demand, with reviewers the human picks |
| `exploration` | A bounded read-only trace supporting the selected phase |
| `design` | The relevant design/UI guidance when a design is needed |
| `implementation` | `wtk-lean` Build or `wtk-implement`; one sequential builder |
| `verification` | A fresh non-author session; the complete feature range and every check, or a fix's diff under [fix verification](validation.md#fix-verification) |
| `qa` | One `wtk-qa-plan` or `wtk-qa-execute` phase per packet |
| `deep_review` | `wtk-deep-review`, on demand, with its existing job bounds |
| `remediation` | Authorized fixes under the active workflow and review policy |
| `delivery` | `wtk-ship` within the user's delivery authority |

Record the model and effort each role resolved to, read from its agent file or the host's badge.
When the host exposes neither, record `inherited` and name the unknown field.

## Dispatch without asking

Do not ask the human to approve roles. State the selection and dispatch. A role the human names
wins. The one exception is `plan_review`: the human picks its reviewers.

Reuse a selection for unchanged retries, resume and handoff. If a host lacks the selected role,
stop that dispatch and name the missing role. Never substitute another role, model or effort.

## Freeze a feature selection

For a feature needing a snapshot, write a local selection JSON:

```json
{
  "version": 4,
  "feature": "feature-slug",
  "checkout": "/absolute/path/to/current/checkout",
  "stages": {
    "implementation": {
      "role": "implementer",
      "provider": "host-provider",
      "model": "model-from-role-file",
      "effort": "effort-from-role-file",
      "rationale": "This task needs one sequential coding worker.",
      "limitations": [],
      "scope": "The approved feature checks"
    }
  }
}
```

Replace the example values with the actual role and the settings it resolved to.
`checkout` is the resolved current checkout path. Include only selected stage keys from the table.
Each stage requires nonempty role, provider, model, effort and rationale plus a list of nonempty named
limitations; `scope` is an optional nonempty string. The provider names the actual project-selected
host mechanism; the snapshot does not impose a vendor list. For `model: inherited` or
`effort: inherited`, include a limitation starting with `model:` or `effort:` respectively,
stating what is inherited and unknown.

```sh
python3 .agents/skills/wtk-lean/scripts/workflow_route.py \
  --root . --feature feature-slug --selection-file /path/to/selection.json
```

Exit 0 returns a version 4 `workflow.json` with the exact stages, feature/checkout scope, Git
revision, approved verification profile, sequential builder and on-demand Deep Review.
Exit 2 rejects malformed, stale, foreign or unsafe input without replacing prior state.
Resume with the same command or omit `--selection-file` to validate and reuse the frozen snapshot.
`--slices` and `--verification-profile` are assertions; `--refresh` recomputes snapshot metadata
from checks using a selection file. Stale schemas require an explicitly replaced selection;
there is no migration or native-file routing mode. Existing native files stay untouched.

## Dispatch and report

Before each dispatch, revalidate feature/checkout scope and current support for its selected row.
Pass the selected stage's skill, approved artifacts, bounded responsibility and current checkout to
the selected role. If the host lacks the role, apply the missing-role rule above.

A fresh session supplies independent context in the current checkout. Keep that checkout for
handoffs and checking; a separate checkout needs a concrete approved exception. Controlled
fault-injection scratch follows the existing verification proof and is discarded after use.
Freeze author edits while independent checking evaluates the complete approved revision/range.

When the project opts into metrics, return the [execution receipt](execution-metrics.md) with
actual provider/model/effort when exposed, identity, interval, source/scope, counters and missing
coverage. Record inherited or unknown settings explicitly. No receipt field, proof obligation or review cadence changes here.
