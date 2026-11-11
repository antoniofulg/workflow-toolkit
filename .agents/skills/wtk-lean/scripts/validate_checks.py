#!/usr/bin/env python3
"""
validate_checks.py - deterministic gate for a feature checks.md, run before any code.

This is the omission catcher. The failure it exists to prevent is not a vague claim
(a human notices those) but a set member that was named in prose and never assigned a
proof: "dispatches over paused, updated, deleted and trial_will_end" reads perfectly
with one of the four missing, so nobody sees it, and that branch ships unproven.

The Coverage join makes that failure structural - every member is its own token beside
the check that proves it - and this script makes the join checkable: a row declaring a
set of 5 with 4 members assigned fails, loudly, before a line of code is written.

Pure standard library, zero dependencies. Operates only on the checks.md markdown
artifact - never on the target codebase - so it stays stack-agnostic - except with --execute,
which runs the `Build:` line once before any code is written.

The requirements and the solution's shape are not this file's business: both were
reviewed in plan.md and are gated by validate_plan.py. What this script owns is the
derivation from them, which is where omissions surface.

What it checks:
  ERROR  - no `## Approval` receipt with a non-empty `- Decision:` line (plan.md, else checks.md)
  ERROR  - no `Build:` line naming the repo's build, type check and lint command (or `none - <why>`)
  ERROR  - no `Profile:` line, or an unknown profile
  ERROR  - a required section is missing (Checks, Coverage, Swept)
  ERROR  - a check with no `Proof:` line
  ERROR  - a `run <name>` proof with no `Run <name>:` line, or with no pass line after `|`
  ERROR  - a duplicate check id
  ERROR  - no checks parsed at all
  ERROR  - a Coverage row with an empty member cell
  ERROR  - a Coverage row whose declared set size exceeds the members assigned
  ERROR  - a Coverage row with a non-empty `Unproven` cell
  ERROR  - a swept dimension missing, or its landing left blank
  ERROR  - an `n/a` swept landing with no reason after it
  ERROR  - a check id referenced in Coverage or Swept that is not defined
  WARN   - a route in plan.md's Surface that nothing here mentions
  WARN   - a proof that names no test selector (a whole suite settles no single claim; a `run`
           proof is exempt - its pass line is its selector)
  WARN   - a claim carrying a vague word instead of a concrete value
  WARN   - a Coverage row that declares no set size
  WARN   - a swept landing that is neither a check, `existing`, `n/a`, nor `Unresolved`
  WARN   - a blocking unresolved question still open
  WARN   - a `Test policy` section is absent under profile standard/ui
  ERROR  - with --execute, when nothing else failed: the `Build:` command is red before any change

Usage:
  python3 <skill-dir>/scripts/validate_checks.py [target] [--root DIR] [--strict] [--execute]

  Invoke from the skill directory that ships this script (not the project root).
  target    Path to a checks.md, a feature directory, a feature name, or a project root.
            Omitted -> auto-detect the single feature under <root>/.specs/features/.
  --root    Project root that contains .specs/ (default: current dir).
  --strict  Treat warnings as errors.
  --execute Before starting to build: also run the `Build:` line once, from --root.

Exit codes: 0 pass, 1 errors found (or warnings under --strict), 2 usage error.
"""

import argparse
import os
import re
import subprocess
import sys

from native_evidence import RUN_PROOF_RE, approval_errors, intent_errors, read_runs, unquote

PROFILES = ("light", "standard", "ui")
REQUIRED_SECTIONS = ["Checks", "Coverage", "Swept"]

