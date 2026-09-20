# Platform integrity boundaries

Original phase-specific synthesis informed by Cloudflare security-audit; Apache-2.0
with retained MIT terms. See [provenance](../THIRD_PARTY_NOTICES.md).

Separate source, dependency, generated input, CI runner, cache/workspace, build
artifact, signer, promoter, update client and rollback authority. Model untrusted PR
or release inputs reaching privileged identities, secrets or mutable artifacts.

For cloud/IaC, map workload and cross-account identity, ingress, network and
control-plane reach, metadata, provider events, storage/object links, namespace or
label selection, admission policy, container privileges, mounts and active overlays.
Declared templates are evidence only for the deployment path that selects them.

For native/FFI/binary surfaces, identify untrusted sizes/objects, ownership and
concurrency boundaries, ABI/representation assumptions, loaders/plugins, generated
code and privileged interfaces. Keep crash, data disclosure, integrity loss and code
execution as distinct possible outcomes until evidence connects them.

For desktop/mobile/local IPC, map deep links, file-open intents, webview bridges,
exported components, sockets/services, peer identity, helpers, local files,
credential stores, installers and device/account lifecycle. Record which caller can
reach each interface and the OS or application control expected to contain it.
