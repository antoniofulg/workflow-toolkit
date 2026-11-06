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

Usage:
  python3 <skill-dir>/scripts/check_commit.py [msgfile]
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


def main(argv=None):
    p = argparse.ArgumentParser(prog="check_commit.py", description="Validate a Conventional Commits message.")
    p.add_argument("msgfile", nargs="?", default=None,
                   help="a commit message file (as git passes to commit-msg), or the message itself")
    p.add_argument("--message", default=None, help="the commit message as a string")
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
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
