# Frontend and browser

Modified synthesis of OpenAI security-best-practices; Apache-2.0.
See [provenance](../THIRD_PARTY_NOTICES.md).

Render untrusted values as text using context-appropriate encoding. If rich HTML
is required, use a deliberate sanitization contract; do not compile user-authored
templates. Verify the actual renderer's escaping and its bypass APIs from current
documentation. HTML escaping does not validate a URL scheme or JavaScript context.
Constrain dynamic URLs, styles and selector fragments for their intended use.

Treat route guards and hidden controls as presentation only; the server owns
authorization. Keep credentials and private server state out of client bundles
and persistent browser storage. Serialize server-rendered state safely and avoid
shared/service-worker caching of private responses.

For cross-origin messages, verify origin, sender and schema. Understand which
credentials browsers attach automatically when selecting CSRF controls; CORS is
not access control. Constrain third-party script execution through the applicable
deployment policy and verify which headers/controls the hosting layer supplies.

Constrain service-worker registration/scope and partition its caches by identity.
Validate WebSocket origin where browser credentials authenticate the connection.
Avoid merging attacker-controlled keys into security-sensitive objects; use objects
without prototypes or explicit key allowlists when prototype pollution is possible.
Bind navigation, opener and frame-sensitive actions to the expected origin and apply
server-enforced frame policy where UI redress would authorize a consequential act.

Test normal rendering alongside hostile text, URLs and message origins. Record
the renderer/control actually used rather than importing a technology checklist.
