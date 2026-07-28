#!/usr/bin/env node

import crypto from "node:crypto";
import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

function parseHistory(historyPath) {
  return fs
    .readFileSync(historyPath, "utf8")
    .split(/\n/)
    .filter((line) => line.trim() !== "")
    .map((line, index) => {
      try {
        return JSON.parse(line);
      } catch (error) {
        throw new Error(
          `Invalid history JSONL at line ${index + 1}: ${error.message}`,
        );
      }
    });
}

export function verifyDailyCompletion({ runDate, historyPath, outputRoot }) {
  if (!/^\d{4}-\d{2}-\d{2}$/.test(runDate ?? "")) {
    throw new Error(`Invalid run date: ${runDate}`);
  }

  const rows = parseHistory(historyPath);
  const deliveryDir = path.join(outputRoot, runDate, "top-5");
  const completion = rows
    .filter(
      (row) =>
        row.run_date === runDate &&
        row.record_type === "run_completion" &&
        row.state === "READY_FOR_REVIEW" &&
        Number.isInteger(row.selection_count) &&
        row.selection_count > 0,
    )
    .at(-1);

  if (!completion) {
    throw new Error(
      `No positive READY_FOR_REVIEW run_completion for ${runDate}`,
    );
  }

  const readyCandidates = rows.filter(
    (row) =>
      row.run_date === runDate &&
      row.candidate_id &&
      row.state === "READY_FOR_REVIEW",
  );
  if (readyCandidates.length < completion.selection_count) {
    throw new Error(
      `Only ${readyCandidates.length} READY_FOR_REVIEW candidate records ` +
        `for selection_count ${completion.selection_count}`,
    );
  }

  const candidateDirs = fs
    .readdirSync(deliveryDir, { withFileTypes: true })
    .filter((entry) => entry.isDirectory())
    .sort((left, right) => left.name.localeCompare(right.name));
  if (candidateDirs.length !== completion.selection_count) {
    throw new Error(
      `Expected ${completion.selection_count} candidate directories, ` +
        `found ${candidateDirs.length}`,
    );
  }

  const recordedHashes = completion.quality_verification?.final_asset_sha256;
  if (
    !recordedHashes ||
    typeof recordedHashes !== "object" ||
    Array.isArray(recordedHashes)
  ) {
    throw new Error("run_completion is missing final_asset_sha256");
  }

  const verifiedHashes = {};
  candidateDirs.forEach((entry, index) => {
    const directory = path.join(deliveryDir, entry.name);
    const files = fs.readdirSync(directory);
    if (files.length !== 1 || files[0] !== "post-translation.png") {
      throw new Error(`${directory} does not contain only post-translation.png`);
    }

    const digest = crypto
      .createHash("sha256")
      .update(fs.readFileSync(path.join(directory, files[0])))
      .digest("hex");
    const candidateNumber = String(index + 1).padStart(2, "0");
    if (recordedHashes[candidateNumber] !== digest) {
      throw new Error(`Hash mismatch for candidate ${candidateNumber}`);
    }
    verifiedHashes[candidateNumber] = digest;
  });

  return {
    run_date: runDate,
    verified_at: new Date().toISOString(),
    selection_count: completion.selection_count,
    run_completion_recorded_at: completion.recorded_at,
    delivery_dir: deliveryDir,
    final_asset_sha256: verifiedHashes,
  };
}

function parseCli(argv) {
  const options = {};
  for (let index = 0; index < argv.length; index += 2) {
    const flag = argv[index];
    const value = argv[index + 1];
    if (!value || !["--date", "--history", "--output-root"].includes(flag)) {
      throw new Error(
        "Usage: verify_daily_completion.mjs --date YYYY-MM-DD " +
          "--history PATH --output-root PATH",
      );
    }
    options[flag.slice(2)] = value;
  }
  if (!options.date || !options.history || !options["output-root"]) {
    throw new Error(
      "Usage: verify_daily_completion.mjs --date YYYY-MM-DD " +
        "--history PATH --output-root PATH",
    );
  }
  return options;
}

const isMain =
  process.argv[1] &&
  path.resolve(process.argv[1]) === fileURLToPath(import.meta.url);
if (isMain) {
  try {
    const options = parseCli(process.argv.slice(2));
    const result = verifyDailyCompletion({
      runDate: options.date,
      historyPath: options.history,
      outputRoot: options["output-root"],
    });
    process.stdout.write(`${JSON.stringify(result)}\n`);
  } catch (error) {
    process.stderr.write(`${error.message}\n`);
    process.exitCode = 1;
  }
}
