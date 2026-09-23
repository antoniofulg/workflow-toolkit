# QA Execute — Adaptive Guidelines recommendation — 2026-09-23

- **Scoped plan:** bounded retest of [`2026-09-23-skills-only-workflow`](2026-09-23-skills-only-workflow.md)
- **Snapshot:** `68e787ce485fd1245cd5d75ae6caa091811143a7`
- **Personas:** Workflow adopter; Repository reader
- **Adapter:** manual documentation readback plus read-only GitHub HTTPS readback
- **Environment:** local source checkout; public GitHub repository and raw README
- **Gate:** `bun test ./tests/skills/distribution.test.js`
- **Evidence:** `docs/qa/evidence/2026-09-23-adaptive-guidelines-recommendation/readback.json` (disposable and ignored)

## Scenario matrix

| Scenario | Verdict | Evidence / limitation |
| --- | --- | --- |
| `ADP-separate-external-security-skills` | pass | README recommends five separately installed companions, names the canonical Adaptive Guidelines source, and gives an accurate use case. Prior install evidence still proves WTK bundles none of them. |
| `DOC-read-explicit-workflow-provenance` | pass | README and pack guide agree that Adaptive Guidelines is an optional companion; the public repository identifies itself as public and its README matches the stated use case. |

## Walk

At `68e787c`, `README.md#recommended-companion-skills-and-tools` links Adaptive Guidelines to
`https://github.com/antoniofulg/adaptive-guidelines` and says it turns recurring agent corrections
into reviewable project guidelines. `docs/toolkit/pack.md#optional-companion-choices` includes it
among five separate choices and retains WTK's native fallback and no-implicit-use boundary.

The public GitHub page identifies `antoniofulg/adaptive-guidelines` as a public repository. Its
README says the skill turns user corrections, stable conventions, and agent mistakes or workflow
inefficiencies into durable lessons and small, reviewable guidelines. This supports the shorter WTK
use case without overstating installation, activation, or execution.

Independent local reload found both current scenario contracts updated to the new recommendation;
their dated prior findings remain labeled as historical.

## Limitations

- The optional skill was not installed or invoked; this walk verifies recommendation provenance and wording only.
- The GitHub readback proves public visibility and current README wording, not package release or runtime behavior.
- Prior full-set install evidence was reused because `68e787c` changes documentation and its regression assertion only; WTK skill trees and installation behavior are unchanged.

## Commands and results

| Command / observation | Result |
| --- | --- |
| GitHub repository and raw README HTTPS readback | Public repository; use case matches the WTK recommendation |
| `bun test tests/skills/distribution.test.js` | No tests selected because Bun treated the argument as a filter; superseded by the corrected path below |
| `bun test ./tests/skills/distribution.test.js` | 6 passed, 0 failed in 319 ms reported test time |
| Targeted scenario contract readback | PASS: README, pack, and 2 current scenario contracts agree |
| `git diff --check` | Exit 0, no output |
