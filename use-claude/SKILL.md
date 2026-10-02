---
name: use-claude
description: Delegate a bounded task to the local `claude` CLI — a second opinion, a code or UI review, or a scoped implementation pass. Use when the user says to use Claude Code, names a Claude model such as Opus or Sonnet, or asks for a second pair of eyes on the work.
---

# Use Claude

Delegate to the local `claude` CLI in one of two roles: **advisor** (read-only
exploration and critique, the default) or **worker** (an authorized, scoped
implementation pass). Report what comes back as an outside opinion.

## Workflow

1. Name the role and boundary in one sentence — advisor or worker, which paths,
   what output.
2. Write the prompt for a **cold** reader. The delegate starts with no
   conversation history: the prompt carries the paths, the constraints, and the
   exact question or task. What it does not say, Claude cannot know.
3. Run `scripts/ask_claude.py` **outside the sandbox**, with escalated
   permissions. `claude` authenticates from the host keychain and needs network;
   a sandboxed call sees neither and fails on auth even though the install is
   fine.
4. Run it from the directory Claude should read, or pass `--cwd`. It defaults to
   `--role advisor --model opus --effort medium`; pass a different model alias
   or effort through as the user said it. `--dry-run` prints the command without
   running it — it is sandbox-safe, and the fastest way to check the shape of a
   call before escalating.
5. Both roles carry Claude's full toolset — Bash, web search and fetch, the
   user's MCP servers and plugins, and Claude in Chrome (`--chrome`, on by
   default; it needs the extension connected, and `--no-chrome` drops it).
   Images are read by path, so name screenshot files in the prompt. Advisor
   loses only the file-edit tools and is told to change nothing; worker keeps
   them. `--tools` narrows either set; `--add-dir` reaches paths outside the
   working root.
   **Auto-review** is the ceiling: both roles run in `auto` permission mode,
   where Claude's classifier approves or blocks each action against the
   prompt's stated scope. Worker may step down to `acceptEdits`, `dontAsk`, or
   `plan`; the wrapper never exposes the permission-bypass mode.
6. Allow minutes, not seconds. `--print` blocks until Claude finishes, so run it
   with a long timeout or in the background — an Opus run at medium effort
   routinely passes two minutes. The wrapper kills the run after `--timeout`
   seconds (default 900) and exits 124 naming the model and effort, and closes
   stdin so a backgrounded call cannot wait on input.
7. Report the result with the model and effort observed, plus the delegation's
   limits. Done when the bounded response is captured, or when the failure is
   reported with its cause and the primary task continues. An auth or credential
   error is first of all a sandbox symptom: re-run escalated before treating it
   as a broken login.

## Command patterns

```text
Advisor: scripts/ask_claude.py --prompt "Read src/auth/, run its tests, and review the token refresh path. Return five findings with fixes."
UI advisor: scripts/ask_claude.py --prompt "Open localhost:3000/settings in Chrome, compare it with design/settings.png, and list five hierarchy or interaction problems with evidence."
Worker:  scripts/ask_claude.py --role worker --tools Read,Edit --prompt "Implement the scoped change in src/... and summarize the files changed."
```

`claude --help` and `scripts/ask_claude.py --help` are the source of truth for
flags and aliases.
