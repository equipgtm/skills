#!/usr/bin/env node
// Portable Studio client. Node 22+, no dependencies. Credentials stay outside the repository.
import { readFile, writeFile, mkdir, lstat, chmod, rm } from "node:fs/promises";
import { homedir } from "node:os";
import { resolve, join, basename, extname } from "node:path";
import { pathToFileURL } from "node:url";

export function apiUrl(origin, path) {
  const base = new URL(origin);
  if (
    base.protocol !== "https:" ||
    base.username ||
    base.password ||
    base.pathname !== "/" ||
    base.search ||
    base.hash
  )
    throw new Error("Use an HTTPS site origin, such as https://equipgtm.com.");
  if (
    !/^\/[A-Za-z0-9_-]/.test(path) ||
    /[\\#]/.test(path) ||
    /%(?:2e|2f|5c)/i.test(path) ||
    path.split(/[/?]/).includes("..")
  )
    throw new Error(
      "Use an API path such as /state, without /api or a hostname.",
    );
  const url = new URL("/api" + path, base);
  if (!url.pathname.startsWith("/api/")) throw new Error("Invalid API path.");
  return url;
}
export async function request(config, method, path, body, fetcher = fetch) {
  if (!["GET", "POST", "PUT", "PATCH", "DELETE"].includes(method))
    throw new Error("Unsupported HTTP method.");
  const response = await fetcher(apiUrl(config.origin, path), {
    method,
    redirect: "error",
    signal: AbortSignal.timeout(60000),
    headers: {
      Authorization: `Bearer ${config.token}`,
      "X-EquipGTM-Workspace": config.workspace,
      ...(body === undefined ? {} : { "Content-Type": "application/json" }),
    },
    ...(body === undefined ? {} : { body: JSON.stringify(body) }),
  });
  const data = await response.json();
  if (!response.ok)
    throw new Error(
      `${response.status}: ${data.error?.message ?? "Studio request failed."}`,
    );
  return data;
}
async function secretInput() {
  if (!process.stdin.isTTY) {
    let value = "";
    for await (const chunk of process.stdin) {
      value += chunk;
      if (value.length > 200) throw new Error("Invalid access token.");
    }
    return value.trim();
  }
  process.stderr.write("Paste temporary access token (hidden), then Enter: ");
  process.stdin.setRawMode(true);
  process.stdin.resume();
  process.stdin.setEncoding("utf8");
  return new Promise((resolveToken, reject) => {
    let value = "";
    const finish = (error) => {
      process.stdin.off("data", onData);
      process.stdin.setRawMode(false);
      process.stdin.pause();
      process.stderr.write("\n");
      if (error) reject(error);
      else resolveToken(value.trim());
    };
    const onData = (chunk) => {
      for (const char of chunk) {
        if (char === "\u0003") return finish(new Error("Cancelled."));
        if (char === "\r" || char === "\n") return finish();
        if (char === "\u007f" || char === "\b") value = value.slice(0, -1);
        else if (char >= " ") value += char;
        if (value.length > 200)
          return finish(new Error("Invalid access token."));
      }
    };
    process.stdin.on("data", onData);
  });
}
async function privateConfigPath() {
  const dir = join(homedir(), ".config", "equipgtm");
  await mkdir(dir, { recursive: true, mode: 0o700 });
  if ((await lstat(dir)).isSymbolicLink())
    throw new Error("Config directory must not be a symlink.");
  await chmod(dir, 0o700);
  const path = join(dir, "access.json");
  const info = await lstat(path).catch((error) => {
    if (error.code !== "ENOENT") throw error;
  });
  if (info && (!info.isFile() || info.isSymbolicLink()))
    throw new Error("Config must be a regular file.");
  if (info) await chmod(path, 0o600);
  return path;
}
export async function upload(
  config,
  workshopId,
  file,
  audience,
  fetcher = fetch,
) {
  if (!/^[A-Za-z0-9_-]+$/.test(workshopId))
    throw new Error("Invalid workshop ID.");
  if (!["learner", "instructor"].includes(audience))
    throw new Error("Choose learner or instructor audience.");
  const info = await lstat(file);
  if (!info.isFile() || info.size < 1 || info.size > 50 * 1024 * 1024)
    throw new Error("Upload a regular file between 1 byte and 50 MiB.");
  const types = {
    ".pptx":
      "application/vnd.openxmlformats-officedocument.presentationml.presentation",
    ".zip": "application/zip",
    ".pdf": "application/pdf",
    ".json": "application/json",
    ".ipynb": "application/json",
    ".md": "text/markdown",
    ".txt": "text/plain",
    ".py": "text/plain",
    ".js": "text/plain",
    ".ts": "text/plain",
    ".csv": "text/csv",
    ".png": "image/png",
    ".jpg": "image/jpeg",
    ".jpeg": "image/jpeg",
    ".webp": "image/webp",
  };
  const mimeType =
    types[extname(file).toLowerCase()] ?? "application/octet-stream";
  const state = await request(config, "GET", "/state", undefined, fetcher);
  const draft = state.workshops.find((item) => item.id === workshopId);
  if (!draft) throw new Error("Workshop not found in this workspace.");
  const grant = await request(
    config,
    "POST",
    `/workshops/${workshopId}/uploads`,
    { name: basename(file), mimeType, audience, size: info.size },
    fetcher,
  );
  const target = new URL(grant.uploadUrl);
  if (
    target.protocol !== "https:" ||
    target.username ||
    target.password ||
    !target.hostname.endsWith(".amazonaws.com")
  )
    throw new Error("Unexpected storage upload destination.");
  // The workspace bearer is never sent to storage. Only the signed URL authorizes this upload.
  const put = await fetcher(target, {
    method: "PUT",
    redirect: "error",
    headers: grant.headers,
    body: await readFile(file),
    signal: AbortSignal.timeout(120000),
  });
  if (!put.ok) throw new Error(`Storage upload failed (${put.status}).`);
  return request(
    config,
    "POST",
    `/workshops/${workshopId}/uploads/${grant.uploadId}/finalize`,
    { expectedUpdatedAt: draft.updatedAt },
    fetcher,
  );
}
export async function main(args = process.argv.slice(2)) {
  const command = args.shift();
  if (!command || ["help", "--help", "-h"].includes(command)) {
    console.log(
      `EquipGTM Studio CLI (Node 22+)\n\nlogin --workspace ID [--origin https://equipgtm.com]\n  Enter temporary access from Studio in your terminal. Never pass it as an argument.\nrequest GET /state\nrequest POST /workshops --file draft-request.json\nrequest PUT /workshops/ID --file update-request.json\nupload WORKSHOP_ID FILE learner|instructor\nrequest GET /sessions/SESSION_ID/results\nlogout\n\nCredentials: ~/.config/equipgtm/access.json (owner-only). Login replaces the active workspace.\nAccess expires within an hour or on website sign-out. Revoke it in Studio to end it early.`,
    );
    return;
  }
  const option = (name) => {
    const i = args.indexOf(name);
    return i < 0 ? undefined : args[i + 1];
  };
  if (!["login", "logout", "request", "upload"].includes(command))
    throw new Error("Unknown command. Use --help.");
  const configPath = await privateConfigPath();
  if (command === "logout") {
    await rm(configPath, { force: true });
    console.log(
      "Local access removed. Revoke temporary access in Studio to invalidate other copies.",
    );
    return;
  }
  if (command === "login") {
    const workspace = option("--workspace");
    const origin = option("--origin") ?? "https://equipgtm.com";
    if (!workspace || !/^[A-Za-z0-9_-]{1,80}$/.test(workspace))
      throw new Error("Provide --workspace with the ID shown in Studio.");
    apiUrl(origin, "/state");
    const token = await secretInput();
    if (!/^egtm_[A-Za-z0-9_-]{43}$/.test(token))
      throw new Error("Invalid access token.");
    const config = { origin, workspace, token };
    await request(config, "GET", "/state");
    await writeFile(configPath, JSON.stringify(config), { mode: 0o600 });
    console.log(
      `Connected to workspace ${workspace}. Temporary access saved outside your repository.`,
    );
    return;
  }
  const config = JSON.parse(
    await readFile(configPath, "utf8").catch(() => {
      throw new Error("Run login first. Create temporary access in Studio.");
    }),
  );
  let result;
  if (command === "upload")
    result = await upload(config, args[0], resolve(args[1] ?? ""), args[2]);
  else {
    const file = option("--file");
    const body = file
      ? JSON.parse(await readFile(resolve(file), "utf8"))
      : undefined;
    result = await request(config, args[0], args[1], body);
  }
  console.log(JSON.stringify(result, null, 2));
}
if (
  process.argv[1] &&
  import.meta.url === pathToFileURL(resolve(process.argv[1])).href
) {
  main().catch((error) => {
    console.error(error.message);
    process.exitCode = 1;
  });
}
