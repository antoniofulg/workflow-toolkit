# BUG-20260923-source-retains-removed-wtk-config-link

- **Status:** open
- **Severity:** minor
- **Scenarios:** `CFG-keep-local-artifacts-out-of-git`; `REL-report-current-workflow-release`
- **Expected:** The source checkout and current 12-skill inventory contain no `wtk-config` skill, alias, configuration payload, or generated residue.
- **Observed:** The tracked symlink `.claude/skills/wtk-config` remains and points to the removed path `../../.agents/skills/wtk-config`; the target does not exist.
- **Snapshot:** `e6002ca18d4fe07f842acff8c03efeca16748a72`
- **Adapter:** Manual source inventory and independent filesystem readback
- **Exact path:** Read the tracked `.claude/skills/` inventory, resolve `.claude/skills/wtk-config`, and compare it with the exact 12 directories under `.agents/skills/` and the installed consumer inventory.
- **Evidence:** `docs/qa/evidence/2026-09-23-native-agent-settings/release-readback.json`

## Impact

The source checkout advertises a Claude skill alias whose canonical skill was removed. Source users
or tooling that follows tracked Claude aliases can discover a dead route even though the package and
Skills CLI installation correctly expose only 12 WTK skills.

## Remediation recommendation

Delete the tracked `.claude/skills/wtk-config` symlink. Extend the existing distribution contract to
compare tracked WTK Claude aliases with the 12 published skill names and require every alias target to
resolve. Then rerun the source/package inventory walk and the two affected scenarios.
