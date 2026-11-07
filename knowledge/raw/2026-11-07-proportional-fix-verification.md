# Proportional fix verification — consuming-project evidence

Recorded on 2026-11-07 from a handoff written in a consuming project. The project's sessions were
reported by that handoff and not independently inspected.

## Reported cost

- About 12 Verifiers ran in one session, each 60k–135k tokens and 2–20 minutes, about 1.1M tokens in total.

## Reported yield

- Verifiers on medium, large or risky changes caught real defects: a draft pull-request gate whose
  green check could read as proof; a weakened deploy workflow shard setting the contract test missed;
  a CLI absent on the CI runner that made every deploy silently run the full gate; formatter failures
  that would fail CI; lease directory permissions.
- Verifiers on small local fixes (a one-line errno guard, a test timeout constant, a formatting line)
  found nothing, and the pull request's hosted CI covered them anyway.
- The handoff estimated that the proposed rule saves about four Verifiers, 300k tokens and 30 minutes
  with no lost findings.

## Proposed rule

1. A Verifier is required for features, refactors, any batch of fixes, and any change touching
   security, authentication/authorization, production/deploy/release paths, CI/CD workflows, data or
   migrations, regardless of size.
2. A small local fix skips it when all hold: one file or a few lines; covered by an existing or new
   focused test, or by the pull request's hosted CI; outside the risk areas. The author runs focused
   tests, lint, typecheck and formatter; hosted CI is the independent check.
3. Fixes answering a Verifier's findings get one fresh Verifier over the whole remediation range, not
   one per commit. A trivial follow-up the Verifier suggested may ride with the next batch or rely on
   CI under rule 2.
4. Kept: a builder never certifies its own non-trivial work; the Verifier gets diff, defect and
   checks, not the builder's conclusions; the stall limit of three attempts.
5. Model hint: a risk Verifier gets the strongest model at high effort; an ordinary one a mid-tier
   model at medium effort.

The maintainer handed this proposal to an agent for implementation and approved recording it here.
