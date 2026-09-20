# Agent and tool requirements

Original synthesis of official MCP/WebMCP guidance. Source versions and applicable
terms are in [provenance](../THIRD_PARTY_NOTICES.md). Keep requirements separate
from code findings. Apply shared questions plus only the relevant protocol below.

## Shared surface — provider and consumer

Identify the user, agent/tool consumer, provider, executing identity and target
asset. State which task authority was actually delegated: read, modify, disclose
or execute, with object/tenant and destination limits. Authentication alone does
not authorize a tool action. Reuse the existing access/data/input requirements.

Providers define actual side effects and minimum input/output data. Consumers
must not let tool names, descriptions, schemas, annotations or results expand
authority. A read-only hint is not an enforced policy; an injection string is
untrusted data, not proof that an attack succeeds. Require mediation at execution
and disclosure boundaries, not just instructions to the model to behave safely.

For consequential actions, specify any required confirmation bound to the action,
object, amount/destination and current identity; respect an existing explicit
delegation instead of requiring a new prompt for every harmless call. Include
limits, cancellation/retry behavior, audit metadata without secrets, and a valid
authorized control alongside negative tests.

## AI context, retrieval and memory

When the system assembles prompts, retrieves context or uses persistent memory, specify the
trust/provenance of every context source and keep data from becoming higher-priority
instructions. Require tenant/session filters at retrieval and memory write/read,
authorization rechecks after sharing or role changes, and deletion propagation to
summaries, embeddings and derived stores. Define measurable context/output sizes,
model-call counts, delegation depth and spend per task or session. Negative tests cover hostile retrieved text,
cross-session context, poisoned memory, stale authorization and generated output
reaching a renderer or execution sink; suspicious prose alone is not a failed control.

## MCP — when a client/server is present

Identify remote HTTP versus locally launched stdio and the protocol version.
For authorized HTTP, require recipient-bound credential validation, appropriate
scopes and object/tenant policy. Reject tokens intended for a different resource;
use separately authorized upstream credentials, not inbound token passthrough.
MCP 2026-07-28 is stateless: do not require a protocol session ID. For older
negotiated versions or application state handles, bind state to its authorized
principal; state is not a substitute for per-request permission checks.

For consumers, define trusted server/launch provenance, permitted tools, resource
access and disclosure destinations. Include metadata/redirect egress. For a proxy
using a static upstream client ID with dynamically registered MCP clients, require
per-user/per-client consent. For stdio, define process identity,
filesystem/network/environment exposure; do not prescribe HTTP OAuth where there
is no HTTP endpoint. A malicious local process must not receive broad privileges
merely because it is packaged as an MCP server.
Do not assume HTTP authorization is mandatory for intentionally public tools.
Require consumers to avoid automatic network schema-reference fetching; any
explicitly enabled resolution needs a destination and resource-budget policy.

## WebMCP — when page tools are present

Distinguish the exposing page, browser, consuming agent, origin/frame and backend.
Require backend enforcement of the same identity/object/action policy as the UI;
page login or a hidden button is not authority to perform every exposed action.
Specify minimum parameters so the agent cannot silently disclose other-site or
private-session information requested by a malicious tool schema.

State the intended origin exposure and approval policy. Verify actual browser
support before relying on permissions, registrations or document lifecycle.
Treat annotations and prospective confirmation APIs as hints/proposals unless
enforcement is evidenced. The upstream security discussion is non-normative.

## Negative-test seeds

Extend stable ABUSE/SEC IDs for foreign-tenant tool access, wrong token recipient,
session replay, poisoned metadata/results attempting disclosure, stale approval
for changed arguments, unapproved origin invocation and unnecessary personal-data
parameters. Pair each with a protected equivalent and legitimate delegated action.
For EARS, state observable denial without executing the action or releasing data;
do not require a particular SDK or hypothetical browser API.
