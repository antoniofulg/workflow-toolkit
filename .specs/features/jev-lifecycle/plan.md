# Jev lifecycle decision assistance

Status: approved by the user on 2026-09-20 ("Perfect. Plan approved", followed by "Do that changes").

Approval includes the subsequent clarification: prioritize Jev before expensive context loading
or investigation; do not claim token savings without comparing total model usage. Reuse the
existing central credential through the caller environment, not a new credential store.
The user's implementation steering, "The jev must be the default, we must always use jev when
available", requires Jev-first consultation for semantic decisions, even when the agent already
has a preferred answer. Deterministic checks do not require inference.

## Problem

Workflow agents currently make planning, implementation and review judgments without a reusable
typed second opinion. Jev is integrated only as a browser QA driver. The user requests Jev
decision assistance throughout development. No measured decision-quality or time baseline exists.

The intended outcome is a focused recommendation at a real decision point, with uncertainty and
evidence gaps visible to the responsible agent. Deterministic rules remain ordinary checks.

## Flow

Reuse the existing workflow roles, phase entrypoints and core package distribution.

1. `wtk` and phase skills (exists) identify a semantic decision and prepare a minimal evidence summary.
2. Jev adviser (door 1) validates explicit JSON input and renders a request locally by default.
3. With explicit send mode, the adviser calls TypeSafe System One (existing external API) once.
4. Out: typed advisory result, input fingerprint, actual model and token usage; the existing agent
   checks the recommendation against current evidence and retains authority for its next action.

## Impact

| Front | What changes |
| --- | --- |
| Workflow | Default Jev-first semantic decisions in routing, planning, build, verification, review, QA and shipping; shared policy lives in one reference |
| Core package | A Node standard-library helper under the existing core skill; no new runtime dependency or background service |
| QA | Existing Jev Ultrafast browser adapter and AD-038 selection policy retain their current meaning |
| Consumer setup | A process-local `TYPESAFE_API_KEY` enables explicit API calls; no key is written by the installer |
| Existing user edits | Preserve the new TypeSafe skill, its Claude link and skills-lock changes |

## Relations

None - no stored-data shape change. Results are process output, not a second workflow ledger.

## Surface

The public development-tool command is
`node .agents/skills/wtk/scripts/advise.mjs --phase <phase> [--send]`.
It reads one JSON object from stdin. Default mode prints the provider request without making a call.
Phases: `plan`, `build`, `verify`, `review`, `qa`, `ship`.
Exit codes: `0` valid preview/advice, `2` invalid input, `3` unavailable provider or credential.
The exact input and output fields are in [dx.md](dx.md). There is no new HTTP ingress or config key.
HTTP routes: None - this public surface is a local CLI with the exit codes listed above.

## Landing

| One-way door | Literal shape | Alternative rejected |
| --- | --- | --- |
| 1: shared advisory contract | `advise.mjs`, bounded JSON stdin, JSON stdout, explicit `--send`, six phases | Extending the browser adapter couples ordinary decisions to CDP and browser fixtures |
| 2: external inference | HTTPS `POST https://api.typesafe.ai/v1/systemone`, `jev-latest`, environment credential | A provider SDK adds a dependency for one documented HTTP operation |

No automatic action dispatcher is introduced. Host-level per-turn hooks would require a separate
host integration and are justified only if conditional skill invocation proves insufficient.

## Criteria

### S1: Advisory decisions across the lifecycle (P1)

**Acceptance Criteria**

1. WHEN a valid decision is submitted for any supported phase THEN the adviser SHALL build a Choice
   question over 2–8 supplied options plus `insufficient_evidence` and a separate Noul asking whether
   the supplied evidence supports choosing among those options.
2. WHEN the command runs without `--send` THEN it SHALL print the request with status `preview`
   and make zero network calls.
3. WHEN `--send` succeeds THEN the adviser SHALL return status `advice`, selected option,
   probabilities, Choice confidence, evidence-sufficiency Noul, actual model, usage and input hash.
4. IF input violates the schema or 32 KiB bound THEN the adviser SHALL return status `invalid`
   and exit 2 before accessing the provider, including malformed JSON or an unknown phase.
5. IF provider access or validation fails THEN the adviser SHALL return status `unavailable` and
   exit 3 with no recommendation: absent key, 20-second timeout, HTTP failure, invalid response
   or response exceeding 64 KiB.
6. The adviser SHALL make at most one provider request per invocation, with no automatic retries.
7. The adviser SHALL execute zero model-selected actions, modify zero workflow artifacts, and
   produce zero gate verdicts, including when an answer has confidence 1.
8. The adviser SHALL send credentials only in the authorization header to the fixed HTTPS endpoint,
   reject redirects, and omit credentials and raw provider errors from its output.
9. The adviser SHALL read only its stdin and the named API-key environment variable, without
   discovering source files, transcripts, browser state, environment dumps or credential files.
