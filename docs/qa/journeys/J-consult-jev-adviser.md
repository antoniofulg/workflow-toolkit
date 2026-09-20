# J-consult-jev-adviser

**Persona:** Workflow operator
**Goal:** Assign tool routing and higher-level advice to Jev without duplicate explicit consultation, while retaining action authority.
**Entry point:** Direct invocation of `/wtk-discover`, `/wtk-plan`, `/wtk-lean`, `/wtk-implement`, `/wtk-deep-review`, `/wtk-qa` or `/wtk-ship`.
**Tags:** wtk-jev-adviser

## Before walking

- Use a checkout-owned disposable consumer and synthetic decision text only.
- The installed shared reference and the relevant direct phase skill are the inspected sources.
- The source repository QA profile prohibits network access; a configured live-provider leg stays untested here.

## Flow

1. Establish whether this session is confirmed to route model requests through an enabled gateway; installation alone does not establish routing.
2. Give a direct phase invocation a higher-level decision, minimal evidence and at least two candidate paths; confirm it reaches the shared adviser guidance.
3. Where the gateway and adviser cover the same decision, confirm the gateway owns it without another explicit consultation, including hint or passthrough; the adviser handles only uncovered decisions. Check the overlap example: gateway A/B/C plus adviser C/D/E yields gateway A/B/C and adviser D/E. For standalone, disabled or unknown routing, retain explicit consultation when available.
4. When no adviser key is available, confirm the adviser reports unavailability and the agent continues its normal evidence-based work.
5. In a consumer environment with an authorized provider session, confirm a configured Jev recommendation is checked against current evidence and causes no automatic action or gate verdict.
6. Change the phase, evidence or options and confirm the earlier advice is no longer used.

## Promises

- [`QAS-consult-jev-adviser`](../scenarios/QAS-consult-jev-adviser.md)

## Limitations

Static entrypoint inspection and CLI contract tests do not prove a host agent will follow the policy. This source-pack checkout cannot perform the live provider leg under its current QA network restriction.
