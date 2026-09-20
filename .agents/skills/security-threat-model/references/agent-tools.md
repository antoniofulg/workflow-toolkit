# Agent and tool trust boundaries

Original synthesis of official MCP/WebMCP guidance. See
[provenance](../THIRD_PARTY_NOTICES.md) for pinned sources and terms. Use shared
modeling plus only the protocol/roles evidenced in the system.

## Shared model

Map user delegation → consumer/planner → tool dispatch → provider execution →
target resource, and the response back into model context. Record identities,
tenant/object policies, actual effects and where authorization/approval occurs.
Treat tool metadata, inputs, retrieved content and outputs as separate untrusted
entry points. Trace disclosure across tools and origins as well as direct writes.

Model a malicious provider/content author and an authenticated malicious caller
separately. State whether they can change metadata, arguments, results, sessions
or the tool implementation, and what they cannot control. Do not assume model
instruction following is a complete security boundary or that suspicious prose
automatically yields exploitation.

Assets include user-task authority, credentials, private data, browser context,
filesystem/network reach and consequential business actions. Identify limits,
retry/idempotency and cancellation behavior that affect the blast radius.

For prompt assembly, retrieval and persistent memory, map context provenance,
priority, tenant/session filters, write authority, derived summaries/embeddings and
deletion paths. Model malicious retrieved content, cross-session context bleed and
memory poisoning through the actual disclosure or action boundary. Record context
and output size, model/tool-call count, delegation depth and operator-spend budgets;
model behavior alone is not a deterministic authorization control.

## MCP branch

For HTTP: map client, authorization server, MCP resource server and any upstream
API separately. Assess wrong-recipient tokens, overbroad scopes, inbound token
passthrough, proxy confused-deputy consent, state-handle reuse/injection and untrusted
discovery/redirect URLs. Token validation, session binding and resource policy
are distinct controls; name each owner and its evidence.
Version 2026-07-28 has no protocol sessions: model per-request authority and any
application handles. Session-specific risks apply only to evidenced older versions.
Also map untrusted schema references if the consumer can fetch network resources;
do not assume automatic remote resolution is required or safe.

For stdio: map launch provenance, executable/dependency trust, inherited identity,
credentials, filesystem/network permissions and client mediation. Absence of HTTP
OAuth is not itself a threat in a pipe-only local design. HTTP loopback endpoints
remain a distinct network boundary requiring their own exposure analysis.

## WebMCP branch

Map page/frame origin → registered callback → authenticated backend, plus the
consumer's cross-site/private context. Compare direct tool and UI code paths;
look for policy checks skipped by the tool. Model misleading intent/read-only
annotations, unneeded personal-data parameters and stale permissions after
identity, document or operation changes.

Origin/permission-policy mechanisms restrict exposure where actually supported;
they do not establish business authorization. Record browser/version and concrete
controls. The source's security/privacy discussion and proposed safeguards are
not proof of deployed confirmation or isolation guarantees.

## Check-in and output

Ask only unresolved questions that change scope/priority: which side is owned,
transport/browser context, privileges, protected data and delegated action policy.
Reuse already-confirmed answers. Keep the final model provisional while required
answers are pending. Map every threat to an asset and boundary, distinguish
implemented controls from recommendations, and justify conditional likelihood
and impact. Do not assume deletion is irreversible or recoverable without evidence
of retention/restore behavior; keep that impact qualifier conditional if unknown.
Separate local launch/CI/dependencies from runtime and test fixtures.
