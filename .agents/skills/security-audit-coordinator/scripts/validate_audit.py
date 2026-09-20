#!/usr/bin/env python3
"""Validate security-audit coverage and finding artifacts; standard library only."""

import json
import re
import stat
import sys
from pathlib import Path, PurePosixPath


MAX_BYTES = 5 * 1024 * 1024
LOAD_FAILED = object()
FINGERPRINT = re.compile(r"[A-Za-z0-9][A-Za-z0-9._:/@+-]{0,255}\Z")
AGENT_ID = re.compile(r"[a-z0-9][a-z0-9_-]{0,63}\Z")
PROFILES = {"quick", "standard", "deep"}
RUN_STATUSES = {"in_progress", "complete", "partial"}
UNIT_STATUSES = {
    "planned", "covered", "candidate", "blocked", "deferred",
    "out_of_scope", "not_applicable",
}
SEVERITIES = {"informational", "low", "medium", "high", "critical"}
VERDICTS = {"confirmed", "needs_validation", "rejected"}


def visible(value):
    return (isinstance(value, str) and bool(value.strip()) and
            not any(ord(char) < 32 or ord(char) == 127 for char in value))


def one_of(value, choices):
    return isinstance(value, str) and value in choices


def positive_integer(value):
    return isinstance(value, int) and not isinstance(value, bool) and value > 0


def string_list(value, *, nonempty=False):
    return (isinstance(value, list) and (not nonempty or bool(value)) and
            all(visible(item) for item in value) and len(value) == len(set(value)))


def safe_path(value):
    if not visible(value) or "\\" in value or re.match(r"^[A-Za-z]:", value):
        return False
    path = PurePosixPath(value)
    return not path.is_absolute() and value not in {".", ".."} and ".." not in path.parts


def add_unknown(errors, location, value, allowed):
    if isinstance(value, dict):
        for key in sorted(set(value) - allowed):
            errors.append(f"{location}: unexpected field {key!r}")


def load_json(path):
    path = Path(path)
    try:
        info = path.lstat()
        if not stat.S_ISREG(info.st_mode) or path.is_symlink():
            return LOAD_FAILED, [f"{path.name}: input must be a regular non-symlink file"]
        if info.st_size > MAX_BYTES:
            return LOAD_FAILED, [f"{path.name}: input exceeds {MAX_BYTES} bytes"]
        text = path.read_text(encoding="utf-8")
        return json.loads(text), []
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        return LOAD_FAILED, [f"{path.name}: cannot read valid UTF-8 JSON ({type(exc).__name__})"]


