# Platform integrity contracts

Original phase-specific synthesis informed by Cloudflare security-audit; Apache-2.0
with retained MIT terms. See [provenance](../THIRD_PARTY_NOTICES.md).

For CI and release features, define trusted source inputs, dependency/artifact
identity, generated-source provenance, secret availability, promotion authority,
signing, update metadata and rollback behavior. A release requirement names the
artifact and principal being bound, not only a tool or branch name.

For cloud/IaC, define workload identity, allowed accounts/tenants, ingress, network
and control-plane reach, object-link scope, provider-event identity, secret readers,
writable mounts and resource budgets. Treat hosted policy and active overlays as
assumptions until the deployment owner confirms them.

For native/FFI/binary work, specify memory-safe bounds, integer/unit conversions,
ownership/lifetime, concurrency and ABI contracts at untrusted-input boundaries.
Require artifact identity for executables, libraries, plugins, updates and generated
code. Negative tests stop at the minimum crash, sanitizer or wrong-result signal;
they do not assume code execution.

For desktop/mobile/local IPC, define peer process or package identity, exported
component access, message schemas, reply correlation, deep-link/file-open authority,
webview-to-native capability and user-presence requirements. Include safe temporary
paths, local file ownership and privileged-helper operation binding.
