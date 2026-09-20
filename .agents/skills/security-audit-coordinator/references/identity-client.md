# Identity, HTTP and client attack surfaces

Select only classes supported by source-visible boundaries.

- Compare request framing, host/forwarded values, cache keys and private-response
  policy across every component that interprets them. A finding needs two concrete
  interpretations and cross-request, cross-user or private-data impact.
- Trace credential issue, storage, transmission, verification, refresh and
  revocation. Verify signature/secret plus issuer, audience, origin, relying party,
  client, session, principal, resource, assurance, expiry and one-time state as
  applicable to JWT, OAuth/OIDC, SAML, passkeys, API keys or mTLS.
- Compare login, MFA, recovery, linking, account switch and logout transitions.
  Bind step-up and callbacks to the initiating identity, session and exact action.
- For browser sessions, establish ambient credentials before claiming CSRF. Compare
  UI and backend authorization; hidden controls and CORS are not access controls.
- Trace untrusted data through DOM sinks, URL schemes, `postMessage`, WebSockets,
  service workers, storage, opener/navigation state and prototype-pollution gadgets.
  Verify actual browser/framework defaults before reporting.

Missing headers, flags or prompts are hardening unless they enable a concrete
boundary failure. Unobserved proxy, identity-provider or browser policy remains an
exact validation blocker, not assumed protection or vulnerability.
