# Repository intelligence

Graphify and Graft are standard development tools, not application dependencies. Specs and current
checkout source remain authoritative; generated context is bounded evidence.

## Routing

1. Existing file, symbol, API, caller, and callee pointers: retrieve nothing.
2. Architectural trigger (module or domain boundary, responsibility transfer, shared abstraction,
   central flow, or unresolved architectural risk): query Graphify first.
3. Unknown implementation location or call relationship: query Graft before broad native search.
4. Exact-text question: use exact native search.

Graphify output can feed a bounded Graft query. Deep Review always prepares fresh Graft context when
selected; it prepares one Graphify context only for an explicit architectural question. It does not
run Graphify for local review work.

## Setup and freshness

The installer reports remediation but does not execute package managers:

```bash
npm install --save-dev --save-exact @nanonets/graft@0.10.1
uv tool install graphifyy==0.9.14
python3 .agents/skills/wtk-deep-review/scripts/repository_intelligence.py \
  graphify-setup --root . --backend <backend> --mode deep
```

Semantic Graphify extraction requires an explicit backend. Setup discloses the backend, source root,
indexed file count, and ignored roots before extraction; credentials stay environment-owned.

Queries validate the exact supported version, active checkout, indexed-source manifest, and current
working-tree fingerprint. Tool-native refresh runs before a result is returned. Missing, failed,
stale, partial, insufficient, interrupted, or incompatible state reports one degraded reason and
continues through targeted native inspection. It never silently presents stale context as ready.

Generated graphs, caches, backend metadata, and benchmark scratch records stay checkout-local and
ignored under `graft/`, `graphify-out/`, and `.repository-intelligence/`. They never become runtime
dependencies or committed product artifacts.

## Retention pilot

Record one JSONL event per controlled terminal task in ignored
`.repository-intelligence/benchmark.jsonl`. Each record carries task ID and category, configuration
(`baseline`, `graft`, or `routed`), repository snapshot, prompt and acceptance hashes, provider,
model, effort, input/output/total tokens, repository-intelligence and native-search calls, files read,
wall-clock time, gate result, Verifier result, review findings, rework count, and terminal outcome.

Compare baseline→Graft and Graft→routed runs only when snapshot, prompt, provider, model, effort, and
acceptance contract match. A report requires 10–20 distinct terminal tasks, groups comparisons by
category, and rejects missing controls or independent gate/Verifier evidence. The result is
directional, not statistically conclusive. Removing routing requires a later explicit project
decision covering provisioning, configuration, generated state, and QA promises together.
