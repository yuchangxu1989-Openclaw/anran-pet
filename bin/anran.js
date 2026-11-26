#!/usr/bin/env node
"use strict";

const crypto = require("node:crypto");
const fs = require("node:fs");
const path = require("node:path");
const { spawn, spawnSync } = require("node:child_process");

function fail(message) {
  process.stderr.write(`anran: ${message}\n`);
  process.exit(1);
}

if (process.platform !== "darwin" || process.arch !== "arm64") {
  fail("this release supports macOS on Apple Silicon only");
}

const root = path.resolve(__dirname, "..");
let manifest;
try {
  manifest = JSON.parse(fs.readFileSync(path.join(root, "release-manifest.json"), "utf8"));
} catch (error) {
  fail(`cannot read the release manifest: ${error.message}`);
}
const pkg = require(path.join(root, "package.json"));
if (manifest.productVersion !== pkg.version || manifest.platform !== process.platform || manifest.arch !== process.arch) {
  fail("launcher and native runtime versions do not match");
}

function sha256(file) {
  return crypto.createHash("sha256").update(fs.readFileSync(file)).digest("hex");
}

const binary = path.join(root, "assets", "runtime", "anran");
try {
  if (sha256(binary) !== manifest.runtime.binarySHA256) fail("bundled native runtime hash mismatch");
  for (const [name, expected] of Object.entries(manifest.runtime.resources)) {
    if (!/^[\w.-]+$/.test(name)) fail("invalid native resource name");
    const resource = path.join(root, "assets", "runtime", "Resources", "anran-assets", name);
    if (sha256(resource) !== expected) fail(`native resource hash mismatch: ${name}`);
  }
} catch (error) {
  fail(error.message);
}

const args = process.argv.slice(2);
const command = args[0] || "help";
let executable = binary;
const forwardedArgs = [...args];
if (["install", "connect", "mcp"].includes(command)) {
  const hostIndex = args.indexOf("--host");
  const host = hostIndex >= 0 ? args[hostIndex + 1] : undefined;
  if (!["auto", "workbuddy", "vbuddy", "qwen", "doubao"].includes(host)) {
    fail("use --host auto, workbuddy, vbuddy, qwen or doubao");
  }
  if (["install", "connect"].includes(command) && process.env.ANRAN_INSTALL_ROOT && !args.includes("--install-root")) {
    forwardedArgs.push("--install-root", process.env.ANRAN_INSTALL_ROOT);
  }
}
if (command === "mcp") {
  const host = args[args.indexOf("--host") + 1];
  const installArgs = ["install", "--host", host, "--print"];
  if (process.env.ANRAN_INSTALL_ROOT) installArgs.push("--install-root", process.env.ANRAN_INSTALL_ROOT);
  const installed = spawnSync(binary, installArgs, {
    encoding: "utf8",
    maxBuffer: 4 * 1024 * 1024,
    env: process.env,
  });
  if (installed.status !== 0) {
    process.stderr.write(installed.stderr || installed.stdout || "native installation failed\n");
    process.exit(installed.status || 1);
  }
  try {
    const result = JSON.parse(installed.stdout);
    if (result.requiresKimi !== false || result.version !== pkg.version || result.binarySHA256 !== manifest.runtime.binarySHA256) {
      fail("installed native runtime readback does not match this package");
    }
    if (!result.executable || sha256(result.executable) !== manifest.runtime.binarySHA256) {
      fail("stable native executable hash mismatch");
    }
    executable = result.executable;
  } catch (error) {
    fail(`native installation readback failed: ${error.message}`);
  }
}

const child = spawn(executable, forwardedArgs, { stdio: "inherit", env: process.env });
for (const signal of ["SIGINT", "SIGTERM", "SIGHUP"]) {
  process.on(signal, () => { if (!child.killed) child.kill(signal); });
}
child.on("error", error => fail(error.message));
child.on("exit", (code, signal) => {
  if (signal) process.kill(process.pid, signal);
  else process.exit(code === null ? 1 : code);
});
