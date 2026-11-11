#!/usr/bin/env python3
"""
check_commit.py - deterministic Conventional Commits validation.

The per-task atomic-commit rule mandates Conventional Commits 1.0.0. This makes
that rule checkable instead of trusting the model to remember the format. Pure
standard library, zero dependencies, agent-agnostic.

It reads the message from (in priority order): a positional file path, --message,
or stdin. The file-path form matches how git passes the message file to a
`commit-msg` hook, so this doubles as an optional git-level guard WITHOUT
coupling the skill to any AI agent:

    hook="$(git rev-parse --git-path hooks)/commit-msg"
    ln -sf "$(pwd)/<skill-dir>/scripts/check_commit.py" "$hook" && chmod +x "$hook"

What it checks:
  ERROR  - header does not match  type(scope)!: description
  ERROR  - type is not one of the allowed Conventional Commits types (`chore` is not one)
  ERROR  - description is empty, starts uppercase, or ends with a period
  WARN   - header longer than 72 characters

After a passing message it prints, for each feature under `<root>/.specs/features/` that has a
checks.md and no verification.md, what the feature still owes: a command's output reaches the agent
after a compaction, where a rule it read hours earlier may not.

Usage:
  python3 <skill-dir>/scripts/check_commit.py [msgfile] [--root DIR]
  python3 <skill-dir>/scripts/check_commit.py --message "feat(auth): add email validation"
  echo "fix(cart): prevent negative quantity" | python3 <skill-dir>/scripts/check_commit.py

Exit codes: 0 pass, 1 violation, 2 usage error.
"""

import argparse
import os
import re
import sys

# Keep in step with the Types table in wtk/references/git.md.
TYPES = ["feat", "fix", "refactor", "perf", "docs", "test", "build", "ci"]
HEADER_RE = re.compile(r"^(?P<type>\w+)(?:\((?P<scope>[^)]+)\))?(?P<bang>!)?: (?P<desc>.+)$")
CAPTURE_RE = re.compile(r"`([^`\s]+\.(?:png|jpe?g|webp|gif))`", re.IGNORECASE)


def read_message(args):
    if args.message is not None:
        return args.message
    if args.msgfile:
        # git passes a path that exists. Anything else is the message itself, which is how a
        # caller invokes this by hand - a traceback there is a worse answer than the check.
        if os.path.isfile(args.msgfile):
            with open(args.msgfile, "r", encoding="utf-8") as f:
                return f.read()
        return args.msgfile
    if not sys.stdin.isatty():
        return sys.stdin.read()
    return ""


def check(message):
    errors, warnings = [], []
    # Ignore comment lines (git puts '#' comments in the message file).
    lines = [ln for ln in message.splitlines() if not ln.lstrip().startswith("#")]
    # Trim leading blank lines.
    while lines and not lines[0].strip():
        lines.pop(0)
    if not lines:
        return (["empty commit message"], warnings)

    header = lines[0].rstrip()
    if len(header) > 72:
        warnings.append(f"header is {len(header)} chars (>72): {header[:60]}...")

    m = HEADER_RE.match(header)
    if not m:
        errors.append(f"header does not match 'type(scope): description': {header!r}")
        return (errors, warnings)

    ctype = m.group("type")
    desc = m.group("desc")

    if ctype not in TYPES:
        errors.append(f"type '{ctype}' is not one of: {', '.join(TYPES)}")
    if not desc.strip():
        errors.append("description is empty")
    else:
        if desc[:1].isupper():
            errors.append(f"description should start lowercase: '{desc[:30]}'")
        if desc.rstrip().endswith("."):
            errors.append("description should not end with a period")

    return (errors, warnings)


def cites_capture(plan_path):
    """True when a numbered criterion under plan.md's `## Criteria` cites a binding capture image."""
    if not os.path.isfile(plan_path):
        return False
    inside = False
    with open(plan_path, "r", encoding="utf-8", errors="replace") as f:
        for ln in f:
            if re.match(r"^#{1,2}\s+\S", ln):
                inside = re.match(r"^#{1,2}\s+Criteria\b", ln, re.IGNORECASE) is not None
            elif inside and re.match(r"^\s*\d+\.\s", ln):
                if any(not c.endswith(".running.png") for c in CAPTURE_RE.findall(ln)):
                    return True
    return False


def owed(root):
    """One line per feature that has checks.md and no verification.md: what it still owes."""
    base = os.path.join(root, ".specs", "features")
    if not os.path.isdir(base):
        return []
    lines = []
    for name in sorted(os.listdir(base)):
        fdir = os.path.join(base, name)
        if not os.path.isfile(os.path.join(fdir, "checks.md")) or os.path.exists(os.path.join(fdir, "verification.md")):
            continue
        judge = " and the screens judge" if cites_capture(os.path.join(fdir, "plan.md")) else ""
        lines.append(
            f"  OWED  {name}: run check_proofs.py {name}, then dispatch the fresh Verifier{judge}; "
            f"done when validate_verification.py {name} exits 0"
        )
    return lines


def main(argv=None):
    p = argparse.ArgumentParser(prog="check_commit.py", description="Validate a Conventional Commits message.")
    p.add_argument("msgfile", nargs="?", default=None,
                   help="a commit message file (as git passes to commit-msg), or the message itself")
    p.add_argument("--message", default=None, help="the commit message as a string")
    p.add_argument("--root", default=".", help="project root that contains .specs/ (default: current dir)")
    args = p.parse_args(argv)

    message = read_message(args)
    if not message.strip():
        print("check_commit: no message provided (pass a file, --message, or pipe via stdin).", file=sys.stderr)
        return 2

    errors, warnings = check(message)
    for w in warnings:
        print(f"  WARN  {w}")
    for e in errors:
        print(f"  ERROR {e}")
    if errors:
        print("\ncheck_commit: FAIL - see https://www.conventionalcommits.org/en/v1.0.0/")
        return 1
    print("check_commit: OK")
    for line in owed(args.root):
        print(line)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
