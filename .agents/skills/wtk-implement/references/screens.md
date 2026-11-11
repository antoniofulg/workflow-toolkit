# Screens

**Read this only under `profile: ui`.** Under `light` or `standard` the interface is out of
scope for the checks, and loading this file costs a run that will not use it.

## The design decides, the check records

**On a screen the concrete values live in the design, so open it before writing the check.**
"Renders the intake" and "the body includes assembling" pass under any interface at all - that is
"gracefully" wearing a string literal. Not fidelity, which no exit code settles, but the values
that are assertable and only the design carries: which elements exist, what the labels say, what
the step counter reads, whether a state is its own screen or a band on one that already exists.
Named, they are settled by the runner like every other check.

**A design is binding, not reference.** When a check and the design disagree, the check is wrong
until the user says otherwise. This is the failure worth naming, because it does not look like
one: a checklist that contradicts the design ships the contradiction with every proof green, and
the build is then correct against the artifact and wrong against the decision.

**It also outranks the screen that is already there.** Reuse is about components - the card, the
button, the container - never about a layout the design replaced. When the feature lands on an
existing screen and the design draws that screen differently, the old composition is the thing
the change is for; keeping it because it was already built is the most comfortable way to ship
the wrong screen with every check green.

## When the repo has a design system

Apply [the UI contract](../../wtk/references/ui-ux.md): preserve the selected source's visible
composition and values using matching tokens and component variants. Record necessary differences
individually before coding. Reuse does not authorize replacing the selected palette or layout.
Render at the contracted viewport with source scale, runtime and device scale recorded; use the shared
report's explicit provenance and local reference/full-page/viewport paths. A resized/cropped render
from another viewport is not evidence of that viewport. The independent Verifier opens actual
images and reproduces interactions; missing files/provenance block completion. Refresh affected
pairs on source/render-input changes; retain unrelated evidence only with independent input equivalence.

## Open it, and say how

**Resolve it before writing a screen check, and do not assume you cannot.** Most designs are
reachable: an artifact URL opens with a fetch, a design file opens through its MCP where one is
connected, an attachment on a tracker issue comes down through that tracker's API, and an image
committed to the repo is a file to read. Work through whatever the environment actually offers,
then say which route worked - "the link was in the ticket" and "I opened the design" are
different claims, and only one of them is evidence.

**Opened means you saw the screens, not that a fetch returned bytes.** A design attachment often
arrives as something that is not an image: a JS bundle, an archive, a page whose markup is a
loader. Downloading that and recording the source as opened is the worst of the three outcomes,
worse than reporting it unreachable, because the checklist then claims an authority nobody
consulted and every later step trusts the claim. If you cannot see the arrangement, the design is
**unresolved** - say what came back, mark the screen checks as written without it, and let the
`Unproven` column carry the composition.

Falling back is allowed; doing it silently is not, and neither is falling back without trying -
a link reported as inaccessible on the strength of its domain is a fabricated fact, not caution.
When nothing resolves, record against the entry in `Sources` what you attempted and what came
back, build the screen checks from the values the task transcribed, and mark those checks as
written without the design. An unresolved design is a finding somebody can act on; an
unmentioned one is what produces the wrong screens.

## How far a screen check reaches

How far a screen check reaches is the same question as any other level and has the same answer:
whatever the repo already asserts. Where a suite drives a browser, a screen check can live there;
where only request tests exist, structural assertions are the ceiling. Never bring in a browser
stack to satisfy this - a proof that cannot run in the project's own setup is worse than none, and
this skill installs nothing.

**Split the screen by what proves it**, under [visual acceptance evidence](../../wtk/references/test-contract.md#visual-acceptance-evidence):

- **Paired captures** prove arrangement, order, count and copy: that a progress bar is drawn and
  no breadcrumb is, that the primary button comes before the secondary, that the counter reads
  `1 of 3`, that `NOW` sits inside the week band rather than beside it, one column or two.
- **The screens judge** compares each picture with its capture and never sees the code: the
  [protocol and `screens.md` schema](../../wtk/references/ui-ux.md#screens-judge-ui) live with the
  UI contract, and a builder never judges its own screens.
- **One structural guard per screen** is the only selector check on its form: the assertion that
  would break first if the composition changed, such as the regions the screen has.
- **Checks** assert behaviour, and copy only where copy is the contract.

Nothing the design decides is exempt. This is the failure this section has actually produced:
every label copied, every count correct, and a screen that reads as a different product - so the
captures are compared for composition, not only for labels, and a mismatch blocks completion.

An exemption still has to enumerate, under the same rule as every other negative in this skill.
"Visual fidelity is unproven" is a blanket that legitimises every mistake of form written after
it - including the ones a check would have caught - and a verifier reading it treats a real gap as
a limitation properly declared. Name the screen and the property: `03 overview - spacing and card
elevation unproven`. Those properties still require the builder comparison and independent visual verdict in the UI
contract; an automated-proof limitation is not a visual acceptance exemption.

## The Screens table needs a column for arrangement

Give the artifact a `## Screens (ui)` section with one row per screen and **three** columns, so
the omission shows up as an empty cell rather than as a shorter sentence:

```markdown
| Screen | Behaviour and contracted copy (checks) | Structural guard (selector) | Arrangement, order, count, copy (paired captures) |
| --- | --- | --- | --- |
| 01 mid-cycle | Continue opens the next stage · Later dismisses · Regenerate rebuilds the cycle | week band contains `NOW` | progress is a **bar**, not a ring · `NOW` **inside** the week band, between last-opened and next · community in **two** columns · stages as numbered circles on a rail · footer: feedback left, Regenerate right · kicker `{N}-DAY CYCLE`, `day K of N`, `THIS WEEK` |
```

The last column is the one this whole file exists for. Without it a row reads as complete with
nothing but labels in it - which is how a screen ships with every string correct and a layout
nobody decided. Each item there is a property the Verifier's paired comparison must PASS.

## Screens are a Coverage set

**Designed screens are a set whose members are the screens.** The design already numbers them, so
the enumeration exists and owes a row like any other. The row is what forces the artifact open,
which is exactly where this fails: a screen nobody mapped is a screen nobody built, and it stays
invisible while every check is green. Map each screen to the check that renders it and leave the
rest in `Unproven`.

```markdown
| designed screens (6) | `01` intake C1 · `02` assembling C5 · `03` overview C19 · `04` player C26 · `05` completion C20 | `06` |
```

Where the design draws a state as a band on an existing screen and a check turned it into a
screen of its own, that is not a gap but a contradiction - say so in the row and settle it with
the user, because the check is the side that is wrong.

And mark the design in `Sources` as binding for the interface, naming the screens it covers:

```markdown
- <design URL or path> - **binding for the interface**: screens 01-06
```
