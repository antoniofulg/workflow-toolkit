# Evidence and confidence

Modified synthesis of Sentry/OWASP and GitHub Awesome Copilot; CC BY-SA 4.0.
See [provenance](../THIRD_PARTY_NOTICES.md).

A finding needs a reachable attacker capability, an input or exposed asset,
a traced path, an unsafe sink/security decision, ineffective controls and a
concrete adverse outcome. Static tracing can establish exploitability without
executing an exploit; state whether evidence is static, test-based or observed.
Never imply a reproduction was run when it was only reasoned about.

Research scope may include the repository; reported scope remains the requested
diff/file/slice. In a diff, cite a changed line and explain how the change creates
or worsens the flaw. Historical adjacent flaws belong outside reported findings.

Use **High confidence** only when every required link is supported. Put missing
middleware, uncertain deployment exposure, unknown data sensitivity or incomplete
call chains in **Needs verification**, with the exact check that would resolve it.
Do not turn a hardening deviation into a vulnerability through a severity label.

Verify whether values are user-controlled, server-controlled, or stored from an
earlier untrusted write. A configuration variable is not SSRF evidence unless an
attacker can influence it or a composed suffix/redirect. A database row is not
automatically trusted. Authentication and signed identity do not prove object
authorization. Check ownership, tenant scoping and delegated permissions.

Severity reflects demonstrated impact, reach, prerequisites and blast radius:
Critical for systemic compromise or comparably severe outcomes; High for serious
data/privilege compromise; Medium for bounded harmful outcomes; Low for limited
but actual adverse effects. Do not assign severity by API name or automatically
lower it because login is required. Confidence is independent from severity.

Before reporting, seek counterevidence: middleware order; shared authorization;
query scopes; escaped rendering; parameterized calls; parser settings; network
controls; dead code; fixture-only usage. Recheck every candidate before reporting.
Summaries count only confirmed findings, not threats, hardening or uncertainties.
