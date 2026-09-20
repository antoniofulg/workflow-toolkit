# Default Jev browser QA surface contract

## Config

| Key | Type | Default | Effect |
| --- | --- | --- | --- |
| `[qa].browser_adapter` | enum: `auto`, `jev`, `playwright-mcp`, `orca`, `maestri`, `manual` | `auto` | `auto` walks Jev -> Playwright MCP -> the declared IDE-native Orca or Maestri adapter -> manual; another value selects only that adapter |

Absent `[qa]` and absent `browser_adapter` both resolve to `auto`. Unknown `[qa]` keys and values
outside the enum are invalid. `jev-ultrafast` is not an alias; `jev` maps internally to the
installed Jev Ultrafast implementation.

## Exports

None.

## Removals

The prose-only Jev activation requirement is removed. `docs/qa/README.md` continues to own fixture,
identity, setup, cleanup, and limitations, while `.wtk.toml` owns browser-adapter selection.