PROFILE_RE = re.compile(r"^\**Profile\**\s*:\s*`?(\w+)`?", re.IGNORECASE)
BUILD_RE = re.compile(r"^\**\s*Build\s*\**\s*:\s*(.+)$", re.IGNORECASE)
CHECK_RE = re.compile(r"^\**\s*(C\d+)\s*\**\s*[-–—:]\s*(.+)$")
PROOF_RE = re.compile(r"^\**\s*Proof\s*\**\s*:\s*(.+)$", re.IGNORECASE)
CID_RE = re.compile(r"\bC\d+\b")
PLACEHOLDER_RE = re.compile(r"^\s*[\[<].+[\]>]\s*$")
SIZE_RE = re.compile(r"\((\d+)\s*(?:[a-z\- ]+)?\)")
HTTP_ROUTE_RE = re.compile(r"\b(?:GET|POST|PUT|PATCH|DELETE|HEAD|OPTIONS)\s+(/[A-Za-z0-9_\-/:{}.]*)")
CODE_SPAN_RE = re.compile(r"`([^`]+)`")
TABLE_DRIVEN_RE = re.compile(r"table[- ]driven", re.IGNORECASE)

SELECTOR_TOKENS = (
    "-n ", "-k ", "-t ", "-e ", "--name", "--only", "--example", "--filter",
    "--testnamepattern", "--test-name", "--run", "-dtest=", "-run ", "::", "#",
    "--grep", "-g ", "--spec",
)

VAGUE_RE = re.compile(
    r"\b(gracefully|properly|correctly|quickly|fast|slow|efficiently|reasonably|"
    r"appropriately|as expected|user-friendly|robust|works)\b",
    re.IGNORECASE,
)

# canonical name -> alternative spellings accepted in the Swept list
DIMENSIONS = {
    "validation": ("validation", "validation and bounds", "input validation"),
    "failure modes": ("failure modes", "failure", "failure and partial failure", "partial failure"),
    "idempotency": ("idempotency", "idempotency and retry", "idempotency, retry, duplicates", "retry"),
    "authorization": ("authorization", "authorisation", "auth", "authorization and rate limits"),
    "concurrency": ("concurrency", "concurrency and ordering", "ordering"),
    "data lifecycle": ("data lifecycle", "lifecycle", "data retention"),
    "dependency failure": (
        "dependency failure", "external-dependency failure", "external dependency failure",
        "external dependency",
    ),
    "state transitions": ("state transitions", "transitions", "state-transition integrity"),
    "observability": ("observability", "logging and metrics", "telemetry"),
    "deploy compatibility": (
        "deploy compatibility", "deploy compatibility / rollback", "deploy compatibility and rollback", "rollback",
    ),
    "performance budget": ("performance budget", "performance"),
}


def resolve_checks(target, root):
    if target:
        if os.path.isfile(target):
            return target
        if os.path.isdir(target):
            cand = os.path.join(target, "checks.md")
            if os.path.isfile(cand):
                return cand
            return _autodetect(target)
        cand = os.path.join(root, ".specs", "features", target, "checks.md")
        if os.path.isfile(cand):
            return cand
        return None
    return _autodetect(root)


def _autodetect(root):
    base = os.path.join(root, ".specs", "features")
    if not os.path.isdir(base):
        return None
    features = [
        d for d in sorted(os.listdir(base))
        if os.path.isfile(os.path.join(base, d, "checks.md"))
    ]
    if len(features) == 1:
        return os.path.join(base, features[0], "checks.md")
    if len(features) == 0:
        return None
    raise SystemExit(
        "validate_checks: multiple features found; pass one explicitly:\n  "
        + "\n  ".join(os.path.join(base, f, "checks.md") for f in features)
    )


def read_build(lines):
    """The first `Build:` line's command text outside fenced blocks, else None."""
    for ln in lines:
        m = BUILD_RE.match(ln.strip())
        if m:
            return unquote(m.group(1))
    return None


def split_row(line):
    return [c.strip() for c in line.strip().strip("|").split("|")]


def is_separator(line):
    return bool(re.match(r"^\s*\|?[\s:|-]+\|?\s*$", line)) and "-" in line


def section_bounds(lines, name):
    pattern = re.compile(r"^#{1,4}\s+" + re.escape(name) + r"\b.*$", re.IGNORECASE)
    start = None
    for i, ln in enumerate(lines):
        if pattern.match(ln.strip()):
            start = i + 1
            break
    if start is None:
        return None
    end = len(lines)
    for j in range(start, len(lines)):
        if re.match(r"^#{1,2}\s+\S", lines[j]):  # only a top-level heading closes it
            end = j
            break
    return (start, end)


