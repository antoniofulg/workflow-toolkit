---
name: wtk-plan-review
description: Run an on-demand peer review of an unapproved Lean plan with reviewers the user picks, then apply only the findings the user selects. Use when asked to peer review the plan or when wtk-lean offers it; not implementation review, an automatic gate, or plan approval.
license: CC-BY-4.0
metadata:
  version: '6.4.0'
---

# Plan review

Find an architecture mistake in `plan.md` while fixing it is still an edit to a paragraph. The review
is opt-in: it runs when the user accepts the `wtk-lean` offer or asks for it, once per request. It
never writes the plan's `## Approval` receipt and never approves; the human approval stays where
`wtk-lean` puts it.

`<skill-dir>` is the directory containing this SKILL.md. Invocation:
`wtk-plan-review [feature] [--reviewers r1,r2] [--round N]`; the round defaults to 1.

## Resolve

Resolve `.specs/features/<feature>/plan.md` from the request or the active feature; ask only when
ambiguous. With no resolvable `plan.md`, report `no plan found` and dispatch nothing.

## Staff

- Reviewers named in the request are dispatched without asking.
- Otherwise list the reviewers the host can dispatch - the roles in the user's routing table
  ([agent selection](../wtk/references/agent-selection.md)) and the host's other agent harnesses -
  and ask the user to pick one or more before any dispatch, as the `plan_review` stage in
  agent selection requires.
- A picked reviewer the host cannot dispatch is named and its dispatch stops; never substitute
  another reviewer. Reviewers that can run proceed.

## Review

1. Dispatch each reviewer as a fresh session that did not author the plan, through the host's
   mechanism, with [the reviewer prompt](references/reviewer-prompt.md) filled in. Each reviewer
   writes only `.wtk-plan-review/<feature>/round<N>-<reviewer>.md`.
2. When every reviewer has returned, run
   `python3 <skill-dir>/scripts/validate_findings.py --round <N> <file>` on each file. A missing or
   invalid file is an incomplete review for that reviewer: report its defects, never `ready`.
3. Report one outcome: `incomplete review` when any file failed (still present the valid files'
   findings), `findings to select` when a valid file holds items, `ready` only when every file is
   valid, reads `readiness: READY` and holds no blocker or nit.
4. Present one merged list, blockers first, each item tagged `<reviewer> B-001` with its title and
   section. Ask the user which items to apply.
5. Edit `plan.md` only for the selected items, then rerun `validate_plan.py` from `wtk-lean`. Do not
   re-decide a `Landing` row the user approved; surface that as a question.
6. Write `.wtk-plan-review/<feature>/round<N>-disposition.md`: a table
   `| Finding | Reviewer | Disposition | Changed |` with one row per finding, disposition `applied`
   or `declined - <reason>`, and `Changed` naming the `plan.md` section edited or `-`.

## Further rounds

Run another round only when the user asks. Send the reviewer the changed plan, the prior findings
and the disposition (the prompt's prior-round slot) and a new `round<N+1>` findings path; unchanged
context is not resent. Preserve earlier round files.

The revised plan returns to the human approval in `wtk-lean`. A real constraint can block
readiness; a stylistic preference cannot.
