# Security

**Read when:** the change touches runtime code, configuration, dependencies, schemas, deployment, data
flows, or public behaviour. Pure documentation and formatting changes are exempt.

**Why this exists:** Security that lives only in a review at the end is theatre. Surfaces declared at
Specify become countable `SEC-` cases; review looks for what the table missed. A control with no test
is a memory, not a requirement.

Security is built, not reviewed in. Review catches what construction missed; it is the last line, not
the first. This guideline is self-contained — it does not depend on any other security document.

Product rules stay authoritative in the consuming project's product docs. Architecture invariants stay
authoritative in its architecture docs. This says how feature work applies and verifies them; it does
not restate them.

## External filesystem writers

Run an external tool that writes files in an isolated environment or with explicitly allowed
directories. Validate destination paths and symlinks before the first write. Preserve destination-only
files and never delete them automatically.

## 1. Before coding — build with the right guidance loaded

1. If the optional `security-implementation` skill is installed, apply it to secure-by-default
   implementation and hardening. Otherwise use the baseline checks in this reference and surface any
   Critical or High concern encountered immediately.
2. If the optional `security-spec` skill is installed, invoke it during Specify to define security
   requirements and negative tests. Otherwise add those cases directly to the feature contract.
3. If the optional `security-threat-model` skill is installed, invoke it during Specify or Design
   when section 4's surfaces apply. Otherwise record the assets, boundaries and threats here.
4. Identify affected languages, frameworks and versions; load the applicable concept references.
   Verify framework APIs and defaults using the consumer's documentation tools and current official
   docs for the installed version. Use a matching framework skill when available; record uncertainty.
5. **Convert that guidance into security outcomes in the spec and the test contract.** Outcomes, not
   controls: a test asserts the required *result*, never the presence of a particular implementation.

## 2. At Specify — declare the surfaces

Every feature declares which of these eleven surfaces it touches. The identifiers are stable; never
rename them.

| ID | Surface |
| --- | --- |
| S1 | Runtime, configuration, dependency, schema, deployment, data-flow or public-behaviour change |
| S2 | External route, ingress or trust boundary |
| S3 | Authentication, session, cookie, CSRF, IP trust or rate limit |
| S4 | Server-side authorization and ID- or tenant-identified resources |
| S5 | Credentials, tokens, secrets, keys or data delivered to the browser |
| S6 | Untrusted input/output and HTML, URL, SQL, shell or filesystem sinks |
| S7 | Uploads, SVG, active content, parsers or decoders |
| S8 | Personal, contact, tenant data or user-generated content |
| S9 | External providers, callbacks, webhooks, jobs or queues |
| S10 | Persistence whose confidentiality or integrity affects product authority |
| S11 | Deployment, processes or isolation |

`## Security Surfaces` goes in `plan.md`. One row per applicable surface, naming the control and the
`SEC-NNN` requirements that prove it:

```markdown
## Security Surfaces

| ID | Surface | Control | Requirements |
| --- | --- | --- | --- |
| S2 | `POST` public create route, unauthenticated | Per-IP rate limit, strict input validation | SEC-001, SEC-002 |
| S6 | Free-text name rendered back to the page | Escaped on output; no HTML sink | SEC-003 |
| S8 | Email stored at rest | Never returned by any list endpoint | SEC-004 |
```

A surface with no control is an open question, not a finished row. Surfaces the feature does not touch
are simply absent — do not write a row to say so.

## 3. At the test contract — abuse cases get IDs

Every control becomes one or more `SEC-` cases in `.specs/features/<feature>/checks.md`. Each case
uses the native checks contract: its claim has a concrete outcome and one or more named proofs, and
each enumerated abuse-case member appears in `Coverage`. SEC IDs trace to native `C<n>` checks, not
tasks, and are audited for orphaned claims like the rest. See `.agents/skills/wtk/references/test-contract.md` and
the [native Lean checks reference](../../wtk-lean/references/checks.md).

Examples only — not a `checks.md` schema:

| ID | Abuse case | Attempt | Expected |
| --- | --- | --- | --- |
| SEC-001 | Unauthenticated read of another account's records | `GET` the list route, no session | 401, no body leakage |
| SEC-002 | Submission floods the endpoint | 100 requests in 10s from one IP | 429 past the limit, no rows written |
| SEC-004 | Personal data leaks through a list endpoint | `GET` the list route as an entitled operator | No `email` field in any item |

This is the whole point: **a control becomes countable instead of remembered.** Pick the cheapest
discriminating layer — most abuse cases are integration tests against the route, not e2e.

Authentication, session, cookie, CSRF, trusted-IP, rate-limit, authorization and tenant-identity
outcomes are layer-independent. A cheaper layer may discriminate the behaviour, but it never removes
the permanent security smoke coverage when the changed surface is unknown, transversal, or
classification-failed.

Browser fixtures use scenario-owned identities and IPs, in-memory session state, exact `finally`
cleanup, and secret-free diagnostics. **No test artifact ever contains credentials, cookies, database
URLs, session headers, or reusable tokens.**

## 4. Threat model — when the surface is serious

Write a scoped threat model during **Specify or Design, before coding**, when the feature introduces
or changes any of S2, S3, S4, S5, S7, S8, S9, S10 or S11. S1 and S6 alone do not trigger one.

Scope it to `.specs/features/<feature>/` and write the report to
`.specs/features/<feature>/threat-model.md`. Ground the deployment, data-sensitivity and attacker
assumptions in canonical documentation, not invention.

Run it again when scope, entrypoints, architecture, assets, trust boundaries or attacker assumptions
change. Behaviour-preserving refactors do not need one.

## 5. At review — the residual only

With surfaces declared and controls tested, review looks for what the table missed rather than
rediscovering the table.

If the optional `security-review` skill is installed, the independent verifier uses it to review the
complete feature diff. It detects flaws in code that now exists — injection, exposed secrets, broken
access control, vulnerable dependencies — which the before-coding skills cannot catch because they
ran before the code was written. When it is absent, the verifier applies the surface list, proof
records, and native inspection below and reports that the optional review skill was unavailable.

Findings carry the same weight as any other: **unresolved Critical or High blocks completion**,
regardless of any project priority label. Accepting a risk requires your explicit approval and an
append-only `AD-NNN` in `.specs/STATE.md`.

## Evidence

The feature's validation report ends with a security section carrying:

- The security skills applied
- The threat-model path, or a specific reason it does not apply
- Every `SEC-NNN`, its surface, `PASS` or `FAIL`, and a resolvable `` `file:line` `` citation
- Open Critical and High counts, each an actual number
- The verdict

**A verdict with no requirement behind it is not evidence**, and a severity named without a number is
not a count. Documentary presence never proves the absence of a vulnerability.

## Scoped campaigns, outside the feature loop

Feature-time security covers the feature. It does not cover the codebase.

Run a scoped security review against an area on its own schedule. It reads the whole codebase to
build confidence but reports only on the scoped area, and what it finds becomes filed issues fixed as
their own work. Never on a feature's critical path.

Two rules keep a campaign useful: **research broadly, report narrowly** — trace where the input
actually comes from and what protections already exist before flagging; and **high confidence only**
— a finding needs a concrete path from attacker-controlled input to a vulnerable sink, never a
pattern match.

## What this drops from earlier ceremony

The substance is unchanged. What goes is the bookkeeping:

- The eleven-row declaration required a row for **every** surface including inapplicable ones. Absent
  now means not applicable.
- A gate that only reads the *shape* of security evidence, and never reads product code looking for a
  flaw, is not a security gate. Keep it out of the full gate.
- The separate security-review artifact folds into the validation report. One evidence file.
