# UI/UX Surface Map

**Read when:** a feature adds or changes a screen, or a task names an approved visual reference.

**Why this exists:** `uiux.md` freezes states and the approved visual source so design and implementation
can execute in one pass and QA can judge the user-visible result. The repository stores only the approved
handoff. Features with no new or changed screen skip the surface map.

## The artifact

`.specs/features/<feature>/uiux.md`, written in Specify before internal design begins. Keep reference facts
here; tasks and packets point to its rows instead of copying a second manifest. When phases are skipped
and a task names a reference, keep the same fields in a bounded inline task record.

An approved source, frame, or frozen export selects reference fidelity, including for a new screen. Open
design keeps its exploration procedure. Resolve disagreements in this order: `spec.md` → `uiux.md` →
approved design artifact → tool or plugin output, then legacy mockup. The source owns visual appearance;
runtime truth, accessibility, and explicit product constraints still apply. Identify and resolve a
conflict with its owner; do not silently reinterpret, round, or rewrite the reference. External/global
aesthetic skills advise within this contract.

```markdown
# <Feature> UI Change Map
## Reference (when an approved source is supplied)
- **Approved source/frame:** tool and frame, or checked-in export path
- **Revision/frozen export:** revision, or frozen export path plus commit/hash
- **Route and mapping:** route; state ↔ exact viewport width×height pairs
- **Captures:** original/reference and implementation capture paths
- **Environment:** browser, OS, DPR, fixtures/content, and loaded fonts/assets
- **Tokens:** source provenance; mapped tokens; aliases/themes; inferred or missing values
- **Layout/responsive constraints:** geometry, breakpoints, and supported differences
- **Expected differences/tolerances:** approved differences recorded before judgment
## Screens
### <Screen name> — `<route>`
- **New or changed:** changed
- **Story:** links the user story it serves
- **Entry points:** how a user reaches it
- **States:** empty · loading · populated · error · submitting · success
- **Viewports:** exact width×height values and the responsive rule at each
## Components
| Component | New or existing | States and variants | Source |
| --- | --- | --- | --- |
| `PublicForm` | new | idle, validating, submitting, error, success | existing primitives |
## Copy
Every user-visible string this feature introduces, in the product's language, with its context.
## Out of scope
Screens and components this feature deliberately does not touch.
```

## Rules

1. **Enumerate states.** Never write "all states"; list each state a design agent can execute.
2. **Reuse before create.** Check design docs and the component inventory; a new generic primitive needs
   a reason and a domain variant takes a domain-prefixed name.
3. **Extract tokens before coding.** Extract actual source values into the canonical token source,
   preferably from a structured export: typography metrics, font weights, line-height, tracking, spacing,
   colours, radii, borders, and shadows. Keep layout constraints separate. Reuse matching tokens, map
   aliases/themes, and record deliberate shared-token changes. Mark raster/fragment inferences explicitly.
4. **Truthful UI wins.** Never render an unsupported control or metric. Runtime truth wins on conflict,
   and the conflict is recorded.
5. **Freeze the surface before internals.** Reopen this document explicitly when the surface changes.
6. Its existence marks the feature UI-bearing for QA when the proportional classifier selects QA.
7. **Trace the common completion path.** Walk from user intent to completion for each changed
   interaction. Remove avoidable clicks, repeated input, navigation, and keyboard-pointer switches with
   platform conventions while preserving clear choices, validation, and feedback. Record start,
   completion, recovery, and next-action behavior in acceptance criteria, then verify that path.
8. **Use native form submission.** For web workflows with an explicit submission, use native `<form>`
   semantics and a primary submit action. Enter in a plain single-line input and activating the submit
   button must use the same submission path; preserve expected Enter behavior for multiline fields,
   selection controls, and active input composition.

   **Example:** Given a valid tag name and selected color, pressing Enter creates exactly one tag with
   those values; an error keeps the input. If repeated creation is intended, leave the next entry ready
   without reopening or restoring focus manually.

## Optional design tooling

When an approved HTML/CSS export is the declared visual source, render it with supplied fonts/assets and
verify that render is ready before implementation; compare it with an original frame only when that
frame is the declared authority. Port structure/styles into the project stack, adapting syntax,
component ownership, and behavior while preserving visual values. The export is source material, not a
blind generated-code dump or compulsory DOM-identity contract; React and Tailwind are examples, not
source-pack dependencies. Keep supported exports/assets usable when the design tool is unavailable; tool
absence or failure falls back to the normal repository artifacts and does not block unrelated work.
Missing source, fonts, assets, or responsive evidence is an
explicit gap; fidelity cannot PASS on assumptions, stale captures, or unavailable proof.

## Working with a design agent

1. State constraints first: user goal, required states/actions, hierarchy, accessibility, responsive behavior, runtime/data
   limits, brand principles, and existing components.
2. Read selected references and inspect affected components read-only. With an approved reference, load
   its `uiux.md` rows and source/export before proposing changes.
3. For an open genuinely new screen or meaningful redesign, provide three distinct directions and a fourth only
   for a named tradeoff. An approved reference selects the direction and skips alternatives; corrections
   never require variants.
4. For open design, prototype in the available tool, isolated HTML, or component playground when useful;
   keep variants out of production. With an approved source, render and inspect it before porting.
5. Subtract purposeless UI only during open design, retaining discoverability, accessibility, actions,
   and feedback. Review against `uiux.md` and the source; one exploration pass and one refinement cap applies
   to open design only.
6. Record source/frame, reused components, states, viewports, copy, token mappings, expected differences,
   and tradeoffs in the UI contract. A reference task points to these rows through `design_excerpt` and
   records paired evidence. Human local QA is recorded only after human confirmation.

No new showcase, preview deployment, design integration, or split frontend/backend delivery is mandatory.

## Verifying the built screen

When a visual reference is named, completion requires fresh paired reference and implementation captures
for every declared exact viewport and state, with fixtures/content, browser/DPR, and loaded fonts/assets.
Use the existing adapter and paired inspection, overlay, or diff to compare geometry, typography, tokens,
imagery, interaction states, and responsive behavior. Record expected differences/tolerances before
judging; source or implementation changes invalidate affected evidence. Missing evidence is unverified;
an unacceptable mismatch fails. Functional assertions alone do not prove fidelity, and no universal
arbitrary pixel threshold applies. Manual comparison is evidence, not an automated test. Keep raw captures
disposable and put the durable verdict and source pointers in the existing task, verifier, or QA report.
