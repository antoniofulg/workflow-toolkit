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
| Direct behavior-preserving correction | Narrowest canonical check covering the affected behavior |
| Mixed documentation and executable change | Canonical tests for the changed executable behavior |
| Feature slice | Named proofs and the scoped gate |
| Closing a task with a browser surface | The consuming project's browser scoped gate, filtered by `@feature:<slug>` |
| Feature close | Fresh full-feature Verifier and the selected local/full gates |

Bounded corrections do not start a feature plan, Verifier, deep review or QA cycle. A missing UI
selector is reported after the narrowest applicable check, not promoted to full e2e. Escalate only
when evidence identifies a changed contract, shared behavior or risk outside that check's scope.
`wtk` owns routing; `.agents/skills/wtk/references/evidence.md` owns the completion claim.

Creating a skill from decided instructions, registering it in an existing catalog, or correcting
CLI copy is bounded maintenance when it adds no executable skill helper, dependency, hook, expanded
tool authority, data contract, new user interaction or unresolved product decision. The active agent completes it directly.
Use the relevant existing checks once; no mandatory delegation, new plan/checks, fault injection,
Verifier, QA charters or full-suite run. An optional forward probe needs a concrete uncertainty.

Delivery does not reclassify a bounded change. For a previously verified feature, retain its receipt
and validate the subsequent diff at its own scope; do not reopen the whole branch or recreate closed
artifacts. Escalation names the changed invariant and why the selected check cannot cover it.
Unrelated findings become follow-ups unless they prevent the requested behavior or compromise a
relevant security boundary. Do not grow a maintenance task into a repository certification.

Feature verification still accounts for every approved check, using fresh or demonstrably reusable
evidence. Feature close, review remediation and delivery do not automatically require a full gate.
Full gates follow the impact conditions below, including at initial feature close.

For reference-driven UI, include the comparison required by `references/ui-ux.md`. QA flags and journeys follow
`../wtk-qa/references/qa-scenarios.md`; scenario tags scope walks, not automated tests.

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

For example, a Members typography fix and a Dashboard mobile-card fix receive their own coverage.
If only Dashboard needs another correction, rerun its affected checks and retain Members evidence.
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

Explicit user skips remain a narrow claim with the limitation recorded. Never weaken, skip or delete
a test to obtain a pass, or describe a failed/unrun gate as passing. Knowledge checks run with bundle
writes, not as an added feature-delivery gate; dependency inventories are not vulnerability proofs.

## Credential-free declarative agent-tool configuration

This route applies only when the whole diff contains agent/server names, public URLs and non-secret
options. Commands, hooks, plugins, dependencies, credentials, OAuth/scopes, permissions, runtime code,
CI/deploy changes and external mutations follow their applicable normal route.

The active agent edits directly and makes one atomic commit, without feature artifacts, delegation,
Verifier, deep review or QA. Before committing:

1. Parse changed files and compare intended names, URLs, keys and values with the client schema.
2. Check for credential material.
3. Query the relevant installed clients read-only, returning only `name`, `url`, `enabled` and `auth_status`.
4. Run `git diff --check` and the project's commit-message validator.

OAuth requires explicit human authorization. Credentials, OAuth clients/scopes, permissions,
authentication behavior and sensitive product data require full Verifier coverage.

## Browser queue ownership

When a consuming project already provides a browser execution queue or lock, use that existing
coordination surface. Keep at most one queued browser execution per checkout; Playwright's internal
workers are part of that execution; they do not count as separate runs. Compare the queued run's
checkout and relevant inputs with the current request before enqueueing. Treat a queued run as stale
only when it is checkout-owned and relevant inputs changed; cancel it safely through the existing
mechanism and confirm cancellation before enqueueing its replacement.

Do not cancel a running test merely to replace queued work; a separately authorized cancellation may
use the consuming project's existing controls. Never kill a foreign run or take a foreign lock
holder's lock. Do not introduce a scheduler, framework, or new lock. If ownership of an existing
queued execution or lock cannot be established, do not kill it or enqueue a duplicate; report the
limitation and leave the existing state unchanged.

## Runtime isolation

Each checkout owns its runtime. Never use `reuseExistingServer: true` across siblings. Resolve a port
collision with a checkout-owned runtime; do not stop another checkout's server merely to run a gate.
Avoid concurrent full gates that compete for the same host resources.
