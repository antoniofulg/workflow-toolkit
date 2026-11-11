#!/usr/bin/env python3
"""
validate_verification.py - deterministic completion gate for a feature.

The skill's strongest invariant is "a feature is done when an independent Verifier's
report accounts for every check." That is prose the model has to remember, and prose
is what a long trajectory quietly drops. This turns it into a checkable pass/fail run
as the closing step, so declaring a feature done without a real report fails loudly.

It does NOT merely check that verification.md exists. A report that exists but holds
the template placeholder, cites no evidence, or records a surviving mutant next to a
PASS verdict would sail through a shallow existence check while proving nothing. The
gate reads the report's own tables and refuses a verdict its rows contradict.

Pure standard library, zero dependencies. Operates only on the .specs/ markdown
artifacts, so it stays stack-agnostic.

What it checks:
  ERROR  - no verification.md (Verify is the closing step of the flow, not an option)
  ERROR  - no proofs.md, a proofs.md row that does not read `pass`, or one written at another HEAD
  ERROR  - the verdict is FAIL, missing, or still the '[PASS | FAIL]' placeholder
  ERROR  - PASS with no file:line evidence anywhere (evidence-or-zero)
  ERROR  - profile standard/ui with no recomputed Coverage section
  ERROR  - a `Risk:` check or an `unsure` check with no fault row naming it (up to five)
  ERROR  - PASS while a fault row's Disposition is not killed, equivalent - <reason>, arid - <reason>
           or accepted - <reason>, or is accepted on a `Risk:` check
  ERROR  - PASS while a check has no `## Checks` row, names no test, or reads `Holds` other than
           `yes` without a closing commit
  ERROR  - PASS while a mutation-run row reports more survivors than equivalent/arid rows record
  ERROR  - PASS while a Coverage row leaves a member Unproven
  ERROR  - PASS while a binding source records a Contradiction or leaves an element Uncovered
  ERROR  - profile ui with missing, incomplete or non-PASS visual fidelity evidence
  ERROR  - profile ui with no screens.md, a verdict other than `matches`, a `**Round**` above 2, or a
           `**HEAD**` other than the current one
  ERROR  - PASS while a Test policy row's expectation is not met
  ERROR  - the report's profile does not match the one checks.md was approved under
  ERROR  - profile ui, but the report carries no binding-sources section (step 1 vanished)
  ERROR  - profile standard/ui with Test policy rows in checks.md, but no verdicts in the report
  WARN   - the report says self-verified (author == verifier: degraded gate)
  WARN   - no `Profile:` line, so a skipped step cannot be told from a forgotten one
  WARN   - no `Round:` line

Usage:
  python3 <skill-dir>/scripts/validate_verification.py [feature] [--root DIR] [--strict]

  Invoke from the skill directory that ships this script (not the project root).
  Pass --root when cwd is not the project that contains .specs/.

Exit codes: 0 ok, 1 the feature is not done, 2 usage error.
"""

import argparse
import os
import re
import subprocess
import sys

from native_evidence import intent_errors, read_risk, unfenced_lines, usable_value

EVIDENCE_RE = re.compile(r"[\w./-]+\.[A-Za-z0-9]+:\d+")
PROFILE_RE = re.compile(r"^\**Profile\**\s*:\s*`?(\w+)`?", re.IGNORECASE | re.MULTILINE)
EMPTY_CELL = {"", "-", "—", "–", "none", "n/a", "na", "nothing"}
CID_RE = re.compile(r"\bC\d+\b")
CHECK_LINE_RE = re.compile(r"^\**\s*(C\d+)\s*\**\s*[-–—:]")
HOLDS_RE = re.compile(r"^(yes|no|unsure)\b", re.IGNORECASE)
SHA_RE = re.compile(r"\b(?=[0-9a-f]*\d)[0-9a-f]{7,40}\b")
MAX_FAULTS = 5
DISPOSITION_RE = re.compile(r"^(killed|equivalent|arid|accepted)\b\s*(?:[-–—:]\s*(.*))?$", re.IGNORECASE)
ROUND_RE = re.compile(r"^\**\s*Round\s*\**\s*:\s*\**\s*(\d+)", re.IGNORECASE)
JUDGED_HEAD_RE = re.compile(r"^\**\s*HEAD\s*\**\s*:\s*\**\s*`?([0-9a-f]{4,40})", re.IGNORECASE)
MAX_ROUNDS = 2
UNMET_RE = re.compile(r"\b(no|not met|unmet|fail|failed|gap)\b", re.IGNORECASE)


