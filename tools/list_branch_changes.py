#!/usr/bin/env python3
# version: 1.0
"""Utility for listing branch changes within a configurable time window."""

from __future__ import annotations

import argparse
import datetime as _dt
import subprocess
import sys
from typing import List


def parse_args(argv: List[str]) -> argparse.Namespace:
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description="List recent commits for a branch using git log."
    )
    parser.add_argument(
        "branch",
        nargs="?",
        default=None,
        help="Branch to inspect (defaults to current HEAD).",
    )
    parser.add_argument(
        "--days",
        type=int,
        default=0,
        help=(
            "Number of days in the past to include. "
            "0 means only today's commits."
        ),
    )
    parser.add_argument(
        "--since",
        default=None,
        help=(
            "Explicit since value understood by git log (overrides --days)."
        ),
    )
    parser.add_argument(
        "--max-count",
        type=int,
        default=None,
        help="Limit the number of commits listed.",
    )
    return parser.parse_args(argv)


def calculate_since(days: int) -> str:
    """Calculate the --since value for git log."""
    today = _dt.datetime.now().date()
    start_day = today - _dt.timedelta(days=days)
    return start_day.isoformat()


def build_git_command(branch: str | None, since: str, max_count: int | None) -> List[str]:
    """Build the git log command."""
    command = [
        "git",
        "log",
        "--pretty=format:%h %ad %an %s",
        "--date=short",
        f"--since={since}",
    ]
    if max_count is not None:
        command.append(f"--max-count={max_count}")
    if branch:
        command.append(branch)
    return command


def run_git_log(command: List[str]) -> subprocess.CompletedProcess[str]:
    """Run git log and return the completed process."""
    try:
        return subprocess.run(
            command,
            capture_output=True,
            text=True,
            check=False,
        )
    except FileNotFoundError as exc:
        raise SystemExit("git executable not found in PATH") from exc


def main(argv: List[str] | None = None) -> int:
    """Entry point for the CLI."""
    args = parse_args(argv or sys.argv[1:])
    since = args.since if args.since is not None else calculate_since(args.days)
    command = build_git_command(args.branch, since, args.max_count)

    result = run_git_log(command)
    if result.returncode != 0:
        sys.stderr.write(result.stderr)
        return result.returncode

    output = result.stdout.strip()
    if not output:
        print("Brak commitów w podanym zakresie.")
    else:
        print(output)
    return 0


if __name__ == "__main__":
    sys.exit(main())
