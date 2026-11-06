# Branch Naming

**Read when:** creating a branch or a worktree.

The branch shape and types below are defaults. A project that defines its own branch naming or
commit types replaces them.

**Why this exists:** A branch named for the implementation (`add-users-table`) or for a checkout
slot hides what the user gets. Work on `main`, leftover merged branches, and two checkouts sharing
a runtime are how a gate silently verifies the wrong tree.

## Shape

```
<type>/<slug>
```

`<type>` is the Conventional Commits type the branch's work will mostly carry. `<slug>` is 2–5
kebab-case words naming the behaviour, not the implementation.

```
feat/account-onboarding
fix/duplicate-submission
docs/guidelines-rebuild
refactor/repository-boundaries
```

## Types

| Type | For |
| --- | --- |
| `feat` | New user-visible behaviour |
| `fix` | A defect in behaviour that already shipped |
| `refactor` | Structure changes, no behaviour change |
| `perf` | Behaviour unchanged, measurably faster |
| `docs` | Documentation and guidelines only |
| `test` | Test-only work — rare, since tests ship with their behaviour |
| `build` | Tooling and dependencies |
| `ci` | CI configuration |

`chore` is not a type; name the real one. `check_commit.py` accepts exactly this set.

## Rules

1. **The slug names the behaviour.** `feat/account-onboarding`, not `feat/add-users-table`. A reader
   should know what the user gets, not what the diff touches.
2. **One branch, one feature.** The branch matches the `.specs/features/<slug>/` directory name when
   the feature has one. Same slug on both sides — no translation step.
3. **Never work on `main`.** Never push to it, never force-push anywhere, never merge without an
   explicit instruction.
4. **Worktree branches are named for their work, not their checkout.** The branch name says what is
   being built.
5. **No personal namespace.** New branches do not use `username/` prefixes.
6. **Delete after merge.** After a PR merges, confirm the merge and a clean tracked worktree, then
   remove every worktree the agent created for that feature or task. Inspect ignored residue before
   using force removal. Keep the primary, active, and unmerged worktrees untouched.

## Backups

A branch created only to preserve state before a risky rebase is prefixed `backup/` and names what it
protects plus why:

```
backup/account-onboarding-pre-rebase
```

These are disposable. Delete them once the operation they protected has succeeded and been verified —
an accumulated wall of `backup/` branches hides the one that still matters.

## Isolated checkouts

Apply [agent selection](agent-selection.md) before creating a separate checkout for delegated work;
a fresh session or handoff stays in the current checkout unless a concrete exception is approved.

Never share a branch between two checkouts. Before runtime setup or worktree removal, apply
[runtime lifecycle](runtime-lifecycle.md): preserve checkout identity, resolve owned resources and
carry their reuse/cleanup evidence through handoffs.