10. WHEN producing a result THEN the adviser SHALL fingerprint the exact normalized phase, state,
    options and questions so a caller can distinguish recommendations from changed inputs.

**Independent test:** exercise all six phases with synthetic stdin and a fake HTTP boundary;
assert typed results, bounded failures and absence of execution or disk writes. A live smoke call
uses only synthetic data when a credential is available; record live testing as unrun otherwise.

### S2: Agents use the adviser at decision points (P1)

**Acceptance Criteria**

11. WHERE TypeSafe is available and a semantic decision is required THEN the guidance SHALL
    require the owning agent to consult Jev before choosing a path, including direct phase
    invocation, with one concrete example for each supported phase; uncertainty is not a prerequisite.
12. The guidance SHALL require minimal non-sensitive summaries and explicit candidate descriptions,
    batch the two independent questions, treat recommendations as advisory, and discard advice
    whose input no longer matches the current decision.
13. IF advice is unavailable or indicates insufficient evidence THEN the guidance SHALL continue
    through the existing agent's reasoning and evidence gathering without marking a gate passed.
14. The core installation SHALL include the helper and shared reference without requiring the
    quality module, browser harness, Jev Ultrafast, or a Vercel key.

**Independent test:** install core into a temporary consumer and run a synthetic dry run; inspect
phase routes and examples for planning ambiguity, build investigation, verification evidence,
review triage, QA priorities and shipping evidence gaps. Contract checks verify links and package
inclusion; semantic instruction review does not claim to prove real agent compliance.

## Traceability

| ID | Slice | Criteria | Status |
| --- | --- | --- | --- |
| JEV-01 | S1 | 1–10 | Complete |
| JEV-02 | S2 | 11–14 | Complete |
| SEC-001 | S1 | 7 | Complete |
| SEC-002 | S1 | 8, 9 | Complete |
| SEC-003 | S1 | 4, 5, 6 | Complete |
| SEC-004 | S2 | 10, 12 | Complete |

## Out of scope

| Excluded | Why |
| --- | --- |
| Autonomous action execution and approval decisions | Initial setup is advisory; existing owners retain authority |
| Hosted service, MCP server and per-turn hooks | Existing command execution and skills provide the required entrypoint |
| Automatic repository/transcript ingestion | Callers can supply the minimum evidence for each decision |
| Replacement browser QA implementation | Existing adapter solves a separate task |
| Learned thresholds and model-quality guarantees | Need representative labeled project decisions before calibration |

## Assumptions

| Assumption | Chosen default | Rationale | Confirmed? |
| --- | --- | --- | --- |
| Rollout | First validate synthetic cases, then assess usefulness on real non-sensitive decisions | No project accuracy baseline exists | n |

**Open questions: none.** Advisory-only authority is approved. A non-empty TypeSafe key was found
in the user's central `~/.config/workflow-toolkit/qa.env`; its validity is untested. Private consumer
content remains outside the disclosed scope; live smoke tests use synthetic data only.

## Observable

| Surface | Decision | Landing |
| --- | --- | --- |
| Command | Input, output, phase, flags and exit codes | AC 1–5; dx.md |
| Command | Empty/malformed/oversize input and provider failure | AC 4–6 |
| API egress | Credentials and destination | AC 8–9 |
| Instructions | Stage examples, uncertainty, stale state and next action | AC 11–13 |
| Installation | Consumer availability | AC 14 |
| Retry and concurrency | Independent calls, no cached authority | AC 6, 7, 10 |
| Data lifecycle | No persistence by the helper | AC 7, 9; provider retention remains an external policy |
| Observability | Actual model, usage, bounded status, no raw input echo in advice | AC 3, 8 |
| UI and tenant authentication | n/a - local command has no screen, server or tenant store | n/a - existing host controls local execution |

## Security Surfaces

| ID | Surface | Control | Requirements |
| --- | --- | --- | --- |
| S1 | Optional development-time helper | No dispatcher or workflow mutation | SEC-001 |
| S2 | JSON input and provider response | Bounded validated schemas | SEC-003 |
| S5 | TypeSafe key | Fixed destination, no redirects or secret output | SEC-002 |
| S6 | Untrusted evidence and suggestions | No execution sink; input fingerprint | SEC-001, SEC-004 |
| S9 | External inference | Explicit send, one bounded request | SEC-002, SEC-003 |

See [threat-model.md](threat-model.md) for provisional assumptions, abuse cases and negative-test seeds.

## Sources

- User request, 2026-09-20: use TypeSafe/Jev for decisions across development, beyond QA.
- [TypeSafe API](https://docs.typesafe.ai/api.md) and [confidence](https://docs.typesafe.ai/confidence.md): typed contract and uncertainty semantics.
- [Skill suggestion cookbook](https://docs.typesafe.ai/cookbooks/skill_suggestion.md): advisory recommendations with a no-match outcome; its benchmark does not establish performance here.
