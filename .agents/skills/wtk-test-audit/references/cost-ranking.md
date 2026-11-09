# Cost ranking

**Read when:** `wtk-test-audit` ranks a suite from CI data.

## Sources

- Pull the job logs of recent pull-request and deploy runs, every attempt included. A single
  attempt hides the retry-passes that define a flake.
- Strip CI timestamps first, then parse the runner's final summary blocks: failed, flaky or passed
  on retry, did not run. Test the parser against a real log excerpt before trusting its counts.

## Aggregation

- Aggregate by file and title, never by line; a line moves with every edit.
- Count per test: retry-passes, failures, distinct branches, runner type and deploy hits.
- Flake rank: distinct branches × events. A failure on only one branch is probably that branch's
  defect; file it there instead of ranking it.
- Duration: the gap between consecutive test start lines × worker count. Rank by median
  worker-seconds; the median survives one cold shard.

## Output

Two rankings, flake and cost, each as `file:line` | test | metric | runs sampled. Record both on
the tracking issue before classifying, so the saving is later measured against them rather than
against the estimate.
