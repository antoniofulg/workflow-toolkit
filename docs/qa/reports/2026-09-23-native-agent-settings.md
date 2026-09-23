# QA Execute — Project-owned agent settings — 2026-09-23

- **Charter:** [`CH-native-agent-settings-2026-09-23`](../charters/CH-native-agent-settings-2026-09-23.md)
- **Product snapshot:** `e6002ca18d4fe07f842acff8c03efeca16748a72`
- **QA plan snapshot:** `3895257327b69a2028630fecb36fce1804ece972`
- **Personas:** Workflow adopter; Workflow operator; Repository reader
- **Adapter:** Vercel Skills CLI 1.5.23/manual, public Python and Node CLIs, and independent filesystem readback through [`docs/qa/README.md`](../README.md)
- **Environment:** local frozen source copy and checkout-owned disposable consumers; no network, registry, browser, server, provider call, or optional companion installation
- **Technical gate:** independent Technical Verification PASS at `e6002ca1`; `bun run test:all` reused there with 80 Bun tests, 20 Node tests, and all tracked Python suites passing
- **Evidence root:** `docs/qa/evidence/2026-09-23-native-agent-settings/` (disposable and ignored)
- **Opening porcelain:** clean at QA plan snapshot `38952573`

## Scenario matrix

| Scenario | Verdict | Evidence / limitation |
| --- | --- | --- |
| `ADP-install-versioned-workflow-package` | pass | Skills CLI found and installed 12/12; 85 local references resolved; no config payload or host mutation. [`install-readback.json`](../evidence/2026-09-23-native-agent-settings/install-readback.json). |
| `ADP-adopt-workflow-safely` | untested — all reachable public legs passed | Install, 18 native files, host sentinels, exact and edited packet migration, and managed conflict passed. Public rollback injection is unavailable. Install and migration evidence. |
| `ADP-resolve-legacy-adoption-conflicts` | untested — all reachable public legs passed | Public preview/apply removed 18 exact packets, preserved 18 edited packets, and refused modified managed content with no writes. Public rollback injection remains unavailable. [`migration-readback.json`](../evidence/2026-09-23-native-agent-settings/migration-readback.json). |
| `CFG-route-project-native-agent-settings` | pass | Create, resume, refresh, and reload passed for Claude, Codex, and Cursor; 18 native files stayed byte-identical and snapshots contained identity only. [`route-readback.json`](../evidence/2026-09-23-native-agent-settings/route-readback.json). |
| `CFG-keep-local-artifacts-out-of-git` | fail | Local runtime ignores and package boundary passed, but tracked `.claude/skills/wtk-config` is a dangling link. [`BUG-20260923-source-retains-removed-wtk-config-link`](../bugs/BUG-20260923-source-retains-removed-wtk-config-link.md). |
| `CFG-resolve-deep-review-cadence` | pass | On-demand review, direct review skill, sequential builder, QA `auto`, and `stall_attempts = 3` passed; third unchanged stall halted. [`defaults-readback.json`](../evidence/2026-09-23-native-agent-settings/defaults-readback.json). |
| `QAS-use-optional-jev-qa-adapter` | untested — reachable helper legs passed | Missing prerequisite and pre-action timeout allowed safe fallback; post-action timeout forbade fallback; every result stayed `not-passed`. No live browser/provider/reload oracle. [`qa-adapter-readback.json`](../evidence/2026-09-23-native-agent-settings/qa-adapter-readback.json). |
| `REL-report-current-workflow-release` | fail | Package, lockfile, README, and 12-skill install agree. Current changelog guidance is absent and the source retains the dangling config alias. [`release-readback.json`](../evidence/2026-09-23-native-agent-settings/release-readback.json). |
| `DOC-read-explicit-workflow-provenance` | pass canary | README, pack guide, notices, Lean attribution, QA provenance, and optional-companion scope remain consistent. Existing scenario verdict remains valid. Same release evidence. |

## Installation and host ownership

Skills CLI 1.5.23 discovered and installed the README's exact 12-skill set from a frozen local copy
of `e6002ca1`. Independent `skills list --json` and filesystem reload found all 12 canonical
directories and resolved 85 local references. No `wtk-config`, WTK TOML, provider template, npm
installer, adoption manifest, or source-only guideline dependency appeared in the consumer.

Existing `AGENTS.md`, `CLAUDE.md`, ignore files, product context, knowledge files, unrelated
configuration, and unrelated data retained exact bytes. All 18 Claude, Codex, and Cursor native
agent files retained bytes and modes. The Skills CLI created only its own skill copies and lock
scope. Evidence: [`install-readback.json`](../evidence/2026-09-23-native-agent-settings/install-readback.json).

## Native routes and fixed defaults

Installed `workflow_route.py` created, resumed, refreshed, and reloaded one feature for each native
provider. Resume ignored a different requested provider and retained frozen identity. Every
snapshot had the nine documented fields, five provider/agent-file role routes, on-demand review,
and disabled parallelization; none contained model, effort, config version, or generated packet
content. All 18 native files remained byte-identical and no TOML appeared.

The installed convergence CLI established one minimum failure set, then recorded three unchanged
failures. Consecutive stalls were `0,1,2,3`; results were `open,open,open,halted`; every generation
reported `stall_attempts: 3`; and the last reason was `stall_threshold_reached`. Installed
instructions exposed the direct `wtk-deep-review` route, on-demand default, sequential builder, and
QA `auto`. Evidence: [`route-readback.json`](../evidence/2026-09-23-native-agent-settings/route-readback.json)
and [`defaults-readback.json`](../evidence/2026-09-23-native-agent-settings/defaults-readback.json).

