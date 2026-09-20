# Protocols and messaging

Original review synthesis informed by Cloudflare security-audit; CC BY-SA 4.0
with retained MIT terms. See [provenance](../THIRD_PARTY_NOTICES.md).

Compare framing, schema, canonicalization, defaults and identity across every
producer, gateway, RPC interceptor, broker and consumer on the path. A finding names
the exact disagreement and security decision it changes; different encodings alone
are not impact.

Trace peer identity into the application principal and authorize each method,
stream item, topic, routing key, subscription, callback and reply. Check envelope
identity against payload-selected tenant/resource fields and inspect batch/stream
paths that bypass unary interceptors.

Examine duplicate, replayed, stale, reordered, poison and partially committed
messages. Verify idempotency-key scope, transaction boundaries, state-commit versus
acknowledgment order, retry/dead-letter disclosure and failure recovery. Ordinary
at-least-once delivery is not a vulnerability without a violated invariant.

Hosted broker ACL, producer identity, delivery guarantees and topology absent from
source are exact validation blockers. Do not send test messages to shared brokers.