def _feature_dirs(root):
    base = os.path.join(root, ".specs", "features")
    if not os.path.isdir(base):
        return base, []
    return base, [d for d in sorted(os.listdir(base)) if os.path.isdir(os.path.join(base, d))]


def split_row(line):
    return [c.strip() for c in line.strip().strip("|").split("|")]


def is_separator(line):
    return bool(re.match(r"^\s*\|?[\s:|-]+\|?\s*$", line)) and "-" in line


def strip_fences(text):
    return unfenced_lines(text)


def find_tables(lines):
    """Return [(header_cells_lowercased, [data_row_cells, ...]), ...] for every table."""
    tables, buf = [], []
    for ln in lines + [""]:
        stripped = ln.strip()
        if stripped.startswith("|"):
            buf.append(stripped)
            continue
        if buf:
            rows = [split_row(r) for r in buf if not is_separator(r)]
            if rows:
                tables.append(([c.lower() for c in rows[0]], rows[1:]))
            buf = []
    return tables


def column(header, *names):
    for i, cell in enumerate(header):
        for n in names:
            if n in cell:
                return i
    return None


def has_heading(lines, *names):
    for ln in lines:
        s = ln.strip()
        for n in names:
            if re.match(r"^#{1,4}\s+" + re.escape(n) + r"\b", s, re.IGNORECASE):
                return True
    return False


def _profile(text):
    m = PROFILE_RE.search(text)
    return m.group(1).lower() if m else None


def _checks_context(fdir):
    """What checks.md was approved under: (profile, has a Test policy section, its unfenced lines)."""
    path = os.path.join(fdir, "checks.md")
    if not os.path.exists(path):
        return None, False, []
    body = open(path, encoding="utf-8", errors="replace").read()
    lines = strip_fences(body)
    return _profile("\n".join(lines)), has_heading(lines, "Test policy"), lines


def _judgments(name, tables, check_ids):
    """The Verifier's `## Checks` table: a row per check with the test it read and whether it holds.

    Returns (errors, ids judged `unsure`). A `Holds` other than `yes` stands only with the commit that
    closed it, so a PASS cannot sit beside an open judgment.
    """
    errors, unsure, judged = [], set(), set()
    for header, rows in tables:
        check, test, holds = column(header, "check"), column(header, "test"), column(header, "holds")
        if check is None or test is None or holds is None:
            continue
        for r in rows:
            cid = r[check].strip("*` ") if check < len(r) else ""
            judged.add(cid)
            if test >= len(r) or not usable_value(r[test]):
                errors.append(f"{name}: `## Checks` row {cid} names no test - write the test its proof selects, file and name")
            cell = r[holds] if holds < len(r) else ""
            m = HOLDS_RE.match(cell.strip("` "))
            if not m:
                errors.append(f"{name}: `## Checks` row {cid} reads Holds {cell[:30]!r} - expected yes, no or unsure")
                continue
            if m[1].lower() == "unsure":
                unsure.add(cid)
            if m[1].lower() != "yes" and not SHA_RE.search(cell):
                errors.append(
                    f"{name}: PASS but check {cid} reads Holds {cell[:40]!r} with no closing commit - fix it "
                    f"and write the commit in the cell"
                )
    if not judged and check_ids:
        errors.append(f"{name}: verification.md has no `## Checks` table with Check, Test and Holds columns")
    else:
        for cid in sorted(check_ids - judged, key=lambda c: int(c[1:])):
            errors.append(f"{name}: verification.md `## Checks` has no row for {cid} - judge its test against the criterion")
    return errors, unsure


