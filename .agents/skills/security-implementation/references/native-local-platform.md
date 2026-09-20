# Native and local platforms

Original phase-specific synthesis informed by Cloudflare security-audit; Apache-2.0
with retained MIT terms. See [provenance](../THIRD_PARTY_NOTICES.md).

Validate sizes, offsets, counts, encodings and units before allocation, pointer
arithmetic, indexing or copying. Use checked conversions and safe ownership APIs.
Initialize complete representations and keep lifetime, reference-count, type and
thread-affinity rules explicit across concurrency and FFI/ABI boundaries.

Define one owner for shared state, avoid check/use races and preserve lock ordering,
cleanup and teardown invariants. At FFI boundaries, validate pointer/length,
alignment, layout, enum, callback and unwind contracts on both sides.

Load executables, libraries, plugins, updates and generated code only from controlled
locations with required artifact identity. Separate writable data from executable
search paths and use supported safe JIT permission transitions where applicable.

For desktop/mobile/local IPC, authenticate the peer process or package, authorize
each operation and validate schemas/reply correlation. Restrict exported components,
deep links, file-open intents and webview bridges. Bind privileged-helper actions to
the requesting user and exact arguments. Create local/temp files safely and resist
symlink, ownership and replacement races.

Use bounded unit tests and sanitizers when available. A crash fix is not evidence of
code execution; test and report the minimum established effect.
