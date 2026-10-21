# Artifact ownership assessment — conversation excerpts

Captured from the workflow assessment conversation on 2026-10-21. Excerpts preserve the
recommendation and the request to record it; they do not document an implemented workflow change.

## Assistant recommendation

> Yes—WTK’s Lean workflow is directly adapted from TLC. I recommend adding ADR and RFC support first, with PRD support available when product decisions need it.

> Reuse the project’s current convention. For a project starting fresh, propose `docs/adr/` for architectural decisions and `docs/rfcs/` for proposals. Keep feature plans linked to those records; preserve ADRs through feature cleanup.

> I found one inconsistency worth fixing: our memory guide allows existing ADR stores, while planning and lifecycle instructions still specifically direct agents to `.specs/STATE.md`.

> PRD support needs particular care: `wtk-discover` already covers situation, problem, success, boundaries, and journey states. When a PRD exists, discovery should consume it and resolve remaining technical questions. It should not repeat the product interview.

> I would make the first WTK improvement a focused integration:
>
> 1. Resolve the conflicting decision-store instructions.
> 2. Document ADR/RFC/PRD triggers in the router’s conditional guidance.
> 3. Initially recommend TLC’s creators as optional companions, following our existing companion model.
> 4. Update planning and verification to follow linked accepted decisions.
> 5. Add a README artifact table covering purpose, trigger, owner, location, and retention.

> The integration must also preserve this repository’s English artifact policy; TLC’s creators otherwise follow the conversation language.

## Recording request and response

Assistant:

> Would you like me to record this assessment in `knowledge/wiki/design/artifact-ownership.md`?

User:

> Sounds perfect.