def _git_head(fdir):
    """Short HEAD of the project holding `.specs/features/<name>`; None when git cannot say."""
    features = os.path.dirname(os.path.abspath(fdir))
    specs = os.path.dirname(features)
    if os.path.basename(features) != "features" or os.path.basename(specs) != ".specs":
        return None
    try:
        proc = subprocess.run(["git", "rev-parse", "--short", "HEAD"], cwd=os.path.dirname(specs),
                              capture_output=True, text=True)
    except OSError:
        return None
    return proc.stdout.strip() if proc.returncode == 0 else None


def _stale(fdir, recorded):
    """True when git can name HEAD and the recorded sha is not it."""
    head = _git_head(fdir)
    return bool(head) and not (head.startswith(recorded) or recorded.startswith(head))


def _screens_errors(fdir, name):
    """screens.md is the screens judge's verdict: it must exist, match, be round 1 or 2, and be current."""
    path = os.path.join(fdir, "screens.md")
    if not os.path.isfile(path):
        return [f"{name}: profile is ui but there is no screens.md - a fresh screens judge compares each "
                f"picture with its capture (wtk/references/ui-ux.md#screens-judge-ui)"]
    with open(path, encoding="utf-8", errors="replace") as source:
        lines = strip_fences(source.read())
    errors = []
    rounds = [int(m[1]) for m in (ROUND_RE.match(ln.strip()) for ln in lines) if m]
    if not rounds:
        errors.append(f"{name}: screens.md has no `**Round**:` line - the judge writes 1, and 2 on the last round")
    elif rounds[0] > MAX_ROUNDS:
        errors.append(f"{name}: screens.md reads `**Round**: {rounds[0]}` - there is no round 3; what still differs goes to the user")
    judged = next((m[1] for m in (JUDGED_HEAD_RE.match(ln.strip()) for ln in lines) if m), None)
    if not judged:
        errors.append(f"{name}: screens.md names no `**HEAD**` - the judge writes the commit it judged")
    elif _stale(fdir, judged):
        errors.append(f"{name}: screens.md judged {judged} and HEAD is {_git_head(fdir)} - the judge runs again at HEAD")
    verdicts = 0
    for header, rows in find_tables(lines):
        verdict, screen = column(header, "verdict"), column(header, "screen")
        if verdict is None or screen is None:
            continue
        for row in rows:
            verdicts += 1
            if verdict >= len(row) or row[verdict].strip("` ").lower() != "matches":
                errors.append(f"{name}: screens.md - '{row[0][:50]}' reads {row[verdict][:20] if verdict < len(row) else ''!r}, not matches")
    if not verdicts:
        errors.append(f"{name}: screens.md has no verdict table with `Screen` and `Verdict` columns")
    return errors


def _proof_counts(checks_lines):
    """{check id: number of `Proof:` lines} outside fenced blocks."""
    counts, current = {}, None
    for ln in checks_lines:
        if re.match(r"^#{1,2}\s+\S", ln):
            current = None
        m = CHECK_LINE_RE.match(ln.strip())
        if m:
            current = m[1]
            counts[current] = 0
        elif current and re.match(r"^\**\s*Proof\s*\**\s*:", ln.strip(), re.IGNORECASE):
            counts[current] += 1
    return counts


