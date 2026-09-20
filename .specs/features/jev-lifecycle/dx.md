# Jev adviser surface contract

Approved surface; approval tracked in plan.md.

## Command

`node .agents/skills/wtk/scripts/advise.mjs --phase <phase> [--send]`

Required phase is one of `plan`, `build`, `verify`, `review`, `qa`, `ship`.
No other flags except `--help`. Help prints usage and exits 0 without network access.
No send flag means local preview. Send mode needs `TYPESAFE_API_KEY` in process environment.

Stdin is UTF-8 JSON, at most 32 KiB, with exactly these fields:

```json
{
  "decision": "Which investigation would best explain the failing checkout test?",
  "evidence": ["Failure occurs only when two coupon requests overlap."],
  "options": {
    "trace_transaction": "Inspect the transaction and uniqueness behavior.",
    "inspect_rendering": "Inspect browser rendering and event handlers."
  }
}
```

`decision` is a non-empty string, at most 2000 characters. `evidence` contains 1–16 non-empty
strings of at most 2000 characters each. `options` contains 2–8 distinct identifiers matching
`[a-z][a-z0-9_]{0,47}` and non-empty descriptions of at most 1000 characters.
`insufficient_evidence` is reserved. Unknown fields are invalid. Input is parsed once with the
native JSON parser; validation, hashing and provider serialization all use that same parsed object.

The caller supplies reviewed non-sensitive summaries. The helper cannot prove arbitrary prose is
free of private information. Preview deliberately shows the proposed payload, without credentials.

One JSON object goes to stdout; no raw provider body or stack trace goes to stdout/stderr.

| Status | Exit | Output |
| --- | --- | --- |
| `preview` | 0 | `status`, `input_hash`, `request` |
| `advice` | 0 | `status`, `input_hash`, `model`, `answers`, `usage` |
| `invalid` | 2 | `status`, `reason` from fixed local validation messages |
| `unavailable` | 3 | `status`, `reason`: `missing_key`, `timeout`, `http_error`, `invalid_response`, or `network_error` |

`answers` has `next_step` (Choice) and `evidence_sufficient` (Noul), following the official API.
Choice selection and probability keys must match the submitted options plus the reserved option.
All probabilities/confidence/Noul values are finite numbers in [0,1]; Choice probabilities sum
to 1 within 0.001. Usage has non-negative integer `input_tokens` and `output_tokens`.
`model` is a non-empty returned string. Response size is bounded to 64 KiB, deadline to 20 seconds.

`input_hash` is SHA-256 over a deterministic serialization of the normalized request, including
phase context and questions. It identifies evidence; it grants no authority and performs no caching.

## Config

Only `TYPESAFE_API_KEY`; no repository credential persistence, endpoint override, configurable
confidence threshold, polling, automatic retries or config migration.
In send mode, if the normalized request contains the exact key value, the command returns
`invalid`/exit 2 before provider access so the key can travel only in the authorization header.

## Exports and removals

No public library exports. No existing surface removed. The helper ships through the existing
core skill tree. Browser QA settings remain scoped to the browser adapter.
