# Purpose

This workflow exists to **keep shipping without pretending the product is safer than it is**.

Two failure modes showed up in the same kind of work:

- **Delivery without a floor.** A green linter, a coverage number, a paraphrase of the spec. The
  feature merges. Users hit a journey nobody walked. Security is “we thought about it”.
- **Reliability without an end.** Every nitpick is remediating in the same iteration. Each fix
  changes the diff. The next round finds new nits. Thirty rounds is not thoroughness; it is a loop
  that cannot converge.

The pack is the floor plus the end condition.

## What “balance” means here

**Delivery** is: a change small enough to implement by vertical slice, a gate cheap enough to run
per slice, one fresh independent Verifier over the complete feature, on-demand Deep Review with a
three-stall remediation bound, and merge authority that stays with the human.

**Reliability** is: tests derived from acceptance criteria, security surfaces named and given
`SEC-` cases, one Verifier that is not the author over the complete feature, a persona walk for
anything a user can see when the classifier selects it, and a full gate once when the classifier selects it.

Neither side is optional for features. A feature that skips the final Verifier is not this
workflow; neither is one that re-reviews Trivials until the diff stops moving. Credential-free
declarative agent-tool configuration is a separate maintenance path defined by
[`validation.md`](../../.agents/skills/wtk/references/validation.md).

## What the caps buy

| Cap | Protects |
| --- | --- |
| One fresh full-feature Verifier | Stops self-certified or incomplete proof from reaching delivery |
| Deep-review once, remediation check per batch, Critical/Major only | Stops nitpick churn from being called “quality” |
| Stages do not loop into each other | Review groups bound repeated reading, then a human |
| Proportional gate selection | Stops low-risk maintenance from paying for unrelated product checks |
| Approval is local-only | Stops an agent from pushing, merging, or deploying on a spec yes |

Escalate is a result after the required post-cap remediation and gate. Shipping past a cap with a
reproducible blocker is not.

The review ledger counts failed remediation cumulatively per immutable finding fingerprint while
the live remediation bound counts consecutive stalls; see
[`REVIEW-ROUNDS.md`](guidelines/REVIEW-ROUNDS.md) for the accounting rule.
The installed `wtk/references/review-rounds.md` owns the runtime copy.

## What this pack is not

It is not a product, a stack, or a starter app. The consuming project fills one paragraph in
`AGENTS.md` and owns `make check`. Reliability rules here are process: they do not name a
framework.
