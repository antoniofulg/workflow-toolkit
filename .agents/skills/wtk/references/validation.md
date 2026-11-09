# Gates

**Read when:** selecting validation for the requested change.

The consuming project owns commands: `make check`, when present, is the full gate; a documented
selector is the scoped gate. Select validation by causal impact since the last valid evidence for
each proof or suite, not by file count, task label, commit identity or elapsed time.

## Scope and completion

| Change | Validation |
| --- | --- |
| Documentation maintenance | Accuracy, affected links/headings and whitespace |
| Bounded agent-instruction change | Consistency and an existing relevant contract check |
| Instruction-only skill plus existing installer registration | Metadata/links and the existing package or adoption check for that registration |
| Direct fix, correction or refactor of executable code | Narrowest canonical check covering the affected behavior, then [fix verification](#fix-verification) |
| Mixed documentation and executable change | Canonical tests for the changed executable behavior, then [fix verification](#fix-verification) |
| Feature slice | Named proofs and the scoped gate |
| Closing a task with an e2e surface | The consuming project's scoped e2e gate, filtered by the feature marker |
| Feature close | Fresh full-feature Verifier and the selected local/full gates |

Bounded corrections do not start a feature plan, deep review or QA cycle. A missing UI
selector is reported after the narrowest applicable check, not promoted to full e2e. Escalate only
when evidence identifies a changed contract, shared behavior or risk outside that check's scope.
`wtk` owns routing; `.agents/skills/wtk/references/evidence.md` owns the completion claim.

Creating a skill from decided instructions, registering it in an existing catalog, or correcting
CLI copy is bounded maintenance when it adds no executable skill helper, dependency, hook, expanded
tool authority, data contract, new user interaction or unresolved product decision. The active agent completes it directly.
Use the relevant existing checks once; no mandatory delegation, new plan/checks, fault injection,
QA charters or full-suite run. CLI copy in executable source still gets fix verification. An optional
forward probe needs a concrete uncertainty.

Delivery does not reclassify a bounded change. For a previously verified feature, retain its receipt
and validate the subsequent diff at its own scope; do not reopen the whole branch or recreate closed
artifacts. Escalation names the changed invariant and why the selected check cannot cover it.
Unrelated findings become follow-ups unless they prevent the requested behavior or compromise a
relevant security boundary. Do not grow a maintenance task into a repository certification.

Feature verification still accounts for every approved check, using fresh or demonstrably reusable
evidence. Feature close, review remediation and delivery need no extra local full gate; T2 still gates merge.
Full gates follow the impact conditions below, including at initial feature close.

For reference-driven UI, validate the contract and builder/independent comparison required by
`references/ui-ux.md`, including actual-viewport states and full-page captures. A green behavior
suite cannot waive missing visual evidence or material fidelity failures. QA flags and journeys follow
`../../wtk-qa/references/qa-scenarios.md`; scenario tags scope walks, not automated tests.

## Test tiers

The project declares its commands per tier, and where T2 runs, under `tiers` in its
[settings](project-settings.md); runner tags, filters and shards (for example Playwright
tags and `--shard`, JUnit or NUnit categories, xUnit traits, CTest labels, pytest markers) are
examples, not requirements.

| Tier | When | Runs |
| --- | --- | --- |
| T0 | Every change | Static checks, then affected unit and integration tests, fail-fast. Select them with the project's impact tool or the stack's changed/related selection. |
| T1 | Every PR or push | T0, affected e2e, and a capped `@smoke` cohort (about three minutes or less): the product's critical entry points (e.g. auth, app shell, one core transaction path, where the product has them) and security smoke. |
| T2 | Pre-merge | The full e2e suite, sharded when the runner supports it. Nothing merges without a green T2. |

T2 is a merge requirement, run where the project's delivery runs it; it does not widen the local
validation a change selects below. When impact is unknown, run the full suite under the
[full-gate conditions](#full-gate-conditions-and-failures).
A quarantined flaky test needs an owner, a cap and an expiry (the `quarantine` setting), and the
verification report's `Quarantined tests` line names it at feature close.

## Fix verification

A fresh Verifier checks every refactor, every batch of fixes, and any change touching security,
authentication or authorization, production, deploy or release paths, CI/CD workflows, data or
migrations, regardless of size. An active Lean feature keeps its own Verifier and review loop; only
its Minor-only remediation batch gets this check.

A small local fix skips the Verifier when all hold: it spans one file or a few lines, an existing or
new focused test or the pull request's hosted CI covers it, and it touches none of those areas. Its
author runs the focused tests, lint, typecheck and formatter; hosted CI is the independent check.
A documentation or instruction-only diff and the declarative [configuration](#configuration-and-shared-locks)
change also skip it. Outside these exceptions a builder never certifies its own fix; when the class
is unclear, verify.

The Verifier is a fresh agent that did not build the change. It receives the diff, the defect or
preserved behavior, and the checks, not the builder's conclusions. It reruns the proofs itself,
confirms they fail without the fix where practical, and reads the code connected to the diff. Its
scope matches the diff, so it needs no spec, `verification.md`, full-feature pass, deep review or
QA. A batch gets one Verifier over its whole range; a fix on top of verified work gets one over the
subsequent diff. Under [agent selection](agent-selection.md), a risk-area fix goes to `verifier-risk`; any other to
`verifier`.

After a timeout, the reported line is where the clock ran out, not the cause; find the slow step
from the trace or step timings before proposing a fix. Test a parser of CI or tool output against an
excerpt copied from real output, never a hand-written sample.

Findings use the [review severities](review-rounds.md#finding-shape). Blocking ones go to remediation
commits, and one fresh Verifier checks the whole remediation range, not each commit, halting at three
stalled attempts. A trivial follow-up the Verifier proposed rides with the next batch or qualifies as
a small local fix.

## Run and reuse evidence

Before selecting or repeating tests, compare current inputs with each proof's last green baseline.
Different suites may have different valid baselines. Trace changed files through imports and direct
dependents, then relevant transitive consumers, affected invariants and journeys that use that path.
Include shared fixtures, generated code, dynamic loading, configuration, dependency/lockfile changes,
runtime and shared resource dependencies. Use existing selectors/tools or scoped manual tracing;
missing graph tooling alone does not require building a graph or running the full suite.

Select the corrected finding's regression, the owning module's canonical suite and affected consumer
coverage. Deduplicate overlapping commands; one canonical invocation may cover several obligations.
Declare the causal path or coverage reason for each selected command, not a separate ritual per test.

Reuse prior results only when tested code, relevant transitive dependencies, fixtures, configuration,
resolved dependency versions, command/selector and runtime inputs remain equivalent. Independently
inspect recorded evidence and its inputs; an author's unsupported PASS is insufficient. Documentation,
reports, evidence files, commits and branch names do not invalidate unrelated tests, but documents
consumed as test inputs do. A reused result still needs the runtime/input-equivalence checks above;
otherwise run the selected command directly.

After merging or rebasing main, examine the incoming delta as well as resolved conflicts, overlapping
files and newly connected paths; disjoint files can still interact. Reuse unaffected evidence.
A review finding invalidates evidence on its causal path, not every previously approved module.

For example, fix A and fix B receive their own coverage. If only fix B needs another correction,
rerun its affected checks and retain fix A's evidence.
A shared style or layout primitive expands coverage to the consumers actually affected.

## Full-gate conditions and failures

Run a full gate when the human explicitly requests it or when a conservatively bounded impact scope
cannot cover the change. Examples include shared infrastructure/runtime configuration, dependency
changes or global primitives whose affected consumers cannot be covered by the selected boundaries.
Inspect the actual lockfile/package delta first; merely touching a shared file does not prove global
impact. Name the uncertainty or missing coverage rather than treating an incomplete global graph as
automatic escalation.

If a full run fails in an apparently unrelated test, rerun that test or the smallest relevant cohort
to investigate order, isolation, resources and harness state. An isolated pass alone does not prove
a flake or lack of causality. Preserve the failed full-run result, distinguish suspected instability
from demonstrated flakiness, and record unresolved limits. Do not repeat the full gate automatically,
or report it as green because targeted retests passed. Fixes reselect coverage from their own delta.

## Selection and evidence record

Before a meaningful validation batch, state the delta, reusable evidence and unchanged inputs,
invalidated tests with their causal edges, and the minimal selected commands. A trivial edit can use
one sentence. No new report file or approval step is required.
At completion, record command, `file -> dependency/boundary -> test`, result, reused evidence/baseline
and real limitations in the existing handoff/report. Every affected invariant needs a green proof
or an explicit unresolved limitation; every selected command needs an impact or coverage justification.

Explicit user skips remain a narrow claim with the limitation recorded. Never weaken or skip a test,
or delete one, to make a red gate pass. Removing a redundant test is a separate, reviewed change
under the [test-pruning procedure](test-contract.md#pruning). Never describe a failed/unrun gate as passing. Knowledge checks run with bundle
writes, not as an added feature-delivery gate; dependency inventories are not vulnerability proofs.

## Configuration and shared locks

A declarative configuration change with no code, credential or permission is validated by its own
read-only query of the configured client, with no Verifier. Never take or break another checkout's
lock or queued run.

## Runtime isolation

Before starting or reusing an environment for a gate, apply [runtime lifecycle](runtime-lifecycle.md).
Verify the checkout-owned runtime and changed inputs, reuse compatible same-checkout services and
account for temporary teardown or intentional retention. Avoid concurrent full gates that compete
for the same host resources.
