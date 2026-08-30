import assert from "node:assert/strict";
import crypto from "node:crypto";
import fs from "node:fs/promises";
import os from "node:os";
import path from "node:path";
import { spawn } from "node:child_process";
import test from "node:test";
import { fileURLToPath } from "node:url";

import { verifyDailyCompletion } from "./verify_daily_completion.mjs";

const guard = fileURLToPath(new URL("./daily_run_guard.sh", import.meta.url));
const runOnce = fileURLToPath(new URL("./daily_run_once.sh", import.meta.url));
const runDate = "2026-07-28";
const pngBytes = Buffer.from(
  "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mNk+A8AAQUBAScY42YAAAAASUVORK5CYII=",
  "base64",
);

async function fixture(t) {
  const root = await fs.mkdtemp(path.join(os.tmpdir(), "xic-daily-guard-test-"));
  t.after(async () => await fs.rm(root, { recursive: true, force: true }));
  const automationRoot = path.join(root, "automation");
  const outputRoot = path.join(root, "output");
  const historyPath = path.join(root, "history.jsonl");
  const assetDir = path.join(outputRoot, runDate, "top-5", "candidate-01");
  await fs.mkdir(assetDir, { recursive: true });
  await fs.writeFile(path.join(assetDir, "post-translation.png"), pngBytes);
  const digest = crypto.createHash("sha256").update(pngBytes).digest("hex");
  const rows = [
    {
      run_date: runDate,
      candidate_id: "candidate-01",
      state: "READY_FOR_REVIEW",
    },
    {
      run_date: runDate,
      record_type: "run_completion",
      state: "READY_FOR_REVIEW",
      selection_count: 1,
      recorded_at: `${runDate}T12:15:00+08:00`,
      quality_verification: { final_asset_sha256: { "01": digest } },
    },
  ];
  await fs.writeFile(
    historyPath,
    `${rows.map((row) => JSON.stringify(row)).join("\n")}\n`,
  );
  return { root, automationRoot, outputRoot, historyPath, assetDir };
}

async function runScript(script, args, paths) {
  return await new Promise((resolve, reject) => {
    const child = spawn(script, args, {
      env: {
        ...process.env,
        XIC_AUTOMATION_ROOT: paths.automationRoot,
        XIC_LOCK_ROOT: path.join(paths.root, "locks"),
        XIC_HISTORY_PATH: paths.historyPath,
        XIC_OUTPUT_ROOT: paths.outputRoot,
        XIC_NODE_BIN: process.execPath,
      },
      stdio: ["ignore", "pipe", "pipe"],
    });
    let stdout = "";
    let stderr = "";
    child.stdout.on("data", (chunk) => {
      stdout += chunk;
    });
    child.stderr.on("data", (chunk) => {
      stderr += chunk;
    });
    child.on("error", reject);
    child.on("close", (code) => resolve({ code, stdout, stderr }));
  });
}

async function runGuard(args, paths) {
  return await runScript(guard, args, paths);
}

test("completion verifier accepts an exact READY_FOR_REVIEW pack", async (t) => {
  const paths = await fixture(t);
  const result = verifyDailyCompletion({
    runDate,
    historyPath: paths.historyPath,
    outputRoot: paths.outputRoot,
  });
  assert.equal(result.selection_count, 1);
  assert.equal(result.delivery_dir, path.join(paths.outputRoot, runDate, "top-5"));
});

test("completion verifier rejects unexpected deliverable files", async (t) => {
  const paths = await fixture(t);
  await fs.writeFile(path.join(paths.assetDir, "caption.txt"), "not allowed");
  assert.throws(
    () =>
      verifyDailyCompletion({
        runDate,
        historyPath: paths.historyPath,
        outputRoot: paths.outputRoot,
      }),
    /does not contain only post-translation\.png/,
  );
});

test("guard serializes runs and persists only verified completion", async (t) => {
  const paths = await fixture(t);
  const first = await runGuard(["acquire", runDate], paths);
  const second = await runGuard(["acquire", runDate], paths);
  assert.equal(first.code, 0, first.stderr);
  assert.equal(first.stdout.trim(), "ACQUIRED");
  assert.equal(second.stdout.trim(), "BUSY");

  const complete = await runGuard(["mark-complete", runDate], paths);
  assert.equal(complete.code, 0, complete.stderr);
  assert.equal(complete.stdout.trim(), "COMPLETED");
  const finalAttempt = await runGuard(["acquire", runDate], paths);
  assert.equal(finalAttempt.stdout.trim(), "ALREADY_COMPLETE");

  const proof = JSON.parse(
    await fs.readFile(
      path.join(paths.automationRoot, "completions", `${runDate}.done`),
      "utf8",
    ),
  );
  assert.equal(proof.selection_count, 1);
});

test("run-once wrapper executes the command only before verified completion", async (t) => {
  const paths = await fixture(t);
  const counterPath = path.join(paths.root, "counter.txt");
  const command = [
    runDate,
    "--",
    process.execPath,
    "-e",
    "require('fs').appendFileSync(process.argv[1], 'run\\n')",
    counterPath,
  ];

  const first = await runScript(runOnce, command, paths);
  const second = await runScript(runOnce, command, paths);
  assert.equal(first.code, 0, first.stderr);
  assert.match(first.stdout, /COMPLETED/);
  assert.equal(second.code, 0, second.stderr);
  assert.equal(second.stdout.trim(), "ALREADY_COMPLETE");
  assert.equal(await fs.readFile(counterPath, "utf8"), "run\n");
});
