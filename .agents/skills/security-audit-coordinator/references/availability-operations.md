# Availability, release and cloud operations

- Trace attacker-controlled work into parsing, matching, decompression, queries,
  allocations, buffers, files, connections, workers, queues and paid operations.
  Check amplification, concurrency, cancellation cleanup, retry storms, quota scope,
  starvation, fatal errors and recovery. Require shared or operator-owned impact;
  self-imposed cost alone is not a boundary failure.
- For dependencies and generated inputs, verify resolved artifacts, source identity,
  integrity, lifecycle hooks and current advisories. Package age or an unpinned
  reference without a concrete substitution path is not a vulnerability.
- Trace untrusted CI events into privileged commands, caches, artifacts, workspaces,
  secrets and promotion. Bind release authorization, signing, provenance, update
  metadata and rollback policy to the artifact that is actually deployed.
- For cloud/IaC, map workload identity, cross-account trust, ingress, provider events,
  object URLs, metadata access, namespace/label selection, admission controls,
  container privileges, writable mounts and control-plane reachability.
- Compare declared configuration with the final active overlay. Provider policy,
  proxy behavior and live IAM absent from source remain `needs_validation`.

Do not stress live availability, execute deployment plans, publish releases, rotate
credentials or contact control planes during an audit.
