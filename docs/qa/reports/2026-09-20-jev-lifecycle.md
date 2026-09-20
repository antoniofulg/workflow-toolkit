# QA Execute — Jev lifecycle — 2026-09-20

- **Charter:** [`CH-consult-jev-adviser-2026-09-20`](../charters/CH-consult-jev-adviser-2026-09-20.md)
- **Branch / HEAD:** `feat/jev-lifecycle` @ `2f9c575b97c5b98d9b8cc3b3ff8d66a9115239fd`
- **Persona:** Workflow operator
- **Adapter:** CLI/manual through the public Node command plus independent filesystem readback, as declared in [`docs/qa/README.md`](../README.md)
- **Exact public path:** `node .agents/skills/wtk/scripts/advise.mjs --phase <phase> [--send]`
- **Environment:** checkout-local Node; synthetic stdin; `TYPESAFE_API_KEY` explicitly absent; no network, browser, server, registry, provider, package install, or external runtime
- **Technical gate:** `node --test --test-name-pattern='JEV-00[1-8]' tests/installer/jev-adviser.test.js tests/installer/package.test.js` — exit 0, 8 passed, 0 failed, 0 skipped at frozen HEAD; not rerun because QA evidence did not change technical scope
- **Evidence root:** `docs/qa/evidence/2026-09-20-jev-lifecycle/` (disposable, ignored)
- **Opening porcelain:** user-owned `skills-lock.json`, `.agents/skills/typesafe-ai/`, `.claude/skills/typesafe-ai`; verifier-owned `.specs/features/jev-lifecycle/verification.md`, this charter, and the planning report

## Scenario matrix

| Scenario | Verdict | Evidence / limitation |
| --- | --- | --- |
| `QAS-consult-jev-adviser` | untested — all reachable offline legs passed | `01-cli-observations.json`; `02-route-policy-readback.json`. Configured provider advice and actual host-agent compliance remain unreachable under the no-key/no-network profile. |

## Walk

### Public six-phase preview

The real public helper ran once for each of `plan`, `build`, `verify`, `review`, `qa`, and `ship`
with identical synthetic stdin and `TYPESAFE_API_KEY` explicitly removed from the child environment.
All six exited 0 and produced one parseable JSON object with `status: preview`, a phase-matching
state, model `jev-latest`, a 64-hex-character hash, a Choice containing both supplied candidates plus
`insufficient_evidence`, and an independent Noul. The six phase hashes were distinct. No command used
`--send`, key material, a provider, or a test mock.

Evidence: [`01-cli-observations.json`](../evidence/2026-09-20-jev-lifecycle/01-cli-observations.json).

### Missing-key send fallback

The same public helper ran with `--phase build --send` while `TYPESAFE_API_KEY` was explicitly absent.
It exited 3 and wrote exactly `{"status":"unavailable","reason":"missing_key"}`. No key file was
read or sourced; the command returned before any provider path and created no checkout artifact.

Evidence: `01-cli-observations.json` → `missing_key`.

### Changed-input fingerprint

Four additional local previews used identical input, reordered option keys, changed evidence, and
changed options. Independent reload found:

- identical and reordered normalized input retained build hash
  `2c9ecf7f5c683cdc8c10d5c014745cffa7b1472d72e24e522262ad7db0154f26`;
- changed evidence produced
  `f1d09a520a7e9f23ed04d02b0bef9308a26ec39e6096e4c48a3e78d3089429b3`;
- changed options produced
  `4579d937585edfb3c127351681708195afe59fd3d96471dee9d9737d2cf5112a`;
- changing build to plan produced
  `5e98dae1e9d6b9549fc27c29ebf60bceb61be2ef380209a42247fed4c731910e`.

This settles the reachable stale-input discriminator without claiming cache or authority behavior.

### Direct phase routes and shared policy

A fresh manual readback process opened the 14 entrypoints named by the charter. Every Markdown link
resolved to `.agents/skills/wtk/references/jev-adviser.md`. Independent policy checks confirmed:

- every semantic path decision consults Jev when a key is available, even with a preferred answer;
- evidence is minimal and non-sensitive, and Choice plus Noul share one request;
- the only optional credential source is the existing trusted caller environment, loaded quietly;
- Jev retains no action, permission, approval, or gate authority;
- unavailable advice continues through existing reasoning; changed input discards stale advice;
- all six phase examples are present.

Evidence: [`02-route-policy-readback.json`](../evidence/2026-09-20-jev-lifecycle/02-route-policy-readback.json).

### Independent reload

A separate Node process reloaded both evidence files and evaluated ten observables: six previews,
preview contract, distinct phase hashes, exact missing-key result, normalization stability, changed
evidence/options/phase hashes, 14 shared links, and policy completeness. All ten were `true`; exit 0.

The configured provider and actual host-agent legs were not attempted. The coordinator's earlier
synthetic live smoke remains separately labeled integration evidence and does not change this QA
result.

## Findings

None. Every safe independent leg on the frozen snapshot matched the charter. No bug record or
Implementer handoff was created.

## Limitations

- Network and provider credentials are forbidden by the repository QA profile, so no configured
  `advice` result was observed.
- Filesystem policy readback proves the shipped route and instructions, not that a future host agent
  will consult Jev, evaluate its recommendation, continue on insufficient evidence, or avoid an
  automatic action in a real session.
- Technical Verification and the coordinator's one synthetic provider smoke remain forward evidence,
  not user-walk evidence. Consequently `QAS-consult-jev-adviser` remains `untested` rather than
  `pass` or `blocked-verify`.

## Cleanup and residue

No disposable consumer, runtime, package, server, or external process was created. Raw evidence is
contained under the checkout-owned ignored evidence root. Closing porcelain matched the opening
snapshot plus the planned execution report and scenario evidence/report pointers. User-owned
`skills-lock.json`, `.agents/skills/typesafe-ai/`, and `.claude/skills/typesafe-ai` remained
unchanged. No product file changed.

## Commands and exit codes

| Command / observation | Count | Exit | Reported wall time |
| --- | ---: | --- | ---: |
| `env -u TYPESAFE_API_KEY node .agents/skills/wtk/scripts/advise.mjs --phase <plan|build|verify|review|qa|ship>` with synthetic stdin | 6 | six × 0 | 0.745 s total |
| Same public command with `--phase build --send`, key absent | 1 | 3, expected unavailable | 0.000004 s |
| Same public command for identical, reordered, changed-evidence, and changed-options hash cases | 4 | four × 0 | 0.066 s total |
| Fresh filesystem route/policy readback | 1 | 0 | 0.045 s |
| Independent evidence reload and ten-observable check | 1 | 0 | 0.008 s |

Public CLI commands: 11 in 0.811 seconds reported wall time. Walk/readback commands: 13 in 0.864
seconds. No retry, test mock, technical gate rerun, provider call, or network command occurred.
