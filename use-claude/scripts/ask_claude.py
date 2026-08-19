#!/usr/bin/env python3
"""Run one bounded, non-interactive Claude Code delegation."""

import argparse
import json
import shutil
import subprocess
import sys
from pathlib import Path


def build_command(args: argparse.Namespace) -> list[str]:
    command = ["claude", "--print", "--no-session-persistence", "--model", args.model, "--effort", args.effort]
    if args.role == "advisor":
        command += ["--tools", ""]
    else:
        if args.permission_mode:
            command += ["--permission-mode", args.permission_mode]
        if args.tools:
            command += ["--tools", *args.tools]
    command += ["--output-format", args.output_format, args.prompt]
    return command


def main() -> int:
    parser = argparse.ArgumentParser(description="Run a bounded Claude Code CLI delegation.")
    parser.add_argument("--prompt", required=True, help="The complete delegation prompt.")
    parser.add_argument("--model", default="opus", help="CLI model alias or full model name.")
    parser.add_argument("--effort", choices=("low", "medium", "high", "xhigh", "max"), default="medium")
    parser.add_argument("--role", choices=("advisor", "worker"), default="advisor")
    parser.add_argument("--permission-mode", choices=("acceptEdits", "auto", "manual", "dontAsk", "plan"))
    parser.add_argument("--tools", nargs="*", help="Worker-only Claude tool names; omit to use Claude defaults.")
    parser.add_argument("--output-format", choices=("text", "json", "stream-json"), default="text")
    parser.add_argument("--cwd", type=Path, default=Path.cwd())
    parser.add_argument("--dry-run", action="store_true", help="Print the command as JSON without executing it.")
    args = parser.parse_args()

    if not shutil.which("claude"):
        print("claude executable not found on PATH", file=sys.stderr)
        return 127
    if not args.cwd.is_dir():
        print(f"working directory does not exist: {args.cwd}", file=sys.stderr)
        return 2

    command = build_command(args)
    if args.dry_run:
        print(json.dumps(command))
        return 0

    completed = subprocess.run(command, cwd=args.cwd, text=True, capture_output=True)
    if completed.stdout:
        print(completed.stdout, end="")
    if completed.returncode:
        if completed.stderr:
            print(completed.stderr, end="", file=sys.stderr)
        return completed.returncode
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