def _proofs_errors(fdir, name, checks_lines):
    """proofs.md is check_proofs.py's record: a row per `Proof:` line, each `pass`, written at the HEAD being gated."""
    path = os.path.join(fdir, "proofs.md")
    if not os.path.isfile(path):
        return [f"{name}: no proofs.md - run check_proofs.py {name} at a clean HEAD"]
    with open(path, encoding="utf-8", errors="replace") as source:
        lines = strip_fences(source.read())
    errors = []
    recorded = re.search(r"\*\*HEAD\*\*\s*:\s*`?([0-9a-f]{4,40})", "\n".join(lines))
    if not recorded:
        errors.append(f"{name}: proofs.md names no `**HEAD**` - run check_proofs.py {name} again")
    elif _stale(fdir, recorded[1]):
        errors.append(f"{name}: proofs.md was written at {recorded[1]} and HEAD is {_git_head(fdir)} - run check_proofs.py {name} again")
    rows, per_check = 0, {}
    for header, table in find_tables(lines):
        result = column(header, "result")
        if result is None or column(header, "proof") is None:
            continue
        for row in table:
            rows += 1
            owner = re.match(r"(C\d+):", row[0])
            if owner:
                per_check[owner[1]] = per_check.get(owner[1], 0) + 1
            if result >= len(row) or row[result] != "pass":
                errors.append(f"{name}: proofs.md - {row[0][:60]} reads {row[result][:20] if result < len(row) else ''!r}")
    if not rows:
        errors.append(f"{name}: proofs.md has no proof rows - run check_proofs.py {name} again")
    for cid, expected in sorted(_proof_counts(checks_lines).items(), key=lambda kv: int(kv[0][1:])):
        if per_check.get(cid, 0) < expected:
            errors.append(
                f"{name}: proofs.md has {per_check.get(cid, 0)} row(s) for {cid} but checks.md names {expected} "
                f"proof(s) - run check_proofs.py {name} again"
            )
    return errors


def _verdict(lines):
    """Return 'pass', 'fail', 'unfilled', or None."""
    candidates = [
        ln for ln in lines
        if re.search(r"^\**verdict\**\s*:", ln.strip(), re.IGNORECASE)
        or re.search(r"^#{1,4}\s*verification\b", ln.strip(), re.IGNORECASE)
    ]
    hay = " ".join(candidates) if candidates else "\n".join(lines)
    has_pass = re.search(r"\bPASS\b", hay) is not None
    has_fail = re.search(r"\bFAIL\b", hay) is not None
    if has_pass and has_fail:
        return "unfilled"
    if has_pass:
        return "pass"
    if has_fail:
        return "fail"
    return None


