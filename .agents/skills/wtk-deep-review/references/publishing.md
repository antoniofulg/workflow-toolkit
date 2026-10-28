# Publish a Review

**Read when:** publishing a completed Deep Review with explicit authority.

Use the PR integration selected in project guidelines or explicitly authorized for this task.
Verify identity, access and the target repository/PR before writing. The skill requires publication
outcomes, not a particular CLI, API transport or hosting provider. If an outcome is unsupported,
retain the complete local report and name the limitation instead of claiming publication.

## Publication contract

1. Upsert one walkthrough comment using `<!-- wtk-deep-review:walkthrough -->`; edit the existing
   comment when its marker is present.
2. Check anchors against the manifest's changed-line ranges. Publish every anchorable in-diff
   defect and advisory inline; low severity is not a reason to collapse it. Keep outside-diff,
   drifted or rejected anchors in the matching review-body section.
3. Preserve each result's fingerprint marker and evidence certificate. The body starts with
   `**Defects posted: <n> · Advisories posted: <n>**`, includes Outside diff, Duplicates and
   unanchorable results, and ends with `Reviewing files that changed between <base> and <head>.`
4. Follow the selected integration's review-event rules and batching limits. An allowed
   request-changes event requires `request_changes_workflow: true` and open Critical/Major defects;
   advisories never change the event. Respect self-review restrictions.
5. Update resolved prior-round comments while preserving their original content and identifying
   the fixing commit. Unresolved prior results appear once under Duplicates, not as new inline posts.
6. Cite the walkthrough and review URLs.

Before posting, check for the same base/head scope line. One review series per round and head SHA
is allowed; a match means that submission already ran. Resume missing publication steps without
duplicating completed comments or reviews.

## Recover prior state

When local state is unavailable, use the selected integration to read PR comments and reviews,
recover `wtk-deep-review:fp:<fingerprint>` markers and the latest reviewed base/head scope line.
A fingerprint absent from current results remains open unless a reviewer supplies an evidence-bearing
`prior_findings` disposition with `status: resolved`; otherwise it remains under Duplicates.

Retain the reviewed commit range, result counts, URLs and any rejected or unsupported operations
in the existing report. A transport failure does not erase review coverage or authorize another tool.
