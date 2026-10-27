# UI/UX Surface Map

**Read when:** a feature adds or changes a screen, or a task names an approved visual reference.

**Why this exists:** `uiux.md` freezes states and the approved visual source so design and implementation
can execute in one pass and QA can judge the user-visible result. The repository stores only the approved
handoff. Features with no new or changed screen skip the surface map.

## The artifact

`.specs/features/<feature>/uiux.md`, written in Specify before internal design begins. Keep reference facts
here; tasks and packets point to its rows instead of copying a second manifest. When phases are skipped
and a task names a reference, keep the same fields in a bounded inline task record.

A request to implement a selected image, design, frame, or frozen export makes its visible composition
binding by default, including for a new screen. Only an explicit user instruction to use it as
inspiration makes it nonbinding; agent-written “directional” wording cannot downgrade that choice. Open
design keeps its exploration procedure. Resolve disagreements in this order: `spec.md` → `uiux.md` →
approved design artifact → tool or plugin output, then legacy mockup. The source owns visual appearance;
runtime truth, accessibility, and explicit product constraints still apply. Identify and resolve a
conflict with its owner; do not silently reinterpret, round, or rewrite the reference. External/global
aesthetic skills advise within this contract. A derived spec or UI map cannot silently override the
selected source; record and resolve each conflict before coding.

```markdown
# <Feature> UI Change Map
## Reference (when an approved source is supplied)
- **Approved source/frame:** tool and frame, or checked-in export path
- **Revision/frozen export:** revision, or frozen export path plus commit/hash
- **Intent:** binding implementation (default), or inspiration with the user instruction cited
- **Route and mapping:** route; selected state ↔ exact mobile and desktop CSS viewport width×height pairs
- **Captures:** local original/reference, full-page and actual viewport capture paths
- **Scale/environment:** source pixels per CSS pixel (source scale), browser, OS, DPR, fixtures/content, loaded fonts/assets and theme
- **Tokens:** source provenance; mapped tokens; aliases/themes; inferred or missing values
- **Composition:** header/navigation, content hierarchy, filter/control placement, cards, footer; order and containment
- **Visual requirements:** spacing/density, typography/scale/weight, palette/theme, borders/radii, media crop/aspect ratio
- **Layout/responsive constraints:** columns, alignment, breakpoints, stacking, sticky/fixed behavior at each viewport
- **Expected differences/tolerances:** one row per difference below; raster estimates marked, no pixel-equality requirement

| Region/property | Source requirement | Implementation difference | Necessity and authority | Preserved requirement / verification |
| --- | --- | --- | --- | --- |
| Result count | sample count | live count | runtime truth | retain position and typography |
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
4. **Record differences individually before coding.** Name each live-data, accessibility, shared-component,
   or unavailable-photo adaptation, its affected property, reason and authority; seek a user decision
   for a material redesign. “Use project tokens” is not an exception: map matching tokens or add a
   scoped variant through the canonical system. Preserve unaffected source requirements. Never render
   unsupported controls or metrics. Use clearly identified placeholder media when real photos are
   missing; stock/generated imagery must not imply it depicts a real venue.
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

For a binding source, use the following acceptance procedure even when behavior tests or QA pass.

1. **Builder:** render at every contracted mobile and desktop **CSS viewport** and state, recording
   source scale, browser/OS, DPR, fixtures, fonts/assets and theme. Capture that genuine render;
   resizing or cropping an image rendered at another viewport does not prove the contracted render.
   Inspect beside the source, fix material mismatches and recapture affected evidence before handoff.
   Capture the full page for composition and the actual viewport for interaction states, including
   scroll/open controls. Full-page evidence alone cannot prove sticky choices, focus or actions
   remain reachable; exercise them in the actual viewport.
2. Compare hierarchy, spacing, typography, palette, controls, media and responsive layout against the
   recorded requirements and individual differences. Check inherited dark-theme leakage against the
   selected theme, and check placeholder imagery/labels cannot imply a photographed real venue.
3. **Independent Verifier:** open the source and captures, check freshness against the implementation
   revision and environment, and judge every contracted pair independently of the builder's verdict.
   Reproduce selected interaction states in actual viewports when captures cannot prove reachability.
   A materially different theme, header, filter layout, card composition or footer is a visual FAIL
   even with green functional tests and QA. Missing source/captures or uninspected pairs are unverified
   and cannot PASS. Put these failures in the existing binding-source findings as well as the verdict.
4. Record evidence in the existing task, verifier or QA report using the literal columns below.
   Source or implementation inputs affecting a contracted pair invalidate that pair's evidence.
   Unrelated HEAD changes do not automatically invalidate all captures: independently record the
   original evidence/revision and an explicit input-equivalence reason for reuse, following
   [validation](validation.md). An old PASS or matching filename alone is not equivalence.
   Keep captures disposable but available through independent review.

| Source/revision | Source scale | Implementation revision | Route/state | Viewport/scroll | Environment | Reference capture | Full-page capture | Viewport capture | Comparison | Result |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| frozen source and revision / contract row | 1x | tested revision | route and selected state | 390x844; scroll: 0,0 | browser: Chromium 130; OS: Linux; DPR: 1; fixtures: seeded; fonts/assets: loaded; theme: light | reference.png | full.png | viewport.png | inspected requirements, individual differences and interactions; independent result and any input-equivalence reason | PASS |

`Source scale` is positive source pixels per CSS pixel; mark inferred raster calibration in the
source/contract, not a fabricated precise value. `Viewport/scroll` uses CSS width×height and CSS
scroll x,y. Record browser, OS and positive `DPR:` explicitly in Environment along with content,
fonts/assets and theme. Each capture cell is one literal local file path, optionally backtick-wrapped;
relative paths resolve beside the report, absolute local paths are allowed. Paths are data, never
commands, shell substitutions or URLs. The Lean completion gate requires these columns, usable
values and existing files under `ui`; non-UI profiles acquire no screenshot obligation. It cannot
authenticate images, detect sophisticated resizing, judge fidelity/freshness or prove matrix
coverage. Independent inspection and state reproduction above remain required.

Use the existing adapter with side-by-side inspection, overlay or diff; manual comparison is evidence,
not an automated test. A conceptual raster binds visible composition without requiring pixel equality:
mark inferred values and responsive adaptations, tolerate minor rendering differences, and fail material
structure or styling drift. For source states/viewports not drawn, explicitly record the inferred rule;
never fabricate a matching reference capture. Do not add a screenshot framework or exhaustive state
matrix solely for this process. See [the regression example](ui-fidelity-example.md).
