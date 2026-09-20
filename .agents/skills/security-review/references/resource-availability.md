# Resource exhaustion and availability

Original review synthesis informed by Cloudflare security-audit; CC BY-SA 4.0
with retained MIT terms. See [provenance](../THIRD_PARTY_NOTICES.md).

Trace lower-trust work into parsing, matching, decompression, queries, allocations,
buffers, files, connections, workers, queues and paid operations. Compare attacker
cost with shared or operator-owned cost, including cardinality and concurrency.

Check cancellation and every error path for detached work or leaked resources.
Inspect retry storms, poison records, head-of-line blocking, quota scope/reset,
priority starvation, fatal errors, deadlocks and unsafe recovery or rollback.

A confirmed availability finding needs a reachable input, missing or bypassable
bound, shared-service or operator-owned victim resource and bounded evidence of the adverse effect. A generic
slow algorithm, self-imposed cost or missing rate limit without abuse impact is a
performance/hardening issue.

Use static reasoning or the smallest sandboxed local check. Never stress a live or
shared process, generate meaningful cost or continue after the minimum effect.
Unobserved upstream limits and autoscaling are neither assumed controls nor assumed
failures; state the exact check the service or deployment owner must confirm.