def _check_feature(fdir, name):
    errors, warnings = intent_errors(os.path.join(fdir, "checks.md")), []
    vpath = os.path.join(fdir, "verification.md")
    if not os.path.exists(vpath):
        errors.append(
            f"{name}: no verification.md - the feature is not done until a fresh Verifier "
            f"(author != verifier) writes it over <feature base>..HEAD with every check"
        )
        return errors, warnings

    text = open(vpath, encoding="utf-8", errors="replace").read()
    lines = strip_fences(text)
    body = "\n".join(lines)

    verdict = _verdict(lines)
    if verdict is None:
        errors.append(f"{name}: no PASS/FAIL verdict (a prose-only report does not count)")
    elif verdict == "unfilled":
        errors.append(f"{name}: verdict is still the template placeholder '[PASS | FAIL]'")
    elif verdict == "fail":
        errors.append(f"{name}: verdict is FAIL - route the ranked gaps back as fixes, then re-verify")

    # The profile decides which steps run, so a report that quietly declares a cheaper one
    # than the feature was approved under makes an entire step disappear without a trace.
    report_profile = _profile(body)
    approved_profile, policy_rows_exist, checks_lines = _checks_context(fdir)
    if report_profile is None:
        warnings.append(f"{name}: no `Profile:` line - a step that did not run is indistinguishable from one forgotten")
    elif approved_profile and report_profile != approved_profile:
        errors.append(
            f"{name}: report says profile '{report_profile}' but checks.md was approved under "
            f"'{approved_profile}' - the profile decides which steps run, so a mismatch silently drops one"
        )
    effective = approved_profile or report_profile
    if not re.search(r"^\**round\**\s*:", body, re.IGNORECASE | re.MULTILINE):
        warnings.append(f"{name}: no `Round:` line - a scoped re-verification must say what was carried forward")
    if re.search(r"self[- ]verified", body, re.IGNORECASE):
        warnings.append(
            f"{name}: report is self-verified (author == verifier) - a degraded gate, "
            f"since a self-check reproduces the author's own blind spot"
        )

    errors += _proofs_errors(fdir, name, _checks_context(fdir)[2])

    if verdict != "pass":
        return errors, warnings

    if not EVIDENCE_RE.search(body):
        errors.append(f"{name}: PASS but cites no file:line evidence - evidence-or-zero not satisfied")

    # A profile-scoped step that produced no section did not run. Requiring the section is what
    # makes "skipped" distinguishable from "forgotten" - otherwise that is only a sentence.
    if effective in ("standard", "ui") and not has_heading(lines, "Coverage"):
        errors.append(
            f"{name}: profile is {effective} but there is no `## Coverage` section - the join has to "
            f"be recomputed from the authority over each set, not read back from the author's table"
        )
    if effective == "ui" and not has_heading(lines, "Binding sources", "Binding source"):
        errors.append(
            f"{name}: profile is ui but there is no `## Binding sources` section - step 1 is the "
            f"only step that can catch a check contradicting the design, and no later step can"
        )
    if effective in ("standard", "ui") and policy_rows_exist and not has_heading(lines, "Test policy"):
        errors.append(
            f"{name}: checks.md carries Test policy rows but the report gives no verdict on them - "
            f"those rows are the bar the author built under, so an unmet one is a finding"
        )

    tables = find_tables(lines)
    if effective == "ui":
        errors += _screens_errors(fdir, name)
        visual_lines = []
        in_visual = False
        for line in lines:
            if line.startswith("## "):
                in_visual = line.strip().lower() == "## visual fidelity"
            elif in_visual:
                visual_lines.append(line)
        visual_tables = find_tables(visual_lines)
        required = (
            "source/revision", "source scale", "implementation revision", "screen/state",
            "viewport/scroll", "environment", "reference capture", "full-page capture",
            "viewport capture", "comparison", "result",
        )
        evidence_rows = 0
        for header, rows in visual_tables:
            if not all(header.count(field) == 1 for field in required):
                errors.append(f"{name}: visual fidelity table has unsupported or incomplete provenance columns - expected {', '.join(required)}")
                continue
            for row in rows:
                evidence_rows += 1
                cells = {field: row[header.index(field)] if header.index(field) < len(row) else ""
                         for field in required}
                missing = [field for field, value in cells.items() if not usable_value(value)]
                if missing:
                    errors.append(f"{name}: visual fidelity row lacks usable provenance: {', '.join(missing)}")
                if cells["result"].upper() != "PASS":
                    errors.append(f"{name}: visual fidelity is not PASS ({row[0][:50]})")
                scale = cells["source scale"].strip("` ")
                if not re.fullmatch(r"(?:[1-9]\d*(?:\.\d+)?|0\.\d*[1-9]\d*)x?", scale):
                    errors.append(f"{name}: visual fidelity source scale must be positive (for example 1x)")
                viewport = cells["viewport/scroll"].strip("` ")
                if not re.fullmatch(r"[1-9]\d*\s*[x×]\s*[1-9]\d*;\s*scroll:\s*\d+(?:\.\d+)?,\s*\d+(?:\.\d+)?", viewport, re.I):
                    errors.append(f"{name}: visual fidelity viewport/scroll must name widthxheight (CSS px or device points); scroll: x,y")
                environment = dict(
                    (key.strip().lower(), value.strip())
                    for part in cells["environment"].split(";") if ":" in part
                    for key, value in [part.split(":", 1)]
                )
                if not usable_value(environment.get("runtime", "")) or not re.fullmatch(
                    r"(?:[1-9]\d*(?:\.\d+)?|0\.\d*[1-9]\d*)", environment.get("scale", "")
                ):
                    errors.append(f"{name}: visual fidelity environment requires runtime (browser or device/OS) and positive scale (DPR or device scale)")
                for field in ("reference capture", "full-page capture", "viewport capture"):
                    capture = cells[field].strip().strip("`")
                    local = capture if os.path.isabs(capture) else os.path.join(fdir, capture)
                    if not usable_value(capture) or re.match(r"[A-Za-z][A-Za-z0-9+.-]*://", capture) or not os.path.isfile(local):
                        errors.append(f"{name}: visual fidelity {field} is not an existing local file: {capture!r} (relative to verification.md)")
        if not evidence_rows:
            errors.append(f"{name}: ui requires a visual fidelity evidence table with {', '.join(required)}")

    check_ids = {m[1] for m in (CHECK_LINE_RE.match(ln.strip()) for ln in checks_lines) if m}
    judgment_errors, unsure = _judgments(name, tables, check_ids)
    errors += judgment_errors
    risk = read_risk(checks_lines) if effective in ("standard", "ui") else None
    risk_ids = set(risk[0]) if risk else set()
    fault_checks = set()
    survivors_run = survivors_recorded = 0

    for header, rows in tables:
        disposition = column(header, "disposition")
        if disposition is not None:
            check, mutation = column(header, "check"), column(header, "mutation")
            for r in rows:
                cell = r[disposition].strip("` ") if disposition < len(r) else ""
                label = r[mutation][:50] if mutation is not None and mutation < len(r) else r[0][:50]
                ids = set(CID_RE.findall(r[check])) if check is not None and check < len(r) else set()
                fault_checks |= ids
                m = DISPOSITION_RE.match(cell)
                if not m:
                    errors.append(
                        f"{name}: PASS but mutant '{label}' has disposition {cell[:30]!r} - expected killed, "
                        f"equivalent - <reason>, arid - <reason> or accepted - <reason>; a survivor is a finding"
                    )
                elif m[1].lower() != "killed":
                    if not usable_value(m[2] or ""):
                        errors.append(f"{name}: {m[1].lower()} mutant '{label}' needs a one-line reason")
                    if m[1].lower() == "accepted":
                        if not ids:
                            errors.append(f"{name}: accepted mutant '{label}' names no Check - an accepted survivor must sit outside the `Risk:` checks")
                        elif ids & risk_ids:
                            errors.append(
                                f"{name}: accepted mutant '{label}' sits in `Risk:` check {', '.join(sorted(ids & risk_ids))} "
                                f"- kill it with a test, or record it equivalent or arid"
                            )
                    survivors_recorded += 1

        survived = column(header, "survived")
        if survived is not None and column(header, "command") is not None:
            command = column(header, "command")
            for r in rows:
                if command >= len(r) or not usable_value(r[command]):
                    errors.append(f"{name}: mutation-run row names no command ({r[0][:40]})")
                count = r[survived].strip("` ") if survived < len(r) else ""
                if not count.isdigit():
                    errors.append(f"{name}: mutation-run Survived must be a count, got {count[:20]!r}")
                else:
                    survivors_run += int(count)

        unproven = column(header, "unproven")
        if unproven is not None:
            for r in rows:
                if unproven < len(r) and r[unproven].lower() not in EMPTY_CELL:
                    errors.append(f"{name}: PASS but Coverage leaves '{r[unproven][:50]}' unproven ({r[0][:40]})")

        contradiction = column(header, "contradiction")
        if contradiction is not None:
            for row in rows:
                if contradiction < len(row) and row[contradiction].lower() not in EMPTY_CELL:
                    errors.append(f"{name}: PASS but a binding source records a contradiction ({row[0][:50]})")

        uncovered = column(header, "uncovered")
        if uncovered is not None:
            for r in rows:
                if uncovered < len(r) and r[uncovered].lower() not in EMPTY_CELL:
                    errors.append(
                        f"{name}: PASS but a binding source leaves '{r[uncovered][:50]}' uncovered ({r[0][:40]})"
                    )

        met = column(header, "expectation met", "met")
        if met is not None:
            for r in rows:
                if met < len(r) and r[met] and UNMET_RE.search(r[met]):
                    errors.append(
                        f"{name}: PASS but a Test policy row is unmet ({r[0][:40]}: '{r[met][:40]}') "
                        f"- the rows priced work the checks do not name"
                    )

    if survivors_run > survivors_recorded:
        errors.append(
            f"{name}: PASS but the mutation run reports {survivors_run} survivor(s) and only "
            f"{survivors_recorded} carry an equivalent, arid or accepted disposition - kill or record each one"
        )

    # Faults run where a weak test costs most: the `Risk:` checks and any check the Verifier is unsure of,
    # one fault each, five at most. `Risk: none` with nothing unsure owes no fault row.
    owed = risk_ids | unsure if effective in ("standard", "ui") else set()
    missing = sorted(owed - fault_checks, key=lambda c: int(c[1:]))
    if owed and len(owed) - len(missing) < min(MAX_FAULTS, len(owed)):
        errors.append(
            f"{name}: no fault row names {', '.join(missing)} - inject at least one fault per `Risk:` check "
            f"and per `unsure` check (up to {MAX_FAULTS}) and put its check id in the Check column"
        )

    return errors, warnings


