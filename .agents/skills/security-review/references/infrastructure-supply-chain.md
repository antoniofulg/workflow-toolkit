# Dependencies, CI/CD and infrastructure

Modified synthesis of Sentry/OWASP and GitHub Awesome Copilot; CC BY-SA 4.0.
See [provenance](../THIRD_PARTY_NOTICES.md).

Use resolved manifests/lockfiles and current ecosystem advisory sources. Typical
tools include npm audit, pip-audit, osv-scanner, govulncheck, cargo audit,
bundler-audit and composer audit; for Java use an available current Maven/Gradle
advisory scanner. Confirm the installed tool's supported options from its help or
official docs. Do not install tools or execute project lifecycle hooks implicitly.

Prefer an available tool; otherwise query current OSV, GitHub Advisory Database
or maintainer advisories for exact ecosystem/package/version. Record date, source,
affected range and fix version. Do not upload private dependency inventories to
third parties without authorization. A stale package or static watchlist is not
proof. Separate affected-version evidence from reachable application exploitation;
unconfirmed reachability belongs in Needs verification, with a verification step.

Do not resolve/install intentionally vulnerable fixtures. A historical fixture
dependency must be rechecked against current advisories at evaluation time.
Network/tool failure is an audit limitation, never a clean dependency result.

For CI/CD, trace untrusted PR/event fields into commands and privileged jobs.
Inspect token permissions, secret availability, workflow triggers, artifact/cache
trust and action pinning in the actual runner context. An unpinned action alone
is hardening unless a concrete compromise path is established.

Trace dependency sources, generated inputs, caches/workspaces and build outputs to
the exact promoted artifact. Check build/promotion identity separation, signing and
attestation binding, mutable release inputs, update metadata, rollback protection,
and plugin/extension authority. A missing signature is hardening unless an attacker
can substitute an artifact across an evidenced trust boundary.

For IaC/cloud, map public ingress/storage, identity grants, state access and secret
outputs to deployable resources. Wildcards require policy and reachability context.
Separate build/dev risks from runtime risks; never apply plans or run deployment
commands during review.

Inspect object-link scope and the final selected overlay; a safe base manifest does
not constrain an unsafe deployment override. Use [runtime isolation](infrastructure-runtime.md)
for shared workload identity, provider-event, metadata/control-plane, namespace,
admission and container-runtime checks.
