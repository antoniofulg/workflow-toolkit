# Frontend and browser controls

Modified synthesis of Sentry/OWASP and GitHub Awesome Copilot; CC BY-SA 4.0.
See [provenance](../THIRD_PARTY_NOTICES.md).

Trace attacker content into its actual rendering context. Verify default escaping
and deliberate bypasses for the installed renderer; text interpolation may be
safe while raw HTML, template compilation or executable URL schemes are not.
Confirm sanitization before reporting. Constant markup is not attacker input.

Inspect client bundles, browser storage and caches for sensitive data and confirm
who can access it. Client routing/visibility does not enforce server permission.
For cross-origin messages, trace origin/source validation and the resulting action;
a listener alone is not exploitation. Verify browser credential behavior for CSRF
and credentialed cross-origin requests; CORS is not authorization.

Constrain service-worker registration and scope; partition its caches by identity.
Validate WebSocket origin where browser credentials authenticate the connection.
For attacker-controlled object keys, trace a reachable prototype-pollution gadget.
Bind navigation and opener actions to the expected origin. Check server-enforced
frame policy where UI redress would authorize a consequential act. A missing frame
header or broad listener without an affected boundary remains hardening.

When a library default determines exploitability, consult current official docs
for the installed version and verify the application's configuration. Record
missing evidence separately instead of assuming every framework escapes—or none do.
