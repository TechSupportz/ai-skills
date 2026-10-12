---
name: codex-computer-use
description: Set up or repair Codex's computer use (cua_repl) as the "codex-cu" MCP server for Claude Code on macOS.
disable-model-invocation: true
---

# Codex computer use

Wire Codex's `cua_repl` into Claude Code as the user MCP server `codex-cu`, so Claude can drive native macOS apps in the background. Run it on a new Mac, or again after a Codex update stops `codex-cu` from connecting.

## 1. Install

Run `python3 -I scripts/install.py` from this skill's folder. It:

- copies `proxy.mjs` and `stop-hook.mjs` to `~/.claude/codex-cu/`;
- re-registers `codex-cu` with the newest `cua_repl` command, args and env, wrapped by the proxy;
- adds the Stop hook to `~/.claude/settings.json` once.

Completion: `claude mcp get codex-cu` reports `✔ Connected`.

## 2. Test

The `codex-cu` tools load only in a new session; ask the user to start one if they are missing. Then use the `js` tool: first call `let app = await cua.getApp("Calculator");` on its own, then type `12*12=` with `app.typeText` and read `app.getAXState()`.

Completion: the AX state shows `144` in Calculator's edit field.

## Reference

- **Proxy**: stamps every `tools/call` with `_meta["x-codex-turn-metadata"]` (`session_id`, `turn_id` as a JSON string); `cua_repl` rejects calls without it. It listens on `$TMPDIR/codex-cu-<uid>/<CLAUDE_PID>.sock`.
- **Stop hook**: pokes only its own session's socket; the proxy then calls the hidden `turn_ended` tool and starts a new `turn_id`.
- **Browsers are out of reach**: the Codex app rejects browser-use callers it did not launch (`untrusted-process-ancestry` in `~/Library/Logs/com.openai.codex/`), so browser calls hang. Use `codex-cu` for native apps and Claude in Chrome for the web.
