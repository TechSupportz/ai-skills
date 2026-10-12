# codex-computer-use

Lets Claude Code use the computer-use engine that ships with the Codex app, so Claude can drive native macOS apps (Calculator, Finder, Notes, …) in the background without taking over your screen.

It registers Codex's `cua_repl` server as a Claude Code MCP server named `codex-cu`. A small proxy in front of it adds the Codex turn metadata that `cua_repl` expects, and a Stop hook tells it when each Claude turn ends.

## Requirements

- macOS with the Codex (ChatGPT) app installed and Computer Use enabled
- Claude Code

## Usage

Run `/codex-computer-use` in Claude Code, or run the installer directly:

```sh
python3 -I scripts/install.py
```

Start a new Claude Code session afterwards to load the `codex-cu` tools. Re-run the installer after a Codex update.

## What's inside

| File | Purpose |
| --- | --- |
| `scripts/install.py` | Registers `codex-cu` from the newest Codex plugin and adds the Stop hook |
| `scripts/proxy.mjs` | stdio proxy that adds `x-codex-turn-metadata` to tool calls |
| `scripts/stop-hook.mjs` | Stop hook that ends the current turn in this session's proxy |

## Limitation

Native apps only. The Codex app only accepts browser control from processes it launched itself, so browser calls through `codex-cu` hang. Use Claude in Chrome for browser work.