def _appears_complete(fdir):
    if os.path.exists(os.path.join(fdir, "verification.md")):
        return True
    checks = os.path.join(fdir, "checks.md")
    if not os.path.exists(checks):
        return False
    body = open(checks, encoding="utf-8", errors="replace").read()
    if not re.search(r"^\**\s*C\d+\s*\**\s*[-–—:]", body, re.MULTILINE):
        return False
    if re.search(r"^\s*-\s*\[\s\]", body, re.MULTILINE):
        return False
    return True


def _resolve(root, feature):
    base, dirs = _feature_dirs(root)
    # An explicit argument is answered on its own terms: "that feature is not here" beats
    # "there is no features directory", which is true but not what was asked.
    if feature:
        fdir = feature if os.path.isdir(feature) else os.path.join(base, feature)
        if not os.path.isdir(fdir):
            print(f"validate_verification: feature not found: {feature}", file=sys.stderr)
            raise SystemExit(2)
        return [(fdir, os.path.basename(fdir.rstrip("/")))]
    if not os.path.isdir(base):
        print(f"validate_verification: no {base} directory - nothing to check.")
        return []
    if len(dirs) == 1:
        return [(os.path.join(base, dirs[0]), dirs[0])]
    if not dirs:
        print("validate_verification: no features under .specs/features/ - nothing to check.")
        return []
    picked = [(os.path.join(base, d), d) for d in dirs if _appears_complete(os.path.join(base, d))]
    if not picked:
        print("validate_verification: no completed feature detected (all in progress) - nothing to gate.")
    return picked