def table_rows(lines, bounds):
    """Data rows of the first contiguous markdown table inside a section."""
    if not bounds:
        return []
    rows, started = [], False
    for i in range(*bounds):
        stripped = lines[i].strip()
        if stripped.startswith("|"):
            started = True
            rows.append(stripped)
        elif started and stripped == "":
            continue
        elif started:
            break
    data = [r for r in rows if not is_separator(r)]
    return data[1:] if data else []


def strip_fences(lines):
    """Drop fenced code blocks so a template example inside the file is not parsed."""
    out, in_fence = [], False
    for ln in lines:
        if ln.strip().startswith("```"):
            in_fence = not in_fence
            out.append("")
            continue
        out.append("" if in_fence else ln)
    return out


def parse_checks(lines):
    """Return (checks: dict id -> {'claim', 'proofs', 'line'}, duplicates: list)."""
    checks, duplicates = {}, []
    current = None
    for i, ln in enumerate(lines, start=1):
        stripped = ln.strip()
        m = CHECK_RE.match(stripped)
        if m and not stripped.startswith("|"):
            cid = m.group(1).upper()
            if cid in checks:
                duplicates.append((cid, i))
                current = None
                continue
            checks[cid] = {"claim": m.group(2).strip(), "proofs": [], "line": i}
            current = cid
            continue
        if re.match(r"^#{1,2}\s+\S", ln):
            current = None
        if current:
            pm = PROOF_RE.match(stripped)
            if pm:
                checks[current]["proofs"].append(pm.group(1).strip())
    return checks, duplicates


def count_members(cell):
    """Count member tokens that carry a check id. Members are separated by '·' or ';'."""
    parts = re.split(r"[·;]", cell)
    return sum(1 for p in parts if CID_RE.search(p))


def plan_interfaces(checks_path):
    """Interfaces named in the sibling plan.md's Surface table: an HTTP route's path, else the
    first code span - a CLI verb, an exported symbol or an event topic."""
    plan = os.path.join(os.path.dirname(os.path.abspath(checks_path)), "plan.md")
    if not os.path.isfile(plan):
        return []
    with open(plan, "r", encoding="utf-8") as f:
        lines = strip_fences(f.read().splitlines())
    bounds = section_bounds(lines, "Surface")
    interfaces = []
    for r in table_rows(lines, bounds):
        cells = split_row(r)
        if not cells or not cells[0] or PLACEHOLDER_RE.match(cells[0]):
            continue
        m = HTTP_ROUTE_RE.search(cells[0]) or CODE_SPAN_RE.search(cells[0])
        interfaces.append(m.group(1).strip() if m else cells[0].strip())
    return interfaces


