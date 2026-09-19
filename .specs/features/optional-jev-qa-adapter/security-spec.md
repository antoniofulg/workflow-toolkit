# Optional Jev QA Adapter Security Specification

## Security surfaces

- Local QA command input crosses into a Python adapter and an external browser process.
- Provider keys cross from the runner environment to TypeSafe and Vercel; browser-session credentials remain inside a dedicated QA profile.
- Natural-language goals, page content, tool metadata, and provider output are untrusted.
- Evidence writes cross into a checkout-owned disposable filesystem root.
- TypeSafe, Vercel AI Gateway, Jev Ultrafast, and Browser Harness are external integrations unavailable in this source checkout.

## Assets and actors

- **Assets:** TypeSafe and Vercel keys; QA browser cookies/session; user task authority; target application test data; evidence integrity; filesystem and network reach.
- **Legitimate actor:** assigned QA Verifier, limited to the declared charter, target, identity, and evidence root.
- **Adversarial actors:** malicious page/content author, compromised or misleading provider/tool output, local caller supplying an invalid destination, and compromised external dependency.
- **Non-capability assumption:** page content and model output cannot authorize a broader action, origin, identity, or evidence destination.

## Trust boundaries

| Origin | Destination | Trust change | Policy |
| --- | --- | --- | --- |
| QA Verifier | adapter CLI | untrusted arguments enter executable code | closed input validation before provider/browser work |
| runner environment | adapter/provider clients | secrets enter child process and network requests | minimum environment, never output values |
| target page | Jev/browser policy | untrusted content becomes model state | supplied goal and declared browser scope remain authoritative |
| adapter | evidence filesystem | external results become local artifacts | containment and symlink checks before first write |
| Jev driver | WTK verdict | probabilistic driver status could be mistaken for proof | independent readback after reload owns `pass` |

## Abuse cases

| ID | Actor and capability | Asset | Path | Adverse outcome | Linked requirements |
| --- | --- | --- | --- | --- | --- |
| ABUSE-001 | Page/provider can influence returned text and diagnostics | provider keys and browser credentials | injected content induces disclosure into trace/output | reusable secret or unrelated session data leaves the process | SEC-001, SEC-002 |
| ABUSE-002 | Caller can request a consequential journey or personal/default browser | user task authority and unrelated browser sessions | unsafe charter/browser reaches Jev without a pre-action mediation hook | unauthorized action or cross-origin disclosure | SEC-002, SEC-006 |
| ABUSE-003 | Local caller controls evidence path | checkout filesystem integrity | traversal or symlink targets a foreign path | overwrite or disclose files outside disposable evidence | SEC-003 |
| ABUSE-004 | Provider/browser can fail after an interaction begins | target application test data | wrapper restarts or retries `Agent.run()` | duplicate or unintended mutation | SEC-007 |
| ABUSE-005 | Missing dependency/key or provider failure is ambiguous | QA verdict integrity | unavailable run is treated as completed/pass | false green QA status | SEC-004, SEC-005 |
| ABUSE-006 | Jev controls its own success signal | QA verdict integrity | `DONE` becomes `pass` without another observation | failed journey recorded as passing | SEC-005 |

## Security requirements

| ID | Abuse cases | Observable rule |
| --- | --- | --- |
| SEC-001 | ABUSE-001 | The adapter SHALL omit credential values, cookies, authorization data, and reusable tokens from stdout, stderr, evidence, reports, and exceptions. |
| SEC-002 | ABUSE-001, ABUSE-002 | WHERE Jev is selected, the adapter SHALL require an explicit dedicated CDP endpoint for headless or headed QA and SHALL reject personal/default-browser attachment. |
| SEC-003 | ABUSE-003 | IF the evidence destination escapes the checkout-owned disposable root or crosses a symlink, THEN the adapter SHALL reject it before the first write. |
| SEC-004 | ABUSE-005 | IF a prerequisite is missing, THEN the adapter SHALL return `unavailable` with prerequisite names only and SHALL allow selection of the existing adapter. |
| SEC-005 | ABUSE-005, ABUSE-006 | WHEN an adapter attempt ends, the QA report SHALL record the actual adapter and independent verification result; only the independent oracle may produce `pass`. |
| SEC-006 | ABUSE-002 | IF the charter is consequential or lacks the dedicated fixture/browser declaration, THEN the adapter SHALL reject Jev before constructing `Agent` and SHALL select the fallback chain. |
| SEC-007 | ABUSE-004 | IF failure occurs after browser execution begins, THEN the adapter SHALL preserve bounded evidence and SHALL NOT call, restart, or retry `Agent.run()` again in that invocation. |

## Negative-test seeds

| IDs | Setup | Action | Expected |
| --- | --- | --- | --- |
| SEC-001 / ABUSE-001 | sentinel-format fake keys and provider/browser exceptions | exercise every terminal status | no sentinel or derived authorization value in any output/evidence |
| SEC-002 / ABUSE-002 | no CDP endpoint, personal/default browser, then dedicated headless and headed CDP endpoints | request each mode | unsafe modes `unavailable`; both dedicated modes may proceed, with headless the default |
| SEC-003 / ABUSE-003 | checkout evidence root plus traversal and symlink destinations | request each invalid path and one contained path | invalid paths write nothing; contained control writes only inside root |
| SEC-004 / ABUSE-005 | remove each prerequisite independently | run preflight | `unavailable` names the missing prerequisite; existing adapter remains selectable |
| SEC-005 / ABUSE-006 | stub Jev `DONE` and an oracle mismatch, then an oracle match | close each QA attempt | mismatch cannot pass; authorized matching control can pass |
| SEC-006 / ABUSE-002 | consequential charter and non-consequential fixture charter | invoke adapter | consequential path constructs no `Agent` and selects Playwright-first fallback; fixture control may proceed |
| SEC-007 / ABUSE-004 | fail after `Agent.run()` starts | observe adapter calls | one `Agent.run()` call, no restart/retry, failed evidence retained |

## Assumptions and open questions

- Dedicated QA browser/profile enforcement is human-confirmed. Jev defaults to a dedicated headless Chromium CDP endpoint; an explicit headed request uses a dedicated headed CDP endpoint.
- Playwright MCP is the first LLM-driven fallback; a declared Orca, Maestri, or manual adapter follows when Playwright is unavailable. None is presented as a native Jev transport.
- The upstream package/module interface and Browser Harness availability must be re-verified at Build; absence is `unavailable`, not a reason to install tooling.
- This repository can prove adapter contracts only with offline collaborators; a consuming web project owns live browser evidence.
- No production targets, accounts, or credentials are in scope.
