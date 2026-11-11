# TLC spec-lean 2.2 adoption — maintainer-approved changes

Date: 2026-11-11. Source: the maintainer's "Aprovado" on the plan for branch
`feat/tlc-lean-2-2-adoption`, including the reversal of the approval decision below and the yes to
update the knowledge records.

Upstream: Tech Leads Club `tlc-spec-lean` 2.2.0 at commit `e74dc8a7e8d59bb36f267afd089580e0858e224a`
(PR #259 and the release post "tlc-spec-driven 4 e tlc-spec-lean 2", which reports Lean verification
falling from about 63 min to 9-25 min once a script ran the proofs and the Verifier only judged).

Decisions relevant to recorded concepts:

1. `## Approval` is gated on presence: `validate_checks.py` fails a feature whose receipt has no
   non-empty `- Decision:` line, so a resumed builder cannot build without a recorded approval. This
   reverses decision 5 of 2026-11-06, which kept the receipt a convention no validator judges. The
   gate checks presence only; the Verifier still judges who approved which revision.
2. `check_proofs.py` runs every proof once at a clean `HEAD` and writes `proofs.md`; the Verifier
   reads it instead of rerunning proofs, and `validate_verification.py` requires it green at `HEAD`.
3. `validate_checks.py --execute` runs the `Build:` line once before the first change.
4. `check_commit.py` prints what each open feature still owes after a passing message.
5. Screens are judged by a fresh sub-agent that never sees the code; `screens.md` is gated under `ui`
   with a bounded second round.
6. The Verifier writes a `Holds` judgment per check; faults run only for `Risk:` checks and `unsure`
   rows, and a survivor outside a `Risk:` check is recorded `accepted` instead of becoming a test.
   Pruning and `wtk-test-review` keep mutation mandatory.
7. The Lean source metadata is re-pinned to the new upstream commit.
