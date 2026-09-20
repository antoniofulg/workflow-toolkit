# Infrastructure and operation

Modified synthesis of OpenAI security-best-practices; Apache-2.0.
See [provenance](../THIRD_PARTY_NOTICES.md).

Keep credentials in the authorized secret-delivery mechanism and restrict their
readers. Exclude them from images, build artifacts, public configuration and logs.
Use least-privilege service identities, controlled writable paths and bounded
CPU, memory, body, connection and storage consumption at relevant boundaries.

Separate runtime from build/dev/test privileges. Avoid exposing deploy credentials
to untrusted build inputs; preserve dependency integrity checks. When changing a
dependency, verify supported APIs and current advisory information instead of
using package age or a historical watchlist as evidence.

Bind generated source, caches, workspaces and build outputs to trusted inputs.
Separate build from promotion authority; sign and attest the artifact that is
actually released, verify update metadata at consumption and preserve a controlled
rollback path. Plugins and extensions receive only their declared capabilities.

For cloud/IaC, scope workload and cross-account identities, ingress, provider events,
metadata access, object links, namespaces/labels, admission policy, control-plane
reach, container capabilities and writable mounts. Verify the final selected overlay;
a safe base template does not constrain an unsafe production override.

Disable development/debug exposure in production, keep diagnostics restricted
and verify trusted hosts and forwarded headers against the real proxy topology.
Do not flag missing TLS/HSTS automatically for local environments or proxy TLS
termination. Set production secure cookies using verified deployment context;
document explicit local HTTP exceptions. Confirm proxy trust and HTTPS coverage
before recommending HSTS because its persistence can cause outages.

Check the resulting configuration and representative valid/denied operations.
State unresolved deployment assumptions; do not deploy, rotate credentials or
apply unrelated hardening merely because implementation work is authorized.
