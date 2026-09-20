# Native and local platforms

Original review synthesis informed by Cloudflare security-audit; CC BY-SA 4.0
with retained MIT terms. See [provenance](../THIRD_PARTY_NOTICES.md).

Trace attacker-controlled sizes, offsets, counts, units, encodings and objects
through allocation, pointer arithmetic, indexing, copies and parsing. Check overflow,
truncation, signedness, initialization, lifetime, reference counts, type conversions,
shared-state races, TOCTOU, lock order and teardown.

At FFI/ABI boundaries, compare pointer-length, ownership, layout, alignment, enum,
callback, unwind and thread-affinity contracts on both sides. For loaders, plugins,
updates, generated code and JITs, trace artifact identity, search order, writable
locations, binary metadata, permission transitions and unload/reload state.

For kernels, helpers, desktop/mobile and local IPC, verify peer process/package
identity, exported component access, per-operation authorization, message schemas,
reply correlation and user presence. Trace deep links, file-open intents and webview
navigation into native bridges. Review local/temp files, sockets, credential stores,
installers and repair flows for ownership and replacement races.

Distinguish crash, disclosure, integrity loss, privilege change and code execution.
Use sanitizers or bounded fixtures only in an approved sandbox; never strengthen an
observed crash into execution without evidence.
