# Workflow Toolkit 1.3.0 release validation

This is scoped release-owner validation, not a new host-agent QA verdict.

- Package source: `e525437`, prepared from the independently verified Jev feature.
- Prior technical receipt: `2026-09-20-jev-lifecycle-plan.md`; offline feature QA:
  `2026-09-20-jev-lifecycle.md`. Product behavior is unchanged after that verification except
  release identity constants moving from 1.2.0 to 1.3.0.
- Release identity: manifest, installer constant, backup metadata, README, changelog and current
  release scenario agree on `1.3.0`. The dependency graph and Bun lockfile are unchanged.

## Selected checks

`bun test tools/shared/tests/qa-skills.test.ts -t 'IT-005 / AIM-11 reports release version and Bun lock identity consistently'`
passed 1 test with 19 assertions.

`node --test tests/installer/engine.test.js tests/installer/transaction.test.js` initially passed
67 of 68 tests. The remaining future-version fixture still used 1.2.1; the 1.3.0 release makes
that an older version. The fixture now uses 1.3.1, preserving rejection of future manifests.
`node --test --test-reporter=spec --test-name-pattern='STATE-001' tests/installer/engine.test.js`
passed all 3 affected tests. Other passing results remain valid; no assertion was removed or weakened.
No new full-repository gate was run.

## Exact archive and consumer

Packed from a clean detached checkout, excluding the operator's unrelated uncommitted TypeSafe
skill and lockfile edits:

`bun pm pack --filename /tmp/wtk-release-1.3.0.XZ8LNi/workflow-toolkit-1.3.0.tgz --ignore-scripts`

- 233 archive members, all under `package/`, with no traversal path.
- SHA-256: `c091a593d75a73ca3601c4df33b82b1c7bf99bde414cdac84253fb318469f35c`.
- Integrity: `sha512-0wc9Ge38eqeJwG+K2FzZXrmbH+FW2zEC7pHuJahGvXo2MD0bbzxOwC9jgqlzl3mDUfIBNHiLoy7U8Tahex6ePA==`.
- Adviser command and shared reference are present. Environment files, `.npmrc`, `.git`,
  `node_modules`, `.specs` and Python caches are absent. The archived skills lock matches committed
  source bytes, not the dirty working copy.

The extracted public CLI installed core into a disposable Git consumer through its terminal
wizard. Runtime dependencies came from the already installed checkout dependency tree; no package
registry install occurred in this check. Independent readback found version 1.3.0, core only,
185 managed files, byte-identical adviser/reference files, and successful credential-free preview.
A fresh installer process reported `Selected modules are up to date. No files will change.`
The consumer's Git status remained clean after its baseline commit and reload.

## Boundaries

The exact archive is the publication candidate; remote registry and GitHub readback occur during
authorized delivery. These local checks do not prove actual host-agent policy compliance or net
token savings. The existing Jev scenario retains its recorded live-host limitation.
