---
name: wtk-qa-execute
description: Execute planned QA through existing public interfaces and record evidence or defects. Use when a Verifier walks QA; Don't use for planning, product fixes, or framework setup.
metadata:
  author: Antonio Fulgêncio
---

# QA Execute

Walk the current QA plan through the consuming project's public surfaces. Select the adapter already
declared by the project, capture evidence, write durable results, and return product defects to an
Implementer without making the QA observer an author.

For semantic QA decisions, follow the [Jev-first guidance](../wtk/references/jev-adviser.md) before choosing a path.

## Provenance

Author: Antonio Fulgêncio.

This is an original project-owned adaptation for this workflow, inspired by Pedro Nauck's
[`qa-execution` skill](https://github.com/pedronauck/skills/tree/main/skills/mine/qa-execution).

## Inputs and boundaries

Read `docs/qa/README.md`, the QA Plan handoff, the in-scope scenarios and charters, open bugs, and
[`../wtk-qa/references/qa-scenarios.md`](../wtk-qa/references/qa-scenarios.md) in full. The guideline owns scenario fields, ids, statuses, and
flag/reset rules. Read [`references/session-protocol.md`](references/session-protocol.md) in full
before the first charter.

For a bounded retest, the existing report's scoped plan and linked scenario/charter satisfy the
QA Plan handoff; references to a charter below include that scoped plan.

Use real public interfaces and the project's existing browser, API, CLI, mobile, or manual adapter.
When no runner is adopted, choose the closest reachable public interface or a manual adapter and
record the limitation. Mark only an unreachable leg `untested`; missing tooling alone is a
limitation, not an unreachable product surface. Report the exact adapter, path, evidence, and
limitation. Keep raw evidence in the repository's disposable evidence path and keep reports, scenario
status, and bug records durable.

QA execution validates the product; it does not write product code, install a framework, invent a
command, or replace the automated gate.

## Browser adapter selection

Use the consuming project's task-scoped QA adapter choice when one is supplied. Without one, use
`auto`. The valid values are `auto`, `jev`, `playwright-mcp`,
`orca`, `maestri`, and `manual`; `jev-ultrafast` is not a public alias. `auto` tries Jev first for
a declared non-consequential fixture journey, then LLM + Playwright MCP, exactly one IDE-native Orca or
Maestri adapter exposed by the host, then manual. If both IDE-native adapters are exposed, choose
Orca before Maestri and invoke only that one. A direct value selects only that adapter; if its
prerequisites are unavailable, record the limitation instead of substituting another adapter.
Use [`jev_adapter.py`](jev_adapter.py) for Jev preflight and the single bounded Jev attempt.

For `auto`, Jev unavailability selects LLM + Playwright MCP as the first fallback. A typed
`TimeoutError` raised while constructing `jev_ultrafast.Agent(url, goal)` is classified
`pre-action-timeout`; its result sets `fallback_safe: true` and
`fallback_adapter: "playwright-mcp"`. Jev's constructor performs initial navigation and read-only
observation; `Agent.run()` is the action loop.
Use the fallback only after an independent read or fixture reset confirms known isolated state.
Once `Agent.run()` starts, a timeout is unsafe to replay even when no action was recorded. The
result classifies recorded action history as `post-action-timeout`, missing history as
`ambiguous-timeout`, sets `fallback_safe: false` and `fallback_adapter: null`, and selects no
automatic fallback. If an action began or state is uncertain, stop and inspect or reset the fixture
before another driver acts. Only `auto` follows fallback metadata; direct values select one adapter.
The helper does not invoke MCP or IDE tools; the Verifier follows the chain using adapters exposed
by its host.

The Jev helper reads credentials from the process environment only: `TYPESAFE_API_KEY` drives Jev
decisions and `AI_GATEWAY_API_KEY` is aliased in process memory as the text-helper credential, so
a stored `TEXT_MODEL_API_KEY` is not required. The caller or secret manager may load a central
environment file before starting the process; this skill does not parse `.env` files. Jev requires
a separately launched dedicated Chromium exposed through an explicit `BU_CDP_URL` or `BU_CDP_WS`.
A headed run is allowed only when explicitly requested and must use the same kind of dedicated CDP
endpoint. Profile labels, personal sessions, and Browser Harness's default local-browser discovery
are not accepted. The helper installs neither Jev Ultrafast nor Browser Harness and does not provide
a Playwright MCP, Orca Browser, or Maestri Portal bridge; those adapters remain host-native.

The helper reports the actual adapter, execution path, allowlisted evidence, failure classification,
fallback eligibility, and limitation. Its `completed`/`DONE` result is driver evidence only: it is
never a QA `pass`. Continue through the independent read path and reload before a Verifier records a
scenario verdict. The wrapper calls `Agent.run()` once; it never restarts or retries that call.
Evidence excludes authorization, cookie, token, and credential fields recursively, and omits raw
exception text.

## Procedure

### 1. Preflight the cycle

Read the profile, plan handoff, affected scenarios, open bugs, and charters. Confirm the recorded
automated gate is green and the product is reachable through a production-parity path. Resolve the
adapter and prerequisite gaps before the first walk. If a runner is missing, use the closest
reachable public interface or manual adapter and record the limitation. A leg is `untested` only
when its product surface is unreachable; a leg that only a human can complete may be
`blocked-verify` with the exact reason.

**Done when:** every charter has a reachable entry point or a named limitation, the gate result is
recorded, and the selected adapter is supported by the profile.

### 2. Select the adapter

Choose the closest existing adapter for each public surface: browser, API, CLI, mobile, or manual.
Prefer a reachable manual walk when no automated runner exists.
Follow the profile's setup, authentication, fixture, seed, cleanup, and residue checks. Preserve the
project's runner and commands as declared by its manifest or CI. Read
[`references/session-protocol.md`](references/session-protocol.md) in full for the execution and
evidence contract.

**Done when:** the session log names one adapter and exact execution path for every walkable surface,
with setup and cleanup prerequisites resolved or recorded as limitations.

### 3. Open the report

Create `docs/qa/reports/<YYYY-MM-DD>-<scope>.md` before the first charter, or resume the current
report when one exists for this cycle. Add every charter and scenario to the matrix with a pending
verdict. Include the adapter, environment, gate command/result, and evidence destination. When a
visual criterion is in scope, point the row at its feature `uiux.md` source/frame and record paired reference
and implementation captures with the declared state, exact viewport, fonts/assets, and expected
differences. Do not count that manual comparison as an automated test.

**Done when:** one dated report contains every in-scope charter and scenario, and no walk has started
with a missing matrix row.

### 4. Walk in persona

Adopt the charter's persona, enter through its public entry point, and walk the journey to its true
end state. Confirm the expected observable through an independent read path and after a reload. Capture
evidence at each checkpoint and divergence, then update the report and scenario status immediately.

**Done when:** every charter has a recorded verdict, independent confirmation, evidence path, and
debrief, or an explicit limitation with the status prescribed by `../wtk-qa/references/qa-scenarios.md`.

### 5. Probe the changed surface

Run the charter's tour and select edge probes and lenses justified by changed promises or named
risks; there is no minimum count. Reuse applicable coverage rather than repeating journeys for a
quota. Record clean attempts as results and keep evidence paths beside their report rows. Apply the
human-UAT reuse rule in [`references/session-protocol.md`](references/session-protocol.md) only for an
applicable scenario or charter with recorded revision and environment; use its relevant-input check.
A scoped UAT result may narrow duplicate exploratory actions, never required proof or evidence.

**Done when:** the selected tour, every chosen edge, and every applicable lens have a recorded
result, evidence path, or named limitation.

### 6. Record findings and govern fixes

Deduplicate against `docs/qa/bugs/` and linked scenario bug ids. File a new bug only for a new
symptom; append re-found or regressed observations to the existing record and link affected
scenarios. When a product defect is confirmed, read
[`references/fix-loop.md`](references/fix-loop.md) in full. Stop unsafe or dependent paths immediately;
finish safe independent paths on the same frozen snapshot, then hand the findings to an Implementer
as one remediation batch. Do not walk a tree while it is being changed.

**Done when:** every finding has a deduplicated bug record, affected scenario links, severity and
evidence, and every product fix is explicitly assigned to an Implementer rather than changed here.

### 7. Close or resume the cycle

After a fix, the same non-author Verifier may resume after identifying the new snapshot and resetting
the environment; replace it if independence, reliable state, or sufficient context is lost. Rerun
only impact-invalidated technical proofs and resume from the affected journey and causally related
canaries. Keep the original report history and update statuses, retest fields, bug
links, and evidence. At close, replace every pending row with a terminal result or an allowed
`untested`/`blocked-verify` explanation, apply `.agents/skills/wtk/references/validation.md` and record
the selected commands, reused evidence and results. QA close does not automatically repeat a full gate.

**Done when:** no report row remains pending, every fixed bug has a passing retest or an explicit
decision, every scenario status matches its evidence, and the final gate result is recorded.
