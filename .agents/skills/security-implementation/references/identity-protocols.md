# Identity protocols

Original phase-specific synthesis informed by Cloudflare security-audit; Apache-2.0
with retained MIT terms. See [provenance](../THIRD_PARTY_NOTICES.md).

Use supported verification APIs and server-configured trust policy for JWT, OAuth/OIDC, SAML,
passkeys, API keys and mTLS. Verify signature or secret plus the bindings the role
requires: issuer, audience/resource, client, redirect/session state, nonce,
origin/relying party, principal, credential membership, assurance and expiry.

Bind MFA/step-up completion to the current identity, session and exact protected
operation. Enrollment, replacement, disablement, recovery, linking and identity
changes require the intended fresh assurance and invalidate superseded credentials
or sessions according to product policy. Keep support/admin recovery within an
explicit, auditable authority boundary.

For API keys, derive tenant, environment and scope from the server record rather
than request fields; store only supported verifiers and make revocation effective
through caches. For proxy-terminated mTLS, accept peer identity only from the
authenticated proxy after removing client-supplied copies and map certificate
identity through an allowlisted policy.

Test wrong issuer/audience/origin, callback swap, replay, stale factor, alternate
route, cross-account linking, revoked key and certificate fallback. Verify current
framework/IdP behavior instead of inventing parameters or defaults.
