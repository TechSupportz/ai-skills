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
6. Advisor still reads the repo — the sandbox is `read-only`, so Codex explores
   files and runs read-only commands but writes nothing. Worker raises that to
   `workspace-write` once the user has authorized writes; both roles run
   automatically inside their sandbox, and the wrapper never exposes
   `danger-full-access`. Add `--add-dir` only for paths outside the working root
   that the scope actually needs.
7. Add `--computer-use` when the task needs evidence from, or authorized
   interaction with, a Mac app. It explicitly enables Codex's stable
   `computer_use` feature and relies on the bundled Computer Use plugin/runtime
   already being installed; the wrapper does not install or configure it.
   Advisor may inspect and navigate UI but does not type, submit, change
   settings, or mutate external state. Worker may interact within the authorized
   task and follows the installed Computer Use confirmation policy. Prefer a
   dedicated connector or CLI when it can complete the task. Native review mode
   does not support Computer Use; use plain advisor mode for UI review.
8. Allow minutes, not seconds. `exec` blocks until Codex finishes, so run it
   with a long timeout or in the background — a medium-effort run routinely
   passes two minutes.
9. Report the result with the model and effort observed, plus the delegation's
   limits. Done when the bounded response is captured, or when the failure is
   reported with its cause and the primary task continues. An auth or
   credential error is first of all a sandbox symptom: re-run escalated before
   treating it as a broken login.

## Command patterns

```text
Advisor: scripts/ask_codex.py --prompt "Read src/auth/ and name the five riskiest assumptions in the token refresh path, each with a concrete failure."
UI advisor: scripts/ask_codex.py --computer-use --prompt "Inspect the running app and identify five interaction or hierarchy problems with screenshots as evidence."
Review:  scripts/ask_codex.py --review --base main
Worker:  scripts/ask_codex.py --role worker --prompt "Implement the scoped change in src/... and summarize the files changed."
UI worker: scripts/ask_codex.py --role worker --computer-use --prompt "Exercise the changed flow in the running app, fix issues within src/..., and summarize the evidence and files changed."
```

`codex exec --help`, `codex exec review --help`, and
`scripts/ask_codex.py --help` are the source of truth for flags and models.
Review mode takes a narrower flag set than plain `exec`.
