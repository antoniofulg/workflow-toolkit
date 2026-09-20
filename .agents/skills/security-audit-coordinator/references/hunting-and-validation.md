# Hunting and validation

## Worker contract

Give each hunter explicit coverage IDs, starting paths, applicable domain sections,
excluded peer-owned work, safe execution limits and the structured result contract.
Require one disposition per assigned unit and repository-relative reviewed paths.

For every investigated invariant:

1. Name the lower-trust principal and starting capability.
2. Trace accepted input, action or state through parsing and identity.
3. Locate the control that should reject, bind, isolate, limit or revoke it.
4. Follow the exact path through stored copies, retries and the final sink.
5. Seek the strongest preventing control and relevant sibling paths.
6. Stop at a concrete adverse result and propose the smallest effective source fix.

Pattern matches and missing best practices are leads. Same-principal authority,
self-impact, defense-in-depth gaps and effects stronger than observed are not
confirmed vulnerabilities. Put exact external/runtime blockers in
`needs_validation`; discard speculative ideas with no source-grounded boundary.

The parent, not workers, owns shared artifacts and delegation. Workers return data
to the parent and do not spawn other workers. This prevents duplicate fan-out and
keeps budget, ownership and coverage observable.

## Independent candidate verification

Deduplicate by stable root-cause fingerprint. Give each survivor to a fresh verifier
that did not hunt it when the platform supports fresh agents. The verifier tries to
refute the claim by re-reading current source, checking every line and control,
reconstructing prerequisites and repeating only safe decisive checks.

The verifier returns exactly one disposition:

- `confirmed`: complete path, boundary failure and concrete adverse outcome;
- `needs_validation`: real source-grounded hypothesis with an exact unresolved fact;
- `rejected`: source, behavior, a preventing control or absent impact disproves it.

A corrected root cause receives a new fingerprint and another independent check.
If independence is unavailable, perform the same counterevidence pass sequentially
and disclose the limitation. Never relabel an unvalidated candidate as a finding.
