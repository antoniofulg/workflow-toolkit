# Verify Core

**Read when:** an independent Verifier runs the Lean or modular verify procedure. Both route
procedures link here for the obligations they share; each keeps its own route-specific steps.

## Approval

Under every profile, apply [construction verification](construction-constraints.md#verify): confirm
the owning artifact's `## Approval` receipt and any explicit reuse, construction-order or approval
requirement.

## Evidence or zero

A check with no located `file:line` counts as not proven - per check, never one citation standing
in for twenty. Search before concluding something is absent, and show the search.

## Visual evidence (`ui`)

Independently inspect the source and implementation captures; record missing evidence or material
visual mismatches in `Binding sources` as `Uncovered` or `Contradiction`, so a functional PASS
cannot conceal a visual FAIL.

Include one `Visual fidelity` row per contracted viewport/state pair using the route's report
template and the shared [UI evidence fields](ui-ux.md#verifying-the-built-screen). A missing or
non-PASS pair blocks completion. The gate checks evidence structure; the Verifier checks actual
images, freshness and matrix coverage.

## Swept re-read

Read the `Swept` rows that resolve to **existing** against the code: is the constraint they cite
actually there? A cited constraint that is not there is a finding. Rows that say `n/a` or *not in
scope* are policy the user approved; there is nothing in the code for them to be wrong about.

## Fault injection (`standard`, `ui`)

A green suite proves the tests run. Fault injection proves they can catch a regression - it is
the only step that produces that information, and under `light` it does not run.

1. **Isolate.** `git worktree add <scratch> HEAD`, and prepare it with the project's restore/build
   command, or use the mutation tool's own sandbox when it never writes the real tree. Never mutate the real tree, and **never use
   `git stash`**: it records state from *before* the mutation, so popping it does not reverse a
   fault applied afterwards, and on a clean tree it creates no entry at all.
2. **Baseline.** Record `git status --porcelain` of the real tree first.
3. **Inject.** When the project declares a mutation command, run it in the scratch with the scope
   the [mutation policy](test-contract.md#mutation) sets, and skip step 4. Record the run as one
   `Mutation run` row (command, scope, killed and survived counts) and each survivor as a
   `Faults injected` row whose `Disposition` is `killed`, `equivalent - <reason>` or `arid - <reason>`. Otherwise inject a
   **behaviour-level fault** in the new code: flip a condition, change a returned value or
   status, shift a bound by one, remove a required side effect.
4. **Run the narrowest covering proof** in the scratch and confirm it FAILS - the mutant is killed.
5. **Discard** the scratch and confirm the real tree's porcelain matches the baseline. If it
   differs, STOP, restore the tree, and treat the run as invalid.

**Manual faults: one per distinct assertion surface, not per risky line.** Three mutations killed by the same
two proofs ran the same experiment three times. Choose faults that force *different* proofs to fail,
stop once every proof carrying a check has been made to fail once, and cap it at five however risky
the feature looks - a quota that scales with risk costs most exactly where checks cluster in risky
code. A second covering proof per fault adds a run and no information.

**A surviving mutant is a finding, not a footnote.** It means the assertion would pass under a
plausible wrong implementation. Resolve it under the [survivor policy](test-contract.md#mutation).
