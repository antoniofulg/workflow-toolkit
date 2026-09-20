# Audit execution safety

Source reading is the default. Run target-controlled builds, tests, parsers,
browsers, emulators or fixtures only when an OS-enforced sandbox provides:

- no external network, with isolated loopback only for a local fixture;
- an empty environment populated from an explicit safe allowlist;
- read-only target and toolchain, with writes confined to per-worker scratch;
- low CPU, memory, process, file-size, disk and wall-clock limits.

Use dummy principals, records and credentials. Do not install dependencies, use
live accounts, probe deployed endpoints, call provider control planes, publish
artifacts, test availability on shared processes or spend paid quota. Stop at the
minimum wrong return value, unauthorized dummy record, sanitizer result or policy
difference needed to establish the boundary failure.

Treat every generated file as target-controlled. Retain only a predeclared,
bounded regular file after the sandbox exits. Reject absolute or traversing paths,
symlinks, hard-linked files, devices, FIFOs, sockets, directories and changing or
oversized files. If the platform cannot enforce safe execution or retention, keep
the source-grounded candidate as `needs_validation` with the exact missing control.

Static analysis can confirm exploitability when it establishes the complete input,
control, sink and adverse outcome. State whether evidence is static, test-based or
observed; never imply that an unperformed reproduction ran.
