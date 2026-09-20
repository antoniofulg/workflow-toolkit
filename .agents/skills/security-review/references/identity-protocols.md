# Identity and HTTP protocols

Original review synthesis informed by Cloudflare security-audit; CC BY-SA 4.0
with retained MIT terms. See [provenance](../THIRD_PARTY_NOTICES.md).

For HTTP framing or cache candidates, identify both components, the same concrete
request/response/key and their divergent interpretations. Confirm cross-request,
cross-user or private-response impact. A custom parser or proxy chain can establish
this in source; an unobserved managed intermediary is Needs verification.

For JWT, OAuth/OIDC, SAML, passkeys, API keys or mTLS, establish the component's
role before judging controls. Trace signature/secret verification and applicable
issuer, audience/resource, client, redirect/session state, nonce, origin/relying
party, principal, credential membership, assurance, expiry and one-time binding.

Review enrollment, step-up, recovery, linking, identity change, impersonation and
logout for alternate routes, callback/session swaps, stale factors and surviving
credentials. For proxy-terminated mTLS, verify only the trusted proxy can supply
the sanitized peer identity and that application mapping is not attacker-chosen.

Missing headers, cookie flags, MFA prompts or rate limits are not findings without
an accepted invalid transition, credential disclosure or affected principal.
Verify current library/browser/IdP behavior when it controls exploitability.
