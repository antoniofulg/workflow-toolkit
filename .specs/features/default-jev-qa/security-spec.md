# Default Jev browser QA security specification

## Security surfaces

- `.wtk.toml` gains an untrusted public enum controlling browser-driver selection.
- Jev and Playwright MCP cross external provider, local-process, browser, page-content, and model-result boundaries.
- Timeout classification controls whether a second driver may act against the same fixture.
- Provider credentials and browser-session data remain sensitive and outside configuration/evidence.

## Assets and actors

- **Assets:** delegated QA authority, fixture integrity, TypeSafe/Gateway/MCP credentials, dedicated browser state, evidence integrity, filesystem/network reach.
- **Legitimate actors:** consuming-project operator selecting an adapter; assigned Verifier executing the declared charter.
- **Adversarial actors:** caller supplying malformed config; page/provider content influencing actions or diagnostics; compromised or misleading external dependency.
- **Non-capabilities:** page/model output cannot change `.wtk.toml`, declare a journey non-consequential, authorize fallback, or turn driver completion into QA pass.

## Trust boundaries

| Origin | Destination | Trust change | Policy |
| --- | --- | --- | --- |
| consumer `.wtk.toml` | Python and installer-side validators | untrusted local text controls routing | identical closed enum/default in both readers |
| Verifier environment | Jev/Playwright providers | secrets enter external clients | process-only credentials; no config/evidence copy |
| Jev/browser/page | fallback selector | uncertain effects could cause replay | fallback only on unavailable or proven pre-action timeout |
| driver result | QA verdict | probabilistic completion becomes evidence | independent readback after reload owns pass |
| adapter | evidence/report | external errors become local artifacts | allowlist and redact; exclude raw exceptions |

## Abuse cases

| ID | Actor and capability | Asset | Path | Adverse outcome | Linked requirements |
| --- | --- | --- | --- | --- | --- |
| ABUSE-001 | local caller controls `.wtk.toml` values | QA routing integrity | unknown adapter or hidden key bypasses intended selection | unapproved tool executes or configuration fails ambiguously | SEC-001, SEC-002 |
| ABUSE-002 | page/provider can fail after an interaction | fixture integrity | timeout mislabeled as pre-action and Playwright repeats the journey | duplicate or unintended mutation | SEC-004, SEC-005 |
| ABUSE-003 | provider exception can contain secrets/page data | credentials and browser state | raw failure copied into result/evidence | reusable secret or private state disclosure | SEC-003 |
| ABUSE-004 | driver controls its completion signal | QA verdict integrity | Jev or fallback completion becomes pass | false-green QA status | SEC-006 |
| ABUSE-005 | missing Jev dependency or credential blocks default | QA availability | default Jev cannot start and no fallback runs | eligible fixture remains untested despite Playwright availability | SEC-004 |

## Security requirements

| ID | Abuse cases | Observable rule |
| --- | --- | --- |
| SEC-001 | ABUSE-001 | IF `[qa]` contains an unknown key or `browser_adapter` is outside the six-value enum THEN both config validators SHALL reject it before adapter execution. |
| SEC-002 | ABUSE-001 | WHEN `[qa].browser_adapter` is absent THEN selection SHALL resolve to `auto`; no implementation-name alias SHALL be accepted. |
| SEC-003 | ABUSE-003 | The configuration, result, evidence, stdout, stderr, and QA report SHALL contain no provider credential, cookie, authorization value, reusable token, or raw exception text. |
| SEC-004 | ABUSE-002, ABUSE-005 | IF Jev is unavailable or a typed timeout is proven before a product action THEN fallback eligibility SHALL be explicit and SHALL select Playwright MCP first. |
| SEC-005 | ABUSE-002 | IF an action began or the action state is uncertain THEN automatic fallback SHALL be forbidden until independent inspection or fixture reset establishes safe state. |
| SEC-006 | ABUSE-004 | WHEN any driver reports completion THEN only matching independent readback after reload SHALL produce QA pass. |

## Negative-test seeds

| IDs | Setup | Action | Expected |
| --- | --- | --- | --- |
| SEC-001, SEC-002 / ABUSE-001 | absent key, six valid values, `jev-ultrafast`, unknown value, unknown key | validate with Python and installer readers | absent resolves `auto`; six valid pass; all others reject before execution |
| SEC-003 / ABUSE-003 | sentinel credentials and timeout exception carrying a sentinel | exercise every terminal/fallback path | sentinel and raw exception absent from all outputs and evidence |
| SEC-004 / ABUSE-005 | missing Jev prerequisite and available Playwright declaration | select adapter | Playwright MCP selected first without a Jev call |
| SEC-004, SEC-005 / ABUSE-002 | typed timeout before any product action, then timeout after/without provable action state | select continuation | first permits Playwright; latter paths forbid automatic fallback |
| SEC-006 / ABUSE-004 | each driver reports completed with mismatching then matching oracle | record verdict | mismatch not passed; matching independent reload may pass |

## Assumptions and open questions

- Confirmed: `auto` is the default browser QA selection and starts with Jev while retaining the non-consequential dedicated-fixture boundary.
- Confirmed: LLM + Playwright MCP is first fallback for an unavailable Jev attempt or timeout proven safe to continue.
- Confirmed: a possible product action prevents automatic replay until inspection/reset.
- Existing process-environment credential delivery and allowlisted evidence remain authoritative.
- This source repository can prove routing and safety contracts with offline collaborators; live provider/browser reliability remains consumer-owned.
- Open questions: none.
