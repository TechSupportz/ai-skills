// stdio MCP proxy for Codex's cua_repl: node proxy.mjs <command> [args...]
// Adds _meta["x-codex-turn-metadata"] to every tools/call, and on a "turn_ended"
// poke from stop-hook.mjs calls the hidden turn_ended tool and starts a new turn.
import { spawn } from "node:child_process";
import { randomUUID } from "node:crypto";
import { mkdirSync, rmSync } from "node:fs";
import net from "node:net";
import os from "node:os";
import path from "node:path";

const [command, ...args] = process.argv.slice(2);
const claudePid = process.env.CLAUDE_PID || String(process.ppid);
const sessionId = process.env.CLAUDE_CODE_SESSION_ID || randomUUID();
let turnId = randomUUID();
let turnUsed = false;

const child = spawn(command, args, { stdio: ["pipe", "pipe", "inherit"] });
child.on("exit", (code) => process.exit(code ?? 1));

function lines(stream, onLine) {
  let buf = "";
  stream.on("data", (d) => {
    buf += d;
    let i;
    while ((i = buf.indexOf("\n")) >= 0) {
      const line = buf.slice(0, i);
      buf = buf.slice(i + 1);
      if (line.trim()) onLine(line);
    }
  });
}

// Claude -> server: stamp tools/call with turn metadata.
lines(process.stdin, (line) => {
  try {
    const msg = JSON.parse(line);
    if (msg.method === "tools/call") {
      msg.params ??= {};
      msg.params._meta = {
        ...msg.params._meta,
        "x-codex-turn-metadata": JSON.stringify({ session_id: sessionId, turn_id: turnId }),
      };
      turnUsed = true;
      line = JSON.stringify(msg);
    }
  } catch {}
  child.stdin.write(line + "\n");
});
process.stdin.on("end", () => child.stdin.end());

// Server -> Claude: pass through, except replies to the proxy's own requests.
const own = new Map();
let ownSeq = 0;
lines(child.stdout, (line) => {
  try {
    const msg = JSON.parse(line);
    if (!msg.method && own.has(msg.id)) {
      own.get(msg.id)(msg);
      own.delete(msg.id);
      return;
    }
  } catch {}
  process.stdout.write(line + "\n");
});

function endTurn() {
  const ended = turnId;
  const used = turnUsed;
  turnId = randomUUID();
  turnUsed = false;
  if (!used) return Promise.resolve();
  const id = `codex-cu-proxy-${++ownSeq}`;
  return new Promise((resolve) => {
    const timer = setTimeout(() => (own.delete(id), resolve()), 10000);
    own.set(id, () => (clearTimeout(timer), resolve()));
    child.stdin.write(JSON.stringify({
      jsonrpc: "2.0", id, method: "tools/call",
      params: { name: "turn_ended", arguments: { hook_event_name: "Stop", session_id: sessionId, turn_id: ended } },
    }) + "\n");
  });
}

// One socket per Claude process, so a Stop hook only reaches its own session.
const dir = path.join(os.tmpdir(), `codex-cu-${process.getuid()}`);
const sock = path.join(dir, `${claudePid}.sock`);
mkdirSync(dir, { recursive: true, mode: 0o700 });
rmSync(sock, { force: true });
net.createServer((conn) => {
  conn.once("data", async (d) => {
    if (d.toString().trim() === "turn_ended") await endTurn();
    conn.end("ok\n");
  });
}).listen(sock);

const cleanup = () => rmSync(sock, { force: true });
process.on("exit", cleanup);
for (const sig of ["SIGINT", "SIGTERM", "SIGHUP"]) process.on(sig, () => { child.kill(sig); process.exit(0); });
