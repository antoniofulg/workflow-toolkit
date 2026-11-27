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

## The recommended change the user approved (as presented, Discover part)

Upstream `tlc-discover` 0.10.0: the design document is now written for a team to align on in one
sitting. `wtk-discover` already has Key decisions and the Status line, but lacks:

- a word budget (about 2,000 words in the part read together, 4,000 in total);
- the "two questions" rule for a fact to earn its place in the document;
- `scripts/validate_design.py` (406 lines, already with five false results fixed);
- a review by a fresh reader before handover, with a stopping rule.

Proposed as its own feature: "validator, word budget and fresh-reader review".

Captures: none.

The Lean 3.2 adoption, the deep-review port and the `ci-speedup` assessment named in the same
request are separate work and are not part of this feature.
