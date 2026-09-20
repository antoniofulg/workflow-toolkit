# Distributed data boundaries

Original phase-specific synthesis informed by Cloudflare security-audit; Apache-2.0
with retained MIT terms. See [provenance](../THIRD_PARTY_NOTICES.md).

Map producer, gateway, serializer, broker, consumer and callback identities. Record
where schema/default normalization, peer-to-principal mapping, topic/resource
authorization and reply correlation occur. Explore duplicate, replayed, stale,
reordered, poison and partially committed messages plus retry/dead-letter paths.

For each protected record, map primary storage and every cache, search/index,
analytics/log, object, export, backup, migration, replica and restore boundary.
Record readers, tenant namespace, invalidation, retention and the component that
propagates ACL changes, deletion, revocation or grant expiry.

Model resource amplification where lower-trust work consumes shared capacity for
parsing, decompression and queries, plus memory, disk, connections, workers, queues or paid APIs.
Include cancellation cleanup, retry storms, quota scope, starvation, fatal errors
and recovery. State the affected principal or operator resource; self-impact alone
does not establish a cross-boundary threat.

Treat hosted broker/storage ACLs, backup access, replica lag and retention as unknown
unless evidenced. Rank conditional paths by the missing control that would change
likelihood or impact.