def check_file(path):
    with open(path, "r", encoding="utf-8") as f:
        raw = f.read().splitlines()
    lines = strip_fences(raw)
    errors, warnings = intent_errors(path) + approval_errors(path), []

    # Profile.
    profile = None
    for ln in lines:
        m = PROFILE_RE.match(ln.strip())
        if m:
            profile = m.group(1).lower()
            break
    if profile is None:
        errors.append("no `Profile:` line - the verification report has to name the profile in force")
    elif profile not in PROFILES:
        errors.append(f"unknown profile '{profile}' (expected one of: {', '.join(PROFILES)})")

    # Build preflight.
    build = read_build(lines)
    if build is None:
        errors.append(
            "no `Build:` line - name the repo's build, type check and lint command (or `Build: none - <why>`); "
            "a green test suite does not show the code compiles"
        )
    elif build.lower().startswith("none") and len(build[4:].strip(" -–—:")) < 3:
        errors.append("`Build: none` with no reason - say why the repo has no build, type check or lint")

    # Sections.
    for name in REQUIRED_SECTIONS:
        if section_bounds(lines, name) is None:
            errors.append(f"missing required section: ## {name}")
    if profile in ("standard", "ui") and section_bounds(lines, "Test policy") is None:
        warnings.append(
            f"profile is {profile} but there is no ## Test policy section - confirm the repo already "
            "answers which level proves each layer and how deeply"
        )

    # Checks.
    checks, duplicates = parse_checks(lines)
    for cid, line_no in duplicates:
        errors.append(f"L{line_no}: duplicate check id {cid} - ids are referenced downstream and must be unique")
    if not checks:
        errors.append("no checks parsed - expected lines shaped `**C1** - <claim>` followed by `Proof: <command>`")
        return errors, warnings, profile

    runs = read_runs(lines)
    for cid, c in sorted(checks.items(), key=lambda kv: int(kv[0][1:])):
        if not c["proofs"]:
            errors.append(f"{cid} has no `Proof:` line - no proof, no check (L{c['line']})")
        for pr in c["proofs"]:
            low = pr.lower()
            text = unquote(pr)
            run = RUN_PROOF_RE.match(text) or re.match(r"^run\s+([\w-]+)\s*$", text, re.IGNORECASE)
            if run and (run.re is RUN_PROOF_RE or run[1] in runs):
                if run[1] not in runs:
                    errors.append(f"{cid}: proof reads `run {run[1]}` and no `Run {run[1]}: <command>` line defines it (L{c['line']})")
                if run.re is not RUN_PROOF_RE or not run[2].strip():
                    errors.append(f"{cid}: `run {run[1]}` names no pass line after `|` - copy the line the run prints when this test passes (L{c['line']})")
                continue
            if not any(tok in low for tok in SELECTOR_TOKENS):
                warnings.append(
                    f"{cid}: proof names no test selector, so it may be a whole suite - "
                    f"a suite going green settles no single claim: {pr[:60]}"
                )
        vague = VAGUE_RE.search(c["claim"])
        if vague:
            warnings.append(f"{cid}: claim uses '{vague.group(0)}' instead of a concrete value")

    referenced = set()

    # Coverage join.
    cov = section_bounds(lines, "Coverage")
    rows = table_rows(lines, cov)
    if cov and not rows:
        warnings.append("Coverage section has no rows - state 'no set rows' explicitly if nothing enumerates")
    for r in rows:
        cells = split_row(r)
        if len(cells) < 2:
            continue
        set_cell, member_cell = cells[0], cells[1]
        unproven = cells[2] if len(cells) > 2 else ""
        if not set_cell or PLACEHOLDER_RE.match(set_cell):
            continue
        label = set_cell[:48]
        if not member_cell or PLACEHOLDER_RE.match(member_cell) or member_cell == "-":
            errors.append(f"Coverage '{label}': empty member cell - every member needs its own token and a check")
            continue
        referenced |= {c.upper() for c in CID_RE.findall(member_cell)}
        sm = SIZE_RE.search(set_cell)
        if not sm:
            warnings.append(f"Coverage '{label}': declares no set size - write it as '(N)' so the join is checkable")
        else:
            declared = int(sm.group(1))
            if TABLE_DRIVEN_RE.search(member_cell) and str(declared) in member_cell:
                pass  # the enumeration lives in the test
            else:
                assigned = count_members(member_cell)
                if assigned < declared:
                    errors.append(
                        f"Coverage '{label}': declares {declared} members but only {assigned} carry a check "
                        f"- the unassigned member is the one that ships unproven"
                    )
        if unproven and unproven not in ("-", "—") and not PLACEHOLDER_RE.match(unproven):
            errors.append(f"Coverage '{label}': Unproven is '{unproven[:40]}' - a member with no proof is a gap")

    # Swept.
    swept = section_bounds(lines, "Swept")
    if swept:
        found = {}
        for i in range(*swept):
            m = re.match(r"^\s*[-*]\s*\**([^:*]+?)\**\s*:\s*(.*)$", lines[i])
            if not m:
                continue
            key = m.group(1).strip().lower()
            landing = m.group(2).strip()
            for canon, aliases in DIMENSIONS.items():
                if key in aliases:
                    found[canon] = (landing, i + 1)
                    break
        for canon in DIMENSIONS:
            if canon not in found:
                errors.append(f"Swept: dimension '{canon}' has no line - all eleven, every time")
                continue
            landing, line_no = found[canon]
            if not landing or PLACEHOLDER_RE.match(landing):
                errors.append(f"Swept '{canon}' (L{line_no}): landing is blank - a criterion, `existing`, or `n/a - <reason>`")
                continue
            low = landing.lower()
            if CID_RE.search(landing):
                referenced |= {c.upper() for c in CID_RE.findall(landing)}
            elif low.startswith("n/a") or low.startswith("not in scope"):
                rest = re.sub(r"^(n/a|not in scope)\b", "", low).strip(" -–—:")
                if len(rest) < 3:
                    errors.append(f"Swept '{canon}' (L{line_no}): `n/a` with no reason - say why it does not apply")
            elif low.startswith("existing"):
                rest = landing[len("existing"):].strip(" -–—:")
                if len(rest) < 3:
                    errors.append(f"Swept '{canon}' (L{line_no}): `existing` with no named guard or constraint")
            elif low.startswith("unresolved") or low.startswith("open"):
                warnings.append(f"Swept '{canon}' (L{line_no}): still Unresolved - confirm it does not block")
            else:
                warnings.append(
                    f"Swept '{canon}' (L{line_no}): landing '{landing[:40]}' is not a check, `existing`, "
                    f"`n/a`, or `Unresolved`"
                )

    # Dangling references.
    for cid in sorted(referenced - set(checks), key=lambda c: int(c[1:])):
        errors.append(f"{cid} is referenced in Coverage or Swept but is not defined in ## Checks")

    # The derivation. checks.md is derived from plan.md, so an interface reviewed there with
    # nothing pointing back at it here is either dead or unproven - and the plan naming it
    # is what makes it look covered.
    for interface in plan_interfaces(path):
        if interface not in "\n".join(lines):
            warnings.append(
                f"plan.md's Surface names `{interface}` but nothing here mentions it - its outcomes "
                f"owe a Coverage row, or the interface is dead"
            )

    # Blocking questions.
    for i, ln in enumerate(lines, start=1):
        if ln.strip().startswith("|") and re.search(r"\|\s*blocks\s*\|", ln, re.IGNORECASE):
            warnings.append(f"L{i}: an unresolved question is marked `blocks` - it cannot be settled while building")

    return errors, warnings, profile


