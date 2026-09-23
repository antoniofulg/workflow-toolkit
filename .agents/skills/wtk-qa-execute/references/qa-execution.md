# QA Execution

**Read when:** a feature reaches its closing QA session.

`wtk-qa-plan` and `wtk-qa-execute` own the procedures. This guideline only decides whether QA runs, dispatches
the existing Verifier, and points to the authorities that keep the contract stable.

## Trigger

QA runs once per feature, at feature close over the integrated tree; no slice runs QA. Run it when
the feature diff changes an observable UI, API, CLI, mobile surface, public configuration,
adoption flow, docs-as-interface, or user-facing copy, unless the proportional classifier in
`.agents/skills/wtk/references/validation.md` selects a narrower route. A behavior-preserving `direct correction` or `UI-only correction`
is the exception: its targeted integration validation covers the consuming project and it receives no QA Plan/Execute cycle,
even when the rendered component changes. A browser-only invariant explicitly
changed by that correction may use one existing targeted scenario. Purely internal refactors receive
technical verification only. Record `no user-visible change` when no public promise changed.

## Dispatch

After the final implementation wtk-deep-review group, use the provider's existing `verifier` with one
phase per packet:

1. Use `phase: wtk-qa-plan` when the scope needs planning; reuse applicable scenarios and charters.
2. Use `phase: wtk-qa-execute` to walk the agreed scope. For clear bounded work, the same non-author
   QA session may process both packets. A retest with an applicable plan needs no new Plan session.

A standalone Plan request stops before execution. Neither QA phase writes product code. Follow
`.agents/skills/wtk-qa-execute/references/fix-loop.md` for frozen-snapshot walks, batched remediation,
observer reuse, and impact-selected retests; a defect does not end all independent walks.

## Authorities and adapters

- `../wtk-qa/references/qa-scenarios.md` owns scenario fields, ids, statuses, and flag/reset rules.
- `docs/qa/README.md` owns the consuming project's public interfaces, existing adapter, setup,
  authentication, fixtures, cleanup, and limitations.
- `wtk-qa-execute` selects the declared browser, API, CLI, mobile, or manual adapter. It records the
  exact path, evidence, and limitation. It does not install tooling or invent commands.
- Each checkout owns its runtime and raw evidence. Keep durable reports and statuses in `docs/qa/`
  and keep generated evidence in the consuming project's disposable evidence path.
- When a selected QA scope carries a visual AC, follow `../../wtk/references/ui-ux.md#verifying-the-built-screen`, point the
  report at its feature `uiux.md` row, and record the paired-capture output fields. A manual comparison
  is evidence, not an automated test; keep behavioral assertions intact.

Read the two skills and `../../wtk-qa/references/qa-scenarios.md` for the active branch; this bridge deliberately carries no
duplicate scenario schema or live-walk protocol.
