# J-use-optional-jev-qa-adapter

**Persona:** Workflow operator
**Goal:** Use the default Jev-first browser QA route without installing browser dependencies or
surrendering the QA verdict to a driver.
**Entry point:** exact local package → `wtk install` → quality module → installed
`.agents/skills/wtk-qa-execute/`
**Tags:** wtk-qa

## Before walking

- Freeze the assigned source snapshot and use only checkout-owned disposable package, runner,
  consumer, and evidence roots.
- Use the local packed package and the CLI/manual filesystem-readback adapter from
  [`docs/qa/README.md`](../README.md). Do not contact a registry or launch a browser.
- Remove `TYPESAFE_API_KEY`, `AI_GATEWAY_API_KEY`, and `TEXT_MODEL_API_KEY` from the child process
  environment. Do not read, copy, print, or synthesize provider credentials.
- Record the opening source status and every disposable path before the first write.

## Flow

1. Pack the assigned snapshot locally and inspect the archive from a separate runner. Confirm the
   quality module contains `wtk-qa-execute/SKILL.md` and `jev_adapter.py`, while package metadata
   declares no Jev Ultrafast, Browser Harness, or Playwright dependency.
2. Run the packed public installer from a disposable Git consumer and select `quality`. Read the
   installed skill and helper through a separate process. Confirm consumer package and lock files
   remain byte-identical and no dependency, browser, provider client, or external skill appears.
3. Read the installed instructions and config example. Confirm `browser_adapter` defaults to `auto`,
   lists the six supported values, uses Jev only for non-consequential fixtures, requires a dedicated
   CDP endpoint, and falls back through Playwright MCP, exactly one host-declared Orca or Maestri
   adapter, then manual. If both native adapters are present, only Orca is selected.
4. With all provider-key variables absent, invoke the installed helper for a non-consequential
   fixture using a checkout-owned evidence destination. Require exit `2`, exactly one JSON result,
   status `unavailable`, `fallback_safe: true`, `fallback_adapter: "playwright-mcp"`, a secret-free
   missing-prerequisite limitation, and no evidence write or browser/provider action.
5. Invoke the installed helper for a consequential journey with the same scrubbed environment.
   Require policy rejection before prerequisite discovery, the same structured unavailable/fallback
   shape, and no evidence write or browser/provider action.
6. Point the installed helper at an evidence destination outside the declared checkout-owned
   evidence root. Require exit `2`, exactly one JSON result with status `invalid`, and an unchanged
   outside sentinel.
7. Independently reload the installed instructions and require `completed`/`DONE` to remain driver
   evidence only, with scenario `pass` reserved for a matching independent readback after reload.
   The execution report must name that no browser adapter was used, the exact installed helper path,
   evidence or its absence, each limitation, and the independent filesystem readback.
8. Remove only the recorded disposable roots. Require source status to match the opening snapshot
   apart from planned durable QA report and scenario-status updates.

## Promises

- [`QAS-use-optional-jev-qa-adapter`](../scenarios/QAS-use-optional-jev-qa-adapter.md)

## Adjacent canary

The packed install and independent readback reuse
[`ADP-install-versioned-workflow-package`](../scenarios/ADP-install-versioned-workflow-package.md).
Its existing promise is unchanged, so this cycle records only a narrow package-membership and
residue canary and does not reset that scenario.

## Limitations

This source repository has no browser surface, server, fixture application, installed Jev runtime,
Browser Harness, or Playwright MCP adapter. Live Jev, browser, provider, and fallback execution stay
outside this journey. Offline contract proofs do not change the scenario's `untested` verdict.
