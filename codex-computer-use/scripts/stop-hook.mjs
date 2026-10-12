// Stop hook: tell this Claude session's codex-cu proxy that the turn ended.
import net from "node:net";
import os from "node:os";
import path from "node:path";

const claudePid = process.env.CLAUDE_PID || String(process.ppid);
const sock = path.join(os.tmpdir(), `codex-cu-${process.getuid()}`, `${claudePid}.sock`);

const conn = net.connect(sock, () => conn.write("turn_ended\n"));
conn.on("data", () => conn.end());
conn.on("error", () => process.exit(0)); // no proxy in this session
setTimeout(() => process.exit(0), 12000).unref();
