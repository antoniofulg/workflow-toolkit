# Identity and client boundaries

Original phase-specific synthesis informed by Cloudflare security-audit; Apache-2.0
with retained MIT terms. See [provenance](../THIRD_PARTY_NOTICES.md).

Map credential issue, transport, verification, refresh and revocation across the
components that own them. For JWT, OAuth/OIDC, SAML, passkeys, API keys or mTLS,
identify which component binds issuer/key source, audience/resource, client,
origin/relying party, principal, session, assurance, expiry and one-time state.

Model recovery, linking, MFA changes, impersonation, account switch and logout as
privilege transitions. Include callback/session swaps, stale factors, fallback
routes and earlier sessions that may survive the transition. Treat identity-provider,
proxy and certificate policy absent from source as material assumptions.

For browser/client boundaries, map ambient credentials, origin/frame, service
workers, storage, cross-window messages, WebSockets, navigation/opener state and
third-party scripts to backend effects. CORS, route guards and hidden controls are
not authorization. Identify which layer owns CSRF, safe rendering, URL policy,
message sender validation and private-cache separation.

Tie each abuse path to a protected identity, action or disclosure. A missing flag
or header without an attacker position and adverse outcome is hardening, not a threat
priority by itself.
