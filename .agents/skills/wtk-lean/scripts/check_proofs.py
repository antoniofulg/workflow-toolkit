#!/usr/bin/env python3
"""
check_proofs.py - run every proof checks.md names once, as the project runs it, and write proofs.md.

The mechanical half of verification: did each named test run, and pass, at HEAD. A model doing this
by hand spends most of the Verifier's time on it and gets it less right than a script, so the
Verifier reads proofs.md and spends its time judging what each test asserts.

It knows no test runner. A proof is the project's own command, run as written:

  Run unit: `npx vitest run src/billing --reporter=verbose`   one command, run once
  Proof: run unit | ✓ failed charge suspends                  the line the run must print
  Proof: `bin/rails test test/billing/dunning_test.rb`         run alone, judged by its exit code

A `run` proof passes when every word after `|` appears, in that order, on one ANSI-stripped line of
the run's output. The words carry the runner's pass marker, so a filter that selects nothing, or a
test that was renamed, reads `no test ran` instead of a green exit code. Commands run one at a time,
each once, with no timeout: a run's own parallelism is whatever the project configured for it.

A dirty working tree (outside `.specs/`) exits 1 before any command runs: the proofs would describe
the working tree, not HEAD.

Usage:
  python3 <skill-dir>/scripts/check_proofs.py <feature> [--root DIR]

Writes .specs/features/<feature>/proofs.md. Exit 0 every proof passed on a clean tree, 1 a proof
failed, no test ran, or the tree is dirty, 2 the feature could not be resolved.
"""

import argparse
import os
import re
import subprocess
import sys

from native_evidence import RUN_PROOF_RE, read_runs, unquote, unfenced_lines
from validate_checks import parse_checks

ANSI_RE = re.compile(r"\x1b\[[0-9;?]*[ -/]*[@-~]")
TAIL = 15
WIDTH = 100


def run(root, command):
    """(exit code, output with ANSI codes stripped), stderr interleaved with stdout."""
    proc = subprocess.run(
        command, shell=True, cwd=root, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
        text=True, errors="replace",
    )
    return proc.returncode, ANSI_RE.sub("", proc.stdout)


def matching_line(output, expected):
    """The first output line holding every word of `expected`, in order; None when no line does."""
    words = expected.split()
    if not words:
        return None
    pattern = re.compile(".*?".join(re.escape(word) for word in words))
    return next((line for line in output.splitlines() if pattern.search(line)), None)


def dirty_paths(root):
    """Uncommitted paths outside .specs/: the proofs would run on the working tree, not on HEAD."""
    proc = subprocess.run(["git", "status", "--porcelain"], cwd=root, capture_output=True, text=True)
    if proc.returncode != 0:
        return []
    return [ln[3:] for ln in proc.stdout.splitlines() if ln[3:] and not ln[3:].startswith(".specs/")]


def git_head(root):
    proc = subprocess.run(["git", "rev-parse", "--short", "HEAD"], cwd=root, capture_output=True, text=True)
    return proc.stdout.strip() if proc.returncode == 0 else "unknown"


def cell(text, width=WIDTH):
    return text.replace("|", "/").replace("`", "").strip()[:width]


def tail(output):
    # a fence inside the output would close the block proofs.md puts it in
    return [ln.replace("```", "'''") for ln in output.strip().splitlines()[-TAIL:]] or ["(no output)"]


def main(argv=None):
    ap = argparse.ArgumentParser(prog="check_proofs.py", description="Run every proof checks.md names once.")
    ap.add_argument("feature")
    ap.add_argument("--root", default=".")
    args = ap.parse_args(argv)
    root = os.path.abspath(args.root)
    fdir = os.path.join(root, ".specs", "features", args.feature)
    checks_path = os.path.join(fdir, "checks.md")
    if not os.path.isfile(checks_path):
        print(f"check_proofs: no checks.md under {fdir}", file=sys.stderr)
        return 2
    with open(checks_path, encoding="utf-8") as source:
        lines = unfenced_lines(source.read())
    checks, _duplicates = parse_checks(lines)
    runs = read_runs(lines)

    dirty = dirty_paths(root)
    if dirty:
        print("check_proofs: the working tree is dirty, so no proof ran - commit or stash first: "
              + ", ".join(dirty[:5]), file=sys.stderr)
        return 1

    # Each command runs once, in the order a check first names it.
    commands = []  # (label, command, is a Run group)
    for check in checks.values():
        for proof in check["proofs"]:
            text = unquote(proof)
            match = RUN_PROOF_RE.match(text)
            command = runs.get(match[1]) if match else text
            label = f"Run {match[1]}" if match else None
            if command and command not in (c for _, c, _ in commands):
                commands.append((label or cell(command), command, bool(match)))
    results = {command: run(root, command) for _, command, _ in commands}

    rows = []  # (check id, proof text, result, line)
    for cid, check in checks.items():
        for proof in check["proofs"]:
            text = unquote(proof)
            match = RUN_PROOF_RE.match(text)
            if match and match[1] not in runs:
                rows.append((cid, text, "fail", f"no `Run {match[1]}:` line"))
            elif match:
                code, output = results[runs[match[1]]]
                line = matching_line(output, match[2])
                rows.append((cid, text, "pass" if line else "no test ran", (line or "").strip()))
            else:
                code, _ = results[text]
                rows.append((cid, text, "pass" if code == 0 else "fail", f"exit {code}"))
    for label, command, is_run in commands:
        code, _ = results[command]
        if is_run and code:
            rows.append((label, command, "fail", f"exit {code}"))
    failed = sum(1 for _, _, result, _ in rows if result != "pass")

    out = [f"# {args.feature} proofs", "",
           f"**HEAD**: {git_head(root)}",
           "**Shell**: /bin/sh",
           f"**Result**: {len(rows) - failed} pass, {failed} fail", "",
           "| Proof | Result | Line |", "| --- | --- | --- |"]
    out += [f"| {cid}: {cell(text)} | {result} | {cell(line)} |" for cid, text, result, line in rows]
    out += ["", "## Output", ""]
    for label, command, _ in commands:
        code, output = results[command]
        out += [f"`{cell(label)}` - exit {code}", "", "```", *tail(output), "```", ""]
    with open(os.path.join(fdir, "proofs.md"), "w", encoding="utf-8") as target:
        target.write("\n".join(out).rstrip() + "\n")
    print("\n".join(out[2:5]))
    for cid, text, result, line in rows:
        if result != "pass":
            print(f"  {cid}: {result} - {cell(text, 80)}")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
