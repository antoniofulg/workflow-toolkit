# Distributed systems and data lifecycle

- Compare framing, schema, normalization, defaults and identity between producers,
  gateways, RPC interceptors, brokers and consumers. Bind peer identity to the
  application principal and authorize each stream item, topic and callback.
- Follow duplicate, replayed, delayed, reordered, partially committed and poison
  messages. Check idempotency keys, acknowledgment/commit order, retry/dead-letter
  disclosure and transactional boundaries against a concrete protected invariant.
- Trace one protected record through primary storage, caches, search indexes,
  analytics, logs, object storage, exports, backups, migrations and replicas. A
  tenant field is not isolation; locate the enforced query, key, policy or path.
- Recheck authorization and lifecycle after role change, grant expiry, deletion,
  revocation, restore and rollback. Look for stale sessions, links, jobs, indexes or
  derived artifacts that still expose or act on the record.
- Treat hosted broker ACL, storage policy, replica lag, backup access and retention
  as unknown unless source or confirmed deployment evidence establishes them.

Confirm only an observable unauthorized read, mutation, state transition or
cross-principal effect. Ordinary duplicate work or eventual consistency without a
violated security invariant is not automatically a vulnerability.
