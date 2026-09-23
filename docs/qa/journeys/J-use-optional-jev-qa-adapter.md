# J-use-optional-jev-qa-adapter

**Persona:** Workflow operator
**Goal:** Use the default Jev-first browser QA route without installing browser dependencies or
surrendering the QA verdict to a driver.
**Entry point:** exact local skill source → Skills CLI full-set install → installed
`.agents/skills/wtk-qa-execute/`
**Tags:** wtk-qa

## Before walking

- Freeze the assigned source snapshot and use only checkout-owned disposable source, runner,
  consumer, and evidence roots.
- Use an exact local copy of the 12 WTK skills and the CLI/manual filesystem-readback adapter from
  [`docs/qa/README.md`](../README.md). Do not contact a registry or launch a browser.
- Remove `TYPESAFE_API_KEY`, `AI_GATEWAY_API_KEY`, and `TEXT_MODEL_API_KEY` from the child process
  environment. Do not read, copy, print, or synthesize provider credentials.
- Record the opening source status and every disposable path before the first write.

## Flow

1. Install the documented complete 12-skill set from the exact local source into a disposable Git
   consumer. Read the installed skill and helper through a separate process. Confirm consumer files
   remain byte-identical and no dependency, browser, provider client, WTK config, or external skill appears.
2. Read the installed instructions. Confirm absence of a task-scoped adapter choice selects `auto`,
   the six supported values remain available, Jev is limited to non-consequential fixtures, a
   dedicated CDP endpoint is required, and fallback proceeds through Playwright MCP, exactly one
   host-declared Orca or Maestri adapter, then manual. If both native adapters exist, select only Orca.
3. With all provider-key variables absent, invoke the installed helper for a non-consequential
   fixture using a checkout-owned evidence destination. Require exit `2`, exactly one JSON result,
   status `unavailable`, `fallback_safe: true`, `fallback_adapter: "playwright-mcp"`, a secret-free
   missing-prerequisite limitation, and no evidence write or browser/provider action.
4. Invoke the installed helper for a consequential journey with the same scrubbed environment.
   Require policy rejection before prerequisite discovery, the same structured unavailable/fallback
   shape, and no evidence write or browser/provider action.
5. Point the installed helper at an evidence destination outside the declared checkout-owned
   evidence root. Require exit `2`, exactly one JSON result with status `invalid`, and an unchanged
   outside sentinel.
6. Independently reload the installed instructions and require `completed`/`DONE` to remain driver
   evidence only, with scenario `pass` reserved for a matching independent readback after reload.
   The execution report must name that no browser adapter was used, the exact installed helper path,
   evidence or its absence, each limitation, and the independent filesystem readback.
7. Remove only the recorded disposable roots. Require source status to match the opening snapshot
   apart from planned durable QA report and scenario-status updates.

## Promises

- [`QAS-use-optional-jev-qa-adapter`](../scenarios/QAS-use-optional-jev-qa-adapter.md)

## Adjacent canary

The full-set install and independent readback reuse
[`ADP-install-versioned-workflow-package`](../scenarios/ADP-install-versioned-workflow-package.md).
The native-agent-settings cycle already resets that scenario, so one isolated install may provide
evidence for both promises without turning offline adapter evidence into a live browser verdict.

## Limitations

This source repository has no browser surface, server, fixture application, installed Jev runtime,
Browser Harness, or Playwright MCP adapter. Live Jev, browser, provider, and fallback execution stay
outside this journey. Offline contract proofs do not change the scenario's `untested` verdict.