def main(argv=None):
    p = argparse.ArgumentParser(
        prog="validate_verification.py",
        description="Completion gate: a done feature needs a real PASS report its own rows do not contradict.",
    )
    p.add_argument("feature", nargs="?", default=None, help="Feature dir or name")
    p.add_argument("--root", default=".", help="Project root containing .specs/ (default: current dir)")
    p.add_argument("--strict", action="store_true", help="Treat warnings as errors")
    p.add_argument("--allow-empty", action="store_true",
                   help="Exit 0 when there is no completed feature to gate (repo-wide sweeps)")
    args = p.parse_args(argv)
    root = os.path.abspath(args.root)

    targets = _resolve(root, args.feature)
    if not targets and not args.allow_empty:
        # Gating nothing is not a pass. This is the completion gate for a feature that was just
        # built, so an empty run means the report could not be found - which reads as green to
        # anything checking only the exit code. Exit 2 says "could not gate", like the other
        # validators do, and leaves 0 to mean a report was read and held up.
        print(
            "validate_verification: gated nothing - this is NOT a pass. Point it at the feature "
            "(validate_verification.py <feature> --root <project>), or pass --allow-empty if you "
            "meant to sweep a repo that has no completed feature yet.",
            file=sys.stderr,
        )
        return 2

    all_errors, all_warnings = [], []
    for fdir, name in targets:
        e, w = _check_feature(fdir, name)
        all_errors += e
        all_warnings += w

    for w in all_warnings:
        print(f"  WARN  {w}")
    for e in all_errors:
        print(f"  ERROR {e}")
    checked = ", ".join(name for _, name in targets) or "(none)"
    fail = all_errors or (all_warnings and args.strict)
    print(f"\nvalidate_verification: {len(all_errors)} error(s), {len(all_warnings)} warning(s) across [{checked}]")
    return 1 if fail else 0


if __name__ == "__main__":
    raise SystemExit(main())
