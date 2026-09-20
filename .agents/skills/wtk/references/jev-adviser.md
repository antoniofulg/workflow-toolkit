# Jev-first semantic decisions

**Read when:** making or reviewing a lifecycle semantic decision.

Use Jev before higher-level decisions about scope, investigation strategy, evidence adequacy,
priorities or readiness whenever the adviser key is available, even with a preferred answer.
Consult before costly context expansion or investigation. Deterministic checks and exact lookups
stay code-owned. Apply the ownership rule below directly, without an inference call to choose it.

## Choose the consultation owner

Treat a session as gateway-managed only when the user or host confirms that this session's model
requests use `jev-gateway` with routing enabled. Installation or an API key alone is not evidence.
Reuse this session fact; reassess when its launcher, endpoint or routing setting changes.

| Current session | Ordinary tool selection and supported argument routing | Higher-level decisions |
| --- | --- | --- |
| Confirmed gateway routing | Let the gateway handle eligible requests and its own fallback; skip an explicit adviser call for the same tool choice | Consult the explicit adviser |
| Standalone, routing off, unavailable gateway, or unknown routing | Consult the explicit adviser when available, as before | Consult the explicit adviser |

Gateway hint or passthrough results, including low-confidence or Jev-error fallback, do not require
a second consultation for the same tool choice; the agent continues within existing authority.
Gateway tool selection does not settle planning, evidence or approval questions. The gateway may
still inspect the tool request used to invoke the
adviser; this policy adds no transport bypass or automatic request deduplication.

## Call Jev

Use one minimal, non-sensitive summary: the decision, only evidence needed to compare it, and two
to eight candidate options with distinct identifiers and short descriptions. The helper adds an
`insufficient_evidence` option and asks an independent evidence-sufficiency Noul in the same
request. Never send repository files, transcripts or unrelated context; the caller is responsible
for keeping free text non-sensitive.

For decisions assigned to the explicit adviser, the phase skill invokes the helper with the
matching phase and `--send` when the key is available:

```sh
node .agents/skills/wtk/scripts/advise.mjs --phase build --send <<'JSON'
{"decision":"Which investigation best explains concurrent checkout failures?","evidence":["One request passes; two overlapping requests fail."],"options":{"trace_concurrency":"Inspect transaction and uniqueness behavior.","inspect_rendering":"Inspect browser rendering and event handlers."}}
JSON
```

Use `TYPESAFE_API_KEY` from the current caller environment. If it is absent and the trusted
`~/.config/workflow-toolkit/qa.env` is readable, load that existing file quietly into the caller
environment without printing or copying its contents:

```sh
if [ -z "${TYPESAFE_API_KEY:-}" ] && [ -r "$HOME/.config/workflow-toolkit/qa.env" ]; then
  set -a
  . "$HOME/.config/workflow-toolkit/qa.env"
  set +a
fi
```

The helper reads only `TYPESAFE_API_KEY`; it never opens credential files. Do not require per-call
user approval or make manual invocation the normal path. If the key is unavailable or the request
fails, continue with existing reasoning, record the limitation, and avoid repeated same-input
attempts.

## Keep Jev advisory

Treat answers as suggestions to check against current evidence. The caller keeps all decision,
permission and action authority; Jev never executes actions, changes artifacts, approves work or
sets gate verdicts, regardless of confidence. If the decision, phase, evidence or options change,
discard the old advice using its input hash and consult again before choosing.

## Phase examples

| Phase | Decision | Candidate options |
| --- | --- | --- |
| `plan` | Which boundary best keeps the first slice observable? | `helper_preview`: prove the bounded command first; `core_install`: include its consumer installation path in the slice. |
| `build` | Which investigation best explains overlapping checkout failures? | `trace_concurrency`: inspect transactions and uniqueness; `inspect_rendering`: inspect browser output and handlers. |
| `verify` | Which evidence best settles a response-bound check? | `run_boundary_proof`: run the named invalid-response proof; `inspect_mapping`: trace each response field to its assertion. |
| `review` | Which concern deserves first inspection? | `trace_redirect`: follow credential handling across redirects; `trace_retry`: inspect retry and request-count behavior. |
| `qa` | Which user journey leg should be observed first? | `missing_key`: observe fallback when no key is available; `stale_advice`: change evidence and observe re-evaluation. |
| `ship` | Which readiness issue should be resolved first? | `close_check`: prove an open acceptance check; `inspect_blocker`: gather evidence for a reported release blocker. |

These are semantic decisions. Fixed validators, exact command results and other deterministic
checks continue without a Jev call.

## Command contract

Invoke `node .agents/skills/wtk/scripts/advise.mjs --phase <phase> [--send]`; supported phases
are `plan`, `build`, `verify`, `review`, `qa` and `ship`. Default mode previews locally with exit
0; `--send` is required for provider access. `--help` prints usage and exits 0.

Stdin is strict UTF-8 JSON no larger than 32 KiB with exactly `decision`, `evidence` and `options`.
Decision is non-empty and at most 2,000 characters; evidence has 1–16 non-empty strings up to
2,000 characters each; options has 2–8 non-empty descriptions up to 1,000 characters, keyed by
unique IDs matching `[a-z][a-z0-9_]{0,47}`. `insufficient_evidence` is reserved.

Send makes one `POST` to `https://api.typesafe.ai/v1/systemone` with model `jev-latest`; redirects
are refused, the 20-second deadline covers response-body reading, and response size is capped at
64 KiB. The key travels only in the authorization header. The response must contain a Choice
(`next_step`) with selected option, probabilities matching all candidates plus
`insufficient_evidence` and summing to 1 within 0.001, and confidence; a Noul
(`evidence_sufficient.noul`); a model string; and non-negative integer input/output token counts.
Probability values, confidence and Noul values are finite numbers in [0,1].

The command writes one JSON object: `preview` returns `status`, `input_hash` and `request`;
`advice` returns `status`, `input_hash`, actual `model`, typed `answers` and `usage`;
`invalid`/`unavailable` return `status` and a fixed `reason`. Unavailable reasons are `missing_key`,
`timeout`, `http_error`, `invalid_response` and `network_error`; provider bodies and errors are
never echoed. Statuses and exits: `preview` 0, `advice` 0, `invalid` 2, `unavailable` 3. An exact
key value in the normalized request is rejected as `invalid` before sending.

`input_hash` is SHA-256 over normalized phase, state, options and questions. It distinguishes advice
from changed inputs; it does not cache results or grant authority. Never claim token savings from
Jev usage alone: compare Jev plus base-model usage against the baseline for the same task.
