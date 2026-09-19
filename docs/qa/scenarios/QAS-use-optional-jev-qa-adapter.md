---
id: QAS-use-optional-jev-qa-adapter
area: QAS
title: Use the optional Jev QA adapter safely
persona: Workflow operator
journey: J-use-optional-jev-qa-adapter
expected: An exact local package installs the optional Jev helper and readable safety policy without browser dependencies, and its installed copy fails closed with structured fallback metadata when prerequisites or policy are unmet.
entry_points: workflow-toolkit package; wtk install; .agents/skills/wtk-qa-execute/SKILL.md; .agents/skills/wtk-qa-execute/jev_adapter.py
qa_status: pass
bug_ids:
fix_status:
retest_status:
fix_commits:
evidence: docs/qa/evidence/2026-09-19-optional-jev-qa-adapter/package-summary.json; docs/qa/evidence/2026-09-19-optional-jev-qa-adapter/installer-transcript.txt; docs/qa/evidence/2026-09-19-optional-jev-qa-adapter/installed-readback.json; docs/qa/evidence/2026-09-19-optional-jev-qa-adapter/preflight-results.json; docs/qa/evidence/2026-09-19-optional-jev-qa-adapter/selected-gates.txt
last_report: docs/qa/reports/2026-09-19-optional-jev-qa-adapter.md
overlaps: ADP-install-versioned-workflow-package; ADP-layered-workflow-adoption
---

This promise owns the packaged optional-adapter boundary. QA reads the exact local archive and an
independently installed quality module, then invokes only preflight paths that cannot reach a live
browser or provider. It confirms helper membership, policy text, no dependency installation,
structured `unavailable` and `invalid` results, Playwright-first fallback metadata, and the external
oracle boundary.

Ready Jev execution, post-start provider/browser failure, and live fallback adapters are not
reachable in this source repository. Their offline contract proofs remain Technical Verification
evidence and cannot produce this scenario's verdict. A `pass` requires the packed install,
preflight results, independent filesystem reload, and clean residue planned by the owning charter.

QA Execute passed this bounded promise at `680076a0` on 2026-09-19. The exact packed and installed
bytes matched, missing-authority and invalid-destination preflights failed closed, no dependency or
external adapter ran, and a fresh post-probe readback preserved the policy and oracle boundary.
