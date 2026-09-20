# Native, binary and local-platform surfaces

- Trace attacker-controlled sizes, offsets, counts, encodings and objects through
  allocation, pointer arithmetic, indexing, copies and parsing. Check overflow,
  truncation, signedness, units, initialization and exact bounds at each handoff.
- Examine lifetime, ownership, reference counts, type/representation conversions,
  concurrency, TOCTOU, lock ordering and teardown. For FFI/ABI boundaries, verify
  pointer-length, layout, alignment, enum, unwind and thread-affinity contracts.
- Map executable, library, plugin and update search order; bind loaded artifacts to
  expected identity, signature and location. Review binary metadata, generated code,
  JIT permission transitions and unload/reload state where present.
- For kernels or privileged helpers, validate repeated user copies, object lifecycle,
  dispatch authorization and least authority. Do not infer code execution from a
  crash or undefined behavior without evidence for that stronger result.
- For desktop/mobile/local IPC, verify peer process or package identity, exported
  component permissions, message schemas, reply correlation and user-presence rules.
  Trace deep links, file-open intents and webview navigation into native bridges.
- Check local files, sockets, temporary paths, credential stores, installers and
  repair flows for ownership, symlink/race, namespace and privileged-deputy issues.

Use sanitizers or bounded local fixtures only inside the approved sandbox. Missing
toolchains, platform entitlements or deployed signing policy are validation blockers.
