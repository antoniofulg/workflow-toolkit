# Reconnaissance and coverage

## Reconnaissance

Map, with repository-relative source evidence:

1. Product actions, principals, protected resources and ordinary authority.
2. Languages, frameworks, build systems and source-visible deployment modes.
3. HTTP/browser, RPC/message, file, CLI/config, plugin/CI, cloud-event, AI/tool,
   native/mobile and local-IPC entry surfaces.
4. Identity, authorization, parsing, isolation, lifecycle and resource controls.
5. Stored and derived copies, privilege transitions, retries and fallback paths.
6. Offline checks that could safely resolve important behavior; do not run them yet.

Always inventory resolved dependency manifests and seed a current-advisory unit.
Also seed repository secret discovery. Use a scanner only after verifying that its
terminal/model output suppresses values; retain path, line and credential type, never
the value, partial value or fingerprint. If safe redaction cannot be guaranteed,
inspect metadata through a redacting wrapper or mark the unit blocked. Never try a
credential against a service or infer validity from its shape.

Separate runtime, build/CI/dev and tests. A fixture is not a deployed component.
Deployment facts absent from source remain unknown in both directions.

For a strict worker budget, reserve one coverage critic and enough fresh verifiers
for expected candidates before assigning hunters. If the budget cannot fund basic
reconnaissance plus those gates, narrow scope or use quick profile before launching
workers. Never spend the verification reserve to make coverage appear broader.

## Coverage units

Create one unit for each material combination of entry surface, trust boundary,
subsystem and applicable attack class. Split lifecycle modes when normal, retry,
rollback, migration, recovery or deletion paths enforce different controls.

Each unit records:

- stable `coverage_id`, human labels and repository-relative starting paths;
- `status`: `planned`, `covered`, `candidate`, `blocked`, `deferred`,
  `out_of_scope` or `not_applicable`;
- reviewed paths, candidate fingerprints and exact unresolved facts.

`covered` and `candidate` require reviewed paths. `candidate` alone carries
fingerprints. `blocked` names the missing evidence. `deferred`, `out_of_scope` and
`not_applicable` carry reasons, never evidence implying coverage.

For prior runs, compare relevant current source and conditions. Revalidate changed
confirmations. Prior unresolved, blocked or deferred units remain work. An unchanged
rejection suppresses only its exact failed claim, not the surrounding coverage unit.

## Coverage critic

After a hunter wave, ask a critic to inspect the architecture, ledger and source for
unmapped entrypoints, parallel paths, lifecycle modes, unjustified exclusions and
units closed without supporting paths. Add accepted gaps as stable units. A quick
profile defers them; standard/deep profiles assign them while budget remains.

Coverage state measures examined work. It never proves the absence of unknown bugs.
