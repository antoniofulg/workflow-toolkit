# Fix verification and execution settings — maintainer decisions

Recorded on 2026-11-04 from a maintainer session and a handoff written from a consuming project.
The consuming project's history was reported by that handoff and not independently inspected.

## Reported failures

- An agent shipped two releases to production on read-only reviews and hosted gates, with no Verifier.
- A board fix passed 18 of 18 focused repeats. Its new test then failed in the wider browser lane.

## Maintainer's rule

> For every fix, we need an agent to verify the fix, like the wtk asks for

## Decisions on its reach

- Documentation and instruction-only corrections are exempt. A mixed change counts as a fix.
- Behaviour-preserving changes: the maintainer asked "The verifier required could be a overkill
  here?". Three options followed: corrections only, all of them, or neither. The agent recommended
  corrections only, because no refactor failure had been observed. The maintainer chose "All of them
  get a Verifier".
- A Minor-only remediation batch in a feature run also gets a Verifier. The maintainer accepted this
  with "Close and record" after the agent reported the gap.

## Decision on model approval

Each delegated stage paused for a human reply on provider, model and effort. On meeting that prompt
for a fix Verifier, the maintainer asked "Can we set a kind of timeout for that question?". The agent
answered that the rule treated a timeout as no acceptance, and proposed a standing approval instead.
The maintainer replied "Let's remove that". The agent read this as removing the approval requirement,
stated that reading and its reach into `workflow_route.py`, and the maintainer did not object.

Released as toolkit 4.2.0.
