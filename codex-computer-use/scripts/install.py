#!/usr/bin/env python3
"""Register Codex's cua_repl as the user MCP server "codex-cu" behind proxy.mjs,
and add the Stop hook that ends its turn. Safe to re-run after a Codex update."""
import json
import shutil
import subprocess
from pathlib import Path

HOME = Path.home()
CACHE = HOME / ".codex/plugins/cache/openai-bundled/unified-computer-use"
INSTALL = HOME / ".claude/codex-cu"
SETTINGS = HOME / ".claude/settings.json"
HERE = Path(__file__).resolve().parent


def newest_cua_repl():
    def version(p):
        return tuple(int(x) for x in p.name.split(".") if x.isdigit())
    versions = sorted((p for p in CACHE.iterdir() if (p / ".mcp.json").is_file()), key=version)
    if not versions:
        raise SystemExit(f"No unified-computer-use plugin under {CACHE}; enable Computer Use in the Codex app.")
    cfg = json.loads((versions[-1] / ".mcp.json").read_text())["mcpServers"]["cua_repl"]
    return versions[-1].name, cfg


def main():
    version, cfg = newest_cua_repl()

    INSTALL.mkdir(parents=True, exist_ok=True)
    for name in ("proxy.mjs", "stop-hook.mjs"):
        shutil.copy2(HERE / name, INSTALL / name)

    node = cfg["command"]
    server = {
        "type": "stdio",
        "command": node,
        "args": [str(INSTALL / "proxy.mjs"), node, *cfg["args"]],
        "env": cfg.get("env", {}),
    }
    subprocess.run(["claude", "mcp", "remove", "--scope", "user", "codex-cu"], capture_output=True)
    subprocess.run(["claude", "mcp", "add-json", "--scope", "user", "codex-cu", json.dumps(server)], check=True)

    settings = json.loads(SETTINGS.read_text()) if SETTINGS.exists() else {}
    stop = settings.setdefault("hooks", {}).setdefault("Stop", [])
    if not any("codex-cu/stop-hook.mjs" in h.get("command", "") for g in stop for h in g.get("hooks", [])):
        stop.append({"hooks": [{
            "type": "command",
            "command": f'{node} "$HOME/.claude/codex-cu/stop-hook.mjs"',
            "timeout": 15,
        }]})
        SETTINGS.write_text(json.dumps(settings, indent=2) + "\n")

    print(f"codex-cu registered from unified-computer-use {version}")


if __name__ == "__main__":
    main()