def validate_coverage(document):
    errors = []
    required = {"source_ref", "scope", "profile", "run_status", "units"}
    allowed = required | {"budget", "prior_runs", "independent_verification"}
    if not isinstance(document, dict):
        return ["coverage: top level must be an object"]
    add_unknown(errors, "coverage", document, allowed)
    for key in sorted(required - set(document)):
        errors.append(f"coverage: missing field {key!r}")
    if not visible(document.get("source_ref")):
        errors.append("coverage.source_ref: visible text required")
    if not string_list(document.get("scope"), nonempty=True):
        errors.append("coverage.scope: unique nonempty text list required")
    if not one_of(document.get("profile"), PROFILES):
        errors.append("coverage.profile: expected quick, standard or deep")
    if not one_of(document.get("run_status"), RUN_STATUSES):
        errors.append("coverage.run_status: invalid status")
    if "prior_runs" in document and not string_list(document["prior_runs"]):
        errors.append("coverage.prior_runs: unique text list required")
    if "independent_verification" in document and not isinstance(
            document["independent_verification"], bool):
        errors.append("coverage.independent_verification: boolean required")
    if "budget" in document and document["budget"] is not None:
        if not positive_integer(document["budget"]):
            errors.append("coverage.budget: positive integer or null required")

    units = document.get("units")
    if not isinstance(units, list):
        errors.append("coverage.units: array required")
        return errors
    ids = []
    for index, unit in enumerate(units):
        location = f"coverage.units[{index}]"
        required_unit = {
            "coverage_id", "surface", "boundary", "subsystem", "attack_class",
            "starting_paths", "status", "reviewed_paths", "candidate_fingerprints", "unresolved",
        }
        allowed_unit = required_unit | {"agent_id"}
        if not isinstance(unit, dict):
            errors.append(f"{location}: object required")
            continue
        add_unknown(errors, location, unit, allowed_unit)
        for key in sorted(required_unit - set(unit)):
            errors.append(f"{location}: missing field {key!r}")
        coverage_id = unit.get("coverage_id")
        if not visible(coverage_id):
            errors.append(f"{location}.coverage_id: visible text required")
        else:
            ids.append(coverage_id)
        for key in ("surface", "boundary", "subsystem", "attack_class"):
            if not visible(unit.get(key)):
                errors.append(f"{location}.{key}: visible text required")
        status_value = unit.get("status")
        if not one_of(status_value, UNIT_STATUSES):
            errors.append(f"{location}.status: invalid status")
        reviewed = unit.get("reviewed_paths")
        if (not isinstance(reviewed, list) or
                not all(isinstance(item, str) for item in reviewed) or
                len(reviewed) != len(set(reviewed))):
            errors.append(f"{location}.reviewed_paths: unique array required")
            reviewed = []
        elif not all(safe_path(item) for item in reviewed):
            errors.append(f"{location}.reviewed_paths: unsafe repository path")
        fingerprints = unit.get("candidate_fingerprints")
        if (not isinstance(fingerprints, list) or
                not all(isinstance(item, str) for item in fingerprints) or
                len(fingerprints) != len(set(fingerprints))):
            errors.append(f"{location}.candidate_fingerprints: unique array required")
            fingerprints = []
        elif not all(isinstance(item, str) and FINGERPRINT.fullmatch(item)
                     for item in fingerprints):
            errors.append(f"{location}.candidate_fingerprints: invalid fingerprint")
        unresolved = unit.get("unresolved")
        if not string_list(unresolved):
            errors.append(f"{location}.unresolved: unique text array required")
            unresolved = []
        starts = unit.get("starting_paths")
        if (not isinstance(starts, list) or not starts or
                not all(safe_path(item) for item in starts) or
                len(starts) != len(set(starts))):
            errors.append(f"{location}.starting_paths: unique nonempty safe path array required")
        if "agent_id" in unit and unit["agent_id"] is not None:
            if not isinstance(unit["agent_id"], str) or not AGENT_ID.fullmatch(unit["agent_id"]):
                errors.append(f"{location}.agent_id: invalid agent identifier")

        if status_value == "planned" and (reviewed or fingerprints or unresolved):
            errors.append(f"{location}: planned unit must have empty result fields")
        if status_value == "covered" and (not reviewed or fingerprints or unresolved):
            errors.append(f"{location}: covered unit needs paths and no candidate/blocker")
        if status_value == "candidate" and (not reviewed or not fingerprints):
            errors.append(f"{location}: candidate unit needs paths and fingerprints")
        if status_value == "blocked" and (not reviewed or fingerprints or not unresolved):
            errors.append(f"{location}: blocked unit needs paths and blockers only")
        if one_of(status_value, {"deferred", "out_of_scope", "not_applicable"}):
            if reviewed or fingerprints or not unresolved:
                errors.append(f"{location}: terminal gap needs only a reason")

    if ids != sorted(ids):
        errors.append("coverage.units: must be sorted by coverage_id")
    if len(ids) != len(set(ids)):
        errors.append("coverage.units: duplicate coverage_id")
    if document.get("run_status") == "complete":
        incomplete = {"planned", "blocked", "deferred"}
        if any(isinstance(unit, dict) and one_of(unit.get("status"), incomplete)
               for unit in units):
            errors.append("coverage.run_status: complete run has unfinished units")
    return errors


def validate_locations(value, location, errors):
    if not isinstance(value, list) or not value:
        errors.append(f"{location}: nonempty array required")
        return
    for index, item in enumerate(value):
        item_location = f"{location}[{index}]"
        if not isinstance(item, dict):
            errors.append(f"{item_location}: object required")
            continue
        allowed = {"file", "line", "description"}
        add_unknown(errors, item_location, item, allowed)
        missing = allowed - set(item)
        if missing:
            errors.append(f"{item_location}: missing fields {', '.join(sorted(missing))}")
            continue
        if not safe_path(item["file"]):
            errors.append(f"{item_location}.file: unsafe repository path")
        if not positive_integer(item["line"]):
            errors.append(f"{item_location}.line: positive integer required")
        if not visible(item["description"]):
            errors.append(f"{item_location}.description: visible text required")


