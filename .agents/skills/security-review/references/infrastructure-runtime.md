# Runtime isolation and privileges

Modified synthesis of Sentry/OWASP and GitHub Awesome Copilot; CC BY-SA 4.0.
See [provenance](../THIRD_PARTY_NOTICES.md).

Check the effective process identity, capabilities, writable paths/mounts, host
access and network exposure in the deployed service, VM or container. Build-stage
privileges and declared ports do not establish runtime permissions or exposure.
Inspect deployment overrides and final artifacts, not just source declarations.

For orchestrated or edge runtimes, inspect namespace/label selection, admission
controls, workload identity, metadata and management-plane access, service-mesh or
trusted-proxy identity, provider-event sources and secret renewal fallback. Treat
hosted policy absent from source as Needs verification rather than assuming defaults.

Root without a concrete escalation/impact path is hardening, not an automatic
Critical finding. If a reachable write/execute path combines with privileged
resources, explain the blast radius without duplicate findings. An unprivileged
identity alone does not prove isolation or resource limits.

Trace copied secrets through artifacts/layers and build logs using redacted output.
Use current advisories and resolved artifacts when assessing runtime dependencies;
a tag's age is not a vulnerability. Do not build or execute untrusted deployment
inputs during review.
