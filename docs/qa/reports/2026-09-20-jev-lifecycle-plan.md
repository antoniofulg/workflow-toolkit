# QA Plan — Jev lifecycle — 2026-09-20

**Phase:** `wtk-qa-plan`
**Disposition:** READY FOR QA EXECUTE
**Frozen snapshot:** `feat/jev-lifecycle` @ `2f9c575b97c5b98d9b8cc3b3ff8d66a9115239fd`
**Profile:** [`docs/qa/README.md`](../README.md)
**Persona:** Workflow operator
**Journey:** [`J-consult-jev-adviser`](../journeys/J-consult-jev-adviser.md)
**Scenario:** [`QAS-consult-jev-adviser`](../scenarios/QAS-consult-jev-adviser.md), retained as `untested`
**Charter:** [`CH-consult-jev-adviser-2026-09-20`](../charters/CH-consult-jev-adviser-2026-09-20.md)

## Scope and criterion disposition

The changed public surface is a local Node CLI plus agent-facing phase guidance. The existing
journey and scenario own the promise; no duplicate scenario or adjacent canary was added.

| Criteria | Execute disposition |
| --- | --- |
| AC1–2 | Walk local preview for every supported phase with synthetic input; observe typed request, exit 0, and residue-free local behavior. |
| AC3 | Live advice remains untested: keys and network are forbidden. Assigned smoke is connectivity evidence only. |
| AC4 | Technical-only deterministic validation matrix; do not repeat it as QA. |
| AC5 | Walk only missing-key `--send`; other provider failures remain technical evidence. |
| AC6 | Technical-only request-count/retry invariant; no provider request is authorized. |
| AC7 | Inspect advisory/no-authority policy and compare checkout residue; actual host behavior remains untested. |
| AC8–9 | Technical-only credential/redirect/error/context boundaries; QA reads no secret and uses only synthetic stdin. |
| AC10 | Walk changed phase/evidence/options hashes plus identical/reordered normalization controls. |
| AC11–13 | Inspect all direct phase routes and shared policy; walk missing-key output. Configured host consultation, advice evaluation, and continuation remain untested. |
| AC14 | Technical-only core installer and package inventory; JEV-007/JEV-008 already cover both assemblies. |

The charter carries the per-criterion detail, exact observables, six probes, stop conditions, and
the rule that successful offline legs do not change the configured-host scenario to `pass`.

## Technical forward receipt

- Range: `012f1295fe25ad8c152c631a8f4918a260310ec8..2f9c575b97c5b98d9b8cc3b3ff8d66a9115239fd`.
- Independent Technical Verification: PASS, 8/8 checks with located assertions and 14 recomputed
  coverage sets with zero unproven members.
- Discrimination: 5 bounded mutants injected in an isolated worktree; 5 killed; no survivor.
- Fresh proof gate:
  `node --test --test-name-pattern='JEV-00[1-8]' tests/installer/jev-adviser.test.js tests/installer/package.test.js`
  — exit 0, 8 passed, 0 failed, 0 skipped.
- Completion gate:
  `python3 .agents/skills/wtk-lean/scripts/validate_verification.py jev-lifecycle`
  — exit 0, 0 errors, 0 warnings; coordinator independently repeated it with the same result.
- The coordinator's one authorized synthetic provider smoke exited 0 in 0.813 seconds with model
  `jev-1.13.0`, 506 input tokens, 75 output tokens, and valid typed advice. This establishes
  connectivity only, not host compliance, savings, decision quality, or a QA verdict.

This receipt preserves the bounded technical result after transient feature artifacts are removed;
it is forward evidence, not a substituted user walk.

## Planned interface and evidence

- Adapter: profile-declared CLI/manual adapter with independent filesystem readback.
- Runner: checkout-local Node executable; no browser, server, package registry, provider, or
  framework.
- Public command: `node .agents/skills/wtk/scripts/advise.mjs --phase <phase> [--send]`.
- Policy readback: the 14 direct lifecycle entrypoints and
  `.agents/skills/wtk/references/jev-adviser.md`.
- Disposable evidence: `docs/qa/evidence/2026-09-20-jev-lifecycle/`.
- Durable execution report: `docs/qa/reports/2026-09-20-jev-lifecycle.md`.

## Limitations and stop conditions

No key may be read or loaded, including the trusted central QA environment file. No network call,
live provider leg, actual host-agent judgment, package installation, product edit, or test double is
authorized. Stop any path that attempts one. Missing live capability leaves
`QAS-consult-jev-adviser` as `untested`, not `blocked-verify`.

No QA command was executed during this planning phase.

## QA Execute handoff

Run canonical `wtk-qa-execute` against the frozen snapshot and charter above. Finish the safe
preview, missing-key, hash, route-inspection, and residue legs; stop the dependent provider/host
legs. Record exact commands, public paths, exit codes, evidence, independent readback, and
limitations. Update only the owning scenario from observed results. Any defect returns as one
batched Implementer handoff; the QA observer does not fix product code.