def red_build(path, root):
    """The `Build:` command run once from `root`; an error message when it exits non-zero."""
    with open(path, "r", encoding="utf-8") as f:
        build = read_build(strip_fences(f.read().splitlines()))
    if not build or build.lower().startswith("none"):
        return []
    proc = subprocess.run(build, shell=True, cwd=root, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                          text=True, errors="replace")
    if proc.returncode == 0:
        return []
    last = next(iter(reversed(proc.stdout.strip().splitlines())), "")
    return [
        f"the build was red before any change: `{build}` exit {proc.returncode} - {last.strip()[:100]}. "
        f"Tell the user and stop; the feature must not inherit a failing baseline"
    ]


def main(argv=None):
    p = argparse.ArgumentParser(
        prog="validate_checks.py",
        description="Pre-build gate for a feature checks.md: proofs, the coverage join, the sweep.",
    )
    p.add_argument("target", nargs="?", default=None)
    p.add_argument("--root", default=".")
    p.add_argument("--strict", action="store_true")
    p.add_argument("--execute", action="store_true", help="Before starting to build: also run the Build line once")
    args = p.parse_args(argv)

    path = resolve_checks(args.target, args.root)
    if not path:
        print(
            "validate_checks: could not locate a checks.md. Pass a path or run from the project root.",
            file=sys.stderr,
        )
        return 2

    errors, warnings, profile = check_file(path)
    if args.execute and not errors:
        errors += red_build(path, os.path.abspath(args.root))
    for w in warnings:
        print(f"  WARN  {w}")
    for e in errors:
        print(f"  ERROR {e}")
    fail = errors or (warnings and args.strict)
    print(f"\nvalidate_checks: {len(errors)} error(s), {len(warnings)} warning(s) in {path} [profile: {profile or 'none'}]")
    return 1 if fail else 0


if __name__ == "__main__":
    raise SystemExit(main())
