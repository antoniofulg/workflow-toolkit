# Cua + Jev local benchmark — 2026-09-19

## Verdict

Keep deterministic Playwright as the default web QA runner. Bounded Jev adds about 1.3 seconds to
this two-action fixture and remains viable for adaptive choice. Cua + Jev is materially slower and
heavier on this web-only task, so retain it as an optional advanced adapter for pre-action policy,
isolated computer use, and native desktop/Electron journeys rather than a cheaper Playwright
replacement.

## Environment

- Host: Apple silicon macOS 27.0, 11 logical CPUs, 18 GiB RAM
- Cua Driver: pinned stable `0.28.2`; telemetry disabled
- Cua source: `trycua/cua@9bbfa7dd3e27ca7f1861ede70aaca390174493f9`
- Playwright: Python `1.63.0`, Chromium 153.0.8010.12
- TypeSafe SDK: `0.6.0`
- Fixture: Cua's loopback verification form with independent `/state` readback
- Browser state: fresh isolated browser state per run; Cua daemon remained warm across measured repetitions
- Credentials: loaded from `~/.config/workflow-toolkit/qa.env`; no values were printed or stored in evidence

## Arms

| Arm | Decision | Execution | Oracle |
| --- | --- | --- | --- |
| Playwright | fixed deterministic sequence | Playwright | exact fixture `/state` |
| Jev + Playwright | two bounded TypeSafe Choice calls over application-owned candidate IDs | Playwright | exact fixture `/state` |
| Jev + Cua | official Cua bounded candidate loop and TypeSafe Choice | Cua Driver isolated Chromium | exact fixture `/state` |

The five-repetition matrix alternated arm order every other round. Every arm received the same
two-action form goal, unique token, viewport intent, disposable state, and independent oracle.

## Five-run results

| Arm | Verified | Median total | Range | Median decision | Median action | Model requests |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| Playwright | 5/5 | 1.004 s | 0.987–37.831 s | n/a | 0.083 s | 0 |
| Jev + Playwright | 5/5 | 2.335 s | 2.016–2.434 s | 0.954 s | 0.086 s | 2 |
| Jev + Cua | 5/5 | 7.683 s | 7.072–8.697 s | 1.508 s | 3.236 s | 2 |

The first Playwright repetition paid a 37.8-second cold-start outlier; the other four runs were
approximately one second. Cua's credential-free cold connection check took 49.62 seconds. Its warm,
single-live-run path is the value used in the comparison.

On this fixture, Jev + Playwright was 2.32× the deterministic median. Jev + Cua was 3.29× the Jev +
Playwright median and 7.65× the deterministic median. Cua's additional time was mostly browser
action/lifecycle work, not the two Jev decisions.

## Resource sample

One additional warm run per arm sampled the complete benchmark process tree every 100 ms. The Cua
sample also included the long-running Cua Driver daemon and its isolated browser descendants.

| Arm | Peak RSS | Median sampled RSS | Mean CPU | Peak CPU | Peak processes |
| --- | ---: | ---: | ---: | ---: | ---: |
| Playwright | 432.6 MiB | 101.6 MiB | 55.18% | 98.1% | 6 |
| Jev + Playwright | 448.7 MiB | 240.9 MiB | 33.69% | 129.3% | 6 |
| Jev + Cua | 1362.4 MiB | 1269.5 MiB | 77.27% | 280.0% | 13 |

CPU percentages can exceed 100% because macOS reports multi-core utilization. This is one directional
resource sample, not a hardware benchmark.

## Cost and calls

- The comparison matrix made 20 Jev requests: two for each of five Jev + Playwright runs and five
  Jev + Cua runs.
- The deterministic arm made no model request.
- The official Cua recipe discards TypeSafe usage metadata, so exact input tokens and dollar cost are
  unavailable from retained evidence. No cost is estimated from character counts.
- The bounded Cua and Playwright arms used only `TYPESAFE_API_KEY`; the Gateway text helper was not
  needed because action arguments were supplied by application code.

## Additional observations

- Cua's credential-free connection check and paid smoke run both passed independent verification.
- One Cua resource-profile attempt met Chrome's Safe Storage keychain dialog and failed its second
  action after the operator denied access. The next fresh isolated run passed; the benchmark never
  received keychain access or used saved browser credentials.
- Three Jev Ultrafast + Browser Harness attempts failed before any model action with a five-second
  `Page.navigate` IPC timeout on this host. That implementation was excluded from the comparison;
  the bounded Jev + Playwright arm measures Jev without Cua while preserving the same candidate-ID
  safety model.
- Cua Driver's idle daemon used about 27 MiB RSS before the browser journey. The larger resource
  footprint appears when the isolated graphical browser stack is active.

## Decision

1. Keep deterministic Playwright tests unchanged and authoritative.
2. Prefer bounded Jev + Playwright when a web journey needs adaptive semantic choice.
3. Use Cua + Jev when pre-action capability policy, isolated whole-computer state, native desktop,
   Electron, or cross-application work justifies roughly 1.3 GiB sampled RAM and higher latency.
4. Do not make Cua mandatory in Workflow Toolkit or install it in consuming projects automatically.
5. Benchmark Cua next on a desktop or cross-application journey; this simple form exercises its cost
   but little of its unique value.

## Evidence and limitations

Raw evidence is under `docs/qa/evidence/2026-09-19-cua-jev-benchmark/`:

- `benchmark.json` — 15-run matrix and summary
- `resource-profile.json` — complete-process-tree resource samples
- `cua-connection-summary.json` — credential-free setup result
- `cua-live-smoke-summary.json` — official mock + live smoke result

Five repetitions of one local form are directional only. This does not establish production
reliability, performance under concurrency, desktop-task success, or general model accuracy. No
production service, personal browser profile, saved password, email, payment, or user data was used.
