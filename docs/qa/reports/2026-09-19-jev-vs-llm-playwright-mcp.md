# Jev versus LLM over Playwright MCP — 2026-09-19

## Verdict

Jev is a strong replacement for the general LLM decision layer in bounded browser QA. With the
browser, MCP server, tool-call count, fixture, and oracle held constant, Jev was 7.32× faster and
used 151.8× fewer aggregate input tokens. Browser-process memory was effectively unchanged, so the
gain is model context, latency, and API-equivalent cost—not local browser RAM.

Deterministic Playwright tests are outside this comparison and remain unchanged.

## Controlled setup

- Browser surface: `@playwright/mcp` `0.0.82`
- Browser mode: headless, isolated Chromium 154.0.8037.0
- Journey: navigate to a loopback form, fill one exact token, submit once, observe result
- Browser calls: exactly five in both arms — navigate, snapshot, fill, click, final snapshot
- Oracle: independent HTTP readback of exact submitted fixture state
- Repetitions: five per arm, alternating order each round
- LLM arm: ephemeral Codex CLI `gpt-5.6-luna`, project/user config and rules ignored
- Jev arm: TypeSafe SDK `0.6.0`, two bounded Choice questions over application-owned action IDs
- Cua: excluded

## Results

| Arm | Verified | Median total | Median input | Cached input | Median output | Model decisions | MCP calls | Median child peak RSS |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| LLM + Playwright MCP | 5/5 | 21.807 s | 142,556 | 126,208 | 462 | aggregate agent turn | 5 | 214.4 MiB |
| Jev + Playwright MCP | 5/5 | 2.980 s | 939 | n/a | 66 | 2 | 5 | 217.8 MiB |

The LLM arm ranged from 20.55 to 41.08 seconds. The Jev arm ranged from 2.86 to 3.15 seconds.
Both completed the same browser sequence and passed the same independent oracle in every run.

## Context and cost interpretation

- Aggregate input-token reduction: 151.8×.
- Even after subtracting the LLM's reported cached-input subset, its remaining 16,348 median input
  tokens were 17.4× Jev's complete 939-token input.
- Output-token reduction: 7×.
- Current TypeSafe list price (`$0.042` per million input tokens, output free) makes the measured Jev
  decision cost approximately `$0.00003944` per journey.
- The LLM ran through a subscription, so actual billed cost is not available. Applying the current
  Vercel AI Gateway standard rates for `openai/gpt-5.6-luna` only as an API-equivalent estimate gives
  approximately `$0.00634816` per journey, about 161× the measured Jev cost. This is not an invoice.

Cached input remains context the general agent must carry and process even when billed at a lower
rate. Jev receives only the current state and bounded decisions.

## What this proves

- Jev can replace a general coding LLM for narrow browser-action selection while preserving the same
  Playwright MCP executor and deterministic oracle.
- The performance gain comes from shrinking the decision context and answer space, not replacing the
  browser or weakening verification.
- The general LLM used five MCP calls and broad agent context. Jev used the same five MCP calls but
  only two small typed decision requests.

## What this does not prove

- Five runs of one two-action fixture do not establish general browser reliability.
- The LLM result is specific to Codex `gpt-5.6-luna` and its current agent prompt/tool context.
- The Jev action set was application-owned and deliberately bounded; open-ended browser exploration
  may require more decisions or escalation.
- No consequential action, production service, personal profile, payment, email, or user data was
  involved.

## Decision

1. Keep Playwright MCP as the browser executor.
2. Use Jev as the optional decision layer for declared, bounded, non-consequential QA journeys.
3. Keep the independent oracle and deterministic test suites unchanged.
4. Fall back to the general LLM when the action set cannot be bounded or Jev abstains/is unavailable.

## Evidence

Raw results: `docs/qa/evidence/2026-09-19-jev-vs-llm-playwright-mcp/benchmark.json`.

Official references:

- Playwright MCP: <https://github.com/microsoft/playwright-mcp>
- TypeSafe Jev: <https://docs.typesafe.ai/introduction>
