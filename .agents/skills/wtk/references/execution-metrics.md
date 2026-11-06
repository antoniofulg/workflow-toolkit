# Execution metrics

**Read when:** the project's `AGENTS.md` opts into execution metrics and implementation,
verification, QA, review, or delivery starts; report below the normal completion summary,
including a stop at the PR or a blocked handoff. Without that declaration, collect nothing.

## Collect during work

The coordinator keeps compact receipts in session state or existing disposable runtime storage;
no tracked metrics artifact, benchmark suite, new gate, or approval step is required. Capture a
clock timestamp and usage baseline at task start and each stage start; take a snapshot at each
stage end, retaining counter timestamps and the last-read time. If collection starts late or state
is lost, name the measured interval and missing coverage instead of reconstructing it from memory.

Before dispatch, give each worker the stage and attempt plus this reference. Each worker returns
its actor/session id, provider/model and billing tier when exposed, start/end timestamps, usage
counters and their source/scope, commands with reported durations, and outcome in its normal handoff. The coordinator
records dispatch/completion boundaries when workers cannot measure their own interval. Include
baseline/snapshot counters (input, cached input, output, total), measurement interval,
last-read time, harness version, scope (self-only or inclusive of children), reset status and missing
coverage. Reuse existing tool timing and telemetry; do not poll, start agents or add turns solely to collect metrics.

Classify initial implementation, technical verification, QA, Deep Review, remediation, and
delivery/readiness separately. Attribute fix work to remediation, not initial implementation;
rechecks stay in the relevant verification/review stage. Include planning/setup or unclassified
time when present rather than silently assigning it to implementation. Count each completed review
pass as one round (initial and remediation passes separately), not each reviewer job or finding;
show interrupted passes separately. Count fix batches and full/targeted gate invocations, including
failed attempts. A cache hit or reused result is not a new test execution.

## Verification–fix loops

Start counting at the builder's first ready-for-verification handoff. Record the checked revision,
stage (technical verification, QA, or Deep Review), actual builder and checking models/efforts when
known, verdict, and confirmed finding ids using the existing finding ledger. Keep these receipts
in the same session state; neither this count nor model comparison changes review/stall policy.

A verdict requiring implementation changes opens one return-to-implementation event. One completed
loop is that return followed by a fix batch and its completed recheck, whether the recheck passes
or fails. A failing recheck can open the next return. Report returns, completed loops and pending
returns separately; interrupted checks, same-code retries, individual findings and parallel reviewer
jobs are not extra loops. Consolidate findings handled by one fix/recheck batch into one loop, with
all originating stages listed. No verification run means first-pass acceptance is `not evaluated`.

For each loop, distinguish newly discovered findings, previously open findings still unresolved,
and regressions of findings previously proven fixed. Newly discovered does not automatically mean
introduced by the fix; attribute that only with evidence. Record the fixing model separately when
it differs from the initial builder, plus fix/recheck time and tokens when available; these are
subtotals of stage costs, not additional cost. Scope changes and tooling blockers are separate reasons,
not implementation defects. Keep finding severity and verification scope beside model comparisons:
fewer loops alone does not establish a better model or justify reducing verification coverage.
Report passes and first-pass acceptance by checking stage; overall first-pass acceptance requires
every required initial checking stage to finish without an implementation return.

Example: ready -> check fails A -> fix -> recheck fails B -> fix -> recheck passes means three
completed verification passes, two returns, two completed loops, zero pending, and no first-pass
acceptance. If B is a new finding while A passed its retest, distinguish it from a failed fix for A.

## Accounting boundaries

- Use actual clock/tool measurements. Total elapsed runs from task start to the reported stopping
  point, not to a merge that has not happened. Stage durations may overlap across actors; report
  cumulative actor time separately and never sum it as feature lead time. Waiting is an annotated
  portion of elapsed time, not an extra duration to add.
- Cumulative actor time sums only supplied, non-overlapping intervals per actor. A task-wide token
  aggregate does not establish a coordinator work interval. Missing intervals make the actor total
  partial; stopping at the requested PR does not itself make the measured task interval partial.
- Gate durations are included in their owning stage and shown separately as overhead; do not add
  them again. Distinguish measured command duration from dispatch-to-return elapsed time.
- Aggregate only proven disjoint session/usage scopes. Record whether parent counters include
  children; never add those parent counters to child receipts. If inclusion is unknown, retain
  separate measurements without a combined total. Name missing participating agents and mark
  aggregates partial. Existing Deep Review aggregates cover their run, not individual jobs/stages.
- Never infer consumed tokens from context budgets, character counts, bytes/4 context estimates
  or benchmark medians. Normalize input to include cache reads/writes once; some providers report
  these as separate buckets. Reasoning may be part of output. Retain raw provider definitions.
- Missing metrics never block delivery or trigger reruns. Use `not run` for an omitted stage and
  `unavailable` for an unmeasured field. A numeric zero requires measured or known-zero activity.

## Token collection procedure

Before declaring tokens `unavailable`, check environment counters, local telemetry for the current
session, then receipts of participating subagents. Record each source's scope or concrete failure;
`the tools do not show usage` is insufficient while local telemetry remains unchecked. Missing
identity, corresponding file not found, absent usage events and unverifiable counter scope are
valid reasons. An unavailable stage delta does not make a measured session cumulative unavailable.

For Codex, Claude Code or Cursor, read the matching section in [harness metrics](execution-metrics-harnesses.md)
before the stage baseline or worker dispatch. Its source/scope rules apply to the same receipt format;
the supplied file reader supports Codex only. Reuse existing supplied payloads, streams and telemetry; do not install hooks/exporters, start sessions, or enable content logging for metrics.

