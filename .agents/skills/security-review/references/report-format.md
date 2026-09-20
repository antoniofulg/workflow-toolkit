# Security review report

Modified synthesis of Sentry/OWASP and GitHub Awesome Copilot; CC BY-SA 4.0.
See [provenance](../THIRD_PARTY_NOTICES.md).

Start with mode, requested scope, snapshot/base/head and counts by severity
(Critical/High/Medium/Low), counting only confirmed findings.

For each confirmed finding include:
- Stable finding ID and short title.
- Severity with contextual rationale; High confidence with supporting evidence.
- File and line (changed line for diff), plus redacted snippet where useful.
- Attacker role, input origin, transformations/control checks and sink.
- Concrete impact, exploit preconditions and evidence of control failure.
- Verification method: static trace, test or observed reproduction.
- Mitigation and regression test; related candidates deduplicated by root cause.

Before finalizing, verify every cited line against the exact reviewed source
snapshot. For virtual files embedded in JSON, decode the file and count its own
lines; JSON container lines and remembered offsets are not source locations.

Then include **Needs verification**, **Hardening recommendations**, and
**Coverage and limitations**. For each gap state the omitted check and consequence.
Report inspected paths/surfaces, tools and versions/date, failed/unavailable checks,
runtime versus build/test coverage, network restrictions and exclusions.

With zero confirmed findings, say “No confirmed vulnerabilities found in the
examined scope,” followed by actual coverage and limitations. Never imply an
unperformed dependency audit or blanket security guarantee.
