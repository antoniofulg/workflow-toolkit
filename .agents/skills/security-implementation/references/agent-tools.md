# Secure agent and tool implementation

Original synthesis of official MCP/WebMCP guidance. See
[provenance](../THIRD_PARTY_NOTICES.md) for pinned sources and terms. Load only
the shared guidance and protocol/roles involved in the authorized change.

## Shared execution contract

Providers validate arguments at execution, derive identity from trusted context,
and enforce action/object/tenant policy at the resource boundary. Reuse the same
enforcement for tools, UI and ordinary APIs. Narrow inputs and outputs; omit
credentials and unrelated personal data. Describe actual side effects accurately.

Consumers bind dispatch and disclosure to the user's delegated task, tool/provider
identity, arguments and destination. Treat tool metadata/results and annotations
as untrusted; enforce policy outside model prose. Do not trust read-only hints to
authorize writes. Preserve existing scoped delegation; require a confirmation or
capability tied to concrete arguments only where the action policy requires it.
Invalidate stale approval when identity, tool, target or material arguments change.

For prompt assembly, retrieval and persistent memory, retain context provenance and
keep lower-trust data from becoming policy. Enforce tenant/session filters on reads
and writes, recheck authorization for derived summaries/embeddings and propagate
deletion or revocation. Bound context/output, recursive delegation, model calls and
paid work. Render generated output as untrusted data unless an explicit execution
boundary validates and authorizes it.

Bound work/output, retries and concurrent calls. For consequential effects, use
idempotency and recheck current policy before committing. Cancellation is not a
rollback guarantee. Log action/decision metadata with redaction, never raw secrets.

## MCP HTTP and local stdio

For HTTP authorization, use current official guidance for the actual negotiated
version and SDK: validate credentials for this resource and appropriate scopes,
then enforce object/tenant policy. Never forward an inbound client token to an
upstream API; obtain separate authorized credentials. Authorize each request.
Version 2026-07-28 is stateless; do not invent protocol sessions. Bind application
handles, or sessions on older negotiated versions, to the validated caller.
When a proxy uses a static upstream client ID with dynamically registered MCP
clients, obtain per-user/per-client consent before upstream authorization.
Validate redirects and state according to the actual OAuth flow; do not treat
ambient upstream sessions as client consent in that proxy scenario.

On network transports, implement applicable Origin/exposure protections and
constrain discovery/redirect destinations against SSRF. For locally launched
stdio, instead scope executable provenance, environment credentials, filesystem
and network authority. Do not add HTTP OAuth to a pipe-only server by analogy.

Consumers must use authorized servers/tools and minimal disclosure; re-evaluate
material tool/permission changes instead of silently reusing prior approval.
Keep tool visibility consistent with current request authority. Avoid automatic
network schema-reference resolution; constrain destinations and work if enabled.
HTTP OAuth is an optional protocol feature, not mandatory for all public tools.
Do not launch untrusted servers or probe credentials merely to test the change.

## WebMCP browser surface

Keep authorization and required transaction confirmation in an enforceable path
shared with the backend. A logged-in page, description, schema or annotation
does not grant task consent. Avoid accepting identity/tenant/approval booleans
from caller arguments as authority. Bind any approval proof to the current actor
and exact operation, with expiry/replay handling appropriate to the action.

Limit exposed tools/origins and minimize requested personal data. Preserve
separation of cross-site and private-browsing context in the consumer. Check
current official specification and actual browser support before choosing API
names, permission controls or lifecycle behavior. Do not invent a universal
browser confirmation gate; the source's security mitigations are non-normative.

Test negative and valid delegated calls, alternate UI/tool paths, changed approval
arguments and failed/replayed operations. Report implementation/hardening outcomes,
not a vulnerability audit. If SDK/browser guarantees are unknown, state the gap
and propose an explicit application control using available APIs.
