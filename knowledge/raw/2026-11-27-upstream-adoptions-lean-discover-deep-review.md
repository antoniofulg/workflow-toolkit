# Upstream adoptions — TLC spec-lean 3.2, TLC discover 0.10, deep-review self-check

Date: 2026-11-27. Source: the maintainer's instruction in conversation, after reading a comparison of
each upstream with the local skill, to apply the recommended changes through merge, proceed with the
remaining updates, adopt the deep-review update "if it gets cheaper, gets better", and say whether
anything in `ci-speedup` can be reused; and the maintainer's yes on 2026-11-28 to record the adoptions
here. The maintainer said the Lean change would be validated further after the merge.

Merged as pull requests #162 (Lean), #163 (Discover), #164 (Deep Review) and #165 (README companion).

## Upstream state compared

- `tlc-spec-lean` 3.2.0 at commit `586a794efa688358e456b942b1849b76672115ae`; the local pin was
  2.2.0 at `e74dc8a`. Upstream 3.x removed `checks.md`, `verify.md`, `check_proofs.py`,
  `validate_checks.py`, `validate_verification.py` and `lessons.py`. Its phases are Plan, Build slice
  by slice, and Review by a fresh sub-agent with one fix pass. Upstream PR #274 gives the reason:
  current models do not need step-by-step build instruction. It publishes no measurement for 3.x.
  The only number on record is the 2.2 one (verification from about 63 min to 9-25 min), which
  justified the proof runner that 3.x removes.
- `tlc-discover` 0.10.0 at commit `d4ab26545b16ed7cfec01bd7fdee0f5305b89d86`. The local skill had no
  recorded pin.
- `deep-review` in `pedronauck/skills` at commit `233da80`: per-job contracts, compact coverage rows,
  draft templates, digests and `prepare_review.py`. No measurement is published.
- `ci-speedup` in `pedronauck/skills`: a skill for slow GitHub Actions workflows.

## Decisions

1. **Lean keeps its proof machinery.** `checks.md`, `proofs.md`, the validators and the structured
   Verifier report stay, against upstream 3.x. The recommendation the maintainer accepted gave three
   reasons: no WTK usage data shows the proofs do not pay for themselves; WTK builders are often
   delegated, cheaper models, where a remembered rule drops most and a script gate is worth most; and
   upstream's own `check_commit.py` keeps a script for the commit format because "a model holds that
   rule at high effort and drops it at lower effort". The maintainer has not yet validated this
   choice beyond the approval.
2. **Lean adopts only what 3.2 adds.** The verbatim `request.md`; answers to the agent's questions
   change the plan and are never the approval; each sentence of the request is read against its
   captures; the first slice is thin and end to end; `check_commit.py` rejects agent trailers and
   lists untracked files; the Verifier reads the request sentence by sentence and changes no data the
   running app holds. Not adopted: upstream's Windows output fix.
3. **Two choices were the coordinator's, not on the approved list.** `validate_checks.py` refuses a
   feature without `request.md` (upstream has no such validator), and trailer rejection is the
   default with `--allow-trailers` to turn it off.
4. **Discover's validator is an unmodified copy.** `validate_design.py` is byte-identical to upstream
   and a test pins its SHA-256. Because the validator accepts only the new section set, the whole
   upstream skill text and document format were merged, beyond the four approved items (validator,
   word budget, two-questions rule, fresh-reader review). A design in the previous section set is
   refused and must be rewritten. `wtk-discover` now records its upstream pin.
5. **Deep Review adopts one piece.** Each reviewer and sweep prompt carries the validation command
   scoped to its own job and status file. The local `run_jobs.py` already had `--only` and
   `--status-file`, so the change is small. The rest of the upstream rework is about 500 lines
   against a fork that had diverged, with no published measurement, and was not ported. The saving of
   the adopted piece is unmeasured: it depends on how often a first artifact is invalid.
6. **`ci-speedup` is listed, not ported.** This repository has no hosted workflows. The README names
   it as an optional companion; which tests can be cheaper stays with `wtk-test-audit`.

## Open

- Both feature plans were written after the maintainer approved the recommendation lists, and were
  not presented before the build. Each Verifier recorded that the approval receipt covers the list,
  not the plan.
