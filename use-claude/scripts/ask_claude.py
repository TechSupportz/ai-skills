#!/usr/bin/env python3
"""Run one bounded, non-interactive Claude Code delegation."""

import argparse
import json
import shutil
import subprocess
import sys
from pathlib import Path

EDIT_TOOLS = ("Edit", "Write", "NotebookEdit")
ADVISOR_GUIDANCE = (
    "You are a read-only advisor. Inspect freely: read files, run read-only commands, search the web, "
    "and use MCP or browser tools to gather evidence. Leave files, git state, and external systems "
    "unchanged; report what should change instead of changing it."
)


def build_command(args: argparse.Namespace) -> list[str]:
    """`--tools` and `--disallowedTools` are variadic, so each is passed as one
    comma-joined argument and always followed by another flag before the positional prompt."""
    command = ["claude", "--print", "--no-session-persistence", "--model", args.model, "--effort", args.effort]
    if args.tools is not None:
        command += ["--tools", args.tools]
    if args.role == "advisor":
        command += ["--disallowedTools", ",".join(EDIT_TOOLS), "--permission-mode", "auto",
                    "--append-system-prompt", ADVISOR_GUIDANCE]
    else:
        command += ["--permission-mode", args.permission_mode or "auto"]
    command.append("--chrome" if args.chrome else "--no-chrome")
    for directory in args.add_dir:
        command += ["--add-dir", str(directory)]
    command += ["--output-format", args.output_format, args.prompt]
    return command


def main() -> int:
    parser = argparse.ArgumentParser(description="Run a bounded Claude Code CLI delegation.")
    parser.add_argument("--prompt", required=True, help="The complete delegation prompt.")
    parser.add_argument("--model", default="opus", help="CLI model alias or full model name.")
    parser.add_argument("--effort", choices=("low", "medium", "high", "xhigh", "max"), default="medium")
    parser.add_argument("--role", choices=("advisor", "worker"), default="advisor")
    parser.add_argument("--permission-mode", choices=("acceptEdits", "auto", "manual", "dontAsk", "plan"))
    parser.add_argument("--tools", help="Comma-separated Claude tool names; defaults to Claude's full set. "
                                        "Advisor never receives the file-edit tools.")
    parser.add_argument("--chrome", action=argparse.BooleanOptionalAction, default=True,
                        help="Claude in Chrome integration (default on; needs the extension connected).")
    parser.add_argument("--add-dir", type=Path, nargs="*", default=[], help="Extra directories Claude may access.")
    parser.add_argument("--output-format", choices=("text", "json", "stream-json"), default="text")
    parser.add_argument("--cwd", type=Path, default=Path.cwd())
    parser.add_argument("--timeout", type=int, default=900,
                        help="Wall-clock limit in seconds before the Claude run is killed (default 900).")
    parser.add_argument("--dry-run", action="store_true", help="Print the command as JSON without executing it.")
    args = parser.parse_args()

    if args.timeout <= 0:
        parser.error("--timeout must be a positive number of seconds")
    if args.role == "advisor" and args.permission_mode is not None:
        parser.error("--permission-mode is worker-only")
    if args.role == "advisor" and args.tools is not None:
        requested_tools = {tool.strip() for tool in args.tools.split(",") if tool.strip()}
        if requested_tools & set(EDIT_TOOLS):
            parser.error(f"advisor --tools cannot include {', '.join(EDIT_TOOLS)}")

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

    # Close stdin so a backgrounded call never waits on input that will not come.
    try:
        completed = subprocess.run(command, cwd=args.cwd, text=True, capture_output=True,
                                   stdin=subprocess.DEVNULL, timeout=args.timeout)
    except subprocess.TimeoutExpired:
        print(f"claude timed out after {args.timeout}s (model={args.model}, effort={args.effort}); "
              "raise --timeout or narrow the prompt", file=sys.stderr)
        return 124
    if completed.stdout:
        print(completed.stdout, end="")
    if completed.returncode:
        if completed.stderr:
            print(completed.stderr, end="", file=sys.stderr)
        return completed.returncode
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
