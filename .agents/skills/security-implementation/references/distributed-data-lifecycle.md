# Distributed data lifecycle

Original phase-specific synthesis informed by Cloudflare security-audit; Apache-2.0
with retained MIT terms. See [provenance](../THIRD_PARTY_NOTICES.md).

Authenticate the producer or peer, validate the envelope and payload independently,
and bind the message, topic, tenant, resource and callback to application policy.
Apply authorization per item in streams and batches. Normalize schema versions and
defaults once before security decisions; reject ambiguous or unsupported variants.

Make duplicate and retry behavior explicit. Scope idempotency keys to the protected
principal/action, persist the result atomically and order state commit with broker
acknowledgment. Durably commit first, acknowledge second, and return the stored
idempotent result when a lost acknowledgment causes redelivery. Bound retries,
dead-letter visibility and poison-message effects.

Carry owner/tenant and lifecycle policy through caches, search, analytics, object
storage, exports, backups and replicas. Namespace derived keys, recheck authorization
at retrieval and invalidate copies after ACL change, deletion, revocation or expiry.
Authorize import/restore outcomes and reapply current policy to historical records.

Bound parsing, decompression, queries, buffering, output, workers, queue depth,
connections, concurrency and paid operations. Stop detached work after cancellation,
release resources on every exit and prevent retries from multiplying cost.
