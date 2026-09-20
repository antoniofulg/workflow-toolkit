# Identity and client contracts

Original phase-specific synthesis informed by Cloudflare security-audit; Apache-2.0
with retained MIT terms. See [provenance](../THIRD_PARTY_NOTICES.md).

Specify the complete credential and account lifecycle when the feature changes
login, federation, MFA, passkeys, recovery, linking, sessions, API keys or mTLS.
Bind credentials to the intended issuer, audience/resource, client, origin/relying
party, principal, session, assurance level and expiry where applicable. Require
rotation or invalidation after privilege, password, account or factor changes.

For recovery and linking, name the current principal, proof of the new identity,
required fresh assurance, initiating session and effects on earlier credentials.
Add negative tests for callback/session swaps, replay, stale factors, wrong audience,
cross-account linking and alternate routes that skip step-up.

For cookie-authenticated browser actions, define effective CSRF protection and
credential attachment assumptions. Treat CORS and hidden UI as presentation, not
authorization. Specify origin/source/schema checks for cross-window messages and
server enforcement for any client-visible route guard.

When client features use service workers, persistent storage, shared caches,
cross-window channels or generated markup, define identity partitioning, invalidation,
safe rendering and navigation/URL rules. Keep proxy, identity-provider and browser
behavior as explicit assumptions until current evidence establishes them.
