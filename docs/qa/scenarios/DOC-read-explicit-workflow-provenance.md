---
id: DOC-read-explicit-workflow-provenance
area: DOC
title: Read explicit credits and a product-neutral workflow scope
persona: Repository reader
journey: J-review-workflow-release
expected: The README, pack guide, notices, lock, archive, and installed tree identify five bundled reviewed security skills, the original security-pentest skill, their respective provenance, and the product-neutral workflow scope consistently.
entry_points: README.md; docs/toolkit/pack.md; skills-lock.json; .agents/skills/wtk-qa-plan/SKILL.md; .agents/skills/wtk-qa-execute/SKILL.md; NOTICE.md
qa_status: untested
bug_ids: BUG-20260909-interactive-installer-omits-security-command
fix_status: fixed
retest_status: pass
fix_commits: 668ac1c3
evidence: docs/qa/evidence/2026-09-13-workflow-toolkit-release/release-retest-summary.md
last_report: docs/qa/reports/2026-09-13-prompt-review-security-follow-up.md
overlaps:
---

The extra manual follow-up was closed as over-scoped under `26950bf`; targeted documentation and
package checks cover this bounded change. No fresh manual-provenance walk is claimed.

Covers public provenance, authorship, clean-room adaptation language, the bundled-versus-external
security-skill boundary in `SSK-07`, and the reusable package's stack-agnostic scope. The current
pass re-read the credits, both QA skill provenance statements, the three immutable external-skill
entries, and the product-neutral introduction as the QA-contract journey's adjacent canary.

The `phase-skills` feature changes the bundled-capability list a reader evaluates: `docs/toolkit/pack.md` now declares eleven local capabilities including the five phase skills, `README.md` names the router plus its phase skills, and `docs/toolkit/roadmap.md` is new. Reconfirmed on 2026-09-03: the eleven-capability claim matches its table and the installed tree, both QA skills keep their provenance statements, and the three external security skills stay pinned dependencies. Prior evidence remains historical.

Fresh closeout QA at `668ac1c3` passed the previously failing handoff. Four packed successful
installs printed the exact separately authorized command once while all three external skill trees
remained absent. README, pack guide, archive, lock entries, installed files, and QA credits agreed.

Workflow Toolkit Lean changes public identity, capability names, and TLC provenance. The 2026-09-13
canary must reconcile current `wtk-*` ownership, unchanged Ponytail names, the pinned Lean source,
and separate security dependencies. Prior evidence remains historical.

Fresh QA at `e9e1c4ac` reloaded the exact local archive. Its 18 catalogued skills retain current
`wtk-*` and original Ponytail names; the Lean source remains pinned to `0ab82f64`; both QA skills
retain project-owned Antonio Fulgêncio authorship and Pedro Nauck inspiration; three pinned external
security skills remain absent from the archive.

That report and evidence remain historical for the former three-skill set. The current public
provenance promise names four external skills and adds project-owned `prompt-review` to the optional
extras catalog. Reset to `untested` pending an independent README, pack guide, lockfile, archive, and
installed-tree readback.

Workflow Toolkit 1.2.0 replaces the external-skill boundary with five bundled reviewed skills,
including `security-audit-coordinator`. Fresh QA must reconcile README, pack guide, notices, lock,
archive membership, and installed aliases.

Workflow Toolkit 1.4.1 adds original `security-pentest` to the bundled core. Check its distinct
Apache-2.0 provenance alongside the five reviewed skills and confirm the sixth installed alias.
