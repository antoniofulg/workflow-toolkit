# Distributed data contracts

Original phase-specific synthesis informed by Cloudflare security-audit; Apache-2.0
with retained MIT terms. See [provenance](../THIRD_PARTY_NOTICES.md).

For RPC, queues, brokers, webhooks or streams, specify producer/peer identity,
schema/version handling, tenant/topic/resource authorization and callback binding.
Define the observable result for duplicate, replayed, stale, reordered, partially
committed and poison messages. State idempotency scope, retry limits, acknowledgment
semantics and dead-letter visibility instead of assuming exactly-once delivery.

Trace protected data requirements across primary records, caches, search, analytics,
logs, object storage, exports, backups, migrations and replicas. Require the same
owner/tenant policy or a documented narrower policy at each read and write path.
Define invalidation after ACL changes, deletion, revocation and grant expiry.

Specify restore/import authority, reauthorization of restored state and handling of
old records that lack current tenant, lifecycle or policy fields. Retention/privacy
preferences become security requirements only when they protect an evidenced access
or revocation boundary.

Set approved budgets for parsing, decompression, queries, output, connections,
workers, retries, concurrency and paid operations where untrusted work consumes
shared resources. Negative tests vary tenant, order, duplication, cancellation,
over-limit input and dependency failure, plus a successful ordinary control.
