#!/usr/bin/env python3
"""Run one bounded, non-interactive Codex delegation."""

import argparse
import json
import shutil
import subprocess
import sys
from pathlib import Path

SANDBOX_FOR_ROLE = {"advisor": "read-only", "worker": "workspace-write"}
# Approved escalations run outside the sandbox, so the advisor's read-only stance is restated in the prompt.
ADVISOR_GUIDANCE = (
    "You are a read-only advisor. Inspect freely: read files, run read-only commands, search the web, "
    "and use MCP, browser, or Computer Use tools to gather evidence. Leave files, git state, and external "
    "systems unchanged; report what should change instead of changing it. When a read-only command fails for lack of network or "
    "sandbox access, re-run it with escalated permissions; an automatic reviewer approves in-scope reads."
)
COMPUTER_USE_GUIDANCE = {
    "advisor": (
        "Computer Use is available for UI evidence gathering only. You may inspect app state, "
        "navigate, and scroll to reveal information, but do not type into controls, submit, change "
        "settings, or otherwise mutate external state. Prefer a dedicated connector or CLI when one "
        "can answer the question."
    ),
    "worker": (
        "Computer Use is available only for UI interactions within the authorized task. Prefer a "
        "dedicated connector or CLI when one can complete the work, and follow the installed Computer "
        "Use confirmation policy before consequential actions."
    ),
}


def build_command(args: argparse.Namespace) -> list[str]:
    """Codex `exec` and `exec review` accept different flags; review takes the narrower set."""
    sandbox = args.sandbox or SANDBOX_FOR_ROLE[args.role]
    command = ["codex", "exec"]
    if args.review:
        command.append("review")
    command += ["--ephemeral", "--skip-git-repo-check"]
    # Auto-review is the ceiling: escalations go to Codex's guardian reviewer, never to a bypass.
    command += ["-c", 'approval_policy="on-request"', "-c", 'approvals_reviewer="guardian_subagent"',
                "-c", f'model_reasoning_effort="{args.effort}"']
    if args.computer_use:
        command += ["--enable", "computer_use"]
    if args.model:
        command += ["--model", args.model]
    if args.review:
        command += ["-c", f'sandbox_mode="{sandbox}"']
        if args.base:
            command += ["--base", args.base]
        if args.commit:
            command += ["--commit", args.commit]
        if args.uncommitted:
            command.append("--uncommitted")
    else:
        command += ["--sandbox", sandbox, "--color", "never"]
        for directory in args.add_dir:
            command += ["--add-dir", str(directory)]
        for image in args.image:
            command.append(f"--image={image}")  # `--image` is variadic; the `=` form cannot swallow the prompt
    if args.json:
        command.append("--json")
    if args.prompt is not None:
        preamble = [ADVISOR_GUIDANCE] if args.role == "advisor" else []
        if args.computer_use:
            preamble.append(COMPUTER_USE_GUIDANCE[args.role])
        command.append("\n\n".join([*preamble, args.prompt]))
    return command


def main() -> int:
    parser = argparse.ArgumentParser(description="Run a bounded Codex CLI delegation.")
    parser.add_argument("--prompt", help="The complete delegation prompt; unavailable with a targeted review.")
    parser.add_argument("--model", help="Codex model name; omit to use the Codex config default.")
    parser.add_argument("--effort", choices=("minimal", "low", "medium", "high", "xhigh"), default="medium")
    parser.add_argument("--role", choices=("advisor", "worker"), default="advisor")
    parser.add_argument("--sandbox", choices=("read-only", "workspace-write"),
                        help="Override the sandbox the role implies.")
    parser.add_argument("--review", action="store_true", help="Use Codex's built-in diff review mode.")
    review_target = parser.add_mutually_exclusive_group()
    review_target.add_argument("--base", help="Review mode: base branch to diff against.")
    review_target.add_argument("--commit", help="Review mode: review one commit.")
    review_target.add_argument("--uncommitted", action="store_true", help="Review mode: review the working tree.")
    parser.add_argument("--add-dir", type=Path, nargs="*", default=[], help="Extra writable directories.")
    parser.add_argument("--computer-use", action=argparse.BooleanOptionalAction, default=None,
                        help="Codex Computer Use runtime (default on, except in review mode).")
    parser.add_argument("--image", type=Path, action="append", default=[],
                        help="Attach an image to the prompt (repeatable).")
    parser.add_argument("--json", action="store_true", help="Emit Codex events as JSONL.")
    parser.add_argument("--cwd", type=Path, default=Path.cwd())
    parser.add_argument("--timeout", type=int, default=900,
                        help="Wall-clock limit in seconds before the Codex run is killed (default 900).")
    parser.add_argument("--dry-run", action="store_true", help="Print the command as JSON without executing it.")
    args = parser.parse_args()

    targeted_review = args.base is not None or args.commit is not None or args.uncommitted
    if args.role == "advisor" and args.sandbox == "workspace-write":
        parser.error("advisor role is always read-only")
    if args.review and args.role != "advisor":
        parser.error("review mode is always read-only; omit --role worker")
    if targeted_review and not args.review:
        parser.error("--base, --commit, and --uncommitted require --review")
    if targeted_review and args.prompt is not None:
        parser.error("--prompt cannot be combined with a targeted review")
    if args.review and args.add_dir:
        parser.error("--add-dir is not supported by Codex review mode")
    if args.review and args.computer_use:
        parser.error("--computer-use is unavailable in Codex review mode; use plain advisor mode")
    if args.review and args.image:
        parser.error("--image is not supported by Codex review mode")
    if args.computer_use is None:
        args.computer_use = not args.review
    if not args.review and args.prompt is None:
        parser.error("--prompt is required unless --review is used")
    if args.timeout <= 0:
        parser.error("--timeout must be a positive number of seconds")

    if not shutil.which("codex"):
        print("codex executable not found on PATH", file=sys.stderr)
        return 127
    if not args.cwd.is_dir():
        print(f"working directory does not exist: {args.cwd}", file=sys.stderr)
        return 2

    command = build_command(args)
    if args.dry_run:
        print(json.dumps(command))
        return 0

    # `codex exec` reads extra input from an open stdin and blocks forever when
    # stdin never closes (e.g. a backgrounded Bash tool call), so close it.
    try:
        completed = subprocess.run(command, cwd=args.cwd, text=True, capture_output=True,
                                   stdin=subprocess.DEVNULL, timeout=args.timeout)
    except subprocess.TimeoutExpired:
        model = args.model or "config default"
        print(f"codex timed out after {args.timeout}s (model={model}, effort={args.effort}); "
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