def validate_findings(document):
    errors = []
    if not isinstance(document, list):
        return ["findings: top level must be an array"]
    fingerprints = []
    common = {"verdict", "fingerprint", "title", "trace", "evidence"}
    branches = {
        "confirmed": {"impact", "severity", "confidence", "verification_method",
                      "remediation", "regression_test"},
        "needs_validation": {"blockers", "validation_plan"},
        "rejected": {"reason"},
    }
    for index, finding in enumerate(document):
        location = f"findings[{index}]"
        if not isinstance(finding, dict):
            errors.append(f"{location}: object required")
            continue
        verdict = finding.get("verdict")
        if not one_of(verdict, VERDICTS):
            errors.append(f"{location}.verdict: invalid verdict")
            continue
        allowed = common | branches[verdict]
        add_unknown(errors, location, finding, allowed)
        for key in sorted(allowed - set(finding)):
            errors.append(f"{location}: missing field {key!r}")
        fingerprint = finding.get("fingerprint")
        if not isinstance(fingerprint, str) or not FINGERPRINT.fullmatch(fingerprint):
            errors.append(f"{location}.fingerprint: invalid fingerprint")
        else:
            fingerprints.append(fingerprint)
        if not visible(finding.get("title")):
            errors.append(f"{location}.title: visible text required")
        validate_locations(finding.get("trace"), f"{location}.trace", errors)
        validate_locations(finding.get("evidence"), f"{location}.evidence", errors)

        if verdict == "confirmed":
            for key in ("impact", "remediation", "regression_test"):
                if not visible(finding.get(key)):
                    errors.append(f"{location}.{key}: visible text required")
            if not one_of(finding.get("severity"), SEVERITIES):
                errors.append(f"{location}.severity: invalid severity")
            if not one_of(finding.get("confidence"), {"low", "medium", "high"}):
                errors.append(f"{location}.confidence: invalid confidence")
            if not one_of(finding.get("verification_method"), {"static", "test", "observed"}):
                errors.append(f"{location}.verification_method: invalid method")
        elif verdict == "needs_validation":
            if not string_list(finding.get("blockers"), nonempty=True):
                errors.append(f"{location}.blockers: nonempty unique text list required")
            if not visible(finding.get("validation_plan")):
                errors.append(f"{location}.validation_plan: visible text required")
        elif not visible(finding.get("reason")):
            errors.append(f"{location}.reason: visible text required")

    if fingerprints != sorted(fingerprints):
        errors.append("findings: must be sorted by fingerprint")
    if len(fingerprints) != len(set(fingerprints)):
        errors.append("findings: duplicate fingerprint")
    return errors


def validate_pair(coverage, findings):
    errors = []
    candidate_fingerprints = set()
    if isinstance(coverage, dict) and isinstance(coverage.get("units"), list):
        for unit in coverage["units"]:
            if isinstance(unit, dict) and isinstance(unit.get("candidate_fingerprints"), list):
                candidate_fingerprints.update(
                    item for item in unit["candidate_fingerprints"] if isinstance(item, str)
                )
    finding_fingerprints = {
        item.get("fingerprint") for item in findings
        if isinstance(item, dict) and isinstance(item.get("fingerprint"), str)
    } if isinstance(findings, list) else set()
    if not finding_fingerprints.issubset(candidate_fingerprints):
        errors.append("pair: every finding must link to a candidate coverage unit")
    if isinstance(coverage, dict) and coverage.get("run_status") == "complete":
        if candidate_fingerprints != finding_fingerprints:
            errors.append("pair: complete run needs a final record for every candidate")
        if isinstance(coverage.get("units"), list) and any(
                isinstance(unit, dict) and unit.get("status") == "candidate" and
                bool(unit.get("unresolved")) for unit in coverage["units"]):
            errors.append("pair: complete run cannot retain unresolved candidate evidence")
        if isinstance(findings, list) and any(
                isinstance(item, dict) and item.get("verdict") == "needs_validation"
                for item in findings):
            errors.append("pair: complete run cannot retain needs_validation blockers")
    return errors


def main(argv=None):
    argv = sys.argv[1:] if argv is None else argv
    if len(argv) != 2:
        print("usage: validate_audit.py COVERAGE_JSON FINDINGS_JSON", file=sys.stderr)
        return 2
    coverage, errors = load_json(argv[0])
    findings, finding_errors = load_json(argv[1])
    errors.extend(finding_errors)
    if coverage is not LOAD_FAILED:
        errors.extend(validate_coverage(coverage))
    if findings is not LOAD_FAILED:
        errors.extend(validate_findings(findings))
    if coverage is not LOAD_FAILED and findings is not LOAD_FAILED:
        errors.extend(validate_pair(coverage, findings))
    if errors:
        print("\n".join(errors[:100]), file=sys.stderr)
        return 1
    print("PASS: coverage and findings are structurally consistent")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
