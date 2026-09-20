# Data isolation and lifecycle

Original review synthesis informed by Cloudflare security-audit; CC BY-SA 4.0
with retained MIT terms. See [provenance](../THIRD_PARTY_NOTICES.md).

Follow a protected record through primary storage, caches, search/indexes, analytics,
logs, object storage, previews, exports, backups, migrations, replicas and restore.
At each reader or writer, find the enforced query, key, namespace, path or policy;
an owner/tenant field on the record is not isolation by itself.

Compare direct, nested, bulk, background, admin and legacy paths. Check whether
derived keys omit tenant/environment, signed links outlive ACL changes, or indexes
and caches return records after role change, deletion, revocation or grant expiry.

Authorize export artifact creation and download separately. Treat imports, restores
and migrations as untrusted state transitions: validate archive content, target
tenant, identifiers, ACL defaults, partial rollout, rollback and resumed work.
Reapply current policy when restoring historical identities or permissions.

External object-store policy, backup access, retention and replica behavior absent
from source remain Needs verification. Privacy preference alone is hardening unless
an evidenced access, deletion or revocation contract is crossed.
