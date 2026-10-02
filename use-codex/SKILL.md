---
name: use-codex
description: Delegate a bounded task to the local `codex` CLI — a cross-model second opinion, a diff review, or a scoped implementation pass. Use when the user says to use Codex or GPT, names an OpenAI model, or asks a different model to check the work.
---

# Use Codex

Delegate to the local `codex` CLI in one of two roles: **advisor** (read-only
exploration and critique, the default) or **worker** (an authorized, scoped
implementation pass). Report what comes back as a second model's opinion, not as
a verdict.

## Workflow

1. Name the role and boundary in one sentence — advisor or worker, which paths,
   what output.
2. Write the prompt for a **cold** reader. The delegate starts with no
   conversation history: the prompt carries the paths, the constraints, and the
   exact question or task. What it does not say, Codex cannot know.
3. Run `scripts/ask_codex.py` **outside the sandbox**, with escalated
   permissions. `codex` authenticates from `~/.codex` and needs network; a
   sandboxed call sees neither and fails on auth even though the install is
   fine.
4. Run it from the directory Codex should read, or pass `--cwd`. It defaults to
   `--role advisor --effort medium` and the model in `~/.codex/config.toml`;
   pass `--model` or a different `--effort` through as the user said it.
   `--dry-run` prints the command without running it — it is sandbox-safe, and
   the fastest way to check the shape of a call before escalating.
5. Reach for `--review` when the task is a diff rather than a question: it runs
   Codex's own review mode over `--base <branch>`, `--commit <sha>`, or
   `--uncommitted`, and returns structured findings. Targeted review flags do
   not accept a custom prompt; use plain advisor mode when custom instructions
   are more important than native review mode.
6. Both roles carry the full toolset — shell, web search, MCP servers and
   plugins from `~/.codex/config.toml`, and Computer Use (on by default outside
   review mode; `--no-computer-use` drops it). Attach screenshots or mockups
   with `--image`. The role sets the sandbox: advisor is `read-only` and is
   told to change nothing; worker is `workspace-write` once the user has
   authorized writes. `--add-dir` reaches paths outside the working root.
7. **Auto-review** is the ceiling. Anything beyond the sandbox — network from
   the shell, an app's UI state — becomes an escalation that Codex's guardian
   reviewer approves or rejects against the prompt's stated scope. The wrapper
   never exposes `danger-full-access` or the bypass flag. So name every
   surface the delegate may touch in the prompt: "inspect the Simulator window
   for the login screen" gets approved where "check the frontmost app" gets
   rejected as reaching past the task.
8. Allow minutes, not seconds. `exec` blocks until Codex finishes, so run it
   with a long timeout or in the background — a medium-effort run routinely
   passes two minutes. The wrapper kills the run after `--timeout` seconds
   (default 900) and exits 124 naming the model and effort; raise it for long
   worker passes.
   The wrapper closes stdin because `codex exec` waits on an open stdin
   ("Reading additional input from stdin...") and hangs silently at ~0 CPU —
   a backgrounded shell never closes it. When calling `codex exec` directly,
   redirect `< /dev/null`. The non-interactive form is `codex exec "prompt"`;
   `codex -p` is `--profile`, a config profile name.
9. Report the result with the model and effort observed, plus the delegation's
   limits. Done when the bounded response is captured, or when the failure is
   reported with its cause and the primary task continues. An auth or
   credential error is first of all a sandbox symptom: re-run escalated before
   treating it as a broken login.

## Command patterns

```text
Advisor: scripts/ask_codex.py --prompt "Read src/auth/ and name the five riskiest assumptions in the token refresh path, each with a concrete failure."
UI advisor: scripts/ask_codex.py --image mock.png --prompt "Compare the running app's settings screen with mock.png and identify five interaction or hierarchy problems with screenshots as evidence."
Review:  scripts/ask_codex.py --review --base main
Worker:  scripts/ask_codex.py --role worker --prompt "Implement the scoped change in src/... and summarize the files changed."
UI worker: scripts/ask_codex.py --role worker --prompt "Exercise the changed flow in the running app, fix issues within src/..., and summarize the evidence and files changed."
```

`codex exec --help`, `codex exec review --help`, and
`scripts/ask_codex.py --help` are the source of truth for flags and models.
Review mode takes a narrower flag set than plain `exec`.