## QA adapter boundary

The public installed helper preflight exited `2` with `status: unavailable` when credentials were
absent and selected Playwright MCP as a safe fallback without starting an action. Scrubbed installed
helper probes classified constructor timeout as `pre-action-timeout` with safe Playwright fallback,
and classified timeout after a recorded click as `post-action-timeout` with no fallback. Both
remained `qa_verdict: not-passed`. No browser or provider was launched, so the end-to-end consumer
scenario remains `untested`. Evidence: [`qa-adapter-readback.json`](../evidence/2026-09-23-native-agent-settings/qa-adapter-readback.json).

## Legacy packet migration

Public preview and apply listed and removed all 18 exact historical Claude, Codex, and Cursor
packets without current provider templates. An unrelated `0600` file retained bytes and mode. A
separate full edited matrix retained all 18 packets, and a modified adoption-owned file made apply
exit `1` with an identical recursive snapshot.

The copied CLI's first `/tmp` invocation returned no report because its entrypoint compared the
symlinked path with a canonical `file:` path; no migration action started. The one clean retry used
the real checkout path and passed. Public CLI help exposes no safe rollback fault injection, so
rollback stays `untested`. Evidence: [`migration-readback.json`](../evidence/2026-09-23-native-agent-settings/migration-readback.json).

## Release and provenance

The package manifest, Bun lockfile, README, installed tree, and skill provenance agree on the
12-skill, project-native settings boundary. The adjacent provenance canary remains valid.

Two independent defects remain. The tracked `.claude/skills/wtk-config` alias points to a removed
directory. Also, `CHANGELOG.md` leaves `Unreleased` empty; the newest visible setup guidance is the
historical `1.4.1` block with the retired npm installer and bundled security promise. Historical
release text should remain intact; current unreleased guidance or a new matching release is needed.

## Findings

1. Major: [`BUG-20260923-changelog-describes-retired-installer`](../bugs/BUG-20260923-changelog-describes-retired-installer.md) — current changelog guidance is absent, leaving retired installation instructions as the newest visible route.
2. Minor: [`BUG-20260923-source-retains-removed-wtk-config-link`](../bugs/BUG-20260923-source-retains-removed-wtk-config-link.md) — tracked Claude alias points to the removed config skill.

## Limitations

- Network and registry access are outside this QA profile; Skills CLI uses an exact local source copy.
- No live browser, Jev runtime, provider, or Playwright MCP is available under this profile.
- The public migration CLI exposes no safe rollback fault injection.
- Agent-selection behavior beyond deterministic route state remains Technical Verification evidence.

## Cleanup and residue

The recorded source, consumer, route, convergence, QA-adapter, exact-packet, edited-packet,
conflict, and stalled-retry roots under `/tmp/wtk-native-settings-qa.6fBrJg` were removed. Closing
source porcelain contains only this cycle's verifier-owned report, eight scenario updates, and two
bug records. Ignored evidence remains under the declared evidence root. No product file changed.

## Commands and results

| Command / observation | Exit | Reported wall time |
| --- | ---: | ---: |
| Local Skills CLI discovery | 0; found 12 | 0.9 s tool wall |
| Exact 12-skill Skills CLI install | 0; installed 12 | 2.5 s tool wall |
| Independent Skills CLI list and installed-tree reload | 0; 12 listed | 2.0 s tool wall |
| Install, sentinel, native-file, and reference readback | 0 | 0.3 s tool wall |
| Claude/Codex/Cursor create, resume, refresh, and reload | 0 | 0.8 s tool wall |
| Convergence CLI plus QA preflight/fallback probes | 0; preflight 2 expected | 0.6 s tool wall |
| Migration first attempt | no action; empty report from `/tmp` path alias | 0.3 s tool wall |
| Migration clean retry: preview/apply/edited/conflict | 0 / 0 / 0 / 1 expected | 0.4 s tool wall |
| Release/package/provenance readback | 0; two defects reported | 0.3 s tool wall |
| `bun test tools/shared/tests/qa-skills.test.ts` | 0; 38 pass, 0 fail, 538 expectations | 0.8 s tool wall |

## Fix-loop accounting

QA opened one return-to-implementation event containing two new findings. No fix batch or recheck
ran in this session, so the return remains pending and first-pass QA acceptance is no.

## Execution metrics

Actor `/root/native_settings_qa_execute`; OpenAI GPT-5; billing tier unavailable. Measured interval
`2026-09-23T21:19:47Z` to `2026-09-23T21:42:30Z` (22m43s, partial: initial skill/context load
preceded the first timestamp). QA completed one execution round; tokens and token cost are
unavailable because the harness exposed no usage counters.

Total measured elapsed and cumulative actor time are both 22m43s partial. Validation overhead
included one targeted gate run at 0.8s; no full gate ran in QA, and the independent Technical
Verification gate was reused from `e6002ca1`. One return to implementation is open, zero fix loops
are complete, one return is pending, and first-pass QA acceptance is no. The initial migration
invocation added 0.3s; resolving the scratch source to its canonical path before launch would avoid
that retry. No waiting or external blocker time was measured.
