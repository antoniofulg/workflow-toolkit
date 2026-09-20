# Audit records and reporting

## Coverage document

`coverage.json` is an object with `source_ref`, `scope`, `profile`, `run_status`
and sorted `units`. Use `complete` only when no unit is planned, in progress,
blocked or deferred and every candidate fingerprint has a final finding record.
Use `partial` for scope, budget, worker, tool or evidence gaps.

## Finding records

Sort `findings.json` by stable fingerprint. Every record includes verdict,
fingerprint, title, ordered repository-relative trace and nonempty evidence.
Fingerprints identify the root cause; exclude line, severity, worker and verdict.

- `confirmed`: include impact, severity, confidence, verification method,
  remediation and regression idea. Overall severity cannot exceed demonstrated
  impact. Static evidence is valid when the complete path is established.
- `needs_validation`: include exact blockers and a bounded local or owner-observed
  validation plan. Omit severity and remediation that assumes the missing fact.
- `rejected`: include the disproving reason. Retain it for future deduplication but
  do not present it as a finding.

Never include secret values, partial values or fingerprints of secrets. Describe
location and credential type only. Put dependency resolved version, current advisory
source/date, affected range and reachability status in `evidence[].description`.

## Human report

Start `REPORT.md` with source ref, dirty state, profile, scope, budget use, prior-run
use and whether verification was independent. State `partial` prominently when
applicable. Then include:

1. Confirmed findings by severity, each with boundary, trace, outcome and fix.
2. Needs-validation records with exact blockers and safe next checks.
3. Separate hardening notes and positive controls.
4. Coverage counts, important exclusions, deferred units and critic result.
5. Tool, documentation, sandbox and deployment limitations.

A zero-finding report says only that no confirmed vulnerabilities were found in
the examined scope. Proposed patches remain proposals until separately authorized.
