# Review agent and tool boundaries

Original synthesis of official MCP/WebMCP guidance; this review documentation
remains CC BY-SA 4.0 with underlying source terms retained in
[provenance](../THIRD_PARTY_NOTICES.md). Apply the ordinary evidence/confidence
gate and requested diff/slice scope. Inspect only relevant protocol/role sections.

## Shared evidence gate

Trace attacker control over metadata, arguments, resource content or results to
the actual dispatch, disclosure or state-changing sink. Identify the executing
identity, asset, delegation policy and ineffective control. A malicious sentence
without a demonstrated action path is not a confirmed prompt-injection finding.
Consider both a malicious provider and a caller misusing legitimate tools.

Verify authorization at the resource boundary, not just tool registration/login.
Compare UI and tool paths, scoped queries, dispatch allowlists, destination/data
restrictions and confirmation/capability checks. A tool name, schema or read-only
annotation is not enforcement; metadata mismatch alone needs a harmful path.
Existing explicit delegation may legitimately authorize an action without another
dialog. Report a missing confirmation only against an evidenced policy and bypass.

For prompt assembly, retrieval and persistent memory, trace context provenance,
priority, tenant/session filters, write authority, derived summaries/embeddings and
deletion. Confirm that hostile retrieved content, cross-session context or poisoned
memory reaches an unauthorized disclosure/action or unsafe renderer; suspicious
text alone is not exploitation. Check recursive delegation, model/tool calls,
context/output and operator-spend bounds.

## MCP branch

For HTTP, confirm wrong-resource token acceptance, missing required scopes or
upstream token passthrough in the actual validation/forwarding path. Verify issuer,
recipient, expiry and applicable authorization policy rather than decoding alone.
Trace proxy OAuth consent/state/redirect handling where relevant. Assess state
reuse or queue injection against caller binding and per-request authorization.
MCP 2026-07-28 has no protocol sessions: absence of a session ID is not a finding.
Only apply older session rules to an evidenced negotiated version; check
application handles separately. Missing OAuth on intentionally public HTTP tools
is not automatically a vulnerability either.

Distinguish local stdio from HTTP: lack of OAuth on a pipe-only local process is
not a vulnerability. Assess launch/input provenance, inherited credentials and
OS privileges instead. For exposed HTTP, inspect applicable Origin protections,
binding address and current transport requirements; untrusted discovery/redirect
URLs need an evidenced SSRF path before reporting.

Provider policy and consumer dispatch policy are separate responsibilities.
Check whether tool updates, resource results or cross-tool data can expand the
consumer's authority. Do not execute untrusted servers, replay sessions or test
tokens against live services during review.
Trace remotely resolved schema references as an egress surface if enabled;
refusing automatic network schema resolution is valid counterevidence.

## WebMCP branch

Trace invocation through page callback and authenticated backend to its effect.
Verify origin/frame exposure and actual browser/version support; do not equate
origin permission with user intent or object authorization. Assess over-requested
personal data only when the consumer can supply it to an unauthorized destination.

For sensitive actions, inspect policy-enforced approval, actor/argument binding,
expiry and replay behavior. Compare provider hints with actual side effects but
seek real counterevidence before treating a misleading hint as exploitable.
Do not report absent proposed APIs as vulnerabilities. The official questionnaire
and security discussion include non-normative or unfinished safeguards; record
those as version/context limits, not universal browser guarantees.

In the report, identify role, transport/browser evidence, attacker input, sink,
impact and violated policy. Keep protocol conformance deviations without confirmed
exploitability in Needs verification/hardening. Include safe counterexamples and
source lines; never reproduce credentials, private data or speculative exploits.