Record whether usage is cumulative, per-request, per-turn or an exported delta. Sum only distinct
finalized requests/turns or delta records; never add their cumulative aggregate too. Current context
occupancy is not session consumption, even when its field name includes `total`.
Subtract baseline from snapshot only for comparable cumulative counters in the same session,
source and scope. Check all counter buckets for decreases, resets and changes of scope, including resets between
endpoints. A reset or lost baseline prevents the stage delta; missing buckets prevent their deltas.
Without a reliable baseline, report the measured session cumulative (or post-reset cumulative),
explicitly labeled; it is not stage consumption. A provider source/model/scope change requires a new baseline and separate receipt.

## Optional token cost

Report three separate results: measured tokens, estimated token cost and actually billed amount.

Calculate cost only for usage scopes with a known provider/model, billable token breakdown and
applicable official rates. When providers hide usage or model identity, report `unavailable` and
skip price lookup for that scope. Missing cost never blocks delivery or requests credentials.

For priceable scopes, consult the provider's current official pricing once and cite its URL,
retrieval date, currency, rates and applicable service tier/context band. For OpenAI, start at
https://developers.openai.com/api/docs/pricing; for other providers use their own official pricing.
Do not hardcode a changing rate table in the skill or assume a tier, discount or cache policy.

Normalize usage into disjoint billable buckets following that provider's definitions, then compute
`sum(bucket_tokens * bucket_rate_per_million) / 1_000_000`. If input includes cached reads and
separately billed cache writes, subtract those subsets before pricing ordinary input; providers
that already separate buckets need no subtraction. Apply distinct rates for cache reads/writes,
output and applicable tiers. Unknown bucket splits or mixed-model/tier aggregates are unpriceable
unless verifiable attribution and the needed breakdown per model/tier are supplied. Use a calculator
or existing runtime for arithmetic.

Show estimated token cost per measured stage/model and fix loop where attribution exists; loop
costs remain subtotals, not extra charges. Sum only disjoint priced scopes and label partial totals
with the missing coverage. Retain precision until the final display. Exclude and name unmeasured
tool, storage, image/audio, infrastructure, tax and other non-token charges; this is not an invoice.
For subscription usage, label it `API-equivalent estimate`, not actual spend. Actual billed amounts
may be shown separately only when supplied by task-scoped billing evidence. If nothing is priceable,
one `Token cost: unavailable — <missing inputs>` line is enough; omit empty cost tables.

## Final footer

Always report the overall result and a compact stage table below the delivery result, including
partial or blocked work. Workers return scoped receipts; the coordinator consolidates them.
Keep existing test results, limitations, artifact links and authorization/stopping status intact.

- Overall: show task elapsed time, cumulative actor time and the measured token total or known
  subtotal, each with complete/partial coverage. Name excluded actors/intervals and unallocated
  session usage. If scopes cannot be combined, show their separate totals and the concrete overlap
  uncertainty; missing complete coverage does not erase an available measured subtotal.
- Stages: show observed elapsed time and token count for implementation, checking and each recheck,
  remediation, QA and other stages actually performed. Identify each count as a comparable delta,
  session cumulative or unavailable, with its measured interval and missing coverage. A combined
  verification/QA receipt stays combined until separate timings/counters exist; never invent a split.
- Totals: sum only proven disjoint scopes/intervals. A subtotal excludes missing or unverifiable
  usage; session cumulative counts and subsequent deltas may be combined only when their coverage
  is demonstrably non-overlapping. Neither their components nor parent-inclusive totals are added
  again. Stage durations are not task lead time when actors overlap or waiting exists.

Keep this summary in the final response; a receipt fragment or a report link alone does not replace
it. Match token and timing coverage explicitly when their observed intervals differ.

```text
Execution metrics — measured interval: <start -> stop; complete or partial>
Stage                    Elapsed       Tokens (total; input / cached input / output)    Rounds
Implementation           ...           ...                                       ...
Technical verification   ...           ...                                       ...
QA                       ...           ...                                       ...
Deep Review              ...           ...                                       initial / remediation
Remediation              ...           ...                                       fix batches
Delivery/readiness       ...           ...                                       ...
Total elapsed: ... | Cumulative actor time: ... | Token total or known subtotal: ... [coverage/source]
Estimated token cost: ... [currency; priced scopes/coverage; rates/source/date, or unavailable]
Actually billed: ... [task-scoped billing evidence, or unavailable — no billing evidence]
Validation overhead (included above): full gates ... runs / ...; targeted ... runs / ...
Reused evidence: ... | Waiting/blockers: ... | Unmeasured scope: ...
Verification cycles: ... passes | ... returns | ... completed loops | ... pending | first-pass: ...
Loop <n>: <stage; revision; builder -> checker; fixing model if changed; verdict>
  Findings: ... new / ... unresolved / ... regressed | Fix + recheck: ... time / ... tokens / ... cost
Optimization: <observed avoidable cost and suggested adjustment, or insufficient evidence>
```

Keep the existing receipt fields; attach per-stage measurement/coverage notes and put session ids,
intervals, baseline/snapshot counters and event/last-read timestamps in the source/coverage detail.
Always retain the overall summary and performed-stage rows; omit only inapplicable stages or empty
optional detail.
Optimization claims need an observed
cause (for example duplicate validation or repeated setup); elapsed time alone does not prove waste.
Label potential savings as estimates. This is a task receipt, not a comparative benchmark.
