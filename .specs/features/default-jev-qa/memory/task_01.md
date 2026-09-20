# Task 01: Build default Jev browser QA

- Objective: close both slices in `checks.md`, in order.
- The plan, DX contract, security specification, threat model, and checks are approved; checks and test-policy rows are fixed.
- The working tree already contains intentional planning edits in `.specs/STATE.md`, `.specs/AD-INDEX.md`, and the feature packet. Preserve them.
- Size gate: S1 ~45k plus S2 ~12k = ~57k, below the 150k one-builder budget.
- Current source supports classifying only a typed timeout thrown before the Jev factory returns as pre-action. Once `Agent.run()` is invoked, any timeout is unsafe unless independent inspection/reset happens first.
