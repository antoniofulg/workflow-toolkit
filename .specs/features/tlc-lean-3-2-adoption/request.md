# Request

Source: maintainer conversation, 2026-11-27. The request is quoted as given (Portuguese, dictated);
the list it approves is the coordinator's recommendation from the same conversation, copied below.

## The user's words

> Olá meu Chacelé, eu gostaria de ver com você se temos atualizações das skills que a gente usou
> como base para o nosso Wispr Flow Toolkit e ver o que a gente pode mudar, o que a gente pode
> melhorar aqui

> Vamos aplicar as mudanças recomendadas, prosseguir para a publicação em merge e depois eu vou
> validar melhor essa mudança da linha
> Então vamos prosseguir com o resto das atualizações e, sobre o deep review também, façam. Se ficar
> mais barato, ficar melhor, podemos, enfim, implementá-los. Sobre o CI speed up do Pedro, eu queria
> saber se tem algo que a gente possa aproveitar também

## The recommended changes the user approved (as presented, Lean part)

Upstream `tlc-spec-lean` went from 2.2.0 to 3.2.0 and removed the proof machinery. The
recommendation was to keep Workflow Toolkit's checks, proofs and Verifier report, and adopt only
what adds to them:

- **`request.md`:** the user's request is saved verbatim before the plan. The Verifier already
  receives "the original request", but from no file, so it is lost in a compaction.
- **Answers are not the approval:** after the answers, the plan is presented again, and they never
  go on the approval line.
- **A capture is a viewport, not the whole request:** each sentence of the request is read against
  the captures (a cut-off column, a state not drawn). Includes asking whether the sample data stays
  in the app.
- **S1 as a tracer bullet:** building layer by layer is forbidden; a slice that turned into a layer
  is cut again by outcome. Today there is only "P1 is a vertical slice".
- **`check_commit.py`:** rejects an agent trailer (`Co-Authored-By`, `Made-with`) and lists
  untracked files.
- **The reviewer does not change app data:** it uses a stub in the browser or a throwaway copy of
  the database.
- **The Verifier reads the request sentence by sentence** against what was built, not only against
  the plan.
- Re-pin `.skill-meta.json` to the new upstream commit.

Captures: none.

The Discover 0.10.0 adoption, the deep-review port and the `ci-speedup` assessment named in the same
request are separate work and are not part of this feature.
